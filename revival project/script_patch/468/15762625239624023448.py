# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyInteractionUI.py
from __future__ import absolute_import
from logic.comsys.interaction.InteractionBaseUI import InteractionBaseUI
from logic.gutils import item_utils
from logic.gcommon.item import lobby_item_type
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gutils.interaction_utils import generate_lobby_spray_info
from logic.gutils import items_book_utils

class LobbyInteractionUI(InteractionBaseUI):
    DLG_ZORDER = DIALOG_LAYER_ZORDER

    def check_action_valid(self, idx):
        if idx < 0:
            return False
        player = global_data.player
        if not player:
            return False
        action_valid = idx in self.action_dict and self.action_dict[idx] != 0
        if not action_valid:
            return False
        role_id = global_data.player.get_role()
        item_no = self.action_dict[idx]
        belong_role_id_list = items_book_utils.get_interaction_belong_to_role(item_no, get_all=True)
        if belong_role_id_list:
            if int(role_id) not in belong_role_id_list:
                return False
        return True

    def try_action(self):
        if self.select_idx not in self.action_dict:
            return
        player = global_data.lobby_player
        if not player:
            return
        if self.enable_select and self.select_idx >= 0:
            item_no = self.action_dict[self.select_idx]
            item_type = item_utils.get_lobby_item_type(item_no)
            if lobby_item_type.L_ITEM_TYPE_SPRAY == item_type:
                lobby_spray_dict = generate_lobby_spray_info(item_no)
                if lobby_spray_dict:
                    global_data.player and global_data.player.on_try_spray(lobby_spray_dict)
            elif lobby_item_type.L_ITEM_TYPE_GESTURE == item_type:
                player.send_event('E_LOBBY_CELEBRATE', item_no, False)
                global_data.player and global_data.player.on_try_gesture(item_no)
            elif lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE == item_type:
                player.send_event('E_LOBBY_CELEBRATE', item_no, False)
                global_data.player and global_data.player.on_try_gesture(item_no)
            elif lobby_item_type.L_ITEM_TYPE_EMOTICON == item_type:
                player.send_event('E_EMOJI', item_no)
                global_data.player and global_data.player.on_try_emoji(item_no)
        self.hide()