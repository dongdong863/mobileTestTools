from html_parse_util import *
from urllib import request


app_url = 'http://repo.yypm.com/dwbuild/mobile/android/entmobile/entmobile-android_7.19.0_earning_feature/'
res = request.urlopen(app_url)
html = str(res.read())
print(html)
hp_util = HTMLParseUtil()
hp_util.feed(html)
print(hp_util.app_recent_version_href)