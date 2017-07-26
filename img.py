import math
import colorsys

class IColor:
	def __init__(self,r=0,g=0,b=0):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	@staticmethod
	def fromInts(r,g,b):
		return IColor(r/255.,g/255.,b/255.)

	@staticmethod
	def fromHSL(h,s,l):
		rgb = colorsys.hls_to_rgb(h,l,s)
		return IColor(rgb[0], rgb[1], rgb[2])

	@staticmethod
	def fromKelvin(k):
		# http://www.zombieprototypes.com/?p=210
		r = g = b = 0
		if k<6600:
			r = 255
		else:
			x = k/100.-55
			r = 351.97690566805693 + 0.114206453784165*x + -40.25366309332127*math.log(x)
		
		if k<1000:
			g = 0
		elif k>=6600:
			x = k/100.-50
			g = 325.4494125711974 + 0.07943456536662342*x + -28.0852963507957*math.log(x)
		else:
			x = k/100.-2
			g = -155.25485562709179 + -0.44596950469579133*x + 104.49216199393888*math.log(x)

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
		x = 0 if x < 0 else x
		x = 1 if x > 1 else x
		# return int(round(x*255.))
		return int(round((x*.3+(x**3)*.7)*255))

	def pack(self):
		a = 255
		r = IColor.scaleClip(self.r)
		g = IColor.scaleClip(self.g)
		b = IColor.scaleClip(self.b)
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
	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.size = self.w*self.h
		self.data = [IColor() for x in range(self.size)]
		self.temp = [IColor() for x in range(self.size)]

	def inBounds(self, x, y):
		return x >= 0 and y >= 0 and x < self.w and y < self.h

	def getPixel(self, x, y):
		if not self.inBounds(x,y):
			return IColor()
		idx = y*self.w + x
		return self.data[idx]

	def setPixel(self, x, y, color):
		if not self.inBounds(x,y):
			return
		idx = y*self.w + x
		self.data[idx] = color

	def sample(self, ix, iy):
		x = int(round(ix*self.w))
		y = int(round(iy*self.h))
		return self.getPixel(x, y)

	def clear(self, color=IColor()):
		for i in range(self.size):
			self.data[i] = color

	def compute(self, func):
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