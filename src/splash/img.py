import math
import colorsys

class IColor:
	"""Represents an RGB color.
	Red, green, and blue components are in the range [0,1].
	pack() can be used to produce a 32-bit ARGB integer for use with Neopixel.
	"""
	def __init__(self,r=0,g=0,b=0):
		"""Keyword arguments:
		r -- red channel value [0,1]
		g -- green channel value [0,1]
		b -- blue channel value [0,1]
		"""
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	@staticmethod
	def fromInts(r,g,b):
		"""Construct an IColor from ints in the range [0,255].
		Contrast with IColor constructor which accepts floats in [0,1].
		"""
		return IColor(r/255.,g/255.,b/255.)

	@staticmethod
	def fromHSL(h,s,l):
		"""Construct an IColor from hue, saturation, and lightness components
		in the range [0,1].
		"""
		rgb = colorsys.hls_to_rgb(h,l,s)
		return IColor(rgb[0], rgb[1], rgb[2])

	@staticmethod
	def fromKelvin(k):
		"""Construct an IColor from a color temperature expressed in Kelvin.
		Uses a formula from http://www.zombieprototypes.com/?p=210
		"""
		r = g = b = 0
		#compute red value
		if k<6600:
			r = 255
		else:
			x = k/100.-55
			r = 351.97690566805693 + 0.114206453784165*x + -40.25366309332127*math.log(x)
		
		#compute green value
		if k<1000:
			g = 0
		elif k>=6600:
			x = k/100.-50
			g = 325.4494125711974 + 0.07943456536662342*x + -28.0852963507957*math.log(x)
		else:
			x = k/100.-2
			g = -155.25485562709179 + -0.44596950469579133*x + 104.49216199393888*math.log(x)

		#compute blue value
		if k<2000:
			b = 0
		elif k>6600:
			b = 255
		else:
			x = k/100.-10
			b = -254.76935184120902 + 0.8274096064007395*x + 115.67994401066147*math.log(x)

		return IColor.fromInts(r,g,b)


	@staticmethod
	def scaleClip(x):
		"""Scale color value from [0,1] float to [0,255] int.
		Use a non-linear scaling formula to improve brightness accuracy for LED output.
		"""
		x = 0 if x < 0 else x
		x = 1 if x > 1 else x
		return int(round((x*.3+(x**3)*.7)*255))

	@staticmethod
	def scaleClipl(x):
		"""Scale color value from [0,1] float to [0,255] int.
		Use a linear scaling forumla.
		"""
		x = 0 if x < 0 else x
		x = 1 if x > 1 else x
		return int(round(x*255.))

	def pack(self):
		"""Return a 32-bit int packed (ARGB) representation of this color."""
		a = 255
		r = IColor.scaleClip(self.r)
		g = IColor.scaleClip(self.g)
		b = IColor.scaleClip(self.b)
		return (a << 24) | (r << 16) | (g << 8) | (b)

	def packl(self):
		"""Return a 32-bit int packed (ARGB) representation of this color.
		Use the linear scaling formula.
		"""
		a = 255
		r = IColor.scaleClipl(self.r)
		g = IColor.scaleClipl(self.g)
		b = IColor.scaleClipl(self.b)
		return (a << 24) | (r << 16) | (g << 8) | (b)

	def __add__(self, other):
		if type(other) == int or type(other) == float:
			return IColor(self.r+other, self.g+other, self.b+other)
		else:
			return IColor(self.r+other.r, self.g+other.g, self.b+other.b)

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return IColor(self.r*other, self.g*other, self.b*other)
		else:
			return IColor(self.r*other.r, self.g*other.g, self.b*other.b)

class Image:
	"""Represents a 2D RGB image.
	Each pixel can be assigned an IColor.

	"""
	def __init__(self, w, h):
		"""Construct an image of given width and height."""
		self.w = w
		self.h = h
		self.size = self.w*self.h
		self.data = [IColor() for x in range(self.size)]
		self.temp = [IColor() for x in range(self.size)]

	def inBounds(self, px, py):
		"""Determine whether a pixel position is within bounds."""
		return px >= 0 and py >= 0 and px < self.w and py < self.h

	def getPixel(self, px, py):
		"""Given a position (in pixel units), get the color of the pixel there.
		See sample() to use percentage unit."""
		if not self.inBounds(px,py):
			return IColor()
		idx = py*self.w + px
		return self.data[idx]

	def setPixel(self, px, py, color):
		"""Given a position (in pixel units), set the color of that pixel."""
		if not self.inBounds(px,py):
			return
		idx = py*self.w + px
		self.data[idx] = color

	def sample(self, x, y):
		"""Given a position (in percentage [0,1]), get the color of the nearest
		pixel to that position.
		Use in a compute() callback to sample colors from an Image.
		See getPixel() to use exact pixel coordinates.
		"""
		px = int(round(x*self.w))
		py = int(round(y*self.h))
		return self.getPixel(px, py)

	def clear(self, color=IColor()):
		"""Clear this Image to a color, or black if no color given."""
		for i in range(self.size):
			self.data[i] = color

	def compute(self, func):
		"""Compute and set the color of each pixel in this image.
		func should be a callback that accepts arguments (x, y, img).
		x -- x position in percentage [0,1]
		y -- y position in percentage [0,1]
		img -- self (this Image)
		func must return an IColor given these arguments.
		"""
		idx = 0
		for y in range(self.h):
			for x in range(self.w):
				color = func(float(x)/(self.w-1), float(y)/(self.h-1), self)
				self.temp[idx] = color
				idx = idx+1
		swap = self.data
		self.data = self.temp
		self.temp = self.data

	def __add__(self, other):
		if type(other) != Image:
			raise TypeError("Other must be an Image.")

		out = Image(self.w, self.h)
		for i in range(out.size):
			out.data[i] = self.data[i] + other.data[i]
		return out

	def __mul__(self, other):
		if type(other) != Image:
			raise TypeError("Other must be an Image.")

		out = Image(self.w, self.h)
		for i in range(out.size):
			out.data[i] = self.data[i] * other.data[i]
		return out