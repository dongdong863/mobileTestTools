#!/usr/bin/python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
from handler.device import *
import threading
import time
import uiautomator2.exceptions
import sys
import traceback


def click_user_center_tab(d):
    try:
        d(resourceId="com.yy.mobile.plugin.homepage:id/hp_home_tab_img",
          className="android.widget.ImageView", instance=4).click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def user_center_tab_exist(d):
    return d(text=u"个人中心").exists(timeout=10)


def click_start_live_in_center(d):
    try:
        for i in range(1, 7, 1):
            if d(text=u"我要开播").exists():
                d(text=u"我要开播").click()
                break
            elif d(text=u"非开播也").exists():
                d(text=u"非开播也").click()
                break
            time.sleep(1)
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def click_start_live_btn(d):
    try:
        time.sleep(1)
        d(resourceId='com.duowan.mobile.entlive:id/start_live').click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def change_cover_exist(d):
    is_exists = d(text=u"更换封面").exists(timeout=3)
    print(is_exists)
    return is_exists


def click_upload_photo_btn(d):
    try:
        d(text=u"去上传").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def choose_photo(d):
    try:
        d(resourceId="com.yy.mobile.plugin.main:id/thumb1").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def click_use_btn(d):
    try:
        d(resourceId="com.yy.mobile.plugin.main:id/btn_use").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def click_interaction_btn(d):
    try:
        d(resourceId="com.duowan.mobile.entlive:id/live_anchor_basic_function_interaction").click()
        # 等待一秒，使互动面板完全加载
        time.sleep(1)
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def wait_interaction_exist(d):
    return d(resourceId="com.duowan.mobile.entlive:id/live_anchor_basic_function_interaction").exists(timeout=30)


def click_happy_pk_btn(d):
    try:
        d(resourceId="com.yy.mobile.plugin.livebasebiz:id/entlive_plugincenteritem_name",
          text=u'欢乐斗').click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def get_friend_num(d):
    try:
        num = d(resourceId="com.yy.mobile.channelpk:id/entry_friend_num").get_text()
        return int(num)
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def click_pk_back_btn(d):
    try:
        d(resourceId="com.yy.mobile.channelpk:id/iv_pk_rank_back").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def click_friend_pk_btn(d):
    try:
        d(resourceId="com.yy.mobile.channelpk:id/friend_pk").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def invite_pk_friend(d):
    try:
        d(resourceId="com.yy.mobile.channelpk:id/bt_invite").click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def agree_pk_invite(d):
    try:
        d(text=u'同意').click()
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def watcher_alert_cover_changer(d):
    try:
        d.watcher("alert_cover_changer").when(text=u"建议换个封面哟").click(text=u"关闭")
        d.watchers.watched = True
    except uiautomator2.exceptions.UiObjectNotFoundError:
        print('UiObjectNotFoundError...')
        traceback.print_exc()


def remove_watcher(d, name):
    try:
        d.watchers.remove(name)
    except:
        traceback.print_exc()
