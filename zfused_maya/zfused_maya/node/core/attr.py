# coding:utf-8
# --author-- lanhua.zhou

""" zfused maya 内部操作数据记录信息 """

from __future__ import print_function

import os
import logging

import zfused_api

import zfused_maya.core.record as record

import maya.cmds as cmds


ATTRIBUTES = [ "project_id", 
               "link_object", 
               "link_id", 
               "project_step_id", 
               "task_id", 
               "output_attr",
               "output_attr_id", 
               "version", 
               "version_id", 
               "is_local"]


def set_node_attr(node, output_attr_id, version_id, is_local = "false"):
    """ set node version attr 
    
    """
    _is_lock = False
    if cmds.lockNode(node, q = True)[0]:
        _is_lock = True
        # unlock node
        cmds.lockNode(node, l = False)
    for _attr in ATTRIBUTES:
        if not cmds.objExists("%s.%s" % (node, _attr)):
            cmds.addAttr(node, ln = _attr, dt = "string")
            cmds.setAttr("%s.%s" % (node, _attr), e = True, keyable = True)
    if _is_lock:
        cmds.lockNode(node, l=True)

    _version = zfused_api.version.Version(version_id)
    _task = _version.task()

    cmds.setAttr("{}.project_id".format(node), 
                 str(_task.project_id()), 
                 type="string")
    cmds.setAttr("{}.link_object".format(node), 
                 str(_task.project_entity_type()), 
                 type="string")
    cmds.setAttr("{}.link_id".format(node), 
                 str(_task.project_entity_id()), 
                 type="string")
    cmds.setAttr("{}.project_step_id".format(node), 
                 str(_task.project_step_id()), 
                 type="string")
    
    _project_step = _task.project_step()
    if _project_step.is_new_attribute_solution():
        _output_attr_handle = zfused_api.attr.Output(output_attr_id)
    else:
        _output_attr_handle = zfused_api.outputattr.OutputAttr(output_attr_id)
    cmds.setAttr("{}.output_attr".format(node), str(_output_attr_handle.code()), type = "string")
    cmds.setAttr("{}.output_attr_id".format(node), str(output_attr_id), type = "string")
    cmds.setAttr("{}.task_id".format(node), 
                 str(_version.data()["TaskId"]), 
                 type="string")
    cmds.setAttr("{}.version".format(node), str(_version.index()), type = "string")
    cmds.setAttr("{}.version_id".format(node), 
                 str(_version.data()["Id"]), 
                 type="string")
    #is_local = "false"
    cmds.setAttr("{}.is_local".format(node), 
                 str(is_local), 
                 type="string")


def get_node_attr(node):
    """ get not attr data

    """
    _attr_data = {}
    _fix_node(node)
    # if not cmds.objExists("{}.project_id".format(node)):
    #     _fix_node(node)
    #     return 
    if not cmds.objExists("{}.project_id".format(node)):
        # _fix_node(node)
        return _attr_data
    _attr_data["project_id"] = int(cmds.getAttr("%s.project_id" % node))
    _attr_data["project_step_id"] = int(cmds.getAttr("%s.project_step_id" % node))
    _attr_data["task_id"] = int(cmds.getAttr("%s.task_id" % node))
    if cmds.objExists("{}.output_attr_id".format(node)):
        _attr_data["output_attr_id"] = int(cmds.getAttr("{}.output_attr_id".format(node)))
    if cmds.objExists("%s.is_local" % node):
        _attr_data["is_local"] = cmds.getAttr("%s.is_local" % node)
    else:
        _attr_data["is_local"] = "false"
    if cmds.objExists("%s.link_object" % node):
        _attr_data["link_object"] = cmds.getAttr("%s.link_object" % node)
    else:
        _attr_data["link_object"] = cmds.getAttr("%s.object" % node)
    if cmds.objExists("%s.link_id" % node):
        _attr_data["link_id"] = int(cmds.getAttr("%s.link_id" % node))
    else:
        _attr_data["link_id"] = int(cmds.getAttr("%s.id" % node))
    if cmds.objExists("%s.version_id" % node):
        _attr_data["version_id"] = int(cmds.getAttr("%s.version_id" % node))
    else:
        # get version id
        _version_index = int(cmds.getAttr("%s.version" % node))
        _version_data = zfused_api.zFused.get("version", filter = {"TaskId": _attr_data["task_id"], "Index": _version_index})[0]
        _attr_data["version_id"] = int(_version_data["Id"])
    if cmds.objExists("{}.version".format(node)):
        _attr_data["version"] = int(cmds.getAttr("%s.version" % node))
    else:
        _version = zfused_api.version.Version(_attr_data["version_id"])
        _attr_data["version"] = _version.index()

    return _attr_data




def _fix_node(node):
    """ 
    """
    if cmds.nodeType(node) == "reference":
        # get reference file
        _file = cmds.referenceQuery(node, f = True, wcn = True)
        _production_files = zfused_api.zFused.get("production_file_record", filter = {"Path": _file})
        if _production_files:
            _production_file = _production_files[-1]
            _index = _production_file.get("Index")
            _task_id = _production_file.get("TaskId")
            _attr_id = _production_file.get("ProjectStepAttrId")
            _versions = zfused_api.zFused.get("version", filter = {"TaskId": _task_id, "Index": _index})
            set_node_attr(node, _attr_id, _versions[-1]["Id"], is_local = "false")
            return

        _files = []
        _link_files = zfused_api.zFused.get("files", filter = {"LinkObject":"task", "FilePath": _file})
        if _link_files:
            _files += _link_files
        if _files:
            _link_file = _files[-1]
            _task_id = _link_file["LinkId"]
            _index = _link_file["Index"]
            _task = zfused_api.task.Task(_task_id)
            _project_step_id = _task.project_step_id()
            _versions = zfused_api.zFused.get("version", filter = {"TaskId": _task_id, "Index": _index})
            _project_step_handle = zfused_api.step.ProjectStep(_project_step_id)
            _output_attrs = _project_step_handle.output_attrs()
            _step_code = os.path.basename(os.path.dirname(_link_file["FilePath"]))
            for _output_attr in _output_attrs:
                if _step_code == _output_attr["Code"]:
                    _output_attr_id = _output_attr["Id"]
            set_node_attr(node, _output_attr_id, _versions[-1]["Id"], is_local = "false")
            
        # else:
        #     _path = os.path.dirname(_file)
        #     _object_code = os.path.basename(_file.split(".")[0])
        #     _project_id = record.current_project_id()
        #     _object_datas = zfused_api.zFused.get("asset", filter = {"ProjectId": _project_id, "Code":_object_code})
        #     if _object_datas:
        #         _object_handle = zfused_api.objects.Objects("asset", _object_datas[0]["Id"])
        #         if "/rig/" in _file:
        #             _project_step_id = 91
        #         elif "/model/" in _file:
        #             _project_step_id = 90

        #         _versions = _object_handle.project_step_versions(_project_step_id)
        #         set_node_attr(node, _project_step_id, _versions[-1]["Id"], is_local = "false")