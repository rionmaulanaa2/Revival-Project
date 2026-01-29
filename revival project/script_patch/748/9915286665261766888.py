# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8016AimUI.py
from __future__ import absolute_import
import six
from .BaseMechaAimUI import BaseMechaAimUI
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gcommon.common_const import skill_const
import common.utils.timer as timer
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.cdata.mecha_status_config import *
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/prog_left_red.png',
 'gui/ui_res_2/battle/mech_attack/prog_left.png']

class Mecha8016AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8016'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def init_parameters(self):
        super(Mecha8016AimUI, self).init_parameters()
        self.is_shooting = False
        self.last_val_percent = 100
        self.panel.progress1.setPercentage(100)
        self._acc_skill_begin_time = None
        self.timer = None
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if not mecha:
            return
        self.mecha = mecha
        regist_func = mecha.regist_event
        regist_func('E_ACC_SKILL_HOLD', self._hold_acc_skill)
        regist_func('E_ACC_SKILL_BEGIN', self._start_acc_skill)
        regist_func('E_ACC_SKILL_END', self._stop_acc_skill)
        regist_func('E_ENERGY_CHANGE', self._on_flight_boost_skill)
        self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
        self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
        self.max_acc_skill_time = self.mecha.sd.ref_8016_acc_skill_time
        self.last_val_percent = self.mecha.ev_g_energy(skill_const.SKILL_DASH_8016) * 100 or 0
        self.progress_pic = 0 if self.last_val_percent <= 25 else 1
        if self.last_val_percent < 100:
            self.panel.PlayAnimation('show_jet')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ACC_SKILL_HOLD', self._hold_acc_skill)
            unregist_func('E_ACC_SKILL_BEGIN', self._start_acc_skill)
            unregist_func('E_ACC_SKILL_END', self._stop_acc_skill)
            unregist_func('E_ENERGY_CHANGE', self._on_flight_boost_skill)
        self.mecha = None
        return

    def do_show_panel--- This code section failed: ---

  72       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'Mecha8016AimUI'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'do_show_panel'
          15  CALL_FUNCTION_0       0 
          18  POP_TOP          

  73      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             3  'panel'
          25  LOAD_ATTR             4  'nd_aim'
          28  LOAD_ATTR             5  'setVisible'
          31  LOAD_GLOBAL           6  'True'
          34  CALL_FUNCTION_1       1 
          37  POP_TOP          

  74      38  LOAD_GLOBAL           7  'global_data'
          41  LOAD_ATTR             8  'is_pc_mode'
          44  POP_JUMP_IF_TRUE     69  'to 69'

  75      47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             3  'panel'
          53  LOAD_ATTR             9  'nd_bullet_ob'
          56  LOAD_ATTR             5  'setVisible'
          59  LOAD_GLOBAL           6  'True'
          62  CALL_FUNCTION_1       1 
          65  POP_TOP          
          66  JUMP_FORWARD          0  'to 69'
        69_0  COME_FROM                '66'

  76      69  LOAD_GLOBAL          10  'getattr'
          72  LOAD_GLOBAL           1  'Mecha8016AimUI'
          75  LOAD_CONST            0  ''
          78  CALL_FUNCTION_3       3 
          81  STORE_FAST            1  'aim_spread_mgr'

  77      84  LOAD_FAST             1  'aim_spread_mgr'
          87  JUMP_IF_FALSE_OR_POP    99  'to 99'
          90  LOAD_FAST             1  'aim_spread_mgr'
          93  LOAD_ATTR            12  '_on_spread'
          96  CALL_FUNCTION_0       0 
        99_0  COME_FROM                '87'
          99  POP_TOP          
         100  LOAD_CONST            0  ''
         103  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 78

    def _hold_acc_skill(self, *args):
        self.panel.progress1.setPercentage(100)
        self._acc_skill_begin_time = -1
        self.panel.PlayAnimation('show_sp')

    def _start_acc_skill(self, *args):
        self._acc_skill_begin_time = get_server_time()
        self.stop_update_front_sight_extra_info()
        if not self.timer:
            self.timer = global_data.game_mgr.register_logic_timer(self.tick, interval=1, times=-1)

    def _stop_acc_skill(self, *args):
        if self._acc_skill_begin_time is None:
            return
        else:
            self.panel.StopAnimation('show_sp')
            self.panel.PlayAnimation('disappear_sp')
            self._acc_skill_begin_time = None
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)
            self.destroy_timer()
            return

    def tick(self):
        if not self.mecha or self.max_acc_skill_time is None or self._acc_skill_begin_time is None or self._acc_skill_begin_time < 0:
            self.destroy_timer()
            return
        else:
            cur_time = get_server_time() - self._acc_skill_begin_time
            percent = cur_time / self.max_acc_skill_time
            percent = max(0.0, min(1.0, percent))
            track_percent = (1.0 - percent) * 100.0
            self.panel.progress1.setPercentage(track_percent)
            return

    def _on_flight_boost_skill(self, skill_id, percent):
        if skill_id != skill_const.SKILL_DASH_8016:
            return
        percent *= 100
        percentage_range = (62, 88)
        rate = (percentage_range[1] - percentage_range[0]) * 1.0 / 100
        if self.last_val_percent < percent == 100:
            self.panel.PlayAnimation('disappear_jet')
        elif self.last_val_percent == 100 > percent:
            self.panel.PlayAnimation('show_jet')
        self.panel.nd_jet.setVisible(True)
        progress_pic = 0 if self.last_val_percent <= 25 else 1
        if self.progress_pic != progress_pic:
            if progress_pic == 0:
                self.panel.PlayAnimation('warning')
            self.progress_pic = progress_pic
            self.panel.prog_jet.SetProgressTexture(PROGRESS_PIC[progress_pic])
            self.panel.prog_jet.setPercentage((percent + 0.01) * rate + percentage_range[0])
        self.panel.prog_jet.setPercentage(percent * rate + percentage_range[0])
        self.last_val_percent = percent

    def destroy_timer(self):
        if not self.timer:
            return
        else:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
            return

    def on_finalize_panel(self):
        super(Mecha8016AimUI, self).on_finalize_panel()
        self.destroy_timer()