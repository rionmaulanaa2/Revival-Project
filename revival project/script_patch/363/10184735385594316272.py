# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8013.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
import logic.gcommon.common_utils.bcast_utils as bcast
import weakref
import world
import math3d
FIRE_EFFECT_KEY = 'fire'
ACCUMULATE_ARROW_STATE_ID = 'accumulate_arrow'
ACCUMULATE_ARROW_EFFECT_ID_MAP = {-1: '',
   0: '3',
   1: '5',
   2: '7'
   }
ACCUMULATE_BOW_STATE_ID = 'accumulate_bow'
ACCUMULATE_BOW_EFFECT_ID_MAP = {-1: '',
   0: '4',
   1: '6',
   2: '8'
   }
SEQUENCE_ARROW_STATE_ID = 'sequence_arrow'
SEQUENCE_ARROW_EFFECT_ID_MAP = {True: '9',
   False: ''
   }
SHOOT_ARROW_STATE_ID = 'shoot_arrow'
SHOOT_ARROW_EFFECT_ID_MAP = {801301: '10',
   801302: '11',
   801303: '12',
   801304: '13',
   801309: '10',
   801310: '11',
   801311: '12'
   }
HOOK_MODEL_EFFECT_ID = '14'
HOOK_DETECT_EFFECT_ID = '15'
HOOK_HIT_EFFECT_ID = '16'
ANIM_FASHE = 'fashe'
ANIM_SHOUHUI = 'back'
MAIN_WEAPONS = {
 PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN3}

class ComMechaEffect8013(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_MECHA_LOD_LOADED_FIRST': 'on_lod_loaded_first',
       'E_HOOK_MODEL_START': 'on_hook_model_start',
       'E_CREATE_HOOK_DETECT_EFFECT': 'on_create_hook_detect_effect',
       'E_CREATE_HOOK_HIT_EFFECT': 'on_create_hook_hit_effect',
       'E_ACCUMULATE_DURATION_CHANGED': 'on_accumulate_duration_changed',
       'E_ACCUMULATE_DURATION_CHANGED_NOTIFY_EFFECT_ONLY': 'on_accumulate_duration_changed',
       'E_ATTACK_END': 'on_attack_end',
       'E_SET_SECOND_WEAPON_ATTACK': 'on_second_weapon_attack',
       'E_GUN_ATTACK': 'on_gun_attack_start'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8013, self).init_from_dict(unit_obj, bdict)
        self.model_ref = None
        self.hook_model = None
        self.is_second_weapon_attack = False
        self.accumulate_bow_level = -1
        self.accumulate_arrow_level = -1
        self.need_refresh_bow_effect = False
        self.cur_hook_anim_name = ''
        self.target_pos = None
        self.rush_time = 0
        self.hook_max_time = 0
        self.hook_max_distance = 0
        self.cur_hook_time = 0
        self.hook_elapsed_time = 0
        self.rush_elapsed_time = 0
        return

    def destroy(self):
        super(ComMechaEffect8013, self).destroy()
        self.model_ref = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8013, self).on_model_loaded(model)
        self.model_ref = weakref.ref(model)

    def on_lod_loaded_first(self):

        def create_cb(model, *args):
            if self.model_ref is None:
                return
            else:
                mecha_model = self.model_ref()
                if not mecha_model or not mecha_model.valid:
                    return
                self.hook_model = model
                mecha_model.bind('hook', self.hook_model, world.BIND_TYPE_TRANSLATE)
                self.hook_model.visible = False
                self.hook_model.inherit_flag &= ~world.INHERIT_VISIBLE
                return

        self.on_trigger_hold_effect(HOOK_MODEL_EFFECT_ID, create_cb=create_cb)

    def disable_hook_model(self):
        if not self.hook_model:
            return
        self.hook_model.visible = False
        self.need_update = False
        self.cur_hook_anim_name = ''

    def on_hook_model_start(self, target_pos, rush_time, hook_max_time, hook_max_distance):
        self.rush_time = rush_time
        self.hook_max_time = hook_max_time
        self.hook_max_distance = hook_max_distance
        if type(target_pos) == tuple or type(target_pos) == list:
            self.target_pos = math3d.vector(*target_pos)
        else:
            self.target_pos = target_pos
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_HOOK_MODEL_START,
         (
          (
           self.target_pos.x, self.target_pos.y, self.target_pos.z), self.rush_time, self.hook_max_time, self.hook_max_distance)], True)
        if self.model_ref is None:
            return
        else:
            model = self.model_ref()
            if not model or not model.valid:
                return
            if not self.hook_model:
                return
            start_pos = self.hook_model.world_position
            dir_vec = self.target_pos - start_pos
            if dir_vec.is_zero:
                return
            self.hook_model.visible = True
            self.play_hook_release_ani()
            self.need_update = True
            return

    def play_hook_release_ani(self):
        start_pos = self.hook_model.world_position
        self.update_forward()
        dir_vec = self.target_pos - start_pos
        distance = dir_vec.length
        hook_time = self.hook_max_time / self.hook_max_distance * distance
        ctrl = self.hook_model.get_anim_ctrl(1)
        total_time = ctrl.get_anim_length(ANIM_FASHE) * 0.001
        if hook_time == 0:
            rate_scale = 5.0
        else:
            rate_scale = total_time / hook_time
        ctrl.play_animation(ANIM_FASHE, -1, 0, 0.0, 0, rate_scale)
        self.cur_hook_anim_name = ANIM_FASHE
        self.rush_elapsed_time = 0
        self.hook_elapsed_time = 0
        self.cur_hook_time = hook_time
        model_scalel = distance / 1330
        self.hook_model.scale = math3d.vector(1.0, 1.0, model_scalel)
        if not self.ev_g_is_avatar():
            m_mat = self.hook_model.world_rotation_matrix
            dir_vec.normalize()
            self.hook_model.world_rotation_matrix = m_mat.make_rotation_x(dir_vec.pitch) * m_mat.make_rotation_y(dir_vec.yaw)

    def play_hook_recover_ani(self):
        self.cur_hook_anim_name = ANIM_SHOUHUI

    def update_forward(self):
        if not self.hook_model or not self.target_pos:
            return
        else:
            forward = self.target_pos - self.hook_model.world_position
            if forward.is_zero:
                return
            forward.normalize()
            if self.model_ref is None:
                return
            macha_model = self.model_ref()
            m_mat = macha_model.world_rotation_matrix
            self.hook_model.world_rotation_matrix = m_mat.make_rotation_x(forward.pitch) * m_mat.make_rotation_y(forward.yaw)
            if self.cur_hook_anim_name == ANIM_SHOUHUI:
                dir_vec = self.target_pos - self.hook_model.world_position
                distance = dir_vec.length
                model_scalel = distance / 1330
                self.hook_model.scale = math3d.vector(1.0, 1.0, model_scalel)
            return

    def tick(self, delta):
        if not self.hook_model:
            return
        self.update_forward()
        if self.cur_hook_anim_name == ANIM_FASHE:
            self.hook_elapsed_time += delta
            if self.hook_elapsed_time >= self.cur_hook_time:
                self.play_hook_recover_ani()
        elif self.cur_hook_anim_name == ANIM_SHOUHUI:
            self.rush_elapsed_time += delta
            if self.rush_elapsed_time >= self.rush_time:
                self.disable_hook_model()

    def on_create_hook_detect_effect(self, create_cb):
        self.on_trigger_hold_effect(HOOK_DETECT_EFFECT_ID, create_cb=create_cb)

    def on_create_hook_hit_effect(self, create_cb):
        self.on_trigger_hold_effect(HOOK_HIT_EFFECT_ID, create_cb=create_cb)

    def on_accumulate_duration_changed(self, weapon_pos, accumulate_duration, touch_accumulate_time, force_trigger=False):
        force_full_shoot_cnt = self.ev_g_add_attr('force_full_shoot_cnt')
        if (self.is_second_weapon_attack or accumulate_duration < 0.18 or weapon_pos not in MAIN_WEAPONS) and not force_trigger and not force_full_shoot_cnt:
            return
        weapon = self.unit_obj.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not weapon:
            return
        cur_energy = force_full_shoot_cnt or self.unit_obj.ev_g_accumulate_duration(weapon_pos) if 1 else 999
        cur_accumulate_level = weapon.get_accumulate_level(cur_energy)
        if cur_accumulate_level != self.accumulate_bow_level or self.need_refresh_bow_effect:
            self.accumulate_bow_level = cur_accumulate_level
            self.on_trigger_state_effect(ACCUMULATE_BOW_STATE_ID, ACCUMULATE_BOW_EFFECT_ID_MAP[cur_accumulate_level], need_sync=True)
            self.need_refresh_bow_effect = False
        if touch_accumulate_time > 0.0:
            accumulate_arrow_level = cur_accumulate_level
        else:
            accumulate_arrow_level = -1
        if accumulate_arrow_level != self.accumulate_arrow_level:
            self.accumulate_arrow_level = accumulate_arrow_level
            self.on_trigger_state_effect(ACCUMULATE_ARROW_STATE_ID, ACCUMULATE_ARROW_EFFECT_ID_MAP[cur_accumulate_level], need_sync=True)

    def on_attack_end(self, *args):
        if len(args) > 0:
            weapon_pos = args[0]
            if weapon_pos in MAIN_WEAPONS:
                self.accumulate_bow_level = -1
                self.on_trigger_state_effect(ACCUMULATE_BOW_STATE_ID, ACCUMULATE_BOW_EFFECT_ID_MAP[-1])
                self.accumulate_arrow_level = -1
                self.on_trigger_state_effect(ACCUMULATE_ARROW_STATE_ID, ACCUMULATE_ARROW_EFFECT_ID_MAP[-1])
            elif weapon_pos == PART_WEAPON_POS_MAIN2:
                self.on_trigger_state_effect(SEQUENCE_ARROW_STATE_ID, SEQUENCE_ARROW_EFFECT_ID_MAP[False], need_sync=True)

    def on_second_weapon_attack(self, flag):
        self.is_second_weapon_attack = flag
        if flag:
            self.on_trigger_state_effect(ACCUMULATE_BOW_STATE_ID, ACCUMULATE_BOW_EFFECT_ID_MAP[-1], need_sync=True)
            self.on_trigger_state_effect(SEQUENCE_ARROW_STATE_ID, SEQUENCE_ARROW_EFFECT_ID_MAP[flag], need_sync=True)
        else:
            self.need_refresh_bow_effect = True

    def on_gun_attack_start(self, socket_name, weapon_pos):
        obj_weapon = self.unit_obj.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        if not obj_weapon:
            return
        cur_energy = self.ev_g_last_accumulate_duration(weapon_pos)
        weapon_id = obj_weapon.get_accumulate_weapon_id(cur_energy)
        if weapon_id not in SHOOT_ARROW_EFFECT_ID_MAP:
            return
        self.on_trigger_state_effect(SHOOT_ARROW_STATE_ID, SHOOT_ARROW_EFFECT_ID_MAP[weapon_id], force=True, need_sync=True)