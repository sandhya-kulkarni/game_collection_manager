"""
USER API endpoints with CSV adapter.
Supported calls:
    get_users
"""
from .config import *


def users_help(parser, verb):
    """
    Extend help text with options specific to users object
    :param parser: (ArgumentParser) the existing help object being built.
    :param verb: (str) optional rest verb to limit scope of help given.
    :return: parser: (ArgumentParser) with extended help arguments
    """
    def get():
        parser.add_argument(
            "--id",
            type=str,
            help="Optional id to limit the information returned to a single user object."
        )

    def post():
        parser.add_argument(
            "--username",
            required=True,
            type=str,
            help="username provided by the user to log in or sign up"
        )
        parser.add_argument(
            "--password",
            required=True,
            type=str,
            help="password provided by the user to log in or sign up"
        )
        parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="""
                    full name provided by the user to sign up.
                    This should be wrapped in quotation marks if spaces are required.
                 """
        )
        parser.add_argument(
            "--date_of_birth",
            required=True,
            type=str,
            help="date of birth provided by user to sign up in the format of DD/MM/YYYY"
        )
        parser.add_argument(
            "--favourite_game_type",
            type=str,
            choices={"Board Game", "Card Game", "Role Playing Game", "Miniature War Game"},
            help="Optional favourite game type provided by the user at sign up."
        )
        parser.add_argument(
            "--favourite_genre",
            type=str,
            choices={"Fantasy", "Other", "Horror", "War"},
            help="Optional favourite game genre provided by the user at sign up."
        )

    if verb == "GET":
        get()
    elif verb == "POST":
        post()
    else:
        get()
        post()

    return parser


def users_usage(parsed_args):
    """
    Return data specific to arguments given relating to users object
    :param parsed_args: the arguments given by the user after being successfully parsed.
    :return: (*) result of given arguments
    """
    if parsed_args.verb == "GET":
        df = get_users(parsed_args.id)
    if parsed_args.verb == "POST":
        df = get_users()
        df = signup(
            df,
            parsed_args.username,
            parsed_args.password,
            parsed_args.name,
            parsed_args.date_of_birth,
            parsed_args.favourite_game_type,
            parsed_args.favourite_genre
        )
    return df


# CONTROLLERS
def get_users(user_id=None):
    """
    Return all available user data.
    :param user_id: (str) Optional user id to return information on a single user.
    :return: (pd.DataFrame)
    """
    df = validate_data_store(user_file, user_terms)
    if user_id is not None:
        df = df.loc[df['user_id'] == user_id]

    return df


def signup(
    input_df,
    username,
    password,
    name,
    date_of_birth,
    favourite_game_type="",
    favourite_game_genre=""
):
    """
    Signs up a new user by capturing the needed information and storing it into the users datastore.
    Certain arguments are required so if they are not passed in an error will be raised.
    Username has to be unique therefore an error is raised if the username already exists.
        :param input_df: (pd.DataFrame) input pandas data frame.
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
        print(
            "For signing up a new account, username, password," +
            "data of birth and full name is required.\n" +
            "Please make sure you add all necessary information."
        )
        return
    users_df = input_df
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
                'user_id': user_id,
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
      user_file,
      mode='a',
      index=False,
      header=False
    )

    create_empty_collection(user_id)

    print("new user (id: {}) was successfully created. ".format(user_id))
    return new_data_row_df


def create_empty_collection(user_id):
    """
    creates a new empty collection for recently signed up user.
    :param: user_id (str) user_id that the new collection is associated with.
    :return: (str) collection_id of the newly created collection.
    """
    collections_df = validate_data_store(collection_file, collection_terms)

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
                'collection_id': collection_id,
                'user_id': user_id,
                'game_ids': '',
                'row_creation_time_utc': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                'row_updated_time_utc': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    new_data_row_df.to_csv(
      collection_file,
      mode='a',
      index=False,
      header=False
    )
    print("new collection (id: {}) successfully created.".format(collection_id))
    return new_data_row_df


# TODO - CONNECT THIS WITH CLI FUNCTION IF REQUIRED.
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


# USER DATA STORE
user_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    API_DATA_STORE + USER_DATA
)
# required columns
user_terms = [
    "user_id",
    "username",
    "password",
    "date_of_birth",
    "favourite_game_type",
    "favourite_genre"
]
# COLLECTION DATA STORE
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