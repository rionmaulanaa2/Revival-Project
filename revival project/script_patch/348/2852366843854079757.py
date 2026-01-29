# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeMiddleBulletWidgetUI.py
from __future__ import absolute_import
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gcommon.common_const import weapon_const
import math
from common.utils.cocos_utils import ccc4aFromHex
from common.uisys.color_table import get_color_val
from logic.gcommon.common_const.weapon_const import MAGAZINE_TYPE_NORMAL, ITEM_ID_LIMITED_BULLET, INIT_UZI_WEAPON_ID
BULLET_PROGRESS_PIC = [
 'gui/ui_res_2/battle/mech_attack/progress_bullet_white.png',
 'gui/ui_res_2/battle/mech_attack/progress_bullet_red.png']

class ScavengeMiddleBulletWidgetUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pick_up/fight_pick_bullet'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IS_FULLSCREEN = True
    GLOBAL_EVENT = {'on_carry_bullet_merged': 'show_carry_bullet_merged'
       }

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.cur_camera_state_type = None
        self.init_parameters()
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self.aim_spread_mgr = None
        self.bullet_widget = None
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'on_observer_weapon_bullet_num_changed': self.on_weapon_bullet_num_changed
           }
        emgr.bind_events(econf)
        return

    def bind_ui_event(self, target):
        target.regist_event('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
        target.regist_event('E_REFRESH_CUR_WEAPON_BULLET', self.weapon_data_changed)
        target.regist_event('E_WPBAR_SWITCHED', self.weapon_data_changed)
        target.regist_event('E_SWITCHED_WP_MODE', self.weapon_data_changed)
        cur_wp = None
        if global_data.player and global_data.player.logic:
            cur_wp = global_data.player.logic.ev_g_wpbar_cur_weapon()
        self.update_bullet_info(cur_wp)
        if global_data.player and global_data.player.logic:
            cur_weapon = global_data.player.logic.ev_g_wpbar_cur_weapon()
            if cur_weapon and cur_weapon.is_multi_wp():
                global_data.player.logic.send_event('E_SWITCH_WEAPON_MODE')
        return

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            target.unregist_event('E_WEAPON_DATA_CHANGED', self.weapon_data_changed)
            target.unregist_event('E_REFRESH_CUR_WEAPON_BULLET', self.weapon_data_changed)
            target.unregist_event('E_WPBAR_SWITCHED', self.weapon_data_changed)
            target.unregist_event('E_SWITCHED_WP_MODE', self.weapon_data_changed)

    def on_finalize_panel(self):
        self.player = None
        self.mecha = None
        return

    def disappear(self):
        if self.panel.HasAnimation('disappear'):
            self.panel.PlayAnimation('disappear')
            delay = self.panel.GetAnimationMaxRunTime('disappear')
            self.panel.SetTimeOut(delay, lambda : self.close())
        else:
            self.close()

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.player = player
        self.unbind_ui_event(player)
        if self.player:
            self.bind_ui_event(self.player)
            if global_data.player.id != player.id:
                self.on_enter_observe(True)
            else:
                self.on_enter_observe(False)
        if global_data.cam_data:
            self.on_camera_switch_to_state(global_data.cam_data.camera_state_type)

    def on_enter_observe(self, is_observe):
        if not self.panel.nd_bullet_ob:
            return
        if is_observe:
            self.panel.nd_bullet_ob.setVisible(False)
        else:
            self.panel.nd_bullet_ob.setVisible(True)

    def weapon_data_changed(self, pos, *args):
        if not self.player:
            return
        self.on_weapon_bullet_num_changed(pos)

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')
        from logic.client.const import camera_const
        if state == camera_const.AIM_MODE:
            self.add_hide_count('AIM_CAMERA')
        elif self.cur_camera_state_type == camera_const.AIM_MODE and state != camera_const.AIM_MODE:
            self.add_show_count('AIM_CAMERA')
        self.cur_camera_state_type = state

    def on_weapon_bullet_num_changed(self, pos_or_pos_list):
        weapon_object = self.player.share_data.ref_wp_bar_cur_weapon if self.player else None
        if weapon_object:
            self.update_bullet_info(weapon_object)
        return

    def format_num(self, num):
        if num < 10:
            return '0{}'.format(num)
        else:
            if num < 100:
                return '{}'.format(num)
            return str(num)

    def update_bullet_info(self, wp):
        self.bullet_ui = self.panel.nd_bullet_ob.nd_bullet.temp_bullet
        progress_bullet = self.bullet_ui.progress_bullet
        lab_bullet_num = self.bullet_ui.lab_bullet_num
        lab_bullet_full = self.bullet_ui.lab_bullet_full
        if not wp:
            lab_bullet_num.SetString('- ')
            lab_bullet_full.SetString('/ -')
            return
        show_ratio = wp.get_show_ratio()
        bullet_cap = wp.get_bullet_cap()
        weapon_data = wp.get_data()
        cur_bullet_num = weapon_data.get('iBulletNum', 0)
        cur_carry_bullet_num = wp.get_carry_bullet_num()
        bullet_color = False
        if 1 <= cur_bullet_num < math.ceil(bullet_cap * 0.4):
            bullet_color = True
        elif cur_bullet_num < 1:
            bullet_color = True
        if bullet_color:
            lab_bullet_num.EnableOutline(ccc4aFromHex(4278190080L + get_color_val('#BR')), 2)
            progress_bullet and progress_bullet.SetProgressTexture(BULLET_PROGRESS_PIC[1])
        else:
            lab_bullet_num.disableEffect()
            progress_bullet and progress_bullet.SetProgressTexture(BULLET_PROGRESS_PIC[0])
        if bullet_cap > 0:
            percent = 100.0 * cur_bullet_num / bullet_cap
        else:
            percent = 0.0
        progress_bullet and progress_bullet.SetPercentage(percent)
        lab_bullet_num.SetString(self.format_num(int(cur_bullet_num * show_ratio)))
        if wp.get_bullet_type() == ITEM_ID_LIMITED_BULLET:
            lab_bullet_full.SetString('/%s' % self.format_num(int(cur_carry_bullet_num * show_ratio)))
        else:
            lab_bullet_full.SetString('/ -')

    def show_carry_bullet_merged(self, add_num):
        bullet_panel = self.panel.nd_bullet_ob.nd_bullet.temp_bullet
        bullet_panel.nd_bullet_ob.vx_bullet_add.lab_bullet_add.setString('+%d' % add_num)
        bullet_panel.PlayAnimation('bullet_add')