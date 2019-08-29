#!/usr/bin/python
# -*- coding: utf-8 -*-

from screenshot import shot_multi_device
from device import *
from install import *
import threading
import datetime
from urllib import request
import os
import sys
sys.path.append('..\\util')
from url_util import app_recent_url


if __name__ == '__main__':

    device_list = [Device('asdfdf', '192.168.253.2', '7912', 'oneplus5'),
                   Device('LVVO6SOJ99999999', '192.168.253.8', '7912', 'vivox6'),
                   Device('redmi', '172.26.128.37', '7912', 'redmi')]
    # Device('ffbf0a3f', '192.168.253.3', '7912', 'r1')]

    base_url = 'http://repo.yypm.com/dwbuild/mobile/android/gouqiktv'

    brunch = '1.0.1'

    apk_file = 'gouqiktv.apk'

    app_url = app_recent_url(base_url, brunch, apk_file)
    print('url:' + app_url)

    # download
    local_path = 'e:\\autoTest\\mobileTestTools'

    file_name = 'gouqiktv.apk'

    app_file = local_path + "\\" + file_name

    mobile_path = '/data/local/tmp/'

    if os.path.exists(app_file):
        os.remove(app_file)
    request.urlretrieve(app_url, app_file)

    # call multi device install
    install_from_local_multi_device(device_list, local_path, mobile_path, file_name)
