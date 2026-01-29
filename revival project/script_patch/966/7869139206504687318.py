# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonPassAwardWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.battle_pass_utils import check_trial_version_sp, get_receive_num, get_buy_season_card_ui_name
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battlepass_const import ROTATE_FACTOR
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L2, SEASON_CARD_TYPE, SEASON_CARD
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_YTPE_VEHICLE_SKIN, L_ITME_TYPE_GUNSKIN
from .SeasonBaseUIWidget import SeasonBaseUIWidget
from .BattlePassDisplayWidget import BattlePassDisplayWidget
from .BattlePassRewardListWidget import BattlePassRewardListWidget
ND_EMPTY = 0
ND_COMMON_REWARD = 2
ND_SPECIAL_REWARD = 3
NEED_SHOW_BELONG_ITEM_NAME_TYPES = {
 L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_YTPE_VEHICLE_SKIN, L_ITME_TYPE_GUNSKIN}

class SeasonPassAwardWidget(SeasonBaseUIWidget):

    def show_init_state(self, need_anim=False):
        if need_anim:
            self.panel.PlayAnimation('show')
            self.panel.temp_content_normal.PlayAnimation('show')
            self.panel.temp_content_normal.PlayAnimation('loop')
        self._update_card_buy_info(need_anim)
        self._award_list_widget.set_current_idx(self._sp_lv - 1)
        self._display_node(ND_EMPTY)
        self._award_list_widget.set_select_btn(None, is_preview=True)
        self._award_list_widget.set_select_btn(None, is_preview=False)
        self._award_list_widget.clear_select_info()
        self._displaying_item_no = None
        display_display = self._sp_data.DEFAULT_DISPLAY
        if display_display:
            display_lv, display_idx = display_display
        else:
            display_lv, display_idx = (1, 1)
        list_item_data = item_utils.get_battle_pass_i_level_award_data(display_lv, SEASON_CARD)
        for idx in (display_idx, 1, 2, 0):
            data = list_item_data[idx]
            if data:
                item_no, _, lv, sp_type, idx = data
                self._display_award_detail(item_no)
                self._show_item_no(item_no, lv)
                self._award_list_widget.select_sub_button(lv - 1, sp_type, idx)
                break

        return

    def season_pass_lv_up(self, bp_lv, bp_point):
        self._sp_lv = bp_lv
        self._sp_point = bp_point
        self._update_exist_item()
        self._award_list_widget.set_current_idx(self._sp_lv - 1)

    def show_jump_state(self, lv, pass_type, idx, reward_id):
        self._display_award_detail(reward_id)
        self._show_item_no(reward_id, lv)
        self._award_list_widget.idx_to_left(lv - 1)
        self._award_list_widget.select_sub_button(lv - 1, pass_type, idx)

    def re_display(self):
        if not self._displaying_item_no:
            global_data.emgr.change_model_display_scene_item.emit(None)
            self._display_node(ND_EMPTY)
            return
        else:
            self._display_award_detail(self._displaying_item_no, True)
            return

    def __init__(self, parent_ui, panel):
        self.global_events = {'season_pass_open_type': self._season_pass_buy_card,
           'season_pass_update_award': self._update_exist_item,
           'update_month_card_info': self._update_daily_reward_info,
           'season_pass_update_daily_award': self._update_daily_reward_info,
           'player_money_info_update_event': self._update_exchange_red_info,
           'update_battle_exchange_rp_event': self._update_exchange_red_info,
           'receive_reward_info_from_server_event': self._update_reward_list,
           'season_pass_buy_active_gift': self._update_exist_item
           }
        super(SeasonPassAwardWidget, self).__init__(parent_ui, panel)
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        self._sp_data = get_now_season_pass_data()
        self._display_widget = None
        self._showing_reward_id = None
        self._lv_num_color_sel = 15592941
        self._init_panel()
        self._init_widget()
        self._update_can_received_num()
        self._init_ui_event()
        self._init_right_display()
        self._init_reward_lst_widget()
        return

    def _init_panel(self):
        self._last_lv = None
        self._sp_lv, self._sp_point = global_data.player.get_battlepass_info()
        self._update_card_buy_info()
        self._update_daily_reward_info()
        self._update_exchange_red_info()
        return

    def _init_widget(self):
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)

    def _init_reward_lst_widget(self):
        lv_cap = self._sp_data.SEASON_PASS_LV_CAP
        sp_coin_begin_lv = self._sp_data.FIRST_LIST_CAP
        self._award_list_widget = BattlePassRewardListWidget(self, self.panel.temp_content_normal, lv_cap, first_list_cap=sp_coin_begin_lv, i_level_award_init_func=self._init_i_level_award)
        self._award_list_widget.init_reward_list()
        self._award_list_widget.set_current_idx(self._sp_lv - 1)
        self._award_list_widget.set_lock(not global_data.player.has_buy_one_kind_season_card())

    def _update_card_buy_info(self, need_anim=False):
        has_buy_final_card = global_data.player.has_buy_final_card()
        self.panel.nd_control.btn_buy_card.setVisible(not has_buy_final_card)
        if need_anim and not has_buy_final_card:
            self.panel.PlayAnimation('appear_up')
            self.panel.StopAnimation('loop')
            self.panel.PlayAnimation('loop2')

    def _update_lv_show(self):
        self.panel.nd_level.lab_level.SetString('LV.' + str(self._sp_lv))
        if self._sp_lv >= self._sp_data.SEASON_PASS_LV_CAP:
            self.panel.nd_exp_num.setVisible(False)
            self.panel.nd_exp.setVisible(False)
            self.panel.nd_basic.temp_buy_level.setVisible(False)
        else:
            sp_lv_data = self._sp_data.season_pass_lv_data
            next_lv_point = sp_lv_data[self._sp_lv][0]
            now_lv_point = 0 if self._sp_lv <= 1 else sp_lv_data[self._sp_lv - 1][0]
            need_point = next_lv_point - now_lv_point
            self.panel.nd_exp_num.lab_num_exp_need.SetString('/' + str(need_point))
            self.panel.nd_exp_num.lab_num_exp.SetString(str(self._sp_point - now_lv_point))
            progress_value = float(self._sp_point - now_lv_point) / float(need_point) * 100
            self.panel.nd_pass.nd_basic.nd_exp.progress_cut.progress_exp.SetPercent(progress_value)

    def is_locked(self, lv, sp_type):
        if not global_data.player:
            return True
        is_lock_lv = True if lv > self._sp_lv + global_data.player.get_unfinished_lv() else False
        if sp_type == SEASON_PASS_L1:
            has_owned = True
        else:
            has_owned = global_data.player or False if 1 else global_data.player.has_buy_one_kind_season_card()
            has_owned = has_owned and check_trial_version_sp(lv, self._sp_data)
        return is_lock_lv or not is_lock_lv and not has_owned

    def is_received(self, lv, sp_type):
        reward_record = global_data.player.get_battlepass_reward_record().get(str(sp_type), None)
        if reward_record is None:
            return False
        else:
            return reward_record.is_record(lv)

    def _init_right_display(self):
        self._displaying_item_no = None
        self._right_node_num = ND_EMPTY
        self._display_map = {ND_EMPTY: {'node': self.panel.nd_empty,'up_func': None},ND_COMMON_REWARD: {'node': self.panel.nd_common_reward,'up_func': None},ND_SPECIAL_REWARD: {'node': self.panel.nd_special_reward,'up_func': None}}
        display_num = ND_EMPTY
        self._display_node(display_num)

        def on_model_drag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.panel.nd_special_reward.BindMethod('OnDrag', on_model_drag)
        return

    def _display_node(self, node_num):
        for key in six_ex.keys(self._display_map):
            if key == node_num:
                self._display_map[key]['node'].setVisible(True)
                node_func = self._display_map[key]['up_func']
                if node_func:
                    node_func()
            else:
                self._display_map[key]['node'].setVisible(False)

        self._right_node_num = node_num

    def _update_can_received_num(self):
        can_receive_num = get_receive_num(self._sp_lv, self._sp_data, False)
        img_num_visible = False if can_receive_num == 0 else True
        self.parent.panel.btn_reward.img_red.setVisible(img_num_visible)
        self.panel.btn_get_all.img_num.setVisible(img_num_visible)
        self.panel.btn_get_all.img_num.lab_num.SetString(str(can_receive_num))
        has_daily_reward = global_data.player and not global_data.player.has_get_season_pass_daily_award()
        if has_daily_reward or img_num_visible:
            self.panel.PlayAnimation('loop')
        else:
            self.panel.StopAnimation('loop')
        self._update_lobby_red_point()

    def _receive_award(self, sp_type, lv):
        if global_data.player:
            global_data.player.receive_battlepass_reward(str(sp_type), str(lv))

    def _update_exist_item(self, *args):
        idx_to_item = self._award_list_widget.get_exist_item_dict()
        last_preview_idx = self._award_list_widget.get_last_preview_idx()
        for idx in idx_to_item:
            if idx == -1:
                lv = last_preview_idx + 1
                self._set_item_state(lv, True)
            else:
                self._set_item_state(idx + 1)

        self._update_can_received_num()

    def _season_pass_buy_card(self, sp_type):
        self._award_list_widget.set_lock(False)
        self._update_exist_item()
        self._update_card_buy_info()

    def _init_i_level_award(self, item, idx, preview=False):
        real_lv = idx + 1
        list_item = [item.temp_reward_1, item.temp_reward_2_1, item.temp_reward_2_2]
        list_item_data = item_utils.get_battle_pass_i_level_award_data(real_lv, SEASON_CARD)
        for idx, sub_item in enumerate(list_item):
            item_data = list_item_data[idx]
            if not item_data:
                sub_item.setVisible(False)
                continue
            else:
                sub_item.setVisible(True)
                template_item = getattr(sub_item, 'mall_item', None)
                if not template_item:
                    template_item = global_data.uisystem.load_template_create('mall/i_item', sub_item, name='mall_item')

                def OnClickCallback(data=item_data):
                    no_item, _, lv, type_sp, reward_sub_num = data
                    is_lock_lv = self.is_locked(lv, type_sp)
                    is_received = self.is_received(lv, type_sp)
                    self._display_award_detail(no_item)
                    self._show_item_no(no_item, lv)
                    if not (is_received or is_lock_lv):
                        self._receive_award(type_sp, lv)
                    self._award_list_widget.select_sub_button(lv - 1, type_sp, reward_sub_num)

                item_no, item_num, sp_lv, sp_type, sub_reward_idx = item_data
                is_core = self._sp_data.is_core_reward_item(sp_lv, sp_type, sub_reward_idx)
                init_tempate_mall_i_item(template_item, item_no, item_num=item_num, callback=OnClickCallback, force_extra_ani=is_core and not preview)

        self._set_item_state(real_lv, preview, data=list_item_data)
        return

    def _show_item_no(self, item_no, lv):
        self.panel.lab_unlock.setVisible(True)
        self.panel.lab_unlock_2.setVisible(True)
        self.panel.lab_unlock.SetString(get_text_by_id(12022).format(lv))
        self.panel.lab_unlock_2.SetString(get_text_by_id(12022).format(lv))
        self._set_reward_list(item_no)

    def _set_reward_list(self, item_no):
        reward_id = confmgr.get('lobby_item', str(item_no), 'use_params', 'reward_id')
        if reward_id:
            item_id_lst = global_data.player.get_reward_display_data(int(reward_id))
            if item_id_lst:
                self._refresh_list_item(item_id_lst)
            self._showing_reward_id = reward_id
        else:
            self.panel.nd_gif_reward.setVisible(False)
            self._showing_reward_id = None
            self.parent.switch_advance_btn_and_btn_guide_show(True)
        return

    def _set_item_state(self, lv, preview=False, data=None):
        record_idx = -1 if preview else lv - 1
        item = self._award_list_widget.get_exist_item_by_idx(record_idx)
        if item is None:
            return
        else:
            reward_records = global_data.player or {} if 1 else global_data.player.get_battlepass_reward_record()
            for sp_type in SEASON_CARD_TYPE:
                reward_record = reward_records.get(str(sp_type), None)
                if reward_record is None:
                    is_received = False if 1 else reward_record.is_record(lv)
                    is_lock_lv = self.is_locked(lv, sp_type)
                    mall_items = ()
                    if sp_type == SEASON_PASS_L1:
                        mall_items = (
                         item.temp_reward_1.mall_item,)
                    elif sp_type == SEASON_PASS_L2:
                        mall_items = (
                         item.temp_reward_2_1.mall_item, item.temp_reward_2_2.mall_item)
                    for mall_item in mall_items:
                        if mall_item:
                            mall_item.nd_lock.setVisible(is_lock_lv)
                            mall_item.nd_get.setVisible(is_received)
                            mall_item.nd_get_tips.setVisible(not is_received and not is_lock_lv)

            if lv == self._sp_lv and not preview:
                item.img_frame_now.setVisible(True)
                item.img_level_now.setVisible(True)
                item.nd_level.lab_level.SetColor(self._lv_num_color_sel)
                if self._last_lv is not None and self._last_lv != self._sp_lv:
                    item = self._award_list_widget.get_exist_item_by_idx(self._last_lv - 1)
                    if item:
                        item.img_frame_now.setVisible(False)
                        item.img_level_now.setVisible(False)
                        item.nd_level.lab_level.SetColor(12106182)
                self._last_lv = self._sp_lv
            return

    def _display_award_detail(self, item_no, reset_display_type=False):
        self._displaying_item_no = item_no
        self._display_widget.display_award(item_no, reset_display_type)
        self._set_reward_list(item_no)

    def _display_cb(self, is_model, item_no):
        super(SeasonPassAwardWidget, self)._display_cb(is_model, item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        if is_model:
            self._display_node(ND_SPECIAL_REWARD)
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type in NEED_SHOW_BELONG_ITEM_NAME_TYPES:
                belong_id = item_utils.get_lobby_item_belong_no(item_no)
                belong_item_name = item_utils.get_lobby_item_name(belong_id)
                item_name = belong_item_name + ' ' + item_name
            self.panel.nd_special_reward.lab_name.SetString(item_name)
            self.panel.nd_special_reward.lab_describe.SetString(item_desc)
            self.panel.nd_special_reward.lab_name.setVisible(True)
        else:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            self._display_node(ND_COMMON_REWARD)
            self.panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self.panel.nd_common_reward.lab_name.SetString(item_name)
            self.panel.nd_common_reward.lab_describe.SetString(item_desc)

    def _update_reward_list(self, *args):
        if self._showing_reward_id and self.is_visible():
            item_id_lst = global_data.player.get_reward_display_data(int(self._showing_reward_id))
            if item_id_lst:
                self._refresh_list_item(item_id_lst)

    def _refresh_list_item(self, item_id_lst):
        self._last_lst_item = None
        self.panel.nd_gif_reward.setVisible(True)
        self.parent.switch_advance_btn_and_btn_guide_show(False)

        def on_create_callback(lv, idx, ui_item, data_lst=item_id_lst):
            item_no = data_lst[idx]

            def OnClickCallback(item_id=item_no, item_node=ui_item):
                if self._last_lst_item != item_node:
                    if self._last_lst_item and self._last_lst_item.isValid():
                        self._last_lst_item and self._last_lst_item.btn_choose.SetSelect(False)
                    self._last_lst_item = item_node
                    item_node.btn_choose.SetSelect(True)
                    self.panel.lab_unlock.setVisible(False)
                    self.panel.lab_unlock_2.setVisible(False)
                    self._display_award_detail(item_id)

            init_tempate_mall_i_item(ui_item, item_no, item_num=1, callback=OnClickCallback)

        nd_preview = self.panel.nd_gif_reward.nd_preview
        nd_preview.list_item.BindMethod('OnCreateItem', on_create_callback)
        nd_preview.list_item.DeleteAllSubItem()
        nd_preview.list_item.SetInitCount(len(item_id_lst))
        return

    def _init_ui_event(self):

        def _on_click_all_reward(*args):
            if global_data.player:
                if not global_data.player.has_get_season_pass_daily_award():
                    global_data.player.try_get_battlepass_daily_reward()
                global_data.player.receive_all_battlepass_reward()

        def _on_click_buy_season_card(*args):
            if global_data.player and not global_data.player.has_buy_final_card():
                global_data.ui_mgr.show_ui(get_buy_season_card_ui_name(), 'logic.comsys.battle_pass')

        def _on_click_daily_reward(*args):
            if not global_data.player:
                return
            if global_data.player.has_yueka():
                global_data.player.try_get_battlepass_daily_reward()
                return
            from logic.gutils.jump_to_ui_utils import jump_to_season_pass_daily_reward
            jump_to_season_pass_daily_reward()

        self.parent.panel.btn_every_day.BindMethod('OnClick', _on_click_daily_reward)
        self.panel.btn_get_all.BindMethod('OnClick', _on_click_all_reward)
        self.panel.nd_control.btn_buy_card.BindMethod('OnClick', _on_click_buy_season_card)
        self.panel.temp_content_normal.btn_advanced.BindMethod('OnClick', _on_click_buy_season_card)

    def _update_daily_reward_info(self, *args):
        has_buy_month_card = global_data.player or False if 1 else global_data.player.has_yueka()
        daily_reward_node = self.parent.panel.btn_every_day
        daily_reward_node.lab_month_card.setVisible(has_buy_month_card)
        if_full_level = self._sp_lv >= self._sp_data.SEASON_PASS_LV_CAP
        if global_data.player and not global_data.player.has_get_season_pass_daily_award() and not if_full_level:
            self.parent.panel.PlayAnimation('daily_reward')
            is_get = False
        else:
            is_get = True
            self.parent.panel.StopAnimation('daily_reward')
            daily_reward_node.SetEnable(False)
            daily_reward_node.SetShowEnable(False)
        daily_reward_node.temp_red.setVisible(not is_get)

    def _update_exchange_red_info(self, *args):
        from logic.gutils import mall_utils
        from logic.gutils.battle_pass_utils import get_exchange_goods_lst, get_season_token, get_now_season
        now_season = get_now_season()
        self.parent.panel.btn_exchange.img_red.setVisible(False)
        if not mall_utils.check_item_money(get_season_token(now_season), 1, pay_tip=False):
            self._update_lobby_red_point()
            return
        need_show_entry_rp = mall_utils.check_can_show_sp_exchange_entry_rp(now_season)
        print('need_show_entry_rp', need_show_entry_rp)
        for goods_id in get_exchange_goods_lst(now_season):
            valid, need_rp = mall_utils.check_sp_exchange_goods(goods_id, now_season)
            if valid and need_rp and need_show_entry_rp:
                self.parent.panel.btn_exchange.img_red.setVisible(True)
                break

        self._update_lobby_red_point()

    def _update_lobby_red_point(self):
        if_full_level = self._sp_lv >= self._sp_data.SEASON_PASS_LV_CAP
        has_daily_reward = global_data.player or True if 1 else not global_data.player.has_get_season_pass_daily_award() and not if_full_level
        has_pass_reward = self.parent.panel.btn_reward.img_red.isVisible()
        has_exchange_red = self.parent.panel.btn_exchange.img_red.isVisible()
        need_show_red = has_pass_reward or has_daily_reward or has_exchange_red
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if ui:
            ui.update_season_red_point(need_show_red)

    def hide(self):
        if self._display_widget:
            self._display_widget.clear_model_display()
        super(SeasonPassAwardWidget, self).hide()

    def destroy(self):
        self._sp_data = None
        self._showing_reward_id = None
        widget_names = [
         '_award_list_widget', '_display_widget']
        for name in widget_names:
            self.destroy_widget(name)

        self._displaying_item_no = None
        super(SeasonPassAwardWidget, self).destroy()
        return