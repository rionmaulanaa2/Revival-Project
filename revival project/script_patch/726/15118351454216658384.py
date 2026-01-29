# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/CommonMovementSystem.py
from __future__ import absolute_import
import world
import collision
from .SystemBase import SystemBase, FPS_30
from ..client.ComDataLogicMovement import ComDataLogicMovement
from ..client.ComDataLogicMovementRel import ComDataLogicMovementRel
from ..client.ComDataLogicMovementFullFps import ComDataLogicMovementFullFps
from math3d import vector
from logic.gcommon.common_const import collision_const
from logic.gcommon.behavior.StateBase import clamp

class CommonMovementSystem(SystemBase):

    def __init__(self, tick_step=FPS_30):
        super(CommonMovementSystem, self).__init__(tick_step)

    def interested_type(self):
        return (
         ComDataLogicMovement, ComDataLogicMovementRel)

    def ignored_type(self):
        return (
         ComDataLogicMovementFullFps,)

    def handler_types(self):
        return []

    def handle_rel_logic_movement(self, dt, unit):
        data = unit.sd.ref_rel_logic_movement
        sim_t = data.sim_t
        buffer = data.buffer
        if data.disable and data.overdue_frames < data.max_overdue_frames:
            data.overdue_frames += 1
        elif not data.disable and data.overdue_frames > 0:
            data.overdue_frames -= 1
        if sim_t >= data.max_predict_t or not buffer:
            if not data.itpl_stop:
                data.last_pos = vector(data.cur_pos)
                data.last_eid = data.cur_eid
                data.cur_pos = vector(data.sim_pos)
                data.cur_eid = data.sim_eid
                data.dirty = True
                data.itpl_stop = True
            return
        else:
            new_sim_t = sim_t + dt
            chase_dt = data.buffer_max_t - new_sim_t
            if chase_dt < 0:
                sim_t = min(new_sim_t, data.max_predict_t)
            elif data.cur_vel.is_zero and buffer and new_sim_t < buffer[0][0]:
                sim_t = buffer[0][0] - 0.03
                data.src_t = sim_t - 0.03
                data.cur_vel = vector(1, 0, 1)
            else:
                sim_t = new_sim_t + chase_dt * dt
            cur_state = None
            for i, info in enumerate(buffer):
                if sim_t > info[0]:
                    cur_state = info
                else:
                    data.buffer = buffer = buffer[i:]
                    break
            else:
                data.buffer = buffer = []

            if cur_state:
                data.src_t, data.src_eid, data.src_pos, data.cur_vel = cur_state
            if buffer:
                dst_t, dst_eid, dst_pos, vel = buffer[0]
                u = (sim_t - data.src_t) / max(0.015, dst_t - data.src_t)
                src_adjust = self.trans_relative_pos(data.src_eid, data.src_pos, dst_eid)
                if src_adjust:
                    data.sim_pos.intrp(src_adjust, dst_pos, u)
                else:
                    data.sim_pos = vector(dst_pos)
                data.sim_eid = dst_eid
            else:
                data.sim_eid = data.src_eid
                data.sim_pos = data.src_pos
            data.sim_t = sim_t
            data.last_pos = vector(data.cur_pos)
            cur_pos_adjust = self.trans_relative_pos(data.cur_eid, data.cur_pos, data.sim_eid)
            if cur_pos_adjust:
                data.cur_pos.intrp(cur_pos_adjust, data.sim_pos, 0.5)
            else:
                data.cur_pos = vector(data.sim_pos)
            data.last_eid = data.cur_eid
            data.cur_eid = data.sim_eid
            data.dirty = True
            data.itpl_stop = False
            return

    def trans_relative_pos(self, eid_before, rel_pos, eid_after):
        if eid_before == eid_after:
            return rel_pos
        else:
            rel_ent_before = global_data.battle.get_entity(eid_before)
            rel_ent_after = global_data.battle.get_entity(eid_after)
            if not rel_ent_before or not rel_ent_before.logic or not rel_ent_after or not rel_ent_after.logic:
                return None
            par_trans_before = rel_ent_before.logic.ev_g_trans()
            world_pos = global_data.carry_mgr.relative_to_world(rel_pos, par_trans_before)
            par_trans_after = rel_ent_after.logic.ev_g_trans()
            return global_data.carry_mgr.world_to_relative(world_pos, par_trans_after)

    def handle_logic_movement(self, dt, unit):
        data = unit.sd.ref_logic_movement
        sim_t = data.sim_t
        buffer = data.buffer
        if sim_t >= data.max_predict_t or data.cur_vel.is_zero and not buffer:
            if not data.itpl_stop:
                data.last_pos = vector(data.cur_pos)
                data.cur_pos = vector(data.sim_pos)
                data.dirty = True
                data.itpl_stop = True
            return
        else:
            new_sim_t = sim_t + dt
            chase_dt = data.buffer_max_t - new_sim_t
            if chase_dt < 0:
                sim_t = min(new_sim_t, data.max_predict_t)
            elif data.cur_vel.is_zero and buffer and new_sim_t < buffer[0][0]:
                sim_t = buffer[0][0] - 0.03
                data.src_t = sim_t - 0.03
                data.cur_vel = vector(1, 0, 1)
            else:
                sim_t = new_sim_t + chase_dt * dt
            cur_state = None
            for i, info in enumerate(buffer):
                if sim_t > info[0]:
                    cur_state = info
                else:
                    data.buffer = buffer = buffer[i:]
                    break
            else:
                data.buffer = buffer = []

            if cur_state:
                data.src_t, data.src_pos, data.cur_vel, data.cur_acc = cur_state
            if not buffer:
                sim_pos = data.src_pos + data.cur_vel * (sim_t - data.src_t)
                if data.cur_vel.y < -13:
                    sim_pos = self.check_cross_ground(data.sim_pos, sim_pos)
                data.sim_pos = sim_pos
            else:
                dst_t, dst_pos, vel, acc = buffer[0]
                u = (sim_t - data.src_t) / max(0.015, dst_t - data.src_t)
                data.sim_pos.intrp(data.src_pos, dst_pos, u)
            data.sim_t = sim_t
            data.last_pos = vector(data.cur_pos)
            data.cur_pos.intrp(data.cur_pos, data.sim_pos, 0.5)
            data.dirty = True
            data.itpl_stop = False
            return

    def tick(self, dt):
        for unit in self._element_list:
            self.handle_rel_logic_movement(dt, unit)
            self.handle_logic_movement(dt, unit)

    def check_cross_ground(self, start, end):
        if start.y < end.y:
            return end
        bias_vector = vector(0, 1.0, 0)
        ray_start = start + bias_vector
        ray_end = end - bias_vector
        scene = world.get_active_scene()
        group = collision_const.GROUP_CAMERA_INCLUDE
        hit, point, normal, fraction, color, obj = scene.scene_col.hit_by_ray(ray_start, ray_end, 0, 65535, group, collision.INCLUDE_FILTER)
        if hit:
            return point + bias_vector
        return end

    def check_cross_ceiling(self, start, end, height=0):
        if not height or not start or start.y > end.y:
            return end
        height_bias = vector(0, height, 0)
        scene = world.get_active_scene()
        group = collision_const.GROUP_CAMERA_INCLUDE
        hit, point, normal, fraction, color, obj = scene.scene_col.hit_by_ray(start, end + height_bias, 0, 65535, group, collision.INCLUDE_FILTER)
        if hit:
            return point - height_bias + vector(0, -1.0, 0)
        return end


class CommonMovementSystemFullFps(CommonMovementSystem):

    def __init__(self):
        super(CommonMovementSystemFullFps, self).__init__(0)

    def interested_type(self):
        return (
         ComDataLogicMovement, ComDataLogicMovementRel, ComDataLogicMovementFullFps)

    def ignored_type(self):
        return ()