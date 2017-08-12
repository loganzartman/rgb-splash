class Client {
	static init(cid) {
		Client.log("Test client loaded!");
		Client.vueInit();
		Client.vm.cid = cid;
		Client.httpReq(`/client/${Client.vm.cid}/fullstate`, "GET", function(data){
			data = JSON.parse(data);
			if (!data.ok) {
				let sb = document.querySelector(".mdl-js-snackbar");
				sb.MaterialSnackbar.showSnackbar({message: `${cid} is offline.`});
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
				cid: null,
				power: false,
				color: [0,0,0],
				fxparams: {
					speed: 0
				}
			},
			methods: {
				makeColor: function(channelIdx) {
					let color = [0,0,0];
					color[channelIdx] = 0.7;
					return {"backgroundColor": `rgb(\
						${Math.floor(color[0]*255)},\
						${Math.floor(color[1]*255)},\
						${Math.floor(color[2]*255)}\
					)`};
				},
				togglePower: function(event) {
					let newPower = !vm.power;
					let button = event.currentTarget;
					button.disabled = true;
					Client.httpReq(
						`/client/${Client.vm.cid}/state/power/` + JSON.stringify(newPower),
						"POST",
						result => {
							button.disabled = false;
							if (JSON.parse(result).ok)
								vm.power = newPower;
						}
					);
				},
				actionHandler: function(action) {
					Client.httpReq(
						`/client/${Client.vm.cid}/state/action/${JSON.stringify(action)}`,
						"POST",
						result => {}
					);
				}
			}
		});

		let colorChange = debounce((oldVal, newVal) => {
			Client.httpReq(
				`/client/${Client.vm.cid}/state/color/` + JSON.stringify([
					parseFloat(vm.color[0]),
					parseFloat(vm.color[1]),
					parseFloat(vm.color[2])
				]),
				"POST",
				result => console.log(result)
			);
		}, 200);

		let fxparamsChange = debounce((oldVal, newVal) => {
			Client.httpReq(
				`/client/${Client.vm.cid}/state/fxparams/` + JSON.stringify(vm.fxparams),
				"POST",
				result => console.log(result)
			);
		}, 200);

		vm.$watch("color", colorChange, {deep: true});
		vm.$watch("fxparams", fxparamsChange, {deep: true});
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
Client.init("test-client");

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