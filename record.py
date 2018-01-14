from pymouse import PyMouseEvent
from pykeyboard import PyKeyboardEvent
import time


LAST_TIME = time.time()


def print_wait():
    global LAST_TIME
    dt = round(time.time() - LAST_TIME, 3)
    print("wait {dt}".format(dt=dt))
    LAST_TIME = time.time()

def update_wait():
    global LAST_TIME
    LAST_TIME = time.time()


class KbListener(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.state = 1  # is_running?

    def tap(self, keycode, character, press):
        # Exit if 'Esc' is pressed.
        if character == 'q':
            self.state = 0
            self.stop()

        if press:
            print_wait()
            self.ts = time.time()
            ts = round(time.time() % 1000, 1)
            print("# {t}: [({char})".format(t=ts, char=character))
            print("press {code}".format(code=keycode))
        else:
            dt = time.time() - self.ts
            update_wait()
            print("# dt={dt} ({char})]".format(dt=dt, char=character))


class MsListener(PyMouseEvent):
    def __init__(self):
        self.state = 1
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        # Exit if middle mouse button is pressed.
        if button == 3:
            self.state = 0
            self.stop()
        if press:
            print_wait()
            self.ts = time.time()
            print("# {t}: [".format(t=round(time.time() % 1000, 1)))
            print("click {btn} {x} {y}".format(btn=button, x=x, y=y))
        else:
            dt = time.time() - self.ts
            update_wait()
            print("# dt={dt}]".format(dt=dt))


if __name__ == "__main__":
    m = MsListener()
    k = KbListener()
    m.start()
    k.start()
    while 1:
        time.sleep(0.05)
        if k.state == 0 or m.state == 0:
            break
