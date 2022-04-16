# -*- coding: UTF-8 -*-
'''
@Time    : 2021/12/23 20:51
@Author  : Jerris_Cheng
@File    : check_widget.py
'''
from __future__ import print_function

from Qt import QtWidgets, QtGui, QtCore

import zfused_api


from . import filter_widget

from . import item_widget




class CheckWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(CheckWidget, self).__init__(parent)
        self._build()

        self._project_id = 0
        self._check_widgets = []

        self.filter_widget.step_changed.connect(self._step_changed)
        self.recheck_button.clicked.connect(self._check)
        self.show_all_checkbox.stateChanged.connect(self._check)


    def load_project_id(self, project_id):
        self._project_id = project_id

        self.filter_widget.load_project_id(project_id)

    def _step_changed(self, step_id):
        self._clear()
        # get project step check list
        _project_step = zfused_api.step.ProjectStep(step_id)
        _project_step_checks = _project_step.checks()
        if _project_step_checks:
            for _project_step_check in _project_step_checks:
                _check = _project_step_check.check()
                widget = item_widget.ItemWidget(_check.name(), _check.check_script(), _check.repair_script(), _project_step_check.is_ignore())
                self._add_check_widget(widget)
        else:
            pass
        pass

    def _check(self):
        if not self._check_widgets:
            return 
        for _widget in self._check_widgets:
            value = _widget.check()
            if not value:
                _is_ok = False
                _widget.setHidden(False)
            else:
                if not self.show_all_checkbox.isChecked():
                    _widget.setHidden(True)
                else:
                    _widget.setHidden(False)
            QtWidgets.QApplication.processEvents()

    def _clear(self):
        self._check_widgets = []
        for i in reversed(range(self.check_listlayout.count())): 
            self.check_listlayout.itemAt(i).widget().setParent(None)

    def _add_check_widget(self, widget):
        self._check_widgets.append(widget)
        self.check_listlayout.addWidget(widget)

    def _show_all_check(self, state):
        if not self._check_widgets:
            return 
        for _widget in self._check_widgets:
            _widget

    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(2)
        _layout.setContentsMargins(2, 2, 2, 2)

        # # current project widget
        # self.project_frame = QtWidgets.QFrame()
        # _layout.addWidget(self.project_frame)
        # self.project_layout = QtWidgets.QHBoxLayout(self.project_frame)
        # self.project_label = QtWidgets.QLabel()
        # self.project_label.setText(u'当前项目名：')
        # self.project_layout.addWidget(self.project_label)

        # contant widget
        self.contant_widget = QtWidgets.QFrame()
        _layout.addWidget(self.contant_widget)
        self.contant_layout = QtWidgets.QHBoxLayout(self.contant_widget)
        self.contant_layout.setSpacing(2)
        self.contant_layout.setContentsMargins(2,2,2,2)

        self.filter_widget = filter_widget.FilterWidget()
        self.contant_layout.addWidget(self.filter_widget)

        # scroll widget
        self.scroll_widget = QtWidgets.QScrollArea()
        self.contant_layout.addWidget(self.scroll_widget)
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scroll_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.check_widget = QtWidgets.QFrame()
        self.scroll_widget.setWidget(self.check_widget)
        self.check_layout = QtWidgets.QVBoxLayout(self.check_widget)
        self.check_layout.setSpacing(0)
        self.check_layout.setContentsMargins(0,0,0,0)
         
        # self.check_infolayout = QtWidgets.QHBoxLayout()
        # self.check_infolayout.setContentsMargins(2,2,2,2)
        # self.check_layout.addLayout(self.check_infolayout)
        # self.check_label = QtWidgets.QLabel()
        # self.check_infolayout.addWidget(self.check_label) 
         
        self.check_listlayout = QtWidgets.QVBoxLayout()
        self.check_listlayout.setContentsMargins(2,2,2,2)
        self.check_layout.addLayout(self.check_listlayout)
        self.check_layout.addStretch(True)

        # operation widget
        self.operation_widget = QtWidgets.QWidget()
        _layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(0,0,0,0)
        # show all item widget
        self.show_all_checkbox = QtWidgets.QCheckBox()
        self.show_all_checkbox.setText(u"显示所有检查面板")
        self.show_all_checkbox.setChecked(True)
        self.operation_layout.addWidget(self.show_all_checkbox)
        self.operation_layout.addStretch(True)
        # recheck button
        self.recheck_button = QtWidgets.QPushButton()
        self.recheck_button.setMinimumSize(100,30)
        self.operation_layout.addWidget(self.recheck_button)
        self.recheck_button.setText(u"检查")
