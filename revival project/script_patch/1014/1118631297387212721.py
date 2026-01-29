# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/reward/ReceiveRewardUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_VKB_CUSTOM
from logic.gutils.item_utils import get_item_need_show, get_owner_mecha_by_lobby_item_no, get_lobby_item_type, is_default_skin
from logic.gcommon.item.item_const import ITEM_SHOW_TYPE_MODEL, ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE, ITEM_SHOW_TYPE_NONE
from logic.gutils.reward_item_ui_utils import refresh_item_info, play_item_appear_to_idle_animation, smash_item_info
import cc
from logic.gcommon import const
from logic.gutils.charm_utils import show_charm_up_tips_and_update_charm_value
from enum import Enum
from logic.gutils import jump_to_ui_utils
from logic.gcommon.item import item_utility
from logic.comsys.mecha_display.MechaLobbyModuleWidget import MechaLobbyModuleWidget
from logic.gcommon.common_const import mecha_const
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_MECHA_SFX, L_ITEM_TYPE_MUSIC, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GESTURE, L_ITEM_KILL_SFX, L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_WALL_PICTURE, L_ITEM_TYPE_UNKONW_ITEM, L_ITEM_TYPE_GUANGMU
from logic.gutils.role_skin_utils import show_jump_to_improve_skin_dlg
from common.cfg import confmgr
SKIP_ITEMS = (111, 70400026, 70200061)
REWARD_ITEM_APPEAR_ACTION_TAG = 20240124

class BtnGoClickedBehavior(Enum):
    BtnGoClickedBehavior = 0
    GoToLottery = 1
    GoToModule = 2
    GoToItemsBook = 3
    UseLobbySkin = 4
    UseMechaPose = 5
    UseLobbyBgm = 6
    UseWallPic = 7
    UseGuangmu = 8


class ReceiveRewardUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/get_award'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    IS_FULLSCREEN = True
    GLOBAL_EVENT = {'receive_award_succ_event': 'on_receive_award_succ',
       'receive_award_succ_event_from_lottery': 'on_receive_award_succ_from_lottery',
       'receive_award_succ_event_from_nile': 'on_receive_award_succ_from_nile',
       'refresh_common_reward_ui_performance_temporarily': 'refresh_performance_temporarily',
       'show_cache_generic_reward': 'show_cache_reward',
       'show_cache_specific_reward': 'show_specific_cache_reward',
       'test_ui_animation_event': 'on_receive_award_test',
       'set_reward_show_blocking_item_no_event': 'on_set_reward_show_blocking_item_no'
       }
    UI_ACTION_EVENT = {'panel.OnClick': 'on_close',
       'panel.temp_btn_go.btn_common_big.OnClick': 'on_btn_go_clicked'
       }
    CACHE_REWARD_LIST = []
    CACHE_REWARD_DICT = {}
    CACHE_REWARD_REASON_HANDLER = {}
    UI_VKB_TYPE = UI_VKB_CUSTOM
    REWARD_TIPS_SWALLOW = 0
    REWARD_TIPS_APPEND_LIST = 1
    REWARD_TIPS_APPEND_DICT = 2

    @staticmethod
    def register_reason_handler(uniq_key, reason_func, handler=REWARD_TIPS_SWALLOW):
        ReceiveRewardUI.CACHE_REWARD_REASON_HANDLER[uniq_key] = (reason_func, handler)

    @staticmethod
    def unregister_reason_handler--- This code section failed: ---

  79       0  LOAD_GLOBAL           0  'ReceiveRewardUI'
           3  LOAD_ATTR             1  'CACHE_REWARD_REASON_HANDLER'
           6  LOAD_ATTR             2  'pop'
           9  LOAD_ATTR             1  'CACHE_REWARD_REASON_HANDLER'
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

    def clear_show_reward(self):
        self.CACHE_REWARD_LIST = []
        self.CACHE_REWARD_DICT.clear()
        self.close()

    def is_showing(self):
        return self.item_showing

    def on_init_panel(self, *args, **kwargs):
        self.hide()
        self.total_reward_queue = []
        self.reward_list = []
        self.reward_count = 0
        self.chips_data = {}
        self.item_update_cb = None
        self.show_list_node = None
        self.show_index = 0
        self.item_showing = False
        self.detailing_item_index = None
        self.smashing_item_index = set()
        self.reward_show_blocking_item_no_set = set()
        self.get_default_no_show_item_no_set()
        self._btn_go_clicked_beh_map = {BtnGoClickedBehavior.GoToLottery: '_on_btn_go_to_lottery_clicked',
           BtnGoClickedBehavior.GoToModule: '_on_btn_go_to_module_clicked',
           BtnGoClickedBehavior.GoToItemsBook: '_on_btn_go_to_items_book_clicked',
           BtnGoClickedBehavior.UseLobbySkin: '_on_btn_use_lobby_skin_clicked',
           BtnGoClickedBehavior.UseMechaPose: '_on_btn_use_mecha_pose_clicked',
           BtnGoClickedBehavior.UseLobbyBgm: '_on_btn_use_lobby_bgm_clicked',
           BtnGoClickedBehavior.UseWallPic: '_on_btn_use_wall_pic_clicked',
           BtnGoClickedBehavior.UseGuangmu: '_on_btn_use_guangmu_clicked'
           }
        self._btn_go_clicked_behavior = BtnGoClickedBehavior.GoToLottery
        self._go_to_module_item_no = None
        self._use_item_no = None
        self._slot_2_module_btn_idx = {mecha_const.MODULE_ATTACK_SLOT: MechaLobbyModuleWidget.BTN_ATK_IDX,
           mecha_const.MODULE_DEFEND_SLOT: MechaLobbyModuleWidget.BTN_DFD_IDX,
           mecha_const.MODULE_MOVE_SLOT: MechaLobbyModuleWidget.BTN_MOVE_IDX,
           mecha_const.SP_MODULE_SLOT: MechaLobbyModuleWidget.BTN_SP1_IDX
           }
        if not global_data.is_low_mem_mode:
            self.panel.list_award.EnableItemAutoPool(True)
            self.panel.list_award.SetInitCount(5)
            self.panel.list_award_18.EnableItemAutoPool(True)
            self.panel.list_award_more.EnableItemAutoPool(True)
        self.close_callback = None
        self.callback_advance_rate = 0.15
        self.temporarily_block_close = False
        return

    def test_data(self):
        reward_dict = {30248001: 1,50301003: 1,50102006: 80,50500008: 3,50101002: 400,50101003: 600,50101006: 1,50101010: 1,50101011: 60,50301014: 2,30160151: 1,30160121: 1,50302014: 1}
        chips_source = {50101006: {208200321: [1, 1]}}

        def cb(ui_item, item_no, item_num, index):
            print('ui_item, item_no, item_no, reason', ui_item, item_no, item_no)
            ui_item.temp_reward.lab_quantity.setVisible(True)
            ui_item.temp_reward.lab_quantity.SetString('wawawawa')

        item_list = [
         (50101010, 2), (30248001, 2), (30248001, 1)]
        ori_list = [(), (), (50500008, 1)]
        global_data.emgr.receive_award_succ_event_from_nile.emit(item_list, ori_list, None)
        return

    def get_default_no_show_item_no_set(self):
        from logic.gutils import dress_utils
        self._default_no_show_item_no_set = set(dress_utils.get_invisible_decoration_id_list())

    def _check_show_reward_item(self):
        ui = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        return not (ui and ui.is_showing_model_item())

    def show_cache_reward(self):
        if not self._check_show_reward_item():
            return
        while ReceiveRewardUI.CACHE_REWARD_LIST:
            data = ReceiveRewardUI.CACHE_REWARD_LIST.pop()
            reward_dict, chips_source = data
            self.on_receive_award_succ(reward_dict, chips_source)

    def show_specific_cache_reward(self, key_item_no, close_callback=None):
        if not self._check_show_reward_item():
            if close_callback and callable(close_callback):
                close_callback()
            return
        if str(key_item_no) in ReceiveRewardUI.CACHE_REWARD_DICT:
            data = ReceiveRewardUI.CACHE_REWARD_DICT.pop(str(key_item_no))
            reward_dict, chips_source = data
            cur_showing = self.item_showing
            self.on_receive_award_succ(reward_dict, chips_source)
            if close_callback and callable(close_callback):
                if cur_showing:
                    close_callback()
                elif self.item_showing:
                    self.close_callback = close_callback
                else:
                    close_callback()
        elif close_callback and callable(close_callback):
            close_callback()

    def _check_is_improved_skin_sfx_item(self, reward_list):
        conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content')
        for item_id, item_count in reward_list:
            if str(item_id) in conf:
                return True

        return False

    def on_receive_award_succ(self, reward_dict, chips_source=None, reason=None, item_update_cb=None):
        if not reward_dict:
            return
        do_show = False
        for key in six.iterkeys(reward_dict):
            type = confmgr.get('lobby_item', str(key), 'type')
            if type:
                type_conf = confmgr.get('lobby_item_type', str(type))
                if type_conf and type_conf.get('need_show', 0):
                    do_show = True
                    break

        if not do_show:
            return
        if reason:
            for uniq_key, (func, handler) in six.iteritems(ReceiveRewardUI.CACHE_REWARD_REASON_HANDLER):
                if func(reason):
                    if handler == ReceiveRewardUI.REWARD_TIPS_APPEND_LIST:
                        ReceiveRewardUI.CACHE_REWARD_LIST.append((reward_dict, chips_source))
                    elif handler == ReceiveRewardUI.REWARD_TIPS_APPEND_DICT:
                        ReceiveRewardUI.CACHE_REWARD_DICT[uniq_key] = (
                         reward_dict, chips_source)
                    return

        if reason and (reason.startswith(const.LOTTERY_ADDITIONAL_ITEMS) or reason.startswith(const.SKIN_ADDITIONAL_ITEMS)):
            lottery_item_no = reason.split('_')[-1]
            ReceiveRewardUI.CACHE_REWARD_DICT[lottery_item_no] = (reward_dict, chips_source)
            return
        if reason == const.MECHA_ROLE_INIT_GIVE_FREE_ITEMS_REASON or not self._check_show_reward_item():
            ReceiveRewardUI.CACHE_REWARD_LIST.append((reward_dict, chips_source))
            return
        if global_data.player and global_data.player.is_in_battle():
            ReceiveRewardUI.CACHE_REWARD_LIST.append((reward_dict, chips_source))
            return
        if reason and (reason.startswith('OPEN_PUZZLE') or reason == 'OPEN_ALL_PUZZLE'):
            ReceiveRewardUI.CACHE_REWARD_DICT[reason] = (
             reward_dict, chips_source)
            return
        if reason and (reason == const.TASK_REWARD_NUOMA or reason == const.TASK_REWARD_YUTONG):
            ReceiveRewardUI.CACHE_REWARD_DICT[reason] = (
             reward_dict, chips_source)
            return
        reward_list = []
        chips_data = {}
        cur_index = 0
        for item_no, item_num in six.iteritems(reward_dict):
            if int(item_no) in self.reward_show_blocking_item_no_set:
                continue
            if int(item_no) in self._default_no_show_item_no_set:
                continue
            if int(item_no) in SKIP_ITEMS:
                continue
            if chips_source and item_no in chips_source:
                chip_source_data = chips_source[item_no]
                for origin_item_no in six.iterkeys(chip_source_data):
                    origin_item_num, chip_num = chip_source_data[origin_item_no]
                    reward_list.append((origin_item_no, origin_item_num))
                    chips_data[cur_index] = (item_no, chip_num)
                    cur_index += 1
                    item_num -= chip_num

            if item_num > 0:
                reward_list.append((item_no, item_num))
                cur_index += 1

        if not reward_list:
            return
        if self._check_is_improved_skin_sfx_item(reward_list):
            show_jump_to_improve_skin_dlg(reward_list)
            return
        self._cur_reward_reason = reason
        reward_count = cur_index
        if not self.item_showing:
            self.item_showing = True
            self.show_award(reward_list, chips_data, reward_count, reason, item_update_cb)
        else:
            self.total_reward_queue.append((reward_list, chips_data, reward_count, reason, item_update_cb))

    def on_receive_award_succ_from_lottery(self, item_list, origin_list):
        if not item_list:
            return
        else:
            self._cur_reward_reason = None
            reward_list = []
            chips_data = {}
            cur_index = 0
            for origin_item_info in origin_list:
                if origin_item_info:
                    if self.check_in_skip_items(origin_item_info):
                        continue
                    reward_list.append(origin_item_info)
                    chips_data[cur_index] = item_list[cur_index]
                else:
                    if self.check_in_skip_items(item_list[cur_index]):
                        continue
                    reward_list.append(item_list[cur_index])
                cur_index += 1

            if not reward_list:
                return
            reward_count = cur_index
            if not self.item_showing:
                self.item_showing = True
                self.show_award(reward_list, chips_data, reward_count, None)
            else:
                self.total_reward_queue.append((reward_list, chips_data, reward_count, None, None))
            return

    def on_receive_award_succ_from_nile(self, item_list, origin_list, cb=None):
        if not item_list:
            return
        else:
            self._cur_reward_reason = None
            reward_list = []
            chips_data = {}
            cur_index = 0
            for origin_item_info in origin_list:
                if origin_item_info:
                    if self.check_in_skip_items(origin_item_info):
                        continue
                    reward_list.append(origin_item_info)
                    chips_data[cur_index] = item_list[cur_index]
                else:
                    if self.check_in_skip_items(item_list[cur_index]):
                        continue
                    reward_list.append(item_list[cur_index])
                cur_index += 1

            if not reward_list:
                return
            reward_count = cur_index
            if not self.item_showing:
                self.item_showing = True
                self.show_award(reward_list, chips_data, reward_count, None, cb)
            else:
                self.total_reward_queue.append((reward_list, chips_data, reward_count, None, cb))
            return

    def refresh_performance_temporarily(self, rate=0.15, block_close=False):
        if self.item_showing and block_close:
            return
        self.callback_advance_rate = rate
        self.temporarily_block_close = block_close

    def on_receive_award_test(self, anim_name):
        self.panel.PlayAnimation(anim_name)

    def show_award(self, reward_list, chips_data, reward_count, reason, item_update_cb=None):
        if not self.isVisible():
            self.show()
            self.panel.temp_btn_go.setVisible(False)
        self.panel.StopAnimation('reset')
        self.panel.img_left.setVisible(False)
        self.panel.img_right.setVisible(False)
        if reward_count <= 7:
            show_list_node = self.panel.list_award
            hide_node_list = [self.panel.list_award_18, self.panel.list_award_more]
        elif reward_count <= 18:
            show_list_node = self.panel.list_award_18
            hide_node_list = [self.panel.list_award, self.panel.list_award_more]
        else:
            show_list_node = self.panel.list_award_more
            hide_node_list = [self.panel.list_award, self.panel.list_award_18]

            @show_list_node.callback()
            def OnScrolling(scroll_list):
                if scroll_list.isValid():
                    self.panel.img_left.setVisible(not scroll_list.IsLeftMost())
                    self.panel.img_right.setVisible(not scroll_list.IsRightMost())

        show_list_node.setVisible(True)
        for one_node in hide_node_list:
            one_node.setVisible(False)

        self.panel.stopAllActions()
        self.reward_list = reward_list
        self.chips_data = chips_data
        self.show_list_node = show_list_node
        self.item_update_cb = item_update_cb
        show_list_node.SetInitCount(reward_count)
        for item in show_list_node.GetAllItem():
            item.setVisible(False)

        show_list_size = show_list_node.GetContentSize()
        self.panel.ignore_btn.SetContentSize(*show_list_size)
        self.show_index = 0
        self.reward_count = reward_count
        action_list = list()
        anim_time = 0.02

        def callback(*args):
            self.panel.PlayAnimation('appear')
            global_data.sound_mgr.play_ui_sound('rewarded')

        action_list.append(cc.CallFunc.create(callback))
        action_list.append(cc.DelayTime.create(anim_time))
        action_list.append(cc.CallFunc.create(lambda : self.show_next_item()))
        self.panel.runAction(cc.Sequence.create(action_list))
        if reason != const.EXPIRE_ITEM_USE_REASON:
            charm_item_list = []
            for idx in range(reward_count):
                if idx not in self.chips_data:
                    charm_item_list.append(reward_list[idx])

            show_charm_up_tips_and_update_charm_value(charm_item_list)
        if show_list_node.OnScrolling:
            show_list_node.OnScrolling()

    def show_next_item(self):
        if self.show_index < self.reward_count:
            item_no, item_num = self.reward_list[self.show_index]
            award_item = self.show_list_node.GetItem(self.show_index)
            if award_item is None:
                return
            if self.item_update_cb:
                self.item_update_cb(award_item, item_no, item_num, self.show_index)
                need_show = ITEM_SHOW_TYPE_NONE
                item_type = L_ITEM_TYPE_UNKONW_ITEM
            else:
                refresh_item_info(award_item, item_no, item_num)
                self.register_detail_click_event(award_item, self.show_index)
                need_show = get_item_need_show(item_no)
                item_type = get_lobby_item_type(item_no)
            ui_anim_end_callback = self.show_next_item
            if need_show == ITEM_SHOW_TYPE_MODEL and not is_default_skin(item_no):
                if self.show_index not in self.chips_data:

                    def func():

                        def callback():
                            if not (self.panel and self.panel.isValid()):
                                return
                            if not self.item_showing:
                                return
                            self.show()
                            self.show_next_item()

                        self.hide()
                        if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                            global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                        global_data.emgr.show_new_model_item.emit(item_no, callback)
                        global_data.emgr.hide_item_desc_ui_event.emit()

                    ui_anim_end_callback = func
            elif need_show == ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE:
                if self.show_index not in self.chips_data:

                    def func_wp():

                        def close_cb():
                            if not (self.panel and self.panel.isValid()):
                                return
                            if not self.item_showing:
                                return
                            self.show()
                            self.show_next_item()

                        self.hide()
                        if not global_data.ui_mgr.get_ui('GetWeaponDisplayUI'):
                            global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
                        global_data.emgr.show_new_weapon_skin.emit(item_no, close_cb)
                        global_data.emgr.hide_item_desc_ui_event.emit()

                    ui_anim_end_callback = func_wp
            elif item_type == L_ITEM_MECHA_SFX:
                if self.show_index not in self.chips_data:

                    def func_wp():

                        def close_cb():
                            if not (self.panel and self.panel.isValid()):
                                return
                            if not self.item_showing:
                                return
                            self.show()
                            self.show_next_item()

                        self.hide()
                        if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                            global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                        global_data.emgr.show_new_effect_item.emit(item_no, close_cb)
                        global_data.emgr.hide_item_desc_ui_event.emit()

                    ui_anim_end_callback = func_wp
            self.show_index += 1
            play_item_appear_to_idle_animation(award_item, item_no, item_num, ui_anim_end_callback, need_reset_node=True, callback_advance_rate=self.callback_advance_rate, action_tag_id=REWARD_ITEM_APPEAR_ACTION_TAG)
        else:
            self.show_item_finished()
        return

    def show_item_finished(self):
        first = False
        action_list = []
        for index in six.iterkeys(self.chips_data):
            award_item = self.show_list_node.GetItem(index)
            if award_item is None:
                continue
            award_item.PlayAnimation('smash')
            self.smashing_item_index.add(index)
            if index == self.detailing_item_index:
                global_data.emgr.hide_item_desc_ui_event.emit()
            if not first:
                first = True
                action_list.append(cc.DelayTime.create(award_item.GetAnimationMaxRunTime('smash')))

        def end_smash_callback():
            self.temporarily_block_close = False
            for _index, chip_data in six.iteritems(self.chips_data):
                item_no, item_num = chip_data
                _award_item = self.show_list_node.GetItem(_index)
                if _award_item is None:
                    continue
                smash_item_info(_award_item, item_no, item_num)
                if _index in self.smashing_item_index:
                    self.smashing_item_index.remove(_index)
                play_item_appear_to_idle_animation(_award_item, item_no, item_num, callback=lambda _award_item=_award_item: _award_item.PlayAnimation('smash_scale'), need_reset_node=True, after_smash=True)

            to_show_btn_go = False
            from logic.gutils import item_utils
            if not to_show_btn_go:
                for data in self.reward_list:
                    item_no = data[0]
                    item_type = item_utils.get_lobby_item_type(item_no)
                    if item_utility.is_mecha_module_only_lobby(item_no) or item_utility.is_mecha_module_slot_only_lobby(item_no):
                        self._go_to_module_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.GoToModule
                        self.panel.temp_btn_go.btn_common_big.SetText(860031)
                        break
                    elif item_type == L_ITEM_TYPE_LOBBY_SKIN:
                        self._use_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.UseLobbySkin
                        self.panel.temp_btn_go.btn_common_big.SetText(80851)
                    elif item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
                        self._use_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.UseMechaPose
                        self.panel.temp_btn_go.btn_common_big.SetText(80851)
                    elif item_type == L_ITEM_TYPE_MUSIC:
                        self._use_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.UseLobbyBgm
                        self.panel.temp_btn_go.btn_common_big.SetText(80851)
                    elif item_type == L_ITEM_TYPE_WALL_PICTURE:
                        self._use_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.UseWallPic
                        self.panel.temp_btn_go.btn_common_big.SetText(80851)
                    elif item_type == L_ITEM_TYPE_GUANGMU:
                        self._use_item_no = item_no
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.UseGuangmu
                        self.panel.temp_btn_go.btn_common_big.SetText(80851)

            if not to_show_btn_go:
                if len(self.reward_list) == 1:
                    from logic.gutils import item_utils
                    item_type = item_utils.get_lobby_item_type(self.reward_list[0][0])
                    if item_type in (L_ITEM_TYPE_GESTURE, L_ITEM_KILL_SFX):
                        to_show_btn_go = True
                        self._btn_go_clicked_behavior = BtnGoClickedBehavior.GoToItemsBook
                        self.panel.temp_btn_go.btn_common_big.SetText(860031)
            self.panel.temp_btn_go.setVisible(to_show_btn_go)
            return

        action_list.append(cc.CallFunc.create(end_smash_callback))
        self.panel.runAction(cc.Sequence.create(action_list))
        return

    def register_detail_click_event(self, item_nd, item_index):
        item_nd.temp_reward.btn_choose.UnBindMethod('OnClick')

        @item_nd.temp_reward.btn_choose.unique_callback()
        def OnBegin(layer, touch, *args):
            if item_index in self.smashing_item_index or self.detailing_item_index:
                return
            self.on_begin_show_detail(touch, item_index)

        @item_nd.temp_reward.btn_choose.unique_callback()
        def OnEnd(*args):
            if item_index in self.smashing_item_index:
                return
            self.on_end_show_detail(item_index)

        @item_nd.nd_smash_item.btn_choose.unique_callback()
        def OnBegin(layer, touch, *args):
            if item_index in self.smashing_item_index or self.detailing_item_index:
                return
            self.on_begin_show_detail(touch, item_index, True)

        @item_nd.nd_smash_item.btn_choose.unique_callback()
        def OnEnd(*args):
            if item_index in self.smashing_item_index:
                return
            self.on_end_show_detail(item_index)

    def on_begin_show_detail(self, touch, item_index, smash=False):
        data_list = smash and self.chips_data if 1 else self.reward_list
        if item_index >= len(data_list):
            return
        else:
            item_no, item_num = data_list[item_index]
            global_data.emgr.show_item_desc_ui_event.emit(item_no, None, touch.getLocation(), {'show_jump': False})
            self.detailing_item_index = item_index
            return

    def on_end_show_detail(self, item_index):
        global_data.emgr.hide_item_desc_ui_event.emit()
        self.detailing_item_index = None
        return

    def on_close(self, *args):
        if self.temporarily_block_close:
            return
        else:
            self.refresh_performance_temporarily()
            self.panel.PlayAnimation('reset')
            self.panel.stopAllActions()
            self.panel.list_award.DeleteAllSubItem()
            self.panel.list_award.StopAllSubItemActionByTag(REWARD_ITEM_APPEAR_ACTION_TAG)
            self.panel.list_award_18.DeleteAllSubItem()
            self.panel.list_award_18.StopAllSubItemActionByTag(REWARD_ITEM_APPEAR_ACTION_TAG)
            self.panel.list_award_more.DeleteAllSubItem()
            self.panel.list_award_more.StopAllSubItemActionByTag(REWARD_ITEM_APPEAR_ACTION_TAG)
            self.smashing_item_index.clear()
            if not self.total_reward_queue:
                self.hide()
                self.item_showing = False
                self.item_update_cb = None
                global_data.emgr.receive_award_end_event.emit()
                if self.close_callback and callable(self.close_callback):
                    self.close_callback()
                    self.close_callback = None
            else:
                reward_list, chips_data, reward_count, reason, item_update_cb = self.total_reward_queue.pop(0)
                self.show_award(reward_list, chips_data, reward_count, reason, item_update_cb)
            self.show_cache_reward()
            return

    def on_btn_go_clicked(self, *args):
        func_name = self._btn_go_clicked_beh_map.get(self._btn_go_clicked_behavior, None)
        if not func_name:
            return
        else:
            func = getattr(self, func_name, None)
            if not func or not callable(func):
                return
            func(self, *args)
            return

    def _on_btn_go_to_lottery_clicked(self, *args):
        from logic.gutils.jump_to_ui_utils import jump_to_lottery
        jump_to_lottery('7')
        self.on_close()

    def _on_btn_go_to_module_clicked(self, *args):
        mecha_id, module_slot = get_owner_mecha_by_lobby_item_no(self._go_to_module_item_no)
        if mecha_id:
            module_btn_idx = None
            if module_slot:
                module_btn_idx = self._slot_2_module_btn_idx.get(module_slot, None)
            jump_to_ui_utils.jump_to_mecha_module(mecha_id, module_btn_idx)
        self.on_close()
        return

    def _on_btn_go_to_items_book_clicked(self, *args):
        if self.reward_list:
            jump_to_ui_utils.jump_to_display_detail_by_item_no(self.reward_list[0][0])
        self.on_close()

    def _on_btn_use_lobby_skin_clicked(self, *args):
        if global_data.player and self._use_item_no:
            global_data.player.change_lobby_skin(self._use_item_no)
        self.on_close()

    def _on_btn_use_mecha_pose_clicked(self, *args):
        if global_data.player and self._use_item_no:
            from logic.gutils import item_utils
            mecha_item_id = item_utils.get_lobby_item_belong_no(self._use_item_no)
            global_data.player.try_set_mecha_pose(mecha_item_id, self._use_item_no)
        self.on_close()

    def _on_btn_use_lobby_bgm_clicked(self, *args):
        if global_data.player and self._use_item_no:
            global_data.player.select_lobby_bgm(self._use_item_no)
            global_data.player.req_del_item_redpoint(self._use_item_no)
        self.on_close()

    def _on_btn_use_wall_pic_clicked(self, *args):
        if global_data.player and self._use_item_no:
            global_data.player.select_wall_picture(self._use_item_no)
        self.on_close()

    def _on_btn_use_guangmu_clicked(self, *args):
        if global_data.player and self._use_item_no:
            global_data.player.set_selected_guangmu(self._use_item_no)
        self.on_close()

    def ui_vkb_custom_func(self):
        self.on_close()

    def on_set_reward_show_blocking_item_no(self, item_no_list):
        self.reward_show_blocking_item_no_set = set(item_no_list)

    def check_in_skip_items(self, item_info):
        if not item_info:
            return False
        if not isinstance(item_info, (list, tuple)):
            return False
        if not len(item_info) > 1:
            return False
        return item_info[0] in SKIP_ITEMS