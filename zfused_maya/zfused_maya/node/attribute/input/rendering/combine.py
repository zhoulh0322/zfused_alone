# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function


import maya.cmds as cmds


import zfused_api


def asset_material_assign(task_id, material_namespace = "material", alembic_namespace = "alembic"):
    _task = zfused_api.task.Task(task_id)
    _project_entity = _task.project_entity()
    # get asset relatives
    _relatives = zfused_api.zFused.get("relative", filter = {"SourceObject": "asset", "TargetObject": _project_entity.object(), "TargetId": _project_entity.id()})
    if not _relatives:
        return
    for _relative in _relatives:
        _namespace = _relative.get("NameSpace")
        # 按名称给alembic指定材质mat
        _asset_id = _relative.get("SourceId")
        _asset = zfused_api.asset.Asset(_asset_id)
        _property = _asset.property()
        if not _property:
            continue
        material_assign_list = _property.get('material_assign')
        if not material_assign_list:
            continue
        for _mat in material_assign_list:
            cmds.select(cl = True)
            _shape =_mat.get('shape')
            _transform = _mat.get('transform')
            _shader_engine = _mat.get('engine')
            new_trans = '{}__in__{}:{}'.format(_namespace, alembic_namespace, _transform)
            if not cmds.objExists(new_trans):
                continue
            # _mesh_name = cmds.listRelatives(new_trans, c=True, ni=True, type ='mesh')
            # new_shape = '{}__in__alembic:{}'.format(_namespace,_shape)
            # shape_con_list = cmds.listConnections(new_shape, type ='shadingEngine')
            # if 'initialShadingGroup' in shape_con_list:
            #     _shape_attr = '{}.instObjGroups[0]'.format(new_shape)
            #     dst_attr =cmds.connectionInfo(_shape_attr,destinationFromSource=True)[0]
            #     cmds.disconnectAttr(_shape_attr,dst_attr)
            new_shader_engine = '{}__in__{}:{}'.format(_namespace, material_namespace, _shader_engine)
            _faces =_mat.get('faces')
            if _faces:
                for _face in _faces:
                    _face_name = '{}__in__{}:{}.f[{}]'.format(_namespace, alembic_namespace, _transform,_face)
                    if '_' in _face_name:
                        _face_name =_face_name.replace('-',":")
                        cmds.select(_face_name,add=True)
            else:
                cmds.select(new_trans,add=True)
            try:
                _sl = cmds.ls(sl=True)
                if _sl:
                    cmds.sets(_sl, e=True, forceElement = new_shader_engine)
                    cmds.select(cl=True)
            except Exception as e:
                print(e)



def combine(task_id):
    _task = zfused_api.task.Task(task_id)
    _project_entity = _task.project_entity()
    # get asset relatives
    _relatives = zfused_api.zFused.get("relative", filter = {"SourceObject": "asset", "TargetObject": _project_entity.object(), "TargetId": _project_entity.id()})
    if not _relatives:
        return
    for _relative in _relatives:
        _namespace = _relative.get("NameSpace")
        # 按名称给alembic指定材质mat
        _asset_id = _relative.get("SourceId")
        _asset = zfused_api.asset.Asset(_asset_id)
        _property = _asset.property()
        if not _property:
            continue
        material_assign_list = _property.get('material_assign')
        if not material_assign_list:
            continue
        for _mat in material_assign_list:
            cmds.select(cl = True)
            _shape =_mat.get('shape')
            _transform = _mat.get('transform')
            _shader_engine = _mat.get('engine')
            new_trans = '{}__in__alembic:{}'.format(_namespace,_transform)
            # _mesh_name = cmds.listRelatives(new_trans, c=True, ni=True, type ='mesh')
            # new_shape = '{}__in__alembic:{}'.format(_namespace,_shape)
            # shape_con_list = cmds.listConnections(new_shape, type ='shadingEngine')
            # if 'initialShadingGroup' in shape_con_list:
            #     _shape_attr = '{}.instObjGroups[0]'.format(new_shape)
            #     dst_attr =cmds.connectionInfo(_shape_attr,destinationFromSource=True)[0]
            #     cmds.disconnectAttr(_shape_attr,dst_attr)
            new_shader_engine = '{}__in__material:{}'.format(_namespace,_shader_engine)
            print(new_shader_engine)
            _faces =_mat.get('faces')
            if _faces:
                for _face in _faces:
                    _face_name = '{}__in__alembic:{}.f[{}]'.format(_namespace,_transform,_face)
                    if '_' in _face_name:
                        _face_name =_face_name.replace('-',":")
                        cmds.select(_face_name,add=True)
            else:
                cmds.select(new_trans,add=True)
            try:
                _sl = cmds.ls(sl=True)
                cmds.sets(_sl, e=True, forceElement = new_shader_engine)
                cmds.select(cl=True)
            except Exception as e:
                print(e)