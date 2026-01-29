# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202312/ActivityChristmasTurnable.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from logic.gutils.common_ui_utils import show_game_rule
from logic.gutils.global_data_utils import get_global_data
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, ITEM_RECEIVED, ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no, get_lobby_item_type
from logic.comsys.lottery.LotteryBuyWidget import LotteryBuyWidget
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DARK_PRICE_COLOR, LOTTERY_ST_OPEN_ONLY_EXCHANGE
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_EXPERIENCE_CARD, L_ITEM_TYPE_GUANGMU
import six_ex
from logic.comsys.activity.widget.TurntableWidget import TurntableWidget
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gutils.mall_utils import get_lottery_turntable_item_data, get_lobby_item_name
import six

class ChristmasLotteryBuyWidget(LotteryBuyWidget):

    def on_inited(self):
        super(ChristmasLotteryBuyWidget, self).on_inited()
        self.btn_click_sound = {SINGLE_LOTTERY_COUNT: 'ui_lottery_start_01',
           CONTINUAL_LOTTERY_COUNT: 'ui_lottery_start_02'
           }

    def set_always_show_enable(self, always_enable):
        self._lottery_btn_always_show_enable = always_enable

    def refresh_buy_btn_enable--- This code section failed: ---

  42       0  LOAD_FAST             1  'enable'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            9  'is-not'
           9  POP_JUMP_IF_FALSE    24  'to 24'

  43      12  LOAD_FAST             1  'enable'
          15  LOAD_GLOBAL           1  'LotteryBuyWidget'
          18  STORE_ATTR            2  'BUY_BUTTON_ENABLED'
          21  JUMP_FORWARD          0  'to 24'
        24_0  COME_FROM                '21'

  44      24  SETUP_LOOP           79  'to 106'
          27  LOAD_GLOBAL           3  'six'
          30  LOAD_ATTR             4  'itervalues'
          33  LOAD_FAST             0  'self'
          36  LOAD_ATTR             5  'nd_buttons'
          39  CALL_FUNCTION_1       1 
          42  GET_ITER         
          43  FOR_ITER             59  'to 105'
          46  STORE_FAST            2  'nd_button'

  45      49  LOAD_FAST             2  'nd_button'
          52  LOAD_ATTR             6  'SetEnable'
          55  LOAD_GLOBAL           1  'LotteryBuyWidget'
          58  LOAD_ATTR             2  'BUY_BUTTON_ENABLED'
          61  CALL_FUNCTION_1       1 
          64  POP_TOP          

  46      65  LOAD_GLOBAL           7  'hasattr'
          68  LOAD_GLOBAL           1  'LotteryBuyWidget'
          71  CALL_FUNCTION_2       2 
          74  POP_JUMP_IF_FALSE    43  'to 43'
          77  LOAD_FAST             0  'self'
          80  LOAD_ATTR             8  '_lottery_btn_always_show_enable'
        83_0  COME_FROM                '74'
          83  POP_JUMP_IF_FALSE    43  'to 43'

  47      86  LOAD_FAST             2  'nd_button'
          89  LOAD_ATTR             9  'SetShowEnable'
          92  LOAD_GLOBAL          10  'True'
          95  CALL_FUNCTION_1       1 
          98  POP_TOP          
          99  JUMP_BACK            43  'to 43'
         102  JUMP_BACK            43  'to 43'
         105  POP_BLOCK        
       106_0  COME_FROM                '24'
         106  LOAD_CONST            0  ''
         109  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 71

    def _get_common_free_goods_id_price_info(self):
        from logic.gutils.mall_utils import get_mall_item_price, lottery_calculate_money_need_spent
        free_price = get_mall_item_price(self.free_single_goods_id)
        original_price_count = free_price[0].get('original_price', 0)
        per_ticket_price = get_mall_item_price(self.data['ticket_goods_id'])
        final_price_info = per_ticket_price
        final_price_info[0]['real_price'] *= original_price_count
        final_price_info[0]['original_price'] *= original_price_count
        final_price_info[0]['discount_price'] = 0
        return final_price_info


class SimpleTurnable(object):

    def __init__(self, lottery_id, reward_id, round_item_list, buy_button_info, buy_price_info, extra_info):
        self.lottery_id = lottery_id
        self.reward_id = reward_id
        self.round_item_list = round_item_list
        self._idx_to_item = []
        self._item_to_idx = {}
        self._last_choose_item = None
        self._init_reward_items(reward_id, round_item_list)
        self._old_buy_button_info_text = {}
        for lottery_count, btn in buy_button_info.items():
            if btn.lab_once:
                default_single_lottery_btn_text = btn.lab_once.getString()
            else:
                default_single_lottery_btn_text = btn.GetText()
            self._old_buy_button_info_text[btn] = default_single_lottery_btn_text

        self.init_buy_widget(buy_button_info, buy_price_info)
        self._turnable_widget = None
        extra_info = extra_info or {}
        self._select_cb = extra_info.get('select_cb', None)
        self._stop_cb = extra_info.get('stop_cb', None)
        self.turntable_ret = None
        self.data = confmgr.get('lottery_page_config', str(lottery_id), default={})
        self.is_destroyed = False
        self.lottery_win_sound_id = None
        self.need_refresh_round_data = False
        if self.data.get('extra_single_goods_id'):
            self.need_refresh_round_data = True
            self.turntable_item_list = confmgr.get('preview_%s' % reward_id, 'turntable_goods_info', default=())
            self.max_draw_count = len(self.turntable_item_list)
            self.all_round_finished = False
            self.cur_single_goods_id = self.data['single_goods_id']
            self.single_goods_id_list = [self.cur_single_goods_id]
            self.single_goods_id_list.extend(self.data['extra_single_goods_id'])
            self.single_goods_id_list.append(self.single_goods_id_list[-1])
            self.refresh_round_data()
        self.process_event(True)
        return

    def refresh_round_data(self):
        if not self.need_refresh_round_data:
            return
        drawn_count = 0
        for item_id, item_count in self.turntable_item_list:
            drawn_count += global_data.player.get_reward_intervene_count(self.reward_id).get(item_id, 0)

        self.cur_single_goods_id = self.single_goods_id_list[drawn_count]
        self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
        self.all_round_finished = self.max_draw_count == drawn_count
        self.buy_widget.set_force_text(611341 if self.all_round_finished else '', price_info=([], False))

    def set_force_text(self, txt):
        if self.buy_widget:
            self.buy_widget.set_force_text(txt, price_info=None)
        return

    def destroy(self):
        global_data.ui_mgr.close_ui('DailyChristmasTaskUI')
        for btn, text in self._old_buy_button_info_text.items():
            if btn.lab_once:
                btn.lab_once.setString(text)
            else:
                btn.SetText(text)

        self._old_buy_button_info_text = {}
        self.is_destroyed = True
        self.process_event(False)
        self.buy_widget and self.buy_widget.destroy()
        self.buy_widget = None
        self._turnable_widget and self._turnable_widget.on_finalize_panel()
        self._turnable_widget = None
        self.round_item_list = []
        self._idx_to_item = []
        self._item_to_idx = {}
        self._select_cb = None
        self._stop_cb = None
        self._last_choose_item = None
        self.turntable_ret = None
        self.data = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_lottery_result': self.on_receive_lottery_result
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_buy_widget(self, buy_button_info, buy_price_info):
        from logic.client.const.mall_const import USE_TEMPLATE_COLOR
        self.buy_widget = ChristmasLotteryBuyWidget(self, None, self.lottery_id, buy_button_info=buy_button_info, price_color=USE_TEMPLATE_COLOR, buy_price_info=buy_price_info)
        self.buy_widget.set_always_show_enable(True)
        return

    def _init_reward_items(self, reward_id, round_item_list):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN
        from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_pic_by_item_no
        reward_items = confmgr.get('preview_%s' % reward_id, 'turntable_goods_info', default=())
        for item_id, item_num in reward_items:
            item_id = int(item_id)
            idx = len(self._idx_to_item)
            self._idx_to_item.append(item_id)
            self._item_to_idx[item_id] = idx
            item_widget = round_item_list[idx]
            self.init_reward_item_helprt(item_widget, item_id, item_num)

    def init_reward_item_helprt(self, item_widget, item_id, item_num):
        pic_path = get_lobby_item_pic_by_item_no(item_id)
        item_widget.item.SetDisplayFrameByPath('', pic_path)
        item_widget.lab_num.SetString('x%d' % item_num)
        item_widget.EnableCustomState(True)

    def _init_turntable_widget(self):
        ext_conf = {'order_item': self.round_item_list,
           'init_interval': 0.05,
           'step_interval': 0.04,
           'max_interval': 0.5
           }
        self._turnable_widget = TurntableWidget(None, None, ext_conf)
        return

    def test1(self):
        item_list = [
         [
          71500012, 4]]
        origin_list = [None]
        extra_data = {}
        extra_info = {'luck_timestamp': None,'luck_score': None,'luck_intervene_weight': None,'send_red_packet': None,'luck_exceed_percent': None}
        self.on_receive_lottery_result(item_list, origin_list, extra_data, extra_info)
        return

    def on_receive_lottery_result(self, item_list, origin_list, extra_data, extra_info):
        self.turntable_ret = [
         item_list, origin_list]
        if item_list:
            target_item_id, target_item_num = item_list[0]
            if target_item_id in self._item_to_idx:
                reward_items = confmgr.get('preview_%s' % self.reward_id, 'turntable_goods_info', default=())
                target_item_id = str(target_item_id)
                for idx, item_id_num in enumerate(reward_items):
                    item_id, item_num = item_id_num
                    if item_id == target_item_id and item_num == target_item_num:
                        self.start_turnable_show(idx)
                        break

    def start_turnable_show(self, idx):
        if self.lottery_win_sound_id:
            global_data.sound_mgr.stop_playing_id(self.lottery_win_sound_id)
            self.lottery_win_sound_id = None
        self._init_turntable_widget()
        self._turnable_widget.set_final_item(idx, self.round_item_list[idx])
        self._turnable_widget.set_choose_callback(self.on_choose_cb)
        self._turnable_widget.set_pass_callback(self.on_choose_cb)
        self._turnable_widget.set_stop_callback(self.on_stop_cb)
        self._turnable_widget.start_turn_animation()
        return

    def on_choose_cb(self, item):
        if self._last_choose_item:
            self.set_item_sel(self._last_choose_item, False)
            self._last_choose_item = None
        self.set_item_sel(item, True)
        self._last_choose_item = item
        global_data.sound_mgr.play_ui_sound('lottery_rolling')
        return

    def on_stop_cb(self, idx, item):

        def cb():
            if self.is_destroyed:
                return
            else:
                if self._last_choose_item:
                    self.set_item_sel(self._last_choose_item, False)
                    self._last_choose_item = None
                global_data.emgr.on_lottery_ended_event.emit()
                global_data.emgr.player_money_info_update_event.emit()
                self.refresh_round_data()
                self._stop_cb and self._stop_cb(idx)
                if self.turntable_ret:
                    global_data.emgr.receive_award_succ_event_from_lottery.emit(*self.turntable_ret)
                    self.turntable_ret = None
                self.lottery_win_sound_id = global_data.sound_mgr.play_ui_sound('lottery_normal')
                return

        import game3d
        game3d.delay_exec(500, cb)

    def test(self):
        item_list = [
         [
          201002231, 1]]
        origin_list = [None]
        extra_data = {}
        extra_info = {'luck_timestamp': None,'luck_score': None,'luck_intervene_weight': None,'send_red_packet': None,'luck_exceed_percent': None}
        self.on_receive_lottery_result(item_list, origin_list, extra_data, extra_info)
        return

    def set_item_sel(self, item, is_sel):
        if item in self.round_item_list:
            idx = self.round_item_list.index(item)
            item.SetSelect(is_sel)
            item.vx_choose.setVisible(is_sel)
            if is_sel:
                self._select_cb and self._select_cb(idx, True)


class NonRepeatableTurnable(SimpleTurnable):

    def __init__(self, lottery_id, reward_id, round_item_list, buy_button_info, buy_price_info, extra_info, anim_round_item_list):
        self.anim_round_item_list = anim_round_item_list
        super(NonRepeatableTurnable, self).__init__(lottery_id, reward_id, round_item_list, buy_button_info, buy_price_info, extra_info)

    def init_reward_item_helprt(self, item_widget, item_id, item_num):
        from logic.gutils.item_utils import check_skin_tag
        pic_path = get_lobby_item_pic_by_item_no(item_id)
        if item_widget.btn_choose:
            item_widget.btn_choose.EnableCustomState(True)
            item_widget.btn_choose.setTouchEnabled(False)
        if get_lobby_item_type(item_id) not in [L_ITEM_TYPE_MECHA_SKIN, L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_GUANGMU]:
            item_widget.img_item.SetDisplayFrameByPath('', pic_path)
            item_widget.lab_num.SetString(str(item_num))
            item_widget.btn_choose.setTouchEnabled(True)

            @item_widget.btn_choose.callback()
            def OnClick(btn, touch, item_id=item_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, item_num=item_num)
                return

        item_widget.lab_name.SetString(get_lobby_item_name(item_id))
        if item_widget.temp_level:
            check_skin_tag(item_widget.temp_level, item_id)
        if item_widget.btn_show:

            @item_widget.btn_show.callback()
            def OnClick(btn, touch, item_id=item_id):
                from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                jump_to_display_detail_by_item_no(item_id)

        if item_widget.nd_got:
            if global_data.player:
                got_rewards_dict = global_data.player.get_reward_intervene_count(self.reward_id)
                item_widget.nd_got.setVisible(str(item_id) in got_rewards_dict)

    def set_item_sel(self, item, is_sel):
        if item in self.round_item_list:
            item.btn_choose.SetSelect(is_sel)

    def on_stop_cb(self, idx, item):

        def cb():
            if self.is_destroyed:
                return
            else:
                if self._last_choose_item:
                    self.set_item_sel(self._last_choose_item, False)
                    self._last_choose_item = None
                self.init_reward_item_helprt(item, self._idx_to_item[idx], -1)
                global_data.emgr.on_lottery_ended_event.emit()
                global_data.emgr.player_money_info_update_event.emit()
                self.refresh_round_data()
                self._stop_cb and self._stop_cb(idx)
                if self.turntable_ret:
                    global_data.emgr.receive_award_succ_event_from_lottery.emit(*self.turntable_ret)
                    self.turntable_ret = None
                return

        import game3d
        game3d.delay_exec(1000, cb)

    def start_turnable_show(self, idx):
        if self._turnable_widget:
            self._turnable_widget.on_finalize_panel()
        self._turnable_widget = None
        show_anim_round_list = list(self.anim_round_item_list)
        if global_data.player:
            got_rewards_dict = global_data.player.get_reward_intervene_count(self.reward_id)
            got_items = got_rewards_dict.keys()
            for item_id in got_items:
                _item_idx = self._item_to_idx.get(int(item_id))
                if _item_idx is not None:
                    if _item_idx == idx:
                        continue
                    item = self.round_item_list[_item_idx]
                    if item in show_anim_round_list:
                        show_anim_round_list.remove(item)

        ext_conf = {'order_item': show_anim_round_list,
           'init_interval': 0.05,
           'step_interval': 0.06,
           'max_interval': 0.4
           }
        self._turnable_widget = TurntableWidget(None, None, ext_conf)
        self._turnable_widget.set_final_item(idx, self.round_item_list[idx])
        self._turnable_widget.set_choose_callback(self.on_choose_cb)
        self._turnable_widget.set_pass_callback(self.on_choose_cb)
        self._turnable_widget.set_stop_callback(self.on_stop_cb)
        self._turnable_widget.start_turn_animation()
        return

    def test(self):
        item_list = [
         [
          201002231, 1]]
        origin_list = [None]
        extra_data = {}
        extra_info = {'luck_timestamp': None,'luck_score': None,'luck_intervene_weight': None,'send_red_packet': None,
           'luck_exceed_percent': None}
        self.on_receive_lottery_result(item_list, origin_list, extra_data, extra_info)
        return


class ActivityChristmasTurnable(ActivityTemplate):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update,
           'task_prog_changed': self.refresh_rp,
           'receive_task_reward_succ_event': self.refresh_rp,
           'receive_task_prog_reward_succ_event': self.refresh_rp
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        super(ActivityChristmasTurnable, self).init_parameters()
        self.repeatable_widget = None
        self.right_repeatable_widget = None
        return

    def on_finalize_panel(self):
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        self.repeatable_widget and self.repeatable_widget.destroy()
        self.repeatable_widget = None
        self.right_repeatable_widget and self.right_repeatable_widget.destroy()
        self.right_repeatable_widget = None
        self._price_top_widget and self._price_top_widget.on_finalize_panel()
        self._price_top_widget = None
        return

    def on_init_panel(self):
        super(ActivityChristmasTurnable, self).on_init_panel()
        self.widget_map = {}
        self.init_button_event()
        self.init_countdown_widget()
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = activity_conf.get('cUiData', {})
        self.left_lottery_id = self.ui_data.get('left_lottery_id', '130')
        self.left_reward_id = self.ui_data.get('left_reward_id', '12302764')
        self.left_currency = self.ui_data.get('left_currency', '71500011')
        self.right_lottery_id = self.ui_data.get('right_lottery_id', '131')
        self.right_reward_id = self.ui_data.get('right_reward_id', '12302765')
        self.right_currency = self.ui_data.get('right_currency', '71500012')
        left_round_item_list = [
         self.panel.btn_item_0, self.panel.btn_item_1, self.panel.btn_item_3, self.panel.btn_item_4]
        self.repeatable_widget = SimpleTurnable(self.left_lottery_id, self.left_reward_id, left_round_item_list, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_click
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.nd_content.temp_price
           }, extra_info={'select_cb': self.left_select_cb,'stop_cb': self.left_stop_cb})
        anim_round_data = self.ui_data.get('anim_round_data', [['list_item_0', [0]], ['list_item_1', [0]], ['list_item_2', [0, 1, 2, 3, 4, 5]]])
        anim_round_item_list = []
        for round_data in anim_round_data:
            widget_name, idx_list = round_data
            widget_list = getattr(self.panel, widget_name)
            if widget_list:
                widget_list.SetInitCount(len(idx_list))
                anim_round_item_list.extend([ widget_list.GetItem(i) for i in idx_list ])

        right_round_item_list = []
        right_round_item_list.extend(reversed(self.panel.list_item_2.GetAllItem()))
        right_round_item_list.extend(self.panel.list_item_1.GetAllItem())
        right_round_item_list.extend(reversed(self.panel.list_item_0.GetAllItem()))
        self.right_repeatable_widget = NonRepeatableTurnable(self.right_lottery_id, self.right_reward_id, right_round_item_list, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_lottery
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_lottery.temp_price
           }, extra_info={'stop_cb': self.right_stop_cb}, anim_round_item_list=anim_round_item_list)
        self.update_right_item_count()
        self.update_left_price_item()
        self.init_price_widget()
        self.refresh_rp()

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        ex_data = {'txt_id': 633922}
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_tips_time, self._activity_type, ex_data)

    def init_price_widget--- This code section failed: ---

 500       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'logic.gcommon.const'
           9  LOAD_ATTR             1  'gcommon'
          12  LOAD_ATTR             2  'const'
          15  STORE_FAST            1  'gconst'

 501      18  LOAD_GLOBAL           3  'PriceUIWidget'
          21  LOAD_GLOBAL           2  'const'
          24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             4  'panel'
          30  LOAD_ATTR             5  'list_money'
          33  LOAD_CONST            3  'pnl_title'
          36  LOAD_GLOBAL           6  'False'
          39  CALL_FUNCTION_513   513 
          42  LOAD_FAST             0  'self'
          45  STORE_ATTR            7  '_price_top_widget'

 502      48  LOAD_FAST             0  'self'
          51  LOAD_ATTR             7  '_price_top_widget'
          54  LOAD_ATTR             8  'show_money_types'
          57  LOAD_CONST            4  '%s_%s'
          60  LOAD_FAST             1  'gconst'
          63  LOAD_ATTR             9  'SHOP_PAYMENT_ITEM'
          66  LOAD_FAST             0  'self'
          69  LOAD_ATTR            10  'right_currency'
          72  BUILD_TUPLE_2         2 
          75  BINARY_MODULO    

 503      76  LOAD_FAST             1  'gconst'
          79  LOAD_ATTR            11  'SHOP_PAYMENT_YUANBAO'
          82  BUILD_LIST_2          2 
          85  CALL_FUNCTION_1       1 
          88  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 39

    def init_button_event(self):
        self.panel.btn_task.BindMethod('OnClick', self.on_click_task)

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            activity_type = self._activity_type
            conf = confmgr.get('c_activity_config', activity_type)
            act_name_id = conf['cNameTextID']
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))

    def on_click_task(self, *args):
        from logic.comsys.activity.Activity202312.DailyChristmasTaskUI import DailyChristmasTaskUI
        DailyChristmasTaskUI.PANEL_CONFIG_NAME = 'activity/activity_202404/activity_turntable/open_activity_turntable'
        DailyChristmasTaskUI.ACTIVITY_TYPE = self._activity_type
        dlg = DailyChristmasTaskUI()

    def on_main_ui_reshow(self):
        child_ui = global_data.ui_mgr.get_ui('DailyChristmasTaskUI')
        if child_ui:
            child_ui.add_show_count(self.__class__.__name__)

    def on_main_ui_hide(self):
        child_ui = global_data.ui_mgr.get_ui('DailyChristmasTaskUI')
        if child_ui:
            child_ui.add_hide_count(self.__class__.__name__)

    def left_select_cb(self, idx, is_sel):
        if is_sel:
            self.panel.img_arrow.setVisible(True)
            self.panel.img_arrow.setRotation(idx * 90)
        else:
            self.panel.img_arrow.setVisible(False)

    def left_stop_cb(self, idx):
        self.panel.img_arrow.setVisible(False)

    def right_stop_cb(self, idx):
        self.update_right_item_count()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_right_item_count(self):
        turntable_item_list = confmgr.get('preview_%s' % self.right_reward_id, 'turntable_goods_info', default=())
        max_draw_count = len(turntable_item_list)
        if not global_data.player:
            count = 0
        else:
            count = len(global_data.player.get_reward_intervene_count(self.right_reward_id))
        self.panel.lab_tips.SetString(get_text_by_id(635200, {'count': count,'max_count': max_draw_count}))
        if count == max_draw_count:
            self.panel.btn_lottery.SetEnable(False)
            self.panel.btn_lottery.lab_btn.setVisible(False)
            if self.repeatable_widget:
                self.repeatable_widget.set_force_text(611341)
            self.panel.btn_click.SetEnable(False)
            self.panel.btn_click.lab_once.SetString(611341)
            if self.right_repeatable_widget:
                self.right_repeatable_widget.set_force_text(611341)
        else:
            self.panel.btn_lottery.SetEnable(True)

    def update_left_price_item(self):
        if global_data.player:
            num = global_data.player.get_item_money(int(self.left_currency))
            self.panel.lab_value.SetString(str(num))

    def _on_player_info_update(self, *args):
        self.update_left_price_item()

    @staticmethod
    def check_lottery_can_draw(lottery_id, reward_id):
        from logic.gutils.mall_utils import get_goods_item_no, is_good_opened, limite_pay
        data = confmgr.get('lottery_page_config', str(lottery_id), default={})
        if 'free_single_goods_id' in data:
            goods_id = data['free_single_goods_id']
            if is_good_opened(goods_id) and not limite_pay(goods_id):
                return True
        if 'extra_single_goods_id' in data:
            turntable_item_list = confmgr.get('preview_%s' % reward_id, 'turntable_goods_info', default=())
            max_draw_count = len(turntable_item_list)
            all_round_finished = False
            cur_single_goods_id = data['single_goods_id']
            single_goods_id_list = [cur_single_goods_id]
            single_goods_id_list.extend(data['extra_single_goods_id'])
            single_goods_id_list.append(single_goods_id_list[-1])
            if not global_data.player:
                count = 0
            else:
                count = len(global_data.player.get_reward_intervene_count(reward_id))
            if max_draw_count == count:
                return False
            cur_single_goods_id = single_goods_id_list[count]
            if is_good_opened(cur_single_goods_id) and not limite_pay(cur_single_goods_id):
                if ActivityChristmasTurnable.check_is_enough_item_for_draw(cur_single_goods_id):
                    return True
        else:
            goods_id = data['single_goods_id']
            if is_good_opened(goods_id) and not limite_pay(goods_id):
                if ActivityChristmasTurnable.check_is_enough_item_for_draw(goods_id):
                    return True
        return False

    @staticmethod
    def check_is_enough_item_for_draw(goods_id):
        from logic.gutils.mall_utils import get_mall_item_price, check_payment
        prices = get_mall_item_price(goods_id)
        for price_info in prices:
            if check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                return True

        return False

    @staticmethod
    def show_tab_rp(activity_type):
        from logic.gutils import task_utils
        activity_conf = confmgr.get('c_activity_config', str(activity_type))
        ui_data = activity_conf.get('cUiData', {})
        left_lottery_id = ui_data.get('left_lottery_id', '130')
        left_reward_id = ui_data.get('left_reward_id', '12302764')
        right_lottery_id = ui_data.get('right_lottery_id', '131')
        right_reward_id = ui_data.get('right_reward_id', '12302765')
        if ActivityChristmasTurnable.is_all_draw_finished(right_reward_id):
            return False
        if ActivityChristmasTurnable.check_lottery_can_draw(left_lottery_id, left_reward_id):
            return True
        if ActivityChristmasTurnable.check_lottery_can_draw(right_lottery_id, right_reward_id):
            return True
        return ActivityChristmasTurnable.get_task_rp(activity_type)

    @staticmethod
    def is_all_draw_finished(reward_id):
        turntable_item_list = confmgr.get('preview_%s' % reward_id, 'turntable_goods_info', default=())
        max_draw_count = len(turntable_item_list)
        if not global_data.player:
            count = 0
        else:
            count = len(global_data.player.get_reward_intervene_count(reward_id))
        return max_draw_count == count

    @staticmethod
    def get_task_rp(act_id):
        from logic.gutils import task_utils
        activity_conf = confmgr.get('c_activity_config', str(act_id))
        ui_data = activity_conf.get('cUiData', {})
        daily_fixed = ui_data.get('daily_fixed')
        daily_random = ui_data.get('daily_random')
        right_reward_id = ui_data.get('right_reward_id', '12302765')
        if ActivityChristmasTurnable.is_all_draw_finished(right_reward_id):
            return False
        if daily_fixed:
            if task_utils.has_unreceived_reward(str(daily_fixed)):
                return True
        if daily_random:
            if task_utils.has_unreceived_reward(str(daily_random)):
                return True
        return False

    def refresh_rp(self, *args, **kargs):
        is_red = ActivityChristmasTurnable.get_task_rp(self._activity_type)
        self.panel.btn_task.temp_red.setVisible(is_red)
        self.panel.img_tips.setVisible(self.is_finish_all_task())

    def is_finish_all_task(self):
        from logic.gutils.task_utils import get_children_task
        from logic.gutils import task_utils
        activity_conf = confmgr.get('c_activity_config', str(self._activity_type))
        ui_data = activity_conf.get('cUiData', {})
        daily_fixed = ui_data.get('daily_fixed')
        daily_random = ui_data.get('daily_random')
        children_task_list = get_children_task(daily_fixed)
        if not global_data.player:
            return False
        for task_id in children_task_list:
            if not global_data.player.is_task_finished(task_id):
                return False

        children_task_list = get_children_task(daily_random)
        for task_id in children_task_list:
            if not global_data.player.is_task_finished(task_id):
                return False

        return True