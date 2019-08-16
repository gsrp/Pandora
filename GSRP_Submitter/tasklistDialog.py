# -*- coding: utf-8 -*-
import socket

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
from ApplicationHelper import  ApplicationHelper

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
        self.pathBtn.setEnabled(False)
        self.resourcePathEdit.setEnabled(False)
        self.setWindowTitle("Tasklist Info")
        self.mayaVersionComboBox.addItem("Maya2019")
        self.renderComboBox.addItem("Redshift 2.6.41")
        self.resourcePathEdit.setText(ApplicationHelper.yaml_obj["proPath"])


    @pyqtSlot()
    def on_pathBtn_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "select resource path", "/")
        if (directory == ""):
            return
        self.resourcePathEdit.setText(directory)

    @pyqtSlot()
    def on_refreshBtn_clicked(self):
        self.refreshTasklist("","")

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
                if not os.path.isdir(path) and os.path.splitext(path)[1] == ".zip":
                    files_.append(self.convert_path(path))
        except Exception as err:
            print("get_all_files Error : "+str(err))
        finally:
            return files_

    def refreshTasklist(self,proPath,type):
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
        #开始针对新增加的文件夹 用maya打开并提交任务
        if type == dirChangedType.create and proPath != "":
            self.submitTask(proPath)

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
                self.observer.schedule(self.event_handler, path, recursive = False)
                self.observer.start()
                self.refreshTasklist("","")
                self.refreshBtn.setEnabled(True)
            except Exception as err :
                print(err)
        else:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "This path does not exist. Please re-select the path！")
            msg_box.exec_()

    # 多网卡情况下，根据前缀获取本地IP
    def GetLocalIPByPrefix(self,prefix):
        localIP = ''
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                localIP = ip

        return localIP

    def refreshAfterOpenScene(self, bResult,text,baseName,curCamera,startFrame,endFrame,framePerTask):
        try:
            self.waitDialog.closeDialog()
            if bResult == True:
                baseName = os.path.splitext(baseName)[0]
                PandoraSubmitter = getattr(__import__("PandoraSubmitter"), "PandoraSubmitter")(core=Pandoraq,
                                                                                               parent=self)
                print ("PandoraSubmitter.cb_cam : " )
                print ()
                #直接进行属性设置，并提交
                PandoraSubmitter.sp_rangeStart.setValue(int(startFrame))
                PandoraSubmitter.sp_rangeEnd.setValue(int(endFrame))

                icount = PandoraSubmitter.cb_cam.count()
                bExist = False
                for i in range(icount):
                    print ("PandoraSubmitter.cb_cam text : "+str(i))
                    print PandoraSubmitter.cb_cam.itemText(i)
                    if PandoraSubmitter.cb_cam.itemText(i) ==curCamera:
                        #msg_box = QMessageBox(QMessageBox.Critical, "Error", "the camera is  exist !")
                        #msg_box.exec_()
                        bExist =True
                        PandoraSubmitter.cb_cam.setCurrentIndex(i)
                        break
                if bExist ==False:
                    msg_box = QMessageBox(QMessageBox.Critical, "Error", "the camera is not exist !")
                    msg_box.exec_()
                    return



                print ("curCamera : " + curCamera)
                #idx = PandoraSubmitter.cb_cam.findText(curCamera)
                #if idx != -1:
                #    PandoraSubmitter.cb_cam.setCurrentIndex(idx)
                #else:
                #    print ("Error : the camera is not exist !")
                #    msg_box = QMessageBox(QMessageBox.Critical, "Error", "the camera is not exist !")
                #    msg_box.exec_()
                #    return
                PandoraSubmitter.sp_framesPerTask.setValue(int(framePerTask))
                print ("framePerTask : "+str(framePerTask))
                localIp = self.GetLocalIPByPrefix(ApplicationHelper.yaml_obj["ipPrefix"])
                print ("localIp : "+str(localIp))

                baseOutPath = "\\\\"+ localIp+"\\GSRP_Server\\renderResult\\"
                print ("baseOutPath : "+str(baseOutPath))
                if not os.path.exists(baseOutPath):
                    msg_box = QMessageBox(QMessageBox.Critical, "Error", "output path is not exist !")
                    msg_box.exec_()
                    return
                outputPath = baseOutPath +baseName+"\\a.zip"
                PandoraSubmitter.e_outputpath.setText(outputPath)
                print ("outputPath settting ")
                PandoraSubmitter.e_projectName.setText(baseName)
                print ("e_projectName settting ")
                PandoraSubmitter.e_jobName.setText(baseName)
                print ("e_jobName settting ")

                #######
                #screen = self.geometry()
                #size = PandoraSubmitter.geometry()
                #PandoraSubmitter.move(screen.left() + (screen.width() - size.width()) / 2,
                #                      screen.top() + (screen.height() - size.height()) / 2)
                #PandoraSubmitter.exec_()
                PandoraSubmitter.startSubmission()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, "Error",text)
                msg_box.exec_()
        except Exception as err:
            print("refreshAfterOpenScene Error : " + str(err))


    @pyqtSlot(int,int)
    def on_projectListWidget_cellDoubleClicked(self,row,col):
        item = self.projectListWidget.item(row, 0)
        print
        self.submitTask(item.text())
        return
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

             self.openSceneThread = openSceneThread(senceFile, self)
             self.openSceneThread.openScenefinishSignal.connect(self.refreshAfterOpenScene)
             self.openSceneThread.start()

             from waittingDialog import waittingDialog
             self.waitDialog = waittingDialog(self)
             self.waitDialog.exec_()

             #self.openScene(senceFile)
             #替换工程里面配置的资源文件路径
             #print("[MayaWorker] Before Relink:{}".format(cmds.filePathEditor(query=True, listDirectories="")))
             #传入外部资源文件所在的正确的路径，后面统一写一个（worker下载任务的路径）
             #self.relink_pathes(project_path=item.text())

    def submitTask(self,path):
        """
        import zip
        dir = os.path.dirname(path)
        baseName = os.path.dirname(path)
        print (dir+"/"+baseName)
        zip.Unzip(path,dir+"/"+baseName)
        """
        import time
        time.sleep(20)
        print ("path : " + path)
        dir = os.path.splitext(path)[0]
        print ("dir : " + dir)
        import zipfile
        z = zipfile.ZipFile(path, 'r')
        z.extractall(path=dir)
        z.close()
        #proPath = os.path.splitext(path)[0]
        #print ("os.path.splitext(path)[0] : "+ os.path.splitext(path)[0])
        configFile = dir +"/config.yaml"
        print ("configFile :" +configFile)
        if not os.path.isfile(configFile):
            print("configFile file not exist!")
            return

        senceFile = ""
        for i in os.listdir(dir):
            path_i = os.path.join(dir, i)
            if os.path.isfile(path_i) and os.path.splitext(i)[1] in ['.mb', '.ma']:
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

            self.openSceneThread = openSceneThread(senceFile,configFile, self)
            self.openSceneThread.openScenefinishSignal.connect(self.refreshAfterOpenScene)
            self.openSceneThread.start()

            from waittingDialog import waittingDialog
            self.waitDialog = waittingDialog(self)
            self.waitDialog.exec_()


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

class dirChangedType:
    move = "on_move"
    create = "on_create"
    delete = "on_delete"
    modified = "on_modified"


class FileEventHandler(FileSystemEventHandler,QObject):
    dirChanged = pyqtSignal(str,str)
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)

    def on_moved(self, event):
        if not event.is_directory:
            print("on_moved")
            self.dirChanged.emit(event.src_path,dirChangedType.move)

    def on_created(self, event):
        if not event.is_directory:
            print("on_created---------------")
            print(event.src_path)
            if os.path.splitext(event.src_path)[1] == ".zip":
                print "emit on create"
                self.dirChanged.emit(event.src_path,dirChangedType.create)
            else:
                print "not zip file "

    def on_deleted(self, event):
        print("---------------------on delete")
        print(event.is_directory)
        #if event.is_directory:
        self.dirChanged.emit(event.src_path,dirChangedType.delete)


    def on_modified(self, event):
        #print("----------------on_modified")
        if not event.is_directory:
            #print("----------------on_modified--is_directory")
            self.dirChanged.emit(event.src_path,dirChangedType.modified)



class openSceneThread(QThread):
    openScenefinishSignal = pyqtSignal(bool,str,str,str,str,str,str)
    def __init__(self, senceFile,configFile ,parent=None):
        super(openSceneThread, self).__init__(parent)
        self.parent = parent
        self.senceFile = senceFile
        self.configFile = configFile
    def run(self):
        try:
            #加载配置文件
            try:
                import yaml
                with open(self.configFile, "r") as yaml_file:
                    config_obj = yaml.load(yaml_file.read())
                    curCamera = config_obj["curCamera"]
                    endFrame = config_obj["endFrame"]
                    framePerTask = config_obj["framePerTask"]
                    startFrame = config_obj["startFrame"]
                    baseName = os.path.basename(self.senceFile)
            except Exception as err:
                self.openScenefinishSignal.emit(False, "Load Config File Error !","","","","","")
                return
            #打开maya工程
            opend = self.parent.openScene(self.senceFile)
            self.openScenefinishSignal.emit(True,"Open Scene Success !",baseName,curCamera,startFrame,endFrame,framePerTask)
        except Exception as err:
            print("openSceneThread error : "+ str(err))
            self.openScenefinishSignal.emit(False, "Open Scene Error !","","","","","")











