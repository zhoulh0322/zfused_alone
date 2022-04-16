# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from Qt import QtWidgets, QtGui, QtCore

import zfused_api

from zwidgets.check_widget import check_widget

import zfused_maya.core.record as record

from zfused_maya.ui.widgets import window

__all__ = ["ChekManageWidget"]

logger = logging.getLogger(__name__)


class CheckManageWidget(window._Window):
    def __init__(self, parent = None):
        super(CheckManageWidget, self).__init__()
        self._build()


    def showEvent(self, event):
        # _project_code = record.current_project_code()
        # self.check_widget.load_project(_project_code)
        super(CheckManageWidget, self).showEvent(event)


    def _build(self):
        self.resize(900, 900)
        self.set_title_name(u"项目检查")

        self.check_widget = check_widget.CheckWidget()
        self.set_central_widget(self.check_widget)