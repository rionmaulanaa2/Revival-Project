# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditRewardUI.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.item_utils import get_lobby_item_name
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class CreditRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/honor_reward'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'on_receive_credit_reward': '_receive_credit_reward'
       }

    def on_init_panel(self):
        super(CreditRewardUI, self).on_init_panel()
        self._lv_to_item = {}
        self._init_reward_st()

    def _init_reward_st(self):
        credit_conf_dict = confmgr.get('credit_conf', 'CreditLevel', 'Content')
        level_lst = six_ex.keys(credit_conf_dict)
        level_lst.sort()
        reward_info_lst = []
        for level in level_lst:
            reward_id = credit_conf_dict.get(str(level), {}).get('Reward', None)
            if reward_id:
                reward_info_lst.append((int(level), reward_id))

        self.panel.list_reward.DeleteAllSubItem()
        reward_sts = global_data.player or [] if 1 else global_data.player.get_credit_reward_sts()
        credit_level = global_data.player or 0 if 1 else global_data.player.get_credit_level()
        for lv, reward_id in reward_info_lst:
            item = self.panel.list_reward.AddTemplateItem()
            self._lv_to_item[lv] = item
            item.lab_level.SetString(get_text_by_id(900001) + 'Lv' + str(lv))
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            desc_txt = ''
            for lobby_item_no, num in reward_list:
                if num > 1:
                    desc_txt += get_lobby_item_name(lobby_item_no) + 'x{0}\n'.format(num)
                else:
                    desc_txt += get_lobby_item_name(lobby_item_no) + '\n'

            item.img_bar.lab_reward.SetString(desc_txt)
            if lv in reward_sts:
                item.img_got.setVisible(True)
                item.btn_get.setVisible(False)
            else:
                item.img_got.setVisible(False)
                item.btn_get.setVisible(True)
                if lv > credit_level:
                    item.btn_get.SetText(81173)
                    item.btn_get.SetEnable(False)
                else:
                    item.btn_get.SetText(606010)
                    item.nd_choose.setVisible(True)
                    item.red_point.setVisible(True)
                    item.btn_get.SetEnable(True)

                    @item.btn_get.unique_callback()
                    def OnClick(btn, touch, level=lv):
                        global_data.player.request_credit_reward(level)

        return

    def _receive_credit_reward(self, level):
        item = self._lv_to_item.get(level, None)
        if item is None:
            return
        else:
            item.img_got.setVisible(True)
            item.btn_get.setVisible(False)
            item.nd_choose.setVisible(False)
            item.red_point.setVisible(False)
            item.btn_get.SetEnable(False)
            return

    def on_finalize_panel(self):
        self._lv_to_item = {}
        self.set_custom_close_func(None)
        return