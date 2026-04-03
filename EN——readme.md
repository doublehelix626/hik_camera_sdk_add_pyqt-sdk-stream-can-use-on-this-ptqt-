# Hikvision PTZ Camera + PyQt Video Stream Demo

<p align="center">
  <img src="./readme_fig/raedme_fig.png" alt="project demo" width="900">
</p>

## Introduction

This project is based on **Python + PyQt5 + Hikvision HCNetSDK**, and implements the access and control of a Hikvision PTZ camera in a PyQt interface.

The main goals of this project are:

- to display the video stream from a Hikvision camera in a PyQt interface
- to solve the problem that the SDK video stream is difficult to play stably and directly in a Qt interface
- to preserve playback-related return codes, so that other SDK functions can continue to be called **without interrupting the video stream**
- to provide basic PTZ control functions, such as pan/tilt movement and zoom in / zoom out
- to support screenshot display and partial position acquisition functions

This project is more suitable as a **Hikvision PTZ + PyQt host-side development demo**, and it can be further extended into a complete device control software system or experimental platform.

---

## Features

- Supports PyQt5 graphical interface
- Supports Hikvision device login and SDK initialization
- Supports RTSP video stream display in Qt widgets
- Supports basic PTZ control of the camera
  - move up
  - move down
  - move left
  - move right
  - zoom in
  - zoom out
- Supports screenshot function
- Reserves SDK / ONVIF-based position acquisition related modules for future extension

---

## Project Structure

```text
.
├── main.py                         # Project entry
├── UI/                             # PyQt interface and UI event binding
│   ├── test.py
│   ├── test.ui
│   ├── testshow.py
│   ├── testshow.ui
│   └── ui_bundle_event.py
├── UIconnect/                      # Binding between UI controls and business logic
│   ├── device_driver_controller.py
│   └── show_video_controller.py
├── base_service/                   # Basic service layer
│   ├── base_control_sdk.py
│   ├── getpos_onvif.py
│   ├── getpos_sdk.py
│   ├── screenshot_sdk.py
│   └── show_video_videocapture.py
├── device_driver/                  # Hikvision SDK wrapper and device initialization
│   ├── HCNetSDK.py
│   ├── PlayCtrl.py
│   ├── device_init.py
│   ├── getptzpos.py
│   └── lib/
│       └── win/                    # Windows SDK dynamic library directory
├── utils/                          # Utility modules
├── logs/                           # Runtime log directory
├── sdklog/                         # SDK log directory
└── readme_fig/                     # README image resources
```

---

## Module Description

- `main.py`  
  The entry point of the project. It is used to create the PyQt application and load the main interface.

- `UI/`  
  Stores UI design files and their corresponding Python files, mainly responsible for interface layout and basic event definitions.

- `UIconnect/`  
  Used to bind UI controls with business logic, connecting interface operations with functions such as video stream display and device control.

- `base_service/`  
  The basic service layer, which encapsulates common functions such as video display, screenshot, and position acquisition.

- `device_driver/`  
  The Hikvision SDK wrapper and device initialization module, responsible for device login, SDK invocation, and part of the low-level PTZ control logic.

- `utils/`  
  Utility classes and helper modules.

- `logs/` and `sdklog/`  
  Used to store program runtime logs and SDK-related logs.

- `readme_fig/`  
  The image resource directory used in the README.

---

## Environment

Recommended environment:

- Windows
- Python 3.8 or above
- PyQt5
- Hikvision HCNetSDK
- PlayCtrl.dll
- Hikvision network camera / PTZ camera
- A network environment where the camera is reachable

If the video display module depends on OpenCV, you can also install:

```bash
pip install opencv-python
```

---

## Installation and Preparation

### 1. Clone the project

```bash
git clone https://github.com/doublehelix626/hik_camera_sdk_add_pyqt-sdk-stream-can-use-on-this-ptqt-.git
cd hik_camera_sdk_add_pyqt-sdk-stream-can-use-on-this-ptqt-
```

### 2. Install Python dependencies

At least install:

```bash
pip install PyQt5
```

If other dependencies are not installed in your local environment, please continue to install them according to the error messages.

---

## Hikvision SDK Configuration

Please make sure that the Hikvision SDK dynamic libraries have been placed in the following directory:

```text
./device_driver/lib/win
```

At least the following files should be loaded correctly by the program:

- `HCNetSDK.dll`
- `PlayCtrl.dll`

If your SDK files are located in a different path, please modify the corresponding library path configuration in the code.

---

## Device Parameter Configuration

Before running the project, please modify the parameters according to your own camera information.

### 1. Modify device login information

Edit the file:

```text
device_driver/device_init.py
```

Change the device parameters to your own values:

- device IP
- device port
- username
- password

### 2. Modify the RTSP address

Edit the file:

```text
UIconnect/show_video_controller.py
```

Change the RTSP address to your own camera address, for example:

```python
stream_addr = "rtsp://<username>:<password>@<ip>:554"
```

---

## How to Run

The project entry file is:

```bash
python main.py
```

After startup, the program will:

1. initialize the PyQt application
2. create the device object
3. load the main interface
4. automatically bind interface events
5. create the log directory
6. display the main window

---

## Implemented Control Logic

At present, the following basic control logic has been implemented and bound in the project:

- video stream display
- screenshot display
- zoom in
- zoom out
- PTZ upward movement
- PTZ downward movement
- PTZ leftward movement
- PTZ rightward movement

The control method mainly adopts the pattern of **pressing a button to start an action and releasing the button to stop it**, which is suitable for real-time PTZ interaction.

---

## Applicable Scenarios

This project is suitable for reference or secondary development in the following scenarios:

- desktop control program for Hikvision PTZ cameras
- PyQt host-side development examples
- camera control experimental platforms
- verification of video stream display and screenshot functions
- SDK secondary encapsulation practice
- robot vision / PTZ control related engineering projects

---

## Possible Extensions

You can continue to extend this project with:

- preset position control
- focal length / zoom ratio status display
- real-time PTZ position reading
- automatic cruise
- multi-camera management
- device parameter configuration pages
- improved logging system
- unified error code encapsulation
- configuration-based management instead of hard-coded parameters

---

## Notes

1. The current project is more suitable as a development example and experimental project.
2. It is recommended not to directly submit real device IPs, usernames, and passwords to a public repository.
3. It is recommended to later change the device configuration to:
   - `config.yaml`
   - `.env`
   - or a separate local configuration file
4. It is recommended to add a `.gitignore` file to avoid submitting logs, IDE configurations, and SDK runtime cache files together.

---

## Acknowledgements

This project is based on:

- Python
- PyQt5
- Hikvision HCNetSDK
- RTSP video stream

and is used to explore the access, display, and control of Hikvision PTZ cameras in a desktop GUI environment.

---
