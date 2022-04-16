# coding:utf-8
# --author-- lanhua.zhou

from Qt import QtGui, QtWidgets, QtCore, QtCompat

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

def GetMayaMainWindowPoint():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(int(ptr), QtWidgets.QWidget)

def GetMayaLayoutPoint(layoutName):
    ptr = OpenMayaUI.MQtUtil.findLayout(layoutName)
    return QtCompat.wrapInstance(int(ptr), QtWidgets.QWidget)

def GetMayaPoint(mayaName):
    """
    Convert a Maya ui path to a Qt object
    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    @return: PyQt representation of that object
    """
    ptr = OpenMayaUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(mayaName)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenu(mayaName)
    if ptr is not None:
        return QtCompat.wrapInstance(int(ptr), QtCore.QObject)

def BuiltInMaya(qt_widget):
    window = cmds.window()
    layout = cmds.formLayout(parent = window)
    qtobj = QtCompat.wrapInstance(int(OpenMayaUI.MQtUtil.findLayout(layout)), QtWidgets.QWidget)
    qtobj.layout().addWidget(qt_widget)
    child = cmds.formLayout(layout, q = True, childArray =True)
    cmds.formLayout(layout, edit=True, attachForm=[(child[0], 'right', 0), (child[0], 'left', 0),(child[0], 'top', 0),(child[0], 'bottom', 0)])
    # cmds.setParent('..')
    return window

# # -----------------------------------------------
# from . import menuinterface
# from . import contentinterface
# from . import projectinterface
# from . import userinterface

# def content_interface():
#     from . import contentinterface
#     _ptr = OpenMayaUI.MQtUtil.findControl("zfused_maya_content_interface")
#     _interface = QtCompat.wrapInstance(int(_ptr), contentinterface.contentguide.ContentGuide)
#     return _interface