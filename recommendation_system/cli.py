#!/usr/bin/env python3
"""
The program processes user, game and review data as inputs and outputs an ordered list of game
recommendations for a given scenario.
"""

from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
import os
import shutil
import sys
import pandas as pd


REST_GET = "GET"
REST_PUT = "PUT"
REST_POST = "POST"
REST_DELETE = "DELETE"
REST_VERBS = [REST_GET, REST_POST, REST_PUT, REST_DELETE]

# For GET calls
GAME_OBJECT = "GAMES"
COLLECTION_OBJECT = "COLLECTIONS"
VALID_OBJECTS_TO_FETCH = [GAME_OBJECT, COLLECTION_OBJECT]

# For POST calls
# since the login request is via a user supplying a username and password
# it is a POST call, as we'd like to send the details via the HTTP
# messages body rather than the URL.
LOGIN = "LOGIN"
LOGOUT = "LOGOUT"
SIGNUP = "SIGNUP"
CREATE_COLLECTION = "CREATE_COLLECTION"
VALID_POST_FUNCTIONS = [CREATE_COLLECTION, LOGIN, LOGOUT, SIGNUP]

CARD = "CARD GAME"
MINIATURE = "MINIATURE WAR GAME"
BOARD = "BOARD GAME"
ROLE = "ROLE PLAYING GAME"
VALID_GAME_TYPE = [CARD, MINIATURE, BOARD, ROLE]

AUTH_COOKIES_PATH = "../auth_cookies.txt"
MAIN_DATA_STORE = "../data_store"
SAMPLE_DATA_STORE = "sample_data"
GAME_DATA_STORE_PATH = "../data_store/games.csv"
COLLECTION_DATA_STORE_PATH = "../data_store/collections.csv"
REVIEW_DATA_STORE_PATH = "../data_store/reviews.csv"
USER_DATA_STORE_PATH = "../data_store/users.csv"

def start(args):
    """
    Main module function.
    :return: None
    """
    # Check if local data store has been initialised
    user_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        GAME_DATA_STORE_PATH
    )
    if not os.path.exists(user_file):
        copy_seed_data()

    parser = ArgumentParser(
        prog="Recommendation system for games based on user collection, preferences and reviews.",
        description="The program processes user, game and review data as inputs and "
                    "outputs an ordered list of game recommendations for a given user "
                    "and scenario conditions."
    )
    parser.add_argument(
        "-v",
        "--verb",
        type=valid_verb,
        default="GET",
        help="Verb signifying intent with given functionality (end-point)"
    )
    parser.add_argument(
        "-o",
        "--object_to_fetch",
        type=valid_object,
        help="The object that is intended to be fetched, in GET request"
    )
    parser.add_argument(
        "-g",
        "--game_id",
        type=valid_game_id,
        help="""The game id of the game in focus.
        can be used to fetch games or add/delete games to/from collections"""
    )
    parser.add_argument(
        "-f",
        "--function",
        type=valid_function,
        help="The function to be posted in a POST request"
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="username provided by the user to log in or sign up"
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="password provided by the user to log in or sign up"
    )
    parser.add_argument(
        "-d",
        "--date_of_birth",
        type=str,
        help="date of birth provided by user to sign up. This should be in the format of DD/MM/YYYY"
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="""full name provided by the user to sign up,
        this should be wrapped in quotation if spaces are put in"""
    )
    parser.add_argument(
        "-fgg",
        "--favourite_game_genre",
        type=str,
        help="""favourite game genre provided by the user at sign up.
        This has to be one of the four genres"""
    )
    parser.add_argument(
        "-fgt",
        "--favourite_game_type",
        type=valid_type,
        help="""favourite game type provided by the user at sign up.
        please choose from Card Game, Miniature War Game, Board Game and Role Playing Game"""
    )
    parser.add_argument(
        "-c",
        "--collection_id",
        type=valid_collection_id,
        help="""collection_id if the collection in focus.
        This can be used when adding or removing games to/from a collection"""
    )

    parsed_arguments = parser.parse_args(args)

    run_function(parsed_arguments)

def run_function(parsed_arguments):
    """
    Depending on the chosen rest verb, this function calls
    the relevant function sub-tree to be executed.
        :param parsed_arguments: (Namespace) Namespace containing the parsed command line arguments.
        :return: None
        :raises: ValueError: if invalid argument given
    """
    if parsed_arguments.verb == REST_GET:
        run_get_requests(parsed_arguments)
    elif parsed_arguments.verb == REST_POST:
        run_post_requests(parsed_arguments)
    elif parsed_arguments.verb ==  REST_PUT:
        run_put_requests(parsed_arguments)
    elif parsed_arguments.verb == REST_DELETE:
        run_delete_requests(parsed_arguments)
    else:
        raise ValueError("%s is an invalid verb value" % parsed_arguments.verb)

def run_get_requests(parsed_arguments):
    """
    run get functions depending on given object_to_fetch arguments.
        :param parsed_arguments: (Namespace) Namespace containing the parsed command line arguments.
        :return: None
        :raises: ValueError: if invalid object_to_fetch argument given
    """
    if parsed_arguments.object_to_fetch == COLLECTION_OBJECT:
        get_user_collections()
    elif parsed_arguments.object_to_fetch == GAME_OBJECT:
        get_game_requests(parsed_arguments.game_id)
    else:
        raise ValueError("%s is an invalid object value" % parsed_arguments.object_to_fetch)

def run_post_requests(parsed_arguments):
    """
    run post functions depending on given function arguments.
        :param parsed_arguments: (Namespace) Namespace containing the parsed command line arguments.
        :return: None
        :raises: ValueError: if invalid function argument given
    """
    if parsed_arguments.function == LOGIN:
        login(parsed_arguments.username, parsed_arguments.password)
    elif parsed_arguments.function == LOGOUT:
        logout()
    elif parsed_arguments.function ==  SIGNUP:
        signup(
            parsed_arguments.username,
            parsed_arguments.password,
            parsed_arguments.name,
            parsed_arguments.date_of_birth,
            parsed_arguments.favourite_game_type,
            parsed_arguments.favourite_game_genre
        )
    elif parsed_arguments.function ==  CREATE_COLLECTION:
        create_collection()
    else:
        raise ValueError("%s is an invalid function value" % parsed_arguments.function)

def run_put_requests(parsed_arguments):
    """
    run put functions depending on given function arguments.
        :param parsed_arguments: (Namespace) Namespace containing the parsed command line arguments.
        :return: None
        :raises: ValueError: if invalid argument combination given
    """
    # Currently the only put call is to add games to a collection.
    if parsed_arguments.collection_id and parsed_arguments.game_id:
        add_game_to_collection(parsed_arguments.collection_id, parsed_arguments.game_id)
    else:
        raise ValueError("you need to specify game_id and collection_id for a put request")

def run_delete_requests(parsed_arguments):
    """
    run delete functions depending on given function arguments.
        :param parsed_arguments: (Namespace) Namespace containing the parsed command line arguments.
        :return: None
        :raises: ValueError: if invalid argument combination given
    """
    if parsed_arguments.collection_id and parsed_arguments.game_id:
        remove_game_from_collection(
           parsed_arguments.collection_id, parsed_arguments.game_id)
    elif parsed_arguments.collection_id:
        delete_collection(parsed_arguments.collection_id)
    else:
        raise ValueError("you need to specify collection_id" +
            " if you're planning to delete one of your collections." +
            " Or game_id and collection_id if you want to delete" +
            " a specific game from a given collection")


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

def get_game_requests(game_id):
    """
    This function fetches games from the database.
    if the game_id is provided it will fetch the specific game.
    If no game_id is provided it will fetch all games within the game datastore
        :param parsed_arguments: (str or None) If provided,
            the game_id of the specific game to fetch.
        :return: None
    """
    games_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            GAME_DATA_STORE_PATH
        )
    )

    if game_id:
        game_id = str(game_id).lower()
        game_row = games_df[games_df['game_id'].str.contains(game_id)]
        print(game_row)

    else:
        print(games_df)

def login(username, password):
    """
    Logs in the user with the given username and password
    and sets the logged in user's user_id in the auth cookies file
    to allow easier usage of the tool.
        :param username: (str) username provided by user.
        :param password: (str) password provided by user.
        :return: None.
    """
    users_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            USER_DATA_STORE_PATH
        )
    )
    if username in users_df.username.values:
        if users_df.loc[users_df.username == username,'password'].tolist()[0] == password:
            with open(
                os.path.join(os.path.abspath(os.path.dirname(__file__)),
                AUTH_COOKIES_PATH
            ), "w") as auth_cookies:
                auth_cookies.write(
                    users_df.loc[users_df.username == username,'user_id'].tolist()[0])
                auth_cookies.close()
            print("Logged in successfully")
            return

    print("username and/or password is incorrect. "
        + "If you don't have an account please use sign up.")

def logout():
    """
    Logs out the current logged in user by resetting the auth_cookies file
        :return: None
    """
    with open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
        AUTH_COOKIES_PATH
    ), "w") as auth_cookies:
        auth_cookies.truncate()
        auth_cookies.close()

def signup(
    username,
    password,
    name,
    date_of_birth,
    favourite_game_type = '',
    favourite_game_genre = ''
):
    """
    Signs up a new user by capturing the needed information and storing it into the users datastore.
    Certain arguments are required so if they are not passed in an error will be raised.
    Username has to be unique therefore an error is raised if the username already exists.
        :param username: (str) username provided by user.
        :param password: (str) password provided by user.
        :param name: (str) full name of the user.
        :param date_of_birth: (str) date of birth provided by user.
        :param favourite_game_type: (str) favourite game type of the user.
        :param favourite_game_genre: (str)favourite game genre of the user.
        :return: None
    """
    # if required arguments are not all passed in
    if not (username and password and name and date_of_birth):
        print("For signing up a new account, username, password,"
          + "data of birth and full name is required."
          + "Please make sure you add all necessary information.")
        return
    users_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            USER_DATA_STORE_PATH
        )
    )
    # if username already exists
    if username in users_df.username.values:
        print("This username already exists, please choose a different username.")
        return

    # user_ids are created incrementally, create a new id based on the size of the users csv.
    # If the incremental id is taken (there is an issue in indexing),
    # create a new id via choosing a higher number that is not taken.
    length = len(users_df)
    user_id = "u_" + str(length + 1)
    i = 2
    while user_id in users_df.user_id.values:
        user_id = "u_" + str(length + i)
        i += 1

    new_data_row_df = pd.DataFrame(
        [
            {
                'user_id':user_id,
                'username': username,
                'full_name': name,
                'password': str(password),
                'date_of_birth': date_of_birth,
                'favourite_game_type': favourite_game_type,
                'favourite_genre': favourite_game_genre,
                'row_creation_time_utc': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    new_data_row_df.to_csv(
      os.path.join(
          os.path.abspath(os.path.dirname(__file__)),
          USER_DATA_STORE_PATH
      ),
      mode='a',
      index = False,
      header=False
    )

    login(username, password)
    print("new user (with id: %s) was successfully created. "%user_id
    + "You are now logged in as %s."%username)

def create_collection():
    """
    creates a new empty collection for the logged in users.
    If the user is not logged in, it will ask the user to log in or sign up.
        :return: (str) collection_id of the newly created collection.
    """
    if not get_logged_in_user():
        print("You need to be logged in to create a collections." +
            " Please log into your account or sign up if you don't have an account.")
        return

    collections_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            COLLECTION_DATA_STORE_PATH
        )
    )

    # Collection_ids are created incrementally,
    # create a new id based on the size of the collection csv.
    # If the incremental id is taken (there is an issue in indexing)
    # create a new id via choosing a higher number that is not taken.
    length = len(collections_df)
    collection_id = "c_" + str(length + 1)
    i = 2
    while collection_id in collections_df.collection_id.values:
        collection_id = "c_" + str(length + i)
        i += 1

    new_data_row_df = pd.DataFrame(
        [
            {
                'collection_id':collection_id,
                'user_id': get_logged_in_user(),
                'game_ids': '',
                'row_creation_time_utc': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                'row_updated_time_utc': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    new_data_row_df.to_csv(
      os.path.join(
          os.path.abspath(os.path.dirname(__file__)),
          COLLECTION_DATA_STORE_PATH
      ),
      mode='a',
      index = False,
      header=False
    )
    print("new collection (with id: %s) was successfully created."%collection_id
    + "The collection is currently empty, you can add games to it via the add functionality.")

def add_game_to_collection(collection_id, game_id):
    """
    adds an existing game to an existing collection_id.
        :param collection_id: (str) collection_id of the collection the game will be added to.
        :param game_id: (str) game_id of the game that will be added to the collection.
        :return: None
    """
    collections_df = get_collections_with_permission_check(collection_id)
    if collections_df is None:
        return

    game_ids = collections_df.loc[collections_df.collection_id == collection_id,'game_ids']
    # check if game already exists in collection, if so no need to add it again.
    games_array = game_ids.values[0].replace(" ", "").split(",")
    if game_id in games_array:
        print("Game with game_id: %s already exists"% game_id
            + " in this collection (collection_id: %s)"% collection_id)
        return

    collections_df.loc[collections_df.collection_id == collection_id,'game_ids'
        ] = game_ids + ", " + game_id
    # TODO currently the whole collection_df is rewritten
    # to make it easier to change game_ids string arrays,
    # this should be changed to a more scalable approach
    # once database tables are used
    collections_df.to_csv(
          os.path.join(
              os.path.abspath(os.path.dirname(__file__)),
              COLLECTION_DATA_STORE_PATH
          ),
          mode='w',
          index = False,
          header=True
    )
    print("game with game_id: %s was successfully added"% game_id
        + " to collection with collection_id: %s"% collection_id)

def remove_game_from_collection(collection_id, game_id):
    """
    remove an existing game from a specific collection_id.
        :param collection_id: (str) collection_id of the collection the game will be removed from.
        :param game_id: (str) game_id of the game that will be removed from the collection.
        :return: None
    """
    collections_df = get_collections_with_permission_check(collection_id)
    if collections_df is None:
        return

    game_ids = collections_df.loc[collections_df.collection_id == collection_id,'game_ids']
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
          os.path.join(
              os.path.abspath(os.path.dirname(__file__)),
              COLLECTION_DATA_STORE_PATH
          ),
          mode='w',
          index = False,
          header=True
    )
    print("game with game_id: %s was successfully removed" % game_id
    + " from collection with collection_id: %s"%collection_id)

def delete_collection(collection_id):
    """
    deletes a given collection, the collection has to be owned by the logged in users.
        :param collection_id: (str) collection_id of the collection that will be removed.
        :return: None.
    """
    collections_df = get_collections_with_permission_check(collection_id)
    if collections_df is None:
        return

    row_index = collections_df[collections_df.collection_id == collection_id].index
    collections_df = collections_df.drop(row_index)

    # TODO currently the whole collection_df is rewritten
    # to make it easier to change game_ids string arrays,
    # this should be changed to a more scalable approach
    # once database tables are used
    collections_df.to_csv(
        os.path.join(
          os.path.abspath(os.path.dirname(__file__)),
          COLLECTION_DATA_STORE_PATH
        ),
        mode='w',
        index = False,
        header=True
    )
    print("collection with collection_id: %s was successfully deleted"%(collection_id))

def get_collections_with_permission_check(collection_id):
    """
    Gets the collection data if the logged in user is allowed to make modifications
    to the given collection_id. If the collection is not owned by the logged in user
    a permission error will be raised.
        :param collection_id: (str) collection_id of the collection that will be removed.
        :return: (None or dataframe) collections dataframe if the user is allowed to
            modify the given collection_id, otherwise None.
        :raises: PermissionError: if collection_id belongs to
            a collection that is not owned by the user.
    """
    if not get_logged_in_user():
        print("You need to be logged in to see your collections." +
        " Please log into your account or sign up if you don't have an account.")
        return

    collections_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            COLLECTION_DATA_STORE_PATH
        )
    )

    collection_row = collections_df.loc[collections_df.collection_id == collection_id]
    if collection_row.user_id.values[0] != get_logged_in_user():
        raise PermissionError("You can only modify a collection you own. "+
            "Please select one of your collections.")

    return collections_df

def valid_verb(verb):
    """
    Ensure valid verb argument is provided to fail fast if invalid.
        :param verb: (str) user given argument to test
        :return: rest_verb: (str) valid rest verb
        :raises: ArgumentTypeError: if invalid argument given
    """
    rest_verb = str(verb).upper()
    if rest_verb not in REST_VERBS:
        raise ArgumentTypeError("%s is an invalid verb value" % rest_verb)
    return rest_verb

def valid_object(object_to_fetch):
    """
    Ensure valid object_to_fetch argument is provided to GET call.
        :param object_to_fetch: (str) user given argument for object to fetch
        :return: object_to_fetch: (str) valid object that can be fetched
        :raises: ArgumentTypeError: if invalid argument given
    """
    object_to_fetch = str(object_to_fetch).upper()
    if object_to_fetch not in VALID_OBJECTS_TO_FETCH:
        raise ArgumentTypeError("%s is an invalid object value" % object_to_fetch)
    return object_to_fetch

def valid_game_id(game_id):
    """
    Ensure valid game_id argument is provided and the game exists in the game database.
        :param game_id: (str) user given argument for game_id
        :return: game_id: (str) valid game_id that exists in the datastore
        :raises: ArgumentTypeError: if invalid argument given, game doesn't exist in datastore.
    """
    game_id = str(game_id).lower()
    games_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            GAME_DATA_STORE_PATH
        )
    )

    if game_id not in games_df.game_id.values :
        raise ArgumentTypeError("%s is an invalid game_id value. " % game_id
            + "This game does not exist in the game data store.")
    return game_id

def valid_function(function):
    """
    Ensure valid function argument is provided to POST call.
        :param function: (str) user given argument for function to be called
        :return: function: (str) valid function that can be acted on
        :raises: ArgumentTypeError: if invalid argument given
    """
    function_to_be_posted = str(function).upper()
    if function_to_be_posted not in VALID_POST_FUNCTIONS:
        raise ArgumentTypeError("%s is an invalid function value" % function_to_be_posted)
    return function_to_be_posted

def valid_type(favourite_game_type):
    """
    Ensure valid game type argument is provided.
        :param favourite_game_type: (str) favourite game type provided by user
        :return: favourite_game_type: (str) valid favourite_game_type that can be stored
        :raises: ArgumentTypeError: if invalid argument given
    """
    if str(favourite_game_type).upper() not in VALID_GAME_TYPE:
        raise ArgumentTypeError("%s is an invalid game type."% favourite_game_type +
            " you should choose from the following genres: %s, %s, %s, %s"
            % (CARD,BOARD,MINIATURE,ROLE))
    return favourite_game_type

def valid_collection_id(collection_id):
    """
    Ensure valid collection_id argument is provided
    and the collection exists in the collection database.
        :param collection_id: (str) user given argument for collection_id
        :return: collection_id: (str) valid collection_id that exists in the datastore
        :raises: ArgumentTypeError: if invalid argument given,
            collection doesn't exist in datastore.
    """
    collection_id = str(collection_id).lower()
    collection_df = pd.read_csv(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            COLLECTION_DATA_STORE_PATH
        )
    )

    if collection_id not in collection_df.collection_id.values :
        raise ArgumentTypeError("%s is an invalid collection_id value" % collection_id)
    return collection_id

def get_logged_in_user():
    """
    returns the user_id of the logged in users from the auth cookies file.
    If user is not logged in it returns null.
        :return: None
    """
    with open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), AUTH_COOKIES_PATH), "r") as auth_cookies:
        logged_in_user = auth_cookies.readline()
        auth_cookies.close()
    return logged_in_user

def copy_seed_data():
    """
    Populate local environment data store with initial data.
    :return: None
    """
    print("Initiating data store")
    shutil.copytree(
          os.path.join(
                os.path.abspath(
                        os.path.dirname(__file__)
                ),
                SAMPLE_DATA_STORE
          ),
         os.path.join(
                os.path.abspath(
                        os.path.dirname(__file__)
                ),
                MAIN_DATA_STORE
         ),
         dirs_exist_ok = True
    )
    print("Complete")

if __name__ == "__main__":
    # pass command line arguments through to main function
    # except for the first element of sys.argv which represents the script name
    # this allows for start() to be called programmatically for more convenient testing
    start(sys.argv[1:])
