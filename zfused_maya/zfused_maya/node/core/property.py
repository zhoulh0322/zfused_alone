# -*- coding: utf-8 -*-
# --author-- lanhua.zhou
from __future__ import print_function

import hashlib
import json
import os.path
import re
import tempfile
import time

import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import xgenm as xg
import xgenm.xgGlobal as xgg

import zfused_api
from zfused_maya.node.core import renderinggroup
import zfused_maya.node.core.xgen as xgens
reload(xgens)
from zcore import filefunc


def task_to_project_entity(task_id):
    if not task_id:
        return
    _task_entity = zfused_api.task.Task(task_id)
    _project_entity = _task_entity.project_entity()
    return _project_entity


# =================================================================
def _write_to_disk(project_entity, data={}):
    if not data:
        return
    _production_path = project_entity.production_path()
    _production_file = "{}/{}.property".format(_production_path, project_entity.file_code())
    # _production_file = "{}/.property".format(_production_path)
    _temp_file = "%s/%s_%s.property" % (tempfile.gettempdir(), project_entity.code(), time.time())
    with open(_temp_file, "w") as handle:
        json.dump(data, handle, indent=4)
    handle.close()
    filefunc.publish_file(_temp_file, _production_file)


# ==================================================================
def correct_float(_float):
    _float = float(_float)
    _int_b, _float_b = str(_float).split(".")
    _float_b = _float_b[:3]
    new_float = float("{}.{}".format(_int_b, _float_b))
    return new_float


def get_md5(pplist):
    m = hashlib.md5()
    m.update(str(pplist))
    _md5 = m.hexdigest()
    return _md5


def get_mesh_md5(_mesh):
    _mesh_md5 = {}
    selectionList = om.MSelectionList()
    selectionList.add(_mesh)
    _node = selectionList.getDependNode(0)
    _fnMesh = om.MFnMesh(_node)
    _verticesNum = _fnMesh.numVertices
    _p = om.MPoint(0, 0, 0)

    for _v in xrange(_verticesNum):
        _p += _fnMesh.getPoint(_v)

    _position = [correct_float(_p.x), correct_float(_p.y), correct_float(_p.z)]
    _md5 = get_md5(_position)
    # _mesh_md5[_mesh] = _md5
    return _md5


# geometry
def get_geometrys():
    _geometry = []
    _is_rendering = renderinggroup.nodes()
    _objs = []
    if _is_rendering:
        _objs = pm.ls(_is_rendering, dag=True, type='mesh')
    else:
        _objs = pm.ls(dag=True, type='mesh')
    if not _objs:
        return _geometry
    for _obj in _objs:
        _mesh = {}
        _mesh["shape"] = _obj.name()
        _mesh["transform"] = _obj.getTransform().name()
        # -----------------------------------------------------------------------------
        _full_path = _obj.fullPath()
        if _is_rendering:
            for _rendering_node in _is_rendering:
                _export_node = "|" + _rendering_node.split("|")[-1]
                if _rendering_node in _full_path:
                    _full_path = _export_node + _full_path.split(_rendering_node)[-1]
        _mesh["full_path"] = _full_path

        _mesh["vertices"] = _obj.numVertices()
        _mesh["edges"] = _obj.numEdges()
        _mesh["faces"] = _obj.numFaces()
        _mesh["polygons"] = _obj._numPolygons()
        _mesh["md5"] = get_mesh_md5(_obj.name())
        _geometry.append(_mesh)
    return _geometry


def get_boundingbox():
    _box = []
    _is_rendering = renderinggroup.nodes()
    _objs = []
    if _is_rendering:
        _objs = pm.ls(_is_rendering, dag=True, type='mesh')
    else:
        _objs = pm.ls(dag=True, type='mesh')
    if not _objs:
        return _box
    _box = pm.exactWorldBoundingBox(_objs)
    return _box


def geometry(task_id):
    # ==================================================================
    # 写入 property geometry 属性内容
    _project_entity = task_to_project_entity(task_id)
    _geometry = get_geometrys()
    if _project_entity:
        _project_entity.update_property("geometry", _geometry)
        # boundingbox
        _box = get_boundingbox()
        if _box:
            _project_entity.update_property("boundingbox", _box)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


# ==================================================================
# material and material
def get_engines():
    # 获取所有shading engines
    _engines = []
    _meshs = cmds.ls(type="mesh")
    for _mesh in _meshs:
        _mesh_sgs = cmds.listConnections(_mesh, type="shadingEngine")
        _engines += _mesh_sgs
    return list(set(_engines))


def get_materials():
    # 获取所有材质
    pass


def get_material_assigns():
    _material_assigns = []
    _engines = get_engines()

    if not _engines:
        return _material_assigns

    rx = re.compile(r'f\[(.*?)\]$')

    for _engine in _engines:
        _meshs = cmds.sets(_engine, q=True)
        if not _meshs:
            continue
        _transforms = []
        _face_ids = {}
        for _mesh in _meshs:
            search = rx.search(_mesh)
            if search:
                _transform = _mesh.split(".f[")[0]
                # _mesh_name = cmds.listRelatives(_transform, c = True, s = True)[0]
                num = search.group(1).replace(":", "-")
                if _transform not in _face_ids:
                    _face_ids[_transform] = []
                _face_ids[_transform].append(num)
            else:
                _mesh_name = _mesh
                _transform = cmds.listRelatives(_mesh_name, p=True)[0]
                _transforms.append(_transform)
        if _transforms:
            for _transform in _transforms:
                _material_assign = {}
                _material_assign["engine"] = _engine
                _material_assign["transform"] = _transform
                _material_assign["shape"] = cmds.listRelatives(_transform, c=True, s=True)[0]
                _material_assigns.append(_material_assign)
        if _face_ids:
            for _transfrom, _faces in _face_ids.items():
                _material_assign = {}
                _material_assign["engine"] = _engine
                _material_assign["transform"] = _transfrom
                _material_assign["shape"] = cmds.listRelatives(_transfrom, c=True, s=True)[0]
                _material_assign["faces"] = _faces
                _material_assigns.append(_material_assign)

    return _material_assigns


def material(task_id):
    # ==================================================================
    # 写入 property material 属性内容
    _project_entity = task_to_project_entity(task_id)
    _engines = get_engines()
    if _project_entity:
        _project_entity.update_property("engine", _engines)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


def material_assign(task_id):
    # ==================================================================
    # 写入 property material assign 属性内容
    _project_entity = task_to_project_entity(task_id)
    _material_assigns = get_material_assigns()
    if _project_entity:
        _project_entity.update_property("material_assign", _material_assigns)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


# ==================================================================
# assets
def get_assets():
    _asset = []
    # 获取reference文件
    _reference_nodes = cmds.ls(rf=True)
    for _node in _reference_nodes:
        _file_path = cmds.referenceQuery(_node, f=True, wcn=True)
        _namespace = cmds.referenceQuery(_node, namespace=True)
        if _namespace.startswith(":"):
            _namespace = _namespace[1::]
        _production_files = zfused_api.zFused.get("production_file_record", filter={
            "Path": _file_path})
        if _production_files:
            _production_file = _production_files[-1]
            _task_id = _production_file.get("TaskId")
            _task = zfused_api.task.Task(_task_id)
            _task_project_entity = _task.project_entity()
            _version_id = _task.versions()
            if _task_project_entity.object() == "asset":
                _asset.append({
                    "id": _task_project_entity.id(),
                    "code": _task_project_entity.code(),
                    "namespace": _namespace,
                    'rfn': _node,
                    'last_cache': "",
                    'project_step_caches': [],
                    'version': _version_id
                })
    return _asset


def asset(task_id):
    # ==================================================================
    # 写入 property assets 属性内容
    _project_entity = task_to_project_entity(task_id)
    _asset = get_assets()
    if _asset and _project_entity:
        _project_entity.update_property("asset", _asset)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


# ==================================================================
# assembly
def get_assemblys():
    _assembly = []
    # 获取reference文件
    _reference_nodes = cmds.ls(rf=True)
    for _node in _reference_nodes:
        _file_path = cmds.referenceQuery(_node, f=True, wcn=True)
        _namespace = cmds.referenceQuery(_node, namespace=True)
        if _namespace.startswith(":"):
            _namespace = _namespace[1::]
        _production_files = zfused_api.zFused.get("production_file_record", filter={
            "Path": _file_path})
        if _production_files:
            _production_file = _production_files[-1]
            _task_id = _production_file.get("TaskId")
            _task = zfused_api.task.Task(_task_id)
            _task_project_entity = _task.project_entity()
            if _task_project_entity.object() == "assembly":
                _assembly.append({
                    "id": _task_project_entity.id(),
                    "code": _task_project_entity.code(),
                    "namespace": _namespace
                })
    return _assembly


def assembly(task_id):
    # ==================================================================
    # 写入 property assemblys 属性内容
    _project_entity = task_to_project_entity(task_id)
    _assembly = get_assemblys()
    if _assembly and _project_entity:
        _project_entity.update_property("assembly", _assembly)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


def get_xgen(task_id):
    _xgen_ = []
    _file_name = cmds.file(q=True, sceneName=True)
    _file_path = os.path.dirname(_file_name)
    if not xgg.Maya:
        return _xgen_
    _all_palettes = xg.palettes()
    _task = zfused_api.task.Task(task_id)
    _task_project_entity = _task.project_entity()
    _task_production_path = _task.production_path()

    # for _palette in _all_palettes:
    #     _palette_dict ={}
    #     _palette_xgen_filename =cmds.getAttr('{}.xgFileName'.format(_palette))
    #     _palette_path =os.path.join(_file_path,_palette_xgen_filename)
    #     _palette_date =xg.getAttr('xgDataPath',_palette)
    #     _palette_dict['_palette_name'] = _palette
    #     _palette_dict['_palette_path'] = _palette_path
    #     _palette_dict['_palette_date'] = _palette_date
    for _palette in _all_palettes:
        _palette_dict = {}
        _palette_xgen_filename = cmds.getAttr('{}.xgFileName'.format(_palette))
        _palette_path = os.path.join(_task_production_path, _palette_xgen_filename).replace('\\', '/')
        _palette_date = xg.getAttr('xgDataPath', _palette)
        _palette_dict['_palette_name'] = _palette
        _palette_dict['_palette_path'] = _palette_path
        _palette_dict['_palette_date'] = _palette_date
        _xgen_.append(_palette_dict)
    return _xgen_


def xgen(task_id):
    _project_entity = task_to_project_entity(task_id)
    # 写入 property xgen 属性内容
    _xgen = get_xgen(task_id)
    if _xgen and _project_entity:
        _project_entity.update_property('xgen', _xgen)
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


def get_gpucache():
    # 获取到所有的gpu
    gpu_caches = []
    _gpu_caches = cmds.ls(type='gpuCache')
    if _gpu_caches:
        for _gpu_cache in _gpu_caches:
            _gpu_cache_path = cmds.getAttr('{}.cacheFileName'.format(_gpu_cache))
            _production_files = zfused_api.zFused.get("production_file_record", filter={
                "Path": _gpu_cache_path})
            if _production_files:
                _production_file = _production_files[-1]
                _task_id = _production_file.get("TaskId")
                _task = zfused_api.task.Task(_task_id)
                _task_project_entity = _task.project_entity()
                _task_project_id = _task_project_entity.id()
                transforms = cmds.listRelatives(_gpu_cache, ap=True)
                for _transform in transforms:
                    _trans_dict = {}
                    _trans_matrix = cmds.xform(_transform, q=True, ws=True, m=True)
                    _trans_vis = cmds.getAttr('{}.visibility'.format(_transform))
                    _trans_dict['transform'] = _transform
                    _trans_dict['gpuCache'] = _gpu_cache
                    _trans_dict['asset_id'] = _task_project_id
                    _trans_dict['transform_matrix'] = _trans_matrix
                    all_connections = cmds.listConnections(_transform)
                    _isrender = True
                    if all_connections:
                        if 'norender' in all_connections:
                            _isrender = False
                    _trans_dict['transform_isrender'] = _isrender
                    gpu_caches.append(_trans_dict)
    return gpu_caches


def gpu_cache(task_id):
    _project_entity = task_to_project_entity(task_id)
    _gpucache = get_gpucache()
    if _gpucache and _project_entity:
        _project_entity.update_property("gpuCache", _gpucache)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)


def camera(task_id):
    _task_entity = zfused_api.task.Task(task_id)
    _project_entity = _task_entity.project_entity()
    _file_code = _project_entity.file_code()
    _cams = cmds.ls("{}*".format(_file_code), fl=1, type="camera")
    _cam_nodes = []
    for _cam in _cams:
        _cam_node = {}
        _cam_tran = cmds.listRelatives(_cam, p=1)[0]
        _cam_node['node'] = _cam_tran
        _cam_nodes.append(_cam_node)
    return _cam_nodes


def camera_node(task_id):
    _project_entity = task_to_project_entity(task_id)
    _cam_nodes = camera(task_id)
    if _cam_nodes and _project_entity:
        _project_entity.update_property("camera", _cam_nodes)
        # write to disk cache
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)



def groom_caching(task_id):
    """
    记录生长面以及相关信息
    :param task_id:
    :return:
    """
    _project_entity = task_to_project_entity(task_id)
    # 写入 property xgen 属性内容
    _groomcacheing = xgens.get_groom_caching_transform_mesh()
    if _groomcacheing and _project_entity:
        _project_entity.update_property('groom_caching', _groomcacheing)
        _data = _project_entity.property()
        _write_to_disk(_project_entity, _data)