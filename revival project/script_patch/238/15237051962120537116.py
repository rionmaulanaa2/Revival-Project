# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleLeftBottomUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import time
import math
from common.const import uiconst

class BattleLeftBottomUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_left_bottom'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(BattleLeftBottomUI, self).on_init_panel()
        self.last_update_battery_time = 0
        self.init_status()
        self.init_network_widget()
        self.init_custom_com()
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.network_widget.destroy()
        self.network_widget = None
        self.destroy_widget('custom_ui_com')
        global_data.emgr.scene_camera_player_setted_event -= self.on_cam_lplayer_setted
        return

    def init_network_widget(self):
        from logic.comsys.battle.BattleInfo.NetworkWidget import NetworkWidget
        self.network_widget = NetworkWidget(self)

    def update_show(self):
        self.update_energy()
        self.update_position()

    def update_battery_show(self):
        self.panel.temp_title.bar_energy.setVisible(not global_data.is_pc_mode)

    def update_energy(self):
        import game3d
        from logic.gcommon import time_utility
        if not self or not self.is_valid():
            return
        if not global_data.is_pc_mode:
            cur_time = time.time()
            if cur_time - self.last_update_battery_time > 60:
                self.panel.temp_title.progress_energy.setPercent(game3d.get_battery_level())
                self.last_update_battery_time = cur_time
        if global_data.is_show_battery_current and hasattr(game3d, 'get_battery_current'):
            current_in_mA = int(game3d.get_battery_current())
            self.panel.temp_title.lab_time.SetString('{}mA'.format(current_in_mA))
        else:
            time_str = time_utility.get_time_string('%m%d %H:%M', time.time())
            time_zone = time_utility.get_timezone() / -3600
            if time_zone >= 0:
                time_str += '(UTC+%d)' % (time_utility.get_timezone() / -3600)
            else:
                time_str += '(UTC%d)' % (time_utility.get_timezone() / -3600)
            self.panel.temp_title.lab_time.SetString(time_str)

    def init_status(self):
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_show),
         cc.DelayTime.create(1.0)])))
        self.update_show()
        self.update_battery_show()

    def update_position(self):
        if global_data.cam_lctarget:
            pos = global_data.cam_lctarget.ev_g_position()
            if pos:
                self.panel.lab_position.setString('({:.0f}, {:.0f}, {:.0f})'.format(pos.x, pos.y, pos.z))

    def on_cam_lplayer_setted(self, *args):
        if global_data.cam_lplayer:
            obj = global_data.cam_lplayer.get_owner()
            if obj:
                try:
                    show_id = int(obj.uid)
                    if not G_IS_NA_USER:
                        show_id -= global_data.uid_prefix
                    self.panel.lab_player_id.SetString(str(show_id))
                except:
                    self.panel.lab_player_id.SetString(str(obj.uid))