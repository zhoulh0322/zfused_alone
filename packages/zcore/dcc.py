# coding:utf-8
# --author-- lanhua.zhou

import sys


def code():
    _exec = sys.executable
    if _exec.endswith("maya.exe"):
        return "maya"
    elif _exec.endswith("houdinifx.exe"):
        return "houdini"
    elif _exec.endswith("katanaBin.exe"):
        return "katana"
    elif "Nuke" in _exec:
        return "nuke"


class _node(object):
    def __init__(self, name, parent = None):
        if parent:
            self._parent = parent
            self._parent.add(self)
        self._childs = []

        self._name = name

    def add(self, node):
        self._childs.append(node)

    def node_type(self):
        return "node type"

    def name(self):
        return self._name

    def parent(self):
        return self._parent

    def childs(self):
        return self._childs

class Group(_node):
    def __init__(self, name, parent = None):
        super(Group, self).__init__(name, parent)

    def node_type(self):
        return "group"


class Transform(_node):
    def __init__(self, name, parent = None):
        super(Transform, self).__init__(name, parent)

    def node_type(self):
        return "transform"


class Geometry(_node):
    def __init__(self, name, parent = None):
        super(Geometry, self).__init__(name, parent)
    
    def node_type(self):
        return "geometry"