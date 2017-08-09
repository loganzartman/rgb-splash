class Client {
	static init() {
		Client.log("Test client loaded!");
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

let vm = new Vue({
	el: "#container",
	data: {
		channels: [
			{name: "red", val: 0},
			{name: "green", val: 0},
			{name: "blue", val: 0}
		]
	},
	computed: {
		mixedColor: function() {
			return {"backgroundColor": `rgb(\
				${Math.floor(this.channels[0].val*255)},\
				${Math.floor(this.channels[1].val*255)},\
				${Math.floor(this.channels[2].val*255)}\
			)`};
		}
	},
	methods: {
		makeColor: function(channelIdx) {
			color = [0,0,0];
			color[channelIdx] = this.channels[channelIdx].val;
			return {"backgroundColor": `rgb(\
				${Math.floor(color[0]*255)},\
				${Math.floor(color[1]*255)},\
				${Math.floor(color[2]*255)}\
			)`};
		},
		power: function(state) {
			Client.httpReq(
				"/client/test/state/power/" + JSON.stringify(state),
				"POST",
				result => console.log(result)
			);
		}
	}
});

let colorChange = debounce((oldVal, newVal) => {
	Client.httpReq(
		"/client/test/state/color/" + JSON.stringify([
			parseFloat(vm.channels[0].val),
			parseFloat(vm.channels[1].val),
			parseFloat(vm.channels[2].val)
		]),
		"POST",
		result => console.log(result)
	);
}, 200);

vm.$watch("channels", colorChange, {deep: true});