"""
Recommendations API endpoints with CSV adapter.
Supported calls:

"""
from .utilities import calculations
from .config import *


def recommendations_help(parser, verb):
    """
    Extend help text with options specific to recommendations object
    :param parser: (ArgumentParser) the existing help object being built.
    :param verb: (str) optional rest verb to limit scope of help given.
    :return: parser: (ArgumentParser) with extended help arguments
    """
    def get():
        parser.add_argument(
            "--user_id",
            type=str,
            required=True,
            help="User id to base recommendations on."
        )

    if verb == "GET":
        get()

    return parser


def recommendations_usage(parsed_args):
    """
    Return data specific to arguments given relating to games object
    :param parsed_args: the arguments given by the user after being successfully parsed.
    :return: (*) result of given arguments
    """
    if parsed_args.verb == "GET":
        df = get_user_user_recommendations(parsed_args.user_id)
    return df


# CONTROLLERS
def get_user_user_recommendations(user_id):
    """
    Return all available review data.
    :param user_id: (str) User ID to based user-user recommendations.
    :return: (pd.DataFrame) of game recommendations
    """
    df = validate_data_store(review_file, review_terms)
    # part 1 - normalise review scores for given user
    df = df.loc[df['user_id'] == user_id]
    df = calculations.user_normalised_reviews(df)
    # part 2 - normalise all user scores and calculate similarity
    return df


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