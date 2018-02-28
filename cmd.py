import time
import logging


class Cmd():
    def __init__(self):
        pass

    def log(self):
        ts = time.strftime("%H:%M:%S", time.gmtime())
        logging.info("{ts} {cmd}".format(ts=ts, cmd=self))

    def execute(self, *args):
        raise NotImplementedError


class WaitCmd(Cmd):
    def __init__(self, delay):
        self.delay = delay

    def execute(self, *args):
        self.log()
        time.sleep(self.delay)


class GoToCmd(Cmd):
    def __init__(self, label):
        self.label = label

    def execute(self, ip, *args):
        self.log()
        ip[0] = self.label - 1  # set instruction pointer


class MouseClickCmd(Cmd):
    def __init__(self, m, button, x, y, duration=0.05):
        self.m = m  # pymouse
        self.button = button
        self.x, self.y = x, y
        self.duration = duration

    def execute(self, *args):
        self.log()
        self.m.press(self.x, self.y, self.button)
        time.sleep(self.duration)
        self.m.release(self.x, self.y, self.button)


class KeyPressCmd(Cmd):
    def __init__(self, k, code, duration=0.05):
        self.k = k  # pykeyboard
        self.code = code
        self.duration = duration

    def execute(self, *args):
        self.log()
        self.k.press_key(self.code)
        time.sleep(self.duration)
        self.k.release_key(self.code)


class KeyPressDownCmd(Cmd):
    def __init__(self, k, code):
        self.k = k  # pykeyboard
        self.code = code

    def execute(self, *args):
        self.log()
        self.k.press_key(self.code)


class KeyPressUpCmd(Cmd):
    def __init__(self, k, code):
        self.k = k  # pykeyboard
        self.code = code

    def execute(self, *args):
        self.log()
        self.k.release_key(self.code)
