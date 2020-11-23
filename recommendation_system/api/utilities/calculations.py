"""
Utility functions to process data frames and include additional numerical data columns.
"""
import pandas as pd


def game_review_mean(game_df, review_df, sort_by="overall_score", weighting=[0, 0, 0, 1]):
    """
    Calculates mean/weighted mean and returns sorted game data by review score of given arguments.
    :param game_df: (pd.DataFrame) input game data (already filtered if required)
    :param review_df: (pd.DataFrame) input review data
    :param sort_by: optional (str) property to calculate mean score value for and sort results by.
    Must be either "complexity_score", "gameplay_score", "visual_score", or "overall_score"
    :param weighting: optional (int list) if sort_by is "overall_score", a user supplied weighting
    may be used to calculate a weighted average of all the properties.
    If no weighting is supplied, then standard arithmetic mean is calculated for "overall_score".
    :return: sorted_return: (pd.DataFrame) game data sorted in desc. order of given arguments.
    :raises TypeError: if arguments are not as expected.
    """
    # todo - slight duplication, can be extracted
    # test arguments:
    # game_df and review_df are data frames of respective data
    if not isinstance(game_df, pd.DataFrame):
        raise TypeError("game_df must be a valid data frame of game data")
    if not isinstance(review_df, pd.DataFrame):
        raise TypeError("review_df must be a valid data frame of review data")
    # sort_by is str value of "complexity_score", "gameplay_score", "visual_score", "overall_score"
    valid_sort_by = ["complexity_score", "gameplay_score", "visual_score", "overall_score"]
    if type(sort_by) != str or sort_by not in valid_sort_by:
        raise TypeError("sort_by must be one of the following: {}".format(", ".join(valid_sort_by)))
    # weighting is list of ints, 4 length in size with each between 0-10
    if type(weighting) != list or len(weighting) != 4 or not all(type(n) is int for n in weighting):
        raise TypeError("weighting must be a list of 4 int values")

    # filter reviews by game_ids present in game_df
    game_ids = list(game_df["game_id"].unique())
    filtered_reviews = review_df[review_df["game_id"].isin(game_ids)]
    # determine mean calculation method - either simple or weighted
    if sort_by == "overall_score" and weighting != [0, 0, 0, 1]:
        # weighted average
        print("weighted average")
        mean_values = filtered_reviews.groupby('game_id').mean().reset_index()
        weighted_mean = [0] * len(mean_values)
        # todo - check if theres a better way
        total_weight = sum(weighting)
        print(total_weight)
        for index, row in mean_values.iterrows():
            weighted_mean[index] =\
                sum([
                    row["complexity_score"]*weighting[0],
                    row["gameplay_score"]*weighting[1],
                    row["visual_score"]*weighting[2],
                    row["overall_score"]*weighting[3]
                ])/total_weight
        mean_values["mean"] = weighted_mean
        print(mean_values)
    else:
        # calculate list of simple mean scores
        mean_values = filtered_reviews.groupby('game_id')[sort_by].mean().reset_index()
        # simplify column names to game_id and mean
        mean_values.columns = ["game_id", "mean"]
    # merge mean calculations into game details as this will be how they are presented
    return_df = pd.merge(game_df, mean_values, on="game_id")
    sorted_return = return_df.sort_values(by=["mean"], ascending=False)
    return sorted_return
