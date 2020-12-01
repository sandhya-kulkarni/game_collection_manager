# Recommendation System

The recommendation system has been identified by the team as one of the main differentiating features of the product and has been chosen as one worthy of prototyping before full development.

The team recognises proper structuring and processing of data as the central tenant to the success of such a system, so has decided to prioritise a command line interface (CLI) for the initial epic to maximise the team’s capacity in this regard.

That said, the ultimate goal of a web app for the product has not been forgotten and many aspects of the CLI have been designed to minimise adaption to this end. Namely:

* Data will be persisted to disk, though CSV files will be used instead of an SQL database; with individual files and initial row mimicking SQL tables and table headings respectively.
* Interaction and intent with particular functionality of the CLI will follow that of [HTTP / RESTful verbs](#HTTP-/-RESTful-Verbs).

One obvious exception is that of authentication; with the CLI assuming as though it is being run by an authorised administrator with access to all user data and the capacity to make changes on their behalf by providing a valid `--user_id`.
 
> @Behineh, if you'd like to keep login / logout then we can sell this as a user impersonation feature.

For more detailed information, please refer to the dedicated article on [the recommendation system](https://git.ecdf.ed.ac.uk/softdevonline2021/group_7/wikis/13.-Recommendation-System).

## Requirements

* Python 3.x
* [Pandas](https://pandas.pydata.org/)

## Usage

To run the recommendation system:

```console
$ python3 recommendation_system/cli.py -h
```

On first usage, the local environment needs to be initialised with seed data for users, games and reviews.

The program will automatically use sample data provided for quick demonstration and populate the directory [data_store](data_store), though should you wish to provide alternative seed data please refer to the section [Input Files](##Input Files).

To run commands, the CLI expects a HTTP / RESTful verb `-v / --verb`, an endpoint object `-o / --object` and optional inputs as arguments.

### HTTP Verbs [-v / --verb]

| Verb | Description |
| --- | --- |
| GET | Read a given object.<br /><br />Optional arguments are typically to filter the amount of information returned. |
| POST | Create a new object item.<br /><br />Optional arguments are typically to associate key value pairs. |
| PATCH | Update and modify an object item.<br /><br />Typically, this would requires at least the resource item's id by which to update along with additional optional arguments that act as key value pairs. |
| PUT | Update and replace an object item.<br /><br />Typically, this would requires at least the resource item's id by which to update along with optional arguments that serve as key value pairs.|
| DELETE | Delete an object item.<br /><br />Typically, this would require at least the resource item's id to delete. |

### Objects [-o / --object]

| Object | Description | Unique Identifier | Notable Fields |
| --- | --- | --- | --- |
| USERS | User records. | `user_id` | `username`, `password`, `date_of_birth`, `favourite_game_type`, `favourite_genre` |
| GAMES | Game records.<br /><br />When queried with a `GET` request will also return data on the item's `mean` review score.| `game_id` | `game_type`, `genre`, `keywords`, `mechanic`|
| COLLECTIONS | Associative entity for mapping user and game records. | `collection_id` | `user_id`, `game_ids` |

For assistance on optional inputs available for a given object, please pass
the help flag [-h] along with the desired option. For example:

```console
$ # Optional argument help, scoped to given scenario
$ python3 recommendation_system/cli.py -v GET -o GAMES -h
$ # Execute Command, with optional argument --sort_by
$ python3 recommendation_system/cli.py -v GET -o GAMES --sort_by "gameplay_score"
```

#### Verb Object Support Matrix

|  | USERS | GAMES | COLLECTIONS |
| --- | --- | --- | --- |
| GET |  Yes | Yes+ | YES |
| POST | Yes | No | No |
| PATCH | No | No | YES |
| PUT | No | No | No |
| DELETE | No | No | Yes |

### Optional Arguments

#### GET USERS

| option | description | default |
|---|---|---|
|`--id`|Optional id to limit the information returned to a single user object| |None|

#### POST USERS

| option | description | required |
|---|---|---|
|`--username`|username provided by the user to log in or sign up|True|
|`--password`|password provided by the user to log in or sign up.|True|
|`--name`|full name provided by the user to sign up.|True|
|`--date_of_birth`|date of birth provided by the user to sign up| True|
|`--favourite_game_type`|Optional favourite game type provided by the user at sign up.<br /><br />Possible values: ["Board Game", "Card Game", "Role Playing Game", "Miniature War Game"]| |
|`--favourite_genre`|Optional favourite game genre provided by the user at sign up.<br /><br />Possible values:["Fantasy", "Other", "Horror", "War"]| |

#### GET GAMES

| option | description | default |
|---|---|---|
|`--id`|Optional id to limit the information returned to a single game object| |None|
|`--game_type`|Optional game type value to filter the information returned.<br /><br />Choices:["Board Game", "Card Game", "Role Playing Game", "Miniature War Game"]|None|
|`--genre`|Optional genre value to filter the information returned.<br /><br />Choices:["Fantasy", "Other", "Horror", "War"]|None|
|`--keywords`|Optional keyword value to filter the information returned.|None|
|`--mechanic`|Optional mechanic value to filter the information returned.|None|
|`--sort_by`|Optional review aspect to sort the information returned.<br /><br />Choices:["complexity_score", "gameplay_score", "visual_score", "overall_score"]|"overall_score"|
|`--weighting`|Optional weighting to calculate mean average by if --sort_by is "overall_score".<br/><br/>Expects list of 4 int values.|[0, 0, 0, 1]|

##### Return Functions (-f / --functions)

| values | description |
|---|---|
| `FILTERS` |Return unique terms within a given selection of game object|

#### GET COLLECTIONS

| option | description | default |
|---|---|---|
|`--id`|Optional collection id to limit the information returned to a single collection object|None|
|`--user_id`|Optional user id to limit the information returned to a single user's collection object|None|

#### PATCH COLLECTIONS

| option | description | required |
|---|---|---|
|`--id`|Collection id to update|True|
|`--user_id`|Game id to add to the given collection object|True|

#### DELETE COLLECTIONS

| option | description | required |
|---|---|---|
|`--id`|Collection id to update|True|
|`--user_id`|Game id to remove from the given collection object|Optional|

### Examples

To return all users:

```console
$ python3 recommendation_system/cli.py -v GET -o USERS
```

To add a new user (signup):

```console
$ python3 recommendation_system/cli.py -v POST -username joe --password jb3000 --name "Joe Bloggs" --date_of_birth "26/01/1985"
```


To return all games of the game_type "Card Game", sorted by the mean review rating given as their "visual_score":

```console
$ python3 recommendation_system/cli.py -v GET -o GAMES --game_type "Card Game" --sort_by "visual_score"
```

To return all unique terms found across all games for filtering purposes:

```console
$ python3 recommendation_system/cli.py -v GET -o GAMES -f FILTERS
```

To add a game to a collection:

```console
$ python3 recommendation_system/cli.py -v PATCH --id <collection_id> --game_id <game_id>
```

To remove a game from a collection:

```console
$ python3 recommendation_system/cli.py -v PATCH --id <collection_id> --game_id <game_id>
```

> TODO - UPDATE BELOW if impersonate user is desired

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
$ python3 -m pytest
```

Alternatively, you may run a specific set of tests (for instance `example.py`) with the following:

```console
$ python3 -m pytest tests/example.py
```

---

Code consistency and standards are encouraged by the use of [pylint](https://pypi.org/project/pylint/),
which follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide as defined in [.pylintrc](.pylintrc).

To quality check the main [recommendation_system](recommendation_system) program, run pylint as a module from within the the [/recommendation_system](/recommendation_system) directory:

```console
$ cd recommendation_system
$ python3 -m pylint recommendation_system/cli.py
```

## Software Development Coursework

The recommendation system has been built as part of the Software Development coursework for session 2020/21.

The [original product spec](spec.md) and [coursework requirements](assessment.md) are maintained as part of the project's repository for convenience; though [the project wiki](https://git.ecdf.ed.ac.uk/softdevonline2021/group_7/wikis/home) should be used as the primary source for information.
