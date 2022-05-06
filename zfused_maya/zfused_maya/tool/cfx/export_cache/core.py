# -*- coding: UTF-8 -*-
'''
@Time    : 2022/3/30 15:09
@Author  : Jerris_Cheng
@File    : export_cache.py
@Description:
'''
from __future__ import print_function

import logging
import os
import sys

import maya.cmds as cmds

import xgenm as xg

import zfused_api

from zfused_maya.node.core import improve

from zfused_maya.node.core import alembiccache, fixmeshname, renderinggroup, xgen
reload(alembiccache)
reload(xgen)


__all__ = ["publish_alembic"]

logger = logging.getLogger(__name__)
_is_load = cmds.pluginInfo("AbcExport", query=True, loaded=True)
if not _is_load:
    try:
        logger.info("try load alembic plugin")
        cmds.loadPlugin("AbcExport")
    except Exception as e:
        logger.error(e)
        sys.exit()

# 缓存预留帧 后面需要存放在数据库上
PREPFRAME = 8
EXPORTATTR = ["worldSpace", "writeVisibility", "uvWrite"]
ATTPREFIX = {
    "attrPrefix": 'xgen'
}

# @improve.viewportOff
def publish_alembic(*args, **kwargs):

    """ 发布xgen 生长面abc
    """
    _suffix = ".abc"
    # _task_id, _output_attr_id = args
    # _output_attr_handle = zfused_api.attr.Output(_output_attr_id)
    # _file_format = _output_attr_handle.format()
    # _suffix = _output_attr_handle.suffix()
    # _attr_code = _output_attr_handle.code()
    # _task = zfused_api.task.Task(_task_id)
    # _task_step = _task.project_step().code()

    # _production_path = _task.production_path()
    # _project_entity = _task.project_entity()
    # _file_code = _task.file_code()
    # if kwargs.get("fix_version"):
    #     _file_index = "{:0>4d}".format(_task.last_version_index(0))
    # else:
    #     _file_index = "{:0>4d}".format(_task.last_version_index() + 1)

    _start_frame = int(cmds.playbackOptions(q=True, min=True)) - PREPFRAME
    _end_frame = int(cmds.playbackOptions(q=True, max=True)) + PREPFRAME

    _publish_path = kwargs.get("cache_path")
    # _cache_path = _task.cache_path()

    # _project_porperty = _project_entity.property()
    # 记录 缓存 上传

    _abc_jobs = []
    
    _trans = []

    # 记录 缓存 上传
    _render_dags = renderinggroup.nodes()
    _assets = kwargs.get("assets")
    # if not _assets:
    #     _assets = _project_porperty.get('asset')
    _asset_namespaces = [_asset.get("namespace") for _asset in _assets]

    for _asset in _assets:
        
        _rfn = _asset.get('rfn')
        _l_ns = _asset.get('namespace')
        for _dag in _render_dags:

            fixmeshname.fix_deformed_mesh_name("_rendering", _dag)

            _dag_dict = {}
            # _ns = cmds.referenceQuery(_dag,ns = 1)
            _short_ns = cmds.referenceQuery(_dag,ns = 1,shn=True)
            _attr_code = 'asset'
            _publish_file = '{}/{}/{}{}'.format(_publish_path,_attr_code,_short_ns,_suffix)
            # _cache_file = '{}/{}/{}.{}{}'.format(_cache_path,_attr_code,_short_ns,_file_index,_suffix)
            # _cover_file = '{}/{}/{}{}'.format(_cache_path,_attr_code,_short_ns,_suffix)
            jober = alembiccache.create_frame_cache(_publish_file,_start_frame,_end_frame,_dag,*EXPORTATTR)
            if _short_ns == _l_ns:
                _abc_jobs.append(jober)

            #     _dag_dict['publish_file'] = _publish_file
            #     _dag_dict['cover_file'] = _cover_file
            #     _dag_dict['cache_file'] = _cache_file

            #     # 关联信息
            #     _dag_dict['relative_entity_type'] = "asset"
            #     _dag_dict['relative_entity_id'] = _asset.get("id")
            #     _dag_dict['relative_name_space'] = _asset.get("namespace")
            #     _trans.append(_dag_dict)

            #     _asset['last_cache'] = _cover_file
                
            #     _project_step_caches = _asset.get('project_step_caches')
            #     if _project_step_caches:
            #         _is_has = False
            #         for _cache in _project_step_caches:
            #             _step = _cache.get('step')
            #             if _step == _task_step:
            #                 _is_has = True
            #                 _cache['path'] = _cache_file
            #         if not _is_has:
            #             _project_step_caches.append({
            #                 "step": _task_step,
            #                 "path": _cache_file
            #             })
            #     else:
            #         _cache_dict = {}
            #         _cache_dict['step'] = _task_step
            #         _cache_dict['path'] = _cache_file
            #         _project_step_caches.append(_cache_dict)
            #     _asset['project_step_caches'] = _project_step_caches


    # groom生长面缓存
    _grow_mesh_grps = xgen.get_groom_caching_grp()
    if _grow_mesh_grps:
        for grow_mesh_grp in _grow_mesh_grps:
            grow_attr_code = 'groom_caching'
            _short_ns = cmds.referenceQuery(grow_mesh_grp, ns=1, shn=True)

            if _short_ns not in _asset_namespaces:
                continue

            _publish_file = '{}/{}/{}{}'.format(_publish_path, grow_attr_code, _short_ns, _suffix)
            # _cache_file = '{}/{}/{}.{}{}'.format(_cache_path, grow_attr_code, _short_ns, _file_index, _suffix)
            # _cover_file = '{}/{}/{}{}'.format(_cache_path, grow_attr_code, _short_ns, _suffix)

            _abc_job = alembiccache.create_frame_cache(_publish_file, _start_frame, _end_frame, grow_mesh_grp, *EXPORTATTR)
            _abc_jobs.append(_abc_job)
            #
            # _dag_dict['publish_file'] = _publish_file
            # _dag_dict['cover_file'] = _cover_file
            # _dag_dict['cache_file'] = _cache_file

    # guide 曲线
    _all_descriptions = xg.descriptions()
    if _all_descriptions:
        for _description in _all_descriptions:
            _out_curves = xgen.get_outcurve_desc(_description)
            print(_out_curves)
            if _out_curves:
                curve_attr_code = 'outcurve'
                _palette = xg.palette(_description)
                outcurve_short_ns = cmds.referenceQuery(_description, ns=1, shn=True)

                if outcurve_short_ns not in _asset_namespaces:
                    continue

                _description_name = _description.replace('{}:'.format(outcurve_short_ns), "")
                _palette_name = _palette.replace('{}:'.format(outcurve_short_ns), "")
                outcurve_publish_file = '{}/{}/{}_{}_{}{}'.format(_publish_path, curve_attr_code, outcurve_short_ns,
                                                                     _palette_name, _description_name,
                                                                     _suffix)
                _abc_job = alembiccache.create_frame_cache(outcurve_publish_file, _start_frame, _end_frame, _out_curves,
                                                           *EXPORTATTR)
                _abc_jobs.append(_abc_job)

    # xgen groom生长面batch
    _all_palettes = xgen.get_all_palettes()
    if _all_palettes:
        for _pallette in _all_palettes:
            _dag_dict = {}
            growmesh_attr_code = 'growmesh_batch'
            pallette_short_ns = cmds.referenceQuery(_pallette, ns=1, shn=True)

            if pallette_short_ns not in _asset_namespaces:
                continue

            _palette_name = _pallette.replace('{}:'.format(pallette_short_ns), "")
            #grow_mesh_grp = xgen.get_growmesh(_pallette)

            _publish_file = '{}/{}/{}_{}{}'.format(_publish_path, growmesh_attr_code, pallette_short_ns, _palette_name, _suffix)
            _abc_job = alembiccache.create_xgen_frame_cache(_publish_file, _start_frame, _end_frame, _pallette)

            _abc_jobs.append(_abc_job)

    try:
        cmds.AbcExport( j = _abc_jobs )
    except Exception as e:
        print(e)
        pass

    # try:
    #     # 输出缓存
    #     cmds.AbcExport(j=_abc_jobs)
    #     for _tran in _trans_list:
            
    #         publish_file = _tran.get('publish_file')
    #         cover_file = _tran.get('cover_file')
    #         cache_file = _tran.get('cache_file')
    #         print(cache_file)

    #         _result = filefunc.publish_file(publish_file, cache_file)
    #         _result = filefunc.publish_file(publish_file, cover_file)

    # except Exception as e:
    #     logger.error(e)
    #     print(e)
    #     return False
    
    return True






def get_assets():
    _reference_elements = []

    # get rendering elements
    _rendering_groups = []
    _groups = cmds.ls(dag = True)
    for _group in _groups:
        if cmds.objExists("{}.rendering".format(_group)):
            _is_rendering = cmds.getAttr("{}.rendering".format(_group))
            if _is_rendering:
                _rendering_groups.append(_group)
    print(_rendering_groups)
    _all_references = []
    for _rendering in _rendering_groups:
        if cmds.referenceQuery(_rendering, isNodeReferenced = True):
            _node = cmds.referenceQuery(_rendering, referenceNode = True)
            if _node not in  _all_references:
                _all_references.append(_node)
            # _all_references[_node].append(obj)
    print(_all_references)
    for _reference in _all_references:
        namespace = cmds.referenceQuery(_reference, namespace = True)
        if namespace.startswith(":"):
            namespace = namespace[1::]
        rfn = cmds.referenceQuery(_reference, rfn = True)
        # #get attr
        # _node_attr = attr.get_node_attr(rfn)
        # if not _node_attr:
        #     continue
        # if _node_attr["project_id"] != _project_id:
        #     continue
        copy_data = {
                        "namespace": "",
                        "reference_node": "",
                        "relation_ship": "reference",
                    }
        # for k in _node_attr.keys():
        #     if copy_data.keys().__contains__(k):
        #         copy_data[k] = _node_attr[k]
        copy_data["namespace"] = namespace
        copy_data["reference_node"] = rfn
        copy_data["rfn"] = rfn
        _reference_elements.append(copy_data)
    
    return _reference_elements



def current_cache_path():
    _path = cmds.file(q = True, sn = True)
    if _path:
        _path = os.path.dirname(_path)
        return "{}/cache".format(_path)
    return ""