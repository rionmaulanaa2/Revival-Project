# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGTopScoreUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
from logic.gutils import role_head_utils
from logic.comsys.effect import ui_effect
from logic.client.const import game_mode_const
import math
from common.const import uiconst
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class GVGTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_gvg/gvg_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_top.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.init_panel()
        self.init_hp_progress_share()
        self.start_hp_tick()

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        self.process_event(False)

    def init_panel(self):
        self.panel.nd_ace.SetOptimize(False)
        self.panel.RecordAnimationNodeState('alarm')
        self.panel.RecordAnimationNodeState('show_bar')
        bat = self.get_battle()
        if not bat:
            return
        self.mecha_choose_dict = bat.mecha_choose_dict
        self.eids = bat.eids
        self.eid_to_index = bat.eid_to_index
        self.init_mecha_head()
        self.update_timestamp()
        if global_data.gvg_battle_data:
            self.update_battle_data()

    def get_battle(self):
        return global_data.battle

    def get_list_node_index(self, soul_id):
        return self.eid_to_index.get(soul_id, 0)

    def get_list_node(self, eid):
        bat = self.get_battle()
        index = 0 if bat.is_friend_group(eid) else 1
        return self.mecha_list_nd[index]

    def init_mecha_head(self):
        bat = self.get_battle()
        for nd in self.mecha_list_nd:
            nd.DeleteAllSubItem()

        for eid in self.eids:
            list_nd = self.get_list_node(eid)
            is_friend = bat.is_friend_group(eid)
            head_index = self.get_list_node_index(eid)
            item_widget = list_nd.AddTemplateItem(head_index)
            item_widget.ani_index = 0
            for round_idx, mecha_id in six.iteritems(self.mecha_choose_dict.get(eid, {})):
                head_nd_name = 'temp_%d' % round_idx
                head_nd = getattr(item_widget, head_nd_name)
                head_nd.nd_clip.SetOptimize(False)
                if not is_friend:
                    head_nd.img_broken.setScaleX(-1)
                    head_nd.lab_time.setScaleX(-1)
                icon_path = role_head_utils.get_head_photo_res_path(int('3021%d' % mecha_id))
                head_nd.img_head.SetDisplayFrameByPath('', icon_path)
                ui_effect.set_gray(head_nd.img_head, False)

        max_num = 0
        for num in six.itervalues(bat.group_to_num):
            max_num = max(num, max_num)

        w = 280 if max_num < 2 else 400
        self.panel.btn_top.SetContentSize(w, 84)
        self.panel.btn_top.ResizeAndPosition(include_self=False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'update_battle_data': self.update_battle_data,
           'choose_mecha_finished': self.choose_mecha_finished,
           'duel_round_interval_event': self.update_duel_battle_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def choose_mecha_finished(self):
        bat = self.get_battle()
        self.mecha_choose_dict = bat.mecha_choose_dict
        self.init_mecha_head()
        self.update_battle_data()

    def init_parameters(self):
        self.mecha_list_nd = (
         self.panel.list_mech_blue, self.panel.list_mech_red)
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.is_warning = False
        self.is_left_10 = False

    def update_timestamp(self, *args):
        self.on_count_down()

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('GVGScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('GVGScoreDetailsUI')
        elif global_data.battle:
            global_data.ui_mgr.show_ui('GVGScoreDetailsUI', 'logic.comsys.battle.gvg')

    def show_count_down(self, show):
        self.panel.nd_time.setVisible(show)

    def on_count_down(self):

        def clear_show():
            self.panel.lab_time.StopTimerAction()
            self.panel.StopAnimation('alarm')
            self.panel.StopAnimation('show_bar')
            self.panel.RecoverAnimationNodeState('alarm')
            self.panel.RecoverAnimationNodeState('show_bar')
            self.panel.lab_time.SetString('')
            global_data.ui_mgr.close_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
            if self.panel.lab_time_vx is not None:
                self.panel.lab_time_vx.SetString('')
            return

        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            if global_data.battle:
                if global_data.battle.get_is_in_round_interval():
                    clear_show()
                    return
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            left_time = revive_time - pass_time
            if left_time <= 60 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('show_bar')
                self.is_warning = True
            elif left_time <= 10 and not self.is_left_10:
                self.panel.PlayAnimation('alarm')
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(left_time)
                global_data.emgr.left_ten_second_event.emit()
                self.is_left_10 = True
            left_time = int(math.ceil(left_time))
            left_time = tutil.get_delta_time_str(left_time)[4:]
            self.panel.lab_time.SetString(left_time)
            if self.panel.lab_time_vx is not None:
                self.panel.lab_time_vx.SetString(left_time)
            return

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[4:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.SetColor('#BW')
        self.panel.StopAnimation('alarm')
        self.panel.StopAnimation('show_bar')
        self.panel.RecoverAnimationNodeState('alarm')
        self.panel.RecoverAnimationNodeState('show_bar')
        self.is_warning = False
        self.is_left_10 = False
        self.panel.lab_time.SetFontSize(20)
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)

    def update_battle_data(self):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            self.update_duel_battle_data()
            return
        bat = self.get_battle()
        mecha_use_dict = global_data.gvg_battle_data.mecha_use_dict
        mecha_revice_ts_dict = global_data.gvg_battle_data.mecha_revice_ts_dict
        frd_left_mecha_num = 0
        emy_left_mecha_num = 0
        for eid in six.iterkeys(self.mecha_choose_dict):
            if bat.is_friend_group(eid):
                frd_left_mecha_num += game_mode_const.GVG_MECHA_NUM
            else:
                emy_left_mecha_num += game_mode_const.GVG_MECHA_NUM

        for eid, die_num in six.iteritems(mecha_use_dict):
            if bat.is_friend_group(eid):
                frd_left_mecha_num -= die_num
            else:
                emy_left_mecha_num -= die_num
            index = self.eid_to_index.get(eid, 0)
            lst_nd = self.get_list_node(eid)
            temp_nd = lst_nd.GetItem(index)
            revice_ts = mecha_revice_ts_dict.get(eid)
            self.on_head_count_down(temp_nd, die_num, revice_ts)

        self.panel.lab_score_blue.SetString(str(frd_left_mecha_num))
        self.panel.lab_score_red.SetString(str(emy_left_mecha_num))

    def update_duel_battle_data(self):
        bat = self.get_battle()
        frd_left_mecha_num = 0
        emy_left_mecha_num = 0
        for eid in six.iterkeys(self.mecha_choose_dict):
            win_cnt = bat.get_eid_win_cnt(eid)
            if bat.is_friend_group(eid):
                frd_left_mecha_num += win_cnt
            else:
                emy_left_mecha_num += win_cnt

        for eid in six.iterkeys(self.mecha_choose_dict):
            index = self.eid_to_index.get(eid, 0)
            lst_nd = self.get_list_node(eid)
            temp_nd = lst_nd.GetItem(index)
            revice_ts = 0
            cur_round = len(bat.soul_round_record.get(eid, []))
            round_record = global_data.battle.get_round_record(eid)
            if cur_round >= 1:
                self.on_head_count_down(temp_nd, cur_round, revice_ts, round_record)

        self.panel.lab_score_blue.SetString(str(frd_left_mecha_num))
        self.panel.lab_score_red.SetString(str(emy_left_mecha_num))

    def on_head_count_down(self, temp_nd, die_num, revice_ts, round_record=()):
        print('on_head_count_down', die_num, revice_ts, round_record)
        if revice_ts:
            revive_time = revice_ts - tutil.get_server_time()
        else:
            revive_time = 0
        head_nd_name = 'temp_%d' % die_num
        node = getattr(temp_nd, head_nd_name)
        if die_num - 1 > 0:
            for i in range(die_num):
                last_head_nd_name = 'temp_%d' % (i + 1)
                last_node = getattr(temp_nd, last_head_nd_name)
                ui_effect.set_gray(last_node.img_head, True)
                last_node.lab_time.setVisible(False)
                last_node.img_broken.setVisible(True)
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                    from logic.entities.DuelBattle import ROUND_LOSE
                    last_node.img_broken.setOpacity(255 if round_record[i] == ROUND_LOSE else 0)

        def refresh_time(pass_time, node=node):
            left_time = int(math.ceil(revive_time - pass_time))
            node.lab_time.SetString(str(left_time))

        def refresh_time_finsh(temp_nd=temp_nd, node=node):
            ani_index = min(die_num, 2)
            if ani_index > temp_nd.ani_index:
                temp_nd.PlayAnimation('rebirth%d' % ani_index)
                temp_nd.ani_index = ani_index
            node.lab_time.setVisible(False)
            node.img_broken.setVisible(True)
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                from logic.entities.DuelBattle import ROUND_LOSE
                if die_num - 1 < len(round_record):
                    node.img_broken.setOpacity(255 if round_record[die_num - 1] == ROUND_LOSE else 0)

        ui_effect.set_gray(node.img_head, True)
        if revive_time <= 0:
            refresh_time_finsh()
            return
        node.lab_time.StopTimerAction()
        node.lab_time.setVisible(True)
        node.img_broken.setVisible(False)
        refresh_time(0)
        node.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=0.1)

    def init_hp_progress_share(self):
        if not (self.panel.prog_blue and self.panel.prog_red):
            return
        progress_list = [
         self.panel.prog_blue, self.panel.prog_red]
        bat = self.get_battle()
        for group, num in six.iteritems(bat.group_to_num):
            index = 0 if bat.my_group == group else 1
            hp_mech_progress = progress_list[index]
            if num == 0:
                hp_mech_progress.setScale(0)
            elif num == 1:
                hp_mech_progress.setScale(0.5)
            else:
                hp_mech_progress.setScale(1)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_DUEL,))
    def start_hp_tick(self):
        if not (self.panel.prog_blue and self.panel.prog_red):
            return
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_hp_status),
         cc.DelayTime.create(0.5)])))

    def update_hp_status(self):
        if not (self.panel.prog_blue and self.panel.prog_red):
            return

        def update_mecha_health(hp_mech_progress, mecha):
            if not (mecha and mecha.logic):
                return
            mecha = mecha.logic
            Value = mecha.get_value
            hp_max = Value('G_MAX_HP')
            hp = Value('G_HP')
            if hp > hp_max:
                hp = hp_max
            hp_mech_progress.SetPercentage(hp / float(hp_max) * 100)

        if not (global_data.battle and global_data.player):
            return
        progress_list = [
         self.panel.prog_blue, self.panel.prog_red]
        for eid in self.eids:
            bat = self.get_battle()
            index = 0 if bat.is_friend_group(eid) else 1
            hp_mech_progress = progress_list[index]
            from mobile.common.EntityManager import EntityManager
            puppet = EntityManager.getentity(eid)
            if hp_mech_progress and puppet and puppet.logic:
                mecha = puppet.logic.ev_g_control_target()
                update_mecha_health(hp_mech_progress, mecha)