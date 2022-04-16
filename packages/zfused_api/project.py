# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function, unicode_literals

import os
import ast
import json
import logging
import datetime

logger = logging.getLogger(__name__)


LOCAL_DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "database"))



def projects():
    _projects = []
    if os.path.isdir(LOCAL_DATABASE_PATH):
        _files = os.listdir(LOCAL_DATABASE_PATH)
        if _files:
            for _file in _files:
                _name, _format = os.path.splitext(_file)
                if _format == ".project":
                    _projects.append(_name)
    return _projects


class Project(object):
    def __init__(self, name):
        self._file = os.path.join(LOCAL_DATABASE_PATH, "{}.project".format(name))
        # local database
        with open(self._file, "r") as handle:
            self._data = json.loads(handle.read())

    def name(self):
        return self._data.get("name")
    
    def code(self):
        return self._data.get("code")

    def project_steps(self):
        return self._data.get("project_step")

    def assets(self):
        return self._data.get("asset")



if __name__ == "__main__":
    print(projects())