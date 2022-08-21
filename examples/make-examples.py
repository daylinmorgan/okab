from altair_saver_resvg import ResvgSaver
from altair_saver import save

from charts import plot_bar, plot_map, plot_area, plot_paths


def main():
    # plot_bar().save("example.vl.json")

    # chart.save doesn't catch new method when json?
    save(plot_bar(), "example-bar-compiled.json", method=ResvgSaver, fmt="vega")

    plot_bar().save("example-bar.svg", method=ResvgSaver)
    plot_bar().save("example-bar.png", method=ResvgSaver)
    plot_bar().save("example-bar-scaled.png", method=ResvgSaver, scale_factor=5.0)

    plot_map().save("example-map.png", method=ResvgSaver)
    plot_area().save("example-area.png", method=ResvgSaver)
    plot_paths().save("example-paths.png", method=ResvgSaver)


if __name__ == "__main__":
    main()
