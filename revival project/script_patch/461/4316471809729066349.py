# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/CamTrkEditorUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const import uiconst

class CamTrkEditorUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/cam_trk_test'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_forward.OnClick': 'on_btn_forward_clicked',
       'btn_back.OnClick': 'on_btn_back_clicked',
       'btn_up.OnClick': 'on_speed_up_clicked',
       'btn_down.OnClick': 'on_speed_down_clicked'
       }

    def on_init_panel(self):
        self.init_data()
        self.update_spd_ratio(0)

    def init_data(self):
        self._cnt_cam_id = 0
        self._cnt_spd_ratio = 1.0

    def on_btn_back_clicked(self, *args):
        global_data.emgr.play_camera_trk_event.emit(self._cnt_cam_id, self.decrease_cnt_cam_id, True, self._cnt_spd_ratio)

    def on_btn_forward_clicked(self, *args):
        global_data.emgr.play_camera_trk_event.emit(self._cnt_cam_id + 1, self.increase_cnt_cam_id, False, self._cnt_spd_ratio)

    def on_speed_up_clicked(self, *args):
        self.update_spd_ratio(0.1)

    def on_speed_down_clicked(self, *args):
        self.update_spd_ratio(-0.1)

    def update_spd_ratio(self, gap):
        new_ratio = self._cnt_spd_ratio + gap
        if new_ratio > 0:
            self.label_spd.SetString(str(new_ratio))
            self._cnt_spd_ratio = new_ratio

    def increase_cnt_cam_id(self):
        self._cnt_cam_id += 1

    def decrease_cnt_cam_id(self):
        self._cnt_cam_id -= 1