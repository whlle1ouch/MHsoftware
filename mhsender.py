from ui.sender import Ui_Form
from PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QHeaderView,QFileDialog,QMessageBox
from PyQt5.QtCore import Qt
import json,os,time
from excel import Excel,is_int


class SenderWindow(QWidget,Ui_Form):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = QWidget.__new__(cls)
        return cls._instance

    def __init__(self, mainwindow = None, parent=None):
        QWidget.__init__(self,parent)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.setWindowTitle('崔毛线')
        self.tableWidget = None
        self.loadSendor()
        self.setEvent()

    def setEvent(self):
        self.pushButton_4.clicked.connect(self.on_clicked_pushButton_4)
        self.pushButton.clicked.connect(self.on_clicked_pushButton)
        self.pushButton_2.clicked.connect(self.on_clicked_pushButton_2)
        self.pushButton_3.clicked.connect(self.on_clicked_pushButton_3)



    def on_clicked_pushButton(self):
        if self.tableWidget:
            if self.pushButton.text()== '修改':
                self.tableWidget.setEnabled(True)
                self.pushButton.setText('取消')
            elif self.pushButton.text()=='取消':
                self.tableWidget.setEnabled(False)
                self.pushButton.setText('修改')

    def on_clicked_pushButton_2(self):
        answer = QMessageBox.warning(self,'警告！','是否确认提交修改？\n  提交后将覆盖本地数据.',
                                     QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if answer ==QMessageBox.Yes:
            self.tableTextChange()
            self.gridLayout.removeWidget(self.tableWidget)
            self.addTable(self.senderList)
            if self.pushButton.text()=='取消':
                self.pushButton.setText('修改')
            self.tableWidget.setEnabled(False)

    def on_clicked_pushButton_3(self):
        if self.senderList:
            e = Excel()
            if self.senderList:
                colnum = len(self.senderList)
                for i in range(len(self.senderList)):
                    e.setRangeFormat('sheet1', 1, i + 1, colnum, i + 1, '@')
            if self.senderList:
                for i, row in enumerate(self.senderList):
                    for j, cell in enumerate(row):
                        e.setCell('sheet1', i + 1, j + 1, str(cell))
            desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
            savename = '发件人信息' + time.strftime('%m%d', time.localtime())
            savepath = desktop + '\\' + savename
            fname = QFileDialog.getSaveFileName(self, '保存', savepath, '.xlxs')
            fpath = os.path.abspath(fname[0])
            try:
                e.save(fpath)
            except Exception as e:
                self.showMsg('错误！', '保存时发生错误：\n {}'.format(e.args))
            finally:
                e.close()

        else:
            self.showMsg('错误！', '请先上传表格并完成转换。')


    def on_clicked_pushButton_4(self):
        self.hide()
        self.mainwindow.showNormal()

    def loadSendor(self):
        with open('data/sender.json','r',encoding='utf-8') as f:
            self.senderList = json.loads(f.read())
        self.addTable(self.senderList)

    def addTable(self, value):
        row = len(value)
        col = len(value[0])
        table = QTableWidget()
        table.setRowCount(row)
        table.setColumnCount(col)

        table.setHorizontalHeaderLabels(value[0])
        table.horizontalHeader().setEnabled(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        # table.setEnabled(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, row in enumerate(value[1:]):
            for j, cell in enumerate(row):
                newItem = QTableWidgetItem(str(cell))
                newItem.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, newItem)
        self.tableWidget = table
        self.tableWidget.setEnabled(False)
        self.gridLayout.addWidget(self.tableWidget)

    def tableTextChange(self):
        if self.tableWidget:
            row = self.tableWidget.rowCount()
            column = self.tableWidget.columnCount()
            newList = list()
            newList.append(self.senderList[0])
            for i in range(row):
                row = list()
                for j in range(column):
                    if self.tableWidget.item(i,j):
                        row.append(self.tableWidget.item(i,j).text())
                newList.append(row)
            self.senderList = newList
            self.save_to_local()

    def save_to_local(self):
        with open('data/sender.json','w',encoding='utf-8') as f:
            data = json.dumps(self.senderList)
            f.write(data)
    def showMsg(self , title , msg):
        return QMessageBox.information(self,title,msg)

    # def checkSenderList(self ,senderlist):
    #     if isinstance(senderlist,list):
    #         slist =  []
    #         for senderitem in senderlist:
    #             sl = [int(i) if is_int(i) else str(i) for i in senderitem]
    #             slist.append(sl)
    #         self.senderList = slist







