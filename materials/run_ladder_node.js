// Runs the SAME engine file the browser loads (assets/ssc-live.js) over the whole ladder and prints
// the canon as JSON, plus the engine selfTest on the shipped data and with a planted fault.
// Usage: node materials/run_ladder_node.js
var path = require("path"), fs = require("fs");
var E = require(path.join(__dirname, "..", "assets", "ssc-live.js"));
var D = JSON.parse(fs.readFileSync(path.join(__dirname, "ssc-data.json"), "utf8"));
var out = E.ladder(D);
out.selfTest = E.selfTest(D);
out.selfTestPlanted = E.selfTest(D, true);
process.stdout.write(JSON.stringify(out, null, 1) + "\n");
