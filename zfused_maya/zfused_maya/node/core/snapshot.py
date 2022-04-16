# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 自动截图 """

import os
import maya.mel as mel
import maya.cmds as cmds


class Snapshot(object):
    def __init__(self, gpuShow = False):
        self.gpuShow = gpuShow

    def Snapshot(self,File):
        Dir = os.path.dirname(File)
        if os.path.exists(Dir) == False:
            os.makedirs(Dir)
        # File = File.split('.')[0]
        File = os.path.splitext(File)[0]
        WindowName = 'Snapshot'
        if cmds.window(WindowName,exists = True) == True:
            cmds.deleteUI(WindowName,window = True)
        if cmds.windowPref(WindowName,exists = True) == True:
            cmds.windowPref(WindowName,remove = True)
        cmds.window(WindowName,title = 'Snapshot')
        modelPanels=cmds.getPanel(typ="modelPanel")
        for currentPanel in modelPanels:
            cmds.modelEditor(currentPanel,e=True,displayAppearance = 'smoothShaded')        
        PaneLayout = cmds.paneLayout(width = 1920,height    = 1080)
        ModelPanel = cmds.modelPanel(copy = cmds.getPanel(withLabel = 'Front View'),menuBarVisible = False)
        cmds.showWindow(WindowName)
        cmds.modelEditor(ModelPanel,edit = True,useDefaultMaterial = True)
        mel.eval('setWireframeOnShadedOption false ' + ModelPanel)
        cmds.modelEditor(ModelPanel,edit = True,allObjects = False)
        cmds.modelEditor(ModelPanel,edit = True,polymeshes = True)
        if self.gpuShow:
            mel.eval('modelEditor -e -pluginObjects gpuCacheDisplayFilter true %s;'%ModelPanel)
        cmds.modelEditor(ModelPanel,edit = True,grid = False)
        mel.eval('SelectAllPolygonGeometry')
        if self.gpuShow:
            gpus = cmds.ls(type = "gpuCache")
            if gpus:
                cmds.select(gpus, add = True)
        mel.eval('LowQualityDisplay')

        cmds.viewFit(cmds.lookThru(ModelPanel,query = True),fitFactor = 0.7,animate = True)
        cmds.select(clear = True)
        cmds.modelEditor(ModelPanel,edit = True,activeView = True)
        cmds.playblast(startTime = 0,endTime = 0,format = 'iff',filename = File,sequenceTime = False,clearCache = True,viewer = False,showOrnaments = False,offScreen = True,framePadding = 4,percent = 100,compression = 'jpg',quality = 100)
        if cmds.window(WindowName,exists = True) == True:
            cmds.deleteUI(WindowName,window = True)
        if cmds.windowPref(WindowName,exists = True) == True:
            cmds.windowPref(WindowName,remove = True)
        if os.path.exists(File + '.jpg') == True:
            os.remove(File + '.jpg')
        os.rename(File + '.0000.jpg',File + '.jpg')


if __name__ == '__main__':
    Snapshot = Snapshot()
    Snapshot.Snapshot('D:/test.jpg')