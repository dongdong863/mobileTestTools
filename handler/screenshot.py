#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import datetime


def take_shot(conn, shot_file):
    try:
        conn.screenshot(shot_file)
    except:
        print('something wrong...')


def shot_multi_device(device_list, shot_file_path):
    cur_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for dev in device_list:
        conn = dev.conn()
        if conn is None:
            continue
        shot_file = shot_file_path + '\\' + dev.get_name() + '_' + cur_time + '.jpg'
        threading.Thread(target=take_shot,
                         args=(conn, shot_file)).start()
