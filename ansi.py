import sys

ESC = '\033['

CODE_CURSOR_UP = 'A'
CODE_CURSOR_DOWN = 'B'
CODE_CURSOR_FWD = 'C'
CODE_CURSOR_BWD = 'D'
CODE_CURSOR_POS = 'H'

CODE_CURSOR_HIDE = 'l'
CODE_CURSOR_SHOW = 'h'

CODE_CURSOR_LOAD = 'u'
CODE_CURSOR_SAVE = 's'

CODE_ERASE = 'J'
CODE_SGR = 'm'

COLOR_FG = 0
COLOR_BG = 10
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7
COLOR_RGB = 8

def csi(code, args=""):
    return ESC + args + code

def output(s):
    sys.stdout.write(s)

def cursorSave():
    return output(csi(CODE_CURSOR_SAVE))

def cursorLoad():
    return output(csi(CODE_CURSOR_LOAD))

def cursorTo(row=1,col=1):
    return output(csi(CODE_CURSOR_POS, "{0};{1}".format(row,col)))

def cursorMove(x=0,y=0):
    if x != 0:
        codeX = CODE_CURSOR_FWD if x>0 else CODE_CURSOR_BWD
        output(csi(codeX, str(abs(x))))
    if y != 0:
        codeY = CODE_CURSOR_DOWN if y>0 else CODE_CURSOR_UP
        output(csi(codeY, str(abs(y))))

def clear():
    val = output(csi(CODE_ERASE, '2'))
    cursorSave()
    return val

def setColor(color,mode=COLOR_FG,bright=False):
    if bright:
        return output(csi(CODE_SGR, "{0};1".format(color+30+mode)))
    else:
        return output(csi(CODE_SGR, "{0}".format(color+30+mode)))

def setColorRGB(r,g,b,mode=COLOR_FG):
    return output(csi(CODE_SGR, "{0};2;{1};{2};{3}".format(COLOR_RGB+30+mode, clipRGB(r), clipRGB(g), clipRGB(b))))

def resetFormat():
    return output(csi(CODE_SGR, '0'))

def clipRGB(v):
    return int(max(0,min(255,v)))

cursorSave()