# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8022.py
from __future__ import absolute_import
import six
from .ComGenericMechaEffect import ComGenericMechaEffect
from common.utils.timer import CLOCK
import logic.gcommon.common_utils.bcast_utils as bcast
import world
import weakref
MAIN_WEAPON_FIRE_STATE_ID_MAP = {0: 'fire1',
   1: 'fire2'
   }
MAIN_WEAPON_FIRE_EFFECT_ID_MAP = {0: '100',
   1: '101'
   }
RELOAD_STATE_ID = 'reload'
RELOAD_EFFECT_ID_MAP = {True: '102',
   False: ''
   }
JUMP_BURST_STATE_ID = 'jump_burst'
JUMP_BURST_EFFECT_ID_MAP = {True: '103',
   False: ''
   }
DASH_BURST_STATE_ID = 'dash_burst'
DASH_BURST_EFFECT_ID_MAP = {True: '104',
   False: ''
   }
DASH_DUST_STATE_ID = 'dash_dust'
DASH_DUST_EFFECT_ID_MAP = {True: '105',
   False: ''
   }
TRANSFORM_WEAPON_SHUTDOWN = 0
TRANSFORM_WEAPON_RELOADING = 1
TRANSFORM_WEAPON_READY = 2
TRANSFORM_WEAPON_STATE_ID = 'transform_weapon'
TRANSFORM_WEAPON_EFFECT_ID_MAP = {TRANSFORM_WEAPON_RELOADING: '106',
   TRANSFORM_WEAPON_READY: '107',
   TRANSFORM_WEAPON_SHUTDOWN: ''
   }
TRANSFORM_JUMP_DUST_EFFECT_ID = '108'
MOVE_DUST_TAIL_EFFECT_ID = '109'
MOVE_DUST_TAIL_EFFECT_SOCKET_LIST = ('fx_move_f_r', 'fx_move_f_l')
MOVE_DUST_TAIL_EFFECT_END_INTERVAL = 0.8

class ComMechaEffect8022(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PLAY_MAIN_WEAPON_FIRE_SFX': 'play_main_weapon_fire_sfx',
       'E_PLAY_RELOAD_SFX': 'play_reload_sfx',
       'E_PLAY_JUMP_BURST_SFX': 'play_jump_burst_sfx',
       'E_PLAY_DASH_BURST_SFX': 'play_dash_burst_sfx',
       'E_PLAY_DASH_DUST_SFX': 'play_dash_dust_sfx',
       'E_PLAY_TRANSFORM_WEAPON_STATE_SFX': 'play_transform_weapon_state_sfx',
       'E_PLAY_TRANSFORM_JUMP_DUST_SFX': 'play_transform_jump_dust_sfx',
       'E_PLAY_MOVE_DUST_TAIL_SFX': 'play_move_dust_tail_sfx',
       'E_ON_LOSE_CONNECT': 'on_lose_connect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8022, self).init_from_dict(unit_obj, bdict)
        self.make_center_anim_dir_equals_to_forward()
        self.move_dust_tail_sfx_ids = []
        self.show_move_dust_tail_sfx = False
        self.move_dust_tail_sfx_update_timer = None
        self.move_dust_tail_sfx_delay_show_timer = None
        self.move_dust_tail_sfx_delay_remove_timer_map = {}
        self.model_ref = None
        return

    def destroy(self):
        super(ComMechaEffect8022, self).destroy()
        for sfx_id in self.move_dust_tail_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.move_dust_tail_sfx_ids = []
        if self.move_dust_tail_sfx_update_timer:
            global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_update_timer)
            self.move_dust_tail_sfx_update_timer = None
        if self.move_dust_tail_sfx_delay_show_timer:
            global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_delay_show_timer)
            self.move_dust_tail_sfx_delay_show_timer = None
        for timer_id in six.itervalues(self.move_dust_tail_sfx_delay_remove_timer_map):
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self.move_dust_tail_sfx_delay_remove_timer_map = {}
        self.model_ref = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8022, self).on_model_loaded(model)
        self.model_ref = weakref.ref(model)

    def play_main_weapon_fire_sfx(self, fired_socket_index):
        self.on_trigger_state_effect(MAIN_WEAPON_FIRE_STATE_ID_MAP[fired_socket_index], MAIN_WEAPON_FIRE_EFFECT_ID_MAP[fired_socket_index], force=True, need_sync=True)

    def play_reload_sfx(self, flag):
        self.on_trigger_state_effect(RELOAD_STATE_ID, RELOAD_EFFECT_ID_MAP[flag], force=flag, need_sync=True)

    def play_jump_burst_sfx(self, flag):
        self.on_trigger_state_effect(JUMP_BURST_STATE_ID, JUMP_BURST_EFFECT_ID_MAP[flag], force=True, need_sync=True)

    def play_dash_burst_sfx(self, flag):
        self.on_trigger_state_effect(DASH_BURST_STATE_ID, DASH_BURST_EFFECT_ID_MAP[flag], force=True, need_sync=True)

    def play_dash_dust_sfx(self, flag):
        self.on_trigger_state_effect(DASH_DUST_STATE_ID, DASH_DUST_EFFECT_ID_MAP[flag], need_sync=True)

    def play_transform_weapon_state_sfx(self, state):
        self.on_trigger_state_effect(TRANSFORM_WEAPON_STATE_ID, TRANSFORM_WEAPON_EFFECT_ID_MAP[state], force=True, need_sync=True)

    def play_transform_jump_dust_sfx(self):
        pos = self.ev_g_position()
        if pos:
            pos = (
             pos.x, pos.y, pos.z)
            self.on_trigger_disposable_effect(TRANSFORM_JUMP_DUST_EFFECT_ID, pos, need_sync=True)

    def update_move_dust_tail_sfx(self):
        if not self.model_ref:
            return
        model = self.model_ref()
        if model and model.valid:
            for i, socket in enumerate(MOVE_DUST_TAIL_EFFECT_SOCKET_LIST):
                sfx = global_data.sfx_mgr.get_sfx_by_id(self.move_dust_tail_sfx_ids[i])
                if not sfx:
                    continue
                if not sfx.visible:
                    sfx.visible = True
                sfx.world_transformation = model.get_socket_matrix(socket, world.SPACE_TYPE_WORLD)

    @staticmethod
    def move_dust_tail_sfx_create_cb(sfx):
        sfx.visible = False

    def delay_show_move_dust_tail_sfx(self):
        self.move_dust_tail_sfx_ids = self.on_trigger_hold_effect(MOVE_DUST_TAIL_EFFECT_ID, create_cb=self.move_dust_tail_sfx_create_cb)
        if self.move_dust_tail_sfx_ids:
            if self.move_dust_tail_sfx_update_timer:
                global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_update_timer)
                self.move_dust_tail_sfx_update_timer = None
            self.move_dust_tail_sfx_update_timer = global_data.game_mgr.register_logic_timer(self.update_move_dust_tail_sfx, interval=1, times=-1)
            self.update_move_dust_tail_sfx()
            self.move_dust_tail_sfx_delay_show_timer = None
        return

    def delay_remove_move_dust_tail_sfx(self, remove_sfx_id_list):
        for sfx_id in remove_sfx_id_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.move_dust_tail_sfx_delay_remove_timer_map.pop(remove_sfx_id_list)

    def play_move_dust_tail_sfx(self, flag, blend_time=0.2):
        if not self.model_ref:
            return
        else:
            if flag == self.show_move_dust_tail_sfx:
                return
            self.show_move_dust_tail_sfx = flag
            if flag:
                if self.move_dust_tail_sfx_delay_show_timer:
                    global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_delay_show_timer)
                    self.move_dust_tail_sfx_delay_show_timer = None
                self.move_dust_tail_sfx_delay_show_timer = global_data.game_mgr.register_logic_timer(self.delay_show_move_dust_tail_sfx, interval=blend_time, times=1, mode=CLOCK)
            else:
                if self.move_dust_tail_sfx_update_timer:
                    global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_update_timer)
                    self.move_dust_tail_sfx_update_timer = None
                if self.move_dust_tail_sfx_delay_show_timer:
                    global_data.game_mgr.unregister_logic_timer(self.move_dust_tail_sfx_delay_show_timer)
                    self.move_dust_tail_sfx_delay_show_timer = None
                else:
                    remove_sfx_ids = (sfx_id for sfx_id in self.move_dust_tail_sfx_ids)
                    self.move_dust_tail_sfx_delay_remove_timer_map[remove_sfx_ids] = global_data.game_mgr.register_logic_timer(self.delay_remove_move_dust_tail_sfx, interval=MOVE_DUST_TAIL_EFFECT_END_INTERVAL, args=(
                     remove_sfx_ids,), times=1, mode=CLOCK)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_MOVE_DUST_TAIL_SFX, (flag, blend_time)], True)
            return

    def on_lose_connect(self):
        if self.ev_g_is_avatar():
            return
        self.play_dash_burst_sfx(False)
        self.play_dash_dust_sfx(False)
        self.play_transform_weapon_state_sfx(TRANSFORM_WEAPON_SHUTDOWN)