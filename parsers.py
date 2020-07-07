import argparse
import ast
import os

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
