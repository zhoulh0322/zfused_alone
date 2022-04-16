# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os

from Qt import QtWidgets, QtGui, QtCore


class ShowPanelWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ShowPanelWidget, self).__init__(parent)
        self.build_panel()
        # self.setMouseTracking(True)

    def mouseReleaseEvent(self, event):
        _pos = event.pos()
        _rect = QtCore.QRectF(0, 0, self.width()-self.panel_content.width(), self.height())
        if _rect.contains(_pos):
            self.close_panel()

    def resizeEvent(self, event):
        """ resize event
        """
        super(ShowPanelWidget, self).resizeEvent(event)
        self.panel.setGeometry(0, 0, self.width(), self.height())
        self.panel_blank_content.resize(self.width()*0.6, self.height())
        self.panel_content.resize(self.width()*0.5, self.height())

        self.panel_content.setMinimumWidth(self.width()*0.5)

    def load_panel_widget(self, title, widget):
        """ load panel widget 
        """
        self.panel_content_layout.addWidget( widget )
        #self.panel_splitter.setSizes([self.width() - widget.width(), widget.width()])

    def close_panel(self):
        """ close panel

        """
        self.panel.setHidden(True)

    def show_panel(self):
        """ show panel

        """
        self.panel.setHidden(False)

    def build_panel(self):
        # build panel widget
        #  panel widget
        self.panel = QtWidgets.QWidget(self)
        self.panel.setHidden(True)
        self.panel_layout = QtWidgets.QHBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(0,0,0,0)
        self.panel_layout.setSpacing(0)
        #  splitter widget
        self.panel_splitter = QtWidgets.QSplitter()
        self.panel_layout.addWidget(self.panel_splitter)
        self.panel_splitter.setStyleSheet("QSplitter{background-color:rgba(100,100,100,100)}")
        #   panel widget
        #    panel blank content
        self.panel_blank_content = QtWidgets.QWidget(self.panel_splitter)
        #    panel widget content
        self.panel_content = QtWidgets.QFrame(self.panel_splitter)
        # self.panel_content.setObjectName("panel_content")
        # self.panel_content.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.panel_content.setStyleSheet("QFrame{background-color:#FFFFFF;border:1px;border-radius:0px}")
        self.panel_content_layout = QtWidgets.QVBoxLayout(self.panel_content)
        self.panel_content_layout.setContentsMargins(0,0,0,0)
        self.panel_content_layout.setSpacing(0)
        
        self.panel_splitter.setStretchFactor(0, 6)
        self.panel_splitter.setStretchFactor(1, 4)

        #_qss = resource.get("qss", "./window.qss")
        _qss = "{}/window.qss".format(os.path.dirname(__file__))
        with open(_qss) as f:
            qss = f.read()
            self.setStyleSheet(qss)


def progress_decorator(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        ProgressWidegt.set_event("start")
        print(' '.join(["before", func_name, "is called"]))
        resp = func(*args, **kwargs)
        print(' '.join(["after", func_name, "is called"]))
        ProgressWidegt.set_event("end")
        return resp
    return wrapper

class ProgressWidegt(QtWidgets.QProgressBar):
    VALUE = 0
    MIN_VALUE = 1
    MAX_VALUE = 100
    EVENT = "end"
    def __init__(self, parent = None):
        super(ProgressWidegt, self).__init__(parent)
        self.__build()

        self._progress_timer = QtCore.QTimer(self)
        self._progress_timer.timeout.connect(self._refresh_value)
        self._progress_timer.start(500)

    def _refresh_value(self):
        if self.EVENT == "start":
            self.setHidden(False)
        else:
            self.setHidden(True)

        if self.minimum != self.MIN_VALUE:
            self.setMinimum(self.MIN_VALUE)
        if self.maximum != self.MAX_VALUE:
            self.setMaximum(self.MAX_VALUE)
        self.setValue(self.VALUE)
        # QtWidgets.QApplication.processEvents()

    @classmethod
    def set_value(cls, value):
        cls.VALUE = value
        if value == cls.MAX_VALUE:
            cls.setHidden(True)
        QtWidgets.QApplication.processEvents()
        
    @classmethod
    def set_max_value(cls, value):
        cls.MAX_VALUE = value

    @classmethod
    def set_min_value(cls, value):
        cls.MIN_VALUE = value

    @classmethod
    def set_event(cls, event = "start"):
        cls.EVENT = event

    def __build(self):
        """
        """
        self.setTextVisible(False)
        self.setHidden(True)
        self.setMaximumHeight(3)
        # # stylesheet
        # qss = """
        # QProgressBar{
        #     border: 0px solid grey;
        #     border-radius: 0px;
        #     text-align: left
        # }
        # QProgressBar::chunk {
        #     background-color: rgb(255, 0, 0);
        #     width: 1px;
        #     margin: 0pax
        # }
        # """
        # self.setStyleSheet(qss)