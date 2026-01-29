# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMonsterIconWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.pve_const import M_NORMAL, M_TOUGH, M_ELITE, M_BOSS
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
from common.utils.cocos_utils import neox_pos_to_cocos
import cc

class PVEMonsterIconWidget(object):
    CACHE_SIZE = 10

    def __init__(self, panel, parent):
        self.parent = parent
        self.panel = panel
        self.init_params()
        self.process_events(True)

    def init_params(self):
        self.widget_dict = {}
        self.cache_pool = []

    def process_events(self, is_bind):
        econf = {'pve_monster_init': self.on_init_monster,
           'pve_monster_hit': self.on_hit_monster,
           'pve_monster_destroy': self.on_destroy_monster
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        for eid in self.widget_dict:
            widget = self.widget_dict[eid]
            widget.ui_nd.retain()
            widget.ui_nd.setVisible(False)
            widget.ui_nd.removeFromParent()
            if len(self.cache_pool) > self.CACHE_SIZE:
                widget.destroy()
            else:
                self.cache_pool.append(widget)

        self.widget_dict = {}

    def clear_all(self):
        for widget in six.itervalues(self.widget_dict):
            widget.destroy()

        for widget in self.cache_pool:
            widget.destroy()

    def destroy(self):
        self.clear_all()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def on_init_monster(self, unit):
        init_eid = unit.id
        if init_eid in self.widget_dict:
            widget = self.widget_dict[init_eid]
        else:
            if self.cache_pool:
                widget = self.cache_pool.pop()
                widget.ui_nd.release()
            else:
                widget = self.init_widget()
            self.widget_dict[init_eid] = widget
            self.panel.AddChild(None, widget.ui_nd)
        widget.set_target(init_eid)
        return widget

    def on_hit_monster(self, hit_eid):
        if hit_eid not in self.widget_dict:
            if self.cache_pool:
                widget = self.cache_pool.pop()
                widget.ui_nd.release()
            else:
                widget = self.init_widget()
            self.widget_dict[hit_eid] = widget
            self.panel.AddChild(None, widget.ui_nd)
        widget = self.widget_dict[hit_eid]
        widget.hit_target(hit_eid)
        return

    def on_destroy_monster(self, unit):
        d_eid = unit.id
        if d_eid not in self.widget_dict:
            return
        widget = self.widget_dict[d_eid]
        widget.tick_end_cb()

    def init_widget(self):
        return IconNodeWidget(self.panel, self)

    def collect_widget(self, eid):
        if eid not in self.widget_dict:
            return
        widget = self.widget_dict[eid]
        widget.ui_nd.retain()
        widget.ui_nd.setVisible(False)
        widget.ui_nd.removeFromParent()
        if len(self.cache_pool) > self.CACHE_SIZE:
            widget.destroy()
        else:
            self.cache_pool.append(widget)
        del self.widget_dict[eid]


class IconNodeWidget(object):
    TEMPLATE = 'pve/i_pve_monster_icon'
    DUR = 600
    RE_DUR = 5.0
    MAX_DIS = 200 * NEOX_UNIT_SCALE
    MIN_DIS = 10 * NEOX_UNIT_SCALE
    MAX_SCL = 1.0
    MIN_SCL = 0.2

    def __init__(self, panel, parent):
        self.panel = panel
        self.parent = parent
        self.ui_nd = None
        self.init_ui_nd()
        self.init_params()
        return

    def init_params(self):
        self.eid = None
        self.target = None
        self.m_type = 0
        return

    def init_ui_nd(self):
        self.ui_nd = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)

    def recollect(self):
        self.ui_nd.StopTimerAction()
        self.parent.collect_widget(self.eid)
        self.init_params()

    def destroy(self):
        self.ui_nd.StopTimerAction()
        self.ui_nd.Destroy()
        self.ui_nd = None
        self.init_params()
        return

    def set_target(self, eid, hit=False):
        if not self.ui_nd or not self.ui_nd.isValid():
            return
        if self.eid == eid:
            if self.m_type == M_BOSS:
                self.ui_nd.setVisible(False)
                return
        else:
            self.eid = eid
            self.target = self.get_target(eid)
            if self.target and self.target.logic:
                m_type = self.target.logic.sd.ref_monster_type
                if m_type == M_BOSS:
                    self.m_type = M_BOSS
                    self.ui_nd.setVisible(False)
                    return
                if m_type != self.m_type:
                    self.m_type = m_type
        if self.eid in self.parent.parent.target_monsters:
            self.ui_nd.icon_target.setVisible(True)
            self.ui_nd.icon_arrow.setVisible(False)
        else:
            self.ui_nd.icon_target.setVisible(False)
            self.ui_nd.icon_arrow.setVisible(True)
        hit or self.init_tick() if 1 else self.re_init_tick()

    def hit_target(self, eid):
        self.set_target(eid, True)

    def get_target(self, eid):
        if self.target:
            return self.target
        else:
            target = EntityManager.getentity(eid)
            if target:
                return target
            return None

    def init_tick(self, dur=DUR):
        self.ui_nd.StopTimerAction()
        self.ui_nd.TimerAction(self.tick_pos, dur, self.tick_end_cb, 0.016)

    def re_init_tick(self, dur=RE_DUR):
        self.ui_nd.setVisible(False)
        self.ui_nd.StopTimerAction()
        self.ui_nd.TimerAction(self.re_tick, dur, self.init_tick, 0.1)

    def tick_pos(self, *args):
        cam = global_data.game_mgr.scene.active_camera
        if self.target and cam:
            if not self.target.logic:
                return
            model = self.target.logic.ev_g_model()
            if model and model.valid:
                pos = self.target.logic.ev_g_model_position()
                dis = cam.position - pos
                scale = max((self.MAX_DIS - dis.length) * 1.0 / self.MAX_DIS, self.MIN_SCL)
                self.ui_nd.setScale(scale)
                socket_pos = model.get_socket_matrix('xuetiao', world.SPACE_TYPE_WORLD).translation
                x, y = cam.world_to_screen(socket_pos)
                x, y = neox_pos_to_cocos(x, y)
                l_pos = self.ui_nd.getParent().convertToNodeSpace(cc.Vec2(x, y))
                self.ui_nd.setPosition(l_pos)
                self.ui_nd.setVisible(True)
                return

    def tick_end_cb(self):
        self.recollect()

    def re_tick(self, *args):
        pass