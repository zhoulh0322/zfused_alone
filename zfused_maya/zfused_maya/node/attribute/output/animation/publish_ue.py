# coding:utf-8
# --author-- ning.qin
from __future__ import print_function

import os
import sys
import logging
import json

import maya.cmds as cmds
from pymel.core import *

import zfused_api

CAM_KEYWORD_LIST = ['cam']
ASSET_TYPE_LIST = ['char', 'prop', 'env']
#ASSET_TYPE_LIST = ['ch', 'env', 'pr', 'wolf']
ATTR_LIST_TRANSFORM = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
ATTR_LIST_CAM_SHAPE = ['focalLength']
ROOT_NAME = 'Root_M'

def read_json_file(file_path):
    with open(os.path.abspath(file_path), "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict if json_dict else {}
def write_json_file(json_dict, file_path):
    with open(file_path,"w") as json_file:
        json_file.write(json.dumps(json_dict,indent = 4,separators=(',',':'), sort_keys = False))
        json_file.close()

def get_playback_frames(*args):
    start_frame = int(playbackOptions(query = True, minTime = True))
    end_frame = int(playbackOptions(query = True, maxTime = True))
    return start_frame, end_frame

def export_fbx(frame_start, frame_end, fbx_path):
    frame_start = str(frame_start)
    frame_end   = str(frame_end)
    mel.eval('FBXResetExport;')
    mel.eval('FBXExportFileVersion "FBX201800"')
    mel.eval('FBXExportBakeComplexAnimation -v true;')
    mel.eval("FBXExportSplitAnimationIntoTakes -clear;")
    mel.eval('FBXExportConvertUnitString "cm"')
    mel.eval('FBXExportInputConnections -v 0')
    mel.eval('FBXExportSplitAnimationIntoTakes -v \"Take_001\" ' + frame_start + ' ' + frame_end)
    mel.eval('FBXExport -f \"' + fbx_path + '\" -s')

def get_cam_list(*args):
	cam_list = []
	cam_list_all = ls(type = 'camera')
	for cam in cam_list_all:
		for cam_keyword in CAM_KEYWORD_LIST:
			if cam_keyword in str(cam):
			    cam_list.append(listRelatives(cam, parent = True)[0])
	return cam_list

def get_current_frame_value_list(node, attr_list):
    value_list = []
    for attr in attr_list:
        value = getAttr(node + '.' + attr)
        value_list.append(value)
    return value_list

def get_cam_dict(frame_ext = 10):
    cam_old       = get_cam_list()[0]
    cam_shape_old = listRelatives(cam_old, shapes = True)[0]
    cam_new = camera()
    cam_shape_new = cam_new[1]
    cam_new = cam_new[0]
    cam_name = str(cam_old)
    rename(cam_old, str(cam_old) + '1')
    rename(cam_new, cam_name)
    parent(cam_new, cam_old)
    setAttr(cam_new + '.translateX', 0)
    setAttr(cam_new + '.translateY', 0)
    setAttr(cam_new + '.translateZ', 0)
    setAttr(cam_new + '.rotateX', 0)
    setAttr(cam_new + '.rotateY', 0)
    setAttr(cam_new + '.rotateZ', 0)
    focal_length = getAttr(cam_shape_old + '.focalLength')
    setAttr(cam_shape_new + '.focalLength', focal_length)
    parent(cam_new, world = True)
    parentConstraint(cam_old, cam_new, maintainOffset = True, weight = 1)

    cam_export = camera()
    cam_shape_export = cam_export[1]
    cam_export = cam_export[0]
    
    print(get_playback_frames())
    frame_start, frame_end = get_playback_frames()
    frame_start_ext = frame_start - frame_ext
    frame_end_ext = frame_end + frame_ext

    for frame in range(frame_start_ext, frame_end_ext + 1):
        #print(frame)
        currentTime(frame, edit = True)
        t = cam_new.getTranslation('world')
        s = cam_new.getScale()
        
        rotation = cam_new.getRotation()
        rotation = datatypes.EulerRotation([rotation[0], rotation[1], rotation[2]]).asQuaternion()
        rotself = datatypes.EulerRotation([-90.0, 0.0, 0.0]).asQuaternion()
        rotself = rotation * rotself
        rotroot = datatypes.EulerRotation([90.0, 0.0, 0.0]).asQuaternion()
        rotroot = rotself * rotroot
        rotation = rotroot.rotate
        cam_export.setTranslation([t[0], t[2], t[1]])
        cam_export.setRotation(rotroot, quaternion = True)
        cam_export.setScale([s[0], s[2], s[1]])
        setKeyframe(cam_export)
    cam_export_rx = listConnections(cam_export + '.rx', destination = False, source = True)[0]
    cam_export_ry = listConnections(cam_export + '.ry', destination = False, source = True)[0]
    cam_export_rz = listConnections(cam_export + '.rz', destination = False, source = True)[0]
    filterCurve(cam_export_rx, cam_export_ry, cam_export_rz)
    
    cam_value_dict = collections.OrderedDict()
    cam_value_dict['cam_name'] = cam_name
    cam_value_dict['cam_transform_attr'] = ATTR_LIST_TRANSFORM
    cam_value_dict['cam_shape_attr'] = ATTR_LIST_CAM_SHAPE
    #cam_value_dict['frame_range'] = get_playback_frames()
    cam_value_dict['frame_start'] = frame_start_ext
    cam_value_dict['frame_end']   = frame_end_ext
    
    cam_value_list = []
    for frame in range(frame_start_ext, frame_end_ext + 1):
        #print(frame)
        currentTime(frame, edit = True)
        frame_cam_value_list = get_current_frame_value_list(cam_export, ATTR_LIST_TRANSFORM)
        frame_cam_shape_value_list = get_current_frame_value_list(cam_shape_old, ATTR_LIST_CAM_SHAPE)
        frame_value_list = frame_cam_value_list + frame_cam_shape_value_list
        cam_value_list.append(frame_value_list)
        #cam_value_list.append(frame)
    #print(cam_value_list)
    cam_value_dict['cam_value_list'] = cam_value_list
    return cam_value_dict

def joint_children(joint_parent, joint_dict, depth):
    # global joint_count
    # joint_count += 1
    # print('|'),
    # print(' ' * depth * 2),
    # print('|'),
    # print(joint_parent)
    export_joint_name = joint_parent.split(':')[-1]
    export_joint_parent = createNode('joint', name = export_joint_name)
    for attr in ATTR_LIST_TRANSFORM:
        value = getAttr(joint_parent + '.' + attr)
        #setAttr(export_joint_name + '.' + attr, value)
    
    child_node_list = listRelatives(joint_parent, type = 'joint')
    child_list = []
    for node in child_node_list:
        child_list.append(str(node))
    if child_list == []:
        return 'end'
    else:
        depth += 1
        #print(child_list)
        joint_dict[str(joint_parent)] = (child_list, collections.OrderedDict())
        for child in child_list:
            #print(child)
            joint_children(child, joint_dict[str(joint_parent)][1], depth)
            export_joint_child_name = child.split(':')[-1]
            parent(export_joint_child_name, export_joint_parent)

def joint_children_set_attr(joint_parent):
    joint_old = ls(joint_parent)[0]
    joint_new = ls(joint_parent.split(':')[-1])[0]
    #print(joint_new)
    translation = joint_old.getTranslation('world')
    joint_new.setTranslation(translation, 'world')
    rotation = joint_old.getRotation('world')
    joint_new.setRotation(rotation, 'world')
    scale = joint_old.getScale()
    joint_new.setScale(scale)
    setKeyframe(joint_new) 
    child_node_list = listRelatives(joint_parent, type = 'joint')
    child_list = []
    for node in child_node_list:
        child_list.append(str(node))
    if child_list == []:
        return 'end'
    else:
        #print(child_list)
        for child in child_list:
            #print(child)
            joint_children_set_attr(child)

def check_root_joint():
    root_check_dict = collections.OrderedDict()

    for asset_type in ASSET_TYPE_LIST:
        asset_dict = collections.OrderedDict()
        ref_list = ls(references = True)
        if ref_list != []:
            for ref in ref_list:
                try:
                    ref_path = referenceQuery(ref, filename = True)
                    asset_type_dir = '/' + asset_type + '/'
                    if asset_type_dir in ref_path:
                        ref_namespace = referenceQuery(ref, namespace = True).split(':')[-1]
                        root_exist = objExists(ref_namespace + ':' + ROOT_NAME)
                        root_check_dict[ref_namespace] = root_exist
                except:
                    print(ref, '            bad bad')
    return(root_check_dict)

def export_shot(shot_data_dir, frame_ext = 10):
    ogs(pause = True)
    ref_count = 0
    for asset_type in ASSET_TYPE_LIST:
        asset_type_dir = '/' + asset_type + '/'
        ref_list = ls(references = True)
        if ref_list != []:
            for ref in ref_list:
                try:
                    ref_path = referenceQuery(ref, filename = True)
                    if asset_type_dir in ref_path:
                        ref_count += 1
                except:
                    print(ref, '            bad bad')
    #print(ref_count)
    progress_window = window(title = u'大家好我是进度条')
    columnLayout()
    progressControl = progressBar(maxValue = ref_count + 1, width = 300)
    showWindow(progress_window)

    file_name = os.path.splitext(os.path.split(sceneName())[1])[0].split('.')[0]
    version   = 0
    try:
        version   = os.path.splitext(os.path.split(sceneName())[1])[0].split('.')[1]
    except:
        pass
    frame_start, frame_end = get_playback_frames()
    frame_start_ext = frame_start - frame_ext
    frame_end_ext = frame_end + frame_ext

    file_export_list = []

    shot_dict = collections.OrderedDict()
    shot_dict['shot_name'] = file_name
    shot_dict['version']   = version
    shot_dict['maya_file'] = sceneName()
    shot_dict['frame_start'] = frame_start
    shot_dict['frame_end']   = frame_end
    shot_dict['frame_start_ext'] = frame_start_ext
    shot_dict['frame_end_ext']   = frame_end_ext
    cam_dict  = collections.OrderedDict()
    char_dict = collections.OrderedDict()
    shot_dict['cam'] = cam_dict
    
    if get_cam_list():
        cam_value_dict = get_cam_dict(frame_ext)
        cam_name = cam_value_dict['cam_name']
        cam_json_file = shot_data_dir + cam_name + '.json'
        cam_fbx_file  = shot_data_dir + cam_name + '.fbx'
        cam_dict[cam_name] = collections.OrderedDict()
        cam_dict[cam_name]['json'] = cam_json_file
        cam_dict[cam_name]['fbx']  = cam_fbx_file
        print(cam_value_dict)
        write_json_file(cam_value_dict, cam_json_file)
        file_export_list.append(cam_json_file)

        select(cam_name, replace = True)
        export_fbx(frame_start_ext, frame_end_ext, cam_fbx_file)
        file_export_list.append(cam_fbx_file)
        delete(cam_name)
    progressBar(progressControl, edit = True, step= 1)

    for asset_type in ASSET_TYPE_LIST:
        asset_dict = collections.OrderedDict()
        shot_dict[asset_type] = asset_dict
        ref_list = ls(references = True)
        if ref_list != []:
            for ref in ref_list:
                try:
                    ref_path = referenceQuery(ref, filename = True)
                    asset_type_dir = '/' + asset_type + '/'
                    if asset_type_dir in ref_path:
                        #print(ref)
                        #print(ref_path)
                        ref_namespace = referenceQuery(ref, namespace = True).split(':')[-1]
                        print(ref_namespace)
                        asset_name = ref_path.split(asset_type_dir)[1].split('/')[0]
                        #ani_name = file_name + '_' + asset_name
                        ani_name = file_name + '_' + ref_namespace
                        fbx_path = shot_data_dir + ani_name + '.fbx'
                        asset_dict[ref_namespace] = collections.OrderedDict()
                        asset_dict[ref_namespace]['maya_path']  = ref_path
                        asset_dict[ref_namespace]['maya_node']  = str(ref)
                        asset_dict[ref_namespace]['asset_name'] = asset_name
                        asset_dict[ref_namespace]['ani_name']   = ani_name
                        asset_dict[ref_namespace]['fbx_path']   = ''
                        asset_dict[ref_namespace]['root_joint_available'] = True
                        if objExists(ref_namespace + ':' + ROOT_NAME):
                            joint_root = ls(ref_namespace + ':' + ROOT_NAME)[0]
                            #print(joint_root)
                            depth = 0
                            joint_count = 0
                            joint_dict = collections.OrderedDict()
                            joint_children(joint_root, joint_dict, 0)
                            
                            for frame in range(frame_start_ext, frame_end_ext + 1):
                                currentTime(frame, edit = True)
                                joint_children_set_attr(joint_root)
                            select(ROOT_NAME, replace = True)
                            export_fbx(frame_start_ext, frame_end_ext, fbx_path)
                            asset_dict[ref_namespace]['fbx_path'] = fbx_path
                            file_export_list.append(fbx_path)
                            delete(ROOT_NAME)

                            progressBar(progressControl, edit = True, step= 1)
                        else:
                            asset_dict[ref_namespace]['root_joint_available'] = False
                except:
                    print(ref, '            bad bad')
    
    shot_json_file = shot_data_dir + file_name + '.json'
    write_json_file(shot_dict, shot_json_file)
    file_export_list.insert(0, shot_json_file)
    deleteUI(progress_window)

    return file_export_list



def publish(*args, **kwargs):
    _task_id, _output_attr_id = args
    print('publish ue')

    # _output_attr_handle = zfused_api.attr.Output(_output_attr_id)
    # print('_output_attr_handle:             ', _output_attr_handle)
    # _file_format = _output_attr_handle.format()
    # print('_file_format:                    ', _file_format)
    # _suffix = _output_attr_handle.suffix()
    # print('_suffix:                         ', _suffix)
    # _attr_code = _output_attr_handle.code()
    # print('_attr_code:                      ', _attr_code)

    _task = zfused_api.task.Task(_task_id)
    # print('_task:                           ', _task)
    # _path = _task.path()
    # print('_path:                           ', _path)
    _production_path = _task.production_path()
    # print('_production_path:                ', _production_path)
    # _transfer_path = _task.transfer_path()
    # print('_transfer_path:                  ', _transfer_path)
    # _backup_path = _task.backup_path()
    # print('_backup_path:                    ', _backup_path)
    # _work_path = _task.work_path()
    # print('_work_path:                      ', _work_path)
    _project_entity_production_path = _task.project_entity().production_path()
    # print('_project_entity_production_path: ', _project_entity_production_path)
    # _temp_path = _task.temp_path()
    # print('_temp_path:                      ', _temp_path)
    # _file_code = _task.file_code()
    # print('_file_code:                      ', _file_code)
    
    _file_index = "{:0>4d}".format(_task.last_version_index( 0 ))
    # print('_file_index 0: ', _file_index)

    _path = 'layout/toue'
    _production_path = '{}/{}'.format(_project_entity_production_path, _path)
    # _production_path = 'E:/project/bkm3a/toue/publish'
    # print('_production_path:                ', _production_path)
    _publish_file_dir = '{}/{}'.format(_production_path, _file_index)
    # print('_publish_file_dir:               ', _publish_file_dir)

    if not os.path.isdir(_publish_file_dir):
        os.makedirs(_publish_file_dir)
    
    _publish_file_dir = _publish_file_dir + '/'
    export_shot(_publish_file_dir)
    