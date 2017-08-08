const PORT = 8080;
const TIMEOUT = 10000;
const express = require("express");
const fs = require("fs");

let app = express();

const defaults = JSON.parse(fs.readFileSync("defaults.json"));
let clientStates = {};
let clientCallbacks = {};

let testCounter = 0;
app.get("/test", (req,res) => {
	let counter = testCounter++;
	setTimeout(()=>{
		res.end(JSON.stringify({
			"ok": true,
			"c": counter
		}));
	}, 1000);
});

app.get("/client/:cid/connect", (req,res) => {
	let cid = req.params.cid;
	clientCallbacks[cid] = Object.assign({}, defaults);
	res.send(JSON.stringify({
		"ok": true,
		"cid": cid
	}));
});

app.get("/client/:cid/disconnect", (req,res) => {
	let cid = req.params.cid;
	delete clientCallbacks[cid];
	res.send(JSON.stringify({
		"ok": true,
		"cid": cid
	}));
});

app.get("/client/:cid/state/:name", (req,res) => {
	let name = req.params.name;
	let cid = req.params.cid;

	//make sure client is online
	if (!(cid in clientCallbacks)) {
		res.end(JSON.stringify({"ok": false}));
		console.log(`Client ${cid} is offline.`);
		return;
	}

	if (clientCallbacks[cid][name])
		clearTimeout(clientCallbacks[cid][name].timer)

	callback = (state) => {
		res.end(JSON.stringify({
			"ok": true,
			[name]: state
		}));
	};
	callback.timer = setTimeout(()=>{
		res.end(JSON.stringify({
			"ok": false
		}));
	}, TIMEOUT);
	clientCallbacks[cid][name] = callback;
});

app.post("/client/:cid/state/:name/:value", (req,res) => {
	let name = req.params.name;
	let cid = req.params.cid;
	let value = JSON.parse(req.params.value);

	//make sure client is online
	if (!(cid in clientCallbacks)) {
		res.end(JSON.stringify({"ok": false}));
		console.log(`Client ${cid} is offline.`);
		return;
	}

	const callback = clientCallbacks[cid][name];
	callback(value);

	res.send(JSON.stringify({
		"ok": true
	}));
});

app.use(express.static("client"));
app.listen(PORT, ()=>{
	console.log(`rgb-splash server running at :${PORT}`);
});
