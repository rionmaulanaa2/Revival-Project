# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Sys3DGuide.py
from __future__ import absolute_import
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
import world
import math3d
import time
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
GUIDE_1 = 1
GUIDE_2 = 2
GUIDE_3 = 3
GUIDE_4 = 4
GUIDE_TIPS = {GUIDE_1: 5038,
   GUIDE_2: 5039,
   GUIDE_3: 5040,
   GUIDE_4: 5041
   }

class Sys3DGuide(ScenePartSysBase):

    def __init__(self):
        super(Sys3DGuide, self).__init__()
        self.init_events()
        self.update_timer_id = None
        self.parachute_end_time = None
        self.cur_guide = None
        return

    def init_events(self):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def on_login_reconnect(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        return

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            stage = global_data.player.logic.share_data.ref_parachute_stage
            if stage == parachute_utils.STAGE_PLANE:
                if not self.update_timer_id:
                    self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)
            else:
                if self.update_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
                    self.update_timer_id = None
                if stage == parachute_utils.STAGE_MECHA_READY:
                    global_data.emgr.show_parachute_guide_tips.emit(get_text_by_id(5037))
            return

    def update(self):
        if not self.check_parachute_end_time():
            return
        guide = self.check_cur_guide()
        if guide != self.cur_guide:
            self.cur_guide = guide
            global_data.emgr.show_parachute_guide_tips.emit(get_text_by_id(GUIDE_TIPS[guide]))
            global_data.emgr.show_parachture_range_guide_event.emit()

    def check_cur_guide(self):
        now = time.time()
        if self.parachute_end_time - now > 22:
            return GUIDE_1
        else:
            player = global_data.player
            if player and player.logic and player.logic.ev_g_parachute_follow_target():
                return GUIDE_4
            can_launch = global_data.emgr.get_launch_status_event.emit()
            if can_launch and can_launch[0]:
                return GUIDE_3
            return GUIDE_2

    def check_parachute_end_time(self):
        if self.parachute_end_time:
            return True
        battle = global_data.battle
        if not battle:
            return False
        if not battle.flight_dict:
            return False
        self.parachute_end_time = battle.flight_dict['start_timestamp'] + battle.flight_dict['flight_time']

    def destroy(self):
        pass