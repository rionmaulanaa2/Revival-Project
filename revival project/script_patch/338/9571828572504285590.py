# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/PrepareUI.py
from __future__ import absolute_import
from __future__ import print_function
import time
from common.uisys.basepanel import BasePanel
from logic.comsys.map.MapBaseUINew import MapBaseUI
from common.const import uiconst
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.battle.BattleInfo.CommunicateWidget import CommunicateWidget
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.hot_key_utils import set_hot_key_common_tip
from data.hot_key_def import PILOT_LAUNCH

class PrepareUIBase(MapBaseUI):
    PANEL_CONFIG_NAME = 'battle_before/fight_before_ready'
    DLG_ZORDER = uiconst.BASE_LAYER_ZORDER
    ENABLE_HOT_KEY_SUPPORT = True
    MOUSE_CURSOR_TRIGGER_SHOW = True
    HOT_KEY_FUNC_MAP = {'switch_mic': 'on_keyboard_switch_mic',
       'switch_speaker': 'on_keyboard_switch_sound',
       PILOT_LAUNCH: 'on_keyboard_pilot_launch'
       }

    def init_event(self):
        super(PrepareUIBase, self).init_event()
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.show_parachute_follow_tips += self.show_parachute_follow_tips
        global_data.emgr.get_launch_status_event += self.get_launch_status
        global_data.emgr.show_parachute_guide_tips += self.show_parachute_guide_tips

    def get_launch_status(self):
        return self.last_can_launch

    def on_login_reconnect(self):
        self.show()
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)

    def on_player_parachute_stage_changed(self, stage):
        if stage == parachute_utils.STAGE_PARACHUTE_DROP:
            self.hide()

    def _enable_btn_launch(self, flag, force=False):
        if flag == self.panel.btn_launch.btn_major.IsEnable() and not force:
            return
        self._btn_launch_enabled = flag
        self.panel.btn_launch.btn_major.SetEnable(flag)
        if global_data.is_pc_mode:
            self.check_hotkey_show(PILOT_LAUNCH)
        if flag:
            self.panel.btn_launch.lab_text.SetString(82112)
            self.panel.btn_launch.lab_text.SetColor(11815709)
            self.panel.PlayAnimation('lauch_appear')
        else:
            self.panel.btn_launch.lab_text.SetString(82114)
            self.panel.btn_launch.lab_text.SetColor(15593463)
            self.panel.StopAnimation('lauch_appear')
            self.panel.RecoverAnimationNodeState('lauch_appear')

    def update(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            player = global_data.cam_lplayer
            if not player:
                return
            not_following = player.ev_g_parachute_follow_target() is None
            if global_data.cam_lplayer and len(global_data.cam_lplayer.ev_g_groupmate()) == 1:
                self._enable_btn_launch(True)
            else:
                stage = player.share_data.ref_parachute_stage
                if not_following:
                    self._enable_btn_launch(True)
                else:
                    follow_id, c_name = global_data.cam_lplayer.ev_g_parachute_follow_target(True)
                    if self.panel.btn_launch.isVisible() or not self.has_initialized or self.following_id != follow_id:
                        if not follow_id:
                            c_name = global_data.cam_lplayer.ev_g_char_name()
                        self.following_id = follow_id
                        self.show_parachute_follow_tips(get_text_by_id(13056, {'playername': c_name}))
                        self._enable_btn_launch(False)
                if not self.has_initialized:
                    self.has_initialized = True
            return

    def init_parameters(self, **kwargs):
        super(PrepareUIBase, self).init_parameters(**kwargs)
        self._btn_launch_enabled = False
        self.init_sub_component()

    def init_sub_component(self):
        self.init_map3d_touch_layer_widget()
        self.init_countdown_widget()
        self.init_teammate_widget()

    def init_map3d_touch_layer_widget(self):
        from logic.comsys.map.map_widget.Map3DTouchLayerWidget import Map3DTouchLayerWidget
        self.map3d_touch_layer_widget = Map3DTouchLayerWidget(self)

    def init_touch_layer_widget(self):
        from logic.comsys.map.map_widget.BigMapTouchLayerWidget import BigMapTouchLayerWidget
        self.touch_layer_widget = BigMapTouchLayerWidget(self)

    def init_countdown_widget(self):
        from logic.comsys.prepare.PrepareCountDownWidget import PrepareCountDownWidget
        self.countdown_widget = PrepareCountDownWidget(self, self.panel)

    def init_parachute_range_widget(self):
        from logic.comsys.map.map_widget.MapParachuteRangeWidget import MapParachuteRangeWidget
        self.para_range_widget = MapParachuteRangeWidget(self, self.map_nd.nd_scale_up)

    def init_teammate_widget(self):
        from logic.comsys.battle.TeammateStatusWidget import TeammateStatusWidget
        self.teammate_widget = TeammateStatusWidget(self.panel.temp_teammate)
        if global_data.battle and global_data.battle.get_max_teammate_num() <= 1:
            self.panel.temp_teammate.setVisible(False)

    def init_parachute_cover_widget(self):
        from logic.comsys.map.map_widget.MapParachuteCoverWidget import MapParachuteCoverWidget
        self.para_cover_widget = MapParachuteCoverWidget(self, self.map_nd.nd_scale_up)

    def on_finalize_panel(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        self.show_main_ui()
        self.destroy_widget('countdown_widget')
        self.destroy_widget('teammate_widget')
        self.destroy_widget('map3d_touch_layer_widget')
        super(PrepareUIBase, self).on_finalize_panel()
        if self.communicate_widget:
            self.communicate_widget.destroy()
            self.communicate_widget = None
        return

    def update_preparing_player_num(self, player_num):
        self.panel.lab_person_num.SetString('{}/{}'.format(player_num, self.total_preparing_player_num))

    def show_parachute_follow_tips(self, text):
        self.panel.lab_follow_tips.SetString(text)

    def show_parachute_guide_tips(self, text):
        pass

    def on_click_setting_btn(self, *args):
        global_data.ui_mgr.show_ui('MainSettingUI', 'logic.comsys.setting_ui')
        return True

    def on_click_launch(self, *args):
        if global_data.enable_parachute_range_circle and not self.prev_mark_info:
            return
        else:
            now = time.time()
            if now - self._last_click_launch_time <= 0.1:
                return
            self._last_click_launch_time = now
            if not global_data.cam_lplayer or not global_data.cam_lplayer.sd:
                return
            if global_data.cam_lplayer.sd.ref_parachute_stage and global_data.cam_lplayer.sd.ref_parachute_stage & parachute_utils.BAN_LAUNCH_STAGE:
                return
            battle = global_data.battle
            if not battle:
                return
            plane = battle.get_entity(battle.plane_id)
            if not plane:
                return
            plane = plane.logic
            pos = plane.ev_g_position()
            if pos is None:
                return
            pos = (
             pos.x, pos.y, pos.z)
            global_data.cam_lplayer.send_event('E_START_PARACHUTE', pos, pos, True)
            global_data.emgr.camera_cancel_all_trk.emit()
            global_data.emgr.camera_enable_follow_event.emit(True)
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
            if global_data.ui_mgr.get_ui('BigMapUI'):
                global_data.ui_mgr.close_ui('BigMapUI')
            return

    def on_hot_key_closed_state(self):
        super(PrepareUIBase, self).on_hot_key_closed_state()
        self.panel.list_pc.setVisible(False)

    def on_hot_key_opened_state(self):
        super(PrepareUIBase, self).on_hot_key_opened_state()
        from logic.gutils.hot_key_utils import get_hot_key_fun_desc
        from data import hot_key_def
        self.panel.list_pc.setVisible(True)
        key_names = [
         (
          2, hot_key_def.SWITCH_PC_MODE)]
        func_text = [
         get_hot_key_fun_desc(hot_key_def.SWITCH_PC_MODE)]
        self.panel.list_pc.SetInitCount(len(key_names))
        all_item = self.panel.list_pc.GetAllItem()
        for idx, names in enumerate(key_names):
            key_type, name = names
            desc = func_text[idx]
            all_item[idx].lab_desc.SetString(desc)
            all_item[idx].temp_pc.pc_tip_list.SetInitCount(1)
            if key_type == 0:
                all_item[idx].temp_pc.pc_tip_list.GetItem(0).lab_pc.SetString(get_text_by_id(name))
            elif key_type == 1:
                set_hot_key_common_tip(all_item[idx].temp_pc, None, name)
            else:
                set_hot_key_common_tip(all_item[idx].temp_pc, name)

        return

    def on_keyboard_switch_mic(self, msg, keycode):
        print('on_keyboard_switch_mic', msg, keycode)
        self.communicate_widget.trigger_btn_speaker()

    def on_keyboard_switch_sound(self, msg, keycode):
        self.communicate_widget.trigger_btn_sound()

    def on_keyboard_pilot_launch(self, msg, keycode):
        if not self._btn_launch_enabled:
            return
        self.on_click_launch()


class PrepareUI(PrepareUIBase):
    UI_ACTION_EVENT = {'temp_functions.btn_set.OnBegin': 'on_click_setting_btn',
       'btn_launch.btn_major.OnClick': 'on_click_launch'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_setting_ui': {'node': 'temp_functions.btn_set.temp_pc'},'switch_mic': {'node': 'temp_functions.btn_speak.temp_pc'},'switch_speaker': {'node': 'temp_functions.btn_sound.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(PrepareUI, self).on_init_panel(*args, **kwargs)
        self.panel.temp_functions.setVisible(True)
        self.panel.temp_functions_pc.setVisible(False)
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
        exceptions_for_judge = ('JudgeLoadingUI', 'BigMapUI', 'SmallMapUI')
        exceptions = ['MoveRockerUI', 'QuickMarkBtn', 'FightChatUI']
        exceptions.extend(exceptions_for_judge)
        self.hide_main_ui(exceptions=exceptions)
        self.update_preparing_player_num(100)
        self.communicate_widget = CommunicateWidget(self.panel.temp_functions)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)
        self.add_blocking_ui_list(['MechaUI'])
        self.panel.temp_teammate.nd_follow_leader.lab_is_leader.SetString(get_text_by_id(13060))
        self.show_parachute_guide_tips(get_text_by_id(16034))
        self.last_can_launch = False
        if global_data.battle:
            self.total_preparing_player_num = min(self.total_preparing_player_num, global_data.battle.alive_player_num)
            self.update_preparing_player_num(global_data.battle.prepare_num)
        return