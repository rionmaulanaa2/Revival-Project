# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathBattleDoorCol.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, REGION_SCENE_GROUP, GROUP_GRENADE, TERRAIN_MASK, GROUP_CAMERA_COLL, GROUP_SHOOTUNIT
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.framework import Functor
from common.framework import Singleton
from common.utils import timer
import world
import math3d
import collision
import math
from logic.comsys.battle import BattleUtils
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
BORN_PART_SIZE_SFX = [
 'effect/fx/scenes/common/occupy/occupy_blue_02.sfx',
 'effect/fx/scenes/common/occupy/occupy_red_02.sfx']

class DeathBattleDoorCol(Singleton):
    ALIAS_NAME = 'death_battle_door_col'

    def init(self):
        self.init_parameters()
        self.process_event(True)
        self._is_ace_time = global_data.battle and global_data.battle.is_ace_time()

    def init_parameters(self):
        self._has_report_enter = False
        self.is_debug = False
        self._ready_col_obj = {}
        self._col_obj = {}
        self.born_part_effect = []
        self.set_trigger_timer = None
        self.is_in_trigger = False
        self.check_timer = None
        self.door_id_to_entity_id = {}
        self.group_to_door_id = {}
        self.buff_screen_sfx_id = None
        self.duration_factor_info = (None, 0)
        self._weak_doors = set()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_death_born_point': self.create_col,'app_resume_event': self.create_col,
           'death_door_weak_power_event': self.on_weak_power,
           'death_into_ace_stage_event': self.death_into_ace_stage_event
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize(self):
        self.process_event(False)
        self.clear_timer()
        self.remove_col()
        self.door_id_to_entity_id = {}
        self.group_to_door_id = {}

    def clear_timer(self):
        self.set_trigger_timer and global_data.game_mgr.get_logic_timer().unregister(self.set_trigger_timer)
        self.set_trigger_timer = None
        self.check_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_timer)
        self.check_timer = None
        return

    def is_game_over(self):
        if not global_data.game_mode.mode:
            return True
        return global_data.game_mode.mode.game_over

    def is_weak_door(self, door_id):
        return door_id in self._weak_doors

    def door_report(self, in_enemy_base, door_id):
        if self.is_game_over():
            global_data.ui_mgr.close_ui('DeathEnemyBaseUI')
            return
        ui = global_data.ui_mgr.get_ui('DeathEnemyBaseUI')
        if in_enemy_base:
            if not self._has_report_enter or not (ui and ui.isVisible()):
                if global_data.player:
                    self._has_report_enter = True
                    global_data.player.call_soul_method('report_enter', (self.door_id_to_entity_id.get(door_id),))
        elif self._has_report_enter or ui and ui.isVisible():
            if global_data.player:
                self._has_report_enter = False
                global_data.player.call_soul_method('report_leave', (self.door_id_to_entity_id.get(door_id),))

    def add_door_entity_id(self, door_id, entity_id):
        self.door_id_to_entity_id[door_id] = entity_id

    def get_door_col(self, door_id):
        return self._col_obj.get(door_id)

    def set_col_trigger(self):
        for door_id, col_info in six.iteritems(self._ready_col_obj):
            _, col, _ = col_info
            col.set_trigger(True)
            col.set_trigger_callback(Functor(self._trigger_cb, door_id))

    def _trigger_cb(self, *args):
        if self.is_game_over():
            global_data.ui_mgr.close_ui('DeathEnemyBaseUI')
            return
        door_id, trigger, col, is_in = args
        group_id, _, door_pos = self._ready_col_obj[door_id]
        if global_data.player and global_data.player.logic:
            character_col = global_data.player.logic.sd.ref_character
            if not character_col:
                mecha_id = global_data.player.logic.ev_g_ctrl_mecha()
                mecha = EntityManager.getentity(mecha_id)
                if mecha and mecha.logic:
                    character_col = mecha.logic.sd.ref_character
                if not character_col:
                    return
            is_my_group = self.get_player_group_id() == group_id
            if is_my_group:
                if not is_in and character_col.cid == col.cid:
                    if global_data.player.logic.ev_g_attr_get('death_mode_leave_base_firstly', True) and door_id and self.door_id_to_entity_id.get(door_id):
                        door_entity = EntityManager.getentity(self.door_id_to_entity_id.get(door_id))
                        if door_entity and door_entity.logic and not door_entity.logic.ev_g_is_door_destroyed():
                            door_entity.report_leave(global_data.player)
                    global_data.player.logic.send_event('S_ATTR_SET', 'death_mode_leave_base_firstly', False)
            else:
                born_dict = global_data.death_battle_data.born_data
                born_data = born_dict.get(group_id)
                if not born_data:
                    return
                _x, _y, _z, _r, _idx, _dict_info = born_data.data
                if not _dict_info or not _dict_info.get(door_id, False):
                    return
                if character_col.cid == col.cid:
                    self.is_in_trigger = bool(is_in)
                    if is_in:
                        if not self._has_report_enter:
                            if global_data.player:
                                self._has_report_enter = True
                                global_data.player.call_soul_method('report_enter', (self.door_id_to_entity_id.get(door_id),))

    def on_weak_power(self, data=None):
        if self.is_game_over():
            global_data.ui_mgr.close_ui('DeathEnemyBaseUI')
            return
        else:
            ui = global_data.ui_mgr.get_ui('DeathEnemyBaseUI')
            if not data:
                ui and ui.add_hide_count('death_door')
                self.clear_screen_sfx()
                return
            duration_factor = data.get('duration_factor')
            is_changeover = data.get('is_changeover', True)
            if duration_factor is None:
                ui and ui.add_hide_count('death_door')
                self.clear_screen_sfx()
                return
            ui = global_data.ui_mgr.show_ui('DeathEnemyBaseUI', 'logic.comsys.battle.Death')
            if not is_changeover:
                if ui:
                    ui.SetInfo(duration_factor)
                    ui.add_show_count('death_door')
            else:
                ui and ui.add_hide_count('death_door')
            self.duration_factor_info = (
             data.get('buff_id'), duration_factor)
            self.create_screen_sfx(data.get('buff_id'), duration_factor)
            return

    def create_screen_sfx(self, buff_id, duration_factor):
        if not buff_id:
            return
        if duration_factor > -0.1:
            self.clear_screen_sfx()
            return
        if not self._has_report_enter:
            ui = global_data.ui_mgr.show_ui('DeathEnemyBaseUI', 'logic.comsys.battle.Death')
            ui.add_hide_count('death_door')
            self.clear_screen_sfx()
            return
        if self.buff_screen_sfx_id:
            return
        from common.cfg import confmgr
        screen_sfx_path = confmgr.get('c_buff_data', str(buff_id), 'ExtInfo', 'screen_sfx', default='')
        if screen_sfx_path:
            size = global_data.really_sfx_window_size
            scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

            def create_callback(sfx, scale=scale):
                sfx.scale = scale

            self.buff_screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(screen_sfx_path, on_create_func=create_callback)

    def clear_screen_sfx(self):
        if self.buff_screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.buff_screen_sfx_id)
        self.buff_screen_sfx_id = None
        return

    def get_player_group_id(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_group_id()

    def create_col(self):
        self._is_ace_time = global_data.battle and global_data.battle.is_ace_time()
        if self._is_ace_time:
            self.death_into_ace_stage_event()
        self.remove_col()
        revive_time = BattleUtils.get_prepare_left_time()
        is_trigger = revive_time <= 0
        born_cfg_data = global_data.game_mode.get_born_data()
        door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
        if global_data.death_battle_data.area_id is None:
            return
        else:
            door_data = born_cfg_data[global_data.death_battle_data.area_id].get('door')
            if not door_data:
                return
            other_born_data = born_cfg_data[global_data.death_battle_data.area_id].get('other_born_data')
            _scn = world.get_active_scene()
            for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
                _x, _y, _z, _r, _idx, _dict_info = born_data.data
                base_pos = math3d.vector(_x, _y, _z)
                is_my_group = self.get_player_group_id() == group_id
                if other_born_data:
                    x, y, z, range = other_born_data[_idx]
                    position = math3d.vector(x, y, z)

                    def create_cb(sfx, range=range):
                        scale = range / (3.0 / 2)
                        sfx.scale = math3d.vector(scale, scale, scale)

                    size_sfx_index = 0 if is_my_group else 1
                    size_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(BORN_PART_SIZE_SFX[size_sfx_index], position, on_create_func=create_cb)
                    self.born_part_effect.append(size_sfx_id)
                if not self._is_ace_time:
                    for index, door_id in enumerate(door_data[_idx]):
                        door_info = door_cfg_data.get(str(door_id))
                        if not door_info:
                            continue
                        door_id = int(door_id)
                        if _dict_info:
                            is_weak_door = _dict_info.get(door_id, False)
                        else:
                            is_weak_door = False
                        x, y, z = door_info.get('pos')
                        dx, dy, dz = door_info.get('rot')
                        scale_x, scale_y, scale_z = door_info.get('scale')
                        size_x, size_y, size_z = door_info.get('size')
                        center_x, center_y, center_z = door_info.get('center_pos')
                        scale = math3d.vector(scale_x, scale_y, scale_z)
                        size = math3d.vector(size_x, size_y, size_z)
                        center_pos = math3d.vector(center_x, center_y, center_z)
                        rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * dx / 180, math.pi * dy / 180, math.pi * dz / 180))
                        door_pos = math3d.vector(x, y, z)
                        size *= scale
                        col_position = door_pos + center_pos * scale * rot_mat
                        need_trigger = is_my_group or is_weak_door or global_data.battle and global_data.battle.get_is_force_trigger_door()
                        if need_trigger:
                            mask = (GROUP_SHOOTUNIT | GROUP_GRENADE) & ~GROUP_CAMERA_COLL
                            group = REGION_SCENE_GROUP & ~GROUP_CAMERA_COLL
                        else:
                            mask = TERRAIN_MASK
                            group = REGION_SCENE_GROUP
                        col = collision.col_object(collision.BOX, size * 0.5, mask, group, 0, True)
                        col.rotation_matrix = rot_mat
                        col.position = col_position
                        _scn.scene_col.add_object(col)
                        self._col_obj[door_id] = col
                        if need_trigger:
                            self._weak_doors.add(door_id)
                        if need_trigger:
                            mask = TERRAIN_MASK
                            group = REGION_SCENE_GROUP
                            col = collision.col_object(collision.BOX, size * 0.5, mask, group, 0, True)
                            col.rotation_matrix = rot_mat
                            col.position = col_position
                            col.enable_ccd = True
                            col.set_trigger(is_trigger)
                            col.set_trigger_callback(Functor(self._trigger_cb, door_id))
                            _scn.scene_col.add_object(col)
                            self._ready_col_obj[door_id] = (group_id, col, door_pos)

            self.clear_timer()
            if not is_trigger and not self._is_ace_time:
                self.set_trigger_timer = global_data.game_mgr.get_logic_timer().register(func=self.set_col_trigger, mode=timer.CLOCK, interval=revive_time + 1, times=1)
            if not self._is_ace_time:
                self.check_timer = global_data.game_mgr.get_logic_timer().register(func=self.check_in_enemy_base, mode=timer.CLOCK, interval=1)
            return

    def cal_enemy_base_range(self, player_pos, born_data, range_data):
        _x, _y, _z, _r, _idx, _dict_info = born_data
        y_range = range_data.get('y_range')
        if not y_range:
            return False
        if player_pos.y < _y + y_range[0] or player_pos.y > _y + y_range[1]:
            return False
        pos_lst = range_data.get('pos_lst', [])
        return pnpoly(len(pos_lst), pos_lst, (player_pos.x, player_pos.z))

    def check_in_enemy_base(self):
        if self.is_in_trigger:
            return
        else:
            in_enemy_base = False
            if not global_data.cam_lplayer:
                return
            player_pos = global_data.cam_lplayer.ev_g_position()
            if not player_pos:
                return
            born_range_data = global_data.game_mode.get_cfg_data('born_range_data')
            born_cfg_data = global_data.game_mode.get_born_data()
            door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
            range_ids = born_cfg_data[global_data.death_battle_data.area_id].get('c_range_accurate')
            if not range_ids:
                range_ids = born_cfg_data[global_data.death_battle_data.area_id].get('c_range')
            if self.is_debug:
                for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
                    _x, _y, _z, _r, _idx, _dict_info = born_data.data
                    range_data = born_range_data.get(str(range_ids[_idx]), {})
                    self.draw_line(born_data.data, range_data)
                    extra_pos_id = range_data.get('extra_pos_id', [])
                    for pos_id in extra_pos_id:
                        range_data = born_range_data.get(str(pos_id), {})
                        self.draw_line(born_data.data, range_data)

            door_data = born_cfg_data[global_data.death_battle_data.area_id].get('door')
            if not door_data:
                return
            mix_dis = 0
            mix_dis_door_pos = None
            for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
                is_my_group = self.get_player_group_id() == group_id
                if is_my_group:
                    continue
                _x, _y, _z, _r, _idx, _dict_info = born_data.data
                base_pos = math3d.vector(_x, _y, _z)
                for index, door_id in enumerate(door_data[_idx]):
                    if _dict_info:
                        is_weak_door = _dict_info.get(door_id, False)
                    else:
                        is_weak_door = False
                    if not is_weak_door:
                        return
                    door_info = door_cfg_data.get(str(door_id))
                    if not door_info:
                        continue
                    door_id = int(door_id)
                    x, y, z = door_info.get('pos')
                    door_pos = math3d.vector(x, y, z)
                    dis = (player_pos - door_pos).length
                    if mix_dis == 0:
                        mix_dis = dis
                        mix_dis_door_pos = (door_id, door_pos, base_pos)
                    elif dis < mix_dis:
                        mix_dis = dis
                        mix_dis_door_pos = (door_id, door_pos, base_pos)

                range_data = born_range_data.get(str(range_ids[_idx]), {})
                in_enemy_base = in_enemy_base or self.cal_enemy_base_range(player_pos, born_data.data, range_data)
                extra_pos_id = range_data.get('extra_pos_id', [])
                for pos_id in extra_pos_id:
                    range_data = born_range_data.get(str(pos_id), {})
                    in_enemy_base = in_enemy_base or self.cal_enemy_base_range(player_pos, born_data.data, range_data)

            if mix_dis_door_pos:
                door_id, door_pos, base_pos = mix_dis_door_pos
                self.door_report(in_enemy_base, door_id)
            return

    def draw_line(self, born_data, range_data):
        _x, _y, _z, _r, _idx, _dict_info = born_data
        y_range = range_data.get('y_range')
        if not y_range:
            return
        pos_lst = range_data.get('pos_lst', [])
        new_pos_lst = []
        for pos in pos_lst:
            new_pos_lst.append(math3d.vector(pos[0], _y, pos[1]))

        new_pos_lst.append(new_pos_lst[0])
        global_data.emgr.scene_draw_line_event.emit(new_pos_lst, alive_time=1, color=16711680)
        new_pos_lst = []
        for pos in pos_lst:
            new_pos_lst.append(math3d.vector(pos[0], _y + y_range[0], pos[1]))

        new_pos_lst.append(new_pos_lst[0])
        global_data.emgr.scene_draw_line_event.emit(new_pos_lst, alive_time=1, color=16711680)
        new_pos_lst = []
        for pos in pos_lst:
            new_pos_lst.append(math3d.vector(pos[0], _y + y_range[1], pos[1]))

        new_pos_lst.append(new_pos_lst[0])
        global_data.emgr.scene_draw_line_event.emit(new_pos_lst, alive_time=1, color=16711680)
        p1 = math3d.vector(_x, _y, _z)
        p2 = math3d.vector(_x, _y + y_range[0], _z)
        p3 = math3d.vector(_x, _y + y_range[1], _z)
        new_pos_lst = [p2, p1, p3]
        global_data.emgr.scene_draw_line_event.emit(new_pos_lst, alive_time=1, color=16711680)
        global_data.emgr.scene_draw_wireframe_event.emit(p1, math3d.matrix(), 1, length=(8,
                                                                                         8,
                                                                                         8))
        global_data.emgr.scene_draw_wireframe_event.emit(p2, math3d.matrix(), 1, length=(8,
                                                                                         8,
                                                                                         8))
        global_data.emgr.scene_draw_wireframe_event.emit(p3, math3d.matrix(), 1, length=(8,
                                                                                         8,
                                                                                         8))

    def death_into_ace_stage_event(self):
        self.check_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_timer)
        self.check_timer = None
        _scn = world.get_active_scene()
        for col in six.itervalues(self._col_obj):
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._col_obj = {}
        for _, col, _ in six.itervalues(self._ready_col_obj):
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._ready_col_obj = {}
        self.clear_screen_sfx()
        global_data.ui_mgr.close_ui('DeathEnemyBaseUI')
        self._weak_doors = set()
        return

    def remove_col(self):
        _scn = world.get_active_scene()
        for col in six.itervalues(self._col_obj):
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._col_obj = {}
        for _, col, _ in six.itervalues(self._ready_col_obj):
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._ready_col_obj = {}
        for sfx_id in self.born_part_effect:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.born_part_effect = []
        self.is_in_trigger = False
        self._weak_doors = set()