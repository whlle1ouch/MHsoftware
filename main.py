import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from loading import LoadingWindow
from PyQt5.QtNetwork import QLocalSocket,QLocalServer



if __name__ == '__main__':
    try:
        app = 0 ##防止内核崩溃
        app = QApplication(sys.argv)
        serverName = 'MhProcess'
        socket = QLocalSocket()
        socket.connectToServer(serverName)
        if socket.waitForConnected(500):
            app.quit()
        else:
            localServer = QLocalServer()
            localServer.listen(serverName)
            LoadingWindow()
            mhaind = MainWindow()

        sys.exit(app.exec_())
    except:
        pass

