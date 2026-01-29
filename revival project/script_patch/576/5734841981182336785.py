# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/RandomDeath/RandomDeathChooseWeaponUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.client.const import game_mode_const
from logic.comsys.battle.RandomDeath.ChooseWeaponWidget import ChooseWeaponWidgetNew
from logic.comsys.archive import archive_key_const
import math
EXCEPT_HIDE_UI_LIST = [
 'DeathBeginCountDown']

class RandomDeathChooseWeaponUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/fight_tdm_count'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        self.init_parameters()
        self.init_event(True)
        self.init_panel()
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST)

    def on_finalize_panel(self):
        self.show_main_ui()
        self.init_event(False)
        self.choose_weapon_widget.destroy()

    def init_parameters(self):
        self.choose_weapon_widget = None
        return

    def init_panel(self):
        self.add_blocking_ui_list(['MechaUI', 'MechaUIPC'])
        self.panel.temp_button.setVisible(False)
        choose_weapon_nd = global_data.uisystem.load_template_create('battle_random/select_weapon', self.panel.temp_panel, name='choose_weapon_nd')
        choose_weapon_nd.SetPosition('50%', '50%')
        self.choose_weapon_widget = ChooseWeaponWidgetNew(choose_weapon_nd)

        @choose_weapon_nd.temp_btn.btn_common_big.cb_with_ani(self.panel.temp_button)
        def OnClick(btn, touch):
            self.on_send_data()
            self.close()

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'death_count_down_start': self.count_down_start,
           'death_count_down_over': self.count_down_over
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_send_data(self):
        weapon = self.choose_weapon_widget.get_selcet_weapon()
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        bat and bat.set_combat_weapons(weapon)

    def count_down_start(self):
        pass

    def count_down_over(self):
        pass

    def send_close_event_for_guide(self):
        if not global_data.player or not global_data.player.logic:
            return
        global_data.player.logic.send_event('E_GUIDE_CLOSE_WEAPON_CHOOSE')

    def on_delay_close(self, revive_time):

        def refresh_time_finsh():
            text = '\xe7\xa1\xae\xe5\xae\x9a\xe9\x80\x89\xe6\x8b\xa9\xef\xbc\x88{}\xe7\xa7\x92\xef\xbc\x89'.format(str(0))
            self.choose_weapon_widget.panel.temp_btn.btn_common_big.SetText(text)
            self.count_down_end()

        def refresh_time(pass_time):
            if not self.choose_weapon_widget.panel:
                return
            left_time = int(math.ceil(revive_time - pass_time))
            text = '\xe7\xa1\xae\xe5\xae\x9a\xe9\x80\x89\xe6\x8b\xa9\xef\xbc\x88{}\xe7\xa7\x92\xef\xbc\x89'.format(str(left_time))
            self.choose_weapon_widget.panel.temp_btn.btn_common_big.SetText(text)
            if left_time <= 0:
                self.choose_weapon_widget.panel.StopTimerAction()
                refresh_time_finsh()
                return

        self.choose_weapon_widget.panel.StopTimerAction()
        if revive_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        global_data.emgr.death_count_down_start.emit()
        self.choose_weapon_widget.panel.TimerAction(refresh_time, revive_time, interval=0.1)

    def count_down_end(self):
        self.close()
        global_data.emgr.death_count_down_over.emit()