# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sounds.ui'
#
# Created: Wed May 20 21:34:01 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(565, 408)
        self.downloadButton = QtGui.QPushButton(Form)
        self.downloadButton.setGeometry(QtCore.QRect(190, 320, 141, 41))
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.layoutWidget = QtGui.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 140, 461, 41))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dirLine = QtGui.QLineEdit(self.layoutWidget)
        self.dirLine.setObjectName(_fromUtf8("dirLine"))
        self.horizontalLayout_2.addWidget(self.dirLine)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.fileButton = QtGui.QToolButton(self.layoutWidget)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.horizontalLayout_3.addWidget(self.fileButton)
        self.layoutWidget1 = QtGui.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(51, 181, 421, 22))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.fileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.getDir)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.downloadButton)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Form.urlPasted)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.downloadButton.setText(_translate("Form", "Download!", None))
        self.label_2.setText(_translate("Form", "Directory to download:", None))
        self.fileButton.setText(_translate("Form", "...", None))
        self.label.setText(_translate("Form", "SoundCloud URL:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

