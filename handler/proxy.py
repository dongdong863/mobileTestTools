#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from handler import install
from handler import device
import threading


def install_proxy_setter(device_list, local_path, mobile_path, file_name):
    install.install_from_local_multi_device(device_list, local_path, mobile_path, file_name)


def set_proxy(conn, proxy_host, proxy_port, ssid, password):
    shell_command = "am start -n tk.elevenk.proxysetter/.MainActivity -e host %s -e port %s -e ssid %s -e key %s" \
                    % (proxy_host, proxy_port, ssid, password)
    output, exit_code = conn.shell(shell_command)
    print('device:%s, execute:\"set proxy host-%s port-%s ssid-%s\", code:%d\n'
          % (conn.info['productName'], proxy_host, proxy_port, ssid, exit_code))


def set_proxy_multi(device_list, proxy_host, proxy_port, ssid, password):
    for dev in device_list:
        conn = dev.conn()
        if conn is not None:
            t = threading.Thread(target=set_proxy, args=(conn, proxy_host, proxy_port, ssid, password))
            t.start()

