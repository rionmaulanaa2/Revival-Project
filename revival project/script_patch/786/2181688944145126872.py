# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaModuleSpSelectUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_const import mecha_const
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from common.const import uiconst

class MechaModuleSpSelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_module_sp_choose'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    HOT_KEY_FUNC_MAP = {'first_sp_module_skill': 'select_first_sp_module_skill',
       'second_sp_module_skill': 'select_second_sp_module_skill'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'first_sp_module_skill': {'node': 'temp_pc_1'},'second_sp_module_skill': {'node': 'temp_pc_2'}}

    def on_init_panel(self):
        self.module_def_card_id_list = []
        from logic.gutils import template_utils
        ui_item = self.panel.nd_module_detials.temp_module
        fight_state_ui = global_data.ui_mgr.get_ui('FightStateUI')
        if fight_state_ui:
            fight_state_ui.add_hide_count(self.__class__.__name__)
        if global_data.player and global_data.player.logic:
            slot_conf = global_data.player.logic.ev_g_mecha_module_slot_conf(mecha_const.SP_MODULE_SLOT)
            module_def_card_id_list = [ card_id for card_id, module_id in slot_conf ]
            if len(module_def_card_id_list) >= 2:
                self.module_def_card_id_list = module_def_card_id_list
                template_utils.init_sp_choose_template(ui_item, mecha_const.SP_MODULE_CHOOSE_ITEM_ID, module_def_card_id_list[0], module_def_card_id_list[1], self.select_slot_function)
            else:
                log_error("MechaModuleSpSelectUI can't got data ", slot_conf)
        self.init_custom_com()
        self.check_distort()
        ui_item.PlayAnimation('show')

    def select_slot_function(self, sel_card_id):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'activate_module', (
             mecha_const.SP_MODULE_SLOT, sel_card_id), True, True)
            self.close()

    def check_distort(self):
        UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')
        fight_state_ui = global_data.ui_mgr.get_ui('FightStateUI')
        if fight_state_ui:
            fight_state_ui.add_show_count(self.__class__.__name__)

    def select_first_sp_module_skill(self, msg, keycode):
        if len(self.module_def_card_id_list) >= 2:
            self.select_slot_function(self.module_def_card_id_list[0])

    def select_second_sp_module_skill(self, msg, keycode):
        if len(self.module_def_card_id_list) >= 2:
            self.select_slot_function(self.module_def_card_id_list[1])