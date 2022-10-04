const read = require("../src/read");
const { parseFmt, parseMode, args } = require("../src/args");
const render = require("../src/render");
const compile = require("../src/compile");

const arg = args();

const fmt = arg.format || parseFmt(arg);
parseMode(arg);

if (fmt === "vega") {
  read(arg.input).then((text) => compile(arg, JSON.parse(text)));
} else if ((fmt === "svg") | (fmt === "png")) {
  render(arg, fmt);
} else {
  console.error(`ERROR: ${fmt} an unsupported format`);
}
