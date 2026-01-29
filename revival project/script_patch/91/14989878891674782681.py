# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/GameDescRewardPreview.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon.common_const import statistics_const as sconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gutils import template_utils

class GameDescRewardPreview(BasePanel):
    PANEL_CONFIG_NAME = 'common/game_describe_reward_list'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    BORDER_INDENT = 24
    UI_ACTION_EVENT = {'panel.OnBegin': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        pass

    def show_reward_preview(self, title, reward_info, wpos):
        self.panel.list_content.DeleteAllSubItem()
        self.panel.lab_title.SetString(title)
        for text, reward_id in reward_info:
            nd_item = self.panel.list_content.AddTemplateItem()
            nd_item.lab.SetString(text)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            for item_no, item_num in reward_list:
                item_temp = nd_item.reward_item.AddTemplateItem()
                template_utils.init_tempate_mall_i_item(item_temp, item_no, show_rare_degree=True, show_tips=True)

        cur_screen_size = global_data.ui_mgr.design_screen_size
        w, h = self.panel.nd_game_describe.GetContentSize()
        if wpos.y > cur_screen_size.height:
            wpos.y = cur_screen_size.height - 10
        elif wpos.y < h:
            wpos.y = h + 10
        elif wpos.x < w / 2:
            wpos.x = w / 2 + 10
        elif wpos.x > cur_screen_size.width - w / 2:
            wpos.x = cur_screen_size.width - w / 2 - 10
        pos = self.panel.nd_game_describe.GetParent().convertToNodeSpace(wpos)
        self.panel.nd_game_describe.setPosition(pos.x, pos.y)

    def ui_vkb_custom_func(self):
        self.close()