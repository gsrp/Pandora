import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from ApplicationHelper import  ApplicationHelper
import os
import yaml

if __name__ == '__main__':
    try:
        QApplication(sys.argv)
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        ApplicationHelper.configPath = dirname +  ApplicationHelper.configPath
        ApplicationHelper.configPath = ApplicationHelper.configPath.replace('\\', '/')
        try:
            import yaml
            with open(ApplicationHelper.configPath, "r") as yaml_file:
                ApplicationHelper.yaml_obj = yaml.load(yaml_file.read())
        except Exception as err:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "conf.ini parse failed !")
            msg_box.exec_()
            sys.exit()
        from  tasklistDialog import mainWindow
        dd = mainWindow()
        dd.show()
    except Exception as err:
        print(err)

    qApp.exec_()
