# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMonsterBloodWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.pve_const import M_NORMAL, M_TOUGH, M_ELITE, M_BOSS, M_TARGET
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
from common.utils.cocos_utils import neox_pos_to_cocos
import cc

class PVEMonsterBloodWidget(object):
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
        econf = {'pve_monster_hit': self.on_hit_monster
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        for eid in self.widget_dict:
            widget = self.widget_dict[eid]
            widget.ui_nd.retain()
            widget.ui_nd.nd_hp.setVisible(False)
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

    def on_init_monster(self, init_eid):
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
        return widget

    def on_hit_monster(self, hit_eid):
        if hit_eid not in self.widget_dict:
            self.on_init_monster(hit_eid)
        widget = self.widget_dict[hit_eid]
        widget.set_target(hit_eid)

    def init_widget(self):
        return HPNodeWidget(self.panel, self)

    def collect_widget(self, eid):
        if eid not in self.widget_dict:
            return
        widget = self.widget_dict[eid]
        widget.ui_nd.retain()
        widget.ui_nd.nd_hp.setVisible(False)
        widget.ui_nd.removeFromParent()
        if len(self.cache_pool) > self.CACHE_SIZE:
            widget.destroy()
        else:
            self.cache_pool.append(widget)
        del self.widget_dict[eid]


class HPNodeWidget(object):
    TEMPLATE = 'pve/i_pve_hp_monster'
    TYPE_RES = {M_NORMAL: None,
       M_TOUGH: 'gui/ui_res_2/pve/hp/icon_pve_hp_monster_yellow.png',
       M_ELITE: 'gui/ui_res_2/pve/hp/icon_pve_hp_monster_purple.png',
       M_BOSS: None
       }
    DUR = 5.0
    REMAIN_DUR = 1.0
    LERP_DUR = 0.5
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
        self.max_hp = 1
        self.cur_hp = 1
        self.max_stun = 1
        self.cur_stun = 1
        return

    def init_ui_nd(self):
        self.ui_nd = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)

    def recollect(self):
        self.bind_event(False)
        self.ui_nd.StopTimerAction()
        self.parent.collect_widget(self.eid)
        self.init_params()

    def destroy(self):
        self.bind_event(False)
        self.ui_nd.StopTimerAction()
        self.ui_nd.Destroy()
        self.ui_nd = None
        self.init_params()
        return

    def set_target(self, eid):
        if not self.ui_nd or not self.ui_nd.isValid():
            return
        else:
            if self.eid == eid:
                if self.m_type == M_BOSS:
                    self.ui_nd.nd_hp.setVisible(False)
                    return
                self.ui_nd.nd_hp.setVisible(True)
                self.init_tick()
            else:
                self.eid = eid
                self.target = self.get_target(eid)
                if self.target and self.target.logic:
                    m_type = self.target.logic.sd.ref_monster_type
                    if m_type == M_BOSS:
                        self.m_type = M_BOSS
                        self.ui_nd.nd_hp.setVisible(False)
                        return
                    if m_type != self.m_type:
                        self.m_type = m_type
                        if self.eid in self.parent.parent.target_monsters:
                            self.ui_nd.icon_target.setVisible(True)
                            self.ui_nd.icon_monster.setVisible(False)
                        else:
                            self.ui_nd.icon_target.setVisible(False)
                            icon_path = self.TYPE_RES.get(m_type, None)
                            self.ui_nd.icon_monster.setVisible(bool(icon_path))
                            icon_path and self.ui_nd.icon_monster.SetDisplayFrameByPath('', icon_path)
                    self.max_hp = self.target.logic.ev_g_max_hp()
                    self.cur_hp = self.target.logic.ev_g_hp()
                    ratio = self.cur_hp / self.max_hp
                    self.ui_nd.hp_monster.SetPercent(ratio * 100)
                    self.ui_nd.hp_monster_dark.SetPercent(ratio * 100)
                    self.max_stun = self.target.logic.ev_g_max_stun()
                    self.cur_stun = self.target.logic.ev_g_stun()
                    ratio = self.cur_stun / self.max_stun if self.max_stun else 0
                    self.ui_nd.nd_vertigo.setVisible(bool(self.max_stun))
                    self.ui_nd.hp_monster_yellow.SetPercent(ratio * 100)
                self.bind_event(True)
                self.ui_nd.nd_hp.setVisible(True)
                self.init_tick()
            return

    def get_target(self, eid):
        if self.target:
            return self.target
        else:
            target = EntityManager.getentity(eid)
            if target:
                return target
            return None

    def bind_event(self, bind=True):
        if not self.target or not self.target.logic:
            return
        if bind:
            self.target.logic.regist_event('E_HEALTH_HP_CHANGE', self.on_hp_change)
            self.target.logic.regist_event('E_HEALTH_HP_EMPTY', self.on_hp_empty)
            self.target.logic.regist_event('E_STUN_CHANGE', self.on_stun_change)
        else:
            self.target.logic.unregist_event('E_HEALTH_HP_CHANGE', self.on_hp_change)
            self.target.logic.unregist_event('E_HEALTH_HP_EMPTY', self.on_hp_empty)
            self.target.logic.unregist_event('E_STUN_CHANGE', self.on_stun_change)

    def on_hp_change(self, hp, mod=0):
        self.cur_hp = hp
        if mod <= 0:
            ratio = self.cur_hp / self.max_hp
            self.ui_nd.hp_monster.SetPercent(ratio * 100)
            self.ui_nd.hp_monster_dark.SetPercent(ratio * 100, self.LERP_DUR)

    def on_hp_empty(self):
        self.init_tick(self.REMAIN_DUR)
        self.ui_nd.PlayAnimation('die')

    def on_stun_change(self, stun, mod=0):
        self.cur_stun = stun
        ratio = self.cur_stun / self.max_stun
        self.ui_nd.hp_monster_yellow.SetPercent(ratio * 100)
        if ratio >= 0.99:
            self.ui_nd.PlayAnimation('vertigo')

    def init_tick(self, dur=DUR):
        self.ui_nd.StopTimerAction()
        self.ui_nd.TimerAction(self.tick_pos, dur, self.tick_end_cb, 0.016)

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
                return

    def tick_end_cb(self):
        self.recollect()