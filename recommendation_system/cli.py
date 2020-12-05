#!/usr/bin/env python3
"""
The program processes user, game and review data as inputs and outputs an ordered list of game
recommendations for a given scenario.
"""
from argparse import ArgumentParser, ArgumentTypeError, RawDescriptionHelpFormatter
import shutil
import sys

from api.config import *
from api.games import games_help, games_usage
from api.users import users_help, users_usage
from api.collections import collections_help, collections_usage
from api.recommendations import recommendations_help, recommendations_usage


def start(args):
    """
    Main module function.
    :return: None
    """
    parser = ArgumentParser(
        prog="RECOMMENDATION SYSTEM\n",
        description="The program processes user, game and review data and outputs an ordered list\n"
                    "of game recommendations for a given user and scenario.\n"
                    "The CLI mimics the behaviour of a webserver, expecting HTTP verbs [-v],\n"
                    "an endpoint object [-o] and optional inputs as arguments.\n\n"
                    "For example:        -v GET -o GAMES\n\n"
                    "For assistance on optional inputs available for a given object, please pass\n"
                    "the help flag [-h] along with the desired option.\n\n"
                    "Help example:       -o GAMES -h\n\n",
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--verb",
        choices=REST_VERBS,
        type=valid_verb,
        required=True,
        help="Verb signifying intent with given endpoint object."
    )
    parser.add_argument(
        "-o",
        "--object",
        choices=VALID_OBJECTS_TO_FETCH,
        type=valid_object,
        required=True,
        help="The endpoint object that is to be fetched, or manipulated."
    )
    parser.add_argument(
        "--output",
        choices=["DataFrame", "JSON"],
        default="DataFrame",
        type=str,
        help="How you would like to view the return output of a given argument."
    )

    # cache object and verb before parsing args
    object_arg = None
    verb_arg = None
    if "-o" in args or "--object" in args:
        object_index = args.index("-o" or "--object")
        object_arg = args[object_index + 1]
    if "-v" in args or "--verb" in args:
        verb_index = args.index("-v" or "--verb")
        verb_arg = args[verb_index + 1]

    # test if help flag is present in args
    # to extend help options if either verb or object is defined
    if "-h" or "--help" in args:
        # ADD GAMES
        if object_arg == "GAMES":
            games_help(parser, verb_arg)
        # ADD USERS
        if object_arg == "USERS":
            users_help(parser, verb_arg)
        # ADD COLLECTIONS
        if object_arg == "COLLECTIONS":
            collections_help(parser, verb_arg)
        # ADD RECOMMENDATIONS
        if object_arg == "RECOMMENDATIONS":
            recommendations_help(parser, verb_arg)

    # will exit as soon as arguments parsed if -h is present
    parsed_arguments = parser.parse_args(args)

    # Check if local data store has been initialised
    # with all required files
    for file in REQUIRED_DATA_FILES:
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            MAIN_DATA_STORE + file
        )
        if not os.path.exists(file_path):
            copy_seed_data()

    # execute given argument
    if object_arg == "GAMES":
        df = games_usage(parsed_arguments)
    if object_arg == "USERS":
        df = users_usage(parsed_arguments)
    if object_arg == "COLLECTIONS":
        df = collections_usage(parsed_arguments)
    if object_arg == "RECOMMENDATIONS":
        df = recommendations_usage(parsed_arguments)

    # return output as directed
    if parsed_arguments.output == "JSON":
        print(df.to_json(orient="records"))
    else:
        print(df)


# TYPE VALIDATION
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


def copy_seed_data():
    """
    Populate local environment data store with initial data.
    :return: None
    """
    print("Unable to find all required data files...")
    print("Initiating data store...")
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
        dirs_exist_ok=True
    )
    print("Complete")


if __name__ == "__main__":
    # pass command line arguments through to main function
    # except for the first element of sys.argv which represents the script name
    # this allows for start() to be called programmatically for more convenient testing
    start(sys.argv[1:])