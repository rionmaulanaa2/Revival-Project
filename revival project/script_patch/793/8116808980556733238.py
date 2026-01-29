# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalLocateWidget.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.cocos_utils import getScreenSize
from common.platform.device_info import DeviceInfo
from common.utils.ui_utils import get_scale
from logic.gutils import screen_utils
import math3d
import cc
import math

class ADCrystalLocateWidget(object):

    def __init__(self, node_template, position):
        self.node = global_data.uisystem.load_template_create(node_template)
        self.init_width = None
        self.init_height = None
        self.position = position
        self.update_timer = None
        self.screen_size = None
        self.is_can_full_screen = None
        self.screen_angle_limit = None
        self.scale_data = None
        self._init_parameters()
        self._start_update()
        return

    def destroy(self):
        self._stop_update()
        if self.node:
            self.node.Destroy()
            self.node = None
        self.screen_size = None
        self.scale_data = None
        return

    def _init_parameters(self):
        self.screen_size = getScreenSize()
        self.is_can_full_screen = DeviceInfo().is_can_full_screen()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (
                      get_scale('90w'), get_scale('280w')),
           'scale_40': (
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
        self.init_width, self.init_height = self.node.prog_time.GetContentSize()
        self.node.list_buff.SetInitCount(3)
        for buff_ui_item in self.node.list_buff.GetAllItem():
            buff_ui_item.setVisible(False)

    def _update(self):
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        position = math3d.vector(*self.position)
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self.node, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        self.node.setPosition(end_pos)
        if not is_in_screen:
            self.node.nd_rotate.setVisible(True)
            self.node.nd_rotate.setRotation(-(angle - 90))
        else:
            self.node.nd_rotate.setVisible(False)

    def _start_update(self):
        self.update_timer = global_data.game_mgr.get_logic_timer().register(func=self._update, interval=1)

    def _stop_update(self):
        if self.update_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.update_timer)
            self.update_timer = None
        return

    def set_icon(self, icon_path):
        self.node.icon.SetDisplayFrameByPath('', icon_path)

    def on_update_crystal_hp(self, left_hp_ratio):
        self.node.prog_time.SetContentSize(self.init_width, self.init_height * left_hp_ratio)
        hp_percent = int(min(math.ceil(100.0 * left_hp_ratio), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        self.node.lab_time.SetString(hp_percent_str)
        self.node.img_timebg.setVisible(True)

    def on_update_crystal_buff(self, player_cnt):
        for idx, buff_ui_item in enumerate(self.node.list_buff.GetAllItem()):
            if idx + 1 <= player_cnt:
                buff_ui_item.setVisible(True)
            else:
                buff_ui_item.setVisible(False)