# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FightBagUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.client.const import pc_const
from logic.gutils import pc_utils
from common.const import uiconst
MODE_BAG_UI = {game_mode_const.GAME_MODE_PVE_EDIT: 'PVEInfoUI',
   game_mode_const.GAME_MODE_PVE: 'PVEInfoUI'
   }

class FightBagUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_bag'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_bag.OnClick': 'on_click_bag_btn',
       'btn_mech_bag.OnClick': 'on_click_bag_btn'
       }
    GLOBAL_EVENT = {'switch_control_target_event': 'on_ctrl_target_changed',
       'scene_observed_player_setted_event': 'on_observed_player_setted',
       'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled'
       }
    ENABLE_HOT_KEY_SUPPORT = True
    HOT_KEY_FUNC_MAP_SHOW = {'switch_battle_bag': {'node': ['nd_bag.temp_pc', 'nd_mech_bag.temp_pc']}}

    def on_init_panel(self, *args, **kwargs):
        self.init_custom_com()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        self._set_human_mode_bag_ui()
        if global_data.is_pc_mode:
            self.hide()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        show = pc_utils.should_pc_key_hint_related_uis_show(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON, hint_switch, display_option, pc_op_mode)
        if show:
            self.add_show_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)
        else:
            self.add_hide_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)

    def on_click_bag_btn(self, *args):
        if global_data.player and global_data.player.logic:
            if not global_data.player.logic.ev_g_is_in_spectate():
                bag_ui_name = MODE_BAG_UI.get(global_data.game_mode.get_mode_type(), 'BagUI')
                bagui = global_data.ui_mgr.get_ui(bag_ui_name)
                if not bagui:
                    global_data.ui_mgr.show_ui(bag_ui_name, 'logic.comsys.control_ui')
                    bagui = global_data.ui_mgr.get_ui(bag_ui_name)
                if bagui:
                    bagui.appear()

    def on_observed_player_setted(self, lplayer):
        if lplayer.__class__.__name__ != 'LAvatar':
            self.panel.nd_bag.setVisible(False)
            self.panel.nd_mech_bag.setVisible(False)

    def on_ctrl_target_changed(self, *args):
        if global_data.cam_lplayer.__class__.__name__ != 'LAvatar':
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.panel.nd_bag.setVisible(False)
            self.panel.nd_mech_bag.setVisible(True)
        else:
            self.panel.nd_bag.setVisible(True)
            self.panel.nd_mech_bag.setVisible(False)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SCAVENGE,))
    def _set_human_mode_bag_ui(self):
        self.panel.nd_bag.setVisible(True)
        self.panel.nd_mech_bag.setVisible(False)