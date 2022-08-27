// modified from vega-cli (modified further from vega-lite-cli)

const vega = require("vega");
const path = require("path");
const read = require("../read");
const vegaLite = require("vega-lite");

const Levels = {
  error: vega.Error,
  warn: vega.Warn,
  info: vega.Info,
  debug: vega.Debug,
  trace: vega.Debug,
};

module.exports = (arg, callback) => {
  // set baseURL, if specified. default to input spec directory
  const base = arg.base || (arg.i ? path.dirname(arg.i) : null);

  // set log level, defaults to logging warning messages
  const loglevel = Levels[String(arg.loglevel).toLowerCase()] || vega.Warn;

  // load config file, if specified
  const config = arg.config ? read(arg.config) : null;

  // set output image scale factor
  const scale = arg.scale || undefined;
  // use a seeded random number generator, if specified
  if (typeof arg.seed !== "undefined") {
    if (Number.isNaN(arg.seed))
      throw "Illegal seed value: must be a valid number.";
    vega.setRandom(vega.randomLCG(arg.seed));
  }

  // locale options, load custom number/time formats if specified
  const locale = {
    number: arg.locale ? read(arg.locale) : null,
    time: arg.timeFormat ? read(arg.timeFormat) : null,
  };

  // instantiate view and invoke headless render method
  function render(spec) {
    const vgSpec = arg.mode.includes("vega-lite")
      ? vegaLite.compile(spec, { config }).spec
      : spec;
    const view = new vega.View(vega.parse(vgSpec), {
      locale: locale, // set locale options
      loader: vega.loader({ baseURL: base }), // load files from base path
      logger: vega.logger(loglevel, "error"), // route all logging to stderr
      renderer: "none", // no primary renderer needed
    }).finalize(); // clear any timers, etc
    return view.toSVG(scale).then((_) => callback(_));
  }

  // read input from file or stdin
  read(arg.i)
    .then((text) => render(JSON.parse(text)))
    .catch((err) => console.error(err));
};
