# -*- coding: UTF-8 -*-
'''
@Time    : 2021/11/4 17:03
@Author  : Jerris_Cheng
@File    : position_ui.py
'''

from __future__ import print_function

import json

from Qt import QtWidgets

import maya.cmds as cmds

import zfused_maya.node.core.element as element
import zfused_maya.core.record as record


class postion_ui(object):
    def __init__(self):
        super(postion_ui,self).__init__()
        self._init()

    def _init(self):
        self.project_id =record.current_project_id()
        self.task_id  =record.current_task_id()

    def get_element_list(self):
        element_list =[]
        all_element= cmds.ls(references=1)
        for _element in all_element:
            element_dict = {}
            _namespace =cmds.referenceQuery(_element,namespace=1)
            filename = cmds.referenceQuery(_element,filename=1,withoutCopyNumber=1)
            short_name =cmds.referenceQuery(_element,filename=1,shortName=1,withoutCopyNumber=1)
            print(short_name)
            _version_info =str(short_name).split(".")
            without_version_name =_version_info[0]+"."+_version_info[-1]
            print(without_version_name)
            element_dict["namespace"] =_namespace.replace(":","")
            element_dict["filename"] = filename
            element_dict["project_id"]=self.project_id
            element_dict["task_id"] =self.task_id
            element_dict["short_name"]=short_name
            element_dict["without_name"] =without_version_name
            element_list.append(element_dict)
        return element_list

    def get_rfn_position(self):
        all_element_list= self.get_element_list()
        for _element in all_element_list:
            name_space =_element.get("namespace")
            main_curve ="{}:Main".format(name_space)
            if cmds.objExists(main_curve):
                curve_matrix = cmds.xform(main_curve,q=True,matrix=True)
                _element["matrix"] =curve_matrix

            else:
                cmds.waring("{}绑定大环没找到".format(name_space))

        return all_element_list

    def write_json_dict(self,json_path, _dict):
        try:
            with open(json_path, "w") as f:
                json.dump(_dict, f, sort_keys=True, indent=4, separators=(',', ':'))
                f.close()
        except Exception as e:
            print(e)
            return False

        return True







