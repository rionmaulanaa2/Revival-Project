# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8031.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import SOUND_TYPE_MECHA_FIRE
import logic.gcommon.common_utils.bcast_utils as bcast
from common.utils.timer import CLOCK
import math3d
import world
DASH_EFFECT_ID = '100'
REAPER_SHAPE_STATE_ID = 'reaper'
REAPER_SHAPE_EFFECT_ID_MAP = {True: '101',
   False: '102'
   }
UP_VECTOR = math3d.vector(0, 1, 0)
BLADE_SLASH_HIT_EFFECT_ID = '105'
BLADE_SLASH_HIT_SCREEN_EFFECT_ID = '106'
BLADE_HIT_STATE_ID = 'hit_effect'
SLASH_HIT_SOUND_NAME = [
 'm_8031_sickle_hit', 'nf']
TELEPORT_GUIDE_EFFECT_ID = '109'
TELEPORT_SHADOW_EFFECT_ID = '110'
SHADOW_SOUND_NAME = 'm_8031_rage_buff_3p'
ENEMY_TELEPORT_GUIDE_EFFECT_ID = '112'
ENEMY_TELEPORT_SHADOW_EFFECT_ID = '113'
DASH_CURE_STATE_ID = 'cure'
DASH_CURE_EFFECT_ID = '114'
BLADE_SLASH_EXECUTE_EFFECT_ID = '115'

class ComMechaEffect8031(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PLAY_DASH_EFFECT': 'on_play_dash_effect',
       'E_SHOW_REAPER_SHAPE_EFFECT': 'show_refresh_reaper_shape_effect',
       'E_SHOW_SLASH_HIT_SFX': 'on_show_blade_slash_hit_sfx',
       'E_SHOW_SLASH_HIT_SCREEN_SFX': 'on_show_blade_slash_hit_screen_sfx',
       'E_SHOW_TELEPORT_SHADOW_SFX': 'show_teleport_shadow_sfx',
       'E_SHOW_TELEPORT_GUIDE_SFX': 'show_teleport_guide_sfx',
       'E_SHOW_DASH_CURE_SFX': 'show_dash_cure_sfx',
       'E_DO_EXECUTE_APPEARANCE': 'show_execute_sfx'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8031, self).init_from_dict(unit_obj, bdict)
        self.dash_sfx = None
        self.dash_event_registered = False
        self.guide_start_pos = None
        self.guide_end_pos = None
        return

    def _remove_dash_effect(self):
        if self.dash_sfx:
            global_data.sfx_mgr.remove_sfx(self.dash_sfx)
            self.dash_sfx = None
        return

    def destroy(self):
        super(ComMechaEffect8031, self).destroy()
        self._process_dash_event(False)
        self._remove_dash_effect()

    def update_dash_sfx_pos(self, *args):
        model = self.ev_g_model()
        if model:
            pos = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD).translation
            self.dash_sfx.position = pos
            if self.dash_sfx_direction is None:
                self.dash_sfx.rotation_matrix = model.rotation_matrix
        return

    def _process_dash_event(self, flag):
        if self.dash_event_registered ^ flag:
            if flag:
                if G_POS_CHANGE_MGR:
                    self.regist_pos_change(self.update_dash_sfx_pos)
                else:
                    self.regist_event('E_POSITION', self.update_dash_sfx_pos)
            elif G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.update_dash_sfx_pos)
            else:
                self.unregist_event('E_POSITION', self.update_dash_sfx_pos)
            self.dash_event_registered = flag

    def dash_sfx_create_callback(self, sfx):
        if not self.is_valid():
            return
        else:
            self._process_dash_event(True)
            self.dash_sfx = sfx
            self.update_dash_sfx_pos()
            if self.dash_sfx_direction is not None:
                sfx.rotation_matrix = math3d.matrix.make_orient(math3d.vector(*self.dash_sfx_direction), UP_VECTOR)
            return

    def dash_sfx_remove_callback(self, sfx):
        if not self.is_valid():
            return
        else:
            self._process_dash_event(False)
            self.dash_sfx = None
            return

    def on_play_dash_effect(self, flag, direction=None):
        if flag:
            self.dash_sfx_direction = direction
            self.on_trigger_hold_effect(DASH_EFFECT_ID, self.dash_sfx_create_callback, self.dash_sfx_remove_callback)
        else:
            self._remove_dash_effect()
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_DASH_EFFECT, (flag, direction)], True)

    def show_refresh_reaper_shape_effect(self, flag):
        self.on_trigger_state_effect('reaper', REAPER_SHAPE_EFFECT_ID_MAP[flag], need_sync=True)

    def on_show_blade_slash_hit_sfx(self, pos, rot=None):
        self.on_trigger_disposable_effect(BLADE_SLASH_HIT_EFFECT_ID, pos, rot, need_sync=True)
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, SLASH_HIT_SOUND_NAME, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, SLASH_HIT_SOUND_NAME, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)

    def on_show_blade_slash_hit_screen_sfx(self):
        self.on_trigger_state_effect(BLADE_HIT_STATE_ID, BLADE_SLASH_HIT_SCREEN_EFFECT_ID, force=True, need_sync=True)

    def _is_campmate(self):
        return global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self.ev_g_camp_id())

    def show_teleport_shadow_sfx(self, pos, rot):
        effect_id = TELEPORT_SHADOW_EFFECT_ID if self._is_campmate() else ENEMY_TELEPORT_SHADOW_EFFECT_ID
        self.on_trigger_disposable_effect(effect_id, pos, rot, duration=0, need_sync=True)

    def on_teleport_guide_sfx_create_cb(self, sfx):
        model = self.ev_g_model()
        if model and self.is_valid():
            sfx.position = math3d.vector(*self.guide_start_pos)
            sfx.endpos_attach(model, 'part_point1')
        else:
            sfx.destroy()

    def show_teleport_guide_sfx(self, start_pos, end_pos):
        self.guide_start_pos = start_pos
        self.guide_end_pos = end_pos
        owner_id = self.unit_obj.id
        pos = math3d.vector(*start_pos)
        global_data.game_mgr.register_logic_timer(lambda : self.is_valid() and global_data.sound_mgr.play_sound_optimize(SHADOW_SOUND_NAME, owner_id, pos, (SHADOW_SOUND_NAME, 'nf')), interval=1.2, times=1, mode=CLOCK)
        effect_id = TELEPORT_GUIDE_EFFECT_ID if self._is_campmate() else ENEMY_TELEPORT_GUIDE_EFFECT_ID
        self.on_trigger_hold_effect(effect_id, self.on_teleport_guide_sfx_create_cb)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_TELEPORT_GUIDE_SFX, (start_pos, end_pos)], True)

    def show_dash_cure_sfx(self):
        self.on_trigger_state_effect(DASH_CURE_STATE_ID, DASH_CURE_EFFECT_ID, force=True, need_sync=True)

    def show_execute_sfx(self, execute_target_eid):
        entity = global_data.battle.get_entity(execute_target_eid)
        if entity and entity.logic:
            pos = entity.logic.ev_g_position()
            pos = (pos.x, pos.y, pos.z)
            self.on_trigger_disposable_effect(BLADE_SLASH_EXECUTE_EFFECT_ID, pos, duration=0)