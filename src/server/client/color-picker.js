Vue.component("color-picker", {
	template: `
		<div class="mdl-grid">
		<span class="mdl-cell mdl-cell--9-col-desktop mdl-cell--12-col mdl-cell--middle">
			<table style="width: 100%; border-spacing: 0; border-radius: 4px;">
				<tr style="width: 100%;" ref="wheelContainer"></tr>
				<tr></tr>
			</table>
		</span>

		<span class="mdl-cell mdl-cell--3-col-desktop mdl-cell--12-col mdl-shadow--3dp"
		 v-bind:style="mixedColor" style="height: inherit; min-height: 108px; border-radius: 4px;"></span>
		</div>`,
	props: ["value"],
	data: function(){
		return {
			value: [0,0,0]
		}
	},
	mounted: function() {
		let container = this.$refs.wheelContainer;
		let wheel = this.makeWheel(container.offsetWidth);
		container.appendChild(wheel);
	},
	computed: {
		mixedColor: function() {
			return {"backgroundColor": `rgb(\
				${Math.floor(this.value[0]*255)},\
				${Math.floor(this.value[1]*255)},\
				${Math.floor(this.value[2]*255)}\
			)`};
		}
	},
	methods: {
		hsl2rgb: function(h, s, l) {
			let r, g, b;
			const hue2rgb = (p, q, t) => {
				if (t < 0) t += 1;
				if (t > 1) t -= 1;
				if (t < 1/6) return p + (q - p) * 6 * t;
				if (t < 1/2) return q;
				if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
				return p;
			};

			if(s === 0) {
				r = g = b = l; // achromatic
			}
			else {
				let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
				let p = 2 * l - q;
				r = hue2rgb(p, q, h + 1/3);
				g = hue2rgb(p, q, h);
				b = hue2rgb(p, q, h - 1/3);
			}
			return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
		},

		computeColor: function(angle, distance, brightness) {
			distance = Math.max(0, Math.min(1, distance));
			let rgb = this.hsl2rgb(angle, distance, brightness);
			return rgb;
		},

		makeWheel: function(size) {
			let display = document.createElement("canvas");
			display.width = size;
			display.height = size;
			let ctx = display.getContext("2d");

			let wheelBuffer = this.createWheelImage(size);

			//adjustable params
			let brightness = 0;
			let distance = 1;
			let angle = 0;

			//redraw function
			const redraw = () => {
				const br = Math.floor(brightness * 255);
				const col = this.computeColor(angle, distance, brightness);

				ctx.save();

				//fill background with brightness
				ctx.clearRect(0, 0, size, size);
				ctx.fillStyle = `rgb(${br}, ${br}, ${br})`;
				ctx.beginPath();
				ctx.arc(size/2, size/2, size/2-1, 0, Math.PI*2);
				ctx.fill();

				//draw color wheel
				ctx.drawImage(wheelBuffer, 0, 0);

				//draw selected color circle
				ctx.lineStyle = "white";
				ctx.lineWidth = 2;
				ctx.fillStyle = `rgb(${col[0]}, ${col[1]}, ${col[2]})`;
				ctx.restore();
			};
			redraw();

			//attach adjustable params to canvas
			Object.defineProperty(display, "brightness", {
				get: function() {
					return brightness;
				},
				set: function(b) {
					brightness = Math.max(0, Math.min(1, b));
					redraw();
				}
			});
			Object.defineProperty(display, "angle", {
				get: function() {
					return angle;
				},
				set: function(a) {
					angle = a;
					redraw();
				}
			});
			Object.defineProperty(display, "distance", {
				get: function() {
					return distance;
				},
				set: function(d) {
					distance = Math.max(0, Math.min(1, d));
					redraw();
				}
			});

			return display;
		},

		createWheelImage: function(size) {
			let canvas = document.createElement("canvas");
			canvas.width = size;
			canvas.height = size;
			let ctx = canvas.getContext("2d");
			let idata = ctx.getImageData(0, 0, size, size);
			let data = idata.data;

			//compute hue wheel
			for (let x=0; x<size; x++) {
				for (let y=0; y<size; y++) {
					let idx = (y*size+x)*4;
					const cx = size/2;
					const cy = size/2;

					//compute hue
					let angle = Math.atan2(y - cx, x - cy) - Math.PI*0.5;
					let h = angle / (Math.PI*2) + 0.5;
					let rgb = this.hsl2rgb(h,1,0.5);
					
					//compute alpha
					let dx = x - cx, dy = y - cy;
					let dist = Math.sqrt(dx*dx+dy*dy);
					let a = dist / (size/2);
					if (a > 1)
						a = Math.max(0, a - (a-1)*(size/2)); //antialias

					//write color
					data[idx+0] = rgb[0];
					data[idx+1] = rgb[1];
					data[idx+2] = rgb[2];
					data[idx+3] = Math.floor(a*255);
				}
			}
			ctx.putImageData(idata, 0, 0);
			return canvas;
		}
	},
	watch: {
		value: function(newValue) {
			this.$emit("input", newValue);
		}
	}
});