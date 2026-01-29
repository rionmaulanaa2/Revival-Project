# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/live/LivePlatformManager.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from logic.gcommon.common_const import liveshow_const

class LivePlatformManager(Singleton):
    ALIAS_NAME = 'live_platform_mgr'

    def init(self):
        self._cur_live_platform = None
        self._support_platform_dicts = {}
        self.init_support_platforms()
        return

    def destroy(self):
        for pt_ty, pt in six.iteritems(self._support_platform_dicts):
            pt.destroy()

        self._support_platform_dicts = {}

    def clear_all_cache(self):
        for pt_ty, pt in six.iteritems(self._support_platform_dicts):
            pt.clear_all_live_cache()
            pt.clear_follow_live_cache()
            pt.clear_tag_channel_cache()
            pt.clear_follow_data()

    def init_support_platforms(self):
        import game3d
        from logic.vscene.part_sys.live.CCLivePlatform import CCLivePlatform
        from logic.vscene.part_sys.live.HuyaLivePlatform import HuyaLivePlatform, HuyaLivePlatformNonSDK
        from logic.vscene.part_sys.live.DouyuLivePlatform import DouyuLivePlatform
        from logic.vscene.part_sys.live.BLBLLivePlatform import BLBLLivePlatform
        from logic.vscene.part_sys.live.KuaishouLivePlatform import KuaishouLivePlatform
        support_platforms = [
         CCLivePlatform, DouyuLivePlatform, BLBLLivePlatform, KuaishouLivePlatform]
        if game3d.get_platform() != game3d.PLATFORM_WIN32 and not global_data.is_android_pc:
            support_platforms.append(HuyaLivePlatform)
        else:
            support_platforms.append(HuyaLivePlatformNonSDK)
        for live_class in support_platforms:
            self._support_platform_dicts[live_class.LIVE_TYPE] = live_class()

        self.require_all_platform_channels()
        self.require_all_platform_follow_anchors()

    def select_platform(self, platform_type):
        self._cur_live_platform = self.get_platform_by_type(platform_type)

    def get_platform_by_type(self, platform_type):
        if platform_type in self._support_platform_dicts:
            return self._support_platform_dicts[platform_type]
        else:
            return None

    def get_cur_platform(self):
        return self._cur_live_platform

    def receive_live_data(self, platform_type, page, total_page, live_list, room_info=None):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            live_list = [ platform.convert_to_common_live_data(l) for l in live_list ]
            platform.receive_all_live_list(page, total_page, live_list, room_info)
            platform.notify_platform_update(platform_type)

    def receive_live_platform_channels(self, platform_type, labels):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.receive_live_labels(labels)
        global_data.emgr.receive_live_platform_channels_event.emit(platform_type, labels)

    def receive_channel_live_list(self, platform_type, labelid, page, livelist):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            livelist = [ platform.convert_to_common_live_data(l) for l in livelist ]
            platform.receive_live_channel_live_list(labelid, page, livelist)
            platform.notify_platform_update(platform_type)

    def receive_anchor_live_list(self, platform_type, page, livelist_dict):
        platform = self.get_platform_by_type(platform_type)
        anchor_data = livelist_dict.get('anchor_status', {})
        fetch_time = livelist_dict.get('fetch_time', 0)
        if platform:
            follow_rule = platform.get_custom_follow_convert_rule()
            new_anchor_data = {k:platform.convert_to_common_live_data(v, follow_rule) for k, v in six.iteritems(anchor_data)}
            livelist_dict['anchor_status'] = new_anchor_data
            platform.receive_follow_anchor_live_list(page, livelist_dict)
            platform.notify_anchor_platform_update(platform_type)

    def require_all_platform_channels(self):
        for platform_type, platform in six.iteritems(self._support_platform_dicts):
            platform.require_live_labels()

    def require_all_platform_follow_anchors(self):
        for platform_type, platform in six.iteritems(self._support_platform_dicts):
            platform.require_follow_anchor_list()

    def follow_anchor(self, platform_type, anchor_id):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.follow_anchor(anchor_id)
        global_data.emgr.notify_follow_anchor_change_event.emit(platform_type, anchor_id, True)

    def unfollow_anchor(self, platform_type, anchor_id):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.unfollow_anchor(anchor_id)
        global_data.emgr.notify_follow_anchor_change_event.emit(platform_type, anchor_id, False)

    def require_follow_anchor(self, platform_type, anchor_id, anchor_data):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.require_follow_anchor(anchor_id, anchor_data)

    def check_is_follow_list_full(self, platform_type):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            return platform.check_is_follow_list_full()
        return False

    def require_unfollow_anchor(self, platform_type, anchor_id):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.require_unfollow_anchor(anchor_id)

    def set_follow_anchor_list(self, platform_type, anchor_list):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.set_follow_anchor_list(anchor_list)
        global_data.emgr.notify_follow_anchor_change_event.emit(platform_type, None)
        return

    def convert_to_common_live_data(self, platform, live_data):
        new_live_data = platform.convert_to_common_live_data(live_data)
        return new_live_data

    def receive_live_param(self, platform_type, live_param):
        platform = self.get_platform_by_type(platform_type)
        if platform:
            platform.receive_live_param(live_param)