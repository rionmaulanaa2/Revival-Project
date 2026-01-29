# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/season/TierRewardUI.py
from __future__ import absolute_import
import six
from six.moves import range
import math
from cocosui import cc
from common import utilities
from logic.gutils import template_utils
from logic.gutils import season_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.gcommon.cdata import dan_data
from logic.comsys.effect import ui_effect
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class TierRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'season/season_reward'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_ACTION_EVENT = {}
    TEMPLATE_NODE_NAME = 'temp_bg'

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'dan_head_frame_reward': self.refresh_redpoint
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)

    def _on_update_reward(self, task_id):
        self.refresh_list()
        self.refresh_redpoint()

    def on_init_panel(self, *args, **kwargs):
        super(TierRewardUI, self).on_init_panel()
        self._refresh_reward_cb = {}
        template_utils.init_common_panel(self.panel.temp_bg, 608012, None)
        self.init_event()
        self.panel.PlayAnimation('appear')
        self.init_tab()
        return

    def init_tab(self):
        self.panel.lab_desc.SetString(610183)
        self._refresh_reward_cb = {}
        self.panel.list_reward.DeleteAllSubItem()
        self.show_task_and_frame_reward()

    def refresh_redpoint(self):
        pass

    def on_create_item(self, inst_cb, dan_list):

        def _on_create_item(list_reward, index, widget_item):
            inst_cb(widget_item, index, dan_list)

        return _on_create_item

    def refresh_list(self):
        for key, cb in six.iteritems(self._refresh_reward_cb):
            cb()

    def on_close(self, *args):
        self.close()

    def show_task_and_frame_reward(self):
        cur_season = global_data.player.get_battle_season()
        task_list = season_utils.get_dan_task_list(cur_season)
        frame_list = season_utils.get_head_frame_info_list()
        task_and_frame_reward_list = []
        for index in range(0, len(task_list)):
            task_and_frame_reward_list.append(task_list[index])
            task_and_frame_reward_list[index].update(frame_list[index])

        list_reward = self.panel.list_reward
        list_reward.BindMethod('OnCreateItem', self.on_create_item(self.on_task_and_frame_item, task_and_frame_reward_list))
        custom_conf = []
        template_name, template_info = list_reward.GetTemplateSetting()
        for i, task_info in enumerate(task_list):
            custom_conf.append({'template': template_name,'template_info': {'temp_tier': {'template_info': {'temp_tier': {'ccbFile': season_utils.get_dan_template(task_info['dan'])
                                                                               }
                                                                 }
                                               }
                                 }
               })

        list_reward.SetCustomizeConf(custom_conf)
        list_reward.SetInitCount(len(task_list))
        list_reward.scroll_Load()
        red_point_map = season_utils.get_dan_frame_reward_redpoint()
        if red_point_map:

            def callback():
                season_utils.clear_dan_frame_reward_redpoint()

            list_reward.DelayCall(1, callback)

    def on_task_and_frame_item(self, widget_item, i, task_and_frame_reward_list):
        task_info = task_and_frame_reward_list[i]
        dan = task_info['dan']
        task_id = task_info['task_id']
        info = task_info.get('info', None)
        if info:
            na_head_frame = info.get('na_head_frame', None)
            head_frame = na_head_frame if G_IS_NA_PROJECT and na_head_frame else info.get('head_frame', None)
        else:
            head_frame = None
        template_utils.init_tier_common(widget_item.temp_tier, dan, 0, show_stage='glow', hide_nd_star=True)
        widget_item.lab_tier_name.SetString(season_utils.get_dan_lv_name(dan))
        widget_item.lab_condition_details.SetString(task_utils.get_task_name(task_id))

        def refresh_cb(task_id=task_id, widget_item=widget_item):
            reward_id = task_utils.get_task_reward(task_id)
            reward_id = reward_id if reward_id else 12000003
            item_no, item_cnt = confmgr.get('common_reward_data', str(reward_id), 'reward_list')[0]
            if global_data.player.has_unreceived_task_reward(task_id):
                widget_item.temp_reward.nd_get_tips.setVisible(True)
                widget_item.temp_reward.PlayAnimation('get_tips')

                def callback():
                    global_data.player.receive_task_reward(task_id)

                template_utils.init_tempate_mall_i_item(widget_item.temp_reward, item_no, item_cnt, callback=callback)
            elif global_data.player.is_all_received_reward(task_id):
                widget_item.temp_reward.nd_get_tips.setVisible(False)
                widget_item.temp_reward.StopAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(widget_item.temp_reward, item_no, item_cnt, isget=True, show_tips=True, callback=False)
            else:
                widget_item.temp_reward.nd_get_tips.setVisible(False)
                widget_item.temp_reward.StopAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(widget_item.temp_reward, item_no, item_cnt, show_tips=True, callback=False)

        self._refresh_reward_cb[i] = refresh_cb
        refresh_cb()
        if head_frame:
            widget_item.lab_frame_details.SetString(610184 if dan != dan_data.LEGEND else 83405)
            isget = False
            cur_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
            if cur_dan >= dan or global_data.player.has_item_by_no(head_frame):
                isget = True
            template_utils.init_tempate_mall_i_item(widget_item.temp_reward_frame, head_frame, 1, isget=isget, show_tips=True)
            total_sec = 1
            red_point_map = season_utils.get_dan_frame_reward_redpoint()
            if dan in red_point_map:
                ui_effect.set_opacity_percent(widget_item.temp_reward.nd_get, 0, recursion=True)

                def show_up(pass_time, widget=widget_item.temp_reward):
                    ui_effect.set_opacity_percent(widget.nd_get, pass_time / total_sec, recursion=True)

                widget_item.temp_reward_frame.nd_get.TimerAction(show_up, total_sec)
        else:
            widget_item.temp_reward_frame.setVisible(False)
            widget_item.lab_frame_details.setVisible(False)
        return