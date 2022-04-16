# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import logging

from Qt import QtWidgets, QtGui, QtCore

from . import constants

class StepItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent = None):
        super(StepItemDelegate, self).__init__(parent)
        self._spacing = constants.Constants.SPACING

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._load_logger)

        # test
        self._timer.start()
        #self.set_steps(["备份文件","model file"])

    def _load_logger(self):
        self.parent().repaint()

    def paint(self, painter, option, index):
        _item_handle = index.data()
        _rect = option.rect

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.setBrush(QtGui.QColor(constants.Constants.BACKGROUND_COLOR))
        painter.drawRoundedRect(_rect, 0, 0)

        painter.setPen(QtGui.QPen(QtGui.QColor("#AAAAAA"), 0.1))
        _font = QtGui.QFont("Microsoft YaHei UI", 9)
        _font.setPixelSize(14)
        _font.setBold(True)
        painter.setFont(_font)

        # draw title
        _title_rect = QtCore.QRect(_rect.x() + self._spacing,
                                   _rect.y(),
                                   _rect.width() - self._spacing*2,
                                   constants.Constants.TITLE_HEIGHT)
        painter.drawText(_title_rect, 
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, 
                         _item_handle.title())

        # draw progress text
        _progress_mum_rect = QtCore.QRect(_rect.x() + self._spacing,
                                          _rect.y(),
                                          _rect.width() - self._spacing*2,
                                          constants.Constants.TITLE_HEIGHT)
        _progress_mum_text = "%.2f"%((_item_handle.value()/(_item_handle.maximum() - _item_handle.minimum() + 1))*100) + "%"
        painter.drawText(_progress_mum_rect, 
                         QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, 
                         _progress_mum_text)

        # progress 
        _progress_rect = QtCore.QRect(_title_rect.x(),
                                         _title_rect.y() + _title_rect.height() 
                                                         + (constants.Constants.PROGRESS_HEIGHT - constants.Constants.PROGRESS_LIN_HEIGHT)/2.0,
                                         _rect.width() - self._spacing*2,
                                         constants.Constants.PROGRESS_LIN_HEIGHT)
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

        # mouse hover press
        bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
        bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
        painter.setPen(bgPen)
        painter.setBrush(bgBrush)
        painter.drawRect(option.rect)
        if option.state & QtWidgets.QStyle.State_Selected:
            bgBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 50))
            bgPen = QtGui.QPen(QtGui.QColor(160, 160, 160, 0), 2)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        elif option.state & QtWidgets.QStyle.State_MouseOver:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 30))
            bgPen = QtGui.QPen(QtGui.QColor(60, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)

        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(constants.Constants.ITEM_DELEGATE_SIZE[0],
                            constants.Constants.ITEM_DELEGATE_SIZE[1])