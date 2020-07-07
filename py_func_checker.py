import os
import collections
from typing import Union
from nltk import pos_tag
from git import Repo
from parsers import ArgParser
from parsers import AstParser


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
    # if p.git:
    #     clone_repo(*p.git)
    path = 'sqlalchemy'  # testing path
    path = os.path.join('.', path)
    file_names = get_filenames(path)  # получаем список файлов в директории
    a = AstParser(file_names)  # получаем список ast деревьев функций в каждом файле
    if p.type_names == 'vars':
        names_list = a.get_vars_name()
    else:
        names_list = a.get_func_name()
    clear_names_list: list = clear_magic_methods(names_list)
    dirty_words_list: list = get_all_words_in_func(clear_names_list)
    words_list = get_part_of_speech(dirty_words_list, p.type_words)
    top_verbs.extend(get_top_verbs(words_list))
    print(f'total {len(top_verbs)} words, {len(set(top_verbs))} is unique')
    for word, occurence in sorted(get_top_verbs(top_verbs, top_size=200), key=lambda item: item[1]):
        print(word, occurence)


if __name__ == "__main__":
    main()
