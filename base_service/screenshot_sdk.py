import time

from device_driver.device_init import Device
from device_driver.HCNetSDK import *
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from utils.QT_thread_pool import QT_ThreadPool
import cv2
import logging
from utils.absoute_sdk_utils import *
import os

pool = QT_ThreadPool()


# device = Device()


def screenshot(device, Label):
    # print("我进到截图里了")
    # logging.info("我进到截图里了")
    image_data = NET_DVR_JPEGPARA()
    image_data.wPicSize = 0xff
    image_data.wPicQuality = 0
    image_data_pointer = LPNET_DVR_JPEGPARA(image_data)
    # image_data_pointer = byref(image_data) # byref的作用在于，获取ctypes定义的变量的指针/地址
    now = datetime.datetime.now()
    file_name = now.strftime("%Y%m%d_%H%M%S")
    sJpegPicFileName = bytes(f"D:\\pycharm\\ptzagent\\image_cache\\{file_name}.jpg", "ascii")  # 这个地方可以为utf-8 也可以为ascii
    let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                   sJpegPicFileName)
    # if not device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1),
    #                                                 image_data_pointer, sJpegPicFileName):
    #     print(f"Error: {device.Objdll.NET_DVR_GetLastError()}")
    # pool.submit("截图", device.Objdll.NET_DVR_CaptureJPEGPicture, c_long(device.lUserID), c_long(1), image_data_pointer,
    #             sJpegPicFileName)
    raw_image_path = f"D:\\pycharm\\ptzagent\\image_cache\\{file_name}.jpg"
    image = cv2.imread(raw_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (720, 480))
    height, width, bytesPerComponent = resized_image.shape
    bytesPerLine = bytesPerComponent * width
    q_image = QImage(resized_image.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(Label.width(),
                                                                                                   Label.height())
    Label.setPixmap(QPixmap.fromImage(q_image))
    # cv2.imwrite(raw_image_path, resized_image)
    logging.info("截图成功！")
    return raw_image_path


def screenshot_raw(device):
    H = 360
    L = 640
    # print("我进到截图里了")
    # logging.info("我进到截图里了")
    image_data = NET_DVR_JPEGPARA()
    image_data.wPicSize = 0xff
    image_data.wPicQuality = 0
    image_data_pointer = LPNET_DVR_JPEGPARA(image_data)
    # image_data_pointer = byref(image_data) # byref的作用在于，获取ctypes定义的变量的指针/地址
    now = datetime.datetime.now()
    file_name = now.strftime("%Y%m%d_%H%M%S")
    sJpegPicFileName = bytes(f"D:\\pycharm\\ptzagent\\image_cache\\{file_name}.jpg", "ascii")  # 这个地方可以为utf-8 也可以为ascii
    let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                   sJpegPicFileName)
    # if not device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1),
    #                                                 image_data_pointer, sJpegPicFileName):
    #     print(f"Error: {device.Objdll.NET_DVR_GetLastError()}")
    # pool.submit("截图", device.Objdll.NET_DVR_CaptureJPEGPicture, c_long(device.lUserID), c_long(1), image_data_pointer,
    #             sJpegPicFileName)
    raw_image_path = f"D:\\pycharm\\ptzagent\\image_cache\\{file_name}.jpg"
    image = cv2.imread(raw_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (L, H))  # 存疑
    cv2.imwrite(raw_image_path, resized_image)
    logging.info("截图成功！")
    return raw_image_path


def screenshot_whttest_true(device, Label):
    # print("我进到截图里了")
    # logging.info("我进到截图里了")
    save_dir = "D:\\pycharm\\ptzagent\\data_whttest\\group1"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    txt_path = os.path.join(save_dir, "log.txt")
    image_data = NET_DVR_JPEGPARA()
    image_data.wPicSize = 0xff
    image_data.wPicQuality = 0
    image_data_pointer = LPNET_DVR_JPEGPARA(image_data)
    index = 1
    while True:
        filename = f"{index:03d}.jpg"  # 生成 001.jpg, 002.jpg 等文件名
        filepath = os.path.join(save_dir, filename)
        if not os.path.exists(filepath):
            break  # 如果文件不存在，找到目标文件名
        index += 1
    if index == 1:
        filename_zero = f"{index - 1:03d}.jpg"
        filepath_zero = os.path.join(save_dir, filename_zero)
        sJpegPicFileName = bytes(filepath_zero, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos_zero = getGisInfo_ptz()
        pos_zero.append(1)
        print("打印txt")
        print(pos_zero)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos_zero}\n")
        sJpegPicFileName = bytes(filepath, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos = getGisInfo_ptz()
        pos.append(1)
        print("打印txt")
        print(pos)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos}\n")
    else:
        file_name = filepath
        sJpegPicFileName = bytes(file_name, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos = getGisInfo_ptz()
        pos.append(1)
        print("打印txt")
        print(pos)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos}\n")
    raw_image_path = filepath
    image = cv2.imread(raw_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (720, 480))
    height, width, bytesPerComponent = resized_image.shape
    bytesPerLine = bytesPerComponent * width
    q_image = QImage(resized_image.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(Label.width(),
                                                                                                   Label.height())
    Label.setPixmap(QPixmap.fromImage(q_image))
    # cv2.imwrite(raw_image_path, resized_image)
    logging.info("截图成功！")
    return raw_image_path


def screenshot_whttest_false(device, Label):
    # print("我进到截图里了")
    # logging.info("我进到截图里了")
    save_dir = "D:\\pycharm\\ptzagent\\data_whttest\\group1"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    txt_path = os.path.join(save_dir, "log.txt")
    image_data = NET_DVR_JPEGPARA()
    image_data.wPicSize = 0xff
    image_data.wPicQuality = 0
    image_data_pointer = LPNET_DVR_JPEGPARA(image_data)
    index = 1
    while True:
        filename = f"{index:03d}.jpg"  # 生成 001.jpg, 002.jpg 等文件名
        filepath = os.path.join(save_dir, filename)
        if not os.path.exists(filepath):
            break  # 如果文件不存在，找到目标文件名
        index += 1
    if index == 1:
        filename_zero = f"{index - 1:03d}.jpg"
        filepath_zero = os.path.join(save_dir, filename_zero)
        sJpegPicFileName = bytes(filepath_zero, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos_zero = getGisInfo_ptz()
        pos_zero.append(0)
        print("打印txt")
        print(pos_zero)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos_zero}\n")
        sJpegPicFileName = bytes(filepath, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos = getGisInfo_ptz()
        pos.append(0)
        print("打印txt")
        print(pos)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos}\n")
    else:
        file_name = filepath
        sJpegPicFileName = bytes(file_name, "ascii")  # 这个地方可以为utf-8 也可以为ascii
        let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
                                                       sJpegPicFileName)
        pos = getGisInfo_ptz()
        pos.append(0)
        print("打印txt")
        print(pos)
        with open(txt_path, "a") as txt_file:
            txt_file.write(f"{pos}\n")
    raw_image_path = filepath
    image = cv2.imread(raw_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (720, 480))
    height, width, bytesPerComponent = resized_image.shape
    bytesPerLine = bytesPerComponent * width
    q_image = QImage(resized_image.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(Label.width(),
                                                                                                   Label.height())
    Label.setPixmap(QPixmap.fromImage(q_image))
    # cv2.imwrite(raw_image_path, resized_image)
    logging.info("截图成功！")
    return raw_image_path


# def screenshot_whttest_false(device, Label):
#     # print("我进到截图里了")
#     # logging.info("我进到截图里了")
#     save_dir = "D:\\pycharm\\ptzagent\\data_whttest\\group1"
#     txt_path = os.path.join(save_dir, "log.txt")
#     image_data = NET_DVR_JPEGPARA()
#     image_data.wPicSize = 0xff
#     image_data.wPicQuality = 0
#     image_data_pointer = LPNET_DVR_JPEGPARA(image_data)
#     index = 1
#     while True:
#         filename = f"{index:03d}.jpg"  # 生成 001.jpg, 002.jpg 等文件名
#         filepath = os.path.join(save_dir, filename)
#         if not os.path.exists(filepath):
#             break  # 如果文件不存在，找到目标文件名
#         index += 1
#     file_name = filepath
#     sJpegPicFileName = bytes(file_name, "ascii")  # 这个地方可以为utf-8 也可以为ascii
#     let = device.Objdll.NET_DVR_CaptureJPEGPicture(c_long(device.lUserID), c_long(1), image_data_pointer,
#                                                    sJpegPicFileName)
#     pos = getGisInfo_ptz()
#     pos_flag = pos.append(0)
#     print("打印txt")
#     print(pos)
#     with open(txt_path, "a") as txt_file:
#         txt_file.write(f"{pos}\n")
#     raw_image_path = filepath
#     image = cv2.imread(raw_image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     resized_image = cv2.resize(image, (720, 480))
#     height, width, bytesPerComponent = resized_image.shape
#     bytesPerLine = bytesPerComponent * width
#     q_image = QImage(resized_image.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(Label.width(),
#                                                                                                    Label.height())
#     Label.setPixmap(QPixmap.fromImage(q_image))
#     # cv2.imwrite(raw_image_path, resized_image)
#     logging.info("截图成功！")
#     return raw_image_path




# if __name__ == '__main__':
# screenshot(device)
