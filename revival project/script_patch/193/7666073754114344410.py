# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeSpItemGuideUI.py
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

class ScavengeSpItemGuideChildUI(object):

    def __init__(self, parent, item_eid):
        self.parent = parent
        self.item_eid = item_eid
        self._nd = global_data.uisystem.load_template_create('battle_pick_up/battle_pick_weapon_position_tips')
        self._nd.setVisible(True)
        self.init_parameters()
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self._nd])
        self.on_tick()

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
        return

    def init_pos_data(self, pos_list):
        self.position = pos_list

    def on_finalize_panel(self):
        self.clear_run_timer()
        self._nd and self._nd.Destroy()
        self._nd = None
        return

    def update_nd_pos(self):
        if not self.position:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        x, y, z = self.position
        position = math3d.vector(x, y + 20, z)
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
                self._nd.nd_dir.setRotation(angle + 90)

    def on_tick(self):
        self.clear_run_timer()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd_pos, interval=1)

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return


class ScavengeSpItemGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.panel.setLocalZOrder(1)
        if global_data.battle.init_guide_locate:
            global_data.death_battle_data and global_data.death_battle_data.update_sp_item_data(global_data.battle.init_guide_locate)

    def on_finalize_panel(self):
        for locate_ui in six.itervalues(self.sp_item_locate):
            locate_ui.on_finalize_panel()

        self.sp_item_locate = {}
        self.process_event(False)

    def init_parameters(self):
        self.sp_item_locate = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_scavenge_sp_item_guide_ui': self.update_scavenge_sp_item_guide_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_scavenge_sp_item_guide_ui(self):
        if not global_data.death_battle_data:
            return
        else:
            sp_item_data = global_data.death_battle_data.sp_item_data
            for item_eid, pos_list in six.iteritems(sp_item_data):
                locate_ui = self.sp_item_locate.get(item_eid, None)
                if not locate_ui:
                    locate_ui = ScavengeSpItemGuideChildUI(self, item_eid)
                    locate_ui.init_pos_data(pos_list)
                    self.panel.AddChild('', locate_ui._nd)
                    self.sp_item_locate[item_eid] = locate_ui

            for item_eid, locate_ui in six.iteritems(self.sp_item_locate):
                if not sp_item_data.get(item_eid, None):
                    locate_ui.on_finalize_panel()

            return