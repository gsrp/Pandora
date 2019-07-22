# -*- coding: utf-8 -*-
import math

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	psVersion = 2
except:
	from PySide.QtCore import *
	from PySide.QtGui import *
	psVersion = 1

from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot
from waitting_ui import Ui_waitDialog






class waittingDialog(QDialog,Ui_waitDialog):
    closeUpdataTimeThreadSignal = pyqtSignal()
    def __init__(self, parent,text=""):
        super(waittingDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setupUi(self)
        self.parent = parent
        self.init(text)

    def drawshadow(self,object, width, height):
        m = 9
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(m, m, width - m * 2, height - m * 2)

        painter = QPainter(object)
        # painter.drawLine(QLineF)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(Qt.white))

        color = QColor(100, 100, 100, 30)

        for i in range(m):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRoundedRect(m - i, m - i, width - (m - i) * 2, height - (m - i) * 2, 1, 1)
            color.setAlpha(90 - math.sqrt(i) * 30)
            painter.setPen(QPen(color, 1, Qt.SolidLine))
            painter.drawRoundedRect(QRect(m - i, m - i, width - (m - i) * 2, height - (m - i) * 2), 0, 0)

    def init(self,text):
        if text != "":
            self.waitMessageLabel.setText(text +",请稍等...(1s)")
        else:
            #原来默认的文字，不需要处理
            pass

        self.updataTimeThread = updataTimeThread(text,self.parent)
        self.updataTimeThread.updataTimeSignal.connect(self.refreshDialogText)
        self.closeUpdataTimeThreadSignal.connect(self.updataTimeThread.closeThread)
        self.updataTimeThread.start()




    def closeDialog(self):
        self.closeUpdataTimeThreadSignal.emit()
        self.accept()


    def refreshDialogText(self,text,iCount):
        if iCount > 1800:
            self.closeDialog()
        self.waitMessageLabel.setText("")
        if text == "":
            self.waitMessageLabel.setText("正在打开场景,请稍等...("+str(iCount) +"s)")
        else:
            self.waitMessageLabel.setText(text + ",请稍等...(" + str(iCount) + "s)")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                QApplication.postEvent(self, QEvent(174))
                event.accept()
            except Exception as err:
                pass

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            try:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()
            except Exception as err:
                pass


    def paintEvent(self, event):
        self.drawshadow(self,self.width(),self.height())




class updataTimeThread(QThread):
    updataTimeSignal = pyqtSignal(str,int)

    def __init__(self,text,parent=None):
        super(updataTimeThread, self).__init__(parent)
        self.parent = parent
        self.text = text
        self.bClose = False

    def run(self):
        try:
            import time
            iTime = 1
            while (1):
                if self.bClose == True:
                    return
                iTime = iTime + 1
                self.updataTimeSignal.emit(self.text,iTime)
                time.sleep(1)
        except Exception as err:
            print("updataTimeThread run error : "+str(err))


    def closeThread(self):
        self.bClose = True
