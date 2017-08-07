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
}
Client.init();
