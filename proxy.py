#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.device import *
from handler.proxy import *
import configparser
import sys


def main():
    if len(sys.argv) == 1:
        print('no args... \nrun the python program like this : python xx.py xx.ini')
        exit(0)
    if len(sys.argv) > 2:
        print('args number out of limit...\nrun the python program like this : python xx.py xx.ini')
        exit(0)
    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file, "utf-8")
    # for sections in config.sections():
    #     print(sections)
    #     for items in config.items(sections):
    #         print(items)
    device_list = []
    for option in config.options('device'):
        option_value = config.get('device', option)
        print(option_value)
        device_id, ip, port, name = option_value.split(',')
        device_list.append(Device(device_id, ip, port, name))

    local_path = config.get('path', 'local_path')
    mobile_path = config.get('path', 'mobile_path')
    file_name = "proxy-setter-debug-0.2.1.apk"

    proxy_host = "172.25.49.33"
    proxy_port = "8888"
    ssid = "360-1"
    password = "test123456"
    # install_proxy_setter(device_list, local_path, mobile_path, file_name)
    set_proxy_multi(device_list, proxy_host, proxy_port, ssid, password)


if __name__ == '__main__':
    main()
