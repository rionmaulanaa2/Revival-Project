# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComHumanSound.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import world
import game3d
from logic.gcommon.common_const import animation_const
import time
from logic.gcommon.common_const import water_const

class ComHumanSound(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete'
       }
    MIN_FOOT_SOUND_PASS_TIME = 0.2

    def __init__(self):
        super(ComHumanSound, self).__init__()
        self.sound_mgr = global_data.sound_mgr
        self._last_foot_sound = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanSound, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        pass

    def on_load_animator_complete(self, *args):
        self._register_sound_event()

    def _register_sound_event(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        import data.weapon_action_config as weapon_action_config
        source_register_dict = {}
        key_dict = {animation_const.SOUND_TYPE_WALK: ('stand_move', 'stand_shoot_move', 'skate_stand_shoot_move', 'squat_move'),
           animation_const.SOUND_TYPE_RUN: ('run_stage_2', 'run_stage_3', 'squat_run')
           }
        model = self.ev_g_model()
        if not model:
            return
        animtion_event = self.ev_g_all_animtion_event()
        for vary_animation in six_ex.values(weapon_action_config.weapon_type_2_action):
            for sound_type, key_list in six.iteritems(key_dict):
                for key in key_list:
                    move_animation = vary_animation[key]
                    for clip_name in move_animation:
                        if clip_name not in source_register_dict:
                            index = 1
                            step_list = []
                            while 'step%d' % index in animtion_event.get(clip_name, []):
                                step_list.append('step%d' % index)
                                index += 1

                            if step_list:
                                animator.add_trigger_clip(clip_name, step_list, self._foot_on_ground_event, sound_type)
                            source_register_dict[clip_name] = True

        special_anim_list = self.ev_g_convert_str_to_anim_list('4,c_ak_move')
        for clip_name in special_anim_list:
            index = 1
            while 'step%d' % index in animtion_event.get(clip_name, []):
                if global_data.enable_animator_reg_event and animator:
                    animator.add_trigger_clip(clip_name, 'step%d' % index, self._foot_on_ground_event, animation_const.SOUND_TYPE_WALK)
                else:
                    model.register_anim_key_event(clip_name, 'step%d' % index, self._foot_on_ground_event, animation_const.SOUND_TYPE_WALK)
                index += 1

            source_register_dict[clip_name] = True

        extent_anim_list = ('dying_move', )
        for clip_name in extent_anim_list:
            index = 1
            while 'step%d' % index in animtion_event.get(clip_name, []):
                if global_data.enable_animator_reg_event and animator:
                    animator.add_trigger_clip(clip_name, 'step%d' % index, self._foot_on_ground_event, animation_const.SOUND_TYPE_WALK)
                else:
                    model.register_anim_key_event(clip_name, 'step%d' % index, self._foot_on_ground_event, animation_const.SOUND_TYPE_WALK)
                index += 1

            source_register_dict[clip_name] = True

    def _foot_on_ground_event(self, model, anim_name, key, data=None):
        now_time = time.time()
        pass_time = now_time - self._last_foot_sound
        if pass_time <= self.MIN_FOOT_SOUND_PASS_TIME:
            return
        else:
            self._last_foot_sound = now_time
            water_status = self.sd.ref_water_status
            if water_status is not None and water_status != water_const.WATER_NONE and water_status != water_const.WATER_DEEP_LEVEL:
                self.send_event('E_FOOT_ON_WATER', model, anim_name, key, data)
            self.send_event('E_PLAY_FOOTSTEP_SOUND', data)
            return

    def destroy(self):
        super(ComHumanSound, self).destroy()