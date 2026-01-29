# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/BattleFlagChooseWidget.py
from __future__ import absolute_import
from logic.gutils import career_utils
from logic.gutils import item_utils

class BattleFlagChooseWidget(object):
    MAX_NUM = 3

    def __init__(self, panel):
        self.panel = panel
        self.on_init_panel()

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel()

    def destroy(self):
        pass

    def init_parameters(self):
        self.flag_data = career_utils.get_owned_badge_ids()
        self.select_flag = global_data.player.get_battle_flag_medal() if global_data.player else []
        self.cur_select_index = None
        return

    def init_panel(self):

        @self.panel.btn_sure.btn_common.callback()
        def OnClick(btn, touch):
            self.on_click_sure_btn()

        self.panel.btn_sure.btn_common.SetEnable(False)
        self.panel.btn_sure.btn_common.SetText(80305)
        self.panel.lab_get_method.setVisible(False)
        self.panel.temp_price.setVisible(False)
        self.panel.img_empty.setVisible(not bool(self.flag_data))
        self.panel.lab_empty.SetString(81709)
        self.init_item_list()

    def init_item_list(self):
        flag_lst_nd = self.panel.list_change
        flag_lst_nd.SetInitCount(0)
        flag_lst_nd.SetTemplate('battle_flag/i_flag_life_item')
        item_count = len(self.flag_data)
        flag_lst_nd.SetInitCount(item_count)
        self.refresh_select_view(True)
        self.panel.lab_item_describe.setVisible(False)

    def set_select_flag(self, index):
        flag_lst_nd = self.panel.list_change
        if self.cur_select_index is not None:
            cur_item_widget = flag_lst_nd.GetItem(self.cur_select_index)
            cur_item_widget.btn.SetSelect(False)
        item_widget = flag_lst_nd.GetItem(index)
        item_widget.btn.SetSelect(True)
        item_no = self.flag_data[index]
        self.panel.lab_item_describe.setVisible(True)
        self.panel.lab_item_describe.SetString(career_utils.get_badge_brief_desc_text(str(item_no)))
        if item_no not in self.select_flag:
            self.panel.btn_sure.btn_common.SetText(80305)
        else:
            self.panel.btn_sure.btn_common.SetText(81247)
        self.panel.btn_sure.btn_common.SetEnable(True)
        self.cur_select_index = index
        return

    def on_click_sure_btn(self):
        item_no = self.flag_data[self.cur_select_index]
        if item_no not in self.select_flag:
            if len(self.select_flag) < self.MAX_NUM:
                self.select_flag.append(item_no)
            else:
                self.select_flag[-1] = item_no
        else:
            self.select_flag.remove(item_no)
        self.refresh_select_view()
        if item_no not in self.select_flag:
            self.panel.btn_sure.btn_common.SetText(80305)
        else:
            self.panel.btn_sure.btn_common.SetText(81247)
            global_data.game_mgr.show_tip(81702)
        if global_data.player:
            global_data.player.set_battle_flag_medal(self.select_flag)

    def refresh_select_view(self, is_click_register=False):
        flag_lst_nd = self.panel.list_change
        all_items = flag_lst_nd.GetAllItem()
        for index, item_widget in enumerate(all_items):
            temp_item = item_widget.temp_life_icon
            item_id = self.flag_data[index]
            if is_click_register:
                medal_task_id = str(item_id)
                level = career_utils.get_badge_level(medal_task_id)
                cp_reward_idx = career_utils.get_badge_got_cp_reward_idx(medal_task_id)
                career_utils.refresh_badge_item(temp_item, medal_task_id, level, cp_reward_idx=cp_reward_idx, check_got=False, ban_anim=True)
                item_widget.btn.SetText(career_utils.get_badge_name_text(medal_task_id))

                @item_widget.btn.unique_callback()
                def OnClick(btn, touch, index=index):
                    self.set_select_flag(index)

            if item_id in self.select_flag:
                item_widget.img_choose.setVisible(True)
                career_utils.darken_badge_item(temp_item, True)
                item_widget.lab_num.SetString(str(self.select_flag.index(item_id) + 1))
            else:
                item_widget.img_choose.setVisible(False)
                career_utils.darken_badge_item(temp_item, False)