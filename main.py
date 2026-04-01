import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from UI import test, ui_bundle_event
from device_driver.device_init import Device
import logging
import os

device = Device()


class Manager(QMainWindow):
    def __init__(self):
        super(Manager, self).__init__()
        # ui
        self.ui_interface = test.Ui_MainWindow()
        self.ui_interface.setupUi(self)  # 调用setupUi()方法，注册到QMainWindow对象
        # event
        ui_bundle_event.MainWindowBundleEvent(self.ui_interface)


if __name__ == '__main__':  ## 这个地方已经没问题了
    app = QtWidgets.QApplication(sys.argv)
    # mainWindow = QtWidgets.QMainWindow()
    # ui = test.Ui_MainWindow()
    # ui.setupUi(mainWindow)
    # ui_bundle_event.MainWindowBundleEvent(ui)
    mainWindow = Manager()
    time.sleep(0.2)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    time.sleep(0.2)

    time.sleep(0.2)
    mainWindow.show()
    sys.exit(app.exec_())
