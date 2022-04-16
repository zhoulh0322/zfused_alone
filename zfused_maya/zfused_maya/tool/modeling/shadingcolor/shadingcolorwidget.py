# coding:utf-8
# --author-- lanhua.zhou

""" shading color widget """

from Qt import QtWidgets, QtGui, QtCore

from zcore import resource

from zfused_maya.ui.widgets import window

from zfused_maya.core import tomaya

import engineitemdelegate

class ShadingColorWidget(window._Window):
    def __init__(self, parent = None):
        super(ShadingColorWidget, self).__init__(parent)
        self._build()

    def _build(self):
        self.resize(800,600)
        self.set_title_name(u"着色引擎颜色(shading engine color)")
        #_layout = QtWidgets.QVBoxLayout(self)

        self.splitter = QtWidgets.QSplitter()

        self.list_widget = QtWidgets.QFrame(self.splitter)
        self.list_layout = QtWidgets.QVBoxLayout(self.list_widget)
        # head widget
        self.head_widget = QtWidgets.QFrame()
        self.head_layout = QtWidgets.QHBoxLayout(self.head_widget)
        self.head_layout.setSpacing(4)
        self.head_layout.setContentsMargins(0,0,0,0)
        self.head_name_button = QtWidgets.QPushButton()
        self.head_name_button.setText(u"着色引擎列表")
        self.head_name_button.setIcon(QtGui.QIcon(resource.get("icons", "list.png")))
        self.refresh_button = QtWidgets.QPushButton()
        self.refresh_button.setMaximumWidth(100)
        self.refresh_button.setText(u"刷新")
        self.refresh_button.setIcon(QtGui.QIcon(resource.get("icons", "refresh.png")))
        self.head_layout.addWidget(self.head_name_button)
        self.head_layout.addWidget(self.refresh_button)
        # content widget
        self.engine_list_widget = QtWidgets.QFrame()
        self.engine_list_layout = QtWidgets.QHBoxLayout(self.engine_list_widget)
        self.engine_list_layout.setSpacing(0)
        self.engine_list_layout.setContentsMargins(0,0,0,0)
        #  engine listwidget
        self.engine_listwidget = QtWidgets.QListWidget()
        self.engine_listwidget.setMouseTracking(True)
        self.engine_list_layout.addWidget(self.engine_listwidget)
        self.engine_listwidget.setSpacing(2)
        self.engine_listwidget.setItemDelegate(engineitemdelegate.EngineItemDelegate(self.engine_listwidget))
        self.engine_listwidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.engine_listwidget.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.engine_listwidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.engine_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_layout.addWidget(self.head_widget)
        self.list_layout.addWidget(self.engine_list_widget)

        # content widget
        self.content_widget = QtWidgets.QFrame(self.splitter)
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        #  name widget
        self.content_name_widget = QtWidgets.QFrame()
        self.content_name_layout = QtWidgets.QHBoxLayout(self.content_name_widget)
        self.content_name_layout.setSpacing(4)
        self.content_name_layout.setContentsMargins(0,0,0,0)
        self.content_name_button = QtWidgets.QPushButton()
        self.color_button = QtWidgets.QPushButton()
        self.color_button.setText(u"提取颜色")
        self.color_button.setMaximumWidth(100)
        self.content_name_layout.addWidget(self.content_name_button)
        self.content_name_layout.addWidget(self.color_button)
        #  color palette widget
        self.content_color_widget = QtWidgets.QFrame()
        self.content_color_widget.setMinimumHeight(40)
        self.content_color_layout = QtWidgets.QHBoxLayout(self.content_color_widget)
        self.content_color_layout.setSpacing(0)
        self.content_color_layout.setContentsMargins(0,0,0,0)
        self.color_label = QtWidgets.QLabel()
        self.color_label.setStyleSheet("QLabel{background-color:#9D9D9D}")
        self.content_color_layout.addWidget(self.color_label)
        #  material object
        self.object_listwidget = QtWidgets.QListWidget()
        self.object_listwidget.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.object_listwidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.object_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        self.content_layout.addWidget(self.content_color_widget)
        self.content_layout.addWidget(self.content_name_widget)
        self.content_layout.addWidget(self.object_listwidget)

        # switch engine 
        self.switch_engine_widget = QtWidgets.QWidget()
        self.switch_engine_layout = QtWidgets.QHBoxLayout(self.switch_engine_widget)
        self.switch_engine_layout.setSpacing(4)
        self.switch_engine_layout.setContentsMargins(4,0,4,0)
        #  orignail engine
        self.orignail_engine_button = QtWidgets.QPushButton()
        self.orignail_engine_button.setFixedSize(100, 30)
        self.orignail_engine_button.setText(u"还原自身材质球")
        #  color engine
        self.color_engine_button = QtWidgets.QPushButton()
        self.color_engine_button.setFixedSize(100, 30)
        self.color_engine_button.setText(u"显示纯色材质球")
        self.switch_engine_layout.addStretch(True)
        self.switch_engine_layout.addWidget(self.orignail_engine_button)
        self.switch_engine_layout.addWidget(self.color_engine_button)

        self.set_central_widget(self.splitter)
        self.set_tail_widget(self.switch_engine_widget)

