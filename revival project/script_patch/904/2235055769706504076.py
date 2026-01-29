# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/DouyuLivePlatform.py
from __future__ import absolute_import
import six
from .LivePlatform import LivePlatformBase
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LivePlatform import LiveChannelBase
import logic.gcommon.time_utility as t_util
from logic.gutils.live_utils import cal_sort_param_sign, cal_sort_param_text, url_pack_helper
import game3d

class DouyuLiveChannel(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(DouyuLiveChannel, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)

    def channel_request_label_live_list(self, labelid, req_page):
        raise NotImplementedError('DouyuLiveChannel Not support:%s, %s' % (str(labelid), str(req_page)))


class DouyuLivePlatform(LivePlatformBase):
    LIVE_TYPE = liveshow_const.DOUYU_LIVE
    METHODID_LIST = ['initLive', 'startLive']
    SUPPORT_DANMU = False

    def __init__(self):
        super(DouyuLivePlatform, self).__init__()
        self._in_request_live_room_data = {}
        self._is_inited = False
        self.set_register_extend_enable(self.METHODID_LIST, True)
        self.init_rule()
        self.generate_raw_rule()

    def destroy(self):
        self.set_register_extend_enable(self.METHODID_LIST, False)

    def init_rule(self):
        from_rule = {'cover': 'rimg',
           'nickname': 'uname',
           'hot_score': 'hot',
           'rid': 'rid',
           'head': 'uimg',
           'title': 'rname'
           }
        func_rule = {'need_request': lambda x: False if x.get('live_url') or x.get('flv_mul') else True,
           'islive': lambda x: x.get('show_status') == 1 or x.get('live_url') or x.get('flv_mul'),
           'source': lambda x: self.generate_vbr_info(x),
           'follow_uid': lambda x: str(x.get('follow_uid') or x.get('rid')),
           'uid': lambda x: x.get('rid')
           }
        self._convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def generate_raw_rule(self):
        from_rule = {'rid': 'rid'
           }
        func_rule = {'islive': lambda x: x.get('show_status') == 1 or x.get('live_url') or x.get('flv_mul'),
           'need_request': lambda x: False if x.get('live_url') or x.get('flv_mul') else True,
           'source': lambda x: self.generate_vbr_info(x),
           'follow_uid': lambda x: str(x.get('rid')),
           'uid': lambda x: x.get('rid')
           }
        _convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            _convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            _convert_rule[key] = func

        self._raw_convert_rule = _convert_rule

    def channel_class(self):
        return DouyuLiveChannel

    def require_live_labels(self):
        pass

    def request_live_room_data(self, live_data):
        self._in_request_live_room_data = live_data
        has_token = self.check_has_valid_douyu_token()
        if not has_token:
            self.request_live_param()
            return
        self.request_live_room_data_with_token(live_data)

    def url_pack_helper(self, interface_url, host='https://openapi.douyu.com'):
        from logic.gcommon import time_utility as tutil
        param = {'aid': self._live_param.get('aid', 'aid'),'time': int(tutil.get_server_time()),'token': self._live_param.get('token', 'token')
           }
        secret = self._live_param.get('secret', '')
        _url = url_pack_helper(param, secret, interface_url, host, 'auth')
        return _url

    def request_live_room_data_with_token(self, live_data):
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        import hashlib
        import json
        interface_url = '/api/thirdPart/getPlay'
        _url = self.url_pack_helper(interface_url)
        import common.http

        def callback(ret, url, args):
            try:
                ret_dict = json.loads(ret)
                code = ret_dict.get('code', 0)
                msg = ret_dict.get('msg', '')
                data = ret_dict.get('data', {})
            except:
                log_error('douyu live request error', ret)
                data = None
                code = None

            if data and code == 0:
                import game3d
                game3d.delay_exec(1, lambda : self.receive_room_data(data))
            return

        header = {'content-type': 'application/json'}
        body = {'rid': live_data.get('rid', '')}
        body_str = json.dumps(body)
        common.http.request_v3(_url, body_str, header, callback)

    def check_has_valid_douyu_token(self):
        if not self._live_param or self._live_param.get('expire_time', 0) < t_util.get_server_time():
            return False
        else:
            return True

    def on_receive_live_param(self):
        if self._in_request_live_room_data:
            self.request_live_room_data_with_token(self._in_request_live_room_data)

    def receive_room_data(self, _dict):
        if not self._in_request_live_room_data or not str(self._in_request_live_room_data.get('rid')) == str(_dict.get('rid')):
            log_error('receive_room_data unmatched!')
            return
        live_data = _dict
        live_data = self.convert_to_common_live_data(live_data, self._raw_convert_rule)
        self.merge_live_room_data_into_live_data(live_data)
        global_data.emgr.receive_live_room_data_event.emit(self.LIVE_TYPE, live_data)

    def merge_live_room_data_into_live_data(self, live_data):
        if self._in_request_live_room_data:
            if str(self._in_request_live_room_data.get('rid')) == str(live_data.get('rid')):
                for key, value in six.iteritems(self._in_request_live_room_data):
                    if key not in live_data:
                        live_data[key] = value

    def generate_vbr_info(self, live_data):
        if not (live_data.get('live_url') or live_data.get('flv_mul')):
            return []
        return [{'vbr_channel': get_text_by_id(80806),'mobile_url': live_data.get('live_url', '')}]

    def batch_request_room_info_with_token(self, int_rids):
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        import hashlib
        import json
        interface_url = '/api/thirdPart/batchGetRoomInfo'
        _url = self.url_pack_helper(interface_url)
        import common.http

        def callback(ret, url, args):
            try:
                ret_dict = json.loads(ret)
                code = ret_dict.get('code', 0)
                msg = ret_dict.get('msg', '')
                data = ret_dict.get('data', {})
            except:
                log_error('douyu live request error', ret)
                data = None
                code = None

            if data and code == 0:
                import game3d
                game3d.delay_exec(1, lambda : self.receive_batch_room_data(data))
            return

        header = {'content-type': 'application/json'}
        body = {'rids': int_rids}
        body_str = json.dumps(body)
        common.http.request_v3(_url, body_str, header, callback)

    def is_support_live_broadcast(self):
        return False

    def start_live_broadcast(self):
        import game3d
        self._wait_for_live_broadcast = True
        if not self._is_inited:
            json = {'methodId': 'initLive','appId': 'jddsaef',
               'appKey': 'Q6khSIe4wiTNnnOrqxgjda4s',
               'needWindow': True,
               'windowType': 1,
               'channel': 'douyu_broadcast_live'
               }
            self.commit_channel_cmd(json)
        else:
            json = {'methodId': 'startLive',
               'channel': 'douyu_broadcast_live'
               }
            self.commit_channel_cmd(json)

    def extend_func_callback(self, json_dict):
        methodId = json_dict.get('methodId', '')
        channel = json_dict.get('channel')
        if channel and channel != 'douyu_broadcast_live':
            return
        if methodId == 'initLive':
            if json_dict.get('result'):
                self._is_inited = True
                json = {'methodId': 'startLive',
                   'channel': 'douyu_broadcast_live'
                   }
                self.commit_channel_cmd(json)
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            if methodId == 'startLive':
                if json_dict.get('result'):
                    global_data.sound_mgr.set_check_mute_enable(False)
            elif methodId == 'closeLiveEvent':
                global_data.sound_mgr.set_check_mute_enable(True)