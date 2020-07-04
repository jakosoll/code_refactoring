import ast
import os
import collections
import argparse
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


def clear_magic_methods(func_list: list) -> list:
    return [f for f in flat(func_list) if not (f.startswith('__') and f.endswith('__'))]


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if is_verb(n)]


def get_all_words_in_func(func_list: list) -> list:
    return flat([split_snake_case_name_to_words(func_name) for func_name in func_list])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_top_verbs(verbs: Union[list, str], top_size: int = 10) -> list:
    return collections.Counter(verbs).most_common(top_size)


class ArgParser:
    def __init__(self):
        p = argparse.ArgumentParser()
        p.add_argument(
            "-g",
            "--github",
            help="--github allows to clone repo from github",
            type=str,
            dest="github"
        )
        p.add_argument(
            "-o",
            "--output",
            help="--output define type of output file: csv, or xls",
            type=str,
            dest="output"
        )
        args = p.parse_args()
        self.github = args.github
        self.output = args.output.lower()

        assert not self.output or self.output == 'xls' or self.output == 'csv', 'Error extensions type'


def main():
    p = ArgParser()
    if p.github:
        pass
    if p.output:
        pass
    top_verbs = []
    for project in projects:
        path = os.path.join('.', project)
        file_names = get_filenames(path)
        if not file_names:
            continue
        trees = parse_ast(file_names)
        func_list: list = get_node_name(trees)
        clear_func_list: list = clear_magic_methods(func_list)
        func_words_list: list = get_all_words_in_func(clear_func_list)
        top_verbs.extend(get_top_verbs(func_words_list))
    # print(top_verbs)
    print(f'total {len(top_verbs)} words, {len(set(top_verbs))} is unique')
    for word, occurence in sorted(get_top_verbs(top_verbs, top_size=200), key=lambda item: item[1]):
        print(word, occurence)


if __name__ == "__main__":
    main()
