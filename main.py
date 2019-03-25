import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from loading import LoadingWindow

if __name__ == '__main__':
    app = 0 ##防止内核崩溃
    app = QApplication(sys.argv)
    LoadingWindow()
    w = MainWindow()
    sys.exit(app.exec_())

