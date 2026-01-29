# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleFightMeow.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER_1
from logic.gcommon.cdata import driver_lv_data
from logic.gcommon.common_const import battle_const
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.const import uiconst

class BattleFightMeowBase(MechaDistortHelper, BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        self.last_num = 0
        self._in_mecha_state = False
        self.player_unit = global_data.cam_lplayer
        self.bind_events(True)
        self.init_custom_com()
        self._on_update_ui()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.bind_events(False)
        self.unbind_player_events(self.player_unit)
        self.player_unit = None
        self.destroy_widget('custom_ui_com')
        return

    def _on_update_ui(self):
        if not self.player_unit or not self.player_unit.is_valid():
            return
        bag_num, bag_size = self.player_unit.ev_g_meow_bag_info() or (0, 0)
        safe_box_num, safe_box_size = self.player_unit.ev_g_meow_safe_box_info() or (0,
                                                                                     0)
        if self.last_num < bag_num and not self.panel.IsPlayingAnimation('add'):
            self.panel.PlayAnimation('add')
        self.last_num = bag_num
        self.panel.lab_num.SetString(str(bag_num))
        self.panel.nd_all.lab_all_num.SetString('%d/%d' % (bag_num, bag_size))
        self.panel.nd_all.lab_all_num.nd_auto_fit.img_full.setVisible(bag_num == bag_size)
        self.panel.nd_box.lab_box_num.SetString('%d/%d' % (safe_box_num, safe_box_size))
        self.panel.nd_box.lab_box_num.nd_auto_fit.img_full.setVisible(safe_box_num == safe_box_size)

    def bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'scene_camera_player_setted_event': self._on_cam_player_setted
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def _on_cam_player_setted(self, *args):
        if global_data.cam_lplayer != self.player_unit:
            self.unbind_player_events(self.player_unit)
            self.player_unit = global_data.cam_lplayer
            self.bind_player_events(self.player_unit)
        self.on_ctrl_target_changed()
        self._on_update_ui()

    def bind_player_events(self, unit):
        if not unit or not unit.is_valid():
            return
        unit.regist_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def unbind_player_events(self, unit):
        if not unit or not unit.is_valid():
            return
        unit.unregist_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def _on_meow_coin_change(self):
        self._on_update_ui()


class BattleFightMeow(BattleFightMeowBase):
    PANEL_CONFIG_NAME = 'battle/fight_coin'
    UI_ACTION_EVENT = BattleFightMeowBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'nd_custom.OnBegin': 'on_meow_btn_begin',
       'nd_custom.OnEnd': 'on_meow_btn_end'
       })

    def on_meow_btn_begin(self, layer, touch):
        self.panel.bag_coin.setVisible(True)

    def on_meow_btn_end(self, layer, touch):
        self.panel.bag_coin.setVisible(False)

    def leave_screen(self):
        super(BattleFightMeow, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleFightMeow')