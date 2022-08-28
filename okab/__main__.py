import subprocess
import sys

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

def main():
    sys.exit(
        subprocess.call([str(files("okab") / "vega" / "vega-resvg"), *sys.argv[1:]])
    )


if __name__ == "__main__":
    main()
