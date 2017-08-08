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

	static httpReq(path, mode, params, callback) {
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

document.getElementById("powerOn").addEventListener("click", function(event){
	Client.httpReq("/power", "POST", {"state": "on"}, result => console.log(result));
}, false);

document.getElementById("powerOff").addEventListener("click", function(event){
	Client.httpReq("/power", "POST", {"state": "off"}, result => console.log(result));
}, false);