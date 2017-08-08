const PORT = 8080;
const express = require("express");

let app = express();

app.get("/hello", (req,res) => {
	res.send("Hello world!");
});

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

let powerCallback = ()=>{};
app.get("/power", (req,res) => {
	powerCallback = (state) => {
		res.end(JSON.stringify({
			"ok": true,
			"power": state
		}));
	};
});

app.post("/power", (req,res) => {
	let state = req.query.state.toLowerCase();
	if (state === "on")
		powerCallback(true);
	else if (state === "off")
		powerCallback(false);
	else {
		res.send(JSON.stringify({
			"error": "state must be on or off"
		}));
		return;
	}
	res.send(JSON.stringify({
		"ok": true
	}));
});

app.use(express.static("client"));
app.listen(PORT, ()=>{
	console.log(`rgb-splash server running at :${PORT}`);
});
