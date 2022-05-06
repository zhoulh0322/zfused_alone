# coding:utf-8
# --author-- lanhua.zhou

""" shading color widget """

import os

from Qt import QtWidgets, QtCore, QtGui

import maya.cmds as cmds

from zcore import resource

from zfused_maya.ui.widgets import window

from . import core


class Window(window._Window):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self._build()

        self.publish_button.clicked.connect(self._publish)
        self.asset_widget.refreshed.connect(self._load_assets)
        self.path_button.clicked.connect(self._set_cache_path)

    def _set_cache_path(self):
        _path = QtWidgets.QFileDialog.getExistingDirectory()+"/"
        self.path_lineedit.setText(_path)

    def load_assets(self, assets):
        self.asset_widget.load_assets(assets)

    def get_assets(self):
        return self.asset_widget.get_assets()

    def cache_path(self):
        return self.path_lineedit.text()

    def _publish(self):
        """ publish file
        :rtype: bool
        """
        self.info_widget.setHidden(True)
        # check info
        _check_value = self._check()
        if not _check_value:
            self.info_widget.setHidden(False)
            return 
        _elements = {}
        _assets = self.get_assets()
        if _assets:
            _elements["assets"] = _assets
        _cache_path = self.cache_path()
        # _attrs = self.get_attrs()
        # _information = {}
        #_information["description"] = u"单独发布 - {}".format( " | ".join([ _asset.get("rfn") for _asset in _assets ]) )
        # self.published.emit(self._task_id, _information, _attrs, _elements)
        args = []
        kwargs = {
            "cache_path": _cache_path,
            "assets": _assets
        }
        core.publish_alembic(*args, **kwargs)

    def _check(self):
        """ check base infomation
        :rtype: bool
        """
        _assets = self.get_assets()
        if not _assets:
            self._set_error_text(u"未选择发布资产")
            return False

        _path = self.cache_path()
        if not _path:
            self._set_error_text(u"未设置缓存输出路径")
            return False

        return True

    def _set_error_text(self, text):
        """ 显示错误信息
        :rtype: None
        """
        self.info_label.setText(text)
        self.info_widget.setHidden(False)

    def _load_assets(self):
        # 获取当前场景资产
        _assets = core.get_assets()
        self.load_assets(_assets)

    def showEvent(self, event):
        self._load_assets()
        # get default path
        _path = core.current_cache_path()
        if _path:
            self.path_lineedit.setText(_path)
        super(Window, self).showEvent(event)
        
    def _build(self):
        self.resize(850, 500)
        self.set_title(u"输出缓存")

        # 布局    
        _widget = QtWidgets.QFrame()
        self.set_central_widget(_widget)
        _layout = QtWidgets.QVBoxLayout(_widget)

        # 输出地址
        # asset widget
        self.asset_widget = AssetWidget()
        _layout.addWidget(self.asset_widget)

        self.operation_widget = QtWidgets.QFrame()
        _layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(0,4,0,0)
        self.path_lineedit = QtWidgets.QLineEdit()
        self.operation_layout.addWidget(self.path_lineedit)
        self.path_button = QtWidgets.QPushButton( u"选择地址")
        self.operation_layout.addWidget(self.path_button)
        self.path_button.setFixedSize(80, 24)
        # self.export_button = QtWidgets.QPushButton(u"输出")
        # self.export_button.setObjectName("create_button")
        # self.operation_layout.addWidget(self.export_button)
        # self.export_button.setFixedSize(100,30)

        # upload widget
        self.upload_widget = QtWidgets.QFrame()
        _layout.addWidget(self.upload_widget)
        self.upload_widget.setObjectName("publish_widget")
        self.upload_layout = QtWidgets.QVBoxLayout(self.upload_widget)
        self.upload_layout.setSpacing(0)
        self.upload_layout.setContentsMargins(2,2,2,2)

        #  information widget
        self.info_widget = QtWidgets.QFrame()
        self.info_widget.setHidden(True)
        self.info_widget.setMaximumHeight(30)
        self.info_layout = QtWidgets.QHBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(0,0,0,0)
        self.info_layout.setSpacing(0)
        self.info_label = QtWidgets.QLabel()
        self.info_label.setMinimumHeight(30)
        self.info_label.setStyleSheet("QLabel{background-color:#220000}")
        self.info_label.setText(u"无缩略图")
        self.info_layout.addWidget(self.info_label)
        self.upload_layout.addWidget(self.info_widget)

        #  push widget
        self.publish_widget = QtWidgets.QFrame()
        self.publish_layout = QtWidgets.QHBoxLayout(self.publish_widget)
        self.publish_layout.setSpacing(0)
        self.publish_layout.setContentsMargins(0,0,0,0)
        self.publish_button = QtWidgets.QPushButton()
        self.publish_button.setObjectName("publish_button")
        self.publish_button.setMinimumSize(100,40)
        self.publish_button.setIcon(QtGui.QIcon(resource.get("icons","publish.png")))
        self.publish_button.setText(u"上传文件")
        self.publish_layout.addStretch(True)
        self.publish_layout.addWidget(self.publish_button)
        self.upload_layout.addWidget(self.publish_widget)




class AssetWidget(QtWidgets.QFrame):
    selected_from_scene = QtCore.Signal()
    refreshed = QtCore.Signal()
    def __init__( self, parent = None ):
        super(AssetWidget, self).__init__(parent)
        self._build()
        self._asset_widgets = {}

        self.scene_selected_button.clicked.connect(self.selected_from_scene.emit)
        self.refresh_button.clicked.connect(self.refreshed.emit)

    def get_assets(self):
        _assets = []
        for _widget, _asset in self._asset_widgets.items():
            if _widget.isChecked():
                _assets.append(_asset)
        return _assets

    def load_assets(self, assets):
        self._asset_widgets = {}
        # clear
        for i in range(self.group_layout.count()):
            self.group_layout.itemAt(i).widget().deleteLater()

        for _asset in assets:
            name = _asset.get('code')
            namesapce = _asset.get('namespace')
            rfn = _asset.get('reference_node')
            _check_box = QtWidgets.QCheckBox(u'{} - {}'.format(namesapce,rfn))
            _check_box.setObjectName(rfn)
            _check_box.setChecked(True)
            self._asset_widgets[_check_box] = _asset
            self.group_layout.addWidget(_check_box)

    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setAlignment(QtCore.Qt.AlignTop)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0,0,0,0)

        #全选
        self.operation_frame = QtWidgets.QFrame()
        _layout.addWidget(self.operation_frame)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_frame)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(0,0,0,0)
        self.all_title = QtWidgets.QLabel(u"资产列表")
        self.operation_layout.addWidget(self.all_title)
        self.refresh_button = QtWidgets.QPushButton(u"刷新")
        self.operation_layout.addWidget(self.refresh_button)
        self.refresh_button.setFixedSize(80, 24)
        self.operation_layout.addStretch(True)
        self.scene_selected_button = QtWidgets.QPushButton(u"场景选择定位")
        self.operation_layout.addWidget(self.scene_selected_button)
        self.scene_selected_button.setFixedSize(100,20)
        self.all_check_box = QtWidgets.QCheckBox(u'全选')
        self.all_check_box.setChecked(True)
        self.all_check_box.stateChanged.connect(self.all_state)
        self.operation_layout.addWidget(self.all_check_box)

        self.scroll_widget = QtWidgets.QScrollArea()
        _layout.addWidget(self.scroll_widget)
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scroll_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.contain_widget = QtWidgets.QFrame()
        self.scroll_widget.setWidget(self.contain_widget)
        self.contain_layout = QtWidgets.QVBoxLayout(self.contain_widget)
        self.contain_layout.setSpacing(0)
        self.contain_layout.setContentsMargins(0,0,0,0)
        self.group_box = QtWidgets.QGroupBox()
        self.contain_layout.addWidget(self.group_box)
        self.group_layout = QtWidgets.QVBoxLayout(self.group_box)
        self.group_layout.setSpacing(0)
        self.group_layout.setContentsMargins(0,0,0,0)
        self.group_layout.setAlignment(QtCore.Qt.AlignTop)
        self.contain_layout.addStretch(True)

    def all_state(self):
        all_boxs = self.group_box.findChildren(QtWidgets.QCheckBox)
        if self.all_check_box.isChecked() is True:
            for check in all_boxs:
                check.setChecked(True)
        else:
            for check in all_boxs:
                check.setChecked(False)
