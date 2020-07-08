# code_refactoring
Code refactoring for script who scans .py files and print most popular prefixes of functions names, vars name.

## General attributes:

* `-g` take git link for clone repo on your hard drive and scan it (may be delete after scanning) 
* `-w` type of words for analise. Should take `noun` or `verb`. Default value: `verb`
* `-o` type of output. Should take `json` or `csv`. If no set this attribute, result will display on console
* `-f` indicate folder with .py files (Not working now. Script scan sub-folders)

## Simple usage:

`python py_func_checker.py -g link-to-git folder_name`

If you clone repo, script asks, should remove git files after scan or keep them on your computer:

```
Repo cloned
Delete repo after scan files? [Y|N]:
```
When you save results with json, file create in current folder