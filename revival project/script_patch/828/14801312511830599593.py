# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/BanPick/ModeBanPickUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import zip
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
import cc
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const.battle_const import BP_MODE_PLAY, BP_MODE_MAP
from common.cfg import confmgr
import time
STATE_SELECTING_NORMAL = 1
STATE_SELECTING_SELECTED = 3
STATE_SELECTING_UNUSABLE = 5
STATE_SELECTED_UNSELECTED = 2
STATE_SELECTED_SELECTED = 4
STATE_SELECTED_UNUSABLE = 6
STATE_SELECTED_TOP = 7
STATE_RESULT_UNSELECTED = 8
STATE_RESULT_SELECTED = 9

class FinishAniHelper(object):
    ACT_TAG = 20220606
    MAX_ANI_DELAY = 0.3
    MIN_ANI_DELAY = 0.1

    def __init__(self, start_data, end_data, anim_len, data_list, possible_list, ui_container):
        self.anim_len = anim_len
        self.start_data = start_data
        self.end_data = end_data
        self.data_list = data_list
        self.possible_list = possible_list
        self.ui_container = ui_container
        self.ani_cb = None
        self.finish_cb = None
        self.total_ani_count = -1
        self.cur_ani_idx = -1
        self.start_ani_time = -1
        self.cur_data = -1
        return

    def set_callback(self, ani_cb, finish_cb):
        self.ani_cb = ani_cb
        self.finish_cb = finish_cb

    def destroy(self):
        self.anim_len = 3.0
        self.start_data = -1
        self.final_bp_ret = (-1, -1)
        self.data_list = []
        self.ui_container = None
        self.ani_cb = None
        self.finish_cb = None
        return

    def setup_finish_ani(self):
        idx = self.data_list.index(self.start_data)
        first_round = len(self.possible_list) - 1 - idx + 1
        end_idx = self.data_list.index(self.end_data)
        end_round = end_idx + 1
        assume_ani_time = int(self.anim_len / ((self.MAX_ANI_DELAY + self.MIN_ANI_DELAY) / 2.0))
        remain_count = assume_ani_time - first_round - end_round
        round_num = remain_count / len(self.possible_list)
        self.cur_data = self.start_data
        self.total_ani_count = round_num * len(self.possible_list) + first_round + end_round
        self.cur_ani_idx = self.total_ani_count
        self.start_ani_time = tutil.get_server_time()
        self.play_an_finish_ani(is_init=True)

    def cal_delay_time(self):
        left_time = self.start_ani_time + self.anim_len - tutil.get_server_time() + 0.3
        diff = 0.19999999999999998 / self.total_ani_count * (self.total_ani_count - self.cur_ani_idx) + 0.1
        if self.cur_ani_idx > 0 and diff > 0.1:
            anim_need_left_time = (0.3 + diff) * self.cur_ani_idx / 2.0
            if left_time < anim_need_left_time:
                diff -= (anim_need_left_time - left_time) / self.cur_ani_idx
        return max(min(left_time, diff), 0.03)

    def play_an_finish_ani(self, is_init=False):
        if self.ani_cb:
            if is_init:
                self.ani_cb(-1, self.cur_data)
            else:
                old_idx = (self.possible_list.index(self.cur_data) - 1) % len(self.possible_list)
                last_data = self.possible_list[old_idx]
                self.ani_cb(last_data, self.cur_data)
        new_idx = (self.possible_list.index(self.cur_data) + 1) % len(self.possible_list)
        self.cur_data = self.possible_list[new_idx]
        delay_time = self.cal_delay_time()
        self.finish_anim_time = self.start_ani_time + 3 - tutil.get_server_time()
        self.cur_ani_idx -= 1
        if self.cur_ani_idx > 0 and delay_time > -0.5:
            self.ui_container.DelayCallWithTag(delay_time, self.play_an_finish_ani, self.ACT_TAG)
        else:
            self.ui_container.stopActionByTag(self.ACT_TAG)
            if self.cur_data >= 0:
                old_idx = (self.possible_list.index(self.cur_data) - 1) % len(self.possible_list)
                last_data = self.possible_list[old_idx]
                self.ani_cb(last_data, -1)
            if self.finish_cb:
                self.finish_cb()

    def play_ani(self, old_idx, cur_idx):
        ui_item = self.ui_container.GetItem(old_idx)
        if ui_item:
            ui_item.vx_choose_top.setVisible(False)
        ui_item = self.ui_container.GetItem(cur_idx)
        if ui_item:
            ui_item.PlayAnimation('pass')


class ModeBanPickUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/bp_choose'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_btn.btn_common_big.OnClick': 'on_click_btn_temp'
       }
    GLOBAL_EVENT = {'battle_match_status_event': 'update_match_status',
       'update_allow_match_ts': 'update_match_status'
       }
    TIMER_TAG = 20220325

    def on_init_panel(self, *args, **kargs):
        self._battle_type = None
        self._player_choose_play_type = None
        self._player_choose_map = None
        self._avatar_comfirmed_chose = (None, None)
        self._pre_choose_area_uid = None
        battle_bp_map_config = confmgr.get('battle_bp_map_config', default={})
        self._all_areas = sorted(six_ex.keys(battle_bp_map_config), key=lambda x: battle_bp_map_config[x]['sort_id'])
        self._available_area_list = []
        self._available_play_type_list = []
        self._ui_item_states = {}
        self._bp_chose_ret = {}
        self._lock_change_state = False
        self._need_show_top = False
        self._on_result_show = False
        self._all_poll_people_num = 10
        self._polled_people_num = 0
        self._poll_end_time = 0
        self._is_support_empty_select = True
        self._is_support_empty_comfirm = False
        self._is_support_empty_mode = False
        self._is_support_empty_map = True
        self._bp_target = BP_MODE_PLAY
        self.finish_ani_helper = None
        self.final_bp_ret = (-1, -1)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(19992), get_text_by_id(19878))

        self.register_timer()
        global_data.ui_mgr.close_ui('BattleMatchUI')
        self.hide_main_ui()
        self.panel.PlayAnimation('show')
        global_data.game_mgr.show_tip(get_text_by_id(19978))
        self.panel.temp_btn.btn_common_big.EnableCustomState(True)
        global_data.ui_mgr.add_ui_show_whitelist([self.__class__.__name__, 'QuickChatEmote', 'GVGReadyUI', 'GVGChooseMecha', 'NormalConfirmUI2', 'GameRuleDescUI', 'NoticeUI'], self.__class__.__name__)
        global_data.sound_mgr.play_music('Deathmatch_bp_select')
        self._bp_chat = None
        return

    def on_finalize_panel(self):
        if self._bp_chat:
            self._bp_chat.destroy()
            self._bp_chat = None
        self.show_main_ui()
        global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
        if self.finish_ani_helper:
            self.finish_ani_helper.destroy()
            self.finish_ani_helper = None
        global_data.sound_mgr.stop_music()
        return

    def update_show_according_to_state(self, ui_item, from_state, to_state):
        if not ui_item:
            return

        def state_selecting_normal_func(ui_item, is_choose):
            pass

        def state_selecting_selected_func(ui_item, is_choose):
            if is_choose:
                ui_item.PlayAnimation('choose')
            else:
                ui_item.StopAnimation('choose')
                ui_item.RecoverAnimationNodeState('choose')

        def state_selecting_unusable_func(ui_item, is_choose):
            ui_item.img_mask_lock.setVisible(is_choose)

        def state_selected_unselected_func(ui_item, is_choose):
            ui_item.img_mask.setVisible(is_choose)

        def state_selected_unusable_func(ui_item, is_choose):
            ui_item.img_mask_lock.setVisible(is_choose)
            ui_item.img_mask.setVisible(is_choose)

        def state_selected_selected_func(ui_item, is_choose):
            if is_choose:
                ui_item.PlayAnimation('chooing')
            else:
                ui_item.StopAnimation('chooing')
                ui_item.RecoverAnimationNodeState('chooing')

        def state_result_unselected(ui_item, is_choose):
            if is_choose:
                ui_item.tag_top.setVisible(False)
                p = ui_item.img_pic.GetDisplayFramePath()
                if p:
                    p = p.replace('.png', '_lock.png')
                    ui_item.img_pic.SetDisplayFrameByPath('', p)
                old_string = ui_item.lab_num.GetString()
                if old_string:
                    new_str = old_string.replace('0XFFE954FF', '0XFFFFFFFF')
                    ui_item.lab_num.SetString(new_str)
                    ui_item.vx_lab_num.SetString(new_str)
                else:
                    ui_item.lab_num.SetString('<color=0XFFFFFFFF>%s</color>/%s' % (0, self._all_poll_people_num))
                    ui_item.vx_lab_num.SetString('<color=0XFFFFFFFF>%s</color>/%s' % (0, self._all_poll_people_num))
                ui_item.lab_name.SetColor(5855591)

        def state_result_selected_func(ui_item, is_choose):
            old_string = ui_item.lab_num.GetString()
            count = 0
            if not old_string:
                ui_item.lab_num.SetString('<size=40><color=0XFFE954FF>%s</color></size>/%s' % (count, self._all_poll_people_num))
                ui_item.vx_lab_num.SetString('<size=40><color=0XFFE954FF>%s</color></size>/%s' % (count, self._all_poll_people_num))

        into_dict = {STATE_SELECTING_NORMAL: state_selecting_normal_func,
           STATE_SELECTING_SELECTED: state_selecting_selected_func,
           STATE_SELECTING_UNUSABLE: state_selecting_unusable_func,
           STATE_SELECTED_UNSELECTED: state_selected_unselected_func,
           STATE_SELECTED_SELECTED: state_selected_selected_func,
           STATE_SELECTED_UNUSABLE: state_selected_unusable_func,
           STATE_RESULT_UNSELECTED: state_result_unselected,
           STATE_RESULT_SELECTED: state_result_selected_func
           }
        state_from_func = into_dict.get(from_state)
        if state_from_func:
            state_from_func(ui_item, False)
        state_to_func = into_dict.get(to_state)
        if state_to_func:
            state_to_func(ui_item, True)

    def init_list_map(self):
        if self._bp_target == BP_MODE_PLAY:
            return
        battle_bp_map_config = confmgr.get('battle_bp_map_config', default={})
        all_areas = self._all_areas
        self.panel.list_item_map.SetInitCount(len(all_areas))
        for idx, area_uid in enumerate(all_areas):
            mode_item = self.panel.list_item_map.GetItem(idx)
            mode_item.tag_top.setVisible(False)
            mode_item.tag_choose.setVisible(False)
            mode_item.lab_num.setString('')
            area_conf = battle_bp_map_config.get(str(area_uid), {})
            img_path = area_conf.get('img_path', 0)
            name_tid = area_conf.get('name_tid', '')
            mode_item.lab_name.SetString(name_tid)
            mode_item.img_pic.SetDisplayFrameByPath('', img_path)
            mode_item.RecordAnimationNodeState('choose')
            mode_item.RecordAnimationNodeState('top')
            mode_item.RecordAnimationNodeState('chooing')

            @mode_item.btn.callback()
            def OnClick(btn, touch, choose=area_uid):
                if self._lock_change_state:
                    global_data.game_mgr.show_tip(get_text_by_id(19953))
                    return
                else:
                    if self._player_choose_play_type is None:
                        log_error('_player_choose_play_type should not be empty!', self._player_choose_play_type, self._player_choose_map)
                        self._set_choose_ui_item_tag(BP_MODE_MAP, False)
                        if self._pre_choose_area_uid != choose:
                            self._pre_choose_area_uid = choose
                        self._player_choose_map = choose
                        self._set_choose_ui_item_tag(BP_MODE_MAP, True)
                        self.update_available_play_type_show()
                    elif not self.check_is_valid_play_type_and_area(self._player_choose_play_type, choose):
                        global_data.game_mgr.show_tip(get_text_by_id(19217))
                        return
                    if choose == self._player_choose_map:
                        global_data.game_mgr.show_tip(get_text_by_id(19216))
                    self._pre_choose_area_uid = None
                    old_choose = self._player_choose_map
                    self._set_choose_ui_item_tag(BP_MODE_MAP, False)
                    self._player_choose_map = choose
                    self._set_choose_ui_item_tag(BP_MODE_MAP, True)
                    if old_choose != self._player_choose_map:
                        self.on_choose_area()
                        self.update_available_play_type_show()
                    return

    def start_show_bp_mode(self, battle_type, candidates, end_ts):
        self._battle_type = battle_type
        self._poll_end_time = end_ts
        self._candidates = candidates
        self._play_type_list = sorted(six_ex.keys(self._candidates))
        self.refresh_time()
        self.update_battle_type_list_show()
        self._ui_item_states.update(list(zip(self._play_type_list, [STATE_SELECTING_NORMAL] * len(self._play_type_list))))
        self._ui_item_states.update(list(zip(self._all_areas, [STATE_SELECTING_NORMAL] * len(self._all_areas))))
        global_data.ui_mgr.close_ui('BattleMatchUI')
        self.init_chat_panel(battle_type)

    def update_bp_record(self, bp_record):
        self._bp_chose_ret = dict(bp_record)
        self._ui_item_states.update(list(zip(self._play_type_list, [STATE_SELECTING_NORMAL] * len(self._play_type_list))))
        self._ui_item_states.update(list(zip(self._all_areas, [STATE_SELECTING_NORMAL] * len(self._all_areas))))
        self.update_choose_show()
        self._avatar_comfirmed_chose = self._bp_chose_ret.get(global_data.player.id, (None,
                                                                                      None))
        self._player_choose_play_type = self._avatar_comfirmed_chose[0]
        self.on_choose_play_type()
        self._player_choose_map = self.get_area_uid_by_play_type_and_area_idx(*self._avatar_comfirmed_chose)
        self.on_choose_area()
        if self._player_choose_play_type is not None:
            self._set_choose_ui_item_tag(BP_MODE_PLAY, True)
        if self._player_choose_map is not None and self._player_choose_map != -1:
            self._set_choose_ui_item_tag(BP_MODE_MAP, True)
        return

    def update_avatar_chose(self):
        old_avatar_choose = self._avatar_comfirmed_chose
        new_avatar_choose = self._bp_chose_ret.get(global_data.player.id, (None, None))
        if old_avatar_choose != new_avatar_choose:
            if any(old_avatar_choose):
                self.set_choose_ui_item_comfirmed(BP_MODE_PLAY, old_avatar_choose[0], False)
                area_uid = self.get_area_uid_by_play_type_and_area_idx(*old_avatar_choose)
                self.set_choose_ui_item_comfirmed(BP_MODE_MAP, area_uid, False)
            if any(new_avatar_choose):
                self.set_choose_ui_item_comfirmed(BP_MODE_PLAY, new_avatar_choose[0], True)
                area_uid = self.get_area_uid_by_play_type_and_area_idx(*new_avatar_choose)
                self.set_choose_ui_item_comfirmed(BP_MODE_MAP, area_uid, True)
        return None

    def on_other_map_bp(self, choose_info):
        avt_id, map_id, area_id = choose_info
        self._bp_chose_ret[avt_id] = (map_id, area_id)
        self._avatar_comfirmed_chose = self._bp_chose_ret.get(global_data.player.id, (None,
                                                                                      None))
        if global_data.player.id == avt_id:
            self.change_lock_state(True)
        self.update_avatar_chose()
        self.update_choose_show()
        return None

    def update_choose_show(self):
        cur_bp_choose_map = self._bp_chose_ret
        self._polled_people_num = len(cur_bp_choose_map)
        max_play_type_count_dict = {}
        max_map_count_dict = {}
        for avt_id, choose in six.iteritems(cur_bp_choose_map):
            play_type, area_idx = choose
            area_uid = self.get_area_uid_by_play_type_and_area_idx(play_type, area_idx)
            max_play_type_count_dict.setdefault(play_type, 0)
            max_play_type_count_dict[play_type] += 1
            max_map_count_dict.setdefault(area_uid, 0)
            max_map_count_dict[area_uid] += 1

        self.update_choose_ret_show(max_play_type_count_dict, max_map_count_dict)

    def on_map_bp_ret(self, play_type_ret, area_ret):
        self.final_bp_ret = (
         play_type_ret, area_ret)
        self.panel.lab_countdown.setVisible(False)
        self.panel.PlayAnimation('result')
        self.show_final_bp_ret_ani(self.show_result)

    def test_map_bp(self):
        self._bp_chose_ret = {}
        self.on_map_bp_ret(11, 0)

    def show_result(self):
        play_type_ret, area_ret = self.final_bp_ret
        self.update_bp_result_show(play_type_ret, area_ret)

    def play_finish_one_ani(self, old_data, new_data):
        if old_data in self._play_type_list:
            idx = self._play_type_list.index(old_data)
            ui_item = self.panel.list_item_mode.GetItem(idx)
            if ui_item:
                ui_item.StopAnimation('pass')
                ui_item.vx_choose_top.setVisible(False)
        if new_data in self._play_type_list:
            idx = self._play_type_list.index(new_data)
            ui_item = self.panel.list_item_mode.GetItem(idx)
            if ui_item:
                ui_item.PlayAnimation('pass')

    def show_final_bp_ret_ani(self, callback):
        play_type_count_dict = {}
        for avt_id, choose in six.iteritems(self._bp_chose_ret):
            play_type, area_idx = choose
            play_type_count_dict.setdefault(play_type, 0)
            play_type_count_dict[play_type] += 1

        if len(play_type_count_dict) == 1:
            callback()
            return
        else:
            if not self.finish_ani_helper:
                anim_len = 3
                if play_type_count_dict:
                    possible_list = sorted(six_ex.keys(play_type_count_dict), key=lambda x: self._play_type_list.index(x))
                    start_data = six_ex.keys(play_type_count_dict)[0]
                else:
                    possible_list = self._play_type_list
                    start_data = self._play_type_list[0]
                end_data, _ = self.final_bp_ret
                if self._player_choose_play_type is not None:
                    ui_item = self.get_play_type_ui_item(self._player_choose_play_type)
                    if ui_item:
                        ui_item.vx_choose_normal.setVisible(False)
                        ui_item.vx_choose_chooing.setVisible(False)
                self.finish_ani_helper = FinishAniHelper(start_data, end_data, anim_len, self._play_type_list, possible_list, self.panel.list_item_mode)
                self.finish_ani_helper.set_callback(self.play_finish_one_ani, self.show_result)
                self.finish_ani_helper.setup_finish_ani()
            return

    def get_play_type_ui_item(self, play_type):
        if play_type in self._play_type_list:
            idx = self._play_type_list.index(play_type)
            ui_item = self.panel.list_item_mode.GetItem(idx)
            if ui_item:
                return ui_item
        return None

    def update_choose_ret_show(self, max_play_type_count_dict, max_map_count_dict):
        if max_map_count_dict and max_play_type_count_dict:

            def set_func(ui_list, data_list, count_dict, available_list=None):
                for idx, key in enumerate(data_list):
                    count = count_dict.get(key, 0)
                    ui_item = ui_list.GetItem(idx)
                    if not ui_item:
                        continue
                    if available_list is None:
                        max_count = max(six_ex.values(count_dict))
                    elif not available_list:
                        max_count = -1
                    else:
                        max_count = max([ count_dict.get(p, 0) for p in available_list ])
                    is_unava = available_list is not None and key not in available_list
                    if count == max_count and not is_unava:
                        if self._need_show_top:
                            ui_item.tag_top.setVisible(True)
                        ui_item.lab_num.SetString('<size=40><color=0XFFE954FF>%s</color></size>/%s' % (count, self._all_poll_people_num))
                        ui_item.vx_lab_num.SetString('<size=40><color=0XFFE954FF>%s</color></size>/%s' % (count, self._all_poll_people_num))
                    else:
                        if self._need_show_top:
                            ui_item.tag_top.setVisible(False)
                        ui_item.lab_num.SetString('<color=0XFFFFFFFF>%s</color>/%s' % (count, self._all_poll_people_num))
                        ui_item.vx_lab_num.SetString('<color=0XFFFFFFFF>%s</color>/%s' % (count, self._all_poll_people_num))

                return

            set_func(self.panel.list_item_mode, self._play_type_list, max_play_type_count_dict)
            max_play_type_count = max(six_ex.values(max_play_type_count_dict))
            max_play_types = [ p for p, c in six.iteritems(max_play_type_count_dict) if c == max_play_type_count ]
            available_maps = []
            if len(max_play_types) == 1:
                available_maps = self.generate_available_list_by_mode(max_play_types[0])
            set_func(self.panel.list_item_map, self._all_areas, max_map_count_dict, available_list=available_maps)
        return

    def update_bp_result_show(self, play_type_ret, area_ret):

        def set_on_comfirm_lock(bp_mode, idx, value, ui_item, is_choose):
            if not is_choose:
                ui_item.StopAnimation('top')
                ui_item.RecoverAnimationNodeState('top')
            else:
                ui_item.setLocalZOrder(2)
                ui_item.lab_new.SetString('FINAL')
                ui_item.PlayAnimation('pass')
                ui_item.PlayAnimation('top')

        self._lock_change_state = True
        self.panel.temp_btn.setVisible(False)
        self.set_gray_to_others(True, (play_type_ret, area_ret), apply_to_target=True, state_sel=STATE_RESULT_SELECTED, state_unsel=STATE_RESULT_UNSELECTED, state_unusable=STATE_RESULT_UNSELECTED)
        self._inner_set_choose_ui_item_tag(BP_MODE_PLAY, play_type_ret, True, set_on_comfirm_lock)
        area_uid = self.get_area_uid_by_play_type_and_area_idx(play_type_ret, area_ret)
        self._inner_set_choose_ui_item_tag(BP_MODE_MAP, area_uid, True, set_on_comfirm_lock)
        self._on_result_show = True
        self.panel.DelayCall(6.0, lambda : self.close())

    def _set_choose_ui_item_tag(self, bp_mode, vis):
        if self._bp_target != bp_mode:
            return
        else:
            self._inner_set_choose_ui_item_tag(bp_mode, None, vis, self.set_on_uncomfirm_choose)
            return

    def set_choose_ui_item_comfirmed(self, bp_mode, value, vis):
        if self._bp_target != bp_mode:
            return
        self._inner_set_choose_ui_item_tag(bp_mode, value, vis, self.set_on_comfirm_choose)

    def _inner_set_choose_ui_item_tag(self, bp_mode, value, vis, callback):
        idx = -1
        if bp_mode == BP_MODE_PLAY:
            play_type = value if value is not None else self._player_choose_play_type
            if play_type in self._play_type_list:
                idx = self._play_type_list.index(play_type)
                ui_item = self.panel.list_item_mode.GetItem(idx)
                if idx >= 0:
                    if ui_item:
                        callback(bp_mode, idx, play_type, ui_item, vis)
        elif bp_mode == BP_MODE_MAP:
            area = value if value is not None else self._player_choose_map
            if area in self._all_areas:
                idx = self._all_areas.index(area)
                ui_item = self.panel.list_item_map.GetItem(idx)
                if idx >= 0:
                    if ui_item:
                        callback(bp_mode, idx, area, ui_item, vis)
        return

    def update_battle_type_list_show(self):
        play_type_list = self._play_type_list
        self.panel.list_item_mode.SetInitCount(len(play_type_list))
        for idx, play_type in enumerate(play_type_list):
            mode_item = self.panel.list_item_mode.GetItem(idx)
            mode_item.tag_top.setVisible(False)
            mode_item.tag_choose.setVisible(False)
            mode_item.lab_num.setString('')
            play_type_conf = confmgr.get('battle_bp_config', str(self._battle_type), str(play_type), default={})
            img_path = play_type_conf.get('img_path', '')
            desc_tid = play_type_conf.get('desc_tid', '')
            name_tid = play_type_conf.get('name_tid', '')
            mode_item.lab_name.SetString(name_tid)
            mode_item.lab_num.SetString('')
            mode_item.vx_lab_num.SetString('')
            mode_item.img_pic.SetDisplayFrameByPath('', img_path)
            mode_item.RecordAnimationNodeState('choose')
            mode_item.RecordAnimationNodeState('top')
            mode_item.RecordAnimationNodeState('chooing')

            @mode_item.btn.callback()
            def OnClick(btn, touch, choose=play_type):
                if self._lock_change_state:
                    if not self._on_result_show:
                        global_data.game_mgr.show_tip(get_text_by_id(19953))
                    return
                if self._pre_choose_area_uid:
                    log_error('_pre_choose_area_uid is deprecated')
                    if self.check_is_valid_play_type_and_area(choose, self._pre_choose_area_uid):
                        self._set_choose_ui_item_tag(BP_MODE_PLAY, False)
                        self._player_choose_play_type = choose
                        self._set_choose_ui_item_tag(BP_MODE_PLAY, True)
                        self.on_choose_play_type()
                        self.update_available_area_show()
                        self._player_choose_map = self._pre_choose_area_uid
                        return
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(19217))
                        return

                if not self._is_support_empty_select:
                    if self._player_choose_map and not self.check_is_valid_play_type_and_area(choose, self._player_choose_map):
                        global_data.game_mgr.show_tip(get_text_by_id(19217))
                        return
                if choose == self._player_choose_play_type:
                    global_data.game_mgr.show_tip(get_text_by_id(19216))
                self._set_choose_ui_item_tag(BP_MODE_PLAY, False)
                self._player_choose_play_type = choose
                self._set_choose_ui_item_tag(BP_MODE_PLAY, True)
                self.on_choose_play_type()
                self.update_available_area_show()

    def update_to_state(self, ui_item, value, new_state):
        current_state = self._ui_item_states.get(value, STATE_SELECTING_NORMAL)
        if current_state == new_state:
            return
        self.update_show_according_to_state(ui_item, current_state, new_state)
        self._ui_item_states[value] = new_state

    def set_on_uncomfirm_choose(self, bp_mode, idx, value, ui_item, is_choose):
        new_state = STATE_SELECTING_SELECTED if is_choose else STATE_SELECTING_NORMAL
        self.update_to_state(ui_item, value, new_state)

    def set_on_comfirm_choose(self, bp_mode, idx, value, ui_item, is_choose):
        new_state = STATE_SELECTED_SELECTED if is_choose else STATE_SELECTED_UNSELECTED
        self.update_to_state(ui_item, value, new_state)

    def on_choose_play_type(self):
        if self._player_choose_play_type is None:
            self._available_area_list = None
            return
        else:
            server_idx_list = self._candidates.get(self._player_choose_play_type, [])
            area_conf_list = confmgr.get('battle_bp_config', str(self._battle_type), str(self._player_choose_play_type), 'area_conf', default=[])
            self._available_area_list = [ area_conf_list[idx].get('area_uid', None) for idx in server_idx_list if idx < len(area_conf_list) ]
            return

    def on_choose_area(self):
        if self._player_choose_map is None or self._player_choose_map == -1:
            self._available_play_type_list = None
            return
        else:
            self._available_play_type_list = [ p for p in self._play_type_list if self.check_is_valid_play_type_and_area(p, self._player_choose_map) ]
            return

    def get_area_uid_by_play_type_and_area_idx(self, play_type, area_idx):
        if self._is_support_empty_select:
            if area_idx is None or area_idx == -1 or play_type is None:
                return
        play_type_dict_conf = confmgr.get('battle_bp_config', str(self._battle_type), default={})
        area_conf_list = play_type_dict_conf.get(str(play_type), {}).get('area_conf', [])
        area_uid = area_conf_list[area_idx].get('area_uid')
        return area_uid

    def update_available_area_show(self):
        for idx, area_uid in enumerate(self._all_areas):
            ui_item = self.panel.list_item_map.GetItem(idx)
            if self._available_area_list is not None:
                if self._available_area_list:
                    available = area_uid in self._available_area_list if 1 else True
                else:
                    available = True
                available or self.update_to_state(ui_item, area_uid, STATE_SELECTING_UNUSABLE)
            elif self._player_choose_map == area_uid:
                new_state = STATE_SELECTING_SELECTED if 1 else STATE_SELECTING_NORMAL
                self.update_to_state(ui_item, area_uid, new_state)

        return

    def update_available_play_type_show(self):
        play_type_list = self._play_type_list
        if self._pre_choose_area_uid is not None:
            available_play_type_list = [ p for p in play_type_list if self.check_is_valid_play_type_and_area(p, self._pre_choose_area_uid) ]
        else:
            available_play_type_list = self._available_play_type_list
        self.panel.list_item_mode.SetInitCount(len(play_type_list))
        for idx, play_type in enumerate(play_type_list):
            ui_item = self.panel.list_item_mode.GetItem(idx)
            if available_play_type_list is not None:
                if available_play_type_list:
                    available = play_type in available_play_type_list if 1 else True
                else:
                    available = True
                available or self.update_to_state(ui_item, play_type, STATE_SELECTING_UNUSABLE)
            elif self._player_choose_play_type == play_type:
                new_state = STATE_SELECTING_SELECTED if 1 else STATE_SELECTING_NORMAL
                self.update_to_state(ui_item, play_type, new_state)

        return

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(1.0),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act.setTag(self.TIMER_TAG)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)

    def get_end_time(self):
        if self._poll_end_time:
            return self._poll_end_time
        return tutil.get_server_time() + 100

    def refresh_time(self):
        end_time = self.get_end_time()
        if end_time:
            server_time = tutil.get_server_time()
            left_time = int(end_time - server_time)
            show_left_time = max(left_time, 0)
            if left_time > 0:
                self.panel.lab_rule.SetString(19877)
            else:
                self.panel.temp_btn.setVisible(False)
            if left_time >= 0:
                self.panel.PlayAnimation('count')
            if show_left_time >= 6:
                color = '#SW'
            elif show_left_time >= 4:
                color = '#SY'
            else:
                color = '#SR'
            self.panel.lab_countdown.SetColor(color)
            self.panel.vx_lab_time.SetColor(color)
            self.panel.lab_countdown.SetString(str(show_left_time))
            self.panel.vx_lab_time.SetString(str(show_left_time))
        else:
            self.panel.lab_rule.SetString(19877)

    def update_match_status(self, *args):
        if self._on_result_show:
            return
        is_matching = global_data.player.is_matching
        if is_matching:
            pass
        else:
            self.close()

    def check_is_valid_choose(self, play_type, index):
        return index in self._candidates.get(play_type, [])

    def check_is_valid_play_type_and_area(self, play_type, area_uid):
        if self._is_support_empty_select:
            return True
        else:
            server_idx_list = self._candidates.get(play_type, [])
            area_conf_list = confmgr.get('battle_bp_config', str(self._battle_type), str(play_type), 'area_conf', default=[])
            _available_area_list = [ area_conf_list[idx].get('area_uid', None) for idx in server_idx_list if idx < len(area_conf_list) ]
            return area_uid in _available_area_list

    def generate_available_list_by_mode(self, play_type):
        server_idx_list = self._candidates.get(play_type, [])
        area_conf_list = confmgr.get('battle_bp_config', str(self._battle_type), str(play_type), 'area_conf', default=[])
        _available_area_list = [ area_conf_list[idx].get('area_uid', None) for idx in server_idx_list if idx < len(area_conf_list) ]
        return _available_area_list

    def set_gray_to_others(self, gray, target_choose, apply_to_target=False, state_unsel=None, state_unusable=None, state_sel=None):
        play_type, area_idx = target_choose
        area_uid = self.get_area_uid_by_play_type_and_area_idx(*target_choose)
        for idx, _value in enumerate(self._play_type_list):
            ui_item = self.panel.list_item_mode.GetItem(idx)
            if not ui_item:
                continue
            if _value != play_type:
                if self._available_play_type_list is not None:
                    new_state = state_unusable if _value not in self._available_play_type_list else state_unsel
                else:
                    new_state = state_unsel
                self.update_to_state(ui_item, _value, new_state)
            elif apply_to_target:
                self.update_to_state(ui_item, _value, state_sel)

        for idx, _value in enumerate(self._all_areas):
            ui_item = self.panel.list_item_map.GetItem(idx)
            if not ui_item:
                continue
            if _value != area_uid:
                if self._available_area_list is not None:
                    new_state = state_unusable if _value not in self._available_area_list else state_unsel
                else:
                    new_state = state_unsel
                self.update_to_state(ui_item, _value, new_state)
            elif apply_to_target:
                self.update_to_state(ui_item, _value, state_sel)

        return

    def change_lock_state(self, to_value):

        def set_on_comfirm_lock(bp_mode, idx, value, ui_item, is_choose):
            if is_choose:
                self.update_to_state(ui_item, value, STATE_SELECTED_SELECTED)
            else:
                self.update_to_state(ui_item, value, STATE_SELECTING_SELECTED)

        if self._lock_change_state == to_value:
            return
        else:
            self._lock_change_state = to_value
            if not self._is_support_empty_select:
                if self._avatar_comfirmed_chose[0] is None or self._avatar_comfirmed_chose[1] is None:
                    return
            if self._lock_change_state:
                self.panel.temp_btn.btn_common_big.SetSelect(True)
                self.panel.temp_btn.btn_common_big.SetText(19215)
                self.set_gray_to_others(True, self._avatar_comfirmed_chose, state_sel=STATE_SELECTED_SELECTED, state_unusable=STATE_SELECTED_UNUSABLE, state_unsel=STATE_SELECTED_UNSELECTED)
                self._inner_set_choose_ui_item_tag(BP_MODE_PLAY, self._avatar_comfirmed_chose[0], True, set_on_comfirm_lock)
                area_uid = self.get_area_uid_by_play_type_and_area_idx(*self._avatar_comfirmed_chose)
                self._inner_set_choose_ui_item_tag(BP_MODE_MAP, area_uid, True, set_on_comfirm_lock)
            else:
                self.panel.temp_btn.btn_common_big.SetSelect(False)
                self.panel.temp_btn.btn_common_big.SetText(80305)
                self.set_gray_to_others(False, self._avatar_comfirmed_chose, state_sel=STATE_SELECTING_SELECTED, state_unusable=STATE_SELECTING_UNUSABLE, state_unsel=STATE_SELECTING_NORMAL)
                self._inner_set_choose_ui_item_tag(BP_MODE_PLAY, self._avatar_comfirmed_chose[0], False, set_on_comfirm_lock)
                area_uid = self.get_area_uid_by_play_type_and_area_idx(*self._avatar_comfirmed_chose)
                self._inner_set_choose_ui_item_tag(BP_MODE_MAP, area_uid, False, set_on_comfirm_lock)
            return

    def on_click_btn_temp(self, btn, touch):
        if self.panel.IsPlayingAnimation('show'):
            return
        else:
            if self._lock_change_state:
                self.change_lock_state(False)
                return
            if self._is_support_empty_select:
                if not self._is_support_empty_comfirm:
                    if self._player_choose_play_type is None and not self._is_support_empty_mode:
                        global_data.game_mgr.show_tip(get_text_by_id(83445))
                        return
                    if self._player_choose_map is None and not self._is_support_empty_map:
                        return
                record = self._bp_chose_ret.get(global_data.player.id, (None, None))
                if record[0] != self._player_choose_play_type:
                    if global_data.player:
                        global_data.player.battle_map_banpick(self._player_choose_play_type, -1)
                        if not self._need_show_top:
                            self._need_show_top = True
                else:
                    self.change_lock_state(True)
                    if not self._need_show_top:
                        self._need_show_top = True
                        self.update_choose_show()
                return
            if self._player_choose_play_type is None or self._player_choose_map is None:
                return
            if self.check_is_valid_play_type_and_area(self._player_choose_play_type, self._player_choose_map):
                if self._player_choose_map in self._available_area_list:
                    area_idx = self._available_area_list.index(self._player_choose_map)
                    record = self._bp_chose_ret.get(global_data.player.id, (None, None))
                    if record[0] != self._player_choose_play_type or record[1] != area_idx:
                        if global_data.player:
                            global_data.player.battle_map_banpick(self._player_choose_play_type, area_idx)
                            if not self._need_show_top:
                                self._need_show_top = True
                    else:
                        self.change_lock_state(True)
                        if not self._need_show_top:
                            self._need_show_top = True
                            self.update_choose_show()
                else:
                    log_error('Invalid chose area uid', self._player_choose_play_type, self._player_choose_map, self._available_area_list)
            return

    def init_chat_panel(self, battle_type):
        from logic.comsys.message.BPChat import BPChat
        self._bp_chat = BPChat(self.panel.nd_chat, self.panel.nd_chat, battle_type)