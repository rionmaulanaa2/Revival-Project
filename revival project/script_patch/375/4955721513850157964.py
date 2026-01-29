# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainSkillSelectUI.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import screen_utils
import math3d
import cc
import math
import copy
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_CLOSE
from common.platform.device_info import DeviceInfo
from logic.gcommon import time_utility as tutil
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import getScreenSize

class TrainSkillSelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_push_train/open_push_train_skill_choose'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        self.skill_data = None
        self.skill_idx_list = []
        self.init_parameters()
        self.init_panel()
        self.panel.setLocalZOrder(1)
        return

    def init_parameters(self):
        if not global_data.battle:
            return
        play_data = global_data.game_mode.get_cfg_data('play_data')
        open_skill = play_data.get('open_skill', {})
        is_atk = global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id()
        self.skill_data = global_data.train_battle_mgr.get_skill_data()
        if is_atk:
            self.skill_idx_list = open_skill.get('1', [])
        else:
            self.skill_idx_list = open_skill.get('2', [])

    def init_panel(self):
        if not self.skill_data:
            return
        idx = 0
        for idx in range(len(self.skill_idx_list)):
            item = self.panel.list_item.GetItem(idx)
            data = self.skill_data[str(self.skill_idx_list[idx])]
            item.icon.SetDisplayFrameByPath('', data.get('big_icon'))
            item.lab_name.SetString(data.get('name_text', 17001))
            item.lab_introduce.SetString(data.get('desc_text', 17001))
            item.img_mecha.setVisible(False)
            item.lab_mecha.setVisible(False)
            item.btn_choose.BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_click_select_skill(self.skill_idx_list[idx]))

    def on_click_select_skill(self, skill_id):
        if not global_data.player or not global_data.player.logic:
            return
        global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'do_train_skill', (skill_id,))
        self.close()

    def on_click_btn_close(self, *args):
        self.close()