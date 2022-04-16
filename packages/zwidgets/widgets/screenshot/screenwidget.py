# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import logging

from Qt import QtWidgets,QtGui,QtCore

__all__ = ["ScreenWidget"]


class ScreenWidget(QtWidgets.QWidget):
    PADDING_ = 10
    direction = {}
    def __init__(self, parent = None):
        super(ScreenWidget, self).__init__(parent)
        self.isPress = False
        self._dir = None

        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
    
        self.listMarker = []

        self.screenshot_tool = _ScreenshotTool()
        self.screenshot_tool.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
        self.size_label = QtWidgets.QLabel()
        self.size_label.resize(80,20)
        self.size_label.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)

    def _get_region(self, cursor):
        ret_dir = None
        pt_lu = self.mapToParent(self.rect().topLeft())
        pt_rl = self.mapToParent(self.rect().bottomRight())

        x = cursor.x()
        y = cursor.y()

        #获得鼠标当前所处窗口的边界方向
        if pt_lu.x() + self.PADDING_ >= x and pt_lu.x() <= x and pt_lu.y() + self.PADDING_ >= y and pt_lu.y() <= y:
            #左上角
            ret_dir = "LEFTUPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif x >= pt_rl.x() - self.PADDING_ and x <= pt_rl.x() and y >= pt_rl.y() - self.PADDING_ and y <= pt_rl.y():
            #右下角
            ret_dir = "RIGHTLOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))

        elif x <= pt_lu.x() + self.PADDING_ and x >= pt_lu.x() and y >= pt_rl.y() - self.PADDING_ and y <= pt_rl.y():
            #左下角
            ret_dir = "LEFTLOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif x <= pt_rl.x() and x >= pt_rl.x() - self.PADDING_ and y >= pt_lu.y() and y <= pt_lu.y() + self.PADDING_:
            #右上角
            ret_dir = "RIGHTUPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif x <= pt_lu.x() + self.PADDING_ and x >= pt_lu.x():
            #左边
            ret_dir = "LEFT"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif x <= pt_rl.x() and x >= pt_rl.x() - self.PADDING_:
            #右边
            ret_dir = "RIGHT"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif y >= pt_lu.y() and y <= pt_lu.y() + self.PADDING_:
            #上边
            ret_dir = "UPPER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif y <= pt_rl.y() and y >= pt_rl.y() - self.PADDING_:
            #下边
            ret_dir = "LOWER"
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        else:
            ret_dir = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        return ret_dir

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

        self._set_label()

    def _set_label(self):
        point = self.pos()
        x = point.x()
        y = point.y()
        size = self.size()
        self.size_label.setText(" %s x %s"%(size.width(),size.height()))
        rect = self.size_label.contentsRect()
        #self.size_label.setGeometry(x,y - rect.height(),rect.width(),rect.height())
        self.size_label.move(QtCore.QPoint(x,y - rect.height()))
        self.size_label.show()

        rect_screenshot_tool = self.screenshot_tool.contentsRect()
        self.screenshot_tool.move(QtCore.QPoint(x + size.width()-rect_screenshot_tool.width(),y + size.height()))
        self.screenshot_tool.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(0,174,255),2)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        pen.setWidth(5)
        pen.setColor("#26E0EE")
        painter.setPen(pen)
        painter.drawPoints(self.listMarker)

    def mousePressEvent(self, event):
        self.isPress = True
        if event.button() == QtCore.Qt.LeftButton:
            #self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.dragPosition = event.globalPos() - self.pos()
            event.accept()
    def mouseReleaseEvent(self, event):
        self.isPress = False
        event.accept()

    def mouseMoveEvent(self, event):
        gloPoint = self.mapToParent(event.pos())
        if not self.isPress:
            co = self.mapToParent(event.pos())
            self._dir = self._get_region(co)
            #get point
            self.originPoint_ = self.mapToParent(self.rect().topLeft())
            self.originPoint_lu = self.mapToParent(self.rect().topLeft())
            self.originPoint_ll = self.mapToParent(self.rect().bottomLeft())
            self.originPoint_ru = self.mapToParent(self.rect().topRight())
            self.originPoint_rl = self.mapToParent(self.rect().bottomRight())
            self.rect_ = self.rect()
        else:
            if event.buttons() == QtCore.Qt.LeftButton:
                global_x = gloPoint.x()
                global_y = gloPoint.y()
                if self._dir == None:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()
                elif self._dir == "LEFT":
                    self.setGeometry(global_x,self.originPoint_lu.y(),abs(global_x - self.originPoint_rl.x()),self.rect_.height())
                elif self._dir == "RIGHT":
                    self.setGeometry(self.originPoint_lu.x(),self.originPoint_lu.y(),abs(global_x - self.originPoint_lu.x()),self.rect_.height())
                elif self._dir == "UPPER":
                    self.setGeometry(self.originPoint_lu.x(),global_y,self.rect_.width(),abs(global_y - self.originPoint_rl.y()))
                elif self._dir == "LOWER":
                    self.setGeometry(self.originPoint_lu.x(),self.originPoint_lu.y(),self.rect_.width(),abs(global_y - self.originPoint_lu.y()))
                elif self._dir == "LEFTUPPER":
                    self.setGeometry(global_x, global_y, self.originPoint_rl.x() - global_x, self.originPoint_rl.y() - global_y)
                elif self._dir == "LEFTLOWER":
                    self.setGeometry(global_x, self.originPoint_lu.y(), self.originPoint_rl.x() - global_x, - self.originPoint_ru.y() + global_y)
                elif self._dir == "RIGHTUPPER":
                    self.setGeometry(self.originPoint_lu.x(), global_y, global_x - self.originPoint_lu.x(), self.originPoint_rl.y() - global_y)
                elif self._dir == "RIGHTLOWER":
                    self.setGeometry(self.originPoint_lu.x(), self.originPoint_lu.y(), global_x - self.originPoint_lu.x(), global_y - self.originPoint_lu.y())
                self.parentWidget().update()
                self._set_label()

class _ScreenshotTool(QtWidgets.QFrame):
    def __init__(self):
        super(_ScreenshotTool,self).__init__()
        self._build()

    def _build(self):
        _layout = QtWidgets.QHBoxLayout(self)   

        # cancel button
        self.cancel_button = QtWidgets.QPushButton()
        self.cancel_button.setText(u"取消")
        #self.cancel_button.setIcon(QtGui.QIcon(resource.get("icons", "cancel.png")))
        # create button
        self.create_button = QtWidgets.QPushButton()
        self.create_button.setText(u"完成")
        #self.create_button.setIcon(QtGui.QIcon(resource.get("icons", "ok.png")))

        _layout.addStretch(True)
        _layout.addWidget(self.cancel_button)
        _layout.addWidget(self.create_button)