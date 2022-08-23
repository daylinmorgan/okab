const fs = require("fs");
const vega = require("vega");
const vegaLite = require("vega-lite");
const { Resvg } = require("@resvg/resvg-js");
const yargs = require("yargs/yargs");

var argv = yargs(process.argv.slice(2))
  .usage("Usage: vega-resvg --spec [file] --opts [json opts] --format [format]")
  .option("spec", {
    describe: "file with vega/vega-lite json",
  })
  .option("opts", {
    describe: "json string with embedOpts",
  })
  .option("format", {
    describe: "output data type",
    choices: ["vega", "svg", "png"],
  })
  .demandOption(["spec", "opts", "format"])
  .wrap(72)
  .version(false).argv;

try {
  var spec = JSON.parse(fs.readFileSync(argv.spec, "utf8"));
} catch (error) {
  console.log(JSON.stringify({ error: error.toString() }));
  process.exit(1);
}

const embedOpt = JSON.parse(argv.opts);
const format = argv.format;

if (embedOpt.mode === "vega-lite") {
  try {
    const compiled = vegaLite.compile(spec);
    spec = compiled.spec;
  } catch (error) {
    console.log(JSON.stringify({ error: error.toString() }));
    process.exit(1);
  }
}

if (format === "vega") {
  console.log(JSON.stringify({ result: spec }));
} else {
  var view = new vega.View(vega.parse(spec), { renderer: "none" });

  if (format === "svg") {
    view
      .toSVG()
      .then(function (result) {
        console.log(JSON.stringify({ result: result }));
      })
      .catch(function (err) {
        console.log(JSON.stringify({ error: err.toString() }));
      });
  } else if (format === "png") {
    view
      .toSVG()
      .then(function (result) {
        svg2png(result);
      })
      .catch(function (err) {
        console.log(JSON.stringify({ error: err.toString() }));
      });
  } else {
    const error = "Unrecognized format: " + format;
    console.log(JSON.stringify({ error: error }));
  }
}

async function svg2png(svg) {
  const opts = {
    fitTo: {
      mode: "zoom",
      value: embedOpt.scaleFactor || 1,
    },
    logLevel: "off",
  };

  const resvg = new Resvg(svg, opts);
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  const dataImagePrefix = `data:image/png;base64,`;
  console.log(
    JSON.stringify({
      result: `${dataImagePrefix}${pngBuffer.toString("base64")}`,
    })
  );
}
