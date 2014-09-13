import io, os, subprocess, wave
import math, audioop, collections
import json

from urllib2 import Request, urlopen

class AudioSource:
    def __init__(self):
        raise NotImplementedError("Abstract Class")
    def __enter__(self):
        raise NotImplementedError("Abstract Class")
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError("Abstract Class")

try:
    import pyaudio
    class Microphone(AudioSource):
        def __init__(self, device_index = None):
            self.device_index = device_index
            self.format = pyaudio.paInt16
            self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
            self.RATE = 44100
            self.CHANNELS = 1
            self.CHUNK = 2205

            self.audio = None
            self.stream = None

        def __enter__(self):
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                input_device_index = self.device_index,
                format = self.format, 
                rate = self.RATE, 
                channels = self.CHANNELS, 
                frames_per_buffer = self.CHUNK,
                input = True,
            )
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            self.audio.terminate()
except ImportError:
    pass
    
class WavFile(AudioSource):
    def __init__(self, filename_or_fileobject):
        if isinstance(filename_or_fileobject, str):
            self.filename = filename_or_fileobject
        else:
            self.filename = None
            self.wav_file = filename_or_fileobject
        self.stream = None

    def __enter__(self):
        if self.filename: self.wav_file = open(self.filename, "rb")
        self.wav_reader = wave.open(self.wav_file, "rb")
        self.SAMPLE_WIDTH = self.wav_reader.getsampwidth()
        self.RATE = self.wav_reader.getframerate()
        self.CHANNELS = self.wav_reader.getnchannels()
        assert self.CHANNELS == 1
        self.CHUNK = 4096
        self.stream = WavFile.WavStream(self.wav_reader)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.filename: self.wav_file.close()
        self.stream = None

    class WavStream(object):
        def __init__(self, wav_reader):
            self.wav_reader = wav_reader

        def read(self, size = -1):
            if size == -1:
                return self.wav_reader.readframes(self.wav_reader.getnframes())
            return self.wav_reader.readframes(size)

    
class AudioData(object):
    def __init__(self, rate, data):
        self.rate = rate
        self.data = data

class Recognizer(AudioSource):
    def __init__(self, language="en-US", key="AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"):
        self.key = key
        self.language = language
        
        self.energy_threshold = 100
        self.pause_threshold = 0.2
        self.quiet_duration = 0.2
        
    def samp2flac(self, source, frame_data):
        import platform, os
        with io.BytesIO() as wav_file:
            wavWriter = wave.open(wav_file, "wb")
            try:
                wavWriter.setsampwidth(source.SAMPLE_WIDTH)
                wavWriter.setnchannels(source.CHANNELS)
                wavWriter.setframerate(source.RATE)
                wavWriter.writeframes(frame_data)
            finally:
                wavWriter.close()
            wav_data = wav_file.getvalue()
        system = platform.system()
        path = os.path.dirname(os.path.abspath(__file__))
        flacConverter = shExists("flac")
        cmd = subprocess.Popen("/usr/local/bin/flac --stdout --totally-silent --best -", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        flacData, stderr = cmd.communicate(wav_data)
        return flacData

    def record(self, source, duration = 2):
        assert isinstance(source, AudioSource) and source.stream

        frames = io.BytesIO()
        seconds_per_buffer = (source.CHUNK + 0.0) / source.RATE
        elapsed_time = 0
        while True:
            elapsed_time += seconds_per_buffer
            if duration and elapsed_time > duration: break

            buffer = source.stream.read(source.CHUNK)
            if len(buffer) == 0: break
            frames.write(buffer)

        frameData = frames.getvalue()
        frames.close()
        return AudioData(source.RATE, self.samp2flac(source, frameData))

    def listen(self, source, timeout = None):
        assert isinstance(source, AudioSource) and source.stream

        frames = collections.deque()
        assert self.pause_threshold >= self.quiet_duration >= 0
        seconds_per_buffer = (source.CHUNK + 0.0) / source.RATE
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer))
        quiet_buffer_count = int(math.ceil(self.quiet_duration / seconds_per_buffer))
        elapsed_time = 0

        while True:
            elapsed_time += seconds_per_buffer
            if timeout and elapsed_time > timeout: 
                raise TimeoutError("listening timed out")

            buffer = source.stream.read(source.CHUNK)
            if len(buffer) == 0: break
            frames.append(buffer)

            energy = audioop.rms(buffer, source.SAMPLE_WIDTH)
            if energy > self.energy_threshold:
                break
            if len(frames) > quiet_buffer_count: 
                frames.popleft()
        pause_count = 0
        while True:
            buffer = source.stream.read(source.CHUNK)
            if len(buffer) == 0: break 
            frames.append(buffer)

            energy = audioop.rms(buffer, source.SAMPLE_WIDTH)
            if energy > self.energy_threshold:
                pause_count = 0
            else:
                pause_count += 1
            if pause_count > pause_buffer_count:
                break

        for i in range(quiet_buffer_count, pause_buffer_count): frames.pop()
        frame_data = b"".join(list(frames))

        return AudioData(source.RATE, self.samp2flac(source, frame_data))
        
    def recognize(self, audio_data, show_all = False):
        assert isinstance(audio_data, AudioData)

        url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=%s&key=%s" % (self.language, self.key)
        self.request = Request(url, data = audio_data.data, headers = {"Content-Type": "audio/x-flac; rate=%s" % audio_data.rate})
        try:
            response = urlopen(self.request)
        except:
            raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")
        response_text = response.read().decode("utf-8")

        actual_result = []
        for line in response_text.split("\n"):
            if not line: continue
            result = json.loads(line)["result"]
            if len(result) != 0:
                actual_result = result[0]

        if "alternative" not in actual_result:
            raise LookupError("Speech is unintelligible")

        if not show_all:
            for prediction in actual_result["alternative"]:
                if "confidence" in prediction:
                    return prediction["transcript"]
            raise LookupError("Speech is unintelligible")

        spoken_text = []

        default_confidence = 0
        if len(actual_result["alternative"])==1: default_confidence = 1

        for prediction in actual_result["alternative"]:
            if "confidence" in prediction:
                spoken_text.append({"text":prediction["transcript"],"confidence":prediction["confidence"]})
            else:
                spoken_text.append({"text":prediction["transcript"],"confidence":default_confidence})
        return spoken_text
                
def shExists(pgm):
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
        
