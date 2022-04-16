# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" shotmask 操作集合 """

import maya.cmds as cmds

PLUG_IN_NAME = "shotmask.py"
NODE_NAME = "shotmask"
TRANSFORM_NODE_NAME = "shotmask"
SHAPE_NODE_NAME = "shotmask_shape"

def create_mask():
    if not cmds.pluginInfo(PLUG_IN_NAME, q=True, loaded=True):
        try:
            cmds.loadPlugin(PLUG_IN_NAME)
        except:
            return False

    if not get_mask():
        transform_node = cmds.createNode("transform", name = TRANSFORM_NODE_NAME)
        cmds.createNode(NODE_NAME, name=SHAPE_NODE_NAME, parent=transform_node)
    return True

def delete_mask():
    mask = get_mask()
    if mask:
        transform = cmds.listRelatives(mask, fullPath=True, parent=True)
        if transform:
            cmds.delete(transform)
        else:
            cmds.delete(mask)

def get_mask():
    if cmds.pluginInfo(PLUG_IN_NAME, q=True, loaded=True):
        nodes = cmds.ls(type = NODE_NAME)
        if len(nodes) > 0:
            return nodes[0]
    return None

def set_border_alpha(alpha):
    _mask = get_mask()
    if not _mask:
        return
    cmds.setAttr("{}.borderAlpha".format(_mask), alpha)

def set_mask_width(width):
    _mask = get_mask()
    if not _mask:
        return
    cmds.setAttr("{}.maskWidth".format(_mask), width)