# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 关联操作集合 """
from __future__ import print_function
from collections import defaultdict

import os
import sys
import glob
import copy 
import json

import maya.cmds as cmds

import zfused_api

import zfused_maya.core.record as record

from . import attr
from . import element


def create_relatives(scene_elements, task_id, version_id):
    """
    创建项目实体关联
    """
    
    # 这边清除当前任务关联和版本关联合理
    zfused_api.relative.clear_relatives("task", task_id)
    zfused_api.relative.clear_relatives("version", version_id)

    _task = zfused_api.task.Task(task_id)
    # _project_step_id = _task.data()["ProjectStepId"]
    _project_step = _task.project_step()
    _mode_dict = defaultdict(list)

    _project_entity_type = _task.project_entity_type()
    _project_entity_id = _task.project_entity_id()

    for _element in scene_elements:
        if _element["link_object"] != _project_entity_type and _element["link_id"] != _project_entity_id:
            _mode_dict["relative"].append(_element)
        _relationship = _element["relation_ship"]
        _name_space = _element["namespace"]
        # create task task relatives
        zfused_api.relative.create_relatives("task", _element["task_id"], "task", task_id, _relationship, _name_space)
        # create version task relatives
        zfused_api.relative.create_relatives("version", _element["version_id"], "task", task_id, _relationship, _name_space)
        # create version version relatives
        zfused_api.relative.create_relatives("version", _element["version_id"], "version", version_id, _relationship, _name_space)


    if _mode_dict["relative"]:
        # create entity entity relatives 
        # 清除项目实体之间的关联
        
        if not _project_step.refresh_relative():
            return

        zfused_api.relative.clear_relatives(_project_entity_type, _project_entity_id)
        
        for _element in _mode_dict["relative"]:
            _relationship = _element["relation_ship"]
            _name_space = _element["namespace"]
            zfused_api.relative.create_relatives(_element["link_object"], _element["link_id"], _project_entity_type, _project_entity_id, _relationship, _name_space)
        
        if _project_entity_type == "shot":
            # get sequence
            _shot_handle = zfused_api.shot.Shot(_project_entity_id)
            _sequence_id = _shot_handle.data()["SequenceId"]
            if _sequence_id:
                for _element in _mode_dict["relative"]:
                    _relationship = _element["relation_ship"]
                    _name_space = _element["namespace"]
                    zfused_api.relative.create_relatives(_element["link_object"], _element["link_id"], "sequence", _sequence_id, _relationship, _name_space)
            _episode_id = _shot_handle.data().get("EpisodeId")
            if _episode_id:
                for _element in _mode_dict["relative"]:
                    _relationship = _element["relation_ship"]
                    _name_space = _element["namespace"]
                    zfused_api.relative.create_relatives(_element["link_object"], _element["link_id"], "episode", _episode_id, _relationship)


def create_relatives_(task_id = 0):
    """ 创建当前关联信息

    """
    _task_id = task_id
    if not _task_id:
        # get current task id
        _task_id = record.current_task_id()
        if not _task_id:
            return 
    _task = zfused_api.task.Task(_task_id)
    _link_object = _task.project_entity_type()
    _link_id = _task.project_entity_id()

    # # get elements 
    # _element_list = element.scene_elements()
    # _link_object_dict = {}
    # _project_step_dict = {}
    # if _element_list:
    #     for _element in _element_list:
    #         _element_object = _element["link_object"] 
    #         if _element_object not in _link_object_dict.keys():
    #             _link_object_dict[_element_object] = {}
    #         _element_project_step_id = _element["project_step_id"]
    #         if _element_project_step_id not in _link_object_dict[_element_object].keys():
    #             _link_object_dict[_element_object][_element_project_step_id] = []
    #         _link_object_dict[_element_object][_element_project_step_id].append(_element["task_id"])
    #         # _project_step_dict[_element["link_object"]]
    #         # _task_ids += [_element["task_id"] for _element in _element_list]
    # if _link_object_dict:
    #     for _object_key, _object_value in _link_object_dict.items():
    #         _max = []
    #         for _project_step_key, _project_step_value in _object_value.items():
    #             # _max = max(_max, _project_step_value)
    #             _max += _project_step_value
    #         _task_ids += _max

    _task_ids = []
    _element_list = element.scene_elements()
    _link_dict = defaultdict(dict)
    if _element_list:
        for _element in _element_list:
            _link_object_id = "{}_{}".format(_element["link_object"], _element["link_id"])
            if _element["output_attr_id"] not in _link_dict[_link_object_id]:
                _link_dict[_link_object_id][_element["output_attr_id"]] = []
            _link_dict[_link_object_id][_element["output_attr_id"]].append(_element["task_id"])
    if _link_dict:
        for _object_key, _object_value in _link_dict.items():
            #print(_object_value)
            _max = []
            for _project_step_key, _project_step_value in _object_value.items():
                _max = _project_step_value
            _task_ids += _max

    # 测试 可能有问题
    if not _task_ids:
        zfused_api.relative.clear_relatives("task", _task_id)
        _version_id = _task.last_version_id()
        _attrs = []
        _sets = cmds.ls(type = "objectSet")
        for _set in _sets:
            _attr = attr.get_node_attr(_set)
            if _attr:
                zfused_api.relative.create_relatives("version", _attr["version_id"], "task", _task_id)
        return
        
    # 取消
    # _task_ids = list(set(_task_ids))

    # 上一级version版本
    _version_id = _task.last_version_id()
    if _version_id:
        #print(_version_id)
        _version_relatives = zfused_api.zFused.get("relative", filter = {"TargetObject": "version", "TargetId": _version_id})
        if not _version_relatives:
            _task_relatives = zfused_api.zFused.get("relative", filter = {"TargetObject": "task", "TargetId": _task_id, "SourceObject": "version"})
            if _task_relatives:
                for _re in _task_relatives:
                    zfused_api.relative.create_relatives("version", _re["SourceId"], "version", _version_id)

    # clear ori relatives
    zfused_api.relative.clear_relatives("task", _task_id)
    zfused_api.relative.clear_relatives(_link_object, _link_id)
    #zfused_api.relative.clear_relatives("version", 0)

    # create relatives
    for _id in _task_ids:
        # create task relatives
        zfused_api.relative.create_relatives("task", _id, "task", _task_id)
           
        # create object relatives
        _handle = zfused_api.task.Task(_id)
        zfused_api.relative.create_relatives(_handle.project_entity_type(), _handle.project_entity_id(), _link_object, _link_id)

    for _element in _element_list:
        # create version relatives
        zfused_api.relative.create_relatives("version", _element["version_id"], "task", _task_id)

    _version_id = _task.last_version_id()
    _attrs = []
    _sets = cmds.ls(type = "objectSet")
    for _set in _sets:
        #print(_set)
        _attr = attr.get_node_attr(_set)
        if _attr:
            zfused_api.relative.create_relatives("version", _attr["version_id"], "task", _task_id)