import rumps, os, time, config, match
import gSpeechAPI as g
from threading import Thread

def checkName():
    r = g.Recognizer()
    m = g.Microphone()
    while True:
        with m as source:
            audio = r.listen(source)
    
        try:
            list = r.recognize(audio,True)
            for prediction in list:
                print(prediction["text"])
                if(match.checkArray(prediction["text"],config.name,0.5)):
                    rumps.notification("Pay attention!", "Someone said your name!", "Dumbass!")
                    os.system("osascript -e 'set Volume 0'")
                    time.sleep(10000)
                    os.system("osascript -e 'set Volume 4'")
                print(prediction["text"])
        except LookupError:
            print("Nothing said!")

class MusicNotifApp(rumps.App):
    def __init__(self):
        super(MusicNotifApp, self).__init__("MusicListener")
        self.menu = ["Preferences"]
        t1 = Thread(target = checkName)
        t1.setDaemon(True)
        t1.start()

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("Edit name in "+os.path.dirname(os.path.realpath(__file__))+"/config.py")

if __name__ == "__main__":
    MusicNotifApp().run()
    


