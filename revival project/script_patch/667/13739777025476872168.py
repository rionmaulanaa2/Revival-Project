# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupyBattleUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
import collision
import math3d
from common.const import uiconst
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.comsys.battle.Death.DeathTopScoreUI import DeathTopScoreUI
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import MutiOccupyPoint
from logic.comsys.battle.MutiOccupy.MutiOccupyMarkUI import PARTID_TO_TEXT
from logic.gcommon.common_const.battle_const import MAIN_NODE_COMMON_INFO, MUTIOCCUPY_ENEMY_OCCUPY_C, MUTIOCCUPY_ENEMY_OCCUPY_A, MUTIOCCUPY_ENEMY_OCCUPY_B, MUTIOCCUPY_SELF_OCCUPY_A, MUTIOCCUPY_SELF_OCCUPY_B, MUTIOCCUPY_SELF_OCCUPY_C, MUTIOCCUPY_SELF_OCCUPY_A, MUTIOCCUPY_SELF_OCCUPY_B, MUTIOCCUPY_SELF_OCCUPY_C, STATE_OCCUPY_SELF, STATE_OCCUPY_ENEMY, OCCUPY_POINT_STATE_SNATCH, STATE_OCCUPY_SNATCH
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
CENTER_TIPS_SELF = {1: MUTIOCCUPY_SELF_OCCUPY_A,
   2: MUTIOCCUPY_SELF_OCCUPY_B,
   3: MUTIOCCUPY_SELF_OCCUPY_C
   }
CENTER_TIPS_ENEMY = {1: MUTIOCCUPY_ENEMY_OCCUPY_A,
   2: MUTIOCCUPY_ENEMY_OCCUPY_B,
   3: MUTIOCCUPY_ENEMY_OCCUPY_C
   }
ND_VS_POSITION = {1: ('50%-74', '50%-26'),
   2: ('50%', '50%-26'),
   3: ('50%74', '50%-26')
   }
MUTIOCCUPY_CENTER_TIPS = {STATE_OCCUPY_SELF: CENTER_TIPS_SELF,
   STATE_OCCUPY_ENEMY: CENTER_TIPS_ENEMY
   }

class MutiOccupyBattleUI(DeathTopScoreUI):
    PANEL_CONFIG_NAME = 'battle_control/fight_top_control'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self):
        super(MutiOccupyBattleUI, self).on_init_panel()
        self.update_occupy_point_state()

    def init_panel(self):
        self.panel.RecordAnimationNodeState('alarm')
        self.panel.prog_blue.SetPercentage(0)
        self.panel.prog_red.SetPercentage(0)
        battle_duration = global_data.game_mode.get_cfg_data('play_data').get('battle_duration', 0)
        left_time = tutil.get_delta_time_str(battle_duration)[3:]
        self.panel.lab_time.SetString(left_time)
        self.panel.lab_time_vx.SetString(left_time)
        if global_data.death_battle_data:
            self.update_group_score(global_data.death_battle_data.get_group_score_data())
            self.update_player_num(global_data.death_battle_data.get_score_details_data())
            self.update_timestamp()
        if global_data.player and global_data.player.logic:
            if not global_data.player.logic.ev_g_is_in_spectate():
                global_data.player.logic.send_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI')

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('MutiOccupyScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('MutiOccupyScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('MutiOccupyScoreDetailsUI', 'logic.comsys.battle.MutiOccupy')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'update_group_score_data': self.update_group_score,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'update_occupy_point_state': self.update_occupy_point_state,
           'update_score_details': self.update_player_num,
           'update_occupy_left_tips': self.on_update_occupy_top_tips
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        super(MutiOccupyBattleUI, self).init_parameters()
        self.part_occupy_dict = {}
        self.part_collsion_dict = {}

    def update_group_score(self, data):
        bat = global_data.player.get_battle()
        if not bat:
            return
        total_point = bat.get_settle_point()
        if not total_point:
            return
        score_str = '{}/{}'
        for g_id in six.iterkeys(data):
            if g_id == self.group_id:
                self.panel.nd_score.lab_score_blue.SetString(score_str.format(str(data[g_id]), str(total_point)))
                percent = 100.0 * data[g_id] / total_point
                self.panel.prog_blue.SetPercentage(percent)
            else:
                self.panel.nd_score.lab_score_red.SetString(score_str.format(str(data[g_id]), str(total_point)))
                percent = 100.0 * data[g_id] / total_point
                self.panel.prog_red.SetPercentage(percent)

    def update_player_num(self, data):
        self.panel.temp_team_blue.lab_value.SetString(str(len(data.get('my_group', []))))
        self.panel.temp_team_red.lab_value.SetString(str(len(data.get('other_group', []))))

    def init_base_data(self, base_data):
        self.position = base_data.get('c_center', [0, 0, 0])
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if play_data:
            self.inc_progress = play_data.get('inc_progress')
            self.dec_progress = play_data.get('dec_progress')

    def init_server_data(self, server_data):
        self.progress = server_data.get('progress', 0)
        self.group_id = server_data.get('group_id', 0)
        self.state = server_data.get('state', 0)
        self.is_occupy = server_data.get('is_occupy', False)

    def update_occupy_point_state(self):
        if not global_data.death_battle_data:
            return
        else:
            occupy_data = global_data.death_battle_data.occupy_data
            is_init = False
            is_in_occupy_point = False
            for part_id, occupy in six.iteritems(occupy_data):
                server_data = occupy.get_occupy_server_data()
                base_data = occupy.get_occupy_base_data()
                locate_ui = self.part_occupy_dict.get(part_id, None)
                if not locate_ui:
                    locate_ui = MutiOccupyPoint(getattr(self.panel, 'temp_prog_{}'.format(part_id)), part_id)
                    locate_ui.init_server_data(server_data)
                    self.part_occupy_dict[part_id] = locate_ui
                    self.part_collsion_dict[part_id] = self.init_point_collsion(base_data)
                    is_init = True
                locate_ui.update_occupy_state(server_data, is_init=is_init)
                player_cnt = server_data.get('player_cnt', [])
                if player_cnt:
                    blue_num = 0
                    red_num = 0
                    if self.check_player_in_occupy_point(self.part_collsion_dict.get(part_id)):
                        is_in_occupy_point = True
                        self.panel.nd_vs.setVisible(True)
                        self.panel.nd_vs.SetPosition(*ND_VS_POSITION.get(part_id))
                        for data in player_cnt:
                            if global_data.cam_lplayer:
                                if global_data.cam_lplayer.ev_g_group_id() == data[0]:
                                    blue_num = data[1]
                                    self.panel.temp_team_blue.lab_value.SetString(str(data[1]))
                                else:
                                    red_num = data[1]
                                    self.panel.temp_team_red.lab_value.SetString(str(data[1]))

                        if blue_num == 0:
                            self.panel.temp_team_blue.lab_value.SetString(str(0))
                        if red_num == 0:
                            self.panel.temp_team_red.lab_value.SetString(str(0))
                state = server_data.get('state', 0)
                if state == OCCUPY_POINT_STATE_SNATCH:
                    locate_ui.play_vx_animation()
                else:
                    locate_ui.stop_vx_animation()

            if not is_in_occupy_point:
                self.panel.nd_vs.setVisible(False)
            return

    def on_update_occupy_top_tips(self, group, points):
        points_text = PARTID_TO_TEXT.get(int(points))
        if group == STATE_OCCUPY_SELF:
            text = get_text_by_id(8001).format(camp=get_text_by_id(291), point=points_text)
        else:
            text = get_text_by_id(8001).format(camp=get_text_by_id(292), point=points_text)
        msg_type = MUTIOCCUPY_CENTER_TIPS.get(group, {}).get(int(points))
        message = {'i_type': msg_type,'content_txt': text}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    def init_point_collsion(self, base_data):
        size = base_data.get('c_size', [1, 1, 1])
        pos = base_data.get('c_center', [0, 0, 0])
        yaw = base_data.get('yaw', 0)
        col_obj = collision.col_object(collision.BOX, math3d.vector(*size) * 0.5, 65535, 65535)
        col_obj.position = pos
        col_obj.rotation_matrix = math3d.matrix.make_rotation_y(yaw * 3.1415926 / 180.0)
        return col_obj

    def check_player_in_occupy_point(self, col_obj):
        player = global_data.cam_lplayer
        if not player or not col_obj:
            return False
        ret = global_data.game_mgr.scene.scene_col.static_test(col_obj, 65535, GROUP_SHOOTUNIT, collision.INCLUDE_FILTER) or []
        if ret:
            for col in ret:
                cid = col.cid
                if global_data.emgr.scene_is_shoot_obj.emit(cid):
                    res = global_data.emgr.scene_find_unit_event.emit(cid)
                    if res and res[0] and player == res[0]:
                        return True

        return False