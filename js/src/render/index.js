const { writeFile } = require("fs");
const svg = require("./svg");
const png = require("./png");

const svgHeader =
  '<?xml version="1.0" encoding="utf-8"?>\n' +
  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ' +
  '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n';

module.exports = (arg, fmt) => {
  svg(arg, function (body) {
    const svgBody = (arg.header ? svgHeader : "") + body;
    if (fmt === "svg") {
      const file = arg.output || null;
      if (file) {
        // write to file
        writeFile(file, svgBody, (err) => {
          if (err) throw err;
        });
      } else {
        // write to stdout
        process.stdout.write(svgBody);
      }
    } else if (fmt === "png") {
      png(arg, svgBody);
    } else {
      console.error(`ERROR: ${arg.format} an unsupported format`);
    }
  });
};
