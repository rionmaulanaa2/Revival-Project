# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/BattleFlagLocationWidget.py
from __future__ import absolute_import
from logic.gutils import locate_utils
from logic.gutils import template_utils
from logic.comsys.effect import ui_effect
from logic.gcommon.common_const import rank_const

class BattleFlagLocationWidget(object):
    MAX_NUM = 99

    def __init__(self, panel):
        self.panel = panel
        self.on_init_panel()
        self.process_event(True)

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel()

    def destroy(self):
        self.panel.list_change.setVisible(True)
        self.panel.list_rank_title.setVisible(False)
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_set_rank_title': self.on_set_rank_title
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        rank_title_dict = global_data.player.rank_title_dict
        self.title_data = locate_utils.get_all_rank_title_list(rank_title_dict)
        self.select_data = self.get_select_data()
        self.cur_select_index = None
        return

    def get_select_data(self):
        cur_use_title = global_data.player.rank_use_title_dict.get(global_data.player.rank_use_title_type, [])
        if cur_use_title:
            select_data = [
             global_data.player.rank_use_title_type]
            select_data.extend(cur_use_title)
            return select_data
        else:
            return None
            return None

    def init_panel(self):

        @self.panel.btn_sure.btn_common.callback()
        def OnClick(btn, touch):
            self.on_click_sure_btn()

        self.panel.btn_sure.btn_common.SetEnable(False)
        self.panel.btn_sure.btn_common.SetText(80305)
        self.panel.lab_get_method.setVisible(False)
        self.panel.temp_price.setVisible(False)
        self.panel.img_empty.setVisible(not bool(self.title_data))
        self.panel.lab_empty.SetString(10374)
        self.panel.list_change.setVisible(False)
        self.panel.list_rank_title.setVisible(True)
        self.init_item_list()

    def init_item_list(self):
        flag_lst_nd = self.panel.list_rank_title
        flag_lst_nd.SetInitCount(0)
        flag_lst_nd.SetTemplate('battle_flag/i_flag_title_item')
        item_count = len(self.title_data)
        flag_lst_nd.SetInitCount(item_count)
        self.refresh_select_view(True)
        self.panel.lab_item_describe.setVisible(False)

    def set_select_flag(self, index):
        flag_lst_nd = self.panel.list_rank_title
        if self.cur_select_index is not None:
            cur_item_widget = flag_lst_nd.GetItem(self.cur_select_index)
            cur_item_widget.btn.SetSelect(False)
        item_widget = flag_lst_nd.GetItem(index)
        item_widget.btn.SetSelect(True)
        rank_data = self.title_data[index]
        title_type = rank_data[0]
        rank_info = rank_data[1:]
        self.panel.lab_item_describe.setVisible(True)
        self.panel.lab_item_describe.SetString(locate_utils.get_rank_title(title_type, rank_info))
        self.cur_select_index = index
        self.refresh_sure_btn()
        return

    def refresh_sure_btn(self):
        rank_data = self.title_data[self.cur_select_index]
        done_text = 81247 if self.select_data and rank_data[0:3] == self.select_data[0:3] else 80305
        self.panel.btn_sure.btn_common.SetText(done_text)
        self.panel.btn_sure.btn_common.SetEnable(True)

    def on_set_rank_title(self):
        self.select_data = self.get_select_data()
        self.refresh_select_view()
        self.refresh_sure_btn()

    def on_click_sure_btn(self):
        rank_data = self.title_data[self.cur_select_index]
        if global_data.player:
            chosen = True if self.select_data and rank_data[0:3] == self.select_data[0:3] else False
            if chosen:
                global_data.player.request_set_rank_title(self.select_data[0], None)
                global_data.emgr.message_on_set_rank_title.emit()
            elif rank_data[0] == rank_const.RANK_TITLE_MECHA_REGION:
                global_data.player.request_set_mecha_region_rank_title(rank_data[1], rank_data[2])
            else:
                global_data.player.request_set_rank_title(rank_data[0], rank_data[1:])
        return

    def refresh_select_view(self, is_click_register=False):
        flag_lst_nd = self.panel.list_rank_title
        all_items = flag_lst_nd.GetAllItem()
        click_index = -1
        for index, item_widget in enumerate(all_items):
            rank_data = self.title_data[index]
            if is_click_register:
                template_utils.init_rank_title(item_widget.temp_title_icon, rank_data[0], rank_data[1:], show_item_expire=True)

                @item_widget.btn.unique_callback()
                def OnClick(btn, touch, index=index):
                    self.set_select_flag(index)

            chosen = True if self.select_data and rank_data[0:3] == self.select_data[0:3] else False
            ui_effect.set_dark(item_widget.temp_title_icon.img_icon, chosen)
            ui_effect.set_dark(item_widget.temp_title_icon.img_bg, chosen)
            item_widget.img_choose.setVisible(False)
            item_widget.temp_title_icon.img_choose.setVisible(chosen)
            if chosen:
                click_index = index

        if click_index >= 0 and is_click_register:
            self.set_select_flag(click_index)