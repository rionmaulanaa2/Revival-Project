# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothOccupyProgressUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
PROGRESS_PATH = [
 'gui/ui_res_2/battle/koth/progress_koth_blue.png',
 'gui/ui_res_2/battle/koth/progresskoth_red.png',
 'gui/ui_res_2/battle/koth/progress_koth_purple.png']
SIDE_COLOR = [
 '#SB', '#SR', '#DP']
from common.const import uiconst
SIDE_TEXT = [
 8002, 8003, 8004]

class KothOccupyProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/koth_occupy_progress'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.sound_id = None
        return

    def on_finalize_panel(self):
        self.stop_sound()

    def stop_sound(self):
        if self.sound_id is not None:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        return

    def set_occupy_info(self, faction_id, from_progress, to_progress, duration, speed):
        if from_progress == to_progress:
            self.end_occupy_progress()
            return
        else:
            if self.sound_id is None:
                self.sound_id = global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                                       'aim_missiles'))

            def progress_end():
                if to_progress >= 100:
                    self.end_occupy_progress()

            self.show()
            show_side = global_data.king_battle_data.get_side_by_faction_id(faction_id)
            if show_side < len(PROGRESS_PATH):
                progress_pic = PROGRESS_PATH[show_side]
                self.panel.progress.SetPath('', progress_pic)
            if from_progress is not None and abs(self.panel.progress.getPercent() - from_progress) > 20:
                self.panel.progress.SetPercent(from_progress)
            self.panel.progress.SetPercent(to_progress, duration, end_cb=progress_end)
            if speed is not None:
                self.panel.list_speed.SetInitCount(int(speed))
            color_str = SIDE_COLOR[show_side]
            if show_side == 0:
                self.panel.lab_ocupy.setString(get_text_by_id(8100))
            else:
                from common.uisys.uielment.CCRichText import format_richtext
                text = format_richtext(color_str + get_text_by_id(8101, {'side': get_text_by_id(SIDE_TEXT[show_side])}))
                self.panel.lab_ocupy.setString(text)
            return

    def end_occupy_progress(self):
        self.stop_sound()
        if self.check_can_hide_count(self.__class__.__name__):
            self.hide()