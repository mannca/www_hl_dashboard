from wordcloud import STOPWORDS

stopwords = set(STOPWORDS).union(
    ["please", "like", "want", "need", "go", "will", "-", ".", ",", "'", "&", "(", ")", "must", "should", "even", "-",
     "/"])

DEFAULT_LOWER_AGE = 14
DEFAULT_UPPER_AGE = 60

MAIN_COLOUR = "rgb(0,123,133)"
MAIN_COLOUR_FAINT = "rgba(0,123,133,0.2)"
DARK_GREY = "rgb(150,150,150)"
SECONDARY_COLOUR = "rgb(216,53,42)"
SECONDARY_COLOUR_FAINT = "rgba(216,53,42,0.2)"
SECONDARY_COLOUR_LESS_FAINT = "rgba(216,53,42,0.5)"
TERTIARY_COLOUR = "rgb(23,13,92)"
QUATERNARY_COLOUR = "rgb(138,0,95)"

TIMEOUT = 20  # for cache

YOUTUBE_VIDEO_ID = 'nBzide5J3Hk'