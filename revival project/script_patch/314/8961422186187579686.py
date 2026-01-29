# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossRangePounceLogic.py
from __future__ import absolute_import
from .PVEMonsterPounceLogic import MonsterPounceBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos, get_bias_aim_pos
import world
from common.cfg import confmgr
from logic.gutils.weapon_utils import recheck_pve_fire_dir
from logic.gcommon.common_const.idx_const import ExploderID
from random import choice
from math import radians
from logic.gcommon.common_const.weapon_const import WP_SWORD_LIGHT
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN

class BossRangePounceBase(MonsterPounceBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_SET_LEADER_STATE': 'set_leader_state'
       }
    econf = {}

    def set_leader_state(self, t_state, l_state, skill_id, *args):
        if t_state != self.sid:
            return
        self.leader_state = l_state
        self.leader_skill_id = skill_id
        self.target_id, self.target_pos = args

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
            self.leader_state = None
            self.leader_skill_id = None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BossRangePounceBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_bias(bdict)

    def init_params(self):
        super(BossRangePounceBase, self).init_params()
        self.fire_bias_dur = 0
        self.leader_state = None
        self.leader_skill_id = None
        return

    def init_bias(self, bdict):
        level = bdict.get('pve_monster_level', None)
        if level:
            level_conf = confmgr.get('monster_level_data', str(bdict.get('npc_id')), 'Content', str(level))
            self.fire_bias_dur = level_conf.get('Fire_Bias_Dur', 0)
        return

    def start_dash_pre(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.start_focus()
        self.delay_call(self.focus_time, self.end_focus)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_dash_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_dash_anim, LOW_BODY, 1)
        if self.sub_state == self.S_DASH_PRE and self.focus_tag and self.pre_face_to_tag:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(None, self.target_pos), False)
        return

    def start_land(self):
        super(BossRangePounceBase, self).start_land()
        self.delay_call(self.fire_ts, self.open_fire)

    def calc_focus_pos(self):
        cur_pos = self.ev_g_position()
        tar_pos = get_aim_pos(None, self.target_pos, False)
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
        return

    def enter(self, *args):
        super(MonsterPounceBase, self).enter(*args)
        if self.leader_state:
            pass
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_DASH_PRE

    def update(self, dt):
        super(BossRangePounceBase, self).update(dt)
        if self.sub_state in (self.S_DASH, self.S_LAND, self.S_DASH_BAC):
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def exit(self, enter_states):
        super(MonsterPounceBase, self).exit(enter_states)
        self.sub_state = self.S_END
        if self.aim_turn:
            if self.leader_state:
                self.send_event('E_PVE_M_AIM_TURN', self.leader_state, self.leader_skill_id, self.target_id, self.target_pos)
            else:
                self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def open_fire(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        mat = model.get_socket_matrix(self.fire_socket, world.SPACE_TYPE_WORLD)
        if not mat:
            if global_data.is_inner_server:
                global_data.game_mgr.show_tip('%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xb5\x84\xe6\xba\x90\xe6\xb2\xa1\xe6\x9c\x89\xe8\xa1\xa8\xe9\x87\x8c\xe5\xa1\xab\xe7\x9a\x84\xe8\xbf\x99\xe4\xb8\xaa\xe5\xbc\x80\xe7\x81\xab\xe6\x8c\x82\xe8\x8a\x82\xe7\x82\xb9 %s' % (self.skill_id, self.fire_socket))
            import exception_hook
            msg = '%s \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x94\xbb\xe5\x87\xbb\xef\xbc\x9a\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xb5\x84\xe6\xba\x90\xe6\xb2\xa1\xe6\x9c\x89\xe8\xa1\xa8\xe9\x87\x8c\xe5\xa1\xab\xe7\x9a\x84\xe8\xbf\x99\xe4\xb8\xaa\xe5\xbc\x80\xe7\x81\xab\xe6\x8c\x82\xe8\x8a\x82\xe7\x82\xb9 %s' % (self.skill_id, self.fire_socket)
            exception_hook.post_stack(msg)
            return
        start_pos = mat.translation
        target_pos = get_bias_aim_pos(self.target_id, self.target_pos, True, self.fire_bias_dur)
        direction = target_pos - start_pos
        direction.normalize()
        wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        wp_kind = wp_conf.get('iKind')
        wp_cus_param = wp_conf.get('cCustomParam', {})
        owner = self.unit_obj.get_owner()
        fix_dir = recheck_pve_fire_dir(wp_cus_param, direction, 0, owner.get_monster_id(), owner.get_pve_monster_level(), self.wp_type)
        up = (0, 1, 0)
        if self.random_rotate_list:
            angle = choice(self.random_rotate_list)
            rad = radians(angle)
            rot_mat = math3d.matrix.make_rotation(math3d.vector(0, 0, 1), rad)
            ret = math3d.vector(0, 1, 0) * rot_mat
            up = (ret.x, ret.y, ret.z)
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': wp_kind,
           'position': (
                      start_pos.x, start_pos.y, start_pos.z),
           'dir': (
                 fix_dir.x, fix_dir.y, fix_dir.z),
           'up': up,
           'sub_idx': 0
           }
        if wp_kind == WP_SWORD_LIGHT:
            throw_item.update({'col_width': wp_cus_param.get('energy_width', 9)
               })
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class BossRangePounce(BossRangePounceBase):

    def init_params(self):
        super(BossRangePounce, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015154)
        self.focus_time = self.custom_param.get('focus_time', 0.6)
        self.focus_dis = self.custom_param.get('focus_dis', 7.0) * NEOX_UNIT_SCALE
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
        self.fire_ts = self.custom_param.get('fire_ts', 0)
        self.fire_socket = self.custom_param.get('fire_socket', '')
        self.wp_type = self.custom_param.get('wp_type', 0)
        self.random_rotate_list = self.custom_param.get('random_rotate_list', [])
        self.pre_face_to_tag = self.custom_param.get('pre_face_to_tag', True)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.sd.ref_bias_dur
            self.reset_sub_states_callback()
            self.register_pounce_callbacks()