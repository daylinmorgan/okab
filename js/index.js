const fs = require("fs");
const path = require("path");
const vega = require("vega");
const vegaLite = require("vega-lite");
const { Resvg } = require("@resvg/resvg-js");
const yargs = require("yargs/yargs");

var argv = yargs(process.argv.slice(2))
  .usage("Usage: vega-resvg --spec [file] --opts [json opts] --format [format]")
  .option("spec", {
    describe: "vega/vega-lite json",
  })
  .option("opts", {
    describe: "embedOpts json string",
  })
  .option("format", {
    describe: "output data type",
    choices: ["vega", "svg", "png"],
  })
  .option("output", {
    describe: "output file",
  })
  .option("log", {
    describe: "log level of resvg",
    choices: ["off", "error", "warn", "info", "debug", "trace"],
    default: "off",
  })
  .demandOption(["spec", "opts", "format"])
  .wrap(88)
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
  if (argv.output) {
    fs.writeFileSync(argv.output, spec);
  } else {
    console.log(JSON.stringify({ result: spec }));
  }
} else {
  var view = new vega.View(vega.parse(spec), { renderer: "none" });

  if (format === "svg") {
    view
      .toSVG(embedOpt.scaleFactor || 1)
      .then(function (result) {
        if (argv.output) {
          fs.writeFileSync(argv.output, result);
        } else {
          console.log(JSON.stringify({ result: result }));
        }
      })
      .catch(function (err) {
        console.log(JSON.stringify({ error: err.toString() }));
      });
  } else if (format === "png") {
    view
      .toSVG(embedOpt.scaleFactor || 1)
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
    logLevel: argv.log,
    font: {
      // two paths are included for now for debugging purposes
      fontDirs: [
        path.join(path.dirname(process.execPath), "fonts"),
        path.join(__dirname, "./assets/fonts"),
      ],
      loadSystemFonts: true,
      defaultFontFamily: "Robot",
    }, // todo: make font loading conditional and configurable
  };

  const resvg = new Resvg(svg, opts);
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  const dataImagePrefix = `data:image/png;base64,`;

  if (argv.output) {
    try {
      fs.writeFileSync(argv.output, pngBuffer);
    } catch (error) {
      console.log(JSON.stringify({ error: error.toString() }));
      process.exit(1);
    }
  } else {
    console.log(
      JSON.stringify({
        result: `${dataImagePrefix}${pngBuffer.toString("base64")}`,
      })
    );
  }
}
