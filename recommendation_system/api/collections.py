"""
Collection API endpoints with CSV adapter.
Supported calls:
"""
from .config import *


def collections_help(parser, verb):
    """
    Extend help text with options specific to collections object
    :param parser: (ArgumentParser) the existing help object being built.
    :param verb: (str) optional rest verb to limit scope of help given.
    :return: parser: (ArgumentParser) with extended help arguments
    """
    def get():
        parser.add_argument(
            "--id",
            type=str,
            help="Optional collection id to limit the information returned to a single collection object."
        )
        parser.add_argument(
            "--user_id",
            type=str,
            help="Optional user id to limit the information returned to a single user's collections object."
        )

    def patch():
        parser.add_argument(
            "--id",
            type=str,
            required=True,
            help="Collection id to update"
        )
        parser.add_argument(
            "--game-id",
            type=str,
            required=True,
            help="Game id to extend collection with."
        )

    def delete():
        parser.add_argument(
            "--id",
            type=str,
            required=True,
            help="Collection id to delete"
        )
        parser.add_argument(
            "--game-id",
            type=str,
            help="Optional Game id, which if given means only the game id is deleted from a given collection."
        )

    if verb == "GET":
        get()
    elif verb == "PATCH":
        patch()
    elif verb == "DELETE":
        delete()
    else:
        get()
        patch()

    return parser


def collections_usage(parsed_args):
    """
    Return data specific to arguments given relating to users object
    :param parsed_args: the arguments given by the user after being successfully parsed.
    :return: (*) result of given arguments
    """
    if parsed_args.verb == "GET":
        df = get_collections(parsed_args.id, parsed_args.user_id)
    if parsed_args.verb == "PATCH":
        df = get_collections()
        df = add_game_to_collection(df, parsed_args.id, parsed_args.game_id)
    if parsed_args.verb == "DELETE":
        df = get_collections()
        if parsed_args.id and parsed_args.game_id:
            df = remove_game_from_collection(
                    df,
                    parsed_args.id,
                    parsed_args.game_id
                )
        elif parsed_args.id:
            df = delete_collection(df, parsed_args.id)

    return df


# CONTROLLERS
def get_collections(collection_id=None, user_id=None):
    """
    Return all available user data.
    :param id: (str) Optional collection id to return information on a single collection.
    :param user_id: (str) Optional user id to return information on a single user's collections.
    :return: (pd.DataFrame)
    """
    df = validate_data_store(collection_file, collection_terms)
    if collection_id is not None:
        df = df.loc[df['collection_id'] == collection_id]
    elif user_id is not None:
        df = df.loc[df['user_id'] == user_id]

    return df


def add_game_to_collection(input_df, collection_id, game_id):
    """
    adds an existing game to an existing collection_id.
        :param input_df: (pd.DataFrame) input pandas data frame.
        :param collection_id: (str) collection_id of the collection the game will be added to.
        :param game_id: (str) game_id of the game that will be added to the collection.
        :return: None
    """
    game_ids = input_df.loc[input_df.collection_id == collection_id, 'game_ids']
    # check if game already exists in collection, if so no need to add it again.
    games_array = game_ids.values[0].replace(" ", "").split(",")
    if game_id in games_array:
        print("Game with game_id: %s already exists"% game_id
            + " in this collection (collection_id: %s)"% collection_id)
        return

    input_df.loc[input_df.collection_id == collection_id, 'game_ids'] = game_ids + ", " + game_id
    # TODO currently the whole collection_df is rewritten
    # to make it easier to change game_ids string arrays,
    # this should be changed to a more scalable approach
    # once database tables are used
    input_df.to_csv(
          collection_file,
          mode='w',
          index=False,
          header=True
    )
    print("game with game_id: %s was successfully added"% game_id
        + " to collection with collection_id: %s"% collection_id)
    return input_df.loc[input_df.collection_id == collection_id]


def remove_game_from_collection(input_df, collection_id, game_id):
    """
    remove an existing game from a specific collection_id.
        :param input_df: (pd.DataFrame) input pandas data frame.
        :param collection_id: (str) collection_id of the collection the game will be removed from.
        :param game_id: (str) game_id of the game that will be removed from the collection.
        :return: None
    """
    collections_df = input_df

    game_ids = collections_df.loc[collections_df.collection_id == collection_id, 'game_ids']
    games_array = game_ids.values[0].replace(" ", "").split(",")
    if game_id not in games_array:
        print("Game with game_id: %s does not exists"% game_id
            + " in this collection (collection_id: %s)"% collection_id)
        return
    games_array.remove(game_id)
    collections_df.loc[collections_df.collection_id == collection_id,'game_ids'
        ] = ', '.join(games_array)
    # TODO currently the whole collection_df is rewritten
    # to make it easier to change game_ids string arrays,
    # this should be changed to a more scalable approach
    # once database tables are used
    collections_df.to_csv(
          collection_file,
          mode='w',
          index=False,
          header=True
    )
    print("game with game_id: %s was successfully removed" % game_id
    + " from collection with collection_id: %s"%collection_id)
    return collections_df.loc[collections_df.collection_id == collection_id]


def delete_collection(input_df, collection_id):
    """
    deletes a given collection, the collection has to be owned by the logged in users.
        :param input_df: (pd.DataFrame) input pandas data frame.
        :param collection_id: (str) collection_id of the collection that will be removed.
        :return: None.
    """
    collections_df = input_df

    row_index = collections_df[collections_df.collection_id == collection_id].index
    collections_df = collections_df.drop(row_index)

    # TODO currently the whole collection_df is rewritten
    # to make it easier to change game_ids string arrays,
    # this should be changed to a more scalable approach
    # once database tables are used
    collections_df.to_csv(
        collection_file,
        mode='w',
        index = False,
        header=True
    )
    print("collection with collection_id: %s was successfully deleted"%(collection_id))
    return collections_df


# GAME DATA STORE
collection_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    API_DATA_STORE + COLLECTION_DATA
)
# required columns
collection_terms = [
    "collection_id",
    "user_id",
    "game_ids"
]


# todo - decide if we want to insist on login or if can be run as admin
def get_user_collections():
    """
    prints the logged in users collections.
    If the user is not logged in, it will ask the user to log in or sign up.
        :return: None
    """
    if not get_logged_in_user():
        print("""You need to be logged in to see your collections.
            Please log into your account or sign up if you don't have an account.""")
        return

    collections_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            COLLECTION_DATA_STORE_PATH
        )
    )
    users_collections = collections_df[collections_df['user_id'] == get_logged_in_user()]
    if len(users_collections) == 0:
        print("No collections found for this user.")
        return
    print("Please see your collections below: ")
    print(users_collections)
