# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/DoorNPC.py
from __future__ import absolute_import
import world
epsilon = 0.001
from math import radians
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision
import math3d
from logic.gcommon.common_const.collision_const import TERRAIN_MASK, WOOD_GROUP

class ITriggerZone(object):

    def on_enter_zone(self, pos):
        pass

    def on_leave_zone(self, pos):
        pass


class DoorNPC(ITriggerZone):
    DIR_FORWARD = -1
    DIR_BACKWARD = 1

    def __init__(self, bdict):
        import math3d
        from logic.gcommon.common_const.ui_operation_const import DOOR_DEF_EXTRA_SIZE, DOOR_OPEN_TIME, DOOR_CLOSE_TIME
        self.id = bdict.get('wid')
        self.door_model = bdict.get('model')
        self.door_model.pickable = True
        self.close_yaw = bdict.get('close_yaw')
        init_state = bdict.get('init_state')
        self.door_type = bdict.get('door_type')
        init_yaw = self.cal_door_state_angle(init_state)
        self.cur_yaw = init_yaw
        self.house_id = bdict.get('house_entity_id')
        self.close_door_wpos = bdict.get('close_door_wpos')
        self.open_state = not abs(self.close_yaw - self.cur_yaw) < epsilon
        extra_size = DOOR_DEF_EXTRA_SIZE
        self.door_open_time = DOOR_OPEN_TIME
        self.door_close_time = DOOR_CLOSE_TIME
        self.scale = math3d.vector(self.door_model.bounding_box.x * 2 + extra_size[0], self.door_model.bounding_box.y * 2 + extra_size[1], self.door_model.bounding_box.z * 2 + extra_size[2])
        self.pos = self.close_door_wpos + self.door_model.center * math3d.matrix.make_rotation_y(self.close_yaw)
        self.model_door_dir = math3d.vector(self.pos.x - self.close_door_wpos.x, 0, self.pos.z - self.close_door_wpos.z)
        self.model_door_dir.normalize()
        self.y_rotation = self.door_model.world_rotation_matrix.yaw
        self._ani_timer_id = None
        self._delay_timer_id = None
        self.add_col()
        self.switch_to_door_angle(self.cur_yaw, False)
        self.interact_target = None
        return

    def on_player_setted(self, player):
        self.player = player

    def get_trigger_zone_size(self):
        pass

    def enter_door_zone_callback(self):
        if self.interact_target:
            self.interact_target.send_event('E_ENTER_DOOR_INTERACTION_ZONE', self.id, self.open_state)

    def leave_door_zone_callback(self, event_type):
        if event_type == world.SCENE_TRIGGER_CALLBACK:
            if self.interact_target:
                self.interact_target.send_event('E_LEAVE_DOOR_INTERACTION_ZONE', self.id)

    def get_switched_door_state(self):
        open_state = not self.open_state
        new_yaw = self._get_switch_to_door_state(open_state)
        return self.get_door_state(open_state, new_yaw)

    def _get_switch_to_door_state(self, is_open):
        if self.door_model:
            if is_open:
                open_dir = self.check_door_open_direction()
                angle = radians(90) if open_dir == -1 * DoorNPC.DIR_FORWARD else radians(-90)
                angle *= -1
                angle += self.close_yaw
            else:
                angle = self.close_yaw
            return angle
        else:
            return self.close_yaw

    def _real_switch_door_action(self, is_open, angle, is_play):
        if is_open:
            ani_time = self.door_open_time if 1 else self.door_close_time
            is_play or self._play_door_animation(angle, 0.001, is_open)
        else:

            def real_action():
                self._delay_timer_id = 0
                self._play_door_animation(angle, ani_time, is_open)

            tm = global_data.game_mgr.get_logic_timer()
            if self._delay_timer_id:
                tm.unregister(self._delay_timer_id)
                self._delay_timer_id = None
            if not is_open:
                from common.utils.timer import CLOCK
                self._delay_timer_id = tm.register(func=lambda : real_action(), interval=0.3, times=1, mode=CLOCK)
            else:
                real_action()
        return

    def switch_to_door_angle(self, angle, is_play=True):
        is_open = abs(angle - self.close_yaw) < epsilon
        self._real_switch_door_action(not is_open, angle, is_play)
        self.open_state = not is_open

    def check_can_open_door(self):
        _scn = world.get_active_scene()
        player = _scn.get_player()
        if not player:
            return False
        else:
            model = player.ev_g_model()
            import math3d
            dir2 = self.pos - model.world_position
            dir2 = math3d.vector(dir2.x, 0, dir2.z)
            dir1 = model.world_transformation.forward
            dir1 = math3d.vector(dir1.x, 0, dir1.z)
            cos_angle = dir1.dot(dir2) / (dir1.length * dir2.length)
            if cos_angle > 0:
                return True
            return False

    def check_door_open_direction(self):
        _scn = world.get_active_scene()
        player = _scn.get_player()
        model = player.ev_g_model()
        import math3d
        import math
        player_vec = model.world_position - self.pos
        player_vec = math3d.vector(player_vec.x, 0, player_vec.z)
        if player_vec.length > 0:
            player_vec.normalize()
        door_forward = self.door_model.world_transformation.forward
        door_forward = math3d.vector(door_forward.x, 0, door_forward.z)
        door_forward.normalize()
        dot_v = min(max(player_vec.dot(door_forward), -1), 1)
        angle_door_for_n_player = math.acos(dot_v)
        door_dir = self.model_door_dir
        ang_player = math.atan2(player_vec.z, player_vec.x)
        if ang_player < 0:
            ang_player += 2 * math.pi
        ang_door = math.atan2(door_dir.z, door_dir.x)
        if ang_door < 0:
            ang_door += 2 * math.pi
        clock_wise_angle = ang_player - ang_door
        if clock_wise_angle < 0:
            clock_wise_angle += 2 * math.pi
        if clock_wise_angle > math.pi:
            if angle_door_for_n_player < 0:
                return DoorNPC.DIR_FORWARD
            return DoorNPC.DIR_BACKWARD
        else:
            if angle_door_for_n_player < 0:
                return DoorNPC.DIR_BACKWARD
            return DoorNPC.DIR_FORWARD

    def show_door_break_animation(self):
        import math3d
        if not self.door_model:
            return
        is_shock = False
        if global_data.player and global_data.player.logic:
            pos = global_data.player.logic.ev_g_position()
            door_pos = self.door_model.world_position
            if pos and door_pos:
                dis = (pos - door_pos).length / NEOX_UNIT_SCALE
                if dis <= 8.0:
                    is_shock = True
        center_w = self.door_model.center_w
        self.door_model.visible = False

        def create_cb(sfx):
            sfx.scale = math3d.vector(1.3, 1.3, 1.3)

        sfx_path = 'effect/fx/interaction/door_broke.sfx'
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, center_w, duration=2, on_create_func=create_cb)
        if is_shock:
            sfx_path = 'effect/fx/weapon/huojiantong/huojiantong_zhenping.sfx'
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, center_w)

    def _play_door_animation(self, y_rotation, time, is_open):
        door_model = self.door_model
        self.cur_yaw = y_rotation
        if door_model:
            interval = 1.0 / 20
            count = int(time / interval)
            if count >= 1:
                y_delta = float(y_rotation - self.y_rotation) / count

                def rotate_func(y_delta=y_delta):
                    self._rotate_func(y_delta)

                self._timer_func(interval, count, callback=lambda : rotate_func())
            else:
                self._rotate_func(y_rotation - self.y_rotation)
            if is_open:
                global_data.sound_mgr.play_sound('Play_door_open', self.pos)
            else:
                global_data.sound_mgr.play_sound('Play_door_close', self.pos)

    def _rotate_func(self, y_delta):
        self.door_model.rotate_y(y_delta)
        self._col_obj.position = self.door_model.center_w
        self._col_obj.rotation_matrix = self.door_model.world_rotation_matrix
        self.y_rotation += y_delta

    def _timer_func(self, interval, times=1, callback=None, args=()):
        self.clear_ani_timer()
        if callback:
            tm = global_data.game_mgr.get_logic_timer()
            from common.utils.timer import CLOCK
            self._ani_timer_id = tm.register(func=callback, args=args, interval=interval, times=times, mode=CLOCK)

    def clear_ani_timer(self):
        tm = global_data.game_mgr.get_logic_timer()
        if self._ani_timer_id:
            tm.unregister(self._ani_timer_id)
        self._ani_timer_id = None
        return

    def add_col(self):
        _scn = world.get_active_scene()
        mass = 0
        mask = TERRAIN_MASK
        group = WOOD_GROUP
        size = math3d.vector(self.door_model.bounding_box.x, self.door_model.bounding_box.y, 1)
        self._col_obj = collision.col_object(collision.BOX, size, mask, group, mass)
        self._col_obj.position = self.door_model.center_w
        self._col_obj.rotation_matrix = self.door_model.world_rotation_matrix
        self._col_obj.model_col_name = str(self.house_id) + '_' + str(self.id)
        house_unit_obj = EntityManager.getentity(self.house_id)
        if house_unit_obj and house_unit_obj.logic:
            global_data.emgr.scene_add_shoot_door_event.emit(self._col_obj.cid, house_unit_obj.logic)
            house_unit_obj.logic.send_event('E_HOUSE_ADD_DOOR_COL', self._col_obj.cid, self.id)
        _scn.scene_col.add_object(self._col_obj)

    def remove_col(self):
        if self._col_obj and self._col_obj.valid:
            global_data.emgr.scene_remove_shoot_door_event.emit(self._col_obj.cid)
            house_unit_obj = EntityManager.getentity(self.house_id)
            if house_unit_obj and house_unit_obj.logic:
                house_unit_obj.logic.send_event('E_HOUSE_DEL_DOOR_COL', self._col_obj.cid)
            _scn = world.get_active_scene()
            _scn.scene_col.remove_object(self._col_obj)
        self._col_obj = None
        return

    def destroy(self):
        self.remove_col()
        tm = global_data.game_mgr.get_logic_timer()
        if self._delay_timer_id:
            tm.unregister(self._delay_timer_id)
            self._delay_timer_id = None
        self.clear_ani_timer()
        self.interact_target = None
        self.player = None
        return

    def destroy_model(self):
        if self.door_model and self.door_model.valid:
            self.door_model.destroy()
        self.door_model = None
        return

    def set_door_animation_time(self, open_time, close_time):
        self.door_close_time = close_time
        self.door_open_time = open_time

    def bind_door_interaction_event(self, target):
        self.interact_target = target

    def on_enter_zone(self, pos):
        if self.check_enter_zone(pos):
            return True
        else:
            return False

    def check_enter_zone(self, pos):
        import math3d
        pos = math3d.vector(pos)
        pos += math3d.vector(0, 15, 0)
        lpos = pos - self.pos
        llpos = lpos * math3d.matrix.make_rotation_y(-self.close_yaw)
        if self.scale.z / 2.0 > llpos.z > -self.scale.z / 2.0 and self.scale.y / 2.0 > llpos.y > -self.scale.y / 2.0:
            if self.scale.x / 2.0 > llpos.x > -self.scale.x / 2.0:
                return True
            else:
                return False

        else:
            return False

    def get_dist(self, pos):
        import math3d
        return (pos + math3d.vector(0, 15, 0) - self.pos).length

    def get_cur_yaw(self):
        return self.cur_yaw

    def get_door_state(self, open_state, yaw):
        from logic.gcommon.const import DOOR_STATE_CLOSE, DOOR_STATE_OPEN_IN, DOOR_STATE_OPEN_OUT
        if not open_state:
            return DOOR_STATE_CLOSE
        if yaw - self.close_yaw > 0:
            if self.door_type == 'l':
                return DOOR_STATE_OPEN_OUT
            else:
                return DOOR_STATE_OPEN_IN

        else:
            if self.door_type == 'r':
                return DOOR_STATE_OPEN_OUT
            return DOOR_STATE_OPEN_IN

    def cal_door_state_angle(self, state):
        from logic.gcommon.const import DOOR_STATE_CLOSE, DOOR_STATE_OPEN_OUT
        if state == DOOR_STATE_CLOSE:
            return self.close_yaw
        if state == DOOR_STATE_OPEN_OUT:
            if self.door_type == 'r':
                return self.close_yaw + radians(-90)
            else:
                return self.close_yaw + radians(90)

        else:
            if self.door_type == 'r':
                return self.close_yaw + radians(90)
            return self.close_yaw + radians(-90)

    def show_all_active_trigger_wireframe(self):
        import world
        import math3d
        _points = [
         math3d.vector(-0.5, -0.5, 0.5), math3d.vector(0.5, -0.5, 0.5),
         math3d.vector(0.5, -0.5, -0.5), math3d.vector(-0.5, -0.5, -0.5)]
        pts = list(_points)
        pts.extend([ pt + math3d.vector(0, 1, 0) for pt in _points ])
        line_idx = [0, 1, 2, 0, 3, 2, 6, 3, 7, 6, 1, 5, 6, 4, 7, 0, 4, 5, 0]
        pts_list = []
        for idx in line_idx:
            pts_list.append((pts[idx].x, pts[idx].y, pts[idx].z, 16711680))

        transform = math3d.matrix()
        transform.do_scale(self.scale)
        transform.do_rotation(math3d.matrix.make_rotation_y(self.close_yaw))
        transform.do_translate(self.pos)
        pri = world.primitives(world.get_active_scene())
        pri.create_line_strip(pts_list)
        pri.world_transformation = transform