# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/MultiChosenRewardUI.py
from __future__ import absolute_import
import six
import six_ex
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget

class MultiChosenRewardUI(WindowMediumBase):
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
        self.selected_num = {}
        self.cur_reward_id = None
        self.id_2_nd = {}
        self.ItemNumBtnWidget = None
        return

    def on_finalize_panel(self):
        self.reward_list = []
        self.reward_data = {}
        self.id_2_nd = {}
        if self.ItemNumBtnWidget:
            self.ItemNumBtnWidget.destroy()
            self.ItemNumBtnWidget = None
        return

    def on_close(self, *args):
        self.close()

    def on_confirm(self, *args):
        selection = []
        total_num = 0
        for reward_id, num in six.iteritems(self.selected_num):
            if 0 < num <= self.box_item_count:
                selection.append((self.reward_list.index(reward_id), num))
                total_num += num

        if total_num > self.box_item_count:
            return
        global_data.player.use_item(self.box_item_id, total_num, {'selection': selection})
        self.close()

    def on_bag_item_changed(self):
        if not self.box_item_id:
            self.close()
        item = global_data.player.get_item_by_id(self.box_item_id)
        new_count = item.get_current_stack_num()
        if new_count != self.box_item_count:
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
        self.panel.list_award_choose.SetInitCount(len(self.reward_list))
        for i, reward_id in enumerate(self.reward_list):
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            ui_item = self.panel.list_award_choose.GetItem(i)
            self.id_2_nd[reward_id] = ui_item
            self.reward_data[reward_id] = (item_id, item_num)
            init_tempate_reward(ui_item.temp_reward, item_id, item_num)

            @ui_item.temp_reward.btn_choose.callback()
            def OnClick(btn, touch, reward_id=reward_id):
                self.on_click_item(reward_id)

            self.update_item_count(reward_id)

        self.update_introduction()
        self.update_box_item_count()
        self.ItemNumBtnWidget = ItemNumBtnWidget(self.panel.temp_num)

    def on_click_item(self, reward_id):
        if reward_id == self.cur_reward_id:
            return
        old_ui_item = self.id_2_nd.get(self.cur_reward_id)
        if old_ui_item:
            old_ui_item.temp_reward.btn_choose.SetSelect(False)
        self.cur_reward_id = reward_id
        ui_item = self.id_2_nd.get(reward_id)
        ui_item.temp_reward.btn_choose.SetSelect(True)
        self.update_introduction()
        self.update_counter()

    def update_introduction(self):
        if not self.cur_reward_id:
            self.panel.img_empty.setVisible(True)
            self.panel.nd_content.setVisible(False)
            self.panel.richtext_num.SetString(get_text_by_id(609187).format(self.box_item_count))
            return
        self.panel.img_empty.setVisible(False)
        self.panel.nd_content.setVisible(True)
        reward_id = self.cur_reward_id
        item_id, item_num = self.reward_data[reward_id]
        init_tempate_reward(self.panel.temp_item, item_id)
        self.panel.lab_name.SetString(get_lobby_item_name(item_id))
        self.panel.lab_quantity.SetString(str(item_num))
        self.panel.lab_details.SetString(get_lobby_item_desc(item_id))

    def update_counter(self):
        if not self.cur_reward_id:
            return
        reward_id = self.cur_reward_id
        max_quantity = self.box_item_count - (sum(six_ex.values(self.selected_num)) - self.selected_num.get(reward_id, 0))
        item_data = {'reward_id': reward_id,
           'quantity': max_quantity,
           'min_num': 0
           }
        init_quantity = self.selected_num.get(reward_id, 0)
        self.ItemNumBtnWidget.init_item(item_data, self.on_num_changed, init_quantity, self.max_tips)

    def on_num_changed(self, reward_data, num):
        reward_id = reward_data['reward_id']
        self.selected_num[reward_id] = num
        self.update_item_count(reward_id)
        self.update_box_item_count()

    def update_box_item_count(self):
        selected_num = sum(six_ex.values(self.selected_num))
        text = '%d/%d' % (selected_num, self.box_item_count)
        self.panel.list_get.txt_price.SetString(text)
        self.panel.temp_btn_sure.btn_major.SetEnable(selected_num > 0)

    def update_item_count(self, reward_id):
        ui_item = self.id_2_nd.get(reward_id)
        if not ui_item:
            return
        count = self.selected_num.get(reward_id, 0)
        ui_item.nd_choose.setVisible(count > 0)
        ui_item.lab_num.SetString('x%d' % count)