# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/GVGEndSceneUI.py
from __future__ import absolute_import
import six
import math
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import statistics_const as stat_const
from logic.gutils.role_head_utils import init_role_head, init_mecha_head, get_mecha_photo
from logic.gutils.observe_utils import format_popular_num
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL
from logic.gcommon.common_const.battle_const import PLAY_TYPE_GVG
from logic.gutils.new_template_utils import ModeSatSurveyButtonWidget
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gutils.settle_scene_utils import *
from logic.comsys.battle.Settle.GenericSettleWidgets import SettleInputWidget, SettleNameWidget, SettleInteractionWidget
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_EMOTICON, L_ITEM_TYPE_GESTURE
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE
from bson.objectid import ObjectId
from logic.gcommon.common_utils import battle_utils
from common.cfg import confmgr
import math3d
import cc
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from common.const import uiconst

class GVGEndSceneUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_statistics_gvg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'extra_scene_added': 'on_extra_scene_added',
       'change_settle_role_interaction': 'on_change_role_interaction',
       'finish_settle_scene_camera': 'on_finish_settle_scene_camera',
       'update_settle_like_info_event': 'on_update_like_info'
       }
    UI_ACTION_EVENT = {'btn_exit.btn_major.OnClick': 'on_click_btn_next',
       'btn_hide.OnClick': 'on_click_btn_hide',
       'btn_expand.OnClick': 'on_click_btn_expand',
       'btn_switch.OnClick': 'on_click_btn_switch',
       'btn_report.OnClick': 'on_click_btn_report',
       'btn_comment.btn_major.OnClick': 'on_click_btn_comment',
       'btn_share_1.OnClick': 'on_click_share_btn',
       'btn_share_2.btn_major.OnClick': 'on_click_share_btn_2',
       'base_layer.OnClick': 'on_click_base_layer'
       }
    SHOW_ACHIEVE = 0
    SHOW_MODELS = 1
    SHOW_ALL_SCORE = 2

    def on_init_panel(self, group_num, settle_dict, reward, teaminfo, achievement):
        self.cur_stage = GVGEndSceneUI.SHOW_ACHIEVE
        self.settle_dict = settle_dict
        self.reward = self._is_ob_settle() or reward if 1 else None
        self.teammate_info = teaminfo
        self.display_count = len(teaminfo) + 1
        self.achieventment = achievement
        self.eid_to_like_lab = dict()
        self.my_abstract_data_item = None
        self.is_show_detail = False
        self.showing_settle_data = False
        self.bg_music = None
        self.screen_capture_helper = ScreenFrameHelper()
        self.model_loader = SettleSceneModelLoader()
        if self._is_ob_settle():
            p_settle_dict = None
        else:
            p_settle_dict = settle_dict
        self.model_loader.set_parameters(p_settle_dict, teaminfo, 0.9, 1.1, False)
        self.screen_capture_helper = ScreenFrameHelper()
        self.init_settle_data()
        self.init_widgets()
        self.init_battle_name_map()
        self.hide()
        self.panel.RecordAnimationNodeState('hide')
        self.panel.RecordAnimationNodeState('unhide')
        self.show_btn_again()
        return

    def _is_ob_settle(self):
        from logic.gutils import judge_utils
        return judge_utils.is_ob()

    def _refresh_judge_related_controls_visibility(self):
        if self._is_ob_settle():
            self.panel.btn_comment.setVisible(False)
            self.panel.btn_report.setVisible(False)
            self.panel.btn_share_2.setVisible(False)
            self.panel.btn_emote.setVisible(False)
            self.panel.btn_chat.setVisible(False)
            self.panel.btn_send.setVisible(False)

    def init_settle_data(self):
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            self.panel.temp_data = global_data.uisystem.re_create_item(self.panel.temp_data, root=self.panel, tmp_path='battle_duel/i_end_dule_data_base')
        my_group_id = str(self.settle_dict.get('group_id', 1))
        enemy_group_id = str(3 - int(my_group_id))
        group_points = self.settle_dict.get('group_points_dict', {})
        my_group_points, enemy_group_points = group_points.get(my_group_id, 0), group_points.get(enemy_group_id, 0)
        self.panel.lab_score_blue.SetString(str(my_group_points))
        self.panel.lab_score_red.SetString(str(enemy_group_points))
        self.win_ending = self.settle_dict.get('rank', 2) == 1
        self.draw_ending = self.settle_dict.get('is_draw', False)
        if self.draw_ending:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        elif self.win_ending:
            if self.settle_dict.get('is_lore', False):
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_konckout.png')
            else:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        else:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
        self._init_group_settle_data(self.settle_dict['settle_detail'][my_group_id], self.panel.temp_data.nd_blue.list_score, self.panel.temp_details.nd_blue.list_score)
        if enemy_group_id in self.settle_dict['settle_detail']:
            self._init_group_settle_data(self.settle_dict['settle_detail'][enemy_group_id], self.panel.temp_data.nd_red.list_score, self.panel.temp_details.nd_red.list_score)
        if global_data.is_judge_ob:
            from bson.objectid import ObjectId
            my_group_data = self.settle_dict['settle_detail'][my_group_id]
            enemy_group_data = self.settle_dict['settle_detail'][enemy_group_id]
            end_list = []

            def append_group_data(group_data, rank):
                member_info = {}
                member_settle_dict = {}
                for mid, mdata in six.iteritems(group_data):
                    member_info[mid] = {'char_name': mdata[1]}
                    member_settle_dict[mid] = {'statistics': {}}
                    member_settle_dict[mid]['statistics'] = self.teammate_info.get(ObjectId(mid), {}).get('statistics', {})

                end_list.append({'member_settle_dict': member_settle_dict,'member_info': member_info,'rank': rank})

            if not self.draw_ending:
                if self.win_ending:
                    append_group_data(my_group_data, 1)
                    append_group_data(enemy_group_data, 2)
                else:
                    append_group_data(enemy_group_data, 1)
                    append_group_data(my_group_data, 2)
            else:
                append_group_data(my_group_data, 1)
                append_group_data(enemy_group_data, 1)
            self._ob_end_data_list = end_list
        else:
            self._ob_end_data_list = {}

    def init_battle_name_map(self):
        map_id = global_data.battle.get_map_id()
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        name_text_id = map_data_conf.get('nameTID', -1)
        self.panel.nd_map.setVisible(True)
        map_name = battle_utils.get_battle_map_name()
        if map_name:
            self.panel.lab_map.SetString(map_name)
        self.panel.lab_battle.SetString(get_text_by_id(name_text_id))

    def _init_group_settle_data(self, group_data, nd_abstract_list, nd_detail_list):
        cur_settle_like_info = global_data.battle.settle_likenum_dict
        nd_abstract_list.DeleteAllSubItem()
        nd_detail_list.DeleteAllSubItem()
        group_data_len = len(group_data)
        nd_abstract_list.SetInitCount(group_data_len)
        nd_detail_list.SetInitCount(group_data_len)
        for index, (eid, data) in enumerate(six.iteritems(group_data)):
            uid, name, head_frame, head_photo, kill_mecha, assist_mecha, score, mecha_data, mecha_dead_count = data
            eid = ObjectId(eid)
            is_self = eid == self._get_self_eid()
            abstract_item = nd_abstract_list.GetItem(index)
            abstract_item.img_self and abstract_item.img_self.setVisible(is_self)
            init_role_head(abstract_item.temp_role, head_frame, head_photo)
            abstract_item.lab_name.SetString(name)
            abstract_item.lab_mech.SetString(str(kill_mecha))
            from logic.client.const import game_mode_const
            if not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                abstract_item.lab_asistance.SetString(str(assist_mecha))
            abstract_item.lab_score.SetString('%.1f' % score)
            self.eid_to_like_lab[eid] = abstract_item.btn_like.lab_num
            self.eid_to_like_lab[eid].setVisible(eid in cur_settle_like_info)
            self.eid_to_like_lab[eid].SetString(str(cur_settle_like_info.get(eid, 0)))
            if not is_self:
                if global_data.message_data.is_friend(uid):
                    abstract_item.btn_add_friend.setVisible(False)
                else:

                    @abstract_item.btn_add_friend.unique_callback()
                    def OnClick(btn, touch, _uid=uid):
                        global_data.player.req_add_friend(_uid)
                        btn.SetSelect(True)
                        btn.SetEnable(False)

                @abstract_item.btn_report.unique_callback()
                def OnClick(btn, touch, _name=name, _eid=eid):
                    from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_BATTLE_END, REPORT_CLASS_BATTLE
                    ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                    ui.report_battle_users([{'eid': _eid,'name': _name}], True, True)
                    ui.set_report_class(REPORT_CLASS_BATTLE)
                    ui.set_extra_report_info('', '', REPORT_FROM_TYPE_BATTLE_END)
                    ui.set_settle_info(self.settle_dict)
                    btn.SetSelect(True)
                    btn.SetEnable(False)

                    def cancel_report():
                        if self.panel and self.panel.isValid():
                            btn.SetSelect(False)
                            btn.SetEnable(True)

                    ui.set_close_callback(cancel_report)

                @abstract_item.btn_like.unique_callback()
                def OnClick(btn, touch, _eid=eid):
                    if not btn.GetSelect():
                        global_data.player.like_player_after_settle(_eid)
                        btn.SetEnable(False)
                        btn.SetSelect(True)
                        btn.img_like_star.setVisible(True)

            else:
                abstract_item.btn_add_friend.SetEnable(False)
                abstract_item.btn_add_friend.setVisible(False)
                abstract_item.btn_report.SetEnable(False)
                abstract_item.btn_report.setVisible(False)
                abstract_item.btn_like.SetEnable(False)
                abstract_item.btn_like.setVisible(False)
                self.my_abstract_data_item = abstract_item
            if self._is_ob_settle():
                abstract_item.btn_add_friend.setVisible(False)
                abstract_item.btn_like.setVisible(False)
                abstract_item.btn_report.setVisible(False)
            detail_item = nd_detail_list.GetItem(index)
            detail_item.img_self and detail_item.img_self.setVisible(is_self)
            for i, (mecha_id, damage, kill_num) in enumerate(mecha_data):
                damage = int(damage)
                nd_mecha_data = detail_item.list_mech.GetItem(i)
                nd_mecha_data.temp_mech_head.img_mech_head.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/role/mech_%s.png' % str(mecha_id))
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                    soul_round_record_dict = global_data.battle.soul_round_record
                    record_list = soul_round_record_dict.get(eid, [])
                    from logic.entities.DuelBattle import ROUND_LOSE
                    if i < len(record_list):
                        nd_mecha_data.temp_mech_head.img_destoryed.setVisible(record_list[i] == ROUND_LOSE)
                    else:
                        nd_mecha_data.temp_mech_head.img_destoryed.setVisible(False)
                else:
                    nd_mecha_data.temp_mech_head.img_destoryed.setVisible(i < mecha_dead_count)
                nd_mecha_data.lab_harm.SetString(format_popular_num(damage * global_data.game_mode.get_mode_scale()))
                nd_mecha_data.lab_destory_num.SetString(str(kill_num))

    def init_widgets(self):
        self._init_name_widget()
        self.panel.btn_emote.setVisible(False)
        self.panel.btn_emote.setOpacity(0)
        self.panel.btn_emote.SetEnable(False)
        self.panel.btn_emote.setScale(0)
        self.input_widget = SettleInputWidget(self, self.panel.btn_chat, self.panel.btn_send, self.display_count)
        self.comment_widget = ModeSatSurveyButtonWidget(self.panel.btn_comment)

    def _get_self_name(self):
        if self._is_ob_settle():
            eid = self._get_self_eid()
            if eid:
                return self.teammate_info.get(eid, {}).get('char_name', '')
            else:
                return ''

        else:
            return global_data.player.logic.ev_g_char_name()

    def _init_name_widget(self):
        eid_list, name_str_list, uid_list, mvp_list, mecha_id_list, priv_settings_list = (list(), list(), list(), list(), list(), list())
        if not self._is_ob_settle():
            eid_list.append(self._get_self_eid())
            name_str_list.append(self._get_self_name())
            uid_list.append(self._get_self_uid())
            mvp_list.append(self.settle_dict.get('mvp', False))
            mecha_fashion_id = self.settle_dict.get('mecha_fashion', {}).get(FASHION_POS_SUIT, 201800100)
            mecha_item_id = get_lobby_item_belong_no(mecha_fashion_id)
            mecha_id_list.append(mecha_lobby_id_2_battle_id(mecha_item_id))
            priv_settings_list.append(self._get_self_priv_settings())
        for eid, info in six.iteritems(self.teammate_info):
            eid_list.append(eid)
            name_str_list.append(info.get('char_name', ''))
            uid_list.append(info.get('uid', None))
            mvp_list.append(info.get('mvp', False))
            mecha_fashion_id = info.get('mecha_fashion', {}).get(FASHION_POS_SUIT, 201800100)
            mecha_item_id = get_lobby_item_belong_no(mecha_fashion_id)
            mecha_id_list.append(mecha_lobby_id_2_battle_id(mecha_item_id))
            priv_settings_list.append(info.get('priv_settings', {}))

        extra_data = {'priv_settings_list': priv_settings_list
           }
        self.name_widget = SettleNameWidget(eid_list, name_str_list, uid_list, mvp_list, not self.win_ending and not self.draw_ending, mecha_id_list, is_ob=self._is_ob_settle(), extra_info=extra_data)
        return

    def _init_interaction_widget(self):

        def touch_cb(on=True):
            self.showing_settle_data and self._hide_settle_data_panel(on)
            not self.showing_settle_data and self.name_widget.set_visible(not on)

        self.interaction_widget = SettleInteractionWidget(self.panel.btn_emote, lambda : touch_cb(True), lambda : touch_cb(False))

    def begin_show(self):
        self._init_achievement()
        self.show()
        self._refresh_judge_related_controls_visibility()

    def _init_achievement(self):
        settle_dict = self.settle_dict
        self.panel.temp_achieve.setTouchEnabled(False)
        self.panel.nd_achieve.btn_left.setVisible(False)
        self.panel.nd_achieve.btn_right.setVisible(False)
        is_mvp = settle_dict.get('mvp', False)
        if is_mvp and not self._is_ob_settle() and (self.win_ending or self.draw_ending):
            template_path = 'end/i_statistics_mvp' if 1 else 'end/i_statistics_defeated_mvp'
            mvp_conf = global_data.uisystem.load_template(template_path)
            nd_mvp = self.panel.temp_achieve.AddItem(mvp_conf)
            mvp_count = global_data.player.get_achieve_stat(PLAY_TYPE_GVG, stat_const.GET_MVP)
            self.panel.PlayAnimation('next')
            nd_mvp.lab_times.SetString(str(mvp_count))
            nd_mvp.PlayAnimation('show')
            global_data.sound_mgr.play_ui_sound('mvp_open')
        else:
            self.on_click_base_layer(None, None)
        return

    def on_finalize_panel(self):
        self.destroy_widget('comment_widget')
        if self.screen_capture_helper:
            self.screen_capture_helper.destroy()
        self.screen_capture_helper = None
        self.destroy_widget('name_widget')
        self.destroy_widget('input_widget')
        self.model_loader and self.model_loader.on_destroy()
        self.model_loader = None
        if self.bg_music:
            global_data.sound_mgr.stop_playing_id(self.bg_music)
            self.bg_music = None
        return

    def on_extra_scene_added(self, scene_type):
        if scene_type not in (SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE):
            return
        remove_rank_model()
        remove_sfx_for_result(self, self.win_ending, self.draw_ending)
        self.model_loader.load_role_mecha_models()

    def on_finish_settle_scene_camera(self):
        self.panel.PlayAnimation('show')
        self.name_widget.reset_position_and_show(False)

    def on_resolution_changed(self):
        if self.name_widget:
            self.name_widget.reset_position_and_show(False)

    def on_change_role_interaction(self, eid, item_no):
        index = self.model_loader.get_role_model_index(eid)
        if index != -1:
            item_type = get_lobby_item_type(item_no)
            if item_type == L_ITEM_TYPE_EMOTICON:

                def cb():
                    self.name_widget and self.name_widget.set_sub_widget_scale_by_eid(eid, 1.0)

                global_data.emgr.change_model_display_emoji.emit(item_no, index, True, cb)
                self.name_widget.set_sub_widget_scale_by_eid(eid, 0.0)
            elif item_type == L_ITEM_TYPE_GESTURE:
                global_data.emgr.change_model_display_anim.emit(item_no, index)

    def on_update_like_info(self, like_soul, liked_soul, like_name, liked_name, like_num):
        if liked_soul in self.eid_to_like_lab:
            lab = self.eid_to_like_lab[liked_soul]
            lab.SetString(str(like_num))
            lab.setVisible(True)
            if liked_soul == self._get_self_eid():
                self.my_abstract_data_item.btn_like.setVisible(True)
        msg = '#SB[{}]\xe7\x82\xb9\xe8\xb5\x9e#SW<img="gui/ui_res_2/common/icon/icon_like2.png">#n[{}]#n'.format(like_name, liked_name)
        global_data.emgr.on_recv_danmu_msg.emit(msg)

    def _get_self_eid(self):
        if self._is_ob_settle():
            return self.settle_dict.get('ob_data', {}).get('watching_soul_id', None)
        else:
            return global_data.player.id
            return None

    def _get_self_uid(self):
        if self._is_ob_settle():
            return self.settle_dict.get('ob_data', {}).get('watching_uid', None)
        else:
            return global_data.player.uid
            return None

    def _get_self_priv_settings(self):
        if self._is_ob_settle():
            eid = self._get_self_eid()
            if eid:
                return self.teammate_info.get(eid, {}).get('priv_settings', {})
            else:
                return {}

        else:
            return global_data.player.get_privilege_setting()

    def on_click_base_layer(self, *args):
        if self.cur_stage == GVGEndSceneUI.SHOW_ACHIEVE:
            global_data.emgr.start_settle_scene_camera.emit()
            self.panel.StopAnimation('next')
            self.panel.PlayAnimation('disappear_achieve')
            self.cur_stage = GVGEndSceneUI.SHOW_MODELS

    def on_click_btn_next(self, *args):
        if self.cur_stage == GVGEndSceneUI.SHOW_MODELS:
            if not global_data.is_judge_ob:
                self.panel.PlayAnimation('appear_details')
            else:
                self.hide()
                from logic.comsys.observe_ui.JudgeObSettleUI import JudgeObSettleUI
                JudgeObSettleUI(None, self._ob_end_data_list)
                return
            self.showing_settle_data = True
            self.name_widget.set_visible(False)
            self.cur_stage = GVGEndSceneUI.SHOW_ALL_SCORE
            self.panel.btn_exit.setVisible(True)
            if not self._is_ob_settle():
                self.panel.btn_comment.setVisible(True)
            self.panel.lab_next.setVisible(False)
            self.panel.btn_share_1.setVisible(False)
            self.panel.btn_hide.setVisible(True)
            self.panel.nd_3.setVisible(False)
        elif self.cur_stage == GVGEndSceneUI.SHOW_ALL_SCORE:
            if self.reward is not None:
                from logic.comsys.battle.Settle.SettleSystem import SettleSystem
                SettleSystem().show_settle_exp(self.settle_dict, self.reward)
            else:
                global_data.player and global_data.player.quit_battle(True)
            self.close()
        return

    def on_click_btn_report(self, btn, *args):
        flag = not btn.GetSelect()
        btn.SetSelect(flag)
        anim_name = 'show_report' if flag else 'disappear_report'
        list_scores = [self.panel.temp_data.nd_blue.list_score, self.panel.temp_data.nd_red.list_score]
        for list_score in list_scores:
            for item in list_score.GetAllItem():
                item.PlayAnimation(anim_name)
                if item != self.my_abstract_data_item:
                    is_ob_settle = self._is_ob_settle()
                    item.btn_add_friend.setVisible(not flag and not is_ob_settle)
                    item.btn_like.setVisible(not flag and not is_ob_settle)
                    item.btn_report.setVisible(flag and not is_ob_settle)

        if not self.showing_settle_data and flag:
            self.on_click_btn_hide()

    def _hide_settle_data_panel(self, flag):
        if flag:
            if self.panel.IsPlayingAnimation('unhide'):
                self.panel.StopAnimation('unhide')
            self.panel.RecoverAnimationNodeState('hide')
            self.panel.PlayAnimation('hide')
            self.panel.nd_2.setVisible(False)
            self.panel.nd_3.setVisible(True)
        else:
            if self.panel.IsPlayingAnimation('hide'):
                self.panel.StopAnimation('hide')
            self.panel.RecoverAnimationNodeState('unhide')
            self.panel.PlayAnimation('unhide')
            self.panel.nd_2.setVisible(True)
            self.panel.nd_3.setVisible(False)

    def on_click_btn_hide(self, *args):
        self._hide_settle_data_panel(self.showing_settle_data)
        self.name_widget.set_visible(self.showing_settle_data)
        self.showing_settle_data = not self.showing_settle_data

    def on_click_btn_expand(self, *args):
        self._hide_settle_data_panel(self.showing_settle_data)
        self.name_widget.set_visible(self.showing_settle_data)
        self.showing_settle_data = not self.showing_settle_data

    def on_click_btn_switch(self, *args):
        if self.is_show_detail:
            self.panel.btn_switch.lab_switch.SetString(get_text_by_id(81107))
            self.panel.temp_data.setVisible(True)
            self.panel.temp_details.setVisible(False)
            self.panel.nd_btn_2.setVisible(True)
            self.is_show_detail = False
        else:
            self.panel.btn_switch.lab_switch.SetString(get_text_by_id(80420))
            self.panel.temp_data.setVisible(False)
            self.panel.temp_details.setVisible(True)
            self.panel.nd_btn_2.setVisible(False)
            self.is_show_detail = True
        if not self.showing_settle_data:
            self.on_click_btn_hide()
        return True

    def on_click_btn_comment(self, btn, touch):
        from logic.comsys.survey.ModeSatisfactionSurveyUI import ModeSatisfactionSurveyUI
        battle_context = self.get_battle_context()
        ui_inst = ModeSatisfactionSurveyUI(None, battle_context)
        return

    def on_click_share_btn(self, btn, touch):
        ui_names = [
         self.__class__.__name__, 'DanmuLinesUI']

        def cb(*args):
            self.panel.btn_share_1.setVisible(True)
            self.panel.lab_next.setVisible(True)
            self.panel.nd_btn_2.setVisible(True)

        if self.screen_capture_helper:
            self.panel.btn_share_1.setVisible(False)
            self.panel.lab_next.setVisible(False)
            self.panel.nd_btn_2.setVisible(False)
            self.screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

    def on_click_share_btn_2(self, btn, touch):
        ui_names = [
         self.__class__.__name__, 'DanmuLinesUI']

        def cb(*args):
            if not self._is_ob_settle():
                self.panel.btn_report.setVisible(True)
                self.panel.btn_comment.setVisible(True)
            self.panel.nd_bottom.setVisible(True)

        if self.screen_capture_helper:
            if not self._is_ob_settle():
                self.panel.btn_report.setVisible(False)
                self.panel.btn_comment.setVisible(False)
            self.panel.nd_bottom.setVisible(False)
            self.screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_DUEL,))
    def show_btn_again(self):
        self.panel.PlayAnimation('again')

        @self.panel.nd_bottom.btn_again.btn_major.unique_callback()
        def OnClick(btn, touch):
            if global_data.player:
                from logic.gcommon.common_const.battle_const import DEFAULT_DUEL_TID
                global_data.player.set_auto_match_tid(DEFAULT_DUEL_TID)
                global_data.player and global_data.player.quit_battle(True)