# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import hashlib

from Qt import QtWidgets,QtCore

import zfused_api

from zcore import filefunc

from zwidgets.widgets import dialog


_server_path = r"pipeline/zfused_alone"
_local_path = r"P:/zfused/pipeline/zfused_alone"

if not os.path.isdir(_local_path):
    os.makedirs(_local_path)


# 计算文件md5值
def md5_for_file(f, block_size=2**20):
    with open(f, 'rb') as fHandle:
        md5 = hashlib.md5()
        while True:
            data = fHandle.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    return md5.hexdigest()

def get_script_files():

    _script_files = {}

    _alone_scripts = zfused_api.zFused.get("alone_scripts")
    for _script in _alone_scripts:
        # print(_script)
        _script_path = _script.get("Path")
        _script_md5 = _script.get("MD5")
        
        _server_script_path = "{}{}".format(_server_path, _script_path)
        _local_script_path = "{}{}".format( _local_path, _script_path )
        
        _is_exist = False
        if os.path.isfile(_local_script_path):
            if md5_for_file(_local_script_path) == _script_md5:
                _is_exist = True

        if not _is_exist:
            try:
                if os.path.isfile(_local_script_path):
                    os.remove(_local_script_path)
            except:
                pass
            # download script file
            print((_server_script_path, _local_script_path))
            _script_files[_script.get("Name")] = [_server_script_path, _local_script_path]

    return _script_files

class UpdateWidget(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(UpdateWidget, self).__init__(parent)
        self._build()

        self._analyse_timer = QtCore.QTimer()
        self._analyse_timer.setSingleShot(True)
        self._analyse_timer.timeout.connect(self._analyse)

        # self._reveive_timer = QtCore.QBasicTimer()
        # self.step = 0

    def _analyse(self):
        self._title_label.setText(u"获取服务器数据,分析中...")
        QtWidgets.QApplication.processEvents()

        _script_files = {}

        _alone_scripts = zfused_api.zFused.get("alone_scripts", fields = ["Name", "MD5", "Path"])
        _outsource_files_num = len(_alone_scripts)

        self._title_label.setText(u"获取服务器数据,总计 {} ".format(_outsource_files_num))
        QtWidgets.QApplication.processEvents()

        self._progress_widget.setRange(0, _outsource_files_num)

        for _index, _script in enumerate(_alone_scripts):
            
            self._title_label.setText(u"{}/{} 分析是否需要更新 {}".format(_index + 1, _outsource_files_num, _script.get("Name")))
            self._progress_widget.setValue(_index + 1)
            QtWidgets.QApplication.processEvents()

            _script_path = _script.get("Path")
            _script_md5 = _script.get("MD5")
            
            _server_script_path = u"{}{}".format(_server_path, _script_path)
            _local_script_path = u"{}{}".format( _local_path, _script_path )
            
            _is_exist = False
            if os.path.isfile(_local_script_path):
                if md5_for_file(_local_script_path) == _script_md5:
                    _is_exist = True

            if not _is_exist:
                try:
                    if os.path.isfile(_local_script_path):
                        os.remove(_local_script_path)
                except:
                    pass
                # download script file
                print((_server_script_path, _local_script_path))
                _script_files[_script.get("Name")] = [_server_script_path, _local_script_path]

                self._receive_label.setText(u"下载中。。。")
                QtWidgets.QApplication.processEvents()
                # 
                filefunc.receive_file(_server_script_path, _local_script_path)
            else:
                self._receive_label.setText(u"无需更新")

        self._receive_label.hide()
        self._title_label.setText(u"已更新完成")
        self.operation_widget.showNormal()

    def _build(self):
        self.setWindowTitle(u"zFused outsource 更新...")

        self.resize(400,60)

        _layout = QtWidgets.QVBoxLayout(self)


        # title
        self._title_label = QtWidgets.QLabel()
        _layout.addWidget(self._title_label)

        self._receive_label = QtWidgets.QLabel()
        _layout.addWidget(self._receive_label)

        self._progress_widget = QtWidgets.QProgressBar(self)
        _layout.addWidget(self._progress_widget)


        self.operation_widget = QtWidgets.QFrame()
        _layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.addStretch(True)
        self.operation_button = QtWidgets.QPushButton()
        self.operation_layout.addWidget(self.operation_button)
        self.operation_button.setText(u"确认")
        self.operation_button.clicked.connect(self.close)
        self.operation_widget.hide()

        # self._progress_widget.setGeometry(30, 40, 200, 25)

        # self.btnStart = QtWidgets.QPushButton('Start', self)
        # self.btnStart.move(30, 80)
        # self.btnStart.clicked.connect(self.startProgress) 

        # self.btnReset = QtWidgets.QPushButton('Reset', self)
        # self.btnReset.move(120, 80)
        # self.btnReset.clicked.connect(self.resetBar) 

    def showEvent(self, event):
        self._analyse_timer.start()
        # self._reveive_timer.start(10, self)

    # def resetBar(self):
    #     self.step = 0
    #     self._progress_widget.setValue(0)

    # def startProgress(self):
    #     if self._reveive_timer.isActive():
    #         self._reveive_timer.stop()
    #     else:
    #         self._reveive_timer.start(100, self)

    # def timerEvent(self, event):
    #     if self.step >= 100:
    #         self._reveive_timer.stop()
    #         return

    #     self.step +=1
    #     self._progress_widget.setValue(self.step)