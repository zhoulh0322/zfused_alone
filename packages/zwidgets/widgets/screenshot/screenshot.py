# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import sys
import copy
import tempfile
import time
import logging


from Qt import QtCore,QtWidgets,QtGui

from . import screenwidget


__all__ = ["ScreenShot"]


TEMPDIR = tempfile.gettempdir()


class ScreenShot(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ScreenShot, self).__init__(parent)
        deskRect = QtWidgets.QApplication.desktop().screenGeometry()
        width = deskRect.width()
        height = deskRect.height()
        self.resize(width, height)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._set_background(width, height)
        
        self.mouse_origin = QtCore.QPoint(0,0)
        self.mouse_end = QtCore.QPoint(0,0)
        
        self.isHas = None
        self.rubber = None
        self.fileName = None

    @staticmethod
    def screen_shot(parent = None):
        dialog = ScreenShot(parent)
        dialog.show()
        dialog.exec_()
        return dialog.fileName

    def resizeEvent(self, event):
        self.listMarker = []
        self.listMarker.append(QtCore.QPoint(0,0))
        self.listMarker.append(QtCore.QPoint(self.width(), 0))
        self.listMarker.append(QtCore.QPoint(0, self.height()))
        self.listMarker.append(QtCore.QPoint(self.width(), self.height()))

        self.listMarker.append(QtCore.QPoint((self.width()/2.0), 0))
        self.listMarker.append(QtCore.QPoint((self.width()/2.0), self.height()))
        self.listMarker.append(QtCore.QPoint(0, (self.height()/2.0)))
        self.listMarker.append(QtCore.QPoint(self.width(), (self.height()/2.0)))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(255,152,0),5)
        painter.setPen(pen)
        painter.drawRect(self.rect())
        super(ScreenShot, self).paintEvent(event)

    def _grab_screen(self):
        point = self.rubber.pos()
        x = point.x()
        y = point.y()
        size = self.rubber.size()
        width = size.width()
        height = size.height()

        self.fileName = "%s/%s.png"%(TEMPDIR,time.time())

        pic = self.bg.copy(x, y, width, height)
        pic.save(self.fileName,"png")
        self.close()
        return self.fileName
        
    def mousePressEvent(self, event):
        if not self.rubber:
            #self.rubber = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self)
            self.rubber = screenwidget.ScreenWidget(self)
            self.rubber.screenshot_tool.create_button.clicked.connect(self._grab_screen)
            self.rubber.screenshot_tool.cancel_button.clicked.connect(self.close)
            self.rubber.show()
            self.mouse_origin = event.pos()
            self.rubber.setGeometry(self.mouse_origin.x(),self.mouse_origin.y(), 0, 0)
        else:
            self.isHas = True

    def mouseMoveEvent(self, event):
        if self.rubber and not self.isHas:
            self.mouse_end = event.pos()
            #resizre
            w = abs(self.mouse_end.x() - self.mouse_origin.x())
            h = abs(self.mouse_end.y() - self.mouse_origin.y())
            x = min(self.mouse_origin.x(),self.mouse_end.x())
            y = min(self.mouse_origin.y(),self.mouse_end.y())
            self.rubber.setGeometry(x,y,w,h)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


    def closeEvent(self, event):
        self.rubber.close()
        self.rubber.size_label.close()
        self.rubber.screenshot_tool.close()
        self.close()


    def _set_background(self, width, height):
        
        fileName = "%s/%s.png"%(TEMPDIR,time.time())
        #截取当前屏幕        
        QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(fileName, 'png')

        bg = QtGui.QImage(fileName)
        self.bg = QtGui.QImage(fileName)
        bg_blend = QtGui.QImage(width,height,QtGui.QImage.Format_RGB32)
        bg_blend.fill(QtGui.QColor(0,0,0,50).rgb())
                
        # 将图片设置为背景
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(bg))
        self.setPalette(palette)

        label = QtWidgets.QLabel(self)
        label.setStyleSheet("QLabel{background-color:rgba(0,0,0,50)}")
        label.setGeometry(0,0,width, height)
