# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPositionChecker.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
from time import time
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
from ...cdata.status_config import ST_SWIM
from collision import INCLUDE_FILTER, EQUAL_FILTER
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, TERRAIN_GROUP, LAND_GROUP
Y_MODIFY_OFFSET = 3

class ComPositionChecker(UnitCom):
    BIND_EVENT = {'E_POSITION': '_check_pos',
       'E_ACTION_SYNC_RB_POS': '_reset_invalid_state'
       }

    def __init__(self):
        super(ComPositionChecker, self).__init__()
        self._cnt_invalid = False
        self._invalid_checking = False
        self._checking_phase = 0
        self._checking_matrix = None
        self._error_result = []
        self._error_model_list = []
        self._check_interval = 0.5
        self._last_check_time = 0
        self._last_valid_pos = None
        self._default_ll_pos = [-350 * NEOX_UNIT_SCALE, -600 * NEOX_UNIT_SCALE]
        self._default_ru_pos = [480 * NEOX_UNIT_SCALE, 390 * NEOX_UNIT_SCALE]
        self._polygon_check_pos = []
        self._repeat_pos_times = 0
        self._last_move_time = 0
        global_data.emgr.battle_new_round += self._on_battle_new_round
        return

    def update_from_config_data(self):
        battle = self.unit_obj.get_battle()
        move_range = battle.get_move_range()
        if move_range:
            if len(move_range) == 2:
                self._min_x = min(move_range[0][0], move_range[1][0])
                self._max_x = max(move_range[0][0], move_range[1][0])
                self._min_z = min(move_range[0][1], move_range[1][1])
                self._max_z = max(move_range[0][1], move_range[1][1])
            else:
                self._min_x = 100000
                self._min_z = 100000
                self._max_x = -100000
                self._max_z = -100000
                self._polygon_check_pos = move_range
                for idx in range(len(self._polygon_check_pos)):
                    check_pos = self._polygon_check_pos[idx]
                    if check_pos[0] > self._max_x:
                        self._max_x = check_pos[0]
                    if check_pos[0] < self._min_x:
                        self._min_x = check_pos[0]
                    if check_pos[1] > self._max_z:
                        self._max_z = check_pos[1]
                    if check_pos[1] < self._min_z:
                        self._min_z = check_pos[1]

        else:
            from common.cfg import confmgr
            map_id = battle.map_id
            conf = confmgr.get('map_config', str(map_id), default={})
            l_pos = conf.get('walkLowerLeftPos', self._default_ll_pos)
            r_pos = conf.get('walkUpRightPos', self._default_ru_pos)
            self._min_x = l_pos[0]
            self._max_x = r_pos[0]
            self._min_z = l_pos[1]
            self._max_z = r_pos[1]

    def _reset_invalid_state(self, *args):
        self._cnt_invalid = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComPositionChecker, self).init_from_dict(unit_obj, bdict)
        self.update_from_config_data()
        self.need_update = True
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._check_pos, 0.2)

    def tick(self, dt):
        if not self.scene:
            return
        cnt_time = time()
        if self._cnt_invalid:
            return
        if self._invalid_checking or cnt_time - self._last_check_time > self._check_interval:
            cam_player = global_data.cam_lplayer
            if cam_player and (cam_player == self.unit_obj or self.sd.ref_driver_id == cam_player.id) and cam_player.ev_g_is_avatar():
                if not self._invalid_checking:
                    self._invalid_checking = True
                    self._last_check_time = cnt_time
                    self._checking_phase = 0
                    from random import randint
                    self._checking_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(randint(0, 360), randint(0, 360), randint(0, 360))))
                position = self.ev_g_position()
                if position:
                    char = self.sd.ref_character
                    if char:
                        position.y = position.y + char.getHeight()
                    self.check_invalid_pos(math3d.vector(position), self._checking_phase)
                self._checking_phase += 1
                if self._checking_phase == 6:
                    self._invalid_checking = False
                    self.analyze_checking_result()
        if global_data.game_time - self._last_move_time > 1.0:
            position = self.ev_g_position()
            if position:
                self._check_pos(position)

    def analyze_checking_result(self):
        if len(self._error_result) >= 6 and not self._cnt_invalid:
            from logic.comsys.control_ui.GMHelperUIFactory import GMHelperUIFactory
            self._cnt_invalid = True
            GMHelperUIFactory.create_gm_helper_ui()
        self._error_result = []
        self._error_model_list = []
        return True

    def check_invalid_pos(self, position, phase):
        pos_valid = self.check_in_building(position, phase) and self.check_under_terrain(position)
        if not pos_valid:
            self._error_result.append(pos_valid)

    def check_in_building(self, position, phase):
        return True
        start_pos = position
        end_pos = math3d.vector(start_pos)
        if phase % 2 == 0:
            offset = 10000 if 1 else -10000
            if phase in (0, 1):
                end_pos.x = end_pos.x + offset
            elif phase in (2, 3):
                end_pos.z = end_pos.z + offset
            elif phase in (4, 5):
                end_pos.y = end_pos.y + offset
            direction = end_pos - start_pos
            direction = direction * self._checking_matrix
            end_pos = start_pos + direction
            scene_col = self.scene.scene_col
            col_result = scene_col.hit_by_ray(start_pos, end_pos, 0, GROUP_STATIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT, INCLUDE_FILTER, False)
            col_result[0] or self._error_model_list.append(None)
            return True
        else:
            model = col_result[-1].model
            if model and model.valid:
                result = model.hit_by_ray(start_pos, direction, True, True)
                self._error_model_list.append(model.filename)
                if result[0]:
                    sub = result[2]
                    tri = result[3]
                    result_normal_hit_by_ray = model.hit_by_ray(start_pos, direction, True)
                    normal = model.get_triangle_normal(sub, tri)
                    res_distance = (start_pos - (start_pos + (end_pos - start_pos) * result[1])).length
                    normal_result_valid = result_normal_hit_by_ray[0] and result_normal_hit_by_ray[2] == sub and tri == result_normal_hit_by_ray[3]
                    normal_result = normal.dot(col_result[2])
                    if result_normal_hit_by_ray[0]:
                        normal_distance = (start_pos - (start_pos + (end_pos - start_pos) * result_normal_hit_by_ray[1])).length
                        if normal_result <= -0.1:
                            normal_result_valid = normal_result_valid or normal_distance > res_distance
                        col_distance = (col_result[1] - start_pos).length
                        if col_distance - normal_distance > 100:
                            return False
                    return normal_result_valid or normal.dot(col_result[2]) >= -0.1
            else:
                self._error_model_list.append(None)
            return True

    def check_under_terrain(self, position):
        if position.y < -2000:
            return False
        if position.y > 0:
            return True
        if self.ev_g_char_waiting():
            return True
        return True

    def update_last_pos(self):
        if self._last_valid_pos:
            self._last_valid_pos.x = max(self._min_x, min(self._max_x, self._last_valid_pos.x))
            self._last_valid_pos.z = max(self._min_z, min(self._max_z, self._last_valid_pos.z))

    def _check_pos(self, pos):
        if self._polygon_check_pos:
            self._special_polygon_check(pos)
            return
        else:
            from logic.client.const import game_mode_const
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
                return
            self._last_move_time = global_data.game_time
            in_correct_area = self._min_x <= pos.x <= self._max_x and self._min_z <= pos.z <= self._max_z
            if not in_correct_area:
                if self.unit_obj.id == global_data.player.id or self.sd.ref_driver_id == global_data.player.id:
                    global_data.player.logic.send_event('E_SHOW_MESSAGE', get_text_local_content(18020))
                if self._last_valid_pos is None:
                    self._last_valid_pos = math3d.vector(pos)
                    self.update_last_pos()
                self.send_event('E_ON_POS_CHECK_INVALID')
                _pos = math3d.vector(pos)
                direction = self._last_valid_pos - _pos
                if not direction.is_zero:
                    direction.normalize()
                    y = self._last_valid_pos.y
                    self._last_valid_pos = self._last_valid_pos + direction * 10
                    self._last_valid_pos.y = y
                if self.ev_g_parachuting() or self.ev_g_is_parachute_stage_free_drop():
                    self._last_valid_pos = math3d.vector(pos)
                    self._last_valid_pos.x = max(self._min_x, min(self._max_x, pos.x))
                    self._last_valid_pos.z = max(self._min_z, min(self._max_z, pos.z))
                elif self.is_unit_obj_type('LAvatar') and not self.ev_g_get_state(ST_SWIM):
                    self._last_valid_pos.y += Y_MODIFY_OFFSET
                self.update_last_pos()
                self.send_event('E_FOOT_POSITION', self._last_valid_pos)
                if G_POS_CHANGE_MGR:
                    self.notify_pos_change(self._last_valid_pos, True)
                else:
                    self.send_event('E_POSITION', self._last_valid_pos)
            else:
                self._last_valid_pos = pos
                self.update_last_pos()
            return

    def _special_polygon_check(self, pos):
        is_out = 0
        min_dis = 1000000
        nearlist_pos = 0
        for idx in range(len(self._polygon_check_pos) - 1):
            cor_1 = self._polygon_check_pos[idx]
            cor_2 = self._polygon_check_pos[idx + 1]
            if cor_1[1] < pos.z and cor_2[1] >= pos.z or cor_1[1] >= pos.z and cor_2[1] < pos.z:
                num = cor_1[0] + (pos.z - cor_1[1]) * (cor_2[0] - cor_1[0]) / (cor_2[1] - cor_1[1])
                if num > pos.x:
                    is_out += 1
            dis = math3d.vector2(*cor_1) - math3d.vector2(pos.x, pos.z)
            if dis.length < min_dis:
                nearlist_pos = math3d.vector(cor_1[0], pos.y, cor_1[1])

        if is_out % 2 == 0:
            if self.unit_obj.id == global_data.player.id or self.sd.ref_driver_id == global_data.player.id:
                global_data.player.logic.send_event('E_SHOW_MESSAGE', get_text_local_content(18020))
            if self._last_valid_pos:
                self.send_event('E_ON_POS_CHECK_INVALID')
                _pos = math3d.vector(pos)
                direction = self._last_valid_pos - _pos
                if not direction.is_zero:
                    direction.normalize()
                    y = self._last_valid_pos.y
                    last_valid_pos = self._last_valid_pos + direction * 10
                    last_valid_pos.y = y
                self._repeat_pos_times += 1
                if self._repeat_pos_times > 3:
                    center_pos = math3d.vector(8817, 1000, -6179)
                    dir = center_pos - _pos
                    if not dir.is_zero:
                        dir.normalize()
                    if G_POS_CHANGE_MGR:
                        self.notify_pos_change(_pos + dir * 13, True)
                    else:
                        self.send_event('E_POSITION', last_valid_pos)
                    self._repeat_pos_times = 0
                    return
                self.send_event('E_FOOT_POSITION', last_valid_pos)
                if G_POS_CHANGE_MGR:
                    self.notify_pos_change(last_valid_pos, True)
                else:
                    self.send_event('E_POSITION', last_valid_pos)
            elif nearlist_pos != 0:
                self._last_valid_pos = nearlist_pos
        else:
            self._repeat_pos_times = 0
            self._last_valid_pos = pos

    def _on_battle_new_round(self, prev, now, mode):
        from logic.client.const import game_mode_const
        if mode != game_mode_const.GAME_MODE_IMPROVISE:
            return
        self.update_from_config_data()

    def destroy(self):
        global_data.ui_mgr.close_ui('GMHelperUI')
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._check_pos)
        global_data.emgr.battle_new_round -= self._on_battle_new_round
        super(ComPositionChecker, self).destroy()

    def output(self, content):
        if self.unit_obj.__class__.__name__ == 'LAvatar':
            print (
             '-----------------------------', content)