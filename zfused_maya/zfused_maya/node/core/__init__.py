# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

# -----------------------------------------------------------------------------
#  使用方法
# -----------------------------------------------------------------------------
# @viewportOff
# def export():
#     """
#     the export/bake process
#     """
#     # do something
#     _mel = 'playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -offScreen  -fp 4 -percent 50 -compression "none" -quality 70;'
#     mel.eval(_mel)

from functools import wraps
from maya import cmds
from maya import mel

def viewportOff( func ):
    """
    Decorator - turn off Maya display while func is running.
    if func will fail, the error will be raised after.
    """
    @wraps(func)
    def wrap( *args, **kwargs ):
 
        # Turn $gMainPane Off:
        mel.eval("paneLayout -e -manage false $gMainPane")
 
        # Decorator will try/except running the function. 
        # But it will always turn on the viewport at the end.
        # In case the function failed, it will prevent leaving maya viewport off.
        try:
            return func( *args, **kwargs )
        except Exception:
            raise # will raise original error
        finally:
            mel.eval("paneLayout -e -manage true $gMainPane")
 
    return wrap
 

from . import assembly
from . import attr
from . import reducemesh