# ICMPing - v1.1.0
ICMPing is a lightweight, open-sourced tool designed to send and analyze ICMP ping requests to IPv4 & IPv6 addresses, making network diagnostics simple and easy. 


![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Caleb-Greene/ICMPing/total?style=for-the-badge&color=029cff) ![GitHub Release](https://img.shields.io/github/v/release/Caleb-Greene/ICMPing?style=for-the-badge&color=029cff)


## Preview
![DEMO1](https://github.com/user-attachments/assets/e6787dd8-d470-460e-8d4b-ff44035ee5c1)
![DEMO2](https://github.com/user-attachments/assets/b361ade2-b666-4b1d-9211-372410095d03)




## Features
### - Input Custom Values
- Ping count
- Interval between pings
- Timeout duration
- Target IPv4 or IPv6 address
### - Real-Time Output
- Round Trip Time (RTT)
- Packet responsiveness
- Timestamped data
### - Detailed Summary
- Packets sent/received
- Packet loss
- RTT min/max/avg
- Jitter
### - Downloadable Data
### - Error Handling
### - Multi-Threaded Execution
### - Lightweight & Open-Sourced

## Dependencies
- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter)
- [`icmplib`](https://github.com/ValentinBELYN/icmplib)
- [`Pillow`](https://github.com/python-pillow/Pillow)

## VirusTotal
Virus Total results can be seen [here](https://www.virustotal.com/gui/file/8f57daea9ff7b8ea3184c10026ae995521281c387d835e98ee2f8760a2a41b26/detection). Please note that the detections are false positives raised due to the fact that the application was packaged using PyInstaller. All code and files are completely safe and open-sourced, so you can download and view them yourself. 

Version v1.1.0 is now verified by Microsoft Security Intelligence as of July 1st, 2025.

## Download Options

### - GitHub
- Download the release from the attached exe [here](https://github.com/Caleb-Greene/ICMPing/releases/download/v1.1.0/ICMPing.exe)
### - Google Drive
- Download the release from [Google Drive](https://drive.google.com/drive/folders/1wt3lZsYCIsp06WSQC9oRksialB3ur3TI?usp=sharing)
### - Source Code
1. Download the dependencies via pip ```bash pip install customtkinter icmplib Pillow```
2. Running the main.py file using Python version 3.7+