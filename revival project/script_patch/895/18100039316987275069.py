# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mode/ComGulag.py
from __future__ import absolute_import
import math3d
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.battle_const import REVIVE_NONE, REVIVE_WAIT, ST_IDLE, ST_IN_QUEUE, ST_IN_GAME, ST_GULAG_PARACHUTE, ST_REVIVE_PENDING
from logic.gcommon import time_utility
from logic.units.LAvatar import LAvatar
from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_REDUCE
from logic.gcommon.item.item_const import ITEM_GULOG_REVIVE_COIN
from logic.gutils import item_utils as iutil

class ComGulag(UnitCom):
    BIND_EVENT = {'E_ON_CAM_LCTARGET_SET': '_on_cam_lctarget_set',
       'E_GULAG_REVIVE_PENDING': 'on_gulag_revive_pending',
       'E_GULAG_GAME_IN_QUEUE': 'on_gulag_game_in_queue',
       'E_ENTER_GULAG_GAME': 'on_gulag_enter_game',
       'E_OTHER_ENTER_GULAG_GAME': 'on_other_enter_gulag_game',
       'E_GULAG_GAME_SETTLE': 'on_gulag_game_settle',
       'E_GULAG_GROUPMATE_REVIVE': 'on_gulag_groupmate_revive',
       'E_ENTER_GULAG_GAME_FINISH': 'on_enter_gulag_game_finish',
       'E_ACTION_SYNC_RB_POS': 'on_rb_pos',
       'E_SET_RECHOOSE_MECHA': ('on_rechoose_mecha', 99),
       'G_CAN_GULAG_REVIVE': 'can_gulag_revive',
       'G_GULAG_GAME_ID': 'get_cur_revive_game_id',
       'G_GULAG_ARENA_NO': 'get_revive_game_arena_no',
       'G_GULAG_STATUS': 'get_gulag_status',
       'E_ITEM_DATA_CHANGED': 'on_revive_coin_count_update',
       'G_IS_REVIVE_CANCEL': 'is_gulag_revive_cancel',
       'E_TRANSFER_REVIVE_COIN': 'on_transfer_revive_coin'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComGulag, self).init_from_dict(unit_obj, bdict)
        self.is_avatar = False
        self.gulag_info = bdict.get('gulag_revive_soul', {})
        self.gulag_cancel = bdict.get('is_gulag_canceled', 0)
        self.game_detail = bdict.get('gulag_revive_game_detail', {})
        self.gulag_enemy_eid = None
        for eid in self.game_detail.get('player_eids', []):
            if eid != self.unit_obj.id:
                self.gulag_enemy_eid = eid
                break

        self.scene_detail = bdict.get('gulag_revive_scene_detail', {})
        self.revive_game_enemy_id = None
        self.enter_screen_sfx_id = None
        self.enter_model_sfx_id = None
        global_data.emgr.scene_cam_observe_player_setted += self._on_scene_cam_observe_player_setted
        global_data.emgr.refresh_gulag_poison_circle += self.on_gulag_poison_circle_update
        global_data.emgr.reduce_gulag_poison_circle += self.on_gulag_poison_circle_update
        return

    def on_init_complete(self):
        self.is_avatar = isinstance(self.unit_obj, LAvatar)
        if self.is_avatar:
            self._on_scene_cam_observe_player_setted()

    def _on_scene_cam_observe_player_setted(self):
        if not self.is_valid():
            return
        else:
            if self.is_cam_target():
                status = self.get_gulag_status()
                if status == ST_IN_QUEUE:
                    global_data.emgr.gulag_revive_game_in_queue.emit(self.gulag_info)
                elif status == ST_IN_GAME and 'game_id' in self.game_detail:
                    global_data.emgr.self_enter_gulag_revive_game.emit(self.game_detail['game_id'], self.game_detail, self.scene_detail)
                    global_data.gulag_sur_battle_mgr and global_data.gulag_sur_battle_mgr.on_enter_revive_game(self.game_detail)
                if self.scene_detail and 'gulag_poison_circle' in self.scene_detail:
                    for game_id, circle_info in six.iteritems(self.scene_detail['gulag_poison_circle'] or {}):
                        if not circle_info:
                            continue
                        global_data.emgr.refresh_gulag_poison_circle.emit(game_id, circle_info)

                self.refresh_mecha_ui_vis(status not in (ST_IN_QUEUE, ST_GULAG_PARACHUTE))
                global_data.gulag_sur_battle_mgr and global_data.gulag_sur_battle_mgr.set_cam_gulag_enemy(self.gulag_enemy_eid)
                self.refresh_see_through()
            else:
                global_data.sfx_mgr.remove_sfx_by_id(self.enter_screen_sfx_id)
                self.enter_screen_sfx_id = None
                self.send_event('E_RESET_CAMP_OUTLINE')
            self.emit_state_changed_event()
            return

    def emit_state_changed_event(self):
        from logic.gcommon.common_const.battle_const import UP_NODE_PLAYER_NUMBER, UP_NODE_AREA_INFO, MAIN_NODE_RANK_AWARD
        if self.is_cam_target():
            gulag_state = self.get_gulag_status()
            global_data.game_mgr.post_exec(lambda : global_data.emgr.cam_lplayer_gulag_state_changed.emit(gulag_state=gulag_state, game_id=self.get_cur_revive_game_id(), can_revive=self.can_gulag_revive(), is_canceled=self.is_gulag_revive_cancel()))
            global_data.emgr.block_battle_message_by_type.emit(gulag_state != ST_IDLE, (UP_NODE_PLAYER_NUMBER, UP_NODE_AREA_INFO, MAIN_NODE_RANK_AWARD), 'gulag')
        else:
            global_data.game_mgr.post_exec(self.change_locate_ui_visible)

    def change_locate_ui_visible(self):
        if not self.unit_obj:
            return
        teammate_ui = global_data.ui_mgr.get_ui('TeammateUI')
        if not teammate_ui:
            return
        teammate_ui.on_teammate_enter_gulag(self.unit_obj.id, self.get_gulag_status() != ST_IDLE)

    def can_gulag_revive(self):
        return self.gulag_info.get('join_cnt', 0) <= 0

    def is_gulag_revive_cancel(self):
        return self.gulag_cancel

    def get_cur_revive_game_id(self):
        status = self.get_gulag_status()
        if status == ST_IDLE:
            return REVIVE_NONE
        if status == ST_IN_QUEUE:
            return REVIVE_WAIT
        return self.gulag_info.get('ongoing_game')

    def get_revive_game_arena_no(self):
        return self.game_detail.get('battlefield_no')

    def get_gulag_status(self):
        return self.gulag_info.get('status', ST_IDLE)

    def get_gulag_enemy_eid(self):
        return self.gulag_enemy_eid

    def is_cam_target(self):
        if not self.unit_obj or not self.is_valid():
            return
        return self.is_avatar or bool(global_data.cam_lplayer and global_data.cam_lplayer.id == self.unit_obj.id)

    def on_gulag_revive_pending(self, delay_revive_timestamp):
        if self.is_cam_target():
            global_data.emgr.enter_gulag_revive_pending.emit(delay_revive_timestamp)

    def on_gulag_game_in_queue(self, in_queue_detail):
        self.gulag_info.update(in_queue_detail)
        if self.is_cam_target():
            global_data.emgr.gulag_revive_game_in_queue.emit(in_queue_detail)
            self.refresh_mecha_ui_vis(False)
        self.emit_state_changed_event()

    def on_gulag_enter_game(self, game_id, game_detail, scene_detail):
        self.game_detail.update(game_detail)
        self.scene_detail.update(scene_detail)
        self.gulag_info['status'] = ST_IN_GAME
        self.gulag_info['ongoing_game'] = game_id
        if self.is_cam_target():
            global_data.emgr.self_enter_gulag_revive_game.emit(game_id, game_detail, scene_detail)
            global_data.gulag_sur_battle_mgr and global_data.gulag_sur_battle_mgr.on_enter_revive_game(game_detail)
        self.emit_state_changed_event()
        if self.is_avatar and global_data.gulag_sur_battle_mgr:
            arena_info = global_data.gulag_sur_battle_mgr.get_arena_info_with_arena_idx(game_detail['battlefield_no'])
            min_x, min_z, max_x, max_z, _ = arena_info['area_info']
            center = ((min_x + max_x) / 2, (min_z + max_z) / 2)
            tp_left_time = game_detail['enter_area_timestamp'] - time_utility.time() + 1

            def after_tp():
                self.look_at_arena_center(center)
                self.refresh_mecha_ui_vis(True)

            if tp_left_time < 0:
                after_tp()
            else:
                game3d.delay_exec(tp_left_time * 1000, after_tp)

    def refresh_mecha_ui_vis(self, visible):
        if not self.is_cam_target():
            return
        self.cur_mecha_ui_vis = visible
        mecha_ui = global_data.ui_mgr.get_ui('MechaUI')
        if mecha_ui:
            if visible:
                mecha_ui.add_show_count('gulag')
            else:
                mecha_ui.add_hide_count('gulag')
        state_change_ui = global_data.ui_mgr.get_ui('StateChangeUI')
        if state_change_ui:
            if visible:
                state_change_ui.add_show_count('gulag')
            else:
                state_change_ui.add_hide_count('gulag')

    def look_at_arena_center(self, center):
        lpos = self.ev_g_position()
        if not lpos:
            return
        target_pos = math3d.vector(center[0], lpos.y, center[1])
        if lpos and target_pos:
            diff_vec = target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                cur_yaw = self.ev_g_yaw() or 0
                global_data.emgr.camera_set_yaw_event.emit(target_yaw)
                global_data.emgr.camera_set_pitch_event.emit(0)
                self.send_event('E_CAM_PITCH', 0)
                self.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def on_rb_pos(self, rb_pos, i_reason):
        if not self.is_cam_target():
            return
        ui = global_data.ui_mgr.get_ui('GulagInfoUI')
        if not ui:
            return
        ui.on_teleport(rb_pos, i_reason)
        global_data.emgr.camera_set_pitch_event.emit(0)
        self.send_event('E_CAM_PITCH', 0)
        if self.get_gulag_status() == ST_GULAG_PARACHUTE:
            self.gulag_info['status'] = ST_IDLE
            self.emit_state_changed_event()
            if self.is_cam_target():
                self.refresh_mecha_ui_vis(True)

    def on_gulag_poison_circle_update(self, game_id, circle_info):
        if self.get_cur_revive_game_id() != game_id:
            return
        if 'gulag_poison_circle' not in self.scene_detail:
            self.scene_detail['gulag_poison_circle'] = {}
        if game_id not in self.scene_detail['gulag_poison_circle'] or not self.scene_detail['gulag_poison_circle'][game_id]:
            self.scene_detail['gulag_poison_circle'][game_id] = circle_info
        else:
            self.scene_detail['gulag_poison_circle'][game_id].update(circle_info)
        self.refresh_see_through()

    def on_enter_gulag_game_finish(self):
        if self.is_cam_target():
            self.enter_screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene('effect/fx/scenes/common/sidou/gulage_1.sfx')
        model = self.ev_g_model()
        if model and model.valid:
            self.enter_model_sfx_id = global_data.sfx_mgr.create_sfx_on_model('effect/fx/scenes/common/sidou/gulage_1_1.sfx', model, 'fx_root')
        self.send_event('E_RESET_CAMP_OUTLINE')

    def on_other_enter_gulag_game(self, other_eid, game_id):
        self.gulag_enemy_eid = other_eid
        if self.is_cam_target():
            global_data.emgr.other_enter_gulag_revive_game.emit(other_eid, game_id)
            global_data.gulag_sur_battle_mgr and global_data.gulag_sur_battle_mgr.set_cam_gulag_enemy(self.gulag_enemy_eid)
            self.refresh_see_through()

    def on_gulag_game_settle(self, notify_detail):
        self.gulag_info.update(notify_detail)
        left_time = notify_detail['parachute_timestamp'] - time_utility.time()
        if self.is_cam_target():
            global_data.emgr.gulag_revive_game_settle.emit(notify_detail)
        self.emit_state_changed_event()
        self.send_event('E_RESET_CAMP_OUTLINE')
        self.refresh_see_through()

    def on_gulag_groupmate_revive(self, eid, name):
        if self.is_cam_target():
            global_data.emgr.gulag_groupmate_revive.emit(eid, name)

    def on_rechoose_mecha--- This code section failed: ---

 296       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'refresh_mecha_ui_vis'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    31  'to 31'

 297      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'refresh_mecha_ui_vis'
          18  LOAD_FAST             0  'self'
          21  LOAD_ATTR             2  'cur_mecha_ui_vis'
          24  CALL_FUNCTION_1       1 
          27  POP_TOP          
          28  JUMP_FORWARD          0  'to 31'
        31_0  COME_FROM                '28'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_revive_coin_count_update(self, item_info):
        if not item_info or item_info.get('item_id', 0) != ITEM_GULOG_REVIVE_COIN:
            return
        small_map = global_data.ui_mgr.get_ui('SmallMapUI')
        if small_map:
            small_map.on_update_can_revive(self.can_gulag_revive(), self.is_gulag_revive_cancel())

    def refresh_see_through(self, *args):
        if not self.is_cam_target():
            return
        global_data.gulag_sur_battle_mgr and global_data.gulag_sur_battle_mgr.enable_gulag_enemy_see_through(self.get_cur_poison_state() >= POISON_CIRCLE_STATE_REDUCE)

    def get_cur_poison_state(self):
        if not self.scene_detail or 'gulag_poison_circle' not in self.scene_detail:
            return 0
        self_game_id = self.get_cur_revive_game_id()
        if self_game_id not in self.scene_detail['gulag_poison_circle']:
            return 0
        return (self.scene_detail['gulag_poison_circle'][self_game_id] or {}).get('state', 0)

    def destroy(self):
        global_data.emgr.scene_cam_observe_player_setted -= self._on_scene_cam_observe_player_setted
        global_data.emgr.refresh_gulag_poison_circle -= self.on_gulag_poison_circle_update
        global_data.emgr.reduce_gulag_poison_circle -= self.on_gulag_poison_circle_update
        super(ComGulag, self).destroy()
        global_data.sfx_mgr.remove_sfx_by_id(self.enter_screen_sfx_id)
        global_data.sfx_mgr.remove_sfx_by_id(self.enter_model_sfx_id)
        self.enter_screen_sfx_id = None
        self.enter_model_sfx_id = None
        return

    def on_transfer_revive_coin(self):
        global_data.game_mgr.show_tip(get_text_by_id(17992))