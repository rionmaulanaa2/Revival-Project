# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/HidingUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst

class HidingUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/hiding_control'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'control.btn_leave.OnClick': 'on_leave_hiding'
       }
    ASSOCIATE_UI_LIST = [
     'FireRockerUI', 'MoveRockerUI', 'ThrowRockerUI', 'FrontSightUI', 'SceneInteractionUI', 'FightLeftShotUI', 'BulletReloadUI']

    def on_init_panel(self, *args, **kargs):
        self.hide_main_ui(ui_list=HidingUI.ASSOCIATE_UI_LIST)

    def on_leave_hiding(self, *args):
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        if player:
            player.send_event('E_REQ_LEAVE_HIDING')

    def on_finalize_panel(self):
        self.show_main_ui()