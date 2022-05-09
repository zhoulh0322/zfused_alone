# coding:utf-8
#--author-- lanhua.zhou
from __future__ import print_function

import os
import glob
import shutil
import py_compile 

localPath = os.path.dirname(os.path.dirname(__file__))
print(localPath)
PATH = "//td/pipeline"
if not os.path.isdir(PATH):
    PATH = "//nas/zfused/pipeline"
serverPath = r"{}/zfused_pipeline/zfused_maya".format(PATH)

def bianli(path):
    _file_list = os.listdir(path)
    for i in _file_list:
        print(i)
        path_new = os.path.join(path,i)
        if os.path.isfile(path_new):
            if path_new.endswith(".pyc"):
                print(path_new)
                os.remove(path_new)
                
                # ser_path = path_new.replace(localPath,serverPath)
                # if not os.path.isdir(os.path.dirname(ser_path)):
                #     os.makedirs(os.path.dirname(ser_path))
                # try:
                #     shutil.copy(path_new, ser_path)
                # except:
                #     pass
                
        if os.path.isdir(path_new):
            if path_new.endswith("__pycache__"):
                shutil.rmtree(path_new)
            else:
                bianli(path_new)
    
bianli(localPath)