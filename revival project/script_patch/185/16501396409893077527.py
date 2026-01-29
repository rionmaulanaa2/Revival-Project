# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/SnatchEggEndUI.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.battle.Death.DeathEndUI import DeathEndUI
from logic.gcommon.ctypes.BattleReward import BattleReward
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL
import math
from logic.gutils.template_utils import init_crystal_icon_list
from logic.gcommon.common_const.battle_const import CRYSTAL_LORE_DAMAGE
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL

class SnatchEggEndUI(DeathEndUI):
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, settle_dict=None, finish_cb=None, count_down=10):
        self.regist_main_ui()
        self.hide_main_ui()
        self.count_donw = count_down
        super(SnatchEggEndUI, self).on_init_panel(settle_dict, finish_cb)
        self.panel.nd_touch_layer.setVisible(True)
        self.panel.nd_touch_layer.SetSwallowTouch(True)
        self.panel.nd_touch_layer.BindMethod('OnClick', self.on_click_empty)

    def on_click_empty(self, *args):
        pass

    def on_finalize_panel(self):
        self.show_main_ui()
        self.unregist_main_ui()
        super(SnatchEggEndUI, self).on_finalize_panel()

    def get_self_group_id(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_group_id(exclude_observe=True)
        else:
            if global_data.player and global_data.battle:
                group_dict = global_data.battle.get_group_loading_dict()
                a_group_id = None
                for gid, g_info in six_ex.items(group_dict):
                    if global_data.player.id in g_info:
                        a_group_id = gid
                        break

                return a_group_id
            return

    def cal_result_display_para(self, settle_dict):
        if not settle_dict:
            anim = 'promote'
            sound_name = 'bt_victory'
            return (
             anim, None, sound_name)
        else:
            self_group_id = self.get_self_group_id()
            group_dict = settle_dict.get('extra_detail', {}).get('group_round_egg_cnt_dict')
            is_draw = settle_dict.get('is_draw')
            if is_draw:
                anim = 'deuce'
                sound_name = 'bt_draw'
                return (
                 anim, None, sound_name)
            if not group_dict:
                anim = 'defeat'
                sound_name = 'bt_failure'
                return (
                 anim, None, sound_name)
            self_score = group_dict.get(str(self_group_id), 0)
            reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
            if self_score > 0:
                anim = 'win'
                sound_name = 'bt_victory'
            elif all([ i == 0 for i in six_ex.values(group_dict) ]):
                anim = 'deuce'
                sound_name = 'bt_draw'
            elif self_score == 0 and any([ i != 0 for i in six_ex.values(group_dict) ]):
                anim = 'defeat'
                sound_name = 'bt_failure'
            else:
                anim = 'win'
                sound_name = 'bt_victory'
            score_anim = None
            return (
             anim, score_anim, sound_name)

    def get_is_win(self, settle_dict):
        if not settle_dict:
            return True
        else:
            group_dict = settle_dict.get('extra_detail', {}).get('group_round_egg_cnt_dict')
            self_group_id = self.get_self_group_id()
            self_score = group_dict.get(str(self_group_id), 0)
            if self_score > 0:
                return True
            return False

    def get_has_next_round(self, settle_dict):
        replay_dict = settle_dict.get('reply_data', {})
        is_draw = settle_dict.get('is_draw')
        group_dict = settle_dict.get('extra_detail', {}).get('group_round_egg_cnt_dict')
        has_next_round_count = 0
        for g_id in six.iterkeys(group_dict):
            if group_dict[g_id]:
                has_next_round_count += 1

        if not is_draw and has_next_round_count > 1:
            return True
        return False

    def begin_show(self, settle_dict, finish_cb):
        self.finish_cb = finish_cb
        self._old_lv = settle_dict.get('lv')
        self._old_exp = settle_dict.get('exp')
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        self._add_exp = battle_reward.exp
        anim, score_anim, sound_name = self.cal_result_display_para(settle_dict)
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.panel.nd_btn.setVisible(True)
        is_win = self.get_is_win(settle_dict)
        if is_win:

            @self.panel.nd_btn.temp_btn_1.btn_common.callback()
            def OnClick(btn, touch):
                pass

            @self.panel.nd_btn.temp_btn_2.btn_common.callback()
            def OnClick(btn, touch):
                self.on_click_next()

            self.panel.nd_btn.temp_btn_1.setVisible(False)
            self.panel.nd_btn.temp_btn_2.setVisible(True)
            self.start_count_down(self.panel.nd_btn.temp_btn_2.btn_common, 80613, self.count_donw)
        else:

            @self.panel.nd_btn.temp_btn_1.btn_common.callback()
            def OnClick(btn, touch):
                self.on_click_next()

            @self.panel.nd_btn.temp_btn_2.btn_common.callback()
            def OnClick(btn, touch):
                self._on_click_btn_watch()

            has_next_round = self.get_has_next_round(settle_dict)
            self.panel.nd_btn.temp_btn_1.setVisible(True)
            if not has_next_round:
                self.panel.nd_btn.temp_btn_2.btn_common.SetEnable(False)
            self.start_count_down(self.panel.nd_btn.temp_btn_1.btn_common, 80374, self.count_donw)
            self.panel.nd_btn.temp_btn_2.btn_common.SetText(80555)

    def _on_click_btn_watch(self, *args):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_REQ_SPECTATE')

    def start_count_down(self, btn, tid, total_time):

        def update_count_down(pass_time):
            left_time = int(total_time - int(pass_time))
            txt = get_text_by_id(tid)
            if '{time}' in txt:
                time_str = txt.format(time=left_time)
            else:
                time_str = txt + '(%ds)' % left_time
            btn.SetText(time_str)

        def update_count_down_finished():
            self.on_click_next()

        btn.StopTimerAction()
        if total_time < 0:
            update_count_down_finished()
            return
        update_count_down(pass_time=0)
        btn.TimerAction(update_count_down, total_time, callback=update_count_down_finished, interval=1)


class SnatchEggPromoteUI(SnatchEggEndUI):
    pass


class SnatchEggEndObserveUI(SnatchEggEndUI):

    def _is_ob_settle(self):
        from logic.gutils import judge_utils
        return judge_utils.is_ob()

    def get_self_group_id(self):
        if self._is_ob_settle():
            return self._settle_dict.get('ob_data', {}).get('watching_settle_id', None)
        else:
            if global_data.cam_lplayer:
                return global_data.cam_lplayer.ev_g_group_id(exclude_observe=True) or global_data.cam_lplayer.ev_g_group_id()
            return self._settle_dict.get('ob_data', {}).get('watching_settle_id', None)
            return None