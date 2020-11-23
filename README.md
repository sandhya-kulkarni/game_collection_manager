# Recommendation System

The recommendation system has been identified by the team as one of the main differentiating features of the product and has been chosen as one worthy of prototyping before full development.

The team recognises proper structuring and processing of data as the central tenant to the success of such a system, so has decided to prioritise a command line interface (CLI) for the initial epic to maximise the team’s capacity in this regard.

That said, the ultimate goal of a web app for the product has not been forgotten and many aspects of the CLI have been designed to minimise adaption to this end. Namely:

* Data will be persisted to disk, though CSV files will be used instead of an SQL database, with individual files and column headings mimicking SQL tables and table headings respectively.
* Interaction and intent with particular functionality of the CLI will follow that of REST verbs: GET, POST, PUT, and DELETE

For more detailed information, please refer to the dedicated article on [the recommendation system](https://git.ecdf.ed.ac.uk/softdevonline2021/group_7/wikis/13.-Recommendation-System).

## Requirements

* Python 3.x

## Usage

To run the recommendation system:

```console
$ python recommendation_system/cli.py -h
```

On first usage, the local environment needs to be initialised with seed data for users, games and reviews.

The program will automatically use sample data provided for quick demonstration and populate the directory [data_store](data_store), though should you wish to provide alternative seed data please refer to the section [Input Files](##Input Files).

To run commands, the CLI accepts rest verbs via the -v (--verb) argument:

```console
$ python recommendation_system/cli.py -v <GET | PUT | POST | DELETE>
```
you can see all functionalities currently available per each rest verb below:

### GET calls
Get calls fetch specific information from the datastore. The object to be fetched needs to be defined via the -o (--object_to_fetch) argument.

Currently the available objects to GET are: games and collections.

#### Game(s)
To fetch all games available in the game datastore run the command below:

This will print out the game datastore to the console. 

You don't need to be logged in to run this command and see all games.

```console
$ python recommendation_system/cli.py -v GET -o GAMES
```

To fetch the info about a specific game you need to pass in the game_id via the -g (--game_id) argument as well, using the below command:

This will print out the specific game's information to the console.

If the game does not exist in the game datastore and error will be printed out to console.

You don't need to be logged in to run this command and see all games.

```console
$ python recommendation_system/cli.py -v GET -o GAMES -g <game_id>
```

#### Collections
To fetch all collections for the logged in user run the command below:

This will print out the logged in user's collections to the console if there are any collections.

You  need to be logged in to see your collections.

If you're not logged in the command will ask you to log in.

```console
$ python recommendation_system/cli.py -v GET -o COLLECTIONS
```

### POST calls
Post calls write/create specific information to the datastore. The function to be acted on needs to be defined via the -f (--function) argument.

Currently the available functions to POST are: login, logout, signup and create_collection.

#### Login
To log in you need to pass in the username and password via -u (--username), -p (--password) arguments as well, using the below command:

This will log you into the account, and save the logged in user inside the auth_cookies file.

If log in is successful a success message is printed out, otherwise if username and/or password is incorrect, an error message is printed. 

```console
$ python recommendation_system/cli.py -v POST -f LOGIN -u <username> -p <password>
```

#### Logout
To log out simply use the logout command as below:

This will remove the saved logged in user from the auth_cookies file.

```console
$ python recommendation_system/cli.py -v POST -f LOGOUT
```

#### Signup
To sign up a new account you need to pass in the following information via it's associated argument:

* chosen username via -u (--username), required
* chosen password via -p (--password), required
* your full name via -n (--name), required. Please not this should be inside quotation if the name contains empty spaces.
* your date of birth via -d (--date_of_birth), required. In the format of DD/MM/YYYY
* your favourite game type via -fgt (--favourite_game_type), optional. This has to be one of the following game types: Board Game, Card Game, Role Playing Game, Miniature War Game. Please not this should be inside quotation as game type contains empty spaces.
* your favourite game genre via -fgg (--favourite_game_type), optional

The username needs to be unique, so if the username already exist the CLI will notify you via printing a message and asking you to choose a new username.

If sign up is successful a success message will be orinted out with the newly created user_id. Additionally you will be automatically logged in, so no need to log in separately.

example command:

```console
$ python recommendation_system/cli.py -v POST -f SIGNUP -u <username> -p <password> -n '<full_name>' -d <DD/MM/YYYY> [-fgt '<one_of_the_4_game_types>'] [-fgg <favourite_game_genre>]
```

#### Create_collections
To create a collection you need to be logged in as you can only create a collection for yourself. There are no extra arguments needed.

If you are not logged in a message will be printed out asking you to log in. 

If you are logged in the command will create an empty collection for the user and print out a success message including the newly created collection_id

```console
$ python recommendation_system/cli.py -v POST -f CREATE_COLLECTION
```
### PUT calls
PUT calls update specific information to the datastore.

Currently the only PUT call available is to add a new game to an existing collection.

#### Add a game to a collection
To add a game to a collection you need to pass in the game ID via -g (--game_id) argument and the collection ID via the -c (--collection_id) argument.

Please note that you need to be logged in to be able to add games to your collections and that you can only add games to collections you own. You can not add games to other user's collections.
If you try to add a game to a collection you don't own a permission error will be raised.

If the game already exists in a collection, a message will be printed to inform you. 

If the game is successfully added to the given collection a success message will be printed out.

```console
$ python recommendation_system/cli.py -v PUT -g <game_id> -c <collection_id>
```

### DELETE calls
DELETE calls delete specific information from the datastore. you can whether delete a whole collection of yours, or delete a game from a collection you own.

#### Remove a game from a collection
To remove a game from a collection you need to pass in the game ID via -g (--game_id) argument and the collection ID via the -c (--collection_id) argument.

Please note that you need to be logged in to be able to remove games from your collections and that you can only remove games from collections you own. You can not remove games from other user's collections.
If you try to remove a game from a collection you don't own a permission error will be raised.

If the game does not exists in a collection, a message will be printed to inform you. 

If the game is successfully removed from the given collection a success message will be printed out.

```console
$ python recommendation_system/cli.py -v DELETE -g <game_id> -c <collection_id>
```

#### Delete a collection
To delete a collection you need to pass in the collection ID via the -c (--collection_id) argument.

Please note that you need to be logged in to be able to delete a collection and that you can only delete collections you own. You can not delete another user's collections.

If the collection is successfully deleted a success message will be printed out.

```console
$ python recommendation_system/cli.py -v DELETE -c <collection_id>
```

### DICE

The recommendation system may be run on [The University of Edinburgh's Distributed Informatics Computing Environment](http://computing.help.inf.ed.ac.uk/).

Python 3 is available on DICE by default, though requires all commands to use `python3` instead of `python`.

```console
$ python3 recommendation_system
```

## Input Files

## Usability Testing

## Local Development

Development tests are located in the [/tests](/recommendation_system/tests) package and require [pytest](https://docs.pytest.org/en/stable/).

For convenience, all development dependencies may be installed with the following:

```console
$ pip install -r requirements.txt
```

To run all tests, start pytest as a module from within the [/recommendation_system](/recommendation_system) directory:

```console
$ cd recommendation_system
$ python -m pytest
```

Alternatively, you may run a specific set of tests (for instance `example.py`) with the following:

```console
$ python -m pytest tests/example.py
```

---

Code consistency and standards are encouraged by the use of [pylint](https://pypi.org/project/pylint/),
which follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide as defined in [.pylintrc](.pylintrc).

To quality check the main [recommendation_system](recommendation_system) program, run pylint as a module from within the the [/recommendation_system](/recommendation_system) directory:

```console
$ cd recommendation_system
$ python -m pylint recommendation_system/cli.py
```

## Software Development Coursework

The recommendation system has been built as part of the Software Development coursework for session 2020/21.

The [original product spec](spec.md) and [coursework requirements](assessment.md) are maintained as part of the project's repository for convenience; though [the project wiki](https://git.ecdf.ed.ac.uk/softdevonline2021/group_7/wikis/home) should be used as the primary source for information.
