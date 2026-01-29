# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupyMarkUI.py
from __future__ import absolute_import
import six
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import screen_utils
import math3d
import cc
import math
from common.uisys.basepanel import BasePanel
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import MutiOccupyPoint
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_const.battle_const import STATE_OCCUPY_EMPTY, STATE_OCCUPY_SELF, STATE_OCCUPY_ENEMY, STATE_OCCUPY_SNATCH, OCCUPY_POINT_STATE_IDLE, OCCUPY_POINT_STATE_DEC, OCCUPY_POINT_STATE_INC
from common.platform.device_info import DeviceInfo
from logic.gcommon import time_utility as tutil
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import getScreenSize
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import TICK_TIME, PROG_ADD, PROG_SCALE
PARTID_TO_TEXT = {1: 'A',
   2: 'B',
   3: 'C'
   }

class MutiOccupyLocateUI(MutiOccupyPoint):

    def __init__(self, parent, part_id):
        self.parent = parent
        self.part_id = part_id
        self._nd = global_data.uisystem.load_template_create('battle_control/i_control_ccb_blue')
        self._nd.setVisible(True)
        self.init_parameters()
        self.init_panel()
        self.on_tick()

    def init_panel(self):
        self._nd.lab_name.SetString(PARTID_TO_TEXT[self.part_id])

    def init_parameters(self):
        self.run_timer = None
        self.screen_size = getScreenSize()
        self.position = None
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('90w'), get_scale('120w')),
           'scale_low': (
                       get_scale('90w'), get_scale('120w'))
           }
        self.progress_timer = None
        self.inc_progress = 10
        self.dec_progress = 10
        return

    def init_base_data(self, base_data):
        self.position = base_data.get('c_center', [0, 0, 0])
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if play_data:
            self.inc_progress = play_data.get('inc_progress')
            self.dec_progress = play_data.get('dec_progress')

    def on_finalize_panel(self):
        self.clear_run_timer()
        self.destory()

    def update_nd_pos(self):
        if not self.position:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        x, y, z = self.position
        position = math3d.vector(x, y, z)
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self._nd, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        dist = cam.position - position
        dist = dist.length / NEOX_UNIT_SCALE
        max_dist = 1000
        scale = max(2, (max_dist - dist) * 1.0 / max_dist)
        self._nd.setScale(scale)
        self._nd.setPosition(end_pos)
        lplayer = global_data.cam_lplayer
        if lplayer:
            self._nd.nd_dir.setVisible(not is_in_screen)
            if not is_in_screen:
                self._nd.nd_dir.setRotation(angle - 90)

    def on_tick(self):
        self.clear_run_timer()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd_pos, interval=1)

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return


class MutiOccupyMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.panel.setLocalZOrder(1)
        self.update_occupy_point_state()

    def on_finalize_panel(self):
        for locate_wrapper in six.itervalues(self.part_occupy_locate):
            locate_wrapper.on_finalize_panel()

        self.part_occupy_locate = {}
        self.process_event(False)

    def init_parameters(self):
        self.part_occupy_locate = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_occupy_point_state': self.update_occupy_point_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_occupy_point_state(self):
        if not global_data.death_battle_data:
            return
        else:
            occupy_data = global_data.death_battle_data.occupy_data
            is_init = False
            for part_id, occupy in six.iteritems(occupy_data):
                server_data = occupy.get_occupy_server_data()
                base_data = occupy.get_occupy_base_data()
                locate_ui = self.part_occupy_locate.get(part_id, None)
                if not locate_ui:
                    locate_ui = MutiOccupyLocateUI(self, part_id)
                    locate_ui.init_server_data(server_data)
                    locate_ui.init_base_data(base_data)
                    self.panel.AddChild('', locate_ui._nd)
                    self.part_occupy_locate[part_id] = locate_ui
                    is_init = True
                locate_ui.update_occupy_state(server_data, is_init=is_init)

            return