# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/AimLensUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import AIM_ZORDER, UI_TYPE_EFFECT
from common.utils.cocos_utils import ccc4, ccp
from logic.gcommon.common_const.weapon_const import LENS_RED_DOT, LENS_FOUR_MAGNITUDE, LENS_TWO_MAGNITUDE
from common.const import uiconst

class AimLensUI(BasePanel):
    PANEL_CONFIG_NAME = 'open_mirror'
    DLG_ZORDER = AIM_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT
    IS_FULLSCREEN = True

    def on_init_panel(self, magnification, open_time):
        self.len_magnification = magnification
        self.open_time = open_time
        self.init_event()
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.unregist_event(self.player)
        self.player = None
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        return

    def init_parameters(self):
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        self.ui_ready = False
        self.animation_callback = None
        self.move_tag = 0
        emgr = global_data.emgr
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self.on_player_setted(spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        return

    def unregist_event(self, player):
        if not (player and player.is_valid()):
            return
        unregister = player.unregist_event
        unregister('E_ATTACK_START', self.on_attack)
        unregister('E_ACTION_MOVE', self.on_move)
        unregister('E_ACTION_MOVE_STOP', self.on_move_stop)

    def regist_event(self, player):
        if not (player and player.is_valid()):
            self.animation_callback = None
            return
        else:
            register = player.regist_event
            register('E_ATTACK_START', self.on_attack)
            register('E_ACTION_MOVE', self.on_move)
            register('E_ACTION_MOVE_STOP', self.on_move_stop)
            return

    def on_player_setted(self, player):
        if self.player:
            self.unregist_event(self.player)
        self.player = player
        if player:
            self.regist_event(player)

    def on_attack(self, *args):
        self.panel.PlayAnimation('zoom_%d' % self.len_magnification)

    def on_move(self, *args):
        if self.ui_ready:
            self.move1()

    def on_move_stop(self, *args):
        self.animation_callback = None
        return

    def move1(self):
        if self.animation_callback:
            return
        self.panel.StopAnimation('shake_2')
        self.panel.PlayAnimation('shake_1')
        self.animation_callback = self.move2
        self.panel.SetTimeOut(0.8, self.move_callback, self.move_tag)

    def move2(self):
        self.panel.StopAnimation('shake_1')
        self.panel.PlayAnimation('shake_2')
        self.animation_callback = self.move1
        self.panel.SetTimeOut(1.2, self.move_callback, self.move_tag)

    def move_callback(self):
        if self.animation_callback:
            cb = self.animation_callback
            self.animation_callback = None
            cb()
        return

    def check_move(self):
        self.ui_ready = True
        if self.player and self.player.ev_g_is_move():
            self.on_move()

    def init_event(self):
        self.init_parameters()
        if not self.player:
            return
        len_attr_data = self.player.ev_g_attachment_attr(1)
        if len_attr_data:
            pic = self.get_weapon_lens_pic(len_attr_data.get('iType'))
        else:
            pic = self.get_weapon_lens_pic(LENS_TWO_MAGNITUDE)
        self.panel.sp_lens.SetDisplayFrameByPath('', pic)
        self.panel.sp_lens.setVisible(True)
        self.show_open_mirror_action()

        @self.panel.btn_close_mirror.callback()
        def OnClick(btn, touch):
            if self.player:
                self.player.send_event('E_QUIT_AIM')

    def get_weapon_lens_pic(self, len_type):
        lens_pic = {LENS_RED_DOT: 'gui/ui_res_2/battle/mirror/mirror_reddot.png',
           LENS_FOUR_MAGNITUDE: 'gui/ui_res_2/battle/mirror/mirror_4times.png',
           LENS_TWO_MAGNITUDE: 'gui/ui_res_2/battle/mirror/mirror_2times.png'
           }
        return lens_pic.get(len_type)

    def show_open_mirror_action(self):
        self.panel.sp_lens.setPosition(self.panel.nd_start_pos.getPosition())
        self.panel.sp_lens.setScale(0.1)
        self.panel.nd_len.stopAllActions()
        move_target = ccp(*self.panel.sp_lens.CalcPosition('50%', '50%'))
        self.panel.sp_lens.runAction(cc.Spawn.create([
         cc.ScaleTo.create(self.open_time, 0.8),
         cc.MoveTo.create(self.open_time, move_target)]))
        self.panel.SetTimeOut(self.open_time + 0.3, self.check_move)