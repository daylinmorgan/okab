import subprocess
import sys

try:
    # python < 3.9
    from importlib_resources import files
except ImportError:
    from importlib.resources import files


def main():
    sys.exit(
        subprocess.call([str(files("okab") / "vega" / "vega-resvg"), *sys.argv[1:]])
    )


if __name__ == "__main__":
    main()
