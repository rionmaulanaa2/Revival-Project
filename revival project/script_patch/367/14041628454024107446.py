# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryTurntableWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.mall_utils import get_lottery_turntable_item_data
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no, get_lobby_item_pic_by_item_no, get_item_rare_degree, REWARD_RARE_COLOR, check_skin_tag
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.item.item_const import RARE_DEGREE_6
from logic.gcommon.item import lobby_item_type
from common.utils.timer import CLOCK, RELEASE
from math import fabs
import cc

def _register_role_skin_item_cb(nd_btn, item_id, item_belong_no):

    @global_unique_click(nd_btn)
    def OnClick(btn, touch):
        ui = global_data.ui_mgr.get_ui('RoleInfoUI')
        if ui:
            ui.clear_show_count_dict()
            ui.hide_main_ui()
        else:
            ui = global_data.ui_mgr.show_ui('RoleInfoUI', 'logic.comsys.role_profile')
        ui.set_role_id(item_belong_no)
        ui.jump_to_skin(item_id)


def _register_mecha_skin_item_cb(nd_btn, item_id, item_belong_no):
    item_belong_no = mecha_lobby_id_2_battle_id(item_belong_no)

    @global_unique_click(nd_btn)
    def OnClick(btn, touch):
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        if ui:
            ui.clear_show_count_dict()
            ui.hide_main_ui()
        else:
            ui = global_data.ui_mgr.show_ui('MechaDetails', 'logic.comsys.mecha_display')
        ui.show_mecha_details(item_belong_no)
        ui.jump_to_skin(item_id)


def _register_vehicle_skin_or_gun_skin_item_cb(nd_btn, item_id, *args):

    @global_unique_click(nd_btn)
    def OnClick(btn, touch):
        ui = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        if ui:
            ui.clear_show_count_dict()
            ui.hide_main_ui()
            ui.select_item(item_id)
        else:
            from logic.comsys.items_book_ui.ItemsBookMainUI import ItemsBookMainUI
            ItemsBookMainUI(item_no=item_id)


def _register_other_item_cb(nd_btn, item_id, *args):

    @nd_btn.unique_callback()
    def OnBegin(btn, touch, *args):
        position = touch.getLocation()
        global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position, extra_info={'show_jump': False})
        return

    @nd_btn.unique_callback()
    def OnEnd(*args):
        global_data.emgr.hide_item_desc_ui_event.emit()


ND_BTN_REGISTER_FUNC = {lobby_item_type.L_ITEM_TYPE_ROLE_SKIN: _register_role_skin_item_cb,
   lobby_item_type.L_ITEM_TYPE_MECHA_SKIN: _register_mecha_skin_item_cb,
   lobby_item_type.L_ITEM_YTPE_VEHICLE_SKIN: _register_vehicle_skin_or_gun_skin_item_cb,
   lobby_item_type.L_ITME_TYPE_GUNSKIN: _register_vehicle_skin_or_gun_skin_item_cb
   }
ITEM_DEFAULT_STATE = 0
ITEM_PASS_STATE = 1
ITEM_CHOSEN_STATE = 2
ITEM_LOOP_STATE = 3
DEFAULT_ANIM_NAME_MAP = {ITEM_PASS_STATE: [
                   'pass'],
   ITEM_CHOSEN_STATE: [
                     'choosed'],
   ITEM_LOOP_STATE: [
                   'loop']
   }
NEED_ADJUST_RARE_DEGREE_PIC_MAP = {'mall/i_collection_activity/common_7times/i_lottery_common_7times_item_1': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_7times/i_lottery_common_7times_item_1_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_7times/i_lottery_common_7times_item_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_2_{}.png',
   'mall/i_collection_activity/common_9times/i_lottery_common_9times_item_1': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_9times/i_lottery_common_9times_item_1_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_9times/i_lottery_common_9times_item_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_2_{}.png',
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_1': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_1_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_1_{}.png',
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_2': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_2_{}.png',
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_4': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_4_{}.png'
   }
NEED_ADJUST_POS_TEMPLATE_DICT = {'mall/i_collection_activity/common_7times/i_lottery_common_7times_item_1': [
                                                                             ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)],
   'mall/i_collection_activity/common_7times/i_lottery_common_7times_item_1_2': [
                                                                               ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)],
   'mall/i_collection_activity/common_9times/i_lottery_common_9times_item_1': [
                                                                             ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)],
   'mall/i_collection_activity/common_9times/i_lottery_common_9times_item_1_2': [
                                                                               ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)],
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_1': [
                                                                                        ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)],
   'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_1_2': [
                                                                                          ('50%0', '50%123', 0.54), ('50%0', '50%69', 0.54)]
   }

class LotteryTurntableWidget(object):

    def __init__(self, parent, panel, lottery_id, turntable_item_list=None, nd_item_format='temp_item_{}', nd_click_name='', need_adjust_rare_degree_pic_template=None, rare_degree_pic_map=None, item_anim_name_map=None, play_item_anim_func_map=None, get_item_action_extra_delay_func_map=None, init_item_data_func=None, init_item_event_func=None, max_single_interval=0.8, med_single_interval=0.1, min_single_interval=0.05, high_speed_count_percent=0.8, max_delighted_time=2, continual_interval=0.03, need_show_got=False, get_nd_got_func=None, check_item_got_func=None, refresh_nd_got_func=None, need_anim_skip_got_item=False, block_show_lottery_result_callback=None, continual_count_reserve_anim=False, get_last_clicked_lottery_count=None):
        self.parent = parent
        self.panel = panel
        self.lottery_id = lottery_id
        self.turntable_item_list = turntable_item_list if turntable_item_list else get_lottery_turntable_item_data(lottery_id)
        self.nd_item_format = nd_item_format
        self.nd_click_name = nd_click_name
        self.need_adjust_rare_degree_pic_template = need_adjust_rare_degree_pic_template
        self.rare_degree_pic_map = rare_degree_pic_map
        self.continual_count_reserve_anim = continual_count_reserve_anim
        self.get_last_clicked_lottery_count = get_last_clicked_lottery_count
        self.item_anim_name_map = item_anim_name_map if item_anim_name_map else DEFAULT_ANIM_NAME_MAP
        for state, anim_name in six.iteritems(self.item_anim_name_map):
            if type(anim_name) == str:
                self.item_anim_name_map[state] = [
                 anim_name]

        self.play_item_anim_func_map = dict()
        if play_item_anim_func_map is None:
            play_item_anim_func_map = {}
        for state in six.iterkeys(self.item_anim_name_map):
            self.play_item_anim_func_map[state] = play_item_anim_func_map.get(state, self._default_play_item_anim_func)

        self.get_item_action_extra_delay_func_map = get_item_action_extra_delay_func_map if get_item_action_extra_delay_func_map else {}
        self.init_item_data_func = init_item_data_func if init_item_data_func else self._init_item_data
        self.init_item_event_func = init_item_event_func if init_item_event_func else self._init_item_event
        self.max_single_interval = max_single_interval
        self.med_single_interval = med_single_interval
        self.min_single_interval = min_single_interval
        self.high_speed_count_percent = high_speed_count_percent
        self.max_delighted_time = max_delighted_time
        self.max_delighted_time_cache = max_delighted_time
        self.continual_interval = continual_interval
        self.need_show_got = need_show_got
        self.get_nd_got_func = get_nd_got_func
        self.check_item_got_func = check_item_got_func
        self.refresh_nd_got_func = refresh_nd_got_func
        self.need_anim_skip_got_item = need_anim_skip_got_item
        self.block_show_lottery_result_callback = block_show_lottery_result_callback
        self.refresh_turntable_item_list()
        self.cur_draw_lottery_count = SINGLE_LOTTERY_COUNT
        self.cur_delight_item_index = 0
        self.delight_anim_timer = None
        self.delight_interval = self.min_single_interval
        self.delta_delight_interval = 0.0
        self.final_delta_delight_interval = 0.0
        self.turntable_ret = ()
        self.target_delight_item_index_list = []
        self.target_delight_item_count = 0
        self.target_delighted_time = 0
        self.choose_anim_timer = None
        self.choose_item_index = 0
        self.show_lottery_result_enabled = True
        return

    def refresh_turntable_item_list(self, turntable_item_list=None):
        if turntable_item_list:
            self.turntable_item_list = turntable_item_list
            self.stop_all_turntable_item_state_anim()
        self.turntable_item_chosen_sound_name_list = []
        self.turntable_item_map = dict()
        self.turntable_item_node_list = []
        self.turntable_item_anim_sequence = []
        for index, (item_id, item_count) in enumerate(self.turntable_item_list):
            rare_degree = get_item_rare_degree(item_id)
            if rare_degree == RARE_DEGREE_6:
                sound_name = 'lottery_spluse' if 1 else 'lottery_normal'
                self.turntable_item_chosen_sound_name_list.append(sound_name)
                self.turntable_item_map[int(item_id), item_count] = index
                item_node = self._get_turntable_item_node(index)
                self.init_item_data_func(item_node, item_id, item_count)
                self.init_item_event_func(item_node, item_id, item_count)
                got = False
                if self.need_show_got:
                    nd_got = self.get_nd_got_func(item_node, index)
                    if nd_got:
                        got = self.check_item_got_func(item_node, item_id, index)
                        nd_got.setVisible(got)
                if self.need_anim_skip_got_item:
                    if not got:
                        self.turntable_item_anim_sequence.append(index)
                else:
                    self.turntable_item_anim_sequence.append(index)
                for anim_name in six_ex.values(self.item_anim_name_map):
                    for name in anim_name:
                        item_node.RecordAnimationNodeState(name)

                self.turntable_item_node_list.append(item_node)

        self.turntable_item_count = len(self.turntable_item_list)
        self.turntable_item_anim_sequence_length = len(self.turntable_item_anim_sequence)

    @property
    def need_skip_anim(self):
        return self.parent.need_skip_anim

    def _release_delight_anim_timer(self):
        if self.delight_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.delight_anim_timer)
            self.delight_anim_timer = None
        return

    def _release_choose_anim_timer(self):
        if self.choose_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.choose_anim_timer)
            self.choose_anim_timer = None
        return

    def destroy(self):
        self.parent = None
        self.panel = None
        self.init_item_data_func = None
        self.init_item_data_func = None
        self.get_nd_got_func = None
        self.check_item_got_func = None
        self.refresh_nd_got_func = None
        self.play_item_anim_func_map = None
        self.get_item_action_extra_delay_func_map = None
        self._release_delight_anim_timer()
        self._release_choose_anim_timer()
        return

    def _get_turntable_item_node(self, index):
        return getattr(self.panel, self.nd_item_format.format(str(index + 1)), None)

    def _init_item_data(self, nd, item_id, item_count):
        nd.lab_num.SetString('x ' + str(item_count))
        nd.lab_num.setVisible(item_count > 1)
        if nd.img_reward._cur_target_path is None:
            nd.img_reward.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_id))
        rare_degree = get_item_rare_degree(item_id)
        if self.need_adjust_rare_degree_pic_template and nd.GetTemplatePath() == self.need_adjust_rare_degree_pic_template:
            pic_path = self.rare_degree_pic_map.get(rare_degree, None)
            if pic_path:
                nd.btn_item_bg.SetFrames('', [pic_path, pic_path, pic_path], True, None)
        pic_path = NEED_ADJUST_RARE_DEGREE_PIC_MAP.get(nd.GetTemplatePath())
        if pic_path:
            nd.temp_kind and check_skin_tag(nd.temp_kind, item_id)
            nd_click = nd.nd_click
            if nd_click:
                color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
                color_pic_path = pic_path.format(color)
                nd_click.SetFrames('', [color_pic_path, color_pic_path, color_pic_path], True, None)
        pos_info = NEED_ADJUST_POS_TEMPLATE_DICT.get(nd.GetTemplatePath())
        img_reward = nd.img_cut.img_reward
        if pos_info and img_reward:
            item_type = get_lobby_item_type(item_id)
            if item_type == lobby_item_type.L_ITEM_TYPE_MECHA_SKIN or item_type == lobby_item_type.L_ITEM_TYPE_ROLE_SKIN:
                pos_x, pos_y, scale = pos_info[0]
                img_reward.SetPosition(pos_x, pos_y)
                img_reward.setScale(scale)
            else:
                pos_x, pos_y, scale = pos_info[1]
                img_reward.SetPosition(pos_x, pos_y)
                img_reward.setScale(scale)
        return

    def _init_item_event(self, nd, item_id, item_count):
        item_type = get_lobby_item_type(item_id)
        item_belong_no = get_lobby_item_belong_no(item_id)
        register_func = ND_BTN_REGISTER_FUNC.get(item_type, _register_other_item_cb)
        if not self.nd_click_name:
            register_func(nd, item_id, item_belong_no)
        else:
            register_func(getattr(nd, self.nd_click_name, nd), item_id, item_belong_no)

    def _default_play_item_anim_func(self, nd, anim_name, item_id, **kwargs):
        for single_anim_name in anim_name:
            nd.HasAnimation(single_anim_name) and nd.PlayAnimation(single_anim_name, **kwargs)

    def _play_item_anim(self, nd, state, item_id, **kwargs):
        anim_name = self.item_anim_name_map[state]
        self.play_item_anim_func_map[state](nd, anim_name, item_id, **kwargs)

    def _get_play_item_action_list(self, nd, state, item_id, need_action_wait=False, advance_time=0.0):
        anim_name = self.item_anim_name_map.get(state, None)
        if anim_name is None:
            return []
        else:
            ret = []
            max_anim_duration = 0.0
            valid_anim_name = []
            for single_anim_name in anim_name:
                if nd.HasAnimation(single_anim_name):
                    valid_anim_name.append(single_anim_name)
                    if need_action_wait:
                        max_anim_duration = max(max_anim_duration, nd.GetAnimationMaxRunTime(single_anim_name))

            action_play = cc.CallFunc.create(lambda : self.play_item_anim_func_map[state](nd, valid_anim_name, item_id))
            ret.append(action_play)
            if need_action_wait:
                action_wait = cc.DelayTime.create(max_anim_duration - advance_time)
                ret.append(action_wait)
            if state in self.get_item_action_extra_delay_func_map:
                delay_time = self.get_item_action_extra_delay_func_map[state](nd, item_id)
                if delay_time:
                    ret.append(cc.DelayTime.create(delay_time))
            return ret

    def _reset_turntable_items(self):
        for index in self.target_delight_item_index_list:
            item = self.turntable_item_node_list[index]
            item.pnl_repeat and item.pnl_repeat.setVisible(False)
            for anim_name in six_ex.values(self.item_anim_name_map):
                for name in anim_name:
                    item.StopAnimation(name)
                    item.RecoverAnimationNodeState(name)

        self.target_delight_item_index_list = []
        self.target_delight_item_count = 0

    def show_lottery_result(self):
        if not self.show_lottery_result_enabled:
            self.block_show_lottery_result_callback and self.block_show_lottery_result_callback()
            self.refresh_all_show_got_node()
            return
        global_data.emgr.refresh_common_reward_ui_performance_temporarily.emit(0.05, True)
        global_data.emgr.receive_award_succ_event_from_lottery.emit(*self.turntable_ret)
        global_data.emgr.on_lottery_ended_event.emit()
        global_data.emgr.player_money_info_update_event.emit()
        if self.need_show_got and self.get_nd_got_func:
            for index in self.target_delight_item_index_list:
                nd = self.turntable_item_node_list[index]
                nd_got = self.get_nd_got_func(nd, index)
                nd_got and nd_got.setVisible(True)
                if self.need_anim_skip_got_item and self.turntable_item_anim_sequence_length > 1:
                    self.turntable_item_anim_sequence.remove(index)
                    self.turntable_item_anim_sequence_length -= 1

    def refresh_all_show_got_node(self):
        if self.need_show_got and self.refresh_nd_got_func:
            for index, (item_id, item_count) in enumerate(self.turntable_item_list):
                self.refresh_nd_got_func(self.turntable_item_node_list[index], item_id, item_count)

    def _delight_single_turntable_item(self):
        if self.panel and self.panel.isValid():
            cur_index = self.turntable_item_anim_sequence[self.cur_delight_item_index]
            cur_item = self.turntable_item_node_list[cur_index]
            pass_anim_duration = 0
            for anim_name in self.item_anim_name_map[ITEM_PASS_STATE]:
                pass_anim_duration = max(pass_anim_duration, cur_item.GetAnimationMaxRunTime(anim_name))

            if pass_anim_duration < self.delight_interval:
                scale = pass_anim_duration / self.delight_interval + 0.05 if 1 else 1.0
                cur_item_id = self.turntable_item_list[cur_index][0]
                self._play_item_anim(cur_item, ITEM_PASS_STATE, cur_item_id, scale=scale)
                global_data.sound_mgr.play_ui_sound('lottery_rolling')
                if self.target_delight_item_index_list:
                    if cur_index == self.target_delight_item_index_list[0] and (not self.need_anim_skip_got_item and self.target_delighted_time >= self.max_delighted_time or self.delight_interval >= self.max_single_interval - self.delta_delight_interval):
                        action_list = list()
                        sound_name = self.turntable_item_chosen_sound_name_list[cur_index]
                        action_list.append(cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound(sound_name)))
                        action_list.extend(self._get_play_item_action_list(cur_item, ITEM_CHOSEN_STATE, cur_item_id, need_action_wait=True, advance_time=0.1))
                        action_list.extend(self._get_play_item_action_list(cur_item, ITEM_LOOP_STATE, cur_item_id))
                        action_list.append(cc.DelayTime.create(0.4))
                        action_list.append(cc.CallFunc.create(self.show_lottery_result))
                        cur_item.runAction(cc.Sequence.create(action_list))
                        return
                    self.target_delighted_time += 1
                self.delight_interval += self.delta_delight_interval
                if self.delight_interval >= self.med_single_interval:
                    self.delta_delight_interval = self.final_delta_delight_interval
                if self.delight_interval > self.max_single_interval + self.delta_delight_interval:
                    self.delight_interval = self.max_single_interval + self.delta_delight_interval
            self.cur_delight_item_index = (self.cur_delight_item_index + 1) % self.turntable_item_anim_sequence_length
            self.delight_anim_timer = global_data.game_mgr.register_logic_timer(self._delight_single_turntable_item, interval=self.delight_interval, times=1, mode=CLOCK)

    def _delight_continual_turntable_item(self):
        if self.panel and self.panel.isValid():
            cur_index = self.cur_delight_item_index
            next_index = (cur_index + 1) % self.turntable_item_count
            cur_item = self.turntable_item_node_list[cur_index]
            cur_item_id = self.turntable_item_list[cur_index][0]
            self._play_item_anim(cur_item, ITEM_PASS_STATE, cur_item_id)
            cor_index = (next_index + self.turntable_item_count / 2) % self.turntable_item_count
            cor_item = self.turntable_item_node_list[cor_index]
            self._play_item_anim(cor_item, ITEM_PASS_STATE, cur_item_id)
            global_data.sound_mgr.play_ui_sound('lottery_rolling')
            self.cur_delight_item_index = next_index
            self.delight_anim_timer = global_data.game_mgr.register_logic_timer(self._delight_continual_turntable_item, interval=self.continual_interval, times=1, mode=CLOCK)

    def _check_need_skip_turntable_anim(self, force_skip_turntable_anim=False):
        if force_skip_turntable_anim:
            return True
        if self.need_skip_anim:
            return True
        if self.need_show_got and self.need_anim_skip_got_item and self.turntable_item_anim_sequence_length <= 1:
            return True
        return False

    def play_turntable_animation(self, lottery_count, force_skip_anim=False):
        self._reset_turntable_items()
        continual_do_not_skip = self.is_continual_do_not_skip()
        if self._check_need_skip_turntable_anim(force_skip_turntable_anim=force_skip_anim) and not continual_do_not_skip:
            return
        self.cur_draw_lottery_count = lottery_count
        self.cur_delight_item_index = 0
        self.turntable_ret = ()
        self._release_delight_anim_timer()
        self._release_choose_anim_timer()
        if lottery_count == SINGLE_LOTTERY_COUNT:
            self.target_delighted_time = 0
            self.delight_interval = self.min_single_interval
            self._delight_single_turntable_item()
        else:
            self.delight_interval = self.continual_interval
            self._delight_continual_turntable_item()

    def _check_is_playing_chosen_or_loop_anim(self, nd_item):
        item_chosen_anim = self.item_anim_name_map[ITEM_CHOSEN_STATE]
        for anim_name in item_chosen_anim:
            if nd_item.IsPlayingAnimation(anim_name):
                return True

        item_loop_anim = self.item_anim_name_map.get(ITEM_LOOP_STATE, [])
        for anim_name in item_loop_anim:
            if nd_item.IsPlayingAnimation(anim_name):
                return True

        return False

    def _play_continual_choose_animation(self):
        self._release_choose_anim_timer()
        self.choose_item_index = 0

        def play_choose_anim():
            turntable_index = self.target_delight_item_index_list[self.choose_item_index]
            cur_item = self.turntable_item_node_list[turntable_index]
            if not cur_item.pnl_repeat.isVisible():
                cur_item.pnl_repeat.setVisible(True)
                cur_item.lab_repeat_num.SetString('x1')
            else:
                old_count = int(cur_item.lab_repeat_num.GetString()[1:])
                cur_item.lab_repeat_num.SetString('x{}'.format(old_count + 1))
            action_list = list()
            sound_name = self.turntable_item_chosen_sound_name_list[turntable_index]
            action_list.append(cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound(sound_name)))
            cur_item_id = self.turntable_item_list[turntable_index][0]
            action_list.extend(self._get_play_item_action_list(cur_item, ITEM_CHOSEN_STATE, cur_item_id, need_action_wait=True, advance_time=0.1))
            action_list.extend(self._get_play_item_action_list(cur_item, ITEM_LOOP_STATE, cur_item_id))
            cur_item.runAction(cc.Sequence.create(action_list))
            self.choose_item_index += 1
            if self.choose_item_index == self.target_delight_item_count:
                self._release_delight_anim_timer()
                self.choose_anim_timer = global_data.game_mgr.register_logic_timer(self.show_lottery_result, interval=1.0, times=1, mode=CLOCK)
                return RELEASE

        self.choose_anim_timer = global_data.game_mgr.register_logic_timer(play_choose_anim, interval=1.0, times=-1, mode=CLOCK)

    def set_turntable_items_got(self, item_list, origin_list, force_play_chosen_anim_when_skip=False, force_skip_turntable_anim=False):
        self.turntable_ret = (item_list, origin_list)
        for i, item_info in enumerate(item_list):
            turntable_item_key = tuple(origin_list[i]) if origin_list[i] else tuple(item_info)
            if turntable_item_key in self.turntable_item_map:
                self.target_delight_item_index_list.append(self.turntable_item_map[turntable_item_key])

        self.target_delight_item_count = len(self.target_delight_item_index_list)
        continual_do_not_skip = self.is_continual_do_not_skip()
        if self._check_need_skip_turntable_anim(force_skip_turntable_anim=force_skip_turntable_anim) and not continual_do_not_skip:
            if force_play_chosen_anim_when_skip:
                cur_item_index = self.target_delight_item_index_list[0]
                cur_item = self.turntable_item_node_list[cur_item_index]
                cur_item_id = self.turntable_item_list[cur_item_index][0]
                action_list = list()
                action_list.append(cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound('lottery_spluse')))
                action_list.extend(self._get_play_item_action_list(cur_item, ITEM_CHOSEN_STATE, cur_item_id, need_action_wait=True))
                action_list.extend(self._get_play_item_action_list(cur_item, ITEM_LOOP_STATE, cur_item_id))
                action_list.append(cc.CallFunc.create(self.show_lottery_result))
                cur_item.runAction(cc.Sequence.create(action_list))
            else:
                self.show_lottery_result()
        elif self.cur_draw_lottery_count == SINGLE_LOTTERY_COUNT:
            target_item_index = self.target_delight_item_index_list[0]
            if target_item_index == self.cur_delight_item_index:
                left_delight_count = self.max_delighted_time * self.turntable_item_count
            else:
                left_delight_count = self.max_delighted_time * self.turntable_item_count + (target_item_index + self.turntable_item_count - self.cur_delight_item_index) % self.turntable_item_count
            med_left_delight_count = int(left_delight_count * self.high_speed_count_percent)
            self.final_delta_delight_interval = (self.max_single_interval - self.med_single_interval) / (left_delight_count - med_left_delight_count)
            self.delta_delight_interval = (self.med_single_interval - self.min_single_interval) / med_left_delight_count
        else:
            self._play_continual_choose_animation()

    def lottery_failed(self):
        self._release_delight_anim_timer()

    def enable_show_lottery_result(self, flag):
        self.show_lottery_result_enabled = flag

    def play_turntable_item_special_animation(self, anim_name):
        for item_node in self.turntable_item_node_list:
            item_node.PlayAnimation(anim_name)

    def play_turntable_item_state_anim(self, state):
        if state not in self.item_anim_name_map:
            return
        for index, item_node in enumerate(self.turntable_item_node_list):
            self._play_item_anim(item_node, state, self.turntable_item_list[index][0])

    def stop_turntable_item_state_anim(self, state):
        if state not in self.item_anim_name_map:
            return
        anim_name = self.item_anim_name_map[state]
        for item_node in self.turntable_item_node_list:
            if type(anim_name) == str:
                item_node.StopAnimation(anim_name)
                item_node.RecoverAnimationNodeState(anim_name)
            else:
                for name in anim_name:
                    item_node.StopAnimation(name)
                    item_node.RecoverAnimationNodeState(name)

    def stop_all_turntable_item_state_anim(self):
        for state in six.iterkeys(self.item_anim_name_map):
            self.stop_turntable_item_state_anim(state)

    def is_continual_do_not_skip(self):
        if not self.get_last_clicked_lottery_count or not callable(self.get_last_clicked_lottery_count):
            return False
        if self.get_last_clicked_lottery_count() != CONTINUAL_LOTTERY_COUNT:
            return False
        if not self.continual_count_reserve_anim:
            return False
        return True