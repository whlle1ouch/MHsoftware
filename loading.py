from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,qApp,QSplashScreen
from PyQt5.QtGui import QPixmap
import time

class LoadingWindow(QWidget):   #创建用户界面的基类
    def __init__(self):
        super().__init__()
        self.initUI('image\loading.png')
        self.show()
        self.splash.finish(self)


    def initUI(self, img):
        print('starting program')
        self.splash = QSplashScreen(QPixmap(img)) #QSplashScreen是Qt提供一个一个载入界面程序
                                                  # QPixmap缩放图像，专门为图像在屏幕上的显示做了优化
        self.splash.showMessage('加载。。0%', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        self.splash.show()                         #显示控件
        qApp.processEvents()
        self.load_data()


    def load_data(self):
        for i in range(1,11):
            time.sleep(0.1)
            self.splash.showMessage("加载。。{0}%".format(i * 10), Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
            qApp.processEvents()



# def loading():
#     print('starting program')
#     splash = QSplashScreen(QPixmap())
#
#     splash.showMessage('加载。。0%', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
#     splash.show()
#     qApp.processEvents()
#     window1 = LoadingWindow()
#     window1.load_data(splash)
#     window1.show()
#     splash.finish(window1)