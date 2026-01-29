# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/MultiChosenSingleRewardUI.py
from __future__ import absolute_import
from functools import cmp_to_key
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from logic.gutils.mall_utils import item_has_owned_by_item_no

class MultiChosenSingleRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/award_choose_optional'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    GLOBAL_EVENT = {}
    UI_ACTION_EVENT = {'panel.temp_bar.btn_close.OnClick': 'on_close',
       'panel.temp_bar.temp_btn_sure.btn_major.OnClick': 'on_confirm'
       }

    def on_init_panel(self, *args, **kwargs):
        self.box_item_id = None
        self.box_item_count = 1
        self.reward_list = []
        self.reward_data = {}
        self.cur_reward_id = None
        self.id_2_nd = {}
        self.panel.temp_num.setVisible(False)
        self.panel.PlayAnimation('move')
        return

    def on_finalize_panel(self):
        self.reward_list = []
        self.reward_data = {}
        self.id_2_nd = {}

    def on_close(self, *args):
        self.close()

    def on_confirm(self, *args):
        total_num = 1
        if not self.cur_reward_id:
            return
        if self.cur_reward_id not in self.reward_list:
            return
        item_id = self.reward_data[self.cur_reward_id][0]
        if item_has_owned_by_item_no(item_id):
            return
        if not global_data.player:
            return
        global_data.player.use_item(self.box_item_id, total_num, {'select_reward_id': self.cur_reward_id})
        self.close()

    def set_use_params(self, item_data, *args, **kwargs):
        item_no = item_data['item_no']
        use_params = confmgr.get('lobby_item', str(item_no), default={})['use_params']
        self.box_item_id = item_data['id']
        self.box_item_count = item_data.get('quantity', 1)
        self.max_tips = use_params.get('max_tips')
        self.id_2_nd = {}
        self.reward_list = use_params['reward_list']
        self.reward_data = {}
        self.init_reward_data()
        self.reward_list = self.reorder_reward_list(self.reward_list)
        self.panel.list_award_choose.SetInitCount(len(self.reward_list))
        for i, reward_id in enumerate(self.reward_list):
            item_id, item_num = self.reward_data[reward_id][0], self.reward_data[reward_id][1]
            owned = item_has_owned_by_item_no(item_id)
            ui_item = self.panel.list_award_choose.GetItem(i)
            self.id_2_nd[reward_id] = ui_item
            init_tempate_reward(ui_item.temp_reward, item_id, item_num, isget=owned)

            @ui_item.temp_reward.btn_choose.callback()
            def OnClick(btn, touch, reward_id=reward_id):
                self.on_click_item(reward_id)

        self.update_introduction()
        self.update_confirm_btn()
        self.on_click_item(self.reward_list[0])

    def set_btn_use_visible(self, flag):
        self.panel.temp_bar.temp_btn_sure.btn_major.setVisible(flag)

    def on_click_item(self, reward_id):
        if reward_id == self.cur_reward_id:
            return
        if reward_id not in self.reward_data:
            return
        old_ui_item = self.id_2_nd.get(self.cur_reward_id)
        if old_ui_item:
            old_ui_item.temp_reward.btn_choose.SetSelect(False)
        self.cur_reward_id = reward_id
        ui_item = self.id_2_nd.get(reward_id)
        ui_item.temp_reward.btn_choose.SetSelect(True)
        self.update_introduction()
        self.update_confirm_btn()

    def update_introduction(self):
        if not self.cur_reward_id:
            self.panel.img_empty.setVisible(True)
            self.panel.nd_content.setVisible(False)
            self.panel.richtext_num.setVisible(False)
            self.panel.lab_choose.setVisible(False)
            return
        self.panel.img_empty.setVisible(False)
        self.panel.nd_content.setVisible(True)
        reward_id = self.cur_reward_id
        item_id, item_num = self.reward_data[reward_id]
        init_tempate_reward(self.panel.temp_item, item_id)
        self.panel.lab_name.SetString(get_lobby_item_name(item_id))
        self.panel.lab_quantity.SetString(str(item_num))
        self.panel.lab_details.SetString(get_lobby_item_desc(item_id))

    def update_confirm_btn(self):
        if self.cur_reward_id not in self.reward_data or not self.cur_reward_id:
            self.panel.temp_bar.temp_btn_sure.btn_major.SetEnable(False)
            return
        item_id = self.reward_data[self.cur_reward_id][0]
        owned = item_has_owned_by_item_no(item_id)
        self.panel.temp_bar.temp_btn_sure.btn_major.SetEnable(not owned)

    def init_reward_data(self):
        for i, reward_id in enumerate(self.reward_list):
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            self.reward_data[reward_id] = (item_id, item_num)

    def reorder_reward_list(self, reward_list):

        def cmp_func(reward_id_a, reward_id_b):
            item_id_a = self.reward_data[reward_id_a][0]
            owned_a = item_has_owned_by_item_no(item_id_a)
            item_id_b = self.reward_data[reward_id_b][0]
            owned_b = item_has_owned_by_item_no(item_id_b)
            if owned_a != owned_b:
                if owned_a:
                    return 1
                else:
                    return -1

            else:
                return 0

        ret_list = sorted(reward_list, key=cmp_to_key(cmp_func))
        return ret_list