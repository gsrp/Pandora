# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\task\Render_GSRP_UI\waitting.ui',
# licensing of 'D:\task\Render_GSRP_UI\waitting.ui' applies.
#
# Created: Mon Jul 22 14:41:29 2019
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_waitDialog(object):
    def setupUi(self, waitDialog):
        waitDialog.setObjectName("waitDialog")
        waitDialog.resize(376, 76)
        waitDialog.setStyleSheet("background-color: #e6e6e6;")
        self.gridLayout = QtWidgets.QGridLayout(waitDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.waitMessageLabel = QtWidgets.QLabel(waitDialog)
        self.waitMessageLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.waitMessageLabel.setStyleSheet("font: 16px \"微软雅黑\";\n"
"background-color: #e6e6e6;\n"
"\n"
"")
        self.waitMessageLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.waitMessageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waitMessageLabel.setObjectName("waitMessageLabel")
        self.gridLayout.addWidget(self.waitMessageLabel, 0, 0, 1, 1)

        self.retranslateUi(waitDialog)
        QtCore.QMetaObject.connectSlotsByName(waitDialog)

    def retranslateUi(self, waitDialog):
        waitDialog.setWindowTitle(QtWidgets.QApplication.translate("waitDialog", "waiting", None, -1))
        self.waitMessageLabel.setText(QtWidgets.QApplication.translate("waitDialog", "正在打开场景,请稍等...(1s)", None, -1))

