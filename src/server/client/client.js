class Client {
	static init() {
		Client.log("Test client loaded!");
		Client.vueInit();
		Client.httpReq("/client/test/fullstate", "GET", function(data){
			data = JSON.parse(data);
			if (!data.ok) {
				alert("Client is offline!");
			}
			else {
				for (let prop in data) {
					if (prop !== "ok") {
						Client.vm[prop] = data[prop];
					}
				}
			}
		});
	}

	static vueInit() {
		let vm = new Vue({
			el: "#container",
			data: {
				power: false,
				color: [0,0,0]
			},
			computed: {
				mixedColor: function() {
					return {"backgroundColor": `rgb(\
						${Math.floor(this.color[0]*255)},\
						${Math.floor(this.color[1]*255)},\
						${Math.floor(this.color[2]*255)}\
					)`};
				}
			},
			methods: {
				makeColor: function(channelIdx) {
					let color = [0,0,0];
					color[channelIdx] = this.color[channelIdx];
					return {"backgroundColor": `rgb(\
						${Math.floor(color[0]*255)},\
						${Math.floor(color[1]*255)},\
						${Math.floor(color[2]*255)}\
					)`};
				},
				setPower: function(state) {
					this.power = state;
				}
			}
		});

		function powerChange(){
			Client.httpReq(
				"/client/test/state/power/" + JSON.stringify(vm.power),
				"POST",
				result => console.log(result)
			);
		}

		let colorChange = debounce((oldVal, newVal) => {
			Client.httpReq(
				"/client/test/state/color/" + JSON.stringify([
					parseFloat(vm.color[0]),
					parseFloat(vm.color[1]),
					parseFloat(vm.color[2])
				]),
				"POST",
				result => console.log(result)
			);
		}, 200);

		vm.$watch("power", powerChange);
		vm.$watch("color", colorChange, {deep: true});
		Client.vm = vm;
	}

	static log(s) {
		console.log(s);
	}

	static httpReq(path, mode, callback, params={}) {
		let xhr = new XMLHttpRequest();

		xhr.onload = function(){
			callback(xhr.responseText);
		};

		let paramstr = Object.keys(params).map(key => key+"="+params[key]).join("&");
		let url = `${path}?${paramstr}`;
		xhr.open(mode, url, true);
		xhr.send();
	}
}
Client.init();

function debounce(f, timeout) {
	let timer = null, call = false;
	let that = null, args = [];

	function handleTimer() {
		if (call)
			f.apply(that, args);
		timer = null;
		call = false;
	}

	return function(){
		that = this;
		args = arguments;
		if (timer === null) {
			f.apply(that, args);
			timer = setTimeout(handleTimer, timeout);
			call = false;
		}
		else {
			call = true;
		}
	}
}