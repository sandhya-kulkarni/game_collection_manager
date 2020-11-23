"""
Utility function to filter a given input by various arguments.
"""
import pandas as pd


def data_frame(input_df, filter_dict):
    """
    Filter a given data frame by a dictionary of key-value pairs.
    Currently only supports equality matches ("a" == "a").
    :param input_df: (pd.DataFrame) input pandas data frame before filter
    :param filter_dict: optional (dict) key-value pairs by which to filter given input item_list
    :return: output_df: (pd.DataFrame) output pandas data frame after filter
    :raises: TypeError: if arguments are not as expected
    :raises: KeyError: if given key within filter_dict does not exist within input_df.
    """
    # test arguments: input_df is as expected and filter_dict is dict of at least 1 key-value pair
    if not isinstance(input_df, pd.DataFrame):
        raise TypeError("input_df must be a valid data frame")
    if type(filter_dict) != dict or len(filter_dict) == 0:
        raise TypeError("filter_dict must be a dictionary with at least one key-value pair")
    # iterate over filter keys and query by key-value pair
    for key in filter_dict:
        try:
            ouput_df = input_df.query(key+'=="'+filter_dict[key]+'"')
        except NameError as err:
            raise KeyError("Invalid filter_dict given: {}".format(err)) from None
    return ouput_df
