# coding:utf-8
# --author-- ning.qin
from __future__ import print_function

import os
from pymel.core import *
import maya.cmds as cmds

CAM_KEYWORD_LIST = ['cam']

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
    _cam =exportSelected(export_path, type = 'mayaAscii')
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