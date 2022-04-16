# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" reference文件操作集合 """

import os
import shutil
import logging

import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm

from zcore import filefunc


logger = logging.getLogger(__name__)

def publish_file(files, src, dst):
    """ upload files 

    """
    _files = files
    for _file in _files:
        #  alembic cache file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _backup_file = os.path.join(dst, _extend_file)
        #  upload alembic cache file
        _result = filefunc.publish_file(_file, _backup_file)

def local_file(files, src, dst):
    """ local download files 

    """
    _files = files
    for _file in _files:
        #  backup texture file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _local_file = os.path.join(dst, _extend_file)
        #  downlocal texture file
        #_result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_dir = os.path.dirname(_local_file)
        if not os.path.isdir(_local_dir):
            os.makedirs(_local_dir)
        _result = shutil.copy(_file, _local_file)

def change_node_path(nodes, src, dst):
    """ change file nodes path

    """
    _file_nodes = nodes
    for _file_node in _file_nodes:
        # change reference file 
        _ori_file_texture_path = cmds.referenceQuery(_file_node, f = True, wcn = True)
        _file_texture_path = _ori_file_texture_path
        _extend_file = _file_texture_path.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _new_file_text_path = "%s/%s"%(dst, _extend_file)
        #while True:
            #cmds.setAttr("{}.abc_File".format(_file_node), _new_file_text_path, type = 'string')
            #if cmds.getAttr("{}.abc_File".format(_file_node)) == _new_file_text_path:
            #    break
        cmds.file(_new_file_text_path, loadReference = _file_node, options = "v=0;")

def nodes(is_local = True):
    """ 获取reference节点

    :rtype: list
    """
    # _file_nodes = list(set(cmds.ls(type = "reference")) - set(["sharedReferenceNode", "_UNKNOWN_REF_NODE_"])) 
    _file_nodes = cmds.ls(rf = True)
    _result_nodes = []
    for _file_node in _file_nodes:
        try:
            if cmds.referenceQuery(_file_node, p = True, rfn = True):
                continue
            _has_attr = cmds.objExists("{}.is_local".format(_file_node))
            if not _has_attr:
                continue
            _is_local = cmds.getAttr("{}.is_local".format(_file_node))
            if _is_local == "false" and is_local:
                continue
            _result_nodes.append(_file_node)
        except:
            pass
    return _result_nodes

def files():
    """get reference file
    
    :rtype: list
    """
    _nodes = nodes()
    files = []
    for _file_node in _nodes:
        # get reference file
        _file_name = cmds.referenceQuery(_file_node, f = True, wcn = True)
        files.append(_file_name)
    return files

def paths(files):
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
        for i in set_list:
            _com = _frist & i
            if not _com:
                _left_list.append(i)
                continue
            value[len(value)-1] = _com
        if _left_list:
            _set(_left_list, value)

    _set_list = _get_file_set_list(files)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value


def import_all_references(except_namespaces = []):
    """ 导入所有reference文件
    """
    done = False
    while (done == False or (len(pm.listReferences()) != 0)):
        refs = pm.listReferences()
        #get rel refs
        pro = []
        if except_namespaces:
            for ref in refs:
                if ref.namespace not in except_namespaces:
                    #refs.remove(ref)
                    pro.append(ref)
        if pro:
            refs = pro
        sn = len(refs)
        en = 0
        for ref in refs:
            if ref.isLoaded():
                done = False
                ref.importContents()
            else:
                en += 1
                done = True
        if sn == en:
            return True
    return True


def remove_all_namespaces():
    allNameSpace = cmds.namespaceInfo(":", recurse = True, listOnlyNamespaces = True, absoluteName = True)
    for whole_ns in allNameSpace :
        if whole_ns != ":UI" and whole_ns != ":shared":
            ns = whole_ns.split(':')[-1]
            try :
                pm.namespace(mv=[ns,':'],f=1)
                if ns in pm.namespaceInfo(lon=1):
                    pm.namespace(rm=ns)
                    logger.info('namespace "{}" removed succeed'.format(ns))
            except Exception as e:
                logger.warning('namespace "{}" removed error'.format(ns))