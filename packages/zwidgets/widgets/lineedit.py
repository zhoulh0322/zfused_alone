#coding:utf-8
#--author-- lanhua.zhou

import sys
import os

from Qt import QtWidgets,QtGui,QtCore

from zcore import resource 

__all__ = ["SearchLineEdit", "LineEdit"]


class LineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.Signal()
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setStyleSheet("QLineEdit{font-family:Microsoft YaHei UI;font: bold 12px;color:#DDDDDD;}"
                           "QLineEdit{border:1px solid #555555; border-bottom:1px solid #555555}")
        self._tip = "info"
        self._is_inputmethod = False
        
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if QtCore.QEvent.KeyPress == event.type():
            self._is_inputmethod = False
        elif QtCore.QEvent.InputMethod == event.type():
            self._is_inputmethod = True
        elif QtCore.QEvent.MouseButtonPress == event.type():
            self.clicked.emit()
        return super(LineEdit, self).eventFilter(obj, event)

    def tip(self):
        return self._tip()

    def set_tip(self, tip):
        self._tip = tip

    def paintEvent(self, event):
        super(LineEdit, self).paintEvent(event)
        if not self.text() and not self._is_inputmethod:
            _rect = self.rect()
            _painter = QtGui.QPainter(self)
            _painter.save()
            _painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            _painter.setPen(QtGui.QColor("#888888"))
            _painter.drawText(QtCore.QRect( _rect.x() + 5, 
                                            _rect.y(), 
                                            _rect.width() - 5,
                                            _rect.height() ), 
                              QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, 
                              self._tip )
            _painter.restore()
        else:
            super(LineEdit, self).paintEvent(event)
        


class SearchLineEdit(QtWidgets.QLineEdit):
    search_clicked = QtCore.Signal(str)
    close_pixmap = QtGui.QPixmap(resource.get("icons", "search.png")).scaled(20, 20, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
    close_pixmap_hover = QtGui.QPixmap(resource.get("icons", "search_hover.png")).scaled(20, 20, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
    close_pixmap_pressed = QtGui.QPixmap(resource.get("icons", "search_pressed.png")).scaled(20, 20, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
    def __init__(self, parent = None):
        super(SearchLineEdit, self).__init__(parent)
        # self.setStyleSheet("QLineEdit{font-family:Microsoft YaHei UI;font: bold 12px;color:#3A3A3A;background-color:#D1D1D7}"
        #                    "QLineEdit{border:0px dotted; border-color:#343D46;padding-left: 20px}")
        self.setStyleSheet("QLineEdit{font-family:Microsoft YaHei UI;font: bold 12px;color:#DFDFDF;background-color:#5D5D5D}"
                           "QLineEdit{border:0px dotted; border-color:#343D46;padding-left: 20px}")
        self._tip = u"关键字搜索,摁enter搜索"
        self._is_inputmethod = False
        self._is_close = False
        self._is_search = False

        self.installEventFilter(self)
        self.setMouseTracking(True)

    def eventFilter(self, obj, event):
        if QtCore.QEvent.KeyPress == event.type():
            self._is_inputmethod = False
        elif QtCore.QEvent.InputMethod == event.type():
            self._is_inputmethod = True
        return super(SearchLineEdit, self).eventFilter(obj, event)

    def tip(self):
        return self._tip()

    def set_tip(self, tip):
        self._tip = tip

    def leaveEvent(self, event):
        self._is_search = False
        self.update()

    def mouseMoveEvent(self, event):
        _pos = event.pos()
        _rect = self.rect()

        _search_rect = QtCore.QRectF( _rect.x(),
                                     _rect.y(),
                                     20,
                                     _rect.height() )
        if _search_rect.contains(_pos):
            self.setCursor(QtCore.Qt.PointingHandCursor)
            self._is_search = True
        else:
            self.setCursor(QtCore.Qt.IBeamCursor)
            self._is_search = False

            if self.text():
                _close_rect = QtCore.QRectF( _rect.x() + _rect.width() - 25,
                                            _rect.y(),
                                            25,
                                            _rect.height())
                if _close_rect.contains(_pos):
                    self.setCursor(QtCore.Qt.PointingHandCursor)
                    self._is_close = True
                else:
                    self.setCursor(QtCore.Qt.IBeamCursor)
                    self._is_close = False
            else:
                self.setCursor(QtCore.Qt.IBeamCursor)
                self._is_close = False
        self.update()
        super(SearchLineEdit, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        """ 回车键和确认键
        """
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter :
            self.search_clicked.emit(self.text())
        super(SearchLineEdit, self).keyPressEvent(event)


    def mouseReleaseEvent(self, event):
        """
        """
        if self._is_close:
            self.clear()
            self.setCursor(QtCore.Qt.IBeamCursor)
            self._is_inputmethod = False
            self.search_clicked.emit(self.text())
        if self._is_search:
            self.search_clicked.emit(self.text())
        # self.update()

    def paintEvent(self, event):
        super(SearchLineEdit, self).paintEvent(event)
        _rect = self.rect()
        _painter = QtGui.QPainter(self)
        _painter.save()
        _painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        _painter.setPen(QtGui.QColor("#A5A5A5"))
        if self._is_search:
            _painter.drawPixmap(_rect.x() , _rect.y() + (_rect.height() - 20)/2, self.close_pixmap_hover )
        else:
            _painter.drawPixmap(_rect.x() , _rect.y() + (_rect.height() - 20)/2, self.close_pixmap )
        if not self.text() and not self._is_inputmethod:
            _painter.drawText(QtCore.QRectF(_rect.x() + 20, _rect.y(), _rect.width() - 5,
                                           _rect.height()), QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self._tip)

        else:
            if self.text():
                if self._is_close:
                    _painter.setPen("#FF0000")
                else:
                    _painter.setPen("#343D46")
                _painter.drawText(QtCore.QRectF(_rect.x() + 5, _rect.y(), _rect.width() - 5,
                                           _rect.height()), QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, " X ")
        _painter.restore()