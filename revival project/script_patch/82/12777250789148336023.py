# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/SettleInteractionUI.py
from __future__ import absolute_import
from logic.comsys.interaction.InteractionBaseUI import InteractionBaseUI
from logic.gutils import item_utils
from logic.gcommon.item import lobby_item_type
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.interaction_utils import generate_lobby_spray_info
from logic.gutils import items_book_utils

class SettleInteractionUI(InteractionBaseUI):
    DLG_ZORDER = DIALOG_LAYER_ZORDER

    def check_action_valid(self, idx):
        if idx < 0:
            return False
        player = global_data.player
        if not player:
            return False
        if not (idx in self.action_dict and self.action_dict[idx] != 0):
            return False
        role_id = global_data.player.get_role()
        item_no = self.action_dict[idx]
        belong_role_id_list = items_book_utils.get_interaction_belong_to_role(item_no, get_all=True)
        if belong_role_id_list:
            if int(role_id) not in belong_role_id_list:
                return False
        item_no = self.action_dict[idx]
        item_type = item_utils.get_lobby_item_type(item_no)
        return item_type in (lobby_item_type.L_ITEM_TYPE_EMOTICON, lobby_item_type.L_ITEM_TYPE_GESTURE)

    def try_action(self):
        if self.select_idx not in self.action_dict:
            return
        player = global_data.player
        if not player:
            return
        if self.enable_select and self.select_idx >= 0:
            item_no = self.action_dict[self.select_idx]
            global_data.emgr.change_settle_role_interaction.emit(global_data.player.id, item_no)
            global_data.player.add_emoji_after_settle(item_no)