# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Occupy/OccupyBattleTips.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import getScreenSize
from common.platform.device_info import DeviceInfo
from logic.gutils import screen_utils
from common.const import uiconst
import cc
import math3d
import math
import time

class OccupyBattleTips(BasePanel):
    PANEL_CONFIG_NAME = 'battle_contention/battle_tips'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    MOVE_SPEED = 50

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.process_event(False)
        self.clear_go_timer()

    def init_parameters(self):
        self.go_timer = None
        self.end_world_pos = None
        self.delay_time = 0
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_size = getScreenSize()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        return

    def init_panel(self):
        pass

    def start_move(self, pos, delay_time):
        wpos = math3d.vector(*pos)
        self.end_world_pos = wpos
        self.panel.PlayAnimation('show')
        anim_time = self.panel.GetAnimationMaxRunTime('show')
        self.delay_time = delay_time - anim_time

        def finished(*args):
            self.lets_go()

        self.panel.SetTimeOut(anim_time, finished)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def lets_go(self):
        self.clear_go_timer()
        self.last_time = time.time()

        def _on_check():
            cam = global_data.game_mgr.scene.active_camera
            if not cam:
                return
            cur_time = time.time()
            interval_time = cur_time - self.last_time
            self.last_time = cur_time
            if interval_time <= 0:
                return
            nd = self.panel.nd_lock
            is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(nd, self.end_world_pos, self.screen_size, self.screen_angle_limit, self.is_can_full_screen)
            cur_pos = self.panel.nd_lock.getPosition()
            end_pos.subtract(cur_pos)
            dir_len = end_pos.length()
            speed = dir_len / (self.delay_time / interval_time)
            self.delay_time -= interval_time
            if self.delay_time <= 0:
                cur_pos.add(end_pos)
                nd.setPosition(cur_pos)
                self.close()
                return
            end_pos.normalize()
            end_pos.scale(speed)
            cur_pos.add(end_pos)
            nd.setPosition(cur_pos)

        self.go_timer = global_data.game_mgr.get_logic_timer().register(func=_on_check, interval=1)

    def clear_go_timer(self):
        self.go_timer and global_data.game_mgr.get_logic_timer().unregister(self.go_timer)
        self.go_timer = None
        return