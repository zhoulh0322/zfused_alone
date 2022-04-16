# coding:utf-8
# --author-- binglu.wang

""" yeti缓存操作集合 """

import os
import logging
import shutil
import maya.cmds as cmds

import zfused_api
from zcore import filefunc

logger = logging.getLogger(__file__)

def nodes():
    '''get pgYteiMaya nodes
    
    '''
    return cmds.ls(type = "pgYetiMaya")

def publish_file(src, dst):
    """ upload files 

    """
    _files = os.listdir(src)
    for _file in _files:
        _srcfile = "{}/{}".format(src,_file)
        _dstfile = "{}/{}".format(dst,_file)
        logger.info("upload file {} to {}".format(_srcfile, _dstfile))
        _result = filefunc.publish_file(_srcfile, _dstfile)

def create_cache(yetiNode,path,startFrame,endFrame,frameSample):
    """ create yeticache 

    """
    if not os.path.isdir(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])
    cmds.pgYetiCommand(yetiNode,writeCache = path,range = [startFrame, endFrame], samples = frameSample,updateViewport = 0, generatePreview = 0)

def get_upload_info(nodes,frameLevel,temp_path,local_path,childfolder = True):
    """ get yeti info

    """
    _json_info = []
    _local_info = {}
    assetlist = get_asset_list()
    for node in nodes:
        try:
            _nsname = cmds.referenceQuery(node,ns = 1)
            if _nsname.startwith(":"):
                _nsname = _nsname[1:]
        except:
            _nsname = node[:-len(node.split(":")[-1])-1]
        cachename = node[len(_nsname)+1:]
        if _nsname in assetlist:
            _assetname = assetlist[_nsname]
            # 短空间名
            short_ns = _nsname.split(":")[-1]
            if childfolder:
                _webpath ="{}/{}/{}/{}.%0{}d.fur".format(temp_path,short_ns,cachename,cachename,frameLevel)
                _localpath ="{}/{}/{}/{}.%0{}d.fur".format(local_path,short_ns,cachename,cachename,frameLevel)
            else:
                _webpath ="{}/{}/{}.%0{}d.fur".format(temp_path,short_ns,cachename,frameLevel)
                _localpath ="{}/{}/{}.%0{}d.fur".format(local_path,short_ns,cachename,frameLevel)
            if not os.path.isdir(os.path.split(_localpath)[0]):
                os.makedirs(os.path.split(_localpath)[0])
            tempinfo = []
            tempinfo.append(_assetname) # assetname
            tempinfo.append(short_ns) # namespacename
            tempinfo.append(node.split("{}:".format(_nsname))[-1]) # nodename
            tempinfo.append(_webpath) # cachepath
            _json_info.append(tempinfo)
            _local_info[node] = [_localpath,_webpath]
        else:
            logger.info("worng asset :{}".format(_nsname))
            continue
    return _json_info,_local_info

def get_asset_list():
    _dict = {}
    import zfused_maya.node.core.element as element
    _elements = element.scene_elements()
    for _element in _elements:
        _link_handle = zfused_api.objects.Objects(_element["link_object"], _element["link_id"])
        if _element["relation_ship"] == "reference":
            _dict[_element["namespace"]] = _link_handle.code()
    return _dict

def import_cache(path,texfile):
    '''导入缓存
    '''
    cmds.setAttr("{}.fileMode".format(texfile),1)
    cmds.setAttr("{}.cacheFileName".format(texfile),path,type = "string")

def arrange_info(info,_dict = {}):
    '''整理json信息
    '''
    for _i in info:
        _asset,_ns,_node,_path = _i
        if _asset not in _dict:
            _dict[_asset] = {}
        if _ns not in _dict[_asset]:
            _dict[_asset][_ns] = []
        _dict[_asset][_ns].append(_node)
        _dict[_asset][_ns].append(_path)
    return _dict

if __name__ == '__main__':
    get_cache_info()
