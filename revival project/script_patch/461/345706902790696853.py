# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/FFAEndSceneUI.py
from __future__ import absolute_import
import six
import six_ex
from .EndSceneUIBase import EndSceneUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.item_utils import get_lobby_item_type
from logic.gutils.settle_scene_utils import *
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_GESTURE
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from .GenericSettleWidgets import SettleInputWidget, SettleRankWidget, SettleNameWidget, SettleInteractionWidget
from logic.gutils.new_template_utils import ModeSatSurveyButtonWidget
from logic.gutils.role_head_utils import init_role_head, init_mecha_head
from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE
from bson.objectid import ObjectId
from common.const import uiconst

class FFAEndSceneUI(EndSceneUIBase):
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
       'btn_exit.btn.OnClick': 'on_click_btn_exit'
       })
    SHARE_TIPS_INFO = (
     'btn_share.btn', 3154, ('50%', '100%-30'))

    def on_init_panel(self, settle_dict, reward, teammate_num, teammate_info, total_fighter_num):
        super(FFAEndSceneUI, self).on_init_panel()
        self.show_details = False
        self.share_content = None
        self.comment_widget = None
        self.name_widget = None
        self.settle_data_widget = None
        self.interaction_widget = None
        self.showing_settle_data = False
        self.self_liked = False
        self.eid_to_settle_data_sub_panel = dict()
        self.settle_dict = settle_dict
        self.reward = reward
        self.teammate_num = teammate_num
        self.teammate_info = teammate_info
        self.total_fighter_num = total_fighter_num
        self.display_count = len(teammate_info) + 1
        self.bg_music = None
        self.model_loader = SettleSceneModelLoader()
        self.model_loader.set_parameters(settle_dict, teammate_info, 0.85, 1.2, show_role_model=False)
        self.screen_capture_helper = ScreenFrameHelper()
        self.init_widgets()
        self.hide()
        return

    def init_widgets(self):
        self.share_content = None
        self.comment_widget = ModeSatSurveyButtonWidget(self.panel.btn_comment)
        self.rank_widget = SettleRankWidget(self, self.settle_dict.get('rank', 99), self.total_fighter_num)
        self._init_name_widgets()
        self._init_settle_data_widget()
        self.input_widget = SettleInputWidget(self, self.panel.btn_chat, self.panel.btn_send, 2)
        self._init_button_list()
        self._init_interaction_widget()
        return

    def _init_name_widgets(self):
        eid_list, name_str_list, uid_list, mecha_id_list, priv_settings_list = (
         list(), list(), list(), list(), list())
        eid_list.append(global_data.player.id)
        uid_list.append(global_data.player.uid)
        name_str_list.append(global_data.player.logic.ev_g_char_name())
        mecha_id_list.append(global_data.battle.chosen_mecha_id)
        priv_settings_list.append(global_data.player.get_privilege_setting())
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        for eid in six.iterkeys(self.teammate_info):
            eid_list.append(eid)
            name_str_list.append(groupmate_info.get(eid, {}).get('char_name', ''))
            uid_list.append(groupmate_info.get(eid, {}).get('uid', None))
            mecha_id_list.append(self.teammate_info[eid]['mecha_id'])
            priv_settings_list.append(self.teammate_info[eid].get('priv_settings', {}))

        extra_data = {'priv_settings_list': priv_settings_list
           }
        self.name_widget = SettleNameWidget(eid_list, name_str_list, uid_list=uid_list, mecha_id_list=mecha_id_list, extra_info=extra_data)
        return

    def _init_item_like_and_add_btn(self, item_nd, eid, uid):
        item_nd.btn_like.lab_num.setVisible(False)
        is_self = global_data.player.id == eid
        item_nd.btn_like.setVisible(not is_self)
        item_nd.btn_like.SetEnable(not is_self)
        item_nd.btn_add.setVisible(not is_self)
        if not is_self:
            if global_data.message_data.is_friend(uid):
                item_nd.btn_add.setVisible(False)
            else:

                @item_nd.btn_add.unique_callback()
                def OnClick(btn, *args):
                    global_data.player.req_add_friend(uid)
                    btn.SetEnable(False)
                    btn.SetSelect(True)

            @item_nd.btn_like.unique_callback()
            def OnClick(btn, *args):
                global_data.player.like_player_after_settle(eid)
                btn.SetEnable(False)
                btn.SetSelect(True)

    def _init_settle_data_widget(self):
        self.panel.temp_ffa.setVisible(True)
        self.settle_data_widget = global_data.uisystem.load_template_create(FFA_SETTLE_DATA_WIDGET.format(self.display_count, self.display_count), parent=self.panel.temp_ffa)
        self.settle_data_widget.setVisible(False)
        rank_data = self.settle_dict.get('group_rank_data', [])
        nd_list = self.settle_data_widget.list_score
        nd_list.SetInitCount(len(rank_data))
        my_group_id = global_data.cam_lplayer.ev_g_group_id()
        my_eid = global_data.cam_lplayer.id
        for index, widget in enumerate(nd_list.GetAllItem()):
            rank, group_id, group_point, dict_data = rank_data[index]
            total_damage = 0
            for e_index, eid in enumerate(six_ex.keys(dict_data)):
                eid, uid, name, head_photo, head_frame, kill_num, kill_mecha_num, points, has_buff, mecha_id, human_damage, mecha_damage = dict_data[eid]
                total_damage += human_damage + mecha_damage
                eid = ObjectId(eid)
                item_nd = getattr(widget, 'nd_player_{}'.format(e_index + 1))
                nd_stat = getattr(item_nd, 'nd_stat%d' % (e_index + 1))
                if mecha_id:
                    init_mecha_head(item_nd.temp_head, head_frame, mecha_id)
                else:
                    init_role_head(item_nd.temp_head, head_frame, head_photo)
                item_nd.lab_name.SetString(name)
                nd_stat.lab_mech.SetString(str(kill_mecha_num))
                is_my = my_eid == eid
                item_nd.lab_name.SetColor('#DB' if is_my else '#SW')
                nd_stat.lab_mech.SetColor('#DB' if is_my else '#SW')
                self.eid_to_settle_data_sub_panel[eid] = item_nd
                self._init_item_like_and_add_btn(item_nd, eid, uid)

            total_damage = int(total_damage)
            is_my_group = my_group_id == group_id
            widget.lab_rank.SetString(str(rank))
            widget.lab_rank.SetColor('#SS' if is_my_group else '#SW')
            widget.lab_score.SetString(str(total_damage))
            widget.lab_score.SetColor('#DB' if is_my_group else '#SW')
            widget.nd_self.setVisible(is_my_group)
            widget.nd_1st.setVisible(rank == 1)
            widget.nd_cover.setVisible(bool(index % 2))
            widget.img_buff_dps.setVisible(False)

    def _init_interaction_widget(self):

        def touch_cb(on):
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
        if self.share_content:
            self.share_content.destroy()
            self.share_content = None
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
        super(FFAEndSceneUI, self).on_finalize_panel()
        return

    def on_extra_scene_added(self, scene_type):
        if scene_type not in (SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE):
            return
        global_data.emgr.hide_screen_effect.emit('DarkCornerEffect')
        global_data.emgr.hide_screen_effect.emit('GrayEffect')
        global_data.emgr.scene_stop_poison_circle.emit()
        remove_sfx_for_ffa_rank(self, self.settle_dict.get('rank', 99))
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
        self.name_widget.reset_position_and_show(name_on_role=False)
        self.show()
        self.panel.PlayAnimation('appear')

    def on_first_success_share(self):
        from logic.gutils.share_utils import hide_share_tips
        hide_share_tips(self.panel.btn_share)

    def on_update_like_info(self, like_soul, liked_soul, like_name, liked_name, like_num):
        if liked_soul == global_data.player.id:
            self.self_liked = True
        if liked_soul in self.eid_to_settle_data_sub_panel:
            nd = self.eid_to_settle_data_sub_panel[liked_soul]
            nd.btn_like.setVisible(True)
            nd.btn_like.lab_num.setVisible(True)
            nd.btn_like.lab_num.SetString(str(like_num))
        msg = '#SB[{}]\xe7\x82\xb9\xe8\xb5\x9e#SW<img="gui/ui_res_2/common/icon/icon_like2.png">#n[{}]#n'.format(like_name, liked_name)
        global_data.emgr.on_recv_danmu_msg.emit(msg)

    def on_click_btn_report(self, btn, touch):
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_END, REPORT_CLASS_BATTLE
        ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
        ui.report_battle_users([], True, True)
        ui.set_report_class(REPORT_CLASS_BATTLE)
        ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)

    def _show_btn_list(self, flag):
        anim_name = 'show' if flag else 'disappear'
        for nd_btn in self.panel.list_function.GetAllItem():
            nd_btn.PlayAnimation(anim_name)

    def on_click_btn_clear(self, btn, *args):
        if self.interaction_widget.selecting_emote:
            return
        if self.showing_settle_data:
            self.settle_data_widget.setVisible(False)
            btn.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/end_icon_unclear.png')
            btn.lab.SetString(860010)
        else:
            self.settle_data_widget.setVisible(True)
            btn.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/end_icon_clear.png')
            btn.lab.SetString(860009)
        self.name_widget.set_visible(self.showing_settle_data)
        self.showing_settle_data = not self.showing_settle_data

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

    def on_click_btn_exit(self, *args):
        if not self.show_details:
            self.settle_data_widget.setVisible(True)
            self.panel.list_function.setVisible(True)
            self._show_btn_list(True)
            self.showing_settle_data = True
            self.name_widget.set_visible(False)
            self.show_details = True
        else:
            self.settle_data_widget.setVisible(False)
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            SettleSystem().show_settle_exp(self.settle_dict, self.reward)
            self.close()