#!/usr/bin/env python3
"""
The program processes user, game and review data as inputs and outputs an ordered list of game
recommendations for a given scenario.
"""

from argparse import ArgumentParser, ArgumentTypeError
import os
import sys


REST_VERBS = ["GET", "POST", "PUT", "DELETE"]


def start(args):
    """
    Main module function.
    :return: None
    """
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
    parsed_arguments = parser.parse_args(args)

    # Check if local data store has been initialised
    user_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "../data_store/user.csv"
    )
    if not os.path.exists(user_file):
        print("No active data store detected.")
        seed_data()
    print("Complete")


def valid_verb(verb):
    """
    Ensure valid verb argument is provided to fail fast if invalid.
        :param verb: (str) user given argument to test
        :return: rest_verb: (str) valid rest verb
        :raises: ArgumentTypeError: if invalid argument given
    """
    rest_verb = str(verb).upper()
    if rest_verb not in REST_VERBS:
        raise ArgumentTypeError("%s is an invalid verb value" % verb)
    return rest_verb


def seed_data():
    """
    Populate local environment data store with initial data.
    :return: None
    """
    print("Initiating data store")


if __name__ == "__main__":
    # pass command line arguments through to main function
    # except for the first element of sys.argv which represents the script name
    # this allows for sim() to be called programmatically for more convenient testing
    start(sys.argv[1:])
