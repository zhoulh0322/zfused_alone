# coding:utf-8
#--author-- lanhua.zhou

""" custom button class """

from __future__ import print_function

import os
import time
import tempfile
import logging
import requests

from Qt import QtWidgets, QtGui, QtCore

from zcore import video

__all__ = ["IconButton", "ThumbnailButton"]

logger = logging.getLogger(__name__)


class Button(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super(Button, self).__init__(parent)

    def enterEvent(self, event):
        super(Button, self).enterEvent(event)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def leaveEvent(self, event):
        super(Button, self).leaveEvent(event)
        self.setCursor(QtCore.Qt.ArrowCursor)


class IconButton(QtWidgets.QPushButton):
    def __init__(self, parent = None, normal_icon = None, hover_icon = None, pressed_icon = None):
        super(IconButton, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)
        # self.setObjectName("icon_button")

    def enterEvent(self, event):
        super(IconButton, self).enterEvent(event)
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)

    def leaveEvent(self, event):
        super(IconButton, self).leaveEvent(event)
        self.setIcon(self._normal_icon)
        #self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(IconButton, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)
        #self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        super(IconButton, self).mouseReleaseEvent(event)


class ToolButton(QtWidgets.QToolButton):
    def __init__(self, parent = None, normal_icon = None, hover_icon = None, pressed_icon = None):
        super(ToolButton, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)
        self.setObjectName("icon_button")

    def enterEvent(self, event):
        super(ToolButton, self).enterEvent(event)
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)

    def leaveEvent(self, event):
        super(ToolButton, self).leaveEvent(event)
        self.setIcon(self._normal_icon)
        #self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(ToolButton, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)
        #self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        super(ToolButton, self).mouseReleaseEvent(event)


class ConfirmButton(QtWidgets.QPushButton):
    def __init__(self, parent = None, normal_icon = None, hover_icon = None, pressed_icon = None):
        super(ConfirmButton, self).__init__(parent)
        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)
        self.setObjectName("icon_button")

        self.setStyleSheet("""
        QPushButton{
            Text-align: center;
            background-color: rgb(66, 209, 127);
            color: #FFFFFF;
            qproperty-iconSize: 16px;
        }

        QPushButton:hover{
            color: #FFFFFF;
            background-color: rgb(66, 189, 107);
        }

        QPushButton:pressed{
            color: #FFFFFF;
            background-color: #4FC1E9;
            border-bottom: 0px solid #444444;
        }
            """)

    def enterEvent(self, event):
        super(ConfirmButtn, self).enterEvent(event)
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)

    def leaveEvent(self, event):
        super(ConfirmButton, self).leaveEvent(event)
        self.setIcon(self._normal_icon)
        #self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(ConfirmButton, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)
        #self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setIcon(self._hover_icon)
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        super(ConfirmButton, self).mouseReleaseEvent(event)


class ThumbnailButton(QtWidgets.QPushButton):
    upload_clicked = QtCore.Signal()
    def __init__(self, thumbnail = None, video = None, parent = None):
        super(ThumbnailButton, self).__init__(parent)
        
        self._tips = u"无缩略图"
        self._thumbnail = thumbnail
        self._video = video

        self._is_hover = False
        self.clicked.connect(self.upload_clicked.emit)

    def thumbnail(self):
        """ get thumbnail file
        :rtype: str
        """
        return self._thumbnail

    def video(self):
        """ get video file
        :rtype: str
        """
        return self._video

    def set_thumbnail(self, thumbnail):
        """ set thumbnail file for show
        
        :rtype: None
        """
        self._thumbnail = thumbnail
        self.update()

    def set_video(self, video_file):
        """ set video file for show

        :rtype: None
        """
        self._video = video_file
        tempDir = tempfile.gettempdir()
        _thumbnail = "%s/%s.png"%(tempDir,time.time())
        value = video.cut_image(video_file, _thumbnail)
        self.set_thumbnail(_thumbnail)

    def enterEvent(self, event):
        super(ThumbnailButton, self).enterEvent(event)
        self._is_hover = True

    def leaveEvent(self, event):
        super(ThumbnailButton, self).leaveEvent(event)
        self._is_hover = False

    def paintEvent(self, event):
        super(ThumbnailButton, self).paintEvent(event)
        _rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # if self._thumbnail and os.path.isfile(self._thumbnail):
        if self._thumbnail:
            if self._thumbnail.startswith("http"):
                req = requests.get(self._thumbnail)
                _pixmap = QtGui.QPixmap()
                _pixmap.loadFromData(req.content)
            else:
                _pixmap = QtGui.QPixmap(self._thumbnail)
            _pixmap_size = _pixmap.size()
            _label_size = QtCore.QSize(_rect.width(), _rect.height())
            if _pixmap_size:
                scale = max(float(_label_size.width() / float(_pixmap_size.width())),
                            float(_label_size.height()) / float(_pixmap_size.height()))
                _pixmap = _pixmap.scaled(_pixmap_size.width() * scale, 
                                        _pixmap_size.height() * scale)
                _thumbnail_pixmap = _pixmap.copy((_pixmap_size.width() * scale - _label_size.width()) / 2.0, 
                                                (_pixmap_size.height() * scale - _label_size.height()) / 2.0, 
                                                _label_size.width(), 
                                                _label_size.height())
                painter.drawPixmap(_rect.x(), _rect.y(), _thumbnail_pixmap)
        else:
            painter.setPen(QtGui.QColor("#1e1e1e"))
            painter.setPen(QtCore.Qt.DotLine)
            painter.drawRoundedRect(_rect, 4, 4)
            painter.setPen(QtGui.QColor("#444444"))
            painter.drawText(_rect, QtCore.Qt.AlignCenter, u"无缩略图")

        path = QtGui.QPainterPath()
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1))
        path.addRect(_rect.x(),_rect.y(),_rect.width(),_rect.height())
        path.addRoundedRect(_rect.x(),_rect.y(),_rect.width(),_rect.height(), 0, 0)
        self._background_color = self.parent().palette().color(self.parent().backgroundRole())
        painter.setBrush(QtGui.QBrush(QtGui.QColor(self._background_color)))
        path.setFillRule(QtCore.Qt.OddEvenFill)
        painter.drawPath(path)

        if self._is_hover:
            _houver_rect = QtCore.QRectF( _rect.x() + (_rect.width() - 100)/2,
                                         _rect.y() + (_rect.height() - 20)/2,
                                         100,20 )
            painter.setBrush(QtGui.QColor(255,255,255,160))
            painter.drawRoundedRect(_houver_rect, 4, 4)
            painter.setPen(QtGui.QColor("#666666"))
            painter.drawText( _houver_rect, QtCore.Qt.AlignCenter, "点击修改缩略图" )
        # painter re
        # painter.drawRoundRect(_rect, 2, 2)
        painter.restore()