from altair_saver import save
from charts import (
    plot_area,
    plot_bar,
    plot_emojis,
    plot_map,
    plot_paths,
    plot_wheat_wages,
)

from okab.saver import OkabSaver


def main():
    # plot_bar().save("example.vl.json")

    # chart.save doesn't catch new method when json?
    save(plot_bar(), "example-bar-compiled.json", method=OkabSaver, fmt="vega")

    plot_bar().save("example-bar.svg", method=OkabSaver)
    plot_bar().save("example-bar.png", method=OkabSaver)
    plot_bar().properties(width=1000,height=1000).save("example-bar-large.png", method=OkabSaver)
    plot_bar().save("example-bar-scaled.png", method=OkabSaver, scale_factor=5.0)

    plot_map().save("example-map.png", method=OkabSaver)
    plot_area().save("example-area.png", method=OkabSaver)
    plot_paths().save("example-paths.png", method=OkabSaver)
    plot_emojis().save("example-emojis.png", method=OkabSaver)
    plot_wheat_wages().save("example-wheat-wages.png", method=OkabSaver)


if __name__ == "__main__":
    main()
