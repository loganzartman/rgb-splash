const PORT = 8080;
const express = require("express");

let app = express();

app.get("/hello", (req,res) => {
	res.send("Hello world!");
});

app.get("/test", (req,res) => {
	setTimeout(()=>{
		res.end(JSON.stringify({
			"ok": true
		}));
	}, 1000);
});

app.use(express.static("client"));
app.listen(PORT, ()=>{
	console.log(`rgb-splash server running at :${PORT}`);
});
