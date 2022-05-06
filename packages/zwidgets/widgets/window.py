# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import webbrowser

from Qt import QtWidgets, QtGui, QtCore

from zcore import resource

from . import button


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        # QtWidgets.QMainWindow.__init__(parent)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self._base_build()

        self._help_url = None
        self._is_press = False
        self._drag_position = QtCore.QPoint(0, 0)

        self.setMouseTracking(True)
        self.__build()
        self.__edge_palce_area = 8
        self.__is_press = False
        self.__drag_position = QtCore.QPoint(0, 0)

        self.close_button.clicked.connect(self.close)
        self.infomation_button.clicked.connect(self._infomation_show)

    def set_title_hide(self):
        self.title_widget.hide()

    def set_title(self, title):
        self.title_label.setText(u"  {}  ".format(title))

    def set_title_name(self, name_text):
        self.title_label.setText(u"  {}  ".format(name_text))

    def add_central_widget(self, widget):
        self.central_layout.addWidget(widget)

    def set_central_widget(self, widget):
        self.central_layout.addWidget(widget)

    def add_tail_widget(self, widget):
        self.tail_widget.setHidden(False)
        self.tail_layout.addWidget(widget)

    def set_tail_widget(self, widget):
        self.tail_widget.setHidden(False)
        self.tail_layout.addWidget(widget)

    def set_help_url(self, url):
        self._help_url = url
    
    def _infomation_show(self):
        webbrowser.open("http://www.unitcg.com/")

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

    def resizeEvent(self, event):
        """ resize event
        """
        self.__edge_place()

    def __edge_place(self):
        """ place edge frame
        """
        _rect = self.rect()

        # 
        self.top_left_edge_frame.setGeometry( _rect.x(),
                                              _rect.y(), 
                                              self.__edge_palce_area, 
                                              self.__edge_palce_area)

        # 
        self.top_right_edge_frame.setGeometry( _rect.x() + self.width() - self.__edge_palce_area, 
                                               _rect.y(),
                                               self.__edge_palce_area,
                                               self.__edge_palce_area )

        # 
        self.top_edge_frame.setGeometry( _rect.x() + self.__edge_palce_area, 
                                         _rect.y(), 
                                         _rect.width() - self.__edge_palce_area*2,  
                                         self.__edge_palce_area)

        # 
        self.left_edge_frame.setGeometry( _rect.x(), 
                                          _rect.y() + self.__edge_palce_area,
                                          self.__edge_palce_area,
                                          _rect.height() - self.__edge_palce_area*2)

        #
        self.bottom_edge_frame.setGeometry( _rect.x() + self.__edge_palce_area, 
                                            _rect.y() + self.height() - self.__edge_palce_area,
                                            _rect.width() - self.__edge_palce_area*2, 
                                            self.__edge_palce_area )

        # 
        self.right_edge_frame.setGeometry( _rect.x() + self.width() - self.__edge_palce_area ,
                                           _rect.y() + self.__edge_palce_area,
                                           self.__edge_palce_area,
                                           _rect.height() - self.__edge_palce_area*2 )

        # 
        self.bottom_left_edge_frame.setGeometry( _rect.x(), 
                                                 _rect.y() + self.height() - self.__edge_palce_area,
                                                 self.__edge_palce_area,
                                                 self.__edge_palce_area)

        #
        self.bottom_right_edge_frame.setGeometry( _rect.x() + self.width() - self.__edge_palce_area,
                                                  _rect.y() + self.height() - self.__edge_palce_area,
                                                  self.__edge_palce_area,
                                                  self.__edge_palce_area)

    def __build(self):
        """ build windows
        """
        self.resize(1200,800)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

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
            # _edge.setStyleSheet("QFrame{background-color: #FF0000}")
            # _edge.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint)
            # _edge.geometry.connect(self._set)

    def _base_build(self):
        self.resize(1200,600)
        self.widget = QtWidgets.QFrame()
        #self.widget.setObjectName("window_frame")
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)
        self.layout = QtWidgets.QVBoxLayout( self.widget )
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.widget)

        # title widget
        self.title_widget = QtWidgets.QFrame()
        self.layout.addWidget(self.title_widget)
        self.title_widget.setObjectName("window_menu_frame")
        self.title_widget.setMinimumHeight(50)
        self.title_widget.setMaximumHeight(50)
        self.title_layout = QtWidgets.QHBoxLayout(self.title_widget)
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(15, 0, 15, 0)
        #  name frame
        self.name_widget = QtWidgets.QWidget()
        self.title_layout.addWidget(self.name_widget)
        self.name_layout = QtWidgets.QHBoxLayout(self.name_widget)
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_button = QtWidgets.QPushButton()
        self.name_button.setObjectName("window_title_button")
        self.name_button.setFlat(True)
        self.name_button.setIcon(QtGui.QIcon(resource.get("icons", "z_title.png")))
        self.name_layout.addWidget(self.name_button)
        # title label
        self.title_label = QtWidgets.QPushButton()
        self.title_label.setFlat(True)
        # self.title_label.setObjectName("title_button")
        self.title_label.setMaximumHeight(30)
        self.title_label.setText("Title")
        self.title_label.setFlat(True)
        self.title_label.setObjectName("window_title_button")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(True)
        # close frame
        self.close_widegt = QtWidgets.QWidget()
        self.title_layout.addWidget(self.close_widegt)
        self.close_layout = QtWidgets.QHBoxLayout(self.close_widegt)
        self.close_layout.setContentsMargins(0, 0, 0, 0)
        self.close_layout.setSpacing(18)
        
        self.video_button = button.Button()
        self.video_button.hide()
        self.video_button.setText(r"视频讲解")
        self.video_button.setFixedHeight(24)
        self.video_button.setIcon(QtGui.QIcon(resource.get("icons", "media.png")))
        self.video_button.setStyleSheet("QPushButton{background-color:transparent;}")
        self.close_layout.addWidget(self.video_button)

        self.close_button = _Button(self.close_widegt, resource.get("icons", "close.png"), 
                                                       resource.get("icons", "close_hover.png"), 
                                                       resource.get("icons", "close_hover.png"))
        self.close_button.setFlat(True)
        self.close_button.setFixedSize(20,20)
        self.close_layout.addWidget(self.close_button)

        # central widget
        self.central_widget = QtWidgets.QFrame()
        self.layout.addWidget(self.central_widget)
        # self.central_widget.setObjectName("central_widget")
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        # tail widget
        self.tail_widget = QtWidgets.QFrame()
        self.layout.addWidget(self.tail_widget)
        self.tail_widget.setHidden(True)
        self.tail_widget.setMinimumHeight(40)
        self.tail_widget.setMaximumHeight(60)
        # self.tail_widget.setObjectName("tail_widget")
        self.tail_layout = QtWidgets.QHBoxLayout(self.tail_widget)
        self.tail_layout.setSpacing(0)
        self.tail_layout.setContentsMargins(0,0,0,0)

        self.infomation_widget = QtWidgets.QFrame()
        self.layout.addWidget(self.infomation_widget)
        self.infomation_widget.setObjectName("window_menu_frame")
        self.infomation_widget.setFixedHeight(24)
        self.infomation_layout = QtWidgets.QHBoxLayout(self.infomation_widget)
        self.infomation_layout.setSpacing(0)
        self.infomation_layout.setContentsMargins(10,2,10,2)
        self.infomation_button = QtWidgets.QPushButton(u"苏州优尼提传媒有限公司(www.unitcg.com) · 2022")
        self.infomation_button.setObjectName("title_button")
        self.infomation_button.setIcon(QtGui.QIcon(resource.get("software", "unit-logo-horizontal.png")))
        self.infomation_layout.addWidget(self.infomation_button)
        self.infomation_layout.addStretch(True)

        #_qss = resource.get("qss", "./window.qss")
        _qss = "{}/window.qss".format(os.path.dirname(__file__))
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


class _Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, normal_icon=None, hover_icon=None, pressed_icon=None):
        super(_Button, self).__init__(parent)
        
        self.setStyleSheet("QPushButton{background-color:transparent;}")

        self._normal_icon = QtGui.QIcon(normal_icon)
        self._hover_icon = QtGui.QIcon(hover_icon)
        self._pressed_icon = QtGui.QIcon(pressed_icon)

        self.setMouseTracking(True)
        self.setIcon(self._normal_icon)

    def enterEvent(self, event):
        super(_Button, self).enterEvent(event)
        self.setIcon(self._hover_icon)

    def leaveEvent(self, event):
        super(_Button, self).leaveEvent(event)
        self.setIcon(self._normal_icon)

    def mousePressEvent(self, event):
        super(_Button, self).mousePressEvent(event)
        self.setIcon(self._pressed_icon)

    def mouseReleaseEvent(self, event):
        super(_Button, self).mouseReleaseEvent(event)
        self.setIcon(self._normal_icon)


class edge_frame(QtWidgets.QFrame):
    geometry = QtCore.Signal(QtCore.QRect)
    def __init__(self, parent = None, area = "top"):
        super(edge_frame, self).__init__(parent)
        self.setMouseTracking(True)

        self._fix_area = 4

        self._is_press = False
        self._drag_position = QtCore.QPoint(0, 0)

        self._area = area

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
        super(edge_frame, self).mousePressEvent(event)
        self._is_press = True
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        super(edge_frame, self).mouseReleaseEvent(event)
        self._is_press = False
        # self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

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
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x() + _mouse_fix.x(), 
                                               self._glo_parent_point_top_left.y(), 
                                               abs(self._glo_parent_point_top_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                               _parent_rect.height() )
                elif self._area == "top":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                               _parent_rect.width(),
                                               abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "right":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y(), 
                                               _mouse_fix.x() + self.width(),
                                               _parent_rect.height() )
                elif self._area == "bottom":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x(), 
                                               self._glo_parent_point_top_left.y(),
                                               _parent_rect.width(),
                                               _mouse_fix.y() + self.height() )
                elif self._area == "top_left":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x() + _mouse_fix.x(), 
                                               self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                               abs(self._glo_parent_point_top_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                               abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "top_right":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x(), 
                                          self._glo_parent_point_top_left.y() + _mouse_fix.y(),
                                          _mouse_fix.x() + self.width(),
                                          abs(self._glo_parent_point_top_left.y() + _mouse_fix.y() - self._glo_parent_point_bottom_right.y()) )
                elif self._area == "bottom_left":
                    _rect = QtCore.QRect( self._glo_parent_point_bottom_left.x() + _mouse_fix.x(),
                                          self._glo_parent_point_top_left.y(), 
                                          abs(self._glo_parent_point_bottom_left.x() + _mouse_fix.x() - self._glo_parent_point_bottom_right.x()),
                                          _mouse_fix.y() + self.height() )
                elif self._area == "bottom_right":
                    _rect = QtCore.QRect( self._glo_parent_point_top_left.x(),
                                          self._glo_parent_point_top_left.y(), 
                                          _mouse_fix.x() + self.width(),
                                          _mouse_fix.y() + self.height() )
                # self.geometry.emit(bottom_rect )
                self.parent().setGeometry(_rect)
        else:
            self._glo_parent_point_top_left = _parent.mapToParent(_parent_rect.topLeft())
            self._glo_parent_point_top_right = _parent.mapToParent(_parent_rect.topRight())
            self._glo_parent_point_bottom_left = _parent.mapToParent(_parent_rect.bottomLeft())
            self._glo_parent_point_bottom_right = _parent.mapToParent(_parent_rect.bottomRight())