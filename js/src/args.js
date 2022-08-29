// modified from vega-lite-cli

exports.args = () => {
  const helpText = `Usage: okab -i [vega-json|vega-lite-json] -f [format]

    If no -o/--output specified  writes to stdout.
    For errors and log messages, writes to stderr.

    To load data, you may need to set a base directory:
    For web retrieval, use '-b http://host/data/'.
    For files, use '-b file:///dir/data/' (absolute) or '-b data/' (relative).`;

  const args = require("yargs").usage(helpText).demand(0);

  // helper command to print executable path
  args.command("show-path", false, function () {
    console.log(process.execPath);
    process.exit(0);
  });

  args
    .string("i")
    .alias("i", "input")
    .describe("i", "vega/vega-lite json spec")
    .demandOption("i");

  args.string("o").alias("o", "output").describe("o", "output file path");
  args
    .string("f")
    .alias("f", "format")
    .describe("f", 'output format. One of "svg","png", or "vega".');

  args
    .string("m")
    .alias("m", "mode")
    .describe("m", "run mode")
    .default("m", "vega-lite");

  args
    .string("b")
    .alias("b", "base")
    .describe(
      "b",
      "Base directory for data loading. Defaults to the directory of the input spec."
    );

  args
    .string("l")
    .alias("l", "loglevel")
    .describe(
      "l",
      'Level of log messages written to stderr.\nOne of "off" "error", "warn" , "info", "debug" or "trace".'
    )
    .default("l", "off");

  args
    .string("c")
    .alias("c", "config")
    .describe("c", "Vega config object. JSON file.");

  args
    .string("locale")
    .describe("locale", "Number format locale descriptor. JSON file.");

  args
    .string("t")
    .alias("t", "timeFormat")
    .describe("t", "Date/time format locale descriptor. JSON file.");

  args
    .boolean("header")
    .describe("header", "Include XML header and SVG doctype.");

  args
    .number("s")
    .alias("s", "scale")
    .default("s", 1)
    .describe("s", "Output resolution scale factor.");

  args.number("seed").describe("seed", "Seed for random number generation.");

  args
    .boolean("p")
    .alias("p", "pretty")
    .describe("p", "Output human readable/pretty spec.");

  args.alias("h", "help").help("help");

  return args.version().strict().argv;
};

exports.parseFmt = (arg) => {
  const ext = arg.o ? arg.o.split(".").pop() : null;

  if (ext) {
    if (ext == "json") {
      // assume json means compiled vega spec
      return "vega";
    } else {
      return ext;
    }
  } else {
    return "svg";
  }
};

exports.parseMode = (arg) => {
  const modes = ["vega", "vega-lite", "vega-altair", "vega-lite-altair"];
  if (!modes.includes(arg.mode)) {
    console.error(
      `ERROR. unknown mode: ${arg.mode}. Must be one of ${modes.join(", ")}.`
    );
    process.exit(1);
  } else if (arg.mode.includes("altair") && arg.o) {
    console.error(
      "ERROR. --mode *-altair and --output are mutually exclusive. " +
        "If executing okab directly use -m vega or -m vega-lite."
    );
    process.exit(1);
  }
};
