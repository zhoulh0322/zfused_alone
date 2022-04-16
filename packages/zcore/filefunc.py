# coding:utf-8
# --author-- lanhua.zhou

""" 文件操作函数集合 """

import os
import sys
import re
import time
import shutil
import subprocess
import tempfile
import hashlib
import locale
import json
import logging

import zfused_api

logger = logging.getLogger(__name__)

def get_internal_trans_server_addr():
    _ip, _port = zfused_api.zFused.INTERNAL_TRANS_SERVER_ADDR.split(":")
    return "{}:{}".format(_ip, int(_port))

def get_transer_exe():
    _dir = os.path.dirname(__file__)
    _dir = os.path.dirname(_dir)
    _publish_exe = "{}/plugins/ztranser/client.exe".format(_dir)
    return _publish_exe

def md5_for_file(f, block_size=2**20):
    with open(f) as fHandle:
        md5 = hashlib.md5()
        while True:
            data = fHandle.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    return md5.hexdigest()

def is_hash_equal(f1, f2):
    if f1 == f2:
        return True
    if os.path.isfile(f1) and os.path.isfile(f2):
        str1 = md5_for_file(f1)  
        str2 = md5_for_file(f2)  
        return str1 == str2 
    return False

def receive_file(src, dst):
    """ 获取文件
        类似拷贝服务器文件
        返回是否领取成功
    :pargarms: src 源文件
    :pargarms: dst 目标文件
    
    :rtype: str
    """

    # check md5
    if is_hash_equal(src, dst):
        return True

    _src_file = src
    _dst_file = dst
    _publish_exe = get_transer_exe()
    if not os.path.isfile(_publish_exe):
        return False
    _ztranser_addr = get_internal_trans_server_addr()
    arg = u'"{}" {} get {} {}'.format(_publish_exe, _ztranser_addr, _src_file, _dst_file)
    # print(arg)
    arg = arg.encode(locale.getdefaultlocale()[1])

    #logger.info(arg)

    # publish info temp
    _publish_temp = tempfile.SpooledTemporaryFile(1024)
    _file_no = _publish_temp.fileno()
    _obj = subprocess.Popen(arg, stdout = _file_no, stderr = _file_no, shell = True)
    _obj.wait()
    _publish_temp.seek(0)
    _logger_data = _publish_temp.readlines()

    for i in _logger_data:
        #print(i)
        if "get over " in i:
            _dst_size = os.path.getsize(_dst_file)
            if int(i.split(" ")[-1]) == _dst_size:
                return True
            else:
                return False
    return False


def publish_file(src, dst, del_src = False):
    """ 上传文件
    
    :pargarms: src 源文件
    :pargarms: dst 目标文件
    :pargarms: del_src 是否删除源文件,默认不删除

    :rtype: bool
    """

    # check md5
    if is_hash_equal(src, dst):
        return True

    _publish_exe = get_transer_exe()
    print(_publish_exe)
    if not os.path.isfile(_publish_exe):
        return False
    # get ztranser server addr
    _ztranser_addr = get_internal_trans_server_addr()

    _src_file = src
    _dst_file = dst

    # # 移除测试下
    # _temp_dir = tempfile.gettempdir()
    # _temp_file = "%s/%s_%s"%(_temp_dir, time.time(), os.path.basename(src) ) # os.path.splitext(src)[-1]) 
    # logger.info("temp file {}".format(_temp_file))   
    # try:
    #     shutil.copy(src, _temp_file)
    # except Exception as e:
    #     logger.error(e)
    #     return False

    # # publish args
    # arg = u'"{}" {} send {} {}'.format(_publish_exe, _ztranser_addr, _temp_file, _dst_file)
    # logger.info(arg)
    # arg = arg.encode(locale.getdefaultlocale()[1])
    # print(arg)

    # publish args
    arg = u'"{}" {} send {} {}'.format(_publish_exe, _ztranser_addr, _src_file, _dst_file)
    logger.info(arg)
    arg = arg.encode(locale.getdefaultlocale()[1])

    # publish info temp_temp_file
    _publish_temp = tempfile.SpooledTemporaryFile(1024)
    _file_no = _publish_temp.fileno()
    _obj = subprocess.Popen(arg, stdout = _file_no, stderr = _file_no, shell = True)
    _obj.wait()
    _publish_temp.seek(0)
    _logger_data = _publish_temp.readlines()
    _dst_size = os.path.getsize(_src_file)

    # remove temp file
    # os.remove(_temp_file)

    # remove src file
    if del_src:
        os.remove(src)

    for i in _logger_data:
        if "send over " in i:
            if int(i.split(" ")[-1]) == _dst_size:
                return True
            else:
                return False
    return False