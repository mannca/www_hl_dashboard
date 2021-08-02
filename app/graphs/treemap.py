import pandas as pd
import plotly.express as px

from util.code_hierarchy import mapping_to_top_level, mapping_to_description


def generate_treemap(tmp_df, description):
    # Preprocessing
    canonical_code_preprocessed = tmp_df.canonical_code.apply(lambda x: "multiple topics" if "/" in x else x)
    if len(set(canonical_code_preprocessed)) == 1 and list(canonical_code_preprocessed)[0] == "multiple topics":
        l = []
        for multiple_topics_code in list(tmp_df.canonical_code):
            for code in multiple_topics_code.split("/"):
                l.append(code)
        canonical_code_preprocessed = pd.Series(l)
        description += " (displaying counts of topics, not of respondents, so some women will be double counted)"
    # Group the data
    vc = canonical_code_preprocessed.value_counts()
    grouped = pd.DataFrame({"label": vc.index, "count": vc.values})
    grouped["top_level"] = grouped.label.map(mapping_to_top_level)
    # Generate the description
    grouped['filter'] = description
    # Rename the country column
    grouped.rename(columns={"alpha3country": "count"}, inplace=True)

    grouped["description"] = grouped.label.map(mapping_to_description)

    # Make the treemap
    treemap_figure = px.treemap(grouped.dropna(), path=['filter', 'top_level', 'label'], values='count',
                                hover_data=['description'],
                                )
    treemap_figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return treemap_figure