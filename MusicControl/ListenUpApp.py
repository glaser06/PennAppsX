import rumps
import ListenToEverything
import MusicNotifApp
import config
import threading

class ListenUpApp(rumps.App):
    def __init__(self):
        super(ListenUpApp, self).__init__("ListenUP!")
        self.menu = ["Alert on Name", "Duck Audio on Speaking", "Configure Name", "Configure Audio Ducking"]
        self.rms_sample_rate = 100
        self.amp_fuzz_factor = 1500
        self.sm = ListenToEverything.SoundMonitor(self.rms_sample_rate, self.amp_fuzz_factor)
        self.icon = 'icon.png'

    @rumps.clicked("Alert on Name")
    def alert_on_name(self, sender):
        sender.state = not sender.state
        if (sender.state):
            f = open('.name')
            name = f.read().split(',')[0]
            f.close()
            t = threading.Thread(target=MusicNotifApp.run, args=(name,))
            t.start()
        else:
            MusicNotifApp.kill()

    @rumps.clicked("Duck Audio on Speaking")
    def duck_on_speaking(self, sender):
        sender.state = not sender.state
        if (sender.state):
            t = threading.Thread(target=self.sm.loop)
            t.daemon = True
            t.start()
        else:
            self.sm.kill()

    @rumps.clicked("Configure Name")
    def configure_name(self, _):
        config.run()

    @rumps.clicked("Configure Audio Ducking")
    def configure_ducking(self, _):
        window = rumps.Window(title='configure ambient noise sample rate', dimensions=(100,20))
        self.sm.set_rms_sample_rate(int(window.run().text))
        window = rumps.Window(title='configure amplitude threshold', dimensions=(100,20))
        self.sm.set_amp_fuzz_factor(int(window.run().text))

if __name__ == "__main__":
    ListenUpApp().run()
