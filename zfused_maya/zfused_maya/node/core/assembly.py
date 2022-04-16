# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 场景集合操作函数集 """
from __future__ import print_function

import os
import logging

import maya.cmds as cmds
import pymel.core as pm

import zfused_maya.node as node


logger = logging.getLogger(__name__)

# load gpu plugin
_is_load = cmds.pluginInfo("sceneAssembly", query=True, loaded = True)
if not _is_load:
    try:
        logger.info("load scene assembly plugin")
        cmds.loadPlugin("sceneAssembly")
    except Exception as e:
        logger.error(e)


class Assembly(object):
    def __init__(self, name):
        self._assembly_name = name

    def name(self):
        """ get assembly name
        """
        return self._assembly_name

    def create_representation(self, name, retype, infile):
        _ad = cmds.assembly(self._assembly_name, edit = True, 
                                                repName = name,
                                                repLabel = name,
                                                createRepresentation = retype,
                                                input = infile)
        _lr = cmds.assembly(self._assembly_name, q = True, lr = True)
        cmds.setAttr("{}.representations[{}].repLabel".format(self._assembly_name, _lr.index(_ad)), name, type = "string")
        
    def set_active(self, active_string):
        cmds.assembly(self._assembly_name, e = True, active = active_string)

def create_assembly_definition(name):
    """ 创建资产集合节点

    :type: zfused_maya.node.core.assembly.Assembly
    """
    _name = cmds.assembly(name='{}_assemblyDefinition_0001'.format(name))
    return Assembly(_name)

def create_assembly_reference(name, reference_file = None):
    """ 创建资产集合节点

    :type: zfused_maya.node.core.assembly.Assembly
    """
    _name = cmds.assembly(name='{}_assemblyReference_0001'.format(name), type = "assemblyReference")
    #return AssemblyDefinition(_name)
    if reference_file:
        cmds.setAttr('{}.definition'.format(_name), reference_file, type = "string" )

    return Assembly(_name)

def scene_assemblys():        
    def _get_data(_node):
        _py_node = pm.PyNode(_node._node)
        _node_data = {}
        _name = _node._node.split(":")[-1].split("_assemblyReference_")[0]
        _node_data["name"] = _name
        _node_data["namespace"] = _py_node.namespace()
        _node_type = _py_node.type()
        if _node_type == "assemblyReference":
            _lrs = cmds.assembly(_node._node, q = True, lr = True)
            if len(_lrs) == 1:
                _node_type = "transform"
            _definition_file = cmds.getAttr('{}.definition'.format(_node._node))
            _name = os.path.splitext(os.path.basename(_definition_file))[0]
            _node_data["name"] = _name
        _node_data["node_type"] = _node_type
        _node_data["attr"] = _node.get_attr()
        _node_data["xform"] = _node.get_xform()
        _node_data["matrix"] = _node.get_matrix()
        _node_data["child"] = []
        _childs = cmds.listRelatives(_node._node, c = True, typ = ["assemblyReference", "transform"], f = True)
        # get child
        if _childs:
            for _child in _childs:
                _child_node = node.Node(_child)
                _child_data = _get_data(_child_node)
                _node_data["child"].append(_child_data)
        return _node_data
    # get root name
    _assembly_root = []
    _assemblys = pm.ls(type = "assembly", ap = True, )
    for _assembly in _assemblys:
        _root = _assembly.root()
        if _root not in _assembly_root:
            _assembly_root.append(_root)
    # get data
    _assembly_node = []
    for _root in _assembly_root:
        _root_node = node.Node(_root.name())
        _root_data = _get_data(_root_node)
        _assembly_node.append(_root_data)
    return _assembly_node



def fix_to_render():

    def is_reference(node):
        _is_reference = cmds.referenceQuery(node, isNodeReferenced = True)
        return _is_reference


    _gpu_caches = cmds.ls(type = "gpuCache")

    _caches = {}
    for _cache in _gpu_caches:
        _file = cmds.getAttr("{}.cacheFileName".format(_cache))
        if not os.path.isfile(_file):
            continue
        if is_reference(_cache):
            continue
        _caches[cmds.listRelatives(_cache, parent = True)[0]] = _file

    for _name, _file in _caches.items():
        _ai_node = "{}_aiStandin".format(_name)
        
        if not cmds.objExists(_ai_node):
            
            _ass_file = _file.replace(".abc", ".ass").replace("/gpu/", "/ass/")
            if os.path.isfile(_ass_file):
                # _name = cmds.listRelatives(_create_gpu, parent = True)[0]
                _ai_node = cmds.createNode("aiStandIn", parent = _name, n = "{}_aiStandin".format(_name))
                cmds.setAttr("{}.dso".format(_ai_node), _ass_file, type = "string")
                cmds.setAttr("{}.min".format(_ai_node), -1.0000002, -1, -1.0000005, type = "float3")
                cmds.setAttr("{}.max".format(_ai_node), 1, 1, 1.0000001, type = "float3")

        _gpu_node = cmds.listRelatives(_name, c = True, type = "gpuCache")[0]
        
        if cmds.objExists(_ai_node):

            cmds.setAttr('%s.ai_self_shadows'%_gpu_node, 0)
            cmds.setAttr('%s.ai_vidr'%_gpu_node, 0)
            cmds.setAttr('%s.ai_visr'%_gpu_node, 0)
            cmds.setAttr('%s.ai_vidt'%_gpu_node, 0)
            cmds.setAttr('%s.ai_vist'%_gpu_node, 0)
            cmds.setAttr('%s.ai_viv'%_gpu_node, 0)
            cmds.setAttr('%s.primaryVisibility'%_gpu_node, 0)
            cmds.setAttr('%s.castsShadows'%_gpu_node, 0)
            cmds.setAttr('%s.aiOpaque'%_gpu_node, 0)
        
            cmds.setAttr("{}.v".format(_ai_node), k = False)
            cmds.setAttr("{}.standin_draw_override".format(_ai_node), 3)
            cmds.setAttr("{}.covm[0]".format(_ai_node), 0, 1, 1)
            cmds.setAttr("{}.cdvm[0]".format(_ai_node), 0, 1, 1)
            cmds.setAttr("{}.standin_draw_override".format(_ai_node), 3)




def gpu_to_model(is_sel = True):

    if is_sel:
        _sels = cmds.ls(sl = True)
    else:
        _sels = cmds.ls(type = "gpuCache")

    for _sel in _sels:
        # print(_sel)
        if not cmds.objExists("{}.cacheFileName".format(_sel)):
            continue
            
        # get gpu file
        _gpu_file = cmds.getAttr("{}.cacheFileName".format(_sel))
        print(_gpu_file)
        _maya_file = _gpu_file.replace("/gpu/", "/file/").replace(".abc", ".mb")
        if not os.path.isfile(_maya_file):
            _maya_file = _gpu_file.replace("/gpu/", "/file/").replace(".abc", ".ma")
        if not os.path.isfile(_maya_file):
            continue

        print(_maya_file)
        
        _shot_scene_node = "shotscene_instance_grp"
        if not cmds.objExists(_shot_scene_node):
            cmds.createNode("transform", name = _shot_scene_node)
        
        _name = os.path.basename(_gpu_file).split(".")[0]
        _parent_node = "{}_instance_grp".format(_name)
        if not cmds.objExists(_parent_node):
            cmds.createNode("transform", name = _parent_node)
            cmds.parent(_parent_node, _shot_scene_node)
            
        _instance_node = "{}_instance_00".format(_name)
        
        #if not cmds.objExists(_instance_node):
        #    cmds.createNode("transform", name = _instance_node)
        #    cmds.parent(_instance_node, _parent_node)
            
        if not cmds.objExists(_instance_node):
            cmds.createNode("transform", name = _instance_node)
            cmds.parent(_instance_node, _parent_node)
            # refernce file
            _ori_assemblies = cmds.ls(assemblies=True)
            rf = cmds.file(_maya_file, r = True, ns = "{}_instance".format(_name))
            rfn = cmds.referenceQuery(rf, rfn = True)
            #attr.set_node_attr(rfn, _key_output_attr["Id"], _version_handle.id(), "false")
            _new_assemblies = cmds.ls(assemblies=True)
            _asset_tops = list(set(_new_assemblies) - set(_ori_assemblies))
            if _asset_tops:
                for _asset_top in _asset_tops:
                    try:
                        cmds.parent(_asset_top, _instance_node)
                    except:
                        pass
        print(_sel)
        if cmds.nodeType(_sel) == "gpuCache":
            _sel = cmds.listRelatives(_sel, p = True)[0]
        _mt = cmds.xform(_sel, q = True, m = True, ws = True)
        _instance = cmds.instance(_instance_node)[0]
        cmds.xform(_instance, m = _mt, ws = True)
        # cmds.parent(_instance, _parent_node)

    _trans = cmds.ls(type = "transform")

    for _tran in _trans:
        if _tran.endswith("_instance_00"):
            cmds.hide(_tran)






def _test():
    import os
    import maya.api.OpenMaya as OpenMaya


    _assembly_references = cmds.ls(type = "assemblyReference", ap = True)

    _copys = []
    _num_dict = {}
    for _assembly_reference in _assembly_references:
        # old
        # _parents = cmds.listRelatives(_assembly_reference, p = True, ad = True)
        # if len(_parents) > 1:
        #     continue
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(_assembly_reference)
        nodeDagPath = selectionList.getDagPath(0)
        if not nodeDagPath.isInstanced():
            _file_name = cmds.getAttr("{}.definition".format( _assembly_reference ))
            if _file_name not in _num_dict.keys():
                _num_dict[_file_name] = []
            _num_dict[_file_name].append(_assembly_reference)

    for _assembly_references in _num_dict.values():
        if len(_assembly_references) > 1:
            _copys += _assembly_references
    # instance group
    _instance_group = "_instance_grp"
    if not cmds.objExists( _instance_group ):
        cmds.createNode("transform", name = _instance_group)

    _will_instances = []
    for _copy in _copys:
        if cmds.listRelatives(_copy, p = True):
            _p_name = cmds.parent(_copy, w = True)
            _new_names = cmds.parent( _p_name, _instance_group )
        else:
            _new_names = cmds.parent( _copy, _instance_group )
        _will_instances += _new_names

    _instances = {}
    for _will_instance in _will_instances:
        _file_name = cmds.getAttr("{}.definition".format( _will_instance ))
        _base_name = os.path.basename(_file_name)
        _code = os.path.splitext( _base_name )[0]
        if _code not in _instances.keys():
            _ins_grp = cmds.createNode("transform", name = "{}_instance".format(_code))
            # create assembly node
            _name = cmds.assembly(name='{}_assemblyReference_0001'.format(_code), type = "assemblyReference")
            cmds.setAttr('{}.definition'.format(_name), _file_name, type = "string" )
            _lrs = cmds.assembly(_name, q = True, lr = True)
            cmds.assembly(_name, e = True, active = _lrs[0])
            cmds.parent(_name, _ins_grp)
            _instances[_code] = _ins_grp
        _ins_name = _instances[_code]
        # instance copy
        _new_ins_name = cmds.instance(_ins_name)[0]
        
        # get parent rotate scale and vis 
        _tanslate = cmds.getAttr("{}.translate".format(_will_instance) )
        cmds.setAttr("{}.translate".format(_new_ins_name), _tanslate[0][0], _tanslate[0][1], _tanslate[0][2])
        _rotate = cmds.getAttr("{}.rotate".format(_will_instance) )
        cmds.setAttr("{}.rotate".format(_new_ins_name), _rotate[0][0], _rotate[0][1], _rotate[0][2])
        _scale = cmds.getAttr("{}.scale".format(_will_instance) )
        cmds.setAttr("{}.scale".format(_new_ins_name), _scale[0][0], _scale[0][1], _scale[0][2])
        _vis = cmds.getAttr("{}.visibility".format(_will_instance) )
        cmds.setAttr("{}.visibility".format(_new_ins_name), _vis)

    # remove instance
    cmds.delete(_instances.values())
    # remove instance grp
    cmds.delete(_instance_group)
    