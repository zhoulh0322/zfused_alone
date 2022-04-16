# coding:utf-8
# --author-- binglu.wang

""" yeti节点操作集合 """

import os
import logging
import shutil
import maya.cmds as cmds

from zcore import filefunc

logger = logging.getLogger(__file__)

def publish_file(files, src, dst):
    """ upload files 

    """
    src = src.replace("\\","/")
    dst = dst.replace("\\","/")
    _texture_files = files
    for _texture_file in _texture_files:
        _texture_file = _texture_file.replace("\\","/")
        #  backup texture file
        # _extend_file = _texture_file.split(src)[-1]
        _extend_file = os.path.basename(_texture_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _backup_texture_file = os.path.join(dst, _extend_file)
        #  upload texture file
        logger.info("upload file {} to {}".format(_texture_file, _backup_texture_file))
        # print(_texture_file,_backup_texture_file)
        _result = filefunc.publish_file(_texture_file, _backup_texture_file)


def local_file(files, src, dst):
    """ local download files 

    """
    src = src.replace("\\","/")
    dst = dst.replace("\\","/")
    _texture_files = files
    for _texture_file in _texture_files:
        #  backup texture file
        _texture_file = _texture_file.replace("\\","/")
        # _extend_file = _texture_file.split(src)[-1]
        _extend_file = os.path.basename(_texture_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _local_texture_file = os.path.join(dst, _extend_file)
        #  downlocal texture file
        # _result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_texture_dir = os.path.dirname(_local_texture_file)
        if not os.path.isdir(_local_texture_dir):
            os.makedirs(_local_texture_dir)
        _result = shutil.copy(_texture_file, _local_texture_file)


def change_node_path(ori_dict, src, dst):
    """ change file nodes path

    """
    for _k,_v in ori_dict.items():
        _v = _v.replace("\\","/")
        # _extend_file = _v.split(src)[-1]
        _extend_file = os.path.basename(_v)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _new_file_text_path = "{}/{}".format(dst,_extend_file)
        # print(_v,_extend_file,_new_file_text_path)
        _node,_tex_node = _k.split("/")
        while True:
            cmds.pgYetiGraph(_node,node = _tex_node,param = "file_name",setParamValueString = _new_file_text_path)
            if cmds.pgYetiGraph(_node,node = _tex_node,param = "file_name",getParamValue = 1) == _new_file_text_path:
                break

def _get_yeti_attr(nodeType,attrName,ignoreReference = True):
    pg_dict = {}
    _pgyetinodes = cmds.ls(type = "pgYetiMaya")
    if _pgyetinodes:
        for _i in _pgyetinodes:
            if ignoreReference and cmds.referenceQuery(_i,inr = 1):
                continue
            selnodes = cmds.pgYetiGraph(_i,listNodes = 1,type = nodeType)
            for selnode in selnodes:
                attr_v = cmds.pgYetiGraph(_i,node = selnode,param = attrName,getParamValue = 1)# 查询param命令lsp = 1
                pg_dict["%s/%s"%(_i,selnode)] = attr_v
    return pg_dict


def tex_files():
    import zfused_maya.node.core.texture as texture
    _texlist = list()
    _pgnodes = cmds.ls(type = "pgYetiMaya")
    for _pgnode in _pgnodes:
        _tex_nodes = cmds.pgYetiGraph(_pgnode,listNodes = 1,type = "texture")
        if not _tex_nodes:
            continue
        for _j in _tex_nodes:
            _v = cmds.pgYetiGraph(_pgnode,node = _j,param = "file_name",getParamValue = 1)
            if not _v:
                continue
            _filepaths = texture.get_udim_texfile(_v,False)
            for _filepath in _filepaths:
                if not os.path.exists(_filepath):
                    continue
                _texlist.append(_filepath)
    return _texlist


def paths(text_files):
    """ 获取文件路径交集

    由于上传前检查了贴图放在同一目录
    所以这一步获取的本地路径就是贴图的真实路径？？

    :rtype: list
    """
    #get texture sets
    def _get_set(path):
        _list = []
        def _get_path(_path, _list):
            _path_new = os.path.dirname(_path)
            if _path_new != _path:
                _list.append(_path_new)
                _get_path(_path_new, _list)
        _get_path(path, _list)
        return _list

    def _get_file_set_list(_files):
        _files_set_dict = {}
        _set_list = []
        for _f in _files:
            _set = set(_get_set(_f))
            _set_list.append(_set)
        return _set_list

    def _set(set_list,value):
        _frist = set_list[0]
        value.append(_frist)
        _left_list = []
        for i in set_list:
            _com = _frist & i
            if not _com:
                _left_list.append(i)
                continue
            value[len(value)-1] = _com
        if _left_list:
            _set(_left_list, value)

    _set_list = _get_file_set_list(text_files)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  
    return _value