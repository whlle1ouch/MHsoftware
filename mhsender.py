from ui.sender import Ui_Form
from PyQt5.QtWidgets import QWidget


class SenderWindow(QWidget,Ui_Form):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = QWidget.__new__(cls)
        return cls._instance

    def __init__(self, mainwindow = None, parent=None):
        QWidget.__init__(self,parent)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.setEvent()

    def setEvent(self):
        self.pushButton_5.clicked.connect(self.on_clicked_pushButton_5)

    def on_clicked_pushButton_5(self):
        self.hide()
        self.mainwindow.showNormal()

