# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFlagClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
import common.utils.timer as timer
import logic.vscene.parts.ctrl.GamePyHook as game_hook
import game
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_DROPPING, FLAG_RECOVER_BY_PLANTING, FLAG_RECOVER_BY_TIME_UP, FLAG_RECOVER_BY_INVALID_REGION
ZERO_VECTOR = math3d.vector(0, 0, 0)

class ComFlagClient(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded',
       'E_TRY_DROP_FLAG': '_try_drop_flag',
       'E_PICK_FLAG_SUCCEED': '_pick_flag_succeed',
       'E_RECOVER_FLAG_SUCCEED': '_recover_flag_succeed'
       }

    def __init__(self):
        super(ComFlagClient, self).__init__()
        self._flag_detect_timer_id = None
        self._flag_base_detect_timer_id = None
        self._pos_change_nty_timer_id = None
        self._hold_flag = False
        self._flag_picker_id = None
        self._model = None
        self._do_flag_drop_move = False
        self._target_pos = None
        self.need_update = True
        self._detect_cd = 0
        self._flag_hint_manager = FlagHintManager()
        self._faction_to_flag_base_id = None
        self._teammate_flag_base = None
        self._light_sfx_id = None
        self._blow_sfx_id = None
        self._unlock_timer = None
        self._small_map_flag_update_timer = None
        self._lock = False
        self._sound_obj_id = None
        self._bac_pos = None
        self._speed_limit = None
        self._speed_detect_timer_id = None
        self._in_base_timer_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlagClient, self).init_from_dict(unit_obj, bdict)
        self.info = bdict
        self.player = global_data.player.logic
        self._building_no = bdict.get('building_no', None)
        self._trigger_dis = {'Mecha': bdict.get('mecha_detect_range'),
           'Avatar': bdict.get('human_detect_range')
           }
        self._plant_dis = {'Mecha': bdict.get('mecha_plant_range'),
           'Avatar': bdict.get('human_plant_range')
           }
        self._detact_cd = bdict.get('detect_cd', 5)
        self._flag_picker_id = bdict.get('picker_id', None)
        self._picker_faction = bdict.get('picker_faction', None)
        self._init_flag_dropping_speed = -8 * NEOX_UNIT_SCALE
        self._init_flag_gravity_acc = 15 * NEOX_UNIT_SCALE
        self._faction_to_flag_base_id = bdict.get('flag_base_info')
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
        self._sound_obj_id = global_data.sound_mgr.register_game_obj('FlagPlantSound')
        self._speed_limit = bdict.get('flag_drop_speed', 20)
        self.process_event(True)
        self._in_base_timer_id = global_data.game_mgr.register_logic_timer(self.check_in_base, 0.5, mode=timer.CLOCK)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_flag_status(self):
        if self._flag_picker_id:
            self._model.visible = False
            self._light_sfx_id = None
            if self._flag_picker_id == self.player.id:
                self._hold_flag = True
        else:
            self.create_flag_effect()
        self._pos_change_nty_timer_id = global_data.game_mgr.register_logic_timer(self.flag_state_change, 0.1, mode=timer.CLOCK)
        return

    def create_flag_effect(self):
        self.del_flag_effect()
        sfx_path = 'effect/fx/scenes/common/zhanqi/zq_guangzhu_yellow_1.sfx'
        model = self.ev_g_model()
        self._light_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_glow')

    def del_flag_effect(self):
        if self._light_sfx_id:
            global_data.sfx_mgr.shutdown_sfx_by_id(self._light_sfx_id)
            self._light_sfx_id = None
        return

    def _try_drop_flag(self):
        if not self._hold_flag:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_drop_flag', (self.player.id,), True)

    def _on_col_loaded(self, model, col):
        self._model = model
        self.init_flag_status()
        self.start_detect()
        global_data.emgr.flagsnatch_flag_init_complete.emit(self.unit_obj.id, self.get_flag_position())
        if self._flag_picker_id:
            global_data.emgr.flagsnatch_flag_pick_up.emit(self._flag_picker_id, self._picker_faction)
        if self._bac_pos:
            self._model.position = math3d.vector(self._bac_pos[0], self._bac_pos[1], self._bac_pos[2])

    def _pick_flag_succeed(self, picker_id, picker_faction):
        global_data.sound_mgr.post_event_2d('Play_ui_pickup', None)
        self.del_flag_effect()
        global_data.emgr.flagsnatch_flag_pick_up.emit(picker_id, picker_faction)
        self._flag_picker_id = picker_id
        if picker_id == self.player.id:
            self._hold_flag = True
        if self._model:
            self._model.visible = False
        return

    def play_blow_effect(self, target_faction):
        if not target_faction:
            return
        base_id = self._faction_to_flag_base_id.get(target_faction)
        if not base_id:
            return
        base_ent = global_data.battle.get_entity(base_id)
        pos = base_ent.logic.ev_g_model_position()
        blow_sfx_path = 'effect/fx/scenes/common/zhanqi/zq_kaiqi.sfx'
        global_data.sfx_mgr.create_sfx_in_scene(blow_sfx_path, pos)

    def play_recover_sound(self, reason, faction):
        if reason == FLAG_RECOVER_BY_PLANTING:
            base_id = self._faction_to_flag_base_id.get(faction)
            base_ent = global_data.battle.get_entity(base_id)
            if base_ent:
                global_data.sound_mgr.post_event('Play_ui_prompt', self._sound_obj_id, self.get_flag_position())
                pos = base_ent.logic.ev_g_hp_position()
                global_data.sound_mgr.post_event('Play_ui_prompt', self._sound_obj_id, pos)
            player_faction = global_data.player.logic.ev_g_group_id()
            if faction == player_faction:
                global_data.sound_mgr.post_event_2d('Play_ui_occupy', None)
            else:
                global_data.sound_mgr.post_event_2d('Play_ui_enemy_occupy', None)
        elif reason == FLAG_RECOVER_BY_TIME_UP or reason == FLAG_RECOVER_BY_INVALID_REGION:
            global_data.sound_mgr.post_event_2d('Play_ui_limit', None)
        elif reason == FLAG_RECOVER_BY_DROPPING:
            if faction == global_data.player.logic.ev_g_group_id():
                global_data.sound_mgr.post_event_2d('Play_ui_lost', None)
            else:
                global_data.sound_mgr.post_event_2d('Play_ui_kill_lost', None)
        return

    def _recover_flag_succeed(self, holder_id, holder_faction, recover_pos, reason, before_pos):
        self.play_recover_sound(reason, holder_faction)
        self.create_flag_effect()
        global_data.emgr.flagsnatch_flag_recover.emit(holder_id, holder_faction, reason)
        if reason == FLAG_RECOVER_BY_PLANTING:
            self.play_blow_effect(holder_faction)
            global_data.emgr.flagsnatch_flag_planting_succeed.emit(holder_id, holder_faction)
            unlock_time = global_data.death_battle_data.flag_lock_time
            if self._unlock_timer:
                global_data.game_mgr.unregister_logic_timer(self._unlock_timer)
            self._unlock_timer = global_data.game_mgr.register_logic_timer(self.unlock, unlock_time, times=1, mode=timer.CLOCK)
        elif reason == FLAG_RECOVER_BY_INVALID_REGION:
            unlock_time = global_data.death_battle_data.flag_lock_time
            if self._unlock_timer:
                global_data.game_mgr.unregister_logic_timer(self._unlock_timer)
            self._unlock_timer = global_data.game_mgr.register_logic_timer(self.unlock, unlock_time, times=1, mode=timer.CLOCK)
        self._flag_picker_id = None
        if holder_id == self.player.id:
            self._hold_flag = False
            self._detect_cd = 3
        if not self._model:
            self._bac_pos = recover_pos
            return
        else:
            self._model.visible = True
            if not before_pos:
                self._model.position = math3d.vector(recover_pos[0], recover_pos[1], recover_pos[2])
                self._do_flag_drop_move = False
            else:
                self.do_flag_drop(math3d.vector(before_pos[0], before_pos[1], before_pos[2]), math3d.vector(recover_pos[0], recover_pos[1], recover_pos[2]), self._init_flag_dropping_speed, self._init_flag_gravity_acc)
            return

    def do_flag_drop(self, start_pos, end_pos, speed, acc_speed):
        self._do_flag_drop_move = True
        self._flag_dropping_speed = speed
        self._flag_gravity_acc = acc_speed
        self._move_dir = end_pos - start_pos
        if self._move_dir != ZERO_VECTOR:
            self._move_dir.normalize()
        self._model.position = start_pos
        self._target_pos = end_pos

    def flag_state_change(self):
        pos = None
        if self._flag_picker_id:
            flag_holder = self.battle.get_entity(self._flag_picker_id)
            if not flag_holder:
                return
            pos = flag_holder.logic.ev_g_position()
            self._model.position = pos
        else:
            pos = self._model.position
        global_data.emgr.flagsnatch_flag_moved.emit(pos)
        return

    def start_detect(self):
        if not self._flag_detect_timer_id:
            self._flag_detect_timer_id = global_data.game_mgr.register_logic_timer(self.detect_player, 0.1, mode=timer.CLOCK)
        if not self._flag_base_detect_timer_id:
            self._flag_base_detect_timer_id = global_data.game_mgr.register_logic_timer(self.flag_base_detect_player, 0.1, mode=timer.CLOCK)

    def detect_player(self):
        if self._flag_picker_id or self._detect_cd > 0:
            return
        ctrl_entity = self.player.ev_g_control_target()
        if not ctrl_entity or not ctrl_entity.logic:
            return
        player_pos = self.player.ev_g_position()
        dist = self._model.position - player_pos
        trigger_dis = self._trigger_dis.get(ctrl_entity.__class__.__name__, 10)
        if dist.length > trigger_dis:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_pick_up_flag', (self.player.id,), True)

    def auto_drop_detect(self):
        pass

    def flag_base_detect_player(self):
        if not self._teammate_flag_base:
            faction = global_data.player.logic.ev_g_group_id()
            base_id = self._faction_to_flag_base_id.get(faction)
            if not base_id:
                return
            self._teammate_flag_base = global_data.battle.get_entity(base_id)
        if not self._teammate_flag_base or not self._teammate_flag_base.logic:
            return
        flag_base_pos = self._teammate_flag_base.logic.ev_g_model_position()
        player_pos = self.player.ev_g_position()
        if not flag_base_pos or not player_pos:
            return
        dist = flag_base_pos - player_pos
        ctrl_entity = self.player.ev_g_control_target()
        trigger_dis = self._plant_dis.get(ctrl_entity.__class__.__name__, 10)
        if dist.length > trigger_dis:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'try_plant_flag', (self.player.id,), True)

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    def handle_drop_flag_when_move_fast(self):

        def speed_detection():
            if not self._flag_picker_id == global_data.player.id:
                return
            mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
            if not mecha:
                return
            character_col = mecha.logic.sd.ref_character
            if not character_col:
                return
            tmp_speed = character_col.getWalkDirection().length / NEOX_UNIT_SCALE
            if tmp_speed >= self._speed_limit:
                self.send_event('E_TRY_DROP_FLAG')

        self._speed_detect_timer_id = global_data.game_mgr.register_logic_timer(speed_detection, 0.02, mode=timer.CLOCK)

    def get_flag_position(self):
        pos = None
        if self._flag_picker_id:
            flag_holder = self.battle.get_entity(self._flag_picker_id)
            if not flag_holder:
                return
            pos = flag_holder.logic.ev_g_position()
        else:
            pos = self._model.position if self._model else None
        return pos

    def destroy(self):
        super(ComFlagClient, self).destroy()
        self.player = None
        self.info = None
        self._building_no = None
        self._trigger_dis = None
        self._model = None
        self.unregister_timer()
        self._flag_hint_manager.destroy()
        self._teammate_flag_base = None
        if self._sound_obj_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_obj_id)
            self._sound_obj_id = None
        self.process_event(False)
        return

    def unregister_timer(self):
        if self._flag_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._flag_detect_timer_id)
            self._flag_detect_timer_id = None
        if self._pos_change_nty_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._pos_change_nty_timer_id)
            self._pos_change_nty_timer_id = None
        if self._flag_base_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._flag_base_detect_timer_id)
        if self._unlock_timer:
            global_data.game_mgr.unregister_logic_timer(self._unlock_timer)
        if self._small_map_flag_update_timer:
            global_data.game_mgr.unregister_logic_timer(self._small_map_flag_update_timer)
        if self._speed_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._speed_detect_timer_id)
        if self._in_base_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._in_base_timer_id)
        return

    def tick(self, delta):
        if self._detact_cd > 0:
            self._detect_cd -= delta
        if self._do_flag_drop_move:
            if self._target_pos:
                self._model.position += self._move_dir * self._flag_dropping_speed * delta
                self._flag_dropping_speed += self._flag_gravity_acc * delta
                if self._model.position.y < self._target_pos.y:
                    self._model.position = self._target_pos
                    self._do_flag_drop_move = False

    def check_enter_base(self):
        battle_data = global_data.death_battle_data
        if battle_data and battle_data.get_is_in_base_part():
            self.send_event('E_CALL_SYNC_METHOD', 'enter_born_region', (self.player.id,), True)

    def check_in_base(self):
        pos = self.get_flag_position()
        battle_data = global_data.death_battle_data
        if battle_data.pos_in_base_part(pos):
            self.send_event('E_CALL_SYNC_METHOD', 'enter_born_region', (self.player.id,), True)


class FlagHintManager(object):
    RECOVER_REASON_TO_UI_TYPE = {FLAG_RECOVER_BY_DROPPING: {'teammate': battle_const.FLAG_BATTLE_FLAG_DROPPED_SELF_TEAM,
                                  'enemy': battle_const.FLAG_BATTLE_FLAG_DROPPED_OTHER_TEAM
                                  },
       FLAG_RECOVER_BY_PLANTING: {'teammate': battle_const.FLAG_BATTLE_FLAG_PLANTED_SELF_TEAM,
                                  'enemy': battle_const.FLAG_BATTLE_FLAG_PLANTED_OTHER_TEAM
                                  },
       FLAG_RECOVER_BY_TIME_UP: {'teammate': battle_const.FLAG_BATTLE_FLAG_RECOVER_TO_ORIGIN,
                                 'enemy': battle_const.FLAG_BATTLE_FLAG_RECOVER_TO_ORIGIN
                                 },
       FLAG_RECOVER_BY_INVALID_REGION: {'teammate': battle_const.FLAG_BATTLE_FLAG_RECOVER_TO_ORIGIN,
                                        'enemy': battle_const.FLAG_BATTLE_FLAG_RECOVER_TO_ORIGIN
                                        }
       }

    def __init__(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_flag_recover': self.show_flag_recover_hint,
           'flagsnatch_flag_pick_up': self.show_flag_pick_hint
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_flag_recover_hint(self, holder_id, holder_faction, reason):
        ui_types = self.RECOVER_REASON_TO_UI_TYPE.get(reason, None)
        if not ui_types:
            return
        else:
            player_faciton = global_data.player.logic.ev_g_group_id()
            if holder_faction == player_faciton:
                faction_type = 'teammate' if 1 else 'enemy'
                ui_type = ui_types.get(faction_type, None)
                return ui_type or None
            msg = {'i_type': ui_type}
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            return

    def show_flag_pick_hint(self, picker_id, picker_faction, *args):
        player_faciton = global_data.player.logic.ev_g_group_id()
        is_teammate = True if player_faciton == picker_faction else False
        if is_teammate:
            msg = {'i_type': battle_const.FLAG_BATTLE_FLAG_PICKED_SELF_TEAM}
        else:
            msg = {'i_type': battle_const.FLAG_BATTLE_FLAG_PICKED_OTHER_TEAM}
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def destroy(self):
        self.process_event(False)