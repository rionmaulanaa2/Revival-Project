# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/HuntingLoadingVsUI.py
from __future__ import absolute_import
from __future__ import print_function
import copy
from logic.gutils import role_head_utils
from common.cfg import confmgr
import cc
from logic.gutils.template_utils import get_ui_picture_pos_anim
from common.const.uiconst import LOADING_ZORDER_ABOVE
from common.uisys.basepanel import BasePanel
from logic.gcommon import time_utility as tutil
import math
from common.const import uiconst
from logic.gutils.role_head_utils import init_role_head, get_mecha_photo, get_role_default_photo, get_head_photo_res_path

class HuntingLoadingVsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_hunting/battle_hunting_loading'
    DLG_ZORDER = LOADING_ZORDER_ABOVE
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        self.group_data = {}
        self.hide_main_ui(['FFABeginCountDown'])

    def on_finalize_panel(self):
        self.show_main_ui()

    def play_animation(self):
        self.panel.PlayAnimation('appear')
        self.panel.SetTimeOut(3.0, self.close)

    def init_parameter(self):
        self.spectate_player_id = global_data.player.get_global_spectate_player_id()
        if self.spectate_player_id is None:
            self.spectate_player_id = global_data.player.id
        return

    def show_vs(self, group_data):
        self.group_data = group_data
        print('group_data', group_data)
        self.init_parameter()
        self.init_widget()
        self.play_animation()

    def init_widget(self):
        mecha_group_data = self.group_data.get('mecha_group', [])
        human_group_data = self.group_data.get('human_group', [])

        def update_throught_data(list_widget, data_ls):
            list_widget.SetInitCount(len(data_ls))
            for idx, role_id in enumerate(data_ls):
                head_widget = list_widget.GetItem(idx)
                if not head_widget:
                    continue
                photo_no = get_role_default_photo(role_id) or get_mecha_photo(role_id)
                icon = get_head_photo_res_path(photo_no)
                head_widget.img_head.SetDisplayFrameByPath('', icon)

        update_throught_data(self.panel.list_head_red, mecha_group_data)
        update_throught_data(self.panel.list_head_blue, human_group_data)