import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

TOTAL_NUMBERS_CARD = [
    dbc.CardHeader("Number of responses"),
    dbc.CardBody(
        [
            dcc.Loading(
                dcc.Graph(
                    id='indicator-graph',
                    figure={
                        'data': [],
                        'layout': {
                            'height': 30,
                            'xaxis': {'visible': False},
                            'yaxis': {'visible': False},
                        }
                    },
                    config={'displayModeBar': False},
                ),
                className='svg-container',
                style={'height': 150},
            ),
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


def generate_histogram_card(desc, id):
    return [
        dbc.CardHeader(html.H5(desc)),
        dbc.CardBody(
            [
                dcc.Loading(
                    id="loading-" + id,
                    children=[
                        dbc.Alert(
                            "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                            id="no-data-alert-" + id,
                            color="warning",
                            style={"display": "none"},
                        ),
                        dcc.Graph(id=id),
                    ],
                    type="default",
                )
            ],
            style={"marginTop": 0, "marginBottom": 0},
        ),
    ]


COUNTRY_HISTOGRAM_CARD = generate_histogram_card("Country histogram", "country-graph")
TOPLEVEL_HISTOGRAM_CARD = generate_histogram_card("Top level category histogram", "top-level-cat-graph")
CAT_HISTOGRAM_CARD = generate_histogram_card("Category histogram", "cat-graph")
AGE_HISTOGRAM_CARD = generate_histogram_card("Age histogram", "age-graph")

data_table = dash_table.DataTable(
    columns=[
        {'name': 'Country', 'id': 'canonical_country', 'type': 'text'},
        {'name': 'Category', 'id': 'code', 'type': 'text'},
        {'name': 'Response', 'id': 'raw_response', 'type': 'text'},
        {'name': 'Age', 'id': 'age', 'type': 'text'},
    ],
    id='datatable-responses',
    page_current=0,
    page_size=10,
    filter_action='native',
    style_table={
        'height': 400,
    },
    style_data={
        'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    }
)
RESPONSE_TABLE_CARD = [
    dbc.CardHeader("Responses"),
    dbc.CardBody(
        [
            data_table
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

MAP_CARD = [
    dbc.CardHeader("Map view"),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-map",
                children=[
                    html.P("Responses count by country"),
                    dcc.Graph(
                        id="map",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

WORDCLOUD_CARD = [
    dbc.CardHeader("Most frequently used words in queries"),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-frequencies",
                            children=[dcc.Graph(id="frequency_figure")],
                            type="default",
                        )
                    ),
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[dcc.Graph(id="bank-treemap")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud",
                                                children=[
                                                    dcc.Graph(id="bank-wordcloud")
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]

BIGRAMS_CARD = [
    dbc.CardHeader("Two- and three- word phrases"),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert2",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs2",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-bigrams",
                                                children=[dcc.Graph(id="bigrams_graph")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-trigrams",
                                                children=[
                                                    dcc.Graph(id="trigrams_graph")
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]