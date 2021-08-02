import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from util.constants import MAIN_COLOUR, SECONDARY_COLOUR_LESS_FAINT
from util.country_filters import country_lookup

# This is nominally the coordinates of the capital of each country
# but where they appear too close together on the map I have shifted them slightly.
# All lat/longs are definitely inside the country that they are supposed to be in,
# but they are sometimes not the capital if that capital is very close to the capital of another country.
country_to_lat_lon = {"PAK": [33.6844 + 1, 73.0479 - 1],
                      "IND": [28.7041 - 2, 77.1025 + 2],
                      "MEX": [19.4326, -99.1332],
                      "TZA": [-6.1630, 35.7516],
                      "KEN": [-1.2921, 36.8219 + 3],  # def in Kenya
                      "UGA": [0.3476 + 2, 32.5825 - 1],  # def in Uganda
                      "MWI": [-13.9626, 33.7741],
                      "NGA": [9.0765 + 1, 7.3986 - 1],  # def in Nigeria
                      "CMR": [3.8480 - 1, 11.5021 + 1]}  # def in Cameroon


# returns choropleth map figure based on status filter
def chloropleth_map(tmp_df, title):
    vc = tmp_df.alpha3country.value_counts()
    tmp_df_grouped = pd.DataFrame({"country code": vc.index, "number of responses": vc.values})
    tmp_df_grouped["country"] = tmp_df_grouped["country code"].map(country_lookup)

    fig = px.choropleth(tmp_df_grouped, locations="country code",
                        color="number of responses",  # lifeExp is a column of gapminder
                        hover_name="country",  # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=title
                        )
    fig.update_layout(go.Layout(
        dragmode="select",  # don't scroll the map
    ))
    fig.update_geos(projection_type="natural earth")

    return fig


def bubble_map(df1, df2, desc1, desc2):
    vc = df1.alpha3country.value_counts()
    tmp_df_grouped1 = pd.DataFrame({"country code": vc.index, "number of responses": vc.values})
    tmp_df_grouped1["country"] = tmp_df_grouped1["country code"].map(country_lookup)

    vc = df2.alpha3country.value_counts()
    tmp_df_grouped2 = pd.DataFrame({"country code": vc.index, "number of responses": vc.values})
    tmp_df_grouped2["country"] = tmp_df_grouped2["country code"].map(country_lookup)

    tmp_df_grouped1["filter"] = desc1
    tmp_df_grouped2["filter"] = desc2

    if desc1 != desc2:
        tmp_df_grouped1 = tmp_df_grouped1.append(tmp_df_grouped2)

    fig = px.scatter_geo(tmp_df_grouped1, locations="country code",
                         color="filter",
                         hover_name="country",
                         size="number of responses",
                         projection="natural earth",
                         title=desc1 + " vs " + desc2,
                         color_discrete_map={desc2: SECONDARY_COLOUR_LESS_FAINT, desc1: MAIN_COLOUR}
                         )
    fig.update_layout(go.Layout(
        dragmode="select",  # don't scroll the map
    ))

    return fig


BUBBLE_SIZE = 400


def bubble_map_2(df1, df2, desc1, desc2, is_filters_identical):
    desc2 += " (normalized)"

    vc = df1.alpha3country.value_counts()
    tmp_df_grouped1 = pd.DataFrame({"country code": vc.index, "number of responses": vc.values})
    tmp_df_grouped1["country"] = tmp_df_grouped1["country code"].map(country_lookup)

    vc = df2.alpha3country.value_counts()
    tmp_df_grouped2 = pd.DataFrame({"country code": vc.index, "number of responses": vc.values})
    tmp_df_grouped2["country"] = tmp_df_grouped2["country code"].map(country_lookup)

    tmp_df_grouped1["filter"] = desc1
    tmp_df_grouped2["filter"] = desc2

    if len(tmp_df_grouped1) > 0:
        max1 = max(tmp_df_grouped1['number of responses'])
    else:
        max1 = 1

    if len(tmp_df_grouped2) > 0:
        max2 = max(tmp_df_grouped2['number of responses'])
    else:
        max2 = 1

    scale = {desc2: max2 / BUBBLE_SIZE,
             desc1: max1 / BUBBLE_SIZE}

    title = desc1
    if not is_filters_identical:
        tmp_df_grouped1 = tmp_df_grouped1.append(tmp_df_grouped2)
        title += "<br>vs " + desc2

    tmp_df_grouped1["lat"] = tmp_df_grouped1["country code"].apply(lambda c: country_to_lat_lon[c][0])
    tmp_df_grouped1["lon"] = tmp_df_grouped1["country code"].apply(lambda c: country_to_lat_lon[c][1])

    tmp_df_grouped1['text'] = tmp_df_grouped1['country'] + '<br>' + (tmp_df_grouped1['number of responses']).astype(
        str) + " women"

    colour_discrete_map = {desc2: SECONDARY_COLOUR_LESS_FAINT, desc1: MAIN_COLOUR}

    fig = go.Figure()

    for this_filter in set(tmp_df_grouped1["filter"]):

        df_sub = tmp_df_grouped1[tmp_df_grouped1["filter"] == this_filter]
        this_scale = scale[this_filter]
        if this_scale == 0:
            this_scale = 1
        fig.add_trace(go.Scattergeo(
            lon=df_sub['lon'],
            lat=df_sub['lat'],
            text=df_sub['text'],
            marker=dict(
                size=df_sub['number of responses'] / this_scale,
                color=colour_discrete_map[this_filter],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area',
            ),
            name=this_filter))

    fig.update_layout(
        showlegend=True,
        geo=dict(
            scope='world',
            landcolor='rgb(217, 217, 217)',
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.2,
        xanchor="left",
        x=0.01,
    ))

    fig.update_geos(projection_type="natural earth")

    return fig