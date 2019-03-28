# -*- coding: utf-8 -*-
from ui.mh import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog,QMessageBox,QMenu,QAction,QTextEdit
from PyQt5.QtGui import QIcon,QCursor
from excel import Excel
from product import translate,colFormat
import os,time
from PyQt5.QtCore import QBasicTimer,QThread,pyqtSignal,Qt,QPoint
from tray import TrayIcon


class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.step = 0
        self.timer = QBasicTimer()

        #数据处理
        self.data = None
        self.output = None

        self.setFixedSize(self.width(), self.height())   ##固定窗口大小
        self.setWindowIcon(QIcon('icon/mh.ico'))   #设置系统图标

        #创建右键
        # self.window.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.window.customContextMenuRequested.connect(self.createRightMenu)
        # self.createContextMenu()

        #显示托盘
        self.setTray()
        self.setEvent()
        self.show()


    def setTray(self):
        self.tray = TrayIcon(self)
        self.tray.show()


    def setEvent(self):
        self.pushButton_3.clicked.connect(self.on_clicked_pushButton_3)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.showNormal()


    def changeEvent(self, *args, **kwargs):
        if self.isMinimized():
            self.hide()
        if self.isMaximized():
            self.show()


    def on_clicked_pushButton_3(self):
        desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
        fname = QFileDialog.getOpenFileName(self.centralwidget , '打开', desktop)
        if fname[0]:
            fpath = os.path.abspath(fname[0])
            if (not fpath.endswith('.xls')) and (not fpath.endswith('.xlsx')):
                self.showMsg('错误!' , '请上xls或者xlsx文件')
                return
            e = Excel(fpath)
            try:
                self.data = e.getContiguousRange('订单表', 1, 1)
                self.data = e.fixStringsAndDates(self.data)
            except Exception as e:
                self.showMsg('错误！','发生错误：\n {}'.format(e.args[:]))
            finally:
                e.close()



    def on_clicked_pushButton_2(self):
        if self.data:
            self.pushButton_2.setEnabled(False)
            if self.timer.isActive():
                self.timer.stop()
                self.step = 0
            self.timer.start(100,self.centralwidget)
            self.prb = WorkTheread()
            self.prb.qsignal.connect(self.timeEnd)
            try:
                self.prb.start()
                self.output = translate(self.data)
            except Exception as e:
                self.showMsg('错误','发生错误：\n {}'.format(e.args[0]))
            else:
                self.showMsg('成功！','已转换完成')
                self.pushButton_2.setEnabled(True)
                self.step = 100
        else:
            self.showMsg('错误！', '请先上传数据')
            self.pushButton_2.setEnabled(True)
            self.step = 0

    def timeEnd(self):
        self.timer.stop()
        self.step = 100
        self.progressBar.setProperty("value", self.step)


    def timerEvent(self, *args, **kwargs):
        self.progressBar.setProperty("value", self.step)
        if self.step >=100:
            self.timer.stop()
        if self.step<99:
            self.step += 1

    def on_clicked_pushButton(self):
        if self.output:
            e = Excel()
            rownum = len(self.output)
            formats = colFormat()
            for i in range(len(formats)):
                e.setRangeFormat('sheet1',2,i+1,rownum,i+1,formats[i])
            e.setRange('sheet1',1,1,self.output)
            desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
            savename = '一品周报'+time.strftime('%m%d',time.localtime())
            savepath = desktop+'\\'+savename
            fname = QFileDialog.getSaveFileName(self,'保存', savepath ,'.xlxs')
            fpath = os.path.abspath(fname[0])
            try:
                e.save(fpath)
            except Exception as e:
                self.showMsg('错误！','发生错误：\n {}'.format(e.args[0]))
            finally:
                e.close()

        else:
            self.showMsg('错误！','请先上传表格并完成转换。')


    def showMsg(self , title , msg):
        return QMessageBox.information(self.centralwidget,title,msg)








class WorkTheread(QThread):
    qsignal = pyqtSignal()
    def __init__(self,parent = None):
        super().__init__(parent)
        self.work = True

    def __del__(self):
        self.work = False
        self.wait()

    def run(self):
        self.qsignal.emit()

