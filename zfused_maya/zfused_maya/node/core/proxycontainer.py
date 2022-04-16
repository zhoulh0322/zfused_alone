# # coding:utf-8
# # --author-- binglu.wang

import os
import re
import maya.cmds as cmds

# load gpu plugin
_is_load = cmds.pluginInfo("gpuCache", query=True, loaded = True)
if not _is_load:
    try:
        cmds.loadPlugin("gpuCache")
    except Exception as e:
        print(e)
        # sys.exit()

def create_rs_container(proxypath, gpupath, lock_attr = True):
    def getname(name):
        index = 1
        while True:
            if not cmds.objExists(name):
                return name
            else:
                if name[-1].isdigit():
                    name = name[:-len(re.findall("\d+",name)[-1])]
                name = "{}{}".format(name,index)
            index += 1

    _proxyname = os.path.splitext(os.path.basename(proxypath))[0]
    _gpuname = os.path.splitext(os.path.basename(gpupath))[0]

    _mesh = cmds.polyCube(n = getname("{}_rsProxy".format(_proxyname)),ch = 0)[0]
    _proxynode = cmds.createNode("RedshiftProxyMesh",n = getname(_proxyname))
    _gpunode = cmds.createNode("gpuCache",n = getname(_gpuname),p = _mesh)
    _dagcontainer = cmds.createNode("dagContainer",n = getname("{}_dag".format(_gpuname)),p = _mesh)
    _meshshape = cmds.listRelatives(_mesh,s = 1)[0]

    cmds.addAttr(_mesh,ln = "GPU",at = "bool",k = 1,dv = 1)
    cmds.addAttr(_mesh,ln = "Proxy",at = "enum",en ="boundingBox:previewMesh:linkedMesh:hideInViewport:",k = 1,dv = 3)
    cmds.connectAttr("{}.o".format(_proxynode),"{}.i".format(_meshshape))
    cmds.connectAttr("{}.GPU".format(_mesh),"{}.v".format(_gpunode))
    cmds.connectAttr("{}.Proxy".format(_mesh),"{}.displayMode".format(_proxynode))
    cmds.setAttr("{}.fileName".format(_proxynode),proxypath,type = "string")
    cmds.setAttr("{}.cacheFileName".format(_gpunode),gpupath,type = "string")
    cmds.setAttr("{}.blackBox".format(_dagcontainer),1)
    cmds.setAttr("{}.hiddenInOutliner".format(_dagcontainer),1)
    cmds.container(_dagcontainer,e = 1,an = _gpunode)
    # 锁住属性，防止模型阶段乱操作
    if lock_attr:
        cmds.setAttr("{}.tx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ty".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.tz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ry".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sy".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.v".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
    return _mesh, _proxynode, _dagcontainer



# 删除使用,vray代理不带材质，不能使用此方案
def create_vray_container(proxypath, gpupath, lock_attr = True):
    def getname(name):
        index = 1
        while True:
            if not cmds.objExists(name):
                return name
            else:
                if name[-1].isdigit():
                    name = name[:-len(re.findall("\d+",name)[-1])]
                name = "{}{}".format(name,index)
            index += 1

    _proxyname = os.path.splitext(os.path.basename(proxypath))[0]
    _gpuname = os.path.splitext(os.path.basename(gpupath))[0]

    _mesh = cmds.polyCube(n = getname("{}_vrayProxy".format(_proxyname)),ch = 0)[0]
    _proxynode = cmds.createNode("VRayMesh",n = getname(_proxyname))
    _gpunode = cmds.createNode("gpuCache",n = getname(_gpuname),p = _mesh)
    _dagcontainer = cmds.createNode("dagContainer",n = getname("{}_dag".format(_gpuname)),p = _mesh)
    _meshshape = cmds.listRelatives(_mesh,s = 1)[0]

    # cmds.addAttr(_mesh,ln = "GPU",at = "bool",k = 1,dv = 1)
    # cmds.addAttr(_mesh,ln = "Proxy",at = "enum",en ="boundingBox:previewMesh:linkedMesh:hideInViewport:",k = 1,dv = 3)
    cmds.connectAttr("{}.o".format(_proxynode),"{}.i".format(_meshshape))
    cmds.setAttr("{}.lodVisibility".format(_meshshape), 0)
    # cmds.connectAttr("{}.GPU".format(_mesh),"{}.v".format(_gpunode))
    # cmds.connectAttr("{}.Proxy".format(_mesh),"{}.geomType".format(_proxynode))
    cmds.setAttr("{}.fileName".format(_proxynode),proxypath,type = "string")
    cmds.setAttr("{}.cacheFileName".format(_gpunode),gpupath,type = "string")
    cmds.setAttr("{}.blackBox".format(_dagcontainer),1)
    cmds.setAttr("{}.hiddenInOutliner".format(_dagcontainer),1)
    cmds.container(_dagcontainer,e = 1,an = _gpunode)
    # 锁住属性，防止模型阶段乱操作
    if lock_attr:
        cmds.setAttr("{}.tx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ty".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.tz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ry".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sy".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.v".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
    return _mesh,_proxynode,_dagcontainer

def create_ass_container(proxypath, gpupath, lock_attr = True):
    def getname(name):
        index = 1
        while True:
            if not cmds.objExists(name):
                return name
            else:
                if name[-1].isdigit():
                    name = name[:-len(re.findall("\d+",name)[-1])]
                name = "{}{}".format(name,index)
            index += 1

    _proxyname = os.path.splitext(os.path.basename(proxypath))[0]
    _gpuname = os.path.splitext(os.path.basename(gpupath))[0]

    _mesh = cmds.createNode("transform",n = getname("{}_assProxy".format(_proxyname)))
    _proxynode = cmds.createNode("aiStandIn",n = getname(_proxyname), p = _mesh)
    _gpunode = cmds.createNode("gpuCache",n = getname(_gpuname),p = _mesh)
    _dagcontainer = cmds.createNode("dagContainer",n = getname("{}_dag".format(_gpuname)),p = _mesh)
    _meshshape = cmds.listRelatives(_mesh,s = 1)[0]

    cmds.addAttr(_mesh,ln = "GPU",at = "bool",k = 1,dv = 1)
    # cmds.addAttr(_mesh,ln = "Proxy",at = "enum",en ="boundingBox:previewMesh:linkedMesh:hideInViewport:",k = 1,dv = 3)
    # cmds.connectAttr("{}.o".format(_proxynode),"{}.i".format(_meshshape))
    # cmds.setAttr("{}.lodVisibility".format(_meshshape), 0)
    cmds.connectAttr("{}.GPU".format(_mesh),"{}.v".format(_gpunode))
    # cmds.connectAttr("{}.Proxy".format(_mesh),"{}.geomType".format(_proxynode))
    cmds.setAttr("{}.standInDrawOverride".format(_proxynode),3)
    cmds.setAttr("{}.dso".format(_proxynode),proxypath,type = "string")
    cmds.setAttr("{}.cacheFileName".format(_gpunode),gpupath,type = "string")
    cmds.setAttr("{}.blackBox".format(_dagcontainer),1)
    cmds.setAttr("{}.hiddenInOutliner".format(_dagcontainer),1)
    cmds.container(_dagcontainer,e = 1,an = _gpunode)
    # 锁住属性，防止模型阶段乱操作
    if lock_attr:
        cmds.setAttr("{}.tx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ty".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.tz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.ry".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.rz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sx".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sy".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.sz".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
        cmds.setAttr("{}.v".format(_mesh) ,lock = 1 ,keyable = 0 ,channelBox = 0)
    return _mesh,_proxynode,_dagcontainer

if __name__ == '__main__':
    create_ass_container(r"D:\wblwork\alice\6.19\dragonman3.ass",
                            r"K:\projects\MILI_XYLZ\asset\scenery\unit\A001_Rock_003\A001_Rock_003_GPU.abc")
