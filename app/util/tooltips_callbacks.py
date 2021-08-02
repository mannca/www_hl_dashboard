from dash.dependencies import Input, Output

from util.constants import YOUTUBE_VIDEO_ID


def add_clientside_callbacks_tooltips(app):
    # Go to next tooltip
    app.clientside_callback(
        """
        function(data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15) {
            var clicks = [data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15];
            var response = [];
            for (i = 0; i < clicks.length; i++) {
                response.push({"display": "none"});
            }
            var is_clicked = false;
            for (i = clicks.length - 1; i >= 0; i--) {
                console.log(i);
                if (clicks[i] != null && clicks[i] > 0) {
                   if (i + 1 < clicks.length) {
                    response[i+1]["display"] = "inline"
                   }
                   is_clicked = true;
                   
                   //location.href = "#";
                   //location.href = "#twtooltip11";
                   //var elementExists = document.getElementById("videoiframe");
                   //var top = document.getElementById("twtooltip1").offsetTop;
                   //##alert("top is", top);
                   //window.scrollTo(0, top);  
                   break;
                }
            }
            if (!is_clicked) {
                response[0]["display"] = "inline";
            }
            return response;
        }
        """,
        [Output("twtooltip0", "style"),
         Output("twtooltip1", "style"),
         Output("twtooltip2", "style"),
         Output("twtooltip3", "style"),
         Output("twtooltip4", "style"),
         Output("twtooltip5", "style"),
         Output("twtooltip6", "style"),
         Output("twtooltip7", "style"),
         Output("twtooltip8", "style"),
         Output("twtooltip9", "style"),
         Output("twtooltip10", "style"),
         Output("twtooltip11", "style"),
         Output("twtooltip12", "style"),
         Output("twtooltip13", "style"),
         Output("twtooltip14", "style"),
         Output("twtooltip15", "style"),
         ],
        [Input("twtooltipbtn0", "n_clicks"),
         Input("twtooltipbtn1", "n_clicks"),
         Input("twtooltipbtn2", "n_clicks"),
         Input("twtooltipbtn3", "n_clicks"),
         Input("twtooltipbtn4", "n_clicks"),
         Input("twtooltipbtn5", "n_clicks"),
         Input("twtooltipbtn6", "n_clicks"),
         Input("twtooltipbtn7", "n_clicks"),
         Input("twtooltipbtn8", "n_clicks"),
         Input("twtooltipbtn9", "n_clicks"),
         Input("twtooltipbtn10", "n_clicks"),
         Input("twtooltipbtn11", "n_clicks"),
         Input("twtooltipbtn12", "n_clicks"),
         Input("twtooltipbtn13", "n_clicks"),
         Input("twtooltipbtn14", "n_clicks"),
         Input("twtooltipbtn15", "n_clicks"),
         ])

    # Restart tooltips
    app.clientside_callback(
        """
        function(reset) {
            if (reset == -1) {
             return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
            }
         return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        }
        """,
        [Output('twtooltipbtn0', 'n_clicks'),
         Output('twtooltipbtn1', 'n_clicks'),
         Output('twtooltipbtn2', 'n_clicks'),
         Output('twtooltipbtn3', 'n_clicks'),
         Output('twtooltipbtn4', 'n_clicks'),
         Output('twtooltipbtn5', 'n_clicks'),
         Output('twtooltipbtn6', 'n_clicks'),
         Output("twtooltipbtn7", "n_clicks"),
         Output("twtooltipbtn8", "n_clicks"),
         Output("twtooltipbtn9", "n_clicks"),
         Output("twtooltipbtn10", "n_clicks"),
         Output("twtooltipbtn11", "n_clicks"),
         Output("twtooltipbtn12", "n_clicks"),
         Output("twtooltipbtn13", "n_clicks"),
         Output("twtooltipbtn14", "n_clicks"),
         Output('twtooltipbtn15', 'n_clicks'),
         ],
        [Input('reset-tooltips-button', 'n_clicks')])

    # Exit tooltips
    app.clientside_callback(
        """function(data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15) {
            var clicks = [data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15];
            for (i = 0; i < clicks.length; i++) {
                if (clicks[i] != null && clicks[i] > 0) {
                    return -1;
                }
            }
            return 0;
        }""",
        Output('reset-tooltips-button', 'n_clicks'),
        [Input("twtooltipbtnexit0", "n_clicks"),
         Input("twtooltipbtnexit1", "n_clicks"),
         Input("twtooltipbtnexit2", "n_clicks"),
         Input("twtooltipbtnexit3", "n_clicks"),
         Input("twtooltipbtnexit4", "n_clicks"),
         Input("twtooltipbtnexit5", "n_clicks"),
         Input("twtooltipbtnexit6", "n_clicks"),
         Input("twtooltipbtnexit7", "n_clicks"),
         Input("twtooltipbtnexit8", "n_clicks"),
         Input("twtooltipbtnexit9", "n_clicks"),
         Input("twtooltipbtnexit10", "n_clicks"),
         Input("twtooltipbtnexit11", "n_clicks"),
         Input("twtooltipbtnexit12", "n_clicks"),
         Input("twtooltipbtnexit13", "n_clicks"),
         Input("twtooltipbtnexit14", "n_clicks"),
         Input("twtooltipbtnexit15", "n_clicks"),

         ])

    app.clientside_callback(
        """function(data) {
            var elementExists = document.getElementById("videoiframe");
            if (data != null && data > 0) {
                if (elementExists)  {
                    elementExists.src = "https://www.youtube.com/embed/""" + YOUTUBE_VIDEO_ID + """?autoplay=1";
                }
                return {"display":"inline"};
            } else {
                if (elementExists)  {
                    elementExists.src = "https://www.youtube.com/embed/""" + YOUTUBE_VIDEO_ID + """";
                }
                return {"display":"none"};
            }
        }""",
        Output('videodiv', 'style'),
        Input("show-video-button", "n_clicks")
    )

    app.clientside_callback(
        """function(data) {
            return 0;
        }""",
        Output("show-video-button", "n_clicks"),
        Input("hide-video-button", "n_clicks")
    )

    # Get the screen width and send to Python
    app.clientside_callback(
            """function(data) {
                return screen.width;
            }""",
            Output("screenwidth", "value"),
            Input("screenwidthtrigger", "value")
    )