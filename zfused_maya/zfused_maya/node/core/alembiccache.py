# -*- coding: utf-8 -*-
# --author-- lanhua.zhou

""" alembic缓存文件操作集合 """

import os
import shutil

import maya.cmds as cmds
import  maya.mel as mel
from zcore import filefunc
import xgenm as xg


def publish_file(files, src, dst):
    """ upload files 
    """
    _files = files
    for _file in _files:
        #  alembic cache file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _backup_file = os.path.join(dst, _extend_file)
        #  upload alembic cache file
        _result = filefunc.publish_file(_file, _backup_file)

def local_file(files, src, dst):
    """ local download files 
    """
    _files = files
    for _file in _files:
        #  backup texture file
        _extend_file = _file.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _local_file = os.path.join(dst, _extend_file)
        #  downlocal texture file
        #_result = filefunc.publish_file(_texture_file, _backup_texture_file)
        _local_dir = os.path.dirname(_local_file)
        if not os.path.isdir(_local_dir):
            os.makedirs(_local_dir)
        _result = shutil.copy(_file, _local_file)

def change_node_path(nodes, src, dst):
    """ change file nodes path
    """
    _file_nodes = nodes
    for _file_node in _file_nodes:
        _ori_file_texture_path = cmds.getAttr("{}.abc_File".format(_file_node))
        _file_texture_path = _ori_file_texture_path
        _extend_file = _file_texture_path.split(src)[-1]
        if _extend_file.startswith("/"):
            _extend_file = _extend_file[1::]
        _new_file_text_path = "%s/%s"%(dst, _extend_file)
        while True:
            cmds.setAttr("{}.abc_File".format(_file_node), _new_file_text_path, type = 'string')
            if cmds.getAttr("{}.abc_File".format(_file_node)) == _new_file_text_path:
                break

def nodes():
    """ 获取alembic cache节点
    :rtype: list
    """
    _file_nodes = cmds.ls(type = "AlembicNode")
    _result_nodes = []
    for _file_node in _file_nodes:
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.abc_File".format(_file_node), l = True)
        if _is_reference and _is_lock:
            continue
        _result_nodes.append(_file_node)
    return _result_nodes

def files():
    """get alembic cache file
    
    :rtype: list
    """
    _all_files = cmds.file(query=1, list=1, withoutCopyNumber=1)
    _all_files_dict = {}
    for _file in _all_files:
        _file_dir_name = os.path.dirname(_file)
        _, _file_suffix = os.path.splitext(_file)
        _all_files_dict[_file] = [_file_dir_name, _file_suffix]
    _file_nodes = cmds.ls(type = "AlembicNode")
    _alembic_files = []
    for _file_node in _file_nodes:
        _is_reference = cmds.referenceQuery(_file_node, isNodeReferenced = True)
        _is_lock = cmds.getAttr("{}.abc_File".format(_file_node), l = True)
        if _is_reference and _is_lock:
            continue
        _file_name = cmds.getAttr("{}.abc_File".format(_file_node))
        _node_dir_name = os.path.dirname(_file_name)
        _, _node_suffix = os.path.splitext(_file_name)
        
        for _file in _all_files:
            _file_dir_name,_file_suffix = _all_files_dict[_file]
            if _node_dir_name == _file_dir_name and _node_suffix == _file_suffix:
                _alembic_files.append(_file)
    return _alembic_files


def paths(alembic_files):
    """ 获取文件路径交集

    :rtype: list
    """
    #get texture sets
    def _get_set(path):
        # 获取文件路径集合
        _list = []
        def _get_path(_path, _list):
            _path_new = os.path.dirname(_path)
            if _path_new != _path:
                _list.append(_path_new)
                _get_path(_path_new, _list)
        _get_path(path, _list)
        return _list

    def _get_file_set_list(_files):
        _files_set_dict = {}
        _set_list = []
        for _f in _files:
            _set = set(_get_set(_f))
            _set_list.append(_set)
        return _set_list

    def _set(set_list,value):
        _frist = set_list[0]
        value.append(_frist)
        _left_list = []
        for i in set_list:
            _com = _frist & i
            if not _com:
                _left_list.append(i)
                continue
            value[len(value)-1] = _com
        if _left_list:
            _set(_left_list, value)

    _set_list = _get_file_set_list(alembic_files)
    if not _set_list:
        return []
    _value = []
    _set(_set_list, _value)  

    return _value

def create_frame_cache(_path,startTime,endTime,grpname,*args,**kwargs):
    '''生成创建缓存命令
    '''
    _dir = os.path.dirname(_path)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)

    if isinstance(grpname,list):
        roots = ''.join(["-root %s "%i for i in grpname])
    else:
        roots = "-root %s "%grpname
    # 导出附加参数
    if args:
        exOptions = ''.join([" -%s"%j for j in args])
    else:
        exOptions = ''
    if kwargs:
        other_attr = ''
        for key,value in kwargs.items():
            other_attr = other_attr + ' -{} {}'.format(key,value)
    else:
        other_attr = ''

    joborder = "-frameRange %s %s %s %s -dataFormat hdf %s -file %s"%(startTime,endTime,other_attr,exOptions,roots,_path)
    return joborder

def import_cache(asset,namespace,node,path,texfile = None):
    '''导入缓存
    '''

    def connect_usedattr(src,dst):
        """connect transform attr
        """
        abc_trans = list(set(cmds.listRelatives(src,ad = 1,type = "transform")) | set([src]))
        tex_trans = list(set(cmds.listRelatives(dst,ad = 1,type = "transform")) | set([dst]))
        for _s,_d in zip(sorted(abc_trans),sorted(tex_trans)):
            # set visibility value
            if cmds.objExists("{}.v".format(_s)) and not cmds.getAttr("{}.v".format(_s)):
                cmds.setAttr("{}.v".format(_d),0)
            # set connected attr
            _usedattr = cmds.listConnections(_s,p = 1,c = 1,d = 0)
            if _usedattr:
                for _i in _usedattr[0::2]:
                    _attrname = _i.split(_s)[-1]
                    cmds.connectAttr(_i,"{}{}".format(_d,_attrname))

    def blend_shape(src, dst):
        _src_nums = len(cmds.listRelatives(src, c = True, type = "mesh", ad = True)) 
        if _src_nums > 999:
            _src_child = cmds.listRelatives(src, c = True, type = "transform")
            _dst_child = cmds.listRelatives(dst, c = True, type = "transform")
            for _src, _dst in zip(_src_child, _dst_child):
                blend_shape(_src, _dst)
        else:
            if _src_nums:
                _bsnode = cmds.blendShape(src,dst,w = (0,1.0))
                cmds.setAttr("{}.origin".format(_bsnode[-1]),0)

    _grp_name = "abc_hidegrp"
    # create abc_grp
    if not cmds.objExists(_grp_name):
        _grp = cmds.createNode("transform",n = _grp_name)
        # cmds.setAttr("{}.hiddenInOutliner".format(_grp),1)
        cmds.setAttr("{}.v".format(_grp),0)
    else:
        _grp = _grp_name

    if asset:
        if not cmds.objExists(texfile):
            raise
        # load alembic file
        _newns = "abc_{}".format(namespace)
        # _newns = get_ns(namespace)
        cmds.file(path,i = 1,iv = 1,ra = 1,mergeNamespacesOnClash = 0,ns = _newns,pr = 1,ifr = 1,itr = "override",type = "Alembic")
        _abcnode = "{}:{}".format(_newns,node)
        cmds.parent(_abcnode,_grp)
        cmds.setAttr("{}.t".format(_abcnode),lock = 1)
        cmds.setAttr("{}.r".format(_abcnode),lock = 1)
        cmds.setAttr("{}.s".format(_abcnode),lock = 1)
        # _bsnode = cmds.blendShape(_abcnode,texfile,w = (0,1.0))
        # # cmds.setAttr("{}.{}".format(_bsnode[-1],node),1)
        # cmds.setAttr("{}.origin".format(_bsnode[-1]),0)
        blend_shape(_abcnode,texfile)
        connect_usedattr(_abcnode,texfile)
    else:
        cmds.file(path,i = 1,iv = 1,ra = 1,mergeNamespacesOnClash = 1,ns = ":",pr = 1,ifr = 1,itr = "override",type = "Alembic")
        cmds.setAttr("{}.t".format(namespace),lock = 1)
        cmds.setAttr("{}.r".format(namespace),lock = 1)
        cmds.setAttr("{}.s".format(namespace),lock = 1)
    return True

def remove_cache(*args):
    '''移除缓存的bs连接
        传入要移除的模型名(传入大组名或任意含有空间名的模型)
        没有传入值移除全部缓存
        附：blendShape常用查询命令
            t #获取所有变形模型
            g #获取所有被变形模型
            dt #获取所有变形器节点和groupid
            w #查询权重属性
            en #查询封套属性（envelope属性，一般不改）
    '''
    def get_removeinfo(nodes,*args):
        list1,list2,list3 = [],[],[]
        for _node in nodes:
            _deformednodes = cmds.blendShape(_node,q = 1,g = 1)
            _trans = cmds.listRelatives(_deformednodes,p = 1,type = "transform")
            _ns = list(set([cmds.referenceQuery(i,ns = 1) for i in _trans]))[0]
            if args and _ns not in args:
                continue
            orishape = set(cmds.listRelatives(_trans,s = 1))-set(cmds.listRelatives(_trans,s = 1,ni = 1))
            list1.extend(orishape)
            list2.extend(_deformednodes)
            list2.extend(cmds.blendShape(_node,q = 1,dt = 1))
            list2.append(_node)
            _target = cmds.blendShape(_node,q = 1,t = 1)
            if _target:
                _grp = get_cache_grp(_target)
                list2.append(_grp)
                _remove_ns = get_namespace(_grp)
                if _remove_ns:
                    list3.append(_remove_ns)
        return list(set(list1)),list(set(list2)),list(set(list3))

    def get_cache_grp(node):
        while True:
            if "abc_hidegrp" in cmds.listRelatives(node,p = 1):
                return node
            else:
                node = cmds.listRelatives(node,p = 1)[0]

    def get_namespace(node):
        _ns = node[:-len(node.split(":")[-1])-1]
        if cmds.namespace(ex = _ns):
            return _ns
        return None

    bsnodes = cmds.ls(type = "blendShape")
    if not bsnodes:
        if cmds.objExists("abc_hidegrp"):
            _allabc = cmds.listRelatives("abc_hidegrp",c = 1)
            if _allabc:
                cmds.delete(_allabc)
        return
    bsnodes = cmds.ls(type = "blendShape")
    if bsnodes:
        bsnodes = [i for i in bsnodes if not cmds.referenceQuery(i,inr = 1)]
        _filters = []
        if args:
            _filters = [cmds.referenceQuery(i,ns = 1) for i in args]
        _orifiles,_removefiles,_namespacefiles = get_removeinfo(bsnodes,*_filters)
        if _removefiles:
            cmds.delete(_removefiles)
        if _orifiles:
            for _orifile in _orifiles:
                cmds.setAttr("{}.intermediateObject".format(_orifile),0)
        if _namespacefiles:
            for _namespacefile in _namespacefiles:
                cmds.namespace(rm = _namespacefile,mnr = 1)
    if not args:
        if cmds.objExists("abc_hidegrp"):
            _allabc = cmds.listRelatives("abc_hidegrp",c = 1)
            if _allabc:
                cmds.delete(_allabc)


class AlembicCache(object):
    '''abc操作类，目前只用于切换abc缓存
    '''
    @classmethod
    def get_bsnode(cls,*args):
        '''获取选择模型的bs节点，不选返回全部非参考的bs节点
        '''
        def get_namespace(bsnode):
            '''获取bs节点关联的材质文件的空间名
            '''
            _deformednodes = cmds.blendShape(bsnode,q = 1,g = 1)
            _trans = cmds.listRelatives(_deformednodes,p = 1,type = "transform")
            _ns = set([cmds.referenceQuery(i,ns = 1) for i in _trans])
            return list(_ns)
        templist = set()
        bsnodes = set(cmds.ls(type = "blendShape"))-set(cmds.ls(type = "blendShape",ro = 1))
        if args:
            _filters = [cmds.referenceQuery(i,ns = 1) for i in args]
            for bsnode in bsnodes:
                _ns = get_namespace(bsnode)
                if _ns[0] not in _filters:
                    templist.add(bsnode)
        return list(set(bsnodes)-templist)

    @classmethod
    def get_connect_info(cls,bsnode,_dict = {}):
        '''获取bs节点上的模型连入信息
        '''
        # _dict = {}
        targets = cmds.blendShape(bsnode,q = 1,t = 1)
        for target in targets:
            targetattr = "{}.worldMesh".format(target)
            _dict[targetattr] = cmds.listConnections(targetattr,p = 1)[0]
        return _dict

    @classmethod
    def get_blend_input(cls, bsnode):
        _input_dict = {}
        targets = cmds.blendShape(bsnode,q = 1,t = 1)
        for target in targets:
            targetattr = "{}.worldMesh".format(target)
            _input_dict[targetattr] = cmds.listConnections(targetattr,p = 1)[0]
        return _input_dict

    @classmethod
    def get_blend_output(cls, bsnode):
        _output_dict = {}
        targets = cmds.blendShape(bsnode,q = 1,g = 1)
        for target in targets:
            targetattr = "{}.inMesh".format(target)
            _in = cmds.listConnections(targetattr,p = 1)[0]
            _output_dict[_in] = targetattr
        return _output_dict

    @classmethod
    def get_texfile_grp(cls,bsnode):
        '''获取bs节点传入的模型大组(材质文件)
        '''
        #print(bsnode)
        _deformed = cmds.blendShape(bsnode,q = 1,g = 1)
        if not _deformed:
            return []
        _target = cmds.listRelatives(_deformed,p = 1,type = "transform")[0]
        while True:
            # if "abc_hidegrp" in cmds.listRelatives(_target,p = 1):
            if cmds.objExists("{}.rendering".format(_target)):
                return _target
            else:
                _target = cmds.listRelatives(_target,p = 1)[0]

    @classmethod
    def get_alembic_grp(cls,bsnode):
        '''获取传入bs节点的模型大组
        '''
        _target = cmds.blendShape(bsnode,q = 1,t = 1)
        if not _target:
            return []
        while True:
            if "abc_hidegrp" in cmds.listRelatives(_target,p = 1):
                return _target
            else:
                _target = cmds.listRelatives(_target,p = 1)[0]

    @classmethod
    def get_alembic_namespace(cls,transform):
        '''获取模型的空间名,最好传入大组名，防止重名
        '''
        _ns = transform.split("|")[-1][:-len(transform.split(":")[-1])-1]
        if cmds.namespace(ex = _ns):
            return _ns
        return None

    @classmethod
    def import_alembic(cls,asset,namespace,node,path):
        '''导入缓存
        '''
        _newns = "abc_{}".format(namespace)
        # _newns = get_ns(namespace)
        cmds.file(path,i = 1,iv = 1,ra = 1,mergeNamespacesOnClash = 0,ns = _newns,pr = 1,ifr = 1,itr = "override",type = "Alembic")
        _abcnode = "{}:{}".format(_newns,node)
        cmds.parent(_abcnode,"abc_hidegrp")
        cmds.setAttr("{}.t".format(_abcnode),lock = 1)
        cmds.setAttr("{}.r".format(_abcnode),lock = 1)
        cmds.setAttr("{}.s".format(_abcnode),lock = 1)
        return _newns,_abcnode

    @classmethod
    def connect_attr(cls,src,dst):
        """连接abc上有变化的属性
                src为abc大组
                dst为材质大组
        """
        abc_trans = list(set(cmds.listRelatives(src,ad = 1,type = "transform")) | set([src]))
        tex_trans = list(set(cmds.listRelatives(dst,ad = 1,type = "transform")) | set([dst]))
        for _s,_d in zip(sorted(abc_trans),sorted(tex_trans)):
            # set visibility value
            if cmds.objExists("{}.v".format(_s)) and not cmds.getAttr("{}.v".format(_s)):
                cmds.setAttr("{}.v".format(_d),0)
            # set connected attr
            _usedattr = cmds.listConnections(_s,p = 1,c = 1,d = 0)
            if _usedattr:
                for _i in _usedattr[0::2]:
                    _attrname = _i.split(_s)[-1]
                    cmds.connectAttr(_i,"{}{}".format(_d,_attrname))

    @classmethod
    def set_namespace(cls,nameSpace):
        # 自动生成空间名序号,暂不使用
        index = 0
        _namespaces = list(set(cmds.namespaceInfo(r = 1, lon = 1)) - set(["shared","UI"]))
        while True:
            if nameSpace in _namespaces:
                if nameSpace[-1].isdigit():
                    _num = re.findall("\d+",nameSpace)[-1]
                    nameSpace = "{}{}".format(nameSpace[:-len(_num)],int(_num)+index)
                else:
                    nameSpace = "{}{}".format(nameSpace,index)
                index += 1
            else:
                return nameSpace

    @classmethod
    def switch(cls,bsnodes,*args):
        '''切换缓存
            bsnodes传入类型为list
        '''
        _input_connect = {}
        _output_connect = {}
        _info = {}
        asset,namespace,node,path = args
        _texgrp = cls.get_texfile_grp(bsnodes[0])
        _abcgrp = cls.get_alembic_grp(bsnodes[0])
        for bsnode in bsnodes:
            # cls.get_connect_info(bsnode,_info)
            _input_connect = cls.get_blend_input(bsnode)
            _output_connect = cls.get_blend_output(bsnode)
        if _abcgrp:
            _ns = cls.get_alembic_namespace(_abcgrp)
            cmds.delete(_abcgrp)
            if _ns:
                cmds.namespace(rm = _ns,mnr = 1)
        cls.import_alembic(asset,namespace,node,path)
        cls.connect_attr(_abcgrp,_texgrp)

        _dis_connect = {}
        for k,v in _input_connect.items():
            cmds.connectAttr(k,v)
            try:
                _k_p = k.split(".worldMesh")[0]
                _k = "{}_rendering.outMesh".format(_k_p)
                _v = v.split(".inputTargetGroup")[0].replace("inputTarget", "input") + ".inputGeometry"
                #print(_k,_v)
                cmds.connectAttr(k,_v)
                _dis_connect[k] = _v
            except:
                pass
        if _dis_connect:
            for k,v in _dis_connect.items():
                cmds.disconnectAttr(k,v)


def create_xgen_frame_cache(_path,startTime,endTime,_pallette,*args):
    '''生成创建缓存命令
    '''
    # _dir = os.path.dirname(_path)
    # if not os.path.isdir(_dir):
    #     os.makedirs(_dir)
    # if isinstance(grpname,list):
    #     roots = ''.join(["-root %s "%i for i in grpname])
    # else:
    #     roots = "-root %s "%grpname
    # # # 导出附加参数
    # # if args:
    # #     exOptions = ''.join([" -%s"%j for j in args])
    # # else:
    # #     exOptions = ''
    # # if kwargs:
    # #     other_attr = ''
    # #     for key,value in kwargs.items():
    # #         other_attr = other_attr + ' -{} {}'.format(key,value)
    # # else:
    # #     other_attr = ''
    # #
    # # joborder = "-frameRange %s %s %s %s -dataFormat hdf %s -file %s"%(startTime,endTime,other_attr,exOptions,roots,_path)


    _dir = os.path.dirname(_path)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)

    cmdAlembicBase = ''
    cmdAlembicBase = cmdAlembicBase + '-frameRange ' + str(startTime) + ' ' + str(endTime)
    cmdAlembicBase = cmdAlembicBase + ' -uvWrite -attrPrefix xgen -worldSpace'
    palette = _pallette
    #for p in range(len(palette)):
    descShapes = cmds.listRelatives(palette, type="xgmDescription", ad=True)
    cmdAlembic = cmdAlembicBase
    for d in range(len(descShapes)):
        descriptions = cmds.listRelatives(descShapes[d], parent=True)
        if len(descriptions):
            patches = xg.descriptionPatches(descriptions[0])
            for patch in patches:
                cmd = 'xgmPatchInfo -p "' + patch + '" -g'
                geom = mel.eval(cmd)
                geomFullName = cmds.ls(geom, l=True)
                cmdAlembic += " -root " + geomFullName[0]
    cmdAlembic = cmdAlembic + ' -stripNamespaces -file \'' + _path + '\'";'
    joborder = cmdAlembic
    return joborder




if __name__ == '__main__':
    asset = "backkomuni"
    namespace = "backkom"
    node = "c_backkomuni_geometry_GRP"
    path = "X:/BKM2/shot/seq006/shot001/animation/maya2017/cache/alembiccache/0005/backkom.abc"
    bsnode = "blendshape1"
    AlembicCache.switch(bsnode,asset,namespace,node,path)