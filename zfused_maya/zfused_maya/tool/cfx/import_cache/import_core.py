# -*- coding: UTF-8 -*-
"""
@Time    : 2022/5/18 18:22
@Author  : Jerris_Cheng
@File    : import_core.py
@Description:
"""
from __future__ import print_function

import os.path

import maya.cmds as cmds

from zfused_maya.node.core import renderinggroup,xgen
import xgenm as xg
import xgenm.xgGlobal as xgg


def get_assets():
    _reference_elements = []

    # get rendering elements
    _rendering_groups = []
    _groups = cmds.ls(dag=True)
    for _group in _groups:
        if cmds.objExists("{}.rendering".format(_group)):
            _is_rendering = cmds.getAttr("{}.rendering".format(_group))
            if _is_rendering:
                _rendering_groups.append(_group)
                continue
        if cmds.objExists("{}.groom_caching".format(_group)):
            _is_rendering = cmds.getAttr("{}.groom_caching".format(_group))
            if _is_rendering:
                _rendering_groups.append(_group)
                continue


    _all_references = []
    for _rendering in _rendering_groups:
        if cmds.referenceQuery(_rendering, isNodeReferenced=True):
            _node = cmds.referenceQuery(_rendering, referenceNode=True)
            if _node not in _all_references:
                _all_references.append(_node)
            # _all_references[_node].append(obj)
    for _reference in _all_references:
        namespace = cmds.referenceQuery(_reference, namespace=True)
        if namespace.startswith(":"):
            namespace = namespace[1::]
        rfn = cmds.referenceQuery(_reference, rfn=True)
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


def merge_abc(*args, **kwargs):
    _caches_path = kwargs.get('cache_path')
    _assets = kwargs.get('assets')
    _render_dags = renderinggroup.nodes()
    for _asset in _assets:
        _rfn = _asset.get('rfn')
        print(_rfn)
        _l_ns = _asset.get('namespace')
        for _dag in _render_dags:
            _short_ns = cmds.referenceQuery(_dag, ns=1, shn=True)
            if _short_ns == _l_ns:
                _abc_path = _caches_path + '{}/{}.abc'.format('asset', _short_ns)
                if not os.path.exists(_abc_path):
                    print(u'{}缓存不存在'.format(_short_ns))
                    continue
                #cmds.select(cl=True)
                # cmds.select(_dag)
                try:
                    cmds.AbcImport(_abc_path, mode='import', fitTimeRange=True, connect=_dag)
                except:
                    print(u'{}缓存merge失败'.format(_short_ns))
                    continue


def fur_file(rfn):
    file_name = cmds.referenceQuery(rfn, filename=True)
    short_name = cmds.referenceQuery(rfn, filename=True, shortName=True)
    _path_split = file_name.split('/')
    _asset_path = ''
    for i in _path_split[:7]:
        _asset_path += '{}/'.format(i)
    # 写死了
    _fur_path = '{}fur/xgen/maya2020/file/{}'.format(_asset_path, short_name)
    if os.path.exists(_fur_path):
        return True, _fur_path
    else:
        return False, None


def fur_cache(*args, **kwargs):
    _caches_path = kwargs.get('cache_path')
    _assets = kwargs.get('assets')


    for _asset in _assets:
        _rfn = _asset.get('rfn')
        _l_ns = _asset.get('namespace')
        _xgen_file = fur_file(_rfn)[1]
        _fur_ns = '{}_Hair'.format(_l_ns)
        if not cmds.namespace(exists = _fur_ns):
            cmds.file(_xgen_file, reference=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,namespace=_fur_ns, options='v=0;')
        _grow_mesh_grps = xgen.get_groom_caching_grp()
        for grow_mesh_grp in _grow_mesh_grps:
            grow_attr_code = 'groom_caching'
            _asset_namespace = _l_ns.replace('_Hair','')
            _grow_ns = cmds.referenceQuery(grow_mesh_grp, ns=1, shn=True)
            if _grow_ns == _fur_ns:
                _abc_path = '{}/{}/{}.abc'.format(_caches_path,grow_attr_code,_asset_namespace)
                if not os.path.exists(_abc_path):
                    print(u'{}缓存不存在'.format(_fur_ns))
                    continue
                try:
                    cmds.AbcImport(_abc_path, mode='import', fitTimeRange=True, connect=grow_mesh_grp)
                except:
                    print(u'{}缓存merge失败'.format(_grow_ns))
        # guide 曲线
        _all_descriptions = xg.descriptions()
        if _all_descriptions:
            outcure_attr = 'outcurve'
            grow_mesh_attr = 'growmesh_batch'
            for _description in _all_descriptions:
                _desc_ns = cmds.referenceQuery(_description, ns=1, shn=True)
                _desc_palette = xg.palette(_description)
                _des_editor = xgg.DescriptionEditor

                _des_editor.setCurrentPalette(_desc_palette)

                _pale_descs = xg.descriptions(_desc_palette)
                pallette_short_ns = cmds.referenceQuery(_desc_palette, ns=1, shn=True)
                if _desc_ns ==_fur_ns:
                    desc_curve_abc = '{}/{}/{}.abc'.format(_caches_path,outcure_attr,_description.replace(':',"_"))
                    if not os.path.exists(desc_curve_abc):
                        print(u'{}缓存不存在'.format(_desc_ns))
                        continue
                    xg.setAttr('renderer', 'Arnold Renderer', _desc_palette, _description, 'RendermanRenderer')
                    xg.setAttr('custom__arnold_rendermode', '1', _desc_palette, _description, 'RendermanRenderer')
                    # xg.setAttr('custom__arnold_useAuxRenderPatch', '1', _palette, _desc, 'RendermanRenderer')
                    xg.setAttr('custom__arnold_multithreading', '1', _desc_palette, _description, 'RendermanRenderer')
                    # xg.setAttr('custom__arnold_auxRenderPatch', str(_production_file), _palette, _desc, 'RendermanRenderer')
                    xg.setAttr('useCache', '1', _desc_palette, _description, 'SplinePrimitive')
                    xg.setAttr('cacheFileName', desc_curve_abc, _desc_palette, _description, 'SplinePrimitive')
                    xg.setAttr('liveMode', '0', _desc_palette, _description, 'SplinePrimitive')

                    #设置生长面补丁
                    _palette_name =_desc_palette.replace('{}:'.format(pallette_short_ns), "")
                    grow_mesh_abc = '{}/{}/{}.abc'.format(_caches_path,grow_mesh_attr,_palette_name)


                    xg.setAttr("renderer", "Arnold Renderer", _desc_palette, _description, "RendermanRenderer")
                    # 设置渲染模式
                    xg.setAttr("custom__arnold_rendermode", "1", _desc_palette, _description, "RendermanRenderer")
                    # 开启读取缓存
                    xg.setAttr("custom__arnold_useAuxRenderPatch", "1", _desc_palette, _description, "RendermanRenderer")
                    oldpatchfile = xg.getAttr("custom__arnold_auxRenderPatch", _desc_palette, _description, "RendermanRenderer")
                    if grow_mesh_abc == oldpatchfile:
                        continue
                    xg.setAttr("custom__arnold_auxRenderPatch", grow_mesh_abc, _desc_palette, _description, "RendermanRenderer")
                    cmds.setAttr(_description + ".ai_use_aux_render_patch", 1)
                    cmds.setAttr(_description + ".ai_batch_render_patch", grow_mesh_abc, type='string')


                    # 　Get the description editor first.
                    # 　_des = xgg.DescriptionEditor
                    # 　Do a full UI refresh
                    _des_editor.refresh("Full")





