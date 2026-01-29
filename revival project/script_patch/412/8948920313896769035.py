# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/privilege/PrivilegeLevelupUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER_2, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL

class PrivilegeLevelupUI(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charge_level_up'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    RECREATE_WHEN_RESOLUTION_CHANGE = True

    def on_init_panel(self):
        if global_data.player:
            priv_lv = global_data.player.get_privilege_level()
        else:
            priv_lv = 0
        self.init_privilege_level(priv_lv)
        self.init_btn_event()
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('show_btn_2')

    def init_privilege_level(self, priv_lv):
        if priv_lv <= 0:
            return
        frame_pic = PRIVILEGE_BAR_BADGE_FRAME[priv_lv]
        level_pic = PRIVILEGE_BAR_BADGE_LEVEL[priv_lv]
        self.panel.bar_level.SetDisplayFrameByPath('', frame_pic)
        self.panel.img_level_now.SetDisplayFrameByPath('', level_pic)

    def init_btn_event(self):

        @self.panel.temp_btn_close.btn_common_big.unique_callback()
        def OnClick(*args):
            self.close()

        @self.panel.temp_btn_go.btn_common_big.unique_callback()
        def OnClick(*args):
            from logic.client.const import game_mode_const
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
                global_data.game_mgr.show_tip(get_text_by_id(83203))
                return
            from logic.gutils.jump_to_ui_utils import jump_to_charge
            from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_PRIVILEGE_TYPE
            jump_to_charge(ACTIVITY_PRIVILEGE_TYPE)
            self.close()

    def close(self, *args):
        super(PrivilegeLevelupUI, self).close(*args)
        global_data.player and global_data.player.try_notify_privilege_max_lv()