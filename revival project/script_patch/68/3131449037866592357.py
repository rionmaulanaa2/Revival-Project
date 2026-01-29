# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BattlePassRewardListWidget.py
from __future__ import absolute_import
from six.moves import range
import math
from common.utils.cocos_utils import ccp
from common.uisys.BaseUIWidget import BaseUIWidget
PREVIEW_RECORD_IDX = -1

class BattlePassRewardListWidget(BaseUIWidget):

    def idx_to_left(self, idx):
        if idx >= self._cap:
            return
        show_first = True if idx < self._cap_first else False
        self.panel.list_award.setVisible(show_first)
        self.panel.list_award_2.setVisible(not show_first)
        self._set_btn_final_state(show_first)
        award_lst = self.panel.list_award if show_first else self.panel.list_award_2
        self._init_lst_load_param(award_lst)
        show_num = self._get_show_num(award_lst)
        if show_first:
            if idx >= self._cap_first - show_num:
                idx = self._cap_first - show_num
        else:
            idx = idx - self._cap_first
            if idx >= self._cap_second - show_num:
                idx = self._cap_second - show_num
        border, indent, ctrl_size = self._get_list_info(award_lst)
        off_set_value = (ctrl_size.width + indent) * idx + border
        award_lst.SetContentOffset(ccp(-off_set_value, 0))
        award_lst.scroll_Load()
        self._update_preview_level(show_first)

    def select_sub_button(self, idx, reward_num, reward_sub_num):
        self._select_info = [
         idx, reward_num, reward_sub_num]
        self._update_preview_select_state()
        sub_item = self._get_sub_item(idx, reward_num, reward_sub_num)
        if not sub_item:
            return
        self.set_select_btn(sub_item.btn_choose, is_preview=False)

    def get_exist_item_by_idx(self, idx):
        item = self._idx_to_item.get(idx, None)
        return item

    def get_exist_item_dict(self):
        return self._idx_to_item

    def get_last_preview_idx(self):
        return self._last_preview_idx

    def set_lock(self, is_locked):
        self.panel.nd_lock.setVisible(is_locked)

    def set_current_idx(self, idx):
        self._current_idx = idx
        self.idx_to_left(idx)

    def set_select_btn(self, btn, is_preview=False):
        attr_name = '_last_select_preview_btn' if is_preview else '_last_select_btn'
        last_select_btn = getattr(self, attr_name)
        if last_select_btn:
            last_select_btn.SetSelect(False)
        setattr(self, attr_name, btn)
        if btn:
            btn.SetSelect(True)

    def clear_select_info(self):
        self._select_info = []

    def __init__(self, parent_ui, panel, cap, first_list_cap=0, i_level_award_init_func=None):
        self.global_events = {}
        super(BattlePassRewardListWidget, self).__init__(parent_ui, panel)
        self._cap_first = first_list_cap
        self._cap_second = cap - first_list_cap
        self._cap = cap
        self._last_right_idx = None
        self._last_preview_idx = None
        self._last_select_btn = None
        self._last_select_preview_btn = None
        self._idx_to_item = dict.fromkeys(range(cap + 1), None)
        self._i_level_award_init_func = i_level_award_init_func
        self._select_info = []
        self._current_idx = 0
        self._inited_reward_lst = set()
        self._btn_back_txt = get_text_by_id(82118).format(self._cap_first)
        self._btn_forward_txt = get_text_by_id(82119).format(self._cap_first)
        self._init_ui_event()
        return

    def init_reward_list(self):

        def on_create_callback(lv, idx, ui_item):
            if lv == self.panel.list_award_2:
                real_idx = self._cap_first + idx if 1 else idx
                self.init_award_item(ui_item, real_idx)
                if self._select_info and self._select_info[0] == idx:
                    sub_item = self._get_sub_item(idx, self._select_info[1], self._select_info[2])
                    if sub_item:
                        self.set_select_btn(sub_item.btn_choose, is_preview=False)

        if self._cap_second:
            reward_lst_init_info = (
             [
              self.panel.list_award, self._cap_first],
             [
              self.panel.list_award_2, self._cap_second])
        else:
            reward_lst_init_info = (
             [
              self.panel.list_award, self._cap_first],)
        for award_lst, cap in reward_lst_init_info:

            def OnScrollingCallback(is_first=award_lst == self.panel.list_award, award_list=award_lst):
                award_list._testScrollAndLoad()
                if award_list.isVisible():
                    self._update_preview_level(is_first)

            award_lst.BindMethod('OnCreateItem', on_create_callback)
            award_lst.OnScrolling = OnScrollingCallback
            award_lst.SetVisibleRange(1, 2)
            award_lst.set_asyncLoad_interval_time(0.06)
            award_lst.SetInitCount(cap, need_load=False)
            award_lst._refreshItemPos()
            award_lst.setAccelerationRelease(-500.0)

    def _init_lst_load_param(self, award_lst, need_delay=True):
        if award_lst in self._inited_reward_lst:
            return
        self._inited_reward_lst.add(award_lst)

        def cb(a_lst=award_lst):
            a_lst.SetVisibleRange(10, 10)
            a_lst.set_asyncLoad_interval_time(0.01)
            a_lst.scroll_Load()

        if need_delay:
            award_lst.DelayCall(1.0, cb)
        else:
            cb()

    def _update_preview_level(self, is_first_lst):
        award_lst = self._get_reward_lst(is_first_lst)
        offset = award_lst.GetContentOffset()
        border, indent, ctrl_size = self._get_list_info(award_lst)
        show_num = self._get_show_num(award_lst)
        left_idx = (abs(offset.x) - border + indent) / (ctrl_size.width + indent)
        right_idx = left_idx + show_num
        if not is_first_lst:
            right_idx += self._cap_first
            left_idx += self._cap_first
        if int(right_idx) == self._last_right_idx:
            return
        self._last_right_idx = int(right_idx)
        next_vis = True if self._current_idx > int(right_idx) else False
        back_vis = True if self._current_idx < int(left_idx) and not next_vis else False
        self.panel.nd_btn_more.btn_back.setVisible(back_vis)
        self.panel.nd_btn_more.btn_next.setVisible(next_vis)
        preview_idx = int(math.ceil(right_idx / 10.0)) * 10 - 1
        if self._last_preview_idx != preview_idx:
            self.init_award_item(self.panel.nd_reward_view.temp_award, preview_idx, preview=True)
            self.panel.nd_reward_view.lab_level.SetString(str(preview_idx + 1))
            self._last_preview_idx = preview_idx
            self._update_preview_select_state()
            self._set_btn_final_state(is_first_lst)

    def init_award_item(self, item, idx, preview=False):
        record_idx = -1 if preview else idx
        self._idx_to_item[record_idx] = item
        self._i_level_award_init_func(item, idx, preview)
        item.lab_level.SetString(str(idx + 1))

    def _get_list_info(self, award_lst):
        border = award_lst.GetHorzBorder()
        indent = award_lst.GetHorzIndent()
        ctrl_size = award_lst.GetCtrlSize()
        return (
         border, indent, ctrl_size)

    def _get_show_num(self, award_lst):
        border, indent, ctrl_size = self._get_list_info(award_lst)
        contentSize = award_lst.GetContentSize()
        show_num = (contentSize[0] - border + indent) / (ctrl_size.width + indent)
        return show_num

    def _get_reward_lst(self, is_first):
        if is_first:
            return self.panel.list_award
        return self.panel.list_award_2

    def _update_preview_select_state(self):
        if not self._select_info or self._last_preview_idx != self._select_info[0]:
            self.set_select_btn(None, is_preview=True)
            return
        else:
            sub_item = self._get_sub_item(PREVIEW_RECORD_IDX, self._select_info[1], self._select_info[2])
            self.set_select_btn(sub_item.btn_choose, is_preview=True)
            return

    def _get_sub_item(self, idx, reward_num, reward_sub_num):
        item = self._idx_to_item.get(idx, None)
        if item is None:
            return
        else:
            if str(reward_num) == '1':
                sub_item = getattr(item, 'temp_reward_{0}'.format(reward_num))
            else:
                sub_item = getattr(item, 'temp_reward_{0}_{1}'.format(reward_num, reward_sub_num + 1))
            if not sub_item:
                return
            sub_item = sub_item.mall_item
            return sub_item

    def _init_ui_event(self):

        def _on_click_check_reward(*args):
            is_first = self.panel.list_award.isVisible()
            self._show_second() if is_first else self._show_first()

        self.panel.btn_final.BindMethod('OnClick', _on_click_check_reward)

        def _on_click_go_to_now(*args):
            self.idx_to_left(self._current_idx)

        self.panel.nd_btn_more.btn_next.BindMethod('OnClick', _on_click_go_to_now)
        self.panel.nd_btn_more.btn_back.BindMethod('OnClick', _on_click_go_to_now)

    def _set_btn_final_state(self, showing_first):
        if showing_first:
            vis = self._last_preview_idx == self._cap_first - 1
            txt_id = self._btn_back_txt
        else:
            vis, txt_id = True, self._btn_forward_txt
        self.panel.btn_final.setVisible(vis)
        self.panel.btn_final.SetText(txt_id)

    def _show_first(self):
        self.panel.list_award.setVisible(True)
        self.panel.list_award_2.setVisible(False)
        self.panel.list_award.ScrollToRight()
        self.panel.list_award._testScrollAndLoad()
        self._set_btn_final_state(True)
        self._update_preview_level(True)
        self._init_lst_load_param(self.panel.list_award, need_delay=False)

    def _show_second(self):
        self.panel.list_award.setVisible(False)
        self.panel.list_award_2.setVisible(True)
        self.panel.list_award_2.ScrollToLeft()
        self.panel.list_award_2._testScrollAndLoad()
        self._set_btn_final_state(False)
        self._update_preview_level(False)
        self._init_lst_load_param(self.panel.list_award_2, need_delay=False)

    def destroy(self):
        self._inited_reward_lst = set()
        self._last_select_btn = None
        self._last_select_preview_btn = None
        self._select_info = []
        super(BattlePassRewardListWidget, self).destroy()
        return