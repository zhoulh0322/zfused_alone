# -*- coding: UTF-8 -*-
'''
@Time    : 2021/9/16 11:27
@Author  : Jerris_Cheng
@File    : playblast_maya.py
'''
from __future__ import print_function

import json
import os
import subprocess
import locale 
import datetime
import shutil

from Qt import QtWidgets,QtCore,QtGui
global font_scale

class Hud_Frame(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(Hud_Frame, self).__init__(parent)

        self._image = ""

        self._config = {}

    def init(self, init_config):
        self._config = init_config

    def set_image(self, image):
        self._image = QtGui.QImage(image)
        self.update()

    def paintEvent(self, event):
        _rect = self.rect()
        painter = QtGui.QPainter()
        painter.begin(self)
        
        # image
        if self._image:
            painter.drawImage(_rect, self._image)

        _font = QtGui.QFont(self._config.get("font-family"))
        _font.setBold(self._config.get("bold"))
        _font.setPixelSize(self._config.get("font-size")*font_scale)
        painter.setFont(_font)
        
        _margin = self._config.get("margin")
        _text_height = self._config.get("text-height")*font_scale
        for _hud in self._config.get("hud"):
            _horizontally, _vertically, _level = _hud.get("text-align")
            if _vertically == -1:
                _hud_rect = QtCore.QRect( _rect.x() + _margin[0],
                                          _rect.y() + _rect.height() - (_margin[3] + _text_height * _level) - _text_height,
                                          _rect.width() - _margin[0] - _margin[2],
                                          _text_height )
            elif _vertically == 1:
                _hud_rect = QtCore.QRect( _rect.x() + _margin[0],
                                          _rect.y() + _margin[1] + _text_height * _level,
                                          _rect.width() - _margin[0] - _margin[2],
                                          _text_height)
            else:
                pass

            painter.setPen(QtGui.QPen(QtGui.QColor(_hud.get("color"))))
            
            text = u"未设置"
            exec(_hud.get("cmd"))
            
            if _horizontally == -1:
                painter.drawText( _hud_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, text )
            elif _horizontally == 0:
                painter.drawText( _hud_rect, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter, text )
            else:
                painter.drawText( _hud_rect, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter, text )
        # _width =_rect.width()
        # _height =_rect.height()
        # painter.drawRect(_width*0.05,_height*0.05,_width*0.9,_height*0.9)
        #
        painter.end()

    def resizeEvent(self,event):
        if self._config:
            width_ratio ,height_ratio = self._config.get("image_size")
            new_size = event.size()
            if (new_size.height()<width_ratio*new_size.height()/height_ratio):
                new_size.setHeight(height_ratio*new_size.width()/width_ratio)
            else:
                new_size.setWidth(width_ratio*new_size.height()/height_ratio)
            self.resize(new_size)


class OperationWidget(QtWidgets.QFrame):
    playblast = QtCore.Signal(str)
    extra_path = QtCore.Signal(str)
    resolution_scale =QtCore.Signal(str)
    def __init__(self, parent = None):
        super(OperationWidget, self).__init__(parent)
        self._build()

        self.playblast_button.clicked.connect(self._playblast)
        self.get_button.clicked.connect(self._extra_path)
        self.open_button.clicked.connect(self._open_dir)
        self.resolution_scale_comebox.currentTextChanged.connect(self._resolution_scale)


    def _extra_path(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getExistingDirectory()
        self.extra_path.emit(file_path)

    def _resolution_scale(self):
        self.resolution_scale.emit(self.resolution_scale_comebox.currentText())

    def _open_dir(self):
        _path = self.path()
        if _path:
            _dir = os.path.dirname(_path)
            if os.path.isdir(_dir):
                os.system("start explorer {}".format(os.path.abspath(_dir)))

    def _playblast(self):
        self.playblast.emit(self.path())

    def path(self):
        return self.path_lineedit.text()

    def set_path(self, path):
        self.path_lineedit.setText(path)

    def is_auto_open_folder(self):
        return self.folder_checkbox.isChecked()

    def _build(self):
        self.setFixedHeight(240)
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(2)
        _layout.setContentsMargins(2,2,2,2)

        _layout.addStretch(True)

        # path widget
        self.path_widget = QtWidgets.QFrame()
        _layout.addWidget(self.path_widget)
        self.path_layout = QtWidgets.QHBoxLayout(self.path_widget)
        self.path_layout.setSpacing(8)
        self.path_layout.setContentsMargins(4,4,4,4)
        self.get_button = QtWidgets.QPushButton()
        self.path_layout.addWidget(self.get_button)
        self.get_button.setFixedSize(100,30)
        self.get_button.setText(u"文件夹选择")
        self.path_lineedit = QtWidgets.QLineEdit()
        self.path_layout.addWidget(self.path_lineedit)
        self.path_lineedit.setFixedHeight(30)
        self.open_button = QtWidgets.QPushButton()
        self.path_layout.addWidget(self.open_button)
        self.open_button.setFixedSize(100,30)
        self.open_button.setText(u"打开文件夹")

        #playblast_parameter  自定义拍屏参数
        self.playblast_parameter_widget =QtWidgets.QFrame()
        _layout.addWidget(self.playblast_parameter_widget)
        self.playblast_parameter_layout =QtWidgets.QHBoxLayout(self.playblast_parameter_widget)
        self.playblast_parameter_layout.setSpacing(4)
        self.playblast_parameter_layout.setContentsMargins(4,4,4,4)
        self.playblast_parameter_layout.addStretch(True)

        #设置缩放参数
        self.resolution_scale_laber =QtWidgets.QLabel(u"缩放比例:")
        self.playblast_parameter_layout.addWidget(self.resolution_scale_laber)
        resolution_scale_list =["0.5","1"]
        self.resolution_scale_comebox =QtWidgets.QComboBox()
        self.playblast_parameter_layout.addWidget(self.resolution_scale_comebox)
        self.resolution_scale_comebox.addItems(resolution_scale_list)
        self.resolution_scale_comebox.setCurrentIndex(1)
        self.resolution_scale_comebox.setFixedWidth(70)

        # playblast 
        self.playblast_widget = QtWidgets.QFrame()
        _layout.addWidget(self.playblast_widget)
        self.playblast_layout = QtWidgets.QHBoxLayout(self.playblast_widget)
        self.playblast_layout.setSpacing(4)
        self.playblast_layout.setContentsMargins(4,4,4,4)
        self.playblast_layout.addStretch(True)

        # open folder
        self.folder_checkbox = QtWidgets.QCheckBox()
        self.playblast_layout.addWidget(self.folder_checkbox)
        self.folder_checkbox.setText(u"自动打开文件夹")
        self.folder_checkbox.setChecked(True)

        self.playblast_button = QtWidgets.QPushButton()
        self.playblast_layout.addWidget(self.playblast_button)
        self.playblast_button.setFixedSize(120,40)
        self.playblast_button.setText(u"拍屏")
        self.playblast_button.setStyleSheet("QPushButton{background-color:#005fdf}")

        _layout.addStretch(True)



class PlayblastWidget(QtWidgets.QFrame):
    playblast = QtCore.Signal(str)
    extra_path = QtCore.Signal(str)
    resolution_scale =QtCore.Signal(str)

    def __init__(self, parent = None):
        super(PlayblastWidget, self).__init__(parent)
        self._build()

        self.operation_widget.playblast.connect(self.playblast.emit)
        self.operation_widget.extra_path.connect(self.extra_path.emit)
        self.operation_widget.resolution_scale.connect(self.resolution_scale.emit)


        self._config = {}

    def init(self, init_config):
        self._config = init_config
        self.hud_widget.init(init_config)

    def set_path(self, path):
        self.operation_widget.set_path(path)
    
    def set_image(self, image):
        self.hud_widget.set_image(image)

    def is_auto_open_folder(self):
        return self.operation_widget.is_auto_open_folder()

    def resizeEvent(self,event):
        if self._config:
            width_ratio,height_ratio = self._config.get("image_size")
            new_size = event.size()
            if (new_size.height()<width_ratio*new_size.height()/height_ratio):
                new_size.setHeight(height_ratio*new_size.width()/width_ratio)
            else:
                new_size.setWidth(width_ratio*new_size.height()/height_ratio)
            self.resize(new_size.width(), new_size.height() + self.operation_widget.height())
            global font_scale
            font_scale = float(new_size.width())/float(width_ratio)*1.5 if float(new_size.width())/float(width_ratio)*1.5<1 else 1


    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0,0,0,0)
        
        self.hud_widget = Hud_Frame()
        _layout.addWidget(self.hud_widget)

        # _layout.addStretch(True)

        self.operation_widget = OperationWidget()
        _layout.addWidget(self.operation_widget)