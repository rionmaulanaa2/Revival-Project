# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/ChooseWeaponWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gcommon import const
from logic.comsys.effect import ui_effect
from logic.gutils.template_utils import get_item_quality
from common.cfg import confmgr
QUALITY_PIC = {item_const.NORMAL_GREEN: 'gui/ui_res_2/battle/panel/pnl_weapon_green.png',item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle/panel/pnl_weapon_blue.png',
   item_const.EPIC_PURPLE: 'gui/ui_res_2/battle/panel/pnl_weapon_purple.png',
   item_const.LEGEND_GILD: 'gui/ui_res_2/battle/panel/pnl_weapon_orange.png'
   }
CANDIDATE_WEAPON_BAR_PIC = {0: 'gui/ui_res_2/battle_train/pnl_weapon.png',
   1: 'gui/ui_res_2/battle_train/pnl_weapon1.png'
   }

class ChooseWeaponWidget(object):
    WEAPON_POS = [
     1, 2, 3]

    def __init__(self, panel):
        self.panel = panel
        self.lview = panel.list_weapon
        self.init_parameters()
        self.init_event(True)
        self.lview.DeleteAllSubItem()
        self.init_item_list()

    def init_parameters(self):
        self.weapon_data = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        self.select_index = {}
        self.select_weapon_data = global_data.death_battle_data.get_select_weapon_data()
        if not self.select_weapon_data or len(self.select_weapon_data) == 1 and const.PART_WEAPON_POS_MAIN_DF in self.select_weapon_data:
            if len(self.weapon_data) >= len(ChooseWeaponWidget.WEAPON_POS):
                self.select_weapon_data = {}
                for i, weapon_pos in enumerate(ChooseWeaponWidget.WEAPON_POS):
                    self.select_weapon_data[weapon_pos] = self.weapon_data[i]

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.weapon_data = []
        self.select_index = {}
        self.select_weapon_data = {}
        self.init_event(False)

    def init_item_list(self):
        item_count = len(self.weapon_data)
        self.lview.SetInitCount(item_count)
        all_items = self.lview.GetAllItem()
        for index, item_widget in enumerate(all_items):
            item_id = int(self.weapon_data[index])
            item_widget.lab_name.SetString(item_utils.get_item_name(item_id))
            item_widget.lab_details.SetString(item_utils.get_item_desc(item_id))
            item_widget.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(item_id))
            icon, txt_id = item_utils.get_gun_quick_icon(item_id)
            for weapon_pos, weapon_id in six.iteritems(self.select_weapon_data):
                if item_id == weapon_id:
                    self.select_index[weapon_pos] = index
                    item_widget.choose.setVisible(True)
                    item_widget.lab_num.SetString(str(weapon_pos))
                    break

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, index=index, item_id=item_id):
                self.select_weapon(index, item_id)

        self.update_choose_weapon_tips()

    def update_choose_weapon_tips(self):
        total_weapon_count = len(ChooseWeaponWidget.WEAPON_POS)
        self.panel.lab_tips.SetString(get_text_by_id(601013).format(total_weapon_count, len(self.select_index), total_weapon_count))

    def select_weapon(self, index, item_data):
        cancle_weapon_pos = None
        for weapon_pos, sel_index in six.iteritems(self.select_index):
            if index == sel_index:
                cancle_weapon_pos = weapon_pos
                item_widget = self.lview.GetItem(index)
                item_widget and item_widget.choose.setVisible(False)

        if cancle_weapon_pos:
            del self.select_index[cancle_weapon_pos]
            self.update_choose_weapon_tips()
            return
        else:
            weapon_pos = self.get_free_weapon_pos()
            if not weapon_pos:
                global_data.game_mgr.show_tip(get_text_by_id(17004))
                return
            self.select_index[weapon_pos] = index
            item_widget = self.lview.GetItem(index)
            item_widget and item_widget.choose.setVisible(True)
            item_widget and item_widget.lab_num.SetString(str(weapon_pos))
            self.update_choose_weapon_tips()
            if len(self.select_index) == len(ChooseWeaponWidget.WEAPON_POS):
                ui = global_data.ui_mgr.get_ui('DeathWeaponChooseUI')
                if ui:
                    ui.close()
            return

    def get_free_weapon_pos(self):
        for pos in self.WEAPON_POS:
            if pos not in self.select_index:
                return pos

    def get_selcet_weapon(self):
        weapon_data = {}
        for pos, index in six.iteritems(self.select_index):
            weapon_data[pos] = self.weapon_data[index]

        return weapon_data


class ChooseWeaponWidgetNew(object):

    def __init__(self, panel):
        self.panel = panel
        self.weapon_id_2_ui_item = {}
        self.highlight_candidate_weapon_id = -1
        self.highlight_selected_weapon_item = None
        self.selected_weapon_dict = self.get_selected_weapon_dict()
        self.cur_weapon_pos = None
        self.cur_index = 0
        self.init_weapon_conf()
        self.init_tab()
        self.init_candidate_weapon_list()
        self.init_selected_weapon_list()
        self.panel.lab_tips.setVisible(False)
        self.panel.list_weapon_2.GetItem(0).lab_tips.setVisible(False)
        self.process_event(True)
        return

    def destroy(self):
        self.process_event(False)
        self.weapon_id_2_ui_item = None
        self.highlight_selected_weapon_item = None
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
        if not player or not player.logic:
            return
        weapon_id_dict = self.get_equiped_weapon_dict(player)
        if six_ex.compare(self.selected_weapon_dict, weapon_id_dict) == 0:
            return
        self.selected_weapon_dict = weapon_id_dict
        self.init_selected_weapon_list()

    def get_equiped_weapon_dict(self, player=None):
        if player is None:
            player = global_data.player
        if not player or not player.logic:
            return
        else:
            weapon_object_dict = player.logic.share_data.ref_wp_bar_mp_weapons
            weapon_id_dict = {}
            for weapon_pos, weapon_obj in six.iteritems(weapon_object_dict):
                if weapon_pos == const.PART_WEAPON_POS_MAIN_DF:
                    continue
                if not weapon_obj:
                    continue
                weapon_data = weapon_obj.get_data()
                weapon_id_dict[weapon_pos] = weapon_data.get('item_id')

            return weapon_id_dict

    def get_selected_weapon_dict(self):
        equ_weapon_data = self.get_equiped_weapon_dict()
        if equ_weapon_data is not None and len(equ_weapon_data) == len(const.EXTRA_WEAPON_LIST):
            return equ_weapon_data
        else:
            can_weapon_data = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
            sel_weapon_data = global_data.death_battle_data.get_select_weapon_data()
            if not sel_weapon_data or len(sel_weapon_data) == 1 and const.PART_WEAPON_POS_MAIN_DF in sel_weapon_data or len(sel_weapon_data) < len(const.EXTRA_WEAPON_LIST):
                if len(can_weapon_data) >= len(const.EXTRA_WEAPON_LIST):
                    ret_select_weapon_data = {}
                    for i, weapon_pos in enumerate(const.EXTRA_WEAPON_LIST):
                        ret_select_weapon_data[weapon_pos] = can_weapon_data[i]

                    return ret_select_weapon_data
            return sel_weapon_data

    def get_last_choose_down_show_weapon(self):
        last_choose_down_weapon = global_data.death_battle_data.get_last_choose_down_weapon()
        other_wp_id_list = six_ex.values(self.selected_weapon_dict)
        candidate_weapon_list = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        show_weapon = []
        for weapon_id in last_choose_down_weapon:
            if other_wp_id_list and weapon_id in other_wp_id_list:
                continue
            if weapon_id not in candidate_weapon_list:
                continue
            show_weapon.append(weapon_id)

        now_cnt = len(show_weapon)
        show_cnt = 6
        if now_cnt >= show_cnt:
            return show_weapon[:show_cnt]
        for weapon_id in candidate_weapon_list:
            weapon_id = int(weapon_id)
            if weapon_id not in show_weapon and weapon_id not in other_wp_id_list:
                show_weapon.append(weapon_id)
                now_cnt += 1
                if now_cnt >= show_cnt:
                    return show_weapon[:show_cnt]

        return show_weapon[:show_cnt]

    def init_weapon_conf(self):
        self.weapon_conf = []
        all_weapon = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        battle_wp_conf = confmgr.get('items_book_conf', 'WeaponConfig', 'Content', default={})
        wp_tab_conf = confmgr.get('items_book_conf', 'WeaponTabConfig', 'Content', default={})
        for _, v in six.iteritems(wp_tab_conf):
            wp_tab_list = v.get('second_tabs', [])
            tab_name_id = v.get('tab_name_id', '')
            valid_wp = []
            if not wp_tab_list or not tab_name_id:
                continue
            for wb_tab in wp_tab_list:
                battle_wp_list = battle_wp_conf.get(str(wb_tab), {}).get('battle_item_no', [])
                for wp in battle_wp_list:
                    if wp in all_weapon:
                        valid_wp.append(wp)

            self.weapon_conf.append([tab_name_id, valid_wp])

    def init_tab(self):
        len_tab = len(self.weapon_conf) + 2
        self.panel.temp_bg.list_tab.SetInitCount(len_tab)
        for i in range(2, len_tab):
            item = self.panel.temp_bg.list_tab.GetItem(i)
            item.btn_window_tab.SetText(get_text_by_id(self.weapon_conf[i - 2][0]))

            @item.btn_window_tab.unique_callback()
            def OnClick(_btn, _touch, _idx=i, *args):
                if global_data.player and global_data.player.logic:
                    self.on_switch_to_widget(_idx)

        item_all = self.panel.temp_bg.list_tab.GetItem(0)
        item_all.btn_window_tab.SetText(get_text_by_id(634134))

        @item_all.btn_window_tab.unique_callback()
        def OnClick(_btn, _touch, _idx=0, *args):
            if global_data.player and global_data.player.logic:
                self.on_switch_to_widget(_idx)

        item_last_choose = self.panel.temp_bg.list_tab.GetItem(1)
        item_last_choose.btn_window_tab.SetText(get_text_by_id(18293))

        @item_last_choose.btn_window_tab.unique_callback()
        def OnClick(_btn, _touch, _idx=1, *args):
            if global_data.player and global_data.player.logic:
                self.on_switch_to_widget(_idx)

    def init_candidate_weapon_list(self):
        last_choose_down_show_weapon = self.get_last_choose_down_show_weapon()
        candidate_weapon_list = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        weapon_list_view = self.panel.list_weapon_2
        weapon_list_view.SetInitCount(1)
        all_weapon_items = weapon_list_view.GetAllItem()[0]
        all_weapon_cnt = len(candidate_weapon_list)
        all_weapon_items.list_weapon_1.SetInitCount(0)
        all_weapon_items.list_weapon_2.SetInitCount(all_weapon_cnt)
        all_weapon_items2 = all_weapon_items.list_weapon_2.GetAllItem()
        all_weapon_items.img_choose.setVisible(False)
        for index, weapon_item in enumerate(all_weapon_items2):
            weapon_id = int(candidate_weapon_list[index])
            weapon_item.name.SetString(item_utils.get_item_name(weapon_id))
            weapon_item.details.SetString(item_utils.get_item_desc(weapon_id))
            weapon_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(weapon_id))
            self.weapon_id_2_ui_item[weapon_id] = weapon_item

            @weapon_item.btn_item.unique_callback()
            def OnClick(btn, touch, cur_weapon_item=weapon_item, cur_weapon_id=weapon_id):
                self.on_click_candidate_weapon_item(cur_weapon_item, cur_weapon_id)

        list_weapon_2_h = 600
        w, h = all_weapon_items.GetContentSize()
        _, h2 = all_weapon_items.list_weapon_2.GetContentSize()
        all_weapon_items.SetContentSize(w, h + (h2 - list_weapon_2_h))
        all_weapon_items.ChildRecursionRePosition()
        weapon_list_view.RefreshItemPos()

    def init_selected_weapon_list(self):
        weapon_list_view = self.panel.list_weapon_1
        weapon_list_view.SetInitCount(len(const.EXTRA_WEAPON_LIST))
        all_weapon_items = weapon_list_view.GetAllItem()
        for index, weapon_item in enumerate(all_weapon_items):
            weapon_pos = const.EXTRA_WEAPON_LIST[index]
            weapon_id = self.selected_weapon_dict.get(weapon_pos)
            weapon_item.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(weapon_id))
            weapon_item.lab_weapon_name.SetString(item_utils.get_item_name(weapon_id))
            weapon_item.img_weapon_level.SetDisplayFrameByPath('', QUALITY_PIC.get(get_item_quality(weapon_id), 'gui/ui_res_2/battle_train/img_dark.png'))

            @weapon_item.btn_weapon.unique_callback()
            def OnClick(btn, touch, cur_weapon_item=weapon_item, cur_weapon_pos=weapon_pos):
                self.on_click_selected_weapon_item(cur_weapon_item, cur_weapon_pos)

        self.on_click_selected_weapon_item(all_weapon_items[0], const.PART_WEAPON_POS_MAIN1)
        self.on_switch_to_widget(0)

    def on_switch_to_widget(self, index):
        self.weapon_id_2_ui_item = {}
        self.panel.temp_bg.list_tab.GetItem(self.cur_index).btn_window_tab.SetSelect(False)
        self.cur_index = index
        self.panel.temp_bg.list_tab.GetItem(index).btn_window_tab.SetSelect(True)
        weapon_list_view = self.panel.list_weapon_2
        weapon_list_view.ScrollToTop()
        weapon_items = weapon_list_view.GetAllItem()[0]
        candidate_weapons_list = []
        all_weapon = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        if 1 < index <= len(self.weapon_conf) + 1:
            candidate_weapons_list = self.weapon_conf[index - 2][1]
        elif index == 0:
            candidate_weapons_list = all_weapon
        else:
            candidate_weapons_list = self.get_last_choose_down_show_weapon()
        candidate_weapons_cnt = len(candidate_weapons_list)
        weapon_items.list_weapon_2.SetInitCount(candidate_weapons_cnt)
        all_weapon_items2 = weapon_items.list_weapon_2.GetAllItem()
        for index, weapon_item in enumerate(all_weapon_items2):
            weapon_id = int(candidate_weapons_list[index])
            weapon_item.name.SetString(item_utils.get_item_name(weapon_id))
            weapon_item.details.SetString(item_utils.get_item_desc(weapon_id))
            weapon_item.sp_item.SetDisplayFrameByPath('', item_utils.get_gun_small_pic_by_item_id(weapon_id))
            if weapon_id == self.selected_weapon_dict.get(self.cur_weapon_pos):
                weapon_item.choose.setVisible(True)
                weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(1))
            else:
                weapon_item.choose.setVisible(False)
                weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(0))
            self.weapon_id_2_ui_item[weapon_id] = weapon_item

            @weapon_item.btn_item.unique_callback()
            def OnClick(btn, touch, cur_weapon_item=weapon_item, cur_weapon_id=weapon_id):
                self.on_click_candidate_weapon_item(cur_weapon_item, cur_weapon_id)

    def on_click_candidate_weapon_item(self, weapon_item, weapon_id):
        other_wp_id_list = six_ex.values(self.selected_weapon_dict)
        if weapon_id in other_wp_id_list:
            return
        else:
            highlight_candidate_weapon_item = self.weapon_id_2_ui_item.get(self.highlight_candidate_weapon_id, None)
            if highlight_candidate_weapon_item:
                highlight_candidate_weapon_item.choose.setVisible(False)
                highlight_candidate_weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(0))
            weapon_item.choose.setVisible(True)
            weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(1))
            self.highlight_candidate_weapon_id = weapon_id
            if self.highlight_selected_weapon_item:
                self.highlight_selected_weapon_item.sp_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(weapon_id))
                self.highlight_selected_weapon_item.lab_weapon_name.SetString(item_utils.get_item_name(weapon_id))
                self.highlight_selected_weapon_item.img_weapon_level.SetDisplayFrameByPath('', QUALITY_PIC.get(get_item_quality(weapon_id), 'gui/ui_res_2/battle_train/img_dark.png'))
            self.selected_weapon_dict[self.cur_weapon_pos] = weapon_id
            return

    def on_click_selected_weapon_item(self, weapon_item, weapon_pos):
        self.cur_weapon_pos = weapon_pos
        weapon_id = self.selected_weapon_dict.get(self.cur_weapon_pos)
        if self.highlight_selected_weapon_item:
            self.highlight_selected_weapon_item.choose.setVisible(False)
        self.highlight_selected_weapon_item = weapon_item
        weapon_item.choose.setVisible(True)
        self.highlight_selected_weapon_item.choose.setVisible(True)
        candidate_weapon_item = self.weapon_id_2_ui_item.get(weapon_id, None)
        highlight_candidate_weapon_item = self.weapon_id_2_ui_item.get(self.highlight_candidate_weapon_id, None)
        if highlight_candidate_weapon_item:
            highlight_candidate_weapon_item.choose.setVisible(False)
            highlight_candidate_weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(0))
        self.highlight_candidate_weapon_id = weapon_id
        if candidate_weapon_item:
            candidate_weapon_item.choose.setVisible(True)
            candidate_weapon_item.item_bar.SetDisplayFrameByPath('', CANDIDATE_WEAPON_BAR_PIC.get(1))
        for wp_item in six_ex.values(self.weapon_id_2_ui_item):
            if wp_item:
                ui_effect.set_gray(wp_item.sp_item, False)

        for other_wp_pos, other_wp_id in six.iteritems(self.selected_weapon_dict):
            if other_wp_pos == const.PART_WEAPON_POS_MAIN_DF:
                continue
            if other_wp_id == weapon_id:
                continue
            other_wp_item = self.weapon_id_2_ui_item.get(other_wp_id)
            if not other_wp_item:
                continue
            ui_effect.set_gray(other_wp_item.sp_item, True)

        return

    def get_selcet_weapon(self):
        return self.selected_weapon_dict