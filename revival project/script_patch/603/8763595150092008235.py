# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapNbombDeviceWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget.MapScaleInterface import CommonMapMark

class MapNbombDeviceWidget(CommonMapMark):

    def __init__(self, parent_nd, mark_no, is_deep, state, parent=None, require_follow_model=False):
        super(MapNbombDeviceWidget, self).__init__(parent_nd, mark_no, is_deep, state, parent, require_follow_model)
        self.deep_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_blue.png'
        self.not_deep_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_red.png'
        self._is_bind_event = False
        self.process_event(True)
        self.change_nbomb_img()

    def destroy(self):
        self.process_event(False)
        super(MapNbombDeviceWidget, self).destroy()

    def process_event(self, is_bind):
        if self._is_bind_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'nbomb_update_explosion': self.change_nbomb_img
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._is_bind_event = is_bind

    def set_deep(self, is_deep=False):
        pass

    def change_nbomb_img(self, *args):
        if not global_data.nbomb_battle_data:
            return
        timestamp = global_data.nbomb_battle_data.get_nbomb_cd_timestamp()
        if not timestamp:
            return
        is_self_camp_installed = global_data.nbomb_battle_data.is_self_group_install_nbomb()
        self_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_blue.png'
        emeny_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_red.png'
        bar_path = self_path if is_self_camp_installed else emeny_path
        self._nd.sp_circle.SetDisplayFrameByPath('', bar_path)
        vx_self_path = 'gui/ui_res_2/battle/map/icon_portal2_vx.png'
        vx_emeny_path = 'gui/ui_res_2/battle/map/icon_portal1_vx.png'
        vx_path = vx_self_path if is_self_camp_installed else vx_emeny_path
        self._nd.vx_light.SetDisplayFrameByPath('', vx_path)