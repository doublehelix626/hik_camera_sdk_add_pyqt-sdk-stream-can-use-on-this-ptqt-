from base_service.base_control_sdk import *
# from PyQt5.QtWidgets import QApplication

# from show_video_sdk import *
device = Device()
dw_returned = c_uint16(0)

"""下面是绑定方法的代码"""


# 可见光视频流变焦放大
def visible_zoomin_controller(visible_up):
    visible_up.pressed.connect(lambda: start_zoomin(device))
    visible_up.released.connect(lambda: stop_zoomin(device))


# 可见光视频流变焦缩小
def visible_zoomout_controller(visible_down):
    visible_down.pressed.connect(lambda: start_zoomout(device))
    visible_down.released.connect(lambda: stop_zoomout(device))


# 摄像头向上转动
def up_rotation_controller(up_rotation):
    up_rotation.pressed.connect(lambda: start_up(device))
    up_rotation.released.connect(lambda: stop_up(device))


# 摄像头向下转动
def down_rotation_controller(down_rotation):
    down_rotation.pressed.connect(lambda: start_down(device))
    down_rotation.released.connect(lambda: stop_down(device))


# 摄像头向左转动
def left_rotation_controller(left_rotation):
    left_rotation.pressed.connect(lambda: start_left(device))
    left_rotation.released.connect(lambda: stop_left(device))


# 摄像头向右转动
def right_rotation_controller(right_rotation):
    right_rotation.pressed.connect(lambda: start_right(device))
    right_rotation.released.connect(lambda: stop_right(device))


# if __name__ == '__main__':
#     class DrawPoints(QWidget):
#         def __init__(self, *args, **kwargs):
#             super(QWidget, self).__init__(*args, **kwargs)
#             # layout = QVBoxLayout()
#             # self.label = QLabel()
#             # layout.addWidget(self.label)
#             # self.setLayout(layout)
#             self.win = QWidget(self)
#             self.win.resize(720, 480)
#             self.win_count = int(self.win.winId())
#
#
#     app = QApplication(sys.argv)
#     win1 = DrawPoints()
#     # print(win1.win_count)
#     show_figure_to_label_service(device, win1.win_count)
#     win1.resize(1280, 720)
#     win1.show()
#     sys.exit(app.exec_())
