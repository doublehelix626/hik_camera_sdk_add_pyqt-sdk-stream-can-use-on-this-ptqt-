import requests
import operator


def onviftosdk_p(x):
    y = (180 * x)
    return y


def sdktoonvif_p(x):
    y = (x / 180)
    return y


def sdktoonvifs_p(x):
    y = ((x - 360) / 180)
    return y


def onviftosdks_p(x):
    y = (180 * x + 360)
    return y


def onviftosdk_t(x):
    y = (-47.6 * x + 42.2)
    return y


def sdktoonvif_t(x):
    y = ((42.2 - x) / 47.6)
    return y


def onviftosdk_z(x):
    y = (22 * x + 1)
    return y


def sdktoonvif_z(x):
    y = ((x - 1) / 22)
    return y


def pos_onvif():
    response = requests.post("http://127.0.0.1:8889/ptz/Configuration/GetStatus")
    response_dict = response.json()
    pos = [response_dict['ConfigurationContent']['Position']['PanTilt']['x'],
           response_dict['ConfigurationContent']['Position']['PanTilt']['y'],
           response_dict['ConfigurationContent']['Position']['Zoom']['x']]
    return pos


def gotopos_onvif(pos):
    if pos[0] > 1:
        pos[0] = 1
    if pos[0] < -1:
        pos[0] = -1
    if pos[1] > 1:
        pos[1] = 1
    if pos[1] < -1:
        pos[1] = -1
    if pos[2] > 1:
        pos[2] = 1
    if pos[2] < 0:
        pos[2] = 0
    data = {
        "Position": {
            "PanTilt": {
                "x": pos[0],
                "y": pos[1]
            },
            "Zoom": {
                "x": pos[2]
            }

        }

    }
    print(data)
    response = requests.post("http://127.0.0.1:8889/ptz/move/AbsoluteMove", json=data)
    print(response.content)
    response_dict = response.json()
    pos = [response_dict['PTZ_Status']['Position']['PanTilt']['x'],
           response_dict['PTZ_Status']['Position']['PanTilt']['y'],
           response_dict['PTZ_Status']['Position']['Zoom']['x']]
    return pos



def sdktoonvif(pos):
    if pos[0] >= 180:
        pos[0] = sdktoonvifs_p(pos[0])
        print(pos[0])
    else:
        pos[0] = sdktoonvif_p(pos[0])
        print(pos[0])
    pos[1] = sdktoonvif_t(pos[1])
    print(pos[1])
    pos[2] = sdktoonvif_z(pos[2])
    print(pos[2])
    return pos


# sdktoonvif([50.384, 30.203, 2])
