#!/usr/bin/python
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import re


class ParseByRecentVersion(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.is_parent_href_scanned = False
        self.app_recent_version_href = ''
        self.is_finish = False

    def handle_starttag(self, tag, attrs):
        # print('begin tab:' + tag)
        if tag == 'a':
            for attr in attrs:
                if self.is_parent_href_scanned and (not self.is_finish):
                    self.app_recent_version_href = attr[1]
                    self.is_finish = True

                if attr[0] == 'href' and attr[1] == '../':
                    print('attr=', attr)
                    self.is_parent_href_scanned = True


class ParseByBuildNumber(HTMLParser):
    def error(self, message):
        pass

    def __init__(self, build_number):
        HTMLParser.__init__(self)
        self.is_parent_href_scanned = False
        self.app_recent_version_href = ''
        self.is_recent_finish = False
        self.is_match_finish = False
        self.is_build_number_matched = False
        self.build_number = build_number

    def handle_starttag(self, tag, attrs):
        # print('begin tab:' + tag)
        if tag == 'a':
            for attr in attrs:
                # print('attr=',attr)
                if not self.is_build_number_matched and not self.is_match_finish:
                    s = re.search(r'.*-%s-.*' % self.build_number, attr[1])
                    if s is not None:
                        print(s)
                        self.app_recent_version_href = attr[1]
                        self.is_match_finish = True

                if self.is_parent_href_scanned and (not self.is_recent_finish):
                    self.app_recent_version_href = attr[1]
                    self.is_recent_finish = True

                if attr[0] == 'href' and attr[1] == '../':
                    print('attr=', attr)
                    self.is_parent_href_scanned = True
