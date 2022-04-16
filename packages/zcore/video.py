# coding:utf-8
# --author-- lanhua.zhou

""" 视频文件操作函数集合 """

from __future__ import print_function

import os
import glob
import subprocess
import shutil
import tempfile
import hashlib
import locale

PATH = os.path.abspath("./plugins")
if not os.path.isdir(PATH):
    # get max app number
    _all_exe_path = glob.glob("{}/app-*".format(os.getcwd()))
    if _all_exe_path:
        _new_exe_path = max(_all_exe_path)
        PATH = "{}/plugins".format(_new_exe_path)
# DIRNAME = os.path.dirname(os.path.dirname(os.path.dirname(PATH)))
PLUGIN_DIRNAME = PATH

PLUGIN_DIRNAME = os.path.join( os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "plugins")

def cut_image(video, image):
    """ cut video to image
    :rtype: nool
    """
    _ffmpeg_exe = os.path.join(PLUGIN_DIRNAME,"ffmpeg/ffmpeg.exe")
    print(_ffmpeg_exe)
    _pic_command = '"{}" -i "{}" -vframes 1 "{}"'.format(_ffmpeg_exe, video, image)
    _pic_process = subprocess.Popen(_pic_command, shell = True)
    _pic_process.communicate()
    if not os.path.isfile(image):
        return False
    return True


def convert_video(inVideo, outVideo):
    """ convet video 
    :rtype: bool
    """
    _ffmpeg_exe = os.path.join(PLUGIN_DIRNAME,"ffmpeg/ffmpeg.exe")
    # _command = u'%s -i "%s" -vcodec h264 -x264opts keyint=1 -y "%s"'%(_ffmpeg_exe, inVideo, outVideo)
    _command = u'%s -i "%s" -vcodec h264 -x264opts keyint=1 -y "%s"'%(_ffmpeg_exe, inVideo, outVideo)
    print(_command)
    _command = _command.encode(locale.getdefaultlocale()[1])
    #_process = subprocess.Popen(_command, shell = True)
    #_process.communicate()
    subprocess.call(_command)
    if not os.path.isfile(outVideo):
        return False
    return True


def mergeVideo(filename, fps, size, images, audio = None, offset = None, time = None):
    _ffmpeg_exe = os.path.join(PLUGIN_DIRNAME,"ffmpeg/ffmpeg.exe")
    if audio:
        cmd = '%s -y -framerate %s -f image2 -s %s -i %s %s -i %s -vcodec libx264 -crf 25 -pix_fmt yuv420p -t %s %s'%(_ffmpeg_exe, fps, size, images, offset, audio, time, filename)
    else:
        cmd = '%s -y -framerate %s -f image2 -s %s -i %s -vcodec libx264 -crf 25 -pix_fmt yuv420p %s'%(_ffmpeg_exe, fps, size,images, filename)

    _process = subprocess.Popen(cmd, shell = True)
    _process.communicate()
    if not os.path.isfile(filename):
        return False
    return True