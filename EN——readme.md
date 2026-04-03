# Hikvision PTZ Camera + PyQt Streaming Demo

<p align="center">
  <img src="./readme_fig/raedme_fig.png" alt="Project Demo" width="900">
</p>

<p align="center">
  A Python + PyQt demo project for Hikvision PTZ camera access, video streaming, and basic PTZ control.
</p>

---

## Introduction

This project connects **Python**, **PyQt**, and a **Hikvision PTZ camera** to build a simple desktop control and streaming demo.

The main purpose of this repository is to solve a practical issue:  
the video stream returned by the Hikvision SDK is not always convenient to display directly inside a Qt-based GUI. This project provides a PyQt-based integration approach and keeps the playback-related return information available, making it easier to call additional SDK methods without interrupting the video stream.

This repository can be used as:

- a PyQt + Hikvision integration example
- a PTZ camera desktop control demo
- a secondary development template for Hikvision SDK projects
- a quick experimental platform for PTZ-related research or engineering tasks

---

## Features

- PyQt-based GUI
- Hikvision device initialization and login
- Video stream display in Qt interface
- Basic PTZ control
- Zoom in / zoom out control
- Screenshot-related module support
- Device driver and controller separation
- Basic project structure for further expansion

---

## Project Structure

```text
.
├── main.py
├── UI/
├── UIconnect/
├── base_service/
├── device_driver/
├── logs/
├── readme_fig/
├── sdklog/
├── utils/
└── README.md
