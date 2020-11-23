"""
Unit tests for mean calculations
"""
import os
import pandas as pd
import pytest
from api.utilities import calculations


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
    2) Expect TypeError if required arguments do not match signature:
        game data (pd.DataFrame),
        review data (pd.DataFrame),
        optional sort_by: "complexity_score", "gameplay_score", "visual_score", or "overall_score"
        optional weighting: int list, 4 size in length
    :return: None
    """
    # Scenario 1
    with pytest.raises(TypeError):
        calculations.game_review_mean()   # pylint: disable=no-value-for-parameter
    # Scenario 2
    with pytest.raises(TypeError):
        calculations.game_review_mean("a", "b")
    with pytest.raises(TypeError):
        calculations.game_review_mean("a", review_df)
    with pytest.raises(TypeError):
        calculations.game_review_mean(game_df, "b")
    with pytest.raises(TypeError):
        calculations.game_review_mean(game_df, review_df, "my_score")
    with pytest.raises(TypeError):
        calculations.game_review_mean(game_df, review_df, "overall_score", [1])


def test_return():
    """
    1) Expect return data frame of only unique game items (identified by game_id)
    2) Expect return to be sorted by computed property mean in descending order
    3) Expect computed property mean to be float, accurate to within pytest.approx
    :return: None
    """
    x = calculations.game_review_mean(game_df, review_df)
    # scenario 1
    assert len(x) == 50
    # scenario 2
    assert x.iloc[0]["mean"] >= x.iloc[1]["mean"] >= x.iloc[2]["mean"]
    # scenario 3
    assert x.iloc[0]["mean"] == pytest.approx(3.50)
