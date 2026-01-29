# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/PrepareUIPC.py
from __future__ import absolute_import
from .PrepareUI import PrepareUIBase
from logic.comsys.battle.BattleInfo.CommunicateWidget import CommunicateWidgetPC
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from data.hot_key_def import PILOT_LAUNCH

class PrepareUIPC(PrepareUIBase):
    UI_ACTION_EVENT = {'temp_functions_pc.btn_set.OnBegin': 'on_click_setting_btn',
       'btn_launch.btn_major.OnClick': 'on_click_launch'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_setting_ui': {'node': 'temp_functions_pc.btn_set.temp_pc'},'switch_mic': {'node': 'temp_functions_pc.btn_speak.temp_pc'},'switch_speaker': {'node': 'temp_functions_pc.btn_sound.temp_pc'},PILOT_LAUNCH: {'node': 'btn_launch.temp_pc'}}
    HOT_KEY_FUNC_MAP_SHOW_CONDITIONAL = {PILOT_LAUNCH: 'on_cond_pilot_launch_show'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PrepareUIPC, self).on_init_panel(*args, **kwargs)
        self.panel.temp_functions.setVisible(False)
        self.panel.temp_functions_pc.setVisible(True)
        self.panel.temp_functions_pc.btn_observed.setVisible(False)
        self.panel.temp_functions_pc.nd_observed_details.setVisible(False)
        self.panel.temp_teammate.SetPosition('0%180', '100%-35')
        self.nd_map.setVisible(False)
        self.panel.RecordAnimationNodeState('lauch_appear')
        self._enable_btn_launch(True, force=True)
        self.prev_mark_info = None
        self.last_notice_pos = None
        self.has_initialized = False
        self._last_click_launch_time = 0
        self.following_id = None
        self.total_preparing_player_num = 100
        global_data.ui_mgr.set_all_ui_visible(True)
        exceptions_for_judge = ('JudgeLoadingUI', 'BigMapUI', 'SmallMapUI', 'SmallMapUIPC',
                                'BigMapUIPC')
        exceptions = ['MoveRockerUI']
        exceptions.extend(exceptions_for_judge)
        self.hide_main_ui(exceptions=exceptions)
        self.update_preparing_player_num(100)
        self.communicate_widget = CommunicateWidgetPC(self.panel.temp_functions_pc)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)
        self.add_blocking_ui_list(['MechaUI', 'MechaUIPC'])
        self.panel.temp_teammate.nd_follow_leader.lab_is_leader.SetString(get_text_by_id(13060))
        self.show_parachute_guide_tips(get_text_by_id(16034))
        self.last_can_launch = False
        if global_data.battle:
            self.total_preparing_player_num = global_data.battle.alive_player_num
            self.update_preparing_player_num(global_data.battle.prepare_num)
        return

    def on_cond_pilot_launch_show(self, common_show, *args):
        if common_show:
            return self._btn_launch_enabled
        else:
            return common_show