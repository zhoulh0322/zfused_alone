# -*- coding: UTF-8 -*-
'''
@Time    : 2020/11/11 14:14
@Author  : Jerris_Cheng
@File    : forbiddendict.py
'''


all_dcit={
    "project":[
        {"nature":u"严禁",
         "synopsis":u"项目制作规范",
         "description":u"软件版本，制作比例，摄像机尺寸，帧率等。不同项目会附带项目要求。"
        },
        {"nature":u"严禁",
         "synopsis":u"禁止使用软件默认命名",
         "description":u"例如模型绑定等等使用 joint1 curve，层级使用default等"
        },
        {"nature":u"严禁",
        "synopsis":u"文件提交和存放规范",
        "description":u"禁止返回修改的镜头没有修改完成的时间预估和时间反馈"
    },
        {"nature":u"严禁",
        "synopsis":u"禁止返回修改的镜头没有修改完成的时间预估和时间反馈",
        "description":u"下游部门打回上游部门进行修改的文件，上游部门没有修改时间的评估和和反馈，使得下游部门无法做计划安排。"
    },
    	{"nature":u"严禁",
        "synopsis":u"上传描述需要严谨",
        "description":u"上传文件的时候，需要详细描述上传文件修改的内容，严禁无意义内容"
    }
    ],
    "model":[
    {
        "nature":u"严禁",
        "synopsis":u"禁止非同材质属性模型混用合并",
        "description":u"不同物理属性的物品不可用同一材质球,\n不同物理属性的物品不可合并到一起\n物体combine不能出现多个材质球（解决方案）项目负责人安排指定人员抽时间检查 TD插件检查"
    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止模型面数过高",
        "description":u"常规场景建筑不超过40W四边面，常规角色角色不超过5W四边面，而身体裸模部分不超过2W面（根据项目具体判断）"
    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止贴图尺寸非2的N次方",
        "description":u"贴图尺寸使用的是非 1024 2048 等"
    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止uv反向和重叠",
        "description":u"每个物体的UV与UV间不要有重叠。"

    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止模型穿插场景穿插浮空",
        "description":u"模型自身穿插，场景物体穿插浮空。"
    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止模型破面和多余点线面",
        "description":u"模型是否有破面以及多余点末清理。如无特殊要求左右是必须是对称的",

    },
    {
        "nature":u"严禁",
        "synopsis":u"禁止无用序列贴图",
        "description":u"场景拆分元素使用的其他部分的序列贴图需要删除，渲染器不会识别拆分模型所用的具体序列贴图，会全部加载"
    },
    {
        "nature":u"建议",
        "synopsis":u"建议尽量不使用多象限",
        "description":u"除了角色、身体和山体这种精度要求高的模型，其它都在第一象限。"
    },
    {
        "nature":u"常规",
        "synopsis":u"模型对称",
        "description":u"如无特殊要求左右是必须是对称的。"

    }
],

    "rig":[
    {
        "nature":u"严禁",
        "synopsis":u"禁止控制器名称修改",
        "description":u"绑定迭代文件出现控制器名称改变，会对动画造成不可预估的后果。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止控制器层级修改",
        "description": u"绑定迭代文件出现控制器层级改变，会对动画造成不可预估的后果。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止控制器key帧，不归零",
        "description": u"绑定在做绑定权重或修型处理的时候，会对角色进行动画编辑，提交时忘记还原k帧。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"修型穿插",
        "description": u"严禁修型后模型部分还是穿插，不符合动画动作要求（例如手部绷带）"
    },


],

    "animation":[
    {
        "nature": u"严禁",
        "synopsis": u"禁止出现角色场景穿插浮空",
        "description": u"角色与场景道具穿插，角色浮空等。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止存在非需要的reference,",
        "description": u"文件里的reference如有不需要使用的，需要移出参考，而不是取消加载refernce，后续环节会有疑惑和误操作的可能，同时也造成文件加载卡顿。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止无前后预留帧动画",
        "description": u"前后需要预留动画，解算渲染需要。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止无T-pose和过度动画",
        "description": u"动画提前50帧做好T-pose，t-pose到入境前，角色不能穿插。"
    },
    {
        "nature": u"建议",
        "synopsis": u"禁止角色自身运动穿插",
        "description": u"角色运动过程中，身体不能自穿，要给解算预留空间，互动角色不能穿插。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止未关闭2D Pan/zoom",
        "description": u"2D Pan/zoom在使用完之后没有关掉，导致后期渲染出来与拍屏不符。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止随意key缩放",
        "description": u"K道具的时候如果没有特殊要求不要放大或缩小，要位移只K位移。"
    },
    {
        "nature": u"建议",
        "synopsis": u"符合物理规律",
        "description": u"不要只根据摄像机角度k帧，在透视图里也看看是否正常，避免穿插错位，没有特殊要求尽量符合物理规律"
    },
    {
        "nature": u"建议",
        "synopsis": u"特效示意未在规定组内",
        "description": u"最终动画文件里，特效示意模型要存放规定组内，会误导后续环节。"
    },
    {
        "nature": u"建议",
        "synopsis": u"整理文件",
        "description": u"动画文件整理不干净，例如不使用的参考资产没有删除，display层没有将没用的分层删除，大纲中没有按照相机、角色、道具、场景、特效示意进行分类等"
    },

],




"cfx":[
    {
        "nature": u"严禁",
        "synopsis": u"禁止穿插，穿帮",
        "description": u"提交文件仔细检查穿帮和穿插"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止无预留缓存",
        "description": u"递交下一环节的缓存动态要正确，前后要多出5帧，影响后期运动模糊"
    },
    {
        "nature": u"建议",
        "synopsis": u"塑形优化",
        "description": u"毛发制作时，毛发套数、曲线的数量、曲线的点数要优化"
    }
],
    "sfx":[
    {
        "nature": u"严禁",
        "synopsis": u"禁止提交缓存错误",
        "description": u"输出缓存alembic不带uv，后期无法渲染"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止提交素材坏帧缺帧",
        "description": u"特效所出的渲染素材/abc有坏帧或者少帧（多出在后期临时需求的素材上）"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止拍屏与nuke文件对不上",
        "description": u"nuke文件更新了，但是拍屏没有更新。"
    },
    {
        "nature": u"严禁",
        "synopsis": u"禁止渲染尺寸不对",
        "description": u"素材渲染尺寸与要求尺寸不符合。"
    },

],
    "lighting":[
    {
        "nature": u"严禁",
        "synopsis": u"禁止未检查小样提交农场",
        "description": u"学生上农场之前多出前中后各出1张小样单帧检查清楚。"
    },
]



}