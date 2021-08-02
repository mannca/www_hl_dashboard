from dash.dependencies import Input, Output


def add_clientside_callbacks_crossfiltering(app):
    # Age graph -> age selector slider
    # This is a callback from selecting an age range on the age graph, to the age control.
    app.clientside_callback(
        """function(count_graph_selected) {
            //alert(JSON.stringify(count_graph_selected));
            var DEFAULT_LOWER_AGE = 14;
            var DEFAULT_UPPER_AGE = 60;
            if (count_graph_selected != null && count_graph_selected["points"].length > 0) {
                var nums = [];
                for (var i = 0; i < count_graph_selected["points"].length; i++) {
                    nums.push(count_graph_selected["points"][i]["pointNumber"]);
                }
                return [Math.min(...nums) + DEFAULT_LOWER_AGE, Math.max(...nums) + DEFAULT_LOWER_AGE + 1];
            }
            return [DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE]; // defaults
        }""",
        Output("year_slider_1", "value"), Input("count_graph", "selectedData"))

    # Tree map -> category dropdown
    # This is a callback from selecting a category on the tree map (main graph), to the category dropdown in the filter box.
    '''app.clientside_callback(
        """function(uber_graph_selected) {
            if (screen.width < 1400) {
                return window.dash_clientside.no_update;
            }
            if (uber_graph_selected != null && uber_graph_selected["points"].length > 0) {
                //var text = uber_graph_selected["points"][0]['label'];
                var text = uber_graph_selected["points"][0]['hovertext'];
                var code = text.split("/")[1];
                return [code.trim()];
            }
            return "";
        }""",
        Output("code_selector_1", "value"), Input("main_graph", "clickData"))'''

    # Map -> country dropdown
    # This is a callback from selecting a country on the world map, to the country dropdown in the filter box.
    app.clientside_callback(
        """function(map_selected) {
            if (map_selected != null && map_selected["points"].length > 0) {
                return [map_selected["points"][0]['text'].replace(/<.+/gi, '')];
            }
            return "";
        }""",
        Output("country_selector_1", "value"), Input("aggregate_graph", "clickData"))

    # Ngrams -> text filter
    # This is a callback from selecting a word in the n-gram view, to filtering all text for that word.
    app.clientside_callback(
        """function(ngram_selected_1) {
            if (ngram_selected_1 != null && ngram_selected_1["points"].length > 0) {
                return ngram_selected_1["points"][0]['label'];
            }
            return "";
        }""",
        Output("text_filter_1", "value"),
        Input("ngram_graph_1", "clickData"))