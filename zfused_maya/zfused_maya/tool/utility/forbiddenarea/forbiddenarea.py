# -*- coding: UTF-8 -*-
'''
@Time    : 2020/11/9 11:55
@Author  : Jerris_Cheng
@File    : ForbiddenArea.py
'''

from Qt import QtWidgets, QtGui, QtCore
from qtpy.QtWidgets import QDialog



from zwidgets.widgets import dialog

# from PySide2.QtWidgets import *
# from PySide2.QtCore import QTimer,Qt

# import zfused_maya.interface.projectinterface.taskframe as taskframe
# import zfused_api.v1.task as task

#from zfused_maya.widgets import window

import forbiddendict


class ForbiddenAreaUI(dialog.Dialog):
    def __init__(self, step_area, parent = None):
        super(ForbiddenAreaUI, self).__init__(parent)
        self._build()
        self._step_area = step_area
        self._config()

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)

    def _build(self):
        self.resize(1200, 800)
        self.base_widget = QtWidgets.QFrame()
        self.add_content_widget(self.base_widget)

        self.baselyout = QtWidgets.QGridLayout(self.base_widget)
        # self.setLayout(self.baselyout)
        self.tree_widget = QtWidgets.QWidget()
        self.baselyout.addWidget(self.tree_widget)
        self.layout = QtWidgets.QGridLayout(self.tree_widget)
        self.forBiddenarea_treewidget = QtWidgets.QTreeWidget()
        self.layout.addWidget(self.forBiddenarea_treewidget)
        self.forBiddenarea_treewidget.setItemsExpandable(False)

        self.forBiddenarea_treewidget.setStyleSheet("font-size:18px")
        self.forBiddenarea_treewidget.header().setStyleSheet("font-size:16px")
        
        # self.toolwidget=QtWidgets.QWidget()
        # self.toolLayout=QtWidgets.QGridLayout(self.toolwidget)
        # self.baselyout.addWidget(self.toolwidget)
        # self.skip_btn = QtWidgets.QPushButton("Skip")
        # self.skip_btn.clicked.connect(self.close_dialog)
        # self.toolLayout.addWidget(self.skip_btn)
        # self.toolLayout.setAlignment(QtCore.Qt.AlignRight)
        # self.skip_btn.setFixedWidth(150)

        self.Timer = QtCore.QTimer()
        self.Timer.start(60000*5)
        self.Timer.timeout.connect(self.close_dialog)


    def _config(self):
        self.setWindowTitle(u"{}部门雷区".format(self._step_area))
        self.set_title (u"{}部门雷区".format(self._step_area))

        self.forBiddenarea_treewidget.setColumnCount(4)
        self.forBiddenarea_treewidget.setHeaderLabels([u"雷区类别", u"雷区性质", u"雷区简述", u"雷区详细描述"])
        self.forBiddenarea_treewidget.setColumnWidth(0, 150)
        self.forBiddenarea_treewidget.setColumnWidth(1, 150)
        self.forBiddenarea_treewidget.setColumnWidth(2, 300)
        self.forBiddenarea_treewidget.setColumnWidth(4, 800)

        # 配置信息
        # 。。。。
        AreaDict = {}
        projectDict = self.get_area_dict("project")
        departmentDict = self.get_area_dict(self._step_area)

        AreaDict.update(departmentDict)
        AreaDict.update(projectDict)

        print(AreaDict)

        for department in AreaDict:
            departmentItem=QtWidgets.QTreeWidgetItem(self.forBiddenarea_treewidget)
            departmentItem.setText(0,department)
            _departmentList=AreaDict.get(department)
            for item in  _departmentList:
                nature=item.get("nature")
                synopsis=item.get("synopsis")
                description=item.get("description")
                item_WidgetItem=QtWidgets.QTreeWidgetItem(departmentItem)


                item_WidgetItem.setText(1,nature)
                item_WidgetItem.setText(2,synopsis)
                item_WidgetItem.setText(3,description)

                if nature==u"严禁":
                    item_WidgetItem.setTextColor(1,"red")
                elif nature==u"建议":
                    item_WidgetItem.setTextColor(1,"Yellow")
                elif nature==u"常规":
                    item_WidgetItem.setTextColor(1,"Green")


        self.forBiddenarea_treewidget.expandAll()

        '''

        for department in AreaDict:
            departmentItem = QtWidgets.QTreeWidgetItem(self.forBiddenarea_treewidget)
            departmentItem.setText(0, department)
            _departmentDict = AreaDict.get(department)
            if _departmentDict:
                for nature in _departmentDict:
                    natureItem = QtWidgets.QTreeWidgetItem(departmentItem)
                    natureItem.setText(1, nature)
                    ForbiddenList = _departmentDict.get(nature)
                    for Forbidden in ForbiddenList:
                        forbiddenitem = QtWidgets.QTreeWidgetItem(natureItem)
                        forbiddenitem.setText(2, Forbidden)
                        explan = AreaExplain.get(Forbidden)
                        forbiddenitem.setText(3, explan)
                        forbiddenitem.setText(1, nature)

        # self.forBiddenarea_treewidget.setRootIsDecorated(False)
        self.forBiddenarea_treewidget.expandAll()
        '''

    def get_area_dict(self, Department):
        #parentdict = ForbiddenArea.get(Department)
        #newDict = {Department: parentdict}
        departmentdict=forbiddendict.all_dcit.get(Department)

        n_Dict={
            Department:departmentdict
        }
        return n_Dict

    def close_dialog(self):
        self.close()






