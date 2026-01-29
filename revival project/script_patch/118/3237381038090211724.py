# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartJudge.py
from __future__ import absolute_import
import six_ex
from . import ScenePart
from logic.gutils.entity_info_cache_utils import EntityInfoCache
from logic.gutils.team_utils import is_judge_group
from mobile.common.EntityManager import EntityManager

class PlayerInfoCache(EntityInfoCache):
    CONCERNS_VAL = {'G_DEATH': (
                 'death', True),
       'G_GROUP_ID': ('group', -1),
       'G_CHAR_NAME': ('char_name', '')
       }

    def __init__(self):
        super(PlayerInfoCache, self).__init__()
        self.cur_teams = {}
        global_data.is_judge_ob = judge_utils.is_ob()
        global_data.judge_need_hide_details = False

    def init_from_other_dict(self, player_info, team_info):
        import copy
        if self._entity_info:
            log_error('There are already team info in PlayerInfoCache!')
            return
        self._entity_info = copy.deepcopy(player_info)
        self.cur_teams = copy.deepcopy(team_info)
        for ent_id in self._entity_info:
            ent = EntityManager.getentity(ent_id)
            if ent and ent.logic:
                self.bind_player_event(ent.logic)

    def on_add_player(self, lplayer):
        super(PlayerInfoCache, self).on_add_player(lplayer)
        if lplayer.id in self._entity_info:
            group_id = self._entity_info[lplayer.id].get('group')
            if group_id is not None and not is_judge_group(group_id) and group_id > 0:
                if group_id not in self.cur_teams:
                    self.cur_teams[group_id] = lplayer.ev_g_groupmate()
        return

    def on_before_del_player(self, ent_id, ent_info):
        group_id = ent_info.get('group')
        if group_id in self.cur_teams:
            pids = self.cur_teams[group_id]
            if ent_id in pids:
                pids.remove(ent_id)

    def destroy(self):
        super(PlayerInfoCache, self).destroy()
        self.cur_teams = {}

    def get_team_info(self, group_id):
        return self.cur_teams.get(group_id, tuple())

    def get_all_team_info(self):
        return self.cur_teams


from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import judge_utils
from common.utils.time_utils import get_time

class PartJudge(ScenePart.ScenePart):
    ENTER_EVENT = {'start_judge_scene_part': '_start_judge',
       'net_disconnect_event': '_on_net_disconnect',
       'judge_ob_destroy_all_entities': '_on_all_entities_destroyed'
       }

    def __init__(self, scene, name):
        super(PartJudge, self).__init__(scene, name)
        self._all_player_info_cache = self._new_cache()
        self._cur_observe_target = None
        self._is_running_judge_logic = False
        self._nearby_distance = 200
        self._check_distance_interval = 1
        self._prev_check_distance_time = 0
        self._nearby_player_info = set()
        self._in_nearby_record_cache = {}
        self._perspective_enabled = False
        self._unit_ids_i_changed_perspective = set()
        self._check_group_status_interval = 1
        self._prev_check_group_status_time = 0
        self._is_started = False
        self._tmp_to_del_set = set()
        return

    def _new_cache(self):
        cache = PlayerInfoCache()
        cache.regist_bind_event('E_DEATH', self._on_player_dead)
        cache.regist_bind_event('E_ON_CONTROL_TARGET_CHANGE_EX', self._on_player_change_ct)
        return cache

    def _start_judge(self):
        if self._is_started:
            return
        self._is_started = True
        all_player = self._get_all_players()
        for entityId, player in six_ex.items(all_player):
            if player and player.logic and not player.logic.ev_g_death():
                self._all_player_info_cache.add_player(player.id)

        if global_data.is_pc_mode:
            from logic.comsys.observe_ui.JudgeObserveUINewPC import JudgeObserveUINewPC
            JudgeObserveUINewPC()
        else:
            from logic.comsys.observe_ui.JudgeObserveUINew import JudgeObserveUINew
            JudgeObserveUINew()
        self._is_running_judge_logic = True
        global_data.emgr.on_player_inited_event += self._on_add_player
        global_data.emgr.scene_observed_player_setted_event += self._on_enter_observe
        global_data.emgr.scene_cam_observe_player_setted += self._on_scene_cam_observe_player_setted
        self.need_update = True

    def _on_net_disconnect(self):
        self._all_player_info_cache.destroy()
        self._all_player_info_cache = self._new_cache()
        self._cur_observe_target = None
        self._prev_check_distance_time = 0
        self._nearby_player_info.clear()
        self._in_nearby_record_cache.clear()
        self._unit_ids_i_changed_perspective.clear()
        self._prev_check_group_status_time = 0
        return

    def _on_all_entities_destroyed(self):
        self._on_net_disconnect()

    def is_nearby(self, pid):
        if pid is None:
            return False
        else:
            return pid in self._nearby_player_info

    def get_readonly_nearby_pids(self):
        return self._nearby_player_info

    def is_perspective_enabled(self):
        return self._perspective_enabled

    def perspective_enabled(self, enable):
        self._perspective_enabled = enable
        for pid in self._nearby_player_info:
            self._change_player_perspective(pid, enable)

        return True

    def _get_logic(self, pid):
        ent = EntityManager.getentity(pid)
        if ent and ent.logic:
            return ent.logic
        else:
            return None

    def update_near_by_info(self, player_id):
        logic = self._get_logic(player_id)
        if not logic.get_owner():
            return None
        else:
            ct = logic.ev_g_control_target()
            if ct and ct.logic:
                position_unit = ct.logic
            else:
                position_unit = logic
            pos = position_unit.ev_g_position()
            if not pos:
                return None
            if not global_data.is_in_judge_camera:
                cam_target_pos = global_data.cam_lctarget.ev_g_position()
            else:
                camera = global_data.game_mgr.scene.active_camera
                cam_target_pos = camera.world_position
            if not cam_target_pos:
                return None
            dis = pos - cam_target_pos
            nearby = dis.length_sqr <= self._nearby_distance * self._nearby_distance * NEOX_UNIT_SCALE * NEOX_UNIT_SCALE
            self._update_nearby_cache(player_id, nearby)
            return nearby

    def on_update(self, dt):
        if get_time() - self._prev_check_distance_time >= self._check_distance_interval:
            all_player_info = self._all_player_info_cache.get_all_player_info()
            self._tmp_to_del_set.clear()
            if all_player_info and (global_data.cam_lctarget or global_data.is_in_judge_camera):
                for player_id in all_player_info:
                    logic = self._get_logic(player_id)
                    if not (logic and logic.is_valid()) or logic.ev_g_death():
                        self._tmp_to_del_set.add(player_id)
                        continue
                    self.update_near_by_info(player_id)

            if self._tmp_to_del_set:
                for player_id in self._tmp_to_del_set:
                    self._on_remove_player(player_id)

            self._prev_check_distance_time = get_time()
        if get_time() - self._prev_check_group_status_time >= self._check_group_status_interval:
            global_data.emgr.update_group_status_for_judge.emit()
            self._prev_check_group_status_time = get_time()

    def _update_nearby_cache(self, pid, nearby, erase=False):
        if erase:
            nearby = False
        if nearby is None:
            return
        else:
            if not erase:
                old = None
                if pid in self._in_nearby_record_cache:
                    old = self._in_nearby_record_cache[pid]
                self._in_nearby_record_cache[pid] = nearby
                changed = old != nearby
            elif pid in self._in_nearby_record_cache:
                del self._in_nearby_record_cache[pid]
                changed = True
            else:
                changed = False
            if changed:
                if nearby:
                    self._nearby_player_info.add(pid)
                elif pid in self._nearby_player_info:
                    self._nearby_player_info.remove(pid)
                if erase:
                    self._change_player_perspective(pid, False)
                elif self._perspective_enabled:
                    self._change_player_perspective(pid, nearby)
            return

    def _change_player_perspective(self, pid, enable):
        if pid is None:
            return
        else:
            if enable is None:
                return
            self._change_perspective_core(pid, enable)
            logic = self._get_logic(pid)
            if logic:
                ct = logic.ev_g_control_target()
                if ct and ct.logic and ct.logic.id != logic.id:
                    self._change_perspective_core(ct.logic.id, enable)
            return

    def _change_perspective_core(self, unit_id, enable):
        if unit_id is None:
            return
        else:
            if enable is None:
                return
            if enable and global_data.cam_lctarget is not None and global_data.cam_lctarget.id == unit_id:
                return
            logic = self._get_logic(unit_id)
            if logic:
                if enable:
                    logic.send_event('E_ENABLE_SEE_THROUGHT_FROM_OUTSIDE', 'ob_judge', True, priority=24)
                    self._unit_ids_i_changed_perspective.add(unit_id)
                else:
                    logic.send_event('E_ENABLE_SEE_THROUGHT_FROM_OUTSIDE', 'ob_judge', False)
                    if unit_id in self._unit_ids_i_changed_perspective:
                        self._unit_ids_i_changed_perspective.remove(unit_id)
            return

    def on_enter(self):
        if judge_utils.is_ob():
            self._start_judge()

    def on_exit(self):
        self._all_player_info_cache.destroy()
        if self._is_running_judge_logic:
            global_data.emgr.on_player_inited_event -= self._on_add_player
            global_data.emgr.scene_observed_player_setted_event -= self._on_enter_observe
            global_data.emgr.scene_cam_observe_player_setted -= self._on_scene_cam_observe_player_setted
        global_data.ui_mgr.close_ui('JudgeObserveUINew')
        self._cur_observe_target = None
        return

    def _on_add_player(self, lplayer):
        if not lplayer:
            return
        else:
            group_id = lplayer.ev_g_group_id()
            if group_id is not None and not is_judge_group(group_id) and group_id > 0:
                self._all_player_info_cache.add_player(lplayer.id)
                global_data.emgr.judge_cache_add_player.emit(lplayer.id)
            return

    def _get_all_players(self):
        all_player = EntityManager.get_entities_by_type('Puppet')
        return all_player

    def _on_remove_player(self, player_id):
        self._update_nearby_cache(player_id, False, erase=True)
        self._all_player_info_cache.del_player(player_id)

    def _on_player_dead(self, player_id, killer_id, *args):
        self._on_remove_player(player_id)
        global_data.emgr.judge_cache_player_dead.emit(player_id, killer_id)

    def _on_player_change_ct(self, player_id, otarget_id, target_id, position):
        if self._perspective_enabled:
            if self.is_nearby(player_id):
                if otarget_id is not None:
                    self._change_perspective_core(otarget_id, False)
                if target_id:
                    self._change_perspective_core(target_id, True)
        return

    def get_cur_battle_info(self):
        return (
         self._all_player_info_cache.get_all_player_info(), self._all_player_info_cache.get_all_team_info())

    def _on_enter_observe(self, target):
        self._cur_observe_target = target

    def _on_scene_cam_observe_player_setted(self):
        for unit_id in set(self._unit_ids_i_changed_perspective):
            self._change_perspective_core(unit_id, False)

        self._unit_ids_i_changed_perspective.clear()
        if self._perspective_enabled:
            for pid in self._nearby_player_info:
                if global_data.cam_lplayer and global_data.cam_lplayer.id == pid:
                    continue
                self._change_player_perspective(pid, True)