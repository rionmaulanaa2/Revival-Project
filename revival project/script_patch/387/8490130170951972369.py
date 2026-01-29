# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/deeplink_utils.py
from __future__ import absolute_import
import re
from logic.client.const import share_const
from logic.gutils.scene_utils import is_lobby_relatived_scene, is_in_lobby
import six
DEEP_LINK_JOIN_TEAM = share_const.DEEP_LINK_JOIN_TEAM
DEEP_LINK_ADD_FRIEND = share_const.DEEP_LINK_ADD_FRIEND
DEEP_LINK_RECRUIT = share_const.DEEP_LINK_RECRUIT
DEEP_LINK_GIVE_COINS = share_const.DEEP_LINK_GIVE_COINS
DEEP_LINK_JOIN_CUSTOMROOM = share_const.DEEP_LINK_JOIN_CUSTOMROOM
DEEP_LINK_CUSTOMROOM_OWNER_NAME = share_const.DEEP_LINK_CUSTOMROOM_OWNER_NAME
DEEP_LINK_CUSTOMROOM_ID = share_const.DEEP_LINK_CUSTOMROOM_ID
DEEP_LINK_CUSTOMROOM_TYPE = share_const.DEEP_LINK_CUSTOMROOM_TYPE
DEEP_LINK_CUSTOMROOM_NEED_PWD = share_const.DEEP_LINK_CUSTOMROOM_NEED_PWD
DEEPLINK_JUMP_TO_LOTTERY = share_const.DEEPLINK_JUMP_TO_LOTTERY
DEEPLINK_JUMP_TO_ACTIVITY = share_const.DEEPLINK_JUMP_TO_ACTIVITY
DEEPLINK_JUMP_TO_MALL = share_const.DEEPLINK_JUMP_TO_MALL
IOS_SCHEME_DEEPLINK_PARAMS = {}

def fetch_ios_scheme_deeplink_param():
    global IOS_SCHEME_DEEPLINK_PARAMS
    ios_scheme_deeplink = global_data.channel.get_prop_str('ios_scheme_deeplink')
    if not ios_scheme_deeplink:
        return
    global_data.channel.set_prop_str('ios_scheme_deeplink', '')
    deep_link_params_dict = parse_ios_scheme_deeplink(ios_scheme_deeplink)
    for k in deep_link_params_dict:
        v = deep_link_params_dict[k]
        IOS_SCHEME_DEEPLINK_PARAMS[k] = v


def parse_ios_scheme_deeplink(ios_scheme_deeplink_str):
    if not ios_scheme_deeplink_str:
        return {}
    import six.moves.urllib.parse
    query = six.moves.urllib.parse.urlparse(ios_scheme_deeplink_str).query
    return {k:v for k, v in six.moves.urllib.parse.parse_qsl(query)}


def get_deep_link_param(key):
    if key in IOS_SCHEME_DEEPLINK_PARAMS:
        return IOS_SCHEME_DEEPLINK_PARAMS[key]
    return global_data.channel.get_prop_str(key)


def reset_deep_link_param--- This code section failed: ---

  60       0  LOAD_FAST             0  'key'
           3  LOAD_GLOBAL           0  'IOS_SCHEME_DEEPLINK_PARAMS'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    23  'to 23'

  61      12  LOAD_GLOBAL           0  'IOS_SCHEME_DEEPLINK_PARAMS'
          15  LOAD_FAST             0  'key'
          18  DELETE_SUBSCR    

  62      19  LOAD_CONST            0  ''
          22  RETURN_END_IF    
        23_0  COME_FROM                '9'

  64      23  LOAD_GLOBAL           1  'global_data'
          26  LOAD_ATTR             2  'channel'
          29  LOAD_ATTR             3  'set_prop_str'
          32  LOAD_ATTR             1  'global_data'
          35  CALL_FUNCTION_2       2 
          38  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 35


def on_deep_link():
    from logic.gutils.salog import SALog
    if not global_data.player or not global_data.game_mgr:
        return
    else:
        cur_scene = global_data.game_mgr.scene
        if not is_in_lobby(cur_scene.scene_type):
            return
        fetch_ios_scheme_deeplink_param()
        salog_writer = SALog.get_instance()
        team_id = get_deep_link_param(DEEP_LINK_JOIN_TEAM)
        if team_id:
            reset_deep_link_param(DEEP_LINK_JOIN_TEAM)
            try:
                group = team_id.split('_')
                team_id = int(group[0])
                if len(group) > 1 and group[1] == 'linegame':
                    salog_writer.write(SALog.LINE_FOLLOW_INVITE, {'invite_role_id': team_id,'invite_type': DEEP_LINK_JOIN_TEAM})
            except:
                return

            if not G_IS_NA_USER:
                if team_id:
                    team_id += global_data.uid_prefix
            if team_id and team_id != global_data.player.uid:
                from common.platform.dctool import interface
                global_data.player.apply_join_team(team_id, need_confirm=interface.is_mainland_package())
        player_id = get_deep_link_param(DEEP_LINK_GIVE_COINS)
        if player_id:
            reset_deep_link_param(DEEP_LINK_GIVE_COINS)
            try:
                group = player_id.split('_')
                player_id = int(group[0])
                if len(group) > 1 and group[1] == 'linegame':
                    salog_writer.write(SALog.LINE_FOLLOW_INVITE, {'invite_role_id': player_id,'invite_type': DEEP_LINK_GIVE_COINS})
            except:
                pass

        room_id = get_deep_link_param(DEEP_LINK_CUSTOMROOM_ID)
        room_type = get_deep_link_param(DEEP_LINK_CUSTOMROOM_TYPE)
        need_pwd = get_deep_link_param(DEEP_LINK_CUSTOMROOM_NEED_PWD)
        if room_id and room_type:
            reset_deep_link_param(DEEP_LINK_JOIN_CUSTOMROOM)
            reset_deep_link_param(DEEP_LINK_CUSTOMROOM_TYPE)
            reset_deep_link_param(DEEP_LINK_CUSTOMROOM_NEED_PWD)
            try:
                room_id = int(room_id)
                room_type = int(room_type)
                if int(need_pwd) == 0:
                    global_data.player.req_enter_room(room_id, room_type, '')
                elif int(need_pwd) == 1:
                    from logic.comsys.room.RoomPasswordUI import RoomPasswordUI

                    def request_pwd(password=''):
                        global_data.player.req_enter_room(room_id, room_type, password)

                    RoomPasswordUI(None, confirm_cb=request_pwd, need_pwd=True, place_holder=get_text_by_id(19316))
            except:
                pass

        lottery_id = get_deep_link_param(DEEPLINK_JUMP_TO_LOTTERY)

        def on_player_check_advance(cb):
            if global_data.player:
                if not global_data.player.has_advance_list():
                    cb()
                else:
                    global_data.player.add_advance_finish_func(cb)
            else:
                log_error('failed to run deep link', IOS_SCHEME_DEEPLINK_PARAMS)

        if lottery_id:

            def run_lottery():
                reset_deep_link_param(DEEPLINK_JUMP_TO_LOTTERY)
                reset_deep_link_param(DEEPLINK_JUMP_TO_LOTTERY)
                from logic.gutils.jump_to_ui_utils import jump_to_lottery
                global_data.game_mgr.next_exec(lambda : jump_to_lottery(str(lottery_id)))

            on_player_check_advance(run_lottery)
        return


TEMP_CLIPBOARD_TEXT = ''

def check_clipboard_text():
    global TEMP_CLIPBOARD_TEXT
    from common.platform.dctool import interface
    import game3d
    if hasattr(game3d, 'get_clipboard_text_bin'):
        text_bin = game3d.get_clipboard_text_bin()
        try:
            text = six.ensure_str(text_bin)
        except:
            return

    else:
        try:
            text = game3d.get_clipboard_text()
        except:
            return

    TEMP_CLIPBOARD_TEXT = text
    if not global_data.player or not global_data.game_mgr:
        return
    if not text:
        return
    cur_scene = global_data.game_mgr.scene
    if not is_in_lobby(cur_scene.scene_type):
        if global_data.player.is_in_battle():
            game3d.set_clipboard_text('')
        return
    index = text.find(share_const.DEEP_LINK_JOIN_TEAM)
    if index != -1:
        team_id = text[index + 1 + len(share_const.DEEP_LINK_JOIN_TEAM):]
        try:
            team_id = int(team_id)
        except:
            return

        if team_id and team_id != global_data.player.uid:
            from common.platform.dctool import interface
            global_data.player.apply_join_team(team_id, need_confirm=interface.is_mainland_package())
    index = text.find(share_const.DEEP_LINK_ADD_FRIEND)
    if index != -1:
        player_id = text[index + 1 + len(share_const.DEEP_LINK_ADD_FRIEND):]
        try:
            player_id = int(player_id)
        except:
            return

        if not global_data.message_data.is_black_friend(str(player_id)) and not global_data.message_data.is_friend(str(player_id)):
            global_data.player.req_add_friend(player_id)
    game3d.set_clipboard_text('')