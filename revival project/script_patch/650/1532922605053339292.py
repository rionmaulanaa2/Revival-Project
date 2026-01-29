# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/judge_utils.py
from __future__ import absolute_import
import six_ex
from logic.gutils import yet_another_observe_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

def get_ob_target_id():
    return yet_another_observe_utils.get_ob_target_id()


def get_ob_target_unit():
    return yet_another_observe_utils.get_ob_target_unit()


def nb_get_player_info(pid):
    all_player_info = nb_get_all_player_info()
    return all_player_info.get(pid, {})


def nb_get_all_player_info():
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            player_info, team_info = part_judge.get_cur_battle_info()
            return player_info
    return {}


def nb_get_team_info(group_id):
    all_team_info = nb_get_all_team_info()
    return all_team_info.get(group_id, [])


def nb_get_all_team_info():
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            player_info, team_info = part_judge.get_cur_battle_info()
            return team_info
    return {}


def is_team_death(group_id):
    pids = get_global_team_info(group_id)
    for pid in pids:
        info = get_global_player_info(pid)
        if not info:
            continue
        is_dead_or_out = info.get('is_dead_or_out', False)
        if not is_dead_or_out:
            return False
    else:
        return True


def get_global_player_info(pid):
    all_player_info = get_all_global_player_info()
    pinfo = all_player_info.get(pid, {})
    from logic.gcommon.common_const import mecha_const as mconst
    ret = {'char_name': pinfo.get('role_name', ''),
       'is_dead_or_out': not pinfo.get('is_alive', True),
       'uid': pinfo.get('uid', 0),
       'group': pinfo.get('group_id', None),
       'position': pinfo.get('position', None),
       'yaw': pinfo.get('yaw', None),
       'in_mecha': pinfo.get('in_mecha', False),
       'mecha_id': pinfo.get('mecha_id', 0),
       'recall_cd_type': pinfo.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL),
       'recall_cd': pinfo.get('recall_cd', 0) / pinfo.get('recall_cd_rate', 1) if pinfo.get('recall_cd_rate', 0) > 0 else 0,
       'recall_cd_end_ts': pinfo.get('recall_cd_end_ts', 0),
       'in_mecha_type': pinfo.get('in_mecha_type', mconst.MECHA_TYPE_NONE)
       }
    return ret


def get_all_global_player_info():
    if global_data.player:
        return global_data.player.get_all_player_info_for_ob()
    return {}


def get_global_team_info(group_id):
    all_team_info = get_all_global_team_info()
    return all_team_info.get(group_id, [])


def get_all_global_team_info():
    if global_data.player:
        return global_data.player.get_all_team_info_for_ob()
    return {}


def is_player_dead_or_out(pid):
    info = get_global_player_info(pid)
    is_dead_or_out = info.get('is_dead_or_out', False)
    return is_dead_or_out


def is_perspective_enabled():
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            return part_judge.is_perspective_enabled()
    return False


def set_perspective_enabled(enabled):
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            return part_judge.perspective_enabled(enabled)
    return False


def is_obable_parachute_stage(stage):
    if stage is None:
        return False
    else:
        from logic.gcommon.common_utils import parachute_utils
        if parachute_utils.is_preparing(stage) or parachute_utils.is_sortie_stage(stage) or stage == parachute_utils.STAGE_FREE_DROP:
            return False
        return True
        return


def try_switch_ob_target(pid, uid=None):
    if not (global_data.player and global_data.player.logic):
        return
    else:
        if pid is None:
            return
        if uid is None:
            static_player_info = get_global_player_info(pid)
            if static_player_info:
                uid = static_player_info.get('uid', 0)
        if uid is None:
            if global_data.is_inner_server:
                pass
            return
        if pid == get_ob_target_id():
            return
        if global_data.is_in_judge_camera:
            if pid == global_data.player.logic.ev_g_spectate_target_id():
                global_data.emgr.try_switch_judge_camera_event.emit(False)
                return
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(pid)
        if ent and ent.logic:
            if ent.logic.ev_g_death():
                global_data.game_mgr.show_tip(get_text_by_id(18168))
                return
            stage = ent.logic.share_data.ref_parachute_stage
            if not is_obable_parachute_stage(stage):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19610))
                return
        else:
            info = get_global_player_info(pid)
            is_dead_or_out = info.get('is_dead_or_out', False)
            if is_dead_or_out:
                global_data.game_mgr.show_tip(get_text_by_id(18168))
                return
        if global_data.player:
            from mobile.common.IdManager import IdManager
            global_data.player.req_global_spectate_switch(IdManager.id2str(pid), uid)
        return


def is_nearby(pid):
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            return part_judge.is_nearby(pid)
    return False


def get_readonly_nearby_pids():
    scn = global_data.game_mgr.scene
    if scn:
        part_judge = scn.get_com('PartJudge')
        if part_judge:
            return part_judge.get_readonly_nearby_pids()
    return set()


def has_judges_in_battle():
    if global_data.player:
        battle = global_data.player.get_joining_battle() or global_data.player.get_battle()
        if battle:
            return battle.has_judges()
    return False


def is_player_mark_enabled():
    if not is_ob():
        return False
    ui_inst = global_data.ui_mgr.get_ui('ScopePlayerUI')
    if ui_inst and ui_inst.isPanelVisible():
        return True
    return False


def is_ob():
    if global_data.player and global_data.player.is_in_judge_ob():
        return True
    else:
        return False


def disable_execute_for_judge():

    def decorator(func):

        def wrapper(*args, **kwargs):
            if is_ob():
                return
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def is_in_competition_battle():
    from logic.gcommon.common_const.battle_const import DEFAULT_COMPETITION_TID_LIST
    in_competition = global_data.player and global_data.player.is_in_battle() and global_data.player.is_in_room() and global_data.player.room_info._room_info.get('battle_type') in DEFAULT_COMPETITION_TID_LIST
    return in_competition


def get_ob_nearest_team_in_direction(cur_teammate_id, direction):
    all_team_info = get_all_global_team_info()
    if not all_team_info:
        return
    else:
        target_id = None
        if global_data.cam_lplayer:
            center_pos = global_data.cam_lplayer.ev_g_position()
        else:
            camera = global_data.game_mgr.scene.active_camera
            center_pos = camera.world_position
        if not center_pos:
            return
        info = get_global_player_info(cur_teammate_id)
        cur_group_id = info.get('group')
        people_dis_dict = {}
        for group_id in all_team_info:
            if group_id == cur_group_id:
                continue
            pids = all_team_info[group_id]
            if not pids:
                continue
            if is_team_death(group_id):
                continue
            for pid in pids:
                pinfo = get_global_player_info(pid)
                pos = pinfo.get('position')
                if not pos:
                    continue
                dis = (pos - center_pos) * direction
                value = 1000000
                if dis.x != 0:
                    value = dis.x
                else:
                    value = dis.z
                two_point_dis = (pos - center_pos).length
                if value > 0:
                    people_dis_dict[pid] = (
                     two_point_dis, value)

        if not people_dis_dict:
            return
        target_pid = min(six_ex.keys(people_dis_dict), key=lambda k: people_dis_dict[k])
        return target_pid


def judge_switch_to_another_teammate(cur_teammate_id, direction):
    info = get_global_player_info(cur_teammate_id)
    group_id = info.get('group')
    pids = get_global_team_info(group_id)
    pids = sorted(pids)
    pids = [ p for p in pids if not is_player_dead_or_out(p) ]
    if cur_teammate_id not in pids:
        return None
    else:
        if len(pids) == 1:
            return None
        ind = pids.index(cur_teammate_id)
        ind += direction
        ind = ind % len(pids)
        return pids[ind]


def get_player_group_id():
    if is_ob():
        obed_unit = get_ob_target_unit()
    else:
        obed_unit = global_data.player and global_data.player.logic
    if obed_unit:
        return obed_unit.ev_g_group_id()