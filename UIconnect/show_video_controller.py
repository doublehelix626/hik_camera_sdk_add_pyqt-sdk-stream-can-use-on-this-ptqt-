from base_service.show_video_videocapture import show_figure_to_label_service as cv_show
from base_service.screenshot_sdk import *
from utils.QT_thread_pool import QT_ThreadPool
from device_driver.device_init import Device
from ctypes import *

pool = QT_ThreadPool()
device = Device()
dw_returned = c_uint16(0)
stream_addr = "rtsp://admin:zmh123456@192.168.1.64:554"
fps = 30


def show_visible_controller_rtsp(video_view):
    # pool.submit("show_visible_sdk", sdk_show, number)
    pool.submit("show_visible_cv", cv_show, stream_addr, fps, video_view)



def show_screenshot(button, Label):
    button.clicked.connect(lambda: screenshot_whttest_true(device, Label))


def show_screenshot_false(button, Label):
    button.clicked.connect(lambda: screenshot_whttest_false(device, Label))
