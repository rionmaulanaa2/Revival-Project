# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditDetailRuleUI.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_desc
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
FIRST_PAGE = 1
NEXT_PAGE = 2

class CreditDetailRuleUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/honor_details'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'nd_details.btn_switch.OnClick': '_switch_show'
       }

    def on_init_panel(self):
        super(CreditDetailRuleUI, self).on_init_panel()
        self._lv_items = []
        self._init_info()
        self._now_page = FIRST_PAGE
        self._show(self._now_page)

    def _show(self, page_num):
        vis = True if FIRST_PAGE == page_num else False
        for item in self._lv_items:
            item.nd_list1.setVisible(vis)
            item.nd_list2.setVisible(not vis)

        self.panel.nd_list1.setVisible(vis)
        self.panel.nd_list2.setVisible(not vis)

    def _switch_show(self, *args):
        self._now_page = NEXT_PAGE if self._now_page == FIRST_PAGE else FIRST_PAGE
        scale = 1 if self._now_page == FIRST_PAGE else -1
        self.panel.btn_switch.setScaleX(scale)
        self._show(self._now_page)

    def _init_info(self):
        credit_conf_dict = confmgr.get('credit_conf', 'CreditLevel', 'Content')
        level_lst = six_ex.keys(credit_conf_dict)
        level_lst.sort()
        for idx, lv in enumerate(level_lst):
            txt = {0: 80817,
               1: 900023
               }
            lv_conf = credit_conf_dict[lv]
            battle_desc = lv_conf.get('battle_desc', 10297)
            frame_reward = lv_conf.get('chat_frame_reward', 0)
            compensation = lv_conf.get('compensation', 0)
            rate = 100 - lv_conf.get('Rate', 100)
            point = lv_conf.get('Span', [0, 0])
            gift_reward = lv_conf.get('Reward', 0)
            item = self.panel.list_switch.AddTemplateItem()
            item.lab_lv.SetString(str(lv))
            if idx == len(level_lst) - 1:
                item.lab_point.SetString(str(point[0]))
            else:
                item.lab_point.SetString(str(point[0]) + '-' + str(point[1]))
            if rate == 0:
                item.lab_get.SetString(80817)
            else:
                item.lab_get.SetString('-%s%%' % rate)
            item.lab_mode.SetString(battle_desc)
            item.lab_compensate.SetString(txt[compensation])
            item.lab_reward.SetString(txt.get(gift_reward, 900023))
            item.lab_best_reward.SetString(txt[frame_reward])
            self._lv_items.append(item)

    def on_finalize_panel(self):
        self._lv_items = []
        self.set_custom_close_func(None)
        return