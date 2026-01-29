# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndLevelUI.py
from __future__ import absolute_import
from common import utilities
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp, get_cur_lv_reward, init_lv_template
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
import common.utils.timer as timer
TICK_INTERVAL = 0.033
from common.const import uiconst

class EndLevelUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_level_up'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self._old_lv = 1
        self._new_lv = self._old_lv
        self._gold = 1
        self._close_cb = None
        self.tick_timer = None
        return

    def play_animation(self, data):
        self._old_lv = data.get('old_lv', 1)
        self._new_lv = data.get('new_lv', global_data.player.get_lv())
        self._old_exp = data.get('old_exp', 1)
        self._add_exp = data.get('add_exp', 1)
        self._close_cb = data.get('close_cb', None)
        self._gold = 0
        self._cur_show_lv = self._old_lv
        if self._new_lv != self._old_lv:
            self.panel.nd_exp_up.setVisible(False)
            self.panel.nd_award.setVisible(True)
            self.set_level(self._old_lv)
            show_lv_list = []
            while self._old_exp + self._add_exp > get_lv_upgrade_need_exp(self._old_lv):
                show_lv_list.append(self._old_lv)
                self._old_exp = 0
                self._add_exp = self._old_exp + self._add_exp - get_lv_upgrade_need_exp(self._old_lv)
                self._old_lv += 1

            self._cur_show_lv = self._new_lv
            self.show_lv_up_animation()
        else:
            self.panel.nd_exp_up.setVisible(False)
            self.panel.nd_award.setVisible(False)
            self.show_exp_up_animation()
        global_data.sound_mgr.play_ui_sound('level_up')
        return

    def show_exp_up_animation(self):
        self.panel.lab_name.SetString(82012)
        self.set_level(self._cur_show_lv)
        self.panel.StopAnimation('appear')
        self.panel.PlayAnimation('appear')
        self.panel.DelayCall(23 * TICK_INTERVAL, self.show_add_exp)

    def show_lv_up_animation(self):
        self.panel.lab_name.SetString(80792)
        lv = self._cur_show_lv
        item_no, self._gold = get_cur_lv_reward(lv + 1)
        self.panel.nd_award.setVisible(self._gold > 0)
        pic_path = get_lobby_item_pic_by_item_no(item_no)
        self.panel.img_money.SetDisplayFrameByPath('', pic_path)
        self.panel.lab_money.SetString(str(0))
        self.set_level(lv)
        self.panel.StopAnimation('appear')
        self.panel.PlayAnimation('appear')
        self.panel.DelayCall(10 * TICK_INTERVAL, self.level_up, lv, True)
        self.panel.DelayCall(23 * TICK_INTERVAL, self.show_add_gold)

    def on_finalize_panel(self):
        if self.tick_timer:
            global_data.game_mgr.unregister_logic_timer(self.tick_timer)
        if self._close_cb:
            self._close_cb()
            self._close_cb = None
        return

    def on_click_close_btn(self, *args):
        self.close()

    def set_level(self, lv):
        init_lv_template(self.panel.nd_level, lv)

    def level_up(self, lv, paly_animate=False):
        self.set_level(lv)
        if paly_animate and int(lv) >= 100:
            self.panel.nd_level.PlayAnimation('break_level')

    def show_add_gold(self):
        tick_count = 20
        self.show_gold = 0
        gold_step = int(self._gold / (tick_count - 1))

        def finish():
            self.panel.lab_money.SetString(str(self._gold))

        def update_progress_time(dt):
            self.show_gold += gold_step
            if self.show_gold > self._gold:
                self.show_gold = self._gold
            self.panel.lab_money.SetString(str(int(self.show_gold)))

        self.panel.TimerAction(update_progress_time, tick_count * TICK_INTERVAL, callback=finish, interval=TICK_INTERVAL)

    def show_add_exp(self):
        self.panel.nd_exp_up.setVisible(True)
        total_exp = get_lv_upgrade_need_exp(self._cur_show_lv)
        show_exp = self._old_exp
        target_exp = self._old_exp + self._add_exp
        show_exp_percent = float(show_exp) / total_exp
        target_exp_percent = float(target_exp) / total_exp
        self.panel.lab_exp.SetString('{}/{}'.format(show_exp, total_exp))
        self.panel.prog_exp.SetPercentage(show_exp_percent * 100)
        self.panel.prog_exp_pre.SetPercentage(target_exp_percent * 100)
        last_time = (target_exp_percent - show_exp_percent) * 0.5 or 1
        step_exp = self._add_exp / last_time

        def finish():
            self.panel.lab_exp.SetString('{}/{}'.format(target_exp, total_exp))
            self.panel.prog_exp.SetPercentage(target_exp_percent * 100)

        def update_progress_time(dt):
            update_exp = utilities.lerp(show_exp, target_exp, dt / last_time)
            self.panel.lab_exp.SetString('{}/{}'.format(int(update_exp), int(total_exp)))
            self.panel.prog_exp.SetPercentage(float(update_exp) / total_exp * 100)

        self.panel.TimerAction(update_progress_time, last_time, callback=finish, interval=TICK_INTERVAL)