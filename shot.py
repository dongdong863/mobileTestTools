#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.device import *
from handler.screenshot import *
import configparser
import sys


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('no args... \nrun the python program like this : '
              '\"python xx.py xx.ini\" or \"python xx.py xx.ini {number}\"')
        exit(0)
    if len(sys.argv) > 3:
        print('args number out of limit...\nrun the python program like this : '
              '\"python xx.py xx.ini\" or \"python xx.py xx.ini {number}\"')
        exit(0)

    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file, "utf-8")

    shot_file_path = config.get('path', 'shot_file_path')

    device_list = []
    if len(sys.argv) == 2:
        for option in config.options('device'):
            option_value = config.get('device', option)
            device_id, ip, port, name = option_value.split(',')
            device_list.append(Device(device_id, ip, port, name))

    if len(sys.argv) == 3:
        try:
            device_index = int(sys.argv[2])
        except ValueError:
            print('args type wrong...')
            exit(0)
        if device_index > len(config.options('device')):
            print('device number out of range')
            exit(0)
        for index in range(len(config.options('device'))):
            if (index + 1) == device_index:
                option_value = config.get('device', config.options('device')[index])
                device_id, ip, port, name = option_value.split(',')
                device_list.append(Device(device_id, ip, port, name))
    # screen shot
    if len(device_list) != 0:
        shot_multi_device(device_list, shot_file_path)
    else:
        print('no device found...')
