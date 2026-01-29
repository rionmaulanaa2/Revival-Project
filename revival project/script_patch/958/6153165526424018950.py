# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyBannerWidget.py
from __future__ import absolute_import
import six_ex
import math
import ccui
import cc
from common.cfg import confmgr
from common.utils.timer import CLOCK
from common.utils.cocos_utils import ccp
from logic.gcommon import time_utility
from logic.gutils import jump_to_ui_utils
from logic.gutils.activity_utils import is_activity_finished
from logic.gutils.mall_utils import is_good_opened
LEFT = 0
RIGHT = 1
REFRESH_INTERVAL = 5.0
ACTIVITY_TYPE = 1
ACTIVITY_BANNER_CUSTOM = 2

class LobbyBannerWidget(object):

    def __init__(self, parent_ui, panel):
        super(LobbyBannerWidget, self).__init__()
        self.parent = parent_ui
        self.panel = panel
        self.sub_panel = self.panel.nd_banner.nd_clip.list_banner
        self._last_offset = 0
        self._scroll_direction = RIGHT
        self._cur_idx = 0
        self._timer = None
        self._show_white_list = []
        self.init_panel()
        self.init_ui_event()
        return

    def init_panel(self):
        self.ad_data_dict = confmgr.get('banner_config', 'Content', default={})
        self.panel.nd_banner.list_num.DeleteAllSubItem()
        self.sub_panel.DeleteAllSubItem()
        for ad_id in six_ex.keys(self.ad_data_dict):
            if self.banner_type_handler(ad_id):
                self.panel.nd_banner.list_num.AddTemplateItem()
                item = self.sub_panel.AddTemplateItem()
                item.nd_banner.SetNoEventAfterMove(True, 1.2)
                pic_path = self.ad_data_dict.get(ad_id).get('ad_pic')
                click_func_info = self.ad_data_dict.get(ad_id).get('click_func')
                item.nd_banner.img_banner.SetDisplayFrameByPath('', pic_path)

                @item.nd_banner.unique_callback()
                def OnClick(btn, touch, jump_info=click_func_info):
                    func_name = jump_info.get('func')
                    args = jump_info.get('args', [])
                    kargs = jump_info.get('kargs', {})
                    if func_name:
                        func = getattr(jump_to_ui_utils, func_name)
                        func and func(*args, **kargs)

        if self.panel.nd_banner.list_num.GetItemCount() > 0:
            self.panel.nd_banner.list_num.GetItem(0).btn_icon_choose.SetSelect(True)
        if self.sub_panel.GetItemCount() > 0:
            self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=REFRESH_INTERVAL, times=-1, mode=CLOCK)
        else:
            self.panel.nd_banner.setVisible(False)

    def init_ui_event(self):
        self.sub_panel.BindMethod('OnScrolling', self._on_scrolling)
        self.sub_panel.addTouchEventListener(self._on_normal_touch)
        self.sub_panel.setInertiaScrollEnabled(False)

    def _on_normal_touch(self, widget, event):
        if event in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED, ccui.WIDGET_TOUCHEVENTTYPE_CANCELED):
            idx_item = self.update_now_idx()
            self._cur_idx = idx_item
            self.sub_panel.LocatePosByItem(idx_item)
            if not self._timer:
                self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=5, times=-1, mode=CLOCK)

    def _on_scrolling(self, *args):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        off_set_now = self.sub_panel.GetContentOffset()
        self._scroll_direction = RIGHT if off_set_now.x - self._last_offset <= 0 else LEFT
        self._last_offset = off_set_now.x
        now_idx = self.update_now_idx()
        if now_idx != self._cur_idx:
            ss = self.panel.nd_banner.list_num.GetItemCount()
            if self._cur_idx >= 0 and self._cur_idx < ss:
                self.panel.nd_banner.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
            if now_idx >= 0 and now_idx < ss:
                self.panel.nd_banner.list_num.GetItem(now_idx).btn_icon_choose.SetSelect(True)
            self._cur_idx = now_idx
        return

    def update_now_idx(self):
        ctrl_size = self.sub_panel.GetCtrlSize()
        off_set_now = self.sub_panel.GetContentOffset()
        off_num = abs(off_set_now.x / ctrl_size.width)
        if self._scroll_direction == RIGHT:
            idx_item = int(math.ceil(off_num))
        else:
            idx_item = int(math.floor(off_num))
        item_count = self.panel.nd_banner.list_num.GetItemCount()
        if idx_item >= item_count:
            return item_count - 1
        return idx_item

    def banner_type_handler(self, ad_id):
        conf = self.ad_data_dict.get(ad_id, {})
        if ad_id in self._show_white_list:
            return True
        else:
            now = time_utility.get_server_time()
            if not conf.get('begin_time', 0) <= now <= conf.get('end_time', now + 1):
                return False
            activity_type = conf.get('activity_type', None)
            if activity_type:
                activity_data_map = global_data.player.get_opened_activity_data() or {}
                if str(activity_type) not in activity_data_map:
                    return False
                if is_activity_finished(str(activity_type)):
                    return False
            open_param = conf.get('open_param', {})
            if 'open_host' in open_param and global_data.channel.get_login_host() not in open_param['open_host']:
                return False
            if 'goods_id' in open_param:
                from logic.gutils.mall_utils import is_valid_goods
                if not is_valid_goods(str(open_param['goods_id'])):
                    return False
            if 'platform' in open_param:
                import game3d
                platform = game3d.get_platform()
                if platform == game3d.PLATFORM_IOS:
                    platform = 'ios'
                else:
                    if platform == game3d.PLATFORM_ANDROID:
                        platform = 'android'
                    elif platform == game3d.PLATFORM_WIN32:
                        platform = 'pc'
                    if platform not in open_param['platform']:
                        return False
            app_channel = self.get_app_channel()
            valid_app_channel = conf.get('valid_app_channel', [])
            if valid_app_channel:
                if 'all_netease' in valid_app_channel and self.is_netease_package():
                    pass
                elif app_channel not in valid_app_channel:
                    return False
            invalid_app_channel = conf.get('invalid_app_channel', [])
            if invalid_app_channel and app_channel in invalid_app_channel:
                return False
            return True

    def is_netease_package(self):
        return global_data.channel.get_name() in ('netease', '')

    def get_app_channel(self):
        return (global_data.channel.get_sauth_info() or {}).get('app_channel', global_data.channel.get_app_channel())

    def tick(self):
        num = self.sub_panel.GetItemCount()
        if num <= 0:
            return
        next_idx = 0 if self._cur_idx + 1 >= num else self._cur_idx + 1
        container = self.sub_panel.GetInnerContainer()
        container.stopAllActions()

        def scroll_end():
            self.sub_panel.LocatePosByItem(next_idx)
            self.panel.nd_banner.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
            self.panel.nd_banner.list_num.GetItem(next_idx).btn_icon_choose.SetSelect(True)
            self._cur_idx = next_idx

        ctrl_size = self.sub_panel.GetCtrlSize()
        container.runAction(cc.Sequence.create([
         cc.MoveTo.create(0.3, ccp(ctrl_size.width * next_idx * -1, container.getPosition().y)),
         cc.CallFunc.create(scroll_end)]))

    def destroy(self):
        self.panel = None
        self.parent = None
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def set_show_white_list(self, ls):
        self._show_white_list = ls
        self.init_panel()