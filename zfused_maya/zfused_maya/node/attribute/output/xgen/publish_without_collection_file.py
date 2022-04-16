# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api

from zcore import zfile,transfer,filefunc

# import zfused_maya.node.core.texture as texture
# import zfused_maya.node.core.material as material
# import zfused_maya.node.core.fixmeshname as fixmeshname
# import zfused_maya.node.core.renderinggroup as renderinggroup
from zfused_maya.node.core import xgen,texture,material,fixmeshname,renderinggroup,referencefile

__all__ = ["publish_without_collection_file"]

logger = logging.getLogger(__name__)

def publish_without_collection_file(*args, **kwargs):
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
    _production_file_dir = os.path.dirname(_production_file)
    _cover_file = "{}/{}/{}{}".format(_production_path, _attr_code, _file_code, _suffix)
    _publish_cover_file = "{}/{}/{}{}".format( _temp_path, _attr_code, _file_code, _suffix )
    _publish_file = "{}/{}/{}.{}{}".format( _temp_path, _attr_code, _file_code, _file_index, _suffix )
    _publish_file_dir = os.path.dirname(_publish_file)
    if not os.path.isdir(_publish_file_dir):
        os.makedirs(_publish_file_dir)
    
    try:
        # save publish file
        cmds.file(rename = _publish_file)
        cmds.file(save = True, type = _file_format, f = True, options = "v=0;")
        
        # publish xgen texture
        _texture_infos = []
        _texture_files = texture.files()
        if _texture_files:
            _path_set = texture.paths(_texture_files)[0]
            _intersection_path = max(_path_set)
            _texture_infos = texture.publish_file(_texture_files, _intersection_path, _project_entity_production_path + "/texture/xgen")
            # change maya texture node path
            _file_nodes = texture.nodes()
            if _file_nodes:
                texture.change_node_path(_file_nodes, _intersection_path, _project_entity_production_path + "/texture/xgen")

        #传输xgen相关信息
        if xgen.files():
            # xgen.publish_file(_production_path)
            cmds.file(save = True, type = _file_format, f = True, options = "v=0;")
            xgen.publish_xgen(_production_file_dir)

        # import all reference
        referencefile.import_all_references()
        # remove all namesapce
        referencefile.remove_all_namespaces()

        # save publish file
        cmds.file(save = True, type = _file_format, f = True, options = "v=0;")

        # 保存不带版本的文件
        cmds.file(rename = _publish_cover_file)
        cmds.file(save = True, type = _file_format, f = True)
        xgen.publish_xgen(os.path.dirname(_cover_file))

        # publish file
        _result = filefunc.publish_file(_publish_file, _production_file)
        _result = filefunc.publish_file(_publish_cover_file, _cover_file)
        
        # production file
        _file_info = zfile.get_file_info(_publish_file, _production_file)
        _cover_file_info = zfile.get_file_info(_publish_file, _cover_file)
        zfused_api.task.new_production_file([_file_info, _cover_file_info] + _texture_infos, _task_id, _output_attr_id, int(_file_index) )

    except Exception as e:
        logger.error(e)
        return False

    return True