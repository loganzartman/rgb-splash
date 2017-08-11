import random
import math

class Noise:
	def __init__(self, seed=12345):
		self.P = [x for x in range(0,256)]
		self.seed = seed
		random.seed(seed)
		random.shuffle(self.P)
		self.P += self.P

	def int1d(self, n):
		n = int(n + self.seed)
		n = (n >> 13) ^ n
		nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
		return 1.0 - (float(nn) / 1073741824.0)

	def perlin(self,x,y,z):
		# unit cube
		X = int(x) & 255
		Y = int(y) & 255
		Z = int(z) & 255

		#relative position
		x -= math.floor(x)
		y -= math.floor(y)
		z -= math.floor(z)

		#fade curves
		u = Noise.perlinFade(x)
		v = Noise.perlinFade(y)
		w = Noise.perlinFade(z)

		#hash cube corners
		A = self.P[X]+Y
		AA = self.P[A]+Z
		AB = self.P[A+1]+Z
		B = self.P[X+1]+Y
		BA = self.P[B]+Z
		BB = self.P[B+1]+Z

		#gradient values
		g0 = Noise.perlinGrad(self.P[AA], x,  y,  z)
		g1 = Noise.perlinGrad(self.P[BA], x-1,y,  z)
		g2 = Noise.perlinGrad(self.P[AB], x,  y-1,z)
		g3 = Noise.perlinGrad(self.P[BB], x-1,y-1,z)
		g4 = Noise.perlinGrad(self.P[AA+1], x,  y,  z-1)
		g5 = Noise.perlinGrad(self.P[BA+1], x-1,y,  z-1)
		g6 = Noise.perlinGrad(self.P[AB+1], x,  y-1,z-1)
		g7 = Noise.perlinGrad(self.P[BB+1], x-1,y-1,z-1)

		#add blended results from 8 corners of cube
		return Noise.lerp(w, Noise.lerp(v, Noise.lerp(u, g0, g1), Noise.lerp(u, g2, g3)), Noise.lerp(v, Noise.lerp(u, g4, g5), Noise.lerp(u, g6, g7)))

	@staticmethod
	def perlinFade(t):
		return t*t*t*(t*(t*6-15)+10)

	@staticmethod
	def lerp(t,a,b):
		return a + t*(b-a)

	@staticmethod
	def perlinGrad(hashval,x,y,z):
		h = int(hashval) & 15
		u = x if h<8 else y
		v = y if h<4 else (x if h==12 or h==14 else z)
		return (u if (h&1) == 0 else -u) + (v if (h&2) == 0 else -v)

if __name__ == "__main__":
	noise = Noise()
	v = [noise.perlin(x * 0.01 + 3, 1, 2) for x in range(1,4)]
	for x in v:
		print(x)