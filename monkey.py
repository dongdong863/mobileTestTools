#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.device import *
from handler.monkey import *
import configparser
import sys


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('no args... \nrun the python program like this : python xx.py xx.ini')
        exit(0)
    if len(sys.argv) > 2:
        print('args number out of limit...\nrun the python program like this : python xx.py xx.ini')
        exit(0)
    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file, "utf-8")

    device_list = []
    for option in config.options('device'):
        option_value = config.get('device', option)
        print(option_value)
        device_id, ip, port, name = option_value.split(',')
        device_list.append(Device(device_id, ip, port, name))

    monkey_args = dict(config.items('monkey'))
    print('monkey_args:', monkey_args)
    print(type(monkey_args))
    for key in monkey_args.keys():
        print('key:%s   value:%s' % (key, monkey_args.get(key)))

    run_monkey_multi_device(device_list, monkey_args)

