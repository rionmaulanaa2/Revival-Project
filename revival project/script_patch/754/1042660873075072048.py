# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CKingMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
import math3d

class CKingMode:

    def __init__(self, map_id):
        self.map_id = map_id
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.king_battle_data and global_data.king_battle_data.finalize()
        self.grid_mgr and self.grid_mgr.on_finalize()
        self.grid_mgr = None
        return

    def init_parameters(self):
        self.grid_mgr = None
        return

    def init_mgr(self):
        self.king_data_mgr()
        self.koth_grid_mgr()

    def king_data_mgr(self):
        from logic.comsys.battle.King.KingBattleData import KingBattleData
        KingBattleData()

    def koth_grid_mgr(self):
        from logic.vscene.parts.gamemode.CGridManager import CGridManager
        self.grid_mgr = CGridManager()
        cfg = global_data.game_mode.get_cfg_data('play_data')
        occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        occupy_ids = cfg.get('king_point_list', [])
        for occupy_id in occupy_ids:
            occupy_data = occupy_cfg.get(str(occupy_id), {})
            position = occupy_data.get('center')
            if not position:
                continue
            position = math3d.vector(*position)
            self.grid_mgr.add_to_grid(occupy_id, position)

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('KingBattleBeginUI')
        global_data.ui_mgr.close_ui('KingBattleReviveUI')
        global_data.ui_mgr.close_ui('KingBattleUI')
        global_data.ui_mgr.close_ui('KothCampShopEntryUI')
        global_data.ui_mgr.close_ui('KothCampShopUI')
        global_data.ui_mgr.close_ui('KingOccupyUI')
        global_data.ui_mgr.close_ui('KingBeaconTowerOccupyUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'target_revive_event': self.on_target_revive,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'on_player_check_rotate_init_event': self.on_player_check_rotate_init,
           'loading_end_event': self.on_loading_end
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY):
            self.create_king_battle_begin_ui()
        elif stage == parachute_utils.STAGE_LAND:
            self.create_king_battle_ui()
        global_data.emgr.enter_koth_battle_scene.emit(stage)

    def on_target_defeated(self, revive_time, killer_id, kill_info):
        global_data.ui_mgr.show_ui('KingBattleReviveUI', 'logic.comsys.battle.King')
        ui = global_data.ui_mgr.get_ui('KingBattleReviveUI')
        if ui:
            ui.on_delay_close(revive_time)
            ui.on_show_defeat_info(killer_id, kill_info)

    def create_king_battle_begin_ui(self):
        global_data.ui_mgr.show_ui('KothCampShopEntryUI', 'logic.comsys.battle.King')
        ui = global_data.ui_mgr.show_ui('KingBattleBeginUI', 'logic.comsys.battle.King')
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if bat:
            timestamp = bat.prepare_timestamp
            revive_time = timestamp - time_utility.get_server_time()
            ui.on_delay_close(revive_time)

    def create_king_battle_ui(self):
        global_data.ui_mgr.show_ui('KothCampShopEntryUI', 'logic.comsys.battle.King')
        global_data.ui_mgr.show_ui('KingOccupyUI', 'logic.comsys.battle.King')
        global_data.ui_mgr.show_ui('BeaconTowerOccupyUI', 'logic.comsys.battle.King')
        ui = global_data.ui_mgr.show_ui('KingBattleUI', 'logic.comsys.battle.King')
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if bat:
            timestamp = bat.prepare_timestamp
            play_duration = global_data.game_mode.get_cfg_data('play_data').get('play_duration', 0)
            play_overtime = global_data.game_mode.get_cfg_data('play_data').get('play_overtime', 0)
            ui.on_count_down(timestamp + play_duration, overtime=timestamp + play_duration + play_overtime)
            ui.on_turns_count_down(timestamp + play_duration, overtime=timestamp + play_duration + play_overtime)

    def on_target_revive(self):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_TO_THIRD_PERSON_CAMERA')
            self.on_player_check_rotate_init()

    def rotate_to_look_at(self, lent, target_pos):
        if not lent:
            return
        lpos = lent.ev_g_position()
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = lent.ev_g_yaw() or 0
                global_data.emgr.fireEvent('camera_set_yaw_event', target_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)
                lent.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def on_player_check_rotate_init(self):
        if global_data.player and global_data.player.logic:
            cfg = global_data.game_mode.get_cfg_data('play_data')
            base_center_pos = cfg.get('map_center')
            import math3d
            position = math3d.vector(*base_center_pos)
            self.rotate_to_look_at(global_data.player.logic, position)

    def on_loading_end(self):
        for ui_name in ['ScalePlateUI']:
            ui = global_data.ui_mgr.get_ui(ui_name)
            ui and ui.add_hide_count('KingMode')