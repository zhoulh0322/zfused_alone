#coding:utf-8
#--author-- binglu.wang

import os
import time
import json
import logging

import maya.cmds as cmds

from zcore import filefunc

logger = logging.getLogger(__file__)

def convert_path(path):
    return path.replace(r'\/'.replace(os.sep, ''), os.sep)

def publish_file(files, src, dst):
    """ upload files 

    """
    for _file in files:
        _extend_file = os.path.basename(_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _backup_file = os.path.join(dst, _extend_file)
        #  upload alembic cache file
        logger.info("upload file {} to {}".format(_file, _backup_file))
        _result = filefunc.publish_file(_file, _backup_file)

def local_file(files, src, dst):
    """ local download files 

    """
    for _file in files:
        #  backup texture file
        _extend_file = os.path.basename(_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _local_file = os.path.join(dst, _extend_file)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        logger.info("local file {} to {}".format(_file, _backup_file))
        _result = shutil.copy(_file, _local_file)


def change_node_path(nodes, src, dst):
    """ change file nodes path

    """
    for _node in nodes:
        _file_node_attr = "%s.cachePath"%_node
        _path = _get_file_full_name(_file_node_attr)
        _extend_file = os.path.basename(_path)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _newpath = "{}/{}".format(dst,_extend_file)
        cmds.setAttr(_file_node_attr, _newpath, type = 'string')
        if convert_path(cmds.getAttr("%s.cachePath"%_node)) != convert_path(_newpath):
            raise

def nodes():
    '''获取所有缓存节点
    '''
    return [i for i in cmds.ls(type = "cacheFile") if cmds.objExists("{}.cachePath".format(i))]


def files():
    '''获取所有缓存路径
    '''
    suffix = [".mcx",".xml"]
    pathlist = []
    _nodes = nodes()
    if _nodes:
        for _node in _nodes:
            _dir = _get_file_full_name("%s.cachePath"%_node)
            _name = cmds.getAttr("%s.cacheName"%_node)
            _path = os.path.join(_dir,_name)
            cachefiles = ["{}{}".format(_path,i).replace("\\","/") for i in suffix]
            checkexists = [1 for i in cachefiles if os.path.exists(i)]
            if len(checkexists) == len(cachefiles):
                pathlist.extend(cachefiles)
        # pathlist.append(convert_path(_path))
    return pathlist


def _get_file_full_name(file_node):
    _path = cmds.getAttr(file_node)
    if "" not  in os.path.splitdrive(_path):
        return _path
    workpath = cmds.workspace(q = 1,fn = 1)
    return r"{}/{}".format(workpath,_path)

def paths(text_files):
    """ 获取文件路径交集

    :rtype: list
    """
    #get texture sets
    def _get_set(path):
        # 获取文件路径集合
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
        _com = _frist #修复不知名bug 也不知道为啥
        for i in set_list:
            _com = _com & i #原代码 _frist & i 没有迭代对比
            if not _com:
                _left_list.append(i)
                continue
            value[len(value)-1] = _com
        if _left_list:
            _set(_left_list, value)

    _set_list = _get_file_set_list(text_files)
    for _set_ in _set_list:
        print(_set_)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value