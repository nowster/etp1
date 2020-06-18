# Uses the Python Imaging Library
# apt-get install python3-pil, or pip/pip3 install Pillow
import PIL.Image
import PIL.ImageColor
import PIL.ImageFilter
from math import pi, sin

# _ is black
# ] is grey block with no border on left
# [ is grey block with no border on right
# = is grey block with no border on left or right
# x is grey block with white borders all round
# | is pulse
# 1=1.5Mhz, 2=2.5MHz, 3=3.5MHz, 4=4.0MHz, 5=4.5MHz, 6=5.25MHz
# a=20% b=40% c=60% d=80% luminance
# g is 75%

# Each block is 48x32 => 768x576 (16x16 basis, except for gratings)

grid = [
    "W_C_C_C__C_C_C_W",
    "_]xxxxxxxxxxxx[_",
    "R]xx[YYRRYY]xx[Y",
    "_=WWWW|___WWWW=Y",
    "R=WWWW|___WWWW=_",
    "_=_g_g_g_g_g_g=W",
    "R=YYCCGGMMRRBB=W",
    "R=YYCCGGMMRRBB=_",
    "_]xxxxxxxxxxxx[_",
    "_]xxxxxxxxxxxx[_",
    "B]112233445566[_",
    "B]112233445566[W",
    "_=__aabbccddWW=W",
    "B=__aabbccddWW=_",
    "_]xxx[BBBB]xxx[Y",
    "B]xxx[BBBB]xxx[Y",
    "_]xxxxxxxxxxxx[_",
    "W_G_G_G__G_G_G_W",
]

white = PIL.ImageColor.getrgb("hsb(0,0%,100%)")
black = PIL.ImageColor.getrgb("hsb(0,0%,0%)")
grey50 = PIL.ImageColor.getrgb("hsb(0,0%,50%)")
grey75 = PIL.ImageColor.getrgb("hsb(0,0%,75%)")

grey20 = PIL.ImageColor.getrgb("hsb(0,0%,20%)")
grey40 = PIL.ImageColor.getrgb("hsb(0,0%,40%)")
grey60 = PIL.ImageColor.getrgb("hsb(0,0%,60%)")
grey80 = PIL.ImageColor.getrgb("hsb(0,0%,80%)")

red = PIL.ImageColor.getrgb("hsb(0,100%,75%)")
yellow = PIL.ImageColor.getrgb("hsb(60,100%,75%)")
green = PIL.ImageColor.getrgb("hsb(120,100%,75%)")
cyan = PIL.ImageColor.getrgb("hsb(180,100%,75%)")
blue = PIL.ImageColor.getrgb("hsb(240,100%,75%)")
magenta = PIL.ImageColor.getrgb("hsb(300,100%,75%)")


def make_colour(colour):
    return [[colour for _ in range(16)] for _ in range(16)]


def make_grid(left=True, right=True):
    grid = []

    grid.append([white for _ in range(48)])
    for _ in range(14):
        line = []
        if left:
            line.append(white)
            line.append(white)
        else:
            line.append(grey50)
            line.append(grey50)
        line.extend([grey50 for _ in range(44)])
        if right:
            line.append(white)
            line.append(white)
        else:
            line.append(grey50)
            line.append(grey50)
        grid.append(line)

    grid.append([white for _ in range(48)])
    return grid


def make_pulse():
    line = []
    for i in range(16):
        if i in [7]:
            line.append(white)
        else:
            line.append(black)
    return [line for _ in range(16)]


def make_grating(frequency, offset=0):
    base = 1 / 15
    line = []
    for i in range(48):
        val = 50 - 50 * sin(2 * pi * frequency * base * (i + offset))
        line.append(PIL.ImageColor.getrgb(f"hsb(0, 0%, {val}%)"))
    return [line for _ in range(16)]


def getblock(block, x):
    offset = 48 * (x % 2)
    if block == "_":
        return make_colour(black)
    elif block == "W":
        return make_colour(white)
    elif block == "R":
        return make_colour(red)
    elif block == "G":
        return make_colour(green)
    elif block == "B":
        return make_colour(blue)
    elif block == "C":
        return make_colour(cyan)
    elif block == "M":
        return make_colour(magenta)
    elif block == "Y":
        return make_colour(yellow)
    elif block == "x":
        return make_grid()
    elif block == "]":
        return make_grid(left=False)
    elif block == "[":
        return make_grid(right=False)
    elif block == "=":
        return make_grid(left=False, right=False)
    elif block == "|":
        return make_pulse()
    elif block == "a":
        return make_colour(grey20)
    elif block == "b":
        return make_colour(grey40)
    elif block == "c":
        return make_colour(grey60)
    elif block == "d":
        return make_colour(grey80)
    elif block == "g":
        return make_colour(grey75)
    elif block == "1":
        return make_grating(1.5, offset=offset)
    elif block == "2":
        return make_grating(2.5, offset=offset)
    elif block == "3":
        return make_grating(3.5, offset=offset)
    elif block == "4":
        return make_grating(4.0, offset=offset)
    elif block == "5":
        return make_grating(4.5, offset=offset)
    elif block == "6":
        return make_grating(5.25, offset=offset)
    else:
        return make_colour(grey75)


image = PIL.Image.new("RGB", (768, 576))
px = image.load()
y = 0
for row in grid:
    x = 0
    for block in row:
        chunk = getblock(block, x / 48)
        ly = y
        if chunk is None:
            breakpoint()
        for r in chunk:
            for _ in range(2):
                lx = x
                jump = 48 // len(r)
                for p in r:
                    for _ in range(jump):
                        px[lx, ly] = p
                        lx += 1
                ly += 1
        x += 16 * 3
    y += 16 * 2

im2 = image.filter(PIL.ImageFilter.GaussianBlur(0.6))

im2.save("etp1.png")
