# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 20:37:21 2021

@author: Cate Mann
"""

import locale
import dash

from dash.dependencies import Input, Output, ClientsideFunction
from flask_caching import Cache

from layout.body import get_body
from util.callbacks import CallbackManager
from util.constants import TIMEOUT
from util.crossfiltering_callbacks import add_clientside_callbacks_crossfiltering
from util.data_loader import get_data
from util.tooltips_callbacks import add_clientside_callbacks_tooltips

locale.setlocale(locale.LC_ALL, '')

# -------------------------- LOAD DATA ---------------------------- #

df_responses = get_data()

callback_manager = CallbackManager(df_responses)

# -------------------------- PROJECT DASHBOARD ---------------------------- #

# Changed for now
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['C:/Users/catie/Documents/MFM/Updated Codes Jan22/app/assets/styles.css']


'''
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')

'''

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"},
    {"name":"google-site-verification", "content":"QCnkA3jOEHxO0ZRM8_DNO1W0lmdBHhEY4CrtVJCObOA"},
    {"name":"description", "content":"We asked over a million women what they want. Explore our health literacy-related survey responses with our interactive dashboard!"}],
    external_scripts=["https://www.googletagmanager.com/gtag/js?id=G-9QN6GRBFKV"]
)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',
    'CACHE_THRESHOLD': 10000
})

server = app.server

# BEFORE PUBLIC DEPLOYMENT
app.config.suppress_callback_exceptions = True

app.layout = get_body()

app.title = 'What Women Want Interactive Health Literacy Dashboard | White Ribbon Alliance'

# -------------------------- GOOGLE ANALYTICS ---------------------------- #
app.scripts.config.serve_locally = False


app.scripts.append_script({
    'external_url': '/assets/gtag.js',
})

# -------------------------- CALLBACK FUNCTIONS ---------------------------- #


# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)


@app.callback(
    [
        Output("well_text", "children"),
        Output("total_desc_1", "children"),
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("total_desc_2", "children"),
        Output("waterText", "children"),
        Output("avg_desc_2", "children"),
        Output("count_graph", "figure"),
        Output("main_graph", "figure"),
        Output("datatable-responses", 'data'),
        Output("aggregate_graph", 'figure'),  # map view
        Output("sample_responses_box", "children"),
        Output("datatable-responses", "page_current")  # reset page to 1
    ],
    [
        Input("country_selector_1", "value"),
        Input("country_selector_2", "value"),
        Input("code_selector_1", "value"),
        Input("code_selector_2", "value"),
        Input("year_slider_1", "value"),
        Input("year_slider_2", "value"),
        Input("text_filter_1", "value"),
        Input("text_filter_2", "value"),
        Input("text_filter_exclude_1", "value"),
        Input("text_filter_exclude_2", "value"),
        Input("screenwidth", "value")
    ],
)
@cache.memoize(timeout=TIMEOUT)
def update_filters_callback(*args):
    return callback_manager.update_filters_callback(*args)


@app.callback(
    [
        Output("ngram_graph_1", "figure"),
        Output("ngram_graph_2", "figure"),
        Output("ngram_graph_3", "figure"),
    ],
    [
        Input("well_text", "children"),
        Input("country_selector_1", "value"),
        Input("country_selector_2", "value"),
        Input("code_selector_1", "value"),
        Input("code_selector_2", "value"),
        Input("year_slider_1", "value"),
        Input("year_slider_2", "value"),
        Input("text_filter_1", "value"),
        Input("text_filter_2", "value"),
        Input("text_filter_exclude_1", "value"),
        Input("text_filter_exclude_2", "value"),
        Input("ngram_filter_checkbox", "value")
    ],
)
@cache.memoize(timeout=TIMEOUT)
def update_filters_callback_ngrams_only(*args):
    # This function should be called last. That's why it has a single dummy input,
    # just to force Dash to trigger it after the main callback which calculates all the graphs except N-grams.
    return callback_manager.update_filters_callback_ngrams_only(*args)


# ----- TOOLTIPS & CROSSFILTERING: ALL CLIENT-SIDE CALLBACKS USING JAVASCRIPT --------- #

add_clientside_callbacks_crossfiltering(app)

add_clientside_callbacks_tooltips(app)

# -------------------------- MAIN ---------------------------- #
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)