# 海康 PTZ 摄像机 + PyQt 视频流显示示例

<p align="center">
  <img src="./readme_fig/raedme_fig.png" alt="项目演示图" width="900">
</p>

## 项目简介

本项目基于 **Python + PyQt5 + Hikvision HCNetSDK**，实现了海康威视 PTZ 摄像机在 PyQt 界面中的接入与控制。

本项目的主要目标包括：

- 在 PyQt 界面中显示海康摄像机的视频流
- 解决 SDK 视频流难以在 Qt 界面中直接稳定播放的问题
- 保留播放相关返回码，从而能够在**不中断视频流**的前提下继续调用其他 SDK 功能
- 提供基础 PTZ 控制功能，例如云台转动与变焦放大 / 缩小
- 支持截图显示以及部分位置获取功能

本项目更适合作为一个 **海康 PTZ + PyQt 上位机开发示例工程**，并可进一步扩展为完整的设备控制软件系统或实验平台。

---

## 功能特性

- 支持 PyQt5 图形界面
- 支持海康设备登录与 SDK 初始化
- 支持在 Qt 控件中显示 RTSP 视频流
- 支持摄像机基础 PTZ 控制
  - 向上移动
  - 向下移动
  - 向左移动
  - 向右移动
  - 放大
  - 缩小
- 支持截图功能
- 预留基于 SDK / ONVIF 的位置获取相关模块，便于后续扩展

---

## 项目结构

```text
.
├── main.py                         # 项目入口
├── UI/                             # PyQt 界面与界面事件绑定
│   ├── test.py
│   ├── test.ui
│   ├── testshow.py
│   ├── testshow.ui
│   └── ui_bundle_event.py
├── UIconnect/                      # UI 控件与业务逻辑绑定
│   ├── device_driver_controller.py
│   └── show_video_controller.py
├── base_service/                   # 基础服务层
│   ├── base_control_sdk.py
│   ├── getpos_onvif.py
│   ├── getpos_sdk.py
│   ├── screenshot_sdk.py
│   └── show_video_videocapture.py
├── device_driver/                  # 海康 SDK 封装与设备初始化
│   ├── HCNetSDK.py
│   ├── PlayCtrl.py
│   ├── device_init.py
│   ├── getptzpos.py
│   └── lib/
│       └── win/                    # Windows 下 SDK 动态库目录
├── utils/                          # 工具模块
├── logs/                           # 运行日志目录
├── sdklog/                         # SDK 日志目录
└── readme_fig/                     # README 图片资源
```

---

## 模块说明

### `main.py`
项目入口文件，用于创建 PyQt 应用并加载主界面。

### `UI/`
存放 UI 设计文件及其对应的 Python 文件，主要负责界面布局和基础事件定义。

### `UIconnect/`
用于绑定 UI 控件与业务逻辑，将界面操作与视频流显示、设备控制等功能连接起来。

### `base_service/`
基础服务层，封装了视频显示、截图和位置获取等通用功能。

### `device_driver/`
海康 SDK 封装与设备初始化模块，负责设备登录、SDK 调用以及部分底层 PTZ 控制逻辑。

### `utils/`
工具类与辅助模块。

### `logs/` 和 `sdklog/`
用于存放程序运行日志以及 SDK 相关日志。

### `readme_fig/`
README 中使用的图片资源目录。

---

## 运行环境

推荐环境如下：

- Windows
- Python 3.8 及以上
- PyQt5
- Hikvision HCNetSDK
- PlayCtrl.dll
- 海康网络摄像机 / PTZ 摄像机
- 摄像机可被访问的网络环境

如果视频显示模块依赖 OpenCV，你也可以安装：

```bash
pip install opencv-python
```

---

## 安装与准备

### 1. 克隆项目

```bash
git clone https://github.com/doublehelix626/hik_camera_sdk_add_pyqt-sdk-stream-can-use-on-this-ptqt-.git
cd hik_camera_sdk_add_pyqt-sdk-stream-can-use-on-this-ptqt-
```

### 2. 安装 Python 依赖

至少安装：

```bash
pip install PyQt5
```

如果你的本地环境中尚未安装其他依赖，请根据报错信息继续补充安装。

---

## 海康 SDK 配置

请确保海康 SDK 的动态库已经放置在以下目录中：

```text
./device_driver/lib/win
```

程序至少需要能够正确加载以下文件：

- `HCNetSDK.dll`
- `PlayCtrl.dll`

如果你的 SDK 文件位于其他路径，请修改代码中对应的库路径配置。

---

## 设备参数配置

在运行项目之前，请根据你自己的摄像机信息修改相关参数。

### 1. 修改设备登录信息

编辑以下文件：

```text
device_driver/device_init.py
```

将设备参数修改为你自己的值：

- 设备 IP
- 设备端口
- 用户名
- 密码

### 2. 修改 RTSP 地址

编辑以下文件：

```text
UIconnect/show_video_controller.py
```

将 RTSP 地址修改为你自己的摄像机地址，例如：

```python
stream_addr = "rtsp://<username>:<password>@<ip>:554"
```

---

## 运行方式

项目入口文件为：

```bash
python main.py
```

程序启动后，将会：

1. 初始化 PyQt 应用
2. 创建设备对象
3. 加载主界面
4. 自动绑定界面事件
5. 创建日志目录
6. 显示主窗口

---

## 已实现的控制逻辑

目前项目中已经实现并绑定了以下基础控制逻辑：

- 视频流显示
- 截图显示
- 放大
- 缩小
- 云台向上移动
- 云台向下移动
- 云台向左移动
- 云台向右移动

控制方式主要采用 **按下按钮开始动作，松开按钮停止动作** 的模式，适用于 PTZ 实时交互。

---

## 适用场景

本项目适用于以下场景中的参考或二次开发：

- 海康 PTZ 摄像机桌面控制程序
- PyQt 上位机开发示例
- 摄像机控制实验平台
- 视频流显示与截图功能验证
- SDK 二次封装实践
- 机器人视觉 / PTZ 控制相关工程项目

---

## 可扩展方向

你可以继续在本项目基础上扩展以下功能：

- 预置位控制
- 焦距 / 变焦倍率状态显示
- PTZ 实时位置读取
- 自动巡航
- 多摄像机管理
- 设备参数配置页面
- 更完善的日志系统
- 统一的错误码封装
- 用配置化管理替代硬编码参数

---




