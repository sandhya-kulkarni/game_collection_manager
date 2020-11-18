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