# coding:utf-8
# --author-- lanhua.zhou

""" shading color functions """

from Qt import QtWidgets, QtGui, QtCore

from zcore import resource

import zfused_maya.node.core.shadingengine as shadingcolorproc

class EngineItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(EngineItemDelegate, self).__init__(parent)

        self._spacing = 10

    def paint(self, painter, option, index):
        _engine_name = index.data()

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        _rect = option.rect
        _pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 0.1)
        painter.setPen(_pen)
        painter.setBrush(QtGui.QColor("#444444"))
        painter.drawRoundedRect(option.rect, 0, 0)
        #fm = QtGui.QFontMetrics(painter.font())
        # 获取引擎颜色值
        _color = shadingcolorproc.get_node_shading_color(_engine_name)
        _icon = resource.get("icons","okay.png")
        if not _color:
            # 判断color值或图片
            """
            _color = shadingcolorproc.get_connect_color(_engine_name)
            if _color:
                shadingcolorproc.set_node_shading_color(_engine_name, _color)
            else:
            """
            _color = "#444444"
            _icon = resource.get("icons","waring.png")
        # 绘制是否存在
        _icon_rect = QtCore.QRect(_rect.x(),
                                   _rect.y(),
                                   _rect.height(),
                                   _rect.height())
        painter.drawPixmap(_icon_rect.x(), _icon_rect.y(), QtGui.QPixmap(_icon).scaled(24, 24))
        # 绘制引擎颜色图标
        _color_rect = QtCore.QRect(_icon_rect.x() + _icon_rect.width() + self._spacing,
                                   _icon_rect.y() + self._spacing/2.0,
                                   _rect.height() - self._spacing,
                                   _rect.height() - self._spacing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(_color)))
        painter.drawEllipse(_color_rect)

        # 绘制着色引擎名称
        _name_rect = QtCore.QRect(_color_rect.x() + _rect.height() + self._spacing,
                                  _rect.y(),
                                  _rect.width() - _color_rect.width(),
                                  _rect.height())
        painter.drawText(_name_rect, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter, _engine_name)

        # 绘制是否存在颜色


        if option.state & QtWidgets.QStyle.State_Selected:
            bgBrush = QtGui.QBrush(QtGui.QColor(149, 194, 197, 150))
            bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        elif option.state & QtWidgets.QStyle.State_MouseOver:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 20))
            bgPen = QtGui.QPen(QtGui.QColor(60, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)
        else:
            bgBrush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 0))
            bgPen = QtGui.QPen(QtGui.QColor(160, 60, 60, 0), 0)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)        
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 30)