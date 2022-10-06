import altair as alt
import pandas as pd
from vega_datasets import data


def plot_bar():
    source = pd.DataFrame(
        {
            "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
        }
    )
    return alt.Chart(source).mark_bar().encode(x="a", y="b")


def plot_map():

    # Data generators for the background
    sphere = alt.sphere()
    graticule = alt.graticule()

    # Source of land data
    source = alt.topo_feature(data.world_110m.url, "countries")

    # Layering and configuring the components
    return (
        alt.layer(
            alt.Chart(sphere).mark_geoshape(fill="lightblue"),
            alt.Chart(graticule).mark_geoshape(stroke="white", strokeWidth=0.5),
            alt.Chart(source).mark_geoshape(fill="ForestGreen", stroke="black"),
        )
        .project("naturalEarth1")
        .properties(width=600, height=400)
        .configure_view(stroke=None)
    )


def plot_area():
    source = data.stocks()

    return (
        alt.Chart(source)
        .transform_filter('datum.symbol==="GOOG"')
        .mark_area(
            line={"color": "darkgreen"},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="white", offset=0),
                    alt.GradientStop(color="darkgreen", offset=1),
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0,
            ),
        )
        .encode(alt.X("date:T"), alt.Y("price:Q"))
    )


def plot_wheat_wages():
    base_wheat = alt.Chart(data.wheat.url).transform_calculate(
        year_end="+datum.year + 5"
    )

    base_monarchs = alt.Chart(data.monarchs.url).transform_calculate(
        offset="((!datum.commonwealth && datum.index % 2) ? -1: 1) * 2 + 95",
        off2="((!datum.commonwealth && datum.index % 2) ? -1: 1) + 95",
        y="95",
        x="+datum.start + (+datum.end - +datum.start)/2",
    )

    bars = base_wheat.mark_bar(**{"fill": "#aaa", "stroke": "#999"}).encode(
        x=alt.X("year:Q", axis=alt.Axis(format="d", tickCount=5)),
        y=alt.Y("wheat:Q", axis=alt.Axis(zindex=1)),
        x2=alt.X2("year_end"),
    )

    area = base_wheat.mark_area(**{"color": "#a4cedb", "opacity": 0.7}).encode(
        x=alt.X("year:Q"), y=alt.Y("wages:Q")
    )

    area_line_1 = area.mark_line(**{"color": "#000", "opacity": 0.7})
    area_line_2 = area.mark_line(**{"yOffset": -2, "color": "#EE8182"})

    top_bars = base_monarchs.mark_bar(stroke="#000").encode(
        x=alt.X("start:Q"),
        x2=alt.X2("end"),
        y=alt.Y("y:Q"),
        y2=alt.Y2("offset"),
        fill=alt.Fill(
            "commonwealth:N", legend=None, scale=alt.Scale(range=["black", "white"])
        ),
    )

    top_text = base_monarchs.mark_text(
        **{"yOffset": 14, "fontSize": 9, "fontStyle": "italic"}
    ).encode(x=alt.X("x:Q"), y=alt.Y("off2:Q"), text=alt.Text("name:N"))

    return (
        (bars + area + area_line_1 + area_line_2 + top_bars + top_text)
        .properties(width=900, height=400)
        .configure_axis(title=None, gridColor="white", gridOpacity=0.25, domain=False)
        .configure_view(stroke="transparent")
    )


def make_animal_df():
    return pd.DataFrame(
        [
            {"country": "Great Britain", "animal": "cattle"},
            {"country": "Great Britain", "animal": "cattle"},
            {"country": "Great Britain", "animal": "cattle"},
            {"country": "Great Britain", "animal": "pigs"},
            {"country": "Great Britain", "animal": "pigs"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "Great Britain", "animal": "sheep"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "cattle"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "pigs"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
            {"country": "United States", "animal": "sheep"},
        ]
    )


def plot_emojis():
    source = make_animal_df()

    return (
        alt.Chart(source)
        .mark_text(size=45, baseline="middle")
        .encode(
            alt.X("x:O", axis=None),
            alt.Y("animal:O", axis=None),
            alt.Row("country:N", header=alt.Header(title="")),
            alt.Text("emoji:N"),
        )
        .transform_calculate(
            emoji="{'cattle': '🐄', 'pigs': '🐖', 'sheep': '🐏'}[datum.animal]"
        )
        .transform_window(x="rank()", groupby=["country", "animal"])
        .properties(width=550, height=140)
    )


def plot_paths():
    source = make_animal_df()

    domains = ["person", "cattle", "pigs", "sheep"]

    shape_scale = alt.Scale(
        domain=domains,
        range=[
            "M1.7 -1.7h-0.8c0.3 -0.2 0.6 -0.5 0.6 -0.9c0 -0.6 -0.4 -1 -1 -1c-0.6 0 -1 0.4 -1 1c0 0.4 0.2 0.7 0.6 0.9h-0.8c-0.4 0 -0.7 0.3 -0.7 0.6v1.9c0 0.3 0.3 0.6 0.6 0.6h0.2c0 0 0 0.1 0 0.1v1.9c0 0.3 0.2 0.6 0.3 0.6h1.3c0.2 0 0.3 -0.3 0.3 -0.6v-1.8c0 0 0 -0.1 0 -0.1h0.2c0.3 0 0.6 -0.3 0.6 -0.6v-2c0.2 -0.3 -0.1 -0.6 -0.4 -0.6z",
            "M4 -2c0 0 0.9 -0.7 1.1 -0.8c0.1 -0.1 -0.1 0.5 -0.3 0.7c-0.2 0.2 1.1 1.1 1.1 1.2c0 0.2 -0.2 0.8 -0.4 0.7c-0.1 0 -0.8 -0.3 -1.3 -0.2c-0.5 0.1 -1.3 1.6 -1.5 2c-0.3 0.4 -0.6 0.4 -0.6 0.4c0 0.1 0.3 1.7 0.4 1.8c0.1 0.1 -0.4 0.1 -0.5 0c0 0 -0.6 -1.9 -0.6 -1.9c-0.1 0 -0.3 -0.1 -0.3 -0.1c0 0.1 -0.5 1.4 -0.4 1.6c0.1 0.2 0.1 0.3 0.1 0.3c0 0 -0.4 0 -0.4 0c0 0 -0.2 -0.1 -0.1 -0.3c0 -0.2 0.3 -1.7 0.3 -1.7c0 0 -2.8 -0.9 -2.9 -0.8c-0.2 0.1 -0.4 0.6 -0.4 1c0 0.4 0.5 1.9 0.5 1.9l-0.5 0l-0.6 -2l0 -0.6c0 0 -1 0.8 -1 1c0 0.2 -0.2 1.3 -0.2 1.3c0 0 0.3 0.3 0.2 0.3c0 0 -0.5 0 -0.5 0c0 0 -0.2 -0.2 -0.1 -0.4c0 -0.1 0.2 -1.6 0.2 -1.6c0 0 0.5 -0.4 0.5 -0.5c0 -0.1 0 -2.7 -0.2 -2.7c-0.1 0 -0.4 2 -0.4 2c0 0 0 0.2 -0.2 0.5c-0.1 0.4 -0.2 1.1 -0.2 1.1c0 0 -0.2 -0.1 -0.2 -0.2c0 -0.1 -0.1 -0.7 0 -0.7c0.1 -0.1 0.3 -0.8 0.4 -1.4c0 -0.6 0.2 -1.3 0.4 -1.5c0.1 -0.2 0.6 -0.4 0.6 -0.4z",
            "M1.2 -2c0 0 0.7 0 1.2 0.5c0.5 0.5 0.4 0.6 0.5 0.6c0.1 0 0.7 0 0.8 0.1c0.1 0 0.2 0.2 0.2 0.2c0 0 -0.6 0.2 -0.6 0.3c0 0.1 0.4 0.9 0.6 0.9c0.1 0 0.6 0 0.6 0.1c0 0.1 0 0.7 -0.1 0.7c-0.1 0 -1.2 0.4 -1.5 0.5c-0.3 0.1 -1.1 0.5 -1.1 0.7c-0.1 0.2 0.4 1.2 0.4 1.2l-0.4 0c0 0 -0.4 -0.8 -0.4 -0.9c0 -0.1 -0.1 -0.3 -0.1 -0.3l-0.2 0l-0.5 1.3l-0.4 0c0 0 -0.1 -0.4 0 -0.6c0.1 -0.1 0.3 -0.6 0.3 -0.7c0 0 -0.8 0 -1.5 -0.1c-0.7 -0.1 -1.2 -0.3 -1.2 -0.2c0 0.1 -0.4 0.6 -0.5 0.6c0 0 0.3 0.9 0.3 0.9l-0.4 0c0 0 -0.4 -0.5 -0.4 -0.6c0 -0.1 -0.2 -0.6 -0.2 -0.5c0 0 -0.4 0.4 -0.6 0.4c-0.2 0.1 -0.4 0.1 -0.4 0.1c0 0 -0.1 0.6 -0.1 0.6l-0.5 0l0 -1c0 0 0.5 -0.4 0.5 -0.5c0 -0.1 -0.7 -1.2 -0.6 -1.4c0.1 -0.1 0.1 -1.1 0.1 -1.1c0 0 -0.2 0.1 -0.2 0.1c0 0 0 0.9 0 1c0 0.1 -0.2 0.3 -0.3 0.3c-0.1 0 0 -0.5 0 -0.9c0 -0.4 0 -0.4 0.2 -0.6c0.2 -0.2 0.6 -0.3 0.8 -0.8c0.3 -0.5 1 -0.6 1 -0.6z",
            "M-4.1 -0.5c0.2 0 0.2 0.2 0.5 0.2c0.3 0 0.3 -0.2 0.5 -0.2c0.2 0 0.2 0.2 0.4 0.2c0.2 0 0.2 -0.2 0.5 -0.2c0.2 0 0.2 0.2 0.4 0.2c0.2 0 0.2 -0.2 0.4 -0.2c0.1 0 0.2 0.2 0.4 0.1c0.2 0 0.2 -0.2 0.4 -0.3c0.1 0 0.1 -0.1 0.4 0c0.3 0 0.3 -0.4 0.6 -0.4c0.3 0 0.6 -0.3 0.7 -0.2c0.1 0.1 1.4 1 1.3 1.4c-0.1 0.4 -0.3 0.3 -0.4 0.3c-0.1 0 -0.5 -0.4 -0.7 -0.2c-0.3 0.2 -0.1 0.4 -0.2 0.6c-0.1 0.1 -0.2 0.2 -0.3 0.4c0 0.2 0.1 0.3 0 0.5c-0.1 0.2 -0.3 0.2 -0.3 0.5c0 0.3 -0.2 0.3 -0.3 0.6c-0.1 0.2 0 0.3 -0.1 0.5c-0.1 0.2 -0.1 0.2 -0.2 0.3c-0.1 0.1 0.3 1.1 0.3 1.1l-0.3 0c0 0 -0.3 -0.9 -0.3 -1c0 -0.1 -0.1 -0.2 -0.3 -0.2c-0.2 0 -0.3 0.1 -0.4 0.4c0 0.3 -0.2 0.8 -0.2 0.8l-0.3 0l0.3 -1c0 0 0.1 -0.6 -0.2 -0.5c-0.3 0.1 -0.2 -0.1 -0.4 -0.1c-0.2 -0.1 -0.3 0.1 -0.4 0c-0.2 -0.1 -0.3 0.1 -0.5 0c-0.2 -0.1 -0.1 0 -0.3 0.3c-0.2 0.3 -0.4 0.3 -0.4 0.3l0.2 1.1l-0.3 0l-0.2 -1.1c0 0 -0.4 -0.6 -0.5 -0.4c-0.1 0.3 -0.1 0.4 -0.3 0.4c-0.1 -0.1 -0.2 1.1 -0.2 1.1l-0.3 0l0.2 -1.1c0 0 -0.3 -0.1 -0.3 -0.5c0 -0.3 0.1 -0.5 0.1 -0.7c0.1 -0.2 -0.1 -1 -0.2 -1.1c-0.1 -0.2 -0.2 -0.8 -0.2 -0.8c0 0 -0.1 -0.5 0.4 -0.8z",
        ],
    )

    color_scale = alt.Scale(
        domain=domains,
        range=[
            "rgb(162,160,152)",
            "rgb(194,81,64)",
            "rgb(93,93,93)",
            "rgb(91,131,149)",
        ],
    )

    return (
        alt.Chart(source)
        .mark_point(filled=True, opacity=1, size=100)
        .encode(
            alt.X("x:O", axis=None),
            alt.Y("animal:O", axis=None),
            alt.Row("country:N", header=alt.Header(title="")),
            alt.Shape("animal:N", legend=None, scale=shape_scale),
            alt.Color("animal:N", legend=None, scale=color_scale),
        )
        .transform_window(x="rank()", groupby=["country", "animal"])
        .properties(width=550, height=140)
    )
