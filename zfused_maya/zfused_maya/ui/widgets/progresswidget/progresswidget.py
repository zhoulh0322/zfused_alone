# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import logging

from Qt import QtWidgets, QtGui, QtCore

from zfused_maya.core import tomaya
import steplogger

from . import constants


global PROGRESS_WIDGET

class ProgressWidget(QtWidgets.QProgressBar):
    PROGRESS_STEP = []
    PROGRESS_LOGGER = {}

    @classmethod
    def clear(cls):
        cls.PROGRESS_STEP = []
        cls.PROGRESS_LOGGER = {}

    def __init__(self, steps = []):
        super(ProgressWidget, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        #super(ProgressWidget, self).__init__()
        #self._build()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #| QtCore.Qt.Window)
        self._spacing = constants.Constants.SPACING

        if steps:
            self.add_steps(steps)
        # test
        #self.add_steps(["backup file","model file"])

    def set_value(self, step, value):
        self.PROGRESS_LOGGER[step].set_value(value)

    def _paint_step(self, painter, rect, step_logger):
        _item_handle = step_logger
        _rect = rect
        painter = painter
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.setBrush(QtGui.QColor(constants.Constants.BACKGROUND_COLOR))
        painter.drawRoundedRect(_rect, 0, 0)

        painter.setPen(QtGui.QPen(QtGui.QColor("#AAAAAA"), 0.1))
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(12)
        _font.setBold(True)
        painter.setFont(_font)

        # draw title
        _title_rect = QtCore.QRect(_rect.x(),
                                   _rect.y() + self._spacing,
                                   _rect.width() - self._spacing*2,
                                   constants.Constants.TITLE_HEIGHT)
        painter.drawText(_title_rect, 
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, 
                         _item_handle.title())

        # draw progress text
        _progress_mum_rect = QtCore.QRect(_rect.x() + self._spacing,
                                          _rect.y() + self._spacing,
                                          _rect.width() - self._spacing*2,
                                          constants.Constants.TITLE_HEIGHT)
        _progress_mum_text = "%.2f"%((_item_handle.value()/(_item_handle.maximum() - _item_handle.minimum() + 1))*100) + "%"
        painter.drawText(_progress_mum_rect, 
                         QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, 
                         _progress_mum_text)

        # progress 
        _progress_rect = QtCore.QRect(   _title_rect.x(),
                                         _title_rect.y() 
                                         + _title_rect.height() + self._spacing, 
                                         #+ (constants.Constants.PROGRESS_HEIGHT - constants.Constants.PROGRESS_LIN_HEIGHT)/2.0,
                                         _rect.width() - self._spacing*2,
                                         constants.Constants.PROGRESS_LIN_HEIGHT)
        
        """
        _progress_rect = QtCore.QRect(_title_rect.x(),
                                         _title_rect.y() + _title_rect.height() - constants.Constants.PROGRESS_LIN_HEIGHT, 
                                         _rect.width() - self._spacing*2,
                                         constants.Constants.PROGRESS_LIN_HEIGHT)
        """

        painter.setBrush(QtGui.QColor("#FFFFFF"))
        painter.drawRoundedRect(_progress_rect, 2, 2)
        #  painter value
        _percent = float(_item_handle.value())/(_item_handle.maximum() - _item_handle.minimum() + 1)
        _percent_rect = QtCore.QRect(_progress_rect.x(),
                                     _progress_rect.y(),
                                     _progress_rect.width()*_percent,
                                     _progress_rect.height())
        painter.setBrush(QtGui.QColor("#FF0000"))
        painter.drawRoundedRect(_percent_rect, 2, 2)

        painter.restore()

    def paintEvent(self, event):
        #_item_handle = self.PROGRESS_LOGGER["model file"]
        _rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(QtGui.QColor("#5C5C5C"))
        painter.setPen(QtGui.QPen(QtGui.QColor("#007ACC"), 1))
        painter.drawRoundedRect(_rect, 1, 1)
        _rect = QtCore.QRect(_rect.x(),
                             _rect.y(),
                             _rect.width(),
                             _rect.height())

        _height = self._spacing
        if self.PROGRESS_STEP:
            for _name in self.PROGRESS_STEP:
                _step_rect = QtCore.QRect(_rect.x(),
                                          _rect.y(),
                                          _rect.width(),
                                          constants.Constants.ITEM_DELEGATE_SIZE[1])
                self._paint_step(painter, _step_rect, self.PROGRESS_LOGGER[_name])
                _height += constants.Constants.ITEM_DELEGATE_SIZE[1] + self._spacing

        painter.restore()

    def add_steps(self, steps):
        """ 设置进度总步骤
        
        """
        #self.PROGRESS_STEP = []
        #self.PROGRESS_LOGGER = {}

        if not steps:
            return 
        _model_data = []
        for _index, _step in enumerate(steps):
            self.PROGRESS_STEP.append(_step)
            print(self.PROGRESS_STEP)
            if not self.PROGRESS_LOGGER.__contains__(_step):
                _data = {"title":_step,
                         "maximum": 100.0,
                         "minimum": 1.0,
                         "value": 0.0,
                         "text": "init"}
                _logger = steplogger.StepLogger(_step, _data)
                self.PROGRESS_LOGGER[_step] = _logger

            # build step widget
            _step_logger = steplogger.StepLogger(_step, self.PROGRESS_LOGGER[_step])
            _model_data.append(_step_logger)
            #self.step_listwidget.addItem(_step_logger)
        #_step_list_model = steplistmodel.StepListModel(_model_data, self.step_listwidget)
        #self.step_listwidget.setModel(_step_list_model)

        _width = tomaya.GetMayaMainWindowPoint().width()
        _height = tomaya.GetMayaMainWindowPoint().height()
        #_x = _width/4.0
        #_progress_width = _width/2.0
        #_progress_height = (constants.Constants.ITEM_DELEGATE_SIZE[1] + self._spacing)*len(_model_data) + self._spacing*3
        
        _progress_width = _width
        #_progress_height = (constants.Constants.ITEM_DELEGATE_SIZE[1] + self._spacing)*len(_model_data) + self._spacing*3
        _progress_height = 30
        #_progress_height = _height
        _x = 0
        _y = 0
        #_y = (_height - _progress_height)/2.0
        #_y = _height - _progress_height
        self.setGeometry(_x, _y, _progress_width, _progress_height)


PROGRESS_WIDGET = ProgressWidget()

def show():
    PROGRESS_WIDGET.show()

def close():
    PROGRESS_WIDGET.close()
    ProgressWidget.PROGRESS_STEP = []
    ProgressWidget.PROGRESS_LOGGER = {}

def set_value(title, value):
    pass