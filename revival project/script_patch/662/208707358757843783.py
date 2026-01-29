# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAICollectLog.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import collision
import math
import math3d
import collision
import world
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_CAN_SHOOT
from logic.units import LPuppet, LMecha
from logic.client.const import game_mode_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_AUTO_AIM, GROUP_CAN_SHOOT, GROUP_SHOOTUNIT
from logic.gcommon.common_const import collision_const
from common.utils.timer import CLOCK
RAY_NUM = 18
PER_RAY_NUM = ((0, 4), (5, 9), (10, 14), (15, 17))
CHESS_BOARD_RADIUS = 1
CHESS_INTERVAL = 3

class ComAICollectLog(UnitCom):
    BIND_EVENT = {'E_FIRE': '_on_record_fire',
       'E_RECORD_FIRE': '_on_record_fire',
       'E_RECORD_SUB_FIRE': '_on_record_sub_fire',
       'E_JUMP': '_on_record_jump',
       'E_CTRL_ROLL': 'on_roll',
       'E_DO_NOTIFIED_AI_LOG_COLLECT': '_notified_collect'
       }

    def __init__(self):
        super(ComAICollectLog, self).__init__()
        self.need_update = False
        self._ray_num = RAY_NUM
        self._chessboard_radius = CHESS_BOARD_RADIUS
        self._chess_interval = CHESS_INTERVAL
        self._per_angle = 360 / RAY_NUM
        self._max_check_distance = 200 * NEOX_UNIT_SCALE
        self._ailog_tick_time = 0
        self._sync_collect_time = 0
        self._ray_idx = 0
        self._ray_pos = None
        self._collectlog_timer_id = None
        self._chessboard_offsets = self._gen_chesssboard_cor_offset()
        self._around_angle_to_vector = self._get_around_angle_to_vector()
        self._ray_distance = {}
        self._last_seen_time = {}
        bat = global_data.battle
        self.is_duel = bat and hasattr(bat, 'is_duel_player')
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAICollectLog, self).init_from_dict(unit_obj, bdict)
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATH):
            return

    def destroy(self):
        super(ComAICollectLog, self).destroy()

    def _notified_collect(self, step):
        self._send_collect_info('around', self.get_ailog_collect_info())
        self.send_event('E_CALL_SYNC_METHOD', 'sync_do_ailog_pack_upload', (step,))

    def _send_collect_info(self, act, args):
        self.send_event('E_CALL_SYNC_METHOD', 'sync_ailog_collect', (act, args))

    def _record_ray_distance(self):
        if self._ray_idx == 0 or not self._ray_pos:
            self._ray_pos = global_data.player.logic.ev_g_position()
        idx_start, idx_end = PER_RAY_NUM[self._ray_idx]
        for i in range(idx_start, idx_end + 1):
            angle = i * self._per_angle
            around_forward = self._around_angle_to_vector[angle]
            res = global_data.game_mgr.scene.scene_col.hit_by_ray(self._ray_pos, self._ray_pos + around_forward * 100000, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
            if res[0]:
                hit_pos = res[1]
                dis = (self._ray_pos - hit_pos).length
            else:
                dis = -1
            self._ray_distance[angle] = dis

    def _env_ray_distance(self):
        dis_dict = {'chess_interval': self._chess_interval,
           'around_distance': self._around_ray_distance(),
           'up_distance': self._up_ray_distance()
           }
        return dis_dict

    def _up_ray_distance(self):
        dis_dict = {}
        if not global_data.player or not global_data.player.logic:
            return dis_dict
        self_pos = global_data.player.logic.ev_g_position()
        if not self_pos:
            return dis_dict
        for offset_loc, offset in six.iteritems(self._chessboard_offsets):
            down_pos = self_pos + offset
            up_pos = self_pos + offset
            down_pos.y -= 100000
            up_pos.y += 100000
            res = global_data.game_mgr.scene.scene_col.hit_by_ray(up_pos, down_pos, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
            if res[0]:
                hit_pos = res[1]
                dis = hit_pos.y - self_pos.y
            else:
                dis = -9999
            dis_dict[offset_loc] = dis

        return dis_dict

    def _around_ray_distance(self):
        dis_dict = {}
        if not global_data.player or not global_data.player.logic:
            return dis_dict
        self_pos = global_data.player.logic.ev_g_position()
        if not self_pos:
            return dis_dict
        player_col_ids = self.ev_g_human_col_id()
        for angle, around_forward in six.iteritems(self._around_angle_to_vector):
            res = global_data.game_mgr.scene.scene_col.hit_by_ray(self_pos, self_pos + around_forward * 100000, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
            if res[0]:
                hit_pos = res[1]
                dis = (self_pos - hit_pos).length
            else:
                dis = -1
            dis_dict[str(angle)] = dis

        return dis_dict

    def get_camera(self):
        return world.get_active_scene().active_camera

    def _on_record_jump(self, *args):
        self._send_collect_info('jump', None)
        return

    def on_roll(self, *args):
        self._send_collect_info('roll', None)
        return

    def get_ailog_collect_info(self):
        info = {'ray_distance': self._env_ray_distance(),
           'see_info': self._find_all_can_see_target(),
           'lst_see_time': self._last_seen_time
           }
        return info

    def _get_around_angle_to_vector(self):
        angle_to_radian = {}
        for i in range(self._ray_num):
            angle = i * self._per_angle
            a = angle * math.pi / 180
            fx = math.cos(a)
            fz = math.sin(a)
            angle_to_radian[angle] = math3d.vector(fx, 0, fz)

        return angle_to_radian

    def _gen_chesssboard_cor_offset(self):
        chess_interval = self._chess_interval * NEOX_UNIT_SCALE
        offsets = {}
        for x in range(-self._chessboard_radius, self._chessboard_radius + 1):
            for z in range(-self._chessboard_radius, self._chessboard_radius + 1):
                offsets[str(x) + ':' + str(z)] = math3d.vector(x * chess_interval, 0, z * chess_interval)

        return offsets

    def _on_record_fire(self, *arg, **kwargs):
        target_id, target_dist = self._get_forward_target_misty()
        if target_id:
            self._send_collect_info('fire', (target_id, target_dist))

    def _on_record_sub_fire(self, *arg, **kwargs):
        target_id, target_dist = self._get_forward_target_misty()
        if target_id:
            self._send_collect_info('subfire', (target_id, target_dist))

    def _get_forward_target_misty(self):
        import math
        import math3d
        scn = global_data.game_mgr.get_cur_scene()
        if not scn:
            return (None, None)
        else:
            all_puppets = global_data.war_noteam_puppets
            if not all_puppets:
                return (None, None)
            camera = scn.active_camera
            camera_matrix = camera.world_rotation_matrix
            camera_pos = camera.world_position
            camera_forward = camera_matrix.forward
            target_id = None
            target_dist = 999999
            for puppet in six.itervalues(all_puppets):
                puppet_pos = puppet.ev_g_position()
                if not puppet_pos:
                    continue
                puppet_dir = puppet_pos - camera_pos
                shoot_dir = math3d.vector(camera_forward)
                puppet_dir.normalize()
                shoot_dir.normalize()
                cos_value = puppet_dir.dot(shoot_dir)
                dist = (camera_pos - puppet_pos).length
                dis_offset = 104
                valid_angle = math.atan(dis_offset / dist)
                valid_cos_value = math.cos(valid_angle)
                if cos_value >= valid_cos_value and dist < target_dist:
                    target_dist = dist
                    target_id = str(puppet.id)

            return (target_id, target_dist)

    def _get_forward_target(self):
        scn = self.scene
        if not scn:
            return (None, None, None, None, None)
        else:
            target_id = None
            pos = None
            speed = None
            is_mecha = None
            camera = scn.active_camera
            camera_matrix = camera.world_rotation_matrix
            camera_pos = camera.world_position
            camera_forward = camera_matrix.forward
            res = scn.scene_col.hit_by_ray(camera_pos, camera_pos + camera_forward * 100000, 0, 65535, GROUP_SHOOTUNIT, collision.INCLUDE_FILTER, True)
            if res and res[0]:
                mecha_player = self.ev_g_ctrl_mecha_obj()
                player_col_ids = mecha_player.logic.ev_g_human_col_id() if mecha_player else self.ev_g_human_col_id()
                hit_info = res[1]
                for hit_res in hit_info:
                    cid = hit_res[4].cid
                    if cid in player_col_ids:
                        continue
                    res_cid = global_data.emgr.scene_find_unit_event.emit(cid)
                    if res_cid and res_cid[0] and isinstance(res_cid[0], (LPuppet.LPuppet, LMecha.LMecha)):
                        aim_target = res_cid[0]
                        if self.ev_g_is_groupmate(aim_target.id):
                            continue
                        target_id = str(aim_target.id)
                        pos = aim_target.ev_g_position()
                        speed = aim_target.ev_g_get_walk_direction()
                        is_mecha = False
                        if isinstance(res_cid[0], LMecha.LMecha):
                            mecha_driver = self.battle.get_entity(aim_target.ev_g_driver())
                            if mecha_driver:
                                is_mecha = True
                                target_id = str(mecha_driver.id)

            if target_id:
                return (target_id, self._change_vector_to_list(camera_forward), self._change_vector_to_list(pos), self._change_vector_to_list(speed), is_mecha)
            min_angle = None
            min_angle_id = None
            character_pos = None
            speed = None
            is_mecha = False
            camera_forward.normalize()
            for lpuppet in self.get_all_lpuppets():
                if not lpuppet:
                    continue
                if self.ev_g_is_groupmate(lpuppet.id):
                    continue
                mecha = lpuppet.ev_g_ctrl_mecha_obj()
                if mecha:
                    character_pos = mecha.logic.ev_g_aim_position() if 1 else lpuppet.ev_g_aim_position()
                    if not character_pos:
                        pass
                    continue
                speed = lpuppet.ev_g_get_walk_direction()
                obj_dir = character_pos - camera_pos
                obj_dir.normalize()
                angle = math.degrees(math.acos(obj_dir.dot(camera_forward)))
                if angle <= 10 and not min_angle or angle < min_angle:
                    min_angle = angle
                    min_angle_id = lpuppet.id
                    is_mecha = True if mecha else False

            if min_angle_id:
                return (str(min_angle_id), self._change_vector_to_list(camera_forward), self._change_vector_to_list(character_pos), self._change_vector_to_list(speed), is_mecha)
            return (
             None, self._change_vector_to_list(camera_forward), None, None, None)

    def _find_all_can_see_target(self):
        target_puppets_info = {}
        if not global_data.player:
            return target_puppets_info
        else:
            self_pos = global_data.player.logic.ev_g_position()
            if not self_pos:
                return target_puppets_info
            all_lpuppets = self.get_all_lpuppets()
            camera = self.get_camera()
            camera_pos = camera.position
            camera_forward = camera.world_rotation_matrix.forward
            scn = self.scene
            target = None
            for lpuppet in all_lpuppets:
                if not lpuppet:
                    continue
                if self.is_duel:
                    if self.ev_g_is_campmate(lpuppet.ev_g_camp_id()):
                        continue
                elif self.ev_g_is_groupmate(lpuppet.id):
                    continue
                mecha = lpuppet.ev_g_ctrl_mecha_obj()
                if mecha:
                    model = mecha.logic.ev_g_model() if 1 else lpuppet.ev_g_model()
                    if not (model and model.is_visible_in_this_frame()):
                        pass
                    continue
                character_pos = mecha.logic.ev_g_aim_position() if mecha else lpuppet.ev_g_aim_position()
                if self.is_enemy_can_hit(scn, camera_pos, camera_forward, lpuppet, character_pos):
                    target_puppets_info[str(lpuppet.id)] = (self_pos - character_pos).length
                    self._last_seen_time[str(lpuppet.id)] = tutil.time()

            return target_puppets_info

    def is_enemy_can_hit(self, scn, camera_pos, camera_forward, enemy, enemy_pos):
        pos_vector = enemy_pos - camera_pos
        if pos_vector.length > self._max_check_distance:
            return False
        else:
            mecha_enemy = enemy.ev_g_ctrl_mecha_obj()
            if mecha_enemy:
                enemy_col_id = mecha_enemy.logic.ev_g_human_col_id() if 1 else enemy.ev_g_human_col_id()
                return enemy_col_id or False
            enemy_col_id = enemy_col_id[0]
            res = scn.scene_col.hit_by_ray(camera_pos, enemy_pos, 0, 65535, GROUP_CAN_SHOOT, collision.INCLUDE_FILTER, True)
            if res and res[0]:
                mecha_player = self.ev_g_ctrl_mecha_obj()
                player_col_ids = mecha_player.logic.ev_g_human_col_id() if mecha_player else self.ev_g_human_col_id()
                hit_info = res[1]
                for hit_res in hit_info:
                    if hit_res[4].cid in player_col_ids:
                        continue
                    if hit_res[4].cid == enemy_col_id:
                        return True
                    return False

            return False

    def get_all_lpuppets(self):
        all_lpuppets = []
        bat = global_data.battle
        if self.is_duel and bat and bat.is_duel_player(self.unit_obj.id):
            puppet_id = bat.get_show_outline_player_id()
            if puppet_id:
                all_lpuppets = [
                 puppet_id]
        else:
            all_lpuppets = six_ex.values(global_data.war_puppets)
        return all_lpuppets

    def _change_vector_to_list(self, vector):
        if vector:
            return [vector.x, vector.y, vector.z]
        return vector