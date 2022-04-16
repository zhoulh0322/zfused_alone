# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

"""
初始化绑定 出版
创建基本统一层级目录结构
    group
        geomrtry
        rig
            master
            joint
            deform
"""

import maya.cmds as cmds


def _set_color(obj, color = (1,1,1)):
    rgb = ("R","G","B")
    cmds.setAttr(obj + ".overrideEnabled",1)
    cmds.setAttr(obj + ".overrideRGBColors",1)
    for channel, color in zip(rgb, color):
        cmds.setAttr(obj + ".overrideColor%s" %channel, color)

def init(task_id):
    # create group
    _group = cmds.group( n='Group', em=True )
    cmds.group( n='geometry', em=True ,parent=_group)
    _rig_group = cmds.group( n='rig',em=True,parent=_group)
    _master_group = cmds.group( n='master',em=True ,parent=_rig_group)
    # create circle
    modellist = cmds.ls(type='mesh')
    if modellist:
        boxlist = cmds.exactWorldBoundingBox(modellist)
        radius= max(boxlist[3],boxlist[5])
        _main_circle = cmds.circle(n='Main',nr=(0, 1, 0),r=radius*1.6)
        _first_circle = cmds.circle(n='First',nr=(0, 1, 0),r=radius*1.3)
        _second_circle= cmds.circle(n='Second',nr=(0, 1, 0),r=radius)
    else:
        _main_circle = cmds.circle(n='Main',nr=(0, 1, 0),r=5)
        _first_circle = cmds.circle(n='First',nr=(0, 1, 0),r=3.8)
        _second_circle= cmds.circle(n='Second',nr=(0, 1, 0),r=2.5) 
    # set circle parent
    cmds.parent(_second_circle,_first_circle)
    cmds.parent(_first_circle,_main_circle)
    cmds.parent(_main_circle,_master_group)
    # color&history
    _set_color('Main', color = (1,0,0))
    cmds.delete('Main', constructionHistory = True)    
    _set_color('First', color = (0,1,0))
    _set_color('Second', color = (0,0,1))
    # create joint
    cmds.group( n='joint',em=True ,parent=_rig_group)
    cmds.joint( n='Root_M')
    cmds.group( n='deform',em=True ,parent=_rig_group)