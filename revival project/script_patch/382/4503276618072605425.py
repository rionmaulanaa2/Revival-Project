# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryGiftsUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import random
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.client.const import mall_const
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
import logic.gcommon.time_utility as tutil
from logic.gcommon.common_const import activity_const
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED
from cocosui import cc, ccui, ccs
IMG_GIFT_PATH = [
 'gui/ui_res_2/item/others/50930213.png',
 'gui/ui_res_2/item/others/50930214.png',
 'gui/ui_res_2/item/others/50930215.png',
 'gui/ui_res_2/item/others/50930216.png']
IMG_BOX_PATH = [
 'gui/ui_res_2/task/liveness_2.png',
 'gui/ui_res_2/task/liveness_3.png',
 'gui/ui_res_2/task/liveness_4.png',
 'gui/ui_res_2/task/liveness_5.png']
IMG_PANEL_PATH = [
 'gui/ui_res_2/activity/activity_202008/pnl_green.png',
 'gui/ui_res_2/activity/activity_202008/pnl_blue.png',
 'gui/ui_res_2/activity/activity_202008/pnl_purple.png',
 'gui/ui_res_2/activity/activity_202008/pnl_yellow.png']

class LotteryGiftsUI(BasePanel):
    INTERVAL_TIMES = 15
    SIMULATE_TIMES = 15
    PANEL_CONFIG_NAME = 'mall/premium_lottery_gifts'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close',
       'btn_des.OnClick': 'on_tips'
       }
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, activity_type):
        self._activity_type = activity_type
        self.init_parameters()
        self.process_event(True)
        self.register_timer()
        self.panel.PlayAnimation('appear')
        self.show_left_time()
        self.show_gifts()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()
        for key, _tick_now_num in six.iteritems(self._tick_now_num_map):
            _tick_goal_num = self._tick_goal_num_map[key]
            if _tick_now_num > _tick_goal_num:
                _tick_now_num = _tick_goal_num
            global_data.player and global_data.player.set_simulate_cache(key, _tick_now_num)

    def init_parameters(self):
        self._times = 0
        self._timer = 0
        self._timer_cb = {}
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self._parent_achieve_id_lst = conf.get('global_achieve_id', [])
        self._gift_goods_lst = conf.get('global_achieve_goods', [])
        self._is_first_open = True
        self._tick_goal_num_map = {}
        self._tick_now_num_map = {}
        self._second_tick_increase_num_map = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.refresh_gifts,
           'message_update_global_stat': self.up_tick_goal_num,
           'message_update_global_reward_receive': self.update_gl_receive_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def on_tips(self, *args):
        conf = confmgr.get('c_activity_config', self._activity_type)
        act_name_id = conf['cNameTextID']
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
        x, y = self.panel.btn_des.GetPosition()
        wpos = self.panel.btn_des.GetParent().ConvertToWorldSpace(x, y)
        dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def show_left_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0))
        self.panel.lab_time.SetString(get_text_by_id(604006).format(start_date, finish_date))

    def show_gifts(self):
        list_gifts = self.panel.list_gifts
        list_gifts.SetInitCount(len(self._parent_achieve_id_lst))
        self.refresh_gifts()
        self._timer_cb[0] = self.second_simulate_up

    def refresh_gifts(self, *args):
        list_gifts = self.panel.list_gifts
        for i, parent_id in enumerate(self._parent_achieve_id_lst):
            item_widget = list_gifts.GetItem(i)
            self.update_item_widget(item_widget, i)

        self.update_gl_receive_state()
        self.up_tick_goal_num()

    def do_buy(self, parent_achieve_id, goods_id):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import lottery_gifts_buy_confirmUI
        limite_buy = mall_utils.limite_pay(goods_id)
        open_date_range = mall_utils.get_goods_item_open_date(goods_id)
        opening, _ = mall_utils.check_limit_time_lottery_open_info(open_date_range)
        if limite_buy:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
            return
        if not opening:
            global_data.game_mgr.show_tip(get_text_by_id(606071))
            return
        lottery_gifts_buy_confirmUI(achieve_id=parent_achieve_id, goods_id=goods_id)

    def update_item_widget(self, item_widget, index):
        from logic.gutils.live_utils import format_view_person
        parent_id = self._parent_achieve_id_lst[index]
        achieve_conf = confmgr.get('global_achieve_data', str(parent_id), default=None)
        if not achieve_conf:
            print('[LotteryGiftsUI] achieve_id conf None', parent_id)
            return
        else:
            iTextID = achieve_conf.get('iTextID', '')
            item_widget.lab_name.SetString(iTextID)
            btn_pic = [
             IMG_GIFT_PATH[index],
             IMG_GIFT_PATH[index]]
            item_widget.btn_gifts.SetFrames('', btn_pic, False, None)
            item_widget.img_title_bar.SetDisplayFrameByPath('', IMG_PANEL_PATH[index])
            goods_id = self._gift_goods_lst[index]
            total_cond_value = 0
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            for i, aid in enumerate(children_achieves):
                child_conf = confmgr.get('global_achieve_data', str(aid))
                achieve_name = child_conf.get('cGStatName', '')
                des_num = child_conf.get('iCondValue')
                total_cond_value = des_num
                lab_num = getattr(item_widget, 'lab_num_{}'.format(i + 1))
                lab_num.SetString('{}'.format(format_view_person(des_num, num_format='%d')))
                temp_box = getattr(item_widget, 'temp_box_{}'.format(i + 1))
                temp_box.img_box.SetDisplayFrameByPath('', IMG_BOX_PATH[index])
                self.on_click_stage_reward(temp_box.btn_box, aid, goods_id, parent_id)

            template_utils.init_price_view(item_widget.temp_price, goods_id, color=mall_const.DARK_PRICE_COLOR)

            @item_widget.btn_buy.btn_common_big.callback()
            def OnClick(btn, touch):
                self.do_buy(parent_id, goods_id)

            @item_widget.btn_gifts.callback()
            def OnClick(btn, touch):
                self.do_buy(parent_id, goods_id)

            return

    def on_click_stage_reward(self, btn_box, achieve_id, goods_id, parent_id):

        @btn_box.callback()
        def OnClick(btn, touch):
            global_stat = global_data.player.get_gl_reward_receive_state(achieve_id)
            limite_buy = mall_utils.limite_pay(goods_id)
            simulate_latest_num = int(self._tick_now_num_map.get(parent_id, 0))
            cond_val = confmgr.get('global_achieve_data', str(achieve_id), 'iCondValue', default=0)
            if global_stat == ITEM_UNRECEIVED and limite_buy and simulate_latest_num >= cond_val:
                global_data.player.try_get_global_achieve(achieve_id)
            else:
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                child_conf = confmgr.get('global_achieve_data', str(achieve_id))
                reward_id = child_conf.get('iRewardID')
                reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)

    def update_gl_receive_state(self):
        list_gifts = self.panel.list_gifts
        for i, parent_id in enumerate(self._parent_achieve_id_lst):
            item_widget = list_gifts.GetItem(i)
            parent_id = self._parent_achieve_id_lst[i]
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            goods_id = self._gift_goods_lst[i]
            item_no = mall_utils.get_goods_item_no(goods_id)
            limite_buy = mall_utils.limite_pay(goods_id)
            open_date_range = mall_utils.get_goods_item_open_date(goods_id)
            opening, _ = mall_utils.check_limit_time_lottery_open_info(open_date_range)
            item_widget.btn_buy.btn_common_big.SetEnable(not limite_buy and opening)
            can_buy = not limite_buy and opening
            price_info = mall_utils.get_mall_item_price(goods_id)
            if price_info and price_info[0]['real_price'] != 0:
                if limite_buy:
                    item_widget.btn_buy.btn_common_big.SetText(80866)
                    item_widget.temp_price.setVisible(False)
                elif not opening:
                    item_widget.btn_buy.btn_common_big.SetText(81154)
                    item_widget.temp_price.setVisible(False)
                else:
                    item_widget.temp_price.setVisible(True)
                    item_widget.btn_buy.btn_common_big.SetText('')
            else:
                if not opening:
                    item_widget.btn_buy.btn_common_big.SetText(81154)
                else:
                    item_widget.btn_buy.btn_common_big.SetText(81025)
                item_widget.temp_price.setVisible(False)
                item_widget.red_point.setVisible(can_buy)
            for i, aid in enumerate(children_achieves):
                global_stat = global_data.player.get_gl_reward_receive_state(aid)
                temp_box = getattr(item_widget, 'temp_box_{}'.format(i + 1))
                temp_box.img_get.setVisible(False)
                temp_box.red_point.setVisible(False)
                simulate_latest_num = int(self._tick_now_num_map.get(parent_id, 0))
                cond_val = confmgr.get('global_achieve_data', str(aid), 'iCondValue', default=0)
                if global_stat == ITEM_UNRECEIVED and limite_buy and simulate_latest_num >= cond_val:
                    if not temp_box.IsPlayingAnimation('get_tips'):
                        temp_box.StopAnimation('get_tips')
                        temp_box.PlayAnimation('get_tips')
                    temp_box.red_point.setVisible(True)
                elif global_stat == ITEM_RECEIVED:
                    temp_box.StopAnimation('get_tips')
                    temp_box.img_get.setVisible(True)

    def up_tick_goal_num(self, *args):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            self.update_progress()
            return
        else:
            for i, parent_id in enumerate(self._parent_achieve_id_lst):
                children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
                achieve_name = confmgr.get('global_achieve_data', str(children_achieves[0]), 'cGStatName', default='')
                latest_num = int(global_stat_data.get(str(parent_id), {}).get(achieve_name, 0))
                cond_vals = [
                 0]
                for ca in children_achieves:
                    cond_vals.append(confmgr.get('global_achieve_data', str(ca), 'iCondValue', default=0))

                cond_ranges = [ [cond_vals[i], cond_vals[i + 1]] for i in range(len(cond_vals) - 1) ]
                stage = 0
                for i, val in enumerate(cond_vals):
                    if latest_num <= val:
                        stage = i
                        break

                stage -= 1
                if stage < 0:
                    stage = len(cond_ranges) - 1
                cur_range = cond_ranges[stage]
                range_val = cur_range[1] - cur_range[0]
                _tick_now_num = self._tick_now_num_map.get(parent_id, 0)
                if self._is_first_open:
                    if not global_data.player:
                        last_cache = 0 if 1 else global_data.player.get_simulate_cache(parent_id)
                        if last_cache >= latest_num:
                            last_cache = latest_num
                        else:
                            last_cache = random.uniform(max(last_cache, max(cur_range[0], latest_num - 0.1 * range_val)), latest_num)
                        _tick_now_num = last_cache
                    if self._tick_goal_num_map.get(parent_id, 0) == latest_num:
                        continue
                    self._tick_goal_num_map[parent_id] = latest_num
                    self._tick_now_num_map[parent_id] = min(latest_num, _tick_now_num)
                    self._second_tick_increase_num_map[parent_id] = int((latest_num - _tick_now_num) / self.SIMULATE_TIMES)

            self._is_first_open = False
            self.update_progress()
            return

    def second_simulate_up(self, *args):
        for i, parent_id in enumerate(self._parent_achieve_id_lst):
            _tick_goal_num = self._tick_goal_num_map.get(parent_id, None)
            _tick_now_num = self._tick_now_num_map.get(parent_id, None)
            if _tick_goal_num is None or _tick_now_num is None:
                continue
            _tick_now_num += self._second_tick_increase_num_map[parent_id]
            if _tick_now_num >= _tick_goal_num:
                _tick_now_num = _tick_goal_num
            self._tick_now_num_map[parent_id] = _tick_now_num
            self.update_progress()

        self.update_gl_receive_state()
        self._times += 1
        if self._times > self.INTERVAL_TIMES:
            self.up_tick_goal_num()
            self._times = 0
        return

    def update_progress(self):
        list_gifts = self.panel.list_gifts
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        global_stat_data = global_stat_data or {} if 1 else global_stat_data
        for i, parent_id in enumerate(self._parent_achieve_id_lst):
            item_widget = list_gifts.GetItem(i)
            parent_id = self._parent_achieve_id_lst[i]
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            achieve_name = confmgr.get('global_achieve_data', str(children_achieves[0]), 'cGStatName', default='')
            latest_num = global_stat_data.get(str(parent_id), {}).get(achieve_name, 0)
            simulate_latest_num = int(self._tick_now_num_map.get(parent_id, 0))
            item_widget.lab_num_total.SetString('{}'.format(simulate_latest_num))
            total_cond_value = confmgr.get('global_achieve_data', str(children_achieves[-1]), 'iCondValue', default=0)
            item_widget.progress_num.SetPercent(float(simulate_latest_num) / total_cond_value * 100.0)

        return