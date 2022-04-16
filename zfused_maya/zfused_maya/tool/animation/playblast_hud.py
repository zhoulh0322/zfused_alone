# coding:utf-8
# author binglu.wang

import os
import json
import getpass
import time
from functools import partial

import maya.cmds as cmds
import maya.mel as mm
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

import zfused_maya.node.core.shotmask as shotmask

try:
    import zfused_maya
    import zfused_api
except ImportError:
    # 线下项目设置
    HUDProject = "SWM"

def get_maya_hud():
    '''get HUDjson file
    '''
    _project_id = zfused_maya.core.record.current_project_id()
    if _project_id:
        _project_handle = zfused_api.project.Project(_project_id)
        _dir = _project_handle.production_path()
        _file = "{}/setup/MAYA_HUD.json".format(_dir)
        print(_file)
        if os.path.isfile(_file):
            return _file
    return None

def get_maya_shotmask():
    '''get maskjson file
    '''
    _project_id = zfused_maya.core.record.current_project_id()
    if _project_id:
        _project_handle = zfused_api.project.Project(_project_id)
        _dir = _project_handle.production_path()
        _file = "{}/setup/MAYA_SHOTMASK.json".format(_dir)
        if os.path.isfile(_file):
            return _file
    return None

class HUD(object):
    viewInfoState = False
    def __init__(self, jsonPath,Versionname = "",Approved = ""):
        self.jsonPath = jsonPath
        self._versionname = Versionname
        self.COMPANY   = u"苏州星龙传媒"
        self._Company = {}
        self._Project = {}
        self._CUT = {}
        self._Timer = {}
        self._ImageSize = {}
        self._Camera_Name = {}
        self._Camera_Near = {}
        self._Camera_Far = {}
        self._Camera_Focal = {}
        self._Camera_Film = {}
        self._FrameInfo = {}
        self._FrameRate = {}

        self._DefaultList = []

        self._set_hud_info()
        if Approved:
            self._set_approved(Approved)

    def _set_hud_info(self):
        '''set HUD info
        '''
        _config_info = self._get_config()
        # set command
        self._Company["c"] = partial(self._get_company,_config_info)
        self._Project["c"] = self._get_project_user_str
        self._CUT["c"] = partial(self._get_version_file_name,self._versionname)
        self._Timer["c"] = self._get_time
        self._ImageSize["c"] = self._get_image_size
        self._Camera_Name["c"] = self._get_camera_name
        self._Camera_Near["c"] = partial(self._get_camera_attr,"nearClipPlane")
        self._Camera_Far["c"] = partial(self._get_camera_attr,"farClipPlane")
        self._Camera_Focal["c"] = partial(self._get_camera_attr,"focalLength")
        self._Camera_Film["c"] = self._get_camera_filmfit
        self._FrameInfo["c"] = self._get_frame_str
        self._FrameRate["c"] = self._get_frame_rate
        alltype = {
                    "_Company" : self._Company,
                    "_Project" : self._Project,
                    "_CUT" : self._CUT,
                    "_Timer" : self._Timer,
                    "_ImageSize" : self._ImageSize,
                    "_Camera_Name" : self._Camera_Name,
                    "_Camera_Near" : self._Camera_Near,
                    "_Camera_Far" : self._Camera_Far,
                    "_Camera_Focal" : self._Camera_Focal,
                    "_Camera_Film" : self._Camera_Film,
                    "_FrameInfo" : self._FrameInfo,
                    "_FrameRate" : self._FrameRate
                }
        if _config_info:
            self._DefaultList = [_i for _i in _config_info.keys()]
            for _k,_v in _config_info.items():
                for _key, _value in _v.items():
                    if _key != "c":
                        alltype[_k][_key] = _value
        else:
            print ("Can't find config file")

    def _get_config(self):
        '''get HUD info
        '''
        if os.path.exists(self.jsonPath):
            try:
                with open(self.jsonPath, 'r') as info:
                    dataInfo = json.load(info)
                    info.close()
                return dataInfo
            except ValueError:
                return None
        else:
            return None

    def _get_project(self):
        '''获取当前项目
        '''
        try:
            _project_id = zfused_maya.core.record.current_project_id()
            _project_handle = zfused_api.project.Project(_project_id)
            return _project_handle.code()
        except:
            global HUDProject
            return HUDProject

    def _get_user(self):
        '''获取项目制作人
        '''
        try:
            _user_id = zfused_api.zFused.USER_ID
            _user_handle = zfused_api.user.User(_user_id)
            return _user_handle.profile["NameEn"]
        except:
            return self._get_computer_user()

    def _get_computer_user(self):
        '''获取电脑账户
        '''
        import getpass
        hostName = getpass.getuser()    
        return hostName

    def _get_project_user_str(self):
        '''combine project&user info
        '''
        user = self._get_user()
        project = self._get_project()
        return "%s | %s"%(project,user)

    def _get_camera_name(self):
        '''获取当前相机名
        '''
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camera = camDag.fullPathName()
        _name = cmds.listRelatives(camera, parent = True)[0]
        return "            Camera:     %s"%(_name)

    def _get_camera_attr(self,attr_name):
        '''获取当前相机属性
        '''
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camera = camDag.fullPathName()
        try:
            # print "%s.%s"%(camera,attr_name)
            value = "%.3f"%cmds.getAttr("%s.%s"%(camera,attr_name))
            return "            %s:     %s"%(attr_name,str(value))
        except:
            return "            %s:     "%attr_name

    def _get_camera_filmfit(self):
        '''获取当前相机fileFit属性
        '''
        _dict = {
            0:"Fill",
            1:"Horizontal",
            2:"Vertical",
            3:"Overscan"
        }
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camera = camDag.fullPathName()
        try:
            value = cmds.getAttr("%s.%s"%(camera,"filmFit"))
            _mode = _dict[value]
            return "            %s:     %s"%("filmFit",_mode)
        except:
            return "            %s:"%"filmFit"

    def _get_frame_rate(self):
        '''获取帧数率
        '''
        _dict = {
            'film':24,
            "pal":25,
            "ntsc":30
        }
        _mode = cmds.currentUnit(q=1, t=1)
        _frame_rate = _dict[_mode]
        return u"帧率: %s"%str(_frame_rate)

    def _get_frame_str(self):
        '''获取帧数范围
        '''
        z_StartFrame = int(cmds.playbackOptions(q = True, min = True))
        z_EndFrame = int(cmds.playbackOptions(q = True, max = True))
        format = "%0" + str(len(str(z_EndFrame))) + "d"
        z_CurrentFrame = format%int(cmds.currentTime(q = True))
        return "%s|%s-%s"%(z_CurrentFrame,z_StartFrame,z_EndFrame)

    def _get_time(self):
        '''获取系统时间
        '''
        import time
        time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return str(time)


    def _get_company(self,datainfo):
        '''获取公司名
        '''
        if "c" in datainfo["_Company"]:
            self.COMPANY = datainfo["_Company"]["c"]
        return u"Company: {}".format(self.COMPANY)

    def _get_file_name(self):
        '''get file name
        '''
        _file = cmds.file(q = True, sn = True)
        if _file:
            _name = os.path.basename(os.path.splitext(_file)[0])
            return _name
        return ""

    def _get_version_file_name(self,versionname = ""):
        if not versionname:
            return self._get_file_name()
        return versionname

    # 获取图像大小
    def _get_image_size(self):
        '''get image pixel
        '''
        # # get project set
        # _project_id = zfused_maya.core.record.current_project_id()
        # _project_handle = zfused_api.project.Project(_project_id)
        # _size = "{}x{}".format(_project_handle.config["ImageWidth"], _project_handle.config["ImageHeight"])
        _size = "%sx%s"%(cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height"))
        return _size

    def _set_approved(self,_str):
        ''' add Approved info
        '''
        # "Approved by Mike"
        self._Approved = {"s":4,"l":_str,"atr":False,"ba":"left"}#,"p" : 75
        self._DefaultList.append("_Approved")

    def _set_show_info(self,*args):
        '''set show info
        '''
        from collections import Counter
        showInfo = {}
        blockindex = []
        for preProject in args:
            preProjectAttr = eval("self.%s"%preProject)
            blockindex.append(preProjectAttr["s"])
            current = Counter(blockindex)
            if "b" not in preProjectAttr:
                preProjectAttr["b"] = current[preProjectAttr["s"]]-1
            showInfo[preProject] = self._complete_info(**preProjectAttr)
        return showInfo

    def _complete_info(self,**kwargs):
        '''补全配置信息
            参数全简称对照及含义:
                attachToRefresh = atr 刷新
                block = b 块序号
                blockAlignment = ba 块对齐方式
                blockSize = bs 纵向边距
                command = c 命令
                dataAlignment = da 数据和块的对齐方式
                dataFontSize = dfs 数据字号
                label = l 标签
                labelFontSize = lfs 标签字号
                labelWidth = lw 标签宽度
                padding = p 缩进单位
                section = s 位置
                label 标签
        '''
        allAttr = {"atr":True,"b":0,"ba":"left","bs":"small","c":None,"dfs":"large","lfs":"large","p":0,"s":0,"da":"left","lw":0,"l":""}
        outdict = {}
        for attr in allAttr.keys():
            if kwargs.has_key(attr):
                outdict[attr] = kwargs[attr]
            else:
                outdict[attr] = allAttr[attr]
        return outdict

    def _displayMode(self,type):
        '''屏显预设
            所有属性名
                'nurbsCurves',
                 'nurbsSurfaces',
                 'cv',
                 'hulls',
                 'polymeshes',
                 'subdivSurfaces',
                 'planes',
                 'lights',
                 'cameras',
                 'imagePlane',
                 'joints',
                 'ikHandles',
                 'deformers',
                 'dynamics',
                 'particleInstancers',
                 'fluids',
                 'hairSystems',
                 'follicles',
                 'nCloths',
                 'nParticles',
                 'nRigids',
                 'dynamicConstraints',
                 'locators',
                 'dimensions',
                 'pivots',
                 'handles',
                 'textures',
                 'strokes',
                 'motionTrails',
                 'pluginShapes',
                 'clipGhosts',
                 'greasePencils',
                 'pluginObjects'
        '''
        # 拍屏预设
        if "playblast" in type:
            hidekeys = ["nurbsCurves","cv","hulls","subdivSurfaces","planes","lights",
                        "cameras","joints","ikHandles","deformers","dynamics",
                        "particleInstancers","fluids","hairSystems","follicles","nCloths",
                        "nParticles","nRigids","dynamicConstraints","locators","dimensions",
                        "pivots","handles","motionTrails","clipGhosts","greasePencils"]
        # 中期制作预设
        elif "mediumTerm" in type:
            hidekeys = ["cv","hulls","subdivSurfaces","planes","lights","imagePlane",
                        "joints","ikHandles","particleInstancers","nParticles","dimensions",
                        "pivots","handles","motionTrails","clipGhosts","greasePencils"]
        # 原始预设
        else:
            hidekeys = ['nc','pl','lt','ca','joints','ikh','df','ha','follicles','hairSystems',
                        'strokes','motionTrails','dimensions','locators','motionTrails']
        # 设置平滑显示
        modelPanels=cmds.getPanel(typ="modelPanel")
        for currentPanel in modelPanels:
            cmds.modelEditor(currentPanel,e = 1,allObjects = 1)
            for item in hidekeys:
                eval("cmds.modelEditor(\'"+currentPanel+"\',e=True,"+item+"=0)")


    @property
    def labelcolor(self):
        return cmds.displayColor("headsUpDisplayLabels", q = True)

    @labelcolor.setter
    def labelcolor(self, num = 14):
        cmds.displayColor("headsUpDisplayLabels", num, dormant = True)

    @property
    def valuecolor(self):
        return cmds.displayColor("headsUpDisplayValues", q = True)

    @valuecolor.setter
    def valuecolor(self, num = 16):
        cmds.displayColor("headsUpDisplayValues", num, dormant = True)

    def _remove(self):
        '''remove HUD info
        '''
        huds = cmds.headsUpDisplay(lh = True)
        if huds:
            for item in huds:
                cmds.headsUpDisplay(item, rem = True)

    def _restore_defalut(self):
        '''reset HUD info
        '''
        self.valuecolor = 16
        self.labelcolor = 16
        mm.eval("source initHUD.mel")

    def _resize_font(self):
        '''重缩放maya字体大小
        '''
        scalemode = cmds.mayaDpiSetting(q = 1,mode = 1)
        if scalemode == 0:
            print (u"error:当前ui缩放模式不正确")
            return
        else:
            hudScale = cmds.mayaDpiSetting(q = 1,scaleValue = 1)
            font_size = int(15/hudScale)
            current_font_size= cmds.displayPref(q = 1,dfs = 1)
            if font_size != current_font_size:
                if font_size == 15:
                    cmds.displayPref(dfs = 16)
                else:
                    cmds.displayPref(dfs = font_size)

    def _show(self):
        self._displayMode("playblast")
        # self._resize_font()
        displayLayout = self._set_show_info(*self._DefaultList)
        self.valuecolor = 16
        self.labelcolor = 14
        for display in displayLayout.keys():
            dis = displayLayout[display]
            if not dis["c"]:
                cmds.headsUpDisplay(display, s = dis["s"], b = dis["b"], ba = dis["ba"],p = dis["p"],
                                        lfs = dis["lfs"], dfs = dis["dfs"], blockSize = dis["bs"], 
                                        atr = dis["atr"],da = dis["da"],lw = dis["lw"],l = dis["l"])
            else:
                cmds.headsUpDisplay(display, s = dis["s"], b = dis["b"], ba = dis["ba"],p = dis["p"],
                                        lfs = dis["lfs"], dfs = dis["dfs"], blockSize = dis["bs"], 
                                        c = dis["c"], atr = dis["atr"],da = dis["da"],lw = dis["lw"],l = dis["l"])
        _mask_json = get_maya_shotmask()
        if _mask_json:
            result = shotmask.create_mask()
            if result:
                _mask = shotmask.get_mask()
                with open(_mask_json, 'r') as info:
                    dataInfo = json.load(info)
                    if dataInfo:
                        for _key, _value in dataInfo.items():
                            cmds.setAttr("{}.{}".format(_mask, _key), _value)

    def change_hud_state(self):
        # print (HUD.viewInfoState)
        isshow = cmds.headsUpDisplay(lh = True)
        if not HUD.viewInfoState:
            self._remove()
            self._show()
            HUD.viewInfoState = True
        else:
            self._remove()
            self._restore_defalut()
            # remove shot mask
            shotmask.delete_mask()
            HUD.viewInfoState = False
        return

if __name__ == '__main__':
    viewInfo = HUD(get_maya_hud())
    viewInfo._remove()
    viewInfo._show()
