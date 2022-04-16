# -*- coding: UTF-8 -*-
'''
@Time    : 2022/1/19 18:01
@Author  : Jerris_Cheng
@File    : publish_ass.py
'''
from __future__ import print_function

import os
import logging
import sys
import zfused_api
import maya.cmds as cmds
from zcore import filefunc,zfile

from zfused_maya.node.core import ass,renderinggroup,texture

__all__ = ["publish_ass"]

logger = logging.getLogger(__name__)

_is_load = cmds.pluginInfo("mtoa", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load mtoa plugin")
        cmds.loadPlugin("mtoa")
    except Exception as e:
        logger.error(e)
        sys.exit()

def publish_ass(*args,**kwargs):
    """
    模型阶段发布ass代理
    :param args:
    :param kwargs:
    :return:
    """
    #_task_id, _output_attr_id = args
    _task_id, _output_attr_id = args

    _output_attr_handle = zfused_api.attr.Output(_output_attr_id)
    _file_format = _output_attr_handle.format()
    _suffix = _output_attr_handle.suffix()
    _attr_code = _output_attr_handle.code()
    _task = zfused_api.task.Task(_task_id)
    _production_path = _task.production_path()
    _project_entity_production_path = _task.project_entity().production_path()
    _temp_path = _task.temp_path()
    _file_code = _task.file_code()
    if kwargs.get("fix_version"):
        _file_index = "{:0>4d}".format(_task.last_version_index( 0 ))
    else:
        _file_index = "{:0>4d}".format(_task.last_version_index() + 1)

    _production_file = "{}/{}/{}.{}{}".format( _production_path, _attr_code, _file_code, _file_index, _suffix )
    _cover_file = "{}/{}/{}{}".format(_production_path, _attr_code, _file_code, _suffix)
    _publish_file = "{}/{}/{}.{}{}".format( _temp_path, _attr_code, _file_code, _file_index, _suffix )
    _publish_file_dir = os.path.dirname(_publish_file)
    if not os.path.isdir(_publish_file_dir):
        os.makedirs(_publish_file_dir)
    _rendering_group = renderinggroup.nodes()
    try:
        # publish texture
        _texture_infos = []
        # _texture_files = texture.files()
        # if _texture_files:
        #     _path_set = texture.paths(_texture_files)[0]
        #     _intersection_path = max(_path_set)
        #     _texture_infos = texture.publish_file(_texture_files, _intersection_path, _project_entity_production_path + "/texture/production")

        if _rendering_group:
            ass.publish_ass(_rendering_group,_publish_file)
            _result = filefunc.publish_file(_publish_file,_production_file)
            _result = filefunc.publish_file(_publish_file,_cover_file)

            # record production file
            _file_info = zfile.get_file_info(_publish_file, _production_file)
            _cover_file_info = zfile.get_file_info(_publish_file, _cover_file)
            zfused_api.task.new_production_file([_file_info, _cover_file_info] + _texture_infos, _task_id, _output_attr_id, int(_file_index) )
            #zfused_api.task.new_production_file([_file_info, _cover_file_info], _task_id, _output_attr_id, int(_file_index) )

    except Exception as e:
        logger.error(e)
        print(e)
        return False
    return True