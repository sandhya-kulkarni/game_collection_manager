"""
Game API endpoints with CSV adapter.
Supported calls:
    get_games - return available game data, along with mean review score.
    get_game_filters - modify return type to detail unique values within "game_type", "genre", "keywords", "mechanic"
"""
from .utilities import calculations, filter
from .config import *


def games_help(parser, verb):
    """
    Extend help text with options specific to games object
    :param parser: (ArgumentParser) the existing help object being built.
    :param verb: (str) optional rest verb to limit scope of help given.
    :return: parser: (ArgumentParser) with extended help arguments
    """
    def get():
        parser.add_argument(
            "--id",
            type=str,
            help="Optional id to limit the information returned to a single game object."
        )
        parser.add_argument(
            "--game_type",
            type=str,
            choices={"Board Game", "Card Game", "Role Playing Game", "Miniature War Game"},
            help="Optional game type value to filter the information returned."
        )
        parser.add_argument(
            "--genre",
            type=str,
            choices={"Fantasy", "Other", "Horror", "War"},
            help="Optional genre value to filter the information returned."
        )
        parser.add_argument(
            "--keywords",
            type=str,
            help="Optional keyword value to filter the information returned."
        )
        parser.add_argument(
            "--mechanic",
            type=str,
            help="Optional mechanic value to filter the information returned."
        )
        parser.add_argument(
            "--sort_by",
            type=str,
            choices={"complexity_score", "gameplay_score", "visual_score", "overall_score"},
            default="overall_score",
            help="Optional review aspect to sort the information returned."
        )
        parser.add_argument(
            "--weighting",
            type=list,
            default=[0, 0, 0, 1],
            help="Optional weighting to calculate mean average. Expects list of 4 int values."
        )
        parser.add_argument(
            "-f",
            "--function",
            choices={"FILTERS"},
            type=str,
            help="Optional function to modify return information about a specific aspect of game objects."
        )

    if verb == "GET":
        get()

    return parser


def games_usage(parsed_args):
    """
    Return data specific to arguments given relating to games object
    :param parsed_args: the arguments given by the user after being successfully parsed.
    :return: (*) result of given arguments
    """
    if parsed_args.verb == "GET":
        filter_dict = {
            "game_type": parsed_args.game_type,
            "genre": parsed_args.genre,
            "keywords": parsed_args.keywords,
            "mechanic": parsed_args.mechanic
        }
        df = get_games(parsed_args.id, filter_dict)
        if parsed_args.function == "FILTERS":
            df = get_game_filters(df)
        else:
            df = post_games(df, parsed_args.sort_by, parsed_args.weighting)
    return df


# CONTROLLERS
def get_games(game_id, filter_dict):
    """
    Return all available game data.
    :param game_id: (str) Optional game id to return information on a single game.
    :param filter_dict: optional (dict) key-value pairs by which to filter game data store
    :return: (pd.DataFrame)
    """
    if type(filter_dict) != dict:
        raise TypeError("filter_dict must be a dictionary with at least one key-value pair")

    df = validate_data_store(game_file, game_terms)
    # reduce game data store by filters if key-value pairs given
    filter_dict = {k: v for k, v in filter_dict.items() if v is not None}
    if len(filter_dict) > 0:
        df = filter.data_frame(df, filter_dict)

    if game_id is not None:
        df = df.loc[df['game_id'] == game_id]

    return df


def get_game_filters(input_df):
    """
    Return unique values found within game columns: "game_type", "genre", "keywords", "mechanic"
    :param input_df: (pd.DataFrame) input pandas data frame to query unique terms of.
    Defaults to main game data store if None given.
    :raises ValueError: if given input_df does not contain all required game columns
    :return: (pd.DataFrame)
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
    return pd.DataFrame([unique_terms])


def post_games(game_data, sort_by="overall_score", weighting=[0, 0, 0, 1]):
    """
    Calculates mean/weighted mean and returns sorted game data by review score of given arguments.
    :param sort_by: optional (str) property to calculate mean score value for and sort results by.
    Must be either "complexity_score", "gameplay_score", "visual_score", or "overall_score"

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
    if type(weighting) != list or len(weighting) != 4 or not all(type(n) is int for n in weighting):
        raise TypeError("weighting must be a list of 4 int values")

    games = game_data
    reviews = validate_data_store(review_file, review_terms)

    # calculate mean of sort_by and return game data in descending order
    sorted_games = calculations.game_review_mean(games, reviews, sort_by, weighting)
    return sorted_games


# GAME DATA STORE
game_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    API_DATA_STORE + GAME_DATA
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
    API_DATA_STORE + REVIEW_DATA
)
# required columns
review_terms = [
    "complexity_score",
    "gameplay_score",
    "visual_score",
    "overall_score",
]