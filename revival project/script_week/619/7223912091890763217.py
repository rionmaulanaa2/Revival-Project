# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/JudgeChooseFactionUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gutils.custom_room_utils import get_custom_faction_config

class JudgeChooseFactionUI(BasePanel):
    PANEL_CONFIG_NAME = 'room/judge_choose_faction'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    BORDER_INDENT = 24
    UI_ACTION_EVENT = {'panel.OnBegin': 'close_faction_list'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameter()
        self.hide()

    def init_parameter(self):
        self.battle_type = None
        self.uid = 0
        return

    def ui_vkb_custom_func(self):
        self.hide()

    def show_faction_list(self, battle_type, uid, name):
        if self.battle_type is None or battle_type != self.battle_type:
            self.battle_type = battle_type
            self.init_faction_list()
        self.uid = uid
        self.init_title(name)
        self.show()
        return

    def close_faction_list(self, *args):
        self.hide()

    def init_faction_list(self):
        custom_faction_config = get_custom_faction_config(self.battle_type)
        faction_ids = sorted(list(custom_faction_config.keys()))
        self.panel.list_faction.DeleteAllSubItem()
        self.panel.list_faction.SetInitCount(len(faction_ids) * 1)
        for idx, faction_id in enumerate(faction_ids):
            nd_item = self.panel.list_faction.GetItem(idx)
            faction_name_text_id = custom_faction_config[faction_id]
            nd_item.lab_faction.SetString(faction_name_text_id)

            @nd_item.unique_callback()
            def OnClick(btn, touch, f_id=faction_id):
                global_data.player.judge_set_room_faction(self.uid, f_id)
                self.hide()

    def init_title(self, player_name):
        self.panel.lab_title.SetString(860469)
        self.panel.lab_name.SetString(player_name)