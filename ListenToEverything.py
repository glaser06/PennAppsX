#!/usr/bin/python

# open a microphone in pyAudio and listen for taps

import pyaudio
import audioop
import struct
import sys
import subprocess
import time
from multiprocessing import Process

import numpy as np
import pylab as pl

FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
TIME_FUZZ_FACTOR = 1.5
RMS_SAMPLE_RATE = 100 # in blocks
AMP_FUZZ_FACTOR = 600

def print_usage():
    print "usage %s <rms_sample_rate> <amp_fuzz_factor>" % sys.argv[0]
    print "    Where rms_sample_rate is the number of blocks to look at to determine ambient noise level"
    print "    and   amp_fuzz_factor is the noise level over ambient to drop system volume at"
    print "    Units are fucked up. 100 and 100 respectively are good starting points"

def set_volume(volume):
    subprocess.call(['osascript', '-e', 'set volume output volume '+str(volume)])

def get_volume():
    ovol = int(subprocess.check_output(['osascript', '-e', 'set ovol to output volume of (get volume settings)']))
    return ovol

def get_rms(block):
    return audioop.rms(block, 2)

class SoundMonitor(object):
    def __init__(self):
        self.amp_threshold = 0
        self.normal_volume = get_volume()
        self.reset=False
        self.errorcount = 0
        self.fuzz_time = 0
        self.rms_blocks = ""
        RMS_SAMPLE_RATE = sys.argv[1]            
        AMP_FUZZ_FACTOR = sys.argv[2]

        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
    
    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        return stream

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # dammit.
            if e[1] == pyaudio.paInputOverflowed:
                self.errorcount += 1
                #print( "(%d) XRUN: %s"%(self.errorcount,e) )
            return
        
        self.rms_blocks += block
        if len(self.rms_blocks) > INPUT_FRAMES_PER_BLOCK*RMS_SAMPLE_RATE*4:
            self.rms_blocks = self.rms_blocks[INPUT_FRAMES_PER_BLOCK*4:]
        self.amp_threshold = get_rms(self.rms_blocks) + AMP_FUZZ_FACTOR

        amplitude = get_rms( block )
        if amplitude > self.amp_threshold:
            print('#'*int(amplitude/100), amplitude, 'Talking!' )
            set_volume(self.normal_volume/4)
            self.reset = True
            self.fuzz_time = time.time()+TIME_FUZZ_FACTOR
        elif self.fuzz_time - time.time() > 0:
            pass
        elif self.reset:
            set_volume(self.normal_volume)
            self.reset = False
        else:
            print( '#'*int(self.amp_threshold/100), self.amp_threshold )
            self.normal_volume = get_volume()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    sm = SoundMonitor()
    while True:
        sm.listen()
