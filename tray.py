# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QSystemTrayIcon,QMenu,QAction,qApp,QWidget,QApplication
from PyQt5.QtGui import QIcon
import sys


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon,self).__init__(parent)
        self.showMenu()
        self.other()

    def showMenu(self):
        self.menu = QMenu()
        self.menu1 = QMenu()
        self.showAction1 = QAction('显示消息2',self,triggered=self.showM)
        self.showAction2 = QAction("显示消息2", self, triggered=self.showM)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu1.addAction(self.showAction1)
        self.menu1.addAction(self.showAction2)
        self.menu.addMenu(self.menu1,)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.menu1.setTitle("二级菜单")
        self.setContextMenu(self.menu)

    def other(self):
        self.activated.connect(self.iconClicked)
        self.messageClicked.connect(self.mClicked)
        self.setIcon(QIcon('icon/tray.icon'))
        self.icon = self.MessageIcon()

    def iconClicked(self, reason):
        if reason == 2 or reason ==3:
            pw = self.parent
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()
        print(reason)

    def mClicked(self):
        self.showMessage("提示", "你点了消息", self.icon)

    def showM(self):
        self.showMessage("测试", "我是消息", self.icon)

    def quit(self):
        self.setVisible(False)
        self.parent.exit()
        qApp.quit()
        sys.exit()

class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        ti = TrayIcon(self)
        ti.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())