# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/spray/SprayUI.py
from __future__ import absolute_import
from logic.comsys.interaction.InteractionBaseUI import InteractionBaseUI
from logic.gutils import item_utils
from logic.gcommon.item import lobby_item_type
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gutils import items_book_utils
OLD_MECHA_VEHICLE_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans'))

class SprayBaseUI(InteractionBaseUI):
    ENABLE_HOT_KEY_SUPPORT = True

    def check_action_valid(self, idx):
        if idx < 0:
            return False
        else:
            player = global_data.player
            if not (player and player.logic):
                return False
            action_valid = idx in self.action_dict and self.action_dict[idx] != 0
            if not action_valid:
                return False
            role_id = global_data.player.get_role()
            mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
            item_no = self.action_dict[idx]
            belong_role_id_list = items_book_utils.get_interaction_belong_to_role(item_no, get_all=True)
            if belong_role_id_list:
                if int(role_id) not in belong_role_id_list and mecha_id not in belong_role_id_list:
                    return False
            in_mecha = player.logic.ev_g_in_mecha()
            item_no = self.action_dict[idx]
            item_type = item_utils.get_lobby_item_type(item_no)
            if lobby_item_type.L_ITEM_TYPE_GESTURE == item_type:
                return not in_mecha
            if lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE == item_type:
                return in_mecha
            return True

    def try_action(self):
        if self.select_idx not in self.action_dict:
            return
        player_valid = global_data.player and global_data.player.logic
        if not player_valid:
            return
        player = global_data.player.logic
        if player.ev_g_death():
            return
        if self.enable_select and self.data_inited and self.select_idx >= 0:
            item_no = self.action_dict[self.select_idx]
            item_type = item_utils.get_lobby_item_type(item_no)
            player.send_event('E_CALL_SYNC_METHOD', 'use_action_item', (item_no,))
            control_target = player.ev_g_control_target()
            if lobby_item_type.L_ITEM_TYPE_SPRAY == item_type:
                player.send_event('E_SPRAY', item_no)
            elif lobby_item_type.L_ITEM_TYPE_EMOTICON == item_type:
                if control_target and control_target.logic.MASK & OLD_MECHA_VEHICLE_TAG_VALUE:
                    control_target.logic.send_event('E_ADD_EMOJI', item_no)
                else:
                    player.send_event('E_ADD_EMOJI', item_no)
            elif control_target and item_type in (lobby_item_type.L_ITEM_TYPE_GESTURE, lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE):
                control_target.logic.send_event('E_CELEBRATE', item_no)

    def on_hot_key_opened_state(self):
        super(SprayBaseUI, self).on_hot_key_opened_state()
        self.panel.nd_action_spray_close.setVisible(False)

    def on_hot_key_closed_state(self):
        super(SprayBaseUI, self).on_hot_key_closed_state()
        self.panel.nd_action_spray_close.setVisible(True)


class SprayUI(SprayBaseUI):
    pass