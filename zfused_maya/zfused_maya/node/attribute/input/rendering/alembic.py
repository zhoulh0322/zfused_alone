# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function


import logging


import maya.cmds as cmds


import zfused_api


from zfused_maya.node.core import renderinggroup


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

    _project = _task.project()
    # _skip_cache_code = 

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
                _renderings = renderinggroup.nodes()
                if not _renderings:
                    continue
                for _rendering in _renderings:
                    _rendering = cmds.ls(_rendering, sn = True)[0]
                    if _rendering.startswith("{}:".format(_exist_namespace)) or _rendering.startswith("|{}:".format(_exist_namespace)):
                        print(_rendering)
                        print(_production_file)
                        cmds.AbcImport(_production_file, mode = 'import', connect = _rendering)

                # cmds.file(_production_file, ns = "{}__in__{}".format(_namespace, _input_task_attr_output.code()), r = True, mergeNamespacesOnClash = False, ignoreVersion = True)