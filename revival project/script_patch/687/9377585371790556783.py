# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndSceneUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import math
from .EndSceneUIBase import EndSceneUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.item_utils import get_lobby_item_type
from logic.gutils.settle_scene_utils import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_GESTURE
from logic.gutils.end_statics_utils import get_battle_achieve_text_id
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE
from .GenericSettleWidgets import SettleInputWidget, SettleRankWidget, SettleNameWidget, SettleInteractionWidget
from logic.gutils.new_template_utils import ModeSatSurveyButtonWidget
from logic.gcommon.cdata.round_competition import check_is_in_competition_battle
from common.const import uiconst

def check_data_initialized(func):

    def wrapper(*args, **kwargs):
        global INITIALIZE_TIMER
        if INITIALIZE_TIMER is None:
            func(*args, **kwargs)
        return

    return wrapper


INITIALIZE_TIMER = None

class EndSceneUI(EndSceneUIBase):
    PANEL_CONFIG_NAME = 'end/end_statistics_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = EndSceneUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({'extra_scene_added': 'on_extra_scene_added',
       'change_settle_role_interaction': 'on_change_role_interaction',
       'finish_settle_scene_camera': 'on_finish_settle_scene_camera',
       'player_first_success_share_event': 'on_first_success_share',
       'update_settle_like_info_event': 'on_update_like_info'
       })
    UI_ACTION_EVENT = EndSceneUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'btn_report.OnClick': 'on_click_btn_report',
       'btn_share.btn.OnClick': 'on_click_btn_share',
       'btn_exit.btn.OnClick': 'on_click_btn_exit',
       'base_layer.OnClick': 'on_click_base_layer',
       'btn_share_1.OnClick': 'on_click_share_mvp',
       'btn_left.OnClick': 'on_click_left_btn',
       'btn_right.OnClick': 'on_click_right_btn'
       })
    SHARE_TIPS_INFO = (
     'btn_share.btn', 3154, ('50%', '100%-30'))
    SHOW_ACHIEVE = 0
    SHOW_MODELS = 1
    MATE_SHOW_NUM = 3

    def on_init_panel(self, settle_dict, reward, teammate_num, teammate_info, achievement, is_done, total_fighter_num):
        super(EndSceneUI, self).on_init_panel()
        self.cur_stage = EndSceneUI.SHOW_ACHIEVE
        self.show_details = False
        self.share_content = None
        self.comment_widget = None
        self.name_widget = None
        self.settle_data_widget = None
        self.interaction_widget = None
        self.showing_settle_data = False
        self.eid_to_settle_data_sub_panel = dict()
        self.settle_dict = settle_dict
        self.reward = reward
        self.teammate_num = teammate_num
        self.teammate_info = teammate_info
        self.display_count = len(teammate_info) + 1
        self.achievement_data = achievement
        self.total_fighter_num = total_fighter_num
        self.bg_music = None
        self.history_mate = self.settle_dict.get('history_mate', [])
        self._cur_mate_display_count = None
        self._cur_mate_index = -1
        if not self.history_mate:
            self.max_mate_index = -1
            self.history_mate_eid_list = []
            self.history_mate_info = {}
            self.history_mate_achivement = {}
            self.panel.lab_team.setVisible(False)
            self.panel.lab_team_num.setVisible(False)
        else:
            self.history_mate_info = self.history_mate[0] or {}
            self.history_mate_achivement = self.history_mate[1] or {}
            self.max_mate_index = int(math.ceil(len(self.history_mate_info) / float(self.MATE_SHOW_NUM))) - 1
            self.history_mate_eid_list = sorted(six_ex.keys(self.history_mate_info))
            self.panel.lab_team_num.SetString('1/%d' % (self.max_mate_index + 2))
            self.panel.lab_team.setVisible(True)
            self.panel.lab_team_num.setVisible(True)
        self._has_requested_uids = set()
        self.model_loader = SettleSceneModelLoader()
        self.model_loader.set_parameters(settle_dict, teammate_info, 0.85, 1.2)
        self.screen_capture_helper = ScreenFrameHelper()
        self.init_widgets()
        self.hide()
        return

    def init_widgets(self):
        global INITIALIZE_TIMER
        INITIALIZE_TIMER = None
        if not global_data.player or not global_data.player.logic:
            if self.panel and self.panel.isValid():
                INITIALIZE_TIMER = global_data.game_mgr.register_logic_timer(self.init_widgets, interval=1, times=1)
            return
        else:
            self.mate_name_widget = None
            self.history_mate_settle_data_widget = None
            self.share_content = None
            self.comment_widget = ModeSatSurveyButtonWidget(self.panel.btn_comment)
            self.rank_widget = SettleRankWidget(self, self.settle_dict.get('rank', 99), self.total_fighter_num)
            self._init_name_widgets()
            self._init_settle_data_widget()
            self.input_widget = SettleInputWidget(self, self.panel.btn_chat, self.panel.btn_send, self.display_count)
            self._init_button_list()
            self._init_interaction_widget()
            self.show_btn_again()
            return

    def _init_name_widgets(self):
        eid_list, name_str_list, uid_list, mvp_list, priv_settings_list = (list(), list(), list(), list(), list())
        eid_list.append(global_data.player.id)
        name_str_list.append(global_data.player.logic.ev_g_char_name())
        uid_list.append(global_data.player.uid)
        is_mvp = self.settle_dict.get('mvp', False)
        mvp_id = self.settle_dict.get('mvp_id', None)
        mvp_list.append(is_mvp)
        priv_settings_list.append(global_data.player.get_privilege_setting())
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        for eid in six.iterkeys(self.teammate_info):
            eid_list.append(eid)
            name_str_list.append(groupmate_info.get(eid, {}).get('char_name', ''))
            uid_list.append(groupmate_info.get(eid, {}).get('uid', None))
            mvp_list.append(str(eid) == str(mvp_id))
            priv_settings_list.append(self.teammate_info.get(eid, {}).get('priv_settings', {}))

        extra_data = {'priv_settings_list': priv_settings_list
           }
        self.name_widget = SettleNameWidget(eid_list, name_str_list, uid_list=uid_list, mvp_list=mvp_list, extra_info=extra_data)
        return

    def _set_settle_data_lab(self, nd, attr_name, text):
        getattr(nd, attr_name).SetString(str(text))
        getattr(nd, attr_name + '_shadow').SetString(str(text))

    def _set_settle_data_visible(self, nd, attr_name, visible):
        getattr(nd, attr_name).setVisible(visible)
        getattr(nd, attr_name + '_shadow').setVisible(visible)

    def _init_settle_data(self, nd, uid, eid, name, score, statistics, achievement_list, hide_like=False):
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid
        if not G_IS_NA_USER:
            nd.lab_time_title_1.SetString(82013)
            nd.lab_time_title_1_shadow.SetString(82013)
        if hide_like:
            nd.btn_like.setVisible(False)

        @nd.btn_like.unique_callback()
        def OnClick(btn, *args):
            can_like_player = global_data.player.like_player_after_settle(eid)
            if can_like_player:
                btn.SetEnable(False)
                btn.SetSelect(True)
                btn.icon_like.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/icon_praise_sel.png')

        if global_data.message_data.is_friend(uid):
            nd.btn_add.setVisible(False)
        elif uid in self._has_requested_uids:
            nd.btn_add.SetEnable(False)
            nd.btn_add.SetSelect(True)
            nd.btn_add.icon_add_friend.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/icon_addfriend_sel.png')
        else:

            @nd.btn_add.unique_callback()
            def OnClick(btn, *args):
                self._has_requested_uids.add(uid)
                global_data.player.req_add_friend(uid)
                btn.SetEnable(False)
                btn.SetSelect(True)
                btn.icon_add_friend.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/icon_addfriend_sel.png')

        self.eid_to_settle_data_sub_panel[eid] = nd
        show_intimacy = init_intimacy_icon_with_uid(nd.temp_intimacy, uid)
        self._set_settle_data_visible(nd.bar_name, 'lab_name', not show_intimacy)
        self._set_settle_data_visible(nd.temp_intimacy, 'lab_name', show_intimacy)
        self._set_settle_data_lab(nd.temp_intimacy if show_intimacy else nd.bar_name, 'lab_name', name)
        self._set_settle_data_lab(nd, 'lab_point', '%.1f' % (score,))
        self._set_settle_data_lab(nd, 'lab_ruin_mech', statistics.get(statistics_const.KILL_MECHA, 0))
        self._set_settle_data_lab(nd, 'lab_kill', statistics.get(statistics_const.KILL_HUMAN, 0))
        damage = statistics.get(statistics_const.HUMAN_DAMAGE, 0) + statistics.get(statistics_const.MECHA_DAMAGE, 0) + statistics.get(statistics_const.MECHA_TRANS_DAMAGE, 0)
        damage = int(damage)
        self._set_settle_data_lab(nd, 'lab_injure', damage)
        if statistics_const.SURVIVAL_TIME not in statistics:
            self._set_settle_data_visible(nd, 'lab_time_title_0', True)
            self._set_settle_data_visible(nd, 'lab_time_title_1', False)
            self._set_settle_data_visible(nd, 'lab_time', False)
        else:
            survival_min = str(int(statistics.get(statistics_const.SURVIVAL_TIME, 0)) // 60)
            survival_sec = str(int(statistics.get(statistics_const.SURVIVAL_TIME, 0)) % 60)
            lab_time_str = survival_min + 'min' + survival_sec + 's'
            self._set_settle_data_lab(nd, 'lab_time', lab_time_str)
        if achievement_list:
            nd.nd_1.setVisible(True)
            count = len(achievement_list)
            if count == 1:
                nd.nd_1.btn_achieve_more.setVisible(False)
            else:
                nd.nd_1.btn_achieve_more.lab_achieve.SetString(str(count))
                nd.nd_more.list_achieve.SetInitCount(count)
                for i in range(count):
                    nd_achieve = nd.nd_more.list_achieve.GetItem(i)
                    self._set_settle_data_lab(nd_achieve, 'lab_achievement', get_text_by_id(get_battle_achieve_text_id(achievement_list[i])))

                original_height = nd.bar.getContentSize().height

                @nd.nd_1.btn_achieve_more.unique_callback()
                def OnClick(*args):
                    nd.nd_1.setVisible(False)
                    nd.nd_more.setVisible(True)
                    nd.bar.SetContentSize('100%', '100%')
                    nd.bar.ChildResizeAndPosition()

                @nd.nd_more.btn_achieve_less.unique_callback()
                def OnClick(*args):
                    nd.nd_1.setVisible(True)
                    nd.nd_more.setVisible(False)
                    nd.bar.SetContentSize('100%', original_height)
                    nd.bar.ChildResizeAndPosition()

            self._set_settle_data_lab(nd.nd_1.temp_achieve, 'lab_achievement', get_text_by_id(get_battle_achieve_text_id(achievement_list[0])))
        else:
            nd.nd_1.setVisible(False)

    def _init_settle_data_widget(self):
        self.panel.temp_data.setVisible(True)
        self.settle_data_widget = global_data.uisystem.load_template_create(SETTLE_DATE_WIDGET.format(self.display_count), parent=self.panel.temp_data)
        self_nd = self.settle_data_widget.temp_player1
        self_statistics = self.settle_dict.get('statistics', {})
        self_name = global_data.player.logic.ev_g_char_name()
        self_score = self.settle_dict.get('settle_score', {}).get('score', 0)
        self.eid_to_settle_data_sub_panel[global_data.player.id] = self_nd
        self._init_settle_data(self_nd, global_data.player.uid, global_data.player.id, self_name, self_score, self_statistics, self.achievement_data.get(global_data.player.id, []))
        self_nd.btn_like.setVisible(False)
        self_nd.btn_like.SetEnable(False)
        self_nd.btn_like.SetSelect(True)
        self_nd.btn_like.icon_like.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/icon_praise_sel.png')
        self_nd.btn_add.setVisible(False)
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        teammate_eid_list = six_ex.keys(self.teammate_info)
        for i in range(self.display_count - 1):
            nd = getattr(self.settle_data_widget, 'temp_player{}'.format(i + 2))
            eid = teammate_eid_list[i]
            name = groupmate_info.get(eid, {}).get('char_name', '')
            score = self.teammate_info[eid].get('settle_score', {}).get('score', 0)
            self._init_settle_data(nd, self.teammate_info[eid]['uid'], eid, name, score, self.teammate_info[eid].get('statistics', {}), self.achievement_data.get(eid, []))

        self.settle_data_widget.setVisible(False)

    def _init_interaction_widget(self):

        def touch_cb(on):
            if self._cur_mate_index == -1:
                self.showing_settle_data and self.settle_data_widget.setVisible(not on)
                not self.showing_settle_data and self.name_widget.set_visible(not on)

        self.interaction_widget = SettleInteractionWidget(self.btn_emote, lambda : touch_cb(True), lambda : touch_cb(False))

    def _init_button_list(self):
        self.btn_emote = self.panel.list_function.GetItem(0).btn
        self.panel.list_function.GetItem(1).btn.BindMethod('OnClick', self.on_click_btn_clear)
        from logic.comsys.report.UserReportUI import UserReportUI
        report_target_list = UserReportUI.get_possible_report_targets()
        if not report_target_list:
            self.panel.btn_report.setVisible(False)
        self.panel.list_function.setVisible(False)

    def on_finalize_panel(self):
        global INITIALIZE_TIMER
        if INITIALIZE_TIMER:
            global_data.game_mgr.unregister_logic_timer(INITIALIZE_TIMER)
            INITIALIZE_TIMER = None
        if self.share_content:
            self.share_content.destroy()
            self.share_content = None
        self.destroy_widget('mate_name_widget')
        self.destroy_widget('mate_settle_widget')
        self.destroy_widget('name_widget')
        self.destroy_widget('comment_widget')
        self.destroy_widget('rank_widget')
        self.settle_data_widget = None
        self.destroy_widget('interaction_widget')
        self.destroy_widget('input_widget')
        self.model_loader and self.model_loader.on_destroy()
        self.model_loader = None
        if self.screen_capture_helper:
            self.screen_capture_helper.destroy()
            self.screen_capture_helper = None
        self.eid_to_settle_data_sub_panel = None
        if self.bg_music:
            global_data.sound_mgr.stop_playing_id(self.bg_music)
            self.bg_music = None
        super(EndSceneUI, self).on_finalize_panel()
        return

    def on_extra_scene_added(self, scene_type):
        if scene_type not in (SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE):
            return
        global_data.emgr.hide_screen_effect.emit('DarkCornerEffect')
        global_data.emgr.hide_screen_effect.emit('GrayEffect')
        global_data.emgr.scene_stop_poison_circle.emit()
        remove_sfx_for_rank(self, self.settle_dict.get('rank', 99))
        self.model_loader.load_role_mecha_models()
        for ui_name in HIDE_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            ui and ui.panel.setVisible(False)

    def on_change_role_interaction(self, eid, item_no):
        index = self.model_loader.get_role_model_index(eid)
        if index != -1:
            item_type = get_lobby_item_type(item_no)
            if item_type == L_ITEM_TYPE_EMOTICON:
                global_data.emgr.change_model_display_emoji.emit(item_no, index, True)
            elif item_type == L_ITEM_TYPE_GESTURE:
                global_data.emgr.change_model_display_anim.emit(item_no, index)

    def on_finish_settle_scene_camera(self):
        if not global_data.player.is_in_battle():
            return
        self.rank_widget.reset_position_and_show()
        self.name_widget.reset_position_and_show()
        self.show()
        self.panel.PlayAnimation('appear')

    def on_resolution_changed(self):
        if self.rank_widget:
            self.rank_widget.reset_position_and_show()
        if self.name_widget:
            self.name_widget.reset_position_and_show()
        if self.mate_name_widget:
            self.mate_name_widget.reset_position_and_show()

    def on_first_success_share(self):
        from logic.gutils.share_utils import hide_share_tips
        hide_share_tips(self.panel.btn_share)

    def on_update_like_info(self, like_soul, liked_soul, like_name, liked_name, like_num):
        if liked_soul in self.eid_to_settle_data_sub_panel:
            nd = self.eid_to_settle_data_sub_panel[liked_soul]
            nd.btn_like.setVisible(True)
            self_eid = global_data.player.id
            self_eid in (like_soul, liked_soul) and nd.PlayAnimation('like')
            nd.btn_like.lab_num.SetString(str(like_num))
        msg = '#SB[{}]\xe7\x82\xb9\xe8\xb5\x9e#SW<img="gui/ui_res_2/common/icon/icon_like2.png">#n[{}]#n'.format(like_name, liked_name)
        global_data.emgr.on_recv_danmu_msg.emit(msg)

    def on_click_btn_report(self, btn, touch):
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_END, REPORT_CLASS_BATTLE, REPORT_FROM_TYPE_COMPETITION
        if check_is_in_competition_battle():
            ui = global_data.ui_mgr.show_ui('RoundCompetitionReportUI', 'logic.comsys.report')
            ui.report_battle_users([], False, False)
            ui.request_report_name_list()
            ui.set_report_class(REPORT_CLASS_BATTLE)
            ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
            ui.set_settle_info(self.settle_dict)
        else:
            ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
            ui.report_battle_users([], True, True)
            ui.set_report_class(REPORT_CLASS_BATTLE)
            ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
            ui.set_settle_info(self.settle_dict)

    def _show_btn_list(self, flag):
        anim_name = 'show' if flag else 'disappear'
        for nd_btn in self.panel.list_function.GetAllItem():
            nd_btn.PlayAnimation(anim_name)

    @check_data_initialized
    def on_click_btn_clear(self, btn, *args):
        if self.interaction_widget.selecting_emote:
            return
        if self.showing_settle_data:
            btn.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/end_icon_unclear.png')
            btn.lab.SetString(860010)
            self.settle_data_widget.PlayAnimation('details_disappear')
            if self.history_mate_settle_data_widget:
                self.history_mate_settle_data_widget.PlayAnimation('details_disappear')
        else:
            btn.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/end_icon_clear.png')
            btn.lab.SetString(860009)
            self.settle_data_widget.setVisible(self._cur_mate_index == -1)
            self.settle_data_widget.PlayAnimation('details_appear')
            for i in range(self.display_count):
                nd = getattr(self.settle_data_widget, 'temp_player{}'.format(i + 1))
                nd.PlayAnimation('appear')

        if self.history_mate_settle_data_widget:
            self.history_mate_settle_data_widget.setVisible(self._cur_mate_index != -1)
            self.history_mate_settle_data_widget.PlayAnimation('details_appear')
        if self.history_mate_settle_data_widget:
            for i in range(self._cur_mate_display_count):
                nd = getattr(self.history_mate_settle_data_widget, 'temp_player{}'.format(i + 1))
                nd.PlayAnimation('appear')

        if self._cur_mate_index == -1:
            self.name_widget.set_visible(self.showing_settle_data)
        elif self.mate_name_widget:
            self.mate_name_widget.set_visible(self.showing_settle_data)
        self.showing_settle_data = not self.showing_settle_data

    @check_data_initialized
    def on_click_btn_share(self, *args):
        if self.interaction_widget.selecting_emote:
            return
        hide_ui_names = [
         self.__class__.__name__, 'DanmuLinesUI']
        if self.screen_capture_helper:

            def custom_cb(*args):
                self.panel.btn_report.setVisible(True)
                self.panel.nd_bottom.setVisible(True)
                self.panel.btn_comment.setVisible(True)
                self.on_end_share()

            self.panel.btn_report.setVisible(False)
            self.panel.nd_bottom.setVisible(False)
            self.panel.btn_comment.setVisible(False)
            self.on_begin_share()
            self.screen_capture_helper.take_screen_shot(hide_ui_names, self.panel, custom_cb=custom_cb)

    @check_data_initialized
    def show_btn_again(self):
        if self.settle_dict and self.settle_dict.get('battle_again', False):
            btn_again = self.panel.nd_bottom.btn_again
            btn_again.setVisible(True)
            from logic.comsys.guide_ui.GuideSetting import GuideSetting
            info = GuideSetting().local_battle_data
            if info.get('first_battle_again', False):
                self.panel.PlayAnimation('again')
            else:
                info['first_battle_again'] = True
                GuideSetting().local_battle_data = info
                self.panel.PlayAnimation('arrow')
                self.panel.PlayAnimation('tips_show')

            @btn_again.btn.unique_callback()
            def OnClick(btn, touch):
                if global_data.player:
                    global_data.player.call_soul_method('try_battle_again')
                btn.SetEnable(False)

        else:
            self.panel.nd_bottom.btn_again.setVisible(False)

    @check_data_initialized
    def on_click_btn_exit(self, *args):
        if not self.show_details:
            self.settle_data_widget.setVisible(self._cur_mate_index == -1)
            self.settle_data_widget.PlayAnimation('details_appear')
            for i in range(self.display_count):
                nd = getattr(self.settle_data_widget, 'temp_player{}'.format(i + 1))
                nd.PlayAnimation('appear')

            if self.history_mate_settle_data_widget:
                self.history_mate_settle_data_widget.setVisible(self._cur_mate_index != -1)
                self.history_mate_settle_data_widget.PlayAnimation('details_appear')
                for i in range(self._cur_mate_display_count):
                    nd = getattr(self.history_mate_settle_data_widget, 'temp_player{}'.format(i + 1))
                    nd.PlayAnimation('appear')

            self.panel.list_function.setVisible(True)
            self._show_btn_list(True)
            self.showing_settle_data = True
            self.name_widget.set_visible(False)
            self.show_details = True
            if self.mate_name_widget:
                self.mate_name_widget.set_visible(False)
        else:
            self.settle_data_widget.PlayAnimation('details_disappear')
            if self.history_mate_settle_data_widget:
                self.history_mate_settle_data_widget.PlayAnimation('details_appear')
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            from logic.client.const import game_mode_const
            if global_data.game_mode.get_mode_type() in game_mode_const.GAME_MODE_SURVIVALS:
                SettleSystem().show_settlement_chart_ui(self.settle_dict, self.teammate_info, self.reward, self.achievement_data.get(global_data.player.id, []))
            else:
                SettleSystem().show_settle_exp(self.settle_dict, self.reward)
            self.close()

    def need_show_mvp(self):
        is_mvp = self.settle_dict.get('mvp', False)
        from logic.gutils import judge_utils
        is_ob = judge_utils.is_ob()
        return is_mvp and not is_ob

    def init_mvp_achievement(self):
        from logic.gcommon.common_const import statistics_const as stat_const
        settle_dict = self.settle_dict
        self.panel.temp_achieve.setTouchEnabled(False)
        is_mvp = self.need_show_mvp()
        if is_mvp:
            template_path = 'end/i_statistics_mvp'
            mvp_conf = global_data.uisystem.load_template(template_path)
            nd_mvp = self.panel.temp_achieve.AddItem(mvp_conf)
            mvp_count = global_data.player.get_achieve_stat(self.get_battle_type(), stat_const.GET_MVP)
            self.panel.PlayAnimation('next')
            nd_mvp.lab_times.SetString(str(mvp_count))
            nd_mvp.PlayAnimation('show')
            global_data.sound_mgr.play_ui_sound('mvp_open')

    def init_achievement(self):
        is_mvp = self.need_show_mvp()
        if is_mvp:
            self.show()
            self.rank_widget.set_visible(False)
            self.name_widget.set_visible(False)
            self.init_mvp_achievement()
        else:
            self.on_click_base_layer(None)
        return

    def on_click_base_layer(self, *args):
        if self.cur_stage == EndSceneUI.SHOW_ACHIEVE:
            global_data.emgr.start_settle_scene_camera.emit()
            is_mvp = self.need_show_mvp()
            if is_mvp:
                self.panel.StopAnimation('next')
                self.panel.PlayAnimation('disappear_achieve')
            self.cur_stage = EndSceneUI.SHOW_MODELS
            if self.history_mate_info:
                self.panel.btn_left.setVisible(True)
                self.panel.btn_right.setVisible(True)

    def begin_show(self):
        self.init_achievement()

    def on_click_share_mvp(self, btn, touch):
        from logic.comsys.share.MVPShareCreator import MVPShareCreator
        share_creator = MVPShareCreator()
        share_creator.create()
        share_content = share_creator
        mvp_info = global_data.battle or {} if 1 else global_data.battle.get_global_mvp_info()
        share_content.set_mvp_info(mvp_info, True)
        share_content.update_ui_bg_sprite()
        self_statistics = self.settle_dict.get('statistics', {})
        kill_mecha = self_statistics.get(statistics_const.KILL_MECHA, 0)
        kill_human = self_statistics.get(statistics_const.KILL_HUMAN, 0)
        data = [('gui/ui_res_2/share/icon_destory.png', 10236, str(kill_mecha)), ('gui/ui_res_2/share/icon_driver.png', 10237, str(kill_human))]
        share_content.set_battle_score(data)
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI().set_share_content_raw(share_content.get_render_texture(), share_content=share_content)

    def on_click_left_btn(self, btn, touch):
        if self.interaction_widget.selecting_emote:
            return
        if self._cur_mate_index == -1:
            self._cur_mate_index = self.max_mate_index
        elif self._cur_mate_index == 0:
            self._cur_mate_index = -1
        else:
            self._cur_mate_index -= 1
        self.show_mate_with_index()

    def on_click_right_btn(self, btn, touch):
        if self.interaction_widget.selecting_emote:
            return
        if self._cur_mate_index == -1:
            self._cur_mate_index = 0
        elif self._cur_mate_index == self.max_mate_index:
            self._cur_mate_index = -1
        else:
            self._cur_mate_index += 1
        self.show_mate_with_index()

    def show_mate_with_index(self):
        if self.mate_name_widget:
            self.mate_name_widget.destroy()
            self.mate_name_widget = None
        if self._cur_mate_index == -1:
            self.model_loader.load_role_mecha_models()
            self.panel.lab_team_num.SetString('1/%d' % (self.max_mate_index + 2))
            self.name_widget.set_visible(not self.showing_settle_data)
            self.settle_data_widget.setVisible(self.showing_settle_data)
            if self.history_mate_settle_data_widget:
                self.history_mate_settle_data_widget.setVisible(False)
            if self.btn_emote:
                self.btn_emote.setVisible(True)
        else:
            eids = self.history_mate_eid_list[self._cur_mate_index * self.MATE_SHOW_NUM:(self._cur_mate_index + 1) * self.MATE_SHOW_NUM]
            self.model_loader.load_history_role_mecha_models(eids, self.history_mate_info)
            self.panel.lab_team_num.SetString('%d/%d' % (self._cur_mate_index + 2, self.max_mate_index + 2))
            self.name_widget.set_visible(False)
            self.settle_data_widget.setVisible(False)
            self.init_history_mate_name_widget(eids)
            self._init_history_settle_data_widget(eids)
            if self.mate_name_widget:
                self.mate_name_widget.reset_position_and_show()
            if self.mate_name_widget:
                self.mate_name_widget.set_visible(not self.showing_settle_data)
            if self.history_mate_settle_data_widget:
                self.history_mate_settle_data_widget.setVisible(self.showing_settle_data)
            if self.btn_emote:
                self.btn_emote.setVisible(False)
        return

    def init_history_mate_name_widget(self, eid_list):
        name_str_list = []
        uid_list = []
        mvp_list = []
        priv_settings_list = []
        mvp_id = self.settle_dict.get('mvp_id', None)
        for eid in eid_list:
            groupmate_info = self.history_mate_info
            name_str_list.append(groupmate_info.get(eid, {}).get('char_name', ''))
            uid_list.append(groupmate_info.get(eid, {}).get('uid', None))
            mvp_list.append(str(eid) == str(mvp_id))
            priv_settings_list.append(groupmate_info.get(eid, {}).get('priv_settings', {}))

        extra_data = {'priv_settings_list': priv_settings_list
           }
        self.mate_name_widget = SettleNameWidget(eid_list, name_str_list, uid_list=uid_list, mvp_list=mvp_list, extra_info=extra_data)
        return

    def _init_history_settle_data_widget(self, eids):
        if not eids:
            return
        else:
            display_count = len(eids)
            if self._cur_mate_display_count != display_count:
                if self.history_mate_settle_data_widget:
                    self.history_mate_settle_data_widget.Destroy()
                    self.history_mate_settle_data_widget = None
                settle_data_widget = global_data.uisystem.load_template_create(SETTLE_DATE_WIDGET.format(display_count), parent=self.panel.temp_data)
            else:
                settle_data_widget = self.history_mate_settle_data_widget
            self._cur_mate_display_count = display_count
            for i in range(display_count):
                nd = getattr(settle_data_widget, 'temp_player{}'.format(i + 1))
                eid = eids[i]
                groupmate_info = self.history_mate_info.get(eid, {})
                name = groupmate_info.get('char_name', '')
                score = groupmate_info.get('settle_score', {}).get('score', 0)
                self._init_settle_data(nd, groupmate_info['uid'], eid, name, score, groupmate_info.get('statistics', {}), self.history_mate_achivement.get(eid, []), hide_like=True)

            self.history_mate_settle_data_widget = settle_data_widget
            settle_data_widget.setVisible(False)
            return