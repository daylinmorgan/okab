const path = require("path");
const { createWriteStream } = require("fs");
const { Resvg } = require("@resvg/resvg-js");

module.exports = (arg, svg) => {
  const opts = {
    logLevel: arg.loglevel,
    font: {
      // two paths are included for now for debugging purposes
      fontDirs: [
        path.join(path.dirname(process.execPath), "fonts"),
        path.join(__dirname, "../../assets/fonts"),
      ],
      loadSystemFonts: true,
      defaultFontFamily: "Liberation Sans",
    }, // todo: make font loading conditional and configurable
  };
  const resvg = new Resvg(svg, opts);
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  const dataImagePrefix = `data:image/png;base64,`;

  if (arg.mode.includes("altair")) {
    console.log(`${dataImagePrefix}${pngBuffer.toString("base64")}`);
  } else {
    const file = arg.o || null;
    const out = file ? createWriteStream(file) : process.stdout;
    out.write(pngBuffer);
  }
};
