# TornadoCenter

The center of tornado, the launcher of tornado servers and clients!

## Introduction

A design pattern focusing on the needs to handle the Tornado C/S instances<br />
which run separately from the main handler of your program~<br />
In TornadoCenter, a command-line application is taken as an example~<br />

## Requirements
- python >= 3.5
- pip install tornado

## Usage

- help
    - Show this help message
- server start \[-p \<port\>\] \[-n \<num_proc\>\]
    - Start Tornado TCPServer
- server stop
    - Stop Tornado TCPServer
- server params
    - Show the params of TCPServer
- server status
    - Show the status of TCPServer
- exit
    - Exit the TornadoCenter
