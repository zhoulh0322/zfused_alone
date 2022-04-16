# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

from Qt import QtWidgets, QtGui, QtCore

from zcore import resource

from zwidgets.widgets import window

import zfused_maya

from zfused_maya.core import tomaya, record


class _Window(window.Window):
    """
    
    """
    def __init__(self, parent = None):
        super(_Window, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        self.name_button.setText("zFused for maya {}".format(zfused_maya.version()))

    def showEvent(self, event):
        # 判定是否设置公司
        _company_id = record.current_company_id()
        print(_company_id)
        if not _company_id:
            # 设置公司
            from zfused_maya.interface import menubar
            _res = menubar.change_company()
            if not _company_id:
                self.close()
                return 
        super(_Window, self).showEvent(event)


class Window(window.Window):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent = tomaya.GetMayaMainWindowPoint())
        self.name_button.setText("zFused for maya {}".format(zfused_maya.version()))


class Window_(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent = tomaya.GetMayaMainWindowPoint())

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
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
        self.help_button.clicked.connect(self._help_show)

    def set_title_name(self, name_text):
        self.title_label.setText(u" {} ".format(name_text))

    def set_central_widget(self, widget):
        self.central_layout.addWidget(widget)

    def set_tail_widget(self, widget):
        self.tail_widget.setHidden(False)
        self.tail_layout.addWidget(widget)

    def set_help_url(self, url):
        self._help_url = url

    def _help_show(self):
        if not self._help_url:
            return
        # webbrowser.open(self._help_url)

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

    def _base_build(self):
        self.resize(1200,600)
        self.widget = QtWidgets.QFrame()
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)
        self.layout = QtWidgets.QVBoxLayout( self.widget )
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setCentralWidget(self.widget)

        # title widget
        self.title_widget = QtWidgets.QFrame()
        self.title_widget.setMinimumHeight(50)
        self.title_widget.setMaximumHeight(50)
        self.title_layout = QtWidgets.QHBoxLayout(self.title_widget)
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(5, 0, 5, 0)
        #  name frame
        self.name_widget = QtWidgets.QWidget()
        self.title_layout.addWidget(self.name_widget)
        self.name_layout = QtWidgets.QHBoxLayout(self.name_widget)
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_button = QtWidgets.QPushButton()
        self.name_button.setObjectName("name_button")
        self.name_button.setFlat(True)
        self.name_button.setEnabled(False)
        self.name_button.setIcon(QtGui.QIcon(resource.get("icons", "z_title.png")))
        self.name_button.setText("zFused for maya {}".format(zfused_maya.version()))
        self.name_layout.addWidget(self.name_button)
        # title label
        self.title_label = QtWidgets.QPushButton()
        self.title_label.setFlat(True)
        self.title_label.setObjectName("title_button")
        self.title_label.setMaximumHeight(30)
        self.title_label.setText("Title Name")
        #self.title_layout.addStretch(True)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(True)
        # close frame
        self.close_widegt = QtWidgets.QWidget()
        self.title_layout.addWidget(self.close_widegt)
        self.close_layout = QtWidgets.QHBoxLayout(self.close_widegt)
        self.close_layout.setContentsMargins(0, 0, 0, 0)

        # =======================================================================================================
        # help button
        self.help_button = _Button(self.close_widegt, resource.get("icons", "help.png"), 
                                                      resource.get("icons", "help_hover.png"),
                                                      resource.get("icons", "help_pressed.png") )
        self.help_button.setFlat(True)
        self.help_button.setMinimumSize(20, 20)
        self.help_button.setMaximumSize(20, 20)
        self.close_layout.addWidget(self.help_button)

        self.close_button = _Button(self.close_widegt, resource.get("icons", "close.png"), 
                                                     resource.get("icons", "close_hover.png"), 
                                                     resource.get("icons", "close_hover.png"))
        self.close_button.setObjectName("close_button")
        self.close_button.setFlat(True)
        self.close_button.setMinimumSize(20, 20)
        self.close_button.setMaximumSize(20, 20)
        # self.close_layout.addWidget(self.min_button)
        # self.close_layout.addWidget(self.max_button)
        self.close_layout.addWidget(self.close_button)

        # central widget
        self.central_widget = QtWidgets.QFrame()
        self.central_widget.setObjectName("central_widget")
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        # tail widget
        self.tail_widget = QtWidgets.QFrame()
        self.tail_widget.setHidden(True)
        self.tail_widget.setMinimumHeight(40)
        self.tail_widget.setMaximumHeight(60)
        self.tail_widget.setObjectName("tail_widget")
        self.tail_layout = QtWidgets.QHBoxLayout(self.tail_widget)
        self.tail_layout.setSpacing(0)
        self.tail_layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.title_widget)
        self.layout.addWidget(self.central_widget)
        self.layout.addWidget(self.tail_widget)


class _Button(QtWidgets.QPushButton):
    def __init__(self, parent=None, normal_icon=None, hover_icon=None, pressed_icon=None):
        super(_Button, self).__init__(parent)
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
        #super(IndexWidget, self).mousePressEvent(event)
        self._is_press = True
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        #super(IndexWidget, self).mouseReleaseEvent(event)
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
                # self.move(event.globalPos() - self._drag_position)
                # _glo_mouse_point = self.parent().mapToParent(event.pos())
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