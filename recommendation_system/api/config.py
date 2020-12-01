"""
Config Values and common imports.
"""
from datetime import datetime
import errno
import os
import pandas as pd

# HTTP / RESTful VERBS
REST_GET = "GET"        # Read
REST_POST = "POST"      # Create
REST_PATCH = "PATCH"    # Update / Modify
REST_PUT = "PUT"        # Update / Replace
REST_DELETE = "DELETE"  # Delete
REST_VERBS = [
    REST_GET,
    REST_POST,
    REST_PATCH,
    REST_PUT,
    REST_DELETE
]

# OBJECTS
GAME_OBJECT = "GAMES"
USER_OBJECT = "USERS"
COLLECTION_OBJECT = "COLLECTIONS"
VALID_OBJECTS_TO_FETCH = [
    GAME_OBJECT,
    USER_OBJECT,
    COLLECTION_OBJECT
]

# DATA STORE
MAIN_DATA_STORE = "../data_store/"
SAMPLE_DATA_STORE = "./sample_data/"
API_DATA_STORE = "../"+MAIN_DATA_STORE

COLLECTION_DATA = "collections.csv"
GAME_DATA = "games.csv"
REVIEW_DATA = "reviews.csv"
USER_DATA = "users.csv"
REQUIRED_DATA_FILES = [
    COLLECTION_DATA,
    GAME_DATA,
    REVIEW_DATA,
    USER_DATA
]


def validate_data_store(file, terms):
    """
    Utility function to ensure csv data is accessible and can be read into a panda's DataFrame
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

# For GET calls

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

AUTH_COOKIES_PATH = "../../auth_cookies.txt"

GAME_DATA_STORE_PATH = "../../data_store/games.csv"
COLLECTION_DATA_STORE_PATH = "../../data_store/collections.csv"
REVIEW_DATA_STORE_PATH = "../../data_store/reviews.csv"
USER_DATA_STORE_PATH = "../../data_store/users.csv"