# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/BLBLLivePlatform.py
from __future__ import absolute_import
import six
from .LivePlatform import LivePlatformBase
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LivePlatform import LiveChannelBase
import logic.gcommon.time_utility as t_util
from logic.gutils.live_utils import cal_sort_param_sign, cal_sort_param_text, url_pack_helper
from common.platform.device_info import DeviceInfo

class BLBLLiveChannel(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(BLBLLiveChannel, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)

    def channel_request_label_live_list(self, labelid, req_page):
        raise NotImplementedError('%s Not support:%s, %s' % (self.__class__.__name__, str(labelid), str(req_page)))


class BLBLLivePlatform(LivePlatformBase):
    LIVE_TYPE = liveshow_const.BILIBILI_LIVE
    SUPPORT_DANMU = False

    def __init__(self):
        super(BLBLLivePlatform, self).__init__()
        self.init_rule()

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
        func_rule = {'islive': lambda x: True if x.get('live_status') == 1 else False,
           'need_request': lambda x: True if x.get('line', True) else False,
           'source': lambda x: self.generate_vbr_info(x)
           }
        self._convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def channel_class(self):
        return BLBLLiveChannel

    def require_live_labels(self):
        pass

    def request_live_room_data(self, live_data):
        self._in_request_live_room_data = live_data
        has_token = self.check_has_valid_BLBL_token()
        if not has_token:
            self.request_live_param()
            return
        self.request_live_room_data_with_token(live_data)

    def check_has_valid_BLBL_token(self):
        if not self._live_param:
            return False
        else:
            return True

    def on_receive_live_param(self):
        if self._in_request_live_room_data:
            self.request_live_room_data_with_token(self._in_request_live_room_data)

    def request_live_room_data_with_token(self, live_data):
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        import hashlib
        import json
        device_info = DeviceInfo()
        from logic.gutils.version_utils import get_integer_script_version
        special_char = [
         '+', '/', '?', '&', '#', '&', '=', ' ']
        device_name = device_info.get_device_model_name()
        os_name = device_info.get_os_name()
        for each in special_char:
            device_name = device_name.replace(each, '_')
            os_name = os_name.replace(each, '_')

        interface_url = '/xlive/app-room/v1/index/getCooInfoByRoom'
        param = {'room_id': int(live_data.get('room_id', '123')),'uid': int(live_data.get('uid', '123')),
           'platform': os_name or 'ios',
           'build': get_integer_script_version() or 1000,
           'device': device_name or 'iPhone10',
           'from': 'jddsaef',
           'ts': str(int(t_util.get_server_time() - 2))
           }
        secret = self._live_param.get('secret', 'secret')
        _url = url_pack_helper(param, secret, interface_url, 'http://api.live.bilibili.com', 'token', sign_need_interface_url=False)
        import common.http

        def callback(ret, url, args):
            try:
                ret_dict = json.loads(ret)
                code = ret_dict.get('code', 0)
                msg = ret_dict.get('msg', '')
                data = ret_dict.get('data', {})
            except:
                log_error('BLBL live request error', ret)
                data = None
                code = None

            if data and code == 0:
                import game3d
                game3d.delay_exec(1, lambda : self.receive_room_data(data))
            return

        header = {'x-user-ip': str(device_info.get_ip())}
        common.http.request_v3(_url, None, header, callback)
        return

    def receive_room_data(self, _dict):
        _dict = self.raw_data_to_live_room_data(_dict)
        if not self._in_request_live_room_data or not str(self._in_request_live_room_data.get('uid')) == str(_dict.get('uid')):
            log_error('receive_room_data unmatched!')
            return
        live_data = _dict
        self.merge_live_room_data_into_live_data(live_data)
        global_data.emgr.receive_live_room_data_event.emit(self.LIVE_TYPE, live_data)

    def raw_data_to_live_room_data(self, raw_dict):
        room_info = raw_dict.get('room_info', {})
        play_info = raw_dict.get('play_info', {})
        anchor_info = raw_dict.get('anchor_info', {}) or {}
        base_info = anchor_info.get('base_info', {}) or {}
        new_dict = {'cover': room_info.get('cover', ''),
           'hot_score': room_info.get('online', 0),
           'room_id': room_info.get('room_id', 123),
           'uid': room_info.get('uid', 123),
           'islive': play_info.get('live_status', 1) == 1,
           'need_request': False,
           'anchor_id': room_info.get('uid', 123),
           'source': self.generate_vbr_info(raw_dict),
           'head': base_info.get('face', ''),
           'follow_uid': room_info.get('uid', 123)
           }
        return new_dict

    def merge_live_room_data_into_live_data(self, live_data):
        if self._in_request_live_room_data:
            if str(self._in_request_live_room_data.get('uid')) == str(live_data.get('uid')):
                for key, value in six.iteritems(self._in_request_live_room_data):
                    if key not in live_data:
                        live_data[key] = value

    def generate_vbr_info(self, live_data):
        if not live_data.get('play_info'):
            return []
        return [{'vbr_channel': get_text_by_id(80806),'mobile_url': live_data.get('play_info', {}).get('play_url', '')}]