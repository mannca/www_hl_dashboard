import operator
from collections import Counter

from nltk.tokenize import TweetTokenizer

from util.constants import stopwords, MAIN_COLOUR, DARK_GREY, SECONDARY_COLOUR, TERTIARY_COLOUR, QUATERNARY_COLOUR

tknzr = TweetTokenizer()

ngram_cache = None  # we are memoising only the N-grams for the entire dataset


def generate_graph(counts_dict1, counts_dict2, desc1, desc2, is_filters_identical, colour):
    counts_dict1 = sorted(counts_dict1.items(), key=operator.itemgetter(1))
    max1 = 0
    if len(counts_dict1) > 0:
        max1 = counts_dict1[-1][1]
    if len(counts_dict1) > 20:
        counts_dict1 = counts_dict1[-20:]
    if len(counts_dict1) == 0:
        word_list_top_1, freq_list_top_1 = [], []
    else:
        word_list_top_1, freq_list_top_1 = zip(*counts_dict1)

    if len(counts_dict2) > 0 and len(counts_dict1) > 0 and len(freq_list_top_1) > 0:
        max2 = max(counts_dict2.values())
        normalisation_factor = max1 / max2
    else:
        normalisation_factor = 1

    freq_list_top_2 = [counts_dict2.get(w, 0) * normalisation_factor for w in word_list_top_1]

    bar_chart_data = []
    if not is_filters_identical:
        bar_chart_data.append({
            "y": word_list_top_1,
            "x": freq_list_top_2,
            "type": "bar",
            "name": desc2 + " (normalized)",
            "orientation": "h",
            "marker": dict(color=[DARK_GREY] * len(freq_list_top_1))
        })
    bar_chart_data.append({
        "y": word_list_top_1,
        "x": freq_list_top_1,
        "type": "bar",
        "name": desc1,
        "orientation": "h",
        "marker": dict(color=[colour] * len(freq_list_top_1))
    })

    frequency_figure_data = {
        "data": bar_chart_data,
        "layout": {"dragmode": "select", "height": "550", "margin": dict(t=20, b=20, l=200, r=20, pad=4),
                   "legend": dict(
                       yanchor="bottom",
                       y=0.01,
                       xanchor="right",
                       x=0.99
                   )
                   },
    }
    return frequency_figure_data


def get_ngrams(df, is_no_filter):
    global ngram_cache

    if is_no_filter and ngram_cache is not None:
        return ngram_cache

    unigram_count_dict = Counter()
    bigram_count_dict = Counter()
    trigram_count_dict = Counter()

    for words in df["tokenized"]:
        for i in range(len(words)):
            if words[i] not in stopwords:
                unigram_count_dict[words[i]] += 1
        for i in range(len(words) - 1):
            if words[i] not in stopwords and words[i + 1] not in stopwords:
                word_pair = words[i] + " " + words[i + 1]
                bigram_count_dict[word_pair] += 1
        for i in range(len(words) - 2):
            if words[i] not in stopwords and words[i + 1] not in stopwords and words[i + 2] not in stopwords:
                word_pair = words[i] + " " + words[i + 1] + " " + words[i + 2]
                trigram_count_dict[word_pair] += 1

    if is_no_filter:
        ngram_cache = unigram_count_dict, bigram_count_dict, trigram_count_dict

    return unigram_count_dict, bigram_count_dict, trigram_count_dict


def generate_ngrams(df1, df2, desc1, desc2, text1, ngram_filter_checkbox, is_no_filter, is_no_filter2,
                    is_filters_identical):
    unigram_count_dict_1, bigram_count_dict_1, trigram_count_dict_1 = get_ngrams(df1, is_no_filter)
    unigram_count_dict_2, bigram_count_dict_2, trigram_count_dict_2 = get_ngrams(df2, is_no_filter2)

    if ngram_filter_checkbox != "0" and len(text1) > 0:
        bigram_count_dict_1 = dict((a, b) for a, b in bigram_count_dict_1.items() if text1 in a)
        trigram_count_dict_1 = dict((a, b) for a, b in trigram_count_dict_1.items() if text1 in a)

    return generate_graph(unigram_count_dict_1, unigram_count_dict_2, desc1, desc2,
                          is_filters_identical, MAIN_COLOUR), generate_graph(bigram_count_dict_1,
                                                                bigram_count_dict_2,
                                                                desc1,
                                                                desc2, is_filters_identical, SECONDARY_COLOUR), generate_graph(
        trigram_count_dict_1, trigram_count_dict_2, desc1, desc2, is_filters_identical, TERTIARY_COLOUR)