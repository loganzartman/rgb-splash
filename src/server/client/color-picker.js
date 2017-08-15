Vue.component("color-picker", {
	template: `
		<div class="mdl-grid">
		<span class="mdl-cell mdl-cell--6-col-desktop mdl-cell--12-col mdl-cell--middle">
			<table style="width: 100%; border-spacing: 0; border-radius: 4px;">
				<tr style="width: 100%;" ref="wheelContainer"></tr>
				<tr><slider-plus v-model="brightness" label="Brightness" min="0" max="1" value="1" step="0.01"></slider-plus></tr>
			</table>
		</span>

		<span class="mdl-cell mdl-cell--6-col-desktop mdl-cell--12-col mdl-shadow--3dp"
		 v-bind:style="mixedColor" style="height: 108px; border-radius: 4px;"></span>
		</div>`,
	props: ["value"],
	data: function(){
		return {
			color: this.value,
			brightness: 1
		}
	},
	mounted: function() {
		let container = this.$refs.wheelContainer;
		let wheel = this.makeWheel(container.offsetWidth, col => this.color = [col[0]/255, col[1]/255, col[2]/255]);
		container.appendChild(wheel);

		this.$watch("brightness", val => wheel.brightness = val);
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
		hsv2rgb: function(h, s, v) {
		    h %= 1;
		    if (h < 0)
		    	h += 1;

		    let r, g, b, i, f, p, q, t;
		    if (arguments.length === 1) {
		        s = h.s, v = h.v, h = h.h;
		    }
		    i = Math.floor(h * 6);
		    f = h * 6 - i;
		    p = v * (1 - s);
		    q = v * (1 - f * s);
		    t = v * (1 - (1 - f) * s);
		    switch (i % 6) {
		        case 0: r = v, g = t, b = p; break;
		        case 1: r = q, g = v, b = p; break;
		        case 2: r = p, g = v, b = t; break;
		        case 3: r = p, g = q, b = v; break;
		        case 4: r = t, g = p, b = v; break;
		        case 5: r = v, g = p, b = q; break;
		    }
		    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
		},

		computeColor: function(angle, distance, brightness) {
			distance = Math.max(0, Math.min(1, distance));
			let rgb = this.hsv2rgb(angle, distance, brightness);
			return rgb;
		},

		makeWheel: function(size, updateCallback) {
			const radius = size/2;
			let display = document.createElement("canvas");
			display.width = size;
			display.height = size;
			let ctx = display.getContext("2d");

			let wheelBuffer = this.createWheelImage(size);

			//adjustable params
			let brightness = 1;
			let distance = 0.5;
			let angle = 0;

			//redraw function
			const redraw = () => {
				const col = this.computeColor(angle / (Math.PI*2) + 0.25, distance, brightness);
				const br = Math.round(brightness * 255);
				const selX = Math.cos(angle)*distance*radius + size/2;
				const selY = Math.sin(angle)*distance*radius + size/2;

				updateCallback(col);

				ctx.save();

				//fill background with brightness
				ctx.clearRect(0, 0, size, size);
				ctx.fillStyle = "black";
				ctx.beginPath();
				ctx.arc(size/2, size/2, size/2-0.25, 0, Math.PI*2);
				ctx.shadowOffsetY = 4;
				ctx.shadowBlur = 6;
				ctx.shadowColor = "rgba(0,0,0,0.25)";
				ctx.fill();

				ctx.restore();
				ctx.save();

				//draw color wheel
				ctx.globalAlpha = brightness;
				ctx.drawImage(wheelBuffer, 0, 0);
				ctx.globalAlpha = 1;

				//draw selected color circle
				ctx.lineWidth = 2;
				ctx.fillStyle = `rgb(${col[0]}, ${col[1]}, ${col[2]})`;
				ctx.beginPath();
				ctx.arc(selX, selY, 14, 0, Math.PI*2);
				ctx.fill();
				ctx.strokeStyle = "black";
				ctx.stroke();
				ctx.beginPath();
				ctx.arc(selX, selY, 13, 0, Math.PI*2);
				ctx.strokeStyle = "white";
				ctx.stroke();
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

			this.attachListeners(display, size);
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
					
					//compute saturation
					let dx = x - cx, dy = y - cy;
					let dist = Math.sqrt(dx*dx+dy*dy);
					let s = Math.min(1, dist / (size/2));

					//compute alpha
					let a = Math.max(1, dist / (size/2));
					if (a > 1)
						a = Math.max(0, a - (a-1)*(size/2)); //antialias

					//write color
					let rgb = this.hsv2rgb(h,s,1);
					data[idx+0] = rgb[0];
					data[idx+1] = rgb[1];
					data[idx+2] = rgb[2];
					data[idx+3] = Math.round(a * 255);
				}
			}
			ctx.putImageData(idata, 0, 0);
			return canvas;
		},

		attachListeners: function(el, size) {
			let down = false;

			//get a position from either touch or mouse event
			//relative to target element
			const normalizePosition = (event) => {
				let x, y;
				if (event.targetTouches) {
					x = event.targetTouches[0].clientX;
					y = event.targetTouches[0].clientY;
				}
				else {
					x = event.clientX;
					y = event.clientY;
				}

				let target = event.target || event.srcElement;
				let rect = target.getBoundingClientRect();
				x -= rect.left;
				y -= rect.top;
				return {x, y};
			};

			//update the internal position data
			const updatePosition = (event) => {
				if (!down)
					return;
				
				let pos = normalizePosition(event);
				let dx = pos.x - size/2, dy = pos.y - size/2;
				let angle = Math.atan2(dy, dx);
				let dist = Math.sqrt(dx*dx+dy*dy) / (size*0.5);
				el.angle = angle;
				el.distance = dist;
			};

			el.addEventListener("mousedown", function(event){event.preventDefault(); down = true;}, false);
			el.addEventListener("mouseup", function(event){event.preventDefault(); down = false;}, false);
			el.addEventListener("mousemove", function(event){updatePosition(event);}, false);

			el.addEventListener("touchstart", function(event){event.preventDefault(); down = true;}, false);
			el.addEventListener("touchend", function(event){event.preventDefault(); down = false;}, false);
			el.addEventListener("touchmove", function(event){updatePosition(event);}, false);
		}
	},
	watch: {
		color: function(newValue) {
			this.$emit("input", newValue);
		}
	}
});