# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import logging


class StepLogger(object):
    def __init__(self, title, data):
        self._title = title
        self._data = data 

    def minimum(self):
        return self._data["minimum"]

    def maximum(self):
        return self._data["maximum"]

    def value(self):
        return self._data["value"]

    def text(self):
        return self._data["text"]

    def set_minimum(self, minimum):
        self._data["minimum"] = minimum

    def set_maximum(self, maximum):
        self._data["maximum"] = maximum

    def set_value(self, value):
        self._data["value"] = value

    def set_text(self, text):
        self._data["text"] = text

    def title(self):
        return self._title

    def data(self):
        return self._data