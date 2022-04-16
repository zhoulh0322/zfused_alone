# -*- coding: UTF-8 -*-
'''
@Time    : 2022/3/30 15:09
@Author  : Jerris_Cheng
@File    : publish_groom_caching.py
@Description:
'''
from __future__ import print_function

import logging
import sys

import maya.cmds as cmds

import zfused_api
from zcore import filefunc
from zfused_maya.node.core import alembiccache, xgen

reload(xgen)
import xgenm as xg

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


def publish_alembic(*args, **kwargs):
    """ 发布xgen 生长面abc
    """

    _task_id, _output_attr_id = args
    _output_attr_handle = zfused_api.attr.Output(_output_attr_id)
    _file_format = _output_attr_handle.format()
    _suffix = _output_attr_handle.suffix()
    _attr_code = _output_attr_handle.code()
    _task = zfused_api.task.Task(_task_id)
    _task_step = _task.project_step().code()

    _production_path = _task.production_path()
    _project_entity = _task.project_entity()
    _file_code = _task.file_code()
    if kwargs.get("fix_version"):
        _file_index = "{:0>4d}".format(_task.last_version_index(0))
    else:
        _file_index = "{:0>4d}".format(_task.last_version_index() + 1)

    _start_frame = int(cmds.playbackOptions(q=True, min=True)) - PREPFRAME
    _end_frame = int(cmds.playbackOptions(q=True, max=True)) + PREPFRAME

    _publish_path = _task.temp_path()
    _cache_path = _task.cache_path()

    _abc_jobs = []
    _trans_list = []

    _project_porperty = _project_entity.property()
    # 记录 缓存 上传

    _grow_mesh_grps = xgen.get_groom_caching_grp()
    for grow_mesh_grp in _grow_mesh_grps:
        _dag_dict = {}
        _short_ns = cmds.referenceQuery(grow_mesh_grp, ns=1, shn=True)
        _publish_file = '{}/{}/{}.{}{}'.format(_publish_path, "groom_caching", _short_ns, _file_index, _suffix)
        _cache_file = '{}/{}/{}.{}{}'.format(_cache_path, _attr_code, _short_ns, _file_index, _suffix)
        _cover_file = '{}/{}/{}{}'.format(_cache_path, _attr_code, _short_ns, _suffix)

        # _abc_job = alembiccache.create_frame_cache(_publish_file, _start_frame, _end_frame, grow_mesh_grp, *EXPORTATTR)
        # _abc_jobs.append(_abc_job)

        _dag_dict['publish_file'] = _publish_file
        _dag_dict['cover_file'] = _cover_file
        _dag_dict['cache_file'] = _cache_file
        _trans_list.append(_dag_dict)

    # _outcurve_grps = xgen.get_all_out_curve_grp()
    # for outcurve_grp in _outcurve_grps:
    #     curve_attr_code = 'outcurve'
    #     outcurve_short_ns = cmds.referenceQuery(outcurve_grp, ns=1, shn=True)
    #     outcurve_publish_file = '{}/{}/{}.{}{}'.format(_publish_path, curve_attr_code, outcurve_short_ns, _file_index,_suffix)
    #
    #     _abc_job = alembiccache.create_frame_cache(outcurve_publish_file, _start_frame, _end_frame, outcurve_grp,*EXPORTATTR)
    #     _abc_jobs.append(_abc_job)
    # _all_descriptions = xg.descriptions()
    # for _description in _all_descriptions:
    #     _out_curves = xgen.get_outcurve_desc(_description)
    #     if _out_curves:
    #         curve_attr_code = 'outcurve'
    #         _palette = xg.palette(_description)
    #         outcurve_short_ns = cmds.referenceQuery(_description, ns=1, shn=True)
    #         _description_name = _description.replace('{}:'.format(outcurve_short_ns), "")
    #         _palette_name = _palette.replace('{}:'.format(outcurve_short_ns), "")
    #         outcurve_publish_file = '{}/{}/{}_{}_{}.{}{}'.format(_publish_path, curve_attr_code, outcurve_short_ns,
    #                                                              _palette_name, _description_name,
    #                                                              _file_index,
    #                                                              _suffix)
    #         _abc_job = alembiccache.create_frame_cache(outcurve_publish_file, _start_frame, _end_frame, _out_curves,
    #                                                    *EXPORTATTR)
    #         _abc_jobs.append(_abc_job)
    #
    # _all_palettes = xgen.get_all_palettes()
    # for _pallette in _all_palettes:
    #     _dag_dict = {}
    #     growmesh_attr_code = 'growmesh_bacth'
    #     pallette_short_ns = cmds.referenceQuery(_pallette, ns=1, shn=True)
    #     _palette_name = _pallette.replace('{}:'.format(pallette_short_ns), "")
    #     grow_mesh_grp = xgen.get_growmesh(_pallette)
    #
    #     _publish_file = '{}/{}/{}_{}.{}{}'.format(_publish_path, growmesh_attr_code, pallette_short_ns, _palette_name,
    #                                               _file_index,
    #                                               _suffix)
    #     _abc_job = alembiccache.create_xgen_frame_cache(_publish_file, _start_frame, _end_frame, grow_mesh_grp,
    #                                                     )
    #
    #     _abc_jobs.append(_abc_job)
    #
    # _all_palettes = xgen.get_all_palettes()
    # for _pallette in _all_palettes:
    #     _dag_dict = {}
    #     growmesh_attr_code = 'growmesh_batch'
    #     pallette_short_ns = cmds.referenceQuery(_pallette, ns=1, shn=True)
    #     _palette_name = _pallette.replace('{}:'.format(pallette_short_ns), "")
    #     grow_mesh_grp = xgen.get_growmesh(_pallette)
    #
    #     _publish_file = '{}/{}/{}_{}.{}{}'.format(_publish_path, growmesh_attr_code, pallette_short_ns, _palette_name,
    #                                               _file_index,
    #                                               _suffix)
    #     _abc_job = alembiccache.create_xgen_frame_cache(_publish_file, _start_frame, _end_frame, grow_mesh_grp,
    #                                                     )
    #
    #     _abc_jobs.append(_abc_job)

    try:
        # 输出缓存
        #cmds.AbcExport(j=_abc_jobs)
        
        for _tran in _trans_list:

            publish_file = _tran.get('publish_file')
            cover_file = _tran.get('cover_file')
            cache_file = _tran.get('cache_file')
            _result = filefunc.publish_file(publish_file, cache_file)
            _result = filefunc.publish_file(publish_file, cover_file)

    except Exception as e:
        logger.error(e)
        print(e)
        return False
    return True
