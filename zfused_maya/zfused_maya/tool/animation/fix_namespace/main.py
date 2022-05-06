# coding:utf-8
# --author-- lanhua.zhou

""" shading color widget """

import os

from Qt import QtWidgets, QtCore

import maya.cmds as cmds

from zfused_maya.ui.widgets import window

from . import core

class Window(window._Window):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self._build()

        self.fix_button.clicked.connect(self._fix)
        
    def _fix(self):
        core.fix_namespace()

    def _build(self):
        self.resize(576, 330)
        self.set_title(u"修复命名空间")
        # 布局    
        _widget = QtWidgets.QFrame()
        self.set_central_widget(_widget)
        _layout = QtWidgets.QVBoxLayout(_widget)
        # 注释
        self.error_label = QtWidgets.QLabel()
        _layout.addWidget(self.error_label)
        _layout.setSpacing(2)
        _layout.setContentsMargins(2,2,2,2)
        
        self.error_label.setStyleSheet("QLabel{font: bold 14px;background-color:#DD4444;color:#EDEDED;Text-align: center;}")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setText("修复前请保存备份文件！\n修复后请另存文件！")
        

        # 操作界面
        self.operation_widget = QtWidgets.QFrame()
        _layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(4,4,4,4)
        
        # 单按钮
        self.fix_button = QtWidgets.QPushButton()
        self.operation_layout.addWidget(self.fix_button)
        self.fix_button.setFixedHeight( 40 )
        self.fix_button.setText(u"修复多层级命名空间")
        self.fix_button.setStyleSheet("QPushButton{background-color:#252526}")

