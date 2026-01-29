# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/LivePlatform.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.common_const.liveshow_const import CC_LIVE, TAG_FOLLOW, TAG_ALL, TAG_PLATFORM_LABEL, FOLLOWED_ANCHOR_MAX_NUM
from common.live.live_page_cache import LivePageCache
import logic.gcommon.time_utility as t_util
import game3d
from logic.gcommon.common_const.liveshow_const import LIVE_LIST_EXPIRE_TIME, PAGE_REQUEST_CD
REQUIRE_CD = 1.0

class LiveChannelBase(object):

    def __init__(self, platform_type, labelid, _start_page_index, type, name, data=None):
        self.labelid = labelid
        self.platform_type = None
        self.type = type
        self.tag_data = data
        self.name = name
        self._all_live_cache = LivePageCache(_start_page_index)
        self._last_require_time = 0
        self._fetch_time = 0
        self.platform_type = platform_type
        return

    def __repr__(self):
        return str(self.type) + str(self.labelid)

    def destroy(self):
        if self._all_live_cache:
            self._all_live_cache.destroy()
            self._all_live_cache = None
        return

    def _get_exact_page_helper(self, live_cache, page):
        if page is None:
            new_page = live_cache.get_next_page_index()
        else:
            new_page = page
        return new_page

    def _get_cache_helper(self, cache, page, suc_cb, fail_cb):
        if page is not None:
            content = cache.get_page(page)
            if content is not None:
                suc_cb(content)
            elif self.check_require_data_cd():
                fail_cb(page)
            else:
                log_error('\xe4\xb8\x8d\xe6\xbb\xa1\xe8\xb6\xb3cd\xe8\xa6\x81\xe6\xb1\x82')
        return

    def notify_platform_update(self, platform_type):
        global_data.emgr.notify_platform_live_list_update_event.emit(platform_type)

    def require_channel_live_list(self, page=None):
        if not global_data.player:
            return
        new_page = self._get_exact_page_helper(self._all_live_cache, page)

        def suc_cb(content):
            self.notify_platform_update(self.platform_type)

        if self.type == TAG_ALL:

            def fail_cb(req_page):
                self._last_require_time = t_util.time()
                self.channel_request_live_list(req_page)

        elif self.type == TAG_FOLLOW:

            def fail_cb(req_page):
                self._last_require_time = t_util.time()
                self.channel_request_follow_anchor_live_list(req_page)

        else:

            def fail_cb(req_page):
                labelid = self.tag_data.get('labelid', None)
                if labelid is None:
                    return
                else:
                    self._last_require_time = t_util.time()
                    self.channel_request_label_live_list(labelid, req_page)
                    return

        self._get_cache_helper(self._all_live_cache, new_page, suc_cb, fail_cb)

    def receive_live_list(self, page, total_page, livelist):
        self._all_live_cache.set_total_page(total_page)
        self._all_live_cache.add_page(page, livelist)

    def clear_cache(self):
        self._all_live_cache.clear()

    def add_page(self, page, content):
        self._all_live_cache.add_page(page, content)

    def get_page(self, page):
        return self._all_live_cache.get_page(page)

    def set_total_page(self, total_page):
        self._all_live_cache.set_total_page(total_page)

    def get_total_page(self):
        return self._all_live_cache.get_total_page()

    def set_total_cnt(self, total_cnt):
        self._all_live_cache.set_total_cnt(total_cnt)

    def is_reach_end(self, page_size):
        return self._all_live_cache.is_reach_end(page_size)

    def get_channel_desc(self):
        return {'type': self.type,'labelid': self.labelid,'name': self.name,'data': self.tag_data}

    def check_require_data_cd(self):
        return t_util.time() - self._last_require_time > REQUIRE_CD

    def channel_request_live_list(self, req_page):
        global_data.player.request_live_room_list(self.platform_type, req_page)

    def channel_request_follow_anchor_live_list(self, req_page):
        global_data.player.require_follow_anchor_status(self.platform_type)

    def channel_request_label_live_list(self, labelid, req_page):
        global_data.player.request_live_channel_data(self.platform_type, labelid, req_page)

    def set_page_expired_time(self, page, expired_time):
        self._all_live_cache.set_page_expire_time_dict(page, expired_time)


class LivePlatformBase(object):
    SUPPORT_DANMU = True
    SUPPORT_EXPIRED_TIME = True
    LIVE_TYPE = CC_LIVE
    METHODID_LIST = []

    def __init__(self):
        self._start_page_index = 1
        self._tag_labels = []
        self._tag_channels = {}
        self._follow_anchor_list = {}
        self._convert_rule = {}
        self._live_param = {}
        self._all_channel = self.channel_class()(self.LIVE_TYPE, -1, self._start_page_index, TAG_ALL, get_text_local_content(15808))
        self._follow_channel = self.channel_class()(self.LIVE_TYPE, -1, self._start_page_index, TAG_FOLLOW, get_text_local_content(15809))
        self._raw_follow_channel_data = {}
        self._to_be_follow_anchor_data = {}

    def channel_class(self):
        return LiveChannelBase

    def is_inited(self):
        return True

    def is_live_inited(self):
        return False

    def destroy(self):
        self._start_page_index = 1
        self._tag_labels = []
        self._follow_anchor_list = {}
        self._convert_rule = {}
        self._live_param = {}
        self._raw_follow_channel_data = {}
        self._to_be_follow_anchor_data = {}
        if self._all_channel:
            self._all_channel.destroy()
            self._all_channel = None
        if self._follow_channel:
            self._follow_channel.destroy()
            self._follow_channel = None
        for tag, ch in six.iteritems(self._tag_channels):
            ch.destroy()

        self._tag_channels = {}
        return

    def get_type(self):
        return self.LIVE_TYPE

    def get_desc(self):
        pass

    def get_desc_name(self):
        raise NotImplementedError('\xe8\xaf\xb7\xe6\x8c\x87\xe6\x98\x8e\xe5\xb9\xb3\xe5\x8f\xb0\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x81')

    def get_desc_pic(self):
        pass

    def get_support_channels(self):
        chn_list = []
        all_desc = self._all_channel.get_channel_desc()
        follow_desc = self._follow_channel.get_channel_desc()
        chn_list.append(all_desc)
        chn_list.append(follow_desc)
        tag_desces = [ self._tag_channels[label['labelid']].get_channel_desc() for label in self._tag_labels ]
        chn_list.extend(tag_desces)
        return chn_list

    def get_label_live_list(self, labelid, page):
        cache = self._tag_channels.get(labelid, None)
        if cache:
            return cache.get_page(page)
        else:
            return

    def get_all_live_list(self, page):
        return self._all_channel.get_page(page)

    def get_follow_live_list(self, page):
        return self._follow_channel.get_page(page)

    def require_live_labels(self):
        pass

    def receive_live_labels(self, labels):
        self._tag_labels = labels
        self._tag_channels = {}
        for label in labels:
            self._tag_channels[label['labelid']] = self.channel_class()(self.LIVE_TYPE, label['labelid'], self._start_page_index, TAG_PLATFORM_LABEL, label['text'], label)

    def request_all_live_list(self, page=None):
        self._all_channel.require_channel_live_list(page)

    def request_follow_anchor_live_list(self, page=None):
        self._follow_channel.require_channel_live_list(page)

    def request_channel_live_list(self, label_data, page=None):
        labelid = label_data['labelid']
        if labelid in self._tag_channels:
            self._tag_channels[labelid].require_channel_live_list(page)

    def request_live_room_data(self, live_data):
        pass

    def receive_all_live_list(self, page, total_page, livelist, room_info=None):
        self._all_channel.set_total_page(total_page)
        self._all_channel.add_page(page, livelist)
        if room_info:
            fetch_time = room_info.get('fetch_time', 0)
            self._all_channel.set_page_expired_time(page, fetch_time + LIVE_LIST_EXPIRE_TIME)

    def receive_live_channel_live_list(self, labelid, page, livelist):
        if labelid in self._tag_channels:
            self._tag_channels[labelid].add_page(page, livelist)

    def set_raw_follow_channel_data_dict(self, data):
        self._raw_follow_channel_data = data

    def receive_follow_anchor_live_list(self, page, livelist_dict):
        self.set_raw_follow_channel_data_dict(livelist_dict)
        anchor_data = livelist_dict.get('anchor_status', {})
        fetch_time = livelist_dict.get('fetch_time', 0)
        sort_keys = sorted(six_ex.keys(anchor_data))
        livelist = [ anchor_data[follow_uid] for follow_uid in sort_keys if str(follow_uid) in self._follow_anchor_list ]
        out_live_list = []
        if self._follow_anchor_list:
            for follow_uid, anchor_info in six.iteritems(self._follow_anchor_list):
                if follow_uid not in anchor_data:
                    name = anchor_info.get('uname', '\xe6\x9c\xaa\xe7\x9f\xa5')
                    info_dict = {'nickname': name,'title': name,'head': anchor_info.get('uimg', ''),
                       'follow_uid': follow_uid}
                    out_live_list.append(info_dict)

        livelist.extend(out_live_list)
        self._follow_channel.add_page(page, livelist)
        from logic.gcommon.time_utility import get_server_time
        expired_time = fetch_time + LIVE_LIST_EXPIRE_TIME
        if get_server_time() - fetch_time >= LIVE_LIST_EXPIRE_TIME:
            expired_time = get_server_time() + PAGE_REQUEST_CD
        self._follow_channel.set_page_expired_time(page, expired_time)

    def get_start_page(self):
        return self._start_page_index

    def clear_all_live_cache(self):
        self._all_channel.clear_cache()

    def clear_tag_channel_cache(self):
        for channel in six.itervalues(self._tag_channels):
            channel.clear_cache()

    def clear_follow_live_cache(self):
        self._follow_channel.clear_cache()

    def clear_follow_data(self):
        self.set_raw_follow_channel_data_dict({})
        self._to_be_follow_anchor_data = {}

    def require_follow_anchor(self, follow_uid, anchor_data):
        if global_data.player:
            global_data.player.follow_anchor(self.LIVE_TYPE, follow_uid)
            self._to_be_follow_anchor_data[str(follow_uid)] = anchor_data

    def require_unfollow_anchor(self, follow_uid):
        if global_data.player:
            global_data.player.unfollow_anchor(self.LIVE_TYPE, follow_uid)

    def follow_anchor(self, follow_uid):
        if 'anchor_status' in self._raw_follow_channel_data:
            self._raw_follow_channel_data['anchor_status'].update({follow_uid: self._to_be_follow_anchor_data.get(follow_uid, {})})
        else:
            self._raw_follow_channel_data['anchor_status'] = {follow_uid: self._to_be_follow_anchor_data.get(follow_uid, {})}
        self._follow_anchor_list[follow_uid] = self._to_be_follow_anchor_data.get(follow_uid, {})
        self.receive_follow_anchor_live_list(1, self._raw_follow_channel_data)

    def unfollow_anchor(self, follow_uid):
        if follow_uid in self._follow_anchor_list:
            del self._follow_anchor_list[follow_uid]
        self.receive_follow_anchor_live_list(1, self._raw_follow_channel_data)

    def check_is_anchor_followed(self, follow_uid):
        return str(follow_uid) in self._follow_anchor_list

    def check_is_follow_list_full(self):
        if len(self._follow_anchor_list) < FOLLOWED_ANCHOR_MAX_NUM:
            return False
        else:
            return True

    def require_follow_anchor_list(self):
        if global_data.player:
            global_data.player.request_followed_anchor_list(self.LIVE_TYPE)

    def set_follow_anchor_list(self, follow_list_dict):
        self._follow_anchor_list = follow_list_dict

    def get_all_live_total_page(self):
        return self._all_channel.get_total_page()

    def get_label_live_total_page(self, labelid):
        if labelid in self._tag_channels:
            return self._tag_channels[labelid].get_total_page()
        return 0

    def get_follow_live_total_page(self):
        return self._follow_channel.get_total_page()

    def notify_platform_update(self, platform_type):
        global_data.emgr.notify_platform_live_list_update_event.emit(platform_type)

    def notify_anchor_platform_update(self, plaform_type):
        global_data.emgr.notify_platform_anchor_list_update_event.emit(plaform_type)

    def check_all_channel_require_data_cd(self):
        return self._all_channel.check_require_data_cd()

    def check_anchor_channel_require_data_cd(self):
        return self._follow_channel.check_require_data_cd()

    def check_tag_channel_require_data_cd(self, labelid):
        if labelid in self._tag_channels:
            self._tag_channels[labelid].check_require_data_cd()

    def is_support_live_broadcast(self):
        return False

    def is_support_follow_anchor(self):
        return True

    def is_support_dammu(self):
        return self.SUPPORT_DANMU

    def is_support_expired_time(self):
        return self.SUPPORT_EXPIRED_TIME

    def start_live_broadcast(self):
        pass

    def convert_to_common_live_data(self, live_data, rule=None):
        _convert_rule = rule or self._convert_rule
        if not _convert_rule:
            raise NotImplementedError('should have convert rule!', self.LIVE_TYPE)
        new_live_data = {}
        for key, rule in six.iteritems(_convert_rule):
            if key in live_data:
                if type(rule) in [six.text_type, str]:
                    new_live_data[rule] = live_data[key]
            if callable(rule):
                new_live_data[key] = rule(live_data)

        return new_live_data

    def get_custom_follow_convert_rule(self):
        return None

    def commit_channel_cmd(self, dic):
        import game3d
        game3d.delay_exec(1, lambda : global_data.channel.extend_func_by_dict(dic) if global_data.channel else None)

    def set_register_extend_enable(self, methodId_list, is_reg):
        if global_data.channel:
            if is_reg:
                for methodId in methodId_list:
                    global_data.channel.register_extend_callback_function(self.__class__.__name__, methodId, self.extend_func_callback)

            else:
                global_data.channel.unregister_extend_callback_function_by_source(self.__class__.__name__)

    def extend_func_callback(self, json_dict):
        pass

    def receive_live_param(self, live_param):
        self._live_param = live_param
        self.on_receive_live_param()

    def request_live_param(self):
        if global_data.player:
            global_data.player.request_live_param(self.LIVE_TYPE)

    def on_receive_live_param(self):
        pass