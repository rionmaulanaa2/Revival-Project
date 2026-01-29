# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseWeaponWidget.py
from __future__ import absolute_import
import six
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gcommon.const import EXTRA_WEAPON_LIST
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const
from logic.gutils.template_utils import get_item_quality
from logic.gutils import item_utils
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
import copy

class ExerciseWeaponWidget(BaseUIWidget):
    SLOT_BG = {item_const.NONE_WHITE: 'gui/ui_res_2/battle_train/img_white.png',
       item_const.NORMAL_GREEN: 'gui/ui_res_2/battle_train/img_green.png',
       item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle_train/img_blue.png',
       item_const.EPIC_PURPLE: 'gui/ui_res_2/battle_train/img_purple.png',
       item_const.LEGEND_GILD: 'gui/ui_res_2/battle_train/img_orange.png',
       item_const.TDM_DARK: 'gui/ui_res_2/battle_train/img_dark.png'
       }
    EMPTY_WP_PIC = 'gui/ui_res_2/battle_train/img_shadow.png'
    ITEM_BG = {0: 'gui/ui_res_2/battle_train/pnl_weapon.png',1: 'gui/ui_res_2/battle_train/pnl_weapon1.png'
       }
    LV_ICON = {item_const.NORMAL_GREEN: 'gui/ui_res_2/battle_train/btn_green.png',
       item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle_train/btn_blue.png',
       item_const.EPIC_PURPLE: 'gui/ui_res_2/battle_train/btn_purple.png',
       item_const.LEGEND_GILD: 'gui/ui_res_2/battle_train/btn_orange.png',
       item_const.TDM_DARK: 'gui/ui_res_2/battle_train/btn_dark.png'
       }
    selected_right_idx = -1
    selected_left_idx = -1
    selected_lv_idx = -1

    def __init__(self, parent, panel):
        self.global_events = {}
        super(ExerciseWeaponWidget, self).__init__(parent, panel)
        self.init_params()
        self.init_data()
        self.init_right_weapon_list()
        self.init_left_weapon_list()
        self.init_lv_list()
        self.parent.weapon_widget = self
        try:
            self.panel.list_weapon_1.GetItem(0).btn_weapon.OnClick(TouchMock())
        except Exception as e:
            pass

    def destroy(self):
        self.upload_wp_conf()
        self.init_params()
        super(ExerciseWeaponWidget, self).destroy()

    def show(self):
        super(ExerciseWeaponWidget, self).show()

    def hide(self):
        super(ExerciseWeaponWidget, self).hide()

    def init_params(self):
        self.wp_conf_dict = {}
        self.ori_wp_conf_dict = {}
        self.right_2_left_idx_dict = {}
        self.lv_items_pos = []
        self.cur_index = 0

    def init_weapon_data(self):
        battle_wp_conf = confmgr.get('items_book_conf', 'WeaponConfig', 'Content', default={})
        wp_tab_conf = confmgr.get('items_book_conf', 'WeaponTabConfig', 'Content', default={})
        classify_help_map = {}
        wp_2_idx_map = {}
        for k, v in six.iteritems(battle_wp_conf):
            for wp in v['battle_item_no']:
                classify_help_map[wp] = k

        for idx, wp_tab in six.iteritems(wp_tab_conf):
            for wp in wp_tab['second_tabs']:
                wp_2_idx_map[str(wp)] = int(idx)

        for i, wp_list in six.iteritems(self.weapons_data[self.cur_index]):
            list_id = wp_list.get('list_id', [])
            if list_id:
                wp_idx = classify_help_map.get(list_id[0], None)
                index = wp_2_idx_map.get(wp_idx, -1)
                if index > 0:
                    wp_dat = self.weapons_data.setdefault(index, {})
                    wp_dat[str(len(wp_dat))] = {'list_id': list_id}

        return

    def init_data(self):
        map_data = confmgr.get('game_mode/exercise/c_map_exercise_conf')
        self.weapons_data = {0: map_data['Weapon']['Content']}
        self.init_weapon_data()
        self.wp_conf_dict = {}
        if global_data.player and global_data.player.logic:
            for slot in EXTRA_WEAPON_LIST:
                slow_wp_data = global_data.player.logic.ev_g_weapon_data(slot)
                if slow_wp_data is not None:
                    self.wp_conf_dict[slot] = slow_wp_data.get('item_id', None)

        self.ori_wp_conf_dict = copy.deepcopy(self.wp_conf_dict)
        self.right_2_left_idx_dict = {}
        self.lv_items_pos = []
        return

    def init_right_weapon_list(self):
        self.panel.lab_title_2.SetString(get_text_by_id(861007))
        self.panel.list_weapon_1.SetInitCount(len(self.wp_conf_dict))
        self.switch_right_list_item(-1)
        all_items = self.panel.list_weapon_1.GetAllItem()
        for index, ui_item in enumerate(all_items):
            slot = index + 1
            cur_wp_id = self.wp_conf_dict.get(slot, -1)
            if cur_wp_id == -1:
                ui_item.sp_weapon.SetDisplayFrameByPath('', self.EMPTY_WP_PIC)
                ui_item.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(item_const.NONE_WHITE))
                ui_item.lab_weapon_name.SetString(' ')
            else:
                cur_wp_lv = get_item_quality(cur_wp_id)
                ui_item.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(cur_wp_id))
                ui_item.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(cur_wp_lv))
                ui_item.lab_weapon_name.SetString(item_utils.get_item_name(cur_wp_id))

            @ui_item.btn_weapon.callback()
            def OnClick(_btn, _touch, _idx=index):
                self.on_click_right_item(_idx)

    def on_switch_tab(self, idx):
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(self.cur_index).btn_window_tab.SetSelect(False)
        self.parent.temp_bg.list_tab.GetItem(0).list_btn_right.GetItem(idx).btn_window_tab.SetSelect(True)
        self.cur_index = idx
        self.panel.list_weapon_2.SetInitCount(len(self.weapons_data[idx]))
        all_items = self.panel.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            wp_dict = self.weapons_data[self.cur_index][str(idx)]
            wp_id_default = wp_dict['list_id'][0]
            ui_item.name.SetString(item_utils.get_item_name(wp_id_default))
            ui_item.details.SetString(item_utils.get_item_desc(wp_id_default))
            ui_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(wp_id_default))

        if len(self.panel.list_weapon_2.GetAllItem()) > self.selected_left_idx >= 0:
            ui_item = self.panel.list_weapon_2.GetItem(self.selected_left_idx)
            ui_item.choose.setVisible(False)
            ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(0))
        self.selected_left_idx = -1
        self.right_2_left_idx_dict = {}
        self.on_click_right_item(self.selected_right_idx)

    def on_switch_widget(self):
        tab_right = self.parent.temp_bg.list_tab.GetItem(0).list_btn_right
        tab_right.SetInitCount(len(self.weapons_data))
        tab_conf = confmgr.get('items_book_conf', 'WeaponTabConfig', 'Content', default={})
        for i, item in enumerate(tab_right.GetAllItem()):
            if i == 0:
                item.btn_window_tab.SetText(get_text_by_id(634134))
            else:
                item.btn_window_tab.SetText(get_text_by_id(tab_conf.get(str(i), {}).get('tab_name_id'), 0))

            @item.btn_window_tab.unique_callback()
            def OnClick(_btn, _touch, _idx=i, *args):
                if global_data.player and global_data.player.logic:
                    self.on_switch_tab(_idx)

    def on_click_right_item(self, idx):
        self.switch_right_list_item(idx)
        self.update_left_weapon_list(idx)
        self.update_lv_list(idx)

    def switch_right_list_item(self, idx):
        if idx != self.selected_right_idx:
            if self.selected_right_idx != -1:
                ui_item = self.panel.list_weapon_1.GetItem(self.selected_right_idx)
                ui_item.btn_weapon.choose.setVisible(False)
            self.selected_right_idx = idx
            if idx != -1:
                ui_item = self.panel.list_weapon_1.GetItem(idx)
                ui_item.btn_weapon.choose.setVisible(True)

    def init_left_weapon_list(self):
        self.panel.lab_title_1.SetString(get_text_by_id(861006))
        self.panel.list_weapon_2.DeleteAllSubItem()
        self.panel.list_weapon_2.SetInitCount(len(self.weapons_data[self.cur_index]))
        all_items = self.panel.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            wp_dict = self.weapons_data[self.cur_index][str(idx)]
            wp_id_default = wp_dict['list_id'][0]
            ui_item.name.SetString(item_utils.get_item_name(wp_id_default))
            ui_item.details.SetString(item_utils.get_item_desc(wp_id_default))
            ui_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(wp_id_default))

        self.panel.list_weapon_2.setVisible(False)
        self.panel.nd_empty.lab_empty.SetString(get_text_by_id(861008))
        self.panel.nd_empty.setVisible(True)

    def update_left_weapon_list(self, index):
        self.panel.list_weapon_2.setVisible(True)
        self.panel.nd_empty.setVisible(False)
        slot = index + 1
        cur_wp_id = self.wp_conf_dict.get(slot, -1)
        all_items = self.panel.list_weapon_2.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            item_wp_dict = self.weapons_data[self.cur_index][str(idx)]
            item_wp_list_id = item_wp_dict.get('list_id', [])
            if cur_wp_id in item_wp_list_id:
                self.switch_left_list_item(idx)
                self.right_2_left_idx_dict[index] = idx
            item_wp_id = item_wp_list_id[-1]

            @ui_item.btn_item.callback()
            def OnClick(_btn, _touch, _idx=idx, _wp_id=item_wp_id, _slot=slot):
                self.on_click_left_item(_idx, _wp_id, _slot)

    def on_click_left_item(self, idx, wp_id, slot):
        self.switch_left_list_item(idx)
        slot_ui = self.panel.list_weapon_1.GetItem(slot - 1)
        if not slot_ui:
            return
        wp_lv = get_item_quality(wp_id)
        slot_ui.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(wp_id))
        slot_ui.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(wp_lv))
        slot_ui.lab_weapon_name.SetString(item_utils.get_item_name(wp_id))
        self.wp_conf_dict[slot] = wp_id
        self.right_2_left_idx_dict[slot - 1] = idx
        self.update_lv_list(slot - 1)

    def switch_left_list_item(self, idx):
        if idx != self.selected_left_idx:
            if self.selected_left_idx != -1:
                ui_item = self.panel.list_weapon_2.GetItem(self.selected_left_idx)
                ui_item.choose.setVisible(False)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(0))
            self.selected_left_idx = idx
            if idx != -1:
                ui_item = self.panel.list_weapon_2.GetItem(idx)
                ui_item.choose.setVisible(True)
                ui_item.item_bar.SetDisplayFrameByPath('', self.ITEM_BG.get(1))

    def init_lv_list(self):
        self.panel.nd_level.setVisible(False)

    def update_lv_list(self, idx):
        slot = idx + 1
        wp_id = self.wp_conf_dict.get(slot, -1)
        if wp_id == -1 or self.right_2_left_idx_dict.get(idx, -1) == -1:
            self.panel.nd_level.setVisible(False)
        else:
            self.panel.nd_level.setVisible(True)
            wp_lv = get_item_quality(wp_id)
            left_idx = self.right_2_left_idx_dict[idx]
            item_wp_list_id = self.weapons_data[self.cur_index][str(left_idx)].get('list_id', [])
            if wp_id in item_wp_list_id:
                self.panel.list_level.DeleteAllSubItem()
                self.panel.list_level.SetInitCount(len(item_wp_list_id))
                self.record_lv_items_pos()
                all_items = self.panel.list_level.GetAllItem()
                select_lv_idx = -1
                for idx, ui_item in enumerate(all_items):
                    item_wp_id = item_wp_list_id[idx]
                    lv = get_item_quality(item_wp_id)
                    ui_item.icon_level.SetDisplayFrameByPath('', self.LV_ICON.get(lv, self.LV_ICON[1]))
                    if lv == wp_lv:
                        self.resize_lv_ui_item(ui_item, True)
                        select_lv_idx = idx
                    else:
                        self.resize_lv_ui_item(ui_item, False)

                    @ui_item.btn_level.callback()
                    def OnClick(_btn, _touch, _idx=idx, _wp_id=item_wp_id, _slot=slot):
                        self.on_click_lv_item(_idx, _wp_id, _slot)

                self.repos_lv_items(select_lv_idx)

    def on_click_lv_item(self, _idx, wp_id, slot):
        self.switch_lv_list_item(_idx)
        slot_ui = self.panel.list_weapon_1.GetItem(slot - 1)
        wp_lv = get_item_quality(wp_id)
        slot_ui.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(wp_id))
        slot_ui.img_weapon_level.SetDisplayFrameByPath('', self.SLOT_BG.get(wp_lv))
        self.wp_conf_dict[slot] = wp_id

    def switch_lv_list_item(self, cur_lv):
        all_items = self.panel.list_level.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            if idx == cur_lv:
                self.resize_lv_ui_item(ui_item, True)
            else:
                self.resize_lv_ui_item(ui_item, False)

        self.repos_lv_items(cur_lv)

    def record_lv_items_pos(self):
        self.lv_items_pos = []
        all_items = self.panel.list_level.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            self.lv_items_pos.append(ui_item.btn_level.GetPosition())

    def resize_lv_ui_item(self, ui_item, is_select):
        if is_select:
            ui_item.btn_level.SetSelect(True)
            size = ui_item.btn_level.GetContentSize()
            ui_item.btn_level.SetContentSize(150, size[1])
            ui_item.btn_level.ChildResizeAndPosition()
        else:
            ui_item.btn_level.SetSelect(False)
            size = ui_item.btn_level.GetContentSize()
            ui_item.btn_level.SetContentSize(74, size[1])
            ui_item.btn_level.ChildResizeAndPosition()

    def repos_lv_items(self, index):
        all_items = self.panel.list_level.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            pos = self.lv_items_pos[idx]
            if idx < index:
                ui_item.btn_level.SetPosition(pos[0] - 74, pos[1])
            else:
                ui_item.btn_level.SetPosition(pos[0], pos[1])
            ui_item.btn_level.ChildResizeAndPosition()

    def upload_wp_conf(self, *args, **kwargs):
        if self.wp_conf_dict == self.ori_wp_conf_dict:
            return
        if not global_data.player:
            return
        if not global_data.player.get_battle():
            return
        global_data.player.get_battle().call_soul_method('set_combat_weapons', (self.wp_conf_dict,))