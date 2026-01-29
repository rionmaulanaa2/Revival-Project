# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryBingoWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils.mall_utils import get_lottery_preview_data
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.template_utils import init_tempate_mall_i_simple_item
from logic.gcommon.common_utils.bingo_reward_utils import transit_to_mask, check_match_mask, check_all_match_mask
import cc
APPEARANCE_INTERVAL = 0.4
FLIP_INTERVAL = 0.07
LINK_INTERVAL = 0.033
LINE_INTERVAL = 0.26
BACKGROUND_PIC_PATH = 'gui/ui_res_2/activity/activity_202112/christmas/bingo/icon_christmas_bingo_item_{}.png'
COMMON_LINE_REWARD_PIC_BG = 'gui/ui_res_2/activity/activity_202112/christmas/bingo/bar_christmas_item_1.png'
SPECIAL_LINE_REWARD_PIC_BG = 'gui/ui_res_2/activity/activity_202112/christmas/bingo/bar_christmas_item_2.png'
ENTER_KEY = 0
SHOW_KEY = 1
FLIP_KEY = 2
LINE_KEY = 3
FULL_KEY = 4
SOUND_MAP = {ENTER_KEY: 'Play_ui_open',
   SHOW_KEY: 'Play_ui_draw_show',
   FLIP_KEY: 'Play_ui_draw',
   LINE_KEY: 'Play_ui_connect',
   FULL_KEY: 'Play_ui_compound'
   }

def play_bingo_sound(key):
    global_data.sound_mgr.post_event_2d(SOUND_MAP[key], None)
    return


class LotteryBingoWidget(object):

    def __init__(self, parent, panel, lottery_id, on_change_show_reward, index_list, nd_list, nd_row_reward_list, nd_column_reward_list, nd_left_up_diagonal_reward, nd_right_up_diagonal_reward):
        self.parent = parent
        self.panel = panel
        self.lottery_id = lottery_id
        self.on_change_show_reward = on_change_show_reward
        index_list = [ int(i) for i in index_list ]
        self.open_index_set = set(index_list)
        self.open_mask = transit_to_mask(index_list)
        self.nd_list = nd_list
        self.nd_row_reward_list = nd_row_reward_list
        self.nd_column_reward_list = nd_column_reward_list
        self.nd_left_up_diagonal_reward = nd_left_up_diagonal_reward
        self.nd_right_up_diagonal_reward = nd_right_up_diagonal_reward
        self.bingo_size = nd_row_reward_list.GetItemCount()
        self.bingo_grid_count = self.bingo_size * self.bingo_size
        self.line_appearance_list = []
        self.bingo_ret = ()
        self.z_order_idx = 1
        self.show_model_id = None
        self.core_reward_id_list = []
        self.show_model_item_id_set = set()
        self.init_panel()
        return

    @property
    def need_skip_anim(self):
        return self.parent.need_skip_anim

    def _initialize_nd_bingo_line_reward(self, nd_item, item_id, got):

        @global_unique_click(nd_item.btn_item)
        def OnClick(*args):
            self.on_change_show_reward(item_id)

        init_tempate_mall_i_simple_item(nd_item.temp_item, item_id)
        nd_item.temp_item.btn_choose.SetFrames('', ['', '', ''])
        nd_item.nd_got.setVisible(got)
        if item_id in self.core_reward_id_list:
            bg_path = SPECIAL_LINE_REWARD_PIC_BG
            if not got:
                nd_item.RecordAnimationNodeState('loop')
                nd_item.PlayAnimation('loop')
        else:
            bg_path = COMMON_LINE_REWARD_PIC_BG
        nd_item.btn_item.SetFrames('', [bg_path, bg_path, bg_path])

    def _get_flip_anim_action_list(self):
        action_list = [
         cc.CallFunc.create(lambda : play_bingo_sound(ENTER_KEY))]
        for i in range(self.bingo_size):
            row, column = 0, i
            while True:
                index = row * self.bingo_size + column
                if index not in self.open_index_set:
                    nd_item = self.nd_list.GetItem(index)
                    action_list.append(cc.CallFunc.create(lambda : play_bingo_sound(SHOW_KEY)))
                    action_list.append(cc.CallFunc.create(lambda nd=nd_item: nd.PlayAnimation('show')))
                if row == i:
                    break
                row += 1
                column -= 1

            action_list.append(cc.DelayTime.create(FLIP_INTERVAL))

        for i in range(1, self.bingo_size):
            row, column = i, self.bingo_size - 1
            while True:
                index = row * self.bingo_size + column
                if index not in self.open_index_set:
                    nd_item = self.nd_list.GetItem(index)
                    action_list.append(cc.CallFunc.create(lambda : play_bingo_sound(SHOW_KEY)))
                    action_list.append(cc.CallFunc.create(lambda nd=nd_item: nd.PlayAnimation('show')))
                if row == self.bingo_size - 1:
                    break
                row += 1
                column -= 1

            action_list.append(cc.DelayTime.create(FLIP_INTERVAL))

        return action_list

    def play_flip_anim(self):
        action_list = self._get_flip_anim_action_list()
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_panel(self):
        for i in range(self.bingo_grid_count):
            nd_bingo = self.nd_list.GetItem(i)
            nd_bingo.icon_item.SetDisplayFrameByPath('', BACKGROUND_PIC_PATH.format(i))
            nd_bingo.img_item.setVisible(False)

        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.play_flip_anim)]))
        match_row_list, match_column_list, left_up, right_up = check_all_match_mask(self.open_mask, self.bingo_size)
        conf = get_lottery_preview_data(self.lottery_id)
        core_reward_id_list = conf['core_rewards']
        self.show_model_id = core_reward_id_list[0]
        self.core_reward_id_list = core_reward_id_list
        self.show_model_item_id_set |= set(self.core_reward_id_list)
        row_item_id_list = conf['row_rewards']
        column_item_id_list = conf['column_rewards']
        match_row_set, match_column_set = set(match_row_list), set(match_column_list)
        for i in range(self.bingo_size):
            self._initialize_nd_bingo_line_reward(self.nd_row_reward_list.GetItem(i), row_item_id_list[i], i in match_row_set)
            self._initialize_nd_bingo_line_reward(self.nd_column_reward_list.GetItem(i), column_item_id_list[i], i in match_column_set)

        left_up_diagonal_item_id = conf['diagonal_left_up_reward']
        right_up_diagonal_item_id = conf['diagonal_right_up_reward']
        self._initialize_nd_bingo_line_reward(self.nd_left_up_diagonal_reward, left_up_diagonal_item_id, left_up)
        self._initialize_nd_bingo_line_reward(self.nd_right_up_diagonal_reward, right_up_diagonal_item_id, right_up)
        self.show_model_item_id_set |= set(row_item_id_list)
        self.show_model_item_id_set |= set(column_item_id_list)
        self.show_model_item_id_set.add(left_up_diagonal_item_id)
        self.show_model_item_id_set.add(right_up_diagonal_item_id)

    def destroy(self):
        self.parent = None
        self.panel = None
        self.on_change_show_reward = None
        self.nd_list = None
        self.nd_row_reward_list = None
        self.nd_column_reward_list = None
        self.nd_left_up_diagonal_reward = None
        self.nd_right_up_diagonal_reward = None
        self.line_appearance_list = None
        return

    @staticmethod
    def _play_line_reward_got_anim(nd_item):
        if nd_item.IsPlayingAnimation('loop'):
            nd_item.StopAnimation('loop')
            nd_item.RecoverAnimationNodeState('loop')
        nd_item.PlayAnimation('disappear')

    @staticmethod
    def _add_item_link_appearance(action_list, nd_item, line_anim_name):
        action_list.append(cc.CallFunc.create(lambda nd=nd_item: nd.PlayAnimation('show_03')))
        action_list.append(cc.CallFunc.create(lambda nd=nd_item: nd.PlayAnimation(line_anim_name)))
        action_list.append(cc.DelayTime.create(LINK_INTERVAL))

    def _add_link_reward_got_appearance(self, action_list, nd_item):
        action_list.append(cc.CallFunc.create(lambda : self._play_line_reward_got_anim(nd_item)))
        action_list.append(cc.DelayTime.create(LINE_INTERVAL))

    def add_row_line_appearance(self, row):
        action_list = [
         cc.CallFunc.create(lambda : play_bingo_sound(LINE_KEY))]
        start = self.bingo_size * row
        for i in range(start, start + self.bingo_size):
            nd_item = self.nd_list.GetItem(i)
            self._add_item_link_appearance(action_list, nd_item, 'show_05')

        self._add_link_reward_got_appearance(action_list, self.nd_row_reward_list.GetItem(row))
        self.line_appearance_list.extend(action_list)

    def add_column_line_appearance(self, column):
        action_list = [
         cc.CallFunc.create(lambda : play_bingo_sound(LINE_KEY))]
        for i in range(self.bingo_size):
            nd_item = self.nd_list.GetItem(column + self.bingo_size * i)
            self._add_item_link_appearance(action_list, nd_item, 'show_04')

        self._add_link_reward_got_appearance(action_list, self.nd_column_reward_list.GetItem(column))
        self.line_appearance_list.extend(action_list)

    def add_left_up_diagonal_line_appearance(self):
        action_list = [
         cc.CallFunc.create(lambda : play_bingo_sound(LINE_KEY))]
        for i in range(self.bingo_size):
            nd_item = self.nd_list.GetItem(i + self.bingo_size * i)
            self._add_item_link_appearance(action_list, nd_item, 'show_06')

        self._add_link_reward_got_appearance(action_list, self.nd_left_up_diagonal_reward)
        self.line_appearance_list.extend(action_list)

    def add_right_up_diagonal_line_appearance(self):
        action_list = [
         cc.CallFunc.create(lambda : play_bingo_sound(LINE_KEY))]
        index_sum = self.bingo_size - 1
        for i in range(self.bingo_size):
            nd_item = self.nd_list.GetItem(index_sum - i + self.bingo_size * i)
            self._add_item_link_appearance(action_list, nd_item, 'show_07')

        self._add_link_reward_got_appearance(action_list, self.nd_right_up_diagonal_reward)
        self.line_appearance_list.extend(action_list)

    def update_open_mask(self, index):
        match_row, match_column, left_up, right_up = check_match_mask(self.open_mask, index, self.bingo_size)
        if match_row != -1:
            self.add_row_line_appearance(match_row)
        if match_column != -1:
            self.add_column_line_appearance(match_column)
        if left_up:
            self.add_left_up_diagonal_line_appearance()
        if right_up:
            self.add_right_up_diagonal_line_appearance()

    def update_open_mask_when_skip_anim(self, index):
        match_row, match_column, left_up, right_up = check_match_mask(self.open_mask, index, self.bingo_size)
        if match_row != -1:
            self._play_line_reward_got_anim(self.nd_row_reward_list.GetItem(match_row))
        if match_column != -1:
            self._play_line_reward_got_anim(self.nd_column_reward_list.GetItem(match_column))
        if left_up:
            self._play_line_reward_got_anim(self.nd_left_up_diagonal_reward)
        if right_up:
            self._play_line_reward_got_anim(self.nd_right_up_diagonal_reward)

    def show_lottery_result(self):
        global_data.emgr.refresh_common_reward_ui_performance_temporarily.emit(0.05, True)
        global_data.emgr.receive_award_succ_event_from_lottery.emit(*self.bingo_ret)
        global_data.emgr.on_lottery_ended_event.emit()
        global_data.emgr.player_money_info_update_event.emit()
        self.bingo_ret = ()

    def _play_opened_anim(self, nd_item, anim_name):
        nd_item.setLocalZOrder(self.z_order_idx)
        self.z_order_idx += 1
        nd_item.PlayAnimation(anim_name)
        play_bingo_sound(FLIP_KEY)

    def _add_all_bingo_appearance(self, action_list):
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('full_show')))
        action_list.append(cc.CallFunc.create(lambda : play_bingo_sound(FULL_KEY)))
        action_list.append(cc.DelayTime.create(1.0))

    def set_bingo_opened(self, item_list, origin_list, extra_data):
        self.bingo_ret = (
         item_list, origin_list)
        action_list = [cc.DelayTime.create(0.5)]
        if self.need_skip_anim:
            for index in extra_data.get('bingo_index_list', []):
                if index not in self.open_index_set:
                    self.update_open_mask_when_skip_anim(index)
                    self.open_index_set.add(index)
                    nd_item = self.nd_list.GetItem(index)
                    nd_item.img_item.setOpacity(0)

            if len(self.open_index_set) == self.bingo_grid_count:
                self._add_all_bingo_appearance(action_list)
            action_list.append(cc.CallFunc.create(self.show_lottery_result))
        else:
            for index in extra_data.get('bingo_index_list', []):
                if index in self.open_index_set:
                    anim_name = 'show_02'
                else:
                    anim_name = 'show_01'
                    self.update_open_mask(index)
                    self.open_index_set.add(index)
                nd_item = self.nd_list.GetItem(index)
                action_list.append(cc.CallFunc.create(lambda nd=nd_item, anim=anim_name: self._play_opened_anim(nd, anim)))
                action_list.append(cc.DelayTime.create(APPEARANCE_INTERVAL))

            action_list.extend(self.line_appearance_list)
            if len(self.open_index_set) == self.bingo_grid_count:
                self._add_all_bingo_appearance(action_list)
            action_list.append(cc.CallFunc.create(self.show_lottery_result))
            self.line_appearance_list = []
        self.panel.runAction(cc.Sequence.create(action_list))

    def refresh_show_model(self, show_model_id=None):
        if str(show_model_id) in self.show_model_item_id_set:
            self.show_model_id = show_model_id
        self.on_change_show_reward(self.show_model_id)