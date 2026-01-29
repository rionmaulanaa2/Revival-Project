# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaProficiencyWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_rare_degree_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status, jump_to_ui
from logic.gcommon.item import item_const
from logic.gutils.template_utils import init_common_item_head, init_tempate_mall_i_item
from common.utils.timer import CLOCK
from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
from common.framework import Functor

class MechaProficiencyWidget(BaseUIWidget):
    USE_CNT_LIST = [
     1, 2, 5]

    def __init__(self, parent, panel, mecha_type):
        self.global_events = {'update_proficiency_event': self.on_update_proficiency,
           'update_proficiency_reward_event': self.on_update_reward_status,
           'on_lobby_bag_item_changed_event': self.on_card_num_changed,
           'player_item_update_event': self.on_update_mecha_status
           }
        super(MechaProficiencyWidget, self).__init__(parent, panel)
        self.init_parameters()
        self.init_widget(str(mecha_type))
        self.init_ui_event()
        self.init_add_prof_item_list()
        self.init_reward_view()

    def init_parameters(self):
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._reward_levels = confmgr.get('proficiency_config', 'RewardLevels')
        self._max_dan_lv = len(self._dan_conf)
        self._max_level = len(self._prof_conf)
        self._cur_mecha_type = None
        self._reward_item_dict = None
        self._show_reward_inf_timer = None
        self._card_item_dict = {}
        self._cnt_timer = None
        self._use_cnt_idx = 0
        self._use_timer = None
        self._can_use = True
        self._cur_select_reward_btn = None
        return

    def init_widget(self, mecha_type):
        if not global_data.player:
            return
        if self._cur_mecha_type == mecha_type:
            return
        if self._cur_mecha_type:
            self._cur_mecha_type = mecha_type
        self._cur_mecha_type = mecha_type
        level, proficiency = global_data.player.get_proficiency(self._cur_mecha_type)
        self.on_update_proficiency(mecha_type, level, proficiency)
        nd = self.panel.nd_details
        nd.nd_proficiency.nd_add_proficiency.setVisible(False)
        has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
        nd.nd_proficiency.setVisible(has_mecha)
        nd.nd_proficiency_lock.setVisible(not has_mecha)
        if not has_mecha:
            self.on_close_proficiency_reward()
        if nd.nd_proficiency_reward.isVisible():
            self.update_all_reward_status()

    def init_ui_event(self):
        nd = self.panel.nd_details
        nd.nd_proficiency.BindMethod('OnClick', Functor(self.on_click_proficiency))
        nd.nd_proficiency_reward.btn_close.BindMethod('OnClick', Functor(self.on_close_proficiency_reward))
        nd.nd_proficiency.nd_proficiency_level.btn_add.BindMethod('OnClick', Functor(self.on_show_add_proficiency, True))
        nd.nd_proficiency.nd_add_proficiency.nd_close.BindMethod('OnClick', Functor(self.on_show_add_proficiency, False))
        nd.nd_proficiency.nd_proficiency_level.btn_tips.BindMethod('OnClick', Functor(self.on_show_tips))

    def init_add_prof_item_list(self):
        nd = self.panel.nd_details
        for item_no in item_const.ITEM_NO_PROF_CARD_LIST:
            nd_item = nd.nd_proficiency.nd_add_proficiency.list_item.AddTemplateItem()
            nd_item.lab_name.SetString(get_lobby_item_name(item_no))
            nd_item.lab_describe.SetString(get_lobby_item_desc(item_no))
            item_num = global_data.player.get_item_num_by_no(item_no)
            init_tempate_mall_i_item(nd_item.temp_item, item_no, item_num)
            if item_num <= 0:
                nd_item.nd_get.setVisible(True)
            else:
                nd_item.nd_get.setVisible(False)
            nd_item.btn_add.item_no = item_no
            nd_item.btn_add.item_num = item_num
            self._card_item_dict[item_no] = nd_item

            @nd_item.btn_add.unique_callback()
            def OnBegin(btn, touch):
                if self._use_timer:
                    return False
                self._use_cnt_idx = 0
                if self.use_card(self._cur_mecha_type, btn.item_no):
                    btn.use_card = True
                    self._cnt_timer = global_data.game_mgr.register_logic_timer(self.on_add_use_cnt, 2, mode=CLOCK)
                    self._use_timer = global_data.game_mgr.register_logic_timer(self.use_card, 0.3, (self._cur_mecha_type, btn.item_no), mode=CLOCK)
                return True

            @nd_item.btn_add.unique_callback()
            def OnClick(btn, touch):
                item_num = global_data.player.get_item_num_by_no(btn.item_no)
                if not btn.use_card and item_num == 0:
                    jump_to_ui(btn.item_no)
                btn.use_card = False
                return True

            @nd_item.btn_add.unique_callback()
            def OnEnd(btn, touch):
                self.cancel_cnt_timer()
                self.cancel_use_timer()
                self._use_cnt_idx = 0
                self._can_use = True
                return True

    def on_add_use_cnt(self):
        self._use_cnt_idx += 1
        if self._use_cnt_idx == len(self.USE_CNT_LIST) - 1:
            self.cancel_cnt_timer()

    def on_card_num_changed(self):
        for item_no in item_const.ITEM_NO_PROF_CARD_LIST:
            nd_item = self._card_item_dict.get(item_no, None)
            if not nd_item:
                continue
            new_item_num = global_data.player.get_item_num_by_no(item_no)
            if new_item_num < nd_item.btn_add.item_num:
                self._can_use = True
            nd_item.btn_add.item_num = new_item_num
            nd_item.temp_item.lab_quantity.SetString(str(new_item_num))
            if new_item_num <= 0:
                nd_item.nd_get.setVisible(True)
            else:
                nd_item.nd_get.setVisible(False)

        return

    def use_card(self, mecha_id, item_no):
        if not self._can_use:
            return False
        if not mecha_has_owned_by_mecha_id(int(mecha_id)):
            return False
        item = global_data.player.get_item_by_no(item_no)
        item_num = global_data.player.get_item_num_by_no(item_no)
        use_cnt = min(item_num, self.USE_CNT_LIST[self._use_cnt_idx])
        if use_cnt > 0:
            global_data.player.use_item(item.get_id(), use_cnt, {'mecha_type': str(mecha_id)})
            self._can_use = False
            return True
        return False

    def on_update_mecha_status(self):
        if self._cur_mecha_type:
            nd = self.panel.nd_details
            if nd and nd.nd_proficiency and nd.nd_proficiency_lock:
                has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
                nd.nd_proficiency.setVisible(has_mecha)
                nd.nd_proficiency_lock.setVisible(not has_mecha)

    def on_show_add_proficiency(self, isVisible, *args):
        nd = self.panel.nd_details
        nd.nd_proficiency.nd_add_proficiency.setVisible(isVisible)
        if isVisible:
            nd.nd_proficiency_reward.setVisible(False)

    def on_show_tips(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(608082), get_text_by_id(608083))

    def cancel_cnt_timer(self):
        if self._cnt_timer:
            global_data.game_mgr.unregister_logic_timer(self._cnt_timer)
        self._cnt_timer = None
        return

    def cancel_use_timer(self):
        if self._use_timer:
            global_data.game_mgr.unregister_logic_timer(self._use_timer)
        self._use_timer = None
        return

    def on_update_proficiency(self, mecha_type, level, proficiency, lv_up=False):
        if self._cur_mecha_type != mecha_type:
            return
        else:
            if level < self._max_level:
                upgrade_value = self._prof_conf.get(str(level + 1), {}).get('upgrade_value', 0)
            else:
                upgrade_value = self._prof_conf.get(str(level), {}).get('upgrade_value', 0)
                proficiency = upgrade_value
            nd = self.panel.nd_details
            nd.lab_level.SetString('Lv%d' % level)
            nd.lab_exp_need.SetString('\\%d' % upgrade_value)
            nd.lab_exp.SetString('%d' % proficiency)
            if upgrade_value:
                nd.progress_exp.SetPercentage(proficiency * 100.0 / upgrade_value)
            else:
                nd.progress_exp.SetPercentage(100)
            if lv_up:
                nd.PlayAnimation('level_up')
            dan_lv = self.get_dan_lv(level)
            self.update_nd_dan_lv(nd, dan_lv)
            next_reward_lv = 0
            reward = None
            for reward_lv in self._reward_levels:
                if reward_lv > level:
                    next_reward_lv = reward_lv
                    reward = self._prof_conf.get(str(next_reward_lv), {}).get('reward', {}).get(self._cur_mecha_type, None)
                    break

            if reward:
                reward_conf = confmgr.get('common_reward_data', str(reward))
                reward_list = reward_conf.get('reward_list', [])
                nd.lab_reward.setVisible(True)
                nd.temp_reward.setVisible(True)
                nd.lab_max.setVisible(False)
                nd.lab_reward.SetString(get_text_by_id(601008).format(next_reward_lv))
                for item_no, item_num in reward_list:
                    nd_item = nd.temp_reward
                    init_tempate_mall_i_item(nd_item, item_no, item_num)

            else:
                nd.lab_reward.setVisible(False)
                nd.temp_reward.setVisible(False)
                nd.lab_max.setVisible(True)
            self._check_has_unreceived_reward()
            return

    def update_nd_dan_lv(self, nd, dan_lv, show_dan_level=True):
        if not show_dan_level:
            nd.img_proficiency_level.setVisible(False)
            nd.lab_proficiency_level.setVisible(False)
        else:
            icon_path = self._dan_conf.get(str(dan_lv), {}).get('icon_path', '')
            name = self._dan_conf.get(str(dan_lv), {}).get('name', 0)
            if icon_path:
                nd.img_proficiency_level.SetDisplayFrameByPath('', icon_path)
            if name:
                nd.lab_proficiency_level.SetString(get_text_by_id(name))

    def get_dan_lv(self, level):
        dan_lv = 1
        for dan_lv in range(1, self._max_dan_lv + 1):
            max_level = self._dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def on_update_reward_status(self, mecha_type, lv, status):
        if self._cur_mecha_type != mecha_type:
            return
        else:
            if not self._reward_item_dict:
                return
            reward_item = self._reward_item_dict.get(lv, None)
            if reward_item:
                update_item_status(reward_item.temp_item, status)
                if status == item_const.ITEM_UNGAIN:
                    reward_item.img_lock.setVisible(True)
                else:
                    reward_item.img_lock.setVisible(False)
            self._check_has_unreceived_reward()
            return

    def _check_has_unreceived_reward(self):
        nd = self.panel.nd_details
        need_tip = global_data.player.has_unreceived_prof_reward(self._cur_mecha_type)
        nd.img_tips.setVisible(need_tip)
        if need_tip:
            nd.PlayAnimation('reward_tips')
        else:
            nd.StopAnimation('reward_tips')

    def on_click_proficiency(self, *args):
        has_mecha = mecha_has_owned_by_mecha_id(self._cur_mecha_type)
        if not has_mecha:
            return
        nd = self.panel.nd_details
        nd.nd_proficiency_reward.setVisible(True)
        self.panel.nd_details.PlayAnimation('proficiency_reward_appear')
        self.panel.nd_details.PlayAnimation('proficiency_reward_checking')
        self.update_all_reward_status()

    def on_close_proficiency_reward(self, *args):
        nd = self.panel.nd_details
        nd.nd_proficiency_reward.setVisible(False)

    def init_reward_data(self):
        nd = self.panel.nd_details
        nd.list_reward.DeleteAllSubItem()
        self._reward_item_dict = {}
        reward_levels = self._reward_levels
        nd.list_reward.SetInitCount(0)
        nd.list_reward.SetInitCount(len(reward_levels))
        nd.list_reward.scroll_Load()
        nd.list_reward._refreshItemPos()

    def init_reward_view(self):

        @self.panel.nd_details.list_reward.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_reward_item(ui_item, idx)

    def init_reward_item(self, reward_item, idx):
        if self._reward_item_dict is None:
            return
        else:
            lv = self._reward_levels[idx]
            reward = self._prof_conf.get(str(lv), {}).get('reward', {}).get(self._cur_mecha_type, None)
            reward_conf = confmgr.get('common_reward_data', str(reward), default={})
            reward_list = reward_conf.get('reward_list', [])
            if reward and reward_list:
                item_no = reward_list[0][0]
                reward_item.lab_level.SetString(str(lv))
                init_tempate_mall_i_item(reward_item.temp_item, item_no)
                dan_lv = self.get_dan_lv(lv)
                if self._dan_conf.get(str(dan_lv - 1), {}).get('max_level', 0) != lv:
                    show_dan_lv = False
                else:
                    show_dan_lv = True
                self.update_nd_dan_lv(reward_item, dan_lv, show_dan_lv)
                self._reward_item_dict[lv] = reward_item
                reward_item.temp_item.btn_choose.item_no = item_no

                @reward_item.temp_item.btn_choose.unique_callback()
                def OnClick(btn, touch, level=lv):
                    self.cancel_show_reward_inf()
                    self._cur_select_reward_btn = btn
                    if global_data.player.can_receive_proficiency_reward(self._cur_mecha_type, level):
                        global_data.player.receive_proficiency_reward(self._cur_mecha_type, level)
                    else:
                        x, y = btn.GetPosition()
                        w, h = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        self.show_reward_inf(btn.item_no, wpos)
                    return True

            cur_lv, _ = global_data.player.get_proficiency(self._cur_mecha_type)
            if lv > cur_lv:
                status = item_const.ITEM_UNGAIN
            elif global_data.player.is_prof_reward_received(self._cur_mecha_type, lv):
                status = item_const.ITEM_RECEIVED
            else:
                status = item_const.ITEM_UNRECEIVED
            self.on_update_reward_status(self._cur_mecha_type, lv, status)
            return

    def update_all_reward_status(self):
        if not self.panel.nd_details.nd_proficiency_reward.isVisible():
            return
        else:
            if self._reward_item_dict is None:
                self.init_reward_data()
            else:
                cur_lv, _ = global_data.player.get_proficiency(self._cur_mecha_type)
                for idx in range(len(self._reward_levels)):
                    lv = self._reward_levels[idx]
                    reward_item = self._reward_item_dict.get(lv, None)
                    if reward_item:
                        self.init_reward_item(reward_item, idx)

            return

    def show_reward_inf(self, item_no, wpos):
        self._show_reward_inf_timer = None
        global_data.emgr.show_item_desc_ui_event.emit(item_no, wpos)
        if self._cur_select_reward_btn:
            self._cur_select_reward_btn.SetSelect(True)
        return

    def cancel_show_reward_inf(self):
        global_data.emgr.hide_item_desc_ui_event.emit()
        if self._cur_select_reward_btn:
            self._cur_select_reward_btn.SetSelect(False)

    def get_prof_reward_status(self, mecha_type, lv):
        reward_record = global_data.player.get_prof_reward_data(mecha_type)
        if not reward_record:
            return item_const.ITEM_UNGAIN
        if reward_record.is_record(lv):
            return item_const.ITEM_RECEIVED
        return item_const.ITEM_UNRECEIVED

    def destroy(self):
        self.cancel_show_reward_inf()
        self.cancel_cnt_timer()
        self.cancel_use_timer()
        self._prof_conf = None
        self._dan_conf = None
        self._reward_levels = None
        self._reward_item_dict = None
        self._cur_select_reward_btn = None
        super(MechaProficiencyWidget, self).destroy()
        return