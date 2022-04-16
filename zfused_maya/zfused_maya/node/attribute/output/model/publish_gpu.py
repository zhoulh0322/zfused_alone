# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import sys
import logging

import maya.cmds as cmds

import zfused_api

from zcore import zfile,transfer,filefunc

from zfused_maya.node.core import shadingengine,reducemesh,renderinggroup

__all__ = ["publish_gpu"]

logger = logging.getLogger(__name__)

# load abc plugin
_is_load = cmds.pluginInfo("AbcExport", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load alembic plugin")
        cmds.loadPlugin("AbcExport")
    except Exception as e:
        logger.error(e)
        # sys.exit()
        
def publish_gpu(*args, **kwargs):
    """ 上传模型abc文件
        args: entity_type, entity_id, attr_id
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

    _file_name = "{}.{}".format(_file_code, _file_index)
        
    _engines = shadingengine.get_shading_engines()
    try:
        _write_materials = True

        _project = _task.project()
        _no_shading_color = _project.variables("no_shading_color")
        if not _no_shading_color:
            _write_materials = False

            # change shading color
            for _index, _engine in enumerate(_engines):
                _color = shadingengine.get_node_shading_color(_engine)
                # 可能会出问题
                if _color:
                    shadingengine.set_node_shading_color(_engine, _color)
            shadingengine.switch_color_shader(_engines)
        
        # get rendering group
        _is_rendering = renderinggroup.nodes()
        _rendering_groups = " ".join(_is_rendering)   

        _alembic_nodes = cmds.ls(type = "AlembicNode")
        if _alembic_nodes:
            _start_time = cmds.playbackOptions(q = True, min = True)
            _end_time = cmds.playbackOptions(q = True, max = True)
            cmds.gpuCache(_rendering_groups, useBaseTessellation = True, startTime = _start_time, endTime = _end_time, writeMaterials = _write_materials, dataFormat='ogawa', directory = _publish_file_dir, fileName = _file_name) #allDagObjects = True)
        else:
            # will reduce mesh
            # get gpu reduce percentage
            _reduce_percentage = _task.project_entity().xattr("gpu_reduce_percentage")
            if _reduce_percentage == "100":
                cmds.gpuCache(_rendering_groups, useBaseTessellation = True, startTime = 1, endTime = 1, writeMaterials = _write_materials, dataFormat='ogawa', directory = _publish_file_dir, fileName = _file_name) #allDagObjects = True)
            else:
                reducemesh.reduce_mesh(float(_reduce_percentage), _publish_file_dir, _file_name)
            
    except Exception as e:
        logger.error(e)
        return False

    # finally:
    #     shadingengine.switch_orignail_shader()
 
    # publish file
    _result = filefunc.publish_file(_publish_file, _production_file)
    _result = filefunc.publish_file(_publish_file, _cover_file)
    
    # record in file
    _file_info = zfile.get_file_info(_publish_file, _production_file)
    _cover_file_info = zfile.get_file_info(_publish_file, _cover_file)
    zfused_api.task.new_production_file([_file_info, _cover_file_info], _task_id, _output_attr_id, int(_file_index) )

    return True