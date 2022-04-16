 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function,division
from functools import wraps

import os
import time
import datetime
import logging

from Qt import QtWidgets, QtGui, QtCore

LABLE_TEXT = ""
MINIMUM = 0
MAXIMUM = 1
VALUE = 1

SUB_LABLE_TEXT = ""
SUB_MINIMUM = 0
SUB_MAXIMUM = 1
SUB_VALUE = 1


def reset():
    global LABLE_TEXT,SUB_LABLE_TEXT,MINIMUM,MAXIMUM,VALUE,SUB_MINIMUM,SUB_MAXIMUM,SUB_VALUE
    LABLE_TEXT = ""
    SUB_LABLE_TEXT = ""
    MINIMUM = 0
    MAXIMUM = 1
    VALUE = 1
    SUB_MINIMUM = 0
    SUB_MAXIMUM = 1
    SUB_VALUE = 1

def set_range(mini, maxi):
    global MINIMUM,MAXIMUM
    MINIMUM = mini
    MAXIMUM = maxi
    QtWidgets.QApplication.processEvents()

def set_label_text(text):
    global LABLE_TEXT
    LABLE_TEXT = text
    QtWidgets.QApplication.processEvents()

def set_value(value):
    global VALUE
    VALUE = value
    QtWidgets.QApplication.processEvents()

def set_sub_range(mini, maxi):
    global SUB_MINIMUM,SUB_MAXIMUM
    SUB_MINIMUM = mini
    SUB_MAXIMUM = maxi
    QtWidgets.QApplication.processEvents()

def set_sub_label_text(text):
    global SUB_LABLE_TEXT
    SUB_LABLE_TEXT = text
    QtWidgets.QApplication.processEvents()

def set_sub_value(value):
    global SUB_VALUE
    SUB_VALUE = value
    QtWidgets.QApplication.processEvents()



class ProgressBar(QtWidgets.QFrame):
    def __init__(self, title, parent = None):
        super(ProgressBar, self).__init__(parent)

        self._spacing = 10
        self._title = title

        self._start_time = 0
        self._end_time = 0

        self.__is_press = False
        self.__drag_position = QtCore.QPoint(0, 0)

        self.setWindowTitle(title)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setFixedSize(600,200)

        self._timer = QtCore.QTimer()
        # self._timer.setInterval(1000)
        self._timer.timeout.connect(self._change_value)
        
        self._background_color = "#444444"
        # _qss = "{}/window.qss".format(os.path.dirname(__file__))
        # with open(_qss) as f:
        #     qss = f.read()
        #     self.setStyleSheet(qss)

    def _change_value(self):
        self.showNormal()
        self.repaint()
        # QtWidgets.QApplication.processEvents()

    def paintEvent(self, event):
        _rect = self.rect()
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        painter.setBrush(QtGui.QColor(self._background_color))
        painter.drawRect(_rect)

        _rect = QtCore.QRect(_rect.x() + 20,
                             _rect.y(),
                             _rect.width() - 40,
                             _rect.height())

        # 设置字体
        _font = QtGui.QFont("Microsoft YaHei UI", 10)
        _font.setPixelSize(12)
        _font.setBold(True)
        painter.setFont(_font)
        fm = QtGui.QFontMetrics(_font)
        _pen = QtGui.QPen(QtGui.QColor("#DDDDDD"), 1, QtCore.Qt.SolidLine)
        _pen.setWidth(0.1)
        painter.setPen(_pen)
        #fm = QtGui.QFontMetrics(self.font())

        # 绘制主进度UI
        _title_rect = QtCore.QRect( 
            _rect.x() + self._spacing,
            _rect.y() + 20,
            _rect.width() - self._spacing*2,
            20
        )
        if not LABLE_TEXT:
            _title = self._title
        else:
            _title = LABLE_TEXT 
        painter.drawText(_title_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, _title)
        # 绘制时间
        _time = int(time.time() - self._start_time)
        painter.setPen(QtGui.QColor("#DD2222"))
        painter.drawText(_title_rect, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter, str(datetime.timedelta(seconds = _time)))
        painter.setPen(QtGui.QColor(0,0,0,0))
        _progress_rect = QtCore.QRect( 
            _rect.x() + self._spacing,
            _title_rect.y() + _title_rect.height() + self._spacing,
            _rect.width() - self._spacing*2,
            20
        )
        painter.setBrush(QtGui.QColor("#1e1e1e"))
        painter.drawRect(_progress_rect)
        _progress_value_rect = QtCore.QRect( 
            _progress_rect.x(),
            _progress_rect.y(),
            VALUE/(MAXIMUM - MINIMUM)*_progress_rect.width(),
            20
        )
        painter.setBrush(QtGui.QColor("#007acc"))
        painter.drawRect(_progress_value_rect)
        
        # 绘制sub进度UI
        _sub_progress = int(SUB_VALUE/(SUB_MAXIMUM - SUB_MINIMUM))
        _sub_title_rect = QtCore.QRect( 
            _rect.x() + self._spacing,
            _progress_rect.y() +  _progress_rect.height() + self._spacing,
            _rect.width() - self._spacing*2,
            20
        )
        if not SUB_LABLE_TEXT:
            _title = self._title
        else:
            _title = SUB_LABLE_TEXT 
        painter.setPen(QtGui.QColor("#FFFFFF"))
        if _sub_progress == 1:
            _title = ""
        painter.drawText(_sub_title_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, _title)
        painter.setPen(QtGui.QColor(0,0,0,0))
        _sub_progress_rect = QtCore.QRect( 
            _rect.x() + self._spacing,
            _sub_title_rect.y() + _sub_title_rect.height() + self._spacing,
            _rect.width() - self._spacing*2,
            16
        )
        if _sub_progress == 1:
            painter.setBrush(QtGui.QColor(self._background_color))
        else:
            painter.setBrush(QtGui.QColor("#1e1e1e"))
        painter.drawRect(_sub_progress_rect)
        _sub_progress_value_rect = QtCore.QRect( 
            _sub_progress_rect.x(),
            _sub_progress_rect.y(),
            SUB_VALUE/(SUB_MAXIMUM - SUB_MINIMUM)*_sub_progress_rect.width(),
            16
        )
        if _sub_progress == 1:
            painter.setBrush(QtGui.QColor(self._background_color))
        else:
            painter.setBrush(QtGui.QColor("#fed500"))
        painter.drawRect(_sub_progress_value_rect)


        painter.end()
        

    def mousePressEvent(self, event):
        self.__is_press = True
        if event.button() == QtCore.Qt.LeftButton:
            self.__drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.__is_press:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(event.globalPos() - self.__drag_position)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.__is_press = False
        event.accept()

    def start(self):
        print(u"显示进度条")
        reset()
        self._timer.start()
        self.showNormal()
        self._start_time = time.time()

    def stop(self):
        print(u"隐藏进度条")
        self._timer.stop()
        self.close()