# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaDetailsForPuppet.py
from __future__ import absolute_import
from logic.gutils import mecha_skin_utils
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, ROTATE_FACTOR
from logic.comsys.mecha_display.MechaDetails import MechaDetails
from common.cfg import confmgr
from logic.gcommon.common_utils import decal_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX

class MechaDetailsForPuppet(MechaDetails):
    UI_ACTION_EVENT = {'nd_mech_touch.OnBegin': '_on_rotate_drag_begin',
       'nd_mech_touch.OnDrag': '_on_rotate_drag',
       'nd_mech_touch.OnEnd': '_on_rotate_drag_end',
       'temp_btn_back.btn_back.OnClick': '_on_click_back_btn',
       'nd_btn_mech_change.btn_last_mech.OnClick': '_on_show_last_mecha',
       'nd_btn_mech_change.btn_next_mech.OnClick': '_on_show_next_mecha',
       'btn_left.OnClick': '_on_click_btn_left'
       }
    GLOBAL_EVENT = {'change_mecha_view_type': 'switch_view_type',
       'change_mecha_view_zoom': '_on_change_mecha_view_zoom',
       'fold_mecha_details_widget': '_on_fold_mecha_details_widget'
       }

    def on_init_panel(self, *args, **kwargs):
        self._puppet_uid = None
        self.puppet_org_mecha_dict = {}
        self.regist_main_ui()
        super(MechaDetailsForPuppet, self).on_init_panel(*args, **kwargs)
        self.panel.list_price.setVisible(False)
        self.set_is_for_puppet()
        return

    def init_open_lst(self):
        super(MechaDetailsForPuppet, self).init_open_lst()

    def on_finalize_panel(self):
        self._puppet_uid = None
        self.puppet_org_mecha_dict = {}
        self.unregist_main_ui()
        super(MechaDetailsForPuppet, self).on_finalize_panel()
        return

    def init_parameters(self):
        super(MechaDetailsForPuppet, self).init_parameters()
        self.BASIC_INFO_WIDGET_IND = -4
        self.SKILL_WIDGET_IND = -3
        self.STORY_WIDGET_IND = -2
        self.MODULE_WIDGET_IND = -1
        self.MEMORY_WIDGET_IND = 0
        self.tab_list_data = [
         {'text': 81607,
            'widget_func': self.init_mecha_career_widget,
            'widget_template': 'mech_display/career/i_mech_career_info'
            }]

    def init_tab_list(self):
        super(MechaDetailsForPuppet, self).init_tab_list()

    def show_puppet_skin_details(self, uid, mecha_id, mecha_dict):
        self._puppet_uid = uid
        self.puppet_org_mecha_dict = mecha_dict
        self.show_mecha_details(mecha_id)

    def init_mecha_career_widget(self, nd):
        from logic.comsys.mecha_display.mecha_memory.MechaMemoryWidget import MechaMemoryWidget
        widget = MechaMemoryWidget(self, nd, self._cur_mecha_id, puppet_uid=self._puppet_uid)
        return widget

    def get_mecha_decal(self, clothing_id):
        _mecha_decal_list = []
        if self.puppet_org_mecha_dict:
            mecha_fashion_dict = self.puppet_org_mecha_dict.get('mecha_fashion', {}).get(str(self._cur_mecha_id), {})
            data_clothing_id = mecha_fashion_dict.get('fashion', {}).get(FASHION_POS_SUIT, -1)
            if str(data_clothing_id) == str(clothing_id):
                decal_list = mecha_fashion_dict.get('custom_skin', {}).get('decal', [])
                _mecha_decal_list = decal_utils.decode_decal_list(decal_list)
                return _mecha_decal_list
        return _mecha_decal_list

    def get_mecha_color(self, clothing_id):
        _mecha_color_dict = {}
        if self.puppet_org_mecha_dict:
            mecha_fashion_dict = self.puppet_org_mecha_dict.get('mecha_fashion', {}).get(str(self._cur_mecha_id), {})
            data_clothing_id = mecha_fashion_dict.get('fashion', {}).get(FASHION_POS_SUIT, -1)
            if str(data_clothing_id) == str(clothing_id):
                color_dict = mecha_fashion_dict.get('custom_skin', {}).get('color', {})
                _mecha_color_dict = decal_utils.decode_color(color_dict) or {}
                return _mecha_color_dict
        return _mecha_color_dict

    def get_mecha_fashion(self, cur_mecha_item_id):
        clothing_id = -1
        if self.puppet_org_mecha_dict:
            battle_mecha_id = mecha_lobby_id_2_battle_id(self._cur_mecha_id)
            mecha_fashion_dict = self.puppet_org_mecha_dict.get('mecha_fashion', {}).get(str(battle_mecha_id), {})
            clothing_id = mecha_fashion_dict.get('fashion', {}).get(FASHION_POS_SUIT, -1)
        if clothing_id == -1:
            clothing_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
        return clothing_id

    def get_mecha_lobby_mode_data(self, item_no):
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        if self.puppet_org_mecha_dict and model_data:
            mecha_fashion_dict = self.puppet_org_mecha_dict.get('mecha_fashion', {}).get(str(self._cur_mecha_id), {})
            weapon_sfx = mecha_fashion_dict.get('fashion', {}).get(FASHION_POS_WEAPON_SFX)
            clothing_id = mecha_fashion_dict.get('fashion', {}).get(FASHION_POS_SUIT, -1)
            for model_data_item in model_data:
                if model_data_item.get('skin_id') == clothing_id:
                    model_data_item['shiny_weapon_id'] = weapon_sfx

        return model_data