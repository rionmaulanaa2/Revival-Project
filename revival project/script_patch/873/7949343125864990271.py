# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySmallBp.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import activity_utils
from logic.gutils.item_utils import get_lobby_item_type
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item import lobby_item_type
from logic.gcommon.cdata import secret_order_conf
from logic.gcommon.common_const.battlepass_const import ROTATE_FACTOR
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.battle_pass.BattlePassDisplayWidget import BattlePassDisplayWidget
from logic.client.const.lobby_model_display_const import SMALL_BP_SCENE_1
LEVEL_BUY_WIDGET = 'activity/activity_new_domestic/i_bp_level_up'
LOW_SP_TYPE = '1'
HIGH_SP_TYPE = '2'

class ActivitySmallBp(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySmallBp, self).__init__(dlg, activity_type)
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)
        self._now_lv = 1
        self._last_lv = None
        self._period = 1
        self._max_level = 8
        self._jelly_goods_info = None
        self._core_reward_item_no = None
        self._has_reward = False
        self._display_type = SMALL_BP_SCENE_1
        self._lv_to_item = {}
        if global_data.lobby_mall_data and global_data.player:
            self._jelly_goods_info = global_data.lobby_mall_data.get_small_bp_sale_info()
        self._update_params()
        self._init_fixed_panel()
        self._init_event()
        return

    def _update_params(self):
        self._max_level = len(secret_order_conf.lv_reward_data)
        self._now_lv = global_data.player or 1 if 1 else global_data.player.secretorder_lv
        self._period = global_data.player or 1 if 1 else global_data.player.secretorder_period
        self._has_reward = activity_utils.small_bp_has_unreceived_reward()
        core_reward_id = secret_order_conf.get_core_reward_id(self._period)
        core_reward_lst = self._get_reward_detail_info(core_reward_id)
        self._display_type = secret_order_conf.get_display_type(self._period)
        if core_reward_lst:
            self._core_reward_item_no = core_reward_lst[1][0]
        else:
            self._core_reward_item_no = None
        self._display_core_widget()
        return

    def _init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        event_mgr = global_data.emgr
        e_event = {'small_bp_update_lv': self._small_bp_lv_up,
           'small_bp_open_type': self._small_bp_buy_card,
           'small_bp_update_award': self._small_bp_receive_award,
           'small_bp_new_period_start': self._small_bp_period_start
           }
        if is_bind:
            event_mgr.bind_events(e_event)
        else:
            event_mgr.unbind_events(e_event)

    def refresh_panel(self):
        if self.panel.IsVisible():
            self._display_core_widget(True)

    def set_show(self, show, is_init=False):
        super(ActivitySmallBp, self).set_show(show, is_init)
        if show:
            self._display_core_widget()
            self.panel.PlayAnimation('show1')
            self.panel.PlayAnimation('loop')
            self._update_time()

    def _update_time(self):
        from logic.gcommon.time_utility import get_server_time
        end_time = secret_order_conf.get_end_ts(self._period)
        from logic.gutils.template_utils import get_left_info
        is_ending, left_text, left_num, left_unit = get_left_info(end_time - get_server_time())
        if is_ending:
            self.panel.lab_time.SetString(get_text_by_id(607613).format(self._period))
        else:
            self.panel.lab_time.SetString(get_text_by_id(607612).format(self._period) + str(left_num) + get_text_by_id(left_unit))

    def _display_core_widget(self, reset_display=False):
        from logic.gcommon.common_const.scene_const import SCENE_JIEMIAN_COMMON
        from logic.gcommon.common_const.scene_const import SCENE_SMALL_BP
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, None, scene_content_type=SCENE_SMALL_BP)
        self._display_widget.set_display_type(self._display_type, reset_display)
        if not self._core_reward_item_no:
            self._display_widget.clear_model_display()
            return
        else:
            item_type = get_lobby_item_type(self._core_reward_item_no)
            is_head_type = item_type == lobby_item_type.L_ITEM_TYPE_HEAD
            self._display_widget.display_award(self._core_reward_item_no, show_conf_model=is_head_type)
            return

    def need_bg(self):
        return False

    def on_init_panel(self):
        self._init_reward_list()
        self._update_btn_buy_state()

    def _update_btn_buy_state(self):
        if self._has_buy_card():
            self.panel.btn_buy.setVisible(False)
            self.panel.btn_sign.setVisible(True)
            if activity_utils.small_bp_has_unreceived_reward():

                @self.panel.btn_sign.btn.unique_callback()
                def OnClick(btn, touch):
                    if global_data.player and self._has_reward:
                        global_data.player.receive_small_bp_reward()

                self.panel.btn_sign.lab_btn_sign.SetString(80834)
                self.panel.btn_sign.btn.SetEnable(True)
            else:
                text_id = 604029 if self._now_lv == self._max_level else 606046
                self.panel.btn_sign.lab_btn_sign.SetString(text_id)
                self.panel.btn_sign.btn.SetEnable(False)
        else:
            self.panel.btn_buy.setVisible(True)
            self.panel.btn_sign.setVisible(False)
            if not self._jelly_goods_info:
                self.panel.btn_buy.lab_btn.SetString('')
                self.panel.btn_buy.btn.SetEnable(False)
            else:
                if mall_utils.is_pc_global_pay() or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(self._jelly_goods_info)
                    price_val = self._jelly_goods_info.get('price')
                else:
                    key = self._jelly_goods_info['goodsid']
                    price_txt = mall_utils.get_charge_price_str(key)
                    price_val = mall_utils.get_charge_price_val(key)
                adjusted_price = mall_utils.adjust_price(str(price_txt))
                self.panel.btn_buy.lab_btn.SetString(get_text_by_id(607607))
                origin_price_val = ''
                try:
                    price_val_str = str(price_val)
                    price_val_str = price_val_str.replace(',', '')
                    start_index = 0
                    for i, ch in enumerate(price_val_str):
                        start_index = i
                        if ch.isdigit():
                            break

                    price_val_str = price_val_str[start_index:]
                    origin_price_val = int(eval(str(price_val_str)) / 0.3)
                except:
                    origin_price_val = ''
                    log_error('ActivitySmallBp - calculate origin price val fail - price_val:', price_val)

                self.panel.btn_buy.lab_price_common.lab_price.SetString(adjusted_price)
                self.panel.btn_buy.lab_price_common.lab_price_before.SetString(str(origin_price_val))
                self.panel.btn_buy.btn.SetEnable(True)

                @self.panel.btn_buy.btn.unique_callback()
                def OnClick(btn, touch):
                    if mall_utils.is_pc_global_pay():
                        from logic.gutils.jump_to_ui_utils import jump_to_web_charge
                        jump_to_web_charge()
                    else:
                        global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

    def on_finalize_panel(self):
        self.process_event(False)
        if self._display_widget:
            self._display_widget.destroy()
            self._display_widget = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        return

    def _display_cb(self, is_model, item_no):
        drag_enable = True if is_model else False
        self.panel.nd_items_touch.setVisible(drag_enable)

    def _init_reward_list(self):
        v_lst = self.panel.list_items

        def on_create_callback(lv, idx, item):
            real_lv = idx + 1
            self._lv_to_item[real_lv] = item
            item.lab_level.SetString(get_text_by_id(604004).format(str(real_lv)))
            show_price = secret_order_conf.get_lv_show_price(real_lv)
            if show_price:
                item.lab_price.setVisible(True)
                text_str = '<img="gui/ui_res_2/icon/icon_crystal.png", scale=0.0>{0}'.format(str(show_price))
                item.lab_price.lab_money.SetString(text_str)
            else:
                item.lab_price.setVisible(False)
            list_item = [
             item.temp_item1, item.temp_item2, item.temp_item3]
            low_reward_id, high_reward_id = secret_order_conf.get_secretorder_reward(self._period, real_lv)
            low_reward_info = self._get_reward_detail_info(low_reward_id)
            high_reward_info = self._get_reward_detail_info(high_reward_id)
            list_award_info = [
             (
              None if len(low_reward_info) < 1 else low_reward_info[0], LOW_SP_TYPE),
             (
              None if len(high_reward_info) < 1 else high_reward_info[0], HIGH_SP_TYPE),
             (
              None if len(high_reward_info) < 2 else high_reward_info[1], HIGH_SP_TYPE)]
            for idx, sub_item in enumerate(list_item):
                reward_item_info, sp_type = list_award_info[idx]
                if reward_item_info:
                    item_no, item_num = reward_item_info
                    init_tempate_mall_i_item(sub_item, item_no, item_num=item_num)

                    @sub_item.btn_choose.unique_callback()
                    def OnClick(btn, touch, parent_class=self, cb_sp_lv=real_lv, cb_sp_type=sp_type, cb_item_no=item_no, cb_item_num=item_num):
                        is_lock_lv = parent_class._is_locked(cb_sp_lv, cb_sp_type)
                        is_received = parent_class._is_received(cb_sp_lv, cb_sp_type)
                        if not (is_received or is_lock_lv):
                            if global_data.player:
                                global_data.player.receive_small_bp_reward_with_type(cb_sp_lv, cb_sp_type)
                        else:
                            x, y = btn.GetPosition()
                            w, h = btn.GetContentSize()
                            x += w * 0.5
                            w_pos = btn.ConvertToWorldSpace(x, y)
                            extra_info = {'show_jump': True}
                            global_data.emgr.show_item_desc_ui_event.emit(cb_item_no, None, w_pos, extra_info=extra_info, item_num=cb_item_num)
                        return

                else:
                    sub_item.setVisible(False)

            self._set_lv_item_state(real_lv)
            return

        v_lst.BindMethod('OnCreateItem', on_create_callback)
        v_lst.DeleteAllSubItem()
        v_lst.SetInitCount(self._max_level - 1)
        on_create_callback(None, 7, self.panel.temp_last_item)
        return

    def _set_lv_item_state(self, lv):
        item = self._lv_to_item.get(lv, None)
        if item is None:
            return
        else:
            item.img_choose.setVisible(lv == self._now_lv)
            item.nd_lock.setVisible(not self._has_buy_card())
            for sp_type in (LOW_SP_TYPE, HIGH_SP_TYPE):
                is_received = self._is_received(lv, sp_type)
                is_lock_lv = self._is_locked(lv, sp_type)
                mall_items = ()
                if sp_type == LOW_SP_TYPE:
                    mall_items = (
                     item.temp_item1,)
                elif sp_type == HIGH_SP_TYPE:
                    mall_items = (
                     item.temp_item2, item.temp_item3)
                for mall_item in mall_items:
                    if mall_item:
                        mall_item.nd_lock.setVisible(is_lock_lv)
                        mall_item.nd_get.setVisible(is_received)
                        if not is_received and not is_lock_lv:
                            mall_item.PlayAnimation('get_tips')
                        else:
                            mall_item.StopAnimation('get_tips')
                            mall_item.nd_get_tips.setVisible(False)

            return

    def _get_reward_detail_info(self, reward_id):
        if not reward_id:
            return []
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        if reward_conf:
            return reward_conf.get('reward_list', [])
        return []

    def _is_locked(self, lv, sp_type):
        is_lock_lv = True if lv > self._now_lv else False
        if sp_type == LOW_SP_TYPE:
            has_owned = True
        else:
            has_owned = self._has_buy_card()
        return is_lock_lv or not is_lock_lv and not has_owned

    def _is_received(self, lv, sp_type):
        reward_record = global_data.player or None if 1 else global_data.player.secretorder_reward_record.get(str(sp_type), None)
        if reward_record is None:
            return False
        else:
            return reward_record.is_record(lv)

    def _has_buy_card(self):
        if not global_data.player:
            return False
        return global_data.player.has_buy_higher_small_bp() > 0

    def _init_fixed_panel(self):

        @self.panel.btn_question.unique_callback()
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(607605), get_text_by_id(607610))

        if self._core_reward_item_no:
            from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
            self.panel.lab_item_name.setVisible(True)
            self.panel.temp_kind.setVisible(True)
            self.panel.lab_item_name.SetString(get_lobby_item_name(self._core_reward_item_no))
            from logic.gutils.item_utils import check_skin_tag
            check_skin_tag(self.panel.temp_kind, self._core_reward_item_no)
        else:
            self.panel.lab_item_name.setVisible(False)
            self.panel.temp_kind.setVisible(False)

        @self.panel.nd_items_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.panel.nd_items_touch.setVisible(False)

        @self.panel.btn_go.btn_common.unique_callback()
        def OnClick(btn, touch):
            if self._core_reward_item_no:
                from logic.gutils.item_utils import jump_to_ui_new
                jump_to_ui_new(self._core_reward_item_no)

    def _small_bp_receive_award(self, *args):
        self._update_btn_buy_state()
        self._update_exist_item()

    def _small_bp_lv_up(self, *args):
        self._now_lv = global_data.player or 1 if 1 else global_data.player.secretorder_lv
        self._update_btn_buy_state()
        self._update_exist_item(False)

    def _small_bp_buy_card(self, *args):
        self._update_exist_item()
        self._update_btn_buy_state()

    def _update_exist_item(self, need_fresh_red=True):
        for real_lv in self._lv_to_item:
            self._set_lv_item_state(real_lv)

        self._update_can_received_num(need_fresh_red)

    def _update_can_received_num(self, need_fresh_red=True):
        self._has_reward = activity_utils.small_bp_has_unreceived_reward()
        if need_fresh_red:
            global_data.emgr.refresh_activity_redpoint.emit()

    def _small_bp_period_start(self):
        if not global_data.player or global_data.player.secretorder_period == 0:
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2

            def close_activity_ui(*args):
                global_data.ui_mgr.close_ui('ActivityPayMainUI')

            NormalConfirmUI2(content=get_text_by_id(607614), on_confirm=close_activity_ui)
            return
        self._update_params()
        self._update_time()
        self._init_fixed_panel()
        self.on_init_panel()
        self._display_core_widget()
        self._update_can_received_num()
        self.panel.PlayAnimation('show1')
        self.panel.PlayAnimation('loop')