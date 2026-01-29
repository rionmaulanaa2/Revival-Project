# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/HuyaLivePlatform.py
from __future__ import absolute_import
import six
from .LivePlatform import LivePlatformBase
from logic.gcommon.common_const import liveshow_const
from logic.vscene.part_sys.live.LivePlatform import LiveChannelBase
import logic.gcommon.time_utility as t_util
import game3d
import copy

class HuyaLiveChannel(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(HuyaLiveChannel, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)

    def channel_request_live_list(self, req_page):
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        plat = LivePlatformManager().get_platform_by_type(self.platform_type)
        if plat:
            plat.channel_request_live_list(req_page)

    def channel_request_label_live_list(self, labelid, req_page):
        raise NotImplementedError('huya sdk Not support:%s, %s' % (str(labelid), str(req_page)))


class HuyaLiveChannelNonSDK(LiveChannelBase):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        super(HuyaLiveChannelNonSDK, self).__init__(platform_type, labelid, _start_page_index, type, name, data)
        self._all_live_cache.set_has_total_page(False)

    def channel_request_label_live_list(self, labelid, req_page):
        raise NotImplementedError('DouyuLiveChannel Not support:%s, %s' % (str(labelid), str(req_page)))


class HuyaLivePlatform(LivePlatformBase):
    LIVE_TYPE = liveshow_const.HUYA_LIVE
    SUPPORT_EXPIRED_TIME = False
    METHODID_LIST = [
     'initLive', 'startLive', 'getLiveListData', 'getLiveData', 'receiveDanmu', 'endLive']

    def __init__(self):
        super(HuyaLivePlatform, self).__init__()
        self._in_request_live_room_data = {}
        self.init_rule()
        self._follow_convert_rule = self.generate_follow_anchor_convert_rule()
        self.init()

    def init_rule(self):
        from_rule = {'cover': 'coverUrl',
           'nickname': 'nickName',
           'hot_score': 'audienceCount',
           'uid': 'uid',
           'head': 'avatar',
           'channel_id': 'channelId',
           'game_id': 'gameId',
           'sub_id': 'subId',
           'title': 'title'
           }
        func_rule = {'islive': lambda x: True if x.get('line') else False,
           'need_request': lambda x: True if x.get('line', True) else False,
           'source': self.sort_line_info,
           'follow_uid': lambda x: str(x.get('follow_uid') or x.get('uid'))
           }
        self._convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def generate_follow_anchor_convert_rule(self):
        from_rule = {'cover': 'rimg',
           'nickname': 'uname',
           'hot_score': 'hot',
           'rid': 'rid',
           'head': 'uimg',
           'title': 'rname',
           'uid': 'uid',
           'follow_uid': 'follow_uid'
           }
        func_rule = {'need_request': lambda x: True,
           'islive': lambda x: True
           }
        _convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            _convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            _convert_rule[key] = func

        return _convert_rule

    def get_custom_follow_convert_rule(self):
        return self._follow_convert_rule

    def sort_line_info(self, live_data):
        new_source_list = []
        line_list = live_data.get('line', {})
        for line in line_list:
            channel_name = line.get('quality')
            line_ind = line.get('lineIndex')
            if line_ind:
                channel_name = channel_name + get_text_by_id(15841, (line_ind,))
            mobile_url = line.get('flvURL') or line.get('hlsURL')
            if not mobile_url:
                continue
            new_source_list.append({'vbr_channel': channel_name,'mobile_url': mobile_url})

        return new_source_list

    def channel_class(self):
        return HuyaLiveChannel

    def is_inited(self):
        return self._is_inited

    def is_live_inited(self):
        return self._is_inited

    def init(self):
        self._is_inited = False
        self.set_register_extend_enable(self.METHODID_LIST, True)
        huaya_init_command = {'methodId': 'initLive',
           'gameId': 5411,
           'appId': 'huya_app_547 ',
           'appKey': '75c00830',
           'landscapeMode': True,
           'hidePauseBtn': False,
           'channel': 'huya_live'
           }
        if global_data.need_huya_wzry:
            huaya_init_command = {'methodId': 'initLive','gameId': 2336,
               'appId': '123456',
               'appKey': 'fasdfasdfa',
               'landscapeMode': True,
               'hidePauseBtn': False,
               'channel': 'huya_live'
               }
        global_data.channel.extend_func_by_dict(huaya_init_command)

    def destroy(self):
        self.set_register_extend_enable(self.METHODID_LIST, False)

    def extend_func_callback(self, json_dict):
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        methodId = json_dict.get('methodId', '')
        channel = json_dict.get('channel')
        if channel and channel != 'huya_live':
            return
        else:
            if methodId == 'initLive':
                self._is_inited = True
                global_data.emgr.live_platform_inited_event.emit(self.LIVE_TYPE)
            elif methodId == 'getLiveListData':
                live_list = copy.deepcopy(json_dict.get('list', []))
                is_refresh = json_dict.get('isRefresh', False)
                if is_refresh:
                    LivePlatformManager().receive_live_data(self.LIVE_TYPE, 1, None, live_list)
                else:
                    LivePlatformManager().receive_live_data(self.LIVE_TYPE, None, None, live_list)
            elif methodId == 'getLiveData':
                live_data = copy.deepcopy(json_dict)
                live_data = self.convert_to_common_live_data(live_data)
                self.merge_live_room_data_into_live_data(live_data)
                global_data.emgr.receive_live_room_data_event.emit(self.LIVE_TYPE, live_data)
            elif methodId == 'receiveDanmu':
                channel_id = None
                danmu_data = self.convert_danmu_content(json_dict)
                if danmu_data:
                    global_data.emgr.live_danmu_msg_event.emit(channel_id, danmu_data)
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                if methodId == 'startLive':
                    global_data.sound_mgr.set_check_mute_enable(False)
                elif methodId == 'endLive':
                    global_data.sound_mgr.set_check_mute_enable(True)
            return

    def merge_live_room_data_into_live_data(self, live_data):
        if self._in_request_live_room_data:
            if str(self._in_request_live_room_data.get('uid')) == str(live_data.get('uid')):
                for key, value in six.iteritems(self._in_request_live_room_data):
                    if key not in live_data:
                        live_data[key] = value

    def convert_danmu_content(self, data):
        if 'nickName' not in data:
            return {}
        return {'list': [
                  {'nick': data.get('nickName', ''),'msg_body': data.get('danmuContent', '')
                     }]
           }

    def get_desc_name(self):
        return get_text_local_content(15830)

    def get_desc(self):
        return {'name': self.get_desc_name()}

    def channel_request_live_list(self, req_page):
        if not self.is_inited():
            return
        command = {'methodId': 'getLiveListData',
           'isRefresh': False if req_page and req_page > 1 else True,
           'channel': 'huya_live'
           }
        self.commit_channel_cmd(command)

    def channel_request_follow_anchor_live_list(self, req_page):
        pass

    def request_live_room_data(self, live_data):
        self._in_request_live_room_data = live_data
        uid = live_data.get('uid')
        if uid:
            cmd = {'methodId': 'getLiveData','uid': uid,
               'needFlv': True,
               'channel': 'huya_live'
               }
            self.commit_channel_cmd(cmd)

    def is_support_live_broadcast(self):
        import game3d
        if game3d.get_platform() in [game3d.PLATFORM_WIN32] or global_data.is_android_pc:
            return False
        return True

    def start_live_broadcast(self):
        if not self.is_inited():
            return
        command = {'methodId': 'startLive','needRecommend': False,
           'channel': 'huya_live'
           }
        self.commit_channel_cmd(command)

    def set_enable_danmu(self, uid, is_enable):
        if not self.is_inited():
            return
        command = {'methodId': 'receiveDanmu','uid': uid,
           'enable': is_enable,
           'channel': 'huya_live'
           }
        self.commit_channel_cmd(command)

    def send_live_dammu(self, msg, uid, channelId, subId):
        if not self.is_inited():
            return
        else:
            cmd = {'methodId': 'sendDanmu',
               'uid': uid,
               'channelId': channelId,
               'subId': subId,
               'text': msg,
               'channel': 'huya_live'
               }
            self.commit_channel_cmd(cmd)
            self_msg = {'list': [
                      {'nick': global_data.player.get_name(),'msg_body': msg
                         }]
               }
            global_data.emgr.live_danmu_msg_event.emit(None, self_msg)
            return


class HuyaLivePlatformNonSDK(LivePlatformBase):
    LIVE_TYPE = liveshow_const.HUYA_LIVE
    SUPPORT_DANMU = False

    def __init__(self):
        super(HuyaLivePlatformNonSDK, self).__init__()
        self._in_request_live_room_data = {}
        self.init_rule()
        self.generate_raw_rule()

    def init_rule(self):
        from_rule = {'cover': 'rimg',
           'nickname': 'uname',
           'hot_score': 'hot',
           'rid': 'rid',
           'head': 'uimg',
           'title': 'rname',
           'uid': 'uid',
           'follow_uid': 'follow_uid'
           }
        func_rule = {'need_request': lambda x: True,
           'islive': lambda x: True
           }
        self._convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            self._convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            self._convert_rule[key] = func

    def channel_class(self):
        return HuyaLiveChannelNonSDK

    def require_live_labels(self):
        pass

    def request_live_room_data(self, live_data):
        self._in_request_live_room_data = live_data
        has_token = self.check_has_valid_douyu_token()
        if not has_token:
            self.request_live_param()
            return
        self.request_live_room_data_with_token(live_data)

    def __build_sign(self, data_str, secret):
        import hashlib
        sign_string = [
         'data=', data_str, '&key=', str(secret)]
        sign_string = ''.join(sign_string).encode(encoding='utf-8')
        import six
        sign_md5 = hashlib.md5(six.ensure_binary(sign_string))
        sign = sign_md5.hexdigest()
        return sign

    def url_pack_helper(self, uid, host=''):
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        from logic.gutils.live_utils import cal_sort_param_text
        from logic.gcommon import time_utility as tutil
        import json
        data = {'pid': int(uid)}
        data_str = json.dumps(data, separators=(',', ':'), sort_keys=True)
        secret = self._live_param.get('app_key', 'app_key')
        sign = self.__build_sign(data_str, secret)
        param_text = six.moves.urllib.parse.urlencode({'data': data_str,'appId': self._live_param.get('app_id', 'appId'),'sign': sign})
        _url = host + '&' + param_text
        return _url

    def request_live_room_data_with_token(self, live_data):
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        import hashlib
        import json
        uid = live_data.get('uid', 0)
        _url = self.url_pack_helper(uid, host='http://open.huya.com/cache.php?m=Live&do=getLiveInfo')
        import common.http

        def callback(ret, url, args):
            try:
                ret_dict = json.loads(ret)
                code = ret_dict.get('code', 0)
                msg = ret_dict.get('msg', '')
                data = ret_dict.get('data', {})
            except:
                log_error('huya live request error', ret)
                data = None
                code = None

            if data and code == 0:
                import game3d
                game3d.delay_exec(1, lambda : self.receive_room_data(data))
            return

        common.http.request_v2(_url, None, {}, callback)
        return

    def check_has_valid_douyu_token(self):
        if not self._live_param or self._live_param.get('expire_time', 0) < t_util.get_server_time():
            return False
        else:
            return True

    def on_receive_live_param(self):
        if self._in_request_live_room_data:
            self.request_live_room_data_with_token(self._in_request_live_room_data)

    def receive_room_data(self, _dict):
        if not self._in_request_live_room_data or not str(self._in_request_live_room_data.get('uid')) == str(_dict.get('uid')):
            log_error('receive_room_data unmatched!')
            return
        live_data = self.convert_to_common_live_data(_dict, self._raw_convert_rule)
        global_data.emgr.receive_live_room_data_event.emit(self.LIVE_TYPE, live_data)

    def is_support_live_broadcast(self):
        import game3d
        if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc:
            return False
        return True

    def start_live_broadcast(self):
        import game3d
        self._wait_for_live_broadcast = True
        json = {'methodId': 'initLive',
           'appId': 'jddsaef',
           'appKey': 'Q6khSIe4wiTNnnOrqxgjda4s',
           'needWindow': True,
           'windowType': 1,
           'channel': 'douyu_broadcast_live'
           }
        self.commit_channel_cmd(json)

    def extend_func_callback(self, json_dict):
        methodId = json_dict.get('methodId', '')
        channel = json_dict.get('channel')
        if channel and channel != 'douyu_broadcast_live':
            return
        if methodId == 'initLive':
            json = {'methodId': 'startLive','channel': 'douyu_broadcast_live'
               }
            self.commit_channel_cmd(json)

    def generate_raw_rule(self):
        from_rule = {'cover': 'screenshot',
           'nickname': 'nick',
           'hot_score': 'totalCount',
           'uid': 'uid',
           'head': 'avatar180',
           'channel_id': 'channel',
           'game_id': 'gid',
           'title': 'roomName'
           }
        func_rule = {'islive': lambda x: True if x.get('flvInfo') else False,
           'need_request': lambda x: True if x.get('line', True) else False,
           'anchor_id': lambda x: x.get('uid'),
           'source': self.sort_line_info,
           'follow_uid': lambda x: str(x.get('follow_uid') or x.get('uid'))
           }
        _convert_rule = {}
        for key, new_key in six.iteritems(from_rule):
            _convert_rule[new_key] = key

        for key, func in six.iteritems(func_rule):
            _convert_rule[key] = func

        self._raw_convert_rule = _convert_rule

    def sort_line_info(self, live_data):
        new_source_list = []
        line_list = live_data.get('flvInfo', [])
        for line in line_list:
            ratios = line.get('ratios', [])
            if ratios:
                channel_name = ratios[0].get('displayName', '')
                ratio = ratios[0].get('ratio', 0)
            else:
                channel_name = 'standard'
                ratio = 1000
            line_ind = line.get('lineIndex', 0)
            if line_ind:
                channel_name = channel_name + get_text_by_id(15841, (line_ind,))
            mobile_url = line.get('url')
            if not mobile_url:
                continue
            new_source_list.append({'vbr_channel': channel_name,'mobile_url': mobile_url,'ratio': ratio})

        new_source_list = sorted(new_source_list, key=lambda x: x.get('ratio', 0), reverse=True)
        return new_source_list

    def set_enable_danmu(self, uid, is_enable):
        pass

    def send_live_dammu(self, msg, uid, channelId, subId):
        pass