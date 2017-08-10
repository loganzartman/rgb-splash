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
			color = [0,0,0];
			color[channelIdx] = this.color[channelIdx];
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
			parseFloat(vm.color[0]),
			parseFloat(vm.color[1]),
			parseFloat(vm.color[2])
		]),
		"POST",
		result => console.log(result)
	);
}, 200);

vm.$watch("channels", colorChange, {deep: true});