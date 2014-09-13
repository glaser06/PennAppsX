import rumps, os, time, config, match
from twilio.rest import TwilioRestClient
import gSpeechAPI as g
import sys
import subprocess
from threading import Thread
from multiprocessing import Process, Value, Lock

r = g.Recognizer()
m = g.Microphone()
account_sid = "AC5a6f9167012e477ce85ae5711fe77466"
auth_token = "c983fea53652eae6595517171700e871"
client = TwilioRestClient(account_sid, auth_token)
annoyanceCounter = 0

def set_volume(volume):
    subprocess.call(['osascript', '-e', 'set volume output volume '+str(volume)])

def get_volume():
    ovol = int(subprocess.check_output(['osascript', '-e', 'set ovol to output volume of (get volume settings)']))
    return ovol

def checkName(audio, lock, v):
    #print("Called checkName")
    try:
        list = r.recognize(audio, True)
        for prediction in list:
            if(match.checkArray(prediction["text"], config.name, 0.5)):
                with lock:
                    v.value += 1
                if(v.value >= 1):
                    rumps.notification("Pay attention!", "Someone said your name!", "Dumbass!")
                if(v.value >= 2):
                    message = client.messages.create(body="Pay some fucking attention to the people around you!",
                    to="+18583822455",
                    from_="+17606704339")
                if(v.value >= 3):
                    set_volume(get_volume()/4)
                break
            #print(prediction["text"])
    except LookupError:
        print("Nothing said!")

if __name__ == "__main__":
    v = Value('i', 0)
    lock = Lock()
    while True:
        with m as source:
            audio = r.record(source)
        t = Thread(target = checkName, args=(audio, lock, v))
        t.setDaemon(True)
        t.start()
