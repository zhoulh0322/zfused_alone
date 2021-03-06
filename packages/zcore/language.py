# coding:utf-8
# --author-- lanhua.zhou

import os
import json
import ast
import logging

logger = logging.getLogger(__name__)

zh_cn = { "login name": "登陆账户",
    "login password": "登陆密码",
    "login name not exist" : "登陆名未填写",
    "login password not exist" : "登陆密码为填写",
    "account name": "用户名",
    "account code": "用户代号",

    "post name": "职务名称",
    "post code": "职务代号",
    "department name": "部门名称",
    
    "search": "关键字搜索",
    "refresh": "刷新",
    "create": "创建",
    "cancel": "退出",
    "required": "必填",
    "remove": "移除",
    "status": "状态",
    "types": "类型",

    "index": "索引",
    "id": "ID",

    "create user": "创建新用户",
    "new account": "新账户",
    "new post": "新职位",

    "production": "产品级",
    "is production": "产品级",

    "create new project":"创建新项目",
    "project setting":"项目设置",
    "project base":"项目基础",
    "project name": "项目名称",
    "project code": "项目代号",
    "project status": "项目状态",
    "project workflow": "项目工作流",
    "project profile":"项目信息",
    "project start time": "项目开始时间",
    "project end time": "项目结束时间",
    "project color": "项目代表色",
    "project config":"项目配置",
    "project size": "项目画面尺寸",
    "project fps": "项目帧率",
    "project production path": "项目路径",
    "project backup path": "项目备份路径",
    "project work path": "项目本地制作路径",
    "project publish path": "项目临时文件路径",
    "project step":"项目环节",
    "project pipeline":"项目流程",
    "project people":"项目成员",
    "project step people":"项目环节成员",
    "project description": "项目描述",
    "project object": "项目对象",
    "project entity": "项目实体",
    "entity": "实体",
    
    "step": "环节",

    "previous": "上一项",
    "next": "下一项",
    "confirm": "确认",

    "menu": "菜单",
    "home" : "首页",
    "library" : "资产库",
    
    "project" : "项目",
    "switch project": "切换项目",
    "select project": "选择项目",
    "new project": "新项目",
    "project setting": "项目设置",
    
    "asset": "资产",
    "asset level": "资产等级",
    "asset difficulty": "资产难度",
    "new asset": "新资产",
    "asset task": "资产任务",
    "asset step": "资产步骤",
    "asset thumbnail": "资产缩略图",
    "asset schedule": "资产计划表",
    "create asset": "创建资产",
    "batch create": "批量创建",
    "batch export": "批量导出",
    "export": "导出",
    "export to excel": "导出到excel",
    "asset name": "资产名称",
    "asset code": "资产代号",
    "asset type": "资产类型",
    "delete assets": "删除资产",
    "asset description": "资产描述",
    "assign asset": "指定资产",

    "assembly": "场景装配",
    "scene assembly": "场景装配",
    "create scene": "创建场景",
    "new assembly":"新场景",

    "episode": "集",
    
    "sequence": "场次",
    "new sequence": "新场次",
    "sequence task": "场次任务",
    "sequence step": "场次步骤",
    "sequence thumbnail": "场次缩略图",
    "create sequence": "创建场次",
    "delete sequences": "删除场次",
    "sequence name": "场次名称",
    "sequence code": "场次代号",
    "sequence description": "场次描述",
    "assign sequence": "指定场次",

    "shot": "镜头",
    "new shot": "新镜头",
    "shot level": "镜头等级",
    "shot difficulty": "镜头难度",
    "shot task": "镜头任务",
    "shot step": "镜头步骤",
    "shot thumbnail": "镜头缩略图",
    "create shot": "创建镜头",
    "shot name": "镜头名称",
    "shot code": "镜头代号",
    "shot type": "镜头类型",
    "delete shots": "删除镜头",
    "shot description": "镜头描述",
    "assign shot": "指定镜头",

    "group": "组",
    "group by": "分组",
    "group by none": "无分组",
    "group by user": "按用户分组",
    "group by status": "按状态分组",
    "group by project step": "按项目环节分组",

    "people": "成员",

    "data manage": "数据管理",
    "extract project data": "提取项目数据",
    "analyze project data": "分析项目数据",
    "analyze": "分析",
    "analysis": "分析", 
    "storage analysis": "入库分析",
    "production analysis": "入库分析",
    "task production analysis": "任务入库分析",
    "task work time": "任务制作时长",

    "workflow": "流程",
    "repository": "资源库",
    "support" : "支持",
    "setting" : "设置",

    "personal": "个人",
    "users": "用户",
    "post": "职位",
    "department": "部门",
    "outsourcer": "外包商",
    "no outsourcer": "内部",
    "outsource manage": "外包管理",
    "outsourcer name": "外包商名称",
    "system": "系统",

    "all users": "所有用户",
    "add user": "添加用户",
    "remove user": "移除用户",
    "filter": "检索",

    "all posts": "所有职务",
    "add post": "添加职务",
    "remove post": "移除职务",

    "all departments": "所有部门",
    "add department": "添加部门",
    "remove department": "移除部门",

    "all outsourcers": "所有外包商",
    "add outsourcer": "添加外包商",
    "remove outsourcer":"移除外包商",
    "assign outsourcer": "分配外包商",

    "is outsource": "外包",


    "task": "任务",
    "new task": "新任务",
    "task name": "任务名称",
    "task status": "任务状态",
    "task assigned to": "任务制作人",
    "my tasks": "我的任务",
    "working tasks": "制作中任务",
    "active tasks": "激活中的任务",
    "pending review tasks": "待审核任务",
    "pending review tasks": "待审核任务",
    "version": "版本",
    "review": "QC审核",

    "assign thumbnail": "指定缩略图",

    "assign user":"添加用户",
    "user": "人员",
    "worker": "制作部",
    "producer": "制作方",

    "name": "名称",
    "code": "代号",
    "thumbnail": "缩略图",
    "plan start time": "预计开始时间",
    "task start time": "任务预计开始时间",
    "plan end time": "预计结束时间",
    "task end time": "任务预计结束时间",
    "plan time": "预计时间",
    "plan estimated time": "预计制作时长",
    "set time": "设定时间",
    "working start time": "制作开始时间",
    "working end time": "制作结束时间",
    "working estimated time": "实际制作时长",
    "submission time": "提交时间",
    "created time": "创建时间",
    "created by": "创建人员",
    "progress": "进度",
    "level": "等级",
    "object": "对象",
    "assigned" : "指派",
    "assigned user" : "制作人",
    "link": "链接",
    "link address": "链接地址",
    "assigned to": "制作人",
    "Submitter": "提交人员",
    "description": "描述",
    "estimated time": "预计工时",
    "working time": "制作工时",
    "tag": "标签",
    "tag name": "标签名称",
    "tag code": "标签代号",
    "tag color": "标签代表色",
    "add tag": "添加标签",
    "link tag": "链接标签",
    "new tag": "新建标签",
    "assign tag": "分配标签",
    "start frame": "起始帧",
    "end frame": "结束帧",

    "setting start time": "设定开始时间",
    "setting end time": "设定结束时间",

    "data manage": "数据管理",

    "no user": "无用户",
    "no assigned user": "未指定制作人员",
    "no task": "无任务",

    "task level": "任务等级",
    "task difficulty": "任务难度",
    "task description": "任务描述",
    "task schedule": "任务甘特图",
    "task step": "任务步骤",
    "project step": "项目步骤(环节)",
    "new task step": "添加任务步骤",
    "new project step": "新项目步骤(环节)",
    "schedule": "甘特图",

    "cc": "抄送",
    "approval to": "审批",
    "approver": "审批人",
    "software": "软件",
    "procedure": "步骤",

    "import from excel": "从excel导入",

    "not start": "还未开始",
    "not end": "还未结束",
    "not estimated time": "无预估时间",

    "day": "天",
    "hour": "小时",
    "only show task": "仅显示任务",
    "show task": "显示任务",

    "change": "更改",
    "work user": "制作人员",
    "change by": "修改人员",
    "change time": "修改时间",

    "create task": "创建任务",
    "create by": "制片",

    "message": "消息",


    "all": "所有",

    "qc": "质量控制",

    "qc & tracking": "质量控制 | 跟踪",

    "submit": "提交",
    "submitter": "提交者",

    "script": "脚本",
    "check script": "检查脚本",
    "attr editor": "属性编辑器",
    "input attr": "输入属性",
    "output attr": "输出属性",
    "input attribute": "输入属性",
    "output attribute": "输出属性",

    "pass": "通过",
    "no pass": "不通过",
    "open file": "打开文件",

    "excel path": "excel文件路径",

    "header": "字段",


    "associate": "关联",
    "new associate": "新关联",

    "last version": "最新版本",

    "input": "输入",
    "output": "输出",

    "priority": "优先级",
    "assign priority": "分配优先级",

    "follow": "关注",
    "my follows": "我的关注",

    "new object": "新实例对象",
    "object name": "实例名称",
    "object code": "实例代号",
    "object description": "实例描述",

    "sort by asc": "升序",
    "sort by desc": "降序",
    "sort by custom": "自定义排序",


    "expand all": "全部展开",
    "expand selected": "展开当前选择",
    "collapse all": "全部折叠",
    "collapse selected": "折叠当前选择",

    "field": "字段",
    "view field": "显示字段",
    "custom fields": "自定义字段",

    "field": "字段",
    "view field": "显示字段",
    "custom fields": "自定义字段",
    "custom view field": "自定义显示字段",

    "application location": "应用程序地址",
    "application script location": "脚本地址",

    "config": "配置",
    "startup": "启动",

    "process management": "进程管理",
    "task management": "任务管理",

    "rage pool": "怒气池",
    "material library": "素材库",

    "fast retrieval": "快速检索",

    "page": "页面",
    "new page": "新页面",
    "page name": "页面名称",
    "page code": "页面代号",
    "page description": "页面描述",
    "add to pages": "添加至页面",
    "remove from current page": "从当前页面移除",

    "unreviewed versions": "未审核版本",
    "unreviewed versions cc to me": "抄送给我的未审核版本",

    "approval": "入库审批",
    "production approval": "入库审批",
    "assign approval": "指定审批",
    "assign production": "指定产品级",
    "not available task": "不可入库任务",
    "not available task cc to me": "抄送给我的不可入库任务",
    "not available task approval to me": "我审批的不可入库任务",

    "color": "颜色",
    "new status": "添加状态",
    "new attr": "新属性",
    "new attribute": "新属性",
    "category": "类别",
    "new category": "新分类",
    "default": "默认",
    "new review": "新审核",
    "new project review": "新项目审核",
    "review name": "审核名称",
    "review code": "审核代号",
    "all project": "所有项目",

    "report": "汇报",
    "multimedia": "多媒体",

    "preview": "预览",
    "base setting": "基础设置",
    "global setting": "全局设置",

    "assign status": "指定状态",
    "create episode": "创建集",
    "new": "新",

    "not started": "未开始",
    "in progress": "进行中",
    "done": "完成",
    "freeze": "冻结",

    "plugin": "插件",
    "new library": "新资源库",
    "new library entity": "新资源",
    "library entity": "资源",

    "previous status": "之前的状态",
    "next status": "之后的状态",
    "working hours": "工时",

    "prophet": "先知",

    "path": "路径" 
    
}

en_us = {

}

DATA = {
    "zh_cn": zh_cn,
    "en_us": en_us
}


class Language(object):
    LANGUAGE = "zh_cn"
    LANGUAGE_DATA = DATA.get(LANGUAGE)

    # _file = os.path.join(":/resources", "language", "{}.json".format(LANGUAGE)).replace(os.sep, "/")
    # print(_file)
    # _stream = QtCore.QFile(_file)
    # _stream.open(QtCore.QIODevice.ReadOnly)
    # _string = _stream.readAll().data().decode()
    # LANGUAGE_DATA = ast.literal_eval(_string)



    logger.info("load language")

    def set_language(self, language):
        self.LANGUAGE = language
        # _file = os.path.join(":/resources", "language", "{}.json".format(self.LANGUAGE)).replace(os.sep, "/")
        # _stream = QtCore.QFile(_file)
        # _stream.open(QtCore.QIODevice.ReadOnly)
        # _string = str(_stream.readAll(), encoding='utf-8')
        # LANGUAGE_DATA = ast.literal_eval(_string)
        Language.LANGUAGE_DATA = DATA[self.LANGUAGE]

def word(language_code):
    _code = Language.LANGUAGE_DATA.get(language_code)
    return _code