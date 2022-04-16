# coding:utf-8
# CODE_TITLE      = u'减面'
# CODE_AUTHOR     = 'ning.qin'
# CODE_VERSION    = '0.1'
# CODE_START_DATE = 20190311
# CODE_EDIT_DATE  = 20190311

from pymel.core import *
import maya.cmds as cmds
import maya.mel as mel

# GPU_DIR = 'D:/project/Backkom/import'
# GPU_FILENAME = 'test_tree_gpu'

def reduce_mesh(reduce_percentage, gpu_dir, gpu_filename):
    _geo_list = ls(type = 'mesh', ni = True)
    _reduced_grp_node = 'reduced_geo_grp'
    createNode('transform', name = 'reduced_geo_grp')
    for _geo in _geo_list:
        _reduced_geo = duplicate(_geo)
        parent(_reduced_geo, 'reduced_geo_grp')
        select(_reduced_geo, replace = True)
        #清理
        mel.eval('polyCleanupArgList 4 { "0","1","0","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0","0" };')
        #减面
        polyReduce(_reduced_geo, version = 1, termination = 0, sharpness = 0, keepBorder = False, keepMapBorder = False, keepColorBorder = True, keepFaceGroupBorder = True, keepHardEdge = True, keepCreaseEdge = True,
                   keepBorderWeight = 0.5, keepMapBorderWeight = 0.5, keepColorBorderWeight = 0.5, keepFaceGroupBorderWeight = 0.5, keepHardEdgeWeight = 0.5, keepCreaseEdgeWeight = 0.5,
                   useVirtualSymmetry = 0, symmetryTolerance = 0.01, symmetryPlaneX = 0, symmetryPlaneY = 1, symmetryPlaneZ = 0, symmetryPlaneW = 0, preserveTopology = True, keepQuadsWeight = 0,
                   vertexMapName = "", cachingReduce = True, caching = True, percentage = reduce_percentage, vertexCount = 0, triangleCount = 0, replaceOriginal = True)
    # mel.eval('gpuCache -startTime 1 -endTime 1 -optimize -optimizationThreshold 40000 -writeMaterials -dataFormat ogawa -directory "{}" -fileName "{}" {};'.format(gpu_dir, gpu_filename, _reduced_grp_node))
    cmds.gpuCache(_reduced_grp_node, useBaseTessellation = True, startTime = 1, endTime = 1, writeMaterials = True, directory = gpu_dir, fileName = gpu_filename) #allDagObjects = True)
        
    delete(_reduced_grp_node)

#reduce_mesh(80, GPU_DIR, GPU_FILENAME)
