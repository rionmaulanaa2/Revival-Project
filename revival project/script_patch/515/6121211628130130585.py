# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/parachute_ui/ParachuteInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import math3d
import world
import collision
import cc
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_COLL
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
HEIGHT_BOTTOM_PERCENT = 100
HEIGHT_TOP_PERCENT = 0
MAX_HEIGHT = 1200
MIN_HEIGHT = -400
from common.const import uiconst

class ParachuteInfoUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'parachute/parachute_main'

    def on_init_panel(self, *args, **kwargs):
        self.attitude_container.setTouchEnabled(False)
        self.attitude_container.jumpToPercentVertical(HEIGHT_TOP_PERCENT)
        self.pro_hight.SetPercent(100)
        self.check_ground_timer = None
        self.ground_pos_change_timer = None
        self.ground_pos = None
        self.last_ground_pos = None
        self.cache_pos = self.panel.node_ground.GetPosition()
        return

    def clear_data(self):
        self.clear_check_ground_timer()
        self.clear_ground_pos_change_timer()
        self.ground_pos = None
        self.last_ground_pos = None
        return

    def enter_screen(self):
        super(ParachuteInfoUI, self).enter_screen()
        global_data.emgr.parachute_height_changed += self.on_parachute_height_update
        global_data.emgr.parachute_speed_changed += self.on_parachute_speed_update
        self.tick_check_ground()
        self.hit_ground()
        self.set_ground_mark_pos()

    def leave_screen(self):
        super(ParachuteInfoUI, self).leave_screen()
        global_data.emgr.parachute_height_changed -= self.on_parachute_height_update
        global_data.emgr.parachute_speed_changed -= self.on_parachute_speed_update
        self.clear_data()

    def on_parachute_speed_update(self, ver_velocity):
        v_km_h = abs(ver_velocity) * 3.6
        self.txt_speed.SetString('%dkm/h' % v_km_h)

    def on_parachute_height_update(self, pos_y):
        if not global_data.cam_lplayer:
            return
        position = global_data.cam_lplayer.ev_g_position()
        if not position:
            return
        pos_y = position.y / NEOX_UNIT_SCALE
        if math.isinf(pos_y) or math.isnan(pos_y):
            pos_y = 0
        self.check_ground()
        percent = (1 - (pos_y - MIN_HEIGHT) * 1.0 / (MAX_HEIGHT - MIN_HEIGHT)) * 100
        self.txt_height.SetString('%dm' % max(pos_y, 0))
        pos = self.panel.node_pointer.GetPosition()
        self.panel.node_pointer.SetPosition(pos[0], '%.2f%%' % (100 - percent))
        self.attitude_container.jumpToPercentVertical(percent)
        self.pro_hight.SetPercent(100 - percent)

    def tick_check_ground(self):
        self.clear_check_ground_timer()
        self.check_ground_timer = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.hit_ground),
         cc.DelayTime.create(1)])))

    def clear_check_ground_timer(self):
        self.check_ground_timer and self.panel.stopAction(self.check_ground_timer)
        self.check_ground_timer = None
        self.ground_pos = None
        return

    def clear_ground_pos_change_timer(self):
        self.ground_pos_change_timer and self.panel.node_ground.stopAction(self.ground_pos_change_timer)
        self.ground_pos_change_timer = None
        return

    def cal_ground_mark_pos(self):
        n_y = self.cache_pos[1]
        if self.last_ground_pos:
            pos_y = self.last_ground_pos.y / NEOX_UNIT_SCALE
            size = self.attitude_container.GetInnerContentSize()
            h = size.height / (MAX_HEIGHT - MIN_HEIGHT) * (pos_y - MIN_HEIGHT)
            offset = self.attitude_container.GetContentOffset()
            n_y = max(h - -offset.y, self.cache_pos[1])
        return n_y

    def set_ground_mark_pos(self):
        n_y = self.cal_ground_mark_pos()
        l_x, _ = self.panel.node_ground.GetPosition()
        self.panel.node_ground.SetPosition(l_x, n_y)

    def check_ground(self):
        if not self.ground_pos:
            self.panel.node_ground.setVisible(False)
            return
        self.panel.node_ground.setVisible(True)
        if self.last_ground_pos and int(self.last_ground_pos.y) == int(self.ground_pos.y):
            if not self.ground_pos_change_timer:
                self.set_ground_mark_pos()
            return
        interval_time = 0.03
        show_time = 0.5
        l_x, l_y = self.panel.node_ground.GetPosition()

        def reset():
            self.set_ground_mark_pos()
            self.clear_ground_pos_change_timer()

        def cb(dt):
            n_y = self.cal_ground_mark_pos()
            off_y = n_y - l_y
            self.panel.node_ground.SetPosition(l_x, off_y * (dt / show_time) + l_y)

        self.clear_ground_pos_change_timer()
        self.ground_pos_change_timer = self.panel.node_ground.TimerAction(cb, show_time, reset, interval=interval_time)
        self.last_ground_pos = math3d.vector(self.ground_pos.x, self.ground_pos.y, self.ground_pos.z)

    def hit_ground(self):
        if not global_data.cam_lplayer:
            return
        position = global_data.cam_lplayer.ev_g_position()
        if not position:
            return
        scene = world.get_active_scene()
        if not scene:
            return
        end_pt = math3d.vector(position.x, position.y - 300 * NEOX_UNIT_SCALE, position.z)
        result = scene.scene_col.hit_by_ray(position, end_pt, 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, collision.INCLUDE_FILTER)
        if result and result[0]:
            self.ground_pos = math3d.vector(result[1].x, result[1].y, result[1].z)
        self.check_ground()