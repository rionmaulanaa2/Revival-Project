# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEShopMarkWidget.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.screen_utils import world_pos_to_screen_pos
from common.utils.cocos_utils import getScreenSize
from math import atan, pi
from common.platform.device_info import DeviceInfo
from common.utils.ui_utils import get_scale
from logic.gcommon.common_const.pve_const import PVE_SHOP_STATE_CLOSED, PVE_SHOP_STATE_OPENED
from logic.gcommon.common_utils.local_text import get_text_by_id

class PVEShopMarkWidget(object):
    MAX_COUNT = 5
    DEFAULT_OFFSET = 9.0
    TEMPLATE = 'battle_tips/pve/i_shop_mark'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_locate_params()
        self.process_events(True)

    def init_params(self):
        self.unit_dict = {}
        self.widget_dict = {}
        self.timer_dict = {}

    def process_events(self, is_bind):
        econf = {'pve_shop_closed_event': self.on_cancel_shop,
           'pve_shop_opened_event': self.on_track_shop,
           'pve_get_shop_tracked_event': self.on_get_track_event
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        for i in self.timer_dict:
            self.reset_timer(i, pop=False)

        self.timer_dict = {}
        for i in self.widget_dict:
            self.destroy_widget(i, pop=False)

        self.widget_dict = {}
        self.unit_dict = {}

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def on_get_track_event(self):
        if self.timer_dict:
            return True
        return False

    def on_track_shop(self, unit, show_tip=False):
        eid = unit.id
        self.unit_dict[eid] = unit
        self.adjust_mark()
        show_tip and global_data.emgr.pve_show_box_shop_tips.emit()

    def on_cancel_shop(self, unit):
        eid = unit.id
        self.reset_timer(eid)
        self.destroy_widget(eid)
        if eid in self.unit_dict:
            del self.unit_dict[eid]
        self.adjust_mark()

    def adjust_mark(self):
        if len(self.widget_dict) < self.MAX_COUNT:
            for i in self.unit_dict:
                if i not in self.widget_dict:
                    self.init_mark(self.unit_dict[i])
                    break

    def init_mark(self, unit):
        eid = unit.id
        self.widget_dict[eid] = self.init_widget()
        self.check_widget_state(unit)
        model = unit.ev_g_model()
        offset = unit.ev_g_mark_offset()
        if not offset:
            offset = self.DEFAULT_OFFSET
        self.reset_timer(eid)
        self.timer_dict[eid] = global_data.game_mgr.register_logic_timer(lambda e=eid, m=model, o=offset: self.tick_pos(e, m, o), 1)

    def init_widget(self):
        widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        widget.setVisible(False)
        return widget

    def destroy_widget(self, eid, pop=True):
        widget = self.widget_dict.get(eid, None)
        if not widget:
            return
        else:
            widget.setVisible(False)
            widget.StopAnimation('keep')
            widget.Destroy()
            if pop:
                self.widget_dict.pop(eid)
            return

    def check_widget_state(self, unit):
        eid = unit.id
        widget = self.widget_dict.get(eid, None)
        if not widget:
            return
        else:
            state = unit.ev_g_shop_state()
            if state == PVE_SHOP_STATE_CLOSED:
                widget.nd_close.setVisible(True)
                widget.nd_open.setVisible(False)
            elif state == PVE_SHOP_STATE_OPENED:
                widget.nd_close.setVisible(False)
                widget.nd_open.setVisible(True)
            return

    def reset_timer(self, eid, pop=True):
        timer = self.timer_dict.get(eid, None)
        if not timer:
            return
        else:
            global_data.game_mgr.unregister_logic_timer(timer)
            if pop:
                self.timer_dict.pop(eid)
            return

    def init_locate_params(self):
        self.screen_size = getScreenSize()
        self.screen_angle_limit = atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / pi
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('40w'), get_scale('120w')),
           'scale_low': (
                       get_scale('160w'), get_scale('220w'))
           }

    def tick_pos(self, eid, model, offset):
        camera = global_data.game_mgr.scene.active_camera
        if not camera:
            return
        else:
            if not global_data.cam_lplayer:
                return
            if not model or not model.valid:
                self.reset_timer(eid)
                self.destroy_widget(eid)
                if eid in self.unit_dict:
                    del self.unit_dict[eid]
                return
            widget = self.widget_dict[eid]
            nd_mark = widget.nd_mark
            nd_arrows = widget.nd_arrows
            position = model.position
            position.y += offset * NEOX_UNIT_SCALE
            is_in_screen, pos, angle = world_pos_to_screen_pos(nd_mark, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
            if is_in_screen:
                if not widget.isVisible():
                    widget.setVisible(True) if 1 else None
                    m_pos = global_data.cam_lplayer.ev_g_position()
                    return m_pos or None
                dist = m_pos - position
                dist = max(0, int(dist.length / NEOX_UNIT_SCALE) - 10)
                nd_mark.setPosition(pos)
                nd_mark.lab_distance.setVisible(True)
                nd_mark.lab_distance.SetString(get_text_by_id(157).format(str(dist)))
                nd_arrows.setVisible(False)
            else:
                widget.isVisible() or widget.setVisible(True) if 1 else None
                nd_mark.setPosition(pos)
                nd_mark.lab_distance.setVisible(False)
                nd_arrows.setVisible(True)
                nd_arrows.setRotation(angle)
            return