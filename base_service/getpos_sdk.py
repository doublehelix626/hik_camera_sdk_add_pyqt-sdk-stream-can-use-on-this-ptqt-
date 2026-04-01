from device_driver.device_init import Device
from device_driver.HCNetSDK import *


def HexToDecMa(x):
    # 十进制转换为十六进制
    x = int(hex(x)[2:].upper()) / 10
    return x


device = Device()


def pos_sdk():
    dw_returned = ctypes.c_uint16(0)
    # 创建一个PTZ的结构体
    ptzpos = NET_DVR_PTZPOS()

    res = device.Objdll.NET_DVR_GetDVRConfig(device.lUserID, NET_DVR_GET_PTZPOS, 1, byref(ptzpos), 255,
                                             byref(dw_returned))
    if not res:
        print('获取PTZ坐标信息失败')

    TempPosture = [0, 0, 0]
    TempPosture[0] = HexToDecMa(ptzpos.wPanPos)
    TempPosture[1] = HexToDecMa(ptzpos.wTiltPos)
    TempPosture[2] = HexToDecMa(ptzpos.wZoomPos)
    if TempPosture[1] > 90:
        TempPosture[1] = TempPosture[1] - 360
    print("此时P的角度为：" + str(TempPosture[0]))
    print("此时T的角度为：" + str(TempPosture[1]))
    print("此时Z的角度为：" + str(TempPosture[2]))
    return TempPosture


pos_sdk()
