# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function
from functools import partial

import sys



def clear():
    # remove class
    for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_maya')):
        del sys.modules[k]
    for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zfused_api')):
        del sys.modules[k]
    for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zcore')):
        del sys.modules[k]
    for k in sorted(k for k, m in sys.modules.items() if m and k.startswith('zwidgets')):
        del sys.modules[k]

