# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 场景集合操作函数集 """
from __future__ import print_function

import logging

import maya.cmds as cmds

logger = logging.getLogger(__name__)


def set_node_attr(node):
    """ set node rendering attr

    """
    if not cmds.objExists("{}.rendering".format(node)):
        cmds.addAttr(node, longName = "rendering",at = 'bool')
        cmds.setAttr("{}.rendering".format(node), True)

def nodes():
    """ get rendering node
    :rtype: list
    """
    _is_rendering = []
    _renderingdag = [i for i in cmds.ls(dag = 1, l = True) if cmds.objExists("{}.groom_caching".format(i))]
    for _dag in _renderingdag:
        _value = cmds.getAttr("%s.groom_caching"%_dag)
        if _value:
            _is_rendering.append(_dag)
    return _is_rendering