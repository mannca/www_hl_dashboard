import numpy as np
import plotly.graph_objects as go

from util.constants import DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE, MAIN_COLOUR, SECONDARY_COLOUR, MAIN_COLOUR_FAINT, \
    SECONDARY_COLOUR_FAINT


def nice_num(the_range, round):
    """
    Returns a "nice" number approximately equal to range Rounds
    the number if round = true Takes the ceiling if round = false.
    :param the_range: the data range
    :param round: whether to round the result
    :return: a "nice" number to be used for the data range
    """
    exponent = np.floor(np.log10(the_range))
    fraction = the_range / np.power(10, exponent)

    if round:
        if fraction < 1.5:
            niceFraction = 1
        elif fraction < 3:
            niceFraction = 2
        elif fraction < 7:
            niceFraction = 5
        else:
            niceFraction = 10
    else:
        if fraction <= 1:
            niceFraction = 1
        elif fraction <= 2:
            niceFraction = 2
        elif fraction <= 5:
            niceFraction = 5
        else:
            niceFraction = 10
    return int(np.round(niceFraction * np.power(10, exponent)))


def get_hist(df, age_filter, is_faint):
    hist_values, hist_bins = np.histogram(df.age, bins=DEFAULT_UPPER_AGE - DEFAULT_LOWER_AGE + 1,
                                          range=[DEFAULT_LOWER_AGE - .5, DEFAULT_UPPER_AGE + 0.5])
    hist_centres = [x + 0.5 for x in hist_bins[:-1]]

    colors = []
    for i in range(DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE):
        if i >= int(age_filter[0]) and i < int(age_filter[1]):
            if is_faint:
                colors.append(SECONDARY_COLOUR)
            else:
                colors.append(MAIN_COLOUR)  # was: rgb(123, 199, 255)"
        else:
            if is_faint:
                colors.append(SECONDARY_COLOUR_FAINT)
            else:
                colors.append(MAIN_COLOUR_FAINT)  # was: "rgba(123, 199, 255, 0.2)"
    return hist_values, hist_centres, colors


def generate_age_histogram(df1, age_filter1, description1, df2, age_filter2, description2, is_filters_identical, screen_width):
    graph_title = "Number and ages of women surveyed"

    if screen_width >= 1400:
        graph_title += "<br>If you want to see results for a particular age group then drag to select that group on the graph."

    is_no_data = len(df1) == 0

    if is_no_data:
        graph_title = "There are no survey responses in your selection."
    # begin make graph
    hist_values1, hist_centres1, colors1 = get_hist(df1, age_filter1, False)
    hist_values2, hist_centres2, colors2 = get_hist(df2, age_filter2, True)

    if len(hist_values1) > 0:
        max_value_pos = np.max(hist_values1)
    else:
        max_value_pos = 0
    if len(hist_values2) > 0:
        max_value_neg = np.max(hist_values2)
        max_ticks = 3
    else:
        max_value_neg = 0
        max_ticks = 3

    if max_value_neg > 0 and max_value_pos > 0:
        scale_factor = max_value_pos / max_value_neg
        hist_values2 = hist_values2 * scale_factor
    else:
        scale_factor = 1

    tickstep = max_value_pos // max_ticks
    if tickstep == 0:
        tickstep = 1
    tickstep = nice_num(tickstep, True)

    max_ticks_neg = max_ticks // 2

    tickstep_neg = max_value_neg // max_ticks_neg
    if tickstep_neg == 0:
        tickstep_neg = 1
    tickstep_neg = nice_num(tickstep_neg, True)

    tickvals_pos = list(range(0, max_value_pos + tickstep - 1, tickstep))

    tickvals_true_neg = list(range(0, max_value_neg + tickstep_neg - 1, tickstep_neg))[1:]

    values_in_range = [x for x in tickvals_true_neg if x <= max_value_neg]
    if len(values_in_range) <= 1:
        tickvals_true_neg = [nice_num(max_value_neg*0.25, 3), nice_num(max_value_neg*0.5, 3),nice_num(max_value_neg*0.75, 3), nice_num(max_value_neg, 3), nice_num(max_value_neg*1.25, 3), nice_num(max_value_neg*1.5, 3)]

    tickvals_true_neg = np.array(tickvals_true_neg)
    tickvals_scaled_neg = tickvals_true_neg * scale_factor

    ticktext_pos = [str(y) for y in tickvals_pos]
    ticktext_neg = [str(int(np.round(y))) for y in tickvals_true_neg]

    tickvals_scaled_neg = [-y for y in tickvals_scaled_neg]

    histogram_data = [
    ]
    if not is_no_data:
        histogram_data.append(
            go.Bar(x=hist_centres1, y=hist_values1, name=description1, marker=dict(color=colors1), offset=None))
        if not is_filters_identical:
            histogram_data.append(
                go.Bar(x=hist_centres2, y=hist_values2, base=-hist_values2, name=description2 + " (normalized)",
                       marker=dict(color=colors2),
                       offset=None))

    figure = go.Figure(
        data=histogram_data,
        layout=go.Layout(
            title=go.layout.Title(text=graph_title),
            dragmode="select",
            showlegend=True,
            autosize=True,
            margin=dict(l=30, r=30, b=20, t=40),
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10), orientation="h"),
            bargap=0,
            barmode='overlay',
            yaxis=dict(
                tickmode='array',
                tickvals=tickvals_pos + tickvals_scaled_neg,
                ticktext=ticktext_pos + ticktext_neg
            )
        )
    )
    figure.update_xaxes(range=[DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE])

    return figure