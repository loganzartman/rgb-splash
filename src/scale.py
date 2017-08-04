import time
import math
from random import randint
from splash.matrix import *

t0 = time.clock()
t = 0

MAT = [[.1, 0,.2, 0,.3, 0,.4],
       [ 0,.5, 0,.6, 0,.7, 0],
       [.8, 0,.9, 0,1., 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0]]

# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	showBitMatrix(strip, MAT, IColor(), IColor(1,0,0))
