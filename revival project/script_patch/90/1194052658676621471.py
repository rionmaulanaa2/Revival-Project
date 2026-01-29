# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8007.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import weakref
INJURY_DECREASE_STATE_ID = 'injury_decrease'
INJURY_DECREASE_EFFECT_ID_MAP = {True: '14',
   False: ''
   }
VISUAL_PATH_EFFECT_ID = '15'
TELEPORT_POSITION_EFFECT_ID = '16'

class ComMechaEffect8007(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_SHOW_VISUAL_PATH': 'on_show_visual_path',
       'E_HIDE_VISUAL_PATH': 'on_hide_visual_path',
       'E_SHOW_INJURY_DECREASE_EFFECT': 'on_show_injury_decrease_effect',
       'G_SHOW_TELEPORT_POSITION_EFFECT': 'on_show_teleport_position_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8007, self).init_from_dict(unit_obj, bdict)
        self.visual_effect = None
        self.start_pos = None
        self.end_pos = None
        self.cur_pos = None
        self.speed = math3d.vector(0, 0, 0)
        self.elapsed_time = 0
        self.total_time = 1
        self.model_ref = None
        self.shadow_stay_time = 0.3
        return

    def destroy(self):
        super(ComMechaEffect8007, self).destroy()
        self.model_ref = None
        self.need_update = False
        if self.visual_effect:
            global_data.sfx_mgr.remove_sfx(self.visual_effect)
            self.visual_effect = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8007, self).on_model_loaded(model)
        model.register_anim_key_event('teleport_03', 'hide', self.hide_model)
        model.register_anim_key_event('teleport_04', 'start', self.show_model)
        self.model_ref = weakref.ref(model)

    def hide_model(self, *args):
        model = self.model_ref()
        if model and model.valid:
            model.visible = False
        global_data.game_mgr.delay_exec(0.4, self.show_model)

    def show_model(self, *args):
        if not self.model_ref:
            return
        model = self.model_ref()
        if model and model.valid:
            model.visible = True

    def on_show_injury_decrease_effect(self, flag):
        self.on_trigger_state_effect(INJURY_DECREASE_STATE_ID, INJURY_DECREASE_EFFECT_ID_MAP[flag])

    def on_hide_visual_path(self):
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_HIDE_VISUAL_PATH, ()], True)
        self.need_update = False
        if self.visual_effect:
            global_data.sfx_mgr.remove_sfx(self.visual_effect)
            self.visual_effect = None
        return

    def on_show_visual_path(self, start_pos, end_pos, time, shadow_stay_time):
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_VISUAL_PATH, (start_pos, end_pos, time, shadow_stay_time)], True)
        self.start_pos = math3d.vector(*start_pos)
        self.end_pos = math3d.vector(*end_pos)
        self.total_time = time
        self.shadow_stay_time = shadow_stay_time
        dist = self.end_pos - self.start_pos
        self.speed = dist * (1.0 / time)

        def create_cb(sfx):
            if not self.is_valid() or not self.unit_obj or not self.unit_obj.is_valid():
                global_data.sfx_mgr.remove_sfx(sfx)
                return
            self.visual_effect = sfx
            self.start_move()

        self.on_trigger_hold_effect(VISUAL_PATH_EFFECT_ID, create_cb=create_cb)

    def start_move(self):
        self.need_update = True
        self.cur_pos = self.start_pos
        self.elapsed_time = 0
        direct = self.end_pos - self.cur_pos
        mat = math3d.matrix.make_orient(direct, math3d.vector(0, 1, 0))
        self.visual_effect.visible = True
        self.visual_effect.rotation_matrix = mat
        self.visual_effect.restart()

    def tick(self, delta):
        self.elapsed_time += delta
        if self.total_time - self.elapsed_time <= -self.shadow_stay_time:
            self.need_update = False
            if self.visual_effect and self.visual_effect.valid:
                self.visual_effect.visible = False
            return
        if self.total_time - self.elapsed_time > 0:
            self.cur_pos += self.speed * delta
            if self.visual_effect and self.visual_effect.valid:
                self.visual_effect.position = self.cur_pos

    def on_show_teleport_position_effect(self, create_cb):
        return self.on_trigger_hold_effect(TELEPORT_POSITION_EFFECT_ID, create_cb=create_cb)