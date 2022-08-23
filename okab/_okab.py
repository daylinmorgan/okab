import base64
import json
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

import altair as alt
from altair_saver.savers import Saver
from altair_saver.types import JSONDict, MimebundleContent


class JavascriptError(RuntimeError):
    pass


class ExecutionError(RuntimeError):
    pass


def vega(spec: JSONDict, opt: Optional[JSONDict], fmt: str) -> JSONDict:
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(json.dumps(spec).encode())
        fp.seek(0)

        # TODO: verify executable is available and executable
        cmd = (
            str(files("okab") / "vega" / "vega-resvg"),
            "--spec",
            fp.name,
            "--opts",
            json.dumps(opt),
            "--format",
            fmt,
        )

        try:
            p = subprocess.run(
                cmd,
                capture_output=True,
                universal_newlines=True,
            )

        except OSError:
            raise ExecutionError(
                "Problems executing vega-resvg, check you installed the version for your platform\n"
                "cmd executed: \n"
                "  " + " ".join(cmd)
            )

    if p.returncode != 0:
        raise ExecutionError(
            f"failed to execute vega-resvg, see below: \n{p.stdout}\n{p.stderr}"
        )

    try:
        return json.loads(p.stdout)
    except json.decoder.JSONDecodeError:
        raise JavascriptError(f"Problems parsing vega output:\n {p.stdout}")


class OkabSaver(Saver):
    """Save charts using okab w/ vega & resvg."""

    valid_formats: Dict[str, List[str]] = {
        "vega": ["png", "svg"],
        "vega-lite": ["png", "svg", "vega"],
    }

    def __init__(
        self,
        spec: JSONDict,
        mode: Optional[str] = None,
        embed_options: Optional[JSONDict] = None,
        vega_version: str = alt.VEGA_VERSION,
        vegalite_version: str = alt.VEGALITE_VERSION,
        vegaembed_version: str = alt.VEGAEMBED_VERSION,
        scale_factor: Optional[float] = 1,
        **kwargs: Any,
    ) -> None:

        if scale_factor != 1:
            embed_options = embed_options or {}
            embed_options.setdefault("scaleFactor", scale_factor)
        super().__init__(
            spec=spec,
            mode=mode,
            embed_options=embed_options,
            vega_version=vega_version,
            vegalite_version=vegalite_version,
            vegaembed_version=vegaembed_version,
            **kwargs,
        )

    def _extract(self, fmt: str) -> MimebundleContent:

        opt = self._embed_options.copy()
        opt["mode"] = self._mode
        result = vega(self._spec, opt, fmt)

        if "error" in result:
            raise JavascriptError(result["error"])
        return result["result"]

    def _serialize(self, fmt: str, content_type: str) -> MimebundleContent:
        out = self._extract(fmt)

        if fmt == "png":
            assert isinstance(out, str)
            return base64.b64decode(out.split(",", 1)[1].encode())
        elif fmt == "svg":
            return out
        elif fmt == "vega":
            return out
        else:
            raise ValueError(f"Unrecognized format: {fmt}")
