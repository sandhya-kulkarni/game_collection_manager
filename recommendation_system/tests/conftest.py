import pytest

@pytest.fixture
def mock_get_verb_cli_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='GET'
    )

@pytest.fixture
def mock_get_verb_cli_arguments_with_games_object():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='GET',
        object_to_fetch='GAMES',
        game_id=None
    )

@pytest.fixture
def mock_get_verb_cli_arguments_with_collections_object():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='GET',
        object_to_fetch='COLLECTIONS'
    )

@pytest.fixture
def mock_get_verb_cli_arguments_with_invalid_object():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='GET',
        object_to_fetch='TEST'
    )

@pytest.fixture
def mock_post_verb_cli_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST'
    )

@pytest.fixture
def mock_post_verb_cli_arguments_with_login_func():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST',
        function='LOGIN',
        username='test',
        password='test'
    )

@pytest.fixture
def mock_post_verb_cli_arguments_with_logout_func():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST',
        function='LOGOUT',
    )

@pytest.fixture
def mock_post_verb_cli_arguments_with_signup_func():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST',
        function='SIGNUP',
        username='test',
        password='test',
        name='test mctest',
        date_of_birth='00/00/1979',
        favourite_game_type=None,
        favourite_game_genre=None
    )

@pytest.fixture
def mock_post_verb_cli_arguments_with_create_collection_func():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST',
        function='CREATE_COLLECTION',
    )

@pytest.fixture
def mock_post_verb_cli_arguments_with_invalid_func():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='POST',
        function='TEST',
    )

@pytest.fixture
def mock_put_verb_cli_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='PUT'
    )

@pytest.fixture
def mock_put_verb_cli_arguments_with_game_and_collection():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='PUT',
        game_id='g1_test',
        collection_id='c_1_test'
    )

@pytest.fixture
def mock_put_verb_cli_arguments_with_invalid_arguments_1():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='PUT',
        game_id='g1_test',
        collection_id=None
    )

@pytest.fixture
def mock_put_verb_cli_arguments_with_invalid_arguments_2():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='PUT',
        collection_id='c_1_test',
        game_id=None
    )

@pytest.fixture
def mock_put_verb_cli_arguments_with_invalid_arguments_3():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='PUT',
        collection_id=None,
        game_id=None
    )

@pytest.fixture
def mock_delete_verb_cli_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='DELETE'
    )

@pytest.fixture
def mock_delete_verb_cli_arguments_with_game_and_collection():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='DELETE',
        game_id='g1_test',
        collection_id='c_1_test'
    )

@pytest.fixture
def mock_delete_verb_cli_arguments_with_collection():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='DELETE',
        collection_id='c_1_test',
        game_id=None
    )

@pytest.fixture
def mock_delete_verb_cli_arguments_with_invalid_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='DELETE',
        collection_id=None,
        game_id=None
    )

@pytest.fixture
def mock_invalid_verb_cli_arguments():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Namespace(
        verb='TEST'
    )