# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivityLuckyBag.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
import logic.gcommon.time_utility as tutil
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityLuckyBag(ActivityBase):

    def on_init_panel(self):
        self.conf = confmgr.get('c_activity_config', self._activity_type)
        self.init_activity_info()
        self.init_lanten_gifts()
        self.init_misc_widget()
        self.panel.PlayAnimation('loop2')
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.refresh_lucky_bag_num
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_activity_info(self):
        start_date = tutil.get_date_str('%Y.%m.%d', self.conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%Y.%m.%d', self.conf.get('cEndTime', 0), ignore_second=21600)
        self.panel.lab_time.SetString('{}-{}'.format(start_date, finish_date))
        self.panel.lab_title_top.SetString(601124)

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            if not G_IS_NA_PROJECT:
                dlg.set_show_rule(601124, 601182)
            else:
                dlg.set_show_rule(601124, 601225)
            dlg.set_node_pos(touch.getLocation(), cc.Vec2(0, 1))

        end_stamp = tutil.time_str_to_timestamp('20210218:0500', '%Y%m%d:%H%M')
        now = tutil.time()
        if now > end_stamp:
            self.panel.nd_lucky_bag.btn_go_more.btn_common.SetEnable(False)
            self.panel.nd_lucky_bag.btn_go_more.btn_common.SetText(81796)
            self.panel.nd_lucky_bag.img_ahead.setVisible(False)

    def init_lanten_gifts(self):
        ui_data = self.conf.get('cUiData')
        if not ui_data:
            return
        else:
            lanten_gift_list = ui_data['gifts']
            nd_gift = self.panel.nd_gift
            for idx, gift_item_id in enumerate(lanten_gift_list):
                temp_name = 'temp_lanten_{:02d}'.format(idx + 1)
                shadow_name = 'img_lanten_shadow_{:02d}'.format(idx + 1)
                temp_gift_nd = getattr(nd_gift, temp_name, None)
                shadow_nd = getattr(nd_gift, shadow_name, None)
                if not temp_gift_nd:
                    continue
                scale = 1 - (len(lanten_gift_list) - idx) / 20.0
                temp_gift_nd.PlayAnimation('loop', scale=scale)
                self.panel.SetTimeOut(0.1, lambda nd=shadow_nd, scale=scale: nd.PlayAnimation('loop', scale=scale))
                path = item_utils.get_lobby_item_pic_by_item_no(gift_item_id)
                temp_gift_nd.img_item.SetDisplayFrameByPath('', path)
                target_w, target_h = temp_gift_nd.nd_img.GetContentSize()
                pic_w, pic_h = temp_gift_nd.img_item.GetContentSize()
                scale = target_h / pic_h
                temp_gift_nd.img_item.setScale(scale)

                @temp_gift_nd.nd_img.unique_callback()
                def OnClick(btn, touch, item_id=gift_item_id):
                    global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=touch.getLocation())
                    return

            return

    def init_misc_widget(self):
        self.refresh_lucky_bag_num()
        lucky_bag_item_id = self.conf.get('cUiData', {}).get('lucky_bag_id', 50101123)

        @self.panel.btn_get_bag.btn_common.unique_callback()
        def OnClick(btn, touch):
            item_num = global_data.player.get_item_num_by_no(lucky_bag_item_id)
            item_name = item_utils.get_lobby_item_name(lucky_bag_item_id)
            if item_num <= 0:
                global_data.game_mgr.show_tip(get_text_by_id(12082, args={'suipian': item_name}))
                return
            item = global_data.player.get_item_by_no(lucky_bag_item_id)
            global_data.player.use_item(item.id, 1)

        @self.panel.btn_go_more.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('LuckyBagObtainUI', 'logic.comsys.activity.SpringFestival')

    def refresh_lucky_bag_num(self, *args):
        lucky_bag_item_id = self.conf.get('cUiData', {}).get('lucky_bag_id', 50101123)
        lucky_bag_item_nums = global_data.player.get_item_num_by_no(lucky_bag_item_id)
        self.panel.lab_num.SetString('\xc3\x97{}'.format(lucky_bag_item_nums))
        self.panel.btn_get_bag.btn_common.SetEnable(lucky_bag_item_nums > 0)
        self.panel.img_btn_light.setVisible(lucky_bag_item_nums > 0)
        global_data.player.trigger_delay_notice_by_item_no(50101124)
        if lucky_bag_item_nums > 0:
            self.panel.btn_get_bag.btn_common.SetText(601125)
            self.panel.PlayAnimation('loop')
        else:
            self.panel.btn_get_bag.btn_common.SetText(601220)
            self.panel.StopAnimation('loop')