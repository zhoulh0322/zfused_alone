# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 修改mesh shape名,统一产线 """

from __future__ import print_function

import logging

import maya.cmds as cmds
import pymel.core as pm
import maya.api.OpenMaya as om

logger = logging.getLogger(__name__)


def fix_mesh_name(post_fix_name, group_list = [], repair_shader = False):
    """修改shape名

    :param post_fix_name: 修改的后缀名称
    :param group_list: 组列表, 按组改名

    :rtype: None
    """

    # 获取组内transform

    def get_members(shape,transform):
        # 速度最快
        meshdict = {}
        _sgs = cmds.listConnections(shape,d = 1,type = "shadingEngine")
        if _sgs:
            for _sg in _sgs:
                cmds.hyperShade(objects = _sg)
                sel = cmds.ls(sl = 1,l = 1)
                meshdict[_sg] = [i for i in sel if transform == i.split(".")[0]]
        return meshdict

    def get_members1(shape,transform):
        # 速度最慢
        meshdict = {}
        _sgs = cmds.listConnections(shape,d = 1,type = "shadingEngine")
        if _sgs:
            for _sg in _sgs:
                sel = pm.PyNode(_sg).elements()
                meshdict[_sg] = [i for i in sel if transform == i.split(".")[0]]
        return meshdict

    def get_members2(shape,transform):
        '''获取材质引擎连接的模型
            速度较慢，待检查
        '''
        meshdict = {}
        _sgs = cmds.listConnections(shape,d = 1,type = "shadingEngine")
        if _sgs:
            msl = om.MSelectionList()
            for _sg in _sgs:
                msl.clear()
                msl.add(_sg)  
                mdp = msl.getDependNode(0)  
                mfs = om.MFnSet(mdp)
                sel = mfs.getMembers(True)
                meshdict[_sg] = [i for i in sel.getSelectionStrings() if transform == i.split(".")[0]]
        return meshdict

    _transforms = []
    if group_list:
        _transforms = cmds.ls(group_list, dag = True, type = "transform",l = 1)
    else:
        _transforms = cmds.ls(type = "transform",l = 1)
    if not _transforms:
        return

    shader_dict = {}
    for i,_transform in enumerate(_transforms):
        _show_shapes = cmds.listRelatives(_transform, s = True, ni = True, f = True, type = "mesh")
        if not _show_shapes:
            continue
        _all_shapes = cmds.listRelatives(_transform, s = True, f = True, type = "mesh")
        _other_shapes = list(set(_all_shapes) - set(_show_shapes))
        if _other_shapes:
            for _shape in _other_shapes:
                if _shape.endswith(post_fix_name):
                    cmds.rename(_shape, "{}_orig".format(_shape.split("|")[-1][0:len(_shape)-len(post_fix_name)]))
        _dict = {}
        for _shape in _show_shapes:
            if repair_shader:
                _dict = get_members(_shape,_transform)
            _new_shape = "{}{}".format(_transform, post_fix_name)
            if "|" in "{}{}".format(_transform, post_fix_name):
                _new_shape = _new_shape.split("|")[-1]
            _new = cmds.rename(_shape, _new_shape)

        if _dict:
            for k,v in _dict.items():
                _mesh = ["{}.{}".format(_transform,i.split(".")[-1]) for i in v]
                if k not in shader_dict:
                    shader_dict[k] = []
                shader_dict[k].extend(_mesh)

    return shader_dict


def fix_deformed_mesh_name(post_fix_name, group_list = []):
    # """修改deformed名
    # :param post_fix_name: 修改的后缀名称
    # :param group_list: 组列表, 按组改名
    # :rtype: None
    # """

    #获取组内transform
    _transforms = []
    if group_list:
        _transforms = cmds.ls(group_list, dag = True, type = "transform")
    else:
        _transforms = cmds.ls(type = "transform")
    if not _transforms:
        return
    for _transform in _transforms:
        _show_shapes = cmds.listRelatives(_transform, s = True, ni = True, f = True, type = "mesh")
        if not _show_shapes:
            continue
        for _shape in _show_shapes:
            if not _shape.endswith(post_fix_name):
                # 导出abc缓存时会自动补齐shape的空间名
                _name = "{}{}".format(_transform.split(":")[-1], post_fix_name)
                # 节点是 read noly node 会
                try:
                    cmds.rename(_shape,_name)
                except Exception as e:
                    print(e)