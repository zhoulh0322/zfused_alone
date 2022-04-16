# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

import maya.cmds as cmds
import pymel.core as pm

import zfused_api

import zfused_maya.core.record as record
import zfused_maya.node.core.renderinggroup as renderinggroup


def get():
    _info = {}
    _is_rendering = renderinggroup.nodes()
    if _is_rendering:
        objs = pm.ls(_is_rendering, dag=True, type='mesh')
    else:
        objs = pm.ls(dag=True, type='mesh')
    _vtx_count = 0
    _edg_count = 0
    _face_count = 0
    _poly_count = 0
    for _obj in objs:
        _vtx_count += _obj.numVertices()
        _edg_count += _obj.numEdges()
        _face_count += _obj.numFaces()
        _poly_count += _obj._numPolygons()
        
    _info["vertices"] = _vtx_count
    _info["edges"] = _edg_count
    _info["faces"] = _face_count

    return _info

def _render_get(material_name):
    _node_type = cmds.nodeType(material_name)
    if _node_type.lower().startswith("ai"):
        return "arnold"
    elif _node_type.lower().startswith("vray"):
        return "vray"
    elif _node_type.lower().startswith("redshift"): 
        return "redshift"
    #else:
    return None

def _hierarchy_tree(parent, tree):
    children = cmds.listRelatives(parent, c=True, type='transform')
    if children:
        tree[parent] = (children, {})
        for child in children:
            _hierarchy_tree(child, tree[parent][1])

def asset_get():
    # # ==================================================================
    # # 写入 property geometry 属性内容
    # # 后面由其他函数实现
    # _task_id = record.current_task_id()
    # _task = zfused_api.task.Task(_task_id)
    # _project_entity = _task.project_entity()
    # _geometry = []
    # _is_rendering = renderinggroup.nodes()
    # _objs = []
    # if _is_rendering:
    #     _objs = pm.ls(_is_rendering, dag=True, type='mesh')
    # else:
    #     _objs = pm.ls(dag=True, type='mesh')
    # if not _objs:
    #     return _geometry
    # for _obj in _objs:
    #     _mesh = {}
    #     _mesh["shape"] = _obj.name()
    #     _mesh["transform"] = _obj.getTransform().name()
    #     _mesh["full_path"] = _obj.fullPath()
    #     _mesh["vertices"] = _obj.numVertices()
    #     _mesh["edges"] = _obj.numEdges()
    #     _mesh["faces"] = _obj.numFaces()
    #     _mesh["polygons"] = _obj._numPolygons()     
    #     _geometry.append(_mesh)
    # _project_entity.update_property("geometry", _geometry)
    
    # get asset base info
    _info = {}
    _is_rendering = renderinggroup.nodes()
    if _is_rendering:
        objs = pm.ls(_is_rendering, dag=True, type='mesh')
    else:
        objs = pm.ls(dag=True, type='mesh')
    _vtx_count = 0
    _edg_count = 0
    _face_count = 0
    _poly_count = 0
    for _obj in objs:
        _vtx_count += _obj.numVertices()
        _edg_count += _obj.numEdges()
        _face_count += _obj.numFaces()
        _poly_count += _obj._numPolygons()        
    _info["vertices"] = _vtx_count
    _info["edges"] = _edg_count
    _info["faces"] = _face_count

    # get material
    _mats = sorted(set(cmds.ls([mat for item in cmds.ls(type='shadingEngine') for mat in cmds.listConnections(item) if cmds.sets(item, q=True)], materials=True)))
    _mat_types = []
    for _mat in _mats:
        _mat_type = _render_get(_mat)
        if _mat_type and _mat_type not in _mat_types:
            _mat_types.append(_mat_type) 
    _info["materials"] = _mat_types

    # get hierarchy
    _info["hierarchy"] = {}
    _is_rendering = renderinggroup.nodes()
    if _is_rendering:
        if len(_is_rendering):
            _hierarchy_tree(_is_rendering[0], _info["hierarchy"])
    
    # bounding box
    _box = pm.exactWorldBoundingBox(objs)
    _info["boundingbox"] = _box

    # cmds.exactWorldBoundingBox(cmds.ls(type = "mesh"))
    # top_node = 'testchartd:c_testchartd_geometry_GRP'
    # hierarchy_tree_new = {}
    # hierarchyTree(top_node, hierarchy_tree_new)
    
    _info["warning"] = []
    # get task lastet task version
    _current_task_id = record.current_task_id()
    if _current_task_id:
        _task_handle = zfused_api.task.Task(_current_task_id)
        _versions = _task_handle.versions(True)
        if _versions:
            _last_version = _versions[-1]
            if _last_version.get("IsApproval") != 1:
                if len(_versions) >= 2:
                    _last_version = _versions[-2]
                else:
                    _last_version = {}
            # get record
            _record = _last_version.get("Record")
            if _record:
                _record = eval(_record)
                _vertices = _record.get("vertices")
                if _vertices:
                    if _vertices != _info["vertices"]:
                        _info["warning"].append(u"模型点数更改")
                _edges = _record.get("edges")
                if _edges:
                    if _edges != _info["edges"]:
                        _info["warning"].append(u"模型边数更改")
                _faces = _record.get("faces")
                if _faces:
                    if _faces != _info["faces"]:
                        _info["warning"].append(u"模型面数更改")
                _hierarchy = _record.get("hierarchy")
                if _hierarchy:
                    if _hierarchy != _info["hierarchy"]:
                        _info["warning"].append(u"层级结构改动")
    return _info


def shot_get():
    _info = {}
    _min_frame = cmds.playbackOptions(q = True, min = True)
    _max_frame = cmds.playbackOptions(q = True, max = True)
    _info["start_frame"] = _min_frame
    _info["end_frame"] = _max_frame
    _info["frame_count"] = _max_frame - _min_frame + 1

    return _info
