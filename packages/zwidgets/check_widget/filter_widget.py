# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import os
import logging

from Qt import QtWidgets, QtGui, QtCore

import zfused_api

from zcore import language,resource

__all__ = ["FilterWidget"]


logger = logging.getLogger(__name__)


class FilterWidget(QtWidgets.QFrame):
    step_changed = QtCore.Signal(int)
    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent)
        self._build()

        self._step_name_id_dict = {}
        self._step_checkboxs = []

    def _task_step_id(self):
        for _checkbox in self._step_checkboxs:
            if _checkbox.isChecked():
                self.step_changed.emit(self._step_name_id_dict[_checkbox.text()])

    def load_project_id(self, project_id):
        """ 加载项目资产类型和任务步骤
        :rtype: None
        """
        # clear asset type item
        self._clear()

        # get current project id
        _project_id = project_id
        if not _project_id:
            return
        _project_handle = zfused_api.project.Project(_project_id)
                
        _project_step_id = 0
        
        # asset task step
        _step_ids = _project_handle.task_step_ids("asset")
        if _step_ids:
            for _step_id in _step_ids:
                _step_handle = zfused_api.step.ProjectStep(_step_id)
                _name = _step_handle.name_code()
                self._step_name_id_dict[_name] = _step_id
                _name_checkbox = QtWidgets.QCheckBox()
                _name_checkbox.setText(_name)
                self.asset_step_checkbox_layout.addWidget(_name_checkbox)
                self.step_group.addButton(_name_checkbox)
                self._step_checkboxs.append(_name_checkbox)
                _name_checkbox.stateChanged.connect(self._task_step_id)
                if _step_id == _project_step_id:
                    _name_checkbox.setChecked(True)
                    self.step_changed.emit(_step_id)

        # assembly task step
        _step_ids = _project_handle.task_step_ids("assembly")
        if _step_ids:
            for _step_id in _step_ids:
                _step_handle = zfused_api.step.ProjectStep(_step_id)
                _name = _step_handle.name_code()
                self._step_name_id_dict[_name] = _step_id
                _name_checkbox = QtWidgets.QCheckBox()
                _name_checkbox.setText(_name)
                self.assembly_step_checkbox_layout.addWidget(_name_checkbox)
                self.step_group.addButton(_name_checkbox)
                self._step_checkboxs.append(_name_checkbox)
                _name_checkbox.stateChanged.connect(self._task_step_id)
                if _step_id == _project_step_id:
                    _name_checkbox.setChecked(True)
                    self.step_changed.emit(_step_id)

        _step_ids = _project_handle.task_step_ids("sequence")
        if _step_ids:
            for _step_id in _step_ids:
                _step_handle = zfused_api.step.ProjectStep(_step_id)
                _name = _step_handle.name_code()
                self._step_name_id_dict[_name] = _step_id
                _name_checkbox = QtWidgets.QCheckBox()
                _name_checkbox.setText(_name)
                self.sequence_step_checkbox_layout.addWidget(_name_checkbox)
                self.step_group.addButton(_name_checkbox)
                self._step_checkboxs.append(_name_checkbox)
                _name_checkbox.stateChanged.connect(self._task_step_id)
                if _step_id == _project_step_id:
                    _name_checkbox.setChecked(True)
                    self.step_changed.emit(_step_id)

        _step_ids = _project_handle.task_step_ids("shot")
        if _step_ids:
            for _step_id in _step_ids:
                _step_handle = zfused_api.step.ProjectStep(_step_id)
                _name = _step_handle.name_code()
                self._step_name_id_dict[_name] = _step_id
                _name_checkbox = QtWidgets.QCheckBox()
                _name_checkbox.setText(_name)
                self.shot_step_checkbox_layout.addWidget(_name_checkbox)
                self.step_group.addButton(_name_checkbox)
                self._step_checkboxs.append(_name_checkbox)
                _name_checkbox.stateChanged.connect(self._task_step_id)
                if _step_id == _project_step_id:
                    _name_checkbox.setChecked(True)
                    self.step_changed.emit(_step_id)

    def _asset_type_ids(self):
        _type_ids = []
        for _checkbox in self._type_checkboxs:
            if _checkbox.isChecked():
                _type_ids.append(self._type_name_id_dict[_checkbox.text()])
        self.asset_type_changed.emit(_type_ids)

    def _clear(self):
        """清除资产类型和任务步骤
        :rtype: None
        """
        # 清除资产类型
        self._type_name_id_dict = {}
        self._type_checkboxs = []
        # _childrens = self.filter_type_widget.findChildren(QtWidgets.QCheckBox)
        # if not _childrens:
        #     return
        # for _child in _childrens:
        #     self.filter_project_step_checkbox_layout.removeWidget(_child)
        #     _child.deleteLater()

        # 清除任务步骤
        self._step_name_id_dict = {}
        self._step_checkboxs = []


    def _build(self):
        self.setMaximumWidth(240)
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0,0,0,0)

        # # asset task step
        # self.step_widget = QtWidgets.QFrame()
        # _layout.addWidget(self.step_widget)
        # self.step_layout = QtWidgets.QVBoxLayout(self.step_widget)
        # self.step_layout.setSpacing(0)
        # self.step_layout.setContentsMargins(0,0,0,0)

        # self.tab_widget = QtWidgets.QTabWidget()
        # self.step_layout.addWidget(self.tab_widget)
        # self.tab_widget.setStyleSheet("QTabBar::tab{height:24px;}")

        # asset frame
        self.asset_widget = QtWidgets.QFrame()
        # self.tab_widget.addTab(self.asset_widget, u"资产")
        _layout.addWidget(self.asset_widget)
        self.asset_layout = QtWidgets.QVBoxLayout(self.asset_widget)
        self.asset_layout.setSpacing(0)
        self.asset_layout.setContentsMargins(0,0,0,0)
        self.asset_step_name_button = QtWidgets.QPushButton()
        self.asset_step_name_button.setObjectName("title_button")
        self.asset_step_name_button.setMaximumHeight(25)
        self.asset_step_name_button.setText(language.word("asset"))
        self.asset_step_name_button.setIcon(QtGui.QIcon(resource.get("icons","asset.png")))
        self.asset_layout.addWidget(self.asset_step_name_button)
        self.asset_step_checkbox_widget = QtWidgets.QFrame()
        self.asset_step_checkbox_layout = QtWidgets.QVBoxLayout(self.asset_step_checkbox_widget)
        self.asset_step_checkbox_layout.setContentsMargins(20,0,0,0)
        self.asset_layout.addWidget(self.asset_step_checkbox_widget)
        self.asset_layout.addStretch(True)
        
        # assembly
        self.assembly_widget = QtWidgets.QFrame()
        # self.tab_widget.addTab(self.assembly_widget, u"场景")
        _layout.addWidget(self.assembly_widget)
        self.assembly_layout = QtWidgets.QVBoxLayout(self.assembly_widget)
        self.assembly_layout.setSpacing(0)
        self.assembly_layout.setContentsMargins(0,0,0,0)
        self.assembly_step_name_button = QtWidgets.QPushButton()
        self.assembly_step_name_button.setObjectName("title_button")
        self.assembly_step_name_button.setMaximumHeight(25)
        self.assembly_step_name_button.setText(language.word("assembly"))
        self.assembly_step_name_button.setIcon(QtGui.QIcon(resource.get("icons","assembly.png")))
        self.assembly_layout.addWidget(self.assembly_step_name_button)
        self.assembly_step_checkbox_widget = QtWidgets.QFrame()
        self.assembly_step_checkbox_layout = QtWidgets.QVBoxLayout(self.assembly_step_checkbox_widget)
        self.assembly_step_checkbox_layout.setContentsMargins(20,0,0,0)
        self.assembly_layout.addWidget(self.assembly_step_checkbox_widget)
        self.assembly_layout.addStretch(True)

        # sequence
        self.sequence_widget = QtWidgets.QFrame()
        # self.tab_widget.addTab(self.sequence_widget, u"场次")
        _layout.addWidget(self.sequence_widget)
        self.sequence_layout = QtWidgets.QVBoxLayout(self.sequence_widget)
        self.sequence_layout.setSpacing(0)
        self.sequence_layout.setContentsMargins(0,0,0,0)
        self.sequence_step_name_button = QtWidgets.QPushButton()
        self.sequence_step_name_button.setObjectName("title_button")
        self.sequence_step_name_button.setMaximumHeight(25)
        self.sequence_step_name_button.setText(language.word("sequence"))
        self.sequence_step_name_button.setIcon(QtGui.QIcon(resource.get("icons","sequence.png")))
        self.sequence_layout.addWidget(self.sequence_step_name_button)
        self.sequence_step_checkbox_widget = QtWidgets.QFrame()
        self.sequence_step_checkbox_layout = QtWidgets.QVBoxLayout(self.sequence_step_checkbox_widget)
        self.sequence_step_checkbox_layout.setContentsMargins(20,0,0,0)
        self.sequence_layout.addWidget(self.sequence_step_checkbox_widget)
        self.sequence_layout.addStretch(True)

        # shot
        self.shot_widget = QtWidgets.QFrame()
        # self.tab_widget.addTab(self.shot_widget, u"镜头")
        _layout.addWidget(self.shot_widget)
        self.shot_layout = QtWidgets.QVBoxLayout(self.shot_widget)
        self.shot_layout.setSpacing(0)
        self.shot_layout.setContentsMargins(0,0,0,0)
        self.shot_step_name_button = QtWidgets.QPushButton()
        self.shot_step_name_button.setObjectName("title_button")
        self.shot_step_name_button.setMaximumHeight(25)
        self.shot_step_name_button.setText(language.word("shot"))
        self.shot_step_name_button.setIcon(QtGui.QIcon(resource.get("icons","shot.png")))
        self.shot_layout.addWidget(self.shot_step_name_button)
        self.shot_step_checkbox_widget = QtWidgets.QFrame()
        self.shot_step_checkbox_layout = QtWidgets.QVBoxLayout(self.shot_step_checkbox_widget)
        self.shot_step_checkbox_layout.setContentsMargins(20,0,0,0)
        self.shot_layout.addWidget(self.shot_step_checkbox_widget)
        self.shot_layout.addStretch(True)

        # # step checkbox widget
        # self.step_checkbox_widget = QtWidgets.QFrame()
        # self.step_checkbox_layout = QtWidgets.QVBoxLayout(self.step_checkbox_widget)
        # self.step_checkbox_layout.setContentsMargins(20,0,0,0)
        self.step_group = QtWidgets.QButtonGroup(self)
        # self.step_layout.addWidget(self.step_checkbox_widget)
        _layout.addStretch(True)