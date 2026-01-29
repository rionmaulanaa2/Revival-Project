# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGoldeneggClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import math
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const.battle_const import EGG_DROPPED, EGG_NOT_PICKED, EGG_PICKED, THROW_EGG
import common.utils.timer as timer
import logic.vscene.parts.ctrl.GamePyHook as game_hook
import game
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_DROPPING, FLAG_RECOVER_BY_PLANTING, FLAG_RECOVER_BY_TIME_UP, FLAG_RECOVER_BY_INVALID_REGION
ZERO_VECTOR = math3d.vector(0, 0, 0)

class ComGoldeneggClient(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded',
       'E_PICK_EGG_SUCCEED': '_pick_egg_succeed',
       'E_DROP_EGG_SUCCEED': '_drop_egg_succeed',
       'E_TRY_THROW_EGG': '_try_throw_egg'
       }

    def __init__(self):
        super(ComGoldeneggClient, self).__init__()
        self._egg_detect_timer_id = None
        self._pos_change_nty_timer_id = None
        self._hold_egg = False
        self._egg_picker_id = None
        self._model = None
        self._do_egg_drop_move = False
        self._target_pos = None
        self.need_update = True
        self._light_sfx_id = None
        self._small_map_egg_update_timer = None
        self._sound_obj_id = None
        self._bac_pos = None
        self._speed_limit = None
        self._speed_detect_timer_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGoldeneggClient, self).init_from_dict(unit_obj, bdict)
        self.info = bdict
        self.player = global_data.player.logic
        self._trigger_dis = {'Mecha': bdict.get('mecha_detect_range')
           }
        self._plant_dis = {'Mecha': bdict.get('mecha_plant_range')
           }
        self._npc_id = bdict.get('npc_id')
        self._egg_picker_id = bdict.get('picker_id', None)
        self.egg_state = bdict.get('egg_state', EGG_NOT_PICKED)
        self._init_egg_dropping_speed = -8 * NEOX_UNIT_SCALE
        self._init_egg_gravity_acc = 15 * NEOX_UNIT_SCALE
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
        self._sound_obj_id = global_data.sound_mgr.register_game_obj('FlagPlantSound')
        self._speed_limit = bdict.get('egg_drop_speed', 20)
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_flag_status(self):
        if self._egg_picker_id:
            self._model.visible = False
            self._light_sfx_id = None
            if self._egg_picker_id == self.player.id:
                self._hold_egg = True
        else:
            self.create_egg_effect()
        self._pos_change_nty_timer_id = global_data.game_mgr.register_logic_timer(self.egg_state_change, 0.1, mode=timer.CLOCK)
        return

    def create_egg_effect(self):
        self.del_egg_effect()
        sfx_path = 'effect/fx/scenes/common/zhanqi/zq_guangzhu_yellow_1.sfx'
        model = self.ev_g_model()
        self._light_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_glow')

    def del_egg_effect(self):
        if self._light_sfx_id:
            global_data.sfx_mgr.shutdown_sfx_by_id(self._light_sfx_id)
            self._light_sfx_id = None
        return

    def _try_throw_egg(self):
        if not self._hold_egg:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_drop_egg', (self.player.id,), True)

    def _on_col_loaded(self, model, col):
        self._model = model
        self.init_flag_status()
        self.start_detect()
        global_data.emgr.flagsnatch_flag_init_complete.emit(self.unit_obj.id, self.get_egg_position())
        if self._egg_picker_id:
            pass
        if self._bac_pos:
            self._model.position = math3d.vector(self._bac_pos[0], self._bac_pos[1], self._bac_pos[2])

    def _pick_egg_succeed(self, picker_id, picker_faction):
        self.del_egg_effect()
        global_data.emgr.snatchegg_egg_pick_up.emit(picker_id, picker_faction, self.unit_obj.id)
        self._egg_picker_id = picker_id
        if picker_id == self.player.id:
            self._hold_egg = True
        if self._model:
            self._model.visible = False

    def _drop_egg_succeed(self, holder_id, holder_faction, recover_pos, reason, before_pos, pass_egg):
        if reason != THROW_EGG:
            self.create_egg_effect()
            self._bac_pos = self._model or recover_pos
            return
        else:
            if not pass_egg:
                self._model.visible = True if 1 else False
                self._model.position = math3d.vector(recover_pos[0], recover_pos[1], recover_pos[2])
                self._egg_picker_id = None
                if holder_id == self.player.id:
                    self._hold_egg = False
            global_data.emgr.snatchegg_egg_drop.emit(holder_id, holder_faction, reason, self.unit_obj.id)
            return

    def egg_state_change(self):
        pos = None
        if self._egg_picker_id:
            egg_holder = self.battle.get_entity(self._egg_picker_id)
            if not egg_holder:
                return
            pos = egg_holder.logic.ev_g_position()
            if pos:
                self._model.position = pos
        else:
            pos = self._model.position
        return

    def start_detect(self):
        if not self._egg_detect_timer_id:
            self._egg_detect_timer_id = global_data.game_mgr.register_logic_timer(self.detect_player, 0.1, mode=timer.CLOCK)

    def detect_player(self):
        if self._egg_picker_id:
            return
        ctrl_entity = self.player.ev_g_control_target()
        if not ctrl_entity or not ctrl_entity.logic:
            return
        player_pos = self.player.ev_g_position()
        dist = self._model.position - player_pos
        trigger_dis = self._trigger_dis.get(ctrl_entity.__class__.__name__, 10)
        if dist.length > trigger_dis:
            return
        if self.player.id in global_data.death_battle_data.egg_picker_dict:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_pick_up_egg', (self.player.id,), True)

    def get_egg_position(self):
        pos = None
        if self._egg_picker_id:
            egg_holder = self.battle.get_entity(self._egg_picker_id)
            if not egg_holder:
                return
            pos = egg_holder.logic.ev_g_position()
        else:
            pos = self._model.position if self._model else None
        return pos

    def destroy(self):
        super(ComGoldeneggClient, self).destroy()
        self.player = None
        self.info = None
        self._trigger_dis = None
        self._model = None
        self.unregister_timer()
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
            self._sound_obj_id = None
        self.process_event(False)
        return

    def unregister_timer(self):
        if self._egg_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._egg_detect_timer_id)
            self._egg_detect_timer_id = None
        if self._pos_change_nty_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._pos_change_nty_timer_id)
            self._pos_change_nty_timer_id = None
        if self._small_map_egg_update_timer:
            global_data.game_mgr.unregister_logic_timer(self._small_map_egg_update_timer)
        if self._speed_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._speed_detect_timer_id)
        return

    def tick(self, delta):
        if self._do_egg_drop_move:
            if self._target_pos:
                self._model.position += self._move_dir * self._flag_dropping_speed * delta
                self._flag_dropping_speed += self._flag_gravity_acc * delta
                if self._model.position.y < self._target_pos.y:
                    self._model.position = self._target_pos
                    self._do_egg_drop_move = False