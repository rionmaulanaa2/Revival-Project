# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartGVGChooseMecha.py
from __future__ import absolute_import
from . import ScenePart
from common.utils import timer
from common.const.uiconst import UI_TYPE_CONFIRM
from logic.client.const import game_mode_const

class PartGVGChooseMecha(ScenePart.ScenePart):
    INIT_EVENT = {'enter_choose_mecha': 'init_choose_mecha_ui',
       'choose_mecha_finished': 'choose_mecha_finished',
       'enter_ready_confirm': 'enter_ready_confirm'
       }

    def __init__(self, scene, name):
        super(PartGVGChooseMecha, self).__init__(scene, name, False)
        self.gvg_ready_timer = None
        self.choose_finished_timer = None
        return

    def clear_gvg_ready_timer(self):
        self.gvg_ready_timer and global_data.game_mgr.get_logic_timer().unregister(self.gvg_ready_timer)
        self.gvg_ready_timer = None
        return

    def clear_choose_finished_timer(self):
        self.choose_finished_timer and global_data.game_mgr.get_logic_timer().unregister(self.choose_finished_timer)
        self.choose_finished_timer = None
        return

    def init_choose_mecha_ui(self, game_mode_type=game_mode_const.GAME_MODE_GVG):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        ui = global_data.ui_mgr.get_ui('GVGReadyUI')

        def _show_ui():
            global_data.ui_mgr.close_ui('JudgeLoadingUI')
            if game_mode_type == game_mode_const.GAME_MODE_DUEL:
                ui = global_data.ui_mgr.show_ui('DuelChooseMecha', 'logic.comsys.battle.Duel')
                ui.enter_choose_mecha()
            else:
                ui = global_data.ui_mgr.show_ui('GVGChooseMecha', 'logic.comsys.battle.gvg')
                ui.enter_choose_mecha()
            self.choose_mecha_finished()

        if ui:
            ui.delay_close()
            self.clear_gvg_ready_timer()
            self.gvg_ready_timer = global_data.game_mgr.get_logic_timer().register(func=lambda : _show_ui(), mode=timer.CLOCK, interval=0.5, times=1)
        else:
            _show_ui()

    def choose_mecha_finished(self):
        bat = global_data.battle
        if bat and bat.choose_finished:
            global_data.emgr.gvg_enter_battle.emit()

    def enter_ready_confirm(self, confirm_end_ts):
        from data.vibrate_key_def import GVG_READY_VIBRATE_LV
        if not global_data.vibrate_mgr:
            from logic.comsys.vibrate.VibrateMgr import VibrateMgr
            VibrateMgr()
        global_data.vibrate_mgr.start_vibrate(GVG_READY_VIBRATE_LV)
        ui = global_data.ui_mgr.show_ui('GVGReadyUI', 'logic.comsys.battle.gvg')
        ui.refresh_data()
        ui.on_count_down(confirm_end_ts)

    def on_exit(self):
        pass