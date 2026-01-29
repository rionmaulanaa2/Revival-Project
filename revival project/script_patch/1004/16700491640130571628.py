# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/KothEndCampStatisticsUI.py
from __future__ import absolute_import
import six
import math
import functools
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.end_statics_utils import init_koth_end_campmate_statistics_new
from common.const import uiconst

class KothEndCampStatisticsUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_statistics_koth_camp'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_exit.btn_common.OnClick': '_on_click_btn_exit'
       }

    def on_init_panel(self, settle_dict):
        global_data.ui_mgr.show_ui('KothEndFullScreenBg', 'logic.comsys.battle.Settle')
        self.entity_id_to_list_index = {}
        self._init_statistics(settle_dict)
        self._play_animation()
        self.init_event()

    def _init_statistics(self, settle_dict):
        self.entity_id_to_list_index = init_koth_end_campmate_statistics_new(self.panel, settle_dict)

    def _play_animation(self):
        self.panel.PlayAnimation('appear')

    def _on_click_btn_exit(self, *args):
        if global_data.player is not None:
            global_data.player.quit_battle()
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_koth_praised_num_event': self.update_koth_praised_num
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        global_data.ui_mgr.close_ui('KothEndFullScreenBg')

    def update_koth_praised_num(self, from_entity_id, to_entity_id, praised_num):
        details = self.panel.list_stat
        for entity_id, likes in six.iteritems(global_data.king_battle_data.end_likes):
            if entity_id not in self.entity_id_to_list_index:
                continue
            index = self.entity_id_to_list_index[entity_id]
            detail = details.GetItem(index)
            detail.lab_like.SetString(str(praised_num))

        if to_entity_id not in self.entity_id_to_list_index:
            return
        index = self.entity_id_to_list_index[to_entity_id]
        detail = details.GetItem(index)
        if global_data.player and from_entity_id == global_data.player.id:
            detail.btn_like.SetEnable(False)
            detail.img_tick.setVisible(True)