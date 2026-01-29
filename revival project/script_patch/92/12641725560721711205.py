# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaBulletWidget.py
from __future__ import absolute_import
import six
import cc
from common.utils.cocos_utils import ccc4aFromHex
from common.uisys.color_table import get_color_val
MAIN_WEAPON = ''
SUB_WEAPON = 'sub_'
SP_WEAPON = 'sp_'
BULLET_PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_bullet_white.png',
 'gui/ui_res_2/battle/mech_attack/progress_bullet_red.png']
ENERGY_BULLET_TYPE_MECHA_IDS = {
 8002}

class BaseBulletWidget(object):

    def __init__(self, parent, weapon_info):
        self.panel = parent
        self.weapon_info = weapon_info
        self.init_parameters()
        self.init_event()
        self.start_bullet_detect()

    def destroy(self):
        self.mecha = None
        self._bullet_action and self.panel.stopAction(self._bullet_action)
        self._bullet_action = None
        return

    def init_parameters(self):
        self.mecha = None
        self.last_bullet_num = {}
        self.cur_weapon_pos = None
        self.nochange = {}
        self.is_bullet_decreasing = {}
        for weapon_key in six.iterkeys(self.weapon_info):
            weapon_type = self.weapon_info[weapon_key]
            temp_bullet = getattr(self.panel, 'temp_%sbullet' % weapon_type)
            temp_bullet.RecordAnimationNodeState('bullet_decrease')
            temp_bullet.RecordAnimationNodeState('bullet_low')
            self.last_bullet_num[weapon_key] = (0, 0)
            self.nochange[weapon_key] = 0
            self.is_bullet_decreasing[weapon_key] = False

        self._bullet_action = None
        return

    def init_event(self):
        pass

    def on_mecha_setted(self, mecha):
        self.show_nd_bullet(True)

    def show_nd_bullet(self, show):
        if not self.panel.nd_bullet:
            return
        is_in_island = global_data.battle and global_data.battle.is_in_island()
        if is_in_island:
            self.panel.nd_bullet.setVisible(False)
            self.panel.nd_bullet_ob and self.panel.nd_bullet_ob.setVisible(False)
        else:
            self.panel.nd_bullet.setVisible(show)

    def unbind_ui_event(self):
        pass

    def format_num(self, num):
        if num < 10:
            return '0{}'.format(num)
        else:
            if num < 100:
                return '{}'.format(num)
            return str(num)

    def bullet_show(self, weapon_key, cur_bullet, bullet_cap, show_ani=True):
        weapon_type = self.weapon_info[weapon_key]
        if self.last_bullet_num[weapon_key][0] > cur_bullet:
            self.nochange[weapon_key] = 0
        temp_bullet = getattr(self.panel, 'temp_%sbullet' % weapon_type)
        progress_bullet = temp_bullet.progress_bullet
        lab_bullet_num = temp_bullet.lab_bullet_num
        lab_bullet_full = temp_bullet.lab_bullet_full
        bar_bullet_vx = temp_bullet.bar_bullet_vx
        bullet_low_ani = 'bullet_low'
        if bullet_cap == 0:
            bar_bullet_vx.setVisible(False)
            progress_bullet and progress_bullet.SetProgressTexture(BULLET_PROGRESS_PIC[0])
            progress_bullet and progress_bullet.SetPercentageWithAni(100.0, 0.1)
        else:
            lab_bullet_num.SetString(self.format_num(cur_bullet))
            if bullet_cap > 1:
                min_bullet_num = int(bullet_cap * 0.2) + 1
            else:
                min_bullet_num = 0
            if cur_bullet <= min_bullet_num and not temp_bullet.IsPlayingAnimation(bullet_low_ani) and self.last_bullet_num[weapon_key][0] > cur_bullet and show_ani:
                temp_bullet.PlayAnimation(bullet_low_ani)
            else:
                temp_bullet.StopAnimation(bullet_low_ani)
                temp_bullet.RecoverAnimationNodeState(bullet_low_ani)
            if cur_bullet <= min_bullet_num:
                lab_bullet_num.EnableOutline(ccc4aFromHex(4278190080L + get_color_val('#BR')), 2)
                if show_ani:
                    bar_bullet_vx.setVisible(True)
                progress_bullet and progress_bullet.SetProgressTexture(BULLET_PROGRESS_PIC[1])
            else:
                lab_bullet_num.disableEffect()
                if show_ani:
                    bar_bullet_vx.setVisible(False)
                progress_bullet and progress_bullet.SetProgressTexture(BULLET_PROGRESS_PIC[0])
            last_progress = 100.0 * self.last_bullet_num[weapon_key][0] / bullet_cap
            cur_progress = 100.0 * cur_bullet / bullet_cap
            time = 0
            if last_progress - cur_progress > 0:
                time = min(int(last_progress - cur_progress) / 10 * 1.0, 0.1)
            progress_bullet and progress_bullet.SetPercentageWithAni(cur_progress, time)
            lab_bullet_full.SetString('/%s' % self.format_num(bullet_cap))
        self.last_bullet_num[weapon_key] = (cur_bullet, bullet_cap)

    def start_bullet_detect(self):
        if self._bullet_action:
            return
        self._bullet_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.detect_bullet),
         cc.DelayTime.create(0.05)])))

    def detect_bullet(self, *args):
        for weapon_key in six.iterkeys(self.weapon_info):
            weapon_type = self.weapon_info[weapon_key]
            self.nochange[weapon_key] += 0.05
            temp_bullet = getattr(self.panel, 'temp_%sbullet' % weapon_type)
            if self.nochange[weapon_key] >= 0.3 and self.is_bullet_decreasing[weapon_key]:
                temp_bullet.StopAnimation('bullet_decrease')
                is_showing_inf = not temp_bullet.lab_bullet_num.isVisible()
                temp_bullet.RecoverAnimationNodeState('bullet_decrease')
                if is_showing_inf:
                    temp_bullet.lab_bullet_num.setVisible(False)
                    temp_bullet.lab_bullet_full.setVisible(False)
                temp_bullet.lab_bullet_num.setOpacity(255)
                temp_bullet.img_bullet and temp_bullet.img_bullet.setOpacity(255)
                self.is_bullet_decreasing[weapon_key] = False
            elif self.nochange[weapon_key] < 0.3 and not self.is_bullet_decreasing[weapon_key]:
                temp_bullet.PlayAnimation('bullet_decrease')
                self.is_bullet_decreasing[weapon_key] = True


class MechaBulletWidget(BaseBulletWidget):

    def init_event(self):
        if not self.mecha:
            return
        for weapon_key in six.iterkeys(self.weapon_info):
            weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_key)
            if weapon:
                self.last_bullet_num[weapon_key] = (
                 weapon.get_bullet_cap(), weapon.get_bullet_cap())
                self.weapon_bullet_changed(weapon_key, is_force=True)
                if self.mecha:
                    cur_bullet = weapon.get_bullet_num()
                    if cur_bullet <= 0:
                        self.mecha.send_event('E_TRY_RELOAD', weapon_key)

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event()
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            regist_func('E_REFRESH_CUR_WEAPON_BULLET', self.refresh_cur_weapon_bullet)
            self.init_event()
            mecha.send_event('E_REFRESH_WEAPON_DATA')
        super(MechaBulletWidget, self).on_mecha_setted(mecha)

    def unbind_ui_event(self):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            unregist_func('E_REFRESH_CUR_WEAPON_BULLET', self.refresh_cur_weapon_bullet)
        self.mecha = None
        return

    def weapon_data_changed(self, pos, *args):
        if not self.mecha:
            return
        self.weapon_bullet_changed(pos)

    def refresh_cur_weapon_bullet(self, pos):
        if not self.mecha:
            return
        self.cur_weapon_pos = pos
        self.weapon_bullet_changed(pos, True, True)

    def check_nd_inf_bullet_refreshed(self, weapon_key, bullet_cap):
        temp_bullet = getattr(self.panel, 'temp_%sbullet' % self.weapon_info[weapon_key])
        not_inf = bool(bullet_cap)
        temp_bullet.lab_bullet_num.setVisible(not_inf)
        temp_bullet.lab_bullet_full.setVisible(not_inf)
        temp_bullet.lab_bullet_inf and temp_bullet.lab_bullet_inf.setVisible(not not_inf)

    def weapon_bullet_changed(self, weapon_key, is_force=False, check_inf_bullet=False):
        if weapon_key not in self.weapon_info:
            return
        else:
            weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_key)
            cur_bullet = weapon.get_bullet_num()
            bullet_cap = weapon.get_bullet_cap()
            if self.last_bullet_num[weapon_key] == (cur_bullet, bullet_cap) and not is_force:
                return
            if self.cur_weapon_pos is not None and weapon_key != self.cur_weapon_pos:
                return
            show_ratio = weapon.get_show_ratio()
            cur_bullet = int(cur_bullet * show_ratio)
            bullet_cap = int(bullet_cap * show_ratio)
            check_inf_bullet and self.check_nd_inf_bullet_refreshed(weapon_key, bullet_cap)
            self.bullet_show(weapon_key, cur_bullet, bullet_cap)
            return


class MechaEnergyWidget(BaseBulletWidget):

    def init_parameters(self):
        super(MechaEnergyWidget, self).init_parameters()
        self.skill_to_weapon = {}
        self.show_ani = True

    def init_event(self):
        if not self.mecha:
            return
        self.skill_to_weapon = {}
        behavior = self.mecha.ev_g_behavior_config()
        for weapon_key in six.iterkeys(self.weapon_info):
            skill_id = behavior[weapon_key]['custom_param']['skill_id']
            self.skill_to_weapon[skill_id] = weapon_key
            cur_bullet = self.mecha.ev_g_energy_segment(skill_id)
            self.last_bullet_num[weapon_key] = (cur_bullet, cur_bullet)
            self.weapon_energy_changed(weapon_key, is_force=True)

    def on_mecha_setted(self, mecha, show_ani=True):
        if self.mecha:
            self.unbind_ui_event()
        if mecha:
            self.mecha = mecha
            self.show_ani = show_ani
            regist_func = mecha.regist_event
            regist_func('E_ENERGY_CHANGE', self.on_energy_change)
            self.init_event()
        super(MechaEnergyWidget, self).on_mecha_setted(mecha)

    def unbind_ui_event(self):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_ENERGY_CHANGE', self.on_energy_change)
        self.mecha = None
        return

    def on_energy_change(self, skill_id, percent):
        if skill_id in self.skill_to_weapon:
            self.weapon_energy_changed(self.skill_to_weapon[skill_id])

    def weapon_energy_changed(self, weapon_key, is_force=False):
        if not (self.mecha and self.mecha.is_valid()):
            return
        if weapon_key not in self.weapon_info:
            return
        behavior = self.mecha.ev_g_behavior_config()
        skill_id = behavior[weapon_key]['custom_param']['skill_id']
        cur_energy = self.mecha.ev_g_energy(skill_id)
        skill_cost = self.mecha.ev_g_energy_cost(skill_id) or 1.0
        cur_bullet = int(cur_energy / skill_cost)
        bullet_cap = self.mecha.ev_g_energy_segment(skill_id)
        if self.last_bullet_num[weapon_key] == (cur_bullet, bullet_cap) and not is_force:
            return
        bullet_cap = self.mecha.ev_g_energy_segment(skill_id)
        self.bullet_show(weapon_key, cur_bullet, bullet_cap, self.show_ani)


class MechaBulletWidgetPC(MechaBulletWidget):

    def init_parameters(self):
        self.mecha = None
        self.last_bullet_num = {}
        self.cur_weapon_pos = None
        self.nochange = {}
        self.is_bullet_decreasing = {}
        for weapon_key in six.iterkeys(self.weapon_info):
            self.last_bullet_num[weapon_key] = (0, 0)
            self.nochange[weapon_key] = 0
            self.is_bullet_decreasing[weapon_key] = False

        self._bullet_action = None
        return

    def bullet_show(self, weapon_key, cur_bullet, bullet_cap, show_ani=True):
        weapon_type = self.weapon_info[weapon_key]
        temp_bullet = getattr(self.panel, 'nd_%sbullet' % weapon_type)
        if temp_bullet is None:
            return
        else:
            if bullet_cap:
                temp_bullet.lab_bullet_num.SetString(self.format_num(cur_bullet))
                temp_bullet.lab_bullet_full.SetString('/%s' % self.format_num(bullet_cap))
                self.panel.PlayAnimation('bullet_low')
            return

    def weapon_bullet_changed(self, weapon_key, is_force=False, check_inf_bullet=False):
        if weapon_key not in self.weapon_info:
            return
        else:
            weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(weapon_key)
            cur_bullet = weapon.get_bullet_num()
            bullet_cap = weapon.get_bullet_cap()
            if self.cur_weapon_pos is not None and weapon_key != self.cur_weapon_pos:
                return
            show_ratio = weapon.get_show_ratio()
            cur_bullet = int(cur_bullet * show_ratio)
            bullet_cap = int(bullet_cap * show_ratio)
            check_inf_bullet and self.check_nd_inf_bullet_refreshed(weapon_key, bullet_cap)
            self.bullet_show(weapon_key, cur_bullet, bullet_cap)
            return

    def start_bullet_detect(self):
        pass

    def show_nd_sp_bullet(self, show):
        if not self.panel.nd_sp_bullet:
            return
        is_in_island = global_data.battle and global_data.battle.is_in_island()
        if is_in_island:
            self.panel.nd_sp_bullet.setVisible(False)
        else:
            self.panel.nd_sp_bullet.setVisible(show)

    def switch_bullet_widget(self, is_switch):
        self.show_nd_bullet(not bool(is_switch))
        self.show_nd_sp_bullet(bool(is_switch))

    def check_nd_inf_bullet_refreshed(self, weapon_key, bullet_cap):
        temp_bullet = self.panel.nd_bullet
        not_inf = bool(bullet_cap)
        temp_bullet.lab_bullet_num.setVisible(not_inf)
        temp_bullet.lab_bullet_full.setVisible(not_inf)
        temp_bullet.lab_bullet_inf and temp_bullet.lab_bullet_inf.setVisible(not not_inf)


class MechaEnergyWidgetPC(MechaEnergyWidget):

    def init_parameters(self):
        self.mecha = None
        self.last_bullet_num = {}
        self.cur_weapon_pos = None
        self.nochange = {}
        self.is_bullet_decreasing = {}
        for weapon_key in six.iterkeys(self.weapon_info):
            self.last_bullet_num[weapon_key] = (0, 0)
            self.nochange[weapon_key] = 0
            self.is_bullet_decreasing[weapon_key] = False

        self._bullet_action = None
        self.skill_to_weapon = {}
        self.show_ani = True
        return

    def weapon_energy_changed(self, weapon_key, is_force=False):
        if not (self.mecha and self.mecha.is_valid()):
            return
        if weapon_key not in self.weapon_info:
            return
        behavior = self.mecha.ev_g_behavior_config()
        skill_id = behavior[weapon_key]['custom_param']['skill_id']
        cur_energy = self.mecha.ev_g_energy(skill_id)
        skill_cost = self.mecha.ev_g_energy_cost(skill_id) or 1.0
        cur_bullet = int(cur_energy / skill_cost)
        bullet_cap = self.mecha.ev_g_energy_segment(skill_id)
        self.bullet_show(weapon_key, cur_bullet, bullet_cap, self.show_ani)

    def bullet_show(self, weapon_key, cur_bullet, bullet_cap, show_ani=True):
        self.panel.nd_bullet.lab_bullet_num.SetString(self.format_num(cur_bullet))
        if bullet_cap:
            self.panel.nd_bullet.lab_bullet_full.SetString('/%s' % self.format_num(bullet_cap))
        self.panel.PlayAnimation('bullet_low')

    def start_bullet_detect(self):
        pass