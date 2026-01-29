# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgePromptUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils import career_utils
from common.uisys.basepanel import BasePanel

class BadgePromptData(object):

    def __init__(self, sub_branch, lv):
        self.sub_branch = sub_branch
        self.lv = lv


class CareerBadgePromptUI(BasePanel):
    PANEL_CONFIG_NAME = 'life/get_achievement'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    DELAY_CLOSE_TAG = 31415926

    def on_init_panel(self, *args, **kwargs):
        super(CareerBadgePromptUI, self).on_init_panel()
        self._msg_queue = []
        self._is_playing = False
        self._finish_cb = None
        return

    def set_finish_cb(self, cb):
        self._finish_cb = cb

    def on_finalize_panel(self):
        del self._msg_queue[:]
        super(CareerBadgePromptUI, self).on_finalize_panel()
        if callable(self._finish_cb):
            self._finish_cb()

    def _refresh_single_badge(self, node, sub_branch, lv):
        badge_item = node.temp_icon
        career_utils.refresh_badge_item(badge_item, sub_branch, lv, check_got=False)
        node.lab_name.SetString(career_utils.get_badge_name_text(sub_branch))

    def push(self, prompt_data_list):
        if not prompt_data_list:
            return
        self._msg_queue.append(prompt_data_list)
        self.play()

    def play(self):
        if self._is_playing:
            return
        if not self._msg_queue:
            return
        self._is_playing = True
        prompt_data_list = self._msg_queue.pop(0)
        each_msg_play_time = self._play_single_msg(prompt_data_list)
        if each_msg_play_time == 0.0:
            self._each_play_ended()
        else:
            self.panel.SetTimeOut(each_msg_play_time, self._each_play_ended)

    def _each_play_ended(self):
        if not self._msg_queue:
            self._is_playing = False
            self.panel.PlayAnimation('disappear')
            disappear_time = self.panel.GetAnimationMaxRunTime('disappear')

            def cb():
                self.close()

            self.panel.DelayCallWithTag(disappear_time, cb, self.DELAY_CLOSE_TAG)
            return
        prompt_data_list = self._msg_queue.pop(0)
        each_msg_play_time = self._play_single_msg(prompt_data_list)
        if each_msg_play_time == 0.0:
            self._each_play_ended()
        else:
            self.panel.SetTimeOut(each_msg_play_time, self._each_play_ended)

    def _play_single_msg(self, prompt_data_list):
        self.panel.PlayAnimation('appear')
        leng = len(prompt_data_list)
        if leng > 6:
            self.panel.list_achievement_6up.setVisible(True)
            self.panel.list_achievement.setVisible(False)
            list_node = self.panel.list_achievement_6up
            bg_node = list_node.img_bar_6up
        else:
            self.panel.list_achievement.setVisible(True)
            self.panel.list_achievement_6up.setVisible(False)
            list_node = self.panel.list_achievement
            bg_node = list_node.img_bar
        list_node.SetInitCount(leng)
        interval_each = 0.1
        DELAY_APPEAR_BADGE_TAG = 31415926
        each_msg_play_time = 0.0
        for i, prompt_data in enumerate(prompt_data_list):
            node = list_node.GetItem(i)
            sub_branch, lv = prompt_data.sub_branch, prompt_data.lv
            self._refresh_single_badge(node, sub_branch, lv)
            delay_appear_time = interval_each * i
            node.setVisible(False)

            def cb(node=node):
                if node.isValid():
                    node.setVisible(True)
                    node.PlayAnimation('appear')

            node.DelayCallWithTag(delay_appear_time, cb, DELAY_APPEAR_BADGE_TAG)
            if i + 1 == leng:
                each_msg_play_time = delay_appear_time + node.GetAnimationMaxRunTime('appear')

        bg_node.ResizeAndPositionSelf()
        return each_msg_play_time + 3.0