import numpy as np
from base_service import getpos_sdk
from ctypes.wintypes import DWORD, BYTE
from device_driver.device_init import Device
from device_driver.HCNetSDK import *
from ctypes import *
import ctypes
from base_service.getpos_onvif import *
import math

# 在调用DLL函数时，None、int、bytes、str是python中仅有的可直接作为函数参数的原生对象。当函数参数为NULL指针时，可以传递None为参数；当函数参数是一个包含数据的内存块指针（char*或wchar_t*）时，可以传递bytes或str为参数；当函数参数为系统平台默认int类型时，可以传递int为参数（为适应c数据类型其值将被部分屏蔽）。

device = Device()


def round_half_up(value, decimals=1):
    multiplier = 10 ** decimals
    return int(value * multiplier + 0.5) / multiplier




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
        ("dwSize", ctypes.c_ulong),  # 结构体大小
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

# # 设置 NET_DVR_GetSTDConfig 的参数
# gis_info = NET_DVR_GIS_INFO()
# gis_info.dwSize = ctypes.sizeof(gis_info)
# get_STD_info = NET_DVR_STD_CONFIG()
# # get_STD_info.lpOutBuffer = byref(gis_info)
# get_STD_info.lpOutBuffer = ctypes.cast(ctypes.pointer(gis_info), ctypes.c_void_p)
# get_STD_info.dwOutSize = ctypes.sizeof(gis_info)
# get_STD_info.lpCondBuffer = ctypes.c_void_p(1)
# get_STD_info.dwCondSize = 4
# lpBytesReturned = ctypes.c_uint32()
#
# # 调用 NET_DVR_GetSTDConfig 函数
# if not device.Objdll.NET_DVR_GetSTDConfig(c_long(device.lUserID), 3711, 0, get_STD_info, sizeof(get_STD_info),
#                                           ctypes.byref(lpBytesReturned)):
#     print(f"Error: {device.Objdll.NET_DVR_GetLastError()}")
# else:
#     # 获取到 gis_info 结构体中的数据
#     print(f"fLongitude: {gis_info.fHorizontalValue}")
#     print(f"fLatitude: {gis_info.fVerticalValue}")
iUserID = c_long(device.lUserID)


# 这个是寻找绝对坐标值的方法,这个没问题
def getGisInfo():
    # 创建 NET_DVR_STD_CONFIG 实例并设置其字段
    std_cfg = NET_DVR_STD_CONFIG()
    std_cfg.dwSize = sizeof(std_cfg)
    lchannel = c_int(1)
    std_cfg.lpCondBuffer = cast(byref(lchannel), c_void_p)
    std_cfg.dwCondSize = sizeof(lchannel)

    # 创建 NET_DVR_GIS_INFO 实例并获取其指针
    gis_info = NET_DVR_GIS_INFO()
    std_cfg.lpOutBuffer = cast(byref(gis_info), c_void_p)
    std_cfg.dwOutSize = sizeof(gis_info)

    # 调用 API 函数
    result = device.Objdll.NET_DVR_GetSTDConfig(iUserID, 3711, byref(std_cfg))

    if result is False:  # 假设错误码为非0值表示失败
        print(f"查询GIS信息失败，错误码：{device.Objdll.NET_DVR_GetLastError()}")
    else:
        print("查询GIS成功\n")
    # print(f"fLongitude: {gis_info.fHorizontalValue}")  # 这个可以 当前视场角
    # print(f"fLatitude: {gis_info.fVerticalValue}")  # 这个可以 当前视场角
    # print(f"fLatitude: {gis_info.struPtzPos.fPanPos}")  # 这个可以输出 PTZ坐标值
    fHorizontalValue = round(gis_info.fHorizontalValue, 2)
    fVerticalValue = round(gis_info.fVerticalValue, 2)
    viewing_angle_dict = {'x': fHorizontalValue,
                          'y': fVerticalValue}
    return viewing_angle_dict


def getGisInfo_ptz():
    # 创建 NET_DVR_STD_CONFIG 实例并设置其字段
    std_cfg = NET_DVR_STD_CONFIG()
    std_cfg.dwSize = sizeof(std_cfg)
    lchannel = c_int(1)
    std_cfg.lpCondBuffer = cast(byref(lchannel), c_void_p)
    std_cfg.dwCondSize = sizeof(lchannel)

    # 创建 NET_DVR_GIS_INFO 实例并获取其指针
    gis_info = NET_DVR_GIS_INFO()
    std_cfg.lpOutBuffer = cast(byref(gis_info), c_void_p)
    std_cfg.dwOutSize = sizeof(gis_info)

    # 调用 API 函数
    result = device.Objdll.NET_DVR_GetSTDConfig(iUserID, 3711, byref(std_cfg))

    if result is False:  # 假设错误码为非0值表示失败
        print(f"查询GIS信息失败，错误码：{device.Objdll.NET_DVR_GetLastError()}")
    else:
        print("查询GIS成功\n")
    # print(f"fLongitude: {gis_info.fHorizontalValue}")  # 这个可以 当前视场角
    # print(f"fLatitude: {gis_info.fVerticalValue}")  # 这个可以 当前视场角
    # print(f"fLatitude: {gis_info.struPtzPos.fPanPos}")  # 这个可以输出 PTZ坐标值
    pos = [gis_info.struPtzPos.fPanPos, gis_info.struPtzPos.fTiltPos, gis_info.struPtzPos.fZoomPos]
    pos_rounded = [round(value, 1) for value in pos]
    print("原坐标值")
    print(pos)
    print("现坐标值")
    print(pos_rounded)
    return pos_rounded


def absoute_coordinate(result_dict):
    viewing_angle_dict = getGisInfo()
    print(viewing_angle_dict)
    pos_now = getGisInfo_ptz()
    absoute_coordinate_dict = {}
    bound_coordinate_dict = {}
    pos_object = []
    H = 360
    L = 640
    for key, value in result_dict.items():
        absoute_coordinate_temp_list = []
        bound_coordinate_temp_list = []
        for i in range(len(value)):
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            x0 = ((x0 * L) / 1000)
            y0 = ((y0 * H) / 1000)
            x1 = ((x1 * L) / 1000)
            y1 = ((y1 * H) / 1000)
            length = x1 - x0
            height = y1 - y0
            center_coordinate = [((x0 + x1) / 2), ((y0 + y1) / 2)]
            print("what center")
            print(center_coordinate)
            if center_coordinate[0] > (L / 2):
                delt_x = np.rad2deg(np.arctan(
                    (center_coordinate[0] - L / 2) / (L / 2) * np.tan(np.deg2rad(viewing_angle_dict['x'] / 2))))
                pos_object.append((pos_now[0] - delt_x))
            else:
                delt_x = np.rad2deg(
                    np.arctan(
                        (L / 2 - center_coordinate[0]) / (L / 2) * np.tan(np.deg2rad(viewing_angle_dict['x'] / 2))))
                pos_object.append((pos_now[0] + delt_x))
            if center_coordinate[1] > (H / 2):
                delt_y = np.rad2deg(
                    np.arctan(
                        (center_coordinate[1] - H / 2) / (H / 2) * np.tan(np.deg2rad(viewing_angle_dict['y'] / 2))))
                pos_object.append((pos_now[1] - delt_y))

            else:
                delt_y = np.rad2deg(
                    np.arctan(
                        (H / 2 - center_coordinate[1]) / (H / 2) * np.tan(np.deg2rad(viewing_angle_dict['y'] / 2))))
                pos_object.append((pos_now[1] + delt_y))
            print(delt_x)
            print(delt_y)
            # pos_object = [(pos_now[0] - delt_x), (pos_now[1] - delt_y), pos_now[2]]
            pos_object.append(pos_now[2])
            if pos_object[1] <= -5:
                pos_object[1] = -5
                # bound_coordinate_temp_list.append([0, 1, 0])
                # center_coordinate[1] = 480 - (height / 2)
                # delt_y_res = np.rad2deg(
                #     np.arctan(
                #         (center_coordinate[1] - 480 / 2) / (480 / 2) * np.tan(np.deg2rad(viewing_angle_dict['y'] / 2))))
                #
                # pos_object[1] = pos_now[1] - delt_y_res
            else:
                bound_coordinate_temp_list.append([0, 0, 0])
            absoute_coordinate_temp_list.append(pos_object)
            print(absoute_coordinate_temp_list)
        absoute_coordinate_dict[key] = absoute_coordinate_temp_list
        bound_coordinate_dict[key] = bound_coordinate_temp_list
    print("okla")
    print(absoute_coordinate_dict)
    return absoute_coordinate_dict


# 存疑方法
def bound_center_y():
    viewing_angle_dict = getGisInfo()
    pos_now = getpos_sdk.pos_sdk()
    delt_y = pos_now[1] - (-5)
    H = 360
    y = (H / 2) * ((np.tan(np.deg2rad(delt_y)) / (np.tan(np.deg2rad(viewing_angle_dict['y'] / 2)))) + 1)
    return y


def bbox_center_true(result_dict, absoute_coordinate_dict):
    L = 640
    H = 360
    for key, value in result_dict.items():
        temp_list = []
        for i in range(len(value)):
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            x0 = ((x0 * L) / 1000)
            y0 = ((y0 * H) / 1000)
            x1 = ((x1 * L) / 1000)
            y1 = ((y1 * H) / 1000)
            length = x1 - x0
            height = y1 - y0
            # x0 = (720 / 2) - (length / 2)
            # x1 = x0 + length
            # y0 = (480 / 2) - (height / 2)
            # y1 = y0 + height
            # bbox_object = [x0, y0, x1, y1]
            # temp_list.append(bbox_object)
            # draw_bbox_dict[key] = temp_list
            if absoute_coordinate_dict[key][i][1] == -5:
                y_center = bound_center_y()


def translate_z(L, H, result_dict, absoute_coordinate_dict):
    # L = 640
    # H = 360
    onvif_dict = {}
    for key, value in absoute_coordinate_dict.items():
        temp_list = []
        for i in range(len(value)):
            temp_list.append(sdktoonvif(value[i]))
        onvif_dict[key] = temp_list
    kH1 = 1.87837538
    kH2 = 0.89869125
    kH3 = 0.27214642
    kV1 = 1.11636674
    kV2 = 0.83942483
    kV3 = 0.25487924
    viewing_angle_dict = getGisInfo()
    pos_now = getpos_sdk.pos_sdk()
    for key, value in result_dict.items():
        # temp_list = []
        for i in range(len(value)):
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            x0 = ((x0 * L) / 1000)
            y0 = ((y0 * H) / 1000)
            x1 = ((x1 * L) / 1000)
            y1 = ((y1 * H) / 1000)
            length = x1 - x0
            height = y1 - y0
            print("让我看老框值")
            print(length)
            print(height)
            # 问题所在
            if absoute_coordinate_dict[key][i][1] == -5:
                y_center = bound_center_y()
                print("让我看看新的y中心点")
                print(y_center)
                height_new = 2 * (H - y_center)
                length_new = (length / height) * height_new
                print("让我看看新的框值")
                print(length_new)
                print(height_new)
                FOVH_need = np.rad2deg(
                    2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                FOVV_need = np.rad2deg(
                    2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                print("让我看看视场角")
                print(FOVH_need)
                print(FOVV_need)
                z1 = (kH2 / (math.log(FOVH_need / kH1))) - kH3
                z2 = (kV2 / (math.log(FOVV_need / kV1))) - kV3
                z = (z1 + z2) / 2
                onvif_dict[key][i][2] = z
                print("让我瞧瞧z")
                print(z1)
                print(z2)
                print(z)
            else:
                if (length / height) >= (L / H):
                    length_new = L
                    height_new = (height / length) * length_new
                    print("让我看看新的框值")
                    print(length_new)
                    print(height_new)
                    FOVH_need = np.rad2deg(
                        2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                    # FOVV_need = np.rad2deg(
                    #     2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                    print("让我看看视场角")
                    print(FOVH_need)
                    # print(FOVV_need)
                    z1 = (kH2 / (np.log(FOVH_need / kH1))) - kH3
                    # z2 = (kV2 / (np.log(FOVV_need / kV1))) - kV3
                    # z = (z1 + z2) / 2
                    onvif_dict[key][i][2] = z1
                    print("让我瞧瞧z1")
                    print(z1)
                    # print(z2)
                    # print(z)
                else:
                    height_new = H
                    length_new = (length / height) * height_new
                    print("让我看看新的框值")
                    print(length_new)
                    print(height_new)
                    # FOVH_need = np.rad2deg(
                    #     2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                    FOVV_need = np.rad2deg(
                        2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                    print("让我看看视场角")
                    # print(FOVH_need)
                    print(FOVV_need)
                    # z1 = (kH2 / (np.log(FOVH_need / kH1))) - kH3
                    z2 = (kV2 / (np.log(FOVV_need / kV1))) - kV3
                    # z = (z1 + z2) / 2
                    onvif_dict[key][i][2] = z2
                    print("让我瞧瞧z2")
                    # print(z1)
                    print(z2)
                    # print(z)
    return onvif_dict


def translate_z_new(result_dict, absoute_coordinate_dict):
    onvif_dict = {}
    for key, value in absoute_coordinate_dict.items():
        temp_list = []
        for i in range(len(value)):
            temp_list.append(sdktoonvif(value[i]))
        onvif_dict[key] = temp_list
    kH1 = 1.87837538
    kH2 = 0.89869125
    kH3 = 0.27214642
    kV1 = 1.11636674
    kV2 = 0.83942483
    kV3 = 0.25487924
    viewing_angle_dict = getGisInfo()
    pos_now = getpos_sdk.pos_sdk()
    H = 480
    L = 720
    for key, value in result_dict.items():
        temp_list = []
        for i in range(len(value)):
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            x0 = ((x0 * 720) / 1000)
            y0 = ((y0 * 480) / 1000)
            x1 = ((x1 * 720) / 1000)
            y1 = ((y1 * 480) / 1000)
            length = x1 - x0
            height = y1 - y0
            print("让我看老框值")
            print(length)
            print(height)
            if absoute_coordinate_dict[key][i][1] == -5:
                print("丸辣，T值到不了中心吧？")
                y_center = bound_center_y()
                print("让我看看新的y中心点")
                print(y_center)
                # height_new = 2 * (H - y_center)
                # length_new = (length / height) * height_new
                # print("让我看看新的框值")
                # print(length_new)
                # print(height_new)
                # FOVH_need = np.rad2deg(
                #     2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                # FOVV_need = np.rad2deg(
                #     2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                FOVV_need = np.rad2deg(
                    2 * np.arctan(np.tan((viewing_angle_dict['y']) / 2) * (((height + 2 * y_center) / H) - 1)))
                print("让我看看视场角")
                # print(FOVH_need)
                print(FOVV_need)
                # z1 = (kH2 / (np.log(FOVH_need / kH1))) - kH3
                z2 = (kV2 / (np.log(FOVV_need / kV1))) - kV3
                # z = (z1 + z2) / 2
                onvif_dict[key][i][2] = z2
                print("让我瞧瞧z")
                # print(z1)
                print(z2)
                # print(z)
            else:
                if (length / height) >= (L / H):
                    length_new = L
                    height_new = (height / length) * length_new
                    print("让我看看新的框值")
                    print(length_new)
                    print(height_new)
                    FOVH_need = np.rad2deg(
                        2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                    FOVV_need = np.rad2deg(
                        2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                    print("让我看看视场角")
                    print(FOVH_need)
                    print(FOVV_need)
                    z1 = (kH2 / (np.log(FOVH_need / kH1))) - kH3
                    z2 = (kV2 / (np.log(FOVV_need / kV1))) - kV3
                    z = (z1 + z2) / 2
                    onvif_dict[key][i][2] = z
                    print("让我瞧瞧z")
                    print(z1)
                    print(z2)
                    print(z)
                else:
                    height_new = H
                    length_new = (length / height) * height_new
                    print("让我看看新的框值")
                    print(length_new)
                    print(height_new)
                    FOVH_need = np.rad2deg(
                        2 * np.arctan((length / length_new) * np.tan(np.deg2rad((viewing_angle_dict['x']) / 2))))
                    FOVV_need = np.rad2deg(
                        2 * np.arctan((height / height_new) * np.tan(np.deg2rad((viewing_angle_dict['y']) / 2))))
                    print("让我看看视场角")
                    print(FOVH_need)
                    print(FOVV_need)
                    z1 = (kH2 / (np.log(FOVH_need / kH1))) - kH3
                    z2 = (kV2 / (np.log(FOVV_need / kV1))) - kV3
                    z = (z1 + z2) / 2
                    onvif_dict[key][i][2] = z
                    print("让我瞧瞧z")
                    print(z1)
                    print(z2)
                    print(z)
    return onvif_dict


# pos = [50.384, 30.203, 2]


# def HexToDecMa(x):
#     # 十进制转换为十六进制
#     x = int(hex(x)[2:].upper()) // 10
#     return x
def HexToDecMa(x):
    # 将浮点数转换为十六进制字符串,保留 4 位小数
    hex_str = format(x, '04x').upper()

    # 将十六进制字符串转换为整数
    int_value = int(hex_str, 16)

    return int_value


def DEC2HEX_doc(x):
    # 十六进制转化为十进制
    x = int(str(int(x * 10)), 16)
    return x


def gotopos_sdk(pos):
    # iUserID
    # class NET_DVR_PTZPOS(Structure):
    # _fields_=[
    #    ("wAction", ctypes.c_uint16),
    #    ("wPanPos", ctypes.c_uint16),
    #    ("wTiltPos", ctypes.c_uint16),
    #    ("wZoomPos", ctypes.c_uint16)]
    # LPNET_DVR_PTZPOS = POINTER(NET_DVR_PTZPOS)
    if pos[1] < 0:
        pos[1] = pos[1] + 360
    ptzpos = NET_DVR_PTZPOS()
    ptzpos.wAction = 1
    ptzpos.wPanPos = DEC2HEX_doc(pos[0])
    ptzpos.wTiltPos = DEC2HEX_doc(pos[1])
    ptzpos.wZoomPos = DEC2HEX_doc(pos[2])
    ptzpos_str = LPNET_DVR_PTZPOS(ptzpos)
    let = device.Objdll.NET_DVR_SetDVRConfig(iUserID, 292, 1, ptzpos_str, byref(ptzpos))
    # print(let) #1为正确返回


def gotopos_sdk_z(pos):
    # iUserID
    # class NET_DVR_PTZPOS(Structure):
    # _fields_=[
    #    ("wAction", ctypes.c_uint16),
    #    ("wPanPos", ctypes.c_uint16),
    #    ("wTiltPos", ctypes.c_uint16),
    #    ("wZoomPos", ctypes.c_uint16)]
    # LPNET_DVR_PTZPOS = POINTER(NET_DVR_PTZPOS)
    if pos[1] < 0:
        pos[1] = pos[1] + 360
    ptzpos = NET_DVR_PTZPOS()
    ptzpos.wAction = 4
    ptzpos.wPanPos = DEC2HEX_doc(pos[0])
    ptzpos.wTiltPos = DEC2HEX_doc(pos[1])
    ptzpos.wZoomPos = DEC2HEX_doc(pos[2])
    ptzpos_str = LPNET_DVR_PTZPOS(ptzpos)
    let = device.Objdll.NET_DVR_SetDVRConfig(iUserID, 292, 1, ptzpos_str, byref(ptzpos))
    # print(let) #1为正确返回


def calculate_focal_length(sensor_width, sensor_height, hfov_degrees, vfov_degrees):
    # 将视场角从度转换为弧度
    hfov_radians = math.radians(hfov_degrees)
    vfov_radians = math.radians(vfov_degrees)

    # 计算水平焦距
    focal_length_horizontal = sensor_width / (2 * math.tan(hfov_radians / 2))
    print(focal_length_horizontal)

    # 计算垂直焦距
    focal_length_vertical = sensor_height / (2 * math.tan(vfov_radians / 2))
    print(focal_length_vertical)

    # 计算有效焦距（可以取水平和垂直焦距的平均值）
    effective_focal_length = (focal_length_horizontal + focal_length_vertical) / 2
    print(effective_focal_length)

    return focal_length_horizontal, focal_length_vertical, effective_focal_length


def absoute_coordinate_test(result_dict, X, Y, f):  # X为传感器宽度 Y为传感器高度 f为有效焦距
    viewing_angle_dict = getGisInfo()
    print(viewing_angle_dict)
    pos_now = getGisInfo_ptz()
    absoute_coordinate_dict = {}
    H = 360
    L = 640
    x0_sensor = X / 2
    y0_sensor = Y / 2
    center_psycial = [x0_sensor, y0_sensor]
    for key, value in result_dict.items():
        absoute_coordinate_temp_list = []
        for i in range(len(value)):
            pos_object = []
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            x0 = ((x0 * L) / 1000)
            y0 = ((y0 * H) / 1000)
            x1 = ((x1 * L) / 1000)
            y1 = ((y1 * H) / 1000)
            length = x1 - x0
            height = y1 - y0
            center_coordinate = [((x0 + x1) / 2), ((y0 + y1) / 2)]
            object_psycial = [(center_coordinate[0] * X) / L, (center_coordinate[1] * Y) / H]
            print("what center")
            print(center_coordinate)
            temp = math.sqrt(((object_psycial[1] - center_psycial[1]) ** 2) + (f ** 2))
            print(temp)
            temp1 = math.sin(
                math.atan((object_psycial[1] - center_psycial[1]) / f) + np.deg2rad(pos_now[1]))
            print(temp1)
            a1 = math.asin((math.sqrt(((object_psycial[1] - center_psycial[1]) ** 2) + (f ** 2))) / (math.sqrt(
                (object_psycial[0] - center_psycial[0]) ** 2 + (
                        object_psycial[1] - center_psycial[1]) ** 2 + f ** 2)) * math.sin(
                math.atan((object_psycial[1] - center_psycial[1]) / f) + np.deg2rad(pos_now[1])))
            ac = a1 - np.deg2rad(pos_now[1])  # 与中心的垂直夹角
            # bc为与中心的水平角
            if object_psycial[0] - center_psycial[0] >= 0:
                bc = math.asin(math.sin(math.atan((object_psycial[0] - center_psycial[0]) / math.sqrt(
                    (object_psycial[1] - center_psycial[1]) ** 2 + f ** 2))) / math.cos(a1))
                bc_now = np.rad2deg(bc)
                pos_object.append(pos_now[0] + bc_now)
            else:
                bc = math.asin(math.sin(math.atan((center_psycial[0] - object_psycial[0]) / math.sqrt(
                    (object_psycial[1] - center_psycial[1]) ** 2 + f ** 2))) / math.cos(a1))
                bc_now = np.rad2deg(bc)
                pos_object.append(pos_now[0] - bc_now)
            ac_now = np.rad2deg(ac)
            # bc_now = np.rad2deg(bc)
            print("ac和bc")
            print(ac_now)
            print(bc_now)
            # pos_object = [(pos_now[0] + bc_now), (pos_now[1] - ac_now), pos_now[2]]
            if (pos_now[1] - ac_now) <= -5.0:
                pos_object.append(-5.0000)
            else:
                pos_object.append(pos_now[1] + ac_now)
            pos_object.append(pos_now[2])
            absoute_coordinate_temp_list.append(pos_object)
        absoute_coordinate_dict[key] = absoute_coordinate_temp_list
    print("okla")
    print(absoute_coordinate_dict)
    return absoute_coordinate_dict


def absoute_coordinate_cvtest(L, H, result_dict, X, Y, f):  # X为传感器宽度 Y为传感器高度 f为有效焦距
    viewing_angle_dict = getGisInfo()
    print(viewing_angle_dict)
    pos_now = getGisInfo_ptz()
    absoute_coordinate_dict = {}
    x0_sensor = X / 2
    y0_sensor = Y / 2
    center_psycial = [x0_sensor, y0_sensor]
    for key, value in result_dict.items():
        absoute_coordinate_temp_list = []
        for i in range(len(value)):
            pos_object = []
            x0 = value[i][0]
            y0 = value[i][1]
            x1 = value[i][2]
            y1 = value[i][3]
            center_coordinate = [((x0 + x1) / 2), ((y0 + y1) / 2)]
            object_psycial = [(center_coordinate[0] * X) / L, (center_coordinate[1] * Y) / H]
            print("what center")
            print(center_coordinate)
            temp = math.sqrt(((object_psycial[1] - center_psycial[1]) ** 2) + (f ** 2))
            print(temp)
            temp1 = math.sin(
                math.atan((object_psycial[1] - center_psycial[1]) / f) + np.deg2rad(pos_now[1]))
            print(temp1)
            a1 = math.asin((math.sqrt(((object_psycial[1] - center_psycial[1]) ** 2) + (f ** 2))) / (math.sqrt(
                (object_psycial[0] - center_psycial[0]) ** 2 + (
                        object_psycial[1] - center_psycial[1]) ** 2 + f ** 2)) * math.sin(
                math.atan((object_psycial[1] - center_psycial[1]) / f) + np.deg2rad(pos_now[1])))
            ac = a1 - np.deg2rad(pos_now[1])  # 与中心的垂直夹角
            # bc为与中心的水平角
            if object_psycial[0] - center_psycial[0] >= 0:
                bc = math.asin(math.sin(math.atan((object_psycial[0] - center_psycial[0]) / math.sqrt(
                    (object_psycial[1] - center_psycial[1]) ** 2 + f ** 2))) / math.cos(a1))
                bc_now = np.rad2deg(bc)
                pos_object.append(pos_now[0] + bc_now)
            else:
                bc = math.asin(math.sin(math.atan((center_psycial[0] - object_psycial[0]) / math.sqrt(
                    (object_psycial[1] - center_psycial[1]) ** 2 + f ** 2))) / math.cos(a1))
                bc_now = np.rad2deg(bc)
                pos_object.append(pos_now[0] - bc_now)
            ac_now = np.rad2deg(ac)
            # bc_now = np.rad2deg(bc)
            print("ac和bc")
            print(ac_now)
            print(bc_now)
            # pos_object = [(pos_now[0] + bc_now), (pos_now[1] - ac_now), pos_now[2]]
            if (pos_now[1] - ac_now) <= -5.0:
                pos_object.append(-5.0000)
            else:
                pos_object.append(pos_now[1] + ac_now)
            pos_object.append(pos_now[2])
            absoute_coordinate_temp_list.append(pos_object)
        absoute_coordinate_dict[key] = absoute_coordinate_temp_list
    print("okla")
    print(absoute_coordinate_dict)
    return absoute_coordinate_dict


# viewing_angle_dict = getGisInfo()
# pos = [200, -1, 1.0]
# gotopos_sdk(pos)
# calculate_focal_length(4.98, 2.8, viewing_angle_dict['x'], viewing_angle_dict['y'])
# 对角线按照18/2.8（海康给出的1英寸=18mm），焦距为5.83 宽度为5.60 高度为3.15
# 对角线按照16/2.8，焦距为5.19 宽度为4.98 高度为2.80（现在在用这个）
# sdk输出Zoom=1没变倍时的焦距，精确到小数点后两位  f为5.35，按照此值计算宽度为5.13,高度为2.89
