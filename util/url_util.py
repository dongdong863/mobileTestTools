#!/usr/bin/python
# -*- coding: utf-8 -*-

from util.html_parse_util import *
from urllib import request


def app_recent_url(base_url, brunch, build_number, apk_file):
    app_url = base_url + '/' + brunch
    res = request.urlopen(app_url)
    html = str(res.read())

    if int(build_number) != 0:
        hp_util = ParseByBuildNumber(build_number)
    else:
        hp_util = ParseByRecentVersion()
    hp_util.feed(html)
    recent_version_href = hp_util.app_recent_version_href
    print(recent_version_href)
    app_url = app_url + '/' + recent_version_href + apk_file
    return app_url
