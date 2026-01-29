# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterRangeLogic.py
from __future__ import absolute_import
from six.moves import range
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY, UP_BODY
import world
import math3d
from logic.gutils.weapon_utils import recheck_pve_fire_dir
from logic.gcommon.common_const.idx_const import ExploderID
from common.utils.timer import CLOCK
from math import pi, radians
from logic.gcommon.common_const.weapon_const import WP_NAVIGATE_GUN, WP_TRACK_MISSILE, WP_SWORD_LIGHT
from common.cfg import confmgr
import game3d
from logic.gutils.pve_utils import get_aim_pos, get_bias_aim_pos
import collision
from logic.gcommon.common_const.collision_const import S_GROUP_SCENE

class MonsterRangeBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    RANGE_END = -1
    RANGE_AIM = 0
    RANGE_PRE = 1
    RANGE_ATK = 2
    RANGE_BAC = 3
    AIM_GAP = 0.1 * pi
    A_T = 0.033
    A_L = 1
    A_R = 2
    A_E = 3

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id, self.target_pos = args
        if self.target_pos:
            self.target_pos = math3d.vector(*self.target_pos)
        self.active_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterRangeBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.RANGE_END

    def init_params(self):
        self.wp_pos = 0
        self.target_id = None
        self.target_pos = None
        self.min_cast_interval = self.custom_param.get('min_cast_interval', 0.2)
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.fire_idx = 0
        self.fire_timer = None
        self.fire_seq = 0
        self.sub_idx = 0
        self.yaw_ts = 0
        self.aim_timer = None
        self.aim_lr = 0
        self.aim_left_anim = None
        self.aim_right_anim = None
        self.aim_gap = None
        self.fire_delay_id = None
        self.bias_dur = 0
        self.move_ts = 0
        self.move_start_ts = 0
        self.move_end_ts = 0
        self.move_anim = ''
        self.move_anim_rate = 1.0
        self.move_tag = False
        self.move_end_tag = False
        self.stand_anim = ''
        self.stand_anim_rate = 1.0
        self.anim_part = LOW_BODY
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def check_transitions(self):
        pass

    def on_init_complete(self):
        super(MonsterRangeBase, self).on_init_complete()
        self.bias_dur = self.sd.ref_bias_dur

    def reset_range_state(self):
        self.reset_sub_states_callback()
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.atk_anim_dur = self.atk_anim_dur_list[self.fire_idx]
        self.atk_anim_rate = self.atk_anim_rate_list[self.fire_idx]
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.register_range_callbacks()

    def register_range_callbacks(self):
        self.register_substate_callback(self.RANGE_PRE, 0, self.begin_pre)
        self.register_substate_callback(self.RANGE_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.RANGE_ATK, 0, self.begin_atk)
        self.register_substate_callback(self.RANGE_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.RANGE_BAC, 0, self.begin_bac)
        self.register_substate_callback(self.RANGE_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def begin_pre(self):
        self.reset_aim_timer()
        if not self.pre_anim_dur:
            return
        self.pre_anim_name = self.pre_anim_name_list[self.fire_idx]
        if self.pre_anim_name:
            self.send_event('E_ANIM_RATE', self.anim_part, self.pre_anim_rate)
            self.send_event('E_POST_ACTION', self.pre_anim_name, self.anim_part, 1)

    def end_pre(self):
        self.sub_state = self.RANGE_ATK

    def begin_atk(self):
        if not self.atk_anim_dur:
            return
        self.atk_anim_name = self.atk_anim_name_list[self.fire_idx]
        if self.atk_anim_name:
            self.send_event('E_ANIM_RATE', self.anim_part, self.atk_anim_rate)
            self.send_event('E_POST_ACTION', self.atk_anim_name, self.anim_part, 1)
        self.cancel_fire_delay()
        if self.fire_delay:
            self.fire_delay_id = game3d.delay_exec(self.fire_delay * 1000, self.init_fire())
        else:
            self.init_fire()

    def end_atk(self):
        self.sub_state = self.RANGE_BAC
        self.cancel_fire_delay()

    def begin_bac(self):
        if not self.bac_anim_dur:
            return
        self.bac_anim_name = self.bac_anim_name_list[self.fire_idx]
        if self.bac_anim_name:
            self.send_event('E_ANIM_RATE', self.anim_part, self.bac_anim_rate)
            self.send_event('E_POST_ACTION', self.bac_anim_name, self.anim_part, 1)

    def end_bac(self):
        if self.fire_idx < self.fire_count - 1:
            self.fire_idx += 1
            self.reset_range_state()
            self.sub_state = self.RANGE_PRE
        else:
            self.sub_state = self.RANGE_END

    def init_fire(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            if self.sub_state != self.RANGE_ATK:
                return
            self.fire_socket = self.fire_socket_list[self.fire_idx]
            mat = model.get_socket_matrix(self.fire_socket, world.SPACE_TYPE_WORLD)
            if not mat:
                if global_data.is_inner_server:
                    global_data.game_mgr.show_tip('%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xb5\x84\xe6\xba\x90\xe6\xb2\xa1\xe6\x9c\x89\xe8\xa1\xa8\xe9\x87\x8c\xe5\xa1\xab\xe7\x9a\x84\xe8\xbf\x99\xe4\xb8\xaa\xe5\xbc\x80\xe7\x81\xab\xe6\x8c\x82\xe8\x8a\x82\xe7\x82\xb9 %s' % (self.skill_id, self.fire_socket))
                import exception_hook
                msg = '%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xb5\x84\xe6\xba\x90\xe6\xb2\xa1\xe6\x9c\x89\xe8\xa1\xa8\xe9\x87\x8c\xe5\xa1\xab\xe7\x9a\x84\xe8\xbf\x99\xe4\xb8\xaa\xe5\xbc\x80\xe7\x81\xab\xe6\x8c\x82\xe8\x8a\x82\xe7\x82\xb9 %s' % (self.skill_id, self.fire_socket)
                exception_hook.post_stack(msg)
                return
            start_pos = mat.translation
            target_pos = get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur)
            if not self.check_fire_pos(start_pos):
                return
            direction = target_pos - start_pos
            direction.normalize()
            self.prepare_fire(start_pos, direction)
            self.fire_delay_id = None
            return

    def prepare_fire(self, start_pos, direction):
        self.check_wp()
        if type(self.wp_pellets) == dict:
            self.reset_fire_timer()
            self.fire_seq = 0
            self.sub_idx = 0
            self.fire_timer = global_data.game_mgr.register_logic_timer(self.open_fire_seq, self.wp_pellets['cd'], (start_pos, direction), len(self.wp_pellets['bullets']), CLOCK)
        else:
            self.sub_idx = 0
            for i in range(0, self.wp_pellets):
                self.open_fire(start_pos, direction)

    def check_wp(self):
        wp_idx = self.fire_idx % len(self.wp_list)
        wp_type = self.wp_list[wp_idx]
        if wp_type != self.wp_type:
            self.wp_type = wp_type
            self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
            self.wp_pellets = self.wp_conf.get('iPellets')
            self.wp_kind = self.wp_conf.get('iKind')
            self.wp_cus_param = self.wp_conf.get('cCustomParam', {})

    def open_fire_seq(self, start_pos, direction):
        if not isinstance(self.wp_pellets, dict):
            self.reset_fire_timer()
            return
        count = self.wp_pellets['bullets'][self.fire_seq]
        for i in range(0, count):
            self.open_fire(start_pos, direction)

        self.fire_seq += 1

    def open_fire(self, start_pos, direction):
        if not self or not self.is_valid():
            return
        else:
            owner = self.unit_obj.get_owner()
            fix_dir = recheck_pve_fire_dir(self.wp_cus_param, direction, self.sub_idx, owner.get_monster_id(), owner.get_pve_monster_level(), self.wp_type)
            throw_item = {'uniq_key': self.get_uniq_key(),
               'item_itype': self.wp_type,
               'item_kind': self.wp_kind,
               'position': (
                          start_pos.x, start_pos.y, start_pos.z),
               'dir': (
                     fix_dir.x, fix_dir.y, fix_dir.z),
               'sub_idx': self.sub_idx
               }
            if self.wp_kind == WP_NAVIGATE_GUN:
                throw_item.update({'aim_target': self.target_id,
                   'm_position': (
                                start_pos.x, start_pos.y, start_pos.z),
                   'wp_pos': self.wp_pos,
                   'aim_pos': (
                             self.target_pos.x, self.target_pos.y, self.target_pos.z)
                   })
            elif self.wp_kind == WP_SWORD_LIGHT:
                throw_item.update({'col_width': self.wp_cus_param.get('energy_width', 9)
                   })
                roll_angle = self.wp_cus_param.get('roll_angle', None)
                if roll_angle:
                    rad = radians(roll_angle)
                    rot_mat = math3d.matrix.make_rotation(math3d.vector(0, 0, 1), rad)
                    ret = math3d.vector(0, 1, 0) * rot_mat
                    up = (ret.x, ret.y, ret.z)
                    throw_item.update({'up': up
                       })
            self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
            self.sub_idx += 1
            return

    def reset_fire_timer(self):
        if self.fire_timer:
            global_data.game_mgr.unregister_logic_timer(self.fire_timer)
            self.fire_timer = None
        return

    def cancel_fire_delay(self):
        if self.fire_delay_id:
            game3d.cancel_delay_exec(self.fire_delay_id)
            self.fire_delay_id = None
        return

    def enter(self, leave_states):
        super(MonsterRangeBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        if self.sub_state == self.RANGE_END:
            self.fire_idx = 0
            self.reset_range_state()
            self.sub_state = self.RANGE_AIM
            self.init_aim()
            self.move_tag = False
            self.move_end_tag = False
            self.move_ts = 0
            self.anim_part = self.move_anim or LOW_BODY if 1 else UP_BODY

    def update(self, dt):
        super(MonsterRangeBase, self).update(dt)
        if self.sub_state == self.RANGE_END:
            self.disable_self()
        elif self.sub_state in (self.RANGE_PRE, self.RANGE_ATK, self.RANGE_BAC):
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.RANGE_AIM:
            self.update_aim_timer(dt)
        if self.aim_lr == self.A_E:
            self.move_ts += dt
            if self.move_start_ts < self.move_ts < self.move_end_ts:
                if self.move_anim and not self.move_tag:
                    self.send_event('E_ANIM_RATE', LOW_BODY, self.move_anim_rate)
                    self.send_event('E_POST_ACTION', self.move_anim, LOW_BODY, 1, loop=self.move_anim_loop)
                    self.move_tag = True
                if self.move_to_point_tag:
                    move_dire = get_aim_pos(None, self.target_pos) - self.ev_g_position()
                else:
                    move_dire = get_aim_pos(self.target_id, self.target_pos) - self.ev_g_position()
                move_dire.normalize()
                self.send_event('E_SET_WALK_DIRECTION', move_dire * self.move_speed)
            elif self.move_ts > self.move_end_ts:
                if self.stand_anim and not self.move_end_tag:
                    self.send_event('E_ANIM_RATE', LOW_BODY, self.stand_anim_rate)
                    self.send_event('E_POST_ACTION', self.stand_anim, LOW_BODY, 1)
                    self.move_end_tag = True
                self.send_event('E_CLEAR_SPEED')
        return

    def init_aim(self):
        self.yaw_ts = 0
        self.aim_lr = 0
        self.reset_aim_timer()
        self.aim_timer = global_data.game_mgr.register_logic_timer(self.update_aim, self.A_T, None, -1, CLOCK, True)
        return

    def update_aim_timer(self, dt):
        self.yaw_ts += dt
        if self.yaw_ts > self.max_aim_dur:
            self.sub_state = self.RANGE_PRE
            self.reset_aim_timer()

    def update_aim(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        ori_pos = self.ev_g_position()
        if not ori_pos or not target_pos:
            return
        tar_dir = target_pos - ori_pos
        tar_yaw = tar_dir.yaw + 2 * pi
        ori_yaw = self.ev_g_forward().yaw + 2 * pi
        diff_yaw = tar_yaw - ori_yaw
        if diff_yaw < -pi:
            diff_yaw += 2 * pi
        else:
            if diff_yaw > pi:
                diff_yaw -= 2 * pi
            aim_gap = self.aim_gap if self.aim_gap else self.AIM_GAP
            if abs(diff_yaw) < aim_gap:
                self.sub_state = self.RANGE_PRE
                self.reset_aim_timer()
                self.aim_lr = self.A_E
                if self.stand_anim:
                    self.send_event('E_ANIM_RATE', LOW_BODY, self.stand_anim_rate)
                    self.send_event('E_POST_ACTION', self.stand_anim, LOW_BODY, 1, loop=True)
                return
        if diff_yaw < 0:
            ret_yaw = ori_yaw - self.aim_speed * dt
            lr_tag = self.A_L
        else:
            ret_yaw = ori_yaw + self.aim_speed * dt
            lr_tag = self.A_R
        self.send_event('E_CAM_YAW', ret_yaw)
        self.send_event('E_ACTION_SYNC_YAW', ret_yaw)
        if self.aim_left_anim and self.aim_lr != lr_tag:
            anim = self.aim_left_anim if lr_tag == self.A_L else self.aim_right_anim
            rate = self.aim_left_anim_rate if lr_tag == self.A_L else self.aim_right_anim_rate
            self.send_event('E_ANIM_RATE', LOW_BODY, rate)
            self.send_event('E_POST_ACTION', anim, LOW_BODY, 1, loop=True)
            self.aim_lr = lr_tag

    def reset_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

    def exit(self, enter_states):
        if self.anim_part == UP_BODY:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        super(MonsterRangeBase, self).exit(enter_states)
        self.sub_state = self.RANGE_END
        self.fire_idx = 0
        self.reset_fire_timer()
        self.reset_aim_timer()
        self.cancel_fire_delay()
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        self.reset_fire_timer()
        self.reset_aim_timer()
        self.cancel_fire_delay()
        super(MonsterRangeBase, self).destroy()

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def update_col_ids(self):
        self._col_ids = self.ev_g_human_col_id()

    def check_fire_pos(self, fire_pos):
        start_pos = self.ev_g_position()
        if not start_pos:
            return False
        else:
            start_pos.y = fire_pos.y
            end_pos = fire_pos
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, S_GROUP_SCENE, S_GROUP_SCENE, collision.EQUAL_FILTER, True)
            if not result[0]:
                return True
            return False


class MonsterRange(MonsterRangeBase):

    def init_params(self):
        super(MonsterRange, self).init_params()
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.wp_list = self.custom_param.get('wp_list', (808012, ))
        self.wp_pos = self.custom_param.get('wp_pos', 1)
        self.wp_type = self.wp_list[self.wp_pos - 1]
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        if not self.wp_conf:
            if global_data.is_inner_server:
                global_data.game_mgr.show_tip('%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xad\xa6\xe5\x99\xa8\xe8\xa1\xa8\xe9\x87\x8c\xe9\x9d\xa2\xe6\xb2\xa1\xe6\x9c\x89\xe9\x85\x8d\xe8\xbf\x99\xe4\xb8\xaa\xe6\xad\xa6\xe5\x99\xa8 \xe7\x8e\xa9\xe4\xb8\x8d\xe4\xba\x86\xe5\x85\x84\xe5\xbc\x9f %s' % (self.skill_id, self.wp_type))
            import exception_hook
            msg = '%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xad\xa6\xe5\x99\xa8\xe8\xa1\xa8\xe9\x87\x8c\xe9\x9d\xa2\xe6\xb2\xa1\xe6\x9c\x89\xe9\x85\x8d\xe8\xbf\x99\xe4\xb8\xaa\xe6\xad\xa6\xe5\x99\xa8 \xe7\x8e\xa9\xe4\xb8\x8d\xe4\xba\x86\xe5\x85\x84\xe5\xbc\x9f %s' % (self.skill_id, self.wp_type)
            exception_hook.post_stack(msg)
        self.wp_pellets = self.wp_conf.get('iPellets')
        self.wp_kind = self.wp_conf.get('iKind')
        self.wp_cus_param = self.wp_conf.get('cCustomParam', {})
        self.skill_id = self.custom_param.get('skill_id', 9010251)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.aim_gap = self.custom_param.get('aim_gap', None)
        self.pre_anim_name_list = self.custom_param.get('pre_anim_name_list', ('', ))
        self.pre_anim_name = self.pre_anim_name_list[self.fire_idx]
        self.pre_anim_rate_list = self.custom_param.get('pre_anim_rate_list', (1.0, ))
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.pre_anim_dur_list = self.custom_param.get('pre_anim_dur_list', (0, ))
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.atk_anim_name_list = self.custom_param.get('atk_anim_name_list', ('attack01', ))
        self.atk_anim_name = self.atk_anim_name_list[self.fire_idx]
        self.atk_anim_rate_list = self.custom_param.get('atk_anim_rate_list', (1.0, ))
        self.atk_anim_rate = self.atk_anim_rate_list[self.fire_idx]
        self.atk_anim_dur_list = self.custom_param.get('atk_anim_dur_list', (1.0, ))
        self.atk_anim_dur = self.atk_anim_dur_list[self.fire_idx]
        self.bac_anim_name_list = self.custom_param.get('bac_anim_name_list', ('', ))
        self.bac_anim_name = self.bac_anim_name_list[self.fire_idx]
        self.bac_anim_rate_list = self.custom_param.get('bac_anim_rate_list', (1.0, ))
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.bac_anim_dur_list = self.custom_param.get('bac_anim_dur_list', (0, ))
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.fire_socket_list = self.custom_param.get('fire_socket_list', ('fx_kaihuo', ))
        self.fire_socket = self.fire_socket_list[self.fire_idx]
        self.fire_delay = self.custom_param.get('fire_delay', 0)
        self.move_start_ts = self.custom_param.get('move_start_ts', 0)
        self.move_end_ts = self.custom_param.get('move_end_ts', 0)
        self.move_anim = self.custom_param.get('move_anim', '')
        self.move_anim_rate = self.custom_param.get('move_anim_rate', 1.0)
        self.move_anim_loop = self.custom_param.get('move_anim_loop', True)
        self.move_speed = self.custom_param.get('move_speed', 0)
        self.move_to_point_tag = self.custom_param.get('move_to_point_tag', False)
        self.stand_anim = self.custom_param.get('stand_anim', '')
        self.stand_anim_rate = self.custom_param.get('stand_anim_rate', 1.0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.sd.ref_bias_dur
            self.reset_sub_states_callback()
            self.register_range_callbacks()