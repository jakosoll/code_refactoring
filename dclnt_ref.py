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
    file_names = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dirname, file))
                if len(file_names) == 100:
                    break
    if file_names:
        print('total %s files' % len(file_names))
    return file_names


def parse_ast(file_names: list, with_filenames=False, with_file_content=False):
    trees = []
    for filename in file_names:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_node_name(trees: list) -> list:
    print('functions extracted')
    return [[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees]


def flat(_list: list) -> list:
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def main():
    pass


if __name__ == "__main__":
    main()

