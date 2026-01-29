# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/MultiRewardUI.py
from __future__ import absolute_import
from six.moves import range
import math
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name, get_item_chip_data
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata.bond_config import get_unlock_role_id_of_bond_item
from logic.gutils.reward_item_ui_utils import refresh_item_info
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA
from logic.gcommon.common_utils.local_text import get_text_by_id

class MultiRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/award_choose'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    GLOBAL_EVENT = {'on_lobby_bag_item_changed_event': 'on_bag_item_changed'
       }
    UI_ACTION_EVENT = {'panel.temp_bar.btn_close.OnClick': 'on_close',
       'panel.temp_bar.temp_btn_sure.btn_major.OnClick': 'on_confirm'
       }

    def on_init_panel(self, *args, **kwargs):
        self.item_id = None
        self.item_count = 1
        self.to_select_num = 0
        self.lobby_items = []
        self.selected_item = []
        self.use_item_count = 1
        self.exchange_open_time = {}
        self.ItemNumBtnWidget = None
        self._touch_pos = None
        self.tag_sort_func_dict = {'role_bond': self._role_bond_sort_func
           }
        self.tag_item_num_func_dict = {'role_bond': self._role_bond_item_update_func
           }
        return

    def on_finalize_panel(self):
        self.tag_sort_func_dict = {}
        self.tag_item_num_func_dict = {}
        self.destroy_widget('ItemNumBtnWidget')

    def click_callback(self, item):
        if self.to_select_num == 1:
            selected = item in self.selected_item
            if not selected:
                if len(self.selected_item) > 0:
                    self.selected_item[0].btn_choose.SetSelect(False)
                self.selected_item = [
                 item]
                item.btn_choose.SetSelect(True)
                self.update_text()
                self.update_suggest_item_use_num()
            return
        selected = item in self.selected_item
        if not selected and self.check_select_valid():
            return global_data.game_mgr.show_tip(get_text_by_id(81162))
        item.btn_choose.SetSelect(not selected)
        if selected:
            self.selected_item.remove(item)
        else:
            self.selected_item.append(item)
        self.update_text()
        self.update_suggest_item_use_num()

    def update_text(self):
        valid_num = self.check_select_valid() and self.use_item_count > 0
        self.panel.temp_btn_sure.btn_major.SetEnable(valid_num)
        if self.to_select_num != 1:
            msg = '{0}/{1}' if valid_num else '#BR{0}#n/{1}'
            self.panel.lab_num.SetString(msg.format(len(self.selected_item), self.to_select_num))
        self.show_bond_effect(valid_num)

    def update_suggest_item_use_num(self):
        item_num_tag_func = self.tag_item_num_func_dict.get(self.lobby_items_use_tag, None)
        if callable(item_num_tag_func):
            if self.selected_item:
                item = self.selected_item[0]
                select_item_no = item.bind_item_no
                item_num_tag_func(select_item_no)
            elif self.lobby_items:
                reward_id = self.lobby_items[0]
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                select_item_no, _ = reward_conf['reward_list'][0]
                item_num_tag_func(select_item_no)
        return

    def on_close(self, *args):
        self.close()

    def on_confirm(self, *args):
        if self.check_select_valid():
            item_list = []
            for item in self.selected_item:
                reward_id = item.bind_reward_id
                if self.get_open_countdown_days(reward_id) > 0:
                    global_data.game_mgr.show_tip(870064)
                    return
                item_list.append(item.bind_item_id)

            if global_data.player:
                global_data.player.use_item(self.item_id, self.use_item_count, {'selection': item_list})
            else:
                global_data.game_mgr.show_tip(get_text_by_id(258))
            if self.to_select_num != 1:
                self.on_close()

    def check_select_valid(self):
        return len(self.selected_item) == self.to_select_num

    def on_num_changed(self, item_data, num):
        self.use_item_count = num
        self.update_text()

    def on_bag_item_changed(self):
        if not self.item_id:
            return
        item = global_data.player.get_item_by_id(self.item_id)
        if not item:
            self.on_close()
            return
        item_data = {'id': self.item_id,
           'item_no': item.get_item_no(),
           'quantity': item.get_current_stack_num()
           }
        self.item_count = item_data.get('quantity', 1)
        if self.ItemNumBtnWidget:
            self.ItemNumBtnWidget.init_item(item_data, self.on_num_changed)
        self.update_list_award_choose()

    def set_click_callback(self, temp_item_ui, item_id):
        temp_item_ui.btn_choose.SetPressEnable(True)
        self._touch_pos = None

        @temp_item_ui.btn_choose.unique_callback()
        def OnBegin(btn, touch):
            self._touch_pos = touch.getLocation()
            return True

        @temp_item_ui.btn_choose.callback()
        def OnPressedWithNum(ctrl, num):
            position = self._touch_pos
            if not position:
                return
            else:
                desc_str = ''
                item_type = get_lobby_item_type(item_id)
                if item_type == L_ITEM_TYPE_MECHA:
                    desc_str = get_text_by_id(592542).format(get_lobby_item_name(item_id))
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position, extra_info={'show_desc': desc_str,'show_jump': False})
                return

        @temp_item_ui.btn_choose.callback()
        def OnClick(ctrl, touch):
            self.click_callback(temp_item_ui)

        return

    def set_use_params(self, item_data, *args, **kwargs):
        item_no = item_data['item_no']
        use_params = confmgr.get('lobby_item', str(item_no), default={})['use_params']
        self.item_id = item_data['id']
        self.to_select_num = use_params['select']
        lobby_items = use_params['reward_list']
        self.lobby_items = lobby_items
        self.lobby_items_use_tag = use_params.get('use_tag', '')
        if self.lobby_items_use_tag:
            func = self.tag_sort_func_dict.get(self.lobby_items_use_tag, '')
            if callable(func):
                self.lobby_items = func(lobby_items)
        self.max_tips = use_params.get('max_tips')
        self.exchange_open_time = use_params.get('item_exchange_open_time', {})
        if self.to_select_num == 1:
            self.item_count = item_data.get('quantity', 1)
            self.panel.temp_num.setVisible(True)
            self.panel.nd_muti_choose.setVisible(False)
            self.ItemNumBtnWidget = ItemNumBtnWidget(self.panel.temp_num)
            self.ItemNumBtnWidget.init_item(item_data, self.on_num_changed, max_tips=self.max_tips)
        else:
            self.panel.temp_num.setVisible(False)
            self.panel.nd_muti_choose.setVisible(True)
        self.update_suggest_item_use_num()
        for i in range(len(self.lobby_items)):
            reward_id = self.lobby_items[i]
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            template_item = self.panel.list_award_choose.AddTemplateItem(bRefresh=True)
            template_item.temp_reward.bind_item_id = lobby_items.index(reward_id)
            template_item.temp_reward.bind_item_no = item_id
            template_item.temp_reward.bind_reward_id = reward_id
            template_item.lab_name.SetString(get_lobby_item_name(item_id))
            init_tempate_reward(template_item.temp_reward, item_id, item_num)
            get_status = self.get_item_get_status(item_id)
            if get_status:
                chip_data = get_item_chip_data(item_id) if 1 else None
                show_get_and_chip = bool(get_status and chip_data)
                template_item.temp_reward.nd_get_2 and template_item.temp_reward.nd_get_2.setVisible(show_get_and_chip)
                template_item.temp_fragments.setVisible(show_get_and_chip)
                chip_data and refresh_item_info(template_item.temp_fragments, chip_data['chip_id'], chip_data['chip_rate'])
                countdown_days = self.get_open_countdown_days(reward_id)
                if countdown_days > 0:
                    template_item.nd_lock.setVisible(True)
                    template_item.nd_lock.lab_lock.SetString(603006, args=(countdown_days,))
                self.set_click_callback(template_item.temp_reward, item_id)

        self.update_text()
        return

    def get_open_countdown_days(self, reward_id):
        now = tutil.get_server_time()
        open_timestamp = self.exchange_open_time.get(str(reward_id))
        if open_timestamp and open_timestamp > now:
            delta_day = tutil.get_delta_days(open_timestamp, now)
            return delta_day
        return 0

    def show_bond_effect(self, valid_num):
        from logic.gutils import bond_utils
        self.panel.nd_like.setVisible(valid_num)
        if not valid_num:
            return
        item = self.selected_item[0]
        select_item_no = item.bind_item_no
        role_id_list = bond_utils.get_roles_by_bond_item(select_item_no, 3)
        if not role_id_list:
            self.panel.nd_like.setVisible(False)
            return
        role_id = role_id_list[0]
        icon_path = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'icon') or ''
        if icon_path:
            self.panel.img_role.SetDisplayFrameByPath('', icon_path)
        name_text = get_lobby_item_name(role_id)
        self.panel.lab_name.SetString(name_text)

    def get_item_get_status(self, item_id):
        player = global_data.player
        if not player:
            return False
        else:
            role_id = get_unlock_role_id_of_bond_item(item_id)
            if role_id:
                if player.has_permanent_item_by_no(role_id):
                    return True
                return False
            return player.get_item_num_by_no(item_id) > 0

    def update_list_award_choose(self, *args):
        if not self.panel or not self.panel.isValid():
            return
        for i in range(len(self.lobby_items)):
            reward_id = self.lobby_items[i]
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            template_item = self.panel.list_award_choose.GetItem(i)
            if not template_item:
                continue
            init_tempate_reward(template_item.temp_reward, item_id, item_num)

    def _role_bond_sort_func(self, reward_list):

        def key_func(reward_id):
            from logic.gcommon.cdata.bond_config import get_unlock_role_id_of_bond_item
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_id, item_num = reward_conf['reward_list'][0]
            role_id = get_unlock_role_id_of_bond_item(item_id)
            has_role = global_data.player.has_permanent_item_by_no(role_id)
            item_count = global_data.player.get_item_num_by_no(item_id)
            return [
             0 if has_role else 1, item_count]

        after_reward_list = sorted(reward_list, key=key_func, reverse=True)
        return after_reward_list

    def _role_bond_item_update_func(self, select_item_no):
        from logic.gutils import bond_utils
        role_id_list = bond_utils.get_roles_by_bond_item(select_item_no, 3)
        if not role_id_list:
            return
        item_count = global_data.player.get_item_num_by_no(select_item_no)
        cost_item = global_data.player.get_item_by_id(self.item_id)
        if self.ItemNumBtnWidget and cost_item:
            item_data = {'id': self.item_id,'quantity': cost_item.get_current_stack_num()
               }
            has_count = cost_item.get_current_stack_num()
            show_count = max(min(30 - item_count, has_count), 1)
            self.ItemNumBtnWidget.init_item(item_data, self.on_num_changed, init_quantity=show_count)