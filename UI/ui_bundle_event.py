import time

from UIconnect.device_driver_controller import *
from UIconnect.show_video_controller import *


"""
这是接口代码，定义了不同任务和控制
摄像头有两个
"""


class MainWindowBundleEvent:
    def __init__(self, ui_main_window):
        show_visible_controller_rtsp(ui_main_window.graph_view_2)
        # 截图按钮功能
        show_screenshot(ui_main_window.pushButton_screenshot, ui_main_window.graph_view)
        # 视频流变焦放大
        visible_zoomin_controller(ui_main_window.pushButton_ZoomIn)
        # 视频流变焦缩小
        visible_zoomout_controller(ui_main_window.pushButton_ZoomOut)
        # 摄像头向上转动
        up_rotation_controller(ui_main_window.pushButton_Up)
        # 摄像头向下转动
        down_rotation_controller(ui_main_window.pushButton_Down)
        # 摄像头向左转动
        left_rotation_controller(ui_main_window.pushButton_Left)
        # 摄像头向右转动
        right_rotation_controller(ui_main_window.pushButton_Right)
