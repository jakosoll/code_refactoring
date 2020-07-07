import ast
import os
import collections
import argparse
from typing import Union
from nltk import pos_tag
from git import Repo

projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]


class ArgParser:
    def __init__(self):
        p = argparse.ArgumentParser()
        p.add_argument(
            "-g",
            "--git",
            nargs=2,
            help="--git allows to clone git repo. Usage: '-g url path'",
            type=str,
            dest="git"
        )
        p.add_argument(
            "-o",
            "--output",
            help="--output define type of output file: 'csv', or 'json'",
            type=str,
            dest="output"
        )
        p.add_argument(
            "-w",
            "--words",
            help="Allows to choice type of searching words: noun or verb",
            choices=[
                'noun',
                'verb'
            ],
            default='verb',
            type=str,
            dest="type_words"
        )
        p.add_argument(
            "-n",
            "--names",
            help="Allows to choice type of searching objects: func or vars",
            choices=[
                "func",
                "vars"
            ],
            default="func",
            dest="type_names"
        )
        args = p.parse_args()
        self.git: list = args.git
        self.output = args.output
        self.type_words = args.type_words
        self.type_names = args.type_names

        assert not self.output or self.output == 'json' or self.output == 'csv', "Error extensions type! Use 'json' or 'csv'"
        assert not self.git or self.git[0].endswith('.git'), "Error '-g' attribute, link must ends with 'git'"

        def _check_path(path: str) -> bool:
            return os.path.exists(path)
        if self.git:
            assert not _check_path(self.git[1]), f'Error, Directory {self.git[1]} exists!'


class AstParser:
    def __init__(self, file_names):
        self.file_names = file_names
        self.trees = []

    def _parse_ast(self, file_names: list, with_filenames=False, with_file_content=False):
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

    def get_func_name(self):
        self.trees = self._parse_ast(self.file_names)
        print('functions extracted')
        return [[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in self.trees]

    def get_vars_name(self):
        self.trees = self._parse_ast(self.file_names)
        print('vars extracted')
        return [[node.attr.lower() for node in ast.walk(t) if isinstance(node, ast.Attribute)] for t in self.trees]


def get_filenames(path: str) -> list:
    """

    :param path:
    :return: list of '.py' file names:
    """
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if len(file_names) == 100:
                break
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
    if file_names:
        print('total %s files' % len(file_names))
    return file_names


def flat(_list: list) -> list:
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def clear_magic_methods(func_list: list) -> list:
    return [f for f in flat(func_list) if not (f.startswith('__') and f.endswith('__'))]


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def get_all_words_in_func(func_list: list) -> list:
    return flat([split_snake_case_name_to_words(func_name) for func_name in func_list])


def get_part_of_speech(word, type_words):
    if type_words == 'noun':
        type_words = 'NN'
    elif type_words == 'verb':
        type_words = 'VB'
    return [w for w in word if pos_tag([w])[0][1] == type_words]


def get_top_verbs(verbs: Union[list, str], top_size: int = 10) -> list:
    return collections.Counter(verbs).most_common(top_size)


def clone_repo(git_url: str, path=None):
    if not path:
        path = os.path.join('.')
    repo = Repo.clone_from(git_url, path)
    return repo


def main():
    p = ArgParser()
    top_verbs = []
    path = 'sqlalchemy'  # testing path
    path = os.path.join('.', path)
    file_names = get_filenames(path)  # получаем список файлов в директории
    a = AstParser(file_names)  # получаем список ast деревьев функций в каждом файле
    if p.type_names == 'vars':
        names_list = a.get_vars_name()
    else:
        names_list = a.get_func_name()
    # pprint.pprint(func_list)
    clear_names_list: list = clear_magic_methods(names_list)
    dirty_words_list: list = get_all_words_in_func(clear_names_list)
    # pprint.pprint(func_words_list)
    words_list = get_part_of_speech(dirty_words_list, p.type_words)
    top_verbs.extend(get_top_verbs(words_list))
    # # print(top_verbs)
    print(f'total {len(top_verbs)} words, {len(set(top_verbs))} is unique')
    for word, occurence in sorted(get_top_verbs(top_verbs, top_size=200), key=lambda item: item[1]):
        print(word, occurence)


if __name__ == "__main__":
    main()
