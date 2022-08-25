# Okab

altair + okab = static beauty

## Install

`Okab` is available with `pip` but it is currently in an alpha release as the API is under active development.
Wheels are also available from the [releases](https://github.com/daylinmorgan/okab/releases).

```bash
pip install okab
```

## Usage

To get started using `okab` you can directly access it's `altair_saver` compatible method.
*Note*: `Okab` at present still has a runtime dependency on `altair_saver` but this may change in future releases.

```python
import altair as alt
from okab import OkabSaver

...

chart.save("chart.png",method=OkabSaver,scale_factor=2)
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

## Building from Source

For now the wheels will need to be built manually and the executable copied into the appropriate package directory. This would ultimately be handled at build time by `setuptools`.

### Building `vega-resvg`

To get started you'll need `npm` and `python`.

```bash
cd js
npm install
npm i -g vercel/pkg
```

In order to cross-compile the executable's you'll need to have available the necessary `resvg-js` node add-ons, you can use `./js/get-binaries.sh` to fetch them all.
The necessary binary for your own architecture should be pickup by the initial `npm install`.

To build the executable run the following specifying your target, see `vercel/pkg` for info about supported targets.
Then copy this binary to `okab/vega/vega-resvg`.

```
pkg index.js --no-bytecode --public-packages "*" --public -C GZip --target linux -o vega-resvg
cp vega-resvg ../okab/vega/vega-resvg
```

Finally, build the wheel:

```
python setup.py bdist_wheel
```

You can then install this wheel and test it using the included examples:
```
pip install dist/*.whl
cd examples
python make-examples.py
```

To cross-compile wheels for windows, mac(x64) and linux:
```
cd js
./get-binaries.sh
cd ..
make wheels
```

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
