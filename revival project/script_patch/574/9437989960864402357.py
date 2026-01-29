# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/RecruitReward.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.new_template_utils import VitalityBoxReward
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from data.c_recruit_data import get_show_recruit_num, get_show_recruit_score, get_vitality_reward, get_recruit_num_percent, get_recruit_score_percent, get_show_verify_gift
from common.cfg import confmgr
from logic.comsys.common_ui.InputBox import InputBox
from logic.gutils import template_utils
IMG_BOX_PATH = {0: 'gui/ui_res_2/task/liveness_1.png',
   1: 'gui/ui_res_2/task/liveness_2.png',
   2: 'gui/ui_res_2/task/liveness_3.png',
   3: 'gui/ui_res_2/task/liveness_4.png',
   4: 'gui/ui_res_2/task/liveness_5.png'
   }
IMG_BOX_GET_PATH = {0: 'gui/ui_res_2/task/liveness_1_1.png',
   1: 'gui/ui_res_2/task/liveness_2_1.png',
   2: 'gui/ui_res_2/task/liveness_3_1.png',
   3: 'gui/ui_res_2/task/liveness_4_1.png',
   4: 'gui/ui_res_2/task/liveness_5_1.png'
   }

class RecruitReward(object):

    def __init__(self, main_panel):
        self.panel = global_data.uisystem.load_template_create('friend/i_friend_invite_2', parent=main_panel)
        self._input_box = None
        self._widgets = []
        self.init_panel()
        global_data.emgr.update_recruit_reward_st += self.update_widget_st
        global_data.emgr.update_recruit_num += self.update_recruit_num_progress
        global_data.emgr.update_recruit_score += self.update_recruit_score_progress
        global_data.emgr.update_recruit_verify_gift_st += self.update_recruit_verify_gift
        self.init_data()
        return

    def init_data(self):
        player = global_data.player
        self.update_recruit_num_progress(player._recruit_num)
        self.update_recruit_score_progress(player._recruit_score)
        self.update_recruit_verify_gift(player.get_recruit_verify_gift_st())

    def update_recruit_verify_gift(self, st):
        nd_content = self.panel.nd_be_invited.nd_content
        if st == 0:
            self.panel.nd_be_invited.setVisible(False)
            return
        if st == 1:
            nd_content.temp_btn_confirm.btn_common.SetEnable(False)
            nd_content.temp_btn_confirm.btn_common.SetText(get_text_by_id(10323))
            self.update_recruit_verify_gift_btn(nd_content.temp_reward, ITEM_UNRECEIVED)
            return
        if st == 2:
            self.panel.nd_be_invited.setVisible(False)
            return
        nd_content.temp_btn_confirm.btn_common.SetEnable(True)
        self.update_recruit_verify_gift_btn(nd_content.temp_reward, ITEM_UNGAIN)

    def update_recruit_verify_gift_btn(self, temp_reward, reward_state):
        if reward_state == ITEM_UNGAIN:
            temp_reward.nd_get.setVisible(False)
            temp_reward.nd_get_tips.setVisible(False)
        elif reward_state == ITEM_UNRECEIVED:
            temp_reward.nd_get.setVisible(False)
            temp_reward.nd_get_tips.setVisible(True)
        else:
            temp_reward.nd_get.setVisible(True)
            temp_reward.nd_get_tips.setVisible(False)
        if reward_state == ITEM_UNRECEIVED:
            temp_reward.PlayAnimation('get_tips')
        else:
            temp_reward.StopAnimation('get_tips')

    def recruit_verify_gift_btn_cb(self, *_):
        st = global_data.player.get_recruit_verify_gift_st()
        if st == 1:
            if global_data.channel.is_guest():
                global_data.channel.guest_bind()
            else:
                global_data.player.get_recruit_verify_gift()
        if st == 3:
            btn = self.panel.nd_be_invited.nd_content.temp_reward.btn_choose
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            item_id = get_show_verify_gift()
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos)
        return True

    def update_widget_st(self, uid):
        self._widgets[uid - 1].update_reward_status(ITEM_RECEIVED)
        self._widgets[uid - 1].nd.StopAnimation('get_tips')

    def update_all_widget_st(self):
        player = global_data.player
        for i in range(10):
            reward_st = player.get_recruit_reward_st(i + 1)
            if reward_st == ITEM_UNRECEIVED:
                self._widgets[i].nd.PlayAnimation('get_tips')

    def update_recruit_num_progress(self, num):
        percent = get_recruit_num_percent(num)
        self.panel.nd_people_reward.nd_content.prog_score.SetPercentage(percent)
        self.update_all_widget_st()

    def update_recruit_score_progress(self, score):
        percent = get_recruit_score_percent(score)
        self.panel.nd_main_reward.nd_content.prog_score.SetPercentage(percent)
        self.update_all_widget_st()
        self.panel.nd_main_reward.nd_tips.lab_score.setString(get_text_by_id(10322).format(score))

    def is_number(self, text):
        if text:
            try:
                ret = int(text)
                return ret
            except ValueError:
                pass

        return None

    def init_put(self):
        temp_input = self.panel.nd_be_invited.nd_content.temp_input
        self._input_box = InputBox(temp_input, max_length=20, placeholder=get_text_by_id(10327))
        ui = global_data.ui_mgr.get_ui('MainFriend')
        self._input_box.set_rise_widget(ui.panel)
        btn_common = self.panel.nd_be_invited.nd_content.temp_btn_confirm.btn_common

        @btn_common.unique_callback()
        def OnClick(*_):
            if global_data.channel.is_guest():
                global_data.channel.guest_bind()
            else:
                text = self._input_box.get_text()
                if self.is_number(text):
                    global_data.player.recruit_verify(text)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(10326))

    def init_panel(self):
        self.panel.nd_main_reward.nd_desc.setString(get_text_by_id(10303))
        self.panel.nd_people_reward.nd_desc.setString(get_text_by_id(10304))
        self.panel.nd_be_invited.nd_desc.setString(get_text_by_id(10305))
        self.panel.nd_be_invited.nd_content.lab_get.setString(get_text_by_id(10319))
        item_no = get_show_verify_gift()
        temp_reward = self.panel.nd_be_invited.nd_content.temp_reward
        template_utils.init_tempate_mall_i_item(temp_reward, item_no, callback=self.recruit_verify_gift_btn_cb)
        self.init_put()
        btn_tips = self.panel.nd_main_reward.nd_tips.btn_tips

        @btn_tips.unique_callback()
        def OnClick(*_):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_local_content(10324), get_text_local_content(10325))

        player = global_data.player
        num_reward = self.panel.nd_people_reward.nd_content.list_reward
        num_reward.DeleteAllSubItem()
        for i in range(5):
            item = num_reward.AddTemplateItem()
            img_box = IMG_BOX_PATH[i]
            item.img_box.SetDisplayFrameByPath('', img_box)
            img_box_get = IMG_BOX_GET_PATH[i]
            item.img_box_get.SetDisplayFrameByPath('', img_box_get)
            item_widget = VitalityBoxReward(item, i + 1, self.on_click_widget)
            item_widget.update_score(get_show_recruit_num(i))
            reward_st = player.get_recruit_reward_st(i + 1)
            if reward_st == ITEM_RECEIVED:
                item_widget.update_reward_status(ITEM_RECEIVED)
            elif reward_st == ITEM_UNRECEIVED:
                item_widget.nd.PlayAnimation('get_tips')
            self._widgets.append(item_widget)

        score_reward = self.panel.nd_main_reward.nd_content.list_reward
        score_reward.DeleteAllSubItem()
        for i in range(5):
            item = score_reward.AddTemplateItem()
            img_box = IMG_BOX_PATH[i]
            item.img_box.SetDisplayFrameByPath('', img_box)
            img_box_get = IMG_BOX_GET_PATH[i]
            item.img_box_get.SetDisplayFrameByPath('', img_box_get)
            item_widget = VitalityBoxReward(item, i + 6, self.on_click_widget)
            item_widget.update_score(get_show_recruit_score(i))
            reward_st = player.get_recruit_reward_st(i + 6)
            if reward_st == ITEM_RECEIVED:
                item_widget.update_reward_status(ITEM_RECEIVED)
            elif reward_st == ITEM_UNRECEIVED:
                item_widget.nd.PlayAnimation('get_tips')
            self._widgets.append(item_widget)

    def on_click_widget(self, btn, touch, lv):
        reward_st = global_data.player.get_recruit_reward_st(lv)
        if reward_st == ITEM_UNRECEIVED:
            global_data.player.receive_recruit_reward(lv)
        elif reward_st == ITEM_RECEIVED:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
        else:
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            reward_id = get_vitality_reward(lv)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)
        return True

    def refresh_score_list_reward(self):
        list_reward = self.panel.nd_main_reward.nd_content.list_reward
        for i, item in enumerate(list_reward.GetAllItem()):
            img_box = IMG_BOX_PATH[i]
            item.img_box.SetDisplayFrameByPath('', img_box)
            img_box_get = IMG_BOX_GET_PATH[i]
            item.img_box_get.SetDisplayFrameByPath('', img_box_get)

    def refresh_num_list_reward(self):
        list_reward = self.panel.nd_people_reward.nd_content.list_reward
        for i, item in enumerate(list_reward.GetAllItem()):
            img_box = IMG_BOX_PATH[i]
            item.img_box.SetDisplayFrameByPath('', img_box)
            img_box_get = IMG_BOX_GET_PATH[i]
            item.img_box_get.SetDisplayFrameByPath('', img_box_get)

    def show_panel(self):
        self.panel.setVisible(True)

    def hide_panel(self):
        self.panel.setVisible(False)

    def destroy(self):
        self.panel = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self._widgets = None
        global_data.emgr.update_recruit_reward_st -= self.update_widget_st
        global_data.emgr.update_recruit_num -= self.update_recruit_num_progress
        global_data.emgr.update_recruit_score -= self.update_recruit_score_progress
        global_data.emgr.update_recruit_verify_gift_st -= self.update_recruit_verify_gift
        return