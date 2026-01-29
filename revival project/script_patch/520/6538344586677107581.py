# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonPassLevelUp.py
from __future__ import absolute_import
from logic.comsys.battle_pass.BpLevelUpBaseUI import BpLevelUpBaseUI
from logic.gutils.battle_pass_utils import is_sp_level_has_reward
from logic.gcommon.common_const import ui_operation_const as uoc

class SeasonPassLevelUp(BpLevelUpBaseUI):
    PANEL_CONFIG_NAME = 'battle_pass/battle_pass_level_up'
    UI_ACTION_EVENT = {'nd_logic.nd_btn_2.temp_btn_close.btn_common_big.OnClick': 'on_click_back_btn',
       'nd_logic.nd_btn_2.temp_btn_go.btn_common_big.OnClick': 'on_click_receive_btn',
       'nd_logic.nd_btn_1.temp_btn_close_1.btn_common_big.OnClick': 'on_click_back_btn'
       }

    def __new__(cls, *args, **kwargs):
        setting_enbale = global_data.player.get_setting_2(uoc.SEASON_LEVEL_UP_REMINDER_KEY)
        if not setting_enbale:
            return
        return super(SeasonPassLevelUp, cls).__new__(cls, *args, **kwargs)

    def on_init_panel(self):
        super(SeasonPassLevelUp, self).on_init_panel()
        self._additional_anim = ''

    def set_level(self, battle_pass_type, old_lv, new_lv):
        super(SeasonPassLevelUp, self).set_level(battle_pass_type, old_lv, new_lv)
        if is_sp_level_has_reward(int(new_lv), None) > 0:
            self.panel.nd_btn_2.setVisible(True)
            self.panel.nd_btn_1.setVisible(False)
            self._additional_anim = 'show_btn_2'
        else:
            self.panel.nd_btn_2.setVisible(False)
            self.panel.nd_btn_1.setVisible(True)
            self._additional_anim = 'show_btn_1'
        return

    def on_click_receive_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()
        from logic.gutils.jump_to_ui_utils import jump_to_season_pass
        jump_to_season_pass()

    def show_level_up(self):
        super(SeasonPassLevelUp, self).show_level_up()
        self.panel.StopAnimation('loop')
        anim_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.SetTimeOut(anim_time, lambda *args: self.panel.PlayAnimation('loop'))
        if self._additional_anim:
            self.panel.PlayAnimation(self._additional_anim)