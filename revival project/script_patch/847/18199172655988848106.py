# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainSkillUI.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import screen_utils
import math3d
import cc
import math
import copy
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from common.platform.device_info import DeviceInfo
from logic.gcommon import time_utility as tutil
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import getScreenSize
from .TrainSkillSelectUI import TrainSkillSelectUI
from logic.gcommon.common_const import battle_const

class TrainSkillUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_push_train/fight_push_train_skill'
    DLG_ZORDER = SMALL_MAP_ZORDER
    GLOBAL_EVENT = {'update_train_skill_prog': 'on_update_skill_prog',
       'train_use_skill_succeed': 'on_use_skill_succeed',
       'show_last_round_info_event': 'on_update_skill_prog'
       }
    UI_ACTION_EVENT = {'btn_rogue.OnClick': 'on_click_use_skill'
       }
    HOT_KEY_FUNC_MAP = {'train_battle_use_item.DOWN_UP': 'on_click_use_skill'
       }
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_custom_com()
        self.panel.setLocalZOrder(1)
        self.panel.prog.SetPercentage(0)
        self.panel.temp_pc.setVisible(False)
        self.panel.RecordAnimationNodeState('tips')
        self.on_update_skill_prog()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_parameters(self):
        self.prog = 0
        self.can_use_skill_tips = False
        self.skill_data = global_data.game_mode.get_cfg_data('train_skill_data')
        self.open_skill = global_data.game_mode.get_cfg_data('play_data').get('open_skill')

    def on_update_skill_prog(self, prog=-1):
        if prog == -1 and global_data.battle:
            prog = global_data.battle.get_skill_power()
        self.prog = int(prog)
        self.panel.prog.SetPercentage(self.prog * 2)
        if self.prog >= 50:
            self.panel.PlayAnimation('tips')
            if not self.can_use_skill_tips:
                self.can_use_skill_tips = True
                message_data = {'i_type': battle_const.TRAIN_CAN_USE_SKILL}
                global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)
        else:
            if self.panel.IsPlayingAnimation('tips'):
                self.panel.RecoverAnimationNodeState('tips')
                self.panel.StopAnimation('tips')
            return

    def on_click_use_skill(self, *args):
        if self.prog < 50:
            return
        if not global_data.player or not global_data.player.logic:
            return
        TrainSkillSelectUI()

    def on_use_skill_succeed(self, soul_id, skill_id, player_name):
        if not global_data.battle:
            return
        if global_data.player and global_data.player.id == soul_id:
            self.on_update_skill_prog(0)
        self.can_use_skill_tips = False
        is_atk = global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id()
        is_self = 0
        i_type = battle_const.TRAIN_USE_SKILL_STOP
        if is_atk:
            if int(skill_id) in self.open_skill.get('1', []):
                is_self = 0
                i_type = battle_const.TRAIN_USE_SKILL_STOP
            else:
                is_self = 1
                i_type = battle_const.TRAIN_USE_SKILL_PUSH
        elif int(skill_id) in self.open_skill.get('2', []):
            is_self = 0
            i_type = battle_const.TRAIN_USE_SKILL_STOP
        else:
            is_self = 1
            i_type = battle_const.TRAIN_USE_SKILL_PUSH
        skill_data = self.skill_data.get(str(skill_id))
        content_txt = get_text_by_id(skill_data['tips_text'])
        tips_icon = skill_data['tips_icon']
        lab_title = skill_data['tips_title']
        message_data = {'i_type': i_type,'lab_title': lab_title[0],'lab_title2': lab_title[1],'content_txt': content_txt,'icon_path': tips_icon[is_self],'show_num': 1,
           'ext_message_func': lambda node: self.set_lab_name(node, player_name)}
        global_data.emgr.show_battle_main_message.emit(message_data, battle_const.MAIN_NODE_COMMON_INFO, False, False)

    def set_lab_name(self, node, player_name):
        if not node or not node.lab_2:
            return
        node.lab_2.SetString(player_name)

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')