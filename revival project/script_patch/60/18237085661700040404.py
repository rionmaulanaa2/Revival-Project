# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, BG_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import mecha_const
from logic.client.const import game_mode_const
from common.utils.ui_utils import get_scale
from logic.gutils.ui_salog_utils import add_uiclick_salog
from common.const import uiconst
from logic.gutils.mecha_utils import calc_mecha_acc_charing_target_progress
from logic.gcommon import time_utility
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.utility import dummy_cb
from logic.gutils.item_utils import get_mecha_role_pic, get_mecha_name_by_id, get_mecha_middle_pic
from logic.gutils import pc_utils
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.common_const import battle_const
import logic.gcommon.time_utility as tutil
import math
import cc
import game
import nxapp

def on_mecha_call_decorator(func):

    def wrapped(*args, **kwargs):
        if global_data.game_mode:
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
                from logic.gcommon.common_const.battle_const import ROUND_TYPE_MECHA
                if global_data.improvise_battle_data and global_data.improvise_battle_data.get_round_type() != ROUND_TYPE_MECHA:
                    return
                if global_data.improvise_battle_data and not global_data.improvise_battle_data.is_operable():
                    return
        return func(*args, **kwargs)

    return wrapped


class MechaBaseUI(BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_mech_call.btn_mech_call.OnClick': 'on_mecha_call',
       'temp_mech_call.btn_mech_call.OnDrag': 'on_drag_mecha_btn',
       'temp_mech_call.btn_mech_call.OnEnd': 'on_touch_end_mecha_btn'
       }
    HOT_KEY_FUNC_MAP = {'open_quick_summon_preview.PRESS': 'keyboard_quick_summon_preview_random',
       'open_quick_summon_preview.CANCEL': 'keyboard_quick_summon_preview_random_cancel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'summon_call_mecha': {'node': 'temp_mech_call.temp_pc'}}

    def init(self, parent=None, *arg, **kwargs):
        if global_data.player.in_local_battle() or global_data.player.in_new_local_battle():
            self.on_mecha_call = self._on_mecha_call
        else:
            self.on_mecha_call = self.on_mecha_call_exc
        self._temp_mech_call_original_pos_y = 0
        super(MechaBaseUI, self).init(parent=parent, *arg, **kwargs)

    def on_init_panel(self):
        from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.enough_panel_ui = global_data.ui_mgr.create_simple_dialog('battle_mech/mech_call_enough', BG_ZORDER, UI_VKB_TYPE=uiconst.UI_VKB_NO_EFFECT)
        self.init_parameters()
        self.init_custom_com()
        self.init_angle_list()
        global_data.emgr.on_init_mecha_ui.emit()
        if self.need_show_signal:
            self._temp_mech_call_original_pos_y = self.panel.temp_mech_call.getPosition().y
            self.panel.temp_mech_call.setPositionY(self.panel.temp_mech_call.getPosition().y + 15)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_angle_list(self):
        per_item_angle = math.pi * 2 / 6
        half_item_angle = per_item_angle / 2
        self.angle_list = [[(-half_item_angle - per_item_angle, -half_item_angle)], [(-half_item_angle, 0), (0, half_item_angle)], [(half_item_angle, half_item_angle + per_item_angle)]]

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        self.enter_quick_call_mode = False
        self.destroy_widget('custom_ui_com')
        self.on_mecha_call = dummy_cb
        if self.enough_panel_ui:
            self.enough_panel_ui.close()
            self.enough_panel_ui = None
        return

    def init_parameters(self):
        self.cur_mecha_lv = 1
        self.player = None
        self.get_mecha_cd_timer = None
        self.get_mecha_count_down = 0
        self.get_mecha_total_cd = mecha_const.RECALL_MAXCD_TYPE_GETMECHA
        self.get_mecha_count_down_progress = 0
        self.lerp_time = 0.5
        self.speed_rate = 1
        self.speed_up = mecha_const.RECALL_MAXCD_TYPE_GETMECHA / 2
        self.icon_mech_path = ''
        self.battle_type = global_data.game_mode.get_mode_type()
        self.quick_call_mecha_btn = {}
        self.quick_call_mecha_ids = []
        self.selected_mecha_id = None
        self.enter_quick_call_mode = False
        self.angle_list = []
        self.panel.temp_mech_call.progress_mech_loop.SetPercentage(0)
        self.panel.temp_mech_call.progress_mech_call.SetPercentage(0)
        pos_x, pos_y = self.panel.temp_mech_call.nd_charge_custom.GetPosition()
        self.wheel_center = self.panel.ConvertToWorldSpace(pos_x, pos_y)
        self._mouse_listener = None
        self._acc_charging_timer = None
        self._acc_charging_cur_progress = 0
        self._acc_charging_total_progress = 0
        self._acc_stop_progress = 0
        self._acc_charing_stay_times = 0
        self._has_charging_buff = False
        self._has_charger_stub = False
        self.need_show_signal = battle_utils.is_battle_signal_open()
        player = global_data.cam_lplayer
        if player:
            self.on_player_setted()
        emgr = global_data.emgr
        emgr.scene_camera_player_setted_event += self.on_player_setted
        emgr.scene_player_setted_event += self.on_scene_player_setted
        emgr.on_observer_charging_event += self.on_acc_charging
        emgr.update_random_mecha_list += self.refresh_random_mecha_icon
        return

    def on_scene_player_setted(self, player):
        if not player:
            self.close()

    def on_player_setted(self):
        player = global_data.cam_lplayer
        self.unbind_ui_event(self.player)
        self.player = player
        if player:
            self.init_speed_new_anim()
            self.init_event()
            self.bind_ui_event(self.player)
            self.init_quick_call_mecha_info()

    def init_quick_call_mecha_info(self):
        from logic.units.LAvatar import LAvatar
        if not isinstance(self.player, LAvatar):
            return
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            usual_mecha_ids = global_data.death_battle_data.get_mecha_list()
        else:
            usual_mecha_ids = global_data.player.get_usual_mecha_ids()
        self.quick_call_mecha_ids = usual_mecha_ids
        self._init_quick_call_btn()

    def init_event(self):
        cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
        self.on_update_change_cd(cd_type, total_cd, left_time)
        mecha_exp = self.player.ev_g_mecha_exp_init()
        self.on_mecha_exp_changed(mecha_exp)
        stage = self.player.share_data.ref_parachute_stage
        if stage is not None:
            self.on_parachute_state_changed(stage)
        return

    def bind_ui_event(self, target):
        regist_func = target.regist_event
        regist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
        regist_func('E_MECHA_EXP_CHANGE', self.on_mecha_exp_changed)
        regist_func('E_MECHA_PARACHUCTE_HIDE_START', self.on_hide_parachute_mecha)
        regist_func('S_CALL_MECHA_SPEED_RATE', self.set_speed_rate)
        regist_func('E_ADD_TEAMMATE', self._update_quick_call_btn, 999)
        regist_func('E_DELETE_TEAMMATE', self._update_quick_call_btn, 999)
        regist_func('E_UPDATE_TEAMMATE_INFO', self._update_teammate_info, 999)
        regist_func('E_ON_SELECT_RANDOM_MECHA', self.refresh_random_mecha_icon)
        regist_func('E_PARACHUTE_STATUS_CHANGED', self.on_parachute_state_changed)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
            unregist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
            unregist_func('E_MECHA_EXP_CHANGE', self.on_mecha_exp_changed)
            unregist_func('E_MECHA_PARACHUCTE_HIDE_START', self.on_hide_parachute_mecha)
            unregist_func('S_CALL_MECHA_SPEED_RATE', self.set_speed_rate)
            unregist_func('E_ON_SELECT_RANDOM_MECHA', self.refresh_random_mecha_icon)
            unregist_func('E_PARACHUTE_STATUS_CHANGED', self.on_parachute_state_changed)
            unregist_func('E_ADD_TEAMMATE', self._update_quick_call_btn)
            unregist_func('E_DELETE_TEAMMATE', self._update_quick_call_btn)
            unregist_func('E_UPDATE_TEAMMATE_INFO', self._update_teammate_info)

    def on_parachute_state_changed(self, stage):
        if stage is None:
            return
        else:
            from logic.gcommon.common_utils.parachute_utils import STAGE_LAND
            if stage >= STAGE_LAND:
                self.add_show_count('self_parachute_state_reason')
            else:
                self.add_hide_count('self_parachute_state_reason')
            return

    def can_mecha_call(self, show_tip=True):
        if not self.player:
            return False
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.ev_g_is_in_spectate():
                return False
        if self.player.ev_g_agony():
            if show_tip:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19017))
            return False
        if global_data.player.in_local_battle():
            if self._get_call_mecha_left_time() > 0:
                if show_tip:
                    global_data.game_mgr.show_tip(get_text_by_id(5018))
                return False
        return True

    def _get_call_mecha_left_time(self):
        left_time = min(self.get_mecha_count_down_progress, self.get_mecha_count_down)
        return left_time

    @on_mecha_call_decorator
    def on_mecha_call_exc(self, btn, touch):
        if not self.player:
            return
        else:
            if not self.can_mecha_call():
                return
            self.panel.temp_mech_call.vx.setVisible(False)
            if global_data.game_mode:
                if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SNIPE):
                    from logic.gutils.mecha_utils import summon_mecha_call_back
                    summon_mecha_call_back(self, 8007, True)
                    return
                if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
                    mecha_type = global_data.improvise_battle_data.get_cur_round_mecha_type_id()
                    if mecha_type:
                        from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                        try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=mecha_type, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                        return
                elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                    mecha_type = self.player.ev_g_selected_random_mecha()
                    if mecha_type:
                        from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                        try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=mecha_type, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                        return

            def open_summon(res):
                if not res:
                    return
                if self.check_has_summon_ui_instance():
                    return
                summon_ui_cls = self.get_summon_ui_cls()
                summon_ui_cls(self.panel.temp_mech_call, self.player)

            if self.get_mecha_count_down_progress <= 0.1:
                from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, check_summon_mecha
                try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, force=False, valid_pos=None: check_summon_mecha(ui_obj, None, False, valid_pos, open_summon), False)
            else:
                open_summon(True)
            return

    @on_mecha_call_decorator
    def _on_mecha_call(self, btn, touch):
        return self.on_mecha_call_exc(btn, touch)

    def set_speed_rate(self, rate):
        self.speed_rate = rate

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        left_time = max(0, min(left_time, mecha_const.RECALL_MAXCD_TYPE_GETMECHA))
        self.get_mecha_count_down = left_time
        self.get_mecha_total_cd = total_cd
        if total_cd > 0:
            pass
        else:
            if cd_type < 0:
                self.on_add_mecha_progress(0)
                return
            self.on_add_mecha_progress(100)
            return
        self.clear_mecha_cd_timer()
        if left_time > 0:
            tick_interval = 0.03

            def reset():
                if self and self.is_valid():
                    self.get_mecha_count_down = 0
                    self.get_mecha_count_down_progress = 0
                    if self.get_mecha_cd_timer:
                        self.panel.temp_mech_call.nd_progress.stopAction(self.get_mecha_cd_timer)
                        self.get_mecha_cd_timer = None
                    if not self.panel.temp_mech_call.img_call_enough.isVisible():
                        self.on_add_mecha_progress(100)
                return

            def cb(dt):
                if self.get_mecha_count_down < self.get_mecha_count_down_progress:
                    self.get_mecha_count_down_progress -= tick_interval * self.speed_up * self.speed_rate
                    if self.get_mecha_count_down_progress < self.get_mecha_count_down:
                        self.get_mecha_count_down_progress = self.get_mecha_count_down
                else:
                    self.get_mecha_count_down_progress -= tick_interval * self.speed_rate
                if self.get_mecha_count_down_progress <= 0:
                    reset()
                self.on_add_mecha_progress(100 * (1 - 1.0 * self.get_mecha_count_down_progress / total_cd))

            self.get_mecha_count_down_progress = left_time
            self.get_mecha_cd_timer = self.panel.temp_mech_call.nd_progress.TimerAction(cb, left_time, reset, interval=tick_interval)
        elif left_time <= 0:
            self.on_add_mecha_progress(100)

    def on_add_mecha_progress(self, progress):
        if not self._acc_charging_timer:
            self.panel.temp_mech_call.progress_mech_call.SetPercentage(progress)
        self._acc_stop_progress = progress
        progress = int(progress)
        self.panel.temp_mech_call.lab_percent.SetString('{0}%'.format(int(progress)))
        is_full = progress == 100
        self.panel.temp_mech_call.progress_mech_call.setVisible(not is_full)
        self.panel.temp_mech_call.progress_mech_call_full.setVisible(is_full)
        if is_full:
            self.stop_speed_new_anim()
            self.panel.temp_mech_call.StopAnimation('charge')
            logic = global_data.player.logic if global_data.player else None
            if logic:
                logic.send_event('E_GUIDE_CHARGER_END')
        icon_path = 'gui/ui_res_2/battle/mech/icon_call_mech.png' if is_full else 'gui/ui_res_2/battle/mech/icon_call_mech2.png'
        if self.icon_mech_path != icon_path:
            self.icon_mech_path = icon_path
            mecha_type = self.player.ev_g_selected_random_mecha() if self.player else None
            if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH and mecha_type:
                pic_path = get_mecha_role_pic(mecha_type, True)
                self.panel.temp_mech_call.icon_mech.SetDisplayFrameByPath('', pic_path)
            else:
                self.panel.temp_mech_call.icon_mech.SetDisplayFrameByPath('', icon_path)
            if is_full:
                self.panel.temp_mech_call.PlayAnimation('enough')
                if self.enough_panel_ui:
                    self.enough_panel_ui.panel.setVisible(self.panel.temp_mech_call.IsVisible())
                    wpos = self.panel.temp_mech_call.vx_liz.ConvertToWorldSpacePercentage(50, 50)
                    lpos = self.enough_panel_ui.panel.getParent().convertToNodeSpace(wpos)
                    self.enough_panel_ui.panel.setPosition(lpos)
            else:
                self.panel.temp_mech_call.StopAnimation('enough')
                self.enough_panel_ui.panel.setVisible(False)
        return

    def do_hide_panel(self):
        super(MechaBaseUI, self).do_hide_panel()
        if self.enough_panel_ui:
            self.enough_panel_ui.panel.setVisible(False)

    def do_show_panel(self):
        super(MechaBaseUI, self).do_show_panel()
        if self.enough_panel_ui:
            self.enough_panel_ui.panel.setVisible(self.panel.temp_mech_call.vx_liz.isVisible())

    def on_mecha_exp_changed(self, mecha_exp):
        from logic.gutils import mecha_utils
        self.cur_mecha_lv = mecha_utils.get_mecha_cur_lv(mecha_exp, self.cur_mecha_lv)

    def on_hide_parachute_mecha(self):
        self.panel.temp_mech_call.StopAnimation('show')
        self.panel.temp_mech_call.PlayAnimation('show')

    def on_acc_charging(self, is_charging, bf_data):
        if not self.player:
            return
        if is_charging:
            if not self.panel.temp_mech_call.IsPlayingAnimation('charge'):
                self.panel.temp_mech_call.RecordAnimationNodeState('charge')
                self.panel.temp_mech_call.PlayAnimation('charge')
            if not bf_data:
                self._has_charger_stub = True
            if self.panel.temp_mech_call.IsPlayingAnimation('speed_new'):
                self.stop_speed_new_anim()
        else:
            if not bf_data:
                self._has_charger_stub = False
            else:
                self._has_charging_buff = False
            if not self._has_charger_stub and not self._has_charging_buff:
                self.panel.temp_mech_call.StopAnimation('charge')
                self.panel.temp_mech_call.RecoverAnimationNodeState('charge')
            if self.need_speed_new_anim() and not self.panel.temp_mech_call.IsPlayingAnimation('charge'):
                self.show_speed_new_anim()
            if not bf_data:
                return
            if is_charging and self._acc_charging_timer:
                return
        if is_charging:
            self.panel.temp_mech_call.progress_mech_loop.setVisible(True)
            self._acc_charging_cur_progress = 0
            self._acc_stop_progress = 0
            self._acc_charing_stay_times = 0
            self._acc_charging_total_progress = calc_mecha_acc_charing_target_progress(self.player, bf_data, self.speed_rate)
            remain_time = bf_data.get('duration', 0) - (time_utility.get_server_time() - bf_data.get('add_time', 0))
            if self._acc_charging_total_progress > 0 and remain_time > 0:
                self._show_acc_charging_progress(True, remain_time)
                self._has_charging_buff = True
        else:
            self.panel.temp_mech_call.RecoverAnimationNodeState('charge')
            self.panel.temp_mech_call.vx.setVisible(False)
            self.panel.temp_mech_call.progress_mech_loop.setVisible(False)
            self._show_acc_charging_progress(False, 0)

    def _show_acc_charging_progress(self, is_charging, duration_time):
        tick_interval = 0.02

        def reset():
            if self and self.is_valid():
                self.clear_acc_charging_timer()
                self.panel.temp_mech_call.progress_mech_loop.SetPercentage(self._acc_charging_total_progress)
                self.panel.temp_mech_call.progress_mech_loop.setVisible(False)
                self._acc_charging_total_progress = 0
                self._acc_charging_cur_progress = 0

        def cb(dt):
            if self._acc_charging_total_progress <= 0:
                return
            add_progress = min(tick_interval * self.speed_rate * 40, 0.8)
            if add_progress <= 0:
                add_progress = 0.8
            if self._acc_charing_stay_times > 0:
                if self._acc_charing_stay_times >= 2:
                    self._acc_charging_cur_progress = 0
                    self._acc_charing_stay_times = 0
                else:
                    self._acc_charing_stay_times += 1
            else:
                self._acc_charging_cur_progress += add_progress
                if self._acc_charging_cur_progress - self._acc_stop_progress >= 0:
                    self._acc_charing_stay_times += 1
                    self._acc_charging_cur_progress = self._acc_stop_progress
            self.panel.temp_mech_call.progress_mech_loop.SetPercentage(self._acc_charging_cur_progress)

        if is_charging:
            self._acc_charging_timer = self.panel.temp_mech_call.nd_progress.TimerAction(cb, duration_time, reset, interval=tick_interval)
            self.panel.temp_mech_call.progress_mech_call.SetPercentage(self._acc_charging_total_progress)
        else:
            reset()

    def clear_acc_charging_timer(self):
        if self._acc_charging_timer:
            self.panel.temp_mech_call.nd_progress.stopAction(self._acc_charging_timer)
            self._acc_charging_timer = None
        return

    def clear_mecha_cd_timer(self):
        if self.get_mecha_cd_timer:
            self.panel.temp_mech_call.nd_progress.stopAction(self.get_mecha_cd_timer)
            self.get_mecha_cd_timer = None
        return

    def change_ui_data(self):
        scale_type_adjust_list = []
        pos_type_adjust_list = []
        need_to_adjust_scale_type_nodes = (('temp_mech_call', 'nd_step_13', None), )
        for source_nd_name, target_nd_name, target_scale_nd_name in need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            scale = nd.getScale()
            scale_type_adjust_list.append((w_pos, scale, target_nd_name, target_scale_nd_name))

        no_need_to_adjust_scale_type_nodes = (('temp_mech_call', 'nd_quick_call_mech'), ('temp_mech_call', 'nd_mech_destroy'))
        for source_nd_name, target_nd_name in no_need_to_adjust_scale_type_nodes:
            nd = getattr(self.panel, source_nd_name)
            w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
            pos_type_adjust_list.append((w_pos, None, target_nd_name))

        ret_dict = {'scale_type': scale_type_adjust_list,
           'pos_type': pos_type_adjust_list
           }
        return ret_dict

    def on_drag_mecha_btn(self, btn, touch):
        if not global_data.player:
            return
        else:
            if global_data.player.in_local_battle():
                return
            if global_data.is_local_editor_mode:
                return
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SNIPE, game_mode_const.GAME_MODE_RANDOM_DEATH)):
                return
            tou_wpos = touch.getLocation()
            tou_begin_pos = touch.getStartLocation()
            if tou_wpos.y - tou_begin_pos.y < get_scale('50w'):
                self._cancel_quick_call_select()
                return
            if not self or not self.is_valid() or not self.player or not self.player.is_valid():
                return
            if not self.can_mecha_call(show_tip=False):
                return
            if self._get_call_mecha_left_time() > 0:
                return
            touch_ui_nodes = [
             self.panel.temp_mech_call.temp_quick_call_1, self.panel.temp_mech_call.temp_quick_call_2, self.panel.temp_mech_call.temp_quick_call_3]
            usual_mecha_ids = self.quick_call_mecha_ids
            if len(usual_mecha_ids) != len(touch_ui_nodes):
                log_error('MechaUI on_drag_mecha_btn size of usual_mecha_ids=%s, not equal size of touch_ui_nodes.', usual_mecha_ids)
                return
            if not self.enter_quick_call_mode:
                self.panel.temp_mech_call.nd_quick_call.setVisible(True)
                self.panel.temp_mech_call.PlayAnimation('quick')
                self.enter_quick_call_mode = True
            wpos = self.panel.temp_mech_call.btn_mech_call.getParent().convertToNodeSpace(touch.getLocation())
            for index, node in enumerate(touch_ui_nodes):
                lpos = node.getPosition()
                nw, nh = node.GetContentSize()
                mecha_id = usual_mecha_ids[index]
                mecha_btn = self.quick_call_mecha_btn.get(mecha_id, None)
                if not mecha_btn:
                    log_error('MechaUI on_drag_mecha_btn not mecha_btn for mecha_id=%s.', mecha_id)
                    continue
                if abs(wpos.x - lpos.x) < nw * 0.1 and abs(wpos.y - lpos.y) < nh * 0.1:
                    if not mecha_btn.is_enable():
                        self.panel.temp_mech_call.lab_active.SetString(18231)
                        self.panel.temp_mech_call.lab_active.setVisible(True)
                    elif self.selected_mecha_id != mecha_id:
                        mecha_btn.set_select(True)
                        self.panel.temp_mech_call.lab_active.SetString(81312)
                        self.panel.temp_mech_call.lab_active.setVisible(True)
                        select_nd = mecha_btn.get_btn_nd('select_nd')
                        select_nd and select_nd.PlayAnimation('choose')
                    self.selected_mecha_id = mecha_id
                else:
                    mecha_btn.set_select(False)
                    if mecha_id == self.selected_mecha_id:
                        self.panel.temp_mech_call.lab_active.setVisible(False)
                        self.selected_mecha_id = None

            return

    def _cancel_quick_call_select(self):
        if self.selected_mecha_id is not None and self.selected_mecha_id > 0:
            mecha_btn = self.quick_call_mecha_btn.get(self.selected_mecha_id, None)
            if mecha_btn:
                mecha_btn.set_select(False)
            self.panel.temp_mech_call.lab_active.setVisible(False)
            self.selected_mecha_id = None
        return

    def on_touch_end_mecha_btn(self, layer, touch):
        if not self.enter_quick_call_mode:
            return
        else:
            if self.selected_mecha_id is not None and self.selected_mecha_id > 0:
                mecha_btn = self.quick_call_mecha_btn.get(self.selected_mecha_id, None)
            else:
                mecha_btn = None
            if mecha_btn and mecha_btn.is_enable():
                from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=self.selected_mecha_id, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                add_uiclick_salog('call_mecha', 'from_quick_mecha_list')
            self.panel.temp_mech_call.nd_quick_call.setVisible(False)
            self.enter_quick_call_mode = False
            return

    def refresh_random_mecha_icon(self):
        from logic.units.LAvatar import LAvatar
        if self.battle_type != game_mode_const.GAME_MODE_RANDOM_DEATH:
            return
        else:
            self.panel.temp_mech_call.lab_time.StopTimerAction()
            if self.player:
                mecha_type = self.player.ev_g_selected_random_mecha() if 1 else None
                self.quick_call_mecha_ids = global_data.death_battle_data.get_mecha_list()
                if mecha_type:
                    pic_path = get_mecha_role_pic(mecha_type, True)
                    self.panel.temp_mech_call.icon_mech.SetDisplayFrameByPath('', pic_path)
                    self.panel.temp_mech_call.nd_random_tips.setVisible(False)
                    self.panel.temp_mech_call.PlayAnimation('choose')
                    self.panel.temp_mech_call.nd_charge_custom.setScale(1.0)
                else:
                    if self.quick_call_mecha_ids:
                        self.panel.temp_mech_call.nd_charge_custom.setScale(0.7)
                        self.enter_quick_call_mode or self.panel.temp_mech_call.nd_random_tips.setVisible(True)
                    pc_op_mode = pc_utils.is_pc_control_enable()
                    if pc_op_mode:
                        self.panel.temp_mech_call.lab_random_tips.SetString(get_text_by_id(17253))
                    for i, mecha_id in enumerate(self.quick_call_mecha_ids):
                        idx = i + 1
                        pic_path = get_mecha_middle_pic(mecha_id)
                        node_img = getattr(self.panel.temp_mech_call, 'img_mech_%s' % idx)
                        node_img.img_mech.SetDisplayFrameByPath('', pic_path)
                        btn = getattr(self.panel.temp_mech_call, 'btn_mech_%s' % idx)

                        @btn.unique_callback()
                        def OnClick(btn, touch, select_idx=idx, node_img=node_img, mecha_list=self.quick_call_mecha_ids):
                            select_id = self.quick_call_mecha_ids[select_idx - 1]
                            self.player.send_event('E_CALL_SYNC_METHOD', 'select_random_mecha', (select_id,), True)
                            from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                            try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=select_id, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                            return

            if isinstance(self.player, LAvatar):
                self._init_quick_call_btn()
            return

    def _init_quick_call_btn(self):
        from logic.comsys.battle.MechaSummonUI import CMechaBtn
        ui_nodes = [
         self.panel.temp_mech_call.temp_quick_call_1, self.panel.temp_mech_call.temp_quick_call_2, self.panel.temp_mech_call.temp_quick_call_3]
        lobby_selected_mecha_id = self.player.get_owner().get_lobby_selected_mecha_id()
        usual_mecha_ids = self.quick_call_mecha_ids
        for index, ui_node in enumerate(ui_nodes):
            if index >= len(usual_mecha_ids):
                ui_node.setVisible(False)
                continue
            ui_node.setVisible(True)
            mecha_id = usual_mecha_ids[index]
            mecha_btn = CMechaBtn(ui_node, mecha_id)
            self.quick_call_mecha_btn[mecha_id] = mecha_btn
            mecha_btn.set_mecha_btn_data(mecha_id, True)
            if mecha_id == lobby_selected_mecha_id:
                mecha_btn.set_select(True)
                self.selected_mecha_id = mecha_id

        self._update_quick_call_btn()

    def _update_quick_call_btn(self, *args):
        from logic.gutils.mecha_utils import get_call_valid_mecha_ids
        call_valid_mecha_ids = get_call_valid_mecha_ids(self.player, self.quick_call_mecha_ids)
        for mecha_id, mecha_btn in six.iteritems(self.quick_call_mecha_btn):
            mecha_btn.set_enable(mecha_id in call_valid_mecha_ids)

    def _update_teammate_info(self, member_id, info):
        if 'created_mecha_type' in info:
            self._update_quick_call_btn()

    def is_in_quick_call_mode(self):
        return self.enter_quick_call_mode

    def _can_interact(self):
        if not global_data.player or not global_data.player.logic:
            return False
        if not self.player:
            return False
        return global_data.player.logic.id == self.player.id

    def keyboard_quick_summon_preview_random(self, msg, keycode):
        if not global_data.is_pc_mode:
            return
        if self.battle_type != game_mode_const.GAME_MODE_RANDOM_DEATH:
            return
        if not self.player or self.player.ev_g_selected_random_mecha():
            return
        pc_op_mode = pc_utils.is_pc_control_enable()
        if msg == game.MSG_KEY_DOWN and not self.enter_quick_call_mode:
            self.panel.temp_mech_call.nd_random_tips.setVisible(False)
            self.panel.temp_mech_call.nd_quick_call.setVisible(True)
            self.panel.temp_mech_call.PlayAnimation('quick')
            self.enter_quick_call_mode = True
            if pc_op_mode:
                global_data.mouse_mgr.set_cursor_move_enable(True)
                nxapp.clip_cursor(True)
            self._register_mouse_event()
        else:
            self.panel.temp_mech_call.nd_random_tips.setVisible(True)
            self.panel.temp_mech_call.nd_quick_call.setVisible(False)
            self.on_press_end_mecha_btn()
            self.enter_quick_call_mode = False
            if pc_op_mode:
                global_data.mouse_mgr.set_cursor_move_enable(False)
                nxapp.clip_cursor(False)
            self._unregister_mouse_event()
            self.unregister_mouse_scroll_event()

    def keyboard_quick_summon_preview_random_cancel(self):
        pass

    def _register_mouse_event(self):
        if self._mouse_listener:
            return
        self._mouse_listener = cc.EventListenerMouse.create()
        self._mouse_listener.setOnMouseMoveCallback(self._on_mouse_move)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self.panel.get())

    def _unregister_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return

    def _on_mouse_move(self, event):
        pos = event.getLocationInView()
        self.on_drag(pos)

    def on_drag(self, wpos):
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        wpos.subtract(self.wheel_center)
        angle = wpos.getAngle(cc.Vec2(0, 1))
        self.select_item_ui(angle)

    def select_item_ui(self, angle):
        choose_idx = self.cal_list_id_by_angle(angle)
        touch_ui_nodes = [self.panel.temp_mech_call.temp_quick_call_1, self.panel.temp_mech_call.temp_quick_call_2, self.panel.temp_mech_call.temp_quick_call_3]
        usual_mecha_ids = self.quick_call_mecha_ids
        if len(usual_mecha_ids) != len(touch_ui_nodes):
            log_error('MechaUI on_drag_mecha_btn size of usual_mecha_ids=%s, not equal size of touch_ui_nodes.', usual_mecha_ids)
            return
        else:
            if not self.enter_quick_call_mode:
                self.panel.temp_mech_call.nd_quick_call.setVisible(True)
                self.panel.temp_mech_call.PlayAnimation('quick')
                self.enter_quick_call_mode = True
            for index, node in enumerate(touch_ui_nodes):
                mecha_id = usual_mecha_ids[index]
                mecha_btn = self.quick_call_mecha_btn.get(mecha_id, None)
                if not mecha_btn:
                    log_error('MechaUI on_drag_mecha_btn not mecha_btn for mecha_id=%s.', mecha_id)
                    continue
                if choose_idx == index:
                    if self.selected_mecha_id != mecha_id:
                        mecha_btn.set_select(True)
                        self.panel.temp_mech_call.lab_active.SetString(81312)
                        self.panel.temp_mech_call.lab_active.setVisible(True)
                        select_nd = mecha_btn.get_btn_nd('select_nd')
                        select_nd and select_nd.PlayAnimation('choose')
                        self.selected_mecha_id = mecha_id
                else:
                    mecha_btn.set_select(False)
                    if mecha_id == self.selected_mecha_id:
                        self.panel.temp_mech_call.lab_active.setVisible(False)
                        self.selected_mecha_id = None

            return

    def on_press_end_mecha_btn(self):
        if not self.enter_quick_call_mode:
            return
        else:
            if self.selected_mecha_id > 0:
                mecha_btn = self.quick_call_mecha_btn.get(self.selected_mecha_id, None)
            else:
                mecha_btn = None
            if mecha_btn and mecha_btn.is_enable():
                from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                self.player.send_event('E_CALL_SYNC_METHOD', 'select_random_mecha', (self.selected_mecha_id,), True)
                try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=self.selected_mecha_id, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
                add_uiclick_salog('call_mecha', 'from_quick_mecha_list')
            self.panel.temp_mech_call.nd_quick_call.setVisible(False)
            self.enter_quick_call_mode = False
            return

    def cal_list_id_by_angle(self, angle):
        for idx, angle_range_list in enumerate(self.angle_list):
            for angle_range in angle_range_list:
                if angle_range[0] <= angle < angle_range[1]:
                    return idx

        return 9999

    def init_speed_new_anim(self):
        self.panel.temp_mech_call.RecordAnimationNodeState('speed_new')
        if self.need_speed_new_anim():
            self.show_speed_new_anim()

    def show_speed_new_anim(self):
        self.panel.temp_mech_call.PlayAnimation('speed_new')

    def stop_speed_new_anim(self):
        self.panel.temp_mech_call.StopAnimation('speed_new')
        self.panel.temp_mech_call.RecoverAnimationNodeState('speed_new')

    def need_speed_new_anim(self):
        if not self.player:
            return False
        else:
            if not global_data.player or not global_data.player.logic:
                return False
            if global_data.player.logic.ev_g_spectate_target():
                return False
            battle = global_data.player.get_battle()
            if not battle:
                return False
            if not battle_utils.is_beginner_battle_type(int(battle.get_battle_tid())):
                return False
            if self.player.ev_g_mecha_recall_times() == 0 and global_data.player.get_total_cnt() == 0 and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                return True
            return False

    def on_change_ui_custom_data(self):
        if self.need_show_signal:
            if self.panel.temp_mech_call.getPosition().y <= self._temp_mech_call_original_pos_y:
                self.panel.temp_mech_call.setPositionY(self.panel.temp_mech_call.getPosition().y + 15)
        if self.enough_panel_ui:
            wpos = self.panel.temp_mech_call.vx_liz.ConvertToWorldSpacePercentage(50, 50)
            lpos = self.enough_panel_ui.panel.getParent().convertToNodeSpace(wpos)
            self.enough_panel_ui.panel.setPosition(lpos)
            self.enough_panel_ui.panel.setScale(self.panel.temp_mech_call.nd_charge_custom.getScale())
            self.enough_panel_ui.panel.SetEnableCascadeOpacityRecursion(True)
            self.enough_panel_ui.panel.setOpacity(self.panel.temp_mech_call.nd_charge_custom.getOpacity())

    def set_mecha_btn_ban_img_visible(self, visible):
        self.panel.temp_mech_call.img_broken.setVisible(visible)

    def get_summon_ui_cls(self):
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_WITH_MECHA_SKIN_CHANGE
        from logic.gcommon.common_const import ui_operation_const as uoc
        player = global_data.player
        battle = global_data.battle
        setting_open = player and player.get_setting_2(uoc.CHANGE_MECHA_SKIN_IN_BATTLE)
        enable_mecha_redress = player and player.logic and player.logic.ev_g_enable_mecha_redress()
        specify_play_type = battle and battle.get_battle_tid() and get_play_type_by_battle_id(battle.get_battle_tid()) in PLAY_TYPE_WITH_MECHA_SKIN_CHANGE
        can_choose_skin = setting_open and enable_mecha_redress and specify_play_type
        if can_choose_skin:
            from logic.comsys.battle.MechaSummonAndChooseSkinUI import MechaSummonAndChooseSkinUI
            return MechaSummonAndChooseSkinUI
        else:
            from logic.comsys.battle.MechaSummonUI import MechaSummonUI
            return MechaSummonUI

    def check_has_summon_ui_instance(self):
        if global_data.ui_mgr.get_ui('MechaSummonUI') or global_data.ui_mgr.get_ui('MechaSummonAndChooseSkinUI'):
            return True
        return False


class MechaUI(MechaBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_mech_call'

    def add_show_count(self, key='_default', count=1, is_check=True):
        super(MechaUI, self).add_show_count(key, count, is_check)

    def add_hide_count(self, key='_default', count=1, no_same_key=True, is_check=True):
        super(MechaUI, self).add_hide_count(key, count, no_same_key, is_check)