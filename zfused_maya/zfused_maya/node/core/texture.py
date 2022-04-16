# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 贴图文件操作集合 """

import os
import glob
import re
import logging
import shutil
import hashlib
import uuid

import maya.cmds as cmds

from zcore import transfer,zfile

from zcore import filefunc

from zwidgets.widgets import progress

logger = logging.getLogger(__file__)


# TEXT_NODE = ["file", "imagePlane", "RedshiftNormalMap","RedshiftCameraMap",'RedshiftSprite','RedshiftEnvironment', 'RedshiftLensDistortion', 'RedshiftDomeLight', 'RedshiftIESLight', 'RedshiftLightGobo']
TEXT_NODE = ["file","movie"]

TEXTURE_ATTR_DICT = {
    "file" : "fileTextureName",
    "movie" : "fileTextureName",
    "imagePlane": "imageName",
    "RedshiftNormalMap":"tex0",
    "RedshiftCameraMap":"tex0",
    "RedshiftSprite":"tex0",
    "RedshiftEnvironment":"tex0",
    "RedshiftLensDistortion":"tex0",
    "RedshiftDomeLight":"tex0",
    "RedshiftIESLight":"tex0",
    "RedshiftLightGobo":"tex0"
}

# REMOVE_NODES = ["audio", "assemblyDefinition", "assemblyReference" ]

TEX_SUFFIX = ['.als',
              '.avi',
              '.bmp',
              '.cin',
              '.dds',
              '.eps',
              '.exr',
              '.gif',
              '.iff',
              '.jpeg',
              '.jpg',
              '.pic',
              '.pict',
              '.png',
              '.pntg',
              '.psd',
              '.qt',
              '.qtif',
              '.rla',
              '.sgi',
              '.svg',
              '.swf',
              '.swft',
              '.tga',
              '.tif',
              '.tiff',
              '.hdr',
              '.yuv']


# def convert_path(path):
#     return path.replace(os.sep, "/")
def convert_path(path):
    return path.replace(r'\/'.replace(os.sep, ''), os.sep)


# 计算文件md5值
def md5_for_file(f, block_size=2**20):
    with open(f, 'rb') as fHandle:
        md5 = hashlib.md5()
        while True:
            data = fHandle.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    return md5.hexdigest()

def _copy_file(src, dst):
    if os.path.isfile(dst):
        # get md5
        _src_md5 = md5_for_file(src)
        _dst_md5 = md5_for_file(dst)
        if _src_md5 == _dst_md5:
            return True
    return shutil.copy(src, dst)

# @progress.progress(u"上传贴图")
def publish_file(files, src, dst):
    _file_infos = []
    _texture_files = files

    
    progress.set_sub_range(0, len(files))

    for _index, _texture_file in enumerate(_texture_files):
        
        progress.set_sub_label_text(u"{}/{} - {}".format(_index, len(files), os.path.basename(_texture_file)))
        progress.set_sub_value(_index+1)
        
        #  backup texture file
        _extend_file = os.path.basename(_texture_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _backup_texture_file = "{}/{}".format(dst, _extend_file)
        #  upload texture file
        # logger.info(u"upload file {} to {}".format(_texture_file, _backup_texture_file))
        
        _result = filefunc.publish_file(_texture_file, _backup_texture_file)
        # transfer.send_file_to_server(_texture_file, _backup_texture_file)

        # 记录贴图数据
        _file_info = zfile.get_file_info(_texture_file, _backup_texture_file)
        _file_infos.append(_file_info)

        #  if has .tx file and will upload
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = u"{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            # _extend_file = _tx_texture_file.split(src)[-1]
            _extend_file = os.path.basename(_tx_texture_file)
            while _extend_file.startswith("/"):
                _extend_file = _extend_file[1:]
            _backup_tx_texture_file = "{}/{}".format(dst, _extend_file)
            #  upload tx file
            _result = filefunc.publish_file(_tx_texture_file, _backup_tx_texture_file)
            # transfer.send_file_to_server(_tx_texture_file, _backup_tx_texture_file)

    return _file_infos

def __publish_file(files, src, dst):
    """ upload files 
    """
    _texture_files = files
    #if _texture_files:
    #    _path_set = texture.paths(_texture_files)[0]
    #    _intersection_path = max(_path_set)
    for _texture_file in _texture_files:
        #  backup texture file
        _extend_file = _texture_file.split(src)[-1]
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _backup_texture_file = "{}/{}".format(dst, _extend_file)
        #  upload texture file
        # logger.info(u"upload file {} to {}".format(_texture_file, _backup_texture_file))
        _result = filefunc.publish_file(_texture_file, _backup_texture_file)
        #  if has .tx file and will upload
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = u"{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            _extend_file = _tx_texture_file.split(src)[-1]
            while _extend_file.startswith("/"):
                _extend_file = _extend_file[1:]
            _backup_tx_texture_file = "{}/{}".format(dst, _extend_file)
            #  upload tx file
            _result = filefunc.publish_file(_tx_texture_file, _backup_tx_texture_file)


# @progress.progress(u"下载贴图")
def local_file(files, src, dst):
    """ local download files 
    """

    progress.set_sub_range(0, len(files))

    _texture_files = files

    for _index, _texture_file in enumerate(_texture_files):

        progress.set_sub_label_text(u"{}/{} - {}".format(_index, len(files), os.path.basename(_texture_file)))
        progress.set_sub_value(_index+1)

        if not os.path.isfile(_texture_file):
            continue
        #  backup texture file
        _extend_file = os.path.basename(_texture_file)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _local_texture_file = "{}/{}".format(dst, _extend_file)
        #  downlocal texture file
        _local_texture_dir = os.path.dirname(_local_texture_file)
        if not os.path.isdir(_local_texture_dir):
            os.makedirs(_local_texture_dir)
        _result = _copy_file(_texture_file, _local_texture_file)
        #  if has .tx file and will local download
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = "{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            # _extend_file = _tx_texture_file.split(src)[-1]
            _extend_file = os.path.basename(_tx_texture_file)
            while _extend_file.startswith("/"):
                _extend_file = _extend_file[1:]
            _local_tx_texture_file = "{}/{}".format(dst, _extend_file)
            #  download tx file
            #_result = filefunc.publish_file(_tx_texture_file, _local_tx_texture_file)
            _local_tx_texture_dir = os.path.dirname(_local_tx_texture_file)
            if not os.path.dirname(_local_tx_texture_dir):
                os.makedirs(_local_tx_texture_dir)
            _result = _copy_file(_tx_texture_file, _local_tx_texture_file)

def __local_file(files, src, dst):
    """ local download files 
    """
    _texture_files = files
    #if _texture_files:
    #    _path_set = texture.paths(_texture_files)[0]
    #    _intersection_path = max(_path_set)
    for _texture_file in _texture_files:
        #  backup texture file
        _extend_file = _texture_file.split(src)[-1]
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _local_texture_file = "{}/{}".format(dst, _extend_file)
        #  downlocal texture file
        #_result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_texture_dir = os.path.dirname(_local_texture_file)
        if not os.path.isdir(_local_texture_dir):
            os.makedirs(_local_texture_dir)
        _result = _copy_file(_texture_file, _local_texture_file)
        #  if has .tx file and will local download
        _except_suffix, _ = os.path.splitext(_texture_file)
        _tx_texture_file = "{}.tx".format(_except_suffix)
        if os.path.isfile(_tx_texture_file):
            _extend_file = _tx_texture_file.split(src)[-1]
            while _extend_file.startswith("/"):
                _extend_file = _extend_file[1:]
            _local_tx_texture_file = "{}/{}".format(dst, _extend_file)
            #  download tx file
            #_result = filefunc.publish_file(_tx_texture_file, _local_tx_texture_file)
            _local_tx_texture_dir = os.path.dirname(_local_tx_texture_file)
            if not os.path.dirname(_local_tx_texture_dir):
                os.makedirs(_local_tx_texture_dir)
            _result = _copy_file(_tx_texture_file, _local_tx_texture_file)

def change_node_path(nodes, src, dst):
    """ change file nodes path
    """
    _file_nodes = nodes
    #if _file_nodes:
    for _file_node_attr in _file_nodes:
        _file_node = _file_node_attr.split(".")[0]
        _type = cmds.nodeType(_file_node)
        _ori_file_texture_path = _get_file_full_name(_file_node_attr)
        _file_texture_path = _ori_file_texture_path

        # _extend_file = _file_texture_path.split(src)[-1]
        _extend_file = os.path.basename(_file_texture_path)
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _new_file_text_path = "%s/%s"%( dst, _extend_file )
        # 锁定节点色彩空间，防止替换贴图时色彩空间设置丢失
        if _type == "file" and not cmds.getAttr("{}.ignoreColorSpaceFileRules".format(_file_node)):
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
        while True:
            cmds.setAttr(_file_node_attr, _new_file_text_path, type = 'string')
            if convert_path(_get_file_full_name(_file_node_attr)) == convert_path(_new_file_text_path):
                break
        # 取消色彩空间锁定(Raw除外)
        if _type == "file":
            _colorSpace = cmds.getAttr('%s.colorSpace'%_file_node)
            if _colorSpace == 'Raw':
                cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
            else:
                cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 0)


def __change_node_path(nodes, src, dst):
    """ change file nodes path

    """
    _file_nodes = nodes
    #if _file_nodes:
    for _file_node_attr in _file_nodes:
        _file_node = _file_node_attr.split(".")[0]
        _type = cmds.nodeType(_file_node)
        _ori_file_texture_path = _get_file_full_name(_file_node_attr)
        _file_texture_path = _ori_file_texture_path

        _extend_file = _file_texture_path.split(src)[-1]
        while _extend_file.startswith("/"):
            _extend_file = _extend_file[1:]
        _new_file_text_path = "%s/%s"%( dst, _extend_file )
        # 锁定节点色彩空间，防止替换贴图时色彩空间设置丢失
        # print(_new_file_text_path)
        if _type == "file" and not cmds.getAttr("{}.ignoreColorSpaceFileRules".format(_file_node)):
            cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
        while True:
            cmds.setAttr(_file_node_attr, _new_file_text_path, type = 'string')
            if convert_path(_get_file_full_name(_file_node_attr)) == convert_path(_new_file_text_path):
                break
        # 取消色彩空间锁定(Raw除外)
        if _type == "file":
            _colorSpace = cmds.getAttr('%s.colorSpace'%_file_node)
            if _colorSpace == 'Raw':
                cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 1)
            else:
                cmds.setAttr("{}.ignoreColorSpaceFileRules".format(_file_node), 0)

def error_nodes():
    """get error file node
       判断 file 节点是否错误,填入错误贴图地址
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [ _file_dir_name, _file_suffix ]

    _error_nodes = []

    _file_nodes = cmds.ls( type = TEXT_NODE )
    for _file_node in _file_nodes:

        _type = cmds.nodeType(_file_node)
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        if _is_reference:
            continue

        # print(_file_node)
        _files = get_file_node_files(_file_node)
        if not _files:
            _error_nodes.append(_file_node)
        # print(_files)
        for _file in _files:
            if not os.path.isfile(_file):
                _error_nodes.append(_file_node)
                break

        # _file_name = _get_file_full_name("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]))
        # _node_dir_name = os.path.dirname(_file_name)
        # _, _node_suffix = os.path.splitext(_file_name)
        # _is_error = True
        # for _file in _all_files:
        #     _file_dir_name,_file_suffix = _all_files_dict[_file]
        #     if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
        #         _is_error = False
        # if _is_error:
        #     _error_nodes.append(_file_node)

    return _error_nodes

# def nodes():
    """ 获取file节点

    :rtype: list
    """
    # _file_nodes = cmds.ls(type = TEXT_NODE)
    # _result_nodes = []
    # for _file_node in _file_nodes:
    #     _type = cmds.nodeType(_file_node)
    #     _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
    #     _is_lock = cmds.getAttr("{}.{}".format(_file_node,TEXTURE_ATTR_DICT[_type]), l = True)
    #     if _is_reference and _is_lock:
    #         continue
    #     _result_nodes.append(_file_node)
    # return _result_nodes

def nodes(withAttribute = True, ignoreReference = True):
    """ 获取file节点
    :rtype: list
    """
    _list = []
    cmds.filePathEditor(rf = 1)
    item = cmds.filePathEditor(query=True, listFiles="", unresolved=False, withAttribute=True)
    if item:
        files = item[0::2]
        nodes = item[1::2]
        for _file,_node_attr in zip(files,nodes):
            _node = _node_attr.split(".")[0]
            if os.path.splitext(_file)[-1].lower() in TEX_SUFFIX:
                _is_reference = cmds.referenceQuery(_node, isNodeReferenced = True)

                if _is_reference and ignoreReference:
                    continue

                if withAttribute:
                    _list.append(_node_attr)
                else:
                    _list.append(_node)
    return _list


def get_node_files(ignoreReference = True):
    pass


def files(ignoreReference = True):
    _texture_files = []
    _nodes = nodes(True,ignoreReference)
    if _nodes:
        for _node_attr in _nodes:
            _node = _node_attr.split(".")[0]
            _path = _get_file_full_name(_node_attr)
            _is_reference = cmds.referenceQuery(_node, isNodeReferenced = True)
            if _is_reference and ignoreReference:
                continue

            _mode,_ani = 0,0
            if cmds.objExists("%s.uvTilingMode"%_node):
                _mode = cmds.getAttr("%s.uvTilingMode"%_node)
            if cmds.objExists("%s.useFrameExtension"%_node):
                _ani = cmds.getAttr("%s.useFrameExtension"%_node)
            if "<UDIM>" in os.path.basename(_path):
                _mode = 1
            if not _mode and not _ani:
                _texture_files.append(_path)
            else:
                if _mode:
                    _texture_files.extend(get_udim_texfile(_path,False))
                if _ani:
                    _texture_files.extend(get_frame_texfile(_path,False))

    return list(set(_texture_files))


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
    # for _set_ in _set_list:
    #     print(_set_)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value


def get_udim_texfile(filepath,boolean = True):
    '''get udim file
    '''
    filelist = []
    _path,_name = os.path.split(filepath)
    if os.path.exists(_path):
        _str,_suffix = os.path.splitext(_name)
        if "<UDIM>" in _str:
            _ele = _str.split("<UDIM>")
            _check_str = "\d{4}".join(_ele)
            for _i in os.listdir(_path):
                if re.search(r"{}{}".format(_check_str,_suffix),_i):
                    filelist.append("{}/{}".format(_path,_i))
        else:
            _udim = re.findall("\d{4}",_str)
            if _udim:
                ele = _str.split(_udim[-1])
                _check_str = _udim[-1].join(ele[:-1])
                for _j in os.listdir(_path):
                    if re.search(r"%s\d{4}%s"%(_check_str,_suffix),_j):
                        filelist.append("{}/{}".format(_path,_j))
    if filelist:
        if boolean:
            return True
        else:
            return filelist
    else:
        if boolean:
            return False
        else:
            return [filepath]

def get_frame_texfile(filepath,boolean = True):
    '''get frame file
    '''
    filelist = []
    _path,_name = os.path.split(filepath)
    if os.path.exists(_path):
        _str,_suffix = os.path.splitext(_name)
        if "<f>" in _str:
            _ele = _str.split("<f>")
            _check_str = "\d+".join(_ele)
            for _i in os.listdir(_path):
                if re.search("{}{}".format(_check_str,_suffix),_i):
                    filelist.append(r"{}/{}".format(_path,_i))
        else:
            _f = re.findall("\d+",_str)
            if _f:
                ele = _str.split(_f[-1])
                _check_str = _f[-1].join(ele[:-1])
                for _j in os.listdir(_path):
                    if re.search(r"%s\d+%s"%(_check_str,_suffix),_j):
                        filelist.append("{}/{}".format(_path,_j))
    if filelist:
        if boolean:
            return True
        else:
            return filelist
    else:
        if boolean:
            return False
        else:
            return [filepath]

# def _get_file_full_name(file_node):
#     cmds.filePathEditor(rf = 1)
#     _dirs = cmds.filePathEditor(q = True,  ld = "")
#     if not _dirs:
#         return cmds.getAttr(file_node)
#     _dir_dict = {}
#     for _dir in _dirs:
#         _file_attr = cmds.filePathEditor(q = True,  ld = _dir, lf = _dir, unresolved=False, withAttribute=True)
#         for _index, _attr in enumerate(_file_attr[1::2]):
#             if file_node == _attr:
#                 _full_name = u"{}/{}".format(_dir, _file_attr[_index*2])
#                 return _full_name

def _get_file_full_name(file_node):
    _path = cmds.getAttr(file_node)
    if "" not  in os.path.splitdrive(_path):
        return _path
    workpath = cmds.workspace(q = 1,fn = 1)
    return r"{}/{}".format(workpath,_path)





# -------------------------------------------------------------------------------
# copy https://gist.github.com/BigRoy/d027323b27bf9de8f92a7c2ea972122a



def get_file_node_files(node):
    """Return the file paths related to the file node
    Note:
        Will only return existing files. Returns an empty list
        if not valid existing files are linked.
    Returns:
        list: List of full file paths.
    """

def seq_to_glob(path):
    """Takes an image sequence path and returns it in glob format,
    with the frame number replaced by a '*'.
    Image sequences may be numerical sequences, e.g. /path/to/file.1001.exr
    will return as /path/to/file.*.exr.
    Image sequences may also use tokens to denote sequences, e.g.
    /path/to/texture.<UDIM>.tif will return as /path/to/texture.*.tif.
    Args:
        path (str): the image sequence path
    Returns:
        str: Return glob string that matches the filename pattern.
    """

    if path is None:
        return path

    # If any of the patterns, convert the pattern
    patterns = {
        "<udim>": "<udim>",
        "<tile>": "<tile>",
        "<uvtile>": "<uvtile>",
        "#": "#",
        "u<u>_v<v>": "<u>|<v>",
        "<frame0": "<frame0\d+>",
        "<f>": "<f>"
    }

    lower = path.lower()
    has_pattern = False
    for pattern, regex_pattern in patterns.items():
        if pattern in lower:
            path = re.sub(regex_pattern, "*", path, flags=re.IGNORECASE)
            has_pattern = True

    if has_pattern:
        return path

    base = os.path.basename(path)
    matches = list(re.finditer(r'\d+', base))
    if matches:
        match = matches[-1]
        new_base = '{0}*{1}'.format(base[:match.start()],
                                    base[match.end():])
        head = os.path.dirname(path)
        return os.path.join(head, new_base)
    else:
        return path


def get_file_node_path(node):
    """Get the file path used by a Maya file node.
    Args:
        node (str): Name of the Maya file node
    Returns:
        str: the file path in use
    """
    # if the path appears to be sequence, use computedFileTextureNamePattern,
    # this preserves the <> tag
    if cmds.attributeQuery('computedFileTextureNamePattern', node=node, exists=True):
        texture_pattern = cmds.getAttr('{0}.computedFileTextureNamePattern'.format(node))

        patterns = ["<udim>", "<tile>", "u<u>_v<v>", "<f>", "<frame0", "<uvtile>"]
        lower = texture_pattern.lower()
        if any(pattern in lower for pattern in patterns):
            return texture_pattern

    # otherwise use fileTextureName
    return cmds.getAttr('{0}.fileTextureName'.format(node))


def get_file_node_files(node):
    """Return the file paths related to the file node
    Note:
        Will only return existing files. Returns an empty list
        if not valid existing files are linked.
    Returns:
        list: List of full file paths.
    """

    path = get_file_node_path(node)
    path = cmds.workspace(expandName=path)
    if node_uses_image_sequence(node):
        glob_pattern = seq_to_glob(path)
        return glob.glob(glob_pattern)
    elif os.path.exists(path):
        return [path]
    else:
        return []


def node_uses_image_sequence(node):
    """Return whether file node uses an image sequence or single image.
    Determine if a node uses an image sequence or just a single image,
    not always obvious from its file path alone.
    Args:
        node (str): Name of the Maya node
    Returns:
        bool: True if node uses an image sequence
    """

    # useFrameExtension indicates an explicit image sequence
    node_path = get_file_node_path(node).lower()

    # The following tokens imply a sequence
    patterns = ["<udim>", "<tile>", "<uvtile>", "u<u>_v<v>", "<frame0"]

    return (cmds.getAttr('%s.useFrameExtension' % node) == True or
            any(pattern in node_path for pattern in patterns))
