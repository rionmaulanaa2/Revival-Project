# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEIceBulletUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.cfg import confmgr
ICE_ITEM_ID = 10000095
ICE_BLESS_SET = {5110401, 5110402}

class PVEIceBulletUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/i_mech_bullet_pve'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'pve_update_ice_cnt': 'update_ice_cnt',
       'pve_update_elem_list_event': 'update_elem_list',
       'scene_camera_player_setted_event': 'on_camera_player_setted'
       }

    def on_init_panel(self):
        max_cnt = confmgr.get('item', str(ICE_ITEM_ID), 'max_overlay', default=20)
        self.panel.lab_bullet_full.SetString('/{}'.format(max_cnt))
        self.panel.nd_pve_energy.setVisible(False)

    def on_camera_player_setted(self, *args):
        if not global_data.cam_lplayer:
            return
        self.update_elem_list(global_data.cam_lplayer.ev_g_choosed_blesses())
        self.update_ice_cnt(global_data.cam_lplayer.ev_g_pve_ice())

    def update_ice_cnt(self, cnt):
        self.panel.lab_bullet_num.SetString(str(cnt))

    def update_elem_list(self, elem_list):
        self.panel.nd_pve_energy.setVisible(bool(set(elem_list) & ICE_BLESS_SET))