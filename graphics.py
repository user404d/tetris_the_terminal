import sys
from collections import namedtuple

ESC = '\x1b'
CSI = ESC + '['


Pixel = namedtuple('Pixel', ('char', 'fore', 'back'))


class Screen(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Pixel(' ', 7, 0) for _ in range(self.width)] for _ in range(self.height)]

    def get_string(self, xoff=0, yoff=0):
        parts = []
        cb = 0
        cf = 7
        for y, row in enumerate(self.pixels):
            parts += [setxy(xoff+1, yoff+1 + y)]
            for c, f, b in row:
                if b != cb:
                    parts += [xback(b)]
                    cb = b
                if f != cf:
                    parts += [xfore(f)]
                    cf = f
                parts += [c]
        return ''.join(parts)

    def draw(self, xoff=0, yoff=0):
        sys.stdout.write(self.get_string(xoff, yoff))

    def paint_border(self):
        mx = self.width-1
        my = self.height-1
        for y in range(self.height):
            self.pixels[y][0] = Pixel('|', 7, 0)
            self.pixels[y][mx] = Pixel('|', 7, 0)
        for x in range(self.width):
            self.pixels[0][x] = Pixel('=', 7, 0)
            self.pixels[my][x] = Pixel('=', 7, 0)
        for x, y in [(0, 0), (mx, 0), (0, my), (mx, my)]:
            self.pixels[y][x] = Pixel('#', 7, 0)



def SGR(code):
    return CSI + code + 'm'

COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

def fore(color):
    return SGR(str(30 + COLORS.index(color)))

def back(color):
    return SGR(str(40 + COLORS.index(color)))

def xfore(color):
    return SGR('38;5;' + str(color))

def xback(color):
    return SGR('48;5;' + str(color))

def setxy(x, y):
    return CSI + str(y) + ';' + str(x) + 'H'
    #return CSI + str(y) + ';' + str(x) + 'f'

