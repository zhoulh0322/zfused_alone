# -*- coding: UTF-8 -*-
'''
@Time    : 2020/11/26 15:15
@Author  : Jerris_Cheng
@File    : xgen.py
'''
from __future__ import print_function

import os
import shutil

import maya.cmds as cmds
import xgenm as xg
import xgenm.xgGlobal as xgg

import zfused_api
from zcore import filefunc, zfile
from zfused_maya.core import record
from zfused_maya.node.core import alembiccache

reload(alembiccache)

ATTR = ['uvWrite', 'worldSpace', 'stripNamespaces']
ATTrPREFIX = ['xgen']


def files():
    if xgg.Maya:
        _palettes = xg.palettes()
        if _palettes:
            return True
    return False


def get_path():
    pass


def is_reference(node):
    _is_reference = cmds.referenceQuery(node, isNodeReferenced=True)
    return _is_reference


# 上传xgen文件

def publish_file(path):
    # 获取collection路径并且修改
    _file_infos = []
    if xgg.Maya:
        # 传输xgenfiles
        _collection_path = {}
        _palettes = xg.palettes()
        for _palette in _palettes:
            if not is_reference(_palette):
                _file_path = xg.expandFilepath(xg.getAttr('xgDataPath', _palette), '', False, False)
                # _file_path = xg.getAttr('xgDataPath', _palette)
                # _project_path = xg.getAttr('xgProjectPath',_palette)
                # if not os.path.isdir(_file_path):
                #     _file_path = _file_path.replace("${PROJECT}",_project_path)
                _collection_path[_palette] = _file_path
        if _collection_path:
            for _palette, _src_path in _collection_path.items():
                _tag_path = "{}/xgen/collections/{}".format(path, _palette)
                # 获取path内文件
                for _root, _dirs, _files in os.walk(_src_path):
                    if _files:
                        for _src_file in _files:
                            _src_file = os.path.join(_root, _src_file)
                            _tag_file = _src_file.replace(_src_path, _tag_path)
                            _result = filefunc.publish_file(_src_file, _tag_file)
                            _file_info = zfile.get_file_info(_src_file, _tag_file)
                            _file_infos.append(_file_info)

                # 修改地址
                xg.setAttr('xgDataPath', _tag_path, _palette)
    return _file_infos


def publish_xgen(path):
    _file_infos = []
    if xgg.Maya:
        _collection_path = {}
        _palettes = xg.palettes()
        # 传输 .xgen 文件
        _current_file = cmds.file(q=True, sn=True)
        _file_path = os.path.dirname(_current_file)
        _file_name = os.path.basename(_current_file)
        _file_code, _ = os.path.splitext(_file_name)
        for _palette in _palettes:
            # 获取namesapce
            _src_xgen_file = "{}/{}__{}.xgen".format(_file_path, _file_code, _palette.replace(":", "__"))
            if os.path.isfile(_src_xgen_file):
                _tag_xgen_file = "{}/{}__{}.xgen".format(path, _file_code, _palette.replace(":", "__"))
                _result = filefunc.publish_file(_src_xgen_file, _tag_xgen_file)
                _file_info = zfile.get_file_info(_src_xgen_file, _tag_xgen_file)
                _file_infos.append(_file_info)

    return _file_infos


# 本地化xgen文件

def local_file(path):
    # 获取collection路径并且修改
    _file_infos = []
    if xgg.Maya:
        # 传输xgenfiles
        _collection_path = {}
        _palettes = xg.palettes()
        for _palette in _palettes:
            if not is_reference(_palette):
                _tag_path = "{}/xgen/collections/{}".format(path, _palette)
                # 修改地址
                xg.setAttr('xgDataPath', _tag_path, _palette)
    return _file_infos


def local_xgen(name, src, dst):
    _xgen_files = [
        os.path.join(src, x)
        for x in os.listdir(src)
        if x.startswith(name) and os.path.splitext(x)[1] in [".xgen", "abc"]
    ]
    if _xgen_files:
        for _file in _xgen_files:
            _dst_file = _file.replace(src, dst)
            shutil.copy(_file, _dst_file)

    # xgen path dir
    _src_path = "{}/xgen".format(src)
    if not os.path.isdir(_src_path):
        return
    _tag_path = "{}/xgen".format(dst)
    for _root, _dirs, _files in os.walk(_src_path):
        if _files:
            for _src_file in _files:
                _src_file = os.path.join(_root, _src_file)
                _tag_file = _src_file.replace(_src_path, _tag_path)
                _tag_file_path = os.path.dirname(_tag_file)
                if not os.path.isdir(_tag_file_path):
                    os.makedirs(_tag_file_path)
                shutil.copy(_src_file, _tag_file)


def boundGeometrys():
    """
    获取生长面
    :return: 返回生长面列表
    """
    _grow = {}
    _xgenPalttes = xg.palettes()
    for _paltte in _xgenPalttes:
        _grow_pal = []
        _descs = xg.descriptions(_paltte)
        for _desc in _descs:
            _growmeshs = xg.boundGeometry(_paltte, _desc)
            for _growmesh in _growmeshs:

                if not _growmesh in _grow_pal:
                    full_path = cmds.ls(_growmesh, l=True)
                    _grow_pal.append(_growmesh)
        _grow[_paltte] = _grow_pal
    return _grow


def export_bound_geometry(start, end, dst):
    """
    导出生长面
    :param dst:导出路径
    :return: 所有生长面的abc 路径
    """
    _grow = boundGeometrys()
    abc_jobs = []
    abc_paths = {}

    for k, v in _grow.items():
        _paltte = k
        _growmeshs = v
        _paltte_path = cmds.getAttr('{}.xgFileName'.format(_paltte)).replace('.xgen', '.abc')
        _abc_path = os.path.join(dst, _paltte_path)
        _job = alembiccache.create_frame_cache(_abc_path, start, end, _growmeshs, ATTR, ATTrPREFIX)
        abc_jobs.append(_job)
        abc_paths[_paltte] = _abc_path

    cmds.AbcExport(j=abc_jobs)

    return abc_paths
    # for _file in _file_list:
    #     if _file.endswith(".xgen"):
    #         src_name = os.path.join(src, _file)
    #         dst_name = os.path.join(dst, _file)
    #         shutil.copy(src_name,dst_name)
    #     elif _file == "xgen":
    #         _src_path = "{}/xgen".format(src)
    #         _tag_path = "{}/xgen".format(dst)
    #         # 获取path内文件
    #         for _root, _dirs, _files in os.walk(_src_path):
    #             if _files:
    #                 for _src_file in _files:
    #                     _src_file = os.path.join(_root, _src_file)
    #                     _tag_file = _src_file.replace(_src_path, _tag_path)
    #                     _tag_file_path = os.path.dirname(_tag_file)
    #                     if not os.path.isdir(_tag_file_path):
    #                         os.makedirs(_tag_file_path)
    #                     shutil.copy(_src_file, _tag_file)
    #     else:
    #         continue


# def getCurrentSceneFiles(self):
#     curFileName = self.core.getCurrentFileName()
#     curFileBase = os.path.splitext(os.path.basename(curFileName))[0]
#     xgenfiles = [
#         os.path.join(os.path.dirname(curFileName), x)
#         for x in os.listdir(os.path.dirname(curFileName))
#         if x.startswith(curFileBase) and os.path.splitext(x)[1] in [".xgen", "abc"]
#     ]
#     scenefiles = [curFileName] + xgenfiles
#     return scenefiles


def xgenfile():
    _xgen_node_list = cmds.ls(type="xgmPalette")

    return _xgen_node_list


def getdirxgen(src, dst):
    file_list = os.listdir(src)
    for _file in file_list:
        if _file.endswith(".xgen"):
            src_name = os.path.join(src, _file)
            dst_name = os.path.join(dst, _file)

            shutil.copy(src_name, dst_name)
        else:
            continue


def publishxgen():
    if _getallxgennode()[0] is True:
        _xgennode_list = _getallxgennode()[1]
        for xgen_node in _xgennode_list:
            _xgen_path = _getxgenfile(xgen_node)
            if not os.path.exists(_xgen_path):
                rf_xgen_path = _getrf_xgenfile(xgen_node)
                scene_xgen_path = _getxgenfile(xgen_node)
                transform_xgenfile(rf_xgen_path, scene_xgen_path)

        return True, u"xgen文件已设置成功"
    else:
        return True, "xgen is ok"


def transform_xgenfile(src, dst):
    try:
        new_src = src.replace("\\", "/")
        new_dst = dst.replace("\\", "/")
        shutil.copy(new_src, new_dst)
    except Exception as e:
        print(e)


def _getallxgennode():
    _xgen_node_list = cmds.ls(type="xgmPalette")
    if not _xgen_node_list:
        return False, _xgen_node_list
    return True, _xgen_node_list


def _getrf_xgenfile(xgen):
    _filepath = _getrf_basepath(xgen)
    _xgenname = _getxgenfilename(xgen)
    _filename = _getfilename()
    if str(_xgenname).find(str(_filename)) != -1:
        _newname = _xgenname.replace(_filename + "__", "")
        return os.path.join(_filepath, _newname)
    return os.path.join(_filepath, _xgenname)


def _getscenepath():
    _scenename = cmds.file(q=True, sceneName=True)
    _path = os.path.abspath(os.path.dirname(_scenename))
    return _path


def _isrefernecenode(xgen):
    if cmds.referenceQuery(xgen, isNodeReferenced=True):
        return True
    else:
        return False


def _getrfpath(xgen):
    path = cmds.referenceQuery(xgen, filename=True)
    return path


def _getrf_basepath(xgen):
    path = cmds.referenceQuery(xgen, filename=True)
    abs_path = os.path.abspath(os.path.dirname(path))
    return abs_path


def _getxgenfilename(xgen):
    _filename = cmds.getAttr(xgen + ".xgFileName")
    return _filename


def _getfilename():
    filename = cmds.file(q=True, sceneName=True, shortName=True, ignoreVersion=True, withoutCopyNumber=True)
    _suffix = str(filename).split(".")[-1]
    name = filename.replace(".{}".format(_suffix), "")
    return name


def _getxgenfile(xgen):
    _xgenfilename = cmds.getAttr(xgen + ".xgFileName")
    _shortname = cmds.file(q=True, shortName=True, sceneName=True)
    _scnename = cmds.file(q=True, sceneName=True)

    all_path = _scnename.replace(_shortname, _xgenfilename)
    return all_path


def getdirxgen(src, dst):
    file_list = os.listdir(src)
    for _file in file_list:
        if _file.endswith(".xgen"):
            src_name = os.path.join(src, _file)
            dst_name = os.path.join(dst, _file)

            shutil.copy(src_name, dst_name)
        else:
            continue


def get_file_grow_meshs():
    """
    获取所有的生长面
    :return:
    """
    _growmeshs = []
    _all_palettes = xg.palettes()
    for _palette in _all_palettes:
        _pale_descs = xg.descriptions(_palette)
        for _desc in _pale_descs:
            _grow_meshs = xg.boundGeometry(_palette, _desc)
            for _mesh in _grow_meshs:
                if not _mesh in _growmeshs:
                    _growmeshs.append(_mesh)
    return _growmeshs


def get_all_out_curve_grp():
    """
    获取所有输出曲线组
    :return:
    """
    all_tr = cmds.ls(transforms=True)
    check_list = []
    for tr in all_tr:
        if cmds.objExists('{}.out_curve'.format(tr)) is True:
            if not tr in check_list:
                check_list.append(tr)
    return check_list


def get_outcurve_guide(guide):
    """
    根据引导线获取到对应的输出曲线
    :param guide:
    :return:
    """
    _follicle_curve = get_follicle_curve_guide(guide)
    if _follicle_curve:
        outcurve = get_outcurve_follicle(_follicle_curve)
        return outcurve
    return None


def get_guide_outcurve(outcurve):
    """
    根据输出曲线 获取引导线
    :param outcurve:
    :return:
    """
    _follicle_curve = get_follicle_curve_outcurve(outcurve)
    if _follicle_curve:
        _guide = get_guide_follicle(_follicle_curve)
        return _guide
    return None


def get_follicle_curve_guide(guide):
    """
    根据引导线获取到毛囊曲线，目前似乎只能用名字来区分
    :param guide:
    :return:
    """
    follicle_curve = guide + '_tempCurve'
    if cmds.objExists(follicle_curve):

        return follicle_curve
    else:
        return None


def get_follicle_curve_outcurve(outcurve):
    """
    根据输出曲线获取到毛囊曲线
    :param outcurve:
    :return:
    """
    _curveshape = cmds.listRelatives(outcurve, children=True, type='nurbsCurve', fullPath=True)
    _follicles = cmds.listConnections(_curveshape, destination=True)
    if _follicles:
        _follicle = _follicles[0]
        _follicle_curve = cmds.listRelatives(_follicle, children=True, type='transform')
        if _follicle_curve:
            return _follicle_curve[0]
    return None


def get_guide_follicle(follicle_curve):
    """
    根据毛囊曲线获取引导线
    :param guide:
    :return:
    """
    _guide_curve = str(follicle_curve).replace('_tempCurve', "")
    if cmds.objExists(_guide_curve):
        return _guide_curve
    else:
        return None


def get_outcurve_follicle(follicle_curve):
    """
     根据毛囊曲线获取输出曲线
    :param follicle_curve:
    :return:
    """
    follicle_shape = cmds.listConnections(follicle_curve, destination=True, shapes=True)
    out_curve = cmds.listConnections(follicle_shape, destination=True, source=False, type='nurbsCurve')
    return out_curve


def get_groom_caching_grp():
    """
    获取所有生长面组
    :return:
    """
    grow_mesh_grps = []
    all_tr = cmds.ls(transforms=True, l=True)
    for tr in all_tr:
        if cmds.objExists('{}.groom_caching'.format(tr)) is True:
            if not tr in grow_mesh_grps:
                grow_mesh_grps.append(tr)
    return grow_mesh_grps


def get_follical_curve(follical_shape):
    """
    根据毛囊shape 获取毛囊曲线
    :param follical:
    :return:
    """
    _follicle = cmds.listRelatives(follical_shape, parent=True)
    if _follicle:
        _follicle_curve = cmds.listRelatives(_follicle, children=True, type='transform')
        return _follicle_curve
    return None


def get_groom_caching_transform_mesh():
    """
    获取生长面组、以及transform 和shape 的关系以及命名
    :return:
    """
    _grp = get_groom_caching_grp()
    _all_mesh = get_file_grow_meshs()
    _dict = {}
    _link = []
    for _mesh in _all_mesh:
        _mesh_dict = {}
        _shape = cmds.ls(_mesh, shapes=True, dag=True)
        _mesh_dict[_mesh] = _shape
        _link.append(_mesh_dict)
    _dict['groom_caching_grp'] = _grp
    _dict['meshs_link'] = _link
    return _dict


# def guides(guide):
#     """
#     判断是否为guide
#     :param guide:
#     :return:
#     """
#     _guideshape = cmds.ls(guide,dag=True,shapes= True)
#     if cmds.objectType(_guideshape,isType='xgmSplineGuide'):
#         return True
#     return False


def get_outcurve_desc(desc):
    """
    根据描述找到所有的输出曲线
    根据描述找到引导线，根据引导线找到输出曲线，可以直接忽略组的影响
    :param desc: 描述
    :return:
    """
    _all_guide = xg.descriptionGuides(desc)
    _outcurves = []
    for _guide in _all_guide:
        _outcurve = get_outcurve_guide(_guide)
        if _outcurve:
            _outcurves.append(_outcurve[0])
    return _outcurves


def get_all_palettes():
    """
    获取所有的有效的palettes
    :return:
    """
    palettes = xg.palettes()
    for pale in palettes:
        if "XG_RENDER_:" in pale:
            xg.deletePalette(pale)
            palettes.remove(pale)
    return palettes


def get_growmesh(palette):
    """
    根据集合获取生长面列表
    :param palette:
    :return:
    """
    all_desc = xg.descriptions(palette)
    _mesh_list = []
    for _desc in all_desc:
        grow_mesh_list = xg.boundGeometry(palette, _desc)
        for _mesh in grow_mesh_list:
            lname = cmds.ls(_mesh, l=1)[0]
            _mesh_list.append(lname)
    return _mesh_list
