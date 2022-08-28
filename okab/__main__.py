import subprocess
import sys

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files


def main():
    try:
        sys.exit(subprocess.call([str(files("okab") / "bin" / "okab"), *sys.argv[1:]]))
    except FileNotFoundError:
        print(
            "\n".join(
                [
                    "ERROR: Backend not found.",
                    "  Check that you installed the correct wheel for your platform",
                    "  Note: source distribution is not supported",
                ]
            )
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
