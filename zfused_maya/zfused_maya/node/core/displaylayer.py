# coding:utf-8
# --author-- binglu.wang

import maya.cmds as cmds

__FILITER__ = "norender"

def nodes():
    return list(set(cmds.ls(type = "displayLayer"))-set(["defaultLayer"]))

def norender_info(layers):
    if layers:
        for layer in layers:
            if __FILITER__ in layer.lower():
                return cmds.editDisplayLayerMembers(layer, query=1,fn = 1)