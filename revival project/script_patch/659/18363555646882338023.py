# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ExerciseBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Float, Tuple, Int, Dict, Uuid
from mobile.common.EntityManager import EntityManager
from mobile.common.IdManager import IdManager
from logic.gcommon.common_const import battle_const
from mobile.common.EntityFactory import EntityFactory
from common.utils import timer
from logic.gutils import scene_utils
import math3d
import world
import game3d
_HASH_roughness_test = game3d.calc_string_hash('roughness_test')
_HASH_metallic_test = game3d.calc_string_hash('metallic_test')

def create_pbr_ball():
    if not (global_data.player and global_data.player.logic):
        return
    scn = world.get_active_scene()
    x_offset = 80
    y_offset = 80
    mtl_offset = 0.25
    pos = global_data.player.logic.ev_g_position()
    for i in range(5):
        for j in range(5):
            new_pos = math3d.vector(pos.x + i * x_offset, pos.y + 60 + j * y_offset, pos.z)
            mod = world.model('model_new/test/bone_sphere.gim', scn)
            mod.position = new_pos
            mod.scale = math3d.vector(60, 60, 60)
            mod.all_materials.set_var(_HASH_roughness_test, 'roughness_test', mtl_offset * i)
            mod.all_materials.set_var(_HASH_metallic_test, 'metallic_test', mtl_offset * j)


class ExerciseBattle(Battle):
    exercise_ui = ('ExerciseCommandUI', 'ExerciseMechaModuleUI', 'ExerciseWeaponConfUI',
                   'ExerciseTimerUI', 'ExerciseDistanceUI')
    ui_to_hide = ('BattleInfoPlayerNumber', 'FightBagUI', 'BattleInfoAreaInfo', 'RogueGiftTopRightUI',
                  'DeathRogueGiftTopRightUI')
    ui_to_close = ('SmallMapUI', 'FightStateUI', 'BattleFightCapacity', 'FightKillNumberUI',
                   'BattleFightMeow')

    def __init__(self, entityid):
        self._exit_timestamp = 0
        super(ExerciseBattle, self).__init__(entityid)

    def init_from_dict(self, bdict):
        self.init_exercise_map_conf()
        super(ExerciseBattle, self).init_from_dict(bdict)
        self.init_event()
        self._king = None
        self._defier = None
        self._duel_queue = []
        self._mvp_entity_id = []
        self._max_duel_queue_cnt = global_data.game_mode.get_cfg_data('play_data').get('max_duel_queue_cnt', 2)
        self._king_info = [0, 0, 0]
        self.concert_stage = -1
        self.is_duel_waiting = False
        self.show_outline_player_id = None
        self.random_weapon = None
        self.duel_start_time = 0
        self.duel_end_time = 0
        self.last_king = None
        self.duel_waiting_timer = None
        self.area_id = 1
        return

    def init_event(self):
        global_data.emgr.resolution_changed += self.on_resolution_changed
        global_data.emgr.camera_lctarget_open_prez += self.on_open_prez

    def on_resolution_changed(self):
        global_data.emgr.update_exit_timestamp.emit(self._exit_timestamp)
        global_data.ui_mgr.close_ui('FightKillNumberUI')

    def update_exit_timestamp(self, exit_timestamp):
        self._exit_timestamp = exit_timestamp
        global_data.emgr.update_exit_timestamp.emit(exit_timestamp)

    @rpc_method(CLIENT_STUB, (Tuple('init_pos'),))
    def create_mecha_robot_sfx(self, pos):
        global_data.sfx_mgr.create_sfx_in_scene('effect/fx/scenes/common/dianziping/dianziping_red_mecha_2.sfx', math3d.vector(pos[0], pos[1], pos[2]))

    def init_exercise_map_conf(self):
        self.map_conf = confmgr.get('game_mode/exercise/c_map_exercise_conf')
        self.barrier_info = self.map_conf['Barrier']['Content']
        self.barrier_info_main = self.barrier_info['main']
        self.barrier_range_lb = self.barrier_info_main['barrier_range_lb']
        self.barrier_range_rt = self.barrier_info_main['barrier_range_rt']
        self.barrier_height = self.barrier_info_main['barrier_height']
        self.barriers_col_model = None
        self.barriers_col_model_2 = None
        self.barrier_sfx_main = None
        self.barrier_sfx_main_id = None
        return

    def boarding_movie_data(self):
        from data.battle_trans_anim import Getmecha_boarding_tdm
        return Getmecha_boarding_tdm()

    def load_finish(self):
        self.init_barrier_col()
        self.init_exercise_ui()
        super(ExerciseBattle, self).load_finish()

    def init_barrier_col(self):
        if self.barriers_col_model:
            return
        barrier_min_x = self.barrier_range_lb[0]
        barrier_min_z = self.barrier_range_lb[2]
        barrier_max_x = self.barrier_range_rt[0]
        barrier_max_z = self.barrier_range_rt[2]
        barrier_center_x = (barrier_min_x + barrier_max_x) * 0.5
        barrier_center_z = (barrier_min_z + barrier_max_z) * 0.5
        self.barriers_col_model = scene_utils.add_region_scene_collision_box((
         barrier_center_x, self.barrier_height, barrier_center_z), (barrier_max_x - barrier_min_x) * 0.5, (barrier_max_z - barrier_min_z) * 0.5)
        barrier_center = math3d.vector(barrier_center_x, self.barrier_height, barrier_center_z)
        self.init_barrier_sfx(barrier_min_x, barrier_min_z, barrier_max_x, barrier_max_z, barrier_center)
        self.barriers_col_model_2 = scene_utils.add_region_scene_collision_box((
         barrier_center_x, self.barrier_height, barrier_center_z), (barrier_max_x - barrier_min_x) * 0.5 + 6.5, (barrier_max_z - barrier_min_z) * 0.5 + 6.5)

    def init_barrier_sfx(self, min_x, min_z, max_x, max_z, center):

        def on_create_func(model):
            scale_x = (max_x - min_x) / (model.bounding_box.x * 2)
            scale_y = 4.0
            scale_z = (max_z - min_z) / (model.bounding_box.z * 2)
            model.world_scale = math3d.vector(scale_x, scale_y, scale_z)
            model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, 0, 0))
            self.barrier_sfx_main = model
            self.barrier_sfx_main_id = None
            self.barrier_sfx_main.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
            return

        barrier_model_path = confmgr.get('script_gim_ref')['region_range_blue']
        self.barrier_sfx_main_id = global_data.model_mgr.create_model_in_scene(barrier_model_path, center, on_create_func=on_create_func)

    def on_open_prez(self, enable):
        if self.barrier_sfx_main:
            if enable:
                self.barrier_sfx_main.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self.barrier_sfx_main.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self.barrier_sfx_main.all_materials.rebuild_tech()

    def init_exercise_ui(self):
        ui_mgr = global_data.ui_mgr
        for ui in self.ui_to_hide:
            ui_mgr.hide_ui(ui)

        for ui in self.ui_to_close:
            ui_mgr.close_ui(ui)

        for ui in self.exercise_ui:
            ui_mgr.show_ui(ui, module_path='logic.comsys.exercise_ui')

    def clear_barrier_col(self):
        if self.barriers_col_model:
            global_data.model_mgr.remove_model_by_id(self.barriers_col_model)
        self.barriers_col_model = None
        if self.barriers_col_model_2:
            global_data.model_mgr.remove_model_by_id(self.barriers_col_model_2)
        self.barriers_col_model_2 = None
        return

    def clear_barrier_sfx(self):
        if self.barrier_sfx_main_id:
            global_data.model_mgr.remove_model_by_id(self.barrier_sfx_main_id)
            self.barrier_sfx_main_id = None
        if self.barrier_sfx_main:
            global_data.model_mgr.remove_model(self.barrier_sfx_main)
            self.barrier_sfx_main = None
        return

    def clear_exercise_ui(self):
        ui_mgr = global_data.ui_mgr
        for ui in self.exercise_ui:
            ui_mgr.close_ui(ui)

    def destroy_exercise_battle(self):
        global_data.emgr.resolution_changed -= self.on_resolution_changed
        global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez
        self.clear_barrier_col()
        self.clear_barrier_sfx()
        self.clear_exercise_ui()

    def destroy(self, clear_cache=True):
        self.destroy_exercise_battle()
        super(ExerciseBattle, self).destroy()
        self.clear_mvp_tv()

    @rpc_method(CLIENT_STUB, (Dict('battle_data'),))
    def update_battle_data(self, battle_data):
        exit_timestamp = battle_data.get('exit_timestamp', None)
        if exit_timestamp is not None:
            self.update_exit_timestamp(exit_timestamp)
        duel_data = battle_data.get('duel_data', None)
        if not duel_data:
            return
        else:
            concert_stage = duel_data['duel_stage']
            duel_info = duel_data['duel_info']
            change_stage = concert_stage != self.concert_stage
            self.concert_stage = concert_stage
            self.random_weapon = duel_info.get('random_weapon')
            self.duel_start_time = duel_info.get('duel_start_time', 0)
            self.duel_end_time = duel_info.get('duel_end_time', 0)
            if self.is_duel_stage():
                self._king = duel_info.get('king', None)
                self._king_info = duel_info.get('king_info', [0, 0, 0])
                self._defier = duel_info.get('defier', None)
                self._duel_queue = duel_info.get('duel_queue', [])
                global_data.emgr.update_battle_data.emit()
                if change_stage:
                    global_data.emgr.camera_cancel_all_trk.emit()
                    if self.concert_stage == battle_const.CONCERT_FIGHT_STAGE:
                        self.start_duel()
            elif self.concert_stage == battle_const.CONCERT_STOP_DUEL_STAGE:
                global_data.ui_mgr.close_ui('ArenaWaitUI')
                global_data.ui_mgr.close_ui('ArenaApplyUI')
                global_data.ui_mgr.close_ui('ArenaConfirmUI')
                global_data.ui_mgr.close_ui('ArenaTopUI')
                global_data.ui_mgr.close_ui('FFABeginCountDown')
                ArenaEndUI = global_data.ui_mgr.get_ui('ArenaEndUI')
                if ArenaEndUI:
                    ArenaEndUI.duel_end()
            self.refresh_mvp_tv()
            global_data.emgr.update_concert_data_info_event.emit()
            if change_stage:
                global_data.emgr.update_battle_stage.emit()
            return

    def get_battle_stage(self):
        return self.concert_stage

    def is_duel_stage(self):
        return self.concert_stage < battle_const.CONCERT_STOP_DUEL_STAGE

    def is_wait_duel_stage(self):
        return self.concert_stage < battle_const.CONCERT_FIGHT_STAGE

    def get_battle_data(self):
        return (
         self._king, self._defier, self._duel_queue, self._king_info)

    def stop_self_fire_and_movement(self):
        from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
        stop_self_fire_and_movement()

    def is_in_queue(self):
        if not global_data.player:
            return False
        player_id = global_data.player.id
        if not player_id:
            return False
        if player_id in (self._king, self._defier) or player_id in self._duel_queue:
            return True
        return False

    def is_duel_player(self, id):
        return id is not None and id in (self._king, self._defier)

    def get_other_duel_player(self):
        if not global_data.player:
            return
        player_id = global_data.player.id
        if not player_id:
            return
        if player_id in (self._king, self._defier):
            if player_id == self._king:
                return self._defier
            return self._king

    def is_king(self):
        if not self._king:
            return False
        if not global_data.player:
            return False
        return global_data.player.id == self._king

    def is_defier(self):
        if not self._defier:
            return False
        if not global_data.player:
            return False
        return global_data.player.id == self._defier

    def is_wait_player(self):
        if not (self._king or self._defier):
            return True
        if not global_data.player:
            return False
        return global_data.player.id not in (self._king, self._defier)

    def is_full_queue(self):
        return len(self._duel_queue) >= self._max_duel_queue_cnt

    def req_duel(self):
        if len(self._duel_queue) >= self._max_duel_queue_cnt:
            return
        self.call_soul_method('req_duel', ())

    def cancel_duel(self):
        self.call_soul_method('cancel_duel', ())

    @rpc_method(CLIENT_STUB, (Int('stop_time'),))
    def pre_stop_duel(self, stop_time):
        from logic.gcommon.common_const.battle_const import UP_NODE_CONCERT_ANCHOR
        global_data.emgr.battle_event_message.emit(get_text_by_id(609913), message_type=UP_NODE_CONCERT_ANCHOR)

    @rpc_method(CLIENT_STUB, (Float('timeout_ts'), Int('confirm_idx')))
    def on_confirm_duel(self, timeout_ts, confirm_idx):
        ui = global_data.ui_mgr.show_ui('ArenaConfirmUI', 'logic.comsys.concert')
        ui.set_timeout_ts(confirm_idx, timeout_ts)

    def confirm_duel(self, confirm_idx, is_confirm):
        self.call_soul_method('confirm_duel', (confirm_idx, is_confirm))

    def clear_outline(self):
        if self.show_outline_player_id:
            show_outline_player = EntityManager.getentity(self.show_outline_player_id)
            if show_outline_player and show_outline_player.logic:
                show_outline_player.logic.send_event('E_ENABLE_MODEL_OUTLINE_ONLY', False)
                self.show_outline_player_id = None
        return

    def get_show_outline_player_id(self):
        return self.show_outline_player_id

    def refresh_outline(self):
        if self.concert_stage != battle_const.CONCERT_FIGHT_STAGE:
            self.clear_outline()
            return
        if global_data.player and global_data.player.id in (self._king, self._defier):
            self.clear_outline()
            show_outline_player_id, view_outline_player_id = (self._defier, self._king) if self.is_king() else (
             self._king, self._defier)
            if show_outline_player_id and global_data.player and global_data.player.id == view_outline_player_id:
                show_outline_player = EntityManager.getentity(show_outline_player_id)
                if show_outline_player and show_outline_player.logic:
                    show_outline_player.logic.send_event('E_ENABLE_MODEL_OUTLINE_ONLY', True)
                    self.show_outline_player_id = show_outline_player_id

    def start_duel(self):
        if global_data.player and global_data.player.id in (self._king, self._defier):
            self.stop_self_fire_and_movement()
            self.refresh_outline()
            import math
            from logic.gcommon import time_utility
            start_left_time = 0
            if self.duel_start_time:
                start_left_time = int(math.ceil(self.duel_start_time - time_utility.time()))
            if start_left_time > 0:
                ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(start_left_time)
            global_data.ui_mgr.show_ui('ArenaTopUI', 'logic.comsys.concert')
            global_data.ui_mgr.close_ui('ArenaApplyUI')
            global_data.ui_mgr.close_ui('ArenaEndUI')
            global_data.ui_mgr.close_ui('KizunaConcertViewUI')
            if start_left_time > 0:
                self.is_duel_waiting = True

                def _end_waiting():
                    self.is_duel_waiting = False

                if self.duel_waiting_timer:
                    global_data.game_mgr.get_logic_timer().unregister(self.duel_waiting_timer)
                self.duel_waiting_timer = global_data.game_mgr.get_logic_timer().register(func=_end_waiting, mode=timer.CLOCK, interval=start_left_time, times=1)

    def get_duel_info(self):
        return (self.random_weapon, self.duel_start_time, self.duel_end_time)

    def can_move(self):
        return not self.is_duel_waiting

    def can_fire(self):
        return not self.is_duel_waiting

    def can_roll(self):
        return not self.is_duel_waiting

    def can_lens_aim(self):
        return not self.is_duel_waiting

    @rpc_method(CLIENT_STUB, (Uuid('winner'), Int('reward_cnt')))
    def on_duel_finish(self, winner, reward_cnt):
        self.stop_self_fire_and_movement()
        self.clear_outline()
        if not global_data.player:
            return
        player_id = global_data.player.id
        is_king = self.is_king()
        is_winner = player_id == winner
        ui = global_data.ui_mgr.show_ui('ArenaEndUI', 'logic.comsys.concert')
        ui.set_winner(winner, is_king, is_winner, reward_cnt)
        global_data.ui_mgr.close_ui('ArenaApplyUI')
        global_data.ui_mgr.close_ui('ArenaTopUI')
        global_data.ui_mgr.close_ui('FFABeginCountDown')

    def refresh_mvp_tv(self):
        info = self.get_duel_mvp_info()
        self.refesh_duel_mvp_info(info)

    def get_duel_mvp_info(self):
        info = {}
        if not self._king:
            return info
        show_ani = False
        if self.last_king != self._king:
            self.last_king = self._king
            show_ani = True
        player = EntityManager.getentity(self._king)
        if player and player.logic:
            num, _, _ = self._king_info
            char_name = player.logic.ev_g_char_name()
            dressed_clothing_id = player.logic.ev_g_dressed_clothing_id()
            info = {'name': char_name,'dressed_clothing_id': dressed_clothing_id,'mvp': num,'show_ani': show_ani}
            return info
        return info

    def refesh_duel_mvp_info(self, info):
        if not self._mvp_entity_id:
            for tv_id in (30003, ):
                entity_id = IdManager.genid()
                entity_obj = EntityFactory.instance().create_entity('Television', entity_id)
                info['show_ani'] = False
                entity_obj.init_from_dict({'tv_id': tv_id,'is_client': True,'is_show': bool(info),'show_info': info})
                entity_obj.on_add_to_battle(self.id)
                self._mvp_entity_id.append(entity_id)

        else:
            for entity_id in self._mvp_entity_id:
                entity_obj = EntityManager.getentity(entity_id)
                if entity_obj and entity_obj.logic:
                    entity_obj.logic.send_event('E_UPDATE_TV_INFO', {'is_show': bool(info),'show_info': info})

    def on_switch_mvp(self):
        super(ExerciseBattle, self).on_switch_mvp()
        info = {'is_show_special': self._is_switch_mvp}
        self.refesh_duel_mvp_info(info)

    def clear_mvp_tv(self):
        for entity_id in self._mvp_entity_id:
            entity_obj = EntityManager.getentity(entity_id)
            if entity_obj:
                entity_obj.on_remove_from_battle()
                entity_obj.destroy()