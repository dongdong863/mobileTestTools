#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.device import *
from handler.install import *
import configparser
from urllib import request
import os
import sys
from util.url_util import app_recent_url


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

    base_url = config.get('package', 'base_url')
    brunch = config.get('package', 'brunch')
    build_number = config.get('package', 'build_number')
    apk_file = config.get('package', 'apk_file')

    local_path = config.get('path', 'local_path')
    mobile_path = config.get('path', 'mobile_path')
    shot_file_path = config.get('path', 'shot_file_path')

    # install app
    app_url = app_recent_url(base_url, brunch, build_number, apk_file)
    print('url:' + app_url)

    file_name = apk_file
    app_file = local_path + "\\" + file_name

    if os.path.exists(app_file):
        os.remove(app_file)
    request.urlretrieve(app_url, app_file)

    # call multi device install
    install_from_local_multi_device(device_list, local_path, mobile_path, file_name)
