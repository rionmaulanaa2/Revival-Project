# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ModeNameUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gutils.pve_utils import get_pve_player_count
from logic.gcommon.common_const import battle_const
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
PVE_TEXT_LIST = [
 0, 449, 450, 451]

class ModeNameUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle/model_tag'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'switch_control_target_event': 'on_ctrl_target_changed',
       'scene_observed_player_setted_event': 'on_observed_player_setted'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ModeNameUI, self).on_init_panel()
        self._mobile_pos = self.panel.lab_text.GetPosition()
        self._mobile_judge_pos = self.panel.nd_mobile_judge.GetPosition()
        self.panel.lab_text.setVisible(False)
        self.panel.lab_text_pc.setVisible(False)
        battle = global_data.battle
        if not battle:
            return
        else:
            battle_tid = battle.get_battle_tid()
            battle_config = confmgr.get('battle_config')
            battle_bp_config = confmgr.get('battle_bp_config')
            battle_info = battle_config.get(str(battle_tid))
            if battle_info is None:
                return
            is_bp_battle = str(battle_tid) in battle_bp_config
            random_map = battle_info.get('cRandomMap')
            if random_map or is_bp_battle:
                map_id = battle.get_map_id()
                map_data_conf = confmgr.get('map_config', str(map_id), default={})
                name_text_id = map_data_conf.get('nameTID', -1)
            else:
                name_text_id = battle_info.get('cNameTID', -1)
            if name_text_id == -1:
                return
            if global_data.game_mode.is_pve():
                difficulty = global_data.battle.get_cur_pve_difficulty()
                if not difficulty:
                    return
                name_text = PVE_TEXT_LIST[difficulty]
                player_count = get_pve_player_count()
                name_text_id = '{} {}'.format(get_text_by_id(name_text), get_text_by_id(481).format(player_count))
            self.panel.lab_text.setVisible(not global_data.is_pc_mode)
            self.panel.lab_text_pc.setVisible(global_data.is_pc_mode)
            self.panel.lab_text.SetString(name_text_id)
            self.panel.lab_text_pc.SetString(name_text_id)
            from logic.gutils import judge_utils
            if not global_data.is_pc_mode:
                if judge_utils.is_ob():
                    pos = self._mobile_judge_pos
                else:
                    pos = self._mobile_pos
                self.panel.lab_text.SetPosition(*pos)
            if global_data.is_judge_ob:
                self.add_hide_count('JUDEG_OB')
            else:
                self.add_show_count('JUDEG_OB')
            return