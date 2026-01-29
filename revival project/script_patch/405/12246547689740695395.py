# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleRightTopUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER_1
from common.uisys.basepanel import BasePanel
from logic.comsys.battle.BattleInfo.CommunicateWidget import CommunicateWidget
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.client.const import pc_const
from logic.gutils import pc_utils
from common.const import uiconst
from logic.gcommon.cdata.round_competition import check_is_in_competition_battle

class BattleRightTopBaseUI(MechaDistortHelper, BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    HOT_KEY_CHECK_VISIBLE = True
    ENABLE_HOT_KEY_SUPPORT = True
    HOT_KEY_FUNC_MAP = {'switch_mic': 'on_keyboard_switch_mic',
       'switch_speaker': 'on_keyboard_switch_sound',
       'open_fight_chat_dialog': 'on_keyboard_open_chat_dialog',
       'show_spectate_info': 'on_keyboard_show_spectate_info',
       'close_voice_list_view': 'on_keyboard_close_all_list'
       }
    GLOBAL_EVENT = {'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled'
       }

    def on_init_panel(self, *args, **kwargs):
        self._in_mecha_state = False
        self.communicate_widget = None
        econf = {'update_animation_info': self.update_animation_info,
           'update_camera_debug_info': self.update_camera_info,
           'scene_camera_player_setted_event': self.on_cam_player_setted,
           'on_observer_num_changed': self.set_observe_num,
           'on_be_like_num_changed': self.set_like_num,
           'scene_observed_player_setted_event': self.on_enter_observe,
           'on_update_spectate_hot_info': self._on_update_spectate_hot_info,
           'ui_refresh_all_custom_ui_conf': self.modify_panel_position,
           'scene_player_setted_event': self.on_player_setted
           }
        global_data.emgr.bind_events(econf)
        self.init_communicate_widget()
        self.init_custom_com()
        self.init_observe_num()
        self.hide_ui()
        self.exercise_field_modify()
        self.pve_field_modify()
        self.ob_modify()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        return

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        return
        show = pc_utils.should_pc_key_hint_related_uis_show(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON, hint_switch, display_option, pc_op_mode)
        if show:
            self.add_show_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)
        else:
            self.add_hide_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)

    def on_cam_player_setted(self, *args):
        self.on_ctrl_target_changed()

    def switch_to_mecha(self):
        self.modify_panel_position(in_mecha=True)
        super(BattleRightTopBaseUI, self).switch_to_mecha()

    def switch_to_non_mecha(self):
        self.modify_panel_position(in_mecha=False)
        super(BattleRightTopBaseUI, self).switch_to_non_mecha()

    def init_communicate_widget(self):
        pass

    def hide_ui(self):
        pass

    @execute_by_mode(True, (game_mode_const.GAME_MODE_EXERCISE,))
    def modify_panel_position(self, in_mecha=False):
        if in_mecha:
            self.panel.nd_custom.SetPosition('i96', 'i5')
        else:
            self.panel.nd_custom.SetPosition('i24', 'i0')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        if self.communicate_widget:
            self.communicate_widget.destroy()
            self.communicate_widget = None
        self.destroy_widget('custom_ui_com')
        return

    def on_click_setting_btn(self, *args):
        if global_data.player:
            global_data.ui_mgr.show_ui('MainSettingUI', 'logic.comsys.setting_ui')
        return True

    def update_animation_info(self, text):
        if text is None:
            text = ''
        visible = False
        if text:
            visible = True
        self.panel.animation_text.setString(text)
        self.panel.animation_bg.setVisible(visible)
        return

    def update_camera_info(self, camera_trk_info_list):
        from common.cfg import confmgr
        camera_name = confmgr.get('camera_transfer', str(global_data.cam_data.camera_state_type), default={}).get('cDesc', '')
        text = '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xa8\xa1\xe5\xbc\x8f: %s %s\n' % (str(global_data.cam_data.camera_state_type), camera_name)
        for tag, trk_path in camera_trk_info_list:
            text += '\xe9\x95\x9c\xe5\xa4\xb4\xe8\xbd\xa8\xe8\xbf\xb9: %s %s \n' % (tag, trk_path)

        self.panel.lab_camera_info.setString(text)

    def on_change_ui_custom_data(self):
        if self._in_mecha_state:
            UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def init_observe_num(self):
        self.set_observe_num(0)
        self.set_like_num(0)
        if global_data.player:
            global_data.player.req_global_spectate_hot_info(global_data.player.uid)

    def _on_update_spectate_hot_info(self, obj_uid, info):
        if global_data.player and global_data.player.uid == obj_uid and info:
            like_cnt = int(info.get('cur_likenum', 0))
            if like_cnt > 0:
                self.set_like_num(like_cnt)

    def modify_btn_report(self):
        pass

    def on_player_setted(self, player):
        self.modify_btn_report()

    @execute_by_mode(False, (game_mode_const.GAME_MODE_EXERCISE,))
    def set_observe_num(self, cnt, name=None):
        if self.is_ob():
            self.panel.btn_observed.setVisible(False)
        else:
            self.panel.btn_observed.setVisible(True)
            cnt = str(cnt)
            self.panel.btn_observed.lab_name.SetString(cnt)
            self.panel.lab_observed.SetString(cnt)
        if name:
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(19168).format(name=name))

    def set_like_num(self, cnt, name=None):
        self.panel.lab_like.SetString(str(cnt))
        if name:
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(19169).format(name=name))

    def on_click_observed_btn(self, *args):
        pass

    def on_enter_observe(self, player):
        self.panel.btn_observed.setVisible(False)
        self.panel.nd_observed_details.setVisible(False)

    def on_keyboard_switch_mic(self, msg, keycode):
        if not self.panel.btn_speak.isVisible():
            return False
        self.communicate_widget.trigger_btn_speaker()

    def on_keyboard_switch_sound(self, msg, keycode):
        if not self.panel.btn_sound.isVisible():
            return False
        self.communicate_widget.trigger_btn_sound()

    def on_keyboard_close_all_list(self, msg, keycode):
        if not (self.panel.list_sound.isVisible() or self.panel.list_speak.isVisible()):
            return False
        self.communicate_widget.close_all_list()

    def on_keyboard_open_chat_dialog(self, msg, keycode):
        global_data.emgr.open_fight_chat_ui_event.emit()

    def on_keyboard_show_spectate_info(self, msg, keycode):
        if not self.panel.btn_observed.isVisible():
            return False
        if self.panel.btn_observed.isVisible():
            self.on_click_observed_btn()
        else:
            nd_detail = self.panel.nd_observed_details
            nd_detail.setVisible(True)

    def exercise_field_modify(self):
        pass

    def pve_field_modify(self):
        pass

    def is_ob(self):
        from logic.gutils import judge_utils
        return judge_utils.is_ob()

    def ob_modify(self):
        pass


class BattleRightTopUI(BattleRightTopBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_right_top'
    UI_ACTION_EVENT = {'btn_set.OnBegin': 'on_click_setting_btn',
       'btn_observed.OnClick': 'on_click_observed_btn',
       'btn_report.OnClick': 'on_click_report_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_setting_ui': {'node': 'btn_set.temp_pc'},'switch_mic': {'node': 'btn_speak.temp_pc'},'switch_speaker': {'node': 'btn_sound.temp_pc'},'show_spectate_info': {'node': 'btn_observed.temp_pc'}}
    if not G_IS_NA_PROJECT:
        GLOBAL_EVENT = BattleRightTopBaseUI.GLOBAL_EVENT.copy()
        GLOBAL_EVENT.update({'update_alive_player_num_event': '_update_alive_player_num'
           })

    def on_init_panel(self, *args, **kwargs):
        self._top_5_nd = None
        super(BattleRightTopUI, self).on_init_panel()
        self.modify_btn_report()
        return

    def on_click_observed_btn(self, *args):
        nd_detail = self.panel.nd_observed_details
        if nd_detail.isVisible():
            nd_detail.setVisible(False)
            self.panel.icon_observe.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/icon_observed.png')
        else:
            nd_detail.setVisible(True)
            self.panel.icon_observe.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/button/btn_close_s.png')
        px, py = self.panel.nd_custom.GetPosition()
        pw, ph = self.panel.nd_custom.GetContentSize()
        w, h = nd_detail.GetContentSize()
        if py < ph + h:
            nd_detail.SetPosition('50%24', '100%30')
        else:
            nd_detail.SetPosition('50%24', '50%-66')

    def on_ctrl_target_changed(self, *args):
        super(BattleRightTopUI, self).on_ctrl_target_changed(*args)
        if G_IS_NA_PROJECT:
            return
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.panel.top_5.SetPosition('100%-80', '100%-84')
        else:
            self.panel.top_5.SetPosition('100%-40', '100%-84')

    def _update_alive_player_num(self, player_num):
        from logic.gcommon.common_utils import battle_utils
        if not battle_utils.is_signal_logic():
            return
        if not global_data.game_mode:
            return
        is_mode_survivals = global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS)
        from logic.gutils.judge_utils import is_ob
        if not is_ob():
            if player_num <= 5 and not self._top_5_nd and is_mode_survivals:
                self._top_5_nd = global_data.uisystem.load_template_create('battle/i_fight_top5', self.panel.top_5)
                self._top_5_nd.PlayAnimation('show')

    def exercise_field_modify(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_EXERCISE):
            self.panel.btn_observed.setVisible(False)
            self.panel.btn_exit.setVisible(True)

            @self.panel.btn_exit.callback()
            def OnClick(*args):

                def on_confirm_quit_exercise():
                    self.close()
                    if global_data.player and global_data.player.logic:
                        global_data.player.logic.send_event('E_QUIT_EXERCISE_FIELD')

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(862009), confirm_callback=on_confirm_quit_exercise)

            self.panel.nd_custom.SetPosition('i24', 'i0')

    def pve_field_modify(self):
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type == game_mode_const.GAME_MODE_PVE_EDIT or mode_type == game_mode_const.GAME_MODE_PVE:
            self.panel.nd_rot.SetPosition('i20', 'i5')

    def is_ob(self):
        from logic.gutils import judge_utils
        return judge_utils.is_ob()

    def ob_modify(self):
        if self.is_ob():
            self.panel.btn_exit.setVisible(False)
            self.panel.btn_speak.setVisible(False)
            self.panel.btn_sound.setVisible(False)
            self.panel.btn_observed.setVisible(False)
            self.panel.btn_report.setVisible(False)

    def init_communicate_widget(self):
        self.communicate_widget = CommunicateWidget(self.panel)

    def leave_screen(self):
        super(BattleRightTopUI, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleRightTopUI')

    def show_only_exit_btn(self):
        self.panel.btn_observed.setVisible(False)
        self.panel.btn_sound.setVisible(False)
        self.panel.btn_speak.setVisible(False)
        self.panel.btn_set.setVisible(False)
        self.panel.btn_exit.setVisible(True)
        self.panel.btn_report.setVisible(False)

    def modify_btn_report(self):
        is_in_global_spectate = global_data.player.is_in_global_spectate() if global_data.player else True
        if check_is_in_competition_battle() and not is_in_global_spectate:
            self.panel.btn_report.setVisible(True)
        else:
            self.panel.btn_report.setVisible(False)

    def on_click_report_btn(self, *args):
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_COMPETITION, REPORT_CLASS_BATTLE
        if check_is_in_competition_battle():
            ui = global_data.ui_mgr.show_ui('RoundCompetitionReportUI', 'logic.comsys.report')
            ui.report_battle_users([], False, False)
            ui.request_report_name_list()
            ui.set_report_class(REPORT_CLASS_BATTLE)
            ui.set_extra_report_info('', '', REPORT_FROM_TYPE_COMPETITION)