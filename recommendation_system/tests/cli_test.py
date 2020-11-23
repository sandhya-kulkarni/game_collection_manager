#!/usr/bin/env python3
"""
The file tests the CLI functionalities.
"""
import argparse
from recommendation_system import cli
import pytest
from mock import patch, MagicMock

@patch('recommendation_system.cli.run_get_requests', MagicMock(return_value=None))
@patch('recommendation_system.cli.run_post_requests', MagicMock(return_value=None))
@patch('recommendation_system.cli.run_put_requests', MagicMock(return_value=None))
@patch('recommendation_system.cli.run_delete_requests', MagicMock(return_value=None))
def test_run_function(
    mock_get_verb_cli_arguments,
    mock_post_verb_cli_arguments,
    mock_put_verb_cli_arguments,
    mock_delete_verb_cli_arguments,
    mock_invalid_verb_cli_arguments
):
    """
    Tests the run_function to call the relevant function sub-tree
    depending on the chosen rest verb.
    """

    # execute run_function with get rest verb
    # and assert the correct function was called.
    cli.run_function(mock_get_verb_cli_arguments)
    cli.run_get_requests.assert_called_once()
    cli.run_post_requests.assert_not_called()
    cli.run_put_requests.assert_not_called()
    cli.run_delete_requests.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_function with post rest verb
    # and assert the correct function was called.
    cli.run_get_requests.reset_mock()
    cli.run_function(mock_post_verb_cli_arguments)
    cli.run_post_requests.assert_called_once()
    cli.run_get_requests.assert_not_called()
    cli.run_put_requests.assert_not_called()
    cli.run_delete_requests.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_function with put rest verb
    # and assert the correct function was called.
    cli.run_post_requests.reset_mock()
    cli.run_function(mock_put_verb_cli_arguments)
    cli.run_put_requests.assert_called_once()
    cli.run_get_requests.assert_not_called()
    cli.run_post_requests.assert_not_called()
    cli.run_delete_requests.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_function with delete rest verb
    # and assert the correct function was called.
    cli.run_put_requests.reset_mock()
    cli.run_function(mock_delete_verb_cli_arguments)
    cli.run_delete_requests.assert_called_once()
    cli.run_get_requests.assert_not_called()
    cli.run_put_requests.assert_not_called()
    cli.run_post_requests.assert_not_called()

    with pytest.raises(ValueError):
        cli.run_function(mock_invalid_verb_cli_arguments)

@patch('recommendation_system.cli.get_user_collections', MagicMock(return_value=None))
@patch('recommendation_system.cli.get_game_requests', MagicMock(return_value=None))
def test_run_get_requests(
    mock_get_verb_cli_arguments_with_invalid_object,
    mock_get_verb_cli_arguments_with_games_object,
    mock_get_verb_cli_arguments_with_collections_object
):
    """
    Tests the run_get_requests to call the relevant function depending on object_to_fetch.
    """

    # execute run_get_requests with games object
    # and assert the correct function was called.
    cli.run_get_requests(mock_get_verb_cli_arguments_with_games_object)
    cli.get_game_requests.assert_called_once()
    cli.get_user_collections.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_get_requests with collections object
    # and assert the correct function was called.
    cli.get_game_requests.reset_mock()
    cli.run_get_requests(mock_get_verb_cli_arguments_with_collections_object)
    cli.get_user_collections.assert_called_once()
    cli.get_game_requests.assert_not_called()

    with pytest.raises(ValueError):
        cli.run_get_requests(mock_get_verb_cli_arguments_with_invalid_object)

@patch('recommendation_system.cli.login', MagicMock(return_value=None))
@patch('recommendation_system.cli.logout', MagicMock(return_value=None))
@patch('recommendation_system.cli.signup', MagicMock(return_value=None))
@patch('recommendation_system.cli.create_collection', MagicMock(return_value=None))
def test_run_post_requests(
    mock_post_verb_cli_arguments_with_login_func,
    mock_post_verb_cli_arguments_with_logout_func,
    mock_post_verb_cli_arguments_with_signup_func,
    mock_post_verb_cli_arguments_with_create_collection_func,
    mock_post_verb_cli_arguments_with_invalid_func
):
    """
    Tests the run_post_requests to call the relevant
    function depending on the function argument passed.
    """

    # execute run_post_requests with login function
    # and assert the correct function was called.
    cli.run_post_requests(mock_post_verb_cli_arguments_with_login_func)
    cli.login.assert_called_once()
    cli.logout.assert_not_called()
    cli.signup.assert_not_called()
    cli.create_collection.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_post_requests with logout function
    # and assert the correct function was called.
    cli.login.reset_mock()
    cli.run_post_requests(mock_post_verb_cli_arguments_with_logout_func)
    cli.logout.assert_called_once()
    cli.login.assert_not_called()
    cli.signup.assert_not_called()
    cli.create_collection.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_post_requests with signup function
    # and assert the correct function was called.
    cli.logout.reset_mock()
    cli.run_post_requests(mock_post_verb_cli_arguments_with_signup_func)
    cli.signup.assert_called_once()
    cli.login.assert_not_called()
    cli.logout.assert_not_called()
    cli.create_collection.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_post_requests with create_collection function
    # and assert the correct function was called.
    cli.signup.reset_mock()
    cli.run_post_requests(mock_post_verb_cli_arguments_with_create_collection_func)
    cli.create_collection.assert_called_once()
    cli.login.assert_not_called()
    cli.logout.assert_not_called()
    cli.signup.assert_not_called()

    with pytest.raises(ValueError):
        cli.run_post_requests(mock_post_verb_cli_arguments_with_invalid_func)

@patch('recommendation_system.cli.add_game_to_collection', MagicMock(return_value=None))
def test_run_put_requests(
    mock_put_verb_cli_arguments_with_game_and_collection,
    mock_put_verb_cli_arguments_with_invalid_arguments_1,
    mock_put_verb_cli_arguments_with_invalid_arguments_2,
    mock_put_verb_cli_arguments_with_invalid_arguments_3
):
    """
    Tests the run_put_requests to call the relevant
    function depending on the function argument passed.
    """
    # execute run_put_requests with game and collection
    # and assert the correct function was called.
    cli.run_put_requests(mock_put_verb_cli_arguments_with_game_and_collection)
    cli.add_game_to_collection.assert_called_once()

    with pytest.raises(ValueError):
        cli.run_put_requests(mock_put_verb_cli_arguments_with_invalid_arguments_1)
    with pytest.raises(ValueError):
        cli.run_put_requests(mock_put_verb_cli_arguments_with_invalid_arguments_2)
    with pytest.raises(ValueError):
        cli.run_put_requests(mock_put_verb_cli_arguments_with_invalid_arguments_3)

@patch('recommendation_system.cli.remove_game_from_collection', MagicMock(return_value=None))
@patch('recommendation_system.cli.delete_collection', MagicMock(return_value=None))
def test_run_put_requests(
    mock_delete_verb_cli_arguments_with_game_and_collection,
    mock_delete_verb_cli_arguments_with_collection,
    mock_delete_verb_cli_arguments_with_invalid_arguments
):
    """
    Tests the run_delete_requests to call the relevant
    function depending on the function argument passed.
    """
    # execute run_delete_requests with game and collection
    # and assert the correct function was called.
    cli.run_delete_requests(mock_delete_verb_cli_arguments_with_game_and_collection)
    cli.remove_game_from_collection.assert_called_once()
    cli.delete_collection.assert_not_called()

    # reset the call history of the previous section.
    # now execute run_delete_requests with collection
    # and assert the correct function was called.
    cli.remove_game_from_collection.reset_mock()
    cli.run_delete_requests(mock_delete_verb_cli_arguments_with_collection)
    cli.delete_collection.assert_called_once()
    cli.remove_game_from_collection.assert_not_called()

    with pytest.raises(ValueError):
        cli.run_delete_requests(mock_delete_verb_cli_arguments_with_invalid_arguments)