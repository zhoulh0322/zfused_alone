# -*- coding: UTF-8 -*-
'''
@Time    : 2022/1/19 18:05
@Author  : Jerris_Cheng
@File    : ass.py
'''


from __future__ import print_function
import os
import maya.cmds as cmds
def publish_ass(node,ass_path):
    """
    导出ass的单帧，适用于资产
    :param node: 需要导出的节点
    :param ass_path: ass的路径
    :return: ass的路径
    """
    cmds.select(cl=True)
    if not os.path.dirname(ass_path):
        os.makedirs(os.path.dirname(ass_path))
    cmds.select(node)
    cmds.arnoldExportAss(f=ass_path,s=True,expandProcedurals=1,shadowLinks=0,mask=6393,lightLinks=0,compressed=0,boundingBox=1)
    if os.path.isfile(ass_path):
        cmds.select(cl=True)
        return ass_path
    else:
        return None


