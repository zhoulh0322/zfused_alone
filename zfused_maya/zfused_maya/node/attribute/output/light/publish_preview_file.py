# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api

from zcore import zfile,transfer,filefunc

from zfused_maya.node.core import texture, xgen, alembiccache


__all__ = ["publish_file"]

logger = logging.getLogger(__name__)


def publish_preview_file(*args, **kwargs):
    """ 上传任务模型文件
    """
    
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
    
    # _xgen_list = xgen.xgenfile()
    # if _xgen_list:
    #     xgen.publishxgen()
    
    try:
        # save publish file
        cmds.file(rename = _publish_file)
        cmds.file(save = True, type = _file_format, f = True, options = "v=0;")

        # _xgen_list = xgen.xgenfile()
        # if _xgen_list:
        #     xgen.publishxgen()

        # # 暂时取消 后面通过检测判定错误 不直接修复问题
        # # fix camera aspect ratio
        # _cameras = cmds.ls("{}*".format(_file_code), type="camera")
        # if _cameras:
        #     for _camera in _cameras:
        #         # get
        #         if cmds.getAttr("{}.filmFit".format(_camera)) == 3:
        #             _v_f = cmds.getAttr("{}.verticalFilmAperture".format(_camera))
        #             cmds.setAttr("{}.horizontalFilmAperture".format(_camera), _v_f * 2.503)

        # publish texture
        _texture_infos = []
        _texture_files = texture.files()
        if _texture_files:
            _path_set = texture.paths(_texture_files)[0]
            _intersection_path = max(_path_set)
            _texture_infos = texture.publish_file(_texture_files, _intersection_path, _project_entity_production_path + "/texture/preview")
            # change maya texture node path
            _file_nodes = texture.nodes()
            if _file_nodes:
                texture.change_node_path(_file_nodes, _intersection_path, _project_entity_production_path + "/texture/preview")
        
        # publish alembic 
        _alembic_files = alembiccache.files()
        if _alembic_files:
            _path_set = alembiccache.paths(_alembic_files)[0]
            _intersection_path = max(_path_set)
            alembiccache.publish_file(_alembic_files, _intersection_path, _production_path + "/cache/alembic")
            _file_nodes = alembiccache.nodes()
            if _file_nodes:
                alembiccache.change_node_path(_file_nodes, _intersection_path, _production_path + "/cache/alembic")
        
        # save publish file
        cmds.file(save = True, type = _file_format, f = True, options = "v=0;")
        
        # publish file
        _result = filefunc.publish_file(_publish_file, _production_file)
        _result = filefunc.publish_file(_publish_file, _cover_file)
        
        # link files
        zfused_api.files.new_file("task", _task_id, _production_file, int(_file_index))
        zfused_api.files.new_file("task", _task_id, _cover_file, int(_file_index))

        # production file
        _file_info = zfile.get_file_info(_publish_file, _production_file)
        _cover_file_info = zfile.get_file_info(_publish_file, _cover_file)
        zfused_api.task.new_production_file([_file_info, _cover_file_info], _task_id, _output_attr_id, int(_file_index) )

        # if _xgen_list:
        #     for _xgen_node in _xgen_list:

        #         _xgen_name = xgen._getxgenfilename(_xgen_node)
        #         _xgen_path = xgen._getxgenfile(_xgen_node)
        #         _cover_xgen_file = "{}/{}/{}/{}/{}".format(_production_path, _step_code, _software_code, _attr_code,
        #                                                    _xgen_name)
        #         _backup_xgenfile = "{}/{}".format(_backup_path, _xgen_name)
        #         if os.path.exists(_xgen_path):
        #             filefunc.publish_file(_xgen_path, _cover_xgen_file)
        #             filefunc.publish_file(_xgen_path, _backup_xgenfile)

    except Exception as e:
        logger.error(e)
        return False

    return True