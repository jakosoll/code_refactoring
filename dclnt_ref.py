import ast
import os
import collections
from typing import Union

from nltk import pos_tag

projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]


def get_filenames(path: str) -> list:
    pass


def parse_ast(file_names: list, with_filenames=False, with_file_content=False):
    pass


def get_node_name(trees):
    pass


def flat(_list: list) -> list:
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def main():
    pass


if __name__ == "__main__":
    main()

