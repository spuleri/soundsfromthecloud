# This Python file uses the following encoding: utf-8
from sounds import Sounds
import json
import os


import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QDialog, QFileDialog
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QThread
from gui import Ui_Form
from dialog import Ui_Status

#pyuic4 -x download_dialog.ui -o dialog.py
#link gui 
#http://stackoverflow.com/a/9526625/3590748
#use code
#http://stackoverflow.com/questions/15362624/how-do-you-execute-pyqt-ui-code-in-python 

    
#url to test resolver
# #http://api.soundcloud.com/resolve.json?url=https://soundcloud.com/jamkins/sets/theabyss&client_id=c585c5f24b092caec68984885cf2b0db

def main():

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
 

    #url = raw_input("Hello, please paste your soundcloud url below" + os.linesep)
    #path = raw_input("Paste the path on your computer to download files to" + os.linesep)
    # url = window.directory
    # print url
    # sound = Sounds(url, path)
    # sound.download()

    print "finished, but there were " + str(len(sound.errors)) + " errors. Check the log file" + os.linesep

    f = open('log.txt', 'wb')

    for error in sound.errors:
        f.write(error["title"].decode('utf-8') +" -> " + error["permalink_url"] + "\n")
        f.write(error["error"])
        f.write("\n\n")


class Window(QtGui.QWidget):
    def __init__(self, directory="", url="", readyToGo = False):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.dialog = Dialog(self)

        #connect QDialog finished slot, to see if pressed OK or CANCEL
        self.dialog.finished.connect(self.dialogFinished)

        

    def getDir(self):
        directory = QFileDialog.getExistingDirectory()
        directory = str(directory)
        print directory
        print type(directory)
        self.directory = directory
        self.ui.dirLine.setText(self.directory)

    def urlPasted(self, QString):
        string = str(QString)
        if "https://soundcloud.com" in string:
            self.url = string
            self.readyToGo = True
            print self.url
            return self.url

    def downloadButton(self):
        if self.readyToGo:

            self.dialog.show()
            sound = Sounds(self.url, self.directory)

            # #set as read only
            self.dialog.ui.statusTextEdit.setReadOnly(True)
            self.dialog.ui.statusTextEdit.insertPlainText("Loading data...")
            # status = sound.download(self.dialog_ui)
            self.workerThread = WorkerThread(sound, self.dialog)
            #connect finished() signal to my own slot
            self.workerThread.finished.connect(self.downloadDone)
            self.workerThread.start()
                     
        else:
            print 'his'
            #popup error box? if self.url="" or self.directory=""

    def downloadDone(self):
        print "we done boiz"
        
        self.dialog.ui.statusTextEdit.appendPlainText("\n" + "Finished all downloads. ")

        #if sound object had errors
        num_errors = len(self.workerThread.sound.errors)
        if num_errors > 0:

            
            error_msg = "But there were " + str(num_errors) + " error(s)." + "\n" + "Check the errors.txt file" + "\n"
            self.dialog.ui.statusTextEdit.appendPlainText(error_msg)

            f = open('errors.txt', 'wb')

            for error in self.workerThread.sound.errors:
                f.write(error["title"].decode('utf-8') +" -> " + error["permalink_url"] + "\n")
                f.write(error["error"])
                f.write("\n\n")

        #after hit "OK" clear dialog statusTextEdit and clear url

    def dialogFinished(self, value):
        #the finished slot returns 1 for OK
        #and 0 for cancel
        if value == 1:
            #reset url values
            self.ui.lineEdit.clear()
            self.url = ""
            #clear dialog
            self.dialog.ui.statusTextEdit.clear()


 

class Dialog (QDialog):

    statusUpdate = pyqtSignal(str)

    def __init__(self, parent = None):
        self.parent = parent
        QDialog.__init__(self, self.parent)
        self.ui = Ui_Status()
        self.ui.setupUi(self)
        #stauts update signal

        # Connect the trigger signal to a slot.
        self.statusUpdate.connect(self.updateStatus)

    def updateStatus(self, string):
        self.ui.statusTextEdit.appendPlainText(string)




class WorkerThread(QThread):
    def __init__(self, sound = None, dialog = None, parent = None):
        super(WorkerThread, self).__init__(parent)
        #sound class instance
        #and dialog instance
        self.sound = sound
        self.dialog = dialog

    def run(self):
        self.sound.download(self.dialog)
        



if __name__ == "__main__":
    main()


