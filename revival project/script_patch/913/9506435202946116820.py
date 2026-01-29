# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleFightCapacity.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER_1
from logic.gcommon.cdata import driver_lv_data
from logic.gcommon.common_const import battle_const
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.const import uiconst

class BattleFightCapacityBase(MechaDistortHelper, BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    TAG_LV_UP_HP = 20201208

    def on_init_panel(self, *args, **kwargs):
        self._in_mecha_state = False
        self.player_unit = global_data.cam_lplayer
        self.bind_events(True)
        self.init_event()
        self.init_custom_com()
        self._update_judge_need_hide_details()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.bind_events(False)
        self.unbind_player_events(self.player_unit)
        self.player_unit = None
        self.destroy_widget('custom_ui_com')
        return

    def init_event(self):
        if not self.player_unit or not self.player_unit.is_valid():
            return
        self.level = self.player_unit.ev_g_attr_get('driver_level') or 0
        self.star_point = self.player_unit.ev_g_attr_get('star_point') or 0
        self._on_update_ui()

    def bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'scene_camera_player_setted_event': self._on_cam_player_setted,
           'on_observer_join_mecha': self._on_join_mecha,
           'on_observer_leave_mecha': self._on_leave_mecha,
           'judge_need_hide_details_event': self._update_judge_need_hide_details
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def _on_cam_player_setted(self, *args):
        if global_data.cam_lplayer != self.player_unit:
            self.unbind_player_events(self.player_unit)
            self.player_unit = global_data.cam_lplayer
            self.bind_player_events(self.player_unit)
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.add_hide_count(self.__class__.__name__)
        else:
            self.add_show_count(self.__class__.__name__)
        self.on_ctrl_target_changed()
        self.init_event()

    def bind_player_events(self, unit):
        if not unit or not unit.is_valid():
            return
        unit.regist_event('E_PLAYER_LEVEL_UP', self._on_player_level_up)

    def unbind_player_events(self, unit):
        if not unit or not unit.is_valid():
            return
        unit.unregist_event('E_PLAYER_LEVEL_UP', self._on_player_level_up)

    def _on_leave_mecha(self):
        self.add_show_count(self.__class__.__name__)

    def _on_join_mecha(self):
        self.add_hide_count(self.__class__.__name__)

    def _on_player_level_up(self, level, star_point):
        level_up = False
        if level > self.level:
            last_level = self.level

            def update_hp_info(panel):
                delta_hp = driver_lv_data.HP_ADD_PER_LEVEL * (level - last_level)
                panel.lab_3.SetString('HP+' + str(delta_hp))

            msg = {'i_type': battle_const.MAIN_NODE_PLAYER_LEVEL_UP,'last_show_num': self.level,'show_num': level,'ext_message_func': update_hp_info}
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            level_up = True

            def update_hp_anim_blow():
                global_data.emgr.lv_up_hp_notice.emit()

            self.panel.DelayCallWithTag(2.0, update_hp_anim_blow, self.TAG_LV_UP_HP)
        self.level = level
        self.star_point = star_point
        self.panel.PlayAnimation('add')
        self._on_update_ui(level_up)

    def _on_update_ui(self, level_up=False):
        if self.level == driver_lv_data.MAX_DRIVER_LEVEL:
            if not self or not self.is_valid():
                return
            self.panel.PlayAnimation('max')
        elif not self or not self.is_valid():
            return

        def level_up_func():
            self.panel.lab_strengh.SetString('Lv %d' % self.level)
            self.panel.vx_lab_strengh.SetString('Lv %d' % self.level)
            if self.level == driver_lv_data.MAX_DRIVER_LEVEL:
                self.panel.lab_strengh.SetColor('#SO')

        if level_up:
            self.panel.PlayAnimation('change_strengh')
            self.panel.DelayCall(0.45, level_up_func)
        else:
            level_up_func()

    def _update_judge_need_hide_details(self):
        if global_data.judge_need_hide_details:
            self.add_hide_count('JUDEG_DETAIL')
        else:
            self.add_show_count('JUDEG_DETAIL')


class BattleFightCapacity(BattleFightCapacityBase):
    PANEL_CONFIG_NAME = 'battle/fight_point'

    def leave_screen(self):
        super(BattleFightCapacity, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleFightCapacity')