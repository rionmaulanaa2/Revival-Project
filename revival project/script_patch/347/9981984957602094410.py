# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/NaverCafeManager.py
from __future__ import absolute_import
from __future__ import print_function
import os
import game3d
from common.framework import Singleton

class NaverCafeManager(Singleton):
    ALIAS_NAME = 'naver_cafe'

    def init(self):
        self._is_success_fully_inited = False
        self._is_in_registering = False
        self._open_homepage_after_registered = False
        self._cur_language_tag = None
        return

    def register_korean_cafe(self):
        if self._is_in_registering:
            return False
        data = {'methodId': 'init','tag': 'cafe',
           'cafeId': 29845859,
           'clientId': 'jfMUaT47COiNCJe_q1nH',
           'clientSecret': 'Bt9tzl_BxI',
           'useScreenshot': False,
           'useVideoRecord': False
           }
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            data.update({'urlScheme': 'com.netease.g93na'
               })
        self._is_in_registering = True
        log_error('cafe register_korean_cafe', data)
        global_data.channel.extend_func_by_dict(data)
        return True

    def cafe_extend_func_result(self, json_data):
        log_error('cafe_extend_func_result', json_data)
        methodId = json_data.get('methodId', '')
        tag = json_data.get('tag', '')
        if tag != 'cafe':
            return
        if methodId == 'init':
            self._is_in_registering = False
            self._is_success_fully_inited = json_data.get('result')
            if self._open_homepage_after_registered:
                self._open_homepage_after_registered = False
                self.open_community_homepage()
        elif methodId == 'onSdkStarted':
            self.on_open_community_homepage()
        elif methodId == 'onSdkStopped':
            self.on_close_community_homepage()

    def on_open_community_homepage(self):
        pass

    def check_homepage_is_show(self):
        data = {'methodId': 'isShowGlink','tag': 'cafe'}
        self.set_data(data)

    def on_close_community_homepage(self):
        if hasattr(game3d, 'set_locale_by_language_tag'):
            if self._cur_language_tag:
                game3d.set_locale_by_language_tag(self._cur_language_tag)

    def open_community_homepage(self):
        if not self._is_success_fully_inited:
            self._open_homepage_after_registered = True
            self.register_korean_cafe()
            return
        if hasattr(game3d, 'get_locale_language_tag'):
            self._cur_language_tag = game3d.get_locale_language_tag()
            game3d.set_locale_by_language_tag('ko-KR')
        self.set_landscape()
        data = {'methodId': 'startHome','tag': 'cafe'}
        log_error('cafe open_community_homepage')
        self.set_data(data)

    def close_community_homepage(self):
        data = {'methodId': 'stopHome','tag': 'cafe'}
        self.set_data(data)

    def show_float_widget(self):
        data = {'methodId': 'startWidget','tag': 'cafe'}
        self.set_data(data)

    def hide_float_widget(self):
        data = {'methodId': 'stopWidget','tag': 'cafe'}
        self.set_data(data)

    def set_landscape(self):
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            data = {'methodId': 'setLandscape','tag': 'cafe','isLandscape': 1}
            self.set_data(data)

    def set_data(self, data):
        if not self._is_success_fully_inited:
            log_error('Should wait for cafe inited!!!!')
            return
        global_data.channel.extend_func_by_dict(data)

    def test_data(self):
        data = {'methodId': 'init',
           'tag': 'cafe',
           'cafeId': 29845859,
           'clientId': 'jfMUaT47COiNCJe_q1nH',
           'clientSecret': 'Bt9tzl_BxI',
           'useScreenshot': False,
           'useVideoRecord': False
           }
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            data.update({'urlScheme': 'com.netease.g93na'
               })
        from logic.gcommon.utility import enhance_class

        class enhance(object):

            def bb_extend_function_callback(self, json_data, *args):
                print('XXXXX', json_data, args)

        from common.platform.channel import Channel
        enhance_class(Channel, enhance)
        global_data.channel._channel.extend_callback = global_data.channel.bb_extend_function_callback
        channel = global_data.channel._channel
        import json
        json_data = json.dumps(data)
        print('\xe4\xbc\xa0\xe7\xbb\x99\xe5\xbc\x95\xe6\x93\x8e\xe7\x9a\x84json', json_data)
        channel.extend_func(json_data)