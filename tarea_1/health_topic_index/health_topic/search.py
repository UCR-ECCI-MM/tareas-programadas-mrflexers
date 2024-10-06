from enum import Enum

import numpy as np

from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from pandas import DataFrame, Series

THRESHOLD = 3.3


class Language(Enum):
    ENGLISH = 'eng'
    SPANISH = 'spa'


class SearchEngine:

    @staticmethod
    def _expand_with_synonyms(tokenized_query: str, languages: list):
        expanded_query = set(tokenized_query)

        for token in tokenized_query:
            for language in languages:
                for syn in wn.synsets(token, lang=language)[:3]:    # Limit to top 3 synonyms per word
                    for language in languages:
                        for lemma in syn.lemmas(language):
                            expanded_query.add(lemma.name().replace("_", " "))

        return list(expanded_query)

    def __init__(self, documents: DataFrame):
        tokenized_docs = [word_tokenize(doc.lower()) for doc in documents['text']]

        self._documents = documents
        self._bm25 = BM25Okapi(tokenized_docs)

    def search(self, query: str) -> Series:
        tokenized_query = word_tokenize(query.lower())

        languages = [lang.value for lang in Language]
        expanded_query = self._expand_with_synonyms(tokenized_query, languages)

        scores = self._bm25.get_scores(expanded_query)

        sorted_indices = np.argsort(scores)[::-1]

        filtered_sorted_indices = [i for i in sorted_indices if scores[i] >= THRESHOLD]

        result_ids = self._documents.iloc[filtered_sorted_indices]['id']

        return result_ids
