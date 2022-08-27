const { createWriteStream } = require("fs");
const vegaLite = require("vega-lite");

module.exports = (arg, vlSpec) => {
  const vgSpec = vegaLite.compile(vlSpec).spec;

  const file = arg.o || null;
  const out = file ? createWriteStream(file) : process.stdout;

  if (arg.p) {
    out.write(compactStringify(vgSpec) + "\n");
  } else {
    out.write(JSON.stringify(vgSpec) + "\n");
  }
};
