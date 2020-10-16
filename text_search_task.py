import logging
import os


class TextSearchTask:

    def __init__(self, filepath, text_to_search):
        self._filepath = filepath
        self._text_to_search = text_to_search
        self._occurences = 0

    def occurences(self):
        return self._occurences

    def text_to_search(self):
        return self._text_to_search

    def filepath(self):
        return self._filepath

    def search(self):
        """Search text inside file. Opens file with read only mode and utf-8 encoding.
           After that make all searching text and document text lower
           to avoid mismatch in letter size"""

        with open(self._filepath, mode='rt', encoding='utf-8') as f:
            document_text = ' '.join(f.readlines()).lower()
            self._text_to_search = self._text_to_search.lower()
            self._occurences = document_text.count(self._text_to_search)
