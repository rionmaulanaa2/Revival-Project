# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/RewardPreviewUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon.common_const import statistics_const as sconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gutils import template_utils

class RewardPreviewUI(BasePanel):
    PANEL_CONFIG_NAME = 'task/i_reward_preview'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    BORDER_INDENT = 24
    GLOBAL_EVENT = {'show_reward_preview_event': '_show_reward_preview',
       'close_reward_preview_event': '_close_reward_preview'
       }
    UI_ACTION_EVENT = {'panel.OnBegin': '_close_reward_preview'
       }

    def on_init_panel(self, *args, **kwargs):
        self.hide()

    def _show_reward_preview(self, reward_list, wpos):
        self.panel.list_reward.DeleteAllSubItem()
        for item_no, num in reward_list:
            nd_item = self.panel.list_reward.AddTemplateItem()
            template_utils.init_tempate_mall_i_item(nd_item.temp_reward, item_no, show_tips=True)
            contact_str = get_text_by_id(602012)
            nd_item.lab_reward.SetString(get_lobby_item_name(item_no) + contact_str + str(num))

        cur_screen_size = global_data.ui_mgr.design_screen_size
        w, h = self.panel.nd_reward.GetContentSize()
        fix_wpos_x = wpos.x
        fix_wpos_y = wpos.y
        if wpos.y > cur_screen_size.height - h / 2:
            fix_wpos_y = cur_screen_size.height - h / 2 - 10
        elif wpos.y < h:
            fix_wpos_y = h + 50
        if wpos.x < w / 2:
            fix_wpos_x = w / 2 + 10
        elif wpos.x > cur_screen_size.width - w / 2:
            fix_wpos_x = cur_screen_size.width - w / 2 - 10
        pos = self.panel.nd_reward.GetParent().convertToNodeSpace(cc.Vec2(fix_wpos_x, fix_wpos_y))
        self.panel.nd_reward.setPosition(pos.x, pos.y)
        self.show()

    def _close_reward_preview(self, *args):
        self.hide()

    def ui_vkb_custom_func(self):
        self.hide()