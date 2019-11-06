# -*- coding: utf-8 -*-
import os
import time

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal,Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QMenu, QAction \
    , QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,QApplication

from excel import Excel
from mhsender import SenderWindow
from product import transform,translate
from tray import TrayIcon
from ui.mh import Ui_MainWindow
import win32timezone


class MainWindow(QMainWindow,Ui_MainWindow):


    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.step = 0
        self.timer = QBasicTimer()
        self.tableWidget = None

        #数据处理
        self.data = None
        self.output = None
        self.outformat = None

        #主窗体
        self.setFixedSize(self.width(), self.height())   ##固定窗口大小
        self.setWindowTitle('Magic&House SoftWare')
        self.setWindowIcon(QIcon('image/mh.ico'))   #设置系统图标

        #其他窗体
        self.senderwindow = SenderWindow(mainwindow=self)

        #显示托盘
        self.setTray()
        self.setEvent()
        self.show()


    def contextMenuEvent(self, event):
        menu = QMenu(self)

        action1 = QAction('上传' , self , triggered=self.on_clicked_pushButton_3)
        action2 = QAction('转化' , self , triggered=self.on_clicked_pushButton_2)
        menu.addAction(action1)
        menu.addAction(action2)
        action = menu.exec_(self.mapToGlobal(event.pos()))


    def setTray(self):
        self.tray = TrayIcon(self)
        self.tray.show()


    def setEvent(self):
        self.pushButton_3.clicked.connect(self.on_clicked_pushButton_3)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_5.clicked.connect(self.on_clicked_pushButton_5)
        self.pushButton_6.clicked.connect(self.on_clicked_pushButton_6)
        self.pushButton_7.clicked.connect(self.on_clicked_pushButton_7)
        self.menu_4.triggered.connect(self.on_clicked_menu_4)
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
                self.showMsg('错误!' , '请上传xls或者xlsx文件')
                return
            e = Excel(fpath)
            try:
                self.data = e.getContiguousRange('订单表', 1, 1)
                self.data = e.fixStringsAndDates(self.data)
            except Exception as e:
                self.showMsg('错误！','发生错误：\n {}'.format(e.args))
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
                transFunction = self.getTransFunction()
                self.output,self.outformat = transFunction(self.data)
            except Exception as e:
                self.showMsg('错误','转换时发生错误：\n {}'.format(e.args))
            else:
                self.showMsg('成功！','已转换完成')
                if self.tableWidget:
                    self.gridLayout.removeWidget(self.tableWidget)
                self.addTable(self.output)
                self.step = 100
            self.pushButton_2.setEnabled(True)
            self.step = 0
            self.progressBar.setValue(self.step)
        else:
            self.showMsg('错误！', '请先上传数据')
            self.pushButton_2.setEnabled(True)
            self.step = 0
    def on_clicked_pushButton_5(self):
        if not self.tableWidget:
            return
        if self.pushButton_5.text() =='修改':
            if self.tableWidget:
                self.tableWidget.setEnabled(True)
                self.pushButton_5.setText('提交')
                self.pushButton_7.setEnabled(True)
        elif self.pushButton_5.text() == '提交':
            answer = QMessageBox.warning(self.centralwidget, '注意！', '是否确认提交修改数据？\n  提交后数据将无法恢复。',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.tableTextChange()
                self.pushButton_5.setText('修改')
                self.tableWidget.setEnabled(False)


    def on_clicked_pushButton(self):
        if self.output:
            e = Excel()
            if self.outformat:
                colnum = len(self.output)
                for i in range(len(self.outformat)):
                    e.setRangeFormat('sheet1',2,i+1,colnum,i+1,self.outformat[i])
            if self.output:
                for i,row in enumerate(self.output):
                    for j,cell in enumerate(row):
                        if isinstance(cell,dict):
                            e.setCell('sheet1',i+1,j+1,cell.get('value',''))
                        elif isinstance(cell,str):
                            e.setCell('sheet1', i+1, j+1, cell)
            desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
            savename = time.strftime('%m%d',time.localtime())
            savepath = desktop+'\\'+savename
            save_select = QFileDialog.getSaveFileName(self,'保存', savepath ,'.xlsx')
            if save_select[0]=='':
                return
            fpath = os.path.abspath(save_select[0])
            if os.path.exists(savepath+'.xlsx'):
                answer = QMessageBox.warning(self.centralwidget,'警告！','{}.xlsx 已经存在于当前目录下，是否覆盖？'.format(savepath),
                                             QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
                if answer == QMessageBox.No:
                    return
            try:
                e.save(fpath)
            except Exception as e:
                self.showMsg('错误！','保存时发生错误：\n {}'.format(e.args))
            finally:
                e.close()

        else:
            self.showMsg('错误！','请先上传表格并完成转换。')

    def on_clicked_pushButton_6(self):
        self.senderwindow.show()

    def on_clicked_pushButton_7(self):
        if self.pushButton_5.text() == '修改':
            self.pushButton_7.setEnabled(False)
        else:
            self.pushButton_5.setText('修改')
            self.gridLayout.removeWidget(self.tableWidget)
            self.addTable(self.output)
            self.pushButton_7.setEnabled(False)

    def on_clicked_menu_4(self):
        with open('data/version.txt','r',encoding='utf-8') as f:
            self.showMsg('版本号',f.read())


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


    def addTable(self, value):
        row = len(value)
        col = len(value[0])
        self.comboBoxList = list()

        table = QTableWidget()
        table.setRowCount(row)
        table.setColumnCount(col)
        table.setHorizontalHeaderLabels(value[0])
        table.horizontalHeader().setEnabled(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table.verticalHeader().hide()
        for i,row in enumerate(value[1:]):
            for j,cell in enumerate(row):
                if isinstance(cell,dict):
                    if not cell.get('select',False):
                        newItem = QTableWidgetItem(cell.get('value',''))
                        newItem.setTextAlignment(Qt.AlignHCenter)
                        newItem.setTextAlignment(Qt.AlignCenter)
                        table.setItem(i,j,newItem)
                    elif not cell.get('corresponding',False):
                        newItem = QComboBox()
                        newItem.setAcceptDrops(True)
                        newItem.setStyleSheet('margin:0;padding:0;border:0.5pxbackground-color:white;text-align:center;vertical-align:middle;')
                        newItem.setSizeAdjustPolicy(QComboBox.AdjustToContents)
                        newItem.addItem(cell.get('value',''))
                        for sender in self.senderwindow.senderList[1:]:
                            newItem.addItem(str(sender[0]))
                        table.setCellWidget(i, j, newItem)
                        table.cellWidget(i,j).currentTextChanged.connect(self.tableComboBoxChange)
                        self.comboBoxList.append(newItem)
                    else:
                        newItem = QLineEdit()
                        newItem.setStyleSheet('margin:0;padding:0;border:0.5px;text-align:center;background-color:white;vertical-align:middle;')
                        newItem.setText(cell.get('value',''))
                        table.setCellWidget(i, j, newItem)
                elif isinstance(cell,str):
                    newItem = QTableWidgetItem(cell)
                    newItem.setTextAlignment(Qt.AlignHCenter)
                    newItem.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, j, newItem)
                QApplication.processEvents()
        table.setEnabled(False)
        self.tableWidget = table
        self.gridLayout.addWidget(self.tableWidget)


    def tableTextChange(self):
        if self.tableWidget:
            row = self.tableWidget.rowCount()
            column = self.tableWidget.columnCount()
            output = list()
            output.append(self.output[0])
            for i in range(row):
                outrow = list()
                for j in range(column):
                    if self.tableWidget.item(i,j):
                        outrow.append(self.tableWidget.item(i,j).text())
                    if self.tableWidget.cellWidget(i,j):
                        widget = self.tableWidget.cellWidget(i,j)
                        if isinstance(widget,QLineEdit):
                            outrow.append(widget.text())
                        elif isinstance(widget,QComboBox):
                            outrow.append(widget.currentText())

                output.append(outrow)
            self.output = output
    def tableComboBoxChange(self):
        if self.sender() in self.comboBoxList:
            row =self.comboBoxList.index(self.sender())
            col = 1
            if self.tableWidget:
                if isinstance(self.sender(),QComboBox):
                    sender = self.sender().currentText()
                    if isinstance(self.tableWidget.cellWidget(row,col+1),QLineEdit):
                        sender_phone = self.findSender(sender)
                        self.tableWidget.cellWidget(row, col + 1).setText(str(sender_phone))

    def getTransFunction(self):
        if self.comboBox.currentText() == '模板1':
            return transform
        elif self.comboBox.currentText() == '模板2':
            return translate

    def findSender(self, sender):
        sender_phone=''
        for senders in self.senderwindow.senderList[1:]:
            if sender == str(senders[0]):
                sender_phone = senders[1]
        return sender_phone

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

