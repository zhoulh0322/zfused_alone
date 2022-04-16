#coding:utf-8

import re
import maya.cmds as cmds


class ColliderGroup():
    def __init__(self):
        pass
    def showUi(self):
        windowName = 'Collider Group'
        if cmds.window(windowName,exists = True) == True:
            cmds.deleteUI(windowName,window = True)
        if cmds.windowPref(windowName,exists = True) == True:
            cmds.windowPref(windowName,remove = True)
        Window = cmds.window(windowName, title = 'Collider Group', sizeable = False)
        forL = cmds.formLayout(parent = Window)
        textB = cmds.text(label = 'Group Name:')
        textF = cmds.textField(width = 300, height = 25, parent = forL)
        creatB = cmds.button(parent = forL, label = 'Create', command = lambda *args: self.creat())
        addB = cmds.button(parent = forL, label = 'Add', command = lambda *args: self.add())
        cmds.formLayout(forL, edit = True, attachForm = [
        (textB, 'top', 8),
        (textB, 'left', 8),
        (textF, 'top', 3),
        (textF, 'right', 3),
        (creatB, 'left', 3),
        (creatB, 'right', 3),
        (addB, 'left', 3),
        (addB, 'right', 3),
        (addB, 'bottom', 3)
        ],
        attachControl = [
        (textF, 'left', 5, textB),
        (creatB, 'top', 5, textF),
        (addB, 'top', 5, creatB),
        ])
        self.textF = textF
        self.Window = Window
        self.getattr()
    def getattr(self):
        window = self.Window
        typeName = ''
        treeName = ''
        if cmds.objExists('*_model_GRP'):
            cmds.select('*_model_GRP')
            grpList = cmds.ls(selection = True)
            typeName = cmds.getAttr(grpList[0] + '.Type')
            treeName = cmds.getAttr(grpList[0] + '.treeName')
            cmds.select(clear = True)
            cmds.showWindow(window)
        else:
            cmds.confirmDialog(message = u'大纲有误请确认', button = ['Yes'], defaultButton = 'Yes')
        self.typeName = typeName
        self.treeName = treeName
    def textFF(self):
        textF = self.textF
        content = cmds.textField(textF, query = True, text = True)
        print content
        return content
    def creat(self):
        groupName = self.textFF()
        if groupName != '':
            self.creatGrp()
        else:
            cmds.confirmDialog(message = u'请填写组名', button = ['Yes'], defaultButton = 'Yes')
    def creatGrp(self):
        groupName = self.textFF()
        typeName = self.typeName
        treeName = self.treeName
        grpList = ['_nrigid_GRP', '_ncloth_GRP', '_nucleus_GRP', '_collider_GRP']
        if cmds.objExists(typeName + '_' + treeName + '_' + groupName + '_GRP') == False:
            xxxGrp = cmds.group(empty = True, name = typeName + '_' + treeName + '_' + groupName + '_GRP')
            cmds.parent(xxxGrp, typeName + '_' + treeName + '_' + 'solverCloth_GRP')
            for i in grpList:
                grpName = cmds.group(empty = True, name = typeName + '_' + treeName + '_' + groupName + i)
                self.addTreeAttr(typeName + '_' + treeName + '_' + groupName + i,i.split('_')[1])
                cmds.parent(grpName, xxxGrp)
        else:
            cmds.confirmDialog(message = u'该组已经存在', button = ['Yes'], defaultButton = 'Yes')
    def addTreeAttr(self,groupName,attrName):
        cmds.addAttr(groupName,longName = 'Name',dataType = 'string')
        cmds.addAttr(groupName,longName = 'Type',dataType = 'string')
        cmds.setAttr(groupName + '.Name', attrName, type = 'string', lock = True)
        cmds.setAttr(groupName + '.Type', 'c', type = 'string', lock = True)                
    def add(self):
        groupName = self.textFF()
        typeName = self.typeName
        treeName = self.treeName
        objList = cmds.ls(selection = True)
        targetGroup = typeName + '_' + treeName + '_' + groupName + '_collider_GRP'
        newName = typeName + '_' + treeName + '_' + groupName + '_collider'
        if len(objList) == 0:
            cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')
        else:
            if cmds.objExists(targetGroup) == True:
                for i in objList:
                    if cmds.listRelatives(i,parent=1) != None:
                        if cmds.listRelatives(i,parent=1)[0] <> targetGroup:# python2中的‘<>’不等于运算符，python3中已废弃；‘<>’类似于‘!=’
                            cmds.parent(i,targetGroup)
                            cmds.rename(i,newName)
                    else:
                        cmds.parent(i,targetGroup)
                        cmds.rename(i,newName)                        
            else:
                cmds.confirmDialog(message = u'没有该组', button = ['Yes'], defaultButton = 'Yes')
        cmds.select(cl=1)

if __name__ == '__main__':
    ColliderGroup = ColliderGroup()
    ColliderGroup.showUi()
    