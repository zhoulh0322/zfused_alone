# coding:utf-8
# --author-- lanhua.zhou

""" shading color widget """
from __future__ import print_function

import os

from Qt import QtWidgets, QtCore

from pymel.core import *
import maya.cmds as cmds
import maya.mel as mm

from zfused_maya.ui.widgets import window


def get_cam_list(*args):
	cam_list = []
	cam_list_all = ls(type = 'camera')
	for cam in cam_list_all:
		for cam_keyword in CAM_KEYWORD_LIST:
			if cam_keyword in str(cam):
			    cam_list.append(listRelatives(cam, parent = True)[0])
	return cam_list

def export_cam_ma(export_dir):
    shot_name = os.path.splitext(os.path.split(sceneName())[1])[0].split('.')[0]
    export_name = shot_name.replace('_lay', '_cam').replace('_Lay', '_cam')
    export_path = export_dir + export_name + '.ma'
    cam = get_cam_list()[0]
    select(cam, r = True)
    _cam = exportSelected(export_path, type = 'mayaAscii')
    if os.path.isfile(_cam):
        return True

def export_cam_dir(seq_dir, export_dir):
    file_list = os.listdir(seq_dir)
    cam_list =[]
    for filename in file_list:
        file_path = seq_dir + '/' + filename
        if os.path.isfile(file_path):
            if file_path.split('.')[-1] == 'ma':
                openFile(file_path, force = True)
                try:
                    export_cam_ma(export_dir)
                    cam_list.append(filename)

                except Exception as e:
                    print(e)
                    pass

    #0 全部导出成功  1 部分导出成功  2 全部没有导出成功
    if cam_list:
        if len(cam_list)==len(file_list):
            return 0
        else:
            return 1
    else:
        return 2    



class ExportCamera(window._Window):
    def __init__(self, parent = None):
        super(ExportCamera, self).__init__(parent)
        self._build()

        self.chose_Button.clicked.connect( self._set_input_folder )
        self.chose_Button2.clicked.connect(lambda :self.btn_fun(self.export_lineedit))

        self.ma_Button.clicked.connect(self._export_line)
        self.dir_Button.clicked.connect(self._seq_line)

    def _set_input_folder(self):
        self.list_widget.clear()
        _path = QtWidgets.QFileDialog.getExistingDirectory()+"/"
        self.seq_lineedit.setText(_path)
        _file_list = os.listdir(_path)
        _cam_list =[]
        for _file_name in _file_list:
            _file_path = _path + '/' + _file_name
            if os.path.isfile(_file_path):
                if _file_path.split('.')[-1] == 'ma':
                    _cam_list.append(_file_path)
        if _cam_list:
            self.list_widget.addItems(_cam_list)

    def _export_line(self):
        _path = self.export_lineedit.text()
        _state = export_cam_ma(_path)
        if _state:
            QtWidgets.QMessageBox.information(self,u"提示",u"相机导出成功！！！！！！！！！")
        else:
            QtWidgets.QMessageBox.critical(self,u"警告",u"相机未导出成功")
    
    def _seq_line(self):
        _inpath = self.seq_lineedit.text()
        _outpath = self.export_lineedit.text()
        _state = export_cam_dir(_inpath,_outpath)
        if _state == 0:
            QtWidgets.QMessageBox.information(self,u"提示",u"相机导出成功！！！！！！！！！")
        elif _state == 1:
            QtWidgets.QMessageBox.information(self,u"提示",u"部分相机导出成功，请检查文件是否正确")
        elif _state == 2:
            QtWidgets.QMessageBox.critical(self,u"警告",u"相机未导出成功")
    
    def prin(self):
        export_path = self.export_lineedit.text()
        print(export_path)

    def _build(self):
        self.resize(576, 330)
        self.set_title(u"导出摄像机(Export Camera)")
        # 布局    
        _widget = QtWidgets.QFrame()
        self.set_central_widget(_widget)
        _layout = QtWidgets.QVBoxLayout(_widget)
        # 注释
        self.error_label = QtWidgets.QLabel()
        _layout.addWidget(self.error_label)
        _layout.setSpacing(2)
        _layout.setContentsMargins(2,2,2,2)
        
        self.error_label.setStyleSheet("QLabel{font: bold 14px;background-color:#DD4444;color:#EDEDED;Text-align: center;}")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setText("每个文件内只能有一个摄像机且后缀为\"_cam\"\n输出当前场景摄像机请设置导出路径-导出当前摄像机\n批量输出请设置批量.ma文件夹路径-设置导出路径-批量导出文件夹下摄像机")
        
        # _layout.addStretch(True)

        # 输出面板
        self.export_widget = QtWidgets.QFrame()
        _layout.addWidget(self.export_widget)
        self.export_layout = QtWidgets.QHBoxLayout(self.export_widget)
        self.export_layout.setSpacing(6)
        self.export_layout.setContentsMargins(4,4,4,4)
        # 文件夹标签
        self.seq_label = QtWidgets.QLabel(self)
        self.export_layout.addWidget(self.seq_label)
        self.seq_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.seq_label.setText(u"批量.ma文件夹:") 
        # 文件夹路径输入
        self.seq_lineedit = QtWidgets.QLineEdit(self)
        self.export_layout.addWidget(self.seq_lineedit)
        # 批量路径选择
        self.chose_Button = QtWidgets.QPushButton(">>")
        self.export_layout.addWidget(self.chose_Button)
        self.chose_Button.setFixedSize(40,24)

        # 输入列表
        self.list_widget = QtWidgets.QListWidget()
        _layout.addWidget(self.list_widget)
        self.list_widget.setFrameShape(QtWidgets.QListWidget.NoFrame)
        self.list_widget.setStyleSheet("background-color:#222222")


        # 输入面板
        self.input_widget = QtWidgets.QFrame()
        _layout.addWidget(self.input_widget)
        self.input_layout = QtWidgets.QHBoxLayout(self.input_widget)
        self.input_layout.setSpacing(6)
        self.input_layout.setContentsMargins(4,4,4,4)
        # 导出标签
        self.export_label = QtWidgets.QLabel(self)
        self.input_layout.addWidget(self.export_label)
        self.export_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.export_label.setText(u"导出文件夹路径:")
        # 导出路径输入    
        self.export_lineedit = QtWidgets.QLineEdit(self)
        self.input_layout.addWidget(self.export_lineedit)
        # 导出路径选择
        self.chose_Button2 = QtWidgets.QPushButton(">>")
        self.input_layout.addWidget(self.chose_Button2)
        self.chose_Button2.setFixedSize(40,24)

        # 操作界面
        self.operation_widget = QtWidgets.QFrame()
        _layout.addWidget(self.operation_widget)
        self.operation_layout = QtWidgets.QHBoxLayout(self.operation_widget)
        self.operation_layout.setSpacing(4)
        self.operation_layout.setContentsMargins(4,4,4,4)
        # 单按钮
        self.ma_Button = QtWidgets.QPushButton()
        self.operation_layout.addWidget(self.ma_Button)
        self.ma_Button.setMinimumSize(QtCore.QSize(100, 40))
        self.ma_Button.setText(u"导出当前场景摄像机")
        self.ma_Button.setFixedWidth(200)
        self.ma_Button.setStyleSheet("QPushButton{background-color:#252526}")
        self.operation_layout.addStretch(True)
        # 批量按钮
        self.dir_Button = QtWidgets.QPushButton()
        self.operation_layout.addWidget(self.dir_Button)
        self.dir_Button.setMinimumSize(QtCore.QSize(10, 40))
        self.dir_Button.setText(u"批量导出文件夹下摄像机")
        self.dir_Button.setFixedWidth(200)
        self.dir_Button.setStyleSheet("QPushButton{background-color:#1e1e1e}")

    def btn_fun(self, line):
        _path = QtWidgets.QFileDialog.getExistingDirectory()+"/"
        line.setText(_path)

    
if __name__ =="__main__": 
    run = ExportCamera()
    run.show()
    sys.exit(app.exec_())