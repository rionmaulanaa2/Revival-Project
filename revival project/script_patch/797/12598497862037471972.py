# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseWeaponConfUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from common.const import uiconst
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class ExerciseWeaponConfUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_weapon_entry'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_mall.OnClick': '_on_click_conf'
       }
    HOT_KEY_FUNC_MAP = {'exercise_weapon_config': '_on_click_conf_PC'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'exercise_weapon_config': {'node': 'nd_adjust_custom.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseWeaponConfUI, self).on_init_panel()
        self.process_events(True)
        self.init_custom_com()
        if global_data.is_pc_mode:
            self.panel.nd_adjust_custom.SetPosition('100%-49', self.panel.nd_adjust_custom.GetPosition()[1])
            self.panel.nd_adjust_custom.setScale(0.8)
        self.panel.lab_change.SetString(get_text_by_id(861001))
        self.select_tab_idx = 0

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'exercise_get_eq_tab': self.on_get_select_tab,
           'exercise_set_eq_tab': self.on_set_select_tab
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self):
        self.on_ctrl_target_changed()

    def switch_to_mecha(self):
        super(ExerciseWeaponConfUI, self).switch_to_mecha()
        self.hide()

    def switch_to_non_mecha(self):
        super(ExerciseWeaponConfUI, self).switch_to_non_mecha()
        self.show()

    def on_get_select_tab(self):
        return self.select_tab_idx

    def on_set_select_tab(self, idx):
        self.select_tab_idx = idx

    def _on_click_conf(self, *args, **kwargs):
        global_data.ui_mgr.show_ui('ExerciseEquipmentUI', module_path='logic.comsys.exercise_ui')
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def _on_click_conf_PC(self, *args, **kwargs):
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event('ExerciseWeaponConfUI', 'btn_mall', need_check_vis=True)

    def _config_weapon(self, weapon_pos):
        ui_mgr = global_data.ui_mgr
        ui_mgr.show_ui('ExerciseWeaponListUI', module_path='logic.comsys.exercise_ui')
        ui = ui_mgr.get_ui('ExerciseWeaponListUI')
        ui.selected_slot = weapon_pos
        ui.selected_wp_id = -1
        ui.switch_btn_group_slot()
        ui.on_click_switch_slot(weapon_pos, -1)

    def on_finalize_panel(self):
        self.select_tab_idx = 0
        self.process_events(False)
        self.destroy_widget('custom_ui_com')
        super(ExerciseWeaponConfUI, self).on_finalize_panel()