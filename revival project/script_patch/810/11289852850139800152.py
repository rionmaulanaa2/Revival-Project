# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/group_proto.py
from __future__ import absolute_import
import six

def add_groupmates(synchronizer, groupmates_info):
    for tid, info in six.iteritems(groupmates_info):
        synchronizer.unit_obj.send_event('E_ADD_TEAMMATE', tid, info)


def begin_rescue(synchronizer, groupmate_id, left_time):
    if synchronizer._is_avatar:
        synchronizer.send_event('E_DO_RESCUE_SUCCESS', groupmate_id)


def stop_rescue(synchronizer, groupmate_id, reason):
    synchronizer.send_event('E_STOP_DO_RESCUE', groupmate_id, reason)


def draw_map_mark(synchronizer, mark_type, lst_map_pos, extra_args=None):
    if type(lst_map_pos) in (list, tuple) and len(lst_map_pos) == 3:
        import math3d
        v3d_map_pos = math3d.vector(*lst_map_pos)
    else:
        v3d_map_pos = None
    synchronizer.send_event('E_DRAW_MAP_SCENE_MARK', synchronizer.unit_obj.id, mark_type, v3d_map_pos, extra_args)
    return


def draw_ray_mark(synchronizer, mark_type, lst_map_pos):
    if type(lst_map_pos) in (list, tuple) and len(lst_map_pos) == 3:
        import math3d
        v3d_map_pos = math3d.vector(*lst_map_pos)
    else:
        v3d_map_pos = None
    synchronizer.send_event('E_DRAW_RAY_MARK', synchronizer.unit_obj.id, mark_type, v3d_map_pos)
    return


def clear_marks(synchronizer):
    synchronizer.send_event('E_CLEAR_SCENE_MARK')


def clear_one_mark(synchronizer, mark_class):
    synchronizer.send_event('E_CLEAR_ONE_SCENE_MARK', mark_class)


def draw_route(synchronizer, points):
    synchronizer.send_event('E_DRAW_MAP_ROUTE', synchronizer.unit_obj.id, points)


def battle_group_voice(synchronizer, voice):
    teamate_id = voice.get('teamate_id', None)
    voice_name = voice.get('voice_name', None)
    global_data.emgr.battle_group_voice.emit(teamate_id, voice_name)
    return


def sync_conn_state(synchronizer, conn_state):
    synchronizer.send_event('E_CONNECT_STATE', conn_state)


def del_groupmate(synchronizer, groupmate_id):
    synchronizer.send_event('E_DELETE_TEAMMATE', groupmate_id)


def update_member_info(synchronizer, member_id, info):
    synchronizer.send_event('E_UPDATE_TEAMMATE_INFO', member_id, info)


def set_camp(synchronizer, faction_id):
    synchronizer.send_event('E_SET_CAMP', faction_id)


def set_group_id(synchronizer, group_id):
    synchronizer.send_event('E_SET_GROUP_ID', group_id)


def invited_parachute(synchronizer, groupmate_id):
    if synchronizer.unit_obj.id == global_data.player.id or synchronizer.unit_obj.id == global_data.cam_lplayer.ev_g_player_id():
        synchronizer.send_event('E_PARACHUTE_FOLLOW_INVITED', groupmate_id)


def follow_parachute(synchronizer, groupmate_id, launch=False):
    synchronizer.send_event('E_SET_PARACHUTE_FOLLOW_TARGET', groupmate_id)


def follow_respond(synchronizer, groupmate_id, agree):
    if synchronizer.unit_obj.id == global_data.player.id or synchronizer.unit_obj.id == global_data.cam_lplayer.ev_g_player_id():
        synchronizer.send_event('E_SHOW_PARACHUTE_INVITE_RESPOND', groupmate_id, agree)


def switch_follow_parachute_mode(synchronizer, mode):
    synchronizer.send_event('E_SWITCH_PARACHUTE_FOLLOW_MODE', mode)


def on_request_tobe_parachute_leader(synchronizer, groupmate_id):
    if synchronizer.unit_obj.id == global_data.player.id or synchronizer.unit_obj.id == global_data.cam_lplayer.ev_g_player_id():
        synchronizer.send_event('E_ON_REQUEST_TRANSFER_LEADER', groupmate_id)


def respond_transfer_parachute_leader(synchronizer, groupmate_id, ret):
    if synchronizer.unit_obj.id == global_data.player.id or synchronizer.unit_obj.id == global_data.cam_lplayer.ev_g_player_id():
        synchronizer.send_event('E_RESPOND_TRANSFER_LEADER', groupmate_id, ret)