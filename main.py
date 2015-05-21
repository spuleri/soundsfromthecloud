#!flask/bin/python
from sounds import Sounds
import json
import os


import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QDialog, QFileDialog
from PyQt4.QtCore import QObject, pyqtSlot
from gui import Ui_Form

#pyuic4 -x sounds.ui -o gui.py
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

    def getDir(self):
        directory = QFileDialog.getExistingDirectory()
        print directory
        self.directory = directory
        self.ui.dirLine.setText(self.directory)

    def urlPasted(self, QString):
        string = str(QString)
        if "https://soundcloud.com" in string:
            self.url = string
            self.readyToGo = True
            print string

    def downloadButton(self):
        if self.readyToGo:
            sound = Sounds(self.url, self.directory)
            status = sound.download()
            #returns true once download finishes
            if status:
                print 'lol'
                #show dialog?


        else:
            print "u aint ready fuckboi"



if __name__ == "__main__":
    main()


