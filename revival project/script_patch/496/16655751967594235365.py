# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8008AimUI.py
from __future__ import absolute_import
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from .MechaBulletWidget import MechaBulletWidget, MechaEnergyWidget, MAIN_WEAPON, SUB_WEAPON
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from logic.gcommon.common_utils import status_utils
import cc
import world
PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_red.png',
 'gui/ui_res_2/battle/mech_attack/progress_mech_8003_jet_white.png']
MECHA_ID = 8008

class Mecha8008AimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8008'
    WEAPON_INFO = {PART_WEAPON_POS_MAIN1: MAIN_WEAPON
       }

    def init_aim_spread_mgr(self):
        from logic.comsys.mecha_ui import MechaAimSpreadMgr
        self.aim_spread_mgr = MechaAimSpreadMgr.MechaAimSpreadMgr(self.panel, MechaAimSpreadMgr.SPREAD_BY_SIZE)

    def init_bullet_widget(self):
        self.bullet_widget = None
        if global_data.is_pc_mode:
            self.panel.nd_bullet_ob.setVisible(False)
        else:
            self.bullet_widget = MechaBulletWidget(self.panel, self.WEAPON_INFO)
        weapon_info = {mecha_status_config.MC_SECOND_WEAPON_ATTACK: SUB_WEAPON}
        self.energy_widget = MechaEnergyWidget(self.panel, weapon_info)
        return

    def on_finalize_panel(self):
        super(Mecha8008AimUI, self).on_finalize_panel()
        self.destroy_widget('energy_widget')

    def init_parameters(self):
        self.timer_id = None
        self.show_sub = False
        self.enable_auto = False
        data = status_utils.get_behavior_config(str(MECHA_ID))
        behavior = data.get_behavior(str(MECHA_ID))
        self._skill_second_weapon = behavior[mecha_status_config.MC_SECOND_WEAPON_ATTACK]['custom_param']['skill_id']
        super(Mecha8008AimUI, self).init_parameters()
        return

    def init_event(self):
        if not self.mecha:
            return
        behavior = self.mecha.ev_g_behavior_config()
        self._skill_second_wepon = behavior[mecha_status_config.MC_SECOND_WEAPON_ATTACK]['custom_param']['skill_id']
        self._skill_laser = behavior[mecha_status_config.MC_PHOTON_ATTACK]['custom_param']['skill_id']
        skill_obj = self.mecha.ev_g_skill(self._skill_laser)
        if skill_obj:
            self.enable_weapon_aim_helper(True, PART_WEAPON_POS_MAIN2)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENERGY_CHANGE', self.on_energy_change)
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            regist_func('E_DO_SKILL', self.on_do_skill)
            self.init_event()
            self.aim_spread_mgr and self.aim_spread_mgr.on_mecha_setted(mecha)
            self.bullet_widget and self.bullet_widget.on_mecha_setted(mecha)
            self.energy_widget and self.energy_widget.on_mecha_setted(mecha)
            self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENERGY_CHANGE', self.on_energy_change)
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            unregist_func('E_DO_SKILL', self.on_do_skill)
        self.mecha = None
        return

    def on_show(self, skill_id):
        if self.show_sub or skill_id != self._skill_second_weapon:
            return
        self.show_sub = True
        self.panel.PlayAnimation('show_sub')
        self.stop_update_front_sight_extra_info()

    def on_hide(self, skill_id):
        if not self.show_sub or skill_id != self._skill_second_weapon:
            return
        self.show_sub = False
        self.panel.PlayAnimation('disappear_sub')
        self.start_update_front_sight_extra_info(PART_WEAPON_POS_MAIN1)

    def on_energy_change(self, key, percent):
        if key == self._skill_laser:
            percent *= 100
            self.panel.progress_charge.setPercent(percent)
            if percent == 100:
                self.enable_auto = True
                self.panel.PlayAnimation('enable_auto')
            elif self.enable_auto:
                self.enable_auto = False
                self.panel.PlayAnimation('unable_auto')

    def enable_weapon_aim_helper(self, flag, weapon_pos):
        if weapon_pos != PART_WEAPON_POS_MAIN2:
            return
        if flag:
            self.panel.StopAnimation('disappear_auto')
            self.panel.PlayAnimation('sample_visable_auto')
        else:
            self.panel.StopAnimation('sample_visable_auto')
            self.panel.PlayAnimation('disappear_auto')

    def on_do_skill(self, skill_id, *args):
        if skill_id != self._skill_laser:
            return
        if not self.mecha:
            return
        target = self.mecha.sd.ref_aim_target
        scn = global_data.game_mgr.scene
        if not scn:
            return
        camera = scn.active_camera
        if not camera:
            return
        self.panel.PlayAnimation('auto_lock')

        def _cb(pass_time):
            if target:
                model = target.ev_g_model()
                if model:
                    bone_matrix = model.get_bone_matrix(BONE_BIPED_NAME, world.SPACE_TYPE_WORLD)
                    if bone_matrix:
                        pos = bone_matrix.translation
                        x, y = camera.world_to_screen(pos)
                        pos = neox_pos_to_cocos(x, y)
                        pos = self.panel.auto.convertToNodeSpace(cc.Vec2(*pos))
                        self.panel.nd_lock.setPosition(pos)
            else:
                self.panel.StopAnimation('auto_lock', finish_ani=True)
                self.panel.StopTimerAction()

        max_time = self.panel.GetAnimationMaxRunTime('auto_lock')
        self.panel.StopTimerAction()
        self.panel.TimerAction(_cb, max_time, interval=0.033)