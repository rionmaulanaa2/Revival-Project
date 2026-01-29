# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaLotteryWidgetUI.py
from __future__ import absolute_import
import time
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_VKB_NO_EFFECT, UI_TYPE_MESSAGE, BASE_LAYER_ZORDER_1
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.gcommon.cdata.global_lottery_config import get_global_lottery_conf
from logic.gutils import item_utils

class KizunaLotteryWidgetUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202212/music_lottery/i_music_lottery_item'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_btn_1.btn_common.OnClick': 'on_click_btn_draw'
       }
    GLOBAL_EVENT = {'into_concert_view_camera_event': 'on_into_concert_view_camera',
       'net_login_reconnect_event': 'on_net_reconnect',
       'net_reconnect_event': 'on_net_reconnect',
       'update_battle_data': 'on_update_battle_data'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'concert_lottery': {'node': 'temp_pc'}}
    HOT_KEY_FUNC_MAP = {'concert_lottery': 'on_keyboard_concert_lottery'
       }
    LOTTERY_TIMER_TAG = 221216
    HIDE_LOTTERY_TIMER_TAG = 221217
    LOTTERY_POP_TIMER_TAG = 221227

    def on_init_panel(self, *args, **kwargs):
        self.regist_main_ui()
        self.cur_concert_idx = -1
        self.lottery_disappear_time = 6
        self._target_time = 0
        self._timer = 0
        self.region_lottery_id_list = []
        self.is_in_hide_act = False
        self.panel.nd_lottery.setVisible(False)
        self.panel.nd_tips.setVisible(False)
        self._is_in_concert_view = False
        self.update_lottery_id_list()
        self.register_count_timer()
        self.check_lottery_count_down_time()

    def on_finalize_panel(self):
        self.unregist_main_ui()
        self.unregister_time_text_timer()
        self.unregister_count_timer()

    def update_lottery_id_list(self):
        if not global_data.battle:
            return
        if self.cur_concert_idx == global_data.battle.concert_idx:
            return
        self.cur_concert_idx = global_data.battle.concert_idx
        from logic.gutils.concert_utils import get_concert_region_lottery_id_list
        region_lottery_id_list = get_concert_region_lottery_id_list()
        self.region_lottery_id_list = region_lottery_id_list
        self.open_time_list = self.get_open_time()

    def on_net_reconnect(self, *args):
        self.check_lottery_count_down_time()

    def check_lottery_count_down_time(self):
        next_index = self.get_next_show_lottery_index()
        if next_index is None:
            return
        else:
            server_time = tutil.get_server_time()
            open_time, close_time = self.open_time_list[next_index]
            if open_time <= server_time <= close_time:
                if not global_data.player:
                    return
                self.show_lottery_ui(next_index)
            elif open_time > server_time:
                pass
            return

    def check_show(self):
        self.update_lottery_id_list()
        next_index = self.get_next_show_lottery_index()
        if next_index is None:
            return
        else:
            server_time = tutil.get_server_time()
            open_time, close_time = self.open_time_list[next_index]
            if open_time <= server_time <= close_time:
                if not self.panel.nd_lottery.isVisible():
                    if not global_data.player:
                        return
                    self.show_lottery_ui(next_index)
            return

    def register_count_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(1),
         cc.CallFunc.create(self.check_show)]))
        self.panel.runAction(act)
        act.setTag(self.LOTTERY_POP_TIMER_TAG)

    def unregister_count_timer(self):
        self.panel.stopActionByTag(self.LOTTERY_POP_TIMER_TAG)

    def get_open_time(self):
        time_list = []
        for lottery_id in self.region_lottery_id_list:
            lottery_conf = get_global_lottery_conf(lottery_id)
            start_time = lottery_conf.get('start_time', 0)
            settle_time = lottery_conf.get('settle_time', 0)
            time_list.append([start_time, settle_time])

        return time_list

    def get_next_show_lottery_index(self):
        server_time = tutil.get_server_time()
        for index, time_range in enumerate(self.open_time_list):
            open_time, close_time = time_range
            if open_time <= server_time <= close_time:
                return index
            if open_time > server_time:
                return index

        return None

    def get_progressing_show_lottery_index(self):
        server_time = tutil.get_server_time()
        for index, time_range in enumerate(self.open_time_list):
            open_time, close_time = time_range
            if open_time <= server_time <= close_time:
                return index

        return None

    def unregister_time_text_timer(self):
        self.panel.stopActionByTag(self.LOTTERY_TIMER_TAG)

    def register_time_text_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act.setTag(self.LOTTERY_TIMER_TAG)

    def register_hide_lottery_timer(self):
        if self.is_in_hide_act:
            return
        act = cc.Sequence.create([
         cc.DelayTime.create(3),
         cc.CallFunc.create(self.check_show_tips),
         cc.DelayTime.create(3),
         cc.CallFunc.create(self.hide_lottery_ui)])
        self.panel.runAction(act)
        act.setTag(self.HIDE_LOTTERY_TIMER_TAG)
        self.is_in_hide_act = True

    def refresh_time(self):
        server_time = tutil.get_server_time()
        left_time = int(self._target_time - server_time)
        if left_time > 0:
            self.panel.lab_time.SetString(get_text_by_id(633922).format(tutil.get_readable_time_hour_minitue_sec(left_time)))
        elif self.panel.nd_lottery.isVisible():
            self.panel.lab_time.SetString(633933)
            self.unregister_time_text_timer()
            self.register_hide_lottery_timer()

    def show_lottery_ui(self, index):
        if index >= len(self.open_time_list) or index is None:
            return
        else:
            open_time, close_time = self.open_time_list[index]
            self._target_time = close_time
            if self.has_participate_round(index):
                self.panel.temp_btn_1.btn_common.SetText(633934)
                self.panel.temp_btn_1.btn_common.SetEnable(False)
                self.panel.btn.SetEnable(False)
            else:
                self.panel.temp_btn_1.btn_common.SetText(633923)
                self.panel.temp_btn_1.btn_common.SetEnable(True)
                self.panel.btn.SetEnable(True)
            self.panel.lab_round.SetString(get_text_by_id(633924).format(index + 1))
            if index + 1 < len(self.open_time_list):
                next_open_time, next_close_time = self.open_time_list[index + 1]
                left_min = int((next_open_time - close_time) / 60.0)
                self.panel.lab_tips.SetString(get_text_by_id(633921).format(left_min))
            else:
                self.panel.lab_tips.SetString('')
            if index == 0:
                self.panel.lab_title.SetString(633926)
            elif index == 1:
                self.panel.lab_title.SetString(633927)
            else:
                self.panel.lab_title.SetString(1600080)
            lottery_id = self.get_cur_lottery_id(index)
            lottery_conf = get_global_lottery_conf(lottery_id)
            lottery_rewards = lottery_conf.get('lottery_reward', [(None, 0)])
            first_reward_id = lottery_rewards[0][0]
            reward_conf = confmgr.get('common_reward_data', str(first_reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if reward_list:
                item_no, item_num = reward_list[0]
                pic = item_utils.get_lobby_item_pic_by_item_no(item_no)
                self.panel.item.SetDisplayFrameByPath('', pic)
            if index == 1:
                self.panel.bar_1.setVisible(False)
                self.panel.bar_2.setVisible(True)
            elif index == 2:
                self.panel.bar_1.setVisible(False)
                self.panel.bar_2.setVisible(False)
            else:
                self.panel.bar_1.setVisible(True)
                self.panel.bar_2.setVisible(True)
            self.panel.nd_lottery.setVisible(True)
            self.register_time_text_timer()
            self.refresh_time()
            return

    def hide_lottery_ui(self):
        if not (self.panel and self.panel.isValid()):
            return
        self.unregister_time_text_timer()
        self.panel.nd_lottery.setVisible(False)
        self.panel.nd_tips.setVisible(False)
        self.is_in_hide_act = False

    def get_cur_lottery_id(self, index):
        if not global_data.player:
            return True
        if index >= len(self.region_lottery_id_list):
            return True
        lottery_id = self.region_lottery_id_list[index]
        return lottery_id

    def has_participate_round(self, index):
        lottery_id = self.get_cur_lottery_id(index)
        if lottery_id:
            return global_data.player.has_attend_global_lottery(lottery_id)
        else:
            return True

    def on_click_btn_draw(self, btn, touch):
        if not global_data.player:
            return
        else:
            bullet_chat_list = confmgr.get('game_mode/concert/play_data', str('bullet_chat_list'), default=['', '', ''])
            index = self.get_next_show_lottery_index()
            if index < len(bullet_chat_list) and index is not None:
                global_data.player.attend_global_anniversary_lottery()
                self.panel.temp_btn_1.btn_common.SetText(633934)
                self.panel.temp_btn_1.btn_common.SetEnable(False)
                self.panel.btn.SetEnable(False)
                if self._is_in_concert_view:
                    self.panel.SetTimeOut(3.0, self.update_concert_view, tag=20221224)
                self.panel.SetTimeOut(1.0, self.on_update_battle_data, tag=20240113)
                from logic.gcommon.common_const import chat_const
                extra_data = {'type': chat_const.MSG_TYPE_CONCERT_BULLET,
                   'text': bullet_chat_list[index]
                   }
                global_data.player.send_msg(chat_const.CHAT_BATTLE_WORLD, pack_text(bullet_chat_list[index]), extra=extra_data)
            return

    def check_show_tips(self):
        next_index = self.get_next_show_lottery_index()
        if next_index is not None:
            self.panel.nd_tips.setVisible(True)
        else:
            self.panel.nd_tips.setVisible(False)
        return

    def on_into_concert_view_camera(self, is_in):
        if not global_data.player:
            return
        self._is_in_concert_view = is_in
        self.update_concert_view()

    def update_concert_view(self):
        is_in = self._is_in_concert_view
        if is_in:
            index = self.get_progressing_show_lottery_index()
            if index is not None:
                if self.has_participate_round(index):
                    self.add_hide_count('concert_view')
                else:
                    self.add_show_count('concert_view')
        else:
            self.add_show_count('concert_view')
        return

    def on_keyboard_concert_lottery(self, btn, touch):
        self.on_click_btn_draw(None, None)
        return

    def on_update_battle_data(self, *args):
        if not global_data.battle:
            return
        else:
            if global_data.battle.is_king_or_defier_player():
                index = self.get_next_show_lottery_index()
                if index is not None:
                    if self.has_participate_round(index):
                        self.add_hide_count('concert_battle')
            else:
                self.add_show_count('concert_battle')
            return