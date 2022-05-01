# coding:utf-8
# --author-- lanhua.zhou


import maya.cmds as cmds
import pymel.core as pm

from zfused_maya.node.core import renderinggroup



def fix_namespace():
    # 
    _nodes = renderinggroup.nodes()
    
    if not _nodes:
        return 
    
    _short_namespace_count = {}
    
    for _node in _nodes:
        _short_namespace = cmds.referenceQuery(_node, ns = True, shn = True)
        if _short_namespace not in _short_namespace_count:
            _short_namespace_count[_short_namespace] = 0
        _short_namespace_count[_short_namespace] += 1

    _will_remove_namesapces = []
    for _node in _nodes:
        _short_namespace = cmds.referenceQuery(_node, ns = True, shn = True)
        _namespace = cmds.referenceQuery(_node, namespace = True)
        if _namespace.count(":") > 1:
            _will_remove_namesapces.append(_namespace[:- (len(_short_namespace) + 1)] ) 
            _count = _short_namespace_count[_short_namespace]
            # rename 
            if _count > 1:
                _namespace = "{}_{:0>2d}".format(_namespace, _count)
                _short_namespace_count[_short_namespace] -= 1
                _resolved_path = cmds.referenceQuery(_node, f = True)
                cmds.file(_resolved_path, e = True, namespace = _namespace.split(":")[-1], f = True)
    
    # 移除parent namespace
    _will_remove_namesapces = list(set(_will_remove_namesapces))
    for _will_remove_namesapce in _will_remove_namesapces:
        _split = _will_remove_namesapce.split(":")
        if len(_split) > 2:
            for i in range(2, len(_split)):
                _new_namespace = ":".join( _split[:i])
                _will_remove_namesapces.append(_new_namespace)
                
    _sorted_ns_namespace = sorted(_will_remove_namesapces, key=lambda ns: ns.count(':'), reverse=True)
    
    for ns in _sorted_ns_namespace:
        pm.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True, f = True)
     


if __name__ == "__main__":
    fix_namespace()