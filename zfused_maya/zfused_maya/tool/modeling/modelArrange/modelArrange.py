#coding:utf-8
import maya.cmds as cmds
import string
import colliderGroup
reload(colliderGroup)

class Ui(object):
    def showUi(self):
        self.windowName = 'ModelArrange'
        if cmds.window(self.windowName, exists = True) == True:
            cmds.deleteUI(self.windowName, window = True)
        if cmds.windowPref(self.windowName, exists = True) == True:
            cmds.windowPref(self.windowName, remove = True)
        self.creatTWindow = cmds.window(self.windowName, title = self.windowName, sizeable = True, tlc = [280, 430])
        self.windowFoL = cmds.formLayout(parent = self.creatTWindow)
        self.creatFrL = cmds.frameLayout(parent = self.windowFoL, label = 'Create Tree')
        self.creatTRCL = cmds.rowColumnLayout(parent = self.creatFrL, numberOfColumns = 5, columnSpacing = [(1, 8), (2, 7), (3, 7), (4, 6)])
        cmds.text(label='Name:', parent = self.creatTRCL)
        self.textFG = cmds.textField(parent = self.creatTRCL, enterCommand = lambda *args: self.creatTree())
        self.typeOM = cmds.optionMenu(parent = self.creatTRCL)        
        cmds.menuItem(parent = self.typeOM, label = 'Characters')
        cmds.menuItem(parent = self.typeOM, label = 'Props')
        cmds.menuItem(parent = self.typeOM, label = 'Scene')
        cmds.menuItem(parent = self.typeOM, label = 'MeshGen')
        cmds.optionMenu(self.typeOM,e=1,cc=lambda *args: self.judgeWin())
        cmds.button(parent = self.creatTRCL, label = 'Create', width = 87, command = lambda *args: self.creatTree())
        cmds.formLayout(parent = self.creatTRCL,w=11)
        self.setNameSpace()
        self.characterComp()
        self.GRPExists()
    def characterComp(self):
        self.controlFrL = cmds.frameLayout(parent = self.windowFoL, label = 'Control', collapsable = True, collapse = True)
        groupFrL = cmds.frameLayout(parent = self.controlFrL, label = 'Geometry Group', collapsable = True, collapse = True)
        controlFoL = cmds.formLayout(parent = groupFrL)
        cmds.formLayout(self.windowFoL, edit = True, attachForm = [
        (self.creatFrL, 'top', 5),
        (self.creatFrL, 'left', 5),
        (self.creatFrL, 'right', 5),
        (self.controlFrL, 'left', 5),
        (self.controlFrL, 'right', 5),
        (self.controlFrL, 'bottom', 5)
        ],
        attachControl = [
        (self.controlFrL, 'top', 5, self.creatFrL)
        ])
        cmds.showWindow(self.creatTWindow)
        self.controlFoL = controlFoL
        self.multipleGRP()
        self.Daniel_modleAss()
        textExist = cmds.textField(self.textFG, query = True, text = True)
        cmds.select(cl=1)
    def propComp(self):
        controlFrL = cmds.frameLayout(parent = self.windowFoL, label = 'Control', collapsable = True, collapse = False)
        porpAssBtn = cmds.button('propBtn',l='geometry',p=controlFrL,c=lambda *args: self.snakeCommand(porpAssBtn))
        cmds.formLayout(self.windowFoL, edit = True, attachForm = [
        (self.creatFrL, 'top', 5),
        (self.creatFrL, 'left', 5),
        (self.creatFrL, 'right', 5),
        (controlFrL, 'left', 5),
        (controlFrL, 'right', 5),
        (controlFrL, 'bottom', 5)
        ],
        attachControl = [
        (controlFrL, 'top', 5, self.creatFrL)
        ])        
        cmds.showWindow(self.creatTWindow)
        self.controlFrL = controlFrL      
        
                
    def Daniel_modleAss(self):
        creatTRCL = cmds.rowColumnLayout(parent = self.controlFoL, numberOfColumns = 2, columnSpacing = [(1, 10)])
        f = cmds.formLayout(nd=100,parent = creatTRCL)
        hairAssBut = cmds.button('hairBut',l="hair",w=100,h=30,bgc = [0.9,0.4,0],command = lambda *args: self.snakeCommand(hairAssBut))
        beardAssBut = cmds.button('beardBut',l='beard',w=50,h=50,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(beardAssBut))
        headBut = cmds.button('head',l='head',w=80,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(headBut))
        R_earAssBut = cmds.button('R_earBut',l='R_ear',w=50,h=60,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(R_earAssBut))
        L_earAssBut = cmds.button('L_earBut',l='L_ear',w=50,h=60,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(L_earAssBut))
        R_elbowAssBut = cmds.button('R_elbowBut',l='R_brow',w=60,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(R_elbowAssBut))
        L_elbowAssBut = cmds.button('L_elbowBut',l='L_brow',w=60,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(L_elbowAssBut))
        R_eyeAssBut = cmds.button('R_eyeBut',l='R_eye',w=60,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(R_eyeAssBut))
        L_eyeAssBut = cmds.button('L_eyeBut',l='L_eye',w=60,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(L_eyeAssBut))
        R_upLassAssBut = cmds.button('R_upLassBut',l='R_upLash',w=60,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.lashCommand_R())
        L_upLassAssBut = cmds.button('L_upLassBut',l='L_upLash',w=60,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.lashCommand_L())
        R_lowLassAssBut = cmds.button('R_lowLassBut',l='R_lowLash',w=60,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.lashCommand_R())
        L_lowLassAssBut =cmds.button('L_lowLassBut',l='L_lowLash',w=60,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.lashCommand_L())
        upTeeAssBut = cmds.button('up_teeBut',l='upTeeth',w=100,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(upTeeAssBut))
        tongueAssBut = cmds.button('tongueBut',l='tongue',w=100,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(tongueAssBut))
        lowTeeAssBut = cmds.button('low_teeBut',l='lowTeeth',w=100,h=20,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(lowTeeAssBut))
        nonnasalityBut = cmds.button('n_lity',l='nonnasality',w=100,h=20,bgc=[0.9,0.4,0.0],command = lambda *args: self.snakeCommand(nonnasalityBut))
        bodyBut = cmds.button('bodyBut',l='body',w=80,h=50,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(bodyBut))
        bodyAssBut = cmds.button('bodyAssBut',l='bodyAss',w=80,h=40,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(bodyAssBut))
        closeEyeBut = cmds.button('closeEyeBut',l='closeEye',w=80,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(closeEyeBut))
        openEyeBut = cmds.button('openEyeBut',l='openEye',w=80,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(openEyeBut))
        
        R_armAssBut = cmds.button('R_armBut',l='R_arm',w=50,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(R_armAssBut))
        L_armAssBut = cmds.button('L_armBut',l='L_arm',w=50,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(L_armAssBut))
        R_handAssBut = cmds.button('R_handBut',l='R_hand',w=50,h=40,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(R_handAssBut))
        L_handAssBut = cmds.button('L_handBut',l='L_hand',w=50,h=40,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(L_handAssBut))
        R_legAssBut = cmds.button('R_legBut',l='R_leg',w=40,h=40,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(R_legAssBut))
        L_legAssBut = cmds.button('L_legBut',l='L_leg',w=40,h=40,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(L_legAssBut))
        R_footAssBut = cmds.button('R_footBut',l='R_foot',w=50,h=40,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(R_footAssBut))
        L_footAssBut = cmds.button('L_footBut',l='L_foot',w=50,h=40,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(L_footAssBut))
        R_shoeAssBut = cmds.button('R_shoeBut',l='R_shoe',w=50,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(R_shoeAssBut))
        L_shoeAssBut = cmds.button('L_shoeBut',l='L_shoe',w=50,h=20,bgc=[0.9,0.4,0],command = lambda *args: self.snakeCommand(L_shoeAssBut))
        
        headAssBut = cmds.button('headBut',l='headAss',parent = f,w=100,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(headAssBut))
        clothBut = cmds.button('clothBut',l='cloth',parent = f,w=70,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(clothBut))
        solverBut = cmds.button('solvermodelBut',l='solvermodel',parent = f,w=70,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.snakeCommand(solverBut))
        disBut = cmds.button('disBut',l='display/hide',parent = f,w=70,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.setDisplay())
        colliderBut = cmds.button('collider',l='colliderBut',parent = f,w=70,h=30,bgc=[0.9,0.9,0.9],command = lambda *args: self.colliderApp())
        
        cmds.formLayout(f,e=1,attachForm=[
        (hairAssBut,'left',110),
        (hairAssBut,'top',0),
        (headBut,'left',120),
        (headBut,'top',31),
        (R_earAssBut,'left',10),
        (R_earAssBut,'top',81),
        (L_earAssBut,'left',265),
        (L_earAssBut,'top',81),
        (R_elbowAssBut,'left',70),
        (R_elbowAssBut,'top',61),
        (L_elbowAssBut,'left',190),
        (L_elbowAssBut,'top',61),
        (R_eyeAssBut,'left',70),
        (R_eyeAssBut,'top',101),
        (R_upLassAssBut,'left',70),
        (R_upLassAssBut,'top',81),
        (R_lowLassAssBut,'left',70),
        (R_lowLassAssBut,'top',121),
        (L_upLassAssBut,'left',190),
        (L_upLassAssBut,'top',81),
        (L_lowLassAssBut,'left',190),
        (L_lowLassAssBut,'top',121),
        (L_eyeAssBut,'left',190),
        (L_eyeAssBut,'top',101),
        (beardAssBut,'left',265),
        (beardAssBut,'top',181),
        (upTeeAssBut,'left',110),
        (upTeeAssBut,'top',181),
        (tongueAssBut,'left',110),
        (tongueAssBut,'top',201),
        (lowTeeAssBut,'left',110),
        (lowTeeAssBut,'top',221),
        (nonnasalityBut,'left',110),
        (nonnasalityBut,'top',241),
        (R_armAssBut,'left',65),
        (R_armAssBut,'top',291),
        (bodyBut,'left',120),
        (bodyBut,'top',311),
        (bodyAssBut,'left',120),
        (bodyAssBut,'top',371),
        
        (closeEyeBut,'left',0),
        (closeEyeBut,'top',181),
        (openEyeBut,'left',0),
        (openEyeBut,'top',221),
        (L_armAssBut,'left',205),
        (L_armAssBut,'top',291),
        (R_handAssBut,'left',30),
        (R_handAssBut,'top',371),
        (L_handAssBut,'left',240),
        (L_handAssBut,'top',371),
        (R_legAssBut,'left',120),
        (R_legAssBut,'top',426),
        (L_legAssBut,'left',160),
        (L_legAssBut,'top',426),
        (R_footAssBut,'left',100),
        (R_footAssBut,'top',541),
        (L_footAssBut,'left',170),
        (L_footAssBut,'top',541),
        (R_shoeAssBut,'left',50),
        (R_shoeAssBut,'top',561),
        (L_shoeAssBut,'left',220),
        (L_shoeAssBut,'top',561),
        (headAssBut,'left',210),
        (headAssBut,'top',0),
        (clothBut,'left',10),
        (clothBut,'bottom',0),
        (solverBut,'left',95),
        (solverBut,'bottom',0),
        (disBut,'left',250),
        (disBut,'bottom',0),
        (colliderBut,'left',170),
        (colliderBut,'bottom',0)
        ])    
        self.hairAssBut = hairAssBut
        self.beardAssBut = beardAssBut
        self.headBut = headBut
        self.R_earAssBut = R_earAssBut
        self.L_earAssBut = L_earAssBut
        self.R_elbowAssBut = R_elbowAssBut
        self.L_elbowAssBut = L_elbowAssBut
        self.R_eyeAssBut = R_eyeAssBut
        self.L_eyeAssBut = L_eyeAssBut
        self.R_upLassAssBut = R_upLassAssBut
        self.L_upLassAssBut = L_upLassAssBut    
        self.R_lowLassAssBut = R_lowLassAssBut
        self.L_lowLassAssBut = L_lowLassAssBut
        self.upTeeAssBut = upTeeAssBut
        self.tongueAssBut = tongueAssBut
        self.lowTeeAssBut = lowTeeAssBut
        self.nonnasalityBut = nonnasalityBut
        self.R_armAssBut = R_armAssBut
        self.bodyBut = bodyBut
        self.bodyAssBut = bodyAssBut
        self.L_armAssBut = L_armAssBut
        self.R_handAssBut = R_handAssBut
        self.L_handAssBut = L_handAssBut
        self.R_legAssBut = R_legAssBut
        self.L_legAssBut = L_legAssBut
        self.R_footAssBut = R_footAssBut
        self.L_footAssBut = L_footAssBut
        self.R_shoeAssBut = R_shoeAssBut
        self.L_shoeAssBut = L_shoeAssBut   
        self.closeEyeBut = closeEyeBut
        self.openEyeBut = openEyeBut
        self.colliderBut = colliderBut

    def creatTree(self):
        typeOM = self.typeOM
        textFG = self.textFG
        confirmD = ''
        typeOMI = cmds.optionMenu(typeOM, query = True, select = True)
        treeName = cmds.textField(textFG, query = True, text = True)
        if treeName=='':
            cmds.confirmDialog(message=u'请输入资产名字！\n\n命名只能由【英文】、【数字】和【下划】线构成，并且首字母必须是英文。\n请注意项目文件名、贴图和物体名字都只能用这些字符。')
            return
        for char in treeName:
            if char not in (string.letters+string.digits+'_'):
                cmds.confirmDialog(message=u'命名只能由【英文】、【数字】和【下划】线构成，并且首字母必须是英文。\n请注意项目文件名、贴图和物体名字都只能用这些字符。\n\n发现资产名中输入了不识别的字：" %s "'%char.replace(' ',u'空格').replace('\t',u'ＴＡＢ'))
                return
        if treeName[0] not in string.letters:
            cmds.confirmDialog(message=u'命名只能由【英文】、【数字】和【下划】线构成，并且首字母必须是英文。\n请注意项目文件名、贴图和物体名字都只能用这些字符。\n\n发现资产名不符合规范')
            return
        if typeOMI in [1,2,3,4]:
            #~ if cmds.objExists('*_model_GRP') == True:
                #~ cmds.select('*_model_GRP')
                #~ GRPName = cmds.ls(sl = True)
            GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
            if GRPName!=[]:
                if cmds.objExists(GRPName[0] + '.treeName') == True:
                    treeType = cmds.getAttr(GRPName[0] + '.Type')
                    if (typeOMI==1 and treeType =='c') or (typeOMI==2 and treeType =='p') or (typeOMI==3 and treeType =='s'):
                        if self.renameTree_1() == 'OK':
                            if treeName.strip() == '':
                                cmds.confirmDialog(message = u'请输入名字', button = ['Yes'], defaultButton = 'Yes')
                            else:
                                cmds.delete(GRPName[0])
                                self.charactersTree()                        
                    else:
                        NameStr = cmds.getAttr(GRPName[0] + '.treeName')
                        confirmD = cmds.confirmDialog(message = u'已有组:' + NameStr + u'   是否清除原有组(包括组里物体)创建新组？', button = ['Yes', 'No'], defaultButton = 'Yes')
                else:
                    cmds.addAttr(GRPName[0], longName = 'treeName', dataType = 'string')
                    cmds.setAttr(GRPName[0] + '.treeName', treeName, type = 'string', lock = True)
                if confirmD == 'Yes':
                    cmds.delete(GRPName)
                    if typeOMI == 1:
                        self.charactersTree()
                    if typeOMI == 2:
                        self.propsTree()
                    if typeOMI == 3:
                        self.sceneTree()
            else:
                if treeName.strip() == '':
                    cmds.confirmDialog(message = u'请输入名字', button = ['Yes'], defaultButton = 'Yes')
                else:
                    if typeOMI == 1:
                        self.charactersTree()
                    if typeOMI == 2:
                        self.propsTree()
                    if typeOMI == 3:
                        self.sceneTree()
                    if typeOMI == 4:
                        self.meshGenTree()
    def snakeCommand(self, button):
        buttonL = cmds.button(button, query = True, label = True)
        self.parentGrp(buttonL)
    def lashCommand_L(self):
        groupName = cmds.textField(self.textFG, query = True, text = True)
        Groups = 'c_' + groupName +'_L_lash_GRP'
        objectName = cmds.ls(selection = True)
        if cmds.listRelatives(objectName,c=1,shapes=1) == None:
            cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')
            return
        NewName = 'c_' + groupName + '_L_lash'
        for i in objectName:
            cmds.select(i)
            if cmds.listRelatives(i,p=1)!= None and cmds.listRelatives(i,p=1)[0] == Groups:
                pass
            else:
                cmds.parent(i,Groups)
                cmds.rename(cmds.ls(sl=1),NewName)
                sel = cmds.ls(sl= True)[0]                         
                shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                cmds.rename(shape,self.getShapeName(sel))                
        cmds.inViewMessage(amg = '已入组', pos = 'midCenter', fade = True)
        cmds.select(cl=1)
    def lashCommand_R(self):
        groupName = cmds.textField(self.textFG, query = True, text = True)
        Groups = 'c_' + groupName +'_R_lash_GRP'
        objectName = cmds.ls(selection = True)
        if cmds.listRelatives(objectName,c=1,shapes=1) == None:
            cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')
            return
        NewName = 'c_' + groupName + '_R_lash'
        for i in objectName:
            cmds.select(i)
            if cmds.listRelatives(i,p=1)!= None and cmds.listRelatives(i,p=1)[0] == Groups:
                pass
            else:            
                cmds.parent(i,Groups)
                cmds.rename(cmds.ls(sl=1),NewName)  
                sel = cmds.ls(sl= True)[0]                         
                shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                cmds.rename(shape,self.getShapeName(sel))                
        cmds.inViewMessage(amg = '已入组', pos = 'midCenter', fade = True)  
        cmds.select(cl=1)
    def charactersTree(self):
        FileType = 'c_'
        treeName = cmds.textField(self.textFG, query = True, text = True).strip()
        modelGRP = FileType + treeName + '_model_GRP'
        geometryGRP = FileType + treeName + '_geometry_GRP'
        headGRP = FileType + treeName + '_head_GRP'
        hairGRP = FileType + treeName + '_hair_GRP'
        headAssGRP = FileType + treeName + '_headAss_GRP'
        
        tarGRP = FileType + treeName + '_tar_GRP'
        closeEyeGRP = FileType + treeName + '_closeEye_GRP'
        openEyeGRP = FileType + treeName + '_openEye_GRP'
        
        eyeGRP = FileType + treeName + '_eye_GRP'
        LeyeGRP = FileType + treeName + '_L_eye_GRP'
        ReyeGRP = FileType + treeName + '_R_eye_GRP'
        browGRP = FileType + treeName + '_brow_GRP'
        LbrowGRP = FileType + treeName + '_L_brow_GRP'
        RbrowGRP = FileType + treeName + '_R_brow_GRP'        
        lashGRP = FileType + treeName + '_lash_GRP'
        LlashGRP = FileType + treeName + '_L_lash_GRP'
        RlashGRP = FileType + treeName + '_R_lash_GRP'        
        earGRP = FileType + treeName + '_ear_GRP'
        LearGRP = FileType + treeName + '_L_ear_GRP'
        RearGRP = FileType + treeName + '_R_ear_GRP'
        beardGRP = FileType + treeName + '_beard_GRP'
        mouthGRP = FileType + treeName + '_mouth_GRP'
        tongueGRP = FileType + treeName + '_tongue_GRP'
        upTeethGRP = FileType + treeName + '_upTeeth_GRP'
        lowTeethGRP = FileType + treeName + '_lowTeeth_GRP'
        nonnasalityGRP = FileType + treeName + '_nonnasality_GRP'
        bodyGRP = FileType + treeName + '_body_GRP'
        bodyAssGRP = FileType + treeName + '_bodyAss_GRP'
        
        RarmGrp = FileType + treeName + '_R_arm_GRP'
        LarmGrp = FileType + treeName + '_L_arm_GRP'
        RhandGrp = FileType + treeName + '_R_hand_GRP'
        LhandGrp = FileType + treeName + '_L_hand_GRP'
        RlegGrp = FileType + treeName + '_R_leg_GRP'
        LlegGrp = FileType + treeName + '_L_leg_GRP'
        RshoeGrp = FileType + treeName + '_R_shoe_GRP'
        LshoeGrp =FileType + treeName + '_L_shoe_GRP'
        RfootGrp = FileType + treeName + '_R_foot_GRP'
        LfootGrp = FileType + treeName + '_L_foot_GRP'
        
        clothGRP = FileType + treeName + '_cloth_GRP'
        deformGRP = FileType + treeName + '_deform_GRP'
        solverClothGRP = FileType + treeName + '_solverCloth_GRP'
        #xxxGRP = FileType + treeName + '_xxx_GRP'
        nrigidGRP = FileType + treeName + '_nrigid_GRP'
        nclothGRP = FileType + treeName + '_ncloth_GRP'
        nucleusGRP = FileType + treeName + '_nucleus_GRP'
        ClothfieldGRP = FileType + treeName + '_Clothfield_GRP'
        solvermodelGRP = FileType + treeName + '_solvermodel_GRP'
        colliderGRP = FileType + treeName + '_collider_GRP'
        if cmds.objExists(modelGRP) == False:
            cmds.group(empty = True, name = modelGRP)
            cmds.addAttr(longName = 'treeName', dataType = 'string')
            cmds.addAttr(longName = 'Name',dataType = 'string')
            cmds.addAttr(longName = 'Type',dataType = 'string')
            cmds.setAttr(modelGRP + '.treeName', treeName, type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Name', 'model', type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Type', 'c', type = 'string', lock = True)
        if cmds.objExists(geometryGRP) == False:
            cmds.group(empty = True, name = geometryGRP, parent = modelGRP)
            self.addTreeAttr(geometryGRP,'geometrty')
            cmds.addAttr(geometryGRP,longName = 'Morh',dataType = 'string')
            cmds.setAttr(geometryGRP + '.Morh', 'm', type = 'string', lock = True) 
            cmds.addAttr(geometryGRP,longName = "rendering",at = 'bool')
            cmds.setAttr("%s.rendering"%geometryGRP, True)        
        if cmds.objExists(headGRP) == False:
            cmds.group(empty = True, name = headGRP, parent = geometryGRP)
            self.addTreeAttr(headGRP,'head')
        if cmds.objExists(hairGRP) == False:
            cmds.group(empty = True, name = hairGRP, parent = headGRP)
            self.addTreeAttr(hairGRP,'hair')
        if cmds.objExists(browGRP) == False:
            cmds.group(empty = True, name = browGRP, parent = headGRP)
            self.addTreeAttr(browGRP,'brow')
        if cmds.objExists(LbrowGRP) == False:
            cmds.group(empty = True, name = LbrowGRP, parent = browGRP)
            self.addTreeAttr(LbrowGRP,'Lbrow')
        if cmds.objExists(RbrowGRP) == False:
            cmds.group(empty = True, name = RbrowGRP, parent = browGRP) 
            self.addTreeAttr(RbrowGRP,'Rbrow')                   
        if cmds.objExists(lashGRP) == False:
            cmds.group(empty = True, name = lashGRP, parent = headGRP)
            self.addTreeAttr(lashGRP,'lash')
        if cmds.objExists(LlashGRP) == False:
            cmds.group(empty = True, name = LlashGRP, parent = lashGRP)
            self.addTreeAttr(LlashGRP,'Llash')
        if cmds.objExists(RlashGRP) == False:
            cmds.group(empty = True, name = RlashGRP, parent = lashGRP) 
            self.addTreeAttr(RlashGRP,'Rlash') 
        if cmds.objExists(eyeGRP) == False:
            cmds.group(empty = True, name = eyeGRP, parent = headGRP)
            self.addTreeAttr(eyeGRP,'eye')
        if cmds.objExists(LeyeGRP) == False:
            cmds.group(empty = True, name = LeyeGRP, parent = eyeGRP)
            self.addTreeAttr(LeyeGRP,'Leye')
        if cmds.objExists(ReyeGRP) == False:
            cmds.group(empty = True, name = ReyeGRP, parent = eyeGRP)
            self.addTreeAttr(ReyeGRP,'Reye')
        if cmds.objExists(earGRP) == False:
            cmds.group(empty = True, name = earGRP, parent = headGRP)
            self.addTreeAttr(earGRP,'ear')
        if cmds.objExists(LearGRP) == False:
            cmds.group(empty = True, name = LearGRP, parent = earGRP)
            self.addTreeAttr(LearGRP,'Lear')            
        if cmds.objExists(RearGRP) == False:
            cmds.group(empty = True, name = RearGRP, parent = earGRP) 
            self.addTreeAttr(RearGRP,'Rear')                           
        if cmds.objExists(mouthGRP) == False:
            cmds.group(empty = True, name = mouthGRP, parent = headGRP)
            self.addTreeAttr(mouthGRP,'mouth')
        if cmds.objExists(tongueGRP) == False:
            cmds.group(empty = True, name = tongueGRP, parent = mouthGRP)
            self.addTreeAttr(tongueGRP,'tongue')
        if cmds.objExists(upTeethGRP) == False:
            cmds.group(empty = True, name = upTeethGRP, parent = mouthGRP)
            self.addTreeAttr(upTeethGRP,'upTeeth')
        if cmds.objExists(lowTeethGRP) == False:
            cmds.group(empty = True, name = lowTeethGRP, parent = mouthGRP)
            self.addTreeAttr(lowTeethGRP,'lowTeeth')
        if cmds.objExists(nonnasalityGRP) == False:
            cmds.group(empty = True, name = nonnasalityGRP, parent = mouthGRP)
            self.addTreeAttr(nonnasalityGRP,'nonnasality')
        if cmds.objExists(beardGRP) == False:
            cmds.group(empty = True, name = beardGRP, parent = headGRP)
            self.addTreeAttr(beardGRP,'beard')
        if cmds.objExists(headAssGRP) == False:
            cmds.group(empty = True, name = headAssGRP, parent = headGRP)
            self.addTreeAttr(headAssGRP,'headAss')
        if cmds.objExists(tarGRP) == False:
            cmds.group(empty = True, name = tarGRP, parent = headGRP)
            self.addTreeAttr(tarGRP,'tar')            
        if cmds.objExists(closeEyeGRP) == False:
            cmds.group(empty = True, name = closeEyeGRP, parent = tarGRP)
            self.addTreeAttr(closeEyeGRP,'closeEye')                
        if cmds.objExists(openEyeGRP) == False:
            cmds.group(empty = True, name = openEyeGRP, parent = tarGRP)
            self.addTreeAttr(openEyeGRP,'openEye') 
            
            
        if cmds.objExists(bodyGRP) == False:
            cmds.group(empty = True, name = bodyGRP, parent = geometryGRP)
            self.addTreeAttr(bodyGRP,'body')
        if cmds.objExists(bodyAssGRP) == False:
            cmds.group(empty = True, name = bodyAssGRP, parent = bodyGRP)
            self.addTreeAttr(bodyAssGRP,'bodyAss')
        
            
            
        if cmds.objExists(RarmGrp) == False:
            cmds.group(empty = True, name = RarmGrp, parent = bodyGRP)            
            self.addTreeAttr(RarmGrp,'Rarm')
        if cmds.objExists(LarmGrp) == False:
            cmds.group(empty = True, name = LarmGrp, parent = bodyGRP)            
            self.addTreeAttr(LarmGrp,'Larm')
        if cmds.objExists(RhandGrp) == False:
            cmds.group(empty = True, name = RhandGrp, parent = bodyGRP)            
            self.addTreeAttr(RhandGrp,'Rhand')
        if cmds.objExists(LhandGrp) == False:
            cmds.group(empty = True, name = LhandGrp, parent = bodyGRP)            
            self.addTreeAttr(LhandGrp,'Lhand')
        if cmds.objExists(RlegGrp) == False:
            cmds.group(empty = True, name = RlegGrp, parent = bodyGRP)            
            self.addTreeAttr(RlegGrp,'Rleg')            
        if cmds.objExists(LlegGrp) == False:
            cmds.group(empty = True, name = LlegGrp, parent = bodyGRP)            
            self.addTreeAttr(LlegGrp,'Lleg') 
        if cmds.objExists(RshoeGrp) == False:
            cmds.group(empty = True, name = RshoeGrp, parent = bodyGRP)            
            self.addTreeAttr(RshoeGrp,'Rshoe') 
        if cmds.objExists(LshoeGrp) == False:
            cmds.group(empty = True, name = LshoeGrp, parent = bodyGRP)            
            self.addTreeAttr(LshoeGrp,'Lshoe') 
        if cmds.objExists(RfootGrp) == False:
            cmds.group(empty = True, name = RfootGrp, parent = bodyGRP)            
            self.addTreeAttr(RfootGrp,'Rfoot') 
        if cmds.objExists(LfootGrp) == False:
            cmds.group(empty = True, name = LfootGrp, parent = bodyGRP)            
            self.addTreeAttr(LfootGrp,'Lfoot')             
            
        if cmds.objExists(clothGRP) == False:
            cmds.group(empty = True, name = clothGRP, parent = geometryGRP)
            self.addTreeAttr(clothGRP,'cloth')
        if cmds.objExists(deformGRP) == False:
            cmds.group(empty = True, name = deformGRP, parent = modelGRP)
            self.addTreeAttr(deformGRP,'deform')
        if cmds.objExists(solverClothGRP) == False:
            cmds.group(empty = True, name = solverClothGRP, parent = modelGRP)
            self.addTreeAttr(solverClothGRP,'solverCloth')
        if cmds.objExists(ClothfieldGRP) == False:
            cmds.group(empty = True, name = ClothfieldGRP, parent = solverClothGRP)
            self.addTreeAttr(ClothfieldGRP,'Clothfield')
        if cmds.objExists(solvermodelGRP) == False:
            cmds.group(empty = True, name = solvermodelGRP, parent = solverClothGRP)
            self.addTreeAttr(solvermodelGRP,'solvermodel')
        cmds.select(clear = True)
    def hairTree(self):
        FileType = 'c_'
        treeName = cmds.textField(self.textFG, query = True, text = True).strip()
        modelGRP = FileType + treeName + '_model_GRP'
        geometryGRP = FileType + treeName + '_geometry_GRP'                  
        solverHairGRP = FileType + treeName + '_solverHair_GRP'
        hairYetiGRP = FileType + treeName + '_hairYeti_GRP'
        hairCollideGRP = FileType + treeName + '_hairCollide_GRP'
        hairsysGRP = FileType + treeName + '_hairsys_GRP'
        hairxxxGRP = FileType + treeName + '_xxx_nhair_GRP'
        hairsysNodeGRP = FileType + treeName + '_hairsysNode_GRP'
        follicGRP = FileType + treeName + '_follic_GRP'
        pfxhairGRP = FileType + treeName + '_pfxhair_GRP'
        outputcurvesGRP = FileType + treeName + '_outputcurves_GRP'
        HairnodesGRP = FileType + treeName + '_Hairnodes_GRP'
        HairfieldGRP = FileType + treeName + '_Hairfield_GRP'
        growMeshGRP = FileType + treeName + '_growMesh_GRP'

        if cmds.objExists(modelGRP) == False:
            cmds.group(empty = True, name = modelGRP)
            cmds.addAttr(longName = 'treeName', dataType = 'string')
            cmds.addAttr(longName = 'Name',dataType = 'string')
            cmds.addAttr(longName = 'Type',dataType = 'string')
            cmds.setAttr(modelGRP + '.treeName', treeName, type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Name', 'model', type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Type', 'c', type = 'string', lock = True)
        if cmds.objExists(geometryGRP) == False:
            cmds.group(empty = True, name = geometryGRP, parent = modelGRP)
            self.addTreeAttr(geometryGRP,'geometrty')            
            cmds.addAttr(geometryGRP,longName = 'Morh',dataType = 'string')
            cmds.setAttr(geometryGRP + '.Morh', 'h', type = 'string', lock = True)                    
        if cmds.objExists(solverHairGRP) == False:
            cmds.group(empty = True, name = solverHairGRP, parent = geometryGRP)
            self.addTreeAttr(solverHairGRP,'solverHair')
        if cmds.objExists(hairYetiGRP) == False:
            cmds.group(empty = True, name = hairYetiGRP, parent = solverHairGRP)
            self.addTreeAttr(hairYetiGRP,'hairYeti')
        if cmds.objExists(hairCollideGRP) == False:
            cmds.group(empty = True, name = hairCollideGRP, parent = solverHairGRP)
            self.addTreeAttr(hairCollideGRP,'hairCollide')
        if cmds.objExists(hairsysGRP) == False:
            cmds.group(empty = True, name = hairsysGRP, parent = solverHairGRP) 
            self.addTreeAttr(hairsysGRP,'hairsys')       
        if cmds.objExists(hairxxxGRP) == False:
            cmds.group(empty = True, name = hairxxxGRP, parent = hairsysGRP) 
            self.addTreeAttr(hairxxxGRP,'hairxxx')          
        if cmds.objExists(hairsysNodeGRP) == False:
            cmds.group(empty = True, name = hairsysNodeGRP, parent = hairxxxGRP)    
            self.addTreeAttr(hairsysNodeGRP,'hairsysNode')        
        if cmds.objExists(follicGRP) == False:
            cmds.group(empty = True, name = follicGRP, parent = hairxxxGRP)
            self.addTreeAttr(follicGRP,'follic')
        if cmds.objExists(pfxhairGRP) == False:
            cmds.group(empty = True, name = pfxhairGRP, parent = hairxxxGRP)
            self.addTreeAttr(pfxhairGRP,'pfxhair')
        if cmds.objExists(outputcurvesGRP) == False:
            cmds.group(empty = True, name = outputcurvesGRP, parent = hairxxxGRP)
            self.addTreeAttr(outputcurvesGRP,'outputcurves')
        if cmds.objExists(HairnodesGRP) == False:
            cmds.group(empty = True, name = HairnodesGRP, parent = solverHairGRP)
            self.addTreeAttr(HairnodesGRP,'Hairnodes')
        if cmds.objExists(HairfieldGRP) == False:
            cmds.group(empty = True, name = HairfieldGRP, parent = solverHairGRP)
            self.addTreeAttr(HairfieldGRP,'Hairfield')
        if cmds.objExists(growMeshGRP) == False:
            cmds.group(empty = True, name = growMeshGRP, parent = solverHairGRP)  
            self.addTreeAttr(growMeshGRP,'growMesh')              
        cmds.select(clear = True)        
        
        
        
    def propsTree(self):
        FileType = 'p_'
        treeName = cmds.textField(self.textFG, query = True, text = True).strip()
        modelGRP = FileType + treeName + '_model_GRP'
        geometryGRP = FileType + treeName + '_geometry_GRP'
        if cmds.objExists(modelGRP) == False:
            cmds.group(empty = True, name = modelGRP)
            cmds.addAttr(longName = 'treeName', dataType = 'string')
            cmds.addAttr(longName = 'Name',dataType = 'string')
            cmds.addAttr(longName = 'Type',dataType = 'string')
            cmds.setAttr(modelGRP + '.treeName', treeName, type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Name', 'model', type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Type', 'p', type = 'string', lock = True)            
        if cmds.objExists(geometryGRP) == False:
            cmds.group(empty = True, name = geometryGRP, parent = modelGRP)
            cmds.addAttr(geometryGRP,longName = 'Name',dataType = 'string')
            cmds.addAttr(geometryGRP,longName = 'Type',dataType = 'string')
            cmds.setAttr(geometryGRP + '.Name', 'geometry', type = 'string', lock = True)
            cmds.setAttr(geometryGRP + '.Type', 'p', type = 'string', lock = True)
            cmds.addAttr(geometryGRP,longName = "rendering",at = 'bool')
            cmds.setAttr("%s.rendering"%geometryGRP, True)           
        cmds.select(clear = True)
    def sceneTree(self):
        FileType = 's_'
        treeName = cmds.textField(self.textFG, query = True, text = True).strip()
        modelGRP = FileType + treeName + '_model_GRP'
        geometryGRP = FileType + treeName + '_geometry_GRP'
        if cmds.objExists(modelGRP) == False:
            cmds.group(empty = True, name = modelGRP)
            cmds.addAttr(longName = 'treeName', dataType = 'string')
            cmds.addAttr(longName = 'Name',dataType = 'string')
            cmds.addAttr(longName = 'Type',dataType = 'string')
            cmds.setAttr(modelGRP + '.treeName', treeName, type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Name', 'model', type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Type', 's', type = 'string', lock = True)    
        if cmds.objExists(geometryGRP) == False:
            cmds.group(empty = True, name = geometryGRP, parent = modelGRP)
            cmds.addAttr(geometryGRP,longName = 'Name',dataType = 'string')
            cmds.addAttr(geometryGRP,longName = 'Type',dataType = 'string')
            cmds.setAttr(geometryGRP + '.Name', 'geometry', type = 'string', lock = True)
            cmds.setAttr(geometryGRP + '.Type', 's', type = 'string', lock = True)   
            cmds.addAttr(geometryGRP,longName = "rendering",at = 'bool')
            cmds.setAttr("%s.rendering"%geometryGRP, True)      
        cmds.select(clear = True)
    def meshGenTree(self):
        FileType = 'm_'
        treeName = cmds.textField(self.textFG, query = True, text = True).strip()
        modelGRP = FileType + treeName + '_model_GRP'
        geometryGRP = FileType + treeName + '_geometry_GRP'
        if cmds.objExists(modelGRP) == False:
            cmds.group(empty = True, name = modelGRP)
            cmds.addAttr(longName = 'treeName', dataType = 'string')
            cmds.addAttr(longName = 'Name',dataType = 'string')
            cmds.addAttr(longName = 'Type',dataType = 'string')
            cmds.setAttr(modelGRP + '.treeName', treeName, type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Name', 'model', type = 'string', lock = True)
            cmds.setAttr(modelGRP + '.Type', 'm', type = 'string', lock = True)    
        if cmds.objExists(geometryGRP) == False:
            cmds.group(empty = True, name = geometryGRP, parent = modelGRP)
            cmds.addAttr(geometryGRP,longName = 'Name',dataType = 'string')
            cmds.addAttr(geometryGRP,longName = 'Type',dataType = 'string')
            cmds.setAttr(geometryGRP + '.Name', 'geometry', type = 'string', lock = True)
            cmds.setAttr(geometryGRP + '.Type', 'm', type = 'string', lock = True)  
            cmds.addAttr(geometryGRP,longName = "rendering",at = 'bool')
            cmds.setAttr("%s.rendering"%geometryGRP, True)       
        cmds.select(clear = True)
        pass
    def GRPExists(self):
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        #~ if cmds.objExists('*_model_GRP') == True:
            #~ cmds.select('*_model_GRP')
            #~ GRPName = cmds.ls(sl = True)
        if GRPName !=[]:
            treeName = '_'.join(GRPName[0].split('_')[1:GRPName[0].split('_').index('model')])
            if GRPName[0][0:1] == 'c':
                
                cmds.optionMenu(self.typeOM, edit = True, select = 1)      
                self.characterComp()
            if GRPName[0][0:1] == 'p':
                cmds.optionMenu(self.typeOM, edit = True, select = 2)
                self.propComp()    
            if GRPName[0][0:1] == 's':
                cmds.optionMenu(self.typeOM, edit = True, select = 3)
                self.propComp()  
            if cmds.objExists(GRPName[0] + '.treeName') == True:
                self.GRPName = GRPName
                self.getGRPName()
            else:
                cmds.addAttr(GRPName[0], longName = 'Name', dataType = 'string')
                cmds.setAttr(GRPName[0] + '.treeName', treeName[1], type = 'string', lock = True)
                self.GRPName = GRPName
                self.getGRPName()
    def getGRPName(self):
        creatTWindow = self.creatTWindow
        GRPName = self.GRPName
        NameStr = cmds.getAttr(GRPName[0] + '.treeName')
        treeName = '_'.join(GRPName[0].split('_')[1:GRPName[0].split('_').index('model')])
        Type = cmds.getAttr(GRPName[0] + '.Type')
        cmds.select(clear = True)
        if cmds.objExists('c_'+treeName+'_geometry_GRP') and cmds.getAttr('c_'+treeName+'_geometry_GRP.Morh') == 'm':
            cmds.window(creatTWindow, title = u'已有人物组:' + NameStr, edit = True)
            cmds.textField(self.textFG, edit = True, text = NameStr)
            cmds.frameLayout(self.controlFrL, edit = True, collapse = False)  
            cmds.optionMenu(self.typeOM, edit = True, select = 1)  
        if cmds.objExists('c_'+treeName+'_geometry_GRP') and cmds.getAttr('c_'+treeName+'_geometry_GRP.Morh') == 'h':
            cmds.window(creatTWindow, title =  u'已有毛发组:' + NameStr, edit = True)
            cmds.textField(self.textFG, edit = True, text = NameStr)
            cmds.frameLayout(self.controlFrL, edit = True, collapse = False)  
            cmds.optionMenu(self.typeOM, edit = True, select = 1)          
        if Type == 'p':
            cmds.window(creatTWindow, title = u'已有道具组:' + NameStr, edit = True)
            cmds.textField(self.textFG, edit = True, text = NameStr)            
        if Type == 's':
            cmds.window(creatTWindow, title = u'已有场景组:' + NameStr, edit = True)
            cmds.textField(self.textFG, edit = True, text = NameStr)                     
    def multipleGRP(self):
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        #~ if cmds.objExists('*_model_GRP') == True:
            #~ cmds.select('*_model_GRP')
            #~ GRPName = cmds.ls(selection = True)
        if GRPName !=[]:
            GRPNum = len(GRPName)
            GRPList = []
            if GRPNum > 1:
                for i in GRPName:
                    GRPList.append(i)
                holdGrp = cmds.confirmDialog(message = u'请选择一个组保留', button = GRPList)
                cmds.select(GRPName)
                cmds.select(holdGrp, deselect = True)
                deleteList = cmds.ls(selection = True)
                cmds.delete(deleteList)
    def confirmDA(self):
        cmds.confirmDialog(message = u'请创建组', button = ['Yes'], defaultButton = 'Yes')
    def parentGrp(self, buttonName):
        #~ if cmds.objExists('*_model_GRP') == True:
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        if GRPName !=[]:
            groupName = cmds.textField(self.textFG, query = True, text = True)
            objectName = cmds.ls(selection = True)
            self.objectName = objectName
            parentName = ''
            typeOMI = cmds.optionMenu(self.typeOM, query = True, select = True)
            if typeOMI == 1: # or typeOMI == 4:
                parentName = 'c_' + groupName + '_' + buttonName + '_GRP'
                self.parentName = parentName
                if cmds.objExists(parentName) == True:
                    if objectName != []:
                        self.parentGrpB()
                    else:
                        cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes') 
                else :
                    cmds.confirmDialog(message = u'该组不存在，请手动检查组', button = ['Yes'], defaultButton = 'Yes')                                
            if typeOMI == 2:
                parentName = 'p_' + groupName + '_geometry_GRP'
                self.parentName = parentName
                if cmds.objExists(parentName) == True:
                    if objectName != []:
                        self.parentGrpA()
                    else:
                        cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')   
                else:
                    cmds.confirmDialog(message = u'请先创建道具组', button = ['Yes'], defaultButton = 'Yes')   
                                                 
            if typeOMI == 3:
                parentName = 's_' + groupName + '_geometry_GRP'
                self.parentName = parentName
                if cmds.objExists(parentName) == True:
                    if objectName != []:
                        self.parentGrpA()
                    else:
                        cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')
                else:
                    cmds.confirmDialog(message = u'请先创建场景组', button = ['Yes'], defaultButton = 'Yes') 
            if typeOMI == 4:
                parentName = 'm_' + groupName + '_geometry_GRP'
                self.parentName = parentName
                if cmds.objExists(parentName) == True:
                    if objectName != []:
                        self.parentGrpA()
                    else:
                        cmds.confirmDialog(message = u'请选择物体', button = ['Yes'], defaultButton = 'Yes')
                else:
                    cmds.confirmDialog(message = u'请先创建场景组', button = ['Yes'], defaultButton = 'Yes') 

        else:
            self.confirmDA()       
    def parentGrpA(self):
        groupName = cmds.textField(self.textFG, query = True, text = True)
        typeOMI = cmds.optionMenu(self.typeOM, query = True, select = True)
        objectName = self.objectName
        parentName = self.parentName
        if cmds.listRelatives(objectName,c=1,shapes=1) == None:
            cmds.confirmDialog(message=u'请先选择物体')
            return
        self.textnameDialog=''
        self.nameDialog()
        if self.textnameDialog=='':
            return
        if typeOMI == 2:
            newGroupName = 'p_' + groupName + '_' + self.textnameDialog + '_GRP'
            newObjName = 'p_' + groupName + '_' + self.textnameDialog + '_1'
            if cmds.objExists(newGroupName):
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True)[0]
                    if cmds.listRelatives(sel,p=1):
                        if cmds.listRelatives(sel,p=1)[0] != newGroupName:
                            cmds.parent(sel, newGroupName)
                    if  cmds.listRelatives(sel,p=1) == None :
                        cmds.parent(sel, newGroupName)
                    sel = cmds.ls(sl= True)[0]
                    cmds.rename(sel, newObjName) 
                    sel = cmds.ls(sl= True)[0]                         
                    shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                    cmds.rename(shape,self.getShapeName(sel))                   
                    cmds.select(cl=1)
            else :
                cmds.select(cl=1)
                cmds.group(name = newGroupName,em=1,parent = parentName)
                cmds.addAttr(newGroupName,longName = 'Name',dataType = 'string')
                cmds.addAttr(newGroupName,longName = 'Type',dataType = 'string')
                cmds.setAttr(newGroupName + '.Name', self.textnameDialog , type = 'string', lock = True)
                cmds.setAttr(newGroupName + '.Type', 'p', type = 'string', lock = True) 
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True)[0]
                    cmds.parent(sel, newGroupName)
                    sel = cmds.ls(sl= True)[0]
                    cmds.rename(sel, newObjName) 
                    sel = cmds.ls(sl= True)[0]                         
                    shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                    cmds.rename(shape,self.getShapeName(sel))                    
                    cmds.select(cl=1)           
            cmds.optionVar(iv = ['inViewMessageEnable', 1])
            cmds.inViewMessage(amg = u'已入组', pos = 'midCenter', fade = True)
            cmds.select(clear = True)            
        if typeOMI == 3:
            newGroupName = 's_' + groupName + '_' + self.textnameDialog+'_GRP'
            newObjName ='s_' + groupName + '_' + self.textnameDialog +'_1'
            if cmds.objExists(newGroupName):
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True)
                    if cmds.listRelatives(sel,p=1):
                        if cmds.listRelatives(sel,p=1)[0] != newGroupName:
                            cmds.parent(sel, newGroupName)
                    if  cmds.listRelatives(sel,p=1) == None :
                        cmds.parent(sel, newGroupName)
                    cmds.rename(sel, newObjName)   
                    cmds.select(cl=1)
            else :
                cmds.select(cl=1)
                cmds.group(name = newGroupName,em=1,parent = parentName)
                cmds.addAttr(newGroupName,longName = 'Name',dataType = 'string')
                cmds.addAttr(newGroupName,longName = 'Type',dataType = 'string')
                cmds.setAttr(newGroupName + '.Name', self.textnameDialog , type = 'string', lock = True)
                cmds.setAttr(newGroupName + '.Type', 's', type = 'string', lock = True) 
                cmds.select(cl=1)
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True,long=1)
                    cmds.parent(sel, newGroupName)
                    sel = cmds.ls(sl = True,long=1)
                    cmds.rename(sel[0], newObjName) 
                    cmds.select(cl=1)           
            cmds.optionVar(iv = ['inViewMessageEnable', 1])
            cmds.inViewMessage(amg = u'已入组', pos = 'midCenter', fade = True)
            cmds.select(clear = True)      
        if typeOMI == 4:
            newGroupName = 'm_' + groupName + '_' + self.textnameDialog+'_GRP'
            newObjName ='m_' + groupName + '_' + self.textnameDialog +'_1'
            if cmds.objExists(newGroupName):
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True)
                    if cmds.listRelatives(sel,p=1):
                        if cmds.listRelatives(sel,p=1)[0] != newGroupName:
                            cmds.parent(sel, newGroupName)
                    if  cmds.listRelatives(sel,p=1) == None :
                        cmds.parent(sel, newGroupName)
                    cmds.rename(sel, newObjName)   
                    cmds.select(cl=1)
            else :
                cmds.select(cl=1)
                cmds.group(name = newGroupName,em=1,parent = parentName)
                cmds.addAttr(newGroupName,longName = 'Name',dataType = 'string')
                cmds.addAttr(newGroupName,longName = 'Type',dataType = 'string')
                cmds.setAttr(newGroupName + '.Name', self.textnameDialog , type = 'string', lock = True)
                cmds.setAttr(newGroupName + '.Type', 'm', type = 'string', lock = True) 
                cmds.select(cl=1)
                for obj in objectName:
                    cmds.select(obj)
                    sel = cmds.ls(sl = True,long=1)
                    cmds.parent(sel, newGroupName)
                    sel = cmds.ls(sl = True,long=1)
                    cmds.rename(sel[0], newObjName) 
                    cmds.select(cl=1)           
            cmds.optionVar(iv = ['inViewMessageEnable', 1])
            cmds.inViewMessage(amg = u'已入组', pos = 'midCenter', fade = True)
            cmds.select(clear = True)      
    def parentGrpB(self):
        objectName = self.objectName
        if cmds.listRelatives(objectName,c=1,shapes=1) == None:
            cmds.confirmDialog(message=u'请先选择物体')
            return
        parentName = self.parentName
        typeOMI = cmds.optionMenu(self.typeOM, query = True, select = True)
        objectNewName = parentName.strip('_GRP')
        parentList = cmds.listRelatives(parentName, children = True)
        if parentList == None:
            for i in objectName:
                cmds.select(i)
                sel = cmds.ls(sl= True)[0]
                cmds.parent(sel, parentName)
                sel = cmds.ls(sl= True)[0]
                cmds.rename(sel, objectNewName)
                sel = cmds.ls(sl= True)[0]                         
                shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                cmds.rename(shape,self.getShapeName(sel))                
                cmds.optionVar(iv = ['inViewMessageEnable', 1])
                cmds.inViewMessage(amg = u'已入组', pos = 'midCenter', fade = True)
                cmds.select(clear = True)
        else:
            for i in objectName:
                if i in parentList:
                    cmds.optionVar(iv = ['inViewMessageEnable', 1])
                    cmds.inViewMessage(amg = u'已存在', pos = 'midCenter', fade = True)
                    cmds.select(clear = True)
                else:
                    cmds.select(i)
                    sel = cmds.ls(sl= True)[0]
                    if cmds.listRelatives(sel,p=1)!= None:
                        if cmds.listRelatives(sel,p=1)[0]== parentName:
                            pass
                        else :
                            cmds.parent(sel, parentName)
                    else :
                        cmds.parent(sel, parentName)
                    sel = cmds.ls(sl= True)[0]
                    cmds.rename(sel, objectNewName)       
                    sel = cmds.ls(sl= True)[0]                         
                    shape = cmds.listRelatives(sel,shapes=1,f=1)[0]
                    cmds.rename(shape,self.getShapeName(sel))
                    cmds.optionVar(iv = ['inViewMessageEnable', 1])
                    cmds.inViewMessage(amg = u'已入组', pos = 'midCenter', fade = True)
                    cmds.select(clear = True)                    
    def nameDialog(self):
        result = cmds.promptDialog(title='Rename Object',message='Enter Name:',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel')
        if result == 'OK' :
            if cmds.promptDialog(query=True, text=True) !='':
                self.textnameDialog = cmds.promptDialog(query=True, text=True)
                return
            else:
                self.nameDialog()
        else:
            self.textnameDialog = ''
            return
    def judgeWin(self):
        if cmds.optionMenu(self.typeOM,q=1,sl=1) == 1 :
            cmds.deleteUI(self.controlFrL)  
            self.characterComp()
        if cmds.optionMenu(self.typeOM,q=1,sl=1) == 2 :
            cmds.deleteUI(self.controlFrL)
            self.propComp()  
        if cmds.optionMenu(self.typeOM,q=1,sl=1) == 3 :
            cmds.deleteUI(self.controlFrL)
            self.propComp()                
        if cmds.optionMenu(self.typeOM,q=1,sl=1) == 4 :
            cmds.deleteUI(self.controlFrL)
            self.propComp()                
    def addTreeAttr(self,groupName,attrName):
        cmds.addAttr(groupName,longName = 'Name',dataType = 'string')
        cmds.addAttr(groupName,longName = 'Type',dataType = 'string')
        cmds.setAttr(groupName + '.Name', attrName, type = 'string', lock = True)
        cmds.setAttr(groupName + '.Type', 'c', type = 'string', lock = True)        
    def renameTree_1(self):
        treeName = cmds.textField(self.textFG, query = True, text = True)
        NameStr = ''
        TypeStr = ''
        TreeName = ''
        #~ if cmds.objExists('*_model_GRP') == True:
            #~ cmds.select('*_model_GRP')
            #~ GRPName = cmds.ls(sl = True)
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        if GRPName!=[]:
            if cmds.objExists(GRPName[0] + '.treeName') == True:
                NameStr = cmds.getAttr(GRPName[0] + '.treeName')   
                TypeStr = cmds.getAttr(GRPName[0] + '.Type')
                TreeName = cmds.getAttr(GRPName[0] + '.treeName')     
        trans = list(set(cmds.ls(tr=1)) - set([u'front',u'persp',u'side',u'top']))  
        if cmds.optionMenu(self.typeOM,q=1,sl=1) == 1 :
            if cmds.objExists('c_'+TreeName+'_geometry_GRP.Morh') and cmds.getAttr('c_'+TreeName+'_geometry_GRP.Morh') == 'm':
                for i in trans:
                    if i[0:2] == (TypeStr +'_'):
                        newName = TypeStr +'_'+treeName + NameStr.join(i[2:].split(NameStr)[1:])
                        if cmds.objExists(i+'.treeName'):
                            cmds.setAttr(i+'.treeName',l=0)
                            cmds.setAttr(i+'.treeName',treeName,type = 'string')
                            cmds.setAttr(i+'.treeName',l=1)
                        cmds.rename(i,newName)   
            else :
                con = cmds.confirmDialog(message=u'大纲中的大组不是人物组，请问要删除当前组(包括组里的物体)并且新建人物组吗?',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel')
                return con
        else:
            for i in trans:
                if i[0:2] == (TypeStr +'_'):
                    newName = TypeStr +'_'+treeName + NameStr.join(i[2:].split(NameStr)[1:])
                    if cmds.objExists(i+'.treeName'):
                        cmds.setAttr(i+'.treeName',l=0)
                        cmds.setAttr(i+'.treeName',treeName,type = 'string')
                        cmds.setAttr(i+'.treeName',l=1)
                    cmds.rename(i,newName)
    def renameTree_2(self):
        treeName = cmds.textField(self.textFG, query = True, text = True)
        NameStr = ''
        TypeStr = ''
        TreeName = ''
        #~ if cmds.objExists('*_model_GRP') == True:
            #~ cmds.select('*_model_GRP')
            #~ GRPName = cmds.ls(sl = True)
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        if GRPName!=[]:
            if cmds.objExists(GRPName[0] + '.treeName') == True:
                NameStr = cmds.getAttr(GRPName[0] + '.treeName')   
                TypeStr = cmds.getAttr(GRPName[0] + '.Type')
                TreeName = cmds.getAttr(GRPName[0] + '.treeName')     
        trans = list(set(cmds.ls(tr=1)) - set([u'front',u'persp',u'side',u'top']))
        if cmds.objExists('c_'+TreeName+'_geometry_GRP.Morh') and cmds.getAttr('c_'+TreeName+'_geometry_GRP.Morh') == 'h':
            for i in trans:
                if i[0:2] == (TypeStr +'_'):
                    newName = TypeStr +'_'+treeName + NameStr.join(i[2:].split(NameStr)[1:])
                    if cmds.objExists(i+'.treeName'):
                        cmds.setAttr(i+'.treeName',l=0)
                        cmds.setAttr(i+'.treeName',treeName,type = 'string')
                        cmds.setAttr(i+'.treeName',l=1)
                    cmds.rename(i,newName)   
        else :
            con = cmds.confirmDialog(message=u'大纲中的大组不是头发组，请问要删除当前组(包括组里的物体)并新建头发组吗?',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel')
            return con                    
    def setDisplay(self):
         #~ if cmds.objExists('*_model_GRP') == True :
             #~ groups = cmds.ls('*_model_GRP')[0]
        GRPName = [x for x in cmds.ls(type='transform') if ('_model_GRP' in x) ]
        if GRPName!=[]:
            groups = GRPName[0]
            attr = 1-cmds.getAttr(groups+'.v')
            cmds.setAttr((groups + '.v'),attr)
    # def getShapeName(self,transName):
    #     #     if transName[-1] in string.digits:
    #     #         return transName[:-1] + 'Shape' + transName[-1]
    #     #     else :
    #     #         return transName + 'Shape'
#修复shape命名错误的bug
    def getShapeName(self, transName):
        if transName.replace("_", "").isalnum() is True:#判断去掉_以后是否为纯字母，目的是判断有数字
            temp_num = []
            stop = -1
            for i in range(-1, -10, -1):#判断后10位，一直到出现字母
                if transName[i].isdigit():
                    temp_num.append(transName[i])#如果是数字就一直加下去，直到遇见字母或者是到10位数以后
                else:
                    stop = i
                    break
            temp_num.reverse()#序列倒序
            return transName[:stop] + 'Shape' + "{}".format("".join(temp_num))#重命名
        else:
            return transName + 'Shape'#如果为纯字母的话就直接改名字

    def colliderApp(self):
        colliderGroup.ColliderGroup().showUi()
    def setNameSpace(self):
        cmds.namespace(setNamespace = ':')
if __name__ == '__main__':
    ModelArrange = Ui()
    ModelArrange.showUi()