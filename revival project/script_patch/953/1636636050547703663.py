# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8027SubUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from .MechaBulletWidget import MAIN_WEAPON
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2
from mobile.common.EntityManager import EntityManager
from common.const.uiconst import AIM_ZORDER
from common.const import uiconst
from common.utils.timer import CLOCK

class Mecha8027SubUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8027_sub'
    DLG_ZORDER = AIM_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True
    ACTION_TAG = 111821

    def on_init_panel(self, *args, **kwargs):
        self.check_aim_target_timer = None
        super(Mecha8027SubUI, self).on_init_panel()
        self.init_parameters()
        self.init_auto_aim_widget()
        return

    def init_auto_aim_widget(self):
        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel)

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self._target = None
        self.second_weapon_skill_id = 802751
        self.show_num = 0
        self.weapon_aim_helper_enabled = False
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        return

    def on_finalize_panel(self):
        self.panel.nd_aim_sec.stopActionByTag(self.ACTION_TAG)
        self.unbind_ui_event(self.player)
        self.player = None
        self.mecha = None
        self.clear_aim_target_timer()
        self.destroy_widget('auto_aim_widget')
        super(Mecha8027SubUI, self).on_finalize_panel()
        return

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_main_weapon_aim)
            regist_func('E_ENERGY_CHANGE', self._on_energy_change)
            regist_func('E_CONTINUOUSSHOOT8027_ANIM_START', self._on_continuous_shoot)
            regist_func('E_AIM_TARGET_BY_BUFF', self._set_aim_target)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            self.refresh_weapon_num()

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_main_weapon_aim)
            unregist_func('E_ENERGY_CHANGE', self._on_energy_change)
            unregist_func('E_CONTINUOUSSHOOT8027_ANIM_START', self._on_continuous_shoot)
            unregist_func('E_AIM_TARGET_BY_BUFF', self._set_aim_target)
        self.mecha = None
        return

    def _set_aim_target(self, target_id, weapon_pos):
        self.clear_aim_target_timer()

        def _check():
            target = EntityManager.getentity(target_id)
            if not target or target and target.logic and target.logic.ev_g_death():
                self._enable_main_weapon_aim(False, weapon_pos)
            else:
                self._enable_main_weapon_aim(True, weapon_pos)

        self.check_aim_target_timer = global_data.game_mgr.register_logic_timer(_check, interval=1, mode=CLOCK)

    def clear_aim_target_timer(self):
        if self.check_aim_target_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_aim_target_timer)
        self.check_aim_target_timer = None
        return

    def enable_main_weapon_aim(self, enabled, weapon_pos, **kwargs):
        self._enable_main_weapon_aim(enabled, weapon_pos)
        if not enabled:
            self.clear_aim_target_timer()

    def _enable_main_weapon_aim(self, enabled, weapon_pos):
        if enabled ^ self.weapon_aim_helper_enabled:
            self.weapon_aim_helper_enabled = enabled
            if enabled and self.auto_aim_widget and self.auto_aim_widget.refresh_auto_aim_range_appearance(weapon_pos):
                self.auto_aim_widget.show()
                self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
                self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_target, weapon_pos)
            else:
                self.auto_aim_widget.hide()
                self.auto_aim_widget.update_aim_target(None, weapon_pos)
        return

    def _on_energy_change(self, key, percent):
        if key == self.second_weapon_skill_id:
            self.refresh_weapon_num(percent)

    def refresh_weapon_num(self, percent=None):
        if not self.mecha:
            return
        else:
            skill_cost = self.mecha.ev_g_energy_cost(self.second_weapon_skill_id) or 1.0
            if percent is None:
                percent = self.mecha.ev_g_energy(self.second_weapon_skill_id)
            if not self.panel:
                return
            self.panel.prog.SetPercentage(percent * 100.0)
            show_num = int(percent / skill_cost)
            if show_num == self.show_num:
                return
            self.show_num = show_num
            self.panel.list_prog.SetInitCount(show_num)
            return

    def _on_continuous_shoot(self, sid):
        if not self.panel:
            return
        nd_aim_sec = self.panel.nd_aim_sec
        if not nd_aim_sec.isVisible():
            self.panel.PlayAnimation('show_sec')
        nd_aim_sec.stopActionByTag(self.ACTION_TAG)

        def _cb():
            if self.panel and self.panel.isValid():
                self.panel.PlayAnimation('disappear_sec')

        nd_aim_sec.SetTimeOut(1, _cb, tag=self.ACTION_TAG)

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if self.player:
            self.bind_ui_event(self.player)
        if global_data.player and self.player:
            if global_data.player.id != player.id:
                self.on_enter_observe(True)
            else:
                self.on_enter_observe(False)

    def bind_ui_event(self, target):
        pass

    def on_enter_observe(self, is_observe):
        self.panel.nd_prog.setVisible(not is_observe)