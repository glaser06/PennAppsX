import gSpeechAPI as g
import os
import time

r = g.Recognizer()
m = g.Microphone()

while True:
    with m as source:
        audio = r.listen(source)
    
    try:
        list = r.recognize(audio,True)
        for prediction in list:
            if(prediction["text"] == "Yusuf"):
                os.system("osascript -e 'set Volume 0'")
                time.sleep(10000)
                os.system("osascript -e 'set Volume 4'")
            print(prediction["text"])
    except LookupError:
        print("Nothing said!")