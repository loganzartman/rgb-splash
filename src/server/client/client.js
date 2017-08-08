class Client {
	static init() {
		Client.outputNode = document.createElement("div");
		document.body.appendChild(Client.outputNode);
		Client.log("Test client loaded!");
	}

	static log(s) {
		if (Client.outputNode.childNodes.length > 0)
			Client.outputNode.appendChild(document.createElement("br"));
		Client.outputNode.appendChild(document.createTextNode(s));
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
		red: 0,
		green: 0,
		blue: 0
	},
	computed: {
		mixedColor: function() {
			return {"backgroundColor": `rgb(\
				${Math.floor(this.red*255)},\
				${Math.floor(this.green*255)},\
				${Math.floor(this.blue*255)}\
			)`};
		}
	},
	methods: {
		makeColor: function(channelName) {
			color = {red: 0, green: 0, blue: 0};
			color[channelName] = this[channelName];
			return {"backgroundColor": `rgb(\
				${Math.floor(color.red*255)},\
				${Math.floor(color.green*255)},\
				${Math.floor(color.blue*255)}\
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
			parseFloat(vm.red),
			parseFloat(vm.green),
			parseFloat(vm.blue)
		]),
		"POST",
		result => console.log(result)
	);
}, 200);

vm.$watch("red", colorChange);
vm.$watch("green", colorChange);
vm.$watch("blue", colorChange);