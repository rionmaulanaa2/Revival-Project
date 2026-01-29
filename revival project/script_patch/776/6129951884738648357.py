# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseWeaponListUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gutils.template_utils import get_item_quality
from logic.gcommon.const import EXTRA_WEAPON_LIST
from common.const import uiconst

class ExerciseWeaponListUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_change_weapon'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_sure.btn_major.OnClick': '_on_click_confirm'
       }
    HOT_KEY_FUNC_MAP = {'exercise_weapon_config_close': '_on_click_close_PC',
       'cancel_action': '_on_click_close_PC'
       }
    SLOT_BG = {item_const.NONE_WHITE: 'gui/ui_res_2/battle_train/img_white.png',item_const.NORMAL_GREEN: 'gui/ui_res_2/battle_train/img_green.png',
       item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle_train/img_blue.png',
       item_const.EPIC_PURPLE: 'gui/ui_res_2/battle_train/img_purple.png',
       item_const.LEGEND_GILD: 'gui/ui_res_2/battle_train/img_orange.png'
       }
    EMPTY_WP_PIC = 'gui/ui_res_2/battle_train/img_shadow.png'
    ITEM_BG = {0: 'gui/ui_res_2/battle_train/img_change_floor_0.png',1: 'gui/ui_res_2/battle_train/img_change_floor_2.png'
       }
    LV_ICON = {item_const.NORMAL_GREEN: 'gui/ui_res_2/battle_train/btn_green.png',item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle_train/btn_blue.png',
       item_const.EPIC_PURPLE: 'gui/ui_res_2/battle_train/btn_purple.png',
       item_const.LEGEND_GILD: 'gui/ui_res_2/battle_train/btn_orange.png'
       }
    selected_slot = 1
    selected_wp_id = -1
    selected_wp_idx = -1

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseWeaponListUI, self).on_init_panel()
        self.hide_main_ui()
        self.panel.temp_bg.PlayAnimation('in')
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

        @self.temp_bg.btn_close.callback()
        def OnClick(*args):
            self.close()
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count('ExerciseWeaponConfUI')

        self.process_events(True)
        self.init_data()
        self.init_right_weapon_list()
        self.init_left_weapon_list()
        self.init_lv_list()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_data(self):
        map_data = confmgr.get('game_mode/exercise/c_map_exercise_conf')
        self.weapons_data = map_data['Weapon']['Content']
        self.wp_conf_dict = {}
        logic = global_data.player.logic if global_data.player else None
        for slot in EXTRA_WEAPON_LIST:
            slot_wp_data = logic.ev_g_weapon_data(slot)
            if slot_wp_data is not None:
                self.wp_conf_dict[slot] = slot_wp_data.get('item_id', None)

        return

    def init_right_weapon_list(self):
        self.list_weapon_1.SetInitCount(3)
        self.switch_btn_group_slot()
        self.update_right_weapon_list()

    def update_right_weapon_list(self):
        all_items = self.list_weapon_1.GetAllItem()
        for index, ui_item in enumerate(all_items):
            slot = index + 1
            cur_wp_id = self.wp_conf_dict.get(slot, -1)
            if cur_wp_id == -1:
                ui_item.sp_weapon.SetDisplayFrameByPath('', self.EMPTY_WP_PIC)
                ui_item.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(item_const.NONE_WHITE))
                ui_item.img_exchange.setVisible(False)
            else:
                cur_wp_lv = get_item_quality(cur_wp_id)
                ui_item.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(cur_wp_id))
                ui_item.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(cur_wp_lv))
                ui_item.img_exchange.setVisible(True)

            @ui_item.btn_weapon.callback()
            def OnClick(_btn, _touch, _slot=slot, _id=cur_wp_id):
                self.selected_slot = _slot
                self.selected_wp_id = _id
                self.switch_btn_group_slot()
                self.on_click_switch_slot(_slot, _id)

    def switch_btn_group_slot(self):
        all_items = self.list_weapon_1.GetAllItem()
        for index, ui_item in enumerate(all_items):
            slot = index + 1
            if slot == self.selected_slot:
                ui_item.choose.setVisible(True)
            else:
                ui_item.choose.setVisible(False)

    def on_click_switch_slot(self, slot, wp_id):
        self.selected_slot = slot
        self.update_left_weapon_list()
        self.init_lv_list()

    def init_left_weapon_list(self):
        item_count = len(self.weapons_data)
        self.list_weapon_2.SetInitCount(item_count)
        all_items = self.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            wp_dict = self.weapons_data[str(idx)]
            wp_id_default = wp_dict['list_id'][0]
            ui_item.name.SetString(item_utils.get_item_name(wp_id_default))
            ui_item.details.SetString(item_utils.get_item_desc(wp_id_default))
            ui_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(wp_id_default))

        self.update_left_weapon_list()

    def update_left_weapon_list(self):
        slot = self.selected_slot
        selected_wp_id = self.wp_conf_dict.get(slot, -1)
        all_items = self.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            item_wp_dict = self.weapons_data[str(idx)]
            item_wp_list_id = item_wp_dict.get('list_id', [])
            if selected_wp_id in item_wp_list_id:
                ui_item.choose.setVisible(True)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(1))
            else:
                ui_item.choose.setVisible(False)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(0))
            item_wp_id = item_wp_list_id[-1]

            @ui_item.btn_item.callback()
            def OnClick(_btn, _touch, _slot=slot, _id=item_wp_id, _idx=idx):
                self.switch_btn_group_item(_idx)
                self.on_click_switch_item(_slot, _id)

    def switch_btn_group_item(self, select_idx):
        all_items = self.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            if idx == select_idx:
                ui_item.choose.setVisible(True)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(1))
            else:
                ui_item.choose.setVisible(False)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(0))

    def on_click_switch_item(self, slot, wp_id):
        slot_ui = self.list_weapon_1.GetItem(slot - 1)
        wp_lv = get_item_quality(wp_id)
        slot_ui.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(wp_id))
        slot_ui.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(wp_lv))
        slot_ui.img_exchange.setVisible(True)
        self.wp_conf_dict[slot] = wp_id
        self.init_lv_list()

    def init_lv_list(self):
        slot = self.selected_slot
        selected_wp_id = self.wp_conf_dict.get(slot, -1)
        self.lab_tips.SetString(5078)
        if selected_wp_id == -1:
            self.nd_level.setVisible(False)
            return
        self.nd_level.setVisible(True)
        selected_wp_lv = get_item_quality(selected_wp_id)
        for index in range(0, self.list_weapon_2.GetItemCount()):
            item_wp_dict = self.weapons_data[str(index)]
            item_wp_list_id = item_wp_dict.get('list_id', [])
            if selected_wp_id in item_wp_list_id:
                self.list_level.SetInitCount(len(item_wp_list_id))
                all_items = self.list_level.GetAllItem()
                for idx, ui_item in enumerate(all_items):
                    wp_id = item_wp_list_id[idx]
                    lv = get_item_quality(wp_id)
                    ui_item.icon_level.SetDisplayFrameByPath('', self.LV_ICON.get(lv, self.LV_ICON[1]))
                    if lv == selected_wp_lv:
                        ui_item.btn_level.SetSelect(True)
                    else:
                        ui_item.btn_level.SetSelect(False)

                    @ui_item.btn_level.callback()
                    def OnClick(_btn, _touch, _slot=slot, _id=wp_id, _idx=idx):
                        self.switch_btn_group_lv(_idx)
                        self.on_click_switch_item(_slot, _id)

                break

    def switch_btn_group_lv(self, select_lv):
        all_items = self.list_level.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            if idx == select_lv:
                ui_item.btn_level.SetSelect(True)
            else:
                ui_item.btn_level.SetSelect(False)

    def _on_click_confirm(self, *args, **kwargs):
        global_data.player.get_battle().call_soul_method('set_combat_weapons', (self.wp_conf_dict,))
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count('ExerciseWeaponConfUI')
        self.close()

    def _on_click_close_PC(self, *args, **kwargs):
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event('ExerciseWeaponListUI', 'temp_bg.btn_close', need_check_vis=True)

    def on_finalize_panel(self):
        self.process_events(False)
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        self.show_main_ui()
        super(ExerciseWeaponListUI, self).on_finalize_panel()