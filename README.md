## RGB-Splash
###### A simple open-source RGB matrix build

![Finished build](http://i.imgur.com/MRoFMbo.jpg)

**Sections**
* [Model and printing](#model)
* [Electrical build](#electrical)
* [Software](#software)

#### The Idea
I had been interested in buying some WiFi-connected RGB light bulbs, but any decent one was fairly expensive. I had also learned that the [Raspberry Pi Zero W][rpi zero w] was available and actually in stock, and looked like a great board to control a WiFi RGB lamp. My completed project was simple and cost only about $40.

### Model and printing <a name="model"/>
![Prototype and Print](http://i.imgur.com/c5eZpfi.jpg)
I 3D-printed a simple stand for my LEDs and electrical components. I printed a small slice of my original model (visible in back), which you can find at `models/proto_1.stl`. I made some slight adjustments before printing the new version, which you can find at `models/proto_1b.stl`. I printed the stands using an original XYZ DaVinci 1.0, using some old ABS filament I had. Visible in the image are some repairs that had to be made to the final print using "ABS slurry".

### Electrical build <a name="electrical"/>
**Parts List**

Part | Cost
--- | ---:
[Raspberry Pi Zero W][part rpi] | $10.00
[GPIO Header][part gpio] | $0.95
[1m WS2811 5050 RGB LED Strip][part rgb] | $10.88
[5V ~2.5A Power Supply][part supply] | $7.95
[MicroSD Card][part sdcard] | $8.24
**Total** | $43.21

**Optional Parts**

Part | Cost
--- | ---:
[Small Breadboards][part breadboard] | $5.99
[Jumper Wires][part jumpers] | $8.39
**Total** | $14.38

#### Build Overview
The LED strip used requires only a 5V supply, a ground connection, and a signal input to control the LEDs. The Raspberry Pi has a couple pins that can output a PWM signal at 3.3V. It also has several 5V pins that are directly connected to the power supply. Several guides I read indicated that it might be necessary to boost the Pi's 3.3V logic signal to 5V, but this proved to be unnecessary in practice. Therefore, the electrical build for this project is simple, with the LED strip connected directly to one each of the 5V, ground, and PWM pins on the Pi.

The power supply used supplies 5V at up to 2.5A. Based on the specifications for the LED strip, I initially believed that I could power only 30 of the LEDs. In practice, I measured a current draw of only about 1A with 30 LEDs at full brightness. Assuming that the Pi draws about half an amp, nearly the entire 60-LED strip could be powered. I decided to use 42 LEDs in my build.

#### Cutting and soldering
The WS2811 LED strip can be cut and reattached between any individual LEDs. My stand design fits 6-LED strips placed vertically, 7 or 8 strips wide. The strips are reattached with hookup wire wherever they are cut. It is easiest to tin the pads on the LED strip and then solder the wires to them.
![Soldering Animation](http://i.imgur.com/pSiaVeP.gif)

### Software <a name="software"/>
On microcontroller boards such as Arduinos, it's easy to control output pins with precise timing. On the Pi, I use jgarff's [rpi_ws281x][rpi lib] to control the Pi's PWM outputs and produce the 800KHz logic signal required by the WS2811 chips in the LED strip. This library also provides its own version of Adafruit's [Neopixel library][neopixel lib] for easy programming with Python.
![LED Test](http://i.imgur.com/ACd9LKz.jpg)
Once the SD card is flashed with an OS and WiFi configuration, the Pi can simply be plugged into a wall and accessed via SSH over the local network. The router's client table page can be used to locate the Pi's IP address.

After building the rpi\_ws281x library, I created several Python scripts to make it easier to control the LED matrix. These scripts depend on rpi\_ws281x's `neopixel.py`. `splash.py` contains configuration data for rpi\_ws281x, as well as functions to set pixels and display images, taking into account the layout of the LED matrix. `img.py` provides an `Image` class and an `IColor` class, which implement RGB images and RGB colors respectively. For more information, see the inline documentation in these scripts.

Using these libraries, it is fairly easy to create effects like this:
![Color Scale](http://i.imgur.com/CrIIVSs.jpg)
The complete source code for this effect follows:

```python
from splash import *

# Defines function to compute pixel color given x,y from 0 to 1
def render(x,y,img):
	# More red to the right, more green to the bottom
	return IColor(x,y,0)

# Main program logic follows:
if __name__ == '__main__':
	# Create LED strip and Image
	strip = createStrip()
	img = Image(LED_W, LED_H)

	# Compute pixels
	img.compute(render)

	# Display result
	showImage(strip, img)
```

---
`rainbow.py`:

![Demo Animation](https://thumbs.gfycat.com/DistortedDopeyEyelashpitviper-size_restricted.gif)

[rpi zero w]: https://www.raspberrypi.org/products/raspberry-pi-zero-w/
[rpi lib]: https://github.com/jgarff/rpi_ws281x
[neopixel lib]: https://github.com/adafruit/Adafruit_NeoPixel
[part rpi]: https://www.sparkfun.com/products/14277
[part gpio]: https://www.sparkfun.com/products/14275
[part rgb]: https://www.amazon.com/Mokungit-Programmable-Individual-Addressable-Non-waterproof/dp/B01D1DRJ0G
[part supply]: https://www.sparkfun.com/products/13831
[part sdcard]: https://www.amazon.com/SanDisk-Mobile-MicroSDHC-Adapter-SDSDQM-016G-B35A/dp/B004ZIENBA
[part breadboard]: https://www.amazon.com/gp/product/B016Q6T7Q4
[part jumpers]: https://www.amazon.com/GenBasic-Solderless-Ribbon-Breadboard-Prototyping/dp/B01L5UJ36U
