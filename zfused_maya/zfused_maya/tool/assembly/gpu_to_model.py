# coding:utf-8
# --author-- lanhua.zhou


from __future__ import print_function

from Qt import QtWidgets, QtCore

import maya.cmds as cmds

from zfused_maya.node.core import assembly

from zfused_maya.ui.widgets import window



class Window(window._Window):
    def __init__(self):
        super(Window, self).__init__()
        
        self._build()

        self.sel_button.clicked.connect(self._to_sel)
        self.all_button.clicked.connect(self._to_all)

    def _to_sel(self):
        _is_hide = self.hide_checkbox.isChecked()
        assembly.gpu_to_model(True, _is_hide)

    def _to_all(self):
        _is_hide = self.hide_checkbox.isChecked()
        assembly.gpu_to_model(False, _is_hide)

    def _build(self):
        self.resize(500,200)
        self.set_title_name(u"gpu to model")

        self.main_widget = QtWidgets.QFrame()
        self.set_central_widget(self.main_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(2,2,2,2)

        # 注释
        self.error_label = QtWidgets.QLabel()
        self.main_layout.addWidget(self.error_label)
        self.error_label.setStyleSheet("QLabel{font: bold 14px;background-color:#DD4444;color:#EDEDED;Text-align: center;}")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setText(u"转换gpu为reference模型instance")
        
        self.hide_checkbox = QtWidgets.QCheckBox(u"隐藏GPU")
        self.main_layout.addWidget(self.hide_checkbox)
        self.hide_checkbox.setChecked(True)

        self.operation_widget = QtWidgets.QFrame()
        self.main_layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.sel_button = QtWidgets.QPushButton(u"选择转换")
        self.operation_layout.addWidget(self.sel_button)
        self.sel_button.setFixedHeight(40)
        self.all_button = QtWidgets.QPushButton(u"全部转换")
        self.operation_layout.addWidget(self.all_button)
        self.all_button.setFixedHeight(40)





if __name__ == "__main__":
    ui = Window()
    ui.show()
