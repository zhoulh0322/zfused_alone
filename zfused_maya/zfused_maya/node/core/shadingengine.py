# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" 材质引擎操作集合 """
import os
from Qt import QtGui
import maya.cmds as cmds

import zfused_maya.core.color as color
import zfused_maya.core.image as image

def nodes():
    """ get all shading engines

    :rtype: list
    """
    _default_shading_engine = ["initialShadingGroup", "initialParticleSE"]
    _all_shading_engines = cmds.ls(type="shadingEngine")
    _all_shading_engines = list(set(_all_shading_engines)
                                - set(_default_shading_engine))
    return _all_shading_engines

def switch_color_shader(engines):
    for _engine in engines:
        if cmds.nodeType(_engine) == "shadingEngine":
            # set original material
            _ori_material = cmds.listConnections("{}.surfaceShader".format(_engine), s=True)[0]
            if not cmds.objExists("{}.surfacematerial".format(_engine)):
                cmds.addAttr(_engine, ln = "surfacematerial", dt="string")
            if not _ori_material.startswith("zfused_shading_color_"):
                cmds.setAttr("{}.surfacematerial".format(_engine), _ori_material, type="string")

    for _engine in engines:
        # get engine color
        _shader = cmds.shadingNode("lambert", name = "zfused_shading_color_0000",asShader = True)
        _color = get_node_shading_color(_engine)
        if _color:
            _qtcolor = QtGui.QColor(_color)
            r,g,b,_ = _qtcolor.getRgb()
            cmds.setAttr("{}.color".format(_shader), r/255.0, g/255.0, b/255.0 ,type = "double3")
            # # connect
            # cmds.connectAttr("{}.outColor".format(_shader), "{}.surfaceShader".format(_engine), f = True)
        _transparency = get_node_shading_transparency(_engine)
        if _transparency:
            _qtcolor = QtGui.QColor(_transparency)
            r,g,b,_ = _qtcolor.getRgb()
            cmds.setAttr("{}.transparency".format(_shader), r/255.0, g/255.0, b/255.0 ,type = "double3")
        _ambientColor = get_node_shading_ambientColor(_engine)
        if _ambientColor:
            _qtcolor = QtGui.QColor(_ambientColor)
            r,g,b,_ = _qtcolor.getRgb()
            cmds.setAttr("{}.ambientColor".format(_shader), r/255.0, g/255.0, b/255.0 ,type = "double3")
        # connect
        cmds.connectAttr("{}.outColor".format(_shader), "{}.surfaceShader".format(_engine), f = True)

def switch_orignail_shader(engines):
    for _engine in engines:
        # get orignail engine
        if not cmds.objExists("{}.surfacematerial".format(_engine)):
            continue
        _ori_shader = cmds.getAttr("{}.surfacematerial".format(_engine))
        _node_type = cmds.nodeType(_ori_shader)
        try:
            if _node_type.startswith("ai"):
                cmds.connectAttr("{}.out".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
            elif _node_type.startswith("Redshift"):
                cmds.connectAttr("{}.outColor".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
            else:
                cmds.connectAttr("{}.outColor".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
        except:
            pass
        # connect
        # cmds.connectAttr("{}.outColor".format(_ori_shader), "{}.surfaceShader".format(_engine), f = True)
    # clear color shader
    _shaders = cmds.ls("zfused_shading_color_*")
    if _shaders:
        cmds.delete(_shaders) 


def get_shading_engines():
    """ get all shading engine

    :rtype: list
    """
    _default_shading_engine = ["initialShadingGroup", "initialParticleSE"]
    _all_shading_engines = cmds.ls(type="shadingEngine")
    _all_shading_engines = list(set(_all_shading_engines) - set(_default_shading_engine))
    return _all_shading_engines


def set_node_shading_color(node, shading_color):
    """ set shading node color attr

    :rtype: bool
    """
    #print("set node color")
    if not cmds.objExists("{}.shadingcolor".format(node)):
        cmds.addAttr(node, ln="shadingcolor", dt="string")
    cmds.setAttr("{}.shadingcolor".format(node), shading_color, type="string")
    if cmds.nodeType(node) == "shadingEngine":
        # set original material
        _ori_material = cmds.listConnections("{}.surfaceShader".format(node), s=True)[0]
        if not cmds.objExists("{}.surfacematerial".format(node)):
            cmds.addAttr(node, ln = "surfacematerial", dt="string")
        if not _ori_material.startswith("zfused_shading_color_"):
            cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
            _mat = cmds.getAttr("{}.surfacematerial".format(node))
            #print(_mat, _ori_material)
            if _ori_material != _mat:
                cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
    return True

def get_node_shading_color(node):
    """ get shading node color attr

    :rtype: str
    """
    if not cmds.objExists("{}.shadingcolor".format(node)):
        return None
    _color = cmds.getAttr("{}.shadingcolor".format(node))
    return _color

def get_connect_color(node):
    """ get connect file color or picture main color
    :rtype:: str
    """
    # get shader node
    _shader_list = cmds.listConnections("{}.surfaceShader".format(node))
    if not _shader_list:
        return None
    _shader = _shader_list[0]
    print(_shader)
    # get shader color or file node
    _node_type = cmds.nodeType(_shader)
    try:
        if _node_type.startswith("ai"):
            _connect = cmds.listConnections("{}.baseColor".format(_shader), type = "file")
        elif _node_type.startswith("Redshift"):
            # modify------------------------------
            try:
                _connect = cmds.listConnections("{}.diffuse_color".format(_shader), type = "file")
            except:
                _connect = cmds.listConnections(_shader, type = "file")
            # modify------------------------------
        elif _node_type == "standardSurface":
            _connect = cmds.listConnections("{}.baseColor".format(_shader), type = "file")
        else:
            _connect = cmds.listConnections("{}.color".format(_shader), type = "file")
    except:
        _connect = None
    print(_connect)
    if not _connect:
        # get color
        _color = None

        if cmds.objExists("{}.color".format(_shader)):
            _color = cmds.getAttr("{}.color".format(_shader))
        if cmds.objExists("{}.baseColor".format(_shader)):
            _color = cmds.getAttr("{}.baseColor".format(_shader))
        if cmds.objExists("{}.diffuse_color".format(_shader)):
            _color = cmds.getAttr("{}.diffuse_color".format(_shader))

        print(_color)
        if _color:

            _c = list(_color[0])

            _r = max(1, int(_c[0]*255))
            _g = max(1, int(_c[1]*255))
            _b = max(1, int(_c[2]*255))

            print(_r,_g,_b)
            _color = color.convert((_r, _g, _b))
            print(_color)
        return _color

        # try:
        #     _color = cmds.getAttr("{}.color".format(_shader))
        #     if _color:
        #         _c = _color[0]
        #         _r = int(_c[0]*255)
        #         _g = int(_c[1]*255)
        #         _b = int(_c[2]*255)
        #         _color = color.convert((_r, _g, _b))
        #         return _color
        #     else:
        #         return None
        # except:
        #     try:
        #         _color = cmds.getAttr("{}.diffuse_color".format(_shader))
        #         if _color:
        #             _c = _color[0]
        #             _r = int(_c[0]*255)
        #             _g = int(_c[1]*255)
        #             _b = int(_c[2]*255)
        #             _color = color.convert((_r, _g, _b))
        #             return _color
        #         else:
        #             return None
        #     except:
        #         return None

    _file_node = _connect[0]
    # get file main color
    _file = cmds.getAttr("{}.fileTextureName".format(_file_node))
    if not os.path.isfile(_file):
        return None
    _color = image.get_dominant_color(_file)
    #print(_color,node)
    return color.convert(_color)


def set_node_shading_transparency(node, shading_transparency):
    """ set shading node color attr

    :rtype: bool
    """
    #print("set node transparency")
    if not cmds.objExists("{}.shadingtransparency".format(node)):
        cmds.addAttr(node, ln="shadingtransparency", dt="string")
    cmds.setAttr("{}.shadingtransparency".format(node), shading_transparency, type="string")
    if cmds.nodeType(node) == "shadingEngine":
        # set original material
        _ori_material = cmds.listConnections("{}.surfaceShader".format(node), s=True)[0]
        if not cmds.objExists("{}.surfacematerial".format(node)):
            cmds.addAttr(node, ln = "surfacematerial", dt="string")
        if not _ori_material.startswith("zfused_shading_color_"):
            cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
            _mat = cmds.getAttr("{}.surfacematerial".format(node))
            #print(_mat, _ori_material)
            if _ori_material != _mat:
                cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
    return True

def get_node_shading_transparency(node):
    """ get shading node color attr

    :rtype: str
    """
    if not cmds.objExists("{}.shadingtransparency".format(node)):
        return None
    _color = cmds.getAttr("{}.shadingtransparency".format(node))
    return _color

def get_connect_transparency(node):
    """ get connect transparency or picture main transparency

    :rtype:: str
    """
    # get shader node
    _shader_list = cmds.listConnections("{}.surfaceShader".format(node))
    if not _shader_list:
        return None
    _shader = _shader_list[0]
    try:
        _transparency = cmds.getAttr("{}.transparency".format(_shader))
        if _transparency:
            _c = _transparency[0]
            _r = int(_c[0]*255)
            _g = int(_c[1]*255)
            _b = int(_c[2]*255)
            _transparency = color.convert((_r, _g, _b))
            return _transparency
        else:
            return None
    except:
        return None


def set_node_shading_ambientColor(node, shading_ambientColor):
    """ set shading node color attr

    :rtype: bool
    """
    if not cmds.objExists("{}.shadingambientColor".format(node)):
        cmds.addAttr(node, ln="shadingambientColor", dt="string")
    cmds.setAttr("{}.shadingambientColor".format(node), shading_ambientColor, type="string")
    if cmds.nodeType(node) == "shadingEngine":
        # set original material
        _ori_material = cmds.listConnections("{}.surfaceShader".format(node), s=True)[0]
        if not cmds.objExists("{}.surfacematerial".format(node)):
            cmds.addAttr(node, ln = "surfacematerial", dt="string")
        if not _ori_material.startswith("zfused_shading_color_"):
            cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
            _mat = cmds.getAttr("{}.surfacematerial".format(node))
            if _ori_material != _mat:
                cmds.setAttr("{}.surfacematerial".format(node), _ori_material, type="string")
    return True

def get_node_shading_ambientColor(node):
    """ get shading node color attr

    :rtype: str
    """
    if not cmds.objExists("{}.shadingambientColor".format(node)):
        return None
    _color = cmds.getAttr("{}.shadingambientColor".format(node))
    return _color

def get_connect_ambientColor(node):
    """ get connect ambientColor or picture main ambientColor

    :rtype:: str
    """
    # get shader node
    _shader_list = cmds.listConnections("{}.surfaceShader".format(node))
    if not _shader_list:
        return None
    _shader = _shader_list[0]
    # # get shader color or file node
    # _node_type = cmds.nodeType(_shader)
    # try:
    #     if _node_type.startswith("ai"):
    #         _connect = cmds.listConnections("{}.baseColor".format(_shader), type = "file")
    #     elif _node_type.startswith("Redshift"):
    #         _connect = cmds.listConnections("{}.diffuse_color".format(_shader), type = "file")
    #     else:
    #         _connect = cmds.listConnections("{}.color".format(_shader), type = "file")
    # except:
    #     _connect = None
    # ##print(_connect)
    # if not _connect:
    #     # get color
    #     try:
    #         _color = cmds.getAttr("{}.color".format(_shader))
    #         ##print(_color)
    #         if _color:
    #             _c = _color[0]
    #             _r = int(_c[0]*255)
    #             _g = int(_c[1]*255)
    #             _b = int(_c[2]*255)
    #             ##print(_r,_g,_b)
    #             _color = color.convert((_r, _g, _b))
    #             return _color
    #         else:
    #             return None
    #     except:
    #         return None
    # _file_node = _connect[0]
    # # get file main color
    # _file = cmds.getAttr("{}.fileTextureName".format(_file_node))
    # if not os.path.isfile(_file):
    #     return None
    # _color = image.get_dominant_color(_file)
    # return color.convert(_color)
    try:
        _ambientColor = cmds.getAttr("{}.ambientColor".format(_shader))
        if _ambientColor:
            _c = _ambientColor[0]
            _r = int(_c[0]*255)
            _g = int(_c[1]*255)
            _b = int(_c[2]*255)
            _ambientColor = color.convert((_r, _g, _b))
            return _ambientColor
        else:
            return None
    except:
        return None