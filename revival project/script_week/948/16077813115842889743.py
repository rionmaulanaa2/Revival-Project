# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/custom_room_utils.py
from __future__ import absolute_import
import six
from logic.gcommon import const
from common.cfg import confmgr
RANDOM_MAP_TEXT_ID = 363

def is_in_judge_seat(seat_idx):
    if seat_idx is None:
        return False
    else:
        return const.OB_GROUP_ID_START <= seat_idx <= const.OB_SIT_INDEX_END


def is_competition(battle_type):
    battle_config = confmgr.get('battle_config')
    battle_info = battle_config.get(str(battle_type))
    if battle_info.get('iRoomNeededItem', None) is None:
        return False
    else:
        return True


def judgement_before_adjust_seat(uid, seat_index):
    room_ui = global_data.ui_mgr.get_ui('RoomUINew')
    if not room_ui:
        return
    room_ui.in_adjust_seat_state = True
    global_data.ui_mgr.close_ui('PlayerSimpleInf')
    global_data.player.judgement_before_adjust_seat(uid, seat_index)


def show_modify_name_dialog(target_uid):
    from logic.comsys.message.ChangeName import ChangeRoomPlayerName
    global_data.ui_mgr.close_ui('PlayerSimpleInf')
    ChangeRoomPlayerName(target_uid=target_uid)


def show_modify_team_name_dialog(_team_idx):
    from logic.comsys.message.ChangeName import ChangeRoomTeamName
    ChangeRoomTeamName(team_idx=_team_idx)


def on_click_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func, is_competition_room, self_seat_idx):
    if is_competition_room:
        on_click_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func, self_seat_idx)
    else:
        on_click_non_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func)


def on_click_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func, self_seat_idx):
    room_ui = global_data.ui_mgr.get_ui('RoomUINew')
    if not room_ui:
        return
    in_adjust_seat_state = room_ui.in_adjust_seat_state
    room_ui.in_adjust_seat_state = False
    if not is_in_judge_seat(self_seat_idx):
        on_click_non_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func)
    elif in_adjust_seat_state:
        player_id = player_id or -1 if 1 else player_id
        global_data.player.judgement_do_adjust_seat(player_id, seat_idx)
    else:
        on_click_non_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func)


def on_click_non_competition_temp_head(player_id, seat_ui, seat_idx, show_player_brief_func):
    if player_id:
        show_player_brief_func(seat_ui, player_id, seat_idx)
    else:
        global_data.player.req_sit_down(global_data.player.uid, seat_idx)


def get_room_layout_cls(class_name):
    class_module = __import__('logic.comsys.room.%s' % class_name, globals(), locals(), [class_name])
    layout_class = getattr(class_module, class_name, None)
    return layout_class


g_competition_room_ids = None

def load_competition_room_ids():
    global g_competition_room_ids
    import six
    import logic.gcommon.item.item_const as iconst
    g_competition_room_ids = []
    battle_config = confmgr.get('battle_config')
    for battle_type, battle_info in six.iteritems(battle_config):
        if battle_info.get('iRoomNeededItem', None) == iconst.ITEM_NO_ROOM_COMPETITION_CARD:
            g_competition_room_ids.append(int(battle_type))

    return


def get_competition_room_ids():
    if not g_competition_room_ids:
        load_competition_room_ids()
    return g_competition_room_ids


def get_custom_faction_config(battle_type):
    battle_info = confmgr.get('battle_config', default={}).get(str(battle_type), {})
    origin_custom_faction_config = battle_info.get('custom_faction_config', {})
    custom_faction_config = {}
    for faction_id, faction_text_id in six.iteritems(origin_custom_faction_config):
        custom_faction_config[int(faction_id)] = faction_text_id

    return custom_faction_config