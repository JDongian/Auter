from cmd import (
    WaitCmd, GoToCmd,
    MouseClickCmd,
    KeyPressCmd, KeyPressDownCmd, KeyPressUpCmd)
from pymouse import PyMouse
from pykeyboard import PyKeyboard


def parse_lines(lines):
    """Read lines as plaintext and parse the commands and arguments.
    """
    m = PyMouse()
    k = PyKeyboard()
    for line in lines:
        line = line.strip()
        if not line or line[0] in {'#', ';'}:
            continue  # skip empty lines
        cmd, *args = line.split()
        cmd = cmd.lower()
        if cmd == "wait":
            assert len(args) == 1
            t, = args
            t = float(t)
            yield WaitCmd(delay=t)
        elif cmd == "goto":
            assert len(args) == 1
            lbl, = args
            lbl = int(lbl)
            yield GoToCmd(label=lbl)
        elif cmd == "click":
            assert 3 <= len(args) <= 4
            btn, x, y, *dur = args
            btn = int(btn)
            x, y = int(x), int(y)
            if dur == []:
                kwargs = dict()
            else:
                kwargs = {'duration': float(dur[0])}
            yield MouseClickCmd(m=m, button=btn, x=x, y=y, **kwargs)
        elif cmd == "press":
            assert len(args) <= 2
            code, *dur = args
            code = int(code)
            if dur == []:
                kwargs = dict()
            else:
                kwargs = {'duration': float(dur[0])}
            yield KeyPressCmd(k=k, code=code, **kwargs)
        elif cmd == "press_down":
            assert len(args) == 1
            code, = args
            code = int(code)
            yield KeyPressDownCmd(k=k, code=code)
        elif cmd == "press_up":
            assert len(args) == 1
            code, = args
            code = int(code)
            yield KeyPressUpCmd(k=k, code=code)


def parse_file(filename):
    with open(filename, 'r') as fp:
        for command in parse_lines(fp):
            yield command
