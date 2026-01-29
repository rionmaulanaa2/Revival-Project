# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8021AimUI.py
from __future__ import absolute_import
import six
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from logic.gcommon.time_utility import get_server_time
from common.cfg import confmgr
from common.utils.timer import RELEASE
MAX_ENHANCE_SLASH_ENERGY_PERCENT = 88
MIN_ENHANCE_SLASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_ENHANCE_SLASH_ENERGY_PERCENT - MIN_ENHANCE_SLASH_ENERGY_PERCENT

class Mecha8021AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8021'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }
    MECHA_EVENT = {'E_ENHANCE_8021_SEC_WP': 'on_enhance_slash',
       'E_UPDATE_SKILL': 'on_update_skill'
       }

    def do_show_panel(self):
        super(Mecha8021AimUI, self).do_show_panel()
        self.nd_sub.setVisible(self.sub_visible)

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui.MechaAimSpreadMgr import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr(self.panel)

    def init_parameters(self):
        self.over_loading = False
        self.playing_dash_pre = False
        self.last_val_percent = 100
        self.showing_ball_fuel = False
        self.is_ball_state = False
        self.need_resume_show_fuel = False
        self.showing_flamethrower_energy = False
        self.flamethrower_energy_state_timer = None
        self.slash_skill_id = 802151
        self.enhance_slash_timer = -1
        self.enhance_slash_duration = 0
        self.enhance_slash_max_duration = confmgr.get('skill_conf', str(self.slash_skill_id), 'ext_info', 'enhance_next_duration', default=10.0)
        self.sub_visible = False
        super(Mecha8021AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            for event_name, func_name in six.iteritems(self.MECHA_EVENT):
                regist_func(event_name, getattr(self, func_name))

            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            unregist_func = self.mecha.unregist_event
            for event_name, func_name in six.iteritems(self.MECHA_EVENT):
                unregist_func(event_name, getattr(self, func_name))

        self.mecha = None
        return

    def on_enhance_slash_start(self, end_timestamp):
        cur_time = get_server_time()
        left_duration = end_timestamp - cur_time
        if left_duration <= 0:
            return
        self.show_sub()
        self.enhance_slash_duration = left_duration
        if self.enhance_slash_timer > -1:
            global_data.game_mgr.unregister_logic_timer(self.enhance_slash_timer)
        self.enhance_slash_timer = global_data.game_mgr.register_logic_timer(self.update_energy, interval=1, times=-1, timedelta=True)
        cur_percent = MIN_ENHANCE_SLASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * float(left_duration) / self.enhance_slash_max_duration
        self.panel.prog_sub_left.SetPercentage(cur_percent)

    def on_enhance_slash_end(self):
        if self.panel:
            self.panel.prog_sub_left.stopAllActions()
            self.disappear_sub()
            if self.enhance_slash_timer > -1:
                global_data.game_mgr.unregister_logic_timer(self.enhance_slash_timer)
                self.enhance_slash_timer = -1

    def on_enhance_slash(self, timestamp):
        if timestamp:
            self.on_enhance_slash_start(timestamp)
        else:
            self.on_enhance_slash_end()

    def on_update_skill(self, skill_id, skill_data):
        if self.enhance_slash_timer < 0:
            return
        else:
            if skill_id != self.slash_skill_id:
                return
            if skill_data.get('active_enhance', None) == 0:
                self.on_enhance_slash_end()
            return

    def update_energy(self, dt):
        if not (self.panel and self.panel.isValid()):
            return RELEASE
        self.enhance_slash_duration -= dt
        if self.enhance_slash_duration < 0.0:
            self.enhance_slash_duration = 0.0
        cur_percent = MIN_ENHANCE_SLASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * float(self.enhance_slash_duration) / self.enhance_slash_max_duration
        self.panel.prog_sub_left.SetPercentage(cur_percent)
        if self.enhance_slash_duration == 0.0:
            self.disappear_sub()
            self.enhance_slash_timer = -1
            return RELEASE

    def show_sub(self):
        self.sub_visible = True
        self.panel.StopAnimation('show_sub')
        self.panel.PlayAnimation('show_sub')

    def disappear_sub(self):
        if self.panel.nd_sub.IsVisible():
            self.panel.PlayAnimation('disappear_sub')
        self.sub_visible = False