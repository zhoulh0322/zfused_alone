# coding:utf-8
#--author-- lanhua.zhou

""" custom dialog class """
from __future__ import print_function

import os
import math

from Qt import QtWidgets, QtGui, QtCore

from zcore import resource,language

from . import button


class Dialog(QtWidgets.QDialog):
    CREATE_CLICKED = QtCore.Signal()
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)
        
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint
        #                | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint
        #                | QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self._mouse_pos = QtCore.QPoint(0,0)
        self._left_button_press = False

        self._is_hold = False
        self._is_ok = False
        self._is_pin = False

        self._is_full = False
        self._normal_rect = None

        self.__build()

        self.__cancel_button.clicked.connect(self.close)
        self.__close_button.clicked.connect(self.close)
        self.__create_button.clicked.connect(self._create)
        self.__pin_button.clicked.connect(self._set_pin)

        # edge
        self.__edge_palce_area = 8
        self.__is_press = False
        self.__drag_position = QtCore.QPoint(0, 0)

        self._base_build()

    def _base_build(self):
        _qss = "{}/window.qss".format(os.path.dirname(__file__))
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


    def set_pin(self, value):
        self._is_pin = value
        if self._is_pin:
            self.__pin_button.setIcon( QtGui.QIcon(resource.get("icons", "pin_hover.png")))
        else:
            self.__pin_button.setIcon( QtGui.QIcon(resource.get("icons", "pin.png")))
            
    def _set_pin(self):
        self._is_pin = not self._is_pin
        if self._is_pin:
            self.__pin_button.setIcon( QtGui.QIcon(resource.get("icons", "pin_hover.png")))
        else:
            self.__pin_button.setIcon( QtGui.QIcon(resource.get("icons", "pin.png")))

    def is_pin(self):
        return self._is_pin

    def _close(self):
        self._is_ok = False
        self.reject()

    def set_tip(self, text, log_type = -1):
        if log_type == -1:
            self.__tip_label.setStyleSheet("QLabel#tip_label{color:#FF0000;background-color: transparent;}")
        elif log_type == 0:
            self.__tip_label.setStyleSheet("QLabel#tip_label{color:rgba(255, 165, 0,255);background-color: transparent;}")
        elif log_type == 1:
            self.__tip_label.setStyleSheet("QLabel#tip_label{color:rgba(8, 174, 99, 255);background-color: transparent;}")
        self.__tip_label.setText(text)

    def set_hold(self, is_hold):
        self._is_hold = is_hold 

    def _create(self):
        """
        """
        self.CREATE_CLICKED.emit()
        self._is_ok = True
        if not self._is_hold:
            self.accept()

    def set_title(self, text, icon = None):
        """ set dialog title

        """
        self.__title_button.setText(text)

        if icon:
            self.__title_button.setIcon(QtGui.QIcon(icon))

    def add_content_widget(self, widget):
        """ add content widget

        """
        self.__content_layout.addWidget(widget)

    def set_operation_hidden(self, va):
        self.__opeartion_widget.setHidden(va)

    def set_title_hidden(self, va):
        self.__head_widget.setHidden(va)

    def _show_full_normal(self):
        if self._is_full:
            self._show_normal()
        else:
            self._show_full()

    def _show_full(self):
        self._is_full = True
        # self.showFullScreen()
        self._normal_rect = self.geometry()
        # self._normal_rect
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        _rect = QtWidgets.QDesktopWidget().availableGeometry(screen=screen)
        self.setGeometry(_rect)

    def _show_normal(self):
        self._is_full = False
        # self.showNormal()
        if self._normal_rect:
            self.setGeometry(self._normal_rect)

    def mouseDoubleClickEvent( self, event ):
        if event.button() == QtCore.Qt.LeftButton:
            self._show_full_normal()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.__head_widget.geometry().contains(event.pos()):
                self.__is_press = True
                self.__drag_position = event.globalPos() - self.pos()
                event.accept()
        super(Dialog, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.__is_press:
            self.move(event.globalPos() - self.__drag_position)
            event.accept()
        super(Dialog, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.__is_press = False
        super(Dialog, self).mouseReleaseEvent(event)

    def resizeEvent(self, event):
        """ resize event

        """
        self.__edge_place()
        super(Dialog, self).resizeEvent(event)

    def showEvent(self, event):
        self.setAttribute(QtCore.Qt.WA_Mapped)
        super(Dialog, self).showEvent(event)

    def __edge_place(self):
        """ place edge frame
        """
        _rect = self.rect()
        _rect = QtCore.QRectF( _rect.x() - 4, 
                              _rect.y() - 4,
                              _rect.width() + 8,
                              _rect.height() + 8 )
        self.top_left_edge_frame.setGeometry( _rect.x(),
                                              _rect.y(), 
                                              self.__edge_palce_area, 
                                              self.__edge_palce_area)
        self.top_right_edge_frame.setGeometry( _rect.x() + _rect.width() - self.__edge_palce_area, 
                                               _rect.y(),
                                               self.__edge_palce_area,
                                               self.__edge_palce_area )
        self.top_edge_frame.setGeometry( _rect.x() + self.__edge_palce_area, 
                                         _rect.y(), 
                                         _rect.width() - self.__edge_palce_area*2,  
                                         self.__edge_palce_area)
        self.left_edge_frame.setGeometry( _rect.x(), 
                                          _rect.y() + self.__edge_palce_area,
                                          self.__edge_palce_area,
                                          _rect.height() - self.__edge_palce_area*2 )
        self.bottom_edge_frame.setGeometry( _rect.x() + self.__edge_palce_area, 
                                            _rect.y() + _rect.height() - self.__edge_palce_area,
                                            _rect.width() - self.__edge_palce_area*2, 
                                            self.__edge_palce_area )
        self.right_edge_frame.setGeometry( _rect.x() + _rect.width() - self.__edge_palce_area ,
                                           _rect.y() + self.__edge_palce_area,
                                           self.__edge_palce_area,
                                           _rect.height() - self.__edge_palce_area*2 )
        self.bottom_left_edge_frame.setGeometry( _rect.x(), 
                                                 _rect.y() + _rect.height() - self.__edge_palce_area,
                                                 self.__edge_palce_area,
                                                 self.__edge_palce_area)
        self.bottom_right_edge_frame.setGeometry( _rect.x() + _rect.width() - self.__edge_palce_area,
                                                  _rect.y() + _rect.height() - self.__edge_palce_area,
                                                  self.__edge_palce_area,
                                                  self.__edge_palce_area)

    def paintEvent(self, event):
        _rect = QtCore.QRectF(0, 0, self.width(), self.height())

        # path = QtGui.QPainterPath() 
        # path.setFillRule(QtCore.Qt.WindingFill)
        # path.addRoundRect(_rect,4,4)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # painter.fillPath(path, QtGui.QBrush(QtCore.Qt.white))
        # painter.setPen(QtGui.QColor("#D0D0D0"))
        # painter.drawPath(path)
        # _time_rect = QtCore.QRectF( _rect.x(), 
        #                            _rect.y(),
        #                            _rect.width(),
        #                            2)

        # _qlineargradient = QtGui.QLinearGradient(0, 0, self.width(), 0)
        # _qlineargradient.setSpread(QtGui.QGradient.PadSpread)
        # _qlineargradient.setColorAt(0, QtGui.QColor(112, 223, 2, 255))
        # _qlineargradient.setColorAt(1, QtGui.QColor(68, 191, 249, 255))
        # painter.setBrush(QtGui.QBrush(_qlineargradient))

        painter.setBrush(QtGui.QColor(0, 122, 204))
        painter.drawRoundedRect(_rect, 0, 0)
    
    def init_progress(self, min_value, max_value):
        self.__progress_bar.setRange(min_value, max_value)

    def set_progress_value(self, value):
        self.__progress_bar.setValue(value)

    def __build(self):
        """ build base dialog

        """
        self.resize(400, 600)

        self.setWindowTitle("zFused Dialog")
        __layout = QtWidgets.QVBoxLayout(self)
        __layout.setSpacing(0)
        __layout.setContentsMargins(1,1,1,1)

        # head title widget 
        self.__head_widget = QtWidgets.QFrame()
        __layout.addWidget(self.__head_widget)
        self.__head_widget.setObjectName("window_menu_frame")
        self.__head_widget.setMaximumHeight(50)
        self.__head_layout = QtWidgets.QHBoxLayout(self.__head_widget)
        #  title label
        self.__title_button = QtWidgets.QPushButton()
        self.__title_button.setObjectName("window_title_button")
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.__head_layout.addWidget(self.__title_button)
        self.__head_layout.addStretch(True)
        #  pin button
        self.__pin_button = QtWidgets.QPushButton( self ) 
        self.__pin_button.setIcon( QtGui.QIcon(resource.get("icons", "pin.png")))
        self.__head_layout.addWidget(self.__pin_button)
        #  close button
        self.__close_button = button.IconButton( self, 
                                                 resource.get("icons", "close.png"),
                                                 resource.get("icons", "close_hover.png"),
                                                 resource.get("icons", "close.png" ))
        self.__close_button.setMaximumSize(20,20)
        self.__head_layout.addWidget(self.__close_button)

        # set progress bar
        self.__progress_bar = QtWidgets.QProgressBar()
        self.__progress_bar.setMaximumHeight(3)
        self.__progress_bar.setHidden(True)
        __layout.addWidget(self.__progress_bar)

        # content widget
        # 
        self.__content_widget = QtWidgets.QFrame()
        __layout.addWidget(self.__content_widget)
        self.__content_widget.setObjectName("attr_frame")
        self.__content_layout = QtWidgets.QVBoxLayout(self.__content_widget)
        self.__content_layout.setSpacing(0)
        self.__content_layout.setContentsMargins(0,0,0,0)

        # opeartion widget
        #
        self.__opeartion_widget = QtWidgets.QFrame()
        __layout.addWidget(self.__opeartion_widget)
        self.__opeartion_widget.setObjectName("operation_frame")
        self.__opeartion_widget.setMaximumHeight(50)
        self.__opeartion_layout = QtWidgets.QHBoxLayout(self.__opeartion_widget)
        self.__opeartion_layout.setSpacing(4)
        self.__opeartion_layout.setContentsMargins(2,4,2,4)
        #  add tips label
        #  tips label
        self.__tip_label = QtWidgets.QLabel()
        self.__tip_label.setObjectName("tip_label")
        self.__opeartion_layout.addWidget(self.__tip_label)
        self.__opeartion_layout.addStretch(True)
        #  cancel button
        self.__cancel_button = QtWidgets.QPushButton()
        self.__cancel_button.setObjectName("cancel_button")
        self.__cancel_button.setText(language.word("cancel"))
        self.__cancel_button.setMinimumSize(100, 36)
        self.__opeartion_layout.addWidget(self.__cancel_button)
        #  create button
        self.__create_button = QtWidgets.QPushButton()
        self.__create_button.setObjectName("create_button")
        self.__create_button.setText(language.word("confirm"))
        self.__create_button.setMinimumSize(100, 36)
        self.__opeartion_layout.addWidget(self.__create_button)

        # top left edge frame
        self.top_left_edge_frame = edge_frame(self, "top_left")
        # top rght edge frame
        self.top_right_edge_frame = edge_frame(self, "top_right")
        # top edge frame
        self.top_edge_frame = edge_frame(self, "top")
        # left edge frame
        self.left_edge_frame = edge_frame(self, "left")
        # right edge frame
        self.right_edge_frame = edge_frame(self, "right")
        # bottom edge frame
        self.bottom_edge_frame = edge_frame(self, "bottom")
        # bottom left edge frame
        self.bottom_left_edge_frame = edge_frame(self, "bottom_left")
        # bottom right edge frame
        self.bottom_right_edge_frame = edge_frame(self, "bottom_right")
        _edges = [ self.top_left_edge_frame, 
                   self.top_right_edge_frame, 
                   self.top_edge_frame, 
                   self.left_edge_frame, 
                   self.right_edge_frame, 
                   self.bottom_edge_frame, 
                   self.bottom_left_edge_frame,
                   self.bottom_right_edge_frame]
        for _edge in _edges:
            _edge.setStyleSheet("QFrame{background-color: transparent}")

    @staticmethod
    def get(parent = None):
        """
        get user 

        rtype: zfused_api.user.User
        """
        dialog = Dialog(parent)
        # dialog.user_list_widget.load_config()
        result = dialog.exec_()
        return (dialog.is_ok, result)

    @classmethod
    def is_ok(cls):
        return cls._is_ok


class ProgressDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ProgressDialog, self).__init__(parent)
        self.__build()

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint
                       | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint
                       | QtCore.Qt.WindowMaximizeButtonHint)

    def __build(self):
        """ build progress dialog
        """
        self.setWindowTitle("zFused Progress Dialog")
        __layout = QtWidgets.QVBoxLayout(self)

        self.__progress_bar = QtWidgets.QProgressBar(self)
        __layout.addWidget(self.__progress_bar)


class edge_frame(QtWidgets.QFrame):
    geometry = QtCore.Signal(QtCore.QRect)
    def __init__(self, parent = None, area = "top"):
        super(edge_frame, self).__init__(parent)
        self.setMouseTracking(True)

        self._fix_area = 4

        self._is_press = False
        self._drag_position = QtCore.QPoint(0, 0)

        self._area = area

        self._glo_parent_point_top_left = None
        self._glo_parent_point_top_right = None
        self._glo_parent_point_bottom_left = None
        self._glo_parent_point_bottom_right = None

    def enterEvent(self, event):
        """
        """
        if self._is_press:
            return
        if self._area == "top":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif self._area == "top_left":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif self._area == "bottom_right":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif self._area == "bottom_left":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif self._area == "top_right":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif self._area == "left":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif self._area == "right":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif self._area == "bottom":
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))

    def mousePressEvent(self, event):
        self._is_press = True
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        self._is_press = False

    def mouseMoveEvent(self, event):
        """
        """
        _parent = self.parent()
        _parent_rect = self.parent().rect()
        if self._is_press:
            if event.buttons() == QtCore.Qt.LeftButton:
                _mouse_fix = event.globalPos() - self._drag_position
                _glo_mouse_point = self.parent().mapToParent(event.pos())
                if self._area == "left":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x() + _mouse_fix.x(), 
                                               self._glo_parent_point_top_left.y(), 
                                               abs(self._glo_parent_point_top_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                               _parent_rect.height() )
                elif self._area == "top":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                               _parent_rect.width(),
                                               abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "right":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y(), 
                                               _mouse_fix.x() + self.width(),
                                               _parent_rect.height() )
                elif self._area == "bottom":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y(),
                                               _parent_rect.width(),
                                               _mouse_fix.y() + self.height() )
                elif self._area == "top_left":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x() + _mouse_fix.x(), 
                                               self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                               abs(self._glo_parent_point_top_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                               abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "top_right":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x(), 
                                          self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                          _mouse_fix.x() + self.width(),
                                          abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "bottom_left":
                    _rect = QtCore.QRectF( self._glo_parent_point_bottom_left.x() + _mouse_fix.x(),
                                          self._glo_parent_point_top_left.y(), 
                                          abs(self._glo_parent_point_bottom_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                          _mouse_fix.y() + self.height() )
                elif self._area == "bottom_right":
                    _rect = QtCore.QRectF( self._glo_parent_point_top_left.x(),
                                          self._glo_parent_point_top_left.y(), 
                                          _mouse_fix.x() + self.width(),
                                          _mouse_fix.y() + self.height() )
                self.parent().setGeometry(_rect)
        else:
            self._glo_parent_point_top_left = _parent.mapToParent(_parent_rect.topLeft())
            self._glo_parent_point_top_right = _parent.mapToParent(_parent_rect.topRight())
            self._glo_parent_point_bottom_left = _parent.mapToParent(_parent_rect.bottomLeft())
            self._glo_parent_point_bottom_right = _parent.mapToParent(_parent_rect.bottomRight())
