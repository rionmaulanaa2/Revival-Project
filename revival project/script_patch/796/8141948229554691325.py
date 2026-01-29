# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewbieAwardContentUI.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import math
from common.cfg import confmgr
from common.utils.cocos_utils import ccp
from logic.gutils import item_utils
from logic.gutils import lobby_model_display_utils
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.task_const import TASK_TYPE_ASSESS
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_EXPERIENCE_CARD, L_ITEM_MECHA_SFX, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN
from logic.gcommon.common_const.battlepass_const import NEWBIE_PASS_TYPE_1, NEWBIE_PASS_L1, NEWBIE_PASS_L2, BATTLE_CARD_TYPE, REWARD_NUM_DICT, NEWBIE_CARD
from logic.gutils.template_utils import init_tempate_mall_i_item
from data.newbiepass_data import newbiepass_lv_data, NEWBIEPASS_LV_CAP, get_lv_reward
from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_path
ROTATE_FACTOR = 850
ND_EMPTY = 0
ND_BUY_CARD = 1
ND_COMMON_REWARD = 2
ND_SPECIAL_REWARD = 3
PREVIEW_RECORD_LEVEL = 0
MODEL_DISPLAY_TYPE = (
 L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN,
 L_ITEM_TYPE_MECHA_SKIN, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN,
 L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_MECHA_SFX)

class NewbieAwardContentUI(object):

    def show_init_state(self):
        self._update_card_buy_info()
        self._lv_award_to_left(self._bp_lv)
        self._init_final_lv_jump_show()
        display_num = ND_EMPTY if self.has_pass_card else ND_BUY_CARD
        self._display_node(display_num)
        self._set_select_btn(None, is_preview=True)
        self._set_select_btn(None, is_preview=False)
        self._select_info = []
        return

    def show_jump_state(self, lv, pass_type, idx, reward_id):
        self._lv_award_to_left(lv)
        self._display_award_detail(lv, pass_type, reward_id)
        self._select_sub_button(lv, pass_type, idx)

    def __init__(self, main_panel):
        self.panel = main_panel.panel
        self._sub_panel = main_panel.panel.nd_content
        self._bind_event(True)
        self._init_panel_data()
        self._update_lv_show()
        self._init_final_lv_jump_show()
        self._update_can_received_num()
        self._init_ui_event()
        self._init_right_display()
        self._init_reward_list()

    def _init_panel_data(self):
        self._last_lv = None
        self._last_preview_level = 0
        self._last_select_btn = None
        self._last_select_preview_btn = None
        self._select_info = []
        self._bp_lv, self._bp_point = global_data.player.get_newbiepass_info()
        self._lv_to_item = dict.fromkeys(range(NEWBIEPASS_LV_CAP + 1), None)
        if global_data.player:
            self.has_pass_card = global_data.player.has_buy_newbie_card_type(str(NEWBIE_PASS_TYPE_1))
        else:
            self.has_pass_card = False
        self._update_card_buy_info()
        return

    def _update_card_buy_info(self):
        self._sub_panel.nd_control.buy_desc.setVisible(not self.has_pass_card)
        self._sub_panel.nd_control.buy_desc_img.setVisible(not self.has_pass_card)
        self._sub_panel.nd_control.temp_buy_card.setVisible(not self.has_pass_card)

    def _init_final_lv_jump_show(self):
        self._on_final_lv = False
        self._sub_panel.btn_final.SetText(80831)
        self._sub_panel.btn_final.img_right.setVisible(True)
        self._sub_panel.btn_final.img_left.setVisible(False)

    def _update_lv_show(self):
        self._sub_panel.nd_level.lab_level.SetString(str(self._bp_lv))
        if self._bp_lv == NEWBIEPASS_LV_CAP:
            self._sub_panel.nd_exp_num.lab_num_exp_need.setVisible(False)
            self._sub_panel.nd_exp_num.lab_num_exp.setVisible(False)
            self._sub_panel.nd_exp.progress_exp.setVisible(False)
        else:
            next_lv_point = newbiepass_lv_data[self._bp_lv][0]
            now_lv_point = 0 if self._bp_lv <= 1 else newbiepass_lv_data[self._bp_lv - 1][0]
            need_point = next_lv_point - now_lv_point
            self._sub_panel.nd_exp_num.lab_num_exp_need.SetString('/' + str(need_point))
            self._sub_panel.nd_exp_num.lab_num_exp.SetString(str(self._bp_point - now_lv_point))
            self._sub_panel.nd_exp.progress_exp.SetPercentage(float(self._bp_point - now_lv_point) / float(need_point) * 100)

    def _init_reward_list(self):

        def OnScrollingCallback():
            self._sub_panel.list_award._testScrollAndLoad()
            self._update_preview_level()

        self._sub_panel.list_award.OnScrolling = OnScrollingCallback

        @self._sub_panel.list_award.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_award_item(ui_item, idx + 1)
            if self._select_info:
                if self._select_info[0] == idx + 1:
                    sub_item = self._get_sub_item(idx + 1, self._select_info[1], self._select_info[2])
                    if sub_item:
                        self._set_select_btn(sub_item.btn_choose, is_preview=False)

        award_lst = self._sub_panel.list_award
        award_lst.SetVisibleRange(1, 2)
        award_lst.set_asyncLoad_interval_time(0.06)
        award_lst.SetInitCount(NEWBIEPASS_LV_CAP)
        award_lst._refreshItemPos()
        self._lv_award_to_left(self._bp_lv)

        def cb():
            award_lst.SetVisibleRange(10, 10)
            award_lst.set_asyncLoad_interval_time(0.01)
            award_lst.scroll_Load()

        award_lst.DelayCall(0.8, cb)

    def _lv_award_to_left(self, lv):
        show_num = self._get_show_num()
        if lv >= NEWBIEPASS_LV_CAP - show_num + 1:
            lv = NEWBIEPASS_LV_CAP - show_num + 1
        ctrl_size = self._sub_panel.list_award.GetCtrlSize()
        self._sub_panel.list_award.SetContentOffset(ccp(-ctrl_size.width * (lv - 1), 0))
        self._sub_panel.list_award.scroll_Load()
        self._update_preview_level()

    def _get_show_num(self):
        contentSize = self._sub_panel.list_award.GetContentSize()
        ctrl_size = self._sub_panel.list_award.GetCtrlSize()
        show_num = contentSize[0] / ctrl_size.width
        return show_num

    def _update_preview_level(self):
        offset = self._sub_panel.list_award.GetContentOffset()
        border = self._sub_panel.list_award.GetHorzBorder()
        indent = self._sub_panel.list_award.GetHorzIndent()
        show_num = self._get_show_num()
        ctrl_size = self._sub_panel.list_award.GetCtrlSize()
        right_level = (abs(offset.x) - border) / (ctrl_size.width + indent) + show_num
        preview_lv = int(math.ceil(right_level / 10.0)) * 10
        if self._last_preview_level != preview_lv:
            self.init_award_item(self._sub_panel.nd_reward_view.temp_award, preview_lv, preview=True)
            self._sub_panel.nd_reward_view.lab_level.SetString(str(preview_lv))
            self._last_preview_level = preview_lv
            self._update_preview_select_state()

    def init_award_item(self, item, lv, preview=False):
        record_lv = 0 if preview else lv
        self._lv_to_item[record_lv] = item
        list_item = [
         item.temp_reward_1, item.temp_reward_2_1, item.temp_reward_2_2]
        list_item_data = []
        for bp_type in BATTLE_CARD_TYPE:
            item_num = REWARD_NUM_DICT[bp_type]
            bp_type_data = [ [] for x in range(item_num) ]
            reward_lv = get_lv_reward(str(bp_type), lv)
            if isinstance(reward_lv, list):
                for x in range(item_num):
                    if x < len(reward_lv):
                        bp_type_data[x] = [
                         reward_lv[x], lv, bp_type, x]

            else:
                bp_type_data[0] = [
                 reward_lv, lv, bp_type, 0]
            list_item_data.extend(bp_type_data)

        for idx, sub_item in enumerate(list_item):
            item_data = list_item_data[idx]
            if not item_data or item_data[0] is None:
                sub_item.setVisible(False)
            else:
                sub_item.setVisible(True)
                template_item = getattr(sub_item, 'mall_item', None)
                if not template_item:
                    template_item = global_data.uisystem.load_template_create('mall/i_item', sub_item, name='mall_item')
                template_item.btn_choose.data = item_data

                @template_item.btn_choose.callback()
                def OnClick(btn, touch):
                    btn_reward_id, lv, bp_type, idx = btn.data
                    is_lock_lv = True if lv > self._bp_lv else False
                    if bp_type == NEWBIE_PASS_L2:
                        is_lock_lv = is_lock_lv or not self.has_pass_card
                    reward_record = global_data.player.get_newbiepass_reward_record().get(str(bp_type), None)
                    if reward_record is None:
                        is_received = False if 1 else reward_record.is_record(lv)
                        self._display_award_detail(lv, bp_type, btn_reward_id)
                        is_received or is_lock_lv or self._receive_award(bp_type, lv)
                    self._select_sub_button(lv, bp_type, idx)
                    return

                reward_id = item_data[0]
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                item_no, item_num = reward_list[0]
                init_tempate_mall_i_item(template_item, item_no, item_num=item_num)

        item.lab_level.SetString(str(lv))
        self._set_item_state(lv, preview)
        return

    def _get_reward_id_info(self, reward_id):
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        item_type = item_utils.get_lobby_item_type(item_no)
        return (
         pic_path, item_name, item_desc, item_num, item_type, item_no)

    def _get_sub_item(self, lv, pass_type, idx):
        item = self._lv_to_item.get(lv, None)
        if item is None:
            return
        else:
            sub_item_dict = {NEWBIE_PASS_L1: [item.temp_reward_1.mall_item],NEWBIE_PASS_L2: [
                              item.temp_reward_2_1.mall_item, item.temp_reward_2_2.mall_item]
               }
            sub_item = sub_item_dict[pass_type][idx]
            if not sub_item:
                return
            return sub_item

    def _select_sub_button(self, lv, pass_type, idx):
        self._select_info = [
         lv, pass_type, idx]
        self._update_preview_select_state()
        sub_item = self._get_sub_item(lv, pass_type, idx)
        if not sub_item:
            return
        self._set_select_btn(sub_item.btn_choose, is_preview=False)

    def _set_select_btn(self, btn, is_preview=False):
        attr_name = '_last_select_preview_btn' if is_preview else '_last_select_btn'
        last_select_btn = getattr(self, attr_name)
        if last_select_btn:
            last_select_btn.SetSelect(False)
        setattr(self, attr_name, btn)
        if btn:
            btn.SetSelect(True)

    def _update_preview_select_state(self):
        if not self._select_info or self._last_preview_level != self._select_info[0]:
            self._set_select_btn(None, is_preview=True)
            return
        else:
            sub_item = self._get_sub_item(PREVIEW_RECORD_LEVEL, self._select_info[1], self._select_info[2])
            self._set_select_btn(sub_item.btn_choose, is_preview=True)
            return

    def _set_item_state(self, lv, preview=False):
        record_lv = 0 if preview else lv
        item = self._lv_to_item.get(record_lv, None)
        if item is None:
            return
        else:
            is_lock_lv = True if lv > self._bp_lv else False
            if global_data.player:
                reward_records = global_data.player.get_newbiepass_reward_record()
            else:
                reward_records = {}
            for bp_type in BATTLE_CARD_TYPE:
                reward_record = reward_records.get(str(bp_type), None)
                if reward_record is None:
                    is_received = False if 1 else reward_record.is_record(lv)
                    mall_items = ()
                    if bp_type == NEWBIE_PASS_L1:
                        if not preview:
                            item.img_lock_1.setVisible(is_lock_lv)
                        mall_items = (
                         item.temp_reward_1.mall_item,)
                    elif bp_type == NEWBIE_PASS_L2:
                        is_lock_lv = is_lock_lv or not is_lock_lv and not self.has_pass_card
                        if not preview:
                            item.img_lock_2.setVisible(is_lock_lv)
                        mall_items = (
                         item.temp_reward_2_1.mall_item, item.temp_reward_2_2.mall_item)
                    for mall_item in mall_items:
                        if mall_item:
                            mall_item.nd_lock.setVisible(is_lock_lv)
                            mall_item.nd_get.setVisible(is_received)
                            mall_item.nd_get_tips.setVisible(not is_received and not is_lock_lv)

            if lv == self._bp_lv and not preview:
                item.img_frame_now.setVisible(True)
                item.img_level_now.setVisible(True)
                if self._last_lv is not None and self._last_lv != self._bp_lv:
                    item = self._lv_to_item.get(self._last_lv)
                    if item:
                        item.img_frame_now.setVisible(False)
                        item.img_level_now.setVisible(False)
                self._last_lv = self._bp_lv
            return

    def _display_award_detail(self, lv, pass_type, reward_id):
        self._display_info = [
         lv, pass_type, reward_id]
        pic_path, item_name, item_desc, item_num, item_type, item_no = self._get_reward_id_info(reward_id)
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type == L_ITEM_TYPE_EXPERIENCE_CARD:
            use_params = item_utils.get_lobby_item_use_parms(item_no) or {}
            add_item_no = use_params.get('add_item', None)
            if add_item_no:
                item_no = add_item_no
                item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in MODEL_DISPLAY_TYPE:
            self._display_node(ND_SPECIAL_REWARD)
            self._sub_panel.nd_special_reward.lab_name.SetString(item_name)
            self._sub_panel.nd_special_reward.lab_name.ChildResizeAndPosition()
            if item_type in (L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_MECHA_SFX):
                scene_data_conf_id = lobby_model_display_const.BATTLE_PASS
            else:
                scene_data_conf_id = lobby_model_display_const.BATTLE_PASS_02
            scene_data = lobby_model_display_utils.get_display_scene_data(scene_data_conf_id)
            global_data.emgr.change_model_display_scene_info.emit(scene_data)
            if item_type == L_ITEM_MECHA_SFX:
                item_display_data = confmgr.get('display_enter_effect', 'Content', str(item_no), default={})
                callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
                cSfxSoundName = item_display_data.get('cSfxSoundName', '')

                def on_finish_create_model(*args):
                    if callOutSfxPath:
                        global_data.emgr.change_model_preview_effect.emit(callOutSfxPath, cSfxSoundName)

                create_callback = on_finish_create_model
                item_no = global_data.player.get_lobby_selected_mecha_item_id()
                clothing_id = global_data.player.get_mecha_fashion(item_no)
                if clothing_id:
                    item_no = clothing_id
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no, is_in_battlepass=True)
                if clothing_id:
                    mecha_id = global_data.player.get_lobby_selected_mecha_id()
                    mpath = get_mecha_model_path(mecha_id, clothing_id)
                    submesh_path = get_mecha_model_h_path(mecha_id, clothing_id)
                    for data in model_data:
                        data['mpath'] = mpath
                        data['sub_mesh_path_list'] = [submesh_path]

            else:
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no, is_in_battlepass=True)
                create_callback = None
            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
        else:
            self._display_node(ND_COMMON_REWARD)
            self._sub_panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self._sub_panel.nd_common_reward.nd_item.img_frame.setVisible(False)
            self._sub_panel.nd_common_reward.lab_name.SetString(item_name)
            self._sub_panel.nd_common_reward.lab_describe.SetString(item_desc)
        return

    def _init_right_display(self):
        self._display_info = []
        self._right_node_num = ND_EMPTY
        self._display_map = {ND_EMPTY: {'node': self._sub_panel.nd_empty,'up_func': None},ND_BUY_CARD: {'node': self._sub_panel.nd_buy_card,'up_func': None},ND_COMMON_REWARD: {'node': self._sub_panel.nd_common_reward,'up_func': None},ND_SPECIAL_REWARD: {'node': self._sub_panel.nd_special_reward,'up_func': None}}
        self._sub_panel.nd_buy_card.lab_describe.SetString(get_text_by_id(80770).format(NEWBIEPASS_LV_CAP))
        self._sub_panel.nd_lock.setVisible(not self.has_pass_card)
        display_num = ND_EMPTY if self.has_pass_card else ND_BUY_CARD
        self._display_node(display_num)

        @self._sub_panel.nd_special_reward.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        @self._sub_panel.nd_buy_card.temp_buy_check.btn_common_big.unique_callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('PreviewReward', 'logic.comsys.battle_pass')
            ui.show_card_reward_desc(NEWBIE_CARD)

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

        if node_num != ND_SPECIAL_REWARD:
            global_data.emgr.change_model_display_scene_item.emit(None)
        self._right_node_num = node_num
        return

    def _update_can_received_num(self):
        can_receive_num = 0
        for bp_type in BATTLE_CARD_TYPE:
            if bp_type == NEWBIE_PASS_L2 and not self.has_pass_card:
                continue
            reward_record = global_data.player.get_newbiepass_reward_record().get(str(bp_type), None)
            for lv in range(self._bp_lv):
                bp_lv = lv + 1
                if reward_record is None:
                    is_received = False if 1 else reward_record.is_record(bp_lv)
                    reward_lv = is_received or get_lv_reward(str(bp_type), bp_lv)
                    if reward_lv:
                        if isinstance(reward_lv, list):
                            can_receive_num += len(reward_lv)
                        else:
                            can_receive_num += 1

        img_num_visible = False if can_receive_num == 0 else True
        self._sub_panel.temp_get_all.img_num.setVisible(img_num_visible)
        self._sub_panel.temp_get_all.img_num.lab_num.SetString(str(can_receive_num))
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def _receive_award(self, pass_type, lv):
        if global_data.player:
            global_data.player.receive_newbiepass_reward(str(pass_type), str(lv))

    def _bind_event(self, bind):
        e_conf = {'newbiepaas_update_lv': self._newbiepass_lv_up,
           'newbiepaas_open_type': self._newbiepass_buy_card,
           'newbiepaas_update_award': self._update_exist_item
           }
        if bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _update_exist_item(self, *args):
        for lv in self._lv_to_item:
            if lv == 0:
                lv = self._last_preview_level
                self._set_item_state(lv, True)
            else:
                self._set_item_state(lv)

        self._update_can_received_num()

    def _newbiepass_lv_up(self, bp_lv, bp_point):
        self._bp_lv = bp_lv
        self._bp_point = bp_point
        self._update_lv_show()
        self._update_exist_item()
        self._lv_award_to_left(self._bp_lv)

    def _newbiepass_buy_card(self, bp_type):
        if bp_type == str(NEWBIE_PASS_TYPE_1):
            self.has_pass_card = True
            self._sub_panel.nd_lock.setVisible(False)
            self._update_exist_item()
            self._update_card_buy_info()
            if self._sub_panel.nd_buy_card.isVisible():
                self._display_node(ND_EMPTY)

    def do_show_panel(self):
        if self.panel.nd_content.isVisible():
            return
        else:
            self.set_visible(True)
            if not self._display_info:
                global_data.emgr.change_model_display_scene_item.emit(None)
                return
            lv, bp_type, btn_reward_id = self._display_info
            self._display_award_detail(lv, bp_type, btn_reward_id)
            return

    def do_hide_panel(self):
        if not self.panel.nd_content.isVisible():
            return
        self.set_visible(False)

    def set_visible(self, flag):
        self.panel.nd_content.setVisible(flag)

    def _init_ui_event(self):

        @self._sub_panel.temp_get_all.btn_common_big.callback()
        def OnClick(*args):
            if global_data.player:
                global_data.player.receive_all_newbiepass_reward()

        @self._sub_panel.nd_control.temp_buy_card.btn_common_big.callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('BuyNewBieCardUI', 'logic.comsys.battle_pass')

        @self._sub_panel.nd_buy_card.temp_buy_card.btn_common_big.callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('BuyNewBieCardUI', 'logic.comsys.battle_pass')

        @self._sub_panel.btn_final.callback()
        def OnClick(*args):
            if self._on_final_lv:
                self._lv_award_to_left(self._bp_lv)
            else:
                contentSize = self._sub_panel.list_award.GetContentSize()
                ctrl_size = self._sub_panel.list_award.GetCtrlSize()
                show_num = contentSize[0] / ctrl_size.width
                self._lv_award_to_left(NEWBIEPASS_LV_CAP - show_num + 1)
            self._on_final_lv = not self._on_final_lv
            self._sub_panel.btn_final.img_right.setVisible(not self._on_final_lv)
            self._sub_panel.btn_final.img_left.setVisible(self._on_final_lv)
            text_id = 80766 if self._on_final_lv else 80831
            self._sub_panel.btn_final.SetText(text_id)

        @self._sub_panel.temp_get_exp.btn_common.unique_callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_task_ui
            jump_to_task_ui(TASK_TYPE_ASSESS)

    def destroy(self):
        self._last_select_btn = None
        self._last_select_preview_btn = None
        self._display_map = {}
        self.panel = None
        self._sub_panel = None
        self._display_info = []
        self._select_info = []
        self._bind_event(False)
        return