# Import required libraries
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Multi-dropdown options
from util.code_hierarchy import get_menu_items
from util.constants import DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE, YOUTUBE_VIDEO_ID
from util.country_filters import get_unique_countries

data_table = dash_table.DataTable(
    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        "font-family": '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif',
        "text-align": "left",
        "vertical-align": "top",
    },
    columns=[
        {'name': 'Country', 'id': 'canonical_country', 'type': 'text'},
        {'name': 'Topic(s)', 'id': 'description', 'type': 'text'},
        {'name': 'Response', 'id': 'raw_response', 'type': 'text'},
        {'name': 'Age', 'id': 'age_str', 'type': 'text'},
    ],
    id='datatable-responses',
    page_current=0,
    page_size=10
)


def get_tab_contents(id):
    items = [
        html.P(
            ["Select countries"],
            className="control_label isrelative",
        ),
        dcc.Dropdown(
            id="country_selector_" + id,
            options=get_unique_countries(),
            multi=True,
            value="",
            className="dcc_control",
        ),

        html.P(
            ["Select response topics"],
            className="control_label isrelative",
        ),
        dcc.Dropdown(
            id="code_selector_" + id,
            options=get_menu_items(),
            multi=True,
            value="",
            className="dcc_control",
        ),
        html.P(
            ["Filter by age (or select range in histogram):"],
            className="control_label isrelative",
        ),
        dcc.RangeSlider(
            id="year_slider_" + str(id),
            min=DEFAULT_LOWER_AGE,
            max=DEFAULT_UPPER_AGE,
            value=[DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE],
            className="dcc_control",
            marks={
                14: {'label': '14', 'style': {'color': '#77b0b1'}},
                20: {'label': '20', 'style': {'color': '#77b0b1'}},
                30: {'label': '30', 'style': {'color': '#77b0b1'}},
                40: {'label': '40', 'style': {'color': '#77b0b1'}},
                50: {'label': '50', 'style': {'color': '#77b0b1'}},
                60: {'label': '60+', 'style': {'color': '#f50'}}
            }
        ),
        html.Div([
            html.Div([
                html.P(
                    "Filter by keyword",
                    className="control_label",
                ),
                dcc.Input(id="text_filter_" + id, value="", className="dcc_control",
                          debounce=True, spellCheck=True),
                # debounce is for delayed processing so not on every keystroke
            ], className="one-half column"),
            html.Div([
                html.P(
                    "Exclude keyword",
                    className="control_label",
                ),
                dcc.Input(id="text_filter_exclude_" + id, value="", className="dcc_control",
                          debounce=True, spellCheck=True)
            ], className="one-half column")
        ], className="row isrelative"),
    ]
    if id == "1":
        items.append(
            dcc.Dropdown(
                id="ngram_filter_checkbox",
                options=[
                    {'label': 'Show all multi-word phrases', 'value': '0'},
                    {'label': 'Show only multi-word phrases containing filter term', 'value': '1'},
                ],
                multi=False,
                value="0",
                className="dcc_control",
            ),
        )
        items.append(html.Div([html.H3("Drill Down vs Compare To"),
                               html.P(
                                   "To compare health literacy responses from two groups of women, such as the women in different age ranges or countries, use the “Drill down” tab to filter for one group of women, and the “Compare to…” tab to filter for the other."),
                               html.P(
                                   "When using the Dashboard to search through only one group of women's health literacy responses, the responses selected in the “Drill down” tab will show."),
                               html.P(
                                   "3/16"),
                               html.Button("Next tip", id="twtooltipbtn2", className="tooltipbutton"),
                               html.Button("Exit tutorial", id="twtooltipbtnexit2", className="tooltipbutton")
                               ],
                              className="box sb5 twtooltipleft twhide",
                              id="twtooltip2"
                              ), )
        items[0].children.append(html.Div([html.H3("Filter by Country "),
                                           html.P(
                                               "Here you can filter health literacy responses by a particular country, or group of countries, by clicking on the country name in the dropdown."),
                                           html.P(
                                               "You can also select a country by clicking on its bubble in the map view at the far bottom right of the Dashboard."),
                                           html.P(
                                               "4/16"),
                                           html.Button("Next tip", id="twtooltipbtn3", className="tooltipbutton"),
                                           html.Button("Exit tutorial", id="twtooltipbtnexit3",
                                                       className="tooltipbutton")],
                                          className="box sb2 twtooltip twhide",
                                          id="twtooltip3"
                                          ),)
        items[2].children.append(html.Div([html.H3("Filter by Health Literacy Response Topics"),
                                           html.P(
                                               "Here you can drill down into what larger categories these health literacy responses are tied to based on the What Women Want campaign"),
                                           html.P("You can select one or more topics by clicking on the category name in the dropdown."),
                                           html.P(
                                               "You can also select a topic by clicking on its rectangle in the topic bar graph below."),
                                           html.P(
                                               "5/16"),
                                           html.Button("Next tip", id="twtooltipbtn4", className="tooltipbutton"),
                                           html.Button("Exit tutorial", id="twtooltipbtnexit4",
                                                       className="tooltipbutton")],
                                          className="box sb2 twtooltip twhide",
                                          id="twtooltip4"
                                          ))
        items[4].children.append(html.Div([html.H3("Filter by Age"),
                                           html.P(
                                               "To select a specific age range, drag the end dots to include only the ages you are filtering for."),
                                           html.P(
                                               "You can also filter an age range by selecting specific bars on the age bar graph to the right."),
                                           html.P(
                                               "6/16"),
                                           html.Button("Next tip", id="twtooltipbtn5", className="tooltipbutton"),
                                           html.Button("Exit tutorial", id="twtooltipbtnexit5",
                                                       className="tooltipbutton")],
                                          className="box sb2 twtooltip twhide",
                                          id="twtooltip5"
                                          ))
        items[6].children.append(html.Div([html.H3("Filter by Keywords"),
                                           html.P(
                                               'The "Filter by keyword" and "Exclude keyword" options allow for an even closer look at the responses by giving you the power to search for a specific keyword of your choosing.'),
                                           html.P(
                                               "To use this filter, type any word or phrase into the search bar and press Enter/Return on your keyboard. The Dashboard will now show only health literacy responses that contain your searched for word or phrase."),
                                           html.P(
                                               "7/16"),
                                           html.Button("Next tip", id="twtooltipbtn6", className="tooltipbutton"),
                                           html.Button("Exit tutorial", id="twtooltipbtnexit6",
                                                       className="tooltipbutton")],
                                          className="box sb2 twtooltip twhide",
                                          id="twtooltip6"
                                          ))
        items[6].children.append(html.Div([html.H3("Advanced Feature"),
                                           html.P(
                                               'To also see all the short phrases containing your chosen keyword term, select "Show only multi-word phrases containing the filter term."'),
                                           html.P(
                                               "8/16"),
                                           html.Br(),
                                           html.Button("Next tip", id="twtooltipbtn7", className="tooltipbutton"),
                                           html.Button("Exit tutorial", id="twtooltipbtnexit7",
                                                       className="tooltipbutton")],
                                          className="box sb2 crankdown twtooltip twhide",
                                          id="twtooltip7"
                                          ))

    return html.Div(items, className="isrelative")
    return items


def get_ngram_tab_contents(id):
    l = []
    if id == "1":
        l.append(html.P("Click on a bar to view health literacy responses containing a word or phrase."))
    l.append(
        dcc.Loading(
            id="loading-ngram-" + id,
            children=[dcc.Graph(id="ngram_graph_" + id)],
            type="circle",
        )
    )
    return l


def get_body():
    return html.Span([
        dcc.Input(id="screenwidth", value="", style={"display": "none"}),
        dcc.Input(id="screenwidthtrigger", value="", style={"display": "none"}),
        html.Nav([
                html.Ul([
                        html.A(
                            [html.Img(src="assets/white-ribbon-nospace_cropped.png", width=300, id="wra_logo")],
                            href="https://www.whiteribbonalliance.org/",  # className="active",
                            id="wra_logo_link"
                        )
                    ]
                )
            ],
            className="topnav"),
        html.Div([
                dcc.Store(id="aggregate_data"),
                # empty Div to trigger javascript file for graph resizing
                html.Div(id="output-clientside"),
                html.Div(
                    [
                        html.Div([
                            ],
                            className="two columns",
                            id="button2",
                        ),
                        html.Div(
                            [
                                html.H2(["What Women Want Interactive Dashboard: Health Literacy"]),
                                html.Div(
                                    [
                                        '''We asked over a million women and adolescent girls around the world: ''',
                                        html.Br(),
                                        html.I('''What is your one request for quality reproductive and maternal healthcare services?''', style={"font-size": "150%"}),
                                        html.Br(),
                                        ''' Their responses were focused on the very basics: respect and dignity; water, sanitation and hygiene (WASH); qualified healthworkers and quality health facilities; and, underneath it all, the ongoing demand for more information on how to best take care of themselves and their families.''', html.Strong(''' This special health literacy version of the What Women Want Interactive Dashboard allows you to dive deep into responses asking for more information on how to understand and use information and services to help them make the best health-related decisions.'''),''' Use this Dashboard to see what women are asking to find out more about when it comes to their healthcare, and then act and deliver on their demands through your work.''',
                                        html.A(["*"], href="#footnote",
                                               style={"color": "rgb(0,123,133); text-decoration: none;"}),
                                    ],
                                    style={"font-size":"large", "margin-bottom": "0px"}
                                ),
                                html.Div([
                                    html.P("Welcome to the What Women Want Interactive Health Literacy Dashboard Tutorial! "),
                                    html.P(
                                        "This step-by-step tutorial will show you how to use the Dashboard’s filters and controls quickly and easily, letting you dive deeper into responses collected from women and girls through the What Women Want campaign than ever before. "),
                                    html.P(
                                        "1/16"),
                                    html.Button("Next tip", id="twtooltipbtn0", className="tooltipbutton"),
                                    html.Button("Exit tutorial", id="twtooltipbtnexit0",
                                                className="tooltipbutton"),
                                ],
                                    className="box sb2 twtooltiptopright",
                                    id="twtooltip0",
                                ),
                            ],
                            className="intro_blurb eight columns",
                            id="title",
                            style={"align-content": "center", "padding-top":"0px"}
                        ),

                        html.Div([
                            ],
                            className="two columns",
                            id="button",
                        ),
                    ],
                    id="header",
                    style={"margin-bottom": "0px", "margin-top":"0px"},
                    className="row flex-display",
                ),
                html.Div([
                        html.Div(
                            [

                            ],
                            className="two columns",
                            id="button6",
                            style={"margin-top":"0px"}
                        ),
                        html.Div([
                                html.A(
                                    html.Button([html.Span("About What Women Want",)],
                                                id="about-www-button",
                                                className="wra-button",
                                                style={"font-size": "18px"}
                                                ),
                                    href=" https://www.whiteribbonalliance.org/whatwomenwant/",
                                    target="newlearnmore",
                                ),
                                dbc.Tooltip(
                                    "Read more about the What Women Want campaign from the White Ribbon Alliance website",
                                    innerClassName="mouseovertooltip",
                                    target="about-www-button",
                                ),
                                html.Br(className="mobileonly"),
                                html.A(
                                    html.Button("Show tutorial", id="reset-tooltips-button", className="wra-button", style={"font-size": "18px"}),
                                ),
                                dbc.Tooltip(
                                    "Learn how to use the dashboard",
                                    innerClassName="mouseovertooltip",
                                    target="reset-tooltips-button",
                                ),
                                html.Br(className="mobileonly"),
                                # On desktop we overlay the video as an iframe,
                                # on mobile we open it as a link and it will hopefully go to YouTube app
                                html.A(
                                    html.Button("Show video", id="show-video-button", className="wra-button", style={"font-size": "18px"}),
                                    id="show-video-link-desktop"
                                ),
                                dbc.Tooltip(
                                    "Watch a short video about the What Women Want campaign",
                                    innerClassName="mouseovertooltip",
                                    target="show-video-link-desktop",
                                ),
                                html.A(
                                    html.Button("Show video", id="show-video-button-mobile", className="wra-button", style={"font-size": "18px"}),
                                    href="https://www.youtube.com/watch?v=" + YOUTUBE_VIDEO_ID,
                                    target="youtubeapp",
                                    id="show-video-link-mobile"
                                ),
                                html.A(
                                    html.Button([html.Span("FAQs",  # className="desktoponly"
                                        )],
                                        id="faq-button",
                                        className="wra-button",
                                        style={"font-size": "18px"}
                                    ),
                                    href="https://www.whiteribbonalliance.org/dashboard/",
                                    target="newfaq",
                                ),
                                dbc.Tooltip(
                                    "Read some of the Frequently Asked Questions about the dashboard and What Women Want campaign",
                                    innerClassName="mouseovertooltip",
                                    target="faq-button",
                                ),
                            ],
                            className="intro_blurb eight columns",
                            id="title5",
                            style={"align-content": "center", "margin-top":"0px", "padding-top":"0px"}
                        ),
                        html.Div(
                            [
                            ],
                            className="two columns",
                            id="button4",
                            style={"margin-top":"0px"}
                        ),
                    ],
                    style={"margin-bottom": "0px", "margin-top": "0px", "padding-top":"0px"},
                    className="row flex-display",
                    id="header2",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Tabs(
                                    id='comparison-tabs', value='tab-1',
                                    children=[
                                        dcc.Tab(get_tab_contents("1"), label='Drill down', id="tab-1"),
                                        dcc.Tab(get_tab_contents("2"), label='Compare to...', id="tab-2")
                                    ]
                                ),
                                html.Div([html.H3("Filter Controls"),
                                          html.P(
                                              "Here you can filter What Women Want campaign health literacy responses."),
                                          html.P(
                                              '"Select Countries" and "Select Response Topics" are dropdowns that allow you to select from the list of participating What Women Want countries and from the list of What Women Want health literacy topic areas and categories.'),
                                          html.P(
                                              "2/16"),
                                          html.Button("Next tip", id="twtooltipbtn1", className="tooltipbutton"),
                                          html.Button("Exit tutorial", id="twtooltipbtnexit1",
                                                      className="tooltipbutton")
                                          ],
                                         className="box sb2 twtooltip",
                                         id="twtooltip1",
                                         style={"display":"none"}
                                         ),
                            ],
                            className="pretty_container four columns",
                            id="cross-filter-options",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Loading(
                                                id="loading-1a",
                                                children=[html.H6(id="well_text")],
                                                type="circle",
                                            ), html.Div([html.H3("Number of Health Literacy Responses"),
                                                         html.P(
                                                             "Here you can see how many women fall into the criteria you have selected in the filters. If you have selected two groups or segments using the 'Compare to...' tab in the filters control panel, then the number of women in the second group will appear in the box on the right."),
                                                         html.P(
                                                             "9/16"),
                                                         html.Button("Next tip", id="twtooltipbtn8",
                                                                     className="tooltipbutton"),
                                                         html.Button("Exit tutorial", id="twtooltipbtnexit8",
                                                                     className="tooltipbutton")],
                                                        className="box sb2 twtooltip twhide",
                                                        id="twtooltip8"
                                                        ),
                                                html.P("Number of Health Literacy Responses", id="total_desc_1")],
                                            id="wells",
                                            className="mini_container",
                                        ),
                                        html.Div(
                                            [dcc.Loading(
                                                id="loading-1b",
                                                children=[html.H6(id="gasText")],
                                                type="circle",
                                            ), html.Div([html.H3("Average Age"),
                                                         html.P(
                                                             "This shows the average age of the women you have selected."),
                                                         html.P(
                                                             "If you have selected two groups or segments using the “Compare to...” tab in the filters control panel, then the average age of the second group will appear in the box on the right."),
                                                         html.P(
                                                             "10/16"),
                                                         html.Button("Next tip", id="twtooltipbtn9",
                                                                     className="tooltipbutton"),
                                                         html.Button("Exit tutorial", id="twtooltipbtnexit9",
                                                                     className="tooltipbutton")],
                                                        className="box sb2 twtooltip twhide",
                                                        id="twtooltip9"
                                                        ),
                                                html.P("Average Age")],
                                            id="gas",
                                            className="mini_container",
                                        ),
                                        html.Div("vs", className="vs"),
                                        html.Div(
                                            [dcc.Loading(
                                                id="loading-1c",
                                                children=[html.H6(id="oilText")],
                                                type="circle",
                                            ), html.P("Number of Health Literacy Responses", id="total_desc_2")],
                                            id="oil",
                                            className="mini_container",
                                        ),
                                        html.Div(
                                            [dcc.Loading(
                                                id="loading-1d",
                                                children=[html.H6(id="waterText")],
                                                type="circle",
                                            ), html.P("Average Age", id="avg_desc_2")],
                                            id="water",
                                            className="mini_container",
                                        ),
                                    ],
                                    id="info-container",
                                    className="row container-display",
                                ),
                                html.Div(
                                    [
                                        dcc.Loading(
                                            id="loading-2",
                                            children=[dcc.Graph(id="count_graph")],
                                            type="circle",
                                        ),
                                        html.Div([html.H3("Age Histogram"),
                                                  html.P(
                                                      "This graph shows the ages of the women you have selected."),
                                                  html.P(
                                                      "If you select a second group of women for comparison under 'Compare to...' in the filter control panel, then their ages will be displayed in this graph underneath the ages of the first group of women."),
                                                  html.P(
                                                      "If you move the mouse over the graph and click the camera icon 📷, you can save this graph to your computer."),
                                                  html.P(
                                                      "11/16"),
                                                  html.Button("Next tip", id="twtooltipbtn10",
                                                              className="tooltipbutton"),
                                                  html.Button("Exit tutorial", id="twtooltipbtnexit10",
                                                              className="tooltipbutton")],
                                                 className="box sb5 twtooltipbelow twhide",
                                                 id="twtooltip10"
                                                 ),
                                    ],
                                    id="countGraphContainer",
                                    className="pretty_container",
                                ),
                            ],
                            id="right-column",
                            className="eight columns",
                        ),
                    ],
                    className="row flex-display",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6("Breakdown of women's health literacy responses by topic"),
                             html.P(
                                 [html.Span("Click on a topic to view health literacy survey responses. ", className="desktoponly"),
                                  html.Span(
                                      "Some women mentioned more than one topic. You can hover over the graph and select the zoom and pan options, or click and drag the graph up and down, to see more. Hover over a bar to see the numbers and full category name.")]),
                             dcc.Loading(
                                 id="loading-3",
                                 children=[dcc.Graph(id="main_graph")],
                                 type="circle",
                             ),
                             html.Div([html.H3("Topic Breakdown"),
                                       html.P(
                                           "White Ribbon Alliance, global conveners of the What Women Want campaign, grouped women's responses into two levels of topics: a broad category, such as “Services, Supplies, and Information,” and relevant sub-categories, totaling 39 topic categories overall."),
                                       html.P(
                                           "Each sub-category is represented as a bar. The length of the bar represents how many women responded in that category."),
                                       html.P(
                                           "You can move the mouse over the graph to see options such as zooming out to view all 39 topics. You can also click on a topic bar to filter for that category."),
                                       html.P(
                                           "12/16"),
                                       html.Button("Next tip", id="twtooltipbtn11",
                                                   className="tooltipbutton"),
                                       html.Button("Exit tutorial", id="twtooltipbtnexit11",
                                                   className="tooltipbutton")],
                                      className="box sb2 twtooltip twhide",
                                      id="twtooltip11"
                                      )
                             ],
                            className="pretty_container six columns",
                        ),
                        html.Div(
                            [html.H6("Health literacy responses from some of the women we talked to", id="sample_responses_box"),
                             html.P(["Question asked: ", html.I(
                                 "What is your one request for quality reproductive and maternal healthcare services?")]),
                             dcc.Loading(
                                 id="loading-4",
                                 children=[data_table],
                                 type="circle",
                             ),
                             html.Div([html.H3("Sample Health Literacy Responses"),
                                       html.P(
                                           "Look here to see a randomized sample of the original responses, in the actual words of the women and girls who shared their demands for quality reproductive and maternal healthcare as part of the What Women Want campaign."),
                                       html.P(
                                           "You can also see which category each response was assigned to, which country the woman lives in, and their age."),
                                       html.P(
                                           "13/16"),
                                       html.Button("Next tip", id="twtooltipbtn12",
                                                   className="tooltipbutton"),
                                       html.Button("Exit tutorial", id="twtooltipbtnexit12",
                                                   className="tooltipbutton")],
                                      className="box sb5 twtooltipbelow twhide",
                                      id="twtooltip12"
                                      )
                             ],
                            className="pretty_container six columns",
                        ),
                    ],
                    className="row flex-display",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div([html.H3("Single words, two-word phrases, and three-word phrases"),
                                          html.P(
                                              "Of the women's health literacy responses that you've selected, here you can see the most common single words that the women mentioned."),
                                          html.P(
                                              "You can also see the most common two-word and three-word phrases that were mentioned within your filtered dataset, allowing for a deeper understanding of what women were asking for when it comes to quality reproductive healthcare."),
                                          html.P(
                                              "Similar to the “Filter by keyword” function at the top of the Dashboard, you can also click on any bar on the “One word phrases” graph to filter the responses for that word."),
                                          html.P(
                                              "14/16"),
                                          html.Button("Next tip", id="twtooltipbtn13",
                                                      className="tooltipbutton"),
                                          html.Button("Exit tutorial", id="twtooltipbtnexit13",
                                                      className="tooltipbutton")],
                                         className="box sb3 twtooltipabove twhide",
                                         id="twtooltip13"
                                         ),
                                html.Div([html.H3("Advanced Feature"),
                                          html.P(
                                              "If you want to limit the two-word and three-word phrases to those phrases containing a keyword, you can select “Show only multi-word phrases containing filter term” in the filter control panel."),
                                          html.P(
                                              "15/16"),
                                          html.Button("Next tip", id="twtooltipbtn14",
                                                      className="tooltipbutton"),
                                          html.Button("Exit tutorial", id="twtooltipbtnexit14",
                                                      className="tooltipbutton")],
                                         className="box sb3 twtooltipabove twhide",
                                         id="twtooltip14"
                                         ),
                                html.H6("Top words and phrases"),
                                dcc.Tabs(
                                    id='ngram-tabs',  # value='ngram-tab-1',
                                    children=[
                                        dcc.Tab(get_ngram_tab_contents("1"), label='One word phrases',
                                                id="ngram-tab-1"),
                                        dcc.Tab(get_ngram_tab_contents("2"), label='Two word phrases',
                                                id="ngram-tab-2"),
                                        dcc.Tab(get_ngram_tab_contents("3"), label='Three word phrases',
                                                id="ngram-tab-3"),
                                    ]
                                ),
                            ],
                            className="pretty_container six columns",
                        ),
                        html.Div(
                            [html.Div([html.H3("Map View"),
                                       html.P(
                                           "Here you can see where the women who responded were located geographically. The size of the bubbles indicates how many respondents were from that country proportionally."),
                                       html.P(
                                           "If you select two segments of respondents then both segments will be displayed in the map, and you can click on the legend to show or hide one segment"),
                                       html.P(
                                           "You can zoom into the map with the mouse scroll wheel."),
                                       html.P(
                                           "If you mouse-over any of the bubbles, it will tell you how many women respondents were in that country."),
                                       html.P(
                                           "If you click on a bubble, the Dashboard will filter for responses from that country."),
                                       html.P(
                                           "16/16"),
                                       html.Button("Next tip", id="twtooltipbtn15",
                                                   className="tooltipbutton twhide"),
                                       html.Button("Finish tutorial", id="twtooltipbtnexit15",
                                                   className="tooltipbutton")],
                                      className="box sb3 twtooltipabove twhide",
                                      id="twtooltip15"
                                      ),
                             html.H6("Where are the women located?"),
                             "Click legend to toggle bubbles, scroll mouse to zoom, click bubbles to view country information",
                             dcc.Graph(id="aggregate_graph")],
                            className="pretty_container six columns",
                        ),
                    ],
                    className="row flex-display",
                ),
            ],
            id="mainContainer",
            style={"display": "flex", "flex-direction": "column"},
        ),
        html.Div(
            [
                html.A(id="footnote"),
                "* All women participating in the What Women Want campaign provided informed consent.",  # TODO: check with Kristy
                html.Br(),
                "The 143,556 responses from the original ",
                html.A(["Hamara Swasthya Hamari Awaz"],
                       href="http://www.whiteribbonallianceindia.org/whats-latest/hamara-swasthya-hamari-awaz",
                       target="hsha"),
                " campaign are not included in these results.",
                html.Br(),
                "To protect anonymity, some respondents have been removed from this dashboard."
            ],
            className="attribution disclaimer"
        ),
        html.Div(
            [
                "Health Literacy dashboard by Cate Mann, representing ",
                html.A(["Merck for Mothers"], href="https://www.merckformothers.com", target="Merck")
            ],
            className="attribution"
        ),
        html.Div(
            [
                "Based on dashboard by ",
                html.A(["Thomas Wood"], href="https://freelancedatascientist.net", target="freelance"),
                " at ",
                html.A(["Fast Data Science"], href="https://fastdatascience.com", target="fds")
            ],
            className="attribution"
        ),
        html.Div(
            html.Div([
                html.Button("Close video", id="hide-video-button", className="wra-button"),
                html.Iframe(width=1120, height=630, src="https://www.youtube.com/embed/" + YOUTUBE_VIDEO_ID,
                            # in case Javascript fails
                            id="videoiframe")],
                className="videodivinternal", id="videodivinternal"
            )
            ,
            className="videodiv", id="videodiv"),
    ]
    )