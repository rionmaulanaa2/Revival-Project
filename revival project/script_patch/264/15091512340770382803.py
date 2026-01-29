# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbySoundEffect.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import SEX_FEMALE
from common.cfg import confmgr
import time

class ComLobbySoundEffect(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded'
       }
    MIN_FOOT_SOUND_PASS_TIME = 0.2

    def __init__(self):
        super(ComLobbySoundEffect, self).__init__()
        self._last_foot_sound = 0
        self.sound_event_name = 'Play_footstep'

    def on_model_loaded(self, *args):
        role_id = self.ev_g_role_id()
        role_sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex')
        self.sound_event_name = 'Play_footstep' if role_sex == SEX_FEMALE else 'Play_footstep_male'
        self.register_sound_event()

    def register_sound_event(self):
        model = self.ev_g_model()
        if not model:
            return
        animator = self.ev_g_animator()
        for clip_name in model.get_anim_names():
            for trigger_name in ['step1', 'step2']:
                if model.has_anim_event(clip_name, trigger_name):
                    if global_data.enable_animator_reg_event and animator:
                        animator.add_trigger_clip(clip_name, trigger_name, self.foot_on_ground_event)
                    else:
                        model.register_anim_key_event(clip_name, trigger_name, self.foot_on_ground_event)

    def foot_on_ground_event(self, *args):
        now_time = time.time()
        pass_time = now_time - self._last_foot_sound
        if pass_time <= self.MIN_FOOT_SOUND_PASS_TIME:
            return
        self._last_foot_sound = now_time
        model = self.ev_g_model()
        if model:
            pos = model.world_position
            global_data.sound_mgr.play_sound(self.sound_event_name, pos, ('fs_type',
                                                                          'walk'), ('materials',
                                                                                    'stone'))