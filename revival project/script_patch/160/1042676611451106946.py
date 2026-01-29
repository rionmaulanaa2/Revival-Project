# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8030.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
import math3d
import world
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_9
from logic.gcommon.const import NEOX_UNIT_SCALE
JUMP_CHARGE_EFFECT_ID = '101'
EXTERN_BONE_STATE_ID = 'extern_bone'
JUMP_EFFECT_ID = '102'
JUMP_STATE_ID = 'jump'
JUMP_END_EFFECT_ID = '103'
JUMP_END_STATE_ID = 'jump_end'
ENHANCE_JUMP_EFFECT_ID = '104'
ENHANCE_JUMP_END_EFFECT_ID = '105'
TAIL_EFFECT_ID = '106'
TAIL_STATE_ID = 'tail'
GHOST_EFFECT_ID = '107'
DASH_END_EFFECT_ID = '108'
DASH_END_EXTERN_BONE_EFFECT_ID = '109'

class ComMechaEffect8030(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_EXTERN_BONE_EFFECT': 'show_extern_bone_effect',
       'E_SET_JUMP_EFFECT_ENHANCE': 'set_jump_effect_enhance',
       'E_SHOW_TAIL_EFFECT': 'show_tail_effect'
       })

    def __init__(self, need_update=False):
        super(ComMechaEffect8030, self).__init__(need_update)
        self.jump_sfx_showed = False
        self.jump_effect_id = JUMP_EFFECT_ID
        self.jump_end_effect_id = JUMP_END_EFFECT_ID
        self.cur_extern_bone_effect_id = ''
        self.start_jump_pos = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8030, self).on_model_loaded(model)
        if self.ev_g_is_avatar():
            model.register_anim_key_event('jump_03', 'start', lambda *args: self.show_jump_sfx(True))

    def _trigger_extern_bone_effect(self, effect_id, force=True):
        self.on_trigger_state_effect(EXTERN_BONE_STATE_ID, effect_id, force=force, need_sync=True)
        self.cur_extern_bone_effect_id = effect_id

    def show_extern_bone_effect(self, effect_id, end=False):
        if end:
            if self.cur_extern_bone_effect_id == effect_id:
                self._trigger_extern_bone_effect('', force=False)
        else:
            self._trigger_extern_bone_effect(effect_id)

    def set_jump_effect_enhance(self, enhance):
        self.jump_effect_id = ENHANCE_JUMP_EFFECT_ID if enhance else JUMP_EFFECT_ID
        self.jump_end_effect_id = ENHANCE_JUMP_END_EFFECT_ID if enhance else JUMP_END_EFFECT_ID

    def show_jump_sfx(self, show_sfx):
        effect_id = self.jump_effect_id if show_sfx else ''
        if effect_id != self.jump_sfx_showed:
            self.jump_sfx_showed = effect_id
            self._trigger_extern_bone_effect(effect_id)
            self.jump_effect_id = JUMP_EFFECT_ID
            if show_sfx:
                self.need_update = True
            else:
                self._trigger_extern_bone_effect(self.jump_end_effect_id)
        if show_sfx:
            self.start_jump_pos = self.ev_g_position()
        else:
            end_pos = self.ev_g_position()
            if end_pos and self.start_jump_pos:
                dist = int((self.start_jump_pos - end_pos).length)
                dist > 0 and self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', (
                 '8030', MECHA_MEMORY_LEVEL_9, dist / NEOX_UNIT_SCALE), False, True)
            self.start_jump_pos = None
        return

    def tick(self, delta):
        if not self.ev_g_is_avatar():
            self.need_update = False
            return
        need_update = False
        if self.jump_sfx_showed:
            character = self.sd.ref_character
            if not character or not character.valid or not character.isActive() or character.verticalVelocity <= 0:
                self.show_jump_sfx(False)
            else:
                need_update = True
        self.need_update = need_update

    def show_tail_effect(self, start_pos, dash_dir):
        up = math3d.vector(0, 1, 0)
        mtx = math3d.matrix.make_orient(dash_dir, up)
        rot = math3d.matrix_to_rotation(mtx)
        rot = (rot.x, rot.y, rot.z, rot.w)
        self.on_trigger_state_effect(TAIL_STATE_ID, TAIL_EFFECT_ID, force=True, rot=rot, need_sync=True)
        self.on_trigger_disposable_effect(GHOST_EFFECT_ID, (start_pos.x, start_pos.y, start_pos.z), need_sync=True)