# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/PrivilegeWeekRewardPreviewUI.py
from __future__ import absolute_import
from .RewardPreviewUI import RewardPreviewUI
import common.const.uiconst
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils import template_utils

class PrivilegeWeekRewardPreviewUI(RewardPreviewUI):
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    GLOBAL_EVENT = {'show_priv_week_reward_preview_event': '_show_reward_preview',
       'close_reward_preview_event': '_close_reward_preview'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PrivilegeWeekRewardPreviewUI, self).on_init_panel()
        self.panel.lab_title.SetString(400392)

    def _show_reward_preview(self, reward_list, wpos):
        self.panel.list_reward.DeleteAllSubItem()
        for item_no, num in reward_list:
            nd_item = self.panel.list_reward.AddTemplateItem()
            template_utils.init_tempate_mall_i_item(nd_item.temp_reward, item_no, show_tips=False)
            contact_str = get_text_by_id(602012)
            nd_item.lab_reward.SetString(get_lobby_item_name(item_no) + contact_str + str(num))

        self.panel.setAnchorPoint(cc.Vec2(0.35, 0.21))
        pos = self.panel.GetParent().convertToNodeSpace(wpos)
        self.panel.setPosition(pos.x, pos.y)
        self.show()