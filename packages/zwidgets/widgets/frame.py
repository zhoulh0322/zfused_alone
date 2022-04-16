# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

from Qt import QtWidgets, QtGui, QtCore


class Frame(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(Frame, self).__init__(parent)
        self._base_build()

    def _base_build(self):
        _qss = "{}/window.qss".format(os.path.dirname(__file__))
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)
