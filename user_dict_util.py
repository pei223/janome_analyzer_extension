from typing import List

import os


def assemble_user_dicts(dest_filepath: str, filepath_list: List[str] = None, dirpath: str = None):
    """
    ユーザー辞書を一つに束ねる
    :param dest_filepath:
    :param filepath_list:
    :param dirpath:
    """
    dict_rows = []
    if filepath_list:
        for filepath in filepath_list:
            dict_rows.extend(_get_user_dict_rows(filepath))
    elif dirpath:
        for filename in os.listdir(dirpath):
            dict_rows.extend(_get_user_dict_rows(dirpath + "/" + filename))
    dict_rows = list(set(dict_rows))
    with open(dest_filepath, "w") as file:
        file.write("\n".join(sorted(dict_rows, key=lambda x: -len(x.split(",")[0]))))  # 短い単語順にソート


def _get_user_dict_rows(filepath: str):
    with open(filepath, "r") as file:
        return file.read().split("\n")
