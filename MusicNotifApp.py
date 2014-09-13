import rumps, os, time, config, match
from twilio.rest import TwilioRestClient
import gSpeechAPI as g
from threading import Thread
from multiprocessing import Process, Value, Lock

r = g.Recognizer()
m = g.Microphone()
account_sid = "AC5a6f9167012e477ce85ae5711fe77466"
auth_token = "c983fea53652eae6595517171700e871"
client = TwilioRestClient(account_sid, auth_token)
annoyanceCounter = 0

def checkName(audio, lock, v):
    print("Called checkName")
    try:
        list = r.recognize(audio, True)
        for prediction in list:
            #print(prediction["text"])
            if(match.checkArray(prediction["text"], config.name, 0.5)):
                #global annoyanceCounter
                with lock:
                    v = v + 1
                if(v == 1):
                    rumps.notification("Pay attention!", "Someone said your name!", "Dumbass!")
                elif(v == 2):
                    message = client.messages.create(body="Pay some fucking attention to the people around you!",
                    to="+18583822455",
                    from_="+17606704339")
                elif(annoyanceCounter == 3):
                    os.system("osascript -e 'set Volume 0'")
            print(prediction["text"])
    except LookupError:
        print("Nothing said!")

class MusicNotifApp(rumps.App):
    def __init__(self):
        super(MusicNotifApp, self).__init__("MusicListener")
        self.menu = ["Preferences"]
        v = Value('i', 0)
        lock = Lock()
        while True:
            with m as source:
                audio = r.listen(source)
            t = Thread(target = checkName, args=(audio, lock, v))
            t.setDaemon(True)
            t.start()

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("Edit name in "+os.path.dirname(os.path.realpath(__file__))+"/config.py")

if __name__ == "__main__":
    MusicNotifApp().run()
