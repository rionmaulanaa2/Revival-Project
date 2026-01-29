# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBossBloodWidget.py
from __future__ import absolute_import
import six
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon.common_const.buff_const import BUFF_ID_PVE_ICE
ICE_MAX_LAYER = len(confmgr.get('mecha_conf', 'HitFlagConfig', 'Content', str(BUFF_ID_PVE_ICE), 'level_list', default=[]))

class PVEBossBloodWidget(object):
    TEMPLATE = 'pve/i_pve_hp_boss'
    LERP_DUR = 0.5

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.process_events(True)
        if global_data.battle:
            b_eid = global_data.battle.get_pve_boss_eid()
            if b_eid:
                self.bind_event(False)
                self.init_boss(b_eid)

    def init_params(self):
        self.eid = None
        self.target = None
        self.widget = None
        self.max_hp = 1
        self.cur_hp = 1
        self.max_stun = 1
        self.cur_stun = 1
        self._cur_ice = 0
        return

    def process_events(self, is_bind):
        econf = {'pve_boss_switch_invincible': self.on_switch_invincible
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.bind_event(False)
        self.widget and self.widget.setVisible(False)

    def destroy(self):
        self.destroy_boss(None)
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def init_boss(self, eid):
        self.eid = eid
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.target = self.get_target(eid)
        if not self.target:
            return
        self.bind_event(True)
        self.widget.nd_name.lab_name.SetString(get_text_by_id(self.target.logic.ev_g_monster_name()))
        self.max_hp = self.target.logic.ev_g_max_hp()
        self.cur_hp = self.target.logic.ev_g_hp()
        ratio = float(self.cur_hp) / self.max_hp
        self.widget.nd_hp.nd_prog.hp_monster.SetPercent(ratio * 100)
        self.widget.nd_hp.nd_prog.hp_monster_dark.SetPercent(ratio * 100)
        self.widget.nd_hp.lab_prog.SetString('%i/%i' % (self.cur_hp, self.max_hp))
        self.max_stun = self.target.logic.ev_g_max_stun()
        self.cur_stun = self.target.logic.ev_g_stun()
        ratio = float(self.cur_stun) / self.max_stun if self.max_stun else 0
        self.widget.nd_hp.nd_prog.nd_vertigo.setVisible(bool(self.max_stun))
        self.widget.nd_hp.nd_prog.nd_vertigo.hp_monster_yellow.SetPercent(ratio * 100)
        self.widget.nd_hp.nd_prog.hp_monster_blue.setVisible(False)
        self.widget.nd_hp.img_ice_pnl.setVisible(False)
        self.widget.nd_hp.vx_baokai_01.setVisible(False)

    def destroy_boss(self, eid):
        self.bind_event(False)
        self.widget and self.widget.setVisible(False)

    def on_switch_invincible(self, ret):
        self.widget and self.widget.nd_hp.nd_invincible.setVisible(ret)

    def get_target(self, eid):
        target = EntityManager.getentity(eid)
        if target:
            return target
        else:
            return None

    def bind_event(self, bind=True):
        if not self.target or not self.target.logic:
            return
        econf = {'E_HEALTH_HP_CHANGE': self.on_hp_change,'E_HEALTH_HP_EMPTY': self.on_hp_empty,
           'E_STUN_CHANGE': self.on_stun_change,
           'E_PVE_ICE_CHANGE': self.on_ice_change
           }
        reg_func = self.target.logic.regist_event if bind else self.target.logic.unregist_event
        for event, func in six.iteritems(econf):
            reg_func(event, func)

    def on_hp_change(self, hp, mod=0):
        self.cur_hp = hp
        ratio = float(self.cur_hp) / self.max_hp
        self.widget.nd_hp.nd_prog.hp_monster.SetPercent(ratio * 100)
        self.widget.nd_hp.nd_prog.hp_monster_dark.SetPercent(ratio * 100, self.LERP_DUR)
        self.widget.nd_hp.lab_prog.SetString('%i/%i' % (self.cur_hp, self.max_hp))

    def on_hp_empty(self):
        from logic.comsys.battle.pve.PVEBossDefeatUI import PVEBossDefeatUI
        PVEBossDefeatUI()

    def on_stun_change(self, stun, mod=0):
        self.cur_stun = stun
        ratio = float(self.cur_stun) / self.max_stun
        self.widget.nd_hp.nd_prog.nd_vertigo.hp_monster_yellow.SetPercent(ratio * 100)
        if ratio >= 0.99:
            self.widget.PlayAnimation('vertigo')

    def on_ice_change(self, ice):
        if ice == self._cur_ice:
            return
        if ice > 0:
            ice = min(ice, ICE_MAX_LAYER)
            self.widget.StopAnimation('ice_break')
            self.widget.nd_hp.vx_baokai_01.setVisible(False)
            self.widget.nd_hp.img_ice_pnl.hp_prog_ice.ResetNodeConfAttr()
            self.widget.nd_hp.img_ice_pnl.hp_prog_ice.SetPercent(ice * 100.0 / ICE_MAX_LAYER)
            if not self.widget.nd_hp.img_ice_pnl.isVisible():
                self.widget.PlayAnimation('ice_show')
        elif ice < 0:
            self.widget.StopAnimation('ice_show')
            self.widget.PlayAnimation('ice_break')
        elif self._cur_ice < ICE_MAX_LAYER:
            self.widget.nd_hp.img_ice_pnl.setVisible(False)
        else:
            return
        self._cur_ice = ice