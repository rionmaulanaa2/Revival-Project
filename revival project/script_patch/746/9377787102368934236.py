# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewbiePassUI.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_const.scene_const import SCENE_NEWBIE_PASS, SCENE_JIEMIAN_COMMON
from logic.gcommon.common_const.battlepass_const import BATTLE_CARD_TYPE
from .NewbieAwardContentUI import NewbieAwardContentUI
from data.newbiepass_data import get_lv_reward, NEWBIEPASS_LV_CAP

class NewbiePassUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/new_pass_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': '_on_click_back_btn'
       }

    def show(self):
        self.clear_show_count_dict()
        self.hide_main_ui()
        self._sub_panel.show_init_state()

    def goto_reward_id_lv(self, reward_id):
        for lv in range(1, NEWBIEPASS_LV_CAP + 1):
            for pass_type in BATTLE_CARD_TYPE:
                reward_lv = get_lv_reward(str(pass_type), lv)
                if not reward_lv:
                    continue
                if isinstance(reward_lv, list):
                    reward_lst = reward_lv if 1 else [reward_lv]
                    for idx, reward_newbie in enumerate(reward_lst):
                        reward_conf = confmgr.get('common_reward_data', str(reward_newbie))
                        if not reward_conf:
                            continue
                        reward_list = reward_conf.get('reward_list', [])
                        item_no, _ = reward_list[0]
                        if str(reward_id) == str(item_no):
                            self._sub_panel.show_jump_state(lv, pass_type, idx, reward_newbie)
                            return True

        return False

    def on_init_panel(self):
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=SCENE_NEWBIE_PASS)
        self.disappearing = False
        self._sub_panel = NewbieAwardContentUI(self)
        self.hide_main_ui()

    def do_show_panel(self):
        super(NewbiePassUI, self).do_show_panel()
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=SCENE_NEWBIE_PASS)
        self._sub_panel.do_show_panel()

    def do_hide_panel(self):
        super(NewbiePassUI, self).do_hide_panel()
        self._sub_panel.do_hide_panel()
        self.disappearing = False

    def _on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()

    def on_finalize_panel(self):
        self.disappearing = False
        self._sub_panel.destroy()
        self._sub_panel = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        return

    def ui_vkb_custom_func(self):
        self._on_click_back_btn()