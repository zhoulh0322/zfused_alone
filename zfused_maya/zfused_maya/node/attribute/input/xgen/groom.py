# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function


import logging


import maya.cmds as cmds


import zfused_api


from zfused_maya.node.core import groom
from zfused_maya.node.core import xgen
import xgenm as xg
import os

logger = logging.getLogger(__name__)
_is_load = cmds.pluginInfo("AbcImport", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load alembic plugin")
        cmds.loadPlugin("AbcImport")
    except Exception as e:
        logger.error(e)


@zfused_api.reset
def alembic_merge(*args,**kwargs):
    # _task_id, _task_attr_input_id, _input_task_id, _input_task_attr_output_id, _namesapce = args
    _task_id = kwargs.get("task_id")
    _task_attr_input_id = kwargs.get("task_attr_input_id")
    _input_task_id = kwargs.get("input_task_id")
    _input_task_attr_output_id = kwargs.get("input_task_attr_output_id")
    _namespace = kwargs.get("namespace")

    _task = zfused_api.task.Task(_task_id)
    _task_attr_input = zfused_api.attr.Input(_task_attr_input_id)
    _extended_version = _task_attr_input.extended_version()

    _input_task = zfused_api.task.Task(_input_task_id)
    _input_task_attr_output = zfused_api.attr.Output(_input_task_attr_output_id)
    _input_task_project_step_id = _input_task_attr_output.project_step_id()
    _input_production_path = _input_task.cache_path()

    # get file 
    _file_suffix = _input_task_attr_output.suffix()
    if _extended_version:
        _file_index = "{:0>4d}".format(_input_task.last_version_index())
        _production_file = "{}/{}/{}.{}{}".format(_input_production_path, _input_task_attr_output.code(), _namespace, _file_index, _file_suffix)
    else:
        _production_file = "{}/{}/{}{}".format(_input_production_path, _input_task_attr_output.code(), _namespace, _file_suffix)

    # get asset material file
    print(_namespace)
    _rf_nodes = cmds.ls( rf = True )
    for _rf_node in _rf_nodes:
        _inr = cmds.referenceQuery(_rf_node, inr = True)
        if not _inr:
            _exist_namespace = cmds.referenceQuery(_rf_node, namespace = True, shn = True)
            print(_exist_namespace)
            # get rendering attribute
            if _exist_namespace.split("__in__")[0] == _namespace:
                _cachings = groom.nodes()
                print(_cachings)
                if not _cachings:
                    continue
                for _caching in _cachings:
                    if _caching.startswith("{}:".format(_exist_namespace)) or _caching.startswith("|{}:".format(_exist_namespace)):
                        print(_caching)
                        print(_production_file)
                        cmds.AbcImport(_production_file, mode = 'import', connect = _caching)
                # cmds.file(_production_file, ns = "{}__in__{}".format(_namespace, _input_task_attr_output.code()), r = True, mergeNamespacesOnClash = False, ignoreVersion = True)



def assgin_growmesh(task_id,stepcode,suffix):
    _task_id = task_id
    _task_entity = zfused_api.task.Task(_task_id)
    _project_entity = _task_entity.project_entity()
    _software_code = _task_entity.software().code()
    _cache_path = _project_entity.cache_path() + '/cfx/{}'.format(_software_code)
    _all_palettes = xgen.get_all_palettes()
    _attr_code = stepcode
    _suffix = suffix
    for _palette in _all_palettes:
        _descriptions = xg.descriptions(_palette)
        for _description in _descriptions:
            exist_short_ns = cmds.referenceQuery(_palette, ns=1, shn=True)
            short_ns = exist_short_ns.split('__in__')[0]
            _palette_name = _palette.replace('{}:'.format(exist_short_ns), "")
            #grow_mesh_grp = xgen.get_growmesh(_palette)
            _cover_file = '{}/{}/{}_{}{}'.format(_cache_path, _attr_code, short_ns, _palette_name, _suffix)
            if not os.path.exists(_cover_file):
                continue
            xg.setAttr("renderer", "Arnold Renderer", _palette, _description, "RendermanRenderer")
            # 设置渲染模式
            xg.setAttr("custom__arnold_rendermode", "1", _palette, _description, "RendermanRenderer")
            # 开启读取缓存
            xg.setAttr("custom__arnold_useAuxRenderPatch", "1", _palette, _description, "RendermanRenderer")
            oldpatchfile = xg.getAttr("custom__arnold_auxRenderPatch", _palette, _description, "RendermanRenderer")
            if _cover_file == oldpatchfile:
                continue
            xg.setAttr("custom__arnold_auxRenderPatch", _cover_file, _palette, _description, "RendermanRenderer")
            cmds.setAttr(_description + ".ai_use_aux_render_patch", 1)
            cmds.setAttr(_description + ".ai_batch_render_patch", _cover_file, type='string')
    return True