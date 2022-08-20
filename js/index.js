var vega = require("vega");
var vegaLite = require("vega-lite");
const { Resvg } = require('@resvg/resvg-js')

if (process.argv.length !== 5) {
  console.error('expected 3 arguments');
  console.error('direct invocation discouraged')
  process.exit(1);
}

const myArgs = process.argv.slice(2);
var spec = JSON.parse(myArgs[0]);
const embedOpt = JSON.parse(myArgs[1]);
const format = myArgs[2];

if (embedOpt.mode === "vega-lite") {
  vegaLite = typeof vegaLite === "undefined" ? vl : vegaLite;
  try {
    const compiled = vegaLite.compile(spec);
    spec = compiled.spec;
  } catch (error) {
    console.log(JSON.stringify({ error: error.toString() }));
    return;
  }
}

if (format === "vega") {
  console.log(JSON.stringify({ result: spec }));
} else {
  var view = new vega.View(vega.parse(spec), { renderer: "none" });

  if (format === "svg") {
    view
      .toSVG()
      .then(function(result) {
        console.log(JSON.stringify({ result: result }));
      })
      .catch(function(err) {
        console.log(JSON.stringify({ error: err.toString() }));
      });
  } else if (format === "png") {
    view
      .toSVG()
      .then(function(result) {
        svg2png(result)
      })
      .catch(function(err) {
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
      mode: 'zoom',
      value: embedOpt.scaleFactor || 1
    },
    logLevel: 'off',
  }

  const resvg = new Resvg(svg, opts)
  const pngData = resvg.render()
  const pngBuffer = pngData.asPng()
  const dataImagePrefix = `data:image/png;base64,`
  console.log(JSON.stringify({ result: `${dataImagePrefix}${pngBuffer.toString('base64')}` }))
}
