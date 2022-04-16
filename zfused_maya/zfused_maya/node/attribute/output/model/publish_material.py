# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api

from zcore import zfile,transfer,filefunc

import zfused_maya.node.core.texture as texture
import zfused_maya.node.core.material as material
import zfused_maya.node.core.fixmeshname as fixmeshname
import zfused_maya.node.core.renderinggroup as renderinggroup

__all__ = ["publish_material"]

logger = logging.getLogger(__name__)

def publish_material(*args, **kwargs):
    """ 上传任务模型文件
        args: output_entity_type, output_entity_id, output_attr_id
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
    try:
        # # save publish file
        # cmds.file(rename = _publish_file)
        # cmds.file(save = True, type = _file_format, f = True, options = "v=0;")
        
        # # fix mesh name
        # _is_rendering = renderinggroup.nodes()
        # fixmeshname.fix_mesh_name("_rendering", _is_rendering)
        
        # # recore material
        # material.record()

        # get all material
        _meshs = _get_rendering_mesh()
        if not _meshs:
            return
        # 对大量模型操作时会卡死，弃用
        # cmds.select(_meshs, replace = True)
        # cmds.hyperShade(shaderNetworksSelectMaterialNodes = True)
        _sgs = cmds.listConnections(_meshs,d = 1,type = "shadingEngine")
        # _mat = [cmds.listConnections("{}.surfaceShader".format(i),d = 1)[0] for i in set(_sgs)]
        # cmds.select(_mat,r =1)
        cmds.select(cl = True)
        cmds.select(_sgs, r = True, ne = True)
        cmds.file(_publish_file, op = "v=0;", type = _file_format, pr = True, es = True, f = True)
        
        
        # publish file
        _result = filefunc.publish_file(_publish_file, _production_file)
        _result = filefunc.publish_file(_publish_file, _cover_file)
        
        # # link files
        # zfused_api.files.new_file("task", _task_id, _production_file, int(_file_index))
        # zfused_api.files.new_file("task", _task_id, _cover_file, int(_file_index))
        
        # record production file
        _file_info = zfile.get_file_info(_publish_file, _production_file)
        _cover_file_info = zfile.get_file_info(_publish_file, _cover_file)
        zfused_api.task.new_production_file([_file_info, _cover_file_info], _task_id, _output_attr_id, int(_file_index) )

    except Exception as e:
        logger.error(e)
        return False

    return True


def _get_rendering_mesh():
    mesh = []
    rendering = []
    allDags = cmds.ls(dag = True)
    for dag in allDags:
        dag
        #get 
        if cmds.objExists("%s.rendering"%dag):
            value = cmds.getAttr("%s.rendering"%dag)
            if value:
                rendering.append(dag)
    for grp in rendering:
        allDags = cmds.ls(grp, dag = True, ni = True)
        mesh += allDags
    return mesh