import time
from splash import *

L_S = [[0, 1, 1, 1, 1, 0, 0],
       [0, 1, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 0, 0],
       [0, 0, 0, 0, 1, 0, 0],
       [0, 1, 1, 1, 1, 0, 0]]

L_E = [[0, 1, 1, 1, 1, 0, 0],
       [0, 1, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 0, 0]]

L_X = [[0, 1, 0, 0, 0, 1, 0],
       [0, 0, 1, 0, 1, 0, 0],
       [0, 0, 0, 1, 0, 0, 0],
       [0, 0, 1, 0, 1, 0, 0],
       [0, 1, 0, 0, 0, 1, 0],
       [0, 1, 0, 0, 0, 1, 0]]


# Main program logic follows:
if __name__ == '__main__':
	strip = createStrip()

	print ('Press Ctrl-C to quit.')
	while True:
		showBitMatrix(strip, L_S, Color(0,0,0), Color(255,0,255))
		time.sleep(1)
		showBitMatrix(strip, L_E, Color(0,0,0), Color(255,255,0))
		time.sleep(1)
		showBitMatrix(strip, L_X, Color(0,0,0), Color(0,255,255))
		time.sleep(1)
		clear(strip)
		time.sleep(0.7)
