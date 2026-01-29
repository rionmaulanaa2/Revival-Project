# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/web_browser.py
from __future__ import absolute_import
from __future__ import print_function
import social
import game3d
from common.platform import is_win32

class WebBrowser(object):
    instance = None

    @staticmethod
    def get_instance():
        if WebBrowser.instance is None:
            WebBrowser.instance = WebBrowser()
        return WebBrowser.instance

    def __init__(self):
        if is_win32():
            return
        self._channel = social.get_channel()

    def open_web_view(self, url, callback):
        if is_win32():
            print('>>> cannot open web view on pc !!!')
            return
        self._channel.open_web_view(url)
        self._channel.web_view_callback = callback

    def open_new_web_view(self, url):
        try:
            game3d.open_web_view(url, False)
        except Exception as e:
            log_error('open_web_view failed. %s' % str(e))
            return

    def open_out_web(self, url):
        game3d.open_url(url)