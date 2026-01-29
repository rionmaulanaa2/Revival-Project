# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Clone/CloneVoteMecha.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from common.cfg import confmgr
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from logic.gcommon import time_utility
from logic.gutils import dress_utils
from logic.gutils import lobby_model_display_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui import InputBox
from logic.gcommon.item import item_const
from collections import Counter
from logic.gcommon.common_utils import text_utils
from logic.gcommon.common_const import battle_const
from logic.gutils import mecha_utils
import cc
SELECTED_PNG_PATH = 'gui/ui_res_2/battle_clone/clone_js_d_cm.png'
UNSELECTED_PNG_PATH = 'gui/ui_res_2/battle_clone/clone_js_d_m.png'
MESSAGE_VISIBLE_TIME = 2
CHAT_MESSAGE_INTERVAL = 10
TEMP_CHAT_CONTINUE_TIME = 3
BTN_SURE_UNREADY_PIC = 'gui/ui_res_2/battle_mech/btn_sure_nml.png'
BTN_SURE_READY_PIC = 'gui/ui_res_2/battle_mech/btn_sure_lock.png'

class CloneVoteMecha(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'battle_clone/clone_choose_mech'
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'btn_skill.OnBegin': 'on_click_skill_begin',
       'btn_skill.OnEnd': 'on_click_skill_end',
       'btn_sure.OnClick': 'on_click_sure',
       'btn_chat_history.OnClick': 'on_click_chat_history',
       'btn_chat_ok.OnClick': 'on_click_chat_ok',
       'nd_tips_close.OnClick': 'on_click_history_close',
       'btn_right_direction.OnClick': 'on_click_expand_btn'
       }

    def ui_vkb_custom_func(self):
        return True

    def on_init_panel(self, *args, **kwargs):
        self.ob_player_id = global_data.is_judge_ob or global_data.player.id if 1 else global_data.player.get_global_spectate_player_id()
        self.init_parameter()
        self.process_event(True)
        self.init_model_display()
        self.hide()

    def on_finalize_panel(self):
        self.process_event(False)
        if self.input_box:
            self.input_box.destroy()
        global_data.ui_mgr.remove_ui_show_whitelist('CloneVoteMecha')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'start_clone_vote_mecha': self.start_vote_count_down,
           'refresh_vote_mecha': self.refresh_vote_mecha,
           'refresh_confirm_vote_mecha': self.refresh_confirm_vote_mecha,
           'refresh_cancel_confirm_vote_mecha': self.refresh_cancel_confirm_vote_mecha,
           'clone_vote_mecha_finished': self.mecha_vote_finished,
           'receive_teammate_message': self.receive_teammate_message,
           'clone_wait_vote_mecha': self.wait_other_to_vote
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameter(self):
        self.mecha_ui_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        self.all_mecha_list, self.own_mecha_list, self.share_mecha_lst = mecha_utils.get_mecha_lst()
        self.usual_mecha_ids = global_data.player.get_usual_mecha_ids()
        self.show_mecha_list = global_data.player.get_battle_mecha_open_list(battle_const.PLAY_TYPE_CLONE)
        self.skill_widget = None
        self.selected_mecha_id = None
        self.mecha_id_2_widget = {}
        self.teammate_last_talk_ts = {}
        self.last_send_ts = 0
        self.is_in_expand_mode = False
        return

    def enter_vote_mecha(self):
        self.init_battle_data()
        self.init_top_widget()
        self.init_area_info_widget()
        self.init_mecha_list_widgets()
        self.init_mecha_vote_widgets()
        self.init_chat_widget()
        self.update_display_mecha_name()
        self.init_confirm_btn()
        self.select_most_proficient_mecha()
        self.show()
        global_data.ui_mgr.add_ui_show_whitelist(['CloneVoteMecha', 'CloneMechaSkillDetail', 'NoticeUI', 'BattleReconnectUI', 'NormalConfirmUI2'], 'CloneVoteMecha')
        global_data.sound_mgr.play_music('clone_standby')

    def init_battle_data(self):
        battle = global_data.battle
        if not battle:
            return
        self.map_conf = confmgr.get('map_config', str(battle.map_id), default={})
        self.group_data = battle.group_data
        self.group_mecha_vote_info = battle.group_mecha_vote_info
        self.group_confirmed_list = battle.group_confirmed_list
        self.my_group = battle.my_group
        self.my_group_data = self.group_data[self.my_group]
        self.ready = self.ob_player_id in self.group_confirmed_list

    def get_team_size(self):
        return len(self.group_data[self.my_group])

    def get_confirmed_player_cnt(self):
        return len(list(set(self.group_confirmed_list)))

    def get_candi_mecha_ui_item(self, mecha_id):
        if mecha_id not in self.show_mecha_list:
            return None
        else:
            index = self.show_mecha_list.index(mecha_id)
            return self.candi_mecha_list_view.get_list_item(index)

    def get_teammate_chosen_widget(self, player_id):
        player_index = self.my_group_data.get(player_id, {}).get('index', -1)
        if player_index >= 0:
            return self.panel.list_duiyou.GetItem(player_index)
        else:
            return None
            return None

    def init_area_info_widget(self):
        battle = global_data.battle
        map_name_text_ids = self.map_conf.get('cMapNameTextIds', [])
        text_id_index = 0
        prefix_str = ''
        if len(map_name_text_ids) > 1 and battle and hasattr(battle, 'area_id'):
            text_id_index = min(int(battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        map_text = ''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])])
        self.panel.lab_map_name.SetString(map_text)

    def init_top_widget(self):
        self.init_time_widget()
        self.init_ready_widget(self.get_confirmed_player_cnt(), self.get_team_size())
        self.init_area_info_widget()

    def init_ready_widget(self, confirmed_cnt, total_cnt):
        self.panel.nd_title.nd_player.lab_nub.SetString('{0}/{1}'.format(confirmed_cnt, total_cnt))
        self.panel.nd_ready.setVisible(self.ready)
        self.panel.nd_await.setVisible(not self.ready)
        if self.ready:
            self.panel.PlayAnimation('change')

    def init_time_widget(self):
        self.start_vote_count_down()

    def start_vote_count_down(self):
        battle = global_data.battle
        if not battle:
            return
        end_ts = battle.mecha_vote_end_ts
        if not end_ts:
            return
        total_time = battle.mecha_vote_end_ts - time_utility.time()
        self.start_count_down(total_time, red=True)

    def start_count_down(self, total_time, red=False):

        def update_count_down(pass_time):
            left_time = int(total_time - int(pass_time))
            self.panel.nd_time.lab_time.SetString('%.2ds' % left_time)
            if red and left_time <= 10:
                self.panel.nd_time.lab_time.SetColor(16000337)
            else:
                self.panel.nd_time.lab_time.SetColor('#SW')

        def update_count_down_finish():
            self.panel.nd_time.lab_time.SetString('00s')

        self.panel.nd_title.StopTimerAction()
        if total_time < 0:
            update_count_down_finish()
            return
        update_count_down(pass_time=0)
        self.panel.nd_title.TimerAction(update_count_down, total_time, callback=update_count_down_finish, interval=1)

    def init_confirm_btn(self):
        if self.ready:
            self.panel.nd_wait.setVisible(True)
            self.panel.PlayAnimation('wait')
            btn_sure_pic = BTN_SURE_READY_PIC
            btn_sure_text = 80295
        else:
            self.panel.nd_wait.setVisible(False)
            self.panel.StopAnimation('wait')
            btn_sure_pic = BTN_SURE_UNREADY_PIC
            btn_sure_text = 80306
        self.panel.btn_sure.SetFrames('', [btn_sure_pic, btn_sure_pic, btn_sure_pic], False, None)
        self.panel.btn_sure.setVisible(not global_data.is_judge_ob)
        self.panel.btn_sure.SetText(btn_sure_text)
        return

    def init_chat_widget(self):
        if not global_data.is_judge_ob:

            def send_cb(*args, **kwargs):
                self.panel.btn_chat_ok.OnClick(None)
                return

            self.input_box = InputBox.InputBox(self.panel.input_box, send_callback=send_cb, detach_after_enter=False)
            self.input_box.set_rise_widget(self.panel)
        else:
            self.panel.btn_chat_ok.setVisible(False)
            self.panel.input_box.setVisible(False)
            self.input_box = None
        self.panel.nd_chat_quick.nd_tips_close.setVisible(False)
        self.panel.nd_chat_quick.temp_chat_quick.setVisible(False)
        self.panel.nd_chat_quick.setVisible(False)
        self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()
        chat_history = global_data.battle.group_chat_history
        for player_id, msg in chat_history:
            self.make_one_history_msg(player_id, msg, self.panel.temp_chat_quick.list_chat_quick, player_id == self.ob_player_id)

        return

    def receive_teammate_message(self, soul_id, message, add_to_history=True):
        self.last_send_ts = time_utility.time()

        def close_temp_chat():
            if time_utility.time() - self.last_send_ts > TEMP_CHAT_CONTINUE_TIME:
                self.panel.nd_chat.setVisible(False)
                self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()

        if add_to_history:
            self.make_one_history_msg(soul_id, message, self.panel.temp_chat_quick.list_chat_quick, soul_id == self.ob_player_id)
            self.panel.temp_chat_quick.list_chat_quick._refreshItemPos()
            if not self.panel.nd_chat_quick.isVisible():
                self.panel.nd_chat.setVisible(True)
                self.make_one_history_msg(soul_id, message, self.panel.nd_chat.list_chat_quick, soul_id == self.ob_player_id, need_color=True)
                self.panel.nd_chat.list_chat_quick._refreshItemPos()
                self.panel.SetTimeOut(TEMP_CHAT_CONTINUE_TIME, close_temp_chat)

    def make_one_history_msg(self, player_id, message, list_chat, is_me, need_color=False):
        if player_id not in self.my_group_data:
            return
        item = list_chat.AddTemplateItem(bRefresh=True)
        user_data = self.my_group_data.get(player_id)
        name = user_data.get('char_name', '')
        if need_color:
            if not is_me:
                content = '<color=0xdadadaff>%s:#N <color=0xffffffff>%s#N' % (name, message)
            else:
                content = '<color=0x4efff0ff>%s:#N <color=0xffffffff>%s#N' % (name, message)
        else:
            content = '{}: {}'.format(name, message)
        item.lab_text.SetString(content)
        item_w, _ = item.GetContentSize()
        item.lab_text.formatText()
        text_size = item.lab_text.getVirtualRendererSize()
        item.SetContentSize(item_w, text_size.height + CHAT_MESSAGE_INTERVAL)
        item.ChildResizeAndPosition()
        list_chat._container._refreshItemPos()
        list_chat._refreshItemPos()
        list_chat.ScrollToBottom()

    def init_mecha_list_widgets(self):
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        self.candi_mecha_list_view = InfiniteScrollWidget(self.panel.list_choose_mecha, self.panel, up_limit=500, down_limit=500)
        self.candi_mecha_list_view.set_template_init_callback(self.init_candi_mecha_btn)
        self.candi_mecha_list_view.enable_item_auto_pool(True)
        self.candi_mecha_list_view.update_data_list(self.show_mecha_list)
        self.candi_mecha_list_view.update_scroll_view()

    def init_candi_mecha_btn(self, candi_mecha_ui_item, mecha_id):
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        icon_path = 'gui/ui_res_2/item/mecha/%d.png' % lobby_mecha_id
        if not candi_mecha_ui_item:
            ui_item = self.get_candi_mecha_ui_item(mecha_id) if 1 else candi_mecha_ui_item
            if not ui_item:
                return
            ui_item.img_mecha.SetDisplayFrameByPath('', icon_path)
            ui_item.img_mecha_shadow.SetDisplayFrameByPath('', icon_path)
            ui_item.StopAnimation('choose')
            ui_item.RecoverAnimationNodeState('choose')
            ui_item.RecordAnimationNodeState('loop')
            if self.selected_mecha_id and self.selected_mecha_id == mecha_id:
                ui_item.btn_mecha.SetSelect(True)
                ui_item.nd_select.setScale(1.1)
                ui_item.PlayAnimation('choose')
                ui_item.PlayAnimation('loop')
                ui_item.SetTimeOut(0.5, lambda mecha_ui_item=ui_item: self.hide_candi_mecha_ui_item_light(mecha_ui_item), tag=210302)
            else:
                ui_item.btn_mecha.SetSelect(False)
                ui_item.nd_select.setScale(1)

            @global_data.is_judge_ob or ui_item.btn_mecha.callback()
            def OnBegin(*args):
                self.on_btn_mecha_begin(ui_item)

            @ui_item.btn_mecha.callback()
            def OnEnd(*args):
                self.on_btn_mecha_end(ui_item)

            @ui_item.btn_mecha.callback()
            def OnCancel(*args):
                self.on_btn_mecha_cancel(ui_item)

            @ui_item.btn_mecha.callback()
            def OnClick(*args):
                self.on_btn_mecha_click(ui_item, mecha_id, lobby_mecha_id)

        ui_display_conf = confmgr.get('ui_display_conf', 'MechaSummonUIItem', 'Content', default={})
        node_ui_conf = ui_display_conf.get(str(mecha_id))
        if node_ui_conf:
            pos = node_ui_conf.get('NodePos')
            if pos:
                ui_item.img_mecha.SetPosition(*pos)
            else:
                ui_item.img_mecha.ReConfPosition()
            pos = node_ui_conf.get('ShadowPos')
            if pos:
                ui_item.img_mecha_shadow.SetPosition(*pos)
            else:
                ui_item.img_mecha_shadow.ReConfPosition()
            scale = node_ui_conf.get('NodeScale')
            if scale:
                ui_item.img_mecha.SetScaleCheckRecord(scale)
                ui_item.img_mecha_shadow.SetScaleCheckRecord(scale)
            else:
                ui_item.img_mecha.ScaleSelfNode()
                ui_item.img_mecha_shadow.ScaleSelfNode()
        else:
            ui_item.img_mecha.ReConfPosition()
            ui_item.img_mecha_shadow.ReConfPosition()
            ui_item.img_mecha.ScaleSelfNode()
            ui_item.img_mecha_shadow.ScaleSelfNode()

    def init_mecha_vote_widgets(self):
        teammate_cnt = self.get_team_size()
        my_group_data = self.group_data[self.my_group]
        self.panel.list_duiyou.SetInitCount(teammate_cnt)
        for player_id, player_data in six.iteritems(my_group_data):
            index = player_data['index']
            ui_item = self.panel.list_duiyou.GetItem(index)
            if not ui_item:
                continue
            is_ready = player_id in self.group_confirmed_list
            is_me = player_id == self.ob_player_id
            ui_item.lab_name.SetString(player_data.get('char_name', ''))
            if is_ready:
                ui_item.nd_ready.setVisible(True)
                ui_item.PlayAnimation('ready')
            else:
                ui_item.nd_ready.setVisible(False)
            self.play_chosen_mecha_widget_anim(ui_item, is_me)

            @ui_item.btn_click.unique_callback()
            def OnClick(btn, touch, soul_id=player_id):
                if self.ready:
                    return
                else:
                    teammate_vote = self.group_mecha_vote_info.get(soul_id, None)
                    self.select_mecha(teammate_vote and teammate_vote[0])
                    return

            vote_info = self.group_mecha_vote_info.get(player_id)
            if not vote_info:
                continue
            chosen_mecha_id, fashion = vote_info
            fashion_id = fashion.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(chosen_mecha_id, -1)
            self.update_chosen_mecha_widget(ui_item, chosen_mecha_id, fashion_id, is_me)
            if global_data.is_judge_ob and is_me:
                self.select_mecha(chosen_mecha_id)
            ui_item.img_ready.setVisible(is_ready)

        self.panel.list_duiyou.setTouchEnabled(False)
        self.process_major_mecha()

    def update_chosen_mecha_widget(self, widget, mecha_id, fashion_id, is_me):
        if mecha_id is None:
            widget.nd_mech_head.setVisible(False)
            return
        else:
            img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(fashion_id), 'half_img_path')
            widget.img_mech.SetDisplayFrameByPath('', img_path)
            widget.nd_mech_head.setVisible(True)
            widget.lab_meach.SetString(item_utils.get_mecha_name_by_id(mecha_id))
            if not is_me:
                widget.lab_meach.SetColor(2961525)
                widget.lab_name.SetColor(3881926)
            else:
                widget.lab_meach.SetColor(3026478)
                widget.lab_name.SetColor(5395543)
            return

    def update_candidate_mecha_widget(self, old_mecha_id, new_mecha_id):
        if old_mecha_id in self.show_mecha_list and old_mecha_id != new_mecha_id:
            cur_widget = self.get_candi_mecha_ui_item(old_mecha_id)
            if cur_widget:
                cur_widget.btn_mecha.SetSelect(False)
                cur_widget.StopAnimation('choose')
                cur_widget.RecoverAnimationNodeState('choose')
                cur_widget.StopAnimation('loop')
                cur_widget.RecoverAnimationNodeState('loop')
                cur_widget.nd_select.setScale(1)
                cur_widget.img_choose_light1.setVisible(False)
        if new_mecha_id in self.show_mecha_list:
            sel_widget = self.get_candi_mecha_ui_item(new_mecha_id)
            if sel_widget:
                sel_widget.PlayAnimation('choose')
                sel_widget.PlayAnimation('loop')
                sel_widget.nd_select.setScale(1.1)
                sel_widget.SetTimeOut(0.5, lambda mecha_ui_item=sel_widget: self.hide_candi_mecha_ui_item_light(mecha_ui_item), tag=201117)

    def play_chosen_mecha_widget_anim(self, widget, is_me):
        if is_me:
            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('show')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('me')),
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('me')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('loop'))]))
        else:
            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('show')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('team'))]))

    def hide_candi_mecha_ui_item_light(self, ui_item):
        ui_item.StopAnimation('choose')
        ui_item.vx_choose_light1.setVisible(False)
        ui_item.vx_choose_light2.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def update_display_mecha_name(self):
        if not self.selected_mecha_id:
            return
        conf = self.mecha_ui_conf[str(self.selected_mecha_id)]
        name_id, _, mecha_positioning = conf['name_text_id']
        self.lab_dingwei.SetString(mecha_positioning)
        self.lab_name.SetString(name_id)

    def select_most_proficient_mecha(self):
        if global_data.is_judge_ob:
            return
        if self.ready:
            return
        most_proficiency = 0
        most_proficient_mecha_id = 8001
        for mecha_id in self.show_mecha_list:
            level, proficiency = global_data.player.get_proficiency(mecha_id)
            if proficiency > most_proficiency:
                most_proficiency = proficiency
                most_proficient_mecha_id = mecha_id

        self.select_mecha(most_proficient_mecha_id)

    def select_mecha(self, mecha_id):
        if mecha_id is None or not global_data.battle:
            return False
        else:
            if self.selected_mecha_id == mecha_id:
                return False
            self.update_candidate_mecha_widget(self.selected_mecha_id, mecha_id)
            self.selected_mecha_id = mecha_id
            self.update_display_mecha_name()
            fashion_id = dress_utils.get_mecha_dress_clothing_id(mecha_id) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
            self.update_chosen_mecha_widget(self.get_teammate_chosen_widget(self.ob_player_id), mecha_id, fashion_id, True)
            self.update_mecha_display()
            if global_data.is_judge_ob:
                return True
            global_data.battle.request_vote_mecha(self.selected_mecha_id)
            return True

    def refresh_vote_mecha(self, soul_id, mecha_id, mecha_fashion):
        if soul_id not in self.my_group_data:
            return
        is_me = soul_id == self.ob_player_id
        fashion_id = mecha_fashion.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        widget = self.get_teammate_chosen_widget(soul_id)
        self.update_chosen_mecha_widget(widget, mecha_id, fashion_id, is_me)
        self.process_major_mecha()
        if global_data.is_judge_ob:
            self.select_mecha(mecha_id)

    def refresh_confirm_vote_mecha(self, soul_id):
        self.panel.PlayAnimation('player')
        widget = self.get_teammate_chosen_widget(soul_id)
        widget and widget.nd_ready.setVisible(True) and widget.PlayAnimation('ready')
        self.init_ready_widget(self.get_confirmed_player_cnt(), self.get_team_size())

    def refresh_cancel_confirm_vote_mecha(self, soul_id):
        self.panel.PlayAnimation('player')
        widget = self.get_teammate_chosen_widget(soul_id)
        widget and widget.nd_ready.setVisible(False) and widget.StopAnimation('ready')
        self.init_ready_widget(self.get_confirmed_player_cnt(), self.get_team_size())

    def mecha_vote_finished(self):
        battle = global_data.battle
        if not battle.mecha_vote_finished:
            return
        self.ready = True
        mecha_id = battle.mecha_use_dict[self.my_group]
        mecha_fashions = battle.group_mecha_fashion[self.my_group]
        for player_id, player_data in six.iteritems(self.my_group_data):
            widget = self.get_teammate_chosen_widget(player_id)
            fashion = mecha_fashions.get(player_id, {})
            fashion_id = fashion.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
            is_me = player_id == self.ob_player_id
            self.update_chosen_mecha_widget(widget, mecha_id, fashion_id, is_me)
            self.refresh_confirm_vote_mecha(player_id)

        self.select_mecha(mecha_id)
        self.refresh_confirm_vote_mecha(self.ob_player_id)
        self.panel.nd_wait.setVisible(True)
        self.panel.btn_sure.setVisible(False)
        self.panel.nd_title.nd_player.lab_nub.SetString('{0}/{1}'.format(self.get_team_size(), self.get_team_size()))
        self.process_major_mecha(is_show=False)
        self.panel.PlayAnimation('wait')
        self.start_count_down(3, red=False)
        self.panel.SetTimeOut(3, lambda : global_data.emgr.change_model_display_scene_item.emit(None))

    def wait_other_to_vote(self):
        self.panel.btn_sure.setVisible(False)
        self.panel.nd_wait.setVisible(True)
        self.panel.PlayAnimation('wait')

    def process_major_mecha(self, is_show=True):
        major_mecha_id = None
        if is_show:
            mecha_vote = Counter((mecha_id for mecha_id, _ in six.itervalues(self.group_mecha_vote_info)))
            if not mecha_vote:
                return
            ordered_vote = mecha_vote.most_common()
            major_mecha_id, the_most_cnt = ordered_vote[0]
            candidate_mechas = [ mid for mid, cnt in ordered_vote if cnt == the_most_cnt ]
            if len(candidate_mechas) > 1:
                major_mecha_id = None
        for eid, mem_data in six.iteritems(self.my_group_data):
            if not self.group_mecha_vote_info.get(eid):
                continue
            selected_mecha_id = self.group_mecha_vote_info[eid][0]
            nd = self.get_teammate_chosen_widget(eid)
            if nd:
                nd.nd_elected.setVisible(selected_mecha_id == major_mecha_id)

        return

    def on_click_sure(self, *args):
        if global_data.is_judge_ob or not global_data.battle:
            return
        if self.ready:
            global_data.battle.cancel_confirm_vote_mecha()
        else:
            global_data.battle.confirm_vote_mecha()
        self.ready = not self.ready
        self.init_confirm_btn()

    def on_click_skill_begin(self, *args):
        ui = global_data.ui_mgr.show_ui('CloneMechaSkillDetail', 'logic.comsys.battle.Clone')
        ui.refresh_ui(self.selected_mecha_id)
        ui.PlayAnimation('appear')
        self.panel.img_shadow.setVisible(True)
        return True

    def on_click_skill_end(self, *args):
        global_data.ui_mgr.close_ui('CloneMechaSkillDetail')
        self.panel.img_shadow.setVisible(False)
        return True

    def on_click_history_close(self, *args):
        self.panel.nd_chat_quick.setVisible(False)

    def on_click_chat_history(self, *args):
        is_visible = not self.panel.nd_chat_quick.isVisible()
        self.panel.nd_chat_quick.nd_tips_close.setVisible(is_visible)
        self.panel.nd_chat_quick.temp_chat_quick.setVisible(is_visible)
        self.panel.nd_chat_quick.setVisible(is_visible)
        if is_visible:
            self.panel.nd_chat.setVisible(False)
            self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()

    def on_click_chat_ok(self, *args):
        if global_data.is_judge_ob or not global_data.battle:
            return
        now = time_utility.time()
        if now - self.last_send_ts < 0.5:
            return
        self.last_send_ts = now
        text = self.input_box.get_text()
        if text == '':
            global_data.game_mgr.show_tip(get_text_by_id(11055), True)
            return
        self.input_box.set_text('')
        check_code, review_pass, msg = text_utils.check_review_words_chat(text)
        if review_pass != text_utils.CHECK_WORDS_PASS:
            global_data.game_mgr.show_tip(get_text_by_id(11009), True)
            return
        global_data.battle.send_message(msg)

    def on_click_expand_btn(self, *args):
        if self.is_in_expand_mode:
            self.panel.list_choose_mecha.SetNumPerUnit(2)
            self.panel.btn_right_direction.setRotation(0)
            self.panel.img_list_bg.setVisible(True)
            self.panel.img_dw4.setVisible(False)
        else:
            self.panel.list_choose_mecha.SetNumPerUnit(4)
            self.panel.btn_right_direction.setRotation(180)
            self.panel.img_list_bg.setVisible(False)
            self.panel.img_dw4.setVisible(True)
        self.is_in_expand_mode = not self.is_in_expand_mode
        self.panel.list_choose_mecha.InitConfContentSize()
        self.panel.nd_dir.setContentSize(self.panel.list_choose_mecha.getContentSize())
        self.panel.nd_dir.ChildResizeAndPosition()
        self.candi_mecha_list_view.change_num_per_unit()

    def on_btn_mecha_begin(self, ui_item):
        ui_item.nd_btn.setScale(1 / 0.83)
        ui_item.setLocalZOrder(1)
        ui_item.img_frame_choose.setVisible(True)
        ui_item.img_choose_light.setVisible(True)
        return True

    def on_btn_mecha_end(self, ui_item):
        ui_item.nd_btn.setScale(1)
        ui_item.setLocalZOrder(0)
        ui_item.img_frame_choose.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def on_btn_mecha_cancel(self, ui_item):
        ui_item.nd_btn.setScale(1)
        ui_item.setLocalZOrder(0)
        ui_item.img_frame_choose.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def on_btn_mecha_click(self, ui_item, mecha_id, lobby_mecha_id):
        if self.ready:
            return
        self.select_mecha(mecha_id)

    def init_model_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def update_mecha_display(self):
        lobby_select_id = dress_utils.get_mecha_dress_clothing_id(self.selected_mecha_id) or dress_utils.battle_id_to_mecha_lobby_id(self.selected_mecha_id)
        shiny_weapon_id = dress_utils.get_mecha_dress_shiny_weapon_id(self.selected_mecha_id)
        if lobby_select_id is None:
            global_data.emgr.change_model_display_scene_item.emit(None)
        else:
            display_type = lobby_model_display_const.CLONE_VOTE_MECHA_SCENE
            global_data.emgr.set_lobby_scene_display_type.emit(display_type)
            model_data = lobby_model_display_utils.get_lobby_model_data(lobby_select_id, consider_second_model=False)
            for data in model_data:
                data['skin_id'] = lobby_select_id
                data['model_scale'] = 3
                data['shiny_weapon_id'] = shiny_weapon_id
                if self.selected_mecha_id == 8028:
                    data['show_anim'] = data['end_anim']

            global_data.emgr.change_model_display_scene_item.emit(model_data)
        return