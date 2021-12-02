from pynput import keyboard
import time
class a():
    def on_key_release(self, key): #what to do on key-release
        time_taken = round(time.time() - self._t, 2) #rounding the long decimal float
        print("The key",key," is pressed for",time_taken,'seconds')
        return False #stop detecting more key-releases

    def on_key_press(self, key): #what to do on key-press
        return False #stop detecting more key-presses

    def run(self):
        with keyboard.Listener(on_press = self.on_key_press) as press_listener: #setting code for listening key-press
            print("joining")
            press_listener.join()

        self._t = time.time() #reading time in sec

        with keyboard.Listener(on_release = self.on_key_release) as release_listener: #setting code for listening key-release
            release_listener.join()

a = a()
a.run()