#coding:utf-8
#--author-- lanhua.zhou

#pyside and qtpy
from Qt import QtGui,QtWidgets,QtCore

import zfused_maya.node.core.check as check
from zfused_maya.ui.widgets import window

class Widget(window._Window, check.Check):
    def __init__(self, parent = None):
        super(Widget, self).__init__(parent)
        self._build()
        self.allCheckWidget = []
        self.recheck_button.clicked.connect(self._check_all)

    def show(self):
        self._check_all()
        super(Widget, self).show()
        
    def _check_all(self):
        _is_ok = True
        for widget in self.allCheckWidget:
            print(widget)
            if self.auto_clear():
                widget.clear()
            value = widget.check()
            if not value:
                _is_ok = False
                widget.setHidden(False)
            else:
                if not self.show_all():
                    widget.setHidden(True)
                else:
                    widget.setHidden(False)
            QtWidgets.QApplication.processEvents()
        if _is_ok:
            self.close()
        check.Check.value = _is_ok

    def add_widget(self, widget):
        """ add check widget 

        """
        self.bodyLayout.addWidget(widget)
        self.allCheckWidget.append(widget)

    def addWidget(self, widget):
        self.bodyLayout.addWidget(widget)
        self.allCheckWidget.append(widget)

    def getAllCheckWidget(self):
        return self.allCheckWidget
        
    def auto_clear(self):
        return self.autoClearCheckBox.isChecked()

    def show_all(self):
        return self.show_all_checkbox.isChecked()

    def _build(self):
        self.resize(600,600)
        #self.set_title_name("检查场景(check scene)")

        # scroll widget
        self.scroll_widget = QtWidgets.QScrollArea()
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scroll_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.bodyWidget = QtWidgets.QFrame()
        self.scroll_widget.setWidget(self.bodyWidget)
        layout = QtWidgets.QVBoxLayout(self.bodyWidget)
        layout.setContentsMargins(4,4,4,4)
        self.bodyLayout = QtWidgets.QVBoxLayout(self.bodyWidget)
        self.bodyLayout.setContentsMargins(8,8,8,8)

        layout.addLayout(self.bodyLayout)
        layout.addStretch()

        # auto recheck button
        self.recheck_widget = QtWidgets.QWidget()
        self.recheck_layout = QtWidgets.QHBoxLayout(self.recheck_widget)
        self.recheck_layout.setSpacing(4)
        self.recheck_layout.setContentsMargins(0,0,0,0)
        
        # show all item widget
        self.show_all_checkbox = QtWidgets.QCheckBox()
        self.show_all_checkbox.setText(u"显示所有检查面板")
        self.recheck_layout.addWidget(self.show_all_checkbox)
        self.recheck_layout.addStretch(True)
        
        # auto checkbox
        self.autoClearCheckBox = QtWidgets.QCheckBox()
        self.recheck_layout.addWidget(self.autoClearCheckBox)
        self.autoClearCheckBox.setText(u"自动清理")
        
        # recheck button
        self.recheck_button = QtWidgets.QPushButton()
        self.recheck_button.setMinimumSize(100,30)
        self.recheck_layout.addWidget(self.recheck_button)
        self.recheck_button.setText(u"重新检查")

        self.set_central_widget(self.scroll_widget)
        self.set_tail_widget(self.recheck_widget)