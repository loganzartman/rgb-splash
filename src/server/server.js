const PORT = 8080;
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

app.get("/client/:cid/state/:name", (req,res) => {
	let name = req.params.name;
	let cid = req.params.cid;

	callback = (state) => {
		res.end(JSON.stringify({
			"ok": true,
			[name]: state
		}));
	};
	clientCallbacks[cid][name] = callback;
});

app.post("/client/:cid/state/:name/:value", (req,res) => {
	let name = req.params.name;
	let cid = req.params.cid;
	let value = req.params.value;

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
