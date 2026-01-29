# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMonsterHPWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.common_const.pve_const import M_NORMAL, M_TOUGH, M_ELITE, M_BOSS
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
from common.utils.cocos_utils import neox_pos_to_cocos
import cc
from time import time
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from common.utils.ui_utils import get_scale
from common.cfg import confmgr
from logic.gcommon.common_const.buff_const import BUFF_ID_PVE_ICE
ICE_MAX_LAYER = len(confmgr.get('mecha_conf', 'HitFlagConfig', 'Content', str(BUFF_ID_PVE_ICE), 'level_list', default=[]))

class PVEMonsterHPWidget(object):
    CACHE_SIZE = 20
    C_MAP = {1: 20,
       2: 30,
       3: 40
       }
    SCREEN_MARGIN = get_scale('40w')

    def __init__(self, panel, parent):
        self.parent = parent
        self.panel = panel
        self.init_params()
        self.process_events(True)

    def init_params(self):
        self.widget_dict = {}
        self.cache_pool = []
        self.target_monsters = []
        if global_data.battle:
            size = global_data.battle.get_pve_player_size_mode()
            self.cache_size = self.C_MAP.get(size, self.CACHE_SIZE)

    def process_events(self, is_bind):
        econf = {'pve_monster_init': self.on_init_monster,
           'pve_monster_hit': self.on_hit_monster,
           'pve_monster_destroy': self.on_destroy_monster,
           'pve_set_target_monsters': self.set_target_monsters,
           'pve_monster_confused': self.on_monster_confused
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        for eid in self.widget_dict:
            widget = self.widget_dict[eid]
            if len(self.cache_pool) > self.cache_size:
                widget.destroy()
            else:
                widget.ui_nd.retain()
                widget.ui_nd.setVisible(False)
                widget.ui_nd.nd_hp.hp_monster.SetColor('#SW')
                widget.ui_nd.StopAnimation('ice_show')
                widget.ui_nd.StopAnimation('ice_break')
                widget.ui_nd.nd_hp.img_ice_pnl.setVisible(False)
                widget.ui_nd.vx.vx_baokai_01.setVisible(False)
                widget.space_nd.setVisible(False)
                widget.space_nd.set_visible_callback(None)
                self.cache_pool.append(widget)

        self.widget_dict = {}
        return

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
        if unit.sd.ref_monster_type == M_BOSS:
            return
        else:
            init_eid = unit.id
            widget = self.widget_dict.get(init_eid, None)
            if not widget:
                if self.cache_pool:
                    widget = self.cache_pool.pop()
                else:
                    widget = self.init_widget()
                self.widget_dict[init_eid] = widget
            widget.init_target(init_eid)
            return

    def on_hit_monster(self, hit_eid):
        widget = self.widget_dict.get(hit_eid, None)
        if not widget:
            return
        else:
            widget.hit_target(hit_eid)
            return

    def on_monster_confused(self, monster_eid, confused):
        widget = self.widget_dict.get(monster_eid, None)
        if not widget:
            return
        else:
            widget.set_confused(confused)
            return

    def on_destroy_monster(self, unit):
        d_eid = unit.id
        widget = self.widget_dict.get(d_eid, None)
        if not widget:
            return
        else:
            widget.destroy_target(d_eid)
            return

    def set_target_monsters(self, target_list):
        self.target_monsters = target_list
        for eid in self.widget_dict:
            if eid in self.target_monsters:
                widget = self.widget_dict[eid]
                widget.ui_nd.nd_hp.hp_icon_target.setVisible(True)
                widget.ui_nd.nd_hp.hp_icon_monster.setVisible(False)
                widget.ui_nd.nd_icon.icon_target.setVisible(True)
                widget.ui_nd.nd_icon.icon_arrow.setVisible(False)

    def init_widget(self):
        return HPNodeWidget(self.panel, self)

    def collect_widget(self, eid):
        if eid not in self.widget_dict:
            return
        else:
            widget = self.widget_dict[eid]
            if len(self.cache_pool) > self.cache_size:
                widget.destroy()
            else:
                widget.ui_nd.retain()
                widget.ui_nd.setVisible(False)
                widget.ui_nd.nd_hp.hp_monster.SetColor('#SW')
                widget.ui_nd.StopAnimation('ice_show')
                widget.ui_nd.StopAnimation('ice_break')
                widget.ui_nd.nd_hp.img_ice_pnl.setVisible(False)
                widget.ui_nd.vx.vx_baokai_01.setVisible(False)
                widget.space_nd.setVisible(False)
                widget.space_nd.set_visible_callback(None)
                self.cache_pool.append(widget)
            del self.widget_dict[eid]
            return


class HPNodeWidget(object):
    TEMPLATE = 'pve/i_pve_hp_monster'
    TYPE_RES = {M_NORMAL: None,
       M_TOUGH: 'gui/ui_res_2/pve/hp/icon_pve_hp_monster_grey.png',
       M_ELITE: 'gui/ui_res_2/pve/hp/icon_pve_hp_monster_purple.png',
       M_BOSS: None
       }
    CONFUSED_ICON = 'gui/ui_res_2/pve/hp/icon_pve_hp_monster_dark.png'
    HIT_DUR = 5.0
    REMAIN_DUR = 0.5
    TRANS_DUR = 2.0
    LERP_DUR = 0.5
    MAX_DIS = 200 * NEOX_UNIT_SCALE
    MIN_DIS = 10 * NEOX_UNIT_SCALE
    MAX_SCL = 1.0
    MIN_SCL = 0.2
    TAG_BASE = 61
    TAG_HIT = 62
    TAG_DIE = 63

    def __init__(self, panel, parent):
        self.panel = panel
        self.parent = parent
        self.space_nd = None
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
        self.ts = 0
        self.hit_tag = False
        self.die_tag = False
        self.confused = False
        return

    def init_ui_nd(self):
        self.space_nd = CCUISpaceNode.Create()
        self.ui_nd = global_data.uisystem.load_template_create(self.TEMPLATE)
        self.space_nd.AddChild('', self.ui_nd)
        self.ui_nd.setPosition(0, NEOX_UNIT_SCALE * 1.0)

    def recollect(self):
        self.bind_event(False)
        self.ui_nd.StopTimerActionByTag(self.TAG_HIT)
        self.parent.collect_widget(self.eid)
        self.init_params()

    def destroy(self):
        self.bind_event(False)
        self.ui_nd.StopTimerActionByTag(self.TAG_HIT)
        self.ui_nd.Destroy()
        self.ui_nd = None
        self.space_nd.Destroy()
        self.space_nd = None
        self.init_params()
        return

    def init_target(self, eid):
        if not self.ui_nd or not self.ui_nd.isValid():
            return
        else:
            if self.eid == eid:
                return
            self.eid = eid
            self.target = self.get_target(eid)
            if self.target and self.target.logic:
                m_type = self.target.logic.sd.ref_monster_type
                self.m_type = m_type
            else:
                self.recollect()
                return
            if self.eid in self.parent.target_monsters:
                self.ui_nd.nd_hp.hp_icon_target.setVisible(True)
                self.ui_nd.nd_hp.hp_icon_monster.setVisible(False)
                self.ui_nd.nd_icon.icon_target.setVisible(True)
                self.ui_nd.nd_icon.icon_arrow.setVisible(False)
            else:
                self.ui_nd.nd_hp.hp_icon_target.setVisible(False)
                icon_path = self.TYPE_RES.get(self.m_type, None)
                self.ui_nd.nd_hp.hp_icon_monster.setVisible(bool(icon_path))
                icon_path and self.ui_nd.nd_hp.hp_icon_monster.SetDisplayFrameByPath('', icon_path)
                self.ui_nd.nd_icon.icon_target.setVisible(False)
                self.ui_nd.nd_icon.icon_arrow.setVisible(True)
            self.max_hp = self.target.logic.ev_g_max_hp()
            self.cur_hp = self.target.logic.ev_g_hp()
            ratio = float(self.cur_hp) / self.max_hp
            self.ui_nd.nd_hp.hp_monster.SetPercent(ratio * 100)
            self.ui_nd.nd_hp.hp_monster_dark.SetPercent(ratio * 100)
            self.max_stun = self.target.logic.ev_g_max_stun()
            self.cur_stun = self.target.logic.ev_g_stun()
            ratio = float(self.cur_stun) / self.max_stun if self.max_stun else 0
            self.ui_nd.nd_hp.nd_vertigo.setVisible(bool(self.max_stun))
            self.ui_nd.nd_hp.nd_vertigo.hp_monster_yellow.SetPercent(ratio * 100)
            self.ui_nd.nd_hp.img_ice_pnl.setVisible(False)
            self.ui_nd.vx.vx_baokai_01.setVisible(False)
            self._cur_ice = 0
            self.bind_event(True)
            self.ui_nd.nd_hp.setVisible(False)
            self.ui_nd.nd_icon.setVisible(True)
            self.ts = 0
            self.hit_tag = False
            self.die_tag = False
            self.bind_target()
            return

    def hit_target(self, eid):
        if self.die_tag:
            return
        if not self.hit_tag:
            self.ui_nd.nd_hp.setVisible(True)
            self.ui_nd.nd_icon.setVisible(False)
            self.hit_tag = True
        if not self.confused and time() - self.ts > self.TRANS_DUR:
            self.ts = time()
            self.init_hit_tick()

    def set_confused(self, confused):
        self.confused = confused
        self.ui_nd.nd_hp.hp_monster.SetColor('#SG' if confused else '#SW')
        icon_path = self.CONFUSED_ICON if confused else self.TYPE_RES.get(self.m_type, None)
        self.ui_nd.hp_icon_monster.setVisible(bool(icon_path))
        icon_path and self.ui_nd.hp_icon_monster.SetDisplayFrameByPath('', icon_path)
        if confused:
            self.ui_nd.StopTimerActionByTag(self.TAG_HIT)
        self.hit_target(None)
        return

    def destroy_target(self, eid):
        self.tick_end_cb()

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
        self.ui_nd.hp_monster.SetPercent(ratio * 100)
        if mod <= 0:
            self.ui_nd.hp_monster_dark.SetPercent(ratio * 100, self.LERP_DUR)
        else:
            self.ui_nd.hp_monster_dark.SetPercent(ratio * 100)

    def on_hp_empty(self):
        self.die_tag = True
        self.ui_nd.PlayAnimation('die')
        self.init_die_tick()

    def on_stun_change(self, stun, mod=0):
        self.cur_stun = stun
        ratio = float(self.cur_stun) / self.max_stun
        self.ui_nd.nd_hp.nd_vertigo.hp_monster_yellow.SetPercent(ratio * 100)
        if ratio >= 0.99:
            self.ui_nd.PlayAnimation('vertigo')

    def on_ice_change(self, ice):
        if ice == self._cur_ice:
            return
        else:
            if ice > 0:
                ice = min(ice, ICE_MAX_LAYER)
                self.ui_nd.StopAnimation('ice_break')
                self.ui_nd.vx.vx_baokai_01.setVisible(False)
                self.ui_nd.nd_hp.img_ice_pnl.hp_prog_ice.ResetNodeConfAttr()
                self.ui_nd.nd_hp.img_ice_pnl.hp_prog_ice.SetPercent(ice * 100.0 / ICE_MAX_LAYER)
                if not self.ui_nd.nd_hp.img_ice_pnl.isVisible():
                    self.ui_nd.PlayAnimation('ice_show')
                self.hit_target(None)
            elif ice < 0:
                self.ui_nd.StopAnimation('ice_show')
                self.ui_nd.PlayAnimation('ice_break')
            elif self._cur_ice < ICE_MAX_LAYER:
                self.ui_nd.nd_hp.img_ice_pnl.setVisible(False)
            else:
                return
            self._cur_ice = ice
            return

    def bind_target(self):
        if self.target and self.target.logic:
            model = self.target.logic.ev_g_model()
            if model and model.valid:

                def vis_cb(last_need_draw, cur_need_draw):
                    if self.ui_nd and self.ui_nd.isValid():
                        self.ui_nd.setVisible(True if cur_need_draw and self.target else False)

                self.space_nd.setVisible(True)
                self.space_nd.set_visible_callback(vis_cb)
                self.space_nd.bind_model(model, 'xuetiao')
                self.space_nd.set_fix_xz(False)
                return True
        self.recollect()
        return False

    def tick_end_cb(self):
        self.recollect()

    def init_hit_tick(self):
        self.ui_nd.StopTimerActionByTag(self.TAG_HIT)
        self.ui_nd.TimerActionByTag(self.TAG_HIT, self.tick_hit, self.HIT_DUR, self.tick_hit_cb, 1.0)

    def tick_hit(self, *args):
        pass

    def tick_hit_cb(self):
        self.ui_nd.nd_hp.setVisible(False)
        self.ui_nd.nd_icon.setVisible(True)
        self.hit_tag = False

    def init_die_tick(self):
        self.ui_nd.StopTimerActionByTag(self.TAG_DIE)
        self.ui_nd.TimerActionByTag(self.TAG_DIE, self.tick_die, self.REMAIN_DUR, self.tick_die_cb, 0.1)

    def tick_die(self, *args):
        pass

    def tick_die_cb(self):
        self.ui_nd.setVisible(False)
        self.die_tag = True

    def get_target(self, eid):
        if self.target:
            return self.target
        else:
            target = EntityManager.getentity(eid)
            if target:
                return target
            return None