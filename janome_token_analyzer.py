from typing import List

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import re


class URLReplacer(RegexReplaceCharFilter):
    """
    URLを特定の文字列で置き換えるCharFilter
    """

    def __init__(self, replace_str: str):
        super().__init__(u'https?://[\w/:%#\$&amp;\?\(\)~\.=\+\-]+', replace_str)


class SymbolAndDigitsReplacer(RegexReplaceCharFilter):
    """
    記号・数字を特定の文字列で置き換えるCharFilter
    """

    def __init__(self, replace_str: str):
        super().__init__(u'[0-9\?!-/:-@¥[-`{-~]', replace_str)


class MinMaxLengthTokenFilter(TokenFilter):
    """
    文字数でフィルタリングするTokenFilter
    """

    def __init__(self, min_len: int, max_len: int):
        self._min_len, self._max_len = min_len, max_len

    def apply(self, tokens):
        for token in tokens:
            if len(token.base_form) < self._min_len or len(token.base_form) > self._max_len:
                continue
            yield token


class StopwordTokenFilter(TokenFilter):
    """
    ストップワードを除去するTokenFilter
    """

    def __init__(self, stopwords: List[str]):
        self._stopwords = stopwords

    def apply(self, tokens):
        for token in tokens:
            if token.base_form in self._stopwords:
                continue
            yield token


class RegexTokenFilter(TokenFilter):
    """
    正規表現でフィルタリングするTokenFilter
    """

    def __init__(self, regex: str):
        self._regex = regex

    def apply(self, tokens):
        for token in tokens:
            if re.match(self._regex, token.base_form):
                continue
            yield token


class JanomeTokenAnalyzerGenerator:
    def __init__(self, additional_char_filters: List[CharFilter] = [], additional_token_filters: List[TokenFilter] = []
                 , user_dict_filepath: str = None, stopwords: List[str] = None):
        """
        :param additional_char_filters:
        :param additional_token_filters:
        :param user_dict_filepath:
        :param stopwords:
        """
        self.char_filters, self.token_filters = additional_char_filters, additional_token_filters
        self._user_dict_filepath = user_dict_filepath
        if stopwords:
            self.token_filters.append(StopwordTokenFilter(stopwords))

    def generate_analyzer(self) -> Analyzer:
        if self._user_dict_filepath:
            tokenizer = Tokenizer(self._user_dict_filepath, udic_type="simpledic", udic_enc="utf8")
        else:
            tokenizer = Tokenizer()
        return Analyzer(char_filters=self.char_filters, tokenizer=tokenizer, token_filters=self.token_filters)


class StrictAnalyzerGenerator(JanomeTokenAnalyzerGenerator):
    """
    デフォルトでCharFilter, TpokenFilterが設定されているAnalyzerGenerator
    """

    def __init__(self, additional_char_filters: List[CharFilter] = [], additional_token_filters: List[TokenFilter] = [],
                 user_dict_filepath: str = None, stopwords: List[str] = None):
        super().__init__(additional_char_filters, additional_token_filters, user_dict_filepath, stopwords)
        self.char_filters += [UnicodeNormalizeCharFilter(), SymbolAndDigitsReplacer("、")]
        self.token_filters += [POSStopFilter(['記号', '接続詞', '副詞', '連体詞', "助詞", "助動詞", "感動詞"]),
                               LowerCaseFilter(), MinMaxLengthTokenFilter(2, 20), CompoundNounFilter()]
        self._user_dict_filepath = user_dict_filepath
