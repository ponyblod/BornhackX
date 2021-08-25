from evdev import InputDevice, categorize, ecodes
from threading import Thread
import vlc 


class Dreamcake():
    """ 
        Give an mp3 file and an input event device.
        Play sound (can stack the sound) :^)
    """
    def __init__(self, mp3, event_device):
        self.device = InputDevice(event_device)
        self.mp3 = mp3

    def start(self):
        self.listen_for_key(self.device, self.mp3) 

    def play_something_thread(self, mp3):
        print('Playing')
        vlc.MediaPlayer(mp3).play()

    def listen_for_key(self, device, mp3): 
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)

                if key_event.keystate == 1: # 0 == Up, 1 == Down, 2 == Hold
                    print('Down')
                    Thread(target=self.play_something_thread, args=(mp3,)).start()


if __name__ == '__main__':
    cake = Dreamcake('gobwah.mp3', '/dev/input/event0')
    cake.start()
