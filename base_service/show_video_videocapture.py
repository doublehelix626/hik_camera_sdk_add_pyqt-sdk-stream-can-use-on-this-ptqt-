import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from utils.QT_thread_pool import QT_ThreadPool
from utils.data import StreamManager

# from deffcode import FFdecoder
stream_manager = StreamManager()
sleep = QThread.msleep

"""
这里是通过推流法显示高山哨兵的图像，这里重点了解下，比较重要
"""


# 这个函数用于将来自视频流的帧显示在一个 GUI 标签上
def show_figure_to_label_service(stream_addr, fps, label):  # 要在ui_main_window.graph_view中显示视频流的视频帧
    # 打开视频流并初始化帧的显示
    visible_obj = stream_manager.open_stream(stream_addr)
    # decoder = FFdecoder("rtsp://admin:zmh123456@192.168.1.64:554").formulate()
    # visible_obj = decoder.generateFrame()
    for frame in visible_obj:
        # 检查帧是否不为空
        if frame is not None:
            # 将帧的颜色空间从BGR转换为RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


            # 对帧进行一些处理：调整大小
            frame = cv2.resize(frame, (720, 480))

            # 获取帧的高度、宽度和字节组件数
            height, width, bytesPerComponent = frame.shape

            center_x = width // 2
            center_y = height // 2
            cv2.circle(frame, (center_x, center_y), 1, (0, 255, 0), -1)
            # cv2.circle(frame, (347, 231), 1, (0, 255, 0), -1)
            # 计算每行像素所占的字节数
            bytesPerLine = bytesPerComponent * width

            # 将帧数据转换为 QImage 对象，并将其缩放以适应 GUI 标签的大小
            q_image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(label.width(),
                                                                                                   label.height())
            # 将 QImage 对象设置为 GUI 标签的图像
            label.setPixmap(QPixmap.fromImage(q_image))
            # 根据指定的帧率暂停一段时间
            # sleep(int(1000/fps))
