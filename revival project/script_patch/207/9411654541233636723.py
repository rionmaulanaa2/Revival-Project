# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/FollowDropUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from data import hot_key_def
from common.const import uiconst

class FollowDropUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_before/fight_follow_info'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_leave.OnClick': 'on_click_leave'
       }
    ID_PIC_PATH = [
     'gui/ui_res_2/battle/icon/icon_teammate_num_blue.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_green.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_yellow.png',
     'gui/ui_res_2/battle/icon/icon_teammate_num_red.png']
    HOT_KEY_FUNC_MAP = {hot_key_def.CANCEL_FLLOW_DROP: 'keyboard_cancel_fllow_drop'
       }
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.CANCEL_FLLOW_DROP: {'node': 'temp_pc'}}

    def on_init_panel(self, *args):
        pass

    def on_finalize_panel(self):
        if global_data.player and global_data.player.logic and global_data.player.logic.is_valid():
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (None, ))
        return None

    def set_follow_info(self, lplayer):
        follow_target_id, c_name = lplayer.ev_g_parachute_follow_target(True)
        self.panel.lab_player_name.SetString(c_name)
        pic_id = lplayer.ev_g_parachute_follow_target_index()
        if pic_id is not None:
            self.panel.img_num.SetDisplayFrameByPath('', self.ID_PIC_PATH[pic_id])
        return

    def on_click_leave(self, *args):
        if global_data.player and global_data.player.logic and global_data.player.logic.is_valid():
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (None, ))
            global_data.player.logic.send_event('E_PARACHUTE_FOLLOW', False)
            self.close()
        return None

    def keyboard_cancel_fllow_drop(self, msg, keycode):
        self.on_click_leave()