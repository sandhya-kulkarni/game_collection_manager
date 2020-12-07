"""
Recommendations API endpoints with CSV adapter.
Supported calls:

"""
from .utilities import calculations
from .config import *
from .collections import get_collections
import numpy as np
import scipy.stats

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
    Returns game recommendations for a user based on what other similar users rated highly.
    :param user_id: (str) User ID to based user-user recommendations.
    :return: (pd.DataFrame) of game recommendations
    """
    rating_df = validate_data_store(review_file, review_terms)
    # normalise all user scores
    normalised_rating_df = calculations.user_normalised_reviews(rating_df)

    # create rating matrix
    rating_matrix_df = rating_df.pivot(index="user_id", columns="game_id", values="overall_score").fillna(0)
    normalise_matrix_df = normalised_rating_df.pivot(index="user_id", columns="game_id", values="overall_score").fillna(0)

    # get similarity between all users and input user_id
    similarity_matrix = np.array(
        [users_similarity(rating_matrix_df.loc[user_id,:], rating_matrix_df.loc[i,:]) for i in rating_matrix_df.index])
    similarity_df = pd.DataFrame(data = similarity_matrix.reshape(-1,1), index=rating_matrix_df.index)

    # get similar users
    similar_users = users_neighbours(similarity_df, user_id)

    # get games not owned by the user
    not_owned_games=get_games_not_owned_by_user(user_id, normalise_matrix_df.columns.values.tolist())
    neighbours_rating_of_not_owned_games = normalise_matrix_df.loc[similar_users][not_owned_games]
    neighbours_similarity= similarity_df[0].loc[similar_users]
    # score not owned games based on what is likely to get a high rating by the given user
    scored_games = score_games(neighbours_rating_of_not_owned_games, neighbours_similarity, rating_matrix_df, user_id)
    sorted_scored_games = scored_games.sort_values(by=0, axis=1, ascending=False)
    positive_scored_games_sorted = sorted_scored_games[sorted_scored_games > 0].dropna(axis=1)
    top_game_recommendations = positive_scored_games_sorted.iloc[0,:5]
    return top_game_recommendations

def users_similarity(user_1, user_2):
    """
    Returns similarity between two user rows using Pearson correlation.
    :param user_1: (pd.DataFrame) first user's review scores of games
    :param user_2: (pd.DataFrame) second user's review scores of games
    :return: (float) correlation coefficients. varying between -1 and +1.
        correlation coefficients 0 means there is no correlation.
        correlations -1 or +1 means there is an exact linear relationship.
        Positive correlations between 2 users mean that if one user rated
        a game highly, there is a good chance the other user will do so too.
    """
    # pearsonr normalises the review scores
    return scipy.stats.pearsonr(user_1, user_2)[0]

def users_neighbours(sim, user_id):
    """
    Returns similar users to a given user via the similarity matrix.
    :param sim: (pd.DataFrame) similarity matrix of a user with other users.
    :param user_id: (str) User ID of user we want similar neighbours of.
    :return: (list) list of similar users.
    """
    # return all neighbours with similarity over the set threshold.
    neighbours = sim[sim.gt(0.1)].dropna().index.values.tolist()
    neighbours.remove(user_id)
    return neighbours

def score_games(neighbours_rating_of_not_owned_games, neighbours_similarity, ratings, user_id):
    """
    Returns score games that the user_id does not own. 
    The score indicates the likelihood of the game getting a good rating by the given user.
    :param neighbours_rating_of_not_owned_games: (pd.DataFrame) rating of not owned games by similar users.
    :param neighbours_similarity: (pd.DataFrame) similarity scores of similar users.
    :param user_id: (str) User ID of user we want similar neighbours of.
    :return: (pd.DataFrame) of games not owned by the given user_id and their likelihood score to be rated high.
    """
    users_mean_rating = np.mean(ratings.loc[user_id, :])
    # calculating a weighted average for scores
    score = np.dot(neighbours_similarity, neighbours_rating_of_not_owned_games) + users_mean_rating
    return pd.DataFrame(
        data = score.reshape(1, len(score)) , columns = neighbours_rating_of_not_owned_games.columns)
      
def get_games_not_owned_by_user(user_id, rated_games):
    """
    Returns list of games that the give user does not own.
    :param user_id: (str) User ID of user we want similar neighbours of.
    :param rated_games: (list) list of games that have ratings/are in the available rating dataframe.
    :return: (list) of games not owned by the given user_id.
    """
    # get user's collections and all games within it
    user_collections = get_collections(user_id=user_id)
    games_owned_by_user = user_collections['game_ids'].tolist()
    flat_games_owned_by_user = ', '.join(games_owned_by_user).split(', ')
    return list(set(rated_games)-set(flat_games_owned_by_user))

