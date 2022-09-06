# Okab

altair + okab = static beauty

## Install

`Okab` is available with `pip` but it is currently in an alpha release as the API is under active development.
Wheels are also available from the [releases](https://github.com/daylinmorgan/okab/releases).

```bash
pip install okab
```

## Usage

### As an altair-saver method

To get started using `okab` you can directly access it's `altair_saver` compatible method.
*Note*: `Okab` as a python library at present still has a runtime dependency on `altair_saver` but this may change in future releases.

```python
import altair as alt
from okab.saver import OkabSaver

...

chart.save("chart.png",method=OkabSaver,scale_factor=2)
```

### As a standalone CLI

You can provide either `vega-lite` or `vega` specs, please specify the `--mode` to match your spec type, by default `okab` expects `vega-lite`.

```bash
okab -i bar.vl.json -o chart.png
```

See `okab -h` for a list of options.

## Results

<table>
  <tr>
    <th> svg </th>
    <th> png </th>
    <th> png (scale factor 5)</th>
    </tr>
    <tr>
    <td><img src="https://raw.githubusercontent.com/daylinmorgan/okab/main/assets/example-bar.svg" height = "300"></td>
    <td><img src="https://raw.githubusercontent.com/daylinmorgan/okab/main/assets/example-bar.png" height = "300"></td>
    <td><img src="https://raw.githubusercontent.com/daylinmorgan/okab/main/assets/example-bar-scaled.png" height="300"></td>
  </tr>
</table>

## Compiling the Wheels

Currently the wheel generation is highly dependent on `make`.
To get started you can bootstrap your environment.
This rule will generate a virtual environment,
install the python and node dependencies,
and the liberation sans font.

```bash
make bootstrap
```

In order to build the wheels we will need to compile the `okab` js backend into standalone executables for all supported targets.
You can do this ahead of time or as the wheels are built.
Regardless, you'll need to have installed `vercel/pkg`.

```bash
npm install -g pkg
```

If you'd just like to compile a single wheel for your platform you can specify the target to compile the backend.

```bash
TARGET=macosx_10_14_x86_64 make single-wheel
```

To generate all supported platform wheels:

```bash
make wheels
```

## How does it work?

We leverage `vercel/pkg` and distribute self-contained platform-specific executables within the python wheels.
This takes the problems of installing and setting up the needed backends from the user and leaves it to a well crafted CI.

First we need access to the libraries that render our visualizations `vega` & `vega-lite`.
We can use the `vega` API to generate a `view` and easily convert this to `svg`.

Generating appropriate png is a different problem. The `vega` view API can return an `svg` or `canvas` object.
In the browser this uses `HTML canvas`, server-side they rely on `node-canvas`.
This works fine in a properly configured `node` environment,
but `canvas` has a number of system dependencies and caveats that make packaging it with `vercel/pkg` a problem.

Instead, we can take advantage of a different `svg` rendering library [`RazrFalcon/resvg`](https://github.com/RazrFalcon/resvg/) and [`yisibl/resvg-js`](https://github.com/yisibl/resvg-js).

## Acknowledgements

This app is made possible by these great open source projects.

- [Altair](https://github.com/altair-viz/altair)
- [Vega Project](https://github.com/vega)
- [Resvg](https://github.com/RazrFalcon/resvg)
- [Resvg-js](https://github.com/yisibl/resvg-js)
