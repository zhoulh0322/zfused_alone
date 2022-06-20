# -*- coding: UTF-8 -*-
"""
@Time    : 2022/5/18 18:19
@Author  : Jerris_Cheng
@File    : import_ui.py
@Description:
"""
from __future__ import print_function

from Qt import QtCore, QtGui, QtWidgets
from zcore import resource
from . import import_core

reload(import_core)
from zfused_maya.ui.widgets import window


class UI(window._Window):
    def __init__(self):
        super(UI, self).__init__()
        self._build()
        self.merge_button.clicked.connect(self._merge_cache)
        self.path_button.clicked.connect(self._set_cache_path)

    def _build(self):
        self.resize(850, 500)
        self.set_title(u"导入缓存")

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
        self.operation_layout.setContentsMargins(0, 4, 0, 0)
        self.path_lineedit = QtWidgets.QLineEdit()
        self.operation_layout.addWidget(self.path_lineedit)
        self.path_button = QtWidgets.QPushButton(u"选择地址")
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
        self.upload_layout.setContentsMargins(2, 2, 2, 2)

        #  information widget
        self.info_widget = QtWidgets.QFrame()
        self.info_widget.setHidden(True)
        self.info_widget.setMaximumHeight(30)
        self.info_layout = QtWidgets.QHBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.info_layout.setSpacing(0)
        self.info_label = QtWidgets.QLabel()
        self.info_label.setMinimumHeight(30)
        self.info_label.setStyleSheet("QLabel{background-color:#220000}")
        self.info_label.setText(u"无缩略图")
        self.info_layout.addWidget(self.info_label)
        self.upload_layout.addWidget(self.info_widget)

        #  push widget
        self.merge_widget = QtWidgets.QFrame()
        self.merge_layout = QtWidgets.QHBoxLayout(self.merge_widget)
        self.merge_layout.setSpacing(0)
        self.merge_layout.setContentsMargins(0, 0, 0, 0)
        self.merge_button = QtWidgets.QPushButton()
        self.merge_button.setObjectName("publish_button")
        self.merge_button.setMinimumSize(100, 40)
        self.merge_button.setIcon(QtGui.QIcon(resource.get("icons", "publish.png")))
        self.merge_button.setText(u"赋缓存")
        self.merge_layout.addStretch(True)
        self.merge_layout.addWidget(self.merge_button)
        self.upload_layout.addWidget(self.merge_widget)

    def _load_assets(self):
        # 获取当前场景资产
        _assets = import_core.get_assets()
        self.load_assets(_assets)

    def load_assets(self, assets):
        self.asset_widget.load_assets(assets)

    def showEvent(self, event):
        self._load_assets()
        # get default path
        # _path = core.current_cache_path()
        # if _path:
        #     self.path_lineedit.setText(_path)
        super(UI, self).showEvent(event)

    def _merge_cache(self):
        """
        给动画文件merge缓存
        :return:
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
        args = []
        kwargs = {
            "cache_path": _cache_path,
            "assets": _assets
        }
        #print(kwargs)
        import_core.merge_abc(*args, **kwargs)

        _fur_assets = self.get_fur_assets()
        _fur_args = []
        _fur_kwargs = {
            'cache_path':_cache_path,
            'assets':_fur_assets
        }
        import_core.fur_cache(*_fur_args,**_fur_kwargs)


    def _check(self):
        """ check base infomation
        :rtype: bool
        """
        _assets = self.get_assets()
        _fur_asset = self.get_fur_assets()
        if not _assets and not _fur_asset:
            self._set_error_text(u"未选择发布资产")
            return False

        _path = self.cache_path()
        if not _path:
            self._set_error_text(u"未设置缓存输出路径")
            return False

        return True

    def cache_path(self):
        return self.path_lineedit.text()

    def get_assets(self):
        return self.asset_widget.get_assets()

    def get_fur_assets(self):
        return self.asset_widget.fur_assets()

    def _set_error_text(self, text):
        """ 显示错误信息
        :rtype: None
        """
        self.info_label.setText(text)
        self.info_widget.setHidden(False)

    def _set_cache_path(self):
        _path = QtWidgets.QFileDialog.getExistingDirectory() + "/"
        self.path_lineedit.setText(_path)


class AssetWidget(QtWidgets.QFrame):
    selected_from_scene = QtCore.Signal()
    refreshed = QtCore.Signal()

    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        self._build()
        self._asset_widgets = {}
        self._fur_widgets = {}

        self.scene_selected_button.clicked.connect(self.selected_from_scene.emit)
        self.refresh_button.clicked.connect(self.refreshed.emit)

    def get_assets(self):
        _assets = []
        for _widget, _asset in self._asset_widgets.items():
            if _widget.isChecked():
                _assets.append(_asset)
        return _assets

    def fur_assets(self):
        _assets = []
        for _widget, _asset in self._fur_widgets.items():
            if _widget.isChecked():
                _assets.append(_asset)
        return _assets

    def load_assets(self, assets):
        self._asset_widgets = {}
        # clear
        for i in range(self.group_layout.count()):
            self.group_layout.itemAt(i).widget().deleteLater()

        for j in range(self.fur_layout.count()):
            self.fur_layout.itemAt(j).widget().deleteLater()

        for _asset in assets:
            name = _asset.get('code')
            namesapce = _asset.get('namespace')
            rfn = _asset.get('reference_node')

            _fur_info = import_core.fur_file(rfn)
            if _fur_info[0] is True:
                _fur_file = _fur_info[1]
                _fur_box = QtWidgets.QCheckBox(u'{} - {}/fur'.format(namesapce, rfn))
                _fur_box.setObjectName(rfn)
                _fur_box.setChecked(True)
                self.fur_layout.addWidget(_fur_box)
                self._fur_widgets[_check_box] = _asset
            else:
                _check_box = QtWidgets.QCheckBox(u'{} - {}'.format(namesapce, rfn))
                _check_box.setObjectName(rfn)
                _check_box.setChecked(True)
                self._asset_widgets[_check_box] = _asset

            self.group_layout.addWidget(_check_box)

    def _build(self):
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setAlignment(QtCore.Qt.AlignTop)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0, 0, 0, 0)

        # 全选
        self.operation_frame = QtWidgets.QFrame()
        _layout.addWidget(self.operation_frame)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_frame)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(0, 0, 0, 0)
        self.all_title = QtWidgets.QLabel(u"资产列表")
        self.operation_layout.addWidget(self.all_title)
        self.refresh_button = QtWidgets.QPushButton(u"刷新")
        self.operation_layout.addWidget(self.refresh_button)
        self.refresh_button.setFixedSize(80, 24)
        self.operation_layout.addStretch(True)
        self.scene_selected_button = QtWidgets.QPushButton(u"场景选择定位")
        # self.operation_layout.addWidget(self.scene_selected_button)
        self.scene_selected_button.setFixedSize(100, 20)
        self.all_check_box = QtWidgets.QCheckBox(u'全选')
        self.all_check_box.setChecked(True)
        self.all_check_box.stateChanged.connect(self.all_state)
        self.operation_layout.addWidget(self.all_check_box)
        self.fur_check_box = QtWidgets.QCheckBox(u'毛发全选')
        self.fur_check_box.setChecked(True)
        self.fur_check_box.stateChanged.connect(self.all_state)
        self.operation_layout.addWidget(self.fur_check_box)
        self.fur_check_box.stateChanged.connect(self.fur_state)

        self.scroll_widget = QtWidgets.QScrollArea()
        _layout.addWidget(self.scroll_widget)
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scroll_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.contain_widget = QtWidgets.QFrame()
        self.scroll_widget.setWidget(self.contain_widget)
        self.contain_layout = QtWidgets.QVBoxLayout(self.contain_widget)
        self.contain_layout.setSpacing(0)
        self.contain_layout.setContentsMargins(0, 0, 0, 0)
        self.group_box = QtWidgets.QGroupBox()
        self.contain_layout.addWidget(self.group_box)
        self.group_layout = QtWidgets.QVBoxLayout(self.group_box)
        self.group_layout.setSpacing(0)
        self.group_layout.setContentsMargins(0, 0, 0, 0)
        self.group_layout.setAlignment(QtCore.Qt.AlignTop)
        self.contain_layout.addStretch(True)
        # 毛发资产
        self.fur_box = QtWidgets.QGroupBox()
        self.fur_layout = QtWidgets.QVBoxLayout(self.fur_box)
        self.fur_layout.setSpacing(0)
        self.fur_layout.setContentsMargins(0, 0, 0, 0)
        self.fur_layout.setAlignment(QtCore.Qt.AlignTop)
        self.contain_layout.addWidget(self.fur_box)

    def all_state(self):
        all_boxs = self.group_box.findChildren(QtWidgets.QCheckBox)
        if self.all_check_box.isChecked() is True:
            for check in all_boxs:
                check.setChecked(True)
        else:
            for check in all_boxs:
                check.setChecked(False)

    def fur_state(self):
        all_boxs = self.fur_box.findChildren(QtWidgets.QCheckBox)
        if self.fur_check_box.isChecked() is True:
            for check in all_boxs:
                check.setChecked(True)
        else:
            for check in all_boxs:
                check.setChecked(False)
