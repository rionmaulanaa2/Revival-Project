# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterPounceLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from logic.gutils.pve_utils import get_aim_pos, get_bias_aim_pos
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_POUNCE_WARN_SFX

class MonsterPounceBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_POUNCE_WARN_SFX': 'create_warn_sfx'
       }
    econf = {}
    S_END = 0
    S_DASH_PRE = 1
    S_DASH = 2
    S_LAND = 3
    S_DASH_BAC = 4

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            if self.is_active:
                return False
            if not self.check_can_active():
                return False
            self.editor_handle()
            self.skill_id, self.target_id, self.target_pos = args
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterPounceBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.focus_pos = None
        self.focus_tag = False
        self.use_bias = False
        self.bias_dur = 0
        self.dash_time = 0
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterPounceBase, self).on_init_complete()
        self.register_pounce_callbacks()
        if self.use_bias:
            self.bias_dur = self.sd.ref_bias_dur

    def register_pounce_callbacks(self):
        self.register_substate_callback(self.S_DASH_PRE, 0, self.start_dash_pre)
        self.register_substate_callback(self.S_DASH_PRE, self.pre_dash_anim_dur / self.pre_dash_anim_rate, self.end_dash_pre)
        self.register_substate_callback(self.S_DASH, 0, self.start_dash)
        self.register_substate_callback(self.S_DASH, self.max_dash_time, self.end_dash)
        self.register_substate_callback(self.S_DASH_BAC, 0, self.start_dash_bac)
        self.register_substate_callback(self.S_DASH_BAC, self.bac_dash_anim_dur / self.bac_dash_anim_rate, self.end_dash_bac)

    def start_dash_pre(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.start_focus()
        self.delay_call(self.focus_time, self.end_focus)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_dash_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_dash_anim, LOW_BODY, 1)
        if self.sub_state == self.S_DASH_PRE and self.focus_tag:
            if self.use_bias:
                self.send_event('E_CTRL_FACE_TO', get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur), False)
            else:
                self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def end_dash_pre(self):
        self.reset_sub_states_callback()
        self.register_pounce_callbacks()
        start_land_ts = self.dash_time - self.land_anim_dur / self.land_anim_rate
        if start_land_ts > 0:
            self.register_substate_callback(self.S_DASH, start_land_ts, self.start_land)
        self.sub_state = self.S_DASH

    def start_dash(self):
        if self.focus_tag:
            self.end_focus()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        if self.dash_anim:
            self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 1, loop=True)
        self.init_dash()
        start_land_ts = self.dash_time - self.land_anim_dur / self.land_anim_rate
        if start_land_ts < 0:
            self.start_land()

    def end_dash(self):
        self.sub_state = self.S_DASH_BAC
        self.send_event('E_CLEAR_SPEED')
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        if self.end_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.end_aoe_skill_id)

    def start_land(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.land_anim_rate)
        if self.land_anim:
            self.send_event('E_POST_ACTION', self.land_anim, LOW_BODY, 1)

    def start_dash_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_dash_anim_rate)
        if self.bac_dash_anim:
            self.send_event('E_POST_ACTION', self.bac_dash_anim, LOW_BODY, 1)
        if self.end_aoe_skill_id_2:
            self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.end_aoe_skill_id_2, self.post_data()), False, True)

    def end_dash_bac(self):
        self.sub_state = self.S_END

    def init_dash(self):
        dash_dir = self.focus_pos - self.ev_g_position()
        dash_hrz_dis = math3d.vector(dash_dir.x, 0, dash_dir.z).length
        dash_time = dash_hrz_dis / self.dash_speed
        if dash_time > self.max_dash_time:
            dash_time = self.max_dash_time
        air_time = dash_time * 0.5
        vertical_speed = abs(air_time * self.gravity)
        self.dash_time = dash_time
        dash_dir.normalize()
        tar_dir = dash_dir * self.dash_speed
        self.send_event('E_SET_WALK_DIRECTION', tar_dir)
        self.send_event('E_GRAVITY', self.gravity)
        self.send_event('E_JUMP', vertical_speed)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)

    def on_ground(self, *args):
        self.end_dash()

    def enter(self, leave_states):
        super(MonsterPounceBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_DASH_PRE

    def update(self, dt):
        super(MonsterPounceBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        super(MonsterPounceBase, self).exit(enter_states)
        self.sub_state = self.S_END
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterPounceBase, self).destroy()

    def start_focus(self):
        self.focus_tag = True

    def end_focus(self):
        self.calc_focus_pos()
        self.focus_tag = False

    def calc_focus_pos(self):
        cur_pos = self.ev_g_position()
        if self.use_bias:
            tar_pos = get_bias_aim_pos(self.target_id, self.target_pos, False, self.bias_dur)
        else:
            tar_pos = get_aim_pos(self.target_id, self.target_pos, False)
        diff = tar_pos - cur_pos
        tar_dir = diff
        tar_dir.normalize()
        self.focus_pos = tar_pos - tar_dir * self.focus_dis
        dash_dir = self.focus_pos - cur_pos
        dash_hrz_dir = math3d.vector(dash_dir.x, 0, dash_dir.z)
        dash_hrz_distance = dash_hrz_dir.length
        dash_time = dash_hrz_distance / self.dash_speed
        if dash_time > self.max_dash_time:
            dash_time = self.max_dash_time
            dash_hrz_dir.normalize()
            sfx_pos = cur_pos + dash_hrz_dir * self.dash_speed * dash_time
        else:
            sfx_pos = self.focus_pos
        self.dash_time = dash_time
        self.create_warn_sfx(self.sid, sfx_pos)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_POUNCE_WARN_SFX, (self.sid, (sfx_pos.x, sfx_pos.y, sfx_pos.z), True)], True)

    def create_warn_sfx(self, sid, pos, is_sync=False):
        if sid != self.sid:
            return
        sfx_pos = is_sync or pos if 1 else math3d.vector(*pos)
        if self.warn_sfx:

            def cb(sfx):
                sfx.scale = math3d.vector(self.warn_sfx_scale, self.warn_sfx_scale, self.warn_sfx_scale)
                sfx.frame_rate = self.warn_sfx_rate

            global_data.sfx_mgr.create_sfx_in_scene(self.warn_sfx, sfx_pos, on_create_func=cb)

    def post_data(self):
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.end_aoe_skill_socket, 1)
        pos = mat.translation
        data = ((pos.x, pos.y, pos.z),)
        return data


class MonsterPounce(MonsterPounceBase):

    def init_params(self):
        super(MonsterPounce, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015154)
        self.focus_time = self.custom_param.get('focus_time', 0.6)
        self.focus_dis = self.custom_param.get('focus_dis', 7.0) * NEOX_UNIT_SCALE
        self.use_bias = self.custom_param.get('use_bias', False)
        self.dash_speed = self.custom_param.get('dash_speed', 2000)
        self.max_dash_time = self.custom_param.get('max_dash_time', 2.0)
        self.gravity = self.custom_param.get('gravity', 1000)
        self.pre_dash_anim = self.custom_param.get('pre_dash_anim', 'attack_04')
        self.pre_dash_anim_dur = self.custom_param.get('pre_dash_anim_dur', 1.2)
        self.pre_dash_anim_rate = self.custom_param.get('pre_dash_anim_rate', 1.0)
        self.dash_anim = self.custom_param.get('dash_anim', 'run')
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.land_anim = self.custom_param.get('land_anim', None)
        self.land_anim_dur = self.custom_param.get('land_anim_dur', 0)
        self.land_anim_rate = self.custom_param.get('land_anim_rate', 1.0)
        self.bac_dash_anim = self.custom_param.get('bac_dash_anim', 'hit')
        self.bac_dash_anim_dur = self.custom_param.get('bac_dash_anim_dur', 0.7)
        self.bac_dash_anim_rate = self.custom_param.get('bac_dash_anim_rate', 1.0)
        self.warn_sfx = self.custom_param.get('warn_sfx', None)
        self.warn_sfx_scale = self.custom_param.get('warn_sfx_scale', 1.0)
        self.warn_sfx_rate = self.custom_param.get('warn_sfx_rate', 1.0)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.end_aoe_skill_id_2 = self.custom_param.get('end_aoe_skill_id_2', None)
        self.end_aoe_skill_socket = self.custom_param.get('end_aoe_skill_socket', 'fx_root')
        self.aim_turn = self.custom_param.get('aim_turn', True)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.sd.ref_bias_dur
            self.reset_sub_states_callback()
            self.register_pounce_callbacks()