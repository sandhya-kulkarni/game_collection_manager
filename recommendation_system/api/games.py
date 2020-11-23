"""
Game API endpoints with CSV adapter.
Supported calls:
    get_games - return all available game data.
    get_game_filters - return unique values within "game_type", "genre", "keywords", "mechanic"
    post_games - returns sorted game data by review score of given argument and filters
"""
import errno
import json
import os
import pandas as pd
from utilities import calculations, filter


# GAME DATA STORE
game_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../sample_data/games.csv"
)
# required columns
game_terms = [
    "game_type",
    "genre",
    "keywords",
    "mechanic"
]
# REVIEW DATA STORE
review_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../sample_data/reviews.csv"
)
# required columns
review_terms = [
    "complexity_score",
    "gameplay_score",
    "visual_score",
    "overall_score",
]


def validate_data_store(file, terms):
    """
    Ensure csv data is accessible and can be read into a panda's DataFrame
    :param file: (str) file location to read as csv data
    :param terms: (str list) list of column names required in given file
    :return: df: (pd.DataFrame)
    :raises FileNotFoundError: if given file is not accessible
    :raises ValueError: if given file cannot be read as csv data into panda's DataFrame
    """
    # Test data store is not corrupted / inaccessible
    if not os.path.exists(file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
    # test input is readable as data frame
    try:
        df = pd.read_csv(file)
    except ValueError as err:
        raise ValueError("Invalid Data Store: {}".format(err)) from None
    # test data_frame has required columns
    if not set(terms).issubset(df.columns):
        raise ValueError("Invalid Data Store. Missing Columns: {}".format(", ".join(terms)))
    return df


# CONTROLLERS
def get_games():
    """
    Return all available game data.
    :return: JSON
    """
    df = validate_data_store(game_file, game_terms)
    return df.to_json(orient="records")


def get_game_filters(input_df):
    """
    Return unique values found within game columns: "game_type", "genre", "keywords", "mechanic"
    :param input_df: (pd.DataFrame) input pandas data frame to query unique terms of.
    Defaults to main game data store if None given.
    :raises ValueError: if given input_df does not contain all required game columns
    :return: JSON
    """
    if input_df is None:
        input_df = validate_data_store(game_file, game_terms)
    terms = [
        "game_type",
        "genre",
        "keywords",
        "mechanic"
    ]

    unique_terms = {}
    for term in terms:
        unique_terms[term] = list(input_df[term].unique())
    return json.dumps(unique_terms)


def post_games(sort_by="overall_score", filter_dict={}, weighting=[0, 0, 0, 1]):
    """
    Calculates mean/weighted mean and returns sorted game data by review score of given arguments.
    :param sort_by: optional (str) property to calculate mean score value for and sort results by.
    Must be either "complexity_score", "gameplay_score", "visual_score", or "overall_score"
    :param filter_dict: optional (dict) key-value pairs by which to filter game data store
    :param weighting: optional (int list) if sort_by is "overall_score", a user supplied weighting
    may be used to calculate a weighted average of all the properties.
    If no weighting is supplied, then standard arithmetic mean is calculated for "overall_score".
    :return: sorted_games: (pd.DataFrame) game data by review score of given argument and filters.
    :raises TypeError: if arguments are not as expected
    """
    valid_sort_by = ["complexity_score", "gameplay_score", "visual_score", "overall_score"]
    # test arguments
    if type(sort_by) != str and sort_by not in valid_sort_by:
        raise TypeError("sort_by must be one of the following: {}".format(", ".join(valid_sort_by)))
    if type(filter_dict) != dict:
        raise TypeError("filter_dict must be a dictionary with at least one key-value pair")
    if type(weighting) != list or len(weighting) != 4 or not all(type(n) is int for n in weighting):
        raise TypeError("weighting must be a list of 4 int values")

    games = validate_data_store(game_file, game_terms)
    reviews = validate_data_store(review_file, review_terms)
    # reduce game data store by filters if key-value pairs given
    if len(filter_dict) > 0:
        games = filter.data_frame(games, filter_dict)
    # calculate mean of sort_by and return game data in descending order
    sorted_games = calculations.game_review_mean(games, reviews, sort_by, weighting)
    return sorted_games.to_json(orient="records")


# usage
#print(get_games())
#print(get_game_filters())
#x = post_games("visual_score", {"game_type": "Board Game"})