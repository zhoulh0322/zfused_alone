# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging


import maya.cmds as cmds

import xgenm as xg
import xgenm.xgGlobal as xgg

import zfused_api


from zfused_maya.node.core import groom


logger = logging.getLogger(__name__)
_is_load = cmds.pluginInfo("AbcImport", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("try load alembic plugin")
        cmds.loadPlugin("AbcImport")
    except Exception as e:
        logger.error(e)


@zfused_api.reset
def alembic_in(*args,**kwargs):
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

    # get asset
    _rf_nodes = cmds.ls( rf = True )
    for _rf_node in _rf_nodes:
        _inr = cmds.referenceQuery(_rf_node, inr = True)
        if not _inr:
            _exist_namespace = cmds.referenceQuery(_rf_node, namespace = True, shn = True)
            print(_exist_namespace)
            # get rendering attribute
            if _exist_namespace.split("__in__")[0] == _namespace:                
                # 获取 xgen collection and description


                _growmeshs = []
                _all_palettes = xg.palettes()
                for _palette in _all_palettes:
                    
                    if not _palette.startswith(_exist_namespace):
                        continue

                    _des_editor = xgg.DescriptionEditor

                    _des_editor.setCurrentPalette(_palette)


                    _pale_descs = xg.descriptions(_palette)
                    for _desc in _pale_descs:
                        
                        _des_editor.setCurrentDescription(_desc)    

                        print(_palette)
                        print(_desc)
                    
                        # _grow_meshs = xg.boundGeometry(_palette, _desc)
                        # for _mesh in _grow_meshs:
                        #     if not _mesh in _growmeshs:
                        #         _growmeshs.append(_mesh)

                        # _guide_cache = str(collectionData.get('path'))

                        if _extended_version:
                            _file_index = "{:0>4d}".format(_input_task.last_version_index())
                            _production_file = "{}/{}/{}_{}_{}.{}{}".format(_input_production_path, _input_task_attr_output.code(), _namespace, _palette.split(":")[-1], _desc.split(":")[-1], _file_index, _file_suffix)
                        else:
                            _production_file = "{}/{}/{}_{}_{}{}".format(_input_production_path, _input_task_attr_output.code(), _namespace, _palette.split(":")[-1], _desc.split(":")[-1], _file_suffix)

                        print(_production_file)
                        print(os.path.isfile(_production_file))


                        xg.setAttr('renderer', 'Arnold Renderer', _palette, _desc, 'RendermanRenderer')
                        xg.setAttr('custom__arnold_rendermode', '1', _palette, _desc, 'RendermanRenderer')
                        # xg.setAttr('custom__arnold_useAuxRenderPatch', '1', _palette, _desc, 'RendermanRenderer')
                        xg.setAttr('custom__arnold_multithreading', '1', _palette, _desc, 'RendermanRenderer')
                        # xg.setAttr('custom__arnold_auxRenderPatch', str(_production_file), _palette, _desc, 'RendermanRenderer')
                        if not os.path.isfile(_production_file):
                            continue
                        xg.setAttr('useCache', '1', _palette, _desc, 'SplinePrimitive')
                        xg.setAttr('cacheFileName', _production_file, _palette, _desc, 'SplinePrimitive')
                        xg.setAttr('liveMode', '0', _palette, _desc, 'SplinePrimitive')

                        #　Get the description editor first.
                        #　_des = xgg.DescriptionEditor
                        #　Do a full UI refresh
                        _des_editor.refresh("Full")

                continue