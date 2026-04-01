from ctypes.wintypes import DWORD, BYTE
from device_driver.device_init import Device
from device_driver.HCNetSDK import *
from ctypes import *
import ctypes

# 在调用DLL函数时，None、int、bytes、str是python中仅有的可直接作为函数参数的原生对象。当函数参数为NULL指针时，可以传递None为参数；当函数参数是一个包含数据的内存块指针（char*或wchar_t*）时，可以传递bytes或str为参数；当函数参数为系统平台默认int类型时，可以传递int为参数（为适应c数据类型其值将被部分屏蔽）。

device = Device()


class NET_DVR_LLI_PARAM(ctypes.Structure):
    """
    经纬度参数
    """
    _fields_ = [
        ("fSec", ctypes.c_float),  # 秒,[0.000000,60.000000]
        ("byDegree", ctypes.c_byte),  # 度:[0,90]纬度,[0,180]经度
        ("byMinute", ctypes.c_byte),  # 分,[0,59]
        ("byRes", ctypes.c_byte * 6)  # 保留字节
    ]


LPNET_DVR_LLI_PARAM = POINTER(NET_DVR_LLI_PARAM)


class NET_DVR_PTZPOS_PARAM(ctypes.Structure):
    """
    云台坐标参数
    """
    _fields_ = [
        ("fPanPos", ctypes.c_float),  # 水平角度,单位:度
        ("fTiltPos", ctypes.c_float),  # 垂直角度,单位:度
        ("fZoomPos", ctypes.c_float),  # 变焦值,单位:倍
        ("byRes", ctypes.c_byte * 16)  # 保留字节
    ]


LPNET_DVR_PTZPOS_PARAM = POINTER(NET_DVR_PTZPOS_PARAM)


class NET_DVR_SENSOR_PARAM(ctypes.Structure):
    """
    Sensor 参数
    """
    _fields_ = [
        ("bySensorType", ctypes.c_byte),  # Sensor 类型: 0-CCD, 1-CMOS
        ("byRes", ctypes.c_byte * 31),  # 保留字节
        ("fHorWidth", ctypes.c_float),  # 水平宽度,单位:cm * 10000
        ("fVerWidth", ctypes.c_float),  # 垂直宽度,单位:cm * 10000
        ("fFold", ctypes.c_float)  # 放大倍数,当 zoom=1 时的实际倍数 * 100
    ]


LPNET_DVR_SENSOR_PARAM = POINTER(NET_DVR_SENSOR_PARAM)


class NET_PTZ_INFO(ctypes.Structure):
    """
    云台信息
    """
    _fields_ = [
        ("fPan", ctypes.c_float),  # 水平角度,单位:度
        ("fTilt", ctypes.c_float),  # 垂直角度,单位:度
        ("fZoom", ctypes.c_float),  # 变焦值,单位:倍
        ("dwFocus", ctypes.c_ulong),  # 焦距,范围:0-100000,单位:未知
        ("byRes", ctypes.c_byte * 4)  # 保留字节
    ]


LPNET_PTZ_INFO = POINTER(NET_PTZ_INFO)


class NET_DVR_GIS_INFO(ctypes.Structure):
    """
    GIS 信息
    """
    _fields_ = [
        ("dwSize", ctypes.c_uint32),  # 结构体大小 c_long
        ("fAzimuth", ctypes.c_float),  # 方位角[0.00度,360.00度)
        ("fHorizontalValue", ctypes.c_float),  # 水平视场角
        ("fVerticalValue", ctypes.c_float),  # 垂直视场角
        ("fVisibleRadius", ctypes.c_float),  # 可见半径
        ("fMaxViewRadius", ctypes.c_float),  # 最大可视距离,0表示无限
        ("byLatitudeType", ctypes.c_byte),  # 纬度类型,0-度分秒,1-小数度
        ("byLongitudeType", ctypes.c_byte),  # 经度类型,0-度分秒,1-小数度
        ("byPTZPosExEnable", ctypes.c_byte),  # PTZ 位置信息标识,0~使用 struPtzPos,1~使用 struPtzPosEx
        ("byRes1", ctypes.c_byte),  # 保留字节
        ("struLatitude", NET_DVR_LLI_PARAM),  # 纬度
        ("struLongitude", NET_DVR_LLI_PARAM),  # 经度
        ("struPtzPos", NET_DVR_PTZPOS_PARAM),  # PTZ 位置
        ("struSensorParam", NET_DVR_SENSOR_PARAM),  # Sensor 参数
        ("struPtzPosEx", NET_PTZ_INFO),  # PTZ 扩展信息(当 byPTZPosExEnable 为 1 时使用)
        ("fMinHorizontalValue", ctypes.c_float),  # 水平视场角最小值(0.0-360.00)
        ("fMaxHorizontalValue", ctypes.c_float),  # 水平视场角最大值(0.0-360.00)
        ("fMinVerticalValue", ctypes.c_float),  # 垂直视场角最小值(0.0-360.00)
        ("fMaxVerticalValue", ctypes.c_float),  # 垂直视场角最大值(0.0-360.00)
        ("byRes", ctypes.c_byte * 220)  # 保留字节
    ]


LPNET_DVR_GIS_INFO = POINTER(NET_DVR_GIS_INFO)


class NET_DVR_STD_CONFIG(ctypes.Structure):
    _fields_ = [
        ("lpCondBuffer", ctypes.c_void_p),  # [in] 条件缓冲区(可选项),可以为NULL
        ("dwCondSize", ctypes.c_ulong),  # [in] lpCondBuffer 的大小
        ("lpInBuffer", ctypes.c_void_p),  # [in] 输入缓冲区(可选项),可以为NULL或非NULL
        ("dwInSize", ctypes.c_ulong),  # [in] lpInBuffer 的大小
        ("lpOutBuffer", ctypes.c_void_p),  # [out] 输出缓冲区(可选项),可以为NULL或非NULL
        ("dwOutSize", ctypes.c_ulong),  # [in] lpOutBuffer 的大小
        ("lpStatusBuffer", ctypes.c_void_p),  # [out] 状态缓冲区(XML格式),可以为NULL或非NULL
        ("dwStatusSize", ctypes.c_ulong),  # [in] lpStatusBuffer 的大小
        ("lpXmlBuffer", ctypes.c_void_p),  # [in/out] 当 byDataType = 1 时使用,xml 格式的数据
        ("dwXmlSize", ctypes.c_ulong),  # [in/out] lpXmlBuffer 的大小,可以在函数调用时修改实际的大小
        ("byDataType", ctypes.c_byte),  # [in] 数据类型/格式,0-使用 lpInBuffer/lpOutBuffer,1-使用 XML 格式 lpXmlBuffer
        ("byRes", ctypes.c_byte * 23)  # [in] 保留字节
    ]


LPNET_DVR_STD_CONFIG = POINTER(NET_DVR_STD_CONFIG)

iUserID = c_long(device.lUserID)


# 这个是寻找绝对坐标值的方法
def getGisInfo():
    # 创建 NET_DVR_STD_CONFIG 实例并设置其字段
    std_cfg = NET_DVR_STD_CONFIG()
    # std_cfg.dwSize = sizeof(std_cfg)
    lchannel = c_int(1)
    std_cfg.lpCondBuffer = cast(byref(lchannel), c_void_p)
    std_cfg.dwCondSize = sizeof(lchannel)

    # 创建 NET_DVR_GIS_INFO 实例并获取其指针
    gis_info = NET_DVR_GIS_INFO()
    gis_info.dwSize = ctypes.sizeof(gis_info)
    # gis_info.byPTZPosExEnable = 1
    # ptz_info = NET_PTZ_INFO()
    # gis_info.struPtzPosEx = ptz_info
    std_cfg.lpOutBuffer = cast(byref(gis_info), c_void_p)
    std_cfg.dwOutSize = sizeof(gis_info)
    lpBytesReturned = ctypes.c_uint32()

    # 调用 API 函数
    result = device.Objdll.NET_DVR_GetSTDConfig(iUserID, 3711, byref(std_cfg))

    if result is False:  # 假设错误码为非0值表示失败
        print(f"查询GIS信息失败，错误码：{device.Objdll.NET_DVR_GetLastError()}")
    else:
        print("查询GIS成功\n")
    # print(f"fLongitude: {gis_info.fHorizontalValue}")  # 这个可以 当前视场角
    # print(f"fLatitude: {gis_info.fVerticalValue}")  # 这个可以 当前视场角
    # 这个可以输出 PTZ坐标值
    print(f"fPanPos: {gis_info.struPtzPos.fPanPos}")
    print(f"fTiltPos: {gis_info.struPtzPos.fTiltPos}")
    print(f"fZoomPos: {gis_info.struPtzPos.fZoomPos}")
    viewing_angle_dict = {'x': gis_info.fHorizontalValue,
                          'y': gis_info.fVerticalValue}
    jiaoju = gis_info.struSensorParam.fFold  # 一倍焦距
    fHorWidth = gis_info.struSensorParam.fHorWidth  # 水平宽度
    fVerWidth = gis_info.struSensorParam.fVerWidth  # 垂直宽度
    bySensorType = gis_info.struSensorParam.bySensorType  # 传感器类型 0 ccd 1 cmos
    print(jiaoju)
    print(fHorWidth)
    print(fVerWidth)
    print(viewing_angle_dict)
    print(bySensorType)


# class NET_DVR_PTZPOS_PARAM(ctypes.Structure):
#     """
#     云台坐标参数
#     """
#     _fields_ = [
#         ("fPanPos", ctypes.c_float),  # 水平角度,单位:度
#         ("fTiltPos", ctypes.c_float),  # 垂直角度,单位:度
#         ("fZoomPos", ctypes.c_float),  # 变焦值,单位:倍
#         ("byRes", ctypes.c_byte * 16)  # 保留字节
#     ]
if __name__ == '__main__':
    getGisInfo()
