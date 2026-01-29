# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/MyTestUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item, get_lobby_item_usage, try_use_lobby_item
from common.cfg import confmgr
from logic.gcommon.item import item_sorter
from logic.gutils import mall_utils
from logic.gutils import item_utils
from data.season_update_config import MONEY_DICT
from common.const import uiconst

class MyTestUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/my_test'
    UI_ACTION_EVENT = {'btn_test.OnClick': 'on_click_test_btn'
       }
    UI_VKB_TYPE = uiconst.UI_TYPE_NORMAL

    def on_click_test_btn(self, *args):
        flag_id = global_data.death_battle_data.flag_ent_id
        flag = global_data.battle.get_entity(flag_id)
        if flag:
            flag.logic.send_event('E_TRY_DROP_FLAG')