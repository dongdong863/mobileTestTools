#!/usr/bin/python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
import threading
from urllib import request
from handler.device import *
import traceback
import time
import json


def install(conn, app_url):
    conn.app_install(app_url)


def rm_mobile_file(dev_name, conn, mobile_path, file_name):
    output, exit_code = conn.shell(["rm", mobile_path + file_name])
    print('device:%s, execute:\"rm %s\", code:%d\n'
          % (dev_name, mobile_path + file_name, exit_code))


def push_apk_file(dev_name, conn, local_path, mobile_path, file_name):
    try:
        print('device:%s, execute:\"push %s to %s\"'
              % (dev_name, local_path + '\\' + file_name, mobile_path))
        r = conn.push(local_path + '\\' + file_name, mobile_path, mode=0o755)
        print("done! %s\n" % str(r))
        time.sleep(1)
    except requests.exceptions.ReadTimeout:
        traceback.print_exc()
        print('retry...')
        try:
            print('device:%s, execute:\"push %s to %s\"'
                  % (dev_name, local_path + '\\' + file_name, mobile_path))
            conn.push(local_path + '\\' + file_name, mobile_path)
            print("done!\n")
            time.sleep(1)
        except requests.exceptions.ReadTimeout:
            print('retry fail... requests.exceptions.ReadTimeout')


def install_in_mobile(dev_name, conn, mobile_path, file_name):
    output, exit_code = conn.shell("pm install -r " + mobile_path + file_name, timeout=300)
    print('device:%s, execute:\"pm install -r %s\", code:%d\n'
          % (dev_name, mobile_path + file_name, exit_code))


def install_multi_device(device_list, app_url):
    for dev in device_list:
        conn = dev.conn()
        threading.Thread(target=install,
                         args=(conn, app_url)).start()


def install_from_local_multi_device(device_list, local_path, mobile_path, file_name):
    # connect device
    conn = {}
    for dev in device_list:
        dev_conn = dev.conn()
        if dev_conn is not None:
            conn[dev.get_name()] = dev_conn

    # rm apk in mobile
    for dev_name in conn.keys():
        rm_mobile_file(dev_name, conn[dev_name], mobile_path, file_name)
        # threading.Thread(target=rm_mobile_file,
        #                  args=(c, mobile_path, file_name)).start()

    # push local apk to mobile
    for dev_name in conn.keys():
        push_apk_file(dev_name, conn[dev_name], local_path, mobile_path, file_name)

    # install apk in mobile
    for dev_name in conn.keys():
        threading.Thread(target=install_in_mobile,
                         args=(dev_name, conn[dev_name], mobile_path, file_name)).start()

