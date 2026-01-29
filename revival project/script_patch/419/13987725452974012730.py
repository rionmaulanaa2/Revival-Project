# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathWeaponChooseBtn.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.cfg import confmgr
from logic.gutils import item_utils
from common.const import uiconst

class DeathWeaponChooseBtn(BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_tdm/tdm_weapon_entry'
    HOT_KEY_FUNC_MAP = {'tdm_open_weapon': 'click_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'tdm_open_weapon': {'node': 'btn_mall.temp_pc'}}

    def on_init_panel(self):
        self.init_panel()
        self.init_event(True)
        self.init_custom_com()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_panel(self):
        self.set_panel_view()

        @self.panel.btn_mall.callback()
        def OnClick(btn, touch):
            is_show = False
            if global_data.death_battle_data:
                is_show = global_data.death_battle_data.get_is_in_base_part()
            if is_show:
                global_data.ui_mgr.show_ui('DeathChooseWeaponUI', 'logic.comsys.battle.Death')

    def click_btn(self, msg, keycode):
        self.panel.btn_mall.OnClick(None)
        return

    def set_panel_view(self):
        is_show = False
        if global_data.death_battle_data:
            is_show = global_data.death_battle_data.get_is_in_base_part()
        if is_show:
            self.show()
            self.play_choose_tip_animation()
        else:
            self.hide()
            global_data.ui_mgr.close_ui('DeathChooseWeaponUI')

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'death_in_base_part_change': self.set_panel_view,
           'death_first_check_in_base': self.set_panel_view
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def stop_choose_tip_animation(self):
        self.panel.StopAnimation('tips')

    def play_choose_tip_animation(self):
        self.panel.PlayAnimation('tips')

    def on_finalize_panel(self):
        self.init_event(False)
        self.destroy_widget('custom_ui_com')

    def do_show_panel(self):
        super(DeathWeaponChooseBtn, self).do_show_panel()
        global_data.emgr.death_weapon_choose_btn_visibility_change.emit(True)

    def do_hide_panel(self):
        super(DeathWeaponChooseBtn, self).do_hide_panel()
        global_data.emgr.death_weapon_choose_btn_visibility_change.emit(False)

    def on_change_ui_custom_data(self):
        ui = global_data.ui_mgr.get_ui('GuideUI')
        if ui:
            param = self.change_ui_data()
            ui.on_change_ui_inform_guide_mixed(param)

    def change_ui_data(self):
        scale_type_adjust_list = []
        pos_type_adjust_list = []
        need_to_adjust_scale_type_nodes = (('nd_adjust_custom', 'nd_weapon_entry', None), )
        for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            scale = nd.getScale()
            scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

        ret_dict = {'scale_type': scale_type_adjust_list,
           'pos_type': pos_type_adjust_list
           }
        return ret_dict