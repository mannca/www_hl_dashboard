import operator
from collections import Counter

import pandas as pd
import plotly.graph_objects as go

from util.code_hierarchy import mapping_to_top_level, mapping_to_description

NUM_CATS_TO_DISPLAY = 20


def generate_bar_graph(tmp_df, description, screen_width):
    counter = Counter()
    for codes in tmp_df.canonical_code:
        for code in codes.split("/"):
            if True or code != "OTHERNONDETERMINABLE":
                counter[code] += 1

    if len(counter) > 0:
        grouped = pd.DataFrame(sorted(counter.items(), key=operator.itemgetter(1), reverse=False))
    else:
        grouped = pd.DataFrame({1: [], 2: []})
    grouped.columns = ["label", "count"]
    grouped["description"] = grouped.label.map(mapping_to_description)
    grouped["top_level"] = grouped.label.map(mapping_to_top_level)
    grouped.dropna(inplace=True)

    max_chars = 40
    if screen_width < 1400:
        max_chars = 20

    grouped["short_description"] = grouped.description.apply(
        lambda x : x if len(x) < max_chars else x[:(max_chars-3)] + "...")

    grouped['x'] = list(range(len(grouped)))

    bars = []

    bars.append(go.Bar(y=grouped.x,
                       x=grouped["count"],
                       hovertext=grouped.top_level + " - " + grouped.description + " / " + grouped.label,
                       orientation="h",
                       )
                )

    fig = go.FigureWidget(data=bars)
    yaxis = dict(
        tickmode='array',
        tickvals=grouped.x,
        ticktext=grouped.short_description
    )
    if len(grouped) > NUM_CATS_TO_DISPLAY:
        yaxis["range"] = [len(grouped) - NUM_CATS_TO_DISPLAY + 0.5, len(grouped) - 0.5]
    layout = go.Layout(
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        yaxis=yaxis,
        margin=dict(l=0, r=0, t=0, b=0),
        dragmode="pan"
    )
    fig.update_layout(layout)

    return fig