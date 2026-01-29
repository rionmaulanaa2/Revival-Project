# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CScoreMode.py
from __future__ import absolute_import
import six
from six.moves import range
from mobile.common.EntityManager import EntityManager
from logic.gcommon.time_utility import time
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK
from logic.gcommon.common_const import battle_const

class CScoreMode:
    MAX_ENEMY = 3
    FRESH_TIME = 5

    def __init__(self, map_id):
        self.map_id = map_id
        self.update_timer_id = 0
        self.enemy_pos_lst = []
        self.init_mgr()
        self.process_event(True)
        self.create_score_ui()

    def on_finalize(self):
        self.clear_logic_timer()
        self.process_event(False)
        self.destroy_ui()
        global_data.score_battle_rank_data.finalize()

    def clear_logic_timer(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = 0

    def init_mgr(self):
        self.init_rank_data_mgr()

    def init_rank_data_mgr(self):
        from logic.comsys.battle.Rank.RankData import RankData
        RankData()

    def create_score_ui(self):
        from logic.comsys.battle.Rank.RankBeginUI import RankBeginUI
        RankBeginUI()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('RankBeginUI')
        global_data.ui_mgr.close_ui('BriefRankUI')
        global_data.ui_mgr.close_ui('RankListUI')
        global_data.ui_mgr.close_ui('KnockoutUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'target_defeated_event': self.on_target_defeated,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'scene_reduce_poison_circle_event': self.reduce_poison_circle,
           'scene_enemy_mark': self.scene_enemy_mark,
           'show_big_map_ui_event': self.on_show_map_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_target_defeated(self, revive_time, killer_id, kill_info):
        global_data.ui_mgr.close_ui('RankListUI')
        global_data.ui_mgr.show_ui('RankListUI', 'logic.comsys.battle.Rank')
        global_data.ui_mgr.get_ui('RankListUI').on_delay_close(revive_time)

    def on_player_parachute_stage_changed(self, stage):
        from logic.gutils.template_utils import set_ui_list_visible_helper
        lavatar = global_data.player.logic
        is_in_battle = lavatar.ev_g_is_parachute_battle_land()
        from logic.gutils.template_utils import set_ui_list_visible_helper
        battle_ui_list = ['RankBeginUI']
        set_ui_list_visible_helper(battle_ui_list, is_in_battle, 'SCOREMODE')

    def on_show_map_ui(self):
        global_data.emgr.scene_enemy_mark.emit(self.enemy_pos_lst)

    def scene_enemy_mark(self, pos_lst):
        self.enemy_pos_lst = pos_lst

    def reduce_poison_circle(self, state, refresh_time, last_time, reduce_type):
        self.clear_logic_timer()
        global_data.emgr.battle_event_message.emit(None, message_type=battle_const.UP_NODE_ENEMYSCAN)

        def _update():
            cur_time = time()
            cur_local_time = refresh_time + last_time - cur_time
            if int(cur_local_time) <= 0:
                global_data.emgr.scene_enemy_mark.emit([])
                self.clear_logic_timer()
                return
            if global_data.score_battle_rank_data.im_in_waring_rank():
                global_data.emgr.scene_scan_enemy.emit()
                pos_lst = self.get_enemy_position()
                global_data.emgr.scene_enemy_mark.emit(pos_lst)
            else:
                global_data.emgr.scene_enemy_mark.emit([])

        self.update_timer_id = global_data.game_mgr.register_logic_timer(_update, 5, mode=CLOCK)
        return

    def get_enemy_position(self):
        pos_lst = []
        dis_lst = []
        is_cal = True
        all_puppet = EntityManager.get_entities_by_type('Puppet')
        if len(all_puppet) < self.MAX_ENEMY:
            bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
            bat and bat.request_enemy_data()
            return pos_lst
        else:
            if len(all_puppet) == self.MAX_ENEMY:
                is_cal = False
            if not (global_data.player and global_data.player.logic and global_data.player.logic.is_valid()):
                return pos_lst
            own_pos = global_data.player.logic.ev_g_position()
            for targetid, target in six.iteritems(all_puppet):
                if not (target and target.logic and target.logic.is_valid()):
                    continue
                pos = target.logic.ev_g_position()
                if is_cal:
                    dis = (own_pos - pos).length / NEOX_UNIT_SCALE
                    if len(dis_lst) < self.MAX_ENEMY:
                        dis_lst.append(dis)
                        pos_lst.append(pos)
                    else:
                        max_dis = -1
                        max_dis_index = None
                        for i in range(self.MAX_ENEMY):
                            if dis_lst[i] > max_dis:
                                max_dis = dis_lst[i]
                                max_dis_index = i

                        if dis < max_dis:
                            dis_lst[max_dis_index] = dis
                            pos_lst[max_dis_index] = pos
                else:
                    pos_lst.append(pos)

            return pos_lst