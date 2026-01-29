# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaTestSightUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from data import camera_state_const
from common.const import uiconst

class MechaTestSightUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/test_mech_sight'
    DLG_ZORDER = UI_TYPE_MESSAGE - 1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'sight_button.OnClick': 'on_click_sight_btn'
       }

    def on_init_panel(self):
        self.panel.setLocalZOrder(self.DLG_ZORDER)
        self.init_parameters()
        global_data.melee_lock_camera = True
        self.panel.sight_button.SetSelect(global_data.melee_lock_camera)
        self.panel.label_state.SetString('\xe9\x94\x81\xe5\xae\x9a\xe8\xa7\x86\xe8\xa7\x92\xe6\xa8\xa1\xe5\xbc\x8f' if global_data.melee_lock_camera else '\xe8\x87\xaa\xe7\x94\xb1\xe8\xa7\x86\xe8\xa7\x92\xe6\xa8\xa1\xe5\xbc\x8f')

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        emgr = global_data.emgr
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)

    def on_mecha_setted(self, mecha):
        pass

    def on_player_setted(self, player):
        if not player:
            self.close()

    def on_click_sight_btn(self, *args):
        global_data.melee_lock_camera = not global_data.melee_lock_camera
        self.panel.sight_button.SetSelect(global_data.melee_lock_camera)
        self.panel.label_state.SetString('\xe9\x94\x81\xe5\xae\x9a\xe8\xa7\x86\xe8\xa7\x92\xe6\xa8\xa1\xe5\xbc\x8f' if global_data.melee_lock_camera else '\xe8\x87\xaa\xe7\x94\xb1\xe8\xa7\x86\xe8\xa7\x92\xe6\xa8\xa1\xe5\xbc\x8f')
        player = global_data.player
        if player and player.logic:
            player.logic.send_event('E_MECHA_CAMERA', camera_state_const.MELEE_MECHA_AIM_MODE if global_data.melee_lock_camera else camera_state_const.MELEE_MECHA_MODE)
            if global_data.melee_lock_camera and global_data.mecha:
                global_data.mecha.logic.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
                global_data.mecha.logic.send_event('E_CHANGE_SPEED')