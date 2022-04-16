# coding:utf-8
# --author-- lanhua.zhou

import sys
import maya.utils

_pipeline_path = r"P:\zfused\pipeline\zfused_alone"

def _python_version():
    _ver = sys.version_info
    _major = _ver.major
    _minor = _ver.minor
    return "_python%s.%s" % (_major, _minor)

sys.path.append(r"{}\libs\{}".format(_pipeline_path, _python_version()))
sys.path.append(r"{}\packages".format(_pipeline_path))
sys.path.append(r"{}\zfused_maya".format(_pipeline_path))

import zfused_maya

maya.utils.executeDeferred(zfused_maya.login)