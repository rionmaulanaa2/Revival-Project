# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/CCLivePlatform.py
from __future__ import absolute_import
import six
from .LivePlatform import LivePlatformBase
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LivePlatform import LiveChannelBase
import logic.gcommon.time_utility as t_util
import game3d

class CCLiveChannel(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(CCLiveChannel, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)


class CCLivePlatform(LivePlatformBase):
    LIVE_TYPE = liveshow_const.CC_LIVE
    METHODID_LIST = ['ccVideoLiveConvertor', 'getUserTicket']

    def __init__(self):
        super(CCLivePlatform, self).__init__()
        self._is_broadcast_inited = False
        self.set_register_extend_enable(self.METHODID_LIST, True)
        self.init_rule()

    def destroy(self):
        self.set_register_extend_enable(self.METHODID_LIST, False)
        super(CCLivePlatform, self).destroy()

    def init_rule(self):
        remain_list = [
         'follow_uid', 'uid', 'channel_id']
        from_rule = {'anchor_id': 'ccid',
           'cover': 'rimg',
           'nickname': 'uname',
           'hot_score': 'hot',
           'rid': 'rid',
           'head': 'uimg',
           'title': 'rname'
           }
        func_rule = {'islive': lambda x: True if x.get('urls') else False,
           'mobile_url': lambda x: x.get('urls', {}).get('mobile_url', ''),
           'video_url': lambda x: x.get('urls', {}).get('video_url', '')
           }
        self._convert_rule = {}
        for key in remain_list:
            self._convert_rule[key] = key

        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def get_desc_name(self):
        return get_text_local_content(15807)

    def get_desc(self):
        return {'name': self.get_desc_name()}

    def channel_class(self):
        return CCLiveChannel

    def is_support_live_broadcast(self):
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc:
            return False
        return True

    def start_live_broadcast(self):
        json = {'methodId': 'ccVideoLiveConvertor',
           'func': 'openSDK',
           'channel': 'cc_broadcast_live',
           'gameType': '9061',
           'gameName': 'jddsaef',
           'ticketType': self.__get_ticket_type(),
           'urs': str(global_data.player.uid)
           }
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            urlScheme = {'urlScheme': 'com.netease.mpay.1kim6ej2tze0ijjt'}
        else:
            urlScheme = {}
        json.update(urlScheme)
        self.commit_channel_cmd(json)

    def __get_ticket_type(self):
        if not global_data.channel:
            return '0'
        name = global_data.channel.get_name()
        if name != 'netease':
            return '0'
        auth_type = global_data.channel.get_auth_type()
        if auth_type == 'native':
            return '1'
        if auth_type == 'mobile':
            return '7'
        return '0'

    def extend_func_callback(self, json_dict):
        methodId = json_dict.get('methodId', '')
        channel = json_dict.get('channel')
        if methodId == 'getUserTicket':
            ticket = json_dict.get('result')
            if ticket:
                cmd = {'methodId': 'ccVideoLiveConvertor','func': 'updateTicket',
                   'unisdkTicket': ticket,
                   'channel': 'cc_broadcast_live'
                   }
                self.commit_channel_cmd(cmd)
            else:
                log_error('getUserTicket failed', str(json_dict))
        if channel and channel != 'cc_broadcast_live':
            return
        if methodId == 'ccVideoLiveConvertor':
            func = json_dict.get('func', '')
            if func == 'ticketExpiredEvent':
                json = {'methodId': 'getUserTicket'}
                self.commit_channel_cmd(json)
            elif func == 'videoStateChangeEvent':
                pass
            elif func == 'recordAudioStateEvent':
                state = json_dict.get('state')
                if state == 0:
                    cmd = {'methodId': 'ccVideoLiveConvertor','func': 'restartAudioCapture',
                       'channel': 'cc_broadcast_live'
                       }
                    self.commit_channel_cmd(cmd)
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                if func == 'openLiveEvent':
                    global_data.sound_mgr.set_check_mute_enable(False)
                elif func == 'closeLiveEvent':
                    global_data.sound_mgr.set_check_mute_enable(True)
                elif func == 'closeSDKEvent':
                    global_data.sound_mgr.set_check_mute_enable(True)