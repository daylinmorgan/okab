import { readFileSync } from "fs";
import { View, parse } from "vega";
import { compile } from "vega-lite";
import { Resvg } from "@resvg/resvg-js";
import yargs from "yargs/yargs";

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
  var spec = JSON.parse(readFileSync(argv.spec, "utf8"));
} catch (error) {
  console.log(JSON.stringify({ error: error.toString() }));
  process.exit(1);
}

const embedOpt = JSON.parse(argv.opts);
const format = argv.format;

if (embedOpt.mode === "vega-lite") {
  try {
    const compiled = compile(spec);
    spec = compiled.spec;
  } catch (error) {
    console.log(JSON.stringify({ error: error.toString() }));
    process.exit(1);
  }
}

if (format === "vega") {
  console.log(JSON.stringify({ result: spec }));
} else {
  var view = new View(parse(spec), { renderer: "none" });

  if (format === "svg") {
    view
      .toSVG(
      embedOpt.scaleFactor || 1
      )
      .then(function (result) {
        console.log(JSON.stringify({ result: result }));
      })
      .catch(function (err) {
        console.log(JSON.stringify({ error: err.toString() }));
      });
  } else if (format === "png") {
    view
      .toSVG(
      embedOpt.scaleFactor || 1
      )
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
