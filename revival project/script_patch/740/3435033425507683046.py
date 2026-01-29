# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMonsterMarkWidget.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.screen_utils import world_to_screen_ellipse_pos
from common.utils.cocos_utils import getScreenSize
from math import atan, pi
from common.platform.device_info import DeviceInfo
from common.utils.ui_utils import get_scale
from logic.gcommon.common_const.pve_const import M_NORMAL, M_TOUGH, M_ELITE, M_BOSS

class PVEMonsterMarkWidget(object):
    MAX_COUNT = 3
    DEFAULT_OFFSET = 4.0
    TEMPLATE = {M_NORMAL: 'battle_tips/pve/i_normal_monster_mark',
       M_TOUGH: 'battle_tips/pve/i_normal_monster_mark',
       M_ELITE: 'battle_tips/pve/i_elite_monster_mark'
       }

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_locate_params()
        self.process_events(True)

    def init_params(self):
        self.unit_dict = {}
        self.type_dict = {}
        self.widget_dict = {}
        self.timer_dict = {}

    def process_events(self, is_bind):
        econf = {'pve_monster_init': self.on_init_monster,
           'pve_monster_die': self.on_destroy_monster
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        for i in self.timer_dict:
            self.reset_timer(i, pop=False)

        self.timer_dict = {}
        for i in self.widget_dict:
            self.destroy_widget(i, pop=False)

        self.widget_dict = {}
        self.type_dict = {}
        self.unit_dict = {}

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def on_init_monster(self, unit):
        m_type = unit.sd.ref_monster_type
        if m_type == M_BOSS:
            return
        eid = unit.id
        self.unit_dict[eid] = unit
        self.type_dict[eid] = m_type
        self.adjust_mark()

    def on_destroy_monster(self, unit):
        if unit.sd.ref_monster_type == M_BOSS:
            return
        eid = unit.id
        self.reset_timer(eid)
        self.destroy_widget(eid)
        if eid in self.type_dict:
            del self.type_dict[eid]
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
        m_type = self.type_dict.get(eid, M_NORMAL)
        self.widget_dict[eid] = self.init_widget(m_type)
        model = unit.ev_g_model()
        offset = unit.ev_g_mark_offset()
        if not offset:
            offset = self.DEFAULT_OFFSET
        self.reset_timer(eid)
        self.timer_dict[eid] = global_data.game_mgr.register_logic_timer(lambda e=eid, m=model, o=offset: self.tick_pos(e, m, o), 1)

    def init_widget(self, m_type):
        widget = global_data.uisystem.load_template_create(self.TEMPLATE[m_type], self.panel)
        widget.setVisible(False)
        return widget

    def destroy_widget(self, eid, pop=True):
        widget = self.widget_dict.get(eid, None)
        if not widget:
            return
        else:
            widget.setVisible(False)
            widget.Destroy()
            if pop:
                self.widget_dict.pop(eid)
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
            if not global_data.player or not global_data.player.logic:
                return
            if not model or not model.valid:
                self.reset_timer(eid)
                self.destroy_widget(eid)
                if eid in self.type_dict:
                    del self.type_dict[eid]
                if eid in self.unit_dict:
                    del self.unit_dict[eid]
                return
            widget = self.widget_dict[eid]
            nd_lab = widget.nd_lab
            nd_arrows = widget.nd_arrows
            position = model.position
            position.y += offset * NEOX_UNIT_SCALE
            is_in_screen, pos, angle = world_to_screen_ellipse_pos(nd_lab, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
            if is_in_screen:
                widget.setVisible(False) if widget.isVisible() else None
            else:
                widget.isVisible() or widget.setVisible(True) if 1 else None
                nd_lab.setPosition(pos)
                nd_lab.lab_text.setVisible(False)
                nd_lab.lab_distance.setVisible(False)
                nd_arrows.setVisible(True)
                nd_arrows.setRotation(angle)
            return