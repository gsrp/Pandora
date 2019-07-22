# -*- coding: utf-8 -*-
try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	psVersion = 2
except:
	from PySide.QtCore import *
	from PySide.QtGui import *
	psVersion = 1

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import sys, os
from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot

import maya.cmds as cmds

for i in ["Ui_MainWindow"]:
	try:
		del sys.modules[i]
	except:
		pass

sys.path.append(os.path.join(os.path.dirname(__file__), "UserInterfacesPandora"))

if psVersion == 1:
    pass
    #import tasklist_uips1 as tasklist_ui
else:
	import projectList_ui


class mainWindow(QDialog, projectList_ui.Ui_projectListDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.init()


    def init(self):
        #self.refreshBtn.clicked.connect(self.on_pathBtn_clicked)
        #init renderSetting and resourcePath from config.xml
        self.observer = Observer()
        #self.projectListWidget.setFocusPolicy(Qt.NoFocus)
        self.projectListWidget.horizontalHeader().setStretchLastSection(True)
        self.refreshBtn.setEnabled(False)
        self.resourcePathEdit.setEnabled(False)
        self.setWindowTitle("Tasklist Info")
        self.mayaVersionComboBox.addItem("Maya2019")
        self.renderComboBox.addItem("Redshift 2.6.41")

    @pyqtSlot()
    def on_pathBtn_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "select resource path", "/")
        if (directory == ""):
            return
        self.resourcePathEdit.setText(directory)

    @pyqtSlot()
    def on_refreshBtn_clicked(self):
        self.refreshTasklist()

    def convert_path(self,path):
        try:
            seps = r'\/'
            sep_other = seps.replace(os.sep, '')
            return path.replace(sep_other, os.sep) if sep_other in path else path
        except Exception as err:
            print("convert_path Error : "+str(err))
            return path

    def get_all_files(self,dir):
        files_ = []
        try:
            list = os.listdir(dir)
            for i in range(0, len(list)):
                path = os.path.join(dir, list[i])
                if os.path.isdir(path):
                    files_.append(self.convert_path(path))
        except Exception as err:
            print("get_all_files Error : "+str(err))
        finally:
            return files_

    def refreshTasklist(self):
        try:
            path = self.resourcePathEdit.text()
            files = self.get_all_files(path)
            count = len(files)
            self.projectListWidget.clearContents()
            self.projectListWidget.setRowCount(count)
            for i in range(count):
                item = QTableWidgetItem(files[i])
                item.setFlags(item.flags() & (~Qt.ItemIsEditable))
                self.projectListWidget.setItem(i, 0, item)
        except Exception as err:
            print("RefreshTasklist Error :"+str(err))

    @pyqtSlot(str)
    def on_resourcePathEdit_textChanged(self,path):
        bExist= os.path.isdir(path)
        if bExist ==True:
            try:
                self.observer.stop()
                self.observer = Observer()
                self.event_handler = FileEventHandler()

                #QObject.connect(self.event_handler, self.event_handler.dirChanged, self.refreshTasklist,Qt.AutoConnection)

                self.event_handler.dirChanged.connect(self.refreshTasklist)
                self.observer.schedule(self.event_handler, path, True)
                self.observer.start()
                self.refreshTasklist()
                self.refreshBtn.setEnabled(True)
            except Exception as err :
                print(err)
        else:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "This path does not exist. Please re-select the path！")
            msg_box.exec_()

    @pyqtSlot(int,int)
    def on_projectListWidget_cellDoubleClicked(self,row,col):
        item = self.projectListWidget.item(row,0)
        senceFile = ""
        for i in os.listdir(item.text()):
            path_i = os.path.join(item.text(), i)
            if os.path.isfile(path_i) and os.path.splitext(i)[1] in ['.mb','.ma']:
                senceFile = path_i
                break
        if senceFile != "":
             global Pandoraq
             import sys
             self.pandoraRoot = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
             sys.path.append(os.path.join(self.pandoraRoot, "Pandora", "Scripts"))

             import maya.standalone
             maya.standalone.initialize('Python')

             Pandoraq = getattr(__import__("PandoraCore"), "PandoraCore")(app="Maya")
             self.openScene(senceFile)
             #替换工程里面配置的资源文件路径
             #print("[MayaWorker] Before Relink:{}".format(cmds.filePathEditor(query=True, listDirectories="")))
             #传入外部资源文件所在的正确的路径，后面统一写一个（worker下载任务的路径）
             #self.relink_pathes(project_path=item.text())
             PandoraSubmitter = getattr(__import__("PandoraSubmitter"), "PandoraSubmitter")(core=Pandoraq,parent=self)

             screen = self.geometry()
             size = PandoraSubmitter.geometry()
             PandoraSubmitter.move(screen.left() + (screen.width() - size.width()) / 2,
                       screen.top() + (screen.height() - size.height()) / 2)
             PandoraSubmitter.exec_()


    def openScene(self, path=None):
        import maya.cmds as cmds
        if os.path.exists(path):
            # self.checkState()
            opend = cmds.file(path, o=True, f=True, esn=True)
            print("\n\n[MayaWorker] Opend Sence: {}\n\n".format(opend))
            return opend

    #############################################################
    # maya操作接口封装
    #############################################################
    def checkState(self):
        import maya.cmds as cmds
        # check if there are unsaved changes
        fileCheckState = cmds.file(q=True, modified=True)

        # if there are, save them first ... then we can proceed
        if fileCheckState:
            cmds.SaveScene()

    def relink_pathes(self, project_path=None):

        results = []
        # 获取当前所有已注册的外部文件
        links = cmds.filePathEditor(query=True, listDirectories="")
        if links == None:
            return results
        # 获取文件相关的所有节点
        for link in links:
            pairs = cmds.filePathEditor(query=True, listFiles=link, withAttribute=True, status=True)
            '''
            paris: list of strings ["file_name node status ...", "file_name node status ...",...]
            we need to make this large list of ugly strings (good inforamtion seperated by white space) into a dictionry we can use
            '''
            l = len(pairs)
            items = l / 3
            order = {}
            index = 0

            '''
            order: dict of {node: [file_name, status],...}
            '''

            for i in range(0, items):
                order[pairs[index + 1]] = [pairs[index], pairs[index + 2]]
                index = index + 3

            for key in order:
                # for each item in the dict, if the status is 0, repath it
                if order[key][1] == "0":
                    if self.repath(key, order[key][0], project_path):
                        results.append(key)
        return results


    def repath(self, node, file, project_path):
        matches = []
        for root, dirnames, filenames in os.walk(project_path):
            for x in filenames:
                if x == file:
                    matches.append([root, os.path.join(root, x)])
                elif x.split(".")[0] == file.split(".")[
                    0]:  # ---> this second option is used when a file is useing ##### padding, we can match by name only

                    x_ext = x.split(".")[len(x.split(".")) - 1]
                    file_ext = file.split(".")[len(file.split(".")) - 1]
                    if x_ext == file_ext:
                        matches.append([root, os.path.join(root, x)])

        if len(matches) > 0:
            return cmds.filePathEditor(node, repath=matches[0][0])

        return None



class FileEventHandler(FileSystemEventHandler,QObject):
    dirChanged = pyqtSignal()
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            self.dirChanged.emit()

    def on_created(self, event):
        if event.is_directory:
            self.dirChanged.emit()


    def on_deleted(self, event):
        print("---------------------on delete")
        print(event.is_directory)
        #if event.is_directory:
        self.dirChanged.emit()


    def on_modified(self, event):
        print("----------------on_modified")
        if event.is_directory:
            print("----------------on_modified--is_directory")
            self.dirChanged.emit()










