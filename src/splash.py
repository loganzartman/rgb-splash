from neopixel import *
from img import *

# LED strip configuration:
LED_W          = 7
LED_H          = 6
LED_COUNT      = LED_W*LED_H  # Number of LED pixels.
LED_PIN        = 18           # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10           # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000       # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5            # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255          # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False        # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0            # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

def createStrip():
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	return strip

def setPixel(strip, x, y, color):
	colOffset = x
	rowOffset = y if colOffset % 2 == 1 else LED_H-1-y
	idx = colOffset * LED_H + rowOffset
	strip.setPixelColor(idx, color.pack())

def showImage(strip, image):
	for y in range(image.h):
		for x in range(image.w):
			setPixel(strip, x, y, image.getPixel(x,y))
	strip.show()

def showBitMatrix(strip, data, color0, color1):
	for y in range(LED_H):
		for x in range(LED_W):
			val = data[y][x]
			setPixel(strip, x, y, color1 * val + color0 * (1-val))
	strip.show()

def clear(strip, color=IColor(0,0,0)):
	color = color.pack()
	for i in range(LED_COUNT):
		strip.setPixelColor(i, color)
	strip.show()