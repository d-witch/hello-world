# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Dialog_HttpMsg.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1111, 679)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.row = QtWidgets.QWidget()
        self.row.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.row.setObjectName("row")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.row)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tb_row = QtWidgets.QTextBrowser(self.row)
        self.tb_row.setObjectName("tb_row")
        self.verticalLayout_2.addWidget(self.tb_row)
        self.tabWidget.addTab(self.row, "")
        self.decoded = QtWidgets.QWidget()
        self.decoded.setObjectName("decoded")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.decoded)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_decoded = QtWidgets.QTextBrowser(self.decoded)
        self.tb_decoded.setObjectName("tb_decoded")
        self.verticalLayout.addWidget(self.tb_decoded)
        self.tabWidget.addTab(self.decoded, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinbox_font_size = QtWidgets.QSpinBox(Dialog)
        self.spinbox_font_size.setSuffix("")
        self.spinbox_font_size.setPrefix("")
        self.spinbox_font_size.setObjectName("spinbox_font_size")
        self.horizontalLayout.addWidget(self.spinbox_font_size)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.row), _translate("Dialog", "原始消息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.decoded), _translate("Dialog", "Url解码"))
        self.label.setText(_translate("Dialog", "字体大小"))
