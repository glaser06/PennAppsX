import rumps, os, time, config, match
from twilio.rest import TwilioRestClient
import gSpeechAPI as g
import sys
import subprocess
from threading import Thread
from multiprocessing import Process, Value, Lock

def genNames():
    #global name
    r = g.Recognizer()
    m = g.Microphone()
    strng = ""
    with m as source:
        audio = r.record(source)
    list = r.recognize(audio, True)
    for prediction in list:
        print prediction["text"]
    textlist = [a["text"] for a in list]
    strng = ",".join(textlist)
    return strng.replace(" ", "")

def run():
    f = open('.name', 'w')
    names = genNames()
    f.write(names)

if __name__ == "__main__":
    run()
