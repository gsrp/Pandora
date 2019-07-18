import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *

if __name__ == '__main__':
    try:
        QApplication(sys.argv)
        from  tasklistDialog import mainWindow
        dd = mainWindow()
        dd.show()


        #global Pandora
        #import PandoraCore
        #import maya.standalone
        #import maya.cmds as cmds

        #maya.standalone.initialize('Python')

        #Pandora = PandoraCore.PandoraCore(app="Maya")
        #Pandora.openSubmitter()
    except Exception as err:
        print(err)

    qApp.exec_()
