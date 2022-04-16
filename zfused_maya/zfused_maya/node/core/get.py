 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import logging

import maya.cmds as cmds

import zfused_api

from zfused_maya.core import record

WORKING_PATH = "/Game"

PRODUCTION_PATH = "{project_production_path}/dcc/"
BACKUP_PATH = "{project_backup_path}/dcc/"

def get_current_project_production_path():
    _project_id = record.current_project_id()
    if not _project_id:
        return None
    _project_handle = zfused_api.project.Project(_project_id)
    return PRODUCTION_PATH.format( project_production_path = _project_handle.production_path().split("/dcc")[0] )

def get_current_project_backup_path():
    _project_id = record.current_project_id()
    if not _project_id:
        return None
    _project_handle = zfused_api.project.Project(_project_id)
    return BACKUP_PATH.format( project_backup_path = _project_handle.backup_path().split("/dcc")[0] )

def get_current_project_cache_path():
    return
    
def get_current_project_support_path():
	_project_id = record.current_project_id()
	if not _project_id:
		return None
	_project_handle=zfused_api.project.Project(_project_id)
	return PRODUCTION_PATH.format( project_production_path = _project_handle.production_path().split("/dcc")[0] ).replace("/dcc","/support/lighting")


def get_work_path_from_task(task_id, absolute = True):
    _task_handle = zfused_api.task.Task(task_id)
    _project_entity_handle = zfused_api.objects.Objects(_task_handle.data()["ProjectEntityType"], _task_handle.data()["ProjectEntityId"])
    if absolute:
        _content_path = unreal.SystemLibrary.get_project_content_directory()
        _work_path = "{}{}".format(_content_path, _project_entity_handle.work_path(absolute = False))
    else:
        _work_path = "{}{}".format(WORKING_PATH, _project_entity_handle.work_path(absolute = False))
    return _work_path