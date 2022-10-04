// modified from vega-lite-cli
const { version } = require("./version.json");

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

  args.options({
    input: {
      alias: "i",
      describe: "vega/vega-lite json spec",
      type: "string",
      demandOption: true,
    },
    output: { alias: "o", describe: "output file path" },
    format: {
      alias: "f",
      describe: 'output format. One of "svg","png", or "vega".',
      type: "string",
    },
    mode: {
      alias: "m",
      describe: "src-output mode",
      default: "vega-lite",
      type: "string",
    },
    base: {
      alias: "b",
      describe:
        "Base directory for data loading. Defaults to the directory of the input spec.",
      type: "string",
    },
    logLevel: {
      alias: "l",
      describe:
        'Level of log messages written to stderr.\nOne of "off" "error", "warn" , "info", "debug" or "trace".',
      default: "off",
      type: "string",
    },
    config: {
      alias: "c",
      describe: "Vega config object. JSON file.",
    },
    locale: {
      describe: "Number format locale descriptor. JSON file.",
    },
    timeFormat: {
      alias: "t",
      describe: "Date/time format locale descriptor. JSON file.",
    },
    header: {
      describe: "Include XML header and SVG doctype.",
    },
    scale: {
      alias: "s",
      default: 1,
      describe: "Output resolution scale factor.",
    },
    seed: {
      describe: "Seed for random number generation.",
    },
    pretty: {
      alias: "p",
      describe: "Output human readable/pretty spec.",
      type: "boolean",
    },
  });

  args.alias("h", "help").help("help");

  return args.version(version).strict().argv;
};

exports.parseFmt = (arg) => {
  const ext = arg.output ? arg.output.split(".").pop() : null;

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
  } else if (arg.mode.includes("altair") && arg.output) {
    console.error(
      "ERROR. --mode *-altair and --output are mutually exclusive. " +
        "If executing okab directly use -m vega or -m vega-lite."
    );
    process.exit(1);
  }
};
