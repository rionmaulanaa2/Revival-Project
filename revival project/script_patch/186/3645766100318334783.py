# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/KuaishouLivePlatform.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from .LivePlatform import LivePlatformBase
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LivePlatform import LiveChannelBase
import logic.gcommon.time_utility as t_util
import game3d

class KuaishouLiveChannel(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(KuaishouLiveChannel, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)

    def channel_request_label_live_list(self, labelid, req_page):
        raise NotImplementedError('%s Not support:%s, %s' % (self.__class__.__name__, str(labelid), str(req_page)))


class KuaishouLivePlatform(LivePlatformBase):
    SUPPORT_DANMU = False
    LIVE_TYPE = liveshow_const.KUAISHOU_LIVE
    METHODID_LIST = ['initLive', 'loginLive', 'startLive']

    def __init__(self):
        super(KuaishouLivePlatform, self).__init__()
        self._is_live_inited = False
        self._is_login = False
        self.init_rule()
        self.init()

    def init_rule(self):
        from_rule = {'cover': 'rimg',
           'nickname': 'uname',
           'hot_score': 'hot',
           'uid': 'uid',
           'head': 'uimg',
           'room_id': 'rid',
           'title': 'rname',
           'follow_uid': 'follow_uid'
           }
        func_rule = {'islive': lambda x: True if x.get('urls') else False,
           'source': lambda x: self.generate_source(x)
           }
        self._convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def channel_class(self):
        return KuaishouLiveChannel

    def require_live_labels(self):
        pass

    def init(self):
        self.set_register_extend_enable(self.METHODID_LIST, True)

    def destroy(self):
        self.set_register_extend_enable(self.METHODID_LIST, False)
        super(KuaishouLivePlatform, self).destroy()

    def generate_source(self, live_data):
        new_source_list = []
        line_dict = live_data.get('urls', {})
        ls = [
         'super', 'high', 'standard']

        def com_func(key):
            key = key.lower()
            if key in ls:
                return ls.index(key)
            else:
                return 1000

        sort_keys = sorted(six_ex.keys(line_dict), key=com_func)
        for key in sort_keys:
            new_source_list.append({'vbr_channel': key.lower(),'mobile_url': line_dict[key]})

        return new_source_list

    def is_live_inited(self):
        return self._is_live_inited

    def start_live_broadcast(self):
        if not self._is_live_inited:
            self._init_sdk()
        elif not self._is_login:
            self._init_login()
        else:
            self._start_live()

    def _init_sdk(self):
        dic = {'methodId': 'initLive',
           'gameName': get_text_by_id(1111),
           'debug': True,
           'channel': 'kuaishou_broadcast_live'
           }
        self.commit_channel_cmd(dic)

    def _init_login(self):
        dic = {'methodId': 'loginLive',
           'channel': 'kuaishou_broadcast_live'
           }
        self.commit_channel_cmd(dic)

    def _start_live(self):
        dic = {'methodId': 'startLive',
           'isLandscape': True,
           'channel': 'kuaishou_broadcast_live'
           }
        self.commit_channel_cmd(dic)

    def extend_func_callback(self, json_dict):
        methodId = json_dict.get('methodId', '')
        print(('ks extend_func_callback', json_dict))
        channel = json_dict.get('channel')
        if channel and channel != 'kuaishou_broadcast_live':
            return
        result = json_dict.get('result', False)
        if not result:
            log_error('kuaishou broadcast live failed', json_dict)
        if methodId == 'initLive':
            result = json_dict.get('result', False)
            if result:
                self._is_live_inited = True
                if not self._is_login:
                    self._init_login()
            else:
                global_data.game_mgr.show_tip(json_dict.get('ksErrMsg', 'Error'))
                log_error('kuaishou broadcast live failed', json_dict)
        elif methodId == 'loginLive':
            result = json_dict.get('result', False)
            if result:
                self._is_login = True
                self._start_live()
        elif methodId == 'startLive':
            pass

    def is_support_live_broadcast(self):
        return True