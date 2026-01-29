# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEElementUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils.pve_utils import get_bless_elem_icon, get_all_elem_type
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.uisys.basepanel import BasePanel

class PVEElementUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'pve/info/battle_pve_info_element'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(PVEElementUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.init_ui()
        self.init_custom_com()
        self.process_events(True)

    def init_params(self):
        self.elem_list = []

    def init_ui(self):
        self.panel.list_item.setVisible(False)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_lplayer_setted,
           'scene_camera_target_setted_event': self.on_cam_lplayer_setted,
           'pve_update_elem_list_event': self.update_elem_list
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_finalize_panel(self):
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        self.init_params()
        self.process_events(False)
        super(PVEElementUI, self).on_finalize_panel()
        return

    def on_cam_lplayer_setted(self, *args):
        self.init_elem_list()

    def update_elem_list(self, bless_data):
        bless_keys = list(bless_data.keys())
        elem_list = get_all_elem_type(bless_keys)
        if self.elem_list == elem_list:
            return
        self.elem_list = elem_list
        list_item = self.panel.list_item
        list_item.DeleteAllSubItem()
        if elem_list:
            list_item.setVisible(True)
        else:
            list_item.setVisible(False)
        for index, elem_id in enumerate(elem_list):
            elem_item = list_item.AddTemplateItem()
            elem_item.img_line.setVisible(index > 0)
            elem_icon = get_bless_elem_icon(elem_id)
            elem_item.img_item.SetDisplayFrameByPath('', elem_icon)
            elem_item.setVisible(True)

    def init_elem_list(self):
        if not global_data.cam_lplayer:
            return
        bless_data = global_data.cam_lplayer.ev_g_choosed_blesses()
        self.update_elem_list(bless_data)