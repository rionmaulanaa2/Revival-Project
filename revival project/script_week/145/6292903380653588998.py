# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Battle.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import os
import math3d
import game
import sys
import exception_hook
import version
import random
import game3d
from mobile.common.EntityManager import Dynamic, EntityManager
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.IdManager import IdManager
from mobile.common.RpcIndex import RpcIndexer
from common.cfg import confmgr
from common.utils.timer import RELEASE, LOGIC, CLOCK
from logic.entities.BaseClientEntity import BaseClientEntity
from logic.gutils.EntityPool import EntityPool
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.time_utility import time
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import battle_const, lobby_const
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE
from logic.vscene import scene_type
from logic.client.const import game_mode_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.archive import archive_manager
from logic.comsys.archive import archive_key_const
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.accelerometer.AccInput import AccInput
from logic.gcommon.cdata.round_competition import get_round_competition_conf
from logic.gcommon import utility as util
from logic.gcommon.common_const import ui_operation_const as uoc

@Dynamic
class Battle(BaseClientEntity):
    ESSENTIAL_MEMBERS = ()

    @staticmethod
    def meta_class(*members):
        _members = list(Battle.ESSENTIAL_MEMBERS)
        _members.extend(members)
        return util.meta_class('logic.entities.battlemembers', _members)

    BATTLE_STATUS_INIT = 0
    BATTLE_STATUS_PREPARE = 1
    BATTLE_STATUS_PARACHUTE = 2
    BATTLE_STATUS_FIGHT = 3
    BATTLE_STATUS_FINISH = 4

    def __init__(self, entityid):
        super(Battle, self).__init__(entityid)
        self.meta_tag = False
        global_data.emgr.net_reconnect_event += self.on_reconnected
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.scene_camera_switch_player_setted_event += self._on_scene_cam_observe_player_setted
        global_data.emgr.scene_after_enter_event += self._on_enter_scene
        global_data.battle = self
        self.is_in_island = lambda : False
        self.is_start_battle = False
        self.prepare_num = 0
        self.init_timestamp = 0
        self.server_name = ''
        self.game_ver = -1
        self._battle_status = Battle.BATTLE_STATUS_INIT
        self._entity_dict = {}
        self._entity_aoi_id_dict = {}
        self.alive_player_num = 0
        self.statistics = {}
        self.group_kill_statistics = 0
        self._ob_in_battle = False
        self._save_init_bdict = None
        self._plane_start_timestamp = 0
        self._plane_start = False
        self._chunk_check_timer_id = 0
        self._force_check_height = 200 * NEOX_UNIT_SCALE
        self.prepare_timestamp = 0
        self.flight_dict = {}
        self.plane_id = None
        self.plane = None
        self.is_settle = False
        self._actors_set = set([])
        self._ui_confirm_playerid = None
        self.is_in_ace_state = False
        self.need_show_enemy_pos = False
        self.settle_likenum_dict = {}
        self._sync_handler = {battle_const.SYNC_TYPE_CREATE: self.create_entity,
           battle_const.SYNC_TYPE_HIDE: self.destroy_entity,
           battle_const.SYNC_TYPE_DESTROY: self.destroy_entity,
           battle_const.SYNC_TYPE_LOGIC: self.logic_entity,
           battle_const.SYNC_TYPE_BATTLE: self.battle_method
           }
        self.poison_circle = None
        self.ob_settle_info = None
        self._mvp_id = None
        server_version = version.get_server_version()
        if server_version is None:
            server_version = 0
        self._mvp_info = {}
        self._battle_flag = {}
        self._brief_group_data = {}
        self._max_teammate_num = 0
        self._is_competition = False
        self._comp_id = ''
        self._comp_round = ''
        self._scene_name = None
        self._switch_timer = None
        self._is_switch_mvp = False
        self._scene_path = None
        archive_manager.ArchiveManager().save_general_archive_data_value(archive_key_const.KEY_LAST_BATTLE_SERVER_VERSION, str(server_version))
        self._sync_queue = []
        self._sync_queue_misty = []
        self._sync_delta_time = 0
        self._ai_level = None
        self._in_recording_video = False
        self._settle_stage_arrive_time = None
        self._flight_time = None
        self._avatar_mecha_dict = {}
        self._is_pure_mecha = False
        self._is_pure_human = False
        self._can_pick_same_weapon = True
        self._carry_bullet_mode = False
        self.has_quit = False
        self.battle_tid = None
        self.next_transfer_ts = 0
        self._max_loading_time = 0
        self.group_loading_dict = {}
        self.soul_loading_data = {}
        self._all_member_ready = {}
        self._default_show_role = 0
        self.group_encourage_dict = {}
        self._loading_group_id = None
        self._delay_load_scene_timer = None
        self._min_x = -350 * NEOX_UNIT_SCALE
        self._max_x = 480 * NEOX_UNIT_SCALE
        self._min_z = -600 * NEOX_UNIT_SCALE
        self._max_z = 390 * NEOX_UNIT_SCALE
        self._is_customed_battle = False
        self.force_trigger_door = False
        self.is_custom_faction_room = False
        global_data.player.join_battle(self.id)
        return

    def is_pure_human_battle(self):
        return self._is_pure_human

    def is_pure_mecha_battle(self):
        return self._is_pure_mecha

    @property
    def force_check_height(self):
        return self._force_check_height

    def init_from_dict_base(self, bdict):
        swtich_data = bdict.get('swtich_data', {})
        if not global_data.feature_mgr.is_support_soc():
            global_data.use_soc = False
        else:
            global_data.use_soc = swtich_data.get('enable_kongdao_soc', False)
        global_data.enable_check_pos = swtich_data.get('enable_check_pos', True)
        battle_srv_time = bdict.get('battle_srv_time', None)
        if battle_srv_time and tutil.TYPE_BATTLE not in tutil.g_success_flag:
            tutil.on_sync_time(tutil.TYPE_BATTLE, battle_srv_time)
        self.is_start_battle = True
        self._save_init_bdict = bdict
        self._is_pure_human = bdict.get('is_pure_human', False)
        self._is_pure_mecha = bdict.get('is_pure_mecha', False)
        self._can_pick_same_weapon = bdict.get('can_pick_same_weapon', True)
        self._carry_bullet_mode = bdict.get('carry_bullet_mode', False)
        self._bp_play_mode = bdict.get('bp_play_mode', None)
        self._bp_play_area = bdict.get('bp_play_area', None)
        self._max_loading_time = bdict.get('max_loading_time', 0)
        self.group_loading_dict = bdict.get('group_loading_dict', {})
        self.soul_loading_data = bdict.get('soul_loading_data', {})
        self._all_member_ready = bdict.get('all_member_ready', False)
        self._default_show_role = bdict.get('default_show_role', 0)
        self.group_encourage_dict = bdict.get('group_encourage_dict', {})
        self._loading_group_id = bdict.get('loading_group_id')
        self.init_battle_status(bdict)
        scene_data = {}
        view_position = bdict.get('view_position', None)
        if view_position:
            scene_data['view_position'] = view_position
        view_range = bdict.get('view_range', None)
        if view_range:
            scene_data['view_range'] = view_range
        brief_group_data = bdict.get('brief_group_data', None)
        self._brief_group_data = brief_group_data
        scene_data['group_data'] = brief_group_data
        scene_data['is_battle'] = True
        is_spectate = bdict.get('is_spectate', False)
        scene_data['is_spectate'] = is_spectate
        scene_data['scene_name'] = bdict.get('scene_name', 'bw_all06')
        self._scene_name = scene_data['scene_name']
        self._scene_path = bdict.get('scene_path', None)
        if 'environment' in bdict:
            scene_data['fog_config'] = scene_data['light_config'] = scene_data['hdr_config'] = bdict['environment']
        flight_dict = bdict.get('flight_dict', {})
        if flight_dict:
            self.flight_dict = flight_dict
            self._check_create_plane()
        self.init_battle_scene(scene_data)
        global_data.game_voice_mgr.init_battle_event()
        from logic.gcommon.common_const import ui_operation_const
        from logic.comsys.video.video_record_utils import is_high_light_support
        high_light_enable = global_data.player.get_setting_2(ui_operation_const.HIGH_LIGHT_KEY)
        battle_type_disable = confmgr.get('battle_config', str(self.battle_tid), default={}).get('bNoHighlight', 0)
        if not battle_type_disable and not is_spectate and high_light_enable and is_high_light_support():
            from logic.comsys.video.VideoRecord import VideoRecord
            self._in_recording_video = VideoRecord().record_battle_video(self.id)
        self._max_teammate_num = bdict.get('max_teammate_num', 1)
        self._is_competition = bdict.get('is_competition', False)
        self._comp_id = bdict.get('comp_id', '')
        self._comp_round = bdict.get('comp_round', '')
        self._is_customed_battle = bdict.get('is_customed_battle', False)
        self._customed_battle_dict = bdict.get('customed_battle_dict', {})
        self._customed_no_multi_mecha_limit = bdict.get('customed_no_multi_mecha_limit', False)
        self._customed_enable_friend_hurt = bdict.get('customed_enable_friend_hurt', False)
        self.next_transfer_ts = bdict.get('next_transfer_ts', 0)
        global_data.player.battle_tmp_consume = bdict.get('battle_consume_info', {})
        self._is_support_surrender = 'surrender_data' in bdict
        self._surrender_data = bdict.get('surrender_data', {})
        surrender_enable_timestamp = self._surrender_data.get('enable_timestamp', None)
        if surrender_enable_timestamp is not None:
            self.enable_surrender((surrender_enable_timestamp, False))
            self.sync_surrender((self._surrender_data,))
        self.is_custom_faction_room = bdict.get('is_custom_faction_room', False)
        return

    def init_from_dict--- This code section failed: ---

 309       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'True'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    24  'to 24'

 310      12  LOAD_GLOBAL           1  'True'
          15  LOAD_FAST             0  'self'
          18  STORE_ATTR            2  'meta_tag'
          21  JUMP_FORWARD          0  'to 24'
        24_0  COME_FROM                '21'

 313      24  LOAD_GLOBAL           3  'False'
          27  STORE_FAST            2  'from_lobby'

 314      30  LOAD_GLOBAL           4  'global_data'
          33  LOAD_ATTR             5  'player'
          36  STORE_FAST            3  'player'

 315      39  LOAD_FAST             3  'player'
          42  POP_JUMP_IF_FALSE    85  'to 85'

 316      45  LOAD_FAST             3  'player'
          48  LOAD_ATTR             6  'get_place'
          51  CALL_FUNCTION_0       0 
          54  LOAD_GLOBAL           7  'lobby_const'
          57  LOAD_ATTR             8  'PLACE_LOBBY'
          60  COMPARE_OP            2  '=='
          63  STORE_FAST            2  'from_lobby'

 317      66  LOAD_FAST             3  'player'
          69  LOAD_ATTR             9  'enter_place'
          72  LOAD_GLOBAL           7  'lobby_const'
          75  LOAD_ATTR            10  'PLACE_BATTLE'
          78  CALL_FUNCTION_1       1 
          81  POP_TOP          
          82  JUMP_FORWARD          0  'to 85'
        85_0  COME_FROM                '82'

 319      85  LOAD_FAST             1  'bdict'
          88  LOAD_ATTR            11  'get'
          91  LOAD_CONST            2  'server_name'
          94  LOAD_CONST            3  ''
          97  CALL_FUNCTION_2       2 
         100  LOAD_FAST             0  'self'
         103  STORE_ATTR           12  'server_name'

 320     106  LOAD_FAST             1  'bdict'
         109  LOAD_ATTR            11  'get'
         112  LOAD_CONST            4  'game_ver'
         115  LOAD_CONST            5  ''
         118  CALL_FUNCTION_2       2 
         121  LOAD_FAST             0  'self'
         124  STORE_ATTR           13  'game_ver'

 321     127  LOAD_FAST             1  'bdict'
         130  LOAD_ATTR            11  'get'
         133  LOAD_CONST            6  'battle_idx'
         136  LOAD_CONST            5  ''
         139  CALL_FUNCTION_2       2 
         142  LOAD_GLOBAL           4  'global_data'
         145  STORE_ATTR           14  'battle_idx'

 323     148  LOAD_FAST             2  'from_lobby'
         151  LOAD_FAST             1  'bdict'
         154  LOAD_CONST            7  'from_lobby'
         157  STORE_SUBSCR     

 325     158  LOAD_FAST             0  'self'
         161  LOAD_ATTR             2  'meta_tag'
         164  POP_JUMP_IF_FALSE   186  'to 186'

 326     167  LOAD_FAST             0  'self'
         170  LOAD_ATTR            15  '_call_meta_member_func'
         173  LOAD_CONST            8  '_init_@_from_dict'
         176  LOAD_FAST             1  'bdict'
         179  CALL_FUNCTION_2       2 
         182  POP_TOP          
         183  JUMP_FORWARD          0  'to 186'
       186_0  COME_FROM                '183'

 328     186  LOAD_FAST             0  'self'
         189  LOAD_ATTR            16  'init_from_dict_base'
         192  LOAD_FAST             1  'bdict'
         195  CALL_FUNCTION_1       1 
         198  POP_TOP          

 329     199  LOAD_FAST             0  'self'
         202  LOAD_ATTR            17  'init_map_size'
         205  CALL_FUNCTION_0       0 
         208  POP_TOP          

 331     209  LOAD_FAST             0  'self'
         212  LOAD_ATTR             2  'meta_tag'
         215  POP_JUMP_IF_FALSE   237  'to 237'

 332     218  LOAD_FAST             0  'self'
         221  LOAD_ATTR            15  '_call_meta_member_func'
         224  LOAD_CONST            9  '_init_@_completed'
         227  LOAD_FAST             1  'bdict'
         230  CALL_FUNCTION_2       2 
         233  POP_TOP          
         234  JUMP_FORWARD          0  'to 237'
       237_0  COME_FROM                '234'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def init_map_size(self):
        from common.cfg import confmgr
        conf = confmgr.get('map_config', str(self.map_id), default={})
        l_pos = conf.get('walkLowerLeftPos', [-350 * NEOX_UNIT_SCALE, -600 * NEOX_UNIT_SCALE])
        r_pos = conf.get('walkUpRightPos', [480 * NEOX_UNIT_SCALE, 390 * NEOX_UNIT_SCALE])
        self._min_x = l_pos[0]
        self._max_x = r_pos[0]
        self._min_z = l_pos[1]
        self._max_z = r_pos[1]

    def get_map_size(self):
        return (
         self._min_x, self._max_x, self._min_z, self._max_z)

    def init_battle_scene(self, scene_data):
        if not global_data.player.is_restore_battle and global_data.scene_type == scene_type.SCENE_TYPE_LOBBY and not scene_data['is_spectate']:
            global_data.ex_scene_mgr_agent.pop_all_lobby_relative_scene()
            from logic.comsys.movie.MovieUI import MovieUI
            MovieUI()
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                global_data.emgr.play_anchor_voice.emit('101_begin')
            global_data.emgr.trigger_lobby_player_move_stop.emit()
            self.try_play_boarding_movie(scene_data)
            if not global_data.player.in_local_battle():
                global_data.sound_mgr.delay_stop_music()
        else:
            self.load_scene(scene_data)
        AccInput()

    def try_play_boarding_movie(self, scene_data):
        from common.cinematic.movie_controller import MovieController
        boarding_movie_data = self.boarding_movie_data()
        if boarding_movie_data:
            if self.need_pvp_loading():
                MovieController().start(boarding_movie_data, lambda : self.try_create_pvp_loading(scene_data))
            else:
                MovieController().start(boarding_movie_data, lambda : self.load_scene(scene_data))
        else:
            self.load_scene(scene_data)

    def try_create_pvp_loading(self, scene_data):
        try:
            from logic.comsys.loading.battle_loading import PlayerListLoadingWidget, SnatchEggPlayerListLoadingWidget
            from common.utils.timer import CLOCK
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SNATCHEGG):
                SnatchEggPlayerListLoadingWidget(map_id=self.map_id)
            else:
                PlayerListLoadingWidget(map_id=self.map_id)
            self._delay_load_scene_timer = game3d.delay_exec(1000, lambda scn_data=scene_data: self.load_scene(scn_data))
        except:
            global_data.ui_mgr.close_ui('PlayerListLoadingWidget')
            global_data.ui_mgr.close_ui('SnatchEggPlayerListLoadingWidget')
            self.clear_delay_load_scene_timer()
            self.load_scene(scene_data)

    def clear_delay_load_scene_timer(self):
        if self._delay_load_scene_timer:
            game3d.cancel_delay_exec(self._delay_load_scene_timer)
            self._delay_load_scene_timer = None
        return

    def boarding_movie_data(self):
        from data.battle_trans_anim import Getmecha_boarding_tdm
        return Getmecha_boarding_tdm()

    def on_player_parachute_stage_changed(self, stage):
        pass

    def _on_scene_cam_observe_player_setted(self):
        if self._mvp_id is not None:
            self._refresh_mvp_mark(self._mvp_id)
        return

    def destroy(self, clear_cache=True):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            _path = os.path.join(game3d.get_doc_dir(), 'in_battle_flag')
            if os.path.exists(_path):
                try:
                    os.remove(_path)
                except:
                    pass

        if self._battle_status == Battle.BATTLE_STATUS_FINISH:
            return
        else:
            if self.meta_tag:
                self._call_meta_member_func('_destroy_@', clear_cache)
            if global_data.player and self.has_quit and not global_data.player.in_local_battle() and not global_data.player.local_battle:
                global_data.player.quit_battle(True)
            global_data.anticheat_utils.force_stop_detact()
            if global_data.player:
                self.remove_entity_imp(global_data.player.id)
            self.on_battle_status_changed(Battle.BATTLE_STATUS_FINISH)
            global_data.game_mgr.unregister_logic_timer(self._chunk_check_timer_id)
            game.on_chunk_changed = None
            if global_data.player:
                global_data.player.leave_join_battle()
            global_data.emgr.net_reconnect_event -= self.on_reconnected
            global_data.emgr.on_player_parachute_stage_changed -= self.on_player_parachute_stage_changed
            global_data.emgr.scene_camera_switch_player_setted_event -= self._on_scene_cam_observe_player_setted
            global_data.emgr.scene_after_enter_event -= self._on_enter_scene
            self.destroy_all_entities()
            if clear_cache:
                EntityPool.clear()
            AccInput().switch_acc_input_open_condition(OPEN_CONDITION_NONE)
            import wwise
            wwise.SoundEngine.SetRTPCValue('game_settlement', 0)
            global_data.sound_mgr.exit_battle()
            global_data.carry_mgr.exit_battle()
            self.clear_switch_timer()
            super(Battle, self).destroy()
            self._sync_handler = None
            global_data.game_voice_mgr.exit_battle_event()
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            SettleSystem.finalize()
            global_data.battle = None
            global_data.battle_idx = 0
            if self._ui_confirm_playerid:
                global_data.sound_mgr.stop_playing_id(self._ui_confirm_playerid)
                self._ui_confirm_playerid = None
            import logic.gcommon.const as gconst
            global_data.ccmini_mgr.stop_capture(gconst.TEAM_ALL_SESSION_ID)
            self.clear_delay_load_scene_timer()
            global_data.war_lrobots = {}
            from common.crashhunter import crashhunter_utils
            crashhunter_utils.check_shader_compile_error()
            return

    def on_reconnected(self, *args):
        if global_data.player.is_in_global_spectate():
            global_data.player._spectate_mgr.on_reconnected()
            return
        global_data.emgr.net_reconnect_before_destroy_event.emit(*args)
        self.destroy(False)

    def load_scene(self, scene_data):
        scene_data.update({'map_id': self.map_id})
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if lobby_ui:
            lobby_ui.disable_click_match_btn()
        map_data_conf = confmgr.get('map_config', str(self.map_id), default={})
        scene_type = map_data_conf.get('cScene', 'Traning')
        scene_path = self._scene_path if self._scene_path else map_data_conf.get('cSceneName', None)
        if scene_path:
            scene_data.update({'scene_path': scene_path})
        preload_cockpit = scene_data.get('preload_cockpit', False)
        scene = global_data.game_mgr.scene
        is_same_scene = scene and scene.is_same_scene(scene_type, scene_data)
        if is_same_scene:
            if scene.is_loaded():
                self.load_finish()
        else:
            cb = preload_cockpit or self.load_finish if 1 else None
            global_data.game_mgr.load_scene(scene_type, scene_data, cb)
        return

    def load_finish(self):
        if global_data.battle and global_data.battle != self:
            global_data.battle.load_finish()
            return
        if not (global_data.player and (global_data.player.is_battle_replaying() or global_data.player.is_in_global_spectate())):
            _path = os.path.join(game3d.get_doc_dir(), 'in_battle_flag')
            last_crashed = False
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                if os.path.exists(_path):
                    last_crashed = True
                    try:
                        os.remove(_path)
                    except:
                        last_crashed = False

            global_data.player.on_loaded_battle(last_crashed)
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                try:
                    f = open(_path, 'w+')
                    f.close()
                except:
                    pass

            from logic.gcommon.common_utils import battle_utils
            battle_utils.inc_play_mode_enter_time(self.map_id)
        global_data.emgr.battle_logic_ready_event.emit()
        global_data.carry_mgr.enter_battle()
        self.close_lobby_ui()
        game.on_chunk_changed = self.on_chunk_changed
        if global_data.player and global_data.player.is_battle_replaying():
            global_data.player.battle_replay_start()
        if global_data.player and global_data.player.is_in_global_spectate():
            global_data.player.global_spectate_start()

    def on_preload_cockpit_complete(self):
        global_data.game_mgr.active_cur_scene(True)
        self.load_finish()

    def is_nan_pos(self, pos):
        return pos.x != pos.x or pos.y != pos.y or pos.z != pos.z

    def chunk_check_timer(self, *args):
        player = global_data.cam_lplayer
        if player and global_data.player and global_data.player.logic and global_data.player.logic == player:
            from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_PLANE, STAGE_NONE, STAGE_LAND
            parachute_stage = player.share_data.ref_parachute_stage
            ignore_prachute_stage = parachute_stage in (STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE, STAGE_PLANE, STAGE_NONE)
            if ignore_prachute_stage:
                return RELEASE
            scene = self.get_scene()
            check_position = player.ev_g_position()
            if not check_position:
                check_position = scene.viewer_position
            nan_pos = self.is_nan_pos(check_position)
            if not nan_pos and scene.check_collision_loaded(check_position, True):
                return RELEASE
            if check_position.y < self._force_check_height:
                player.send_event('E_REWAIT_DETAIL')
                control_target = player.ev_g_control_target()
                if control_target and control_target.logic and control_target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                    control_target.logic.send_event('E_REWAIT_DETAIL')
                return RELEASE
            return False
        return RELEASE

    def on_chunk_changed(self):
        global_data.game_mgr.unregister_logic_timer(self._chunk_check_timer_id)
        if self.chunk_check_timer() != RELEASE:
            self._chunk_check_timer_id = global_data.game_mgr.register_logic_timer(self.chunk_check_timer, interval=1, times=-1, mode=LOGIC)
        global_data.emgr.scene_chunk_changed.emit()

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_num = stage_dict.get('prepare_num', 0)
        player_num = stage_dict.get('fighter_num', 0)
        prepare_timestamp = stage_dict.get('prepare_timestamp', 0)
        flight_dict = stage_dict.get('flight_dict', {})
        self.update_prepare_num((prepare_num, player_num))
        self.flight_dict = flight_dict
        self.prepare_timestamp = prepare_timestamp
        self.on_battle_status_changed(Battle.BATTLE_STATUS_PREPARE)
        global_data.emgr.battle_change_prepare_timestamp.emit()

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def parachute_stage(self, stage_dict):
        prepare_num = stage_dict.get('prepare_num', 0)
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        flight_dict = stage_dict.get('flight_dict', {})
        self.poison_circle = poison_circle
        if not flight_dict:
            return
        lavatar = global_data.player.logic
        from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE, STAGE_ISLAND
        from logic.comsys.accelerometer.AccInput import AccInput
        self.update_prepare_num((prepare_num, player_num))
        self.flight_dict = flight_dict
        AccInput().switch_acc_input_open_condition(OPEN_CONDITION_NONE)
        lavatar.send_event('E_INIT_PARACHUTE_COM')
        from logic.gutils import judge_utils
        is_ob = judge_utils.is_ob()
        exclude_list = [
         global_data.player.id]
        if not is_ob:
            exclude_list = global_data.player.logic.ev_g_groupmate() or exclude_list
            all_puppet = EntityManager.get_entities_by_type('Puppet')
            for k, v in six.iteritems(all_puppet):
                if k in exclude_list:
                    continue
                if not v.logic:
                    continue
                if not v.logic.ev_g_in_parachute_stage_idle():
                    exclude_list.append(k)

        else:
            all_puppet = EntityManager.get_entities_by_type('Puppet')
            p_list = six_ex.keys(all_puppet)
            p_list = list(p_list)
            exclude_list.extend(p_list)
        self.destroy_all_entities(exclude=exclude_list)
        psg_list = []
        if is_ob:
            exclude_list = exclude_list[1:]
        for eid in exclude_list:
            ent = EntityManager.getentity(eid)
            if ent and ent.logic:
                ent_stage = ent.logic.share_data.ref_parachute_stage
                if ent_stage in (STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE, STAGE_ISLAND):
                    psg_list.append(eid)
                    ent.logic.reset()
                if ent_stage in (STAGE_NONE, STAGE_MECHA_READY, STAGE_ISLAND):
                    ent.logic.send_event('E_PLANE')
                    ent.logic.send_event('E_UNLIMIT_HEIGHT')

        self._check_create_plane()
        if self.plane and self.plane():
            global_data.emgr.plane_set_passenger_event.emit(psg_list)
            if lavatar.id == lavatar.ev_g_spectate_target_id():
                if lavatar.id in psg_list:
                    if plane.logic:
                        cur_plane_yaw = plane.logic.ev_g_plane_cur_yaw()
                        global_data.emgr.camera_set_yaw_event.emit(cur_plane_yaw)
            plane_start_timestamp = flight_dict['start_timestamp']
            dt = max(0, flight_dict['ready_time'] - max(0, time() - plane_start_timestamp))
            if dt > 0:
                import game3d
                game3d.delay_exec(dt * 1000, lambda : self.plane_stage_start())
            else:
                self.plane_stage_start()
        lavatar.send_event('E_CLEAN_JUMP')
        global_data.sound_mgr.play_music('flight')
        global_data.sound_mgr.poison_level = 0
        self.on_battle_status_changed(Battle.BATTLE_STATUS_PARACHUTE)

    def _check_create_plane(self):
        if self.plane and self.plane():
            return
        if not self.flight_dict:
            return
        flight_dict = self.flight_dict
        self._plane_start_timestamp = flight_dict['start_timestamp']
        from mobile.common.IdManager import IdManager
        self.plane_id = IdManager.genid()
        plane = self.create_entity('Plane', self.plane_id, -1, flight_dict)
        import weakref
        self.plane = weakref.ref(plane)
        global_data.emgr.draw_airline_event.emit(math3d.vector(*flight_dict['start_pos']), math3d.vector(*flight_dict['end_pos']))

    def plane_stage_start(self):
        self._plane_start = True
        global_data.emgr.plane_stage_start_event.emit()

    @property
    def plane_started(self):
        return self._plane_start

    def get_airline_pos(self):
        if not self.flight_dict:
            return None
        else:
            return (
             math3d.vector(*self.flight_dict['start_pos']), math3d.vector(*self.flight_dict['end_pos']))

    def get_move_range(self):
        return {}

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        battle_mark = stage_dict.get('mark_dict', {})
        self.update_player_num((player_num,))
        self.on_battle_status_changed(Battle.BATTLE_STATUS_FIGHT)
        global_data.player.logic and global_data.player.logic.send_event('E_START_POSITION_CHECKER')
        self.init_poison_circle(poison_circle)
        global_mark_dict = battle_mark.get('global_mark_dict', {})
        group_mark_dict = battle_mark.get('group_mark_dict', {})
        soul_mark_dict = battle_mark.get('soul_mark_dict', {})
        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(global_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(group_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(soul_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

    @rpc_method(CLIENT_STUB, (Int('pre_time'),))
    def pre_ace_stage(self, pre_time):
        self.pre_ace_stage_helper(pre_time)

    def pre_ace_stage_helper(self, pre_time):
        message = {'i_type': battle_const.MAIN_WILL_ACE_TIME,'content_txt': get_text_by_id(81158, {'sec': pre_time})
           }
        global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, ())
    def ace_stage(self):
        self.is_in_ace_state = True
        message = [{'i_type': battle_const.MAIN_SOUND_VISIBLE_INFO}, {'i_type': battle_const.MAIN_MECHA_RECALL_INFO}, {'i_type': battle_const.MAIN_ACE_TIME}]
        message_type = [battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)
        global_data.emgr.battle_into_ace_stage_event.emit()

    @rpc_method(CLIENT_STUB, (Int('group_num'), Dict('disable_dict')))
    def disable_stage(self, group_num, disable_dict):
        if not global_data.player or not global_data.player.logic:
            return
        if not global_data.player.logic.ev_g_all_groupmates_dead() and self.get_battle_play_type() not in (battle_const.PLAY_TYPE_GVG,):
            global_data.emgr.show_death_replay_event.emit(self.battle_tid, group_num, disable_dict)
        global_data.emgr.scene_show_teammate_name_event.emit(False)

    @rpc_method(CLIENT_STUB, (Int('alive_fighter_num'), Dict('settle_dict'), Dict('team_dict'), Dict('achivement'), Int('totol_fighter_num')))
    def settle_stage(self, alive_fighter_num, settle_dict, team_dict, achievement, totol_fighter_num):
        if settle_dict.get('kicked', False):
            return
        self.on_settle_stage_msg(alive_fighter_num, settle_dict, team_dict, achievement, totol_fighter_num)
        if global_data.is_inner_server:
            print('[Battle] settle stage:', settle_dict.get('highlight_moment', []))
        if self._in_recording_video:
            from logic.comsys.video.VideoRecord import VideoRecord
            VideoRecord().stop_battle_record(settle_dict.get('highlight_moment', []), 2)
            self._in_recording_video = False

    def on_settle_stage_msg(self, alive_fighter_num, settle_dict, team_dict, achievement, totol_fighter_num):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            self.is_settle = True
            from logic.gcommon.ctypes.BattleReward import BattleReward
            battle_reward = BattleReward()
            battle_reward.init_from_dict(settle_dict.get('reward', {}))
            statistics = settle_dict.get('statistics', {})
            enemy_dict = settle_dict.get('enemy_info', {})
            self._enemy_dict = {}
            self._teammate_dict = {}
            for enemy_info_key, enemy_info in six.iteritems(enemy_dict):
                eid = str(enemy_info_key)
                self._enemy_dict[eid] = {}
                self._enemy_dict[eid]['mecha_id'] = enemy_info.get('mecha_id', None)
                self._enemy_dict[eid]['role_id'] = enemy_info.get('role_id', None)

            for teammate_info_key, teammate_info in six.iteritems(team_dict):
                eid = str(teammate_info_key)
                self._teammate_dict[eid] = {}
                self._teammate_dict[eid]['mecha_id'] = teammate_info.get('mecha_id', None)
                self._teammate_dict[eid]['role_id'] = teammate_info.get('role_id', None)

            self._settle_stage_arrive_time = tutil.get_server_time()
            self._is_winner = settle_dict.get('rank') == 1
            global_data.emgr.settle_stage_event.emit(self.battle_tid, alive_fighter_num, settle_dict, battle_reward, team_dict, enemy_dict, achievement, totol_fighter_num)
            global_data.emgr.scene_show_teammate_name_event.emit(False)
            return

    def get_settle_stage_arrive_time(self):
        return self._settle_stage_arrive_time

    def is_in_settle_celebrate_stage(self):
        if self.is_settle and self._is_winner:
            return True
        else:
            return False

    def is_settled(self):
        return self.is_settle

    def init_battle_status(self, bdict):
        self.init_timestamp = bdict.get('init_timestamp', 0)
        self.battle_tid = bdict.get('battle_type')
        self.map_id = bdict.get('map_id')
        self.alive_player_num = bdict['player_num']
        self.statistics = bdict.get('statistics', {})
        self.group_kill_statistics = bdict.get('group_kill_statistics', 0)
        self.prepare_timestamp = bdict['prepare_timestamp'] or bdict['predict_timestamp']
        self.is_in_ace_state = bdict.get('is_in_ace_state', False)
        self.need_show_enemy_pos = bdict.get('need_show_enemy_pos', False)
        self._mvp_info = bdict.get('mvp_info', {})
        self._ob_in_battle = bdict.get('ob_in_battle', False)
        self._flight_time = bdict.get('flight_time', 0)
        self._battle_status = bdict.get('battle_status', Battle.BATTLE_STATUS_INIT)
        from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
        CGameModeManager().set_enviroment(bdict.get('environment', None))
        CGameModeManager().set_map(self.map_id, self.battle_tid)
        confmgr.change_to_pve(global_data.game_mode.is_pve())
        self.__check_is_in_island()
        from logic.vscene.parts.camera.camera_controller.CameraData import CameraData
        CameraData()
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_KING):
            global_data.emgr.scene_reset_poison_level.emit(battle_const.BATTLE_SOUND_STATE_LOW)
        global_data.emgr.battle_change_prepare_timestamp.emit()
        self._mvp_id = bdict.get('mvp_id', None)
        if not self._mvp_id:
            self._mvp_id = bdict.get('mvp_eid', None)
        self._ai_level = bdict.get('ai_level', 1)
        self._ai_hit_box = bdict.get('ai_hit_box', 1.0)
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        return

    def avatar_has_mecha(self, mecha_id):
        server_ok = mecha_id in self._avatar_mecha_dict
        from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
        return server_ok and mecha_has_owned_by_mecha_id(mecha_id)

    def get_ai_level(self):
        return self._ai_level

    def on_battle_status_changed(self, status):
        self._battle_status = status
        self.__check_is_in_island()
        global_data.emgr.on_battle_status_changed.emit(self._battle_status)

    def get_battle_tid(self):
        return self.battle_tid

    def get_battle_play_type(self):
        return battle_utils.get_play_type_by_battle_id(self.battle_tid)

    def get_map_id(self):
        return self.map_id

    def get_flight_time(self):
        return self._flight_time

    def has_judges(self):
        return self._ob_in_battle

    def update_battle_statistics(self, obj_id, kill, kill_mecha, assist_mecha):
        killer_statistics = self.statistics.get(obj_id, {})
        killer_statistics['kill'] = kill
        killer_statistics['kill_mecha'] = kill_mecha
        killer_statistics['assist_mecha'] = assist_mecha
        self.statistics[obj_id] = killer_statistics

    def close_lobby_ui(self):
        global_data.ui_mgr.close_ui('LobbyUI')
        global_data.ui_mgr.close_ui('MatchMode')
        global_data.ui_mgr.close_ui('MainChat')
        global_data.ui_mgr.close_ui('MainFriend')
        global_data.ui_mgr.close_ui('MainRank')
        global_data.ui_mgr.close_ui('PlayerInfoUI')
        global_data.ui_mgr.close_ui('ActivityMain')
        global_data.ui_mgr.close_ui('ActivityCenterMainUI')
        global_data.ui_mgr.close_ui('ActivityGranbelmMainUI')
        global_data.ui_mgr.close_ui('LobbyCommonBgUI')
        global_data.ui_mgr.close_ui('ModelArrowUI')
        global_data.ui_mgr.close_ui('PVEMainUI')
        if global_data.redpoint_mgr:
            global_data.redpoint_mgr.remove_all_elems()

    def is_battle_prepare_stage(self, battle_status=None):
        battle_status = battle_status or self._battle_status
        return battle_status <= Battle.BATTLE_STATUS_PREPARE

    def is_battle_init_status(self):
        return self._battle_status == Battle.BATTLE_STATUS_INIT

    def is_battle_fight_stage(self, battle_status=None):
        battle_status = battle_status or self._battle_status
        return battle_status >= Battle.BATTLE_STATUS_FIGHT

    def __check_is_in_island(self):
        from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
        if self._battle_status == Battle.BATTLE_STATUS_PREPARE and CGameModeManager().is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):

            def _is_in_island():
                if self._save_init_bdict:
                    prepare_time = self._save_init_bdict.get('prepare_timestamp', 0)
                    left_time = max(0, prepare_time - tutil.get_server_time())
                    return left_time > parachute_utils.PARACHUTE_ANIM_TIME

            self.is_in_island = _is_in_island
        else:
            self.is_in_island = lambda : False
            global_data.emgr.battle_island_finish.emit()

    @rpc_method(CLIENT_STUB, (Int('prepare_num'), Int('player_num')))
    def update_prepare_num(self, prepare_num, player_num):
        self.prepare_num = prepare_num
        prepare_ui = global_data.ui_mgr.get_ui('PrepareUI')
        if prepare_ui:
            prepare_ui.update_preparing_player_num(prepare_num)
        self.update_player_num((player_num,))

    @rpc_method(CLIENT_STUB, (Int('player_num'),))
    def update_player_num(self, player_num):
        self.alive_player_num = player_num
        global_data.emgr.update_alive_player_num_event.emit(player_num)

    @rpc_method(CLIENT_STUB, (Dict('report_dict'),))
    def battle_report(self, report_dict):
        killer_id, injured_id, _ = battle_utils.parse_battle_report_death(report_dict)
        if killer_id:
            killer_statistics = self.statistics.get(killer_id, {})
            killer_statistics['kill'] = killer_statistics.get('kill', 0) + 1
            self.statistics[killer_id] = killer_statistics
            global_data.emgr.update_player_kill_num_event.emit(killer_id, killer_statistics)
            if global_data.cam_lplayer and killer_id == global_data.cam_lplayer.id:
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'kill_people'))
                global_data.emgr.play_game_voice.emit('h_kill_human')
        mecha_killer_id, mecha_injured_id = battle_utils.parse_battle_report_mecha_death(report_dict)
        if mecha_killer_id:
            killer_statistics = self.statistics.get(mecha_killer_id, {})
            killer_statistics['kill_mecha'] = killer_statistics.get('kill_mecha', 0) + 1
            self.statistics[mecha_killer_id] = killer_statistics
            global_data.emgr.on_target_kill_mecha_event.emit(mecha_killer_id, mecha_injured_id, killer_statistics)
            if global_data.cam_lplayer and mecha_killer_id == global_data.cam_lplayer.id:
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'kill_ui'))
                global_data.emgr.play_game_voice.emit('h_kill_mecha')
        for killer_id in report_dict.get('killer_assisters', []):
            killer_statistics = self.statistics.get(killer_id, {})
            killer_statistics['assist_mecha'] = killer_statistics.get('assist_mecha', 0) + 1
            self.statistics[killer_id] = killer_statistics

        global_data.emgr.show_battle_report_event.emit(report_dict)
        self.on_receive_report_dict(report_dict)

    def on_receive_report_dict(self, report_dict):
        pass

    def get_entity(self, entity_id):
        return EntityManager.getentity(entity_id)

    def move_entity(self, entity_id, x, y, z):
        pass

    def destroy_all_entities(self, exclude=()):
        for entity_id in six_ex.keys(self._entity_dict):
            if exclude and entity_id in exclude:
                continue
            del_entity = EntityManager.getentity(entity_id)
            self.destroy_entity(entity_id)

    def reset_entity_imp(self, entity_id):
        entity = EntityManager.getentity(entity_id)
        if entity and entity.logic:
            entity.logic.reset()

    def reset_all_entities(self, entity_id_list):
        for entity_id in entity_id_list:
            self.reset_entity_imp(entity_id)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('entity_aoi_id'), Dict('entity_dict')))
    def add_entity(self, entity_id, entity_aoi_id, entity_dict):
        entity = EntityManager.getentity(entity_id)
        if not entity:
            return
        if entity_id in self._entity_dict:
            entity.on_remove_from_battle()
            self._entity_dict.pop(entity_id)
        entity.update_data_from_dict(entity_dict)
        self.add_entity_imp(entity_id, entity_aoi_id)
        global_data.emgr.scene_add_entity_event.emit(entity_id)

    def local_add_entity(self, entity_id, entity_aoi_id, entity_dict):
        entity = EntityManager.getentity(entity_id)
        if not entity:
            return
        entity.update_data_from_dict(entity_dict)
        self.add_entity_imp(entity_id, entity_aoi_id)
        global_data.emgr.scene_add_entity_event.emit(entity_id)

    def entity_in_battle(self, entity_id):
        if entity_id in self._entity_dict:
            return True
        return False

    def add_entity_imp(self, entity_id, entity_aoi_id=None):
        if entity_id in self._entity_dict:
            self.logger.error('Cannot add existed entity to battle : ent_id, %s', entity_id)
            return
        else:
            entity = EntityManager.getentity(entity_id)
            if entity is None:
                self.logger.error('Cannot add non-existed entity to battle : ent_id, %s', entity_id)
                return
            self._entity_dict[entity_id] = entity_aoi_id
            if entity_aoi_id is not None and entity_aoi_id > 0:
                self._entity_aoi_id_dict[entity_aoi_id] = entity_id
            entity.on_add_to_battle(self.id)
            return

    def get_entity_aoi_id(self, entity_id):
        return self._entity_dict.get(entity_id)

    def update_entity_imp(self, entity_id, entity_aoi_id=None):
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            self.logger.error('update entity is None : ent_id, %s', entity_id)
            return
        else:
            entity.on_update_to_battle(self.id)
            old_aoi_id = self._entity_dict.get(entity_id)
            self._entity_dict[entity_id] = entity_aoi_id
            if entity_aoi_id is not None and entity_aoi_id > 0:
                self._entity_aoi_id_dict.pop(old_aoi_id, None)
                self._entity_aoi_id_dict[entity_aoi_id] = entity_id
            try:
                if entity.logic:
                    entity.logic.send_event('E_ON_AOI_ID_CHANGED')
            except Exception as e:
                self.logger.log_last_except()
                exception_hook.upload_exception(*sys.exc_info())

            return

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'),))
    def remove_entity(self, entity_id):
        self.remove_entity_imp(entity_id)
        global_data.emgr.scene_remove_entity_event.emit(entity_id)

    def local_remove_entity(self, entity_id):
        self.remove_entity_imp(entity_id)
        global_data.emgr.scene_remove_entity_event.emit(entity_id)

    def remove_entity_imp(self, entity_id):
        if entity_id not in self._entity_dict:
            return
        else:
            entity = EntityManager.getentity(entity_id)
            if entity is None:
                return
            entity.on_remove_from_battle()
            entity_aoi_id = self._entity_dict.pop(entity_id, None)
            self._entity_aoi_id_dict.pop(entity_aoi_id, None)
            return entity

    def call_soul_method(self, methodname, parameters=()):
        if global_data.player:
            global_data.player.call_soul_method(methodname, parameters, self.id)

    def call_soul_method_misty(self, methodname, parameters=()):
        if global_data.player:
            global_data.player.call_misty_soul_method(methodname, parameters, self.id)

    def tick(self, delta):
        self._sync_delta_time += delta
        if self._sync_delta_time >= 0.03:
            self._do_sync_logic_entity()
            self._sync_delta_time = 0
        if self.meta_tag:
            self._call_meta_member_func('_tick_@', delta)

    def sync_logic_entity(self, sync_id, methodname, parameters):
        if self._sync_queue and self._sync_queue[-1][0] == sync_id:
            self._sync_queue[-1][1].append((methodname, parameters))
        else:
            self._sync_queue.append((sync_id, [(methodname, parameters)]))

    def sync_logic_entity_misty(self, sync_id, methodname, parameters):
        if self._sync_queue_misty and self._sync_queue_misty[-1][0] == sync_id:
            self._sync_queue_misty[-1][1].append((methodname, parameters))
        else:
            self._sync_queue_misty.append((sync_id, [(methodname, parameters)]))

    def _do_sync_logic_entity(self):
        if self._sync_queue:
            sync_queue = self._sync_queue
            self._sync_queue = []
            self.call_soul_method('sync_battle', (sync_queue,))
        if self._sync_queue_misty:
            sync_queue = self._sync_queue_misty
            self._sync_queue_misty = []
            self.call_misty_soul_method('sync_battle_misty', (sync_queue,))

    @rpc_method(CLIENT_STUB, (List('method_pack'),))
    def sync_battle(self, method_pack):
        self.sync_battle_direct(method_pack)

    @rpc_method(CLIENT_STUB, (List('method_pack'),))
    def sync_battle_misty(self, method_pack):
        self.sync_battle_direct(method_pack)

    def sync_battle_direct(self, method_pack):
        for data in method_pack:
            try:
                self._sync_handler[data[0]](*data[1:])
            except Exception as e:
                self.logger.log_last_except()
                exception_hook.upload_exception(*sys.exc_info())

    def battle_method(self, method_index, parameters):
        methodname = RpcIndexer.INDEX2RPC[method_index]
        method = getattr(self, methodname, None)
        method(parameters)
        return

    def create_entity(self, entity_type, entity_id, entity_aoi_id, entity_dict):
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            entity = EntityPool.create_entity(entity_type, entity_id)
            entity.init_from_dict(entity_dict)
            self.add_entity_imp(entity_id, entity_aoi_id)
        else:
            entity.update_from_dict(entity_dict)
            self.update_entity_imp(entity_id, entity_aoi_id)
        return entity

    def destroy_entity(self, entity_id):
        entity = self.remove_entity_imp(entity_id)
        if entity:
            EntityPool.destroy_entity(entity)
            return True
        return False

    def get_entity_by_aoi_id(self, aoi_id):
        entity_id = self._entity_aoi_id_dict.get(aoi_id, None)
        if entity_id is not None:
            return EntityManager.getentity(entity_id)
        else:
            return

    def aoi_2_entity_id(self, aoi_id):
        return self._entity_aoi_id_dict.get(aoi_id, None)

    def logic_entity(self, sync_id, method_name, parameters):
        entity_id = None
        try:
            entity_id = self._entity_aoi_id_dict.get(sync_id, None) or IdManager.str2id(sync_id)
            entity = EntityManager.getentity(entity_id)
        except:
            entity = None

        if entity is None:
            from logic.gcommon.component.proto.client import methods
            log_name = methods.get(method_name, method_name)
            self.logger.error('Cannot sync non-existed entity to battle, sync_id, %s %s %s %s', sync_id, str(entity_id), log_name, parameters)
            return
        else:
            if entity.logic is None or not entity.logic.is_enable():
                return
            entity.logic.sd.ref_sync_method(method_name, parameters)
            return

    def init_poison_circle(self, poison_dict):
        from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_STABLE, POISON_CIRCLE_STATE_REDUCE, POISON_CIRCLE_STATE_OVER
        if not poison_dict:
            return
        state = poison_dict['state']
        refresh_time = poison_dict['refresh_time']
        last_time = poison_dict['last_time']
        level = poison_dict['level']
        poison_point = poison_dict['poison_point']
        safe_point = poison_dict['safe_point']
        reduce_type = poison_dict['reduce_type']
        if state in (POISON_CIRCLE_STATE_STABLE, POISON_CIRCLE_STATE_OVER):
            self.refresh_poison_circle((state, reduce_type, refresh_time, last_time, level, poison_point, safe_point))
        elif state == POISON_CIRCLE_STATE_REDUCE:
            self.refresh_poison_circle((state, reduce_type, 0, 0, level, poison_point, safe_point))
            self.reduce_poison_circle((state, reduce_type, refresh_time, last_time))
        global_data.emgr.scene_reset_poison_level.emit(level)

    @rpc_method(CLIENT_STUB, (Int('state'), Float('refresh_time'), Float('last_time')))
    def start_poison_circle(self, state, refresh_time, last_time):
        global_data.emgr.scene_start_poison_circle_event.emit(state, refresh_time, last_time)

    @rpc_method(CLIENT_STUB, (Int('state'), Int('reduce_type'), Float('refresh_time'), Float('last_time'), Int('level'), List('poison_point'), List('safe_point')))
    def refresh_poison_circle(self, state, reduce_type, refresh_time, last_time, level, poison_point, safe_point):
        global_data.emgr.scene_refresh_poison_circle_event.emit(state, refresh_time, last_time, level, poison_point, safe_point, reduce_type)
        global_data.emgr.scene_reset_poison_level.emit(level)

    @rpc_method(CLIENT_STUB, (Int('state'), Int('reduce_type'), Float('refresh_time'), Float('last_time')))
    def reduce_poison_circle(self, state, reduce_type, refresh_time, last_time):
        global_data.emgr.scene_reduce_poison_circle_event.emit(state, refresh_time, last_time, reduce_type)
        global_data.sound_mgr.play_ui_sound('remind')

    @rpc_method(CLIENT_STUB, (Dict('explose_info'),))
    def throwable_item_explosion(self, explose_info):
        global_data.emgr.scene_throw_item_explosion_event.emit(explose_info, is_time_out=True)

    @rpc_method(CLIENT_STUB, (List('unique_keys'),))
    def remove_throwable_item(self, unique_keys):
        global_data.emgr.scene_remove_throw_items_event.emit(unique_keys)

    @rpc_method(CLIENT_STUB, (Int('mark_id'), Int('mark_no'), List('point'), Bool('is_deep'), Int('state'), Float('create_timestamp'), Float('deep_timestamp')))
    def add_mark(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

    def add_mark_imp(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        global_data.emgr.scene_add_mark.emit(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

    @rpc_method(CLIENT_STUB, (Int('mark_id'), Bool('is_deep'), Int('state'), Float('deep_timestamp')))
    def deep_mark(self, mark_id, is_deep, state, deep_timestamp):
        global_data.emgr.scene_deep_mark.emit(mark_id, is_deep, state, deep_timestamp)

    @rpc_method(CLIENT_STUB, (Int('mark_id'),))
    def del_mark(self, mark_id):
        global_data.emgr.scene_del_mark.emit(mark_id)

    @rpc_method(CLIENT_STUB, (Int('mark_id'), List('point'), List('state')))
    def update_ai_mark(self, mark_id, point, state):
        global_data.emgr.scene_ai_mark.emit(mark_id, point, state)

    def get_scene(self):
        return global_data.game_mgr.get_cur_scene()

    @property
    def battle_status(self):
        return self._battle_status

    def is_single_person_battle(self):
        return confmgr.get('battle_config', str(self.battle_tid), default={}).get('cTeamNum', 1) == 1

    @rpc_method(CLIENT_STUB, (List('paradrops'),))
    def show_paradrop_tip(self, paradrops):
        _, paradrop_no, _, _ = paradrops[0]
        from logic.gcommon.common_const import battle_const
        from logic.gcommon.common_const.paradrop_const import PARADROP_BALL
        m_type = battle_const.UP_NODE_PARADROP_BALL if paradrop_no == PARADROP_BALL else battle_const.UP_NODE_PARADROP
        global_data.emgr.battle_event_message.emit(paradrops, message_type=m_type)

    @rpc_method(CLIENT_STUB, (Uuid('paradrop_id'),))
    def hide_paradrop_tip(self, paradrop_id):
        global_data.emgr.scene_del_paradrop.emit(paradrop_id)

    @rpc_method(CLIENT_STUB, (Dict('msg'),))
    def group_message(self, msg):
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return
        unit_id = msg['id']
        unit_name = msg['char_name']
        msg['msg']['head_frame'] = msg['head_frame']
        msg['msg']['role_id'] = msg['role_id']
        global_data.emgr.add_battle_group_msg_event.emit(unit_id, unit_name, msg)
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_ADD_GROUP_HISTORY_MSG', unit_id, unit_name, msg['msg'])

    @rpc_method(CLIENT_STUB, (Dict('chat_info'),))
    def battle_encourage_teammates(self, chat_info):
        self.on_battle_encourage_teammates(chat_info)

    def on_battle_encourage_teammates(self, chat_info):
        from logic.gutils.role_head_utils import get_head_frame_res_path, get_head_photo_res_path
        unit_name = chat_info['char_name']
        head_photo = chat_info['head_photo']
        msg = chat_info['msg']
        feed_item = global_data.uisystem.load_template_create('battle_before/i_fight_interact_tips')
        text = msg
        feed_item.lab_tips.SetString(text)
        res_path = get_head_photo_res_path(head_photo)
        feed_item.icon_head.SetDisplayFrameByPath('', res_path)
        from logic.comsys.common_ui.NoticeUI import NoticeUI
        notice_ui = NoticeUI()
        notice_ui.add_message(feed_item)

    @rpc_method(CLIENT_STUB, (Int('msg_id'), Tuple('msg_data')))
    def battle_message(self, msg_id, msg_data):
        from logic.gcommon.common_const import battle_const
        cnf = confmgr.get('battle_msg_conf', str(msg_id), default={})
        if cnf.get('msg_type') == battle_const.TDM_OTHER_KILL_KING:
            killer_id, name, role_id, mecha_id, old_mvp = msg_data
            self._mvp_id = killer_id
            self.show_tdm_mvp(msg_data)
        else:
            msg_pos_type = cnf.get('msg_pos_type')
            if msg_pos_type == battle_const.MSG_UP_TIP:
                global_data.emgr.battle_event_message.emit(msg_data, message_type=cnf.get('msg_type'))
            elif msg_pos_type == battle_const.MAIN_DWN_TIP:
                msg_child_type = cnf.get('msg_child_type')
                content_txt = ''
                can_send = True
                if msg_child_type in [battle_const.MAIN_KILL_KING, battle_const.MAIN_END_KILL_KING]:
                    player = global_data.cam_lplayer
                    player_name = msg_data[0]
                    type_to_txt_id = {battle_const.MAIN_KILL_KING: (7017, 860044),battle_const.MAIN_END_KILL_KING: (7018, 7020)
                       }
                    if player:
                        name = player.ev_g_char_name()
                        can_send = name == player_name
                        content_txt = get_text_by_id(type_to_txt_id.get(msg_child_type)[1])
                    if msg_child_type in (battle_const.MAIN_KILL_KING,):
                        name, killer_id = msg_data
                        msg_dict = {}
                        msg_dict['name'] = name
                        msg_dict['killer_id'] = killer_id
                        msg_dict['msg_type'] = msg_child_type
                        msg_dict['is_groupmate'] = bool(player and player.ev_g_is_groupmate(killer_id, False))
                        global_data.emgr.show_battle_report_msg_ex_event.emit(msg_dict)
                        self._mvp_id = killer_id
                        self._refresh_mvp_mark(killer_id)
                    else:
                        msg_txt = get_text_by_id(type_to_txt_id.get(msg_child_type)[0]).format(name=player_name)
                        global_data.emgr.show_battle_report_msg_event.emit(msg_txt, '#SW')
                if can_send:
                    msg = {'i_type': msg_child_type}
                    if content_txt:
                        msg['content_txt'] = content_txt
                    global_data.emgr.show_battle_main_message.emit(msg, cnf.get('msg_type'))

    @rpc_method(CLIENT_STUB, (Str('msg'),))
    def ob_send_battle_message(self, msg):
        global_data.emgr.on_recv_danmu_msg.emit(msg)

    def get_mvp_id(self):
        return self._mvp_id

    def show_tdm_mvp(self, msg_data):
        killer_id, name, role_id, mecha_id, old_mvp = msg_data
        self._refresh_mvp_mark(killer_id)
        if global_data.cam_lplayer and global_data.cam_lplayer.id != killer_id:
            from logic.gcommon.common_const import battle_const
            if mecha_id:
                head_id = '3021%d' % mecha_id
            elif int(role_id) == 111:
                head_id = '30201111'
            else:
                head_id = str(30200000 + int(role_id))
            ui_msg = get_text_by_id(7041, {'name': name})
            msg = {'i_type': battle_const.TDM_OTHER_KILL_KING,'other_mvp_info': {'head': head_id,'msg': ui_msg}}
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    def _refresh_mvp_mark(self, mvp_eid):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == mvp_eid:
            ui = global_data.ui_mgr.get_ui('BattleMvpUI')
            if not ui:
                global_data.ui_mgr.show_ui('BattleMvpUI', 'logic.comsys.battle.BattleInfo')
            else:
                ui.restart_show()
        else:
            ui = global_data.ui_mgr.get_ui('BattleMvpUI')
            if ui:
                ui.delay_close()
        global_data.emgr.refresh_mvp_event.emit(mvp_eid)

    @rpc_method(CLIENT_STUB, (Uuid('like_soul'), Uuid('liked_soul'), Str('like_name'), Str('liked_name'), Int('likenum')))
    def update_settle_likenum(self, like_soul, liked_soul, like_name, liked_name, likenum):
        if not self.is_settle:
            return
        else:
            self.settle_likenum_dict[liked_soul] = likenum
            global_data.emgr.update_settle_like_info_event.emit(like_soul, liked_soul, like_name, liked_name, likenum)
            if liked_soul == global_data.player.id:
                mode_type = global_data.game_mode.get_mode_type()
                if game_mode_const.is_mode_type(mode_type, game_mode_const.TDM_SettleLike):
                    like_soul_str = str(like_soul)
                    from logic.gutils.role_head_utils import get_mecha_photo, get_role_default_photo
                    if like_soul_str in self._enemy_dict:
                        message_text = get_text_by_id(random.choice([610133, 610134, 610135, 610136]))
                        like_player_info = self._enemy_dict[like_soul_str]
                        mecha_id = like_player_info.get('mecha_id', None)
                        photo_no = get_mecha_photo(mecha_id)
                        if not mecha_id:
                            photo_no = get_role_default_photo(like_player_info.get('role_id', 11))
                        end_like_notice_ui = global_data.ui_mgr.get_ui('EndLikeNoticeUI')
                        if end_like_notice_ui is not None:
                            end_like_notice_ui.add_message(message_text, photo_no, False)
                    elif like_soul_str in self._teammate_dict:
                        message_text = get_text_by_id(random.choice([610129, 610130, 610131, 610132]))
                        like_player_info = self._teammate_dict[like_soul_str]
                        mecha_id = like_player_info.get('mecha_id', None)
                        photo_no = get_mecha_photo(mecha_id)
                        if not mecha_id:
                            photo_no = get_role_default_photo(like_player_info.get('role_id', 11))
                        end_like_notice_ui = global_data.ui_mgr.get_ui('EndLikeNoticeUI')
                        if end_like_notice_ui is not None:
                            end_like_notice_ui.add_message(message_text, photo_no, True)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(81226, {'name': like_name}))
            return

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'),))
    def newbie_call_speedup_msg(self, soul_id):
        ui = global_data.ui_mgr.show_ui('NewbieMechaTipsUI', 'logic.comsys.battle')
        if ui:
            ui.show_newbie_mecha_tips(soul_id)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Bool('enable')))
    def parachute_speedup_msg(self, soul_id, enable):
        pass

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'),))
    def on_celebrate_fireworks(self, soul_id):
        if soul_id == global_data.player.id:
            return

    def add_actor_id(self, eid):
        self._actors_set.add(eid)

    def get_actors_count(self):
        return len(self._actors_set)

    def del_actor_id(self, eid):
        if eid in self._actors_set:
            self._actors_set.remove(eid)

    def get_actors_frame_visible_count(self):
        cnt = 0
        for eid in self._actors_set:
            entity = EntityManager.getentity(eid)
            if not entity or not entity.logic:
                continue
            mdl = entity.logic.ev_g_model()
            if mdl and mdl.visible and mdl.is_visible_in_this_frame():
                cnt += 1

        return cnt

    @rpc_method(CLIENT_STUB, (List('prompt_id_list'), Str('eid'), Str('name'), Dict('short_kill_info')))
    def on_kill_prompt(self, prompt_id_list, eid, name, short_kill_info):
        for prompt_id in prompt_id_list:
            self.on_kill_promt_helper(prompt_id, eid, name)

    def on_kill_promt_helper(self, prompt_id, eid, name):
        from logic.gcommon.common_const import battle_const
        from logic.gcommon.common_utils.local_text import get_text_by_id
        kill_conf = confmgr.get('kill_prompt', 'KillPrompt', 'Content') or {}
        kill_prompt_conf = kill_conf.get(str(prompt_id), {})
        FIRST_BLOOD_TIPS_TYPE = 1
        other_msg_info = kill_prompt_conf.get('other_msg_info', {})
        if other_msg_info:
            i_type = other_msg_info.get('i_type', battle_const.TDM_KILL_TIPS)
            text_id = other_msg_info.get('text_id', 81204)
            if prompt_id == FIRST_BLOOD_TIPS_TYPE:
                content_txt = get_text_by_id(text_id, {'name': name})
            else:
                content_txt = get_text_by_id(text_id)
            if global_data.player and str(global_data.player.id) != eid:
                msg = {'i_type': i_type,'content_txt': content_txt}
            else:
                msg = {'i_type': battle_const.TDM_KILL_TIPS,'content_txt': get_text_by_id(kill_prompt_conf.get('desc_id')),
                   'bar_path': kill_prompt_conf.get('icon_path')
                   }
            if global_data.game_mode.is_pve():
                if msg.get('i_type') == battle_const.TDM_KILL_TIPS:
                    msg.update({'voice_dict': {'tag': 'Play_ui_pve_achievement'}})
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_KILL_ACHIEVEMENT)
        else:
            msg = {'i_type': battle_const.TDM_KILL_TIPS,'content_txt': get_text_by_id(kill_prompt_conf.get('desc_id')),
               'bar_path': kill_prompt_conf.get('icon_path')
               }
            if global_data.game_mode.is_pve():
                if msg.get('i_type') == battle_const.TDM_KILL_TIPS:
                    msg.update({'voice_dict': {'tag': 'Play_ui_pve_achievement'}})
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_KILL_ACHIEVEMENT)

    @rpc_method(CLIENT_STUB, (Dict('mvp_info'),))
    def update_mvp_info(self, mvp_info):
        self._mvp_info = mvp_info
        self._update_television(mvp_info)

    def _on_enter_scene(self):
        self.switch_mvp_between_coco()

    def _update_television(self, mvp_info):
        from logic.gutils.tv_panel_utils import MVP_TV_CHANNEL
        param = []
        for channel_id in MVP_TV_CHANNEL:
            param.append((channel_id, mvp_info))

        global_data.emgr.update_tv_channel.emit(param)
        self._is_switch_mvp = False
        self.switch_mvp_between_coco()

    def clear_switch_timer(self):
        self._switch_timer and global_data.game_mgr.get_logic_timer().unregister(self._switch_timer)
        self._switch_timer = None
        return

    def on_switch_mvp(self):
        from logic.gutils.tv_panel_utils import MVP_TV_CHANNEL
        param = []
        self._is_switch_mvp = not self._is_switch_mvp
        info = {'is_show_special': self._is_switch_mvp}
        for channel_id in MVP_TV_CHANNEL:
            param.append((channel_id, info))

        global_data.emgr.update_tv_channel.emit(param)

    def switch_mvp_between_coco(self):
        from logic.gutils.tv_panel_utils import is_collaborate
        if not is_collaborate():
            return
        self.clear_switch_timer()
        self._switch_timer = global_data.game_mgr.get_logic_timer().register(func=self.on_switch_mvp, mode=CLOCK, interval=5)

    def get_global_mvp_info(self):
        return self._mvp_info

    @rpc_method(CLIENT_STUB)
    def require_screenshot(self):
        global_data.player.do_upload_screenshot()

    @rpc_method(CLIENT_STUB, (Str('content'),))
    def battle_echo(self, content):
        pass

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('item_no')))
    def on_add_emoji_after_settle(self, soul_id, item_no):
        if soul_id == global_data.player.id:
            return
        global_data.emgr.change_settle_role_interaction.emit(soul_id, item_no)

    @rpc_method(CLIENT_STUB, (Str('char_name'), Str('msg')))
    def on_receive_danmu_msg(self, char_name, msg):
        if not global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return
        msg = '[{}]: {}'.format(char_name, msg)
        priority = 0
        if global_data.player.logic and char_name == global_data.player.logic.ev_g_char_name():
            msg = '<size=32>#SY{}#n</size>'.format(msg)
            priority = 1
        global_data.emgr.on_recv_danmu_msg.emit(msg, priority)

    @rpc_method(CLIENT_STUB, (Str('char_name'), Int('msg_type'), Dict('msg_data')))
    def on_receive_format_danmu_msg(self, char_name, msg_type, msg_data):
        print('---------------------on_receive_format_danmu_msg-------------------', char_name, msg_type, msg_data)
        self.on_receive_format_danmu_msg_imp(char_name, msg_type, msg_data)

    def on_receive_format_danmu_msg_imp(self, char_name, msg_type, msg_data):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            from logic.gcommon.common_const import chat_const

            def custom_item_func(panel, danmu):
                panel.lab_1.SetString(danmu.text)
                return panel.lab_1.getTextContentSize()

            if msg_type == chat_const.DANMU_TYPE_SEND_RED:
                templ = 'activity/activity_202307/summer_live/i_summer_live_scrolling'
                priority = 1
                from logic.gutils.red_packet_utils import get_red_packet_info
                coin_type = msg_data.get('coin_type')
                red_packet_conf = get_red_packet_info(coin_type)
                cur_id = red_packet_conf.get('cur_id')
                from logic.gutils.mall_utils import get_lobby_item_name
                name = get_lobby_item_name(cur_id)
                char_str = '<color=0XFFD809FF>%s</color>' % char_name
                msg = get_text_by_id(634888).format(name=char_str, num=msg_data.get('coin_num', 0), coin_type=name)
                global_data.emgr.on_recv_danmu_msg.emit(msg, 0, template=templ, custom_item_func=custom_item_func, tag='red_packet')
            elif msg_type == chat_const.DANMU_TYPE_REVC_RED:
                self_name = msg_data.get('receiver', '')
                sender_name = msg_data.get('sender', '')
                templ = 'activity/activity_202307/summer_live/i_summer_live_scrolling'
                from logic.gutils.red_packet_utils import get_red_packet_info
                coin_type = msg_data.get('coin_type')
                red_packet_conf = get_red_packet_info(coin_type)
                cur_id = red_packet_conf.get('cur_id')
                from logic.gutils.mall_utils import get_lobby_item_name
                name = get_lobby_item_name(cur_id)
                sender_str = '<color=0XFFD809FF>%s</color>' % sender_name
                msg = get_text_by_id(634889).format(pick_name=self_name, name=sender_str, red_packet=name)
                global_data.emgr.on_recv_danmu_msg.emit(msg, 0, template=templ, custom_item_func=custom_item_func, tag='red_packet')
            else:
                teml = None
                log_error('on_receive_format_danmu_msg_imp: unknown msg_type', msg_type)
            return

    def on_settle_info_for_ob(self, settle_info_by_rank):
        from logic.gutils.judge_utils import is_ob
        if is_ob():
            self.ob_settle_info = settle_info_by_rank
            global_data.emgr.judge_ob_settle_event.emit()

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Dict('data')))
    def update_brief_group_data(self, soul_id, data):
        if self._brief_group_data is None:
            return
        else:
            old_data = self._brief_group_data.setdefault(soul_id, {})
            old_data.update(data)
            return

    def get_brief_group_data(self):
        return self._brief_group_data

    def get_scene_name(self):
        return self._scene_name

    def get_max_teammate_num(self):
        return self._max_teammate_num

    def is_customed_battle(self):
        return self._is_customed_battle

    def get_customed_battle_dict(self):
        return self._customed_battle_dict

    def is_customed_no_multi_mecha_limit(self):
        return self._customed_no_multi_mecha_limit

    def is_customed_enable_friend_hurt(self):
        return self._customed_enable_friend_hurt

    def recruit_valid(self):
        if self._is_competition or self._max_teammate_num < 2:
            return False
        if self.alive_player_num <= battle_const.RESCUE_RECRUIT_ALIVE_NUM or self.is_in_ace_state:
            return False
        return True

    def is_ace_time(self):
        return self.is_in_ace_state

    def get_is_competition(self):
        return self._is_competition

    def get_is_round_competition(self):
        if not self._comp_round or not self._comp_id:
            return False
        else:
            conf = get_round_competition_conf(self._comp_id, self._comp_round)
            return conf and conf.get('battle_info', {}).get('round', None)

    def get_round_competition_data(self):
        return (
         self._comp_id, self._comp_round)

    def get_is_force_trigger_door(self):
        return self.force_trigger_door

    def teleport_by_transfer_portal(self, eid):
        self.call_soul_method('teleport_by_transfer_portal', (eid,))

    @rpc_method(CLIENT_STUB, (Float('next_transfer_ts'), List('target_pos')))
    def update_next_transfer_ts(self, next_transfer_ts, target_pos):
        self.next_transfer_ts = next_transfer_ts
        global_data.emgr.teleport_update_cd_on_simple_portal.emit(next_transfer_ts)
        from logic.gutils.granhack_utils import create_simple_tele_sfx
        create_simple_tele_sfx(target_pos)
        global_data.sound_mgr.play_event('Play_ui_pve_transitions', None)
        return

    def get_next_transfer_ts(self):
        return self.next_transfer_ts

    def get_banpick_para(self):
        return (
         self._bp_play_mode, self._bp_play_area)

    def need_skip_end_exp_ui(self):
        return False

    @rpc_method(CLIENT_STUB, (Dict('member_order_dict'), Uuid('member_id')))
    def refresh_group_orders(self, member_order_dict, member_id):
        pass

    def get_max_loading_time(self):
        return self._max_loading_time

    def get_group_loading_dict(self):
        return self.group_loading_dict

    def get_soul_loading_data(self):
        return self.soul_loading_data

    def get_group_encourage_dict(self):
        return self.group_encourage_dict

    def try_encourage_teammates(self):
        self.call_soul_method('try_encourage_teammates', ())

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('group_id'), Int('tip_text_id'), Bool('all_encourage')))
    def on_try_encourage_teammates(self, soul_id, group_id, tip_text_id, all_encourage):
        encourage_list = self.group_encourage_dict.setdefault(group_id, [])
        if soul_id not in encourage_list:
            encourage_list.append(soul_id)
        global_data.emgr.on_try_encourage_teammates_event.emit(soul_id, group_id, tip_text_id, all_encourage)

    def try_show_guangmu(self, guangmu_id):
        self.call_soul_method('show_canopy', (guangmu_id,))

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('canopy_item_no'), Float('next_show_canopy_item')))
    def syn_show_canopy(self, soul_id, canopy_item_no, next_show_canopy_item):
        global_data.emgr.on_play_guangmu.emit(soul_id, canopy_item_no, next_show_canopy_item)

    @rpc_method(CLIENT_STUB, ())
    def on_all_member_ready(self):
        self._all_member_ready = True
        global_data.emgr.all_member_ready_event.emit()

    def is_all_member_ready(self):
        return self._all_member_ready

    def report_soul_load_prog(self, prog):
        self.call_soul_method('report_soul_load_prog', (prog,))

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('prog')))
    def update_player_load_prog(self, soul_id, prog):
        global_data.emgr.player_loading_prog_change_event.emit(soul_id, prog)

    def get_default_show_role(self):
        return self._default_show_role == 1

    def get_loading_group_id(self):
        return self._loading_group_id

    def need_pvp_loading(self):
        return self._max_loading_time > 0

    @rpc_method(CLIENT_STUB, (Int('text_id'),))
    def show_tip(self, text_id):
        global_data.game_mgr.show_tip(get_text_by_id(text_id))

    def is_support_surrender(self):
        return self._is_support_surrender

    def initiate_surrender(self):
        if self.is_enable_surrender_vote():
            self.call_soul_method('initiate_surrender')
        else:
            global_data.game_mgr.show_tip(get_text_by_id(634274))

    def vote_surrender(self, flag):
        self.call_soul_method('vote_surrender', (flag,))

    def is_enable_surrender(self):
        return 'enable_timestamp' in self._surrender_data

    def is_enable_surrender_vote(self):
        if not self.is_enable_surrender():
            return False
        else:
            now = tutil.get_server_time()
            enable_timestamp = self._surrender_data['enable_timestamp']
            if enable_timestamp - now > 0:
                return False
            vote_timestamp = self._surrender_data.get('vote_timestamp', None)
            if vote_timestamp is not None:
                vote_left_time = battle_const.SURRENDER_VOTE_DURATION - (now - vote_timestamp)
                return vote_left_time > 0
            return True
            return

    def is_initiate_surrender(self):
        return self._surrender_data.get('vote_timestamp', None) is not None

    def get_surrender_data(self):
        return self._surrender_data

    @rpc_method(CLIENT_STUB, (Float('timestamp'), Bool('show_tips')))
    def enable_surrender(self, timestamp, show_tips):
        self._surrender_data['enable_timestamp'] = timestamp
        show_tips and global_data.game_mgr.show_tip(get_text_by_id(634279))
        global_data.emgr.enable_battle_surrender.emit()

    @rpc_method(CLIENT_STUB, (Dict('surrender_data'),))
    def sync_surrender(self, surrender_data):
        self._surrender_data = surrender_data
        if not self._surrender_data.get('vote_timestamp', None):
            return False
        else:
            now = tutil.get_server_time()
            timestamp = self._surrender_data['vote_timestamp']
            left_time = battle_const.SURRENDER_VOTE_DURATION - (now - timestamp)
            if left_time <= 0:
                return False
            give_up_ui = global_data.ui_mgr.show_ui('BattleGiveUpUI', 'logic.comsys.battle')
            give_up_ui and give_up_ui.refresh_ui(self._surrender_data.get('vote', {}), left_time)
            return

    def finish_akf_status(self):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'finish_akf_status', ())
        battle_utils.set_block_control(False, 'ON_HOOK')

    @rpc_method(CLIENT_STUB, (Dict('sync_data'),))
    def sync_custom_faction_members(self, sync_data):
        pass

    @rpc_method(CLIENT_STUB, ())
    def faction_room_show_enemy_pos(self):
        self.need_show_enemy_pos = True

    def enable_faction_rescue(self):
        return self.is_custom_faction_room