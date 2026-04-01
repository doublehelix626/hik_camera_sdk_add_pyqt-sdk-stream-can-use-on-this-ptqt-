# 登录的设备信息
import ctypes
import os
from ctypes import create_string_buffer, byref
from device_driver.HCNetSDK import NET_DVR_LOCAL_SDK_PATH, NET_DVR_DEVICEINFO_V30, NET_DVR_PTZPOS

DEV_IP = create_string_buffer(b'192.168.1.64')
DEV_PORT = 8000
DEV_USER_NAME = create_string_buffer(b'admin')
DEV_PASSWORD = create_string_buffer(b'zmh123456')
PlayCtrl_Port = ctypes.c_long(-1)


# 设置SDK初始化依赖库路径
def SetSDKInitCfg(obj_dll, str_path):
    # 设置HCNetSDKCom组件库和SSL库加载路径
    str_path = str_path.encode('gbk')
    sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
    sdk_ComPath.sPath = str_path
    obj_dll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
    obj_dll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(str_path + b'\libcrypto-1_1-x64.dll'))
    obj_dll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(str_path + b'\libssl-1_1-x64.dll'))


def LoginDev(obj_dll):
    # 登录注册设备
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = obj_dll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    return lUserId, device_info


## 记得里面的路径要改成你们自己的路径，里面有一些结构定义直接照着我的写就行，比如NET_DVR_PTZPOS()这个数据结构，没必要去深究
class Device:
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, lib_path="./device_driver/lib/win"):
        if self.__first_init:
            self.Objdll = ctypes.CDLL(os.path.join(lib_path, 'HCNetSDK.dll'))  # 加载网络库
            # if not os.path.exists(os.path.join(lib_path, 'IRSThermalCameraSDK_Demo/x64/Release'
            #                                              '/IRSThermalCameraSDK_Demo.dll')):
            #     raise Exception("lib missing, please check")
            # self.Objdll2 = ctypes.CDLL(os.path.join(lib_path, r'IRSThermalCameraSDK_Demo/x64/Release'
            #                                                   r'/IRSThermalCameraSDK_Demo.dll'))
            self.Playctrldll = ctypes.CDLL(os.path.join(lib_path, 'PlayCtrl.dll'))
            SetSDKInitCfg(self.Objdll, lib_path)  # 设置组件库和SSL库加载路径
            # 启用SDK写日志w
            self.Objdll.NET_DVR_Init()
            self.dw_returned = ctypes.c_uint16(0)
            self.ptzpos = NET_DVR_PTZPOS()
            self.Objdll.NET_DVR_SetLogToFile(3,
                                             bytes(str(os.path.join(lib_path, "SdkLog_Python")), encoding="utf-8"),
                                             False)
            # if not self.Playctrldll.PlayM4_GetPort(byref(PlayCtrl_Port)):
            #     print(u'获取播放库句柄失败')
            self.lUserID, _ = LoginDev(self.Objdll)
            if self.lUserID == -1:
                raise Exception("login device failure")
        self.__first_init = False
