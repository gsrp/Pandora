import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *

if __name__ == '__main__':
    try:
        QApplication(sys.argv)
        from  tasklistDialog import mainWindow
        dd = mainWindow()
        dd.show()
    except Exception as err:
        print(err)

    qApp.exec_()
