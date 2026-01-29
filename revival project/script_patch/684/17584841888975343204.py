# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8025SecondAimUI.py
from __future__ import absolute_import
from six.moves import range
from .BaseMechaAimUI import BaseMechaAimUI
from logic.gcommon.const import PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from logic.gcommon.common_const.skill_const import SKILL_MISSILE_8025

class Mecha8025SecondAimUI(BaseMechaAimUI):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8025_2'
    WEAPON_INFO = {}

    def on_init_panel(self, *args, **kwargs):
        self.panel.list_bullet.SetInitCount(4)
        self.panel.nd_missile.setVisible(False)
        for group_bullet in self.panel.list_bullet.GetAllItem():
            group_bullet.list_bullet.SetInitCount(1)

        super(Mecha8025SecondAimUI, self).on_init_panel()
        self.init_auto_aim_widget()

    def init_parameters(self):
        self.second_aim_show = False
        self.last_valid_bullet_count = 0
        super(Mecha8025SecondAimUI, self).init_parameters()

    def init_aim_spread_mgr(self):
        pass

    def init_bullet_widget(self):
        pass

    def init_auto_aim_widget(self):

        def play_lock_sound_func():
            global_data.sound_mgr.post_event_2d('m_8025_missile_lock_1p', None)
            return

        from .MechaAutoAimWidget import MechaAutoAimWidget
        self.auto_aim_widget = MechaAutoAimWidget(self.panel, show_anim_name='', target_refreshed_anim_map={PART_WEAPON_POS_MAIN2: [ 'auto_sub_lock_%d' % i for i in range(1, 5) ],PART_WEAPON_POS_MAIN3: [ 'auto_sub_lock_%d' % i for i in range(1, 5) ]}, lock_count_refreshed_anim_map={PART_WEAPON_POS_MAIN2: [ 'auto_lock_number_%d' % i for i in range(1, 5) ],PART_WEAPON_POS_MAIN3: [ 'auto_lock_number_%d' % i for i in range(1, 5) ]}, play_lock_sound_func=play_lock_sound_func, need_play_lock_sound_map={PART_WEAPON_POS_MAIN2: True,
           PART_WEAPON_POS_MAIN3: True
           }, lock_node_map={PART_WEAPON_POS_MAIN2: [ getattr(self.panel, 'nd_sub_aim_lock_%d' % i) for i in range(1, 5) ],PART_WEAPON_POS_MAIN3: [ getattr(self.panel, 'nd_sub_aim_lock_%d' % i) for i in range(1, 5) ]}, reset_node_map={PART_WEAPON_POS_MAIN2: self.panel.img_aim1,
           PART_WEAPON_POS_MAIN3: self.panel.img_aim1
           }, lock_node_parent_map={PART_WEAPON_POS_MAIN2: self.panel.nd_sub_aim,
           PART_WEAPON_POS_MAIN3: self.panel.nd_sub_aim
           })

    def on_finalize_panel(self):
        super(Mecha8025SecondAimUI, self).on_finalize_panel()
        self.destroy_widget('auto_aim_widget')

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            regist_func('E_SET_MULTIPLE_AIM_TARGET_MAX_COUNT', self.update_valid_bullet_count)
            regist_func('E_ENERGY_CHANGE', self.on_energy_changed)
            self.auto_aim_widget and self.auto_aim_widget.on_mecha_set(mecha)
            self.last_valid_bullet_count = mecha.ev_g_skill_valid_cast_count(SKILL_MISSILE_8025)
            self.on_energy_changed(SKILL_MISSILE_8025, mecha.ev_g_energy(SKILL_MISSILE_8025))

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENABLE_WEAPON_AIM_HELPER', self.enable_weapon_aim_helper)
            unregist_func('E_SET_MULTIPLE_AIM_TARGET_MAX_COUNT', self.update_valid_bullet_count)
            unregist_func('E_ENERGY_CHANGE', self.on_energy_changed)
        self.mecha = None
        return

    def enable_weapon_aim_helper(self, enabled, weapon_pos):
        self.second_aim_show = enabled
        if enabled:
            self.panel.PlayAnimation('show_sub')
            self.panel.PlayAnimation('show_sub_auto')
            self.auto_aim_widget.refresh_auto_aim_parameters(weapon_pos)
            self.auto_aim_widget.update_aim_target(self.mecha.sd.ref_aim_targets.get(weapon_pos), weapon_pos)
        else:
            self.panel.PlayAnimation('disappear_sub')
            self.panel.PlayAnimation('disappear_sub_auto')
            self.auto_aim_widget.hide()
            self.auto_aim_widget.update_aim_target([], weapon_pos)

    def update_valid_bullet_count(self, weapon_pos, valid_bullet_count, force_update=False):
        self.panel.nd_missile.setVisible(bool(valid_bullet_count))
        self.panel.nd_missile.lab_num.SetString('x %d' % valid_bullet_count)

    def on_energy_changed(self, skill_id, mp_percent):
        if skill_id != SKILL_MISSILE_8025:
            return
        else:
            index, left, right = (0, 0, 0.25)
            cur_valid_count = -1
            while index < 4:
                cur_bullet_group = self.panel.list_bullet.GetItem(index).list_bullet
                if mp_percent >= right:
                    for bullet in cur_bullet_group.GetAllItem():
                        bullet.prog_bullet.SetPercent(100)

                    cur_valid_count = index
                elif mp_percent < left:
                    for bullet in cur_bullet_group.GetAllItem():
                        bullet.prog_bullet.SetPercent(0)

                else:
                    percent = (mp_percent - left) * 400
                    for bullet in cur_bullet_group.GetAllItem():
                        bullet.prog_bullet.SetPercent(percent)

                index += 1
                left += 0.25
                right += 0.25

            if cur_valid_count + 1 > self.last_valid_bullet_count:
                global_data.sound_mgr.post_event_2d('m_8025_missile_ready_1p', None)
            self.last_valid_bullet_count = cur_valid_count + 1
            return