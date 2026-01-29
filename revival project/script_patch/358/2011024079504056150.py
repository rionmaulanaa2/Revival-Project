# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8501AimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
import logic.gcommon.const as g_const
from common.cfg import confmgr
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
import cc
import math
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
from common.const import uiconst

class Mecha8501AimUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_chicken'
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True
    AUTO_AIM_SIZE = 60.0

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_event()
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        from logic.comsys.battle.AimColorWidget import AimColorWidget
        self._aimColorWidget = AimColorWidget(self, self.panel)
        self._aimColorWidget.set_top_color_exclude_list([self.panel.nd_bullet])
        self._aimColorWidget.calculate_aim_node()

    def on_finalize_panel(self):
        self.destroy_widget('_aimColorWidget')
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.cur_bullet = 0
        self.last_bullet_num = 0
        self.weapon_pos = g_const.PART_WEAPON_POS_MAIN1
        width, height = self.panel.GetContentSize()
        x_fov = confmgr.get('camera_config', THIRD_PERSON_MODEL, POSTURE_STAND, 'fov', default=80)
        d = width / 2.0 / math.tan(math.radians(x_fov / 2.0))
        cell = 30
        y_fov = math.atan(cell / 2.0 / d) * 180 / math.pi * 2.0
        self._scale_value = cell / y_fov
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def init_event(self):
        if not self.mecha:
            return
        self.refresh_bullet_num()

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
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            regist_func('E_AIM_SPREAD', self._on_aim_spread)
            regist_func('E_STAND', self._on_spread, 1)
            regist_func('E_JUMP', self._on_spread, 1)
            regist_func('E_MECHA_ON_GROUND', self._on_spread, 1)
            regist_func('E_ACTION_MOVE', self._on_spread, 1)
            regist_func('E_ACTION_MOVE_STOP', self._on_spread, 1)
            self.init_event()
            self._on_spread()
            if self._aimColorWidget:
                self._aimColorWidget.setup_color()

    def bind_ui_event(self, target):
        pass

    def unbind_ui_event(self, target):
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            unregist_func('E_AIM_SPREAD', self._on_aim_spread)
            unregist_func('E_STAND', self._on_spread)
            unregist_func('E_JUMP', self._on_spread)
            unregist_func('E_MECHA_ON_GROUND', self._on_spread)
            unregist_func('E_ACTION_MOVE', self._on_spread)
            unregist_func('E_ACTION_MOVE_STOP', self._on_spread)
        self.mecha = None
        return

    def show_reload_ui(self, flag):
        self.panel.nd_aim.setVisible(flag)

    def format_num(self, num):
        if num < 10:
            return '0{}'.format(num)
        else:
            if num < 100:
                return '{}'.format(num)
            return str(num)

    def refresh_bullet_num(self):
        weapon = self.mecha.share_data.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return
        cur_bullet = weapon.get_bullet_num()
        bullet_cap = weapon.get_bullet_cap()
        self.panel.lab_bullet_num.SetString(self.format_num(cur_bullet))
        if bullet_cap <= 5:
            self.panel.lab_bullet_num.SetColor('#DB')
        elif cur_bullet <= 5 and bullet_cap > 5:
            self.panel.lab_bullet_num.SetColor('#DR')
        else:
            self.panel.lab_bullet_num.SetColor('#DB')
        self.cur_bullet = cur_bullet

    def weapon_data_changed(self, pos, *args):
        if not self.mecha:
            return
        self.refresh_bullet_num()

    def on_enter_observe(self, is_observe):
        pass

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _on_spread(self, *args):
        if not self.mecha or not self.panel.aim_circle or not self.panel.aim_circle.isVisible():
            return
        spread_values = self.mecha.get_value('G_SPREAD_VALUES')
        if not spread_values:
            return
        spread_base, spread_value, recover_time = spread_values
        if spread_value < 0.01:
            return
        aim_circle = self.panel.aim_circle
        scale_value = self._scale_value * 2.0 / self.AUTO_AIM_SIZE
        aim_circle.setScale(scale_value * spread_value)
        aim_circle.stopAllActions()
        aim_circle.runAction(cc.Sequence.create([
         cc.ScaleTo.create(0.1, scale_value * spread_value),
         cc.ScaleTo.create(0.1, scale_value * spread_base)]))

    def _on_aim_spread(self, _spread_base, _spread_value, delay_time, _recover_time, weapon_pos=None):
        if not self.mecha or not self.panel.aim_circle or not self.panel.aim_circle.isVisible():
            return
        spread_values = self.mecha.get_value('G_SPREAD_VALUES')
        if not spread_values:
            return
        spread_base, spread_value, recover_time = spread_values
        if spread_value < 0.01:
            return
        aim_circle = self.panel.aim_circle
        scale_value = self._scale_value * 2.0 / self.AUTO_AIM_SIZE
        aim_circle.setScale(scale_value * spread_value)
        aim_circle.stopAllActions()
        aim_circle.runAction(cc.Sequence.create([
         cc.DelayTime.create(delay_time),
         cc.ScaleTo.create(0.1, scale_value * spread_base)]))