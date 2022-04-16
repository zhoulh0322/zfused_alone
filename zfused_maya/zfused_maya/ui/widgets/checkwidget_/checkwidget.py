# coding:utf-8
# --author-- lanhua.zhou
import maya.cmds as cmds

from Qt import QtGui,QtWidgets,QtCore

import zfused_maya.node.core.check as check

from . import widget
from . import itemwidget


class CheckWidget(widget.Widget):
    def __init__(self, project_step_checks):
        super(CheckWidget, self).__init__()
        self._init(project_step_checks)

    @classmethod
    def Reset(cls):
        cls.value = False
    
    # def _check_all_del(self):
    #     _is_ok = True
    #     for widget in self.allCheckWidget:
    #         print(widget)
    #         if self.auto_clear():
    #             widget.clear()
    #         value = widget.check()
    #         if not value:
    #             _is_ok = False
    #             widget.setHidden(False)
    #         else:
    #             if not self.show_all():
    #                 widget.setHidden(True)
    #             else:
    #                 widget.setHidden(False)
    #         QtWidgets.QApplication.processEvents()
    #     if _is_ok:
    #         self.close()
    #     widget.Widget.value = _is_ok
    #     check.Check.value = _is_ok

    def _init(self, project_step_checks):
        self.set_title_name(u"检查")

        for _project_step_check in project_step_checks:
            _check = _project_step_check.check()
            widget = itemwidget.ItemWidget(_check.name(), _check.check_script(), _check.repair_script(), _project_step_check.is_ignore())
            self.add_widget(widget)