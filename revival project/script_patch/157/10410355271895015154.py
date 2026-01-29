# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathChooseWeaponUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.client.const import game_mode_const
from logic.comsys.battle.Death.ChooseWeaponWidget import ChooseWeaponWidgetNew
from logic.comsys.archive import archive_key_const
EXCEPT_HIDE_UI_LIST = [
 'DeathBeginCountDown']

class DeathChooseWeaponUI(BasePanel):
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
        choose_weapon_nd = global_data.uisystem.load_template_create('battle_occupy/i_list_weapon_new', self.panel.temp_panel, name='choose_weapon_nd')
        choose_weapon_nd.SetPosition('50%', '50%')
        self.choose_weapon_widget = ChooseWeaponWidgetNew(choose_weapon_nd)

        @choose_weapon_nd.btn_sure.btn_major.cb_with_ani(self.panel.temp_button)
        def OnClick(btn, touch):
            self.on_send_data()
            self.close()
            self.send_close_event_for_guide()

        @choose_weapon_nd.temp_bg.btn_close.callback()
        def OnClick(_btn, touch):
            self.close()
            self.send_close_event_for_guide()

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
        if not global_data.player:
            return
        last_weapon = self.choose_weapon_widget.get_equiped_weapon_dict()
        weapon = self.choose_weapon_widget.get_selcet_weapon()
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        bat and bat.set_combat_weapons(weapon)
        key = archive_key_const.KEY_LAST_DEATH_CHOOSE_WEAPON
        key2 = archive_key_const.KEY_LAST_DEATH_CHOOSE_DOWN_WEAPON
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUMAN_DEATH):
            key = archive_key_const.KEY_LAST_HUMAN_DEATH_CHOOSE_WEAPON
            key2 = archive_key_const.KEY_LAST_HUMAN_DEATH_CHOOSE_DOWN_WEAPON
        version = global_data.player.get_settings_version()
        battle_type = global_data.player.get_battle().__class__.__name__
        global_data.player.update_data({'version': version,'weapon_settings.%s' % battle_type: weapon})
        global_data.death_battle_data.set_select_weapon_data(weapon)
        if last_weapon:
            change_down_weapon = list(set(six_ex.values(last_weapon)) - set(six_ex.values(weapon)))
            last_choose_down_weapon = global_data.death_battle_data.get_last_choose_down_weapon()
            for weapon_id in change_down_weapon:
                if weapon_id in last_choose_down_weapon:
                    last_choose_down_weapon.remove(weapon_id)
                last_choose_down_weapon.insert(0, weapon_id)

            last_choose_down_weapon = last_choose_down_weapon[:9]
            global_data.achi_mgr.save_general_archive_data_value(key2, last_choose_down_weapon)

    def count_down_start(self):
        pass

    def count_down_over(self):
        pass

    def send_close_event_for_guide(self):
        if not global_data.player or not global_data.player.logic:
            return
        global_data.player.logic.send_event('E_GUIDE_CLOSE_WEAPON_CHOOSE')