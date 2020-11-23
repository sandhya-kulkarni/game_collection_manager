"""
Unit tests for game filter function
"""
import os
import pandas as pd
import pytest
from api.utilities import filter


# Sample Data
# todo - create mock data for tests
game_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../sample_data/games.csv"
)
review_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../sample_data/reviews.csv"
)
game_df = pd.read_csv(game_file)
review_df = pd.read_csv(review_file)


def test_arguments():
    """
    1) Expect TypeError if no arguments given
    2) Expect TypeError if second argument is not a dictionary of key-value pairs by which to filter
    3) Expect KeyError if filter_dict key is not within input_df
    :return: None
    """
    # Scenario 1
    with pytest.raises(TypeError):
        filter.data_frame()   # pylint: disable=no-value-for-parameter
    # scenario 2
    with pytest.raises(TypeError):
        filter.data_frame(game_df, {})
    # scenario 3
    with pytest.raises(KeyError):
        filter.data_frame(game_df, {"games_ids": "g1"})


def test_return():
    """
    1) Expect 0 items to be returned if filter key is valid, but value is not present in input list
    2) Expect data frame as return, of length matching items through equality
    3) Have multiple filters combine in AND fashion
    :return: None
    """
    # scenario 1
    x = filter.data_frame(game_df, {"game_id": "g0"})
    assert len(x) == 0
    # scenario 2
    x = filter.data_frame(game_df, {"game_type": "Board Game", "game_id": "g1"})
    assert isinstance(x, pd.DataFrame)
    assert len(x) == 1
