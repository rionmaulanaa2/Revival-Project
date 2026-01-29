# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/RandomDeath/ChooseWeaponWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gcommon import const
from logic.comsys.effect import ui_effect
from logic.gutils.template_utils import get_item_quality
QUALITY_PIC = {item_const.NORMAL_GREEN: 'gui/ui_res_2/battle_random/btn_green.png',item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle_random/btn_blue.png',
   item_const.EPIC_PURPLE: 'gui/ui_res_2/battle_random/btn_purple.png',
   item_const.LEGEND_GILD: 'gui/ui_res_2/battle_random/btn_orange.png'
   }
CANDIDATE_WEAPON_BAR_PIC = {0: 'gui/ui_res_2/battle_random/bar_weapon_02.png',
   1: 'gui/ui_res_2/battle_random/bar_weapon_03.png'
   }

class ChooseWeaponWidgetNew(object):

    def __init__(self, panel):
        self.panel = panel
        self.weapon_id_2_ui_item = {}
        self.highlight_candidate_weapon_item = None
        self.highlight_selected_weapon_item = None
        self.selected_weapon_dict = None
        self.selected_weapon_index = 0
        self.cur_weapon_pos = None
        self.init_candidate_weapon_list()
        self.process_event(True)
        self.panel.temp_btn.btn_common_big.SetEnable(False)
        return

    def destroy(self):
        self.process_event(False)
        self.weapon_id_2_ui_item = None
        self.highlight_selected_weapon_item = None
        self.highlight_candidate_weapon_item = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_setted(self, player):
        pass

    def get_selected_weapon_dict(self):
        if self.selected_weapon_index:
            selected_index = self.selected_weapon_index if 1 else 1
            candidate_weapon_list = global_data.death_battle_data.get_weapon_list()
            return candidate_weapon_list or {}
        weapon_list_data = candidate_weapon_list[selected_index - 1]
        ret_select_weapon_data = {}
        for i, weapon_pos in enumerate(const.EXTRA_WEAPON_LIST):
            ret_select_weapon_data[weapon_pos] = weapon_list_data[i]

        return ret_select_weapon_data

    def init_candidate_weapon_list(self):
        candidate_weapon_list = global_data.death_battle_data.get_weapon_list()
        for i in range(1, 4):
            weapon_list_node = getattr(self.panel, 'btn_weapon_{}'.format(str(i)))
            weapon_list_view = weapon_list_node.list_weapon
            weapon_list_data = candidate_weapon_list[i - 1]
            weapon_list_view.SetInitCount(len(weapon_list_data))

            @weapon_list_node.unique_callback()
            def OnClick(btn, touch, choose_idx=i):
                self.on_click_candidate_weapon_item(choose_idx)

            for index, weapon_item in enumerate(weapon_list_view.GetAllItem()):
                weapon_id = int(weapon_list_data[index])
                weapon_item.name.SetString(item_utils.get_item_name(weapon_id))
                weapon_item.details.SetString(item_utils.get_item_desc(weapon_id))
                weapon_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(weapon_id))
                weapon_item.img_level.SetDisplayFrameByPath('', QUALITY_PIC.get(get_item_quality(weapon_id), 'gui/ui_res_2/battle_random/btn_orange.png'))

    def on_click_candidate_weapon_item(self, choose_idx):
        self.panel.temp_btn.btn_common_big.SetEnable(True)
        if choose_idx == self.selected_weapon_index:
            return
        if self.selected_weapon_index:
            weapon_list_node = getattr(self.panel, 'btn_weapon_{}'.format(str(self.selected_weapon_index)))
            weapon_list_node.SetSelect(False)
            weapon_list_view = weapon_list_node.list_weapon
            for index, weapon_item in enumerate(weapon_list_view.GetAllItem()):
                weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(0))

        self.selected_weapon_index = choose_idx
        weapon_list_node = getattr(self.panel, 'btn_weapon_{}'.format(str(choose_idx)))
        weapon_list_node.SetSelect(True)
        weapon_list_view = weapon_list_node.list_weapon
        for index, weapon_item in enumerate(weapon_list_view.GetAllItem()):
            weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(1))

    def get_selcet_weapon(self):
        return self.get_selected_weapon_dict()