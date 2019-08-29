#!/usr/bin/python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
from uiautomator2 import adbutils
import requests.exceptions


class Device:
    def __init__(self, device_id, ip, port, name):
        self.device_id = device_id
        self.ip = ip
        self.port = port
        self.name = name

    def get_name(self):
        return self.name

    def get_device_id(self):
        return self.device_id

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def set_name(self, name):
        self.name = name

    def set_device_id(self, device_id):
        self.device_id = device_id

    def set_ip(self, ip):
        self.ip = ip

    def set_port(self, port):
        self.port = port

    def conn(self):
        device_addr = 'http://' + self.ip + ":" + self.port
        conn = u2.connect(device_addr)

        # 如果agent不能连上，捕获异常
        if not conn.agent_alive:
            try:
                conn = u2.connect_usb(self.device_id)
                if not conn.agent_alive:
                    return None
            except adbutils.errors.AdbError:
                print('AdbError: device not found')
                print('%s(%s) connect fail,please check...' % (self.name, self.ip))
                return None
        print('%s(%s) is connected...' % (self.name, self.ip))

        # 如果u2服务没启动，就启动一下
        if not conn.alive:
            try:
                conn.service('uiautomator').start()
            except requests.exceptions.HTTPError:
                print('requests.exceptions.HTTPError: 500 Server Error'
                      'Internal Server Error for url: http://%s:7912/uiautomator' % self.ip)
        return conn

    def check(self):
        device_addr = 'http://' + self.ip + ":" + self.port
        print(u2.connect(device_addr).agent_alive)

