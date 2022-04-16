# -*- coding: UTF-8 -*-
'''
@Time    : 2021/9/16 11:27
@Author  : Jerris_Cheng
@File    : playblast_maya.py
'''
from __future__ import division
from __future__ import print_function

import json
import os
import subprocess
import locale 
import datetime
import shutil
import inspect
import copy

from Qt import QtWidgets,QtCore,QtGui

import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mm
import maya.cmds as cmds
from pymel.core import *

from zwidgets.playblast import playblast_widget
reload(playblast_widget)

from zfused_maya.ui.widgets import window

# 显示配置信息
HUD_INIT = {

    "spacing": 8,
    "margin": [8,8,8,8],
    "text-height": 25,
    "font-family": "Microsoft YaHei UI",
    "font-size": 20,
    "color": "#FF0000",
    "bold": False,
    "background-color": "#222222",
    
    "image_size":[2048,858],
    "fps":24,

    "hud": [
        {
            "code": "project",
            "color": "#EEEEEE",
            "text-align": [-1, 1, 0],
            "cmd": "text = '《未配置项目显示信息》'"
        },
        {
            "code": "file",
            "color": "#EEEEEE",
            "text-align": [0, 1, 0],
            "cmd": "import os;import maya.cmds as cmds;text,_=os.path.splitext(cmds.file(q=True, sn=True, shn=True))"
        },
        {
            "code": "time",
            "color": "#EEEEEE",
            "text-align": [1, 1, 0],
            "cmd": "import time;text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())"
        },
        {
            "code": "image_size",
            "color": "#EEEEEE",
            "text-align": [0, -1, 0],
            "cmd": "text = '2048 x 858'"
        },
        {
            "code": "camera",
            "color": "#EEEEEE",
            "text-align": [-1, -1, 0],
            "cmd": '''
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
view = OpenMayaUI.M3dView.active3dView()
camDag = OpenMaya.MDagPath()
view.getCamera(camDag)
cameraname =camDag.fullPathName().split('|')[-2]
text ="相机:    {}".format(cameraname)
            '''
        },
        {
            "code":"camera_focal",
            "color":"#EEEEEE",
            "text-align": [-1, -1, 1],
            "cmd":'''
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
view = OpenMayaUI.M3dView.active3dView()
camDag = OpenMaya.MDagPath()
view.getCamera(camDag)
current_cam = camDag.fullPathName().split('|')[-1]
focal_length = cmds.getAttr("{}.focalLength".format(current_cam))
text ="焦距:    {:.2f}".format(focal_length)
            '''

        },
        {
            "code": "frame",
            "color": "#EEEEEE",
            "text-align": [1, -1, 0],
            "cmd": '''
import maya.cmds as cmds
_s_t = int(cmds.playbackOptions(q = True, min = True))
_e_t = int(cmds.playbackOptions(q = True, max = True))
# _format = '%0' + str(len(str(_e_t))) + 'd'
# _c_t = _format%int(cmds.currentTime(q = True))
_c_t = int(cmds.currentTime(q = True))
text = '帧数:    %s|%s-%s'%(_c_t,_s_t,_e_t)'''
        },
        {
            "code": "fps",
            "color": "#EEEEEE",
            "text-align": [1, -1, 1],
            "cmd": '''
import pymel.core as pm
_frame =  int(pm.mel.currentTimeUnitToFPS())
text = "帧率:    %s"%str(_frame)
'''
        }
    ] 
}


# CAM_INIT = {
#     "filmFit":1,
#     "displayResolution":False,
#     "displayGateMask":True,
#     "displayGateMaskOpacity":1.0,
#     "displayGateMaskColor":[
#         0.0,
#         0.0,
#         0.0
#     ],
#     "displaySafeAction":True,
#     "overscan":1
# }

CAM_INIT = [
    {
        "attr":"filmFit",
        "value":1,
    },
    {
        "attr":"displayResolution",
        "value":False,
    },
    {
        "attr":"displayGateMask",
        "value":1.0,
    },
    {
        "attr":"displayGateMaskColor",
        "value":[0,0,0],
        "type":"double3"
    },
    {
        "attr": "displayGateMaskOpacity",
        "value": 1.0
    },
    {
        "attr":"displaySafeAction",
        "value":True,
    },
    {
        "attr":"overscan",
        "value":1.0,
    }

]


def get_ffmpeg():
    try:
        import zfused_api
        _FFMPEG = inspect.getfile(zfused_api).split('zfused_api')[0] + r'plugins\ffmpeg\ffmpeg.exe'
    except:
        _FFMPEG = r"\\td\pipeline\zfused_pipeline\packages\plugins\ffmpeg\ffmpeg.exe"
    return _FFMPEG


def get_cam_init():
    pass

def get_hud_init():
    try:
        import zfused_api
        from zfused_maya.core import record
        _project_id = record.current_project_id()
        _project = zfused_api.project.Project(_project_id)
        _playblast_maya = _project.variables("playblast_maya")
    except :
        _playblast_maya ={}
    return _playblast_maya


class Playblast(window._Window):
    def __init__(self, parent = None):
        super(Playblast, self).__init__(parent)
        self._build()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._update)

        self._snap_timer = QtCore.QTimer()
        self._snap_timer.timeout.connect(self._temp_snap)

        self.playblast_widget.extra_path.connect(self._extra_path)
        self.playblast_widget.playblast.connect(self._playblast)
        self.playblast_widget.resolution_scale.connect(self._resolution_scale)
        
        self._config = {}
        self._temp_config = {}

    def init(self, init_config):
        self._config = init_config
        self._temp_config = copy.deepcopy(init_config)
        self.playblast_widget.init(init_config)

    def _playblast(self, path):
        self.playblast_widget.setEnabled(False)
        cmds.select(cl=1)
        # 运行camera拍屏设置
        self._cam_init(CAM_INIT)

        #获取开始帧
        _min_time = int(cmds.playbackOptions(q=True, minTime=True))
        _max_time = int(cmds.playbackOptions(q=True, maxTime=True))
        _time = float(_max_time - _min_time + 1)/self._temp_config.get("fps")

        # 清除原有的所有HUD
        self.remove_all_hud()

        # 获取当前临时路径
        _temp_folder =self._get_temp_image_folder()
                
        # 最终拍屏路径
        _video_path = path

        _file_code, _ = os.path.splitext(cmds.file(q=True, sn=True, shn=True))
        #获取音效
        sound = None
        aPlayBackSliderPython = mm.eval('$temVar=$gPlayBackSlider')
        if aPlayBackSliderPython:
            sound = cmds.timeControl(aPlayBackSliderPython, q=True, sound=True)
        
        _image_path = _temp_folder + "/" + _file_code
        _image = None
        for i in range(_min_time, _max_time + 1):
            _image = cmds.playblast( format ="image",
                                     filename = _temp_folder + "/" + _file_code,
                                     startTime = i, 
                                     endTime = i, 
                                     forceOverwrite =1,
                                     sequenceTime=0,
                                     clearCache=1,
                                     viewer=0, 
                                     showOrnaments=1, 
                                     offScreen=1, 
                                     fp=4,
                                     percent=100,
                                     compression="jpg",
                                     quality= 100,
                                     w = self._temp_config.get("image_size")[0],
                                     h = self._temp_config.get("image_size")[1])
            _progress_image = _image.replace("####","{:0>4d}").format(i)
            self.playblast_widget.set_image(_progress_image)
            QtWidgets.QApplication.processEvents()
            self.process_image(_progress_image)

        production_image_path = _image.replace("####","%04d")
        if sound:
            sound_path = cmds.getAttr(sound + '.filename')
            if os.path.isfile(sound_path):
                self.conver_image_mov(production_image_path, _video_path, self._temp_config.get("fps"), _time ,sound = sound_path,start_frame = _min_time)
        else:
            self.conver_image_mov(production_image_path, _video_path, self._temp_config.get("fps"), _time, start_frame = _min_time)

        # 删除临时路径及文件
        try:
            _dir = os.path.dirname(production_image_path)
            shutil.rmtree(_dir)
        except:
            pass

        # 恢复原有的HUD显示
        self._restore_defalut()

        
        # 打开拍屏路径文件夹
        if self.playblast_widget.is_auto_open_folder():
            video_folder = os.path.normpath(os.path.dirname(_video_path))
            os.system("start explorer {}".format(video_folder))

        self.playblast_widget.setEnabled(True)

        return 0

    def conver_image_mov(self,image_path,outpath,fps,time,sound="",start_frame=101):
        _FFMPEG = get_ffmpeg()
        # -b:v 100000k -bufsize 150000k -vcodec h264  -x264opts keyint=1
        #_command = '{} -start_number {} -i {} -framerate {} -r {} -t {} -s {} -vcodec libx264 -crf 12 -pix_fmt yuv420p -y {}'.format(_FFMPEG, start_frame, image_path, fps, fps, time,resolution, outpath )
        _command = '{} -framerate {} -start_number {} -i {} -r {} -t {} -vcodec copy -acodec copy -y {}'.format(_FFMPEG, fps, start_frame, image_path, fps, time, outpath )

        if os.path.exists(sound):
            _command = '{} -framerate {} -start_number {} -i {} -i {} -r {} -t {} -shortest -vcodec libx264 -crf 12 -pix_fmt yuv420p -y {}'.format(_FFMPEG, fps, start_frame, image_path, sound, fps, time, outpath)

        _command=_command.encode(locale.getdefaultlocale()[1])
        print(_command)
        feedback = subprocess.call(_command)
        print(feedback)

    def process_image(self, image_path):
        _image = QtGui.QImage( image_path )
        painter = QtGui.QPainter()
        painter.begin(_image)
        self.painter(painter)
        painter.end()
        _image.save(image_path, quality = 100)

    def remove_all_hud(self):
        huds = cmds.headsUpDisplay(lh=True)
        if huds:
            for item in huds:
                cmds.headsUpDisplay(item, rem=True)

    def _restore_defalut(self):
        '''reset HUD info
        '''
        self.valuecolor = 16
        self.labelcolor = 16
        mm.eval("source initHUD.mel")

    def _get_temp_image_folder(self):
        _sys_temp = os.environ["TEMP"]
        _code,_ = os.path.splitext(cmds.file(q=True, sn=True, shn=True))
        _image_folder = os.path.join(_sys_temp, _code)
        if not os.path.exists(_image_folder):
            os.makedirs(_image_folder)
        return _image_folder

    def painter(self, painter, rect = None):
        _width = self._temp_config.get("image_size")[0]
        _height = self._temp_config.get("image_size")[1]
        print(_width, _height)
        _rect = QtCore.QRect( 0,
                              0,
                              int(_width),
                              int(_height)
                               )

        _font = QtGui.QFont(self._temp_config.get("font-family"))
        _font.setBold(self._temp_config.get("bold"))
        _font.setPixelSize(self._temp_config.get("font-size"))
        painter.setFont(_font)
        painter.drawRect(_width*0.05,_height*0.05,_width*0.9,_height*0.9)
        _margin = self._temp_config.get("margin")
        _text_height = self._temp_config.get("text-height")
        for _hud in self._temp_config.get("hud"):
            _horizontally, _vertically, _level = _hud.get("text-align")
            if _vertically == -1:
                _hud_rect = QtCore.QRect(_rect.x() + _margin[0],
                                         _rect.y() + _rect.height() - (
                                                     _margin[3] + _text_height * _level) - _text_height,
                                         _rect.width() - _margin[0] - _margin[2],
                                         _text_height)
            elif _vertically == 1:
                _hud_rect = QtCore.QRect(_rect.x() + _margin[0],
                                         _rect.y() + _margin[1] + _text_height * _level,
                                         _rect.width() - _margin[0] - _margin[2],
                                         _text_height)
            else:
                pass

            painter.setPen(QtGui.QPen(QtGui.QColor(_hud.get("color"))))

            text = u"未设置"
            exec (_hud.get("cmd"))
            if _horizontally == -1:
                painter.drawText(_hud_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)
            elif _horizontally == 0:
                painter.drawText(_hud_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)
            else:
                painter.drawText(_hud_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)


        
        painter.end()

    def resizeEvent(self,event):
        if self._temp_config:
            self._resize()
        super(Playblast, self).resizeEvent(event)

    def _resize(self):
        width_ratio =self._temp_config.get("image_size")[0]
        height_ratio = self._temp_config.get("image_size")[1]
        new_size = self.size()
        if (new_size.height()<width_ratio*new_size.height()/height_ratio):
            new_size.setHeight(height_ratio*new_size.width()/width_ratio)
        else:
            new_size.setWidth(width_ratio*new_size.height()/height_ratio)
        self.resize(new_size.width(), new_size.height() + self.playblast_widget.operation_widget.height())

    def _extra_path(self, path):
        _file_name = cmds.file(q=True, sn=True)
        _file_code,_ = os.path.splitext(cmds.file(q=True, sn=True, shn=True))
        _file_dir = path
        if os.path.isdir(_file_dir):
            _media_name = r"{}/{}.mov".format(_file_dir, _file_code)
            self.playblast_widget.set_path(_media_name)
    
    def _resolution_scale(self,_scale):
        _scale = float(_scale)
        self._temp_config = copy.deepcopy(self._config)
        self._temp_config["image_size"] = [int(self._temp_config.get("image_size")[0]*_scale),int(self._temp_config.get("image_size")[1]*_scale)]
        self.playblast_widget.init(self._temp_config)
        _huds = self._temp_config.get("hud")
        for _index, _hud in enumerate(_huds):
            if _hud.get("code") == "image_size":
                self._temp_config["hud"][_index]["cmd"] = "text = '{} x {}'".format(int(self._temp_config["image_size"][0]), int(self._temp_config["image_size"][1]))
                break

    def closeEvent(self, event):
        self._timer.stop()
        # self._snap_timer.stop()
        return super(Playblast, self).closeEvent(event)

    def showEvent(self, event):
        # 获取配置文件
        _hud_init = get_hud_init()
        self.init(_hud_init)

        self._resize()

        _file_name = cmds.file(q=True, sn=True)
        _file_code,_ = os.path.splitext(cmds.file(q=True, sn=True, shn=True))
        _file_dir = os.path.dirname(_file_name)
        if os.path.isdir(_file_dir):
            _media_name = r"{}/{}.mov".format(_file_dir, _file_code)
            self.playblast_widget.set_path(_media_name)
        
        self._temp_snap()

        # "glFrameTrigger"
        allJobs = cmds.scriptJob(lj = True)
        for job in allJobs:
            if "zfused_maya.tool.technology.playblast" in job:
                id = int(job.split(":")[0])
                cmds.scriptJob(kill= id, force=True)

        # cmds.scriptJob(e = ("timeChanged", self._temp_snap), protected = True)

        self._timer.start(1000)
        # self._snap_timer.start(1000*30)

        super(Playblast,self).showEvent(event)

    def _update(self):
        # self._temp_snap()
        self.update()

    def _temp_snap(self):
        _frame = int(cmds.currentTime(q = True))
        _temp_folder =self._get_temp_image_folder()
        _image = cmds.playblast( format ="image",
                                    filename = _temp_folder + "/snap",
                                    startTime = _frame, 
                                    endTime = _frame, 
                                    forceOverwrite =1,
                                    sequenceTime=0,
                                    clearCache=1,
                                    viewer=0, 
                                    showOrnaments=1, 
                                    offScreen=1, 
                                    fp=4,
                                    percent=100,
                                    compression="jpg",
                                    quality= 100,
                                    w = self._temp_config.get("image_size")[0],
                                    h = self._temp_config.get("image_size")[1] )
        _progress_image = _image.replace("####","{:0>4d}").format(_frame)
        self.playblast_widget.set_image(_progress_image)
        QtWidgets.QApplication.processEvents()

    def _cam_init(self,_config):
        view = OpenMayaUI.M3dView.active3dView()
        camDag = OpenMaya.MDagPath()
        view.getCamera(camDag)
        camerashape =camDag.fullPathName().split('|')[-1]
        for attr in _config:
            _attr = attr.get("attr")
            _value =attr.get("value")
            _type =attr.get("type")
            try:
                if _type:
                    setAttr("{}.{}".format(camerashape,_attr),_value,type=_type)
                else:
                    setAttr("{}.{}".format(camerashape,_attr),_value)
            except Exception as e:
                print(e)
                cmds.warning(u"{}.{} 设置失败".format(camerashape,_attr))
                pass


    def _build(self):
        self.set_title_name("Maya PlayBlast")
        self.playblast_widget = playblast_widget.PlayblastWidget()
        self.set_central_widget(self.playblast_widget)


if __name__ == '__main__':
    from zfused_maya.tool.technology.playblast import playblast_maya
    reload(playblast_maya)

    ui = playblast_maya.Playblast()

    ui.init(playblast_maya.HUD_INIT)

    ui.show()