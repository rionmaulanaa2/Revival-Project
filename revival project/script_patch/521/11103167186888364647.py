# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/OpenBoxUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_00
from common.utils.cocos_utils import cocos_pos_to_neox, neox_pos_to_cocos
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils.item_utils import get_item_need_show, get_item_rare_degree, get_lobby_item_type
from logic.gutils.reward_item_ui_utils import refresh_item_info, play_item_appear_to_idle_animation, smash_item_info
from logic.client.const import lobby_model_display_const
from logic.gcommon.item.item_const import ITEM_NO_EXP, ITEM_NO_BATTLEPASS_POINT
from logic.client.const.mall_const import MODE_NORMAL, MODE_SPECIAL, MODE_SPECIAL_2, SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DEF_PRICE_COLOR
from logic.gcommon.item.item_const import ITEM_SHOW_TYPE_MODEL, ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE, RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_5, RARE_DEGREE_6
from logic.gcommon.item.lobby_item_type import L_ITEM_MECHA_SFX, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN
from common.utils.timer import LOGIC, CLOCK
from logic.gcommon.common_const import scene_const
from logic.gutils.charm_utils import show_charm_up_tips_and_update_charm_value
from logic.gutils.mall_utils import get_special_price_info_for_yueka_single_lottery, special_buy_logic_for_yueka_single_lottery, get_mall_item_price, get_special_price_info_for_half_art_collection_single_lottery, special_buy_logic_for_half_art_collection_single_lottery
from logic.comsys.lottery.LotteryBuyWidget import LotteryBuyWidget
from common.platform.dctool.interface import is_mainland_package
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility
from common.cfg import confmgr
from common.const import uiconst
from random import randint
import math3d
import world
import time
import cc
from logic.gcommon.common_const.chat_const import CHAT_FRIEND, CHAT_CLAN, CHAT_WORLD, MSG_TYPE_LUCKY_LOTTERY
from common.const.property_const import U_ID, U_LV, CLAN_ID, C_NAME
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
BOX_WIDGET_PATH = 'mall/i_lottery_reward_item'
TOTAL_COUNT = 10
TEXTURE_PATH = [
 'model_new/scene/items/niudan/textures/niudan_red.tga',
 'model_new/scene/items/niudan/textures/niudan_blue.tga',
 'model_new/scene/items/niudan/textures/niudan_green.tga',
 'model_new/scene/items/niudan/textures/niudan_purple.tga',
 'model_new/scene/items/niudan/textures/niudan_yellow.tga',
 'model_new/scene/items/niudan/textures/niudan_cyan.tga']
EFFECT_PATH = 'effect/fx/niudan/caidan_%s_%s.sfx'
EFFECT_COLOR_LIST = ['white', 'green', 'blue', 'purple', 'jinse', 'leishe', 'red']
SOCKET_NAME = 'fx_root'
OPEN_EFFECT_DURATION = 1.0
CAPSULE_IDLE_ANIM = 'idle'
CAPSULE_OPEN_ANIM = 'open'
OPEN_ANIM_SPEED = 1
OPEN_ANIM_DURATION = 0.6 / OPEN_ANIM_SPEED
STAGE_IDLE = 0
STAGE_ROLL = 1
STAGE_HOLD = 2
STAGE_OPEN = 3
STAGE_ANIMATION = {STAGE_IDLE: [
              'idle', None],
   STAGE_ROLL: [
              'open_01', 0.5],
   STAGE_HOLD: [
              'open_02', None],
   STAGE_OPEN: [
              'open_03', 0.13]
   }
LOTTERY_OPEN_SOUND = {'single': {RARE_DEGREE_1: 'ui_luckyball_burst_green',
              RARE_DEGREE_2: 'ui_luckyball_burst_blue',
              RARE_DEGREE_3: 'ui_luckyball_burst_purple',
              RARE_DEGREE_4: 'ui_luckyball_burst_golden',
              RARE_DEGREE_6: 'ui_luckyball_burst_golden',
              RARE_DEGREE_5: 'ui_luckyball_burst_golden'
              },
   'multi': {RARE_DEGREE_1: 'ui_luckyball_multi_burst_green',
             RARE_DEGREE_2: 'ui_luckyball_multi_burst_blue',
             RARE_DEGREE_3: 'ui_luckyball_multi_burst_purple',
             RARE_DEGREE_4: 'ui_luckyball_multi_burst_golden',
             RARE_DEGREE_6: 'ui_luckyball_multi_burst_golden',
             RARE_DEGREE_5: 'ui_lottery_ss'
             }
   }
FRIEND_SHARE = 0
CLAN_SHARE = 1
CHAT_SHARE = 2
SHARE_INFO = (
 (
  FRIEND_SHARE, 634662),
 (
  CLAN_SHARE, 634663),
 (
  CHAT_SHARE, 800150))
SHARE_TYPE_TO_CHAT_TYPE = {FRIEND_SHARE: CHAT_FRIEND,
   CLAN_SHARE: CHAT_CLAN,
   CHAT_SHARE: CHAT_WORLD
   }
SEND_CD = 60

class OpenBoxUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/open_box'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'nd_bg.OnBegin': 'on_begin_bg',
       'nd_bg.OnDrag': 'on_drag_bg',
       'nd_bg.OnEnd': 'on_end_bg'
       }
    MODEL_DEFAULT_POSITION = {}

    def hide(self, *args):
        super(OpenBoxUI, self).hide()

    def show(self, *args):
        super(OpenBoxUI, self).show()
        self._reset_box_widgets_position()

    def on_init_panel(self):
        self.hide()
        self._is_continuous = False
        self._is_10_try = False
        self._extra_info = {}
        self.box_widget = dict()
        self.init_parameters()
        self.init_ui_click_event()
        self.init_buy_widget()
        self.init_lucky_widget()
        self.show_again_btn(False)
        self.process_event(True)

    def init_ui_click_event(self):

        @global_unique_click(self.panel.btn_sure)
        def OnClick(*args, **kwargs):
            if self.can_close and not self.item_showing:
                self.close()

    def init_buy_widget(self):

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == SINGLE_LOTTERY_COUNT:
                scene_type = confmgr.get('lottery_page_config', self.lottery_id, 'scene_type')
                if scene_type == 'special':
                    return get_special_price_info_for_yueka_single_lottery(self.lottery_id, price_info)
                if scene_type == 'art':
                    return get_special_price_info_for_half_art_collection_single_lottery(self.lottery_id, price_info)
            return False

        def check_buy_action_disabled(lottery_count):
            if is_mainland_package() and self.cur_lottery_count + lottery_count > self.max_lottery_count:
                global_data.game_mgr.show_tip(get_text_by_id(82040))
                return True
            return False

        def special_buy_logic_func(price_info, lottery_count):
            if self._is_10_try:
                if self.buy_widget.do_buy_10_try():
                    self.close()
                return True
            self._is_continuous = True
            if lottery_count == SINGLE_LOTTERY_COUNT:
                scene_type = confmgr.get('lottery_page_config', self.lottery_id, 'scene_type')
                if scene_type == 'special':
                    return special_buy_logic_for_yueka_single_lottery(self.lottery_id, self.panel, price_info, lambda : self.buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count))
                if scene_type == 'art':
                    extra_info = {'lottery_id': self.lottery_id}
                    return special_buy_logic_for_half_art_collection_single_lottery(self.lottery_id, self.panel, price_info, lambda : self.buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count), extra_info)
            return False

        def buying_callback(lottery_count):
            self.can_close = False
            self.show_again_btn(False)
            self.panel.temp_lucky.setVisible(False)
            self.lottery_count = lottery_count
            self._is_continuous = True
            result_item_ids = set()
            for item_no, item_num in six.itervalues(self.lottery_result):
                result_item_ids.add(item_no)

            global_data.emgr.lottery_open_box_result.emit(result_item_ids)

        lottery_ui = global_data.ui_mgr.get_ui('LotteryMainUI')
        cur_lottery_widget = lottery_ui.get_lottery_widget(self.lottery_id) if lottery_ui else None
        if cur_lottery_widget:
            if hasattr(cur_lottery_widget, 'custom_get_special_price_info'):
                custom_get_special_price_info = cur_lottery_widget.custom_get_special_price_info()
            else:
                custom_get_special_price_info = get_special_price_info
            if hasattr(cur_lottery_widget, 'custom_money_need_spent_func'):
                custom_money_need_spent_func = cur_lottery_widget.custom_money_need_spent_func()
            else:
                custom_money_need_spent_func = None
        else:
            custom_get_special_price_info = get_special_price_info
            custom_money_need_spent_func = None
        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, price_color=DEF_PRICE_COLOR, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_many_times
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_many_times.temp_price
           }, check_buy_action_disabled=check_buy_action_disabled, get_special_price_info=custom_get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback, special_money_need_spent_func=custom_money_need_spent_func)
        return

    def init_lucky_widget(self):
        temp_path = 'mall/luck/i_mall_luck_value_mine'
        self._lucky_widget = global_data.uisystem.load_template_create(temp_path, parent=self.panel.temp_lucky, name='_lucky_widget')

    def init_parameters(self):
        self.model_list = list()
        self.model_to_id = dict()
        self.texture_id_list = [ 0 for i in range(10) ]
        self.sfx_id_list = [ {} for i in range(10) ]
        self.model_opened = dict()
        self.lottery_result = dict()
        self.final_lottery_result = dict()
        self.model_stage = dict()
        self.stage_timer = dict()
        self.timer_execute_func_dict = dict()
        self.need_restart_timer_func = False
        self.items_show_id_queue = list()
        self.model_opened_id_set = set()
        self.model_opened_id_sequence = list()
        self.can_open_new = True
        self.ready_smash_id_map_queue = list()
        self.model_opened_full_set = set()
        self.loop_sound_id = dict()
        self.open_sound_waiting_play_list = list()
        self.open_sound_played = [ False for i in range(10) ]
        self.total_count = TOTAL_COUNT
        self.can_close = False
        self.detailing_widget_id = None
        self.item_showing = False
        self.from_auto_show_next = False
        self._cur_charm_items = []
        self.showing_model_id = None
        conf = confmgr.get('lottery_page_config', default={})
        self.lottery_id, self.lottery_count = global_data.emgr.get_cur_lucky_draw_info.emit()[0]
        self.max_lottery_count = conf[self.lottery_id].get('day_limit', 0)
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        self._screen_capture_helper = None
        self._friend_widget = None
        self._last_send_time_list = dict()
        return

    def _init_model_parameters(self, model, cur_id):
        self.model_list.append(model)
        if model.valid:
            model.get_sub_material(0).set_texture('Tex0', TEXTURE_PATH[self.generate_texture_id(cur_id, random=self.lottery_id != MODE_NORMAL)])
            self.model_opened[cur_id] = False
            self.scene.add_to_group(model, 'pickable_item')
            model.pickable = True

    def show_again_btn(self, flag):
        self.panel.btn_once.setVisible(flag)
        self.panel.btn_many_times.setVisible(flag)
        self.panel.btn_sure.setVisible(flag)

    def on_resolution_changed(self):
        self._reset_box_widgets_position()

    def _reset_box_widgets_position(self):
        if not self.box_widget or not self.model_list:
            return
        camera = self.scene.active_camera
        for i in range(self.total_count):
            model = self.model_list[i]
            widget = self.box_widget[i]
            if model.valid:
                x, y = camera.world_to_screen(model.world_position)
                x, y = neox_pos_to_cocos(x, y)
                pos = self.panel.convertToNodeSpace(cc.Vec2(x, y))
                widget.SetPosition(pos.x, pos.y)

    def _init_box_widget(self, cur_id):
        dlg = self.box_widget.get(cur_id) or global_data.uisystem.load_template_create(BOX_WIDGET_PATH, parent=self.panel)
        dlg.setVisible(False)
        self.box_widget[cur_id] = dlg

        @dlg.temp_reward.btn_choose.unique_callback()
        def OnBegin(btn, touch, *args):
            if self.item_showing:
                return
            self.on_begin_box_widget(touch, cur_id)

        @dlg.temp_reward.btn_choose.unique_callback()
        def OnEnd(*args):
            self.on_end_box_widget()

        @dlg.nd_smash_item.btn_choose.unique_callback()
        def OnBegin(btn, touch, *args):
            if self.item_showing:
                return
            self.on_begin_box_widget(touch, cur_id, True)

        @dlg.nd_smash_item.btn_choose.unique_callback()
        def OnEnd(*args):
            self.on_end_box_widget()

    def hide_box_widget(self):
        for widget in six.itervalues(self.box_widget):
            widget.setVisible(False)
            widget.stopAllActions()

    def on_background(self, *args):
        if self.panel.isVisible():
            self.on_end_box_widget()
            self.on_end_bg(None, None)
        return

    def on_resume(self):
        if self.panel.isVisible():
            global_data.emgr.set_lobby_scene_display_type.emit(lobby_model_display_const.LOTTERY)

    def on_before_login_reconnect_destroy(self):
        pass

    def on_login_reconnect(self):
        self.need_restart_timer_func = True

    def on_login_success(self):
        if self.need_restart_timer_func:
            for func in six.itervalues(self.timer_execute_func_dict):
                func and func()

            self.timer_execute_func_dict = dict()
            self.need_restart_timer_func = False

    def get_art_collect_scene_ball(self, index):
        self._stage_model = self.scene.get_model('niudan_tai_7')
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            log_error('[Error] test--get_art_collect_scene_ball--hang_ball_model = None')
            return
        bind_point = 'niudan_' + str(index)
        ball_model = hang_ball_model.get_socket_obj(bind_point, 0)
        return ball_model

    def lottery_ready(self, *args):
        self.show()
        self._enter_show_camera_scene()
        self.hide_main_ui()
        global_data.ui_mgr.close_ui('ScreenLockerUI')
        global_data.emgr.player_money_info_update_event.emit()
        if self.scene.scene_type != 'Lottery':
            return
        ui = global_data.ui_mgr.get_ui('LotteryBroadcastUI')
        ui and ui.show()
        pos_list = OpenBoxUI.MODEL_DEFAULT_POSITION.setdefault(self.lottery_id, [])
        need_init_default_pos = not pos_list
        for i in range(1, 11):
            cur_id = i - 1
            model = self.scene.get_model('niudan_%02d' % i)
            is_visible = cur_id < self.total_count
            model.visible = is_visible
            self.model_to_id[model] = cur_id
            if need_init_default_pos:
                pos_list.append(model.world_position)
            self._init_model_parameters(model, cur_id)

        if self.total_count == SINGLE_LOTTERY_COUNT:
            self.model_list[0].world_position = (pos_list[2] + pos_list[7]) * 0.5
        else:
            pos_list = OpenBoxUI.MODEL_DEFAULT_POSITION.setdefault(self.lottery_id, [])
            self.model_list[0].world_position = pos_list[0]
        camera = self.scene.active_camera
        for i in range(TOTAL_COUNT):
            model = self.model_list[i]
            if not model.visible:
                continue
            rand_speed = 0.9 + 0.01 * randint(1, 25)
            self._process_next_stage(i, STAGE_IDLE, rand_speed)
            self._init_box_widget(i)
            refresh_item_info(self.box_widget[i], max_len=11, *self.lottery_result[i])

        global_data.game_mgr.register_logic_timer(self._reset_box_widgets_position, times=1, interval=2, mode=LOGIC)

    def _reset_capsule_model(self):
        if type(self.model_list) in (tuple, list):
            for model in self.model_list:
                if model and model.valid:
                    model and model.stop_animation()

        self.model_list = []
        self.model_to_id = {}

    def ui_vkb_custom_func(self, *args):
        if global_data.is_pc_mode:
            ids = self._get_unopened_model_ids()
            if ids:
                self._open_all_balls()
            else:
                self.close()
            return True
        else:
            return False

    def on_finalize_panel(self):
        global_data.emgr.leave_current_scene.emit()
        for index, model in enumerate(self.model_list):
            if model.valid:
                model.play_animation(CAPSULE_IDLE_ANIM, 0, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
                model.visible = True
                if self.lottery_id == MODE_NORMAL:
                    model.get_sub_material(0).set_texture('Tex0', TEXTURE_PATH[self.generate_texture_id(index)])

        if self.total_count == SINGLE_LOTTERY_COUNT and self.model_list and self.model_list[0].valid:
            pos_list = OpenBoxUI.MODEL_DEFAULT_POSITION.setdefault(self.lottery_id, [])
            self.model_list[0].world_position = pos_list[0]
        global_data.game_mgr.register_logic_timer(self._reset_capsule_model, interval=2, times=1, mode=LOGIC)
        ui = global_data.ui_mgr.get_ui('MainChat')
        if ui:
            ui.set_need_show_btn(True)
        self.texture_id_list = None
        self.shutdown_box_opened_sfx()
        for sfx_type_to_id in self.sfx_id_list:
            for sfx_id in six.itervalues(sfx_type_to_id):
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_id_list = None
        self.box_widget = None
        self.model_opened = None
        result_item_ids = set()
        for ret in six.itervalues(self.lottery_result):
            item_no, item_num = ret
            result_item_ids.add(item_no)
            if item_no == ITEM_NO_EXP:
                global_data.player.accept_to_add_exp()
            elif item_no == ITEM_NO_BATTLEPASS_POINT:
                global_data.player.accept_to_add_bp()

        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        self.lottery_result = None
        self.final_lottery_result = None
        self.model_stage = None
        self.stage_timer = None
        self.timer_execute_func_dict = None
        self.items_show_id_queue = None
        self.model_opened_id_set = None
        self.model_opened_id_sequence = None
        self.ready_smash_id_map_queue = None
        self.model_opened_full_set = None
        ui = global_data.ui_mgr.get_ui('LotteryBroadcastUI')
        ui and ui.hide()
        self.show_main_ui()
        global_data.emgr.on_lottery_ended_event.emit()
        global_data.emgr.lottery_open_box_result.emit(result_item_ids)
        for playing_sound_id in six.itervalues(self.loop_sound_id):
            global_data.sound_mgr.stop_playing_id(playing_sound_id)

        self.process_event(False)
        global_data.player and global_data.player.check_waiting_bond_upgrade_sequences()
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        if self._friend_widget:
            self._friend_widget.destroy()
        self._friend_widget = None
        global_data.career_badge_prompt_mgr.play()
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'app_background_event': self.on_background,
           'app_lost_focus_event': self.on_background,
           'app_resume_event': self.on_resume,
           'art_collect_animation_end_event': self.lottery_ready,
           'net_login_reconnect_event': self.on_login_reconnect,
           'on_login_success_event': self.on_login_success,
           'shutdown_box_opened_sfx': self.shutdown_box_opened_sfx
           }
        if is_mainland_package():
            econf['buy_good_success'] = self.refresh_lottery_limit_count
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _filter_smash_items(self, items, origin_items):
        conf = confmgr.get('lobby_item_rare_degree_count').get_conf()
        for index, (item_id, count) in enumerate(items):
            if str(item_id) in conf and origin_items[index] and origin_items[index][0] in conf[str(item_id)]['ignore_smash_item_list']:
                origin_items[index] = None

        return

    def set_box_items(self, items, origin_items, is_10_try=False, extra_info=None):
        self._is_10_try = is_10_try
        self._extra_info = {} if extra_info is None else extra_info
        if is_10_try:
            goods_id = confmgr.get('lottery_page_config', self.lottery_id, 'try_params', 'goods_id', default=None)
            price = get_mall_item_price(goods_id)
            self.buy_widget.set_force_text(610829, (price, False))
        if self._is_continuous:
            self.hide_box_widget()
            self.init_parameters()
        self._filter_smash_items(items, origin_items)
        self.total_count = len(items)
        if self.total_count > TOTAL_COUNT:
            self.total_count = TOTAL_COUNT
        for i in range(TOTAL_COUNT):
            if i >= self.total_count:
                break
            if origin_items[i]:
                self.lottery_result[i] = origin_items[i]
            else:
                self.lottery_result[i] = items[i]
            self.final_lottery_result[i] = items[i]

        def callback():

            def pass_anim_callback():
                self.lottery_ready()

            transition_ui = global_data.ui_mgr.get_ui('GetModelDisplayBeforeUI')
            if not transition_ui:
                from logic.comsys.mall_ui.GetModelDisplayBeforeUI import GetModelDisplayBeforeUI
                transition_ui = GetModelDisplayBeforeUI()
            transition_ui.show_transition(pass_anim_callback)

        delay_time = 1 if self.lottery_id == MODE_NORMAL and not self._is_continuous else 0.01
        global_data.game_mgr.register_logic_timer(callback, interval=delay_time, times=1, mode=CLOCK)
        self.panel.lab_tips2.setVisible(bool(self._is_10_try))
        self.panel.lab_rule.setVisible(bool(self._is_10_try))
        return

    def on_begin_box_widget(self, touch, box_id, smash=False):
        if getattr(self, 'item_desc_showing', False):
            return
        else:
            self.item_desc_showing = True
            item_id = self.final_lottery_result[box_id][0] if smash else self.lottery_result[box_id][0]
            need_show = get_item_need_show(item_id)
            if need_show in (ITEM_SHOW_TYPE_MODEL, ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE) and self.lottery_result[box_id][0] == self.final_lottery_result[box_id][0] and not self._is_10_try:
                if need_show == ITEM_SHOW_TYPE_MODEL:

                    def callback():
                        self._enter_show_camera_scene()
                        self.show()

                    self.hide()
                    if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                        global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                    global_data.emgr.show_new_model_item.emit(item_id, callback, True, True)
                elif need_show == ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE:

                    def callback():
                        self._enter_show_camera_scene()
                        self.show()

                    self.hide()
                    if not global_data.ui_mgr.get_ui('GetWeaponDisplayUI'):
                        global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
                    global_data.emgr.show_new_weapon_skin.emit(item_id, callback)
            else:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position, extra_info={'show_jump': False})
            self.panel.nd_bg.setTouchEnabled(False)
            self.detailing_widget_id = box_id
            return

    def on_end_box_widget(self):
        global_data.emgr.hide_item_desc_ui_event.emit()
        self.panel.nd_bg.setTouchEnabled(True)
        self.detailing_widget_id = None
        self.item_desc_showing = False
        return

    def on_begin_bg(self, layer, touch):
        if self.can_close or self.item_showing:
            return
        self._do_touch_on_model(touch)

    def on_drag_bg(self, layer, touch):
        if self.can_close or self.item_showing:
            return
        self._do_touch_on_model(touch)

    def on_end_bg(self, layer, touch):
        self._on_end_bg()

    def _on_end_bg(self):
        if self.can_close:
            return
        if self.model_opened_id_set:
            if self.ready_smash_id_map_queue:
                ready_smash_map = self.ready_smash_id_map_queue.pop(0)
            else:
                ready_smash_map = dict()
                ready_smash_map['count'] = 0
            sound_waiting_play_set = set()
            highest_rare_degree = RARE_DEGREE_1
            charm_items = []
            for model_id in self.model_opened_id_set:
                ready_smash_map[model_id] = 1
                ready_smash_map['count'] += 1
                sound_waiting_play_set.add(model_id)
                self.open_sound_played[model_id] = False
                item_id, item_num = self.lottery_result[model_id]
                charm_items.append(self.final_lottery_result[model_id])
                rare_degree = get_item_rare_degree(item_id, item_num, ignore_imporve=True)
                highest_rare_degree = max(highest_rare_degree, rare_degree)

            self.open_sound_waiting_play_list.append([sound_waiting_play_set, highest_rare_degree])
            self.ready_smash_id_map_queue.append(ready_smash_map)
            self.can_open_new = False
            self._boom_one_by_one()
            self.model_opened_id_set.clear()
            self._cur_charm_items = charm_items

    def _handle_obsolete_stage_timer(self, model_id):
        cur_stage, start_time = self.model_stage[model_id]
        if cur_stage != STAGE_ROLL:
            return
        else:
            if model_id in self.stage_timer:
                global_data.game_mgr.unregister_logic_timer(self.stage_timer[model_id])
                self.stage_timer[model_id] = None
                self.stage_timer.pop(model_id)
                _, roll_duration = STAGE_ANIMATION[STAGE_ROLL]
                left_roll_time = roll_duration - (time.time() - start_time)
                if left_roll_time > 0:
                    global_data.game_mgr.register_logic_timer(lambda : self._process_next_stage(model_id, STAGE_OPEN), interval=left_roll_time, times=1, mode=CLOCK)
                else:
                    self._process_next_stage(model_id, STAGE_OPEN)
            return

    def _get_animation_info(self, stage, rare_degree):
        if stage == STAGE_OPEN and rare_degree in (RARE_DEGREE_4, RARE_DEGREE_6, RARE_DEGREE_5):
            return ('niudan03_open_03', 1.26)
        return STAGE_ANIMATION[stage]

    def _process_next_stage(self, model_id, target_stage=None, anim_speed=1.0):
        if model_id in self.timer_execute_func_dict:
            self.timer_execute_func_dict[model_id] = None
        next_stage = self.model_stage[model_id][0] + 1 if target_stage is None else target_stage
        if next_stage > STAGE_OPEN:
            self._on_model_animation_end(model_id)
            return
        else:
            item_id, item_num = self.lottery_result[model_id]
            rare_degree = get_item_rare_degree(item_id, item_num, ignore_imporve=True)
            anim_name, duration = self._get_animation_info(next_stage, rare_degree)
            if duration is None:
                loop_type = world.PLAY_FLAG_LOOP
            else:

                def execute_func():
                    self._process_next_stage(model_id)

                self.stage_timer[model_id] = global_data.game_mgr.register_logic_timer(execute_func, interval=duration, times=1, mode=CLOCK)
                self.timer_execute_func_dict[model_id] = execute_func
                loop_type = world.PLAY_FLAG_NO_LOOP
            self.model_list[model_id].valid and self.model_list[model_id].play_animation(anim_name, -1, world.TRANSIT_TYPE_DEFAULT, 0, loop_type, anim_speed)
            self.model_stage[model_id] = (next_stage, time.time())
            if next_stage == STAGE_OPEN:
                self.start_sfx_on_model(model_id, CAPSULE_OPEN_ANIM)
                global_data.sound_mgr.play_ui_sound(LOTTERY_OPEN_SOUND['multi'][rare_degree])
            if next_stage == STAGE_HOLD:
                self.loop_sound_id[model_id] = global_data.sound_mgr.play_sound_2d('Play_ui_click', ('ui_click',
                                                                                                     'ui_luckyball_open_loop'))
            elif self.loop_sound_id.get(model_id, None) is not None:
                global_data.sound_mgr.stop_playing_id(self.loop_sound_id[model_id])
                self.loop_sound_id.pop(model_id)
            return

    def _boom_one_by_one(self):
        if self.model_opened_id_sequence:
            model_id = self.model_opened_id_sequence.pop(0)
            self.model_opened[model_id] = True
            if self.model_stage[model_id][0] == STAGE_ROLL:
                self._handle_obsolete_stage_timer(model_id)
            else:
                self._process_next_stage(model_id)
            self.end_sfx_on_model(model_id, CAPSULE_IDLE_ANIM)
        else:
            self.can_open_new = True
            if not self._is_10_try:
                show_charm_up_tips_and_update_charm_value(self._cur_charm_items)
            self._cur_charm_items = []

    def _get_chosen_model_id(self, touch):
        pos = touch.getLocation()
        x, y = cocos_pos_to_neox(pos.x, pos.y)
        model = self.scene.pick(x, y, 'pickable_item', 1)[0]
        if model and model.visible:
            return self.model_to_id[model]
        else:
            return None

    def _do_touch_on_model(self, touch):
        if not self.can_open_new:
            return
        model_id = self._get_chosen_model_id(touch)
        self._do_touch_on_model_id(model_id)

    def _do_touch_on_model_id(self, model_id):
        if not self.can_open_new:
            return
        else:
            if model_id is not None:
                opened = self.model_opened.get(model_id, None)
                if opened is None:
                    return
                if not self.model_opened[model_id]:
                    item_id, item_num = self.lottery_result[model_id]
                    rare_degree = get_item_rare_degree(item_id, item_num, ignore_imporve=True)
                    if rare_degree >= RARE_DEGREE_4:
                        global_data.sound_mgr.play_ui_sound('luckyball_golden_open')
                    else:
                        global_data.sound_mgr.play_ui_sound('ui_luckyball_open')
                    self.model_opened[model_id] = True
                    self.model_opened_id_set.add(model_id)
                    self.model_opened_id_sequence.append(model_id)
                    self.start_sfx_on_model(model_id, CAPSULE_IDLE_ANIM)
                    self._process_next_stage(model_id)
            return

    def _open_all_balls(self):
        if self.can_close or self.item_showing:
            return
        ids = self._get_unopened_model_ids()
        if ids:
            for model_id in ids:
                if model_id < self.total_count:
                    self._do_touch_on_model_id(model_id)

            self._on_end_bg()

    def _get_unopened_model_ids(self):
        return [ model_id for model_id in self.model_opened if not self.model_opened[model_id] ]

    def _on_model_animation_end(self, model_id):
        if model_id in self.model_opened_full_set:
            return
        if self.model_list and self.model_list[model_id].valid:
            self.model_list[model_id].visible = False
            self.model_list[model_id].valid and self.model_list[model_id].play_animation(CAPSULE_IDLE_ANIM, 0, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
            self.model_opened_full_set.add(model_id)
            if len(self.model_opened_full_set) == self.total_count:
                self._finish_opened()
            item_id = self.lottery_result[model_id][0]
            need_show = get_item_need_show(item_id)
            item_type = get_lobby_item_type(item_id)
            is_show_model = False
            if need_show in (ITEM_SHOW_TYPE_MODEL, ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE) or item_type == L_ITEM_MECHA_SFX:
                is_show_model = True
            ready_smash_map = self.ready_smash_id_map_queue[0]
            not_smash = self.lottery_result[model_id] == self.final_lottery_result[model_id]
            if model_id in ready_smash_map and is_show_model and not_smash:
                ready_smash_map[model_id] += 1
            self._play_ui_animation(model_id, is_show_model)
            if is_show_model and not_smash and not self._is_10_try:
                self.items_show_id_queue.append((item_id, model_id))
                self.from_auto_show_next = False
                self.show_next_item()
            else:
                self._boom_one_by_one()

    def _finish_opened(self):
        self.panel.lab_tips.setVisible(False)
        self.can_close = True
        self.buy_widget.refresh_lottery_price()
        self.buy_widget.refresh_buy_btn_enable(True)
        self.show_again_btn(True)
        conf = confmgr.get('lottery_page_config', self.lottery_id)
        if len(self.lottery_result) == CONTINUAL_LOTTERY_COUNT and 'luck_rank_list' in conf:
            temp_lucky = self.panel.temp_lucky
            temp_lucky.setVisible(True)
            temp_lucky.setLocalZOrder(100)
            self._update_my_record()

    def _update_my_record(self):
        widget = self._lucky_widget
        widget.temp_lucky_value.PlayAnimation('show')
        bar_value = widget.temp_lucky_value.nd_tips.bar_value
        lab_tips_lottery = bar_value.lab_tips_lottery
        luck_score = int(self._extra_info.get('luck_score', 0))
        lab_value_lucky = bar_value.lab_lucky.nd_auto_fit.lab_value_lucky
        lab_value_lucky.setString(str(luck_score))
        lab_value_lucky.SetColor(16772438 if luck_score >= NORMAL_LUCK_SCORE_EDGE else 4650239)
        luck_intervene_weight_list = self._extra_info.get('luck_intervene_weight')
        luck_exceed_percent = self._extra_info.get('luck_exceed_percent')
        if luck_intervene_weight_list:
            value = next(iter(luck_intervene_weight_list.values()))
            if value <= LOTTERY_COUNT_SHOW_BAODI:
                lab_tips_lottery.setString(get_text_by_id(634637).format(value))
                lab_tips_lottery.setScale(1)
                self.panel.PlayAnimation('show')
            elif value > LOTTERY_COUNT_SHOW_BAODI or luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
                lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
                lab_tips_lottery.setScale(1)
                self.panel.PlayAnimation('show')
            else:
                lab_tips_lottery.setScale(0)
        elif luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
            lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
            lab_tips_lottery.setScale(1)
            self.panel.PlayAnimation('show')
        else:
            lab_tips_lottery.setScale(0)
        nd_red_packet = widget.nd_red_packet
        if self._extra_info.get('send_red_packet'):
            nd_red_packet.setVisible(True)
            nd_red_packet_visible = True

            @nd_red_packet.btn_show.unique_callback()
            def OnClick(btn, touch):
                ui = global_data.ui_mgr.get_ui('MainChat')
                if not ui:
                    return
                from logic.comsys.chat.MainChat import UI_WORLD_INDEX
                ui.clear_show_count_dict()
                ui.show_main_chat_ui(channel=UI_WORLD_INDEX)
                ui.block_all_click()
                ui.set_need_show_btn(False)
                ui.show_btn_tab_by_index_list([UI_WORLD_INDEX])

        else:
            nd_red_packet_visible = False
            nd_red_packet.setVisible(False)
        btn_sure = self.panel.btn_sure
        btn_once = self.panel.btn_once
        btn_many_times = self.panel.btn_many_times
        nd_share = widget.nd_share
        nd_red_packet = widget.nd_red_packet

        def share_cb(*args):
            btn_sure.setVisible(True)
            btn_once.setVisible(True)
            btn_many_times.setVisible(True)
            nd_share.setVisible(True)
            nd_red_packet.setVisible(nd_red_packet_visible)

        widget.btn_share_2.setVisible(global_data.is_share_show)

        @widget.btn_share_2.unique_callback()
        def OnClick(btn, touch):
            btn_sure.setVisible(False)
            btn_once.setVisible(False)
            btn_many_times.setVisible(False)
            nd_share.setVisible(False)
            nd_red_packet.setVisible(False)
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._screen_capture_helper.take_screen_shot([self.__class__.__name__], self.panel, custom_cb=share_cb)

        list_share = nd_share.list_share
        btn_share = nd_share.btn_share

        def update_arrow():
            is_visible = list_share.isVisible()
            btn_share.img_icon.setRotation(0 if is_visible else 180)

        for i in range(3):
            share_type, img_text = SHARE_INFO[i]
            item = list_share.option_list.GetItem(i)
            item.button.SetText(img_text)

            @item.button.callback()
            def OnClick(btn, touch, share_type=share_type):

                def on_click_friend(f_data):
                    uid = f_data[U_ID]
                    lv = f_data[U_LV]
                    last_send_time = self._last_send_time_list.get(uid, 0)
                    pass_time = time_utility.time() - last_send_time
                    if pass_time > SEND_CD:
                        global_data.game_mgr.show_tip(get_text_by_id(2177))
                        self._last_send_time_list[uid] = time_utility.time()
                        extra_data = self._get_extra_data()
                        global_data.message_data.recv_to_friend_msg(uid, f_data[C_NAME], '', lv, extra=extra_data)
                        global_data.player.req_friend_msg(uid, lv, f_data.get(CLAN_ID, -1), '', extra=extra_data)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(634638))

                def check_can_share--- This code section failed: ---

 946       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_last_send_time_list'
           6  LOAD_ATTR             1  'get'
           9  LOAD_ATTR             1  'get'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'last_send_time'

 947      18  LOAD_GLOBAL           2  'time_utility'
          21  LOAD_ATTR             3  'time'
          24  CALL_FUNCTION_0       0 
          27  LOAD_FAST             1  'last_send_time'
          30  BINARY_SUBTRACT  
          31  STORE_FAST            2  'pass_time'

 948      34  LOAD_FAST             2  'pass_time'
          37  LOAD_GLOBAL           4  'SEND_CD'
          40  COMPARE_OP            4  '>'
          43  POP_JUMP_IF_FALSE   137  'to 137'

 949      46  LOAD_GLOBAL           5  'global_data'
          49  LOAD_ATTR             6  'game_mgr'
          52  LOAD_ATTR             7  'show_tip'
          55  LOAD_GLOBAL           8  'get_text_by_id'
          58  LOAD_CONST            2  2177
          61  CALL_FUNCTION_1       1 
          64  CALL_FUNCTION_1       1 
          67  POP_TOP          

 950      68  LOAD_GLOBAL           2  'time_utility'
          71  LOAD_ATTR             3  'time'
          74  CALL_FUNCTION_0       0 
          77  LOAD_DEREF            0  'self'
          80  LOAD_ATTR             0  '_last_send_time_list'
          83  LOAD_FAST             0  'share_type'
          86  STORE_SUBSCR     

 951      87  LOAD_DEREF            0  'self'
          90  LOAD_ATTR             9  '_get_extra_data'
          93  CALL_FUNCTION_0       0 
          96  STORE_FAST            3  'extra_data'

 952      99  LOAD_GLOBAL          10  'SHARE_TYPE_TO_CHAT_TYPE'
         102  LOAD_FAST             0  'share_type'
         105  BINARY_SUBSCR    
         106  STORE_FAST            4  'chat_channel'

 953     109  LOAD_GLOBAL           5  'global_data'
         112  LOAD_ATTR            11  'player'
         115  LOAD_ATTR            12  'send_msg'
         118  LOAD_FAST             4  'chat_channel'
         121  LOAD_CONST            3  ''
         124  LOAD_CONST            4  'extra'
         127  LOAD_FAST             3  'extra_data'
         130  CALL_FUNCTION_258   258 
         133  POP_TOP          
         134  JUMP_FORWARD         22  'to 159'

 955     137  LOAD_GLOBAL           5  'global_data'
         140  LOAD_ATTR             6  'game_mgr'
         143  LOAD_ATTR             7  'show_tip'
         146  LOAD_GLOBAL           8  'get_text_by_id'
         149  LOAD_CONST            5  634638
         152  CALL_FUNCTION_1       1 
         155  CALL_FUNCTION_1       1 
         158  POP_TOP          
       159_0  COME_FROM                '134'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

                if share_type == FRIEND_SHARE:
                    if self._friend_widget is None:
                        from logic.comsys.share.CommonFriendListWidget import CommonFriendListWidget
                        nd = global_data.uisystem.load_template_create('common/i_common_friend_list', parent=widget.nd_friend)
                        self._friend_widget = CommonFriendListWidget(self, nd)
                        self._friend_widget.set_select_friend_cb(on_click_friend)
                        self._friend_widget.panel.nd_content.nd_search.setVisible(False)
                    else:
                        is_visible = self._friend_widget.is_visible()
                        if is_visible:
                            self._friend_widget.hide()
                        else:
                            self._friend_widget.show()
                elif share_type == CLAN_SHARE:
                    if global_data.player.get_clan_id() == -1:
                        global_data.game_mgr.show_tip(get_text_by_id(800098))
                        return
                    check_can_share(CLAN_SHARE)
                elif share_type == CHAT_SHARE:
                    check_can_share(CHAT_SHARE)
                list_share.setVisible(False)
                update_arrow()
                return

        @btn_share.callback()
        def OnClick(*args):
            list_share.setVisible(not list_share.isVisible())
            update_arrow()

        @list_share.nd_close.callback()
        def OnClick(*args):
            list_share.setVisible(False)
            update_arrow()

    def _get_extra_data(self):
        extra_data = {}
        extra_data['item_no'] = -1
        conf = confmgr.get('lottery_page_config', default={})
        luck_share_items = conf[self.lottery_id].get('luck_share_items')
        for item_no in luck_share_items:
            for item in self.lottery_result.values():
                result_item_no = item[0]
                if item_no == result_item_no:
                    extra_data['item_no'] = item_no
                    break

            if extra_data['item_no'] != -1:
                break

        lottery_result = {}
        for index, value in self.lottery_result.items():
            lottery_result[str(index)] = value

        extra_data['item_list'] = lottery_result
        extra_data['extra_info'] = self._extra_info
        extra_data['type'] = MSG_TYPE_LUCKY_LOTTERY
        extra_data['text_id'] = conf[self.lottery_id].get('text_id')
        extra_data['lottery_id'] = self.lottery_id
        return extra_data

    def _play_smash_animaiton(self, widget, cur_id):

        def end_smash_callback():
            item_id, item_num = self.final_lottery_result[cur_id]
            smash_item_info(widget, item_id, item_num)
            item_id, item_num = self.lottery_result[cur_id]
            play_item_appear_to_idle_animation(widget, item_id, item_num, callback=lambda : widget.PlayAnimation('smash_scale'), need_reset_node=True, after_smash=True)

        action_list = [
         cc.CallFunc.create(lambda : widget.PlayAnimation('smash')),
         cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound('ui_switch_card')),
         cc.DelayTime.create(widget.GetAnimationMaxRunTime('smash')),
         cc.CallFunc.create(end_smash_callback)]
        widget.runAction(cc.Sequence.create(action_list))

    def _handle_ready_smash_box_widget(self, model_id):
        if not self.ready_smash_id_map_queue:
            return
        ready_smash_map = self.ready_smash_id_map_queue[0]
        ready_smash_map[model_id] -= 1
        if ready_smash_map[model_id] == 0:
            ready_smash_map['count'] -= 1
        if ready_smash_map['count'] == 0:
            ready_smash_map.pop('count')
            for cur_id in six.iterkeys(ready_smash_map):
                if self.lottery_result[cur_id] == self.final_lottery_result[cur_id]:
                    continue
                if cur_id == self.detailing_widget_id:
                    global_data.emgr.hide_item_desc_ui_event.emit()
                self._play_smash_animaiton(self.box_widget[cur_id], cur_id)

            self.ready_smash_id_map_queue.pop(0)

    def _play_ui_animation(self, model_id, is_show_model):
        item_no, item_count = self.lottery_result[model_id]
        play_item_appear_to_idle_animation(self.box_widget[model_id], item_no, item_count, callback=lambda : self._handle_ready_smash_box_widget(model_id), need_reset_node=True)
        if not is_show_model and global_data.player:
            global_data.player.trigger_delay_notice_by_item_no(item_no)

    def _enter_show_camera_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_LOTTERY, lobby_model_display_const.LOTTERY)

    def check_texture_id_legal(self, index, texture_id):
        if index < 5:
            if index == 0:
                return True
            else:
                if index == 1:
                    return texture_id != self.texture_id_list[index - 1]
                return texture_id not in (self.texture_id_list[index - 1], self.texture_id_list[index - 2])

        elif 5 <= index < 10:
            if index == 5:
                return texture_id != self.texture_id_list[index - 5]
            else:
                if index == 6:
                    return texture_id not in (self.texture_id_list[index - 1], self.texture_id_list[index - 5])
                return texture_id not in (self.texture_id_list[index - 1], self.texture_id_list[index - 2], self.texture_id_list[index - 5])

        else:
            return True

    def generate_texture_id(self, index, random=True):
        if not random:
            return 0
        texture_id = randint(0, 5)
        while not self.check_texture_id_legal(index, texture_id):
            texture_id = randint(0, 5)

        self.texture_id_list[index] = texture_id
        return texture_id

    def _get_sfx_path(self, rare_degree, sfx_type):
        color = EFFECT_COLOR_LIST[rare_degree]
        return EFFECT_PATH % (color, sfx_type)

    def _get_sfx_scale(self, rare_degree):
        if self.total_count == CONTINUAL_LOTTERY_COUNT and rare_degree < RARE_DEGREE_4:
            return math3d.vector(0.6, 0.6, 0.6)
        return math3d.vector(1.0, 1.0, 1.0)

    def start_sfx_on_model(self, model_id, sfx_type):
        item_id, item_num = self.lottery_result[model_id]
        rare_degree = get_item_rare_degree(item_id, item_num, ignore_imporve=True)
        if rare_degree is None:
            print('\xe8\xbf\x99\xe6\x98\xaf\xe4\xbb\x80\xe4\xb9\x88\xe9\xac\xbc\xe7\x89\xa9\xe5\x93\x81\xe7\x89\xa9\xe5\x93\x81\xe8\xa1\xa8\xe9\x87\x8c\xe6\x9c\x89\xe5\xae\x83\xe5\x90\x97!!----item_id', item_id)
        sfx_path = self._get_sfx_path(rare_degree, sfx_type)
        if sfx_type == CAPSULE_IDLE_ANIM:
            sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self.model_list[model_id], SOCKET_NAME)
            self.sfx_id_list[model_id][sfx_type] = sfx_id
        elif self.model_list and self.model_list[model_id].valid:
            trans = self.model_list[model_id].get_socket_matrix('fx_root', world.SPACE_TYPE_WORLD)
            pos = trans.translation
            rot = trans.rotation

            def on_create_func(sfx):
                sfx.world_rotation_matrix = rot
                sfx.scale = self._get_sfx_scale(rare_degree)

            if not global_data.feature_mgr.is_postprocess_residual_in_partical_fixed():

                def on_remove_func(sfx):
                    sfx.destroy()

            else:
                on_remove_func = None
            sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=on_create_func, on_remove_func=on_remove_func)
            self.sfx_id_list[model_id][sfx_type] = sfx_id
        return

    def end_sfx_on_model(self, model_id, sfx_type):
        sfx_id = self.sfx_id_list[model_id].get(sfx_type, None)
        if sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
        return

    def shutdown_box_opened_sfx(self):
        if self.showing_model_id is not None and self.sfx_id_list[self.showing_model_id].get(CAPSULE_OPEN_ANIM, None):
            global_data.sfx_mgr.shutdown_sfx_by_id(self.sfx_id_list[self.showing_model_id][CAPSULE_OPEN_ANIM])
            self.showing_model_id = None
        return

    def refresh_lottery_limit_count(self):
        if not is_mainland_package():
            return
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)

    def auto_show_next_item(self):
        self.item_showing = False
        self.from_auto_show_next = True
        self.show_next_item()

    def show_next_item(self):
        if self.item_showing:
            return
        if self.items_show_id_queue:

            def delay_show():
                item_id, model_id = self.items_show_id_queue.pop(0)
                self.showing_model_id = model_id
                if model_id in self.timer_execute_func_dict:
                    self.timer_execute_func_dict[model_id] = None

                def callback():
                    self.show()
                    self._handle_ready_smash_box_widget(model_id)
                    self.auto_show_next_item()

                self.hide()
                self.on_end_bg(None, None)
                item_type = get_lobby_item_type(item_id)
                if item_type == L_ITEM_MECHA_SFX:
                    if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                        global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                    global_data.emgr.show_new_effect_item.emit(item_id, callback)
                elif item_type in (L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN):
                    if not global_data.ui_mgr.get_ui('GetWeaponDisplayUI'):
                        global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
                    global_data.emgr.show_new_weapon_skin.emit(item_id, callback)
                else:

                    def show_model_get():
                        if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                            global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                        global_data.emgr.show_new_model_item.emit(item_id, callback, False, not self.from_auto_show_next)

                    role_video_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(item_id), 'chuchang_video', default=None)
                    mecha_video_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(item_id), 'chuchang_video', default=None)
                    video_path = role_video_path or mecha_video_path
                    if video_path:
                        global_data.video_player.play_video(video_path, show_model_get, repeat_time=1, bg_play=True)
                    else:
                        show_model_get()
                return

            self.item_showing = True
            global_data.emgr.hide_item_desc_ui_event.emit()
            if self.from_auto_show_next:
                delay_show()
            else:
                _item_id, _model_id = self.items_show_id_queue[0]
                _item_num = self.lottery_result[_model_id][1]
                if get_item_rare_degree(_item_id, _item_num, ignore_imporve=True) >= RARE_DEGREE_4:
                    delay_show()
                    return
                delay_show()
        else:
            self._enter_show_camera_scene()
            self.show()
            self._boom_one_by_one()

    def get_can_close(self):
        return self.can_close