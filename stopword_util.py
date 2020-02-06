from typing import List
from urllib import request

import os


def get_stopwords_from_slothlib(filepath: str):
    """
    SlothLibからストップワードを取得する.
    :param filepath キャッシュ先ファイルパス
    :return: list of step words.
    """
    stopwords = []
    try:
        with open(filepath, 'r') as file:
            stopwords = file.read().split(",")
    except FileNotFoundError:
        ja_slothlib_file = request.urlopen('http://svn.sourceforge.jp/svnroot/slothlib/CSharp/'
                                           'Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt')
        stopwords.extend(
            list(filter(lambda x: not x == u'', [line.decode('utf-8').strip() for line in ja_slothlib_file])))

        english_stopwords_file = request.urlopen("http://algs4.cs.princeton.edu/35applications/stopwords.txt")
        stopwords.extend(
            list(filter(lambda x: not x == u'',
                        [line.decode('utf-8').strip() for line in english_stopwords_file])))
        with open(filepath, 'w') as file:
            file.write(",".join(stopwords))
    return stopwords


def get_stopwords_from_csv_files(filepath_list: List[str] = None, dirpath: str = None):
    stopwords = []
    if dirpath:
        filepath_ls = list(map(lambda x: os.path.join(dirpath, x), os.listdir(dirpath)))
    else:
        filepath_ls = filepath_list
    for filepath in filepath_ls:
        with open(filepath, 'r') as file:
            stopwords.extend(file.read().split(","))
    return list(set(stopwords))
