# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sounds.ui'
#
# Created: Sat Jun 13 21:22:40 2015
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
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(202, 10, 161, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(190, 320, 201, 41))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.downloadButton = QtGui.QPushButton(self.splitter)
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.pushButton = QtGui.QPushButton(self.splitter)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(60, 150, 411, 93))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dirLine = QtGui.QLineEdit(self.widget)
        self.dirLine.setObjectName(_fromUtf8("dirLine"))
        self.horizontalLayout.addWidget(self.dirLine)
        self.fileButton = QtGui.QToolButton(self.widget)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.horizontalLayout.addWidget(self.fileButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.fileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.getDir)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.downloadButton)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Form.urlPasted)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit.clear)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit.clear)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.dirLine.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "soundsfromthecloud", None))
        self.label_3.setText(_translate("Form", "***Please support the artists***", None))
        self.downloadButton.setText(_translate("Form", "Download!", None))
        self.pushButton.setText(_translate("Form", "Clear Fields", None))
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

