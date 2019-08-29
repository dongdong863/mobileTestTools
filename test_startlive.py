#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.device import *
from handler.action import *
import configparser
import sys
import threading


class HappyPkInviterThread(threading.Thread):
    def __init__(self, event, conn):
        super(HappyPkInviterThread, self).__init__()
        self.event = event
        self.conn = conn

    def run(self):
        print('inviter begin invite actions..')
        self.conn.implicitly_wait(20.0)
        click_interaction_btn(self.conn)
        click_happy_pk_btn(self.conn)
        count = 0
        friend_num = get_friend_num(self.conn)
        print("friend num is:%s" % friend_num)
        while friend_num == 0 and count < 10:
            click_pk_back_btn(self.conn)
            click_interaction_btn(self.conn)
            click_happy_pk_btn(self.conn)
            count = count + 1
            time.sleep(1)
        click_friend_pk_btn(self.conn)
        invite_pk_friend(self.conn)
        self.event.set()


class HappyPkReceiverThread(threading.Thread):
    def __init__(self, event, conn):
        super(HappyPkReceiverThread, self).__init__()
        self.event = event
        self.conn = conn

    def run(self):
        self.event.wait()
        print('receiver begin agree actions..')
        agree_pk_invite(self.conn)


signal = threading.Event()


def start_live_actions(dev_conn):
    print('device:%s, starting live' % dev_conn.info['productName'])
    dev_conn.app_stop('com.duowan.mobile')
    dev_conn.app_start('com.duowan.mobile')
    # 注册一个更换封面弹窗的watcher
    watcher_alert_cover_changer(dev_conn)

    dev_conn.implicitly_wait(10.0)
    if user_center_tab_exist(dev_conn):

        click_user_center_tab(dev_conn)
        click_start_live_in_center(dev_conn)
        if change_cover_exist(dev_conn):
            click_start_live_btn(dev_conn)
        else:
            click_start_live_btn(dev_conn)
            click_upload_photo_btn(dev_conn)
            choose_photo(dev_conn)
            click_use_btn(dev_conn)
            click_start_live_btn(dev_conn)
        # 要等互动图标加载出来，才算开播成功了
        wait_interaction_exist(dev_conn)
    remove_watcher(dev_conn, "alert_cover_changer")


def start_live_action_multi(dev_conn_list):
    threads = []
    for conn in dev_conn_list:
        if conn is not None:
            threads.append(threading.Thread(target=start_live_actions,
                                            args=(conn,)))
    for t in threads:
        t.start()
    return threads


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

    if len(device_list) > 2:
        print('device number more than 2..')
        exit(0)

    conn_list = []
    for dev in device_list:
        c = dev.conn()
        if c is not None:
            conn_list.append(c)

    start_live_threads = start_live_action_multi(conn_list)
    for th in start_live_threads:
        th.join()

    time.sleep(2)
    anchor_inviter = HappyPkInviterThread(signal, conn_list[0])
    anchor_receiver = HappyPkReceiverThread(signal, conn_list[1])
    anchor_inviter.start()
    anchor_receiver.start()

