# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import time
import logging

import maya.cmds as cmds

import zfused_api

from zcore import filefunc,zfile

from zfused_maya.core import progress
from zfused_maya.core import record

from zfused_maya.node.core import yeti, check, alembiccache, texture, referencefile, relatives, element, xgen
reload(xgen)

from zfused_maya.ui.widgets import checkwidget

logger = logging.getLogger(__file__)


@progress.progress(u"上传文件。。。")
def publish_file(task_id, infomation={}, is_auto=False):
    """ publish file
    :rtype: bool
    """
    _start_time = time.time()

    # 进度条设置区间
    progress.set_range(0, 4)

    # 写入当前任务
    record.write_task_id(task_id)

    cmds.file(lf = 0)
    cmds.file(save = True, f = True, options = "v=0;")
    _current_file = cmds.file(q=True, sn=True)

    _task = zfused_api.task.Task(task_id)
    _project_entity = _task.project_entity()
    _project_step = _task.project_step()
    _output_scripts = _project_step.output_attrs()
    _is_new_attribute_solution = _project_step.is_new_attribute_solution()

    if not is_auto:
        # 查看文件是否为领取上传
        if not _task.data().get("IsOutsource"):
            _versions = _task.versions()
            if _versions:
                _last_version = _versions[-1]
                if _last_version.get("IsApproval"):
                    if zfused_api.zFused.USER_ID != _last_version.get("CreatedBy"):
                        _is_error = False
                        if not cmds.objExists("defaultResolution.file_check"):
                            _is_error = True
                        else:
                            _file_check = cmds.getAttr("defaultResolution.file_check")
                            _file_check = eval( _file_check )
                            if _file_check.get("version_index") != _last_version.get("Index"):
                                _is_error = True
                        if _is_error:
                            cmds.confirmDialog(message=u"未领取最新提交版本文件修改")
                            return

        # # 查看雷区
        # _forbidden_script = _project_step.forbidden_script()
        # if _forbidden_script:
        #     forbidden_value = True
        #     exec(_forbidden_script)
        #     if not forbidden_value:
        #         return
        
        # 检查节点
        progress.set_label_text(u"1/4 - 文件上传检查")
        progress.set_value(1)

        _project_step_checks = _project_step.checks()
        if _project_step_checks:
            _ui = checkwidget.CheckWidget(_project_step_checks)
            if not check.Check.value:
                _ui.show()
            if check.Check.value == True:
                _ui.close()
                check.Check.value = False
            else:
                return False
        else:
            # 逐渐省略。。。
            # 检查
            _check_script = _project_step.check_script()
            if _check_script and len(_check_script) != 1:
                if not check.Check.value:
                    exec(_check_script)
                if check.Check.value == True:
                    check.Check.value = False
                else:
                    return False

    # 获取场景信息
    _scene_elements = element.scene_elements()

    # 更新propertry
    _property_script = _project_step.property_script()
    if _property_script:
       # global project_entity,task_id
        project_entity = _task.project_entity()
        exec(_property_script)

    # 运算脚本
    compute_result = {}
    _compute_script = _project_step.data().get("ComputeScript")
    exec(_compute_script)
    _record = compute_result

    # # 提交关联信息
    # relatives.create_relatives()

    # 提交预览信息
    if "video" in infomation:
        if infomation["video"]:
            _approval_file = infomation["video"]
        else:
            _approval_file = infomation["thumbnail"]
    else:
        _approval_file = infomation["thumbnail"]
    _zfile = zfile.LocalFile(_approval_file, "approval")
    _res = _zfile.upload()
    if _res:
        thumbnail_path = _zfile._cloud_thumbnail_path
        _task.update_thumbnail_path(thumbnail_path)
    _thumbnail_path = _zfile._cloud_thumbnail_path


    # 上传备份文件
    progress.set_label_text(u"2/4 - 上传备份文件")
    progress.set_value(2)

    _value = publish_backup(task_id, infomation)
    if not _value:
        cmds.confirmDialog(message=u"上传备份文件失败")
        return False

    
    progress.set_label_text(u"3/4 - 上传自定义数据文件")
    progress.set_value(3)

    # 运行自定义脚本
    if _output_scripts:
        for _output_script in _output_scripts:
            publish_result = False
            _output_entity_type = _task.project_entity_type()
            _output_entity_id = _task.project_entity_id()
            _output_attr_id = _output_script["Id"]
            # 为了兼容新旧attribute 需要设定 _is_new_attribute_solution
            kwargs = {"is_new_attribute_solution": _is_new_attribute_solution}
            if _is_new_attribute_solution:
                args = (task_id, _output_attr_id)
            else:
                args = (_output_entity_type, _output_entity_id, _output_attr_id)
            # run scrpt
            zfused_api.zFused.RESET = True
            print(args)
            print(kwargs)
            print(_output_script["Script"])
            exec(_output_script["Script"])
            zfused_api.zFused.RESET = False
            if not publish_result:
                cmds.confirmDialog(message=u"发布失败 \n{}".format(_output_script["Script"]))
                cmds.file(_current_file, o=True, f=True, pmt=False)
                return False

    # 此处获取信息 是主 file 文件
    _key_output_attr = _project_step.key_output_attr()
    _file_suffix = _key_output_attr["Suffix"].replace(".", "")

    _name = _task.file_code()
    
    _index = "%04d" % (_task.last_version_index() + 1)
    _file_name = "/{}.{}.{}".format(_name, _index, _file_suffix)
    _video_file = infomation["video"]
    _video_name = None
    if _video_file:
        _video_suffix = os.path.splitext(_video_file)[-1]
        _video_name = "/%s.%s%s" % (_name, _index, _video_suffix)
    _thumbnail_file = infomation["thumbnail"]
    _thumbnail_suffix = os.path.splitext(_thumbnail_file)[-1]
    _thumbnail_name = "/%s.%s%s" % (_name, _index, _thumbnail_suffix)

    # 提交审批数据
    progress.set_label_text(u"4/4 - 提交数据库")
    progress.set_value(4)

    _introduction = {}
    _introduction["msgtype"] = "rich-text"
    _introduction["text"] = infomation["description"]
    _introduction["image"] = []
    _image_data = {}
    _image_data["path"] = _zfile._cloud_thumbnail_path
    _size = _zfile.get_local_thumbnail_size()
    _image_data["width"] = _size[0]
    _image_data["height"] = _size[1]
    _image_data["file_type"] = _zfile.file_type()
    _image_data["file_format"] = _zfile.file_format()
    _image_data["file_name"] = _zfile.file_name()
    _image_data["file_md5"] = _zfile.file_md5()
    _introduction["image"].append(_image_data)
    _publish_time = int(time.time() - _start_time)
    _record["publish_time"] = _publish_time    
    _v, _info = _task.submit_approval( "{}.{}".format(_name, _index),
                                       _file_name,
                                       zfused_api.zFused.USER_ID,
                                       _project_step.approvalto_user_ids(),
                                       _project_step.cc_user_ids(),
                                       _video_name,
                                       _thumbnail_name,
                                       _thumbnail_path,
                                       infomation["description"],
                                       str(_introduction),
                                       str(_record) )
    if not _v:
        cmds.confirmDialog(message=u"上传数据库信息失败 {}".format(_info))
        return False

    # 提交关联信息
    _version_id = _v
    relatives.create_relatives(_scene_elements, task_id, _version_id)

    # 更新关联任务 产品级 测试
    # 特别占资源 再取得好的解决方案之前 先取消
    # _tasks = zfused_api.zFused.get("relative", filter = {"SourceObject":"task", "SourceId":task_id, "TargetObject":"task"})
    # if _tasks:
    #     for _task in _tasks:
    #         _relative_task = zfused_api.task.Task(_task["TargetId"])
    #         _relative_task.update_is_production(-1)

    _task.analy_is_production()
    _task.update_is_production(_task.is_production())

    # # 修改任务状态为审查中
    # _review_ids = zfused_api.status.review_status_ids()
    # if _review_ids:
    #     _task.update_status(_review_ids[0])

    # 打开空文件
    cmds.file(new=True, f=True)

    if not is_auto:
        # 上传结果ui
        cmds.confirmDialog(message=u"上传成功")
        return True

    return False


def batch_alone_publish_file(task_id, infomation={}, is_auto=False):
    """ publish file

    :rtype: bool
    """
    _current_file = cmds.file(q=True, sn=True)
    _task = zfused_api.task.Task(task_id)
    _project_entity = _task.project_entity()
    _project_step = zfused_api.step.ProjectStep(_task.data()["ProjectStepId"])
    _output_scripts = _project_step.output_attrs()

    # # 检查 省去检查部分
    # if not is_auto:
    #     _check_script = _project_step.check_script()
    #     if not check.Check.value:
    #         exec(_check_script)
    #     if check.Check.value == True:
    #         check.Check.value = False
    #     else:
    #         return False

    # 获取场景信息
    _scene_elements = element.scene_elements()

    # # 提交关联信息
    # relatives.create_relatives()

    # 提交预览信息
    if "video" in infomation:
        if infomation["video"]:
            _approval_file = infomation["video"]
        else:
            _approval_file = infomation["thumbnail"]
    else:
        _approval_file = infomation["thumbnail"]
    _zfile = zfile.LocalFile(_approval_file, "approval")
    _err = _zfile.upload()
    if _err:
        thumbnail_path = _zfile._cloud_thumbnail_path
        _task.update_thumbnail_path(thumbnail_path)

    # 上传备份文件
    _value = publish_backup(task_id, infomation)
    if not _value:
        # cmds.confirmDialog(message = u"上传备份文件失败")
        return False

    # 运行自定义脚本
    if _output_scripts:
        for _output_script in _output_scripts:
            publish_result = False
            _output_entity_type = _task.project_entity_type()
            _output_entity_id = _task.project_entity_id()
            _output_attr_id = _output_script["Id"]
            args = (_output_entity_type, _output_entity_id, _output_attr_id)
            kwargs = {}
            # run scrpt
            zfused_api.zFused.RESET = True
            #print(args)
            #print(_output_script["Script"])
            exec (_output_script["Script"])
            zfused_api.zFused.RESET = False
            if not publish_result:
                # cmds.confirmDialog(message = u"发布失败 \n{}".format(_output_script["Script"]))
                cmds.file(_current_file, o=True, f=True, pmt=False)
                return False

    # 此处获取信息 是主 file 文件
    _key_output_attr = _project_step.key_output_attr()
    _file_suffix = _key_output_attr["Suffix"].replace(".", "")

    _name = _task.file_code()
    _index = "%04d" % (_task.last_version_index() + 1)
    _file_name = "/{}.{}.{}".format(_name, _index, _file_suffix)
    _video_file = infomation["video"]
    _video_name = None
    if _video_file:
        _video_suffix = os.path.splitext(_video_file)[-1]
        _video_name = "/%s.%s%s" % (_name, _index, _video_suffix)
    _thumbnail_file = infomation["thumbnail"]
    _thumbnail_suffix = os.path.splitext(_thumbnail_file)[-1]
    _thumbnail_name = "/%s.%s%s" % (_name, _index, _thumbnail_suffix)

    # introduction
    _introduction = {}
    _introduction["msgtype"] = "rich-text"
    _introduction["text"] = infomation["description"]
    _introduction["image"] = []
    _image_data = {}
    _image_data["path"] = _zfile._cloud_thumbnail_path
    _size = _zfile.get_local_thumbnail_size()
    _image_data["width"] = _size[0]
    _image_data["height"] = _size[1]
    # _image_data["file_type"] = _zfile._file_type
    _image_data["file_type"] = _zfile.file_type()
    _image_data["file_format"] = _zfile.file_format()
    _image_data["file_name"] = _zfile.file_name()
    _image_data["file_md5"] = _zfile.file_md5()
    _introduction["image"].append(_image_data)
    # 修复提交审批为version
    _v, _info = _task.submit_approval("{}.{}".format(_name, _index),
                                             _file_name,
                                             zfused_api.zFused.USER_ID,
                                             _project_step.approvalto_user_ids(),
                                             _project_step.cc_user_ids(),
                                             _video_name,
                                             _thumbnail_name,
                                             _thumbnail_path,
                                             infomation["description"],
                                             str(_introduction))
    if not _v:
        # cmds.confirmDialog(message = u"上传数据库信息失败 {}".format(_info))
        return False

    # 提交关联信息
    _version_id = _v
    relatives.create_relatives(_scene_elements, task_id, _version_id)

    # 更新关联任务 产品级 测试
    _tasks = zfused_api.zFused.get("relative",
                                   filter={"SourceObject": "task", "SourceId": task_id, "TargetObject": "task"})
    if _tasks:
        for _task in _tasks:
            _relative_task = zfused_api.task.Task(_task["TargetId"])
            _relative_task.update_is_production(-1)
    _task.analy_is_production()
    _task.update_is_production(_task.is_production())

    # 修改任务状态为审查中
    _review_ids = zfused_api.status.review_status_ids()
    if _review_ids:
        _task.update_status(_review_ids[0])

    # 打开空文件
    cmds.file(new=True, f=True)

    if not is_auto:
        # 上传结果ui
        # cmds.confirmDialog(message = u"上传成功")
        return True

    return False


def single_publish_file(task_id, output_attr):
    _current_file = cmds.file(q=True, sn=True)
    _task = zfused_api.task.Task(task_id)
    _project_entity = _task.project_entity()
    _project_step = zfused_api.step.ProjectStep(_task.data()["ProjectStepId"])
    _output_scripts = _project_step.output_attrs()

    # 检查
    _check_script = _project_step.check_script()
    if not check.Check.value:
        exec (_check_script)
    if check.Check.value == True:
        check.Check.value = False
    else:
        return

        # 提交关联信息
    # relatives.create_relatives()

    # 上传备份文件
    _value = publish_backup(task_id, {}, True)
    if not _value:
        cmds.confirmDialog(message=u"上传备份文件失败")
        return

    # 运行自定义脚本
    # if _output_scripts:
    #     for _output_script in _output_scripts:
    _output_script = output_attr
    publish_result = False
    _output_entity_type = _task.project_entity_type()
    _output_entity_id = _task.project_entity_id()
    _output_attr_id = _output_script["Id"]
    args = (_output_entity_type, _output_entity_id, _output_attr_id)
    kwargs = {"fix_version": True}
    # run scrpt
    zfused_api.zFused.RESET = True
    exec (_output_script["Script"])
    zfused_api.zFused.RESET = False
    if not publish_result:
        cmds.confirmDialog(message=u"发布失败 \n{}".format(_output_script["Script"]))
        cmds.file(_current_file, o=True, f=True, pmt=False)
        return

    # # 此处获取信息 是主 file 文件
    # _key_output_attr = _project_step.key_output_attr()
    # _file_suffix = _key_output_attr["Suffix"].replace(".", "")

    _name = _task.file_code()
    _index = "%04d" % (_task.last_version_index(0))


    #  发送通知信息
    _user_id = zfused_api.zFused.USER_ID
    zfused_api.im.submit_message("user",
                                 _user_id,
                                 _project_step.approvalto_user_ids() + _project_step.cc_user_ids(),
                                 {"msgtype": "text",
                                  "text": "single publish - {}.{} - {}".format(_name, _index, _output_script["Name"])},
                                 "text",
                                 "",
                                 0)

    # 修改任务状态为审查中
    _review_ids = zfused_api.status.review_status_ids()
    if _review_ids:
        _task.update_status(_review_ids[0])

    # 打开空文件
    cmds.file(new=True, f=True)

    # 上传结果ui
    cmds.confirmDialog(message=u"上传成功")


def fix_file(task_id, infomation={}):
    """ publish file
    :rtype: bool
    """
    _current_file = cmds.file(q=True, sn=True)
    _task = zfused_api.task.Task(task_id)
    _project_entity = zfused_api.objects.Objects(_task.data()["ProjectEntityType"],
                                              _task.data()["ProjectEntityId"])
    _project_step = zfused_api.step.ProjectStep(_task.data()["ProjectStepId"])
    _output_scripts = _project_step.output_attrs()
    _is_new_attribute_solution = _project_step.is_new_attribute_solution()

    # 检查
    _check_script = _project_step.check_script()
    if not check.Check.value:
        exec (_check_script)
    if check.Check.value == True:
        check.Check.value = False
    else:
        return

    # 提交关联信息
    # 暂时不提交关联信息
    # relatives.create_relatives()

    # 上传备份文件
    _value = publish_backup(task_id, infomation, True)
    if not _value:
        cmds.confirmDialog(message=u"上传备份文件失败")
        return

    # 运行自定义脚本
    if _output_scripts:
        for _output_script in _output_scripts:
            #print(_output_script)
            publish_result = False
            _output_entity_type = _task.data()["ProjectEntityType"]
            _output_entity_id = _task.data()["ProjectEntityId"]
            _output_attr_id = _output_script["Id"]

            # args = (_output_entity_type, _output_entity_id, _output_attr_id)
            # kwargs = {"fix_version": True}
            # 为了兼容新旧attribute 需要设定 _is_new_attribute_solution
            kwargs = {"fix_version":True, "is_new_attribute_solution":_is_new_attribute_solution}
            if _is_new_attribute_solution:
                args = (task_id, _output_attr_id)
            else:
                args = (_output_entity_type, _output_entity_id, _output_attr_id)

            # run scrpt
            #print(_output_script["Script"])
            exec (_output_script["Script"])
            if not publish_result:
                cmds.confirmDialog(message=u"发布失败 \n{}".format(_output_script["Script"]))
                cmds.file(_current_file, o=True, f=True, pmt=False)
                return

    # 此处获取信息 是主 file 文件
    _key_output_attr = _project_step.key_output_attr()
    _file_suffix = _key_output_attr["Suffix"].replace(".", "")

    _name = _task.file_code()
    _index = "%04d" % (_task.last_version_index(0))
    _file_name = "/{}.{}.{}".format(_name, _index, _file_suffix)
    _video_file = infomation["video"]
    _video_name = None
    if _video_file:
        _video_suffix = os.path.splitext(_video_file)[-1]
        _video_name = "/%s.%s%s" % (_name, _index, _video_suffix)
    _thumbnail_file = infomation["thumbnail"]
    _thumbnail_suffix = os.path.splitext(_thumbnail_file)[-1]
    _thumbnail_name = "/%s.%s%s" % (_name, _index, _thumbnail_suffix)

    #  发送通知信息
    _user_id = zfused_api.zFused.USER_ID
    zfused_api.im.submit_message("user",
                                 _user_id,
                                 _project_step.approvalto_user_ids() + _project_step.cc_user_ids(),
                                 {"msgtype": "text",
                                  "text": "fix version %s.%s" % (_name, _index)},
                                 "text",
                                 "",
                                 0)

    # 修改任务状态为审查中
    _review_ids = zfused_api.status.review_status_ids()
    if _review_ids:
        _task.update_status(_review_ids[0])

    # 打开空文件
    cmds.file(new=True, f=True)

    # 上传结果ui
    cmds.confirmDialog(message=u"上传成功")
    
    return True


def publish_backup(task_id, infomation={}, fix_version=False):
    """ 上传备份文件
    """
    try:
        _format_type = cmds.file(q=True, typ=True)[0]
        cmds.file(save=True, type=_format_type, f=True, options="v=0;")
    except:
        pass

    _infomation = infomation
    _current_file = cmds.file(q=True, sn=True)

    _task_id = task_id

    # get backup file path
    _task = zfused_api.task.Task(_task_id)
    _project = _task.project()
    _project_entity = _task.project_entity()
    _backup_path = _task.backup_path()
    _production_path = _task.production_path()
    _file_code = _task.file_code()
    if fix_version:
        _file_index = _task.last_version_index(0)
    else:
        _file_index = _task.last_version_index() + 1

    # if _task.project_entity_type() == "asset":
    #     _file_suffix = "mb"
    #     _file_type = "mayaBinary"
    # else:
    #     _file_suffix = "ma"
    #     _file_type = "mayaAscii"

    _project_step = _task.project_step()
    _key_attr = _project_step.key_output_attr()
    _file_type = _key_attr.get("Format")
    _file_suffix = _key_attr.get("Suffix").replace(".","")

    _backup_file = "%s/%s.%04d.%s" % (_backup_path, _file_code, _file_index, _file_suffix)

    # get publish file path
    _temp_path = _task.temp_path()
    _publish_file = "%s/%s.%04d.%s" % (_temp_path, _file_code, _file_index, _file_suffix)
    _publish_file_dir = os.path.dirname(_publish_file)
    #print("publish_path:{}".format(_production_path))

    _is_sync_backup_external_files = _project.variables("is_sync_backup_external_files", 1)

    if not os.path.isdir(_publish_file_dir):
        os.makedirs(_publish_file_dir)
    try:
        # save publish file
        cmds.file(rename=_publish_file)
        cmds.file(save=True, type=_file_type, f=True, options="v=0;")

        # publish xgen file
        if xgen.files():
            xgen.publish_file(_backup_path)
            cmds.file(save=True, type=_file_type, f=True, options="v=0;")
            xgen.publish_xgen(_backup_path)

        if _is_sync_backup_external_files:
            # publish texture
            _texture_files = texture.files()
            if _texture_files:
                _path_set = texture.paths(_texture_files)[0]
                _intersection_path = max(_path_set)
                texture.publish_file(_texture_files, _intersection_path, _backup_path + "/texture")
                # change maya texture node path
                _file_nodes = texture.nodes()
                if _file_nodes:
                    texture.change_node_path(_file_nodes, _intersection_path, _backup_path + "/texture")
            # publish alembic cache
            _alembic_files = alembiccache.files()
            if _alembic_files:
                _path_set = alembiccache.paths(_alembic_files)[0]
                _intersection_path = max(_path_set)
                alembiccache.publish_file(_alembic_files, _intersection_path, _backup_path + "/cache/alembic")
                _file_nodes = alembiccache.nodes()
                if _file_nodes:
                    alembiccache.change_node_path(_file_nodes, _intersection_path, _backup_path + "/cache/alembic")
            # publish reference file
            _reference_files = referencefile.files()
            if _reference_files:
                _path_set = referencefile.paths(_reference_files)[0]
                _intersection_path = max(_path_set)
                referencefile.publish_file(_reference_files, _intersection_path, _backup_path + "/reference")
                _file_nodes = referencefile.nodes()
                if _file_nodes:
                    referencefile.change_node_path(_file_nodes, _intersection_path, _backup_path + "/reference")
            # publish yetinode texture
            _yeti_texture_file = yeti.tex_files()
            if _yeti_texture_file:
                _path_set = yeti.paths(_yeti_texture_file)[0]
                _intersection_path = max(_path_set)
                yeti.publish_file(_yeti_texture_file, _intersection_path, _backup_path + "/texture/yeti")
                _yeti_texture_dict = yeti._get_yeti_attr("texture", "file_name")
                yeti.change_node_path(_yeti_texture_dict, _intersection_path, _backup_path + "/texture/yeti")

        # save publish file
        cmds.file(save=True, type=_file_type, f=True, options="v=0;")

        # publish file
        _result = filefunc.publish_file(_publish_file, _backup_file)

        if _infomation:
            _project_handle = zfused_api.project.Project(_task.data()["ProjectId"])
            _project_step = zfused_api.step.ProjectStep(_task.data()["ProjectStepId"])
            _approval_ftp = "/storage/approval/{}/{}/{}/{}".format(_project_handle.code(),
                                                                   _task.data()["ProjectEntityType"],
                                                                   _project_step.code(),
                                                                   _project_entity.code())
            # publish thumbnail and video
            if "video" in _infomation:
                _video_file = _infomation["video"]
                if _video_file:
                    _video_suffix = os.path.splitext(_video_file)[-1]
                    _video_backup_file = "%s/%s.%04d%s" % (_backup_path, _file_code, _file_index, _video_suffix)
                    _video_production_file = "%s/thumbnail/%s.%04d%s" % (
                    _production_path, _file_code, _file_index, _video_suffix)
                    _result = filefunc.publish_file(_video_file, _video_backup_file)
                    _result = filefunc.publish_file(_video_file, _video_production_file)

            _thumbnail_file = _infomation["thumbnail"]
            _thumbnail_suffix = os.path.splitext(_thumbnail_file)[-1]
            _thumbnail_backup_file = "%s/%s.%04d%s" % (_backup_path, _file_code, _file_index, _thumbnail_suffix)
            _thumbnail_production_file = "%s/thumbnail/%s.%04d%s" % (
            _production_path, _file_code, _file_index, _thumbnail_suffix)
            _result = filefunc.publish_file(_thumbnail_file, _thumbnail_backup_file)
            _result = filefunc.publish_file(_thumbnail_file, _thumbnail_production_file)

    except Exception as e:
        logger.error(e)
        return False
    if _is_sync_backup_external_files:
        cmds.file(new=True, f=True)
        cmds.file(_current_file, o=True, f=True, pmt=False)
    return True

                 
