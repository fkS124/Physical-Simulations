from src.app import App
from math import pi
import sys


if __name__ == "__main__":

    val = {
        'k' : 13,
        'm' : 7,
        'dm' : 2,
        'a1' : pi/2,
        'a2' : 2*pi/3
    }

    for arg in sys.argv:
        sp = arg.split("=")
        if len(sp) >= 2:
            if sp[0] in val:
                val[sp[0]] = eval(sp[1])

    App(*[val[item] for item in val]).run()