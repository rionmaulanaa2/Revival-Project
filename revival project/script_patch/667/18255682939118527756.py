# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8011AimUI.py
from __future__ import absolute_import
import six
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
import logic.gcommon.const as g_const
from common.cfg import confmgr
from common.utils.timer import RELEASE
import cc
WEAPON_ID_MAP = {3: '801103',
   4: '801104',
   6: '801106',
   7: '801107'
   }

class Mecha8011AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8011'
    WEAPON_INFO = {g_const.PART_WEAPON_POS_MAIN1: MAIN_WEAPON,
       g_const.PART_WEAPON_POS_MAIN2: MAIN_WEAPON
       }
    ACC_ANIM_TAG = 210113

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

        def get_aim_node():
            return self.panel.nd_aim.nd_spread

        self.aim_spread_mgr.replace_get_aim_node_func(get_aim_node)
        self.aim_spread_mgr.set_weapon_pos(g_const.PART_WEAPON_POS_MAIN1)

    def on_finalize_panel(self):
        super(Mecha8011AimUI, self).on_finalize_panel()
        self.stopActionByTag(self.ACC_ANIM_TAG)
        if self.weapon_accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.weapon_accumulate_timer)
            self.weapon_accumulate_timer = None
        return

    def init_parameters(self):
        self.is_shooting = False
        self.in_dragon_shape = False
        accumulate_config = confmgr.get('accumulate_config', default={})
        self.weapon_max_accumulate_duration = {}
        for weapon_pos, weapon_id in six.iteritems(WEAPON_ID_MAP):
            self.weapon_max_accumulate_duration[weapon_pos] = accumulate_config.get(weapon_id, {}).get('fMaxCD', 0.0)

        self.cur_weapon_max_accumulate_duration = 0.0
        self.weapon_accumulate_duration = 0.0
        self.weapon_accumulate_timer = None
        super(Mecha8011AimUI, self).init_parameters()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_TRANS_TO_DRAGON', self._trans_to_dragon)
            regist_func('E_ACC_SKILL_BEGIN', self._start_acc_weapon)
            regist_func('E_ACC_SKILL_END', self._stop_acc_weapon)
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN1)
            buff_data, dragon_left_time = mecha.ev_g_dragon_shape_left_time()
            dragon_left_time > 0.0 and self._trans_to_dragon(buff_data, dragon_left_time)
            self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_TRANS_TO_DRAGON', self._trans_to_dragon)
            unregist_func('E_ACC_SKILL_BEGIN', self._start_acc_weapon)
            unregist_func('E_ACC_SKILL_END', self._stop_acc_weapon)
        self.mecha = None
        return

    def _trans_to_dragon(self, data, left_time):
        if left_time > 0:
            self.in_dragon_shape = True
            self.panel.PlayAnimation('show_sec')
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN2)
        else:
            self.in_dragon_shape = False
            self.panel.PlayAnimation('disappear_sec')
            self.mecha.send_event('E_REFRESH_CUR_WEAPON_BULLET', g_const.PART_WEAPON_POS_MAIN1)
        self.aim_spread_mgr._on_spread()

    def _start_acc_weapon(self, weapon_pos):
        self.cur_weapon_max_accumulate_duration = self.weapon_max_accumulate_duration[weapon_pos]
        if self.in_dragon_shape:
            self.panel.PlayAnimation('charge_sub')
        else:
            action_list = list()
            action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_sec')))
            action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show_sec')))
            action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('charge_sub')))
            action = self.panel.runAction(cc.Sequence.create(action_list))
            action.setTag(self.ACC_ANIM_TAG)
        if self.cur_weapon_max_accumulate_duration == 0.0:
            self.panel.temp_extra_progress.progress_charge.SetPercentage(100)
        else:
            self.panel.temp_extra_progress.progress_charge.SetPercentage(0)
            self.weapon_accumulate_duration = self.cur_weapon_max_accumulate_duration

            def acc_tick(dt):
                self.weapon_accumulate_duration -= dt
                if self.weapon_accumulate_duration < 0.0:
                    self.weapon_accumulate_duration = 0.0
                self.panel.temp_extra_progress.progress_charge.SetPercentage(53 + (1.0 - self.weapon_accumulate_duration / self.cur_weapon_max_accumulate_duration) * 18)
                if self.weapon_accumulate_duration <= 0.0:
                    self.weapon_accumulate_timer = None
                    return RELEASE
                else:
                    return

            self.weapon_accumulate_timer = global_data.game_mgr.register_logic_timer(acc_tick, interval=1, times=-1, timedelta=True)
        self.panel.temp_extra_progress.StopAnimation('spread_fire_disappear')
        self.panel.temp_extra_progress.PlayAnimation('spread_fire_show')
        self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN3)

    def _stop_acc_weapon(self, *args):
        self.stopActionByTag(self.ACC_ANIM_TAG)
        self.panel.StopAnimation('charge_sub')
        self.panel.nd_aim_sec.setVisible(True)
        if not self.in_dragon_shape:
            action_list = list()
            action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('disappear_sec')))
            action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('disappear_sec') + 0.1))
            action_list.append(cc.CallFunc.create(lambda : self.aim_spread_mgr._on_spread()))
            action = self.panel.runAction(cc.Sequence.create(action_list))
            action.setTag(self.ACC_ANIM_TAG)
            self.panel.PlayAnimation('disappear_sec')
        self.panel.temp_extra_progress.StopAnimation('spread_fire_show')
        self.panel.temp_extra_progress.PlayAnimation('spread_fire_disappear')
        if self.weapon_accumulate_timer:
            global_data.game_mgr.unregister_logic_timer(self.weapon_accumulate_timer)
            self.weapon_accumulate_timer = None
        self.start_update_front_sight_extra_info(g_const.PART_WEAPON_POS_MAIN1)
        return