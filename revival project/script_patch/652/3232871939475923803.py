# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySelectRewardsWidget.py
from __future__ import absolute_import
import six
import six_ex
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gutils.item_utils import check_skin_tag, get_lobby_item_rare_degree_pic_by_item_no, get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.lobby_click_interval_utils import global_unique_click
import six.moves.collections_abc
import collections

class LotterySelectRewardsWidget(BasePanel):
    PANEL_CONFIG_NAME = 'mall/bg_lottery_change_reward'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, selectable_turntable_item_list, selected_items_set, check_item_drawn_func, check_item_got_func, select_rewards_callback):
        self.selectable_turntable_item_list = selectable_turntable_item_list
        self.selected_items_set = selected_items_set
        self.check_item_drawn_func = check_item_drawn_func
        self.check_item_got_func = check_item_got_func
        self.select_rewards_callback = select_rewards_callback
        self.cur_selected_items_map = collections.OrderedDict()
        self.item_id_to_nd_map = {}
        self.init_panel()
        self.refresh_panel()

    def _register_btn_select(self, nd_btn, line_no, nd, item_id):

        @global_unique_click(nd_btn)
        def OnClick(*args):
            old_selected_item_id = self.cur_selected_items_map[line_no]
            if old_selected_item_id != item_id:
                self.item_id_to_nd_map[old_selected_item_id].icon.setVisible(False)
                self.cur_selected_items_map[line_no] = item_id
                nd.icon.setVisible(True)

    def init_panel(self):
        self.panel.list_item.SetInitCount(len(self.selectable_turntable_item_list))
        for line_no, turntable_item_list in enumerate(self.selectable_turntable_item_list):
            nd_list = self.panel.list_item.GetItem(line_no).list_item
            nd_list.SetInitCount(len(turntable_item_list))
            for i, (item_id, _) in enumerate(turntable_item_list):
                nd = nd_list.GetItem(i)
                check_skin_tag(nd.temp_level, item_id)
                nd.bar_bg.SetDisplayFrameByPath('', get_lobby_item_rare_degree_pic_by_item_no(item_id, 1))
                nd.item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_id))
                nd.lab_name.SetString(get_lobby_item_name(item_id))
                nd.icon.setVisible(False)
                self.item_id_to_nd_map[item_id] = nd
                self._register_btn_select(nd.btn_item, line_no, nd, item_id)
                self._register_btn_select(nd.btn_click, line_no, nd, item_id)

        @global_unique_click(self.panel.temp_confirm.btn_common)
        def OnClick(*args):
            cur_selected_items_set = set(six_ex.values(self.cur_selected_items_map))
            if cur_selected_items_set ^ self.selected_items_set:
                self.select_rewards_callback(cur_selected_items_set)
            self.hide()

        @global_unique_click(self.panel.btn_close)
        def OnClick(*args):
            self.hide()

    def refresh_panel(self):
        self.cur_selected_items_map.clear()
        for line_no, turntable_item_list in enumerate(self.selectable_turntable_item_list):
            cur_default_select_item_got = False
            for item_id, _ in turntable_item_list:
                nd = self.item_id_to_nd_map[item_id]
                if self.check_item_drawn_func(item_id):
                    nd.nd_got.setVisible(True)
                    nd.nd_got.txt_have.SetString(906668)
                    nd.icon.setVisible(False)
                    nd.btn_item.SetEnable(False)
                    nd.btn_click.SetEnable(False)
                else:
                    got = bool(self.check_item_got_func(item_id))
                    nd.nd_got.setVisible(got)
                    nd.nd_got.txt_have.SetString(80451)
                    nd.icon.setVisible(False)
                    if item_id in self.selected_items_set:
                        self.cur_selected_items_map[line_no] = item_id
                    else:
                        if line_no not in self.cur_selected_items_map:
                            self.cur_selected_items_map[line_no] = item_id
                            if got:
                                cur_default_select_item_got = True
                            continue
                        if not got and cur_default_select_item_got:
                            self.cur_selected_items_map[line_no] = item_id

            if line_no in self.cur_selected_items_map:
                item_id = self.cur_selected_items_map[line_no]
                self.item_id_to_nd_map[item_id].icon.setVisible(True)

    def on_finalize_panel(self):
        self.selectable_turntable_item_list = None
        self.selected_items_set = None
        self.check_item_drawn_func = None
        self.check_item_got_func = None
        self.select_rewards_callback = None
        self.cur_selected_items_map = None
        self.item_id_to_nd_map = None
        return

    def show(self, selected_items_set=None):
        super(LotterySelectRewardsWidget, self).show()
        if selected_items_set is not None:
            self.selected_items_set = selected_items_set
        self.refresh_panel()
        return


class LotteryPromareSelectRewardsWidget(BasePanel):
    PANEL_CONFIG_NAME = 'mall/i_mall_content_lottery_ss_reward_pool_new'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, selectable_item_list, selected_item_id, check_item_got_func, select_rewards_callback, hide_callback):
        self.selectable_item_list = selectable_item_list
        self.selected_item_id = selected_item_id
        self.check_item_got_func = check_item_got_func
        self.select_rewards_callback = select_rewards_callback
        self.hide_callback = hide_callback
        self.cur_selected_item_id = None
        self.item_id_to_nd_map = {}
        self.init_panel()
        self.refresh_panel()
        return

    def _register_btn_select(self, nd_item, item_id):

        @global_unique_click(nd_item.btn_choose)
        def OnClick(*args):
            if self.cur_selected_item_id != item_id:
                self.item_id_to_nd_map[self.cur_selected_item_id].btn_choose.SetSelect(False)
                self.cur_selected_item_id = item_id
                self.item_id_to_nd_map[item_id].btn_choose.SetSelect(True)

    def init_panel(self):
        self.panel.list_review_all.SetInitCount(1)
        nd_title = self.panel.list_review_all.GetItem(0)
        nd_title.img_quatity.SetDisplayFrameByPath('', 'gui/ui_res_2/lottery/img_quality_splus_ss.png')
        nd_title.lab_rate.setVisible(False)
        self.panel.temp_list.SetInitCount(1)
        nd_item_list = self.panel.temp_list.GetItem(0).list_all_item
        nd_item_list.SetInitCount(len(self.selectable_item_list))
        for index, item_id in enumerate(self.selectable_item_list):
            nd_item = nd_item_list.GetItem(index)
            init_tempate_mall_i_item(nd_item, item_id, isget=self.check_item_got_func(item_id), show_jump=False)
            self.item_id_to_nd_map[item_id] = nd_item
            self._register_btn_select(nd_item, item_id)

        @global_unique_click(self.panel.temp_btn_2.btn_common)
        def OnClick(*args):
            if self.cur_selected_item_id != self.selected_item_id:
                self.select_rewards_callback(self.cur_selected_item_id)
            self.hide()

        @global_unique_click(self.panel.temp_btn_1.btn_common)
        def OnClick(*args):
            self.hide()

    def refresh_panel(self):
        for item_id, nd_item in six.iteritems(self.item_id_to_nd_map):
            nd_item.btn_choose.SetSelect(item_id == self.cur_selected_item_id)

    def on_finalize_panel(self):
        self.selectable_item_list = None
        self.check_item_got_func = None
        self.select_rewards_callback = None
        self.item_id_to_nd_map = {}
        return

    def show(self, selected_item_id=None):
        super(LotteryPromareSelectRewardsWidget, self).show()
        if selected_item_id is not None:
            self.selected_item_id = selected_item_id
            self.cur_selected_item_id = selected_item_id
        if not self.cur_selected_item_id:
            self.cur_selected_item_id = self.selectable_item_list[0]
        self.refresh_panel()
        return

    def hide(self):
        super(LotteryPromareSelectRewardsWidget, self).hide()
        self.hide_callback()