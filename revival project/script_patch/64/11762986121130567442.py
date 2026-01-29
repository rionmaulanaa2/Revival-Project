# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaAccumulateUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.utils.timer import CLOCK
import common.cfg.confmgr as confmgr
import time
import common.utils.timer as timer
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
from common.const import uiconst

class MechaAccumulateUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        self.panel.PlayAnimation('cannon_show')
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        self.max_accumulate_time = None
        self.start_time = None
        self.timer = None
        self.is_full = False
        self.stage_level = 0
        emgr = global_data.emgr
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.on_observer_success_aim_event += self.close
        from logic.comsys.battle.AimColorWidget import AimColorWidget
        self._aimColorWidget = AimColorWidget(self, self.panel)
        self._aimColorWidget.set_top_color_exclude_list([])
        self._aimColorWidget.calculate_aim_node()
        return

    def on_player_setted(self, player):
        if player is None:
            self.close()
        return

    def set_weapon_id(self, weapon_type):
        self.panel.nd_cannon_progress.setVisible(True)
        self.accumulate_data = confmgr.get('accumulate_config', str(weapon_type), default=None)
        self.max_accumulate_time = self.accumulate_data['fEnergyCD_2']
        self.start_time = time.time()
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
        self.timer = global_data.game_mgr.register_logic_timer(self.tick, interval=1, times=-1, mode=timer.LOGIC)
        if self._aimColorWidget:
            self._aimColorWidget.setup_color()
        return

    def tick(self):
        cur_time = time.time() - self.start_time
        percent = int(cur_time * 100.0 / self.max_accumulate_time)
        percent /= 2
        if percent > 50:
            percent = 50
        self.panel.cannon_progress.SetPercentage(percent)
        if not self.is_full:
            if cur_time > self.accumulate_data['fEnergyCD_%d' % self.stage_level]:
                self.stage_level += 1
                if self.stage_level == 3:
                    self.is_full = True
                    self.panel.cannon_full.setVisible(True)
                    self.panel.PlayAnimation('cannon_power_full')

    def delay_close(self):
        self.panel.nd_cannon_progress.setVisible(False)
        self.panel.PlayAnimation('cannon_disappear')
        self.panel.SetTimeOut(0.5, self.close, 0)

    def on_finalize_panel(self):
        self.destroy_widget('_aimColorWidget')
        self.show_main_ui()
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
        emgr = global_data.emgr
        emgr.scene_player_setted_event -= self.on_player_setted
        return