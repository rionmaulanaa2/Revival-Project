# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/DeathModeAdvanceUI.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id

class DeathModeAdvanceUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/tdm_open_ad'
    APPEAR_ANIM = 'appear'
    LASTING_TIME = 0.5

    def get_close_node(self):
        return (
         self.panel.nd_close, self.panel.temp_btn_close.btn_back)

    def set_content(self):
        now_datetime = tutil.get_utc8_datetime()
        res_day = max(11 - now_datetime.day, 0)
        img_name = {3: ('img_3.png', 606066),
           2: ('img_2.png', 606066),
           1: ('img_1.png', 606067),
           0: ('img_go.png', 606065)
           }
        if res_day not in img_name:
            global_data.game_mgr.post_exec(self.close)
            return
        img_path = 'gui/ui_res_2/activity/activity_201907/' + img_name[res_day][0]
        self.panel.img_num.SetDisplayFrameByPath('', img_path)
        if res_day:
            self.panel.img_title.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/activity_201907/txt_tdm_view.png')
            self.panel.lab_describe.SetString(get_text_by_id(img_name[res_day][1]).format(num=res_day))
        else:
            self.panel.img_title.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/activity_201907/txt_tdm_open.png')
            self.panel.lab_describe.SetString(img_name[res_day][1])
            battle_opening, battle_count_down = global_data.player.get_open_state_count_down()
            from logic.gcommon.common_utils import battle_utils
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH, MATCH_DEATH, BATTLE_TYPE_COMPETITION
            battle_tid = battle_utils.get_battle_id_by_player_mode_and_type(PLAY_TYPE_DEATH, MATCH_DEATH, BATTLE_TYPE_COMPETITION)
            if battle_opening.get(battle_tid, False):
                self.btn_go.setVisible(True)

                @self.panel.btn_go.callback()
                def OnClick(*args):
                    if global_data.player:
                        global_data.player.clear_advance_sequence()
                    self.close()
                    ui = global_data.ui_mgr.get_ui('LobbyUI')
                    if ui:
                        ui.match_widget.on_click_mode_btn()
                        match_mode_ui = global_data.ui_mgr.get_ui('MatchMode')
                        if match_mode_ui:
                            match_mode_ui.try_to_choose_death_mode()