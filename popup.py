# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updated.ui'
#
# Created: Tue Mar 03 02:48:54 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Popup(object):
    def setupUi(self, Popup):
        Popup.setObjectName(_fromUtf8("Popup"))
        Popup.setWindowModality(QtCore.Qt.ApplicationModal)
        Popup.resize(273, 193)
        Popup.setMinimumSize(QtCore.QSize(0, 0))
        Popup.setMaximumSize(QtCore.QSize(273, 193))
        self.gridLayout = QtGui.QGridLayout(Popup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.updateLabel = QtGui.QLabel(Popup)
        self.updateLabel.setMaximumSize(QtCore.QSize(1000, 1000))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.updateLabel.setFont(font)
        self.updateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.updateLabel.setObjectName(_fromUtf8("updateLabel"))
        self.gridLayout.addWidget(self.updateLabel, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(Popup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.updatePushButton = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updatePushButton.sizePolicy().hasHeightForWidth())
        self.updatePushButton.setSizePolicy(sizePolicy)
        self.updatePushButton.setObjectName(_fromUtf8("updatePushButton"))
        self.gridLayout_2.addWidget(self.updatePushButton, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi(Popup)
        QtCore.QMetaObject.connectSlotsByName(Popup)

    def retranslateUi(self, Popup):
        Popup.setWindowTitle(_translate("Popup", "Updated", None))
        self.updateLabel.setText(_translate("Popup", "Received an ATIS Update", None))
        self.updatePushButton.setText(_translate("Popup", "OK!", None))

