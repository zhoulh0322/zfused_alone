 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import shutil
import logging
import datetime
import time

import maya.cmds as cmds

import zfused_api

from zcore import filefunc


from zfused_maya.core import progress
import zfused_maya.core.record as record

import zfused_maya.node.core.alembiccache as alembiccache
import zfused_maya.node.core.texture as texture
import zfused_maya.node.core.referencefile as referencefile
import zfused_maya.node.core.attr as attr
import zfused_maya.node.core.element as element
import zfused_maya.node.core.relatives as relatives
import zfused_maya.node.core.xgen as xgen


logger = logging.getLogger(__file__)

# 此函数输入参数需要修改 目前不算合理
def receive_file(argv_task_id, argv_attr_id, argv_attr_code, argv_attr_type, argv_attr_mode, argv_attr_local, task_id = 0, input_attr_id = 0):
    """ receive file
        base receive file script
    :rtype: bool
    """
    if not argv_task_id:
        return
    _task = zfused_api.task.Task(argv_task_id)
    _version_id = _task.last_version_id()
    if not _version_id:
        return
    _production_path = _task.production_path()
    _version = zfused_api.version.Version(_version_id)
    _production_file = _version.production_file()

    _extended_version = 1
    # get attr id
    if input_attr_id:
        _input_attr_handle = zfused_api.inputattr.InputAttr(input_attr_id)
        _extended_version = _input_attr_handle.data().get("ExtendedVersion")

    # get file 
    _input_attr_handle = zfused_api.outputattr.OutputAttr(argv_attr_id)
    _file_index = "{:0>4d}".format(_task.last_version_index())
    _file_suffix = _input_attr_handle.data().get("Suffix")

    if _extended_version:
        # get from production 
        _production_file = zfused_api.zFused.get("production_file", filter = {"TaskId": argv_task_id, "ProjectStepAttrId": argv_attr_id, "Index": int(_file_index)})
        if _production_file:
            _production_file = _production_file[0]["Path"]
        else:
            _production_file = "{}/{}/{}.{}{}".format(_production_path,_input_attr_handle.code(),_task.file_code(),_file_index, _file_suffix)
    else:
        _production_file = "{}/{}/{}{}".format(_production_path,_input_attr_handle.code(),_task.file_code(), _file_suffix)

    # type 
    if argv_attr_type == "reference":
        if argv_attr_local:
            # reference local file
            # download file
            _current_task_id = record.current_task_id()
            _current_task = zfused_api.task.Task(_current_task_id)
            _local_file = "{}/reference/{}".format(_current_task.work_path(), os.path.basename(_production_file))
            _local_dir = os.path.dirname(_local_file)
            if not os.path.isdir(_local_dir):
                os.makedirs(_local_dir)
            # copy file
            filefunc.receive_file(_production_file, _local_file)
            rf = cmds.file(_local_file, r = True, ns = _task.file_code())
            rfn = cmds.referenceQuery(rf, rfn = True)
            attr.set_node_attr(rfn, argv_attr_id, _version_id, "true")
        else:
            # reference server file
            #print(_task.file_code())
            rf = cmds.file(_production_file, r = True, ns = _task.file_code())
            #print("reference")
            rfn = cmds.referenceQuery(rf, rfn = True)
            attr.set_node_attr(rfn, argv_attr_id, _version_id, "false")
    elif argv_attr_type == "import":
        rf = cmds.file(_production_file, i = True, namespace = ":", ra = True, ignoreVersion = True, mergeNamespacesOnClash = True, options = "v=0;", pr = True)
    elif argv_attr_type == "open":
        #print("-------------------open file {}".format(_production_file))
        rf = cmds.file(_production_file, o = True, f = True, pr = True)

    elif argv_attr_type == "replace":
        # change reference step ...
        # get attr project step
        _project_steps = zfused_api.zFused.get("step_attr_output", filter = {"Id": argv_attr_id})
        if _project_steps:
            _project_step_id = _project_steps[0]["ProjectStepId"]
            # get scene elements
            _scene_elements = element.scene_elements()
            if _scene_elements:
                for _element in _scene_elements:
                    try:
                        element.replace_by_step(_element, _project_step_id)
                    except Exception as e:
                        logger.warning(e)
                # save local reference
                for _element in _scene_elements:
                    if _element.has_key("is_local"):
                        try:
                            if _element["is_local"] == "true":
                                #保存本地二级参考
                                _file = cmds.referenceQuery(_element["reference_node"], f = True)
                                cmds.file(_file, f = True, saveReference = True)
                        except:
                            pass
    # elif argv_attr_type == "import":

    # frame
    _project_entity = _task.project_entity()
    _project = zfused_api.project.Project(_task.project_id())
    if isinstance( _project_entity, zfused_api.shot.Shot ):
        # start frame and end frame
        _start_frame = _project_entity.start_frame()
        _end_frame = _project_entity.end_frame()
        cmds.playbackOptions( min = _start_frame, max = _end_frame )
        cmds.currentTime(_start_frame)


@progress.progress(u"领取版本文件")
def receive_version_file(version_id):
    """ receive version file 
        if not has versions,assembly new file
    :rtype: bool
    """

    progress.set_range(0, 5)

    # 按照版本领取文件
    _version = zfused_api.version.Version(version_id)
    _version_backup_file = _version.backup_file()
    _version_work_file = _version.work_file()
    _task = zfused_api.task.Task(_version.data().get("TaskId"))

    _project_step = _task.project_step()
    _key_attr = _project_step.key_output_attr()
    _format = _key_attr.get("Format")
    _suffix = _key_attr.get("Suffix")
    
    print(_version_backup_file)
    if not os.path.isfile(_version_backup_file):
        # if _suffix == ".ma" and os.path.splitext(_version_backup_file)[-1] == ".ma":
        _version_backup_file = _version_backup_file.replace(".ma", ".mb")
        if not os.path.isfile(_version_backup_file):
            _version_backup_file = _version_backup_file.replace(".mb", ".ma")

    # if _task.project_entity_type() == "asset":
    #     _maya_asset_work_format = _project.variables("maya_asset_work_format", "mayaBinary")
    #     _format = _maya_asset_work_format
    #     _file_suffix = "mb"
    #     _version_backup_file = _version_backup_file.replace(".ma", ".mb")
    #     _version_work_file = _version_work_file.replace(".ma", ".mb")
    # else:
    #     _format = "mayaAscii"
    #     _file_suffix = "ma"
    #     _version_backup_file = _version_backup_file.replace(".mb", ".ma")
    #     _version_work_file = _version_work_file.replace(".mb", ".ma")

    _name, _suffix = os.path.splitext(_version_work_file)
    _user = zfused_api.user.User(zfused_api.zFused.USER_ID)
    _name = "{}.{}".format(_name, _user.code())
    _version_work_dir = os.path.dirname(_version_work_file)
    _files = []
    if os.path.isdir(_version_work_dir):
        _files = os.listdir(_version_work_dir)
    if _files:
        _file_name = os.path.basename(_name)
        _files = [_file for _file in _files if _file.startswith( _file_name )]
        # if not _files:
        #     _files = []
        _name = "{}.{:>04d}".format(_name, len(_files))
    else:
        _name = "{}.{:>04d}".format(_name, 0)
    _version_work_file = "{}{}".format(_name, _suffix)

    # 备份文件
    progress.set_label_text(u"1/5 - 备份已存在文件")
    progress.set_value(1)

    _backup_file(_version_work_file)
    # 设置帧速率
    _project = zfused_api.project.Project(_version.data()["ProjectId"])
    _change_time_mode(_project.config["Fps"])

    # copy backup file to work file
    _version_work_dir = os.path.dirname(_version_work_file)
    if not os.path.isdir(_version_work_dir):
        os.makedirs(_version_work_dir)

    # _work_in_backup = _project.variables("work_in_backup")
    # if not _work_in_backup:

    
    # 是否本地话数据
    # is_local_backup_data
    # is_publish_backup_data

    _is_sync_backup_external_files = _project.variables("is_sync_backup_external_files", 1)
    print(_is_sync_backup_external_files)
    if _is_sync_backup_external_files:

        shutil.copy(_version_backup_file, _version_work_file)

        # local xgen
        _file_name = os.path.splitext(os.path.basename(_version_backup_file))[0]
        xgen.local_xgen(_file_name, os.path.dirname(_version_backup_file), _version_work_dir)
        try:
            cmds.file(_version_work_file, o = True, f = True)
        except:
            pass
        xgen.local_file(_version_work_dir)
        # local reference file
        progress.set_label_text(u"2/5 - 本地化reference文件")
        progress.set_value(2)
        _task = zfused_api.task.Task(_version.data()["TaskId"])
        _work_path = _task.work_path()
        _files = referencefile.files()
        if _files:
            _path_set = referencefile.paths(_files)[0]
            _intersection_path = max(_path_set)
            referencefile.local_file(_files, _intersection_path, _work_path + "/reference")
            _file_nodes = referencefile.nodes()
            if _file_nodes:
                referencefile.change_node_path(_file_nodes, _intersection_path, _work_path + "/reference")
        # local texture
        progress.set_label_text(u"3/5 - 领取贴图")
        progress.set_value(3)
        _task = zfused_api.task.Task(_version.data()["TaskId"])
        _work_path = _task.work_path()
        _texture_files = texture.files()
        if _texture_files:
            _path_set = texture.paths(_texture_files)[0]
            _intersection_path = max(_path_set)
            texture.local_file(_texture_files, _intersection_path, _work_path + "/texture")
            _file_nodes = texture.nodes()
            if _file_nodes:
                texture.change_node_path(_file_nodes, _intersection_path, _work_path + "/texture")
        # local alembic cache
        progress.set_label_text(u"4/5 - 本地化alembic文件")
        progress.set_value(4)
        _alembic_files = alembiccache.files()
        if _alembic_files:
            _path_set = alembiccache.paths(_alembic_files)[0]
            _intersection_path = max(_path_set)
            alembiccache.local_file(_alembic_files, _intersection_path, _work_path + "/cache/alembic")
            _file_nodes = alembiccache.nodes()
            if _file_nodes:
                alembiccache.change_node_path(_file_nodes, _intersection_path, _work_path + "/cache/alembic")   
    else:
        cmds.file(_version_backup_file, o = True, f = True)
        cmds.file(rename = _version_work_file)
        cmds.file(save = True, options = "v=0;", f = True, type = _format)

    # wireframe
    viewport = cmds.getPanel( withFocus = True)
    if 'modelPanel' in viewport:
        cmds.modelEditor( viewport, edit = True, displayAppearance = "wireframe" )

    # # create relatives
    # _scene_elements = element.scene_elements()
    # relatives.create_relatives(_scene_elements, _version.data()["TaskId"], version_id)

    # 记录领取数据
    progress.set_label_text(u"5/5 - 记录领取数据")
    progress.set_value(5)

    _task = _task
    _project = _task.project()
    _project_entity = _task.project_entity()
    _file_check = {
        "project_id" : _project.id(),
        "project_entity_type" : _project_entity.object(),
        "project_entity_id" : _project_entity.id(),
        "version_index" : _version.index()
    }
    if not cmds.objExists("defaultResolution.file_check"):
        cmds.addAttr("defaultResolution", ln = "file_check", dt = "string")
        cmds.setAttr("defaultResolution.file_check", e = True, keyable = True)
    cmds.setAttr("defaultResolution.file_check", "{}".format(_file_check), type = "string" )

    return True


def assembly_file(task_id):
    """ assembly new task file
    :rtype: None
    """
    task_id = task_id
    import maya.cmds as cmds
    cmds.file(new = True, f = True)

    _task = zfused_api.task.Task(task_id)
    _project_step_id = _task.project_step_id()

    # 设置帧速率
    _project = zfused_api.project.Project(_task.data()["ProjectId"])
    _change_time_mode(_project.config["Fps"])

    # file name
    _work_path = _task.work_path()
    _version = "%04d"%(_task.last_version_index() + 1) 

    # 需要修改 改成带 制作人员名字 和 版本
    _user = zfused_api.user.User(zfused_api.zFused.USER_ID)
    _name = "{}.{}.{}".format(_task.file_code(), _version, _user.code())
    _files = []
    if os.path.isdir(_work_path):
        _files = os.listdir(_work_path)
    # _files = os.listdir(_work_path)
    if _files:
        _files = [_file for _file in _files if _file.startswith( _name )]
        if not _files:
            _files = []
        _name = "{}.{:>04d}".format(_name, len(_files))
    else:
        _name = "{}.{:>04d}".format(_name, 0)

    # 可以从key output获取
    # if _task.project_entity_type() == "asset":
    #     _format = "mayaBinary"
    #     _file_name = "%s/%s.mb"%(_work_path, _name)
    # else:    
    #     _format = "mayaAscii"
    #     _file_name = "%s/%s.ma"%(_work_path, _name)

    _project_step = _task.project_step()
    _key_attr = _project_step.key_output_attr()
    _format = _key_attr.get("Format")
    _suffix = _key_attr.get("Suffix")
    _file_name = "{}/{}{}".format(_work_path, _name, _suffix)
    
    _file_dir = os.path.dirname(_file_name)
    if not os.path.isdir(_file_dir):
        os.makedirs(_file_dir)
 
    # BACKUP FILE 
    # 如果存在同名文件则备份
    _backup_file(_file_name)

    cmds.file(rename = _file_name)

    # init 初始化脚本
    _project_step = _task.project_step()
    _init_script = _project_step.init_script()
    if _init_script:
        # global task_id
        exec(_init_script)

    cmds.file(rename = _file_name)

    # 获取输入属性
    _input_attrs = _project_step.input_attrs()
    _is_new_attribute_solution = _project_step.is_new_attribute_solution()

    # get input task
    _input_tasks = _task.input_tasks()
    _input_attr_ids = [_input_task["Id"] for _input_task in _input_attrs]


    
    # zfused link sets
    _sets = cmds.sets(name = "zfused_link_sets", em = True)
    print(_sets)
    cmds.lockNode(_sets, l = True)
    _child_sets = []
    
    if _input_tasks:
        if _is_new_attribute_solution:
            _task_id = task_id

            _task_attr_conn_ids = []
            _task_attr_conn_ids = _input_tasks.keys()

            # for _task_attr_conn_id in _task_attr_conn_ids:
            #     if _task_attr_conn_id not in _task_attr_conn_ids:
            #         _task_attr_conn_ids.append(_task_attr_conn_id)

            _exec_scripts = []
            
            print(_task_attr_conn_ids)

            for _task_attr_conn_id in _task_attr_conn_ids:
                _task_list = _input_tasks[ _task_attr_conn_id ]
                _attr_conn = zfused_api.zFused.get_one("attr_conn", _task_attr_conn_id)
                _task_attr_input = zfused_api.attr.Input(_attr_conn.get("AttrInputId"))
                _script = _task_attr_input.script()
                for _input_task in _task_list:
                    _input_task_id = _input_task["Id"]
                    _argv = {
                        "task_id" : _task_id,
                        "task_attr_input_id": _attr_conn.get("AttrInputId"),
                        "input_task_id": _input_task_id,
                        "input_task_attr_output_id": _attr_conn.get("AttrOutputId"),
                        "namespace": _input_task.get("NameSpace")
                    }
                    
                    args = (_task_id, _attr_conn.get("AttrInputId"), _input_task_id, _attr_conn.get("AttrOutputId"), _input_task.get("NameSpace"))
                    kwargs = _argv
                    print(args)
                    print(kwargs)
                    print(_script)
                    # 动态创建类
                    try:
                        exec(_script)
                    except:
                        pass
        else:

            _input_task_attr_ids = _input_tasks.keys()
            for _input_task_attr_id in _input_task_attr_ids:
                if _input_task_attr_id not in _input_attr_ids:
                    _input_attr_ids.append(_input_task_attr_id)

            for _input_attr_id in _input_attr_ids:
                _task_list = _input_tasks[ _input_attr_id ]
                logger.info("{}".format(_input_attr_id))
                _input_attr_handle = zfused_api.inputattr.InputAttr(_input_attr_id)
                _script = _input_attr_handle.data()["Script"]
                for _input_task in _task_list:
                    _task_id = _input_task["Id"]
                    _argv = {
                        "argv_task_id" : _task_id,
                        "argv_attr_id" : _input_attr_handle.data()["StepAttrId"],
                        "argv_attr_code" : _input_attr_handle.data()["Code"], 
                        "argv_attr_type" : _input_attr_handle.data()["Type"], 
                        "argv_attr_mode" : _input_attr_handle.data()["Mode"],
                        "argv_attr_local": _input_attr_handle.data()["IsLocal"],
                        "task_id": _task_id,
                        "input_attr_id": _input_attr_id,
                    }
                    # 动态创建类
                    exec(_script, _argv)
                    if _input_attr_handle.data()["Type"] == "custom":
                        _input_task = zfused_api.task.Task(_task_id)
                        _project_step = zfused_api.step.ProjectStep(_input_task.data()["ProjectStepId"])
                        _last_version_id = _input_task.last_version_id()
                        if _last_version_id:
                            _set = cmds.sets(name = _input_task["Name"], em = True)
                            attr.set_node_attr(_set, _project_step.key_output_attr()["Id"], _last_version_id)
                            cmds.sets(_set, edit = True, fe = _sets)
                            cmds.lockNode(_set, l = True)
                            _child_sets.append(_set)
    try:
        if not _child_sets:
            cmds.lockNode(_sets, l = False)
            cmds.delete(_sets)
    except:
        pass
    
    cmds.file(rename = _file_name)

    # combine 最终组合脚本
    _attr_input_combines = zfused_api.zFused.get("attr_input_combine", filter = {"ProjectStepId": _project_step_id})
    if _attr_input_combines:
        for _attr_input_combine in _attr_input_combines:
            _script = _attr_input_combine.get("Script")
            exec(_script)

    # init 初始化脚本
    _combine_script = _project_step.combine_script()
    if _combine_script:
        # global task_id
        print(_combine_script)
        exec(_combine_script)

    # wireframe
    # viewport = cmds.getPanel( withFocus = True)
    # if 'modelPanel' in viewport:
    #     cmds.modelEditor( viewport, edit = True, displayAppearance = "wireframe" )

    # 设置画面分辨率
    cmds.setAttr("defaultResolution.width", _project.config.get("ImageWidth"))
    cmds.setAttr("defaultResolution.height", _project.config.get("ImageHeight"))

    _project_entity = _task.project_entity()
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", _project_entity.image_path(), type = "string")

    cmds.file(save = True, options = "v=0;", f = True, type = _format)

    # 测试，全新领取文件可能会出错
    # 记录领取数据
    _project = _task.project()
    _project_entity = _task.project_entity()
    _file_check = {
        "project_id" : _project.id(),
        "project_entity_type" : _project_entity.object(),
        "project_entity_id" : _project_entity.id(),
        "version_index" : len(_task.versions())
    }
    if not cmds.objExists("defaultResolution.file_check"):
        cmds.addAttr("defaultResolution", ln = "file_check", dt = "string")
        cmds.setAttr("defaultResolution.file_check", e = True, keyable = True)
    cmds.setAttr("defaultResolution.file_check", "{}".format(_file_check), type = "string" )

    # create relatives
    # 先取消记录 关联关系 后期领取总是判定错误
    # relatives.create_relatives()

    # 设置镜头起始结束帧
    _project_entity = _task.project_entity()
    if isinstance( _project_entity, zfused_api.shot.Shot ):
        _start_frame = _project_entity.start_frame()
        _end_frame = _project_entity.end_frame()
        cmds.playbackOptions( min = _start_frame, max = _end_frame )
        cmds.currentTime(_start_frame)


    return True


# 备份
def _backup_file(ori_file):
    """ backup files
    """
    if not os.path.isfile(ori_file):
        return

    _dir = os.path.dirname(ori_file)
    _time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    _backup_dir = "{}/backup/{}".format(_dir, _time_str)
    if not os.path.isdir(_backup_dir):
        os.makedirs(_backup_dir)

    _file_name = os.path.basename(ori_file)
    _name = os.path.splitext(_file_name)[0]

    _xgen_files = [
        os.path.join(_dir, x)
        for x in os.listdir(_dir)
        if x.startswith(_name) and os.path.splitext(x)[1] in [".xgen", "abc"]
    ]

    if _xgen_files:
        for _file in _xgen_files:
            _dst_file = _file.replace(_dir, _backup_dir)
            shutil.copy(_file, _dst_file)
            # remove src file
            os.remove(_file)

    # copy file and rename 
    # _suffix = os.path.splitext(_file_name)
    # new name
    # _new_name = "{}.{}.{}".format(_suffix[0], _time_str, _suffix[-1])
    _new_file = "{}/{}".format(_backup_dir, _file_name)
    shutil.copy(ori_file, _new_file)


def _change_time_mode( fps ):
    '''切换当前场景帧速率,type(mode) = string
        模式对照
        24fps ： film
        25fps ： pal
        30fps ： ntsc
    '''
    _dict = {
        24: "film",
        25: "pal",
        30: "ntsc"
    }
    _mode = _dict[fps]
    cmds.currentUnit( time = _mode )