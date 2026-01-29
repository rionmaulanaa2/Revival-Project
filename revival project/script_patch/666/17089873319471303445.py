# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterDashAtkLogic.py
from __future__ import absolute_import
from logic.gcommon.behavior.StateBase import StateBase
from .BoostLogic import OxRushNew
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
import math3d
from logic.gutils.scene_utils import dash_filtrate_hit
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from logic.gutils.pve_utils import get_aim_pos

class MonsterDashAtkBase(OxRushNew):
    BIND_EVENT = OxRushNew.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       })
    econf = {}
    STAGE_ENTER = 1
    STAGE_RUSH = 2

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            self.skill_id, self.target_id, self.target_pos = args
            if self.target_pos:
                self.target_pos = math3d.vector(*self.target_pos) if 1 else None
                if self.is_active:
                    return False
                return self.check_can_active() or False
            self.editor_handle()
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterDashAtkBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.target_id = None
        self.target_pos = None
        self.dash_dur = 0
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.is_hit_play_skill = False
        self.hit_id = set()
        self.check_hit_timer = None
        self.rush_direction = None
        self.in_free_cam = False
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def read_data_from_custom_param(self):
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.col_info = self.custom_param.get('col_info', (30, 50))
        super(MonsterDashAtkBase, self).read_data_from_custom_param()

    def editor_handle(self):
        pass

    def on_init_complete(self):
        super(MonsterDashAtkBase, self).on_init_complete()

    def init_parameters(self):
        super(MonsterDashAtkBase, self).init_parameters()
        self.rush_direction = None
        self.start_pos = None
        return

    def enter(self, leave_states):
        super(MonsterDashAtkBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.air_walk_direction_setter.reset()
        if self.calc_dir_stage == self.STAGE_ENTER:
            if not self.calc_direction():
                self.disable_self()
                return
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_OXRUSH_MONSTER', True)

    def calc_direction(self):
        if not self.target_id and not self.target_pos:
            return False
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        start_pos = self.ev_g_position()
        self.rush_direction = target_pos - start_pos
        self.rush_direction.y = 5
        self.start_pos = start_pos
        if not self.target_id:
            self.dash_dur = self.rush_direction.length / self.max_rush_speed
        self.rush_direction.normalize()
        return True

    def update(self, dt):
        StateBase.update(self, dt)
        if self.sub_state == self.STATE_PRE:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        if self.is_accelerating:
            pass
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.dash_dur:
            if self.elapsed_time > self.dash_dur + self.pre_anim_duration / self.pre_anim_rate:
                self.sub_state = self.STATE_MISS
        if self.rush_direction is not None and self.is_moving:
            walk_direction = self.get_walk_direction(self.rush_direction)
            self.air_walk_direction_setter.execute(walk_direction)
        return

    def exit(self, enter_states):
        super(MonsterDashAtkBase, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_MONSTER', False)
        self.stop_check_hit()
        self.rush_direction = None
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        self.send_event('E_ON_STATE_EXIT', self.sid)
        return

    def destroy(self):
        self.clear_check_hit_timer()
        self.process_event(False)
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        super(MonsterDashAtkBase, self).destroy()
        return

    def on_begin_rush(self):
        super(MonsterDashAtkBase, self).on_begin_rush()
        if self.calc_dir_stage == self.STAGE_ENTER:
            if not self.calc_direction():
                self.disable_self()
                return
        self.start_check_hit()
        self.send_event('E_FORWARD', self.rush_direction, True)
        if self.begin_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.begin_aoe_skill_id)

    def on_end_rush(self):
        self.sub_state = self.STATE_MISS

    def on_begin_miss(self):
        super(MonsterDashAtkBase, self).on_begin_miss()
        if self.end_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.end_aoe_skill_id)

    def refresh_air_dash_end_speed(self):
        if not self.rush_direction:
            return
        self.cur_speed = self.air_dash_end_speed
        walk_direction = self.get_walk_direction(self.rush_direction)
        self.send_event('E_VERTICAL_SPEED', 0)
        walk_direction.y = 0
        self.send_event('E_SET_WALK_DIRECTION', walk_direction)
        self.sd.ref_cur_speed = walk_direction.length

    def start_check_hit(self):
        self.clear_check_hit_timer()
        self.check_hit_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_hit, mode=2, interval=0.1)

    def stop_check_hit(self):
        self.clear_check_hit_timer()
        self.hit_id = set()

    def _check_hit(self):
        ret_dict = self.get_hit_ret()
        if ret_dict:
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, ret_dict), False, True)

    def get_hit_ret(self):
        height, radius = self.col_info
        hit_ret = {}
        if global_data.player and global_data.player.logic:
            pos = self.ev_g_position() + math3d.vector(0, height, 0)
            if global_data.is_inner_server and self.is_draw_col and not global_data.skip_pve_draw_col:
                global_data.emgr.scene_draw_wireframe_event.emit(pos, math3d.matrix(), 10, length=(radius * 2, radius * 2, radius * 2))
            hit_units = global_data.emgr.scene_get_hit_all_enemy_unit.emit(self.unit_obj.ev_g_camp_id(), pos, radius)
            if hit_units and hit_units[0]:
                for unit in hit_units[0]:
                    unit_id = unit.id
                    if unit_id not in self.hit_id:
                        if dash_filtrate_hit(self.unit_obj, unit):
                            continue
                        self.hit_id.add(unit_id)
                        unit_pos = unit.ev_g_position()
                        temp_d = unit_pos - self.start_pos
                        temp_d.normalize()
                        cos_phi = self.rush_direction.dot(temp_d)
                        ret = self.start_pos + self.rush_direction * (unit_pos - self.start_pos).length * cos_phi
                        hit_ret[unit_id] = (ret.x, ret.y, ret.z)

        return hit_ret

    def clear_check_hit_timer(self):
        self.check_hit_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
        self.check_hit_timer = None
        return


class MonsterDashAtk(MonsterDashAtkBase):

    def read_data_from_custom_param(self):
        super(MonsterDashAtk, self).read_data_from_custom_param()
        self.max_rush_duration = self.custom_param.get('max_rush_duration', 3.0)
        self.max_rush_speed = self.custom_param.get('max_rush_speed', 180)
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 3.0)
        self.pre_anim = self.custom_param.get('pre_anim', 'attack_04')
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 1.0)
        self.start_acc_time = self.custom_param.get('start_acc_time', self.pre_anim_duration)
        self.rush_anim = self.custom_param.get('rush_anim', 'run')
        self.rush_anim_rate = self.custom_param.get('rush_anim_rate', 2.0)
        self.miss_anim = self.custom_param.get('miss_anim', 'hit')
        self.miss_anim_rate = self.custom_param.get('miss_anim_rate', 1.0)
        self.miss_anim_duration = self.custom_param.get('miss_anim_duration', 1.0)
        self.end_brake_time = self.custom_param.get('end_brake_time', 0.1)
        self.air_dash_end_speed = self.custom_param.get('air_dash_end_speed', 30)
        self.skill_id = self.custom_param.get('skill_id', 9010153)
        self.tick_interval = self.custom_param.get('tick_interval', 0.03)
        self.is_draw_col = self.custom_param.get('is_draw_col', True)
        self.col_info = self.custom_param.get('col_info', (30, 100))
        self.begin_aoe_skill_id = self.custom_param.get('begin_aoe_skill_id', None)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.calc_dir_stage = self.STAGE_ENTER
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.read_data_from_custom_param()
            self.reset_sub_states_callback()
            self._register_sub_state_callbacks()