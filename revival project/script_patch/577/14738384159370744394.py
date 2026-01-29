# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/SnatchEggTopScoreUI.py
from __future__ import absolute_import
import six
import six_ex
from collections import defaultdict
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
import math
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import ROUND_STATUS_INTERVAL, BTN_DROP_EGG
import logic.gutils.delay as delay
from logic.gcommon.common_const import battle_const as bconst
EGG_DROP_TIP_TIME = 2

class SnatchEggTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_golden_egg/battle_golden_egg_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'crystal_round_settle_timestamp_event': 'update_round_settle_timestamp',
       'snatchegg_egg_drop': 'on_drop_egg',
       'snatchegg_egg_pick_up': 'on_pick_egg',
       'update_group_score_data': 'update_top_score',
       'player_revived': 'on_revive',
       'show_battle_report_event': 'on_defeated',
       'snatchegg_round_interval_event': 'on_round_interval',
       'scene_player_setted_event': 'on_player_setted',
       'update_battle_data': 'update_top_score'
       }

    def on_init_panel(self, *args, **kwargs):
        self.regist_main_ui()
        self.init_parameters()
        self.update_group_id(None)
        self.init_widgets()
        self.update_lab_mine()
        return

    def init_parameters(self):
        self.is_warning = False
        self.left_10_seconds = False
        self.group_id = None
        self.group_idx_dict = {}
        self.soul_btn_dict = {}
        self.group_egg_cnt = {}
        self.group_dict = global_data.battle.get_group_loading_dict()
        self.egg_drop_timer = {}
        idx = 0
        group_list = global_data.battle.get_show_group_list()
        for gid in group_list:
            self.group_idx_dict[gid] = idx
            idx += 1

        self.group_name_dict = {0: 'A',1: 'B',
           2: 'C',
           3: 'D'
           }
        return

    def on_finalize_panel(self):
        self.stop_count_down()
        self.stop_drop_timer()

    def init_widgets(self):
        self.panel.RecordAnimationNodeState('alarm')
        self.start_count_down()
        self.init_top_score()

    def update_group_id(self, ltarget):
        if global_data.player and global_data.player.logic:
            self.group_id = global_data.player.logic.ev_g_group_id()
        elif ltarget:
            self.group_id = ltarget.ev_g_group_id()

    def start_count_down(self):
        if not global_data.battle:
            return
        round_left_time = global_data.battle.get_round_left_time()
        if round_left_time <= 0:
            return
        if global_data.battle.get_round_status() == ROUND_STATUS_INTERVAL:
            return
        self.panel.lab_time.SetColor(1190474)

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            cur_left_time = round_left_time - pass_time
            if cur_left_time <= 30 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif cur_left_time > 30 and self.is_warning:
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
            if cur_left_time <= 20 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(cur_left_time)
                self.left_10_seconds = True
            left_time = int(math.ceil(cur_left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finish():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, round_left_time, callback=refresh_time_finish, interval=1)

    def stop_count_down(self):
        self.panel.lab_time.StopTimerAction()

    def init_top_score(self):
        battle = global_data.battle
        if not battle:
            return
        score_list = self.panel.list_score
        score_list.SetInitCount(len(self.group_dict))
        for gid in six_ex.keys(self.group_idx_dict):
            g_idx = self.group_idx_dict[gid]
            g_item = score_list.GetItem(g_idx)
            txt = get_text_by_id(17946, (self.group_name_dict[g_idx],))
            g_item.lab_team.SetString(txt)
            g_item.list_head.SetInitCount(len(six_ex.keys(self.group_dict[gid])))
            for idx, soul_id in enumerate(six_ex.keys(self.group_dict[gid])):
                head_item = g_item.list_head.GetItem(idx)
                self.soul_btn_dict[soul_id] = head_item.btn_player

        self.update_top_score()
        self.update_group_status()

    def delay_close_drop_tip(self, holder_id, head_item):
        if self.egg_drop_timer.get(holder_id):
            head_item.frame.setVisible(False)
            head_item.frame_ban.icon_ban.setVisible(False)
            self.egg_drop_timer[holder_id] = None
        else:
            return
        return

    def stop_drop_timer(self):
        for key, timer in six.iteritems(self.egg_drop_timer):
            timer and delay.cancel(timer)

        self.egg_drop_timer = {}

    def update_round_settle_timestamp(self, settle_timestamp):
        self.start_count_down()

    def on_drop_egg(self, holder_id, faction, reason, npc_id):
        if reason == BTN_DROP_EGG:
            return
        battle = global_data.battle
        player = global_data.player
        if not battle or not player:
            return
        ent = battle.get_entity(holder_id)
        if not ent or not ent.logic or not player.logic:
            return
        gid = ent.logic.ev_g_group_id()
        self.group_egg_cnt.setdefault(gid, 0)
        if gid in self.group_egg_cnt and self.group_egg_cnt[gid] > 0:
            self.group_egg_cnt[gid] -= 1
        g_item = self.panel.list_score.GetItem(self.group_idx_dict[gid])
        g_item.lab_num.SetString(str(self.group_egg_cnt[gid]))
        head_item = self.soul_btn_dict[holder_id]
        head_item.frame_ban.icon_ban.setVisible(True)
        drop_handler = delay.call(EGG_DROP_TIP_TIME, lambda : self.delay_close_drop_tip(holder_id, head_item))
        self.egg_drop_timer[holder_id] = drop_handler
        if gid == player.logic.ev_g_group_id():
            if self.group_egg_cnt[gid] <= 0:
                tip_type = bconst.OUR_GROUP_DROP_LAST_EGG_TIP
                message = {'i_type': tip_type,'in_anim': 'show','out_anim': 'disappear'}
                global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            else:
                tip_type = bconst.OUR_GROUP_DROP_EGG_TIP
                message = {'i_type': tip_type,'in_anim': 'appear','out_anim': 'disappear'}
                global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
        else:
            tip_type = bconst.OTHER_GROUP_DROP_EGG_TIP
            message = {'i_type': tip_type,'in_anim': 'appear','out_anim': 'disappear'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)

    def on_pick_egg(self, picker_id, faction, npc_id):
        battle = global_data.battle
        if not battle:
            return
        else:
            ent = battle.get_entity(picker_id)
            if not ent or not ent.logic:
                return
            gid = ent.logic.ev_g_group_id()
            g_data = self.group_dict[gid]
            if gid == global_data.player.logic.ev_g_group_id():
                idx = six_ex.keys(g_data).index(picker_id) + 1
                self.our_group_pick_egg_tip(idx)
            else:
                idx = self.group_name_dict[self.group_idx_dict[gid]]
                self.other_group_pick_egg_tip(idx)
            self.group_egg_cnt.setdefault(gid, 0)
            self.group_egg_cnt[gid] += 1
            g_item = self.panel.list_score.GetItem(self.group_idx_dict[gid])
            g_item.lab_num.SetString(str(self.group_egg_cnt[gid]))
            head_item = self.soul_btn_dict[picker_id]
            mecha_id = ent.logic.ev_g_get_bind_mecha_type()
            mecha_id and head_item.frame.icon_mecha.SetDisplayFrameByPath('', 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id)
            head_item.frame.setVisible(True)
            head_item.frame_ban.icon_ban.setVisible(False)
            timer = self.egg_drop_timer.get(picker_id, None)
            if timer:
                delay.cancel(timer)
            self.egg_drop_timer[picker_id] = None
            return

    def on_revive(self, eid):
        head_item = self.soul_btn_dict.get(eid)
        head_item and head_item.SetEnable(True)

    def on_defeated(self, report):
        dead_id = report.get('injured_id')
        head_item = self.soul_btn_dict.get(dead_id)
        head_item and head_item.SetEnable(False)

    def our_group_pick_egg_tip(self, idx):
        text = get_text_by_id(17941, [idx])
        tip_type = bconst.OUR_GROUP_PICK_EGG_TIP
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
        global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)

    def other_group_pick_egg_tip(self, idx):
        text = get_text_by_id(17944, [idx])
        tip_type = bconst.OTHER_GROUP_PICK_EGG_TIP
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'show','out_anim': 'disappear'}
        global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)

    def update_top_score(self, *args):
        battle = global_data.battle
        if not battle:
            return
        score_list = self.panel.list_score
        for gid in six_ex.keys(self.group_idx_dict):
            g_idx = self.group_idx_dict[gid]
            g_item = score_list.GetItem(g_idx)
            egg_cnt = 0
            for idx, soul_id in enumerate(six_ex.keys(self.group_dict[gid])):
                head_item = g_item.list_head.GetItem(idx)
                if global_data.death_battle_data.egg_picker_dict.get(soul_id):
                    ent = battle.get_entity(soul_id)
                    if not ent or not ent.logic:
                        mecha_id = battle.temp_mecha_info.get(soul_id)
                    else:
                        mecha_id = ent.logic.ev_g_get_bind_mecha_type()
                    egg_cnt += 1
                    head_item.frame.setVisible(True)
                    mecha_id and head_item.frame.icon_mecha.SetDisplayFrameByPath('', 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id)
                else:
                    head_item.frame.setVisible(False)
                head_item.btn_player.SetSelect(soul_id == global_data.player.id)

            g_item.lab_num.SetString(str(egg_cnt))
            self.group_egg_cnt[gid] = egg_cnt

    def update_group_status(self):
        if not global_data.battle:
            return
        battle = global_data.battle
        all_group_ids = battle.get_all_group_ids()
        score_list = self.panel.list_score
        for gid in six_ex.keys(self.group_idx_dict):
            g_idx = self.group_idx_dict[gid]
            g_item = score_list.GetItem(g_idx)
            g_item.nd_ban.setVisible(gid not in all_group_ids)

    def on_round_interval(self):
        self.update_group_status()

    def on_player_setted(self, player):
        if not player:
            return
        self.update_lab_mine()

    def update_lab_mine(self):
        ui_item = self.panel.list_score.GetItem(0)
        if ui_item:
            ui_item.lab_mine.setVisible(self.get_is_part_of_match())

    def get_is_part_of_match(self):
        if not global_data.player:
            return False
        pid = global_data.player.id
        for group_member_dict in six.itervalues(self.group_dict):
            if pid in six_ex.keys(group_member_dict):
                return True

        return False