# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 材质文件操作集合 """

import os

import maya.cmds as cmds
import maya.mel as mel


def delete_unused():
    #import maya.mel as mel
    mel.eval('MLdeleteUnused;')

def get_connection():
    """ material connection

    :rtype: dict
    """
    matDict = {}
    MaterialList = cmds.ls(materials = True)
    matDict = {}
    for MaterialName in MaterialList: #loop all mats
        if MaterialName in ['lambert1','particleCloud1']:
            continue
        if cmds.objExists(MaterialName + '.outColor') == True:
            ModelList = []
            NodeList = cmds.listConnections(MaterialName + '.outColor', s=0, d=1, type='shadingEngine')
            if NodeList != None:
                for NodeName in NodeList:
                    #if cmds.objectType(NodeName) ==    'shadingEngine': #already filtered
                    PlugList = cmds.listConnections(NodeName, d=0,s=1, plugs=True, shapes=True)
                    for PlugName in PlugList:
                        PlugSplit = PlugName.split('.')
                        #~ if 'instObjGroups' in PlugSplit.split('[')[0]:
                        #~ if MaterialName == 'tou':
                        for tmp in PlugSplit:
                            PlugSplit2 = tmp.split('[')[0]
                            if 'instObjGroups' in PlugSplit2:
                                #~ if MaterialName == 'tou':
                                ReturnedList = []
                                if cmds.objExists(PlugName + '.objectGrpCompList') == True:
                                    ReturnedList = cmds.getAttr(PlugName + '.objectGrpCompList')
                                if len(ReturnedList) == 0:
                                    ModelList.append(PlugSplit[0])
                                elif ReturnedList == [u'vtx[*]']:# todo: problem is about here or next else
                                    ModelList.append(PlugSplit[0])
                                else:
                                    FaceList = ReturnedList
                                    for FaceName in FaceList:
                                        ModelList.append(PlugSplit[0] + '.' + FaceName)
                                break
            matDict[MaterialName] = ModelList
    return matDict

def record():
    matDict = get_connection()        
    # tmpFile = cmds.file(q=1,sceneName=1)
    # cmds.file(save=1) #用于编辑材质文件后重回到模型文件
    for MaterialName in matDict:
        ModelList = matDict[MaterialName]
        if len(ModelList) != 0:
            if cmds.objExists(MaterialName + '.model') == False:
                cmds.addAttr(MaterialName,longName = 'model',dataType = 'string')
            cmds.setAttr(MaterialName + '.model',','.join(ModelList),type = 'string')

def repair_link(element):
    '''修复材质连接
    '''
    _nsnode = element["namespace"]
    import time
    _start = time.time()
    mats = [i for i in cmds.ls(mat = 1) if i.split(":")[0] == _nsnode]
    if not mats:
        return
    for mat in mats:
        _meshattr = "{}.model".format(mat)
        if cmds.objExists(_meshattr):
            meshs = ["{}:{}".format(_nsnode,_i) for _i in cmds.getAttr(_meshattr).split(",")]
            if not meshs:
                continue
            new_meshs = []
            for mesh in meshs:
                # meshtrans = set([cmds.listRelatives(_i.split(".f")[0],p = 1)[0] if cmds.nodeType(_i) == "mesh" else _i for _i in meshs])
                if cmds.nodeType(mesh) == "mesh":
                    meshtrans = cmds.listRelatives(mesh.split(".f")[0],p = 1)[0]
                else:
                    meshtrans = mesh
                new_meshs.extend([mesh.replace(mesh.split(".f")[0],i) for i in cmds.listRelatives(meshtrans,s = 1,ni = 1)])
            if not new_meshs:
                continue
            cmds.select(new_meshs)
            cmds.hyperShade(assign = "lambert1")
            cmds.hyperShade(assign = mat)

    _end = time.time()


class trans_renderinfo(object):
    def __init__(self,src,dst):
        # super(trans_renderinfo,self).__init__(src,dst)
        self.src = src
        self.dst = dst

    def trans_shader(self,copyshader = False):
        _srcns = self.get_namespace(self.src)
        _dstns = self.get_namespace(self.dst)
        mats = self.get_shader(_srcns)
        #print(mats)
        if mats:
            for mat in mats:
                _meshattr = "{}.model".format(mat)
                if cmds.objExists(_meshattr):
                    meshs = ["{}:{}".format(_srcns,_i) for _i in cmds.getAttr(_meshattr).split(",")]
                    if not meshs:
                        continue
                    new_meshs = []
                    for mesh in meshs:
                        if cmds.nodeType(mesh) == "mesh":
                            meshtrans = cmds.listRelatives(mesh.split(".f")[0],p = 1)[0]
                        else:
                            meshtrans = mesh
                        _new_mesh = "{}{}".format(_dstns,meshtrans[len(_srcns):])
                        if cmds.objExists(_new_mesh):
                            new_meshs.append(_new_mesh)
                    if not new_meshs:
                        continue
                    cmds.select(new_meshs)
                    # cmds.hyperShade(assign = "lambert1")
                    # if copyshader:
                    cmds.hyperShade(assign = mat)

    def get_shader(self,namespace):
        # if namespace:
        return [i for i in cmds.ls(mat = 1) if i.split(":")[0] == namespace]
        # else:
        #     return
        #     # 暂不启用
        #     # return [i for i in cmds.ls(mat = 1) if not cmds.referenceQuery(i,inr = 1)]

    def get_namespace(self,grp):
        if cmds.referenceQuery(grp,inr = 1):
            return cmds.referenceQuery(grp,ns = 1)[1:]
        else:
            return grp[:-len(grp.split(":")[-1])-1]


def transform_material(src, dst):
    try:
        _rf_node = cmds.referenceQuery(src, rfn = True)
    except:
        return
    # remove dst original material connect
    _cons = cmds.listConnections("{}".format(dst), p = 1, c = True)
    if _cons:
        #print(_cons)
        for i in range(0, len(_cons), 2):
            _out = _cons[i + 1]
            if cmds.nodeType(_out) == "shadingEngine":
                try:
                    cmds.disconnectAttr(_cons[i], _cons[i+1])
                except:
                    pass

    # get material
    shading_grps = cmds.listConnections(src,type='shadingEngine')
    # get the shaders:
    mats = [cmds.listConnections("{}.surfaceShader".format(i),d = 1)[0] for i in set(shading_grps)]
    # for _shader in shaders:
    for mat in mats:
        cmds.select(mat, r = True)
        try:
            cmds.setAttr("{}.intermediateObject".format(src), 0)
            cmds.hyperShade(objects="")
        except:
            pass
        finally:
            cmds.setAttr("{}.intermediateObject".format(src), 1)
        _meshs = cmds.ls(sl = True, fl = False, ni = False)
        for _mesh in _meshs:
            if _mesh.startswith(src):
                _dst_mesh = _mesh.replace(src, dst)
                #print(_dst_mesh)

                if cmds.objExists(_dst_mesh):
                    _fix_dst_mesh = _dst_mesh
                    try:
                        if ".f" in _dst_mesh:
                            _fix_dst_mesh = _dst_mesh.split(".f")[0]
                        _output_connections = cmds.listConnections(_fix_dst_mesh, s = False, d = True, p = True, c = True, scn = True)
                        for _index, _output_connection in enumerate(_output_connections):
                            if "{}.placeHolderList".format(_rf_node) in _output_connection:
                                cmds.disconnectAttr(_output_connections[_index -1], _output_connections[_index])
                    except:
                        pass
                    cmds.select(_dst_mesh)
                    cmds.hyperShade(assign = mat)


if __name__ == "__main__":
    import zfused_maya.node.core.material as material

    _meshs = cmds.ls(sl = True, type = "mesh", ni = True, dag=True)
    for _mesh in _meshs:
        _transforms = cmds.listRelatives(_mesh, parent = True)
        if _transforms:
            _transform = _transforms[0]
            _rendering_shape = "{}_rendering".format(_transform)
            if not cmds.objExists(_rendering_shape):
                continue
            #print(_rendering_shape)        
            _mat = material.transform_material(_rendering_shape, _mesh)     