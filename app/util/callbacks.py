import re

from graphs.age_histogram import generate_age_histogram
from graphs.category_bar_graph_generator import generate_bar_graph
from graphs.map_generator import bubble_map_2
from graphs.ngram_generator import generate_ngrams
from util.code_hierarchy import mapping_to_description
from util.constants import DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE
from util.nlg import generate_description_of_filter
from util.number_formatter import human_format


def get_all_descriptions(code):
    return mapping_to_description.get(code, " / ".join(
        sorted(set([mapping_to_description.get(x, x) for x in code.split("/")]))))


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_filters_identical(country1, country2, code1, code2, age1, age2, text1, text2, text_exclude1,
                          text_exclude2):
    """
    Find out if both sets of filters are identical.
    If both filters are identical then we should not display dual graphs.
    Some filters are nested lists so they should be un-nested before performing the check.
    :param country1:
    :param country2:
    :param code1:
    :param code2:
    :param age1:
    :param age2:
    :param text1:
    :param text2:
    :param text_exclude1:
    :param text_exclude2:
    :return:
    """
    country1 = flatten(country1)
    country2 = flatten(country2)

    code1 = flatten(code1)
    code2 = flatten(code2)
    return country1 == country2 and code1 == code2 and age1 == age2 and text1 == text2 and text_exclude1 == text_exclude2


class CallbackManager:

    def __init__(self, df_responses):
        self.df_responses = df_responses

    def apply_filters_to_dataframe(self, country, code, age, text, text_exclude):
        lower_age = age[0]
        upper_age = age[1]
        if lower_age == DEFAULT_LOWER_AGE:
            lower_age = None
        if upper_age == DEFAULT_UPPER_AGE:
            upper_age = None
        tmp_df = self.df_responses
        if len(country) > 0:
            tmp_df = tmp_df[tmp_df.canonical_country.isin(country)]
        if len(code) > 0:
            condition = tmp_df.canonical_code.isin(code) | tmp_df.top_level.isin(code)
            for c in code:
                condition |= tmp_df.canonical_code.str.contains(r'\b' + c + r'\b', regex=True)
            if "multiple topics" in code:
                condition |= tmp_df.canonical_code.str.contains("/")
            tmp_df = tmp_df[
                condition
            ]

        if text != "":
            text_re = r'\b' + re.escape(text)
            tmp_df = tmp_df[tmp_df.lemmatized.str.contains(text_re, regex=True)]
        if text_exclude != "":
            text_exclude_re = r'\b' + re.escape(text_exclude)
            tmp_df = tmp_df[~tmp_df.lemmatized.str.contains(text_exclude_re, regex=True)]

        tmp_df_age_filtered = tmp_df
        if lower_age is not None:
            tmp_df_age_filtered = tmp_df_age_filtered[tmp_df_age_filtered.age >= lower_age]
        if upper_age is not None:
            tmp_df_age_filtered = tmp_df_age_filtered[tmp_df_age_filtered.age <= upper_age]
        
        description = generate_description_of_filter(country, code, lower_age, upper_age, text, text_exclude,
                                                     len(tmp_df_age_filtered))
        
        return tmp_df, tmp_df_age_filtered, description

    def update_year_slider(self, count_graph_selected):
        print("SELECTED", count_graph_selected)
        if count_graph_selected is None or len(count_graph_selected['points']) == 0:
            return [DEFAULT_LOWER_AGE, DEFAULT_UPPER_AGE]

        nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
        return [min(nums) + DEFAULT_LOWER_AGE, max(nums) + DEFAULT_LOWER_AGE + 1]

    def update_filters_callback(self, country1, country2, code1, code2, age1, age2, text1, text2, text_exclude1,
                                text_exclude2, screen_width):
        try:
            screen_width = int(screen_width)
        except:
            screen_width = 9999

        text1 = text1.lower()
        text2 = text2.lower()
        text_exclude1 = text_exclude1.lower()
        text_exclude2 = text_exclude2.lower()

        is_filters_identical = get_filters_identical(country1, country2, code1, code2, age1, age2, text1, text2,
                                                     text_exclude1,
                                                     text_exclude2)

        
        # Apply the first filter ("Drill down" on the dashboard controls)
        df1, df1_age_filtered, desc1 = self.apply_filters_to_dataframe(country1, code1, age1, text1, text_exclude1)

        # Apply the second filter ("Compare to...")
        df2, df2_age_filtered, desc2 = self.apply_filters_to_dataframe(country2, code2, age2, text2, text_exclude2)

        # Generate the histogram
        figure = generate_age_histogram(df1, age1, desc1, df2, age2, desc2, is_filters_identical, screen_width)

        # Generate the bar graph for the codes
        fig_top_level = generate_bar_graph(df1_age_filtered, desc1, screen_width)

        data_excerpt = df1_age_filtered
        # Generate the map
        map_view = bubble_map_2(df1_age_filtered, df2_age_filtered, desc1, desc2, is_filters_identical)

        # Calculate the average values
        avg1 = "N/A"
        if len(df1_age_filtered) > 0:  #
            avg1 = human_format(df1_age_filtered[df1_age_filtered.age > 0].age.mean())
        avg2 = "N/A"
        if len(df2_age_filtered) > 0:  #
            avg2 = human_format(df2_age_filtered[df2_age_filtered.age > 0].age.mean())

        # Generate the survey responses excerpt
        if len(data_excerpt) > 1000:
            data_excerpt = data_excerpt.sample(1000)
            sample_responses_box = "A sample of 1000 responses"
        elif len(data_excerpt) == 0:
            sample_responses_box = "No responses to display because no women are selected"
        elif len(data_excerpt) == 1:
            sample_responses_box = "Response from the only woman in your selection"
        else:
            sample_responses_box = "Responses from all " + str(
                len(data_excerpt)) + " women in your selection"
        data_excerpt["description"] = data_excerpt["canonical_code"].apply(get_all_descriptions)
        data_excerpt_dict = data_excerpt[['canonical_country', 'description', 'raw_response', 'age_str']].to_dict(
            'records')

        hf2 = human_format(len(
            df2_age_filtered))

        avg_desc_2 = "Average age"

        if is_filters_identical:
            # Don't fill out the "vs" panel if both filters are identical
            hf2 = ""
            desc2 = ""
            avg2 = ""
            avg_desc_2 = ""

        return human_format(
            len(
                df1_age_filtered)), desc1, avg1, hf2, desc2, avg2, avg_desc_2, figure, fig_top_level, data_excerpt_dict, map_view, sample_responses_box, 0

    def update_filters_callback_ngrams_only(self, dummy, country1, country2, code1, code2, age1, age2, text1, text2,
                                            text_exclude1, text_exclude2, ngram_filter_checkbox):
        """
        :param dummy: This is just to trigger the callback, to make sure we calculate N-grams last
        :param country1:
        :param country2:
        :param code1:
        :param code2:
        :param age1:
        :param age2:
        :param text1:
        :param text2:
        :return:
        """
        text1 = text1.lower()
        text2 = text2.lower()
        text_exclude1 = text_exclude1.lower()
        text_exclude2 = text_exclude2.lower()

        is_filters_identical = get_filters_identical(country1, country2, code1, code2, age1, age2, text1, text2,
                                                     text_exclude1,
                                                     text_exclude2)

        is_no_filter = len(country1) == 0 and len(code1) == 0 and age1[0] == DEFAULT_LOWER_AGE and age1[
            1] == DEFAULT_UPPER_AGE and text1 == "" and text_exclude1 == ""
        is_no_filter2 = len(country2) == 0 and len(code2) == 0 and age2[0] == DEFAULT_LOWER_AGE and age2[
            1] == DEFAULT_UPPER_AGE and text2 == "" and text_exclude2 == ""

       # Get N-grams for the first filter group ("Drill down")
        df1, df1_age_filtered, desc1 = self.apply_filters_to_dataframe(country1, code1, age1, text1, text_exclude1)

        # Get N-grams for the second filter group ("Compare to...")
        df2, df2_age_filtered, desc2 = self.apply_filters_to_dataframe(country2, code2, age2, text2, text_exclude2)

        # Generate the N-grams graphs
        unigrams, bigrams, trigrams = generate_ngrams(df1_age_filtered, df2_age_filtered, desc1, desc2, text1,
                                                      ngram_filter_checkbox, is_no_filter, is_no_filter2,
                                                      is_filters_identical)
        return unigrams, bigrams, trigrams
