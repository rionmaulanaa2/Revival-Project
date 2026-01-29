# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeObserveUINew.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gutils.custom_ui_utils import get_cut_name
from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget
from logic.gutils import judge_utils
from logic.gcommon.common_utils import battle_utils
from data.camera_state_const import OBSERVE_FREE_MODE
from logic.comsys.observe_ui.ObserveUI import FREE_VIEW_PIC_PATH, FOLLOW_VIEW_PIC_PATH
from logic.gcommon.common_const.ui_operation_const import FIRST_SWITCH_OBSERVE_CAM
from logic.comsys.observe_ui.JudgeOptionUINewWidget import JudgeOptionUINewWidget
from logic.gutils.team_utils import is_judge_group
from logic.comsys.chat.JudgeDanmuWidget import JudgeDanmuWidget
from common.cfg import confmgr
from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH
from common.const.property_const import *
from common.const import uiconst
from logic.comsys.observe_ui.ObserveUI import ObserveCameraWidget
from logic.gcommon.common_utils.local_text import get_text_by_id

class JudgeObserveUINew(BasePanel):
    PANEL_CONFIG_NAME = 'observe/judgement_basic'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'layer_observe.OnBegin': '_on_begin_layer_observe',
       'layer_observe.OnDrag': '_on_drag_layer_observe',
       'nd_choose.btn_change.OnClick': '_on_click_show_list_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        global_data.ui_mgr.close_ui('ObserveUI')
        self.process_event(True)
        self._observe_target_id = None
        if global_data.player and global_data.player.logic:
            spe_target_id = global_data.player.logic.ev_g_spectate_target_id()
            if spe_target_id:
                self._switch_observe_target_id(spe_target_id)
        self._cur_cam_state = None
        self._judge_setting_widget = JudgeOptionUINewWidget()
        self._judge_setting_widget.on_init_panel(self.panel)
        self.judge_observation_list_widget = None
        self._init_judge_list()
        self.observe_camera_widget = ObserveCameraWidget(self.__class__.__name__, self.panel, self.panel.btn_hide, self.panel.btn_hide_2, self.panel.btn_lock, self.panel.btn_free, self.panel.nd_observe_change.btn_change)
        self._init_view()
        bg_map_ui = global_data.ui_mgr.get_ui('BigMapUI')
        if bg_map_ui:
            self.add_hide_count('BigMapUI')
            bg_map_ui._hide_name_list.append(self.__class__.__name__)
        self._update_judge_need_hide_details()
        self._judge_danmu_widget = JudgeDanmuWidget(self.panel.nd_danmu)
        if global_data.ui_mgr.get_ui('BattleSceneOnlyUI') and global_data.ui_mgr.get_ui('BattleSceneOnlyUI').isValid():
            self.observe_camera_widget.show_camera_control_ui()
        self.init_kick_player_btn()
        return

    def on_resolution_changed(self):
        self.observe_camera_widget and self.observe_camera_widget.on_resolution_changed()

    def try_free_camera(self):
        if self.observe_camera_widget:
            self.observe_camera_widget.on_click_btn_free(None, None)
        return

    def _init_view(self):
        if global_data.player and global_data.player.get_setting(FIRST_SWITCH_OBSERVE_CAM):
            self.panel.img_tips.setVisible(True)
        else:
            self.panel.img_tips.setVisible(False)
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            cur_cam_type = partcam.get_cur_camera_state_type()
            self._on_set_camera_state(cur_cam_type)
        self._refresh_cur_ob_target_ui()

    def _init_judge_list(self):
        from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget, OB_LIST_TYPE_NEARBY
        self.judge_observation_list_widget = JudgeObservationListWidget(self.panel.list_tab_change, self.panel.list_choose)

    def on_finalize_panel(self):
        self.process_event(False)
        self._judge_setting_widget.on_finalize_panel()
        self._judge_setting_widget = None
        if self.judge_observation_list_widget:
            self.judge_observation_list_widget.destroy()
            self.judge_observation_list_widget = None
        self.destroy_widget('observe_camera_widget')
        return

    def _on_begin_layer_observe(self, *args):
        if self._cur_cam_state == OBSERVE_FREE_MODE:
            return True
        else:
            return False

    def _on_drag_layer_observe(self, layer, touch):
        import world
        scene = world.get_active_scene()
        if not scene:
            return
        else:
            ctrl = scene.get_com('PartCtrl')
            if not ctrl:
                return
            vec_temp = touch.getDelta()
            x_delta = vec_temp.x
            y_delta = vec_temp.y
            ctrl.on_touch_slide(x_delta, y_delta, None, touch.getLocation(), True)
            return

    def _on_click_show_list_btn(self, *args):
        if self.judge_observation_list_widget is None:
            log_error('coding error in _on_click_show_list_btn.')
            return
        else:
            self.panel.nd_list.setVisible(not self.panel.nd_list.isVisible())
            return

    def _refresh_cur_ob_target_ui(self):
        if self._observe_target_id is None:
            return
        else:
            player_info = judge_utils.get_global_player_info(self._observe_target_id)
            char_name = player_info.get('char_name', '')
            self.panel.lab_name.SetString(get_cut_name(six.text_type(char_name), 16))
            kill_player_num, kill_mecha_num = battle_utils.get_player_kill_num(self._observe_target_id)
            self.panel.lab_kill_num.SetString(str(kill_player_num))
            self.panel.lab_mech_num.SetString(str(kill_mecha_num))
            group_id = player_info.get('group', None)
            if group_id is None:
                self.panel.img_name_bg.setVisible(False)
                self.panel.nd_team.setVisible(False)
            else:
                self.panel.img_name_bg.setVisible(True)
                self.panel.img_name_bg.SetDisplayFrameByPath('', JudgeObservationListWidget.get_team_bg_img_path(group_id, False))
                self.panel.nd_team.setVisible(True)
                self.panel.lab_num.SetString(str(group_id))
            return

    def _on_add_player(self, lplayer):
        if lplayer and lplayer.id == self._observe_target_id:
            self._refresh_cur_ob_target_ui()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'show_battle_report_event': self._on_show_battle_report,
           'on_player_inited_event': self._on_player_model_load,
           'scene_observed_player_setted_event': self._on_switch_observe_target,
           'camera_switch_to_state_event': self._on_set_camera_state,
           'judge_cache_add_player': self._on_judge_cache_add_player,
           'judge_cache_player_dead': self._on_judge_cache_player_dead,
           'switch_judge_camera_event': self._switch_judge_camera,
           'judge_need_hide_details_event': self._update_judge_need_hide_details
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_judge_cache_add_player(self, pid):
        if pid == self._observe_target_id:
            self._refresh_cur_ob_target_ui()

    def _on_judge_cache_player_dead(self, pid, killer_id):
        if pid == self._observe_target_id:
            self._refresh_cur_ob_target_ui()

    def _on_show_battle_report(self, report_dict):
        self._refresh_cur_ob_target_ui()

    def _on_player_model_load(self, lplayer):
        if is_judge_group(lplayer.ev_g_group_id()):
            return
        self._on_add_player(lplayer)

    def _on_switch_observe_target(self, observe_target):
        if observe_target:
            self._switch_observe_target_id(observe_target.id)
        else:
            self._switch_observe_target_id(None)
        return

    def _switch_observe_target_id(self, observe_target_id):
        self._observe_target_id = observe_target_id
        self._refresh_cur_ob_target_ui()

    def _on_set_camera_state(self, state, *args):
        if self._cur_cam_state == OBSERVE_FREE_MODE and state != OBSERVE_FREE_MODE:
            self.panel.layer_observe.SetEnableTouch(False)
            self.panel.layer_observe.SetEnableTouch(True)
            self.panel.layer_observe.setVisible(False)
        else:
            self.panel.layer_observe.setVisible(True)
        self._cur_cam_state = state
        self.observe_camera_widget.set_camera_state(state)

    def exit_free_camera(self):
        panel = self.panel
        if panel and panel.isValid():
            if panel.nd_control:
                panel.nd_control.setVisible(True)

    def exit_lock_camera(self):
        panel = self.panel
        if panel and panel.isValid():
            if panel.nd_control:
                panel.nd_control.setVisible(True)

    def _switch_judge_camera(self, enable, *args):
        if global_data.judge_need_hide_details:
            self.panel.nd_observe_change.setVisible(False)
            self.panel.nd_set.setVisible(False)
        else:
            self.panel.nd_observe_change.setVisible(not enable)
            self.panel.nd_set.setVisible(not enable)
        if not self.is_competition_battle():
            self.panel.nd_set.setVisible(False)

    def _update_judge_need_hide_details(self):
        self.panel.nd_judgement_info.setVisible(not global_data.judge_need_hide_details)
        if global_data.judge_need_hide_details:
            self.panel.nd_observe_change.setVisible(False)
            self.panel.nd_set.setVisible(False)
            self.panel.nd_danmu.setVisible(False)
        else:
            self.panel.nd_observe_change.setVisible(not global_data.is_in_judge_camera)
            self.panel.nd_set.setVisible(not global_data.is_in_judge_camera)
            self.panel.nd_danmu.setVisible(not global_data.is_in_judge_camera)
        if not self.is_competition_battle():
            self.panel.nd_set.setVisible(False)

    def get_judge_setting_widget(self):
        return self._judge_setting_widget

    def is_competition_battle(self):
        if global_data.battle:
            return global_data.battle.get_is_competition()
        else:
            return False

    def init_kick_player_btn(self):

        @self.panel.btn_kick.unique_callback()
        def OnClick(*args):
            self.on_click_btn_kick_player()

    def on_click_btn_kick_player(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            from logic.gutils.hot_key_utils import judge_kick_out_player_func
            judge_kick_out_player_func()

        SecondConfirmDlg2().confirm(content=get_text_by_id(860465), confirm_callback=confirm_callback)