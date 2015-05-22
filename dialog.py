# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_dialog.ui'
#
# Created: Thu May 21 23:20:29 2015
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

class Ui_Status(object):
    def setupUi(self, Status):
        Status.setObjectName(_fromUtf8("Status"))
        Status.resize(412, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Status)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.statusTextEdit = QtGui.QPlainTextEdit(Status)
        self.statusTextEdit.setGeometry(QtCore.QRect(30, 30, 351, 161))
        self.statusTextEdit.setObjectName(_fromUtf8("statusTextEdit"))

        self.retranslateUi(Status)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Status.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Status.reject)
        QtCore.QMetaObject.connectSlotsByName(Status)

    def retranslateUi(self, Status):
        Status.setWindowTitle(_translate("Status", "Dialog", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Status = QtGui.QDialog()
    ui = Ui_Status()
    ui.setupUi(Status)
    Status.show()
    sys.exit(app.exec_())

