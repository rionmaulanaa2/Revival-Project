# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGoLottery.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils.activity_utils import is_activity_in_limit_time
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, get_pc_charge_price_str, adjust_price, is_steam_pay, get_charge_price_str, adjust_price_decimal2
from common.cfg import confmgr
from logic.gutils.task_utils import get_task_conf_by_id, has_unreceived_prog_reward, get_total_prog
from logic.gutils.jump_to_ui_utils import jump_to_web_charge
from logic.client.const import mall_const
from logic.gcommon import time_utility
from logic.gutils import mall_utils
from logic.gcommon.cdata import loop_activity_data
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityGoLottery(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGoLottery, self).__init__(dlg, activity_type)
        self.widget_map = {}
        self._idx_to_item = []
        self._item_to_idx = {}

    def on_init_panel(self):
        self.init_parameters()
        self._init_reward_items()
        self._init_turntable_widget()
        self._init_countdown_widget()
        self._set_question_info()
        self._init_btn_text()
        self._refresh_buy_btn()
        self.process_events(True)

    def on_finalize_panel(self):
        self.process_events(False)
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        super(ActivityGoLottery, self).on_finalize_panel()
        return

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._login_task_id = ui_data.get('login_task_id', '')
        self._goods_id = ui_data.get('goods_id', '')
        self.goods_list_name = ui_data.get('jelly_goods', '')
        self._goods_list = getattr(mall_const, self.goods_list_name)
        if not self._goods_list:
            log_error('!!!!ActivityGoLottery: Goods list name invalid!!!!')
        self._jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(self._goods_list)
        if loop_activity_data.is_loop_activity(self._activity_type):
            _, end_time = loop_activity_data.get_loop_activity_open_time(self._activity_type)
        else:
            end_time = conf['cEndTime']
        self._remind_day_no = time_utility.get_rela_day_no(end_time)
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        if global_data.lobby_mall_data and global_data.player:
            self.goods_info = global_data.lobby_mall_data.get_activity_sale_info(self.goods_list_name)
            if self.goods_info:
                key = self.goods_info['goodsid']
                goods_id = global_data.player.get_goods_info(key).get('cShopGoodsId')
                if goods_id:
                    self._goods_id = goods_id

    def process_events(self, is_bind):
        e_conf = {'task_prog_changed': self._on_update_reward,
           'buy_good_success': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'receive_award_succ_event': self._on_receive_reward
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _on_update_reward(self, *args):
        self._refresh_buy_btn()

    def _init_btn_text(self):
        txt_buy = self.panel.nd_content.btn_click.img_type
        if not self.goods_info:
            txt_buy.SetString('******')
            return
        if self.is_pc_global_pay or is_steam_pay():
            price_txt = get_pc_charge_price_str(self.goods_info)
        else:
            price_txt = get_charge_price_str(self.goods_info['goodsid'])
        txt_buy.SetString(adjust_price_decimal2(str(price_txt)))
        if G_IS_NA_PROJECT:
            self.panel.nd_content.bar_tips._nameless_children[0].SetString(634404)
        else:
            self.panel.nd_content.bar_tips._nameless_children[0].SetString(611342)

    def _refresh_buy_btn(self):
        has_bought = limite_pay(self._goods_id)
        self.panel.img_type.setVisible(False)
        self.panel.img_type2.setVisible(False)
        self.panel.img_type3.setVisible(False)
        self.panel.bar_tips.setVisible(False)
        self.panel.bar_tips2.setVisible(False)
        if not has_bought:
            self.panel.img_type.setVisible(True)
            self.panel.btn_click.SetEnable(True)
            self.panel.bar_tips.setVisible(True)

            @self.panel.btn_click.unique_callback()
            def OnClick(btn, touch):
                if loop_activity_data.is_loop_activity(self._activity_type):
                    if not loop_activity_data.is_loop_activity_open(self._activity_type):
                        global_data.game_mgr.show_tip(607911)
                        return
                elif not is_activity_in_limit_time(self._activity_type):
                    global_data.game_mgr.show_tip(607911)
                    return
                has_bought = limite_pay(self._goods_id)
                if has_bought:
                    return

                def buy():
                    if is_pc_global_pay():
                        jump_to_web_charge()
                    elif self._jelly_goods_info:
                        global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

                cur_day_no = time_utility.get_rela_day_no()
                left_day = self._remind_day_no - cur_day_no + 1
                if left_day < 7:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    sec_confirm_dlg = SecondConfirmDlg2()
                    content = get_text_by_id(611344).format(left_day)
                    sec_confirm_dlg.confirm(content=content, confirm_callback=buy)
                else:
                    buy()

        elif has_unreceived_prog_reward(self._login_task_id):
            self.panel.img_type2.setVisible(True)
            self.panel.btn_click.SetEnable(True)

            @self.panel.btn_click.unique_callback()
            def OnClick(btn, touch):
                if global_data.player and global_data.player.is_matching or global_data.player.get_battle():
                    global_data.game_mgr.show_tip(get_text_by_id(12097))
                    return
                global_data.player.receive_all_task_prog_reward(self._login_task_id)
                self.widget_map['turntable'].start_turn_animation()
                self.panel.PlayAnimation('btn_once_click')

        else:
            self.panel.img_type3.setVisible(True)
            self.panel.btn_click.SetEnable(False)
            self.panel.bar_tips2.setVisible(True)
            cur_prog = global_data.player.get_task_prog(self._login_task_id)
            max_prog = get_total_prog(self._login_task_id)
            left_times = max_prog - cur_prog
            if left_times <= 0:
                self.panel.lab_tips.SetString(611345)
            else:
                self.panel.lab_tips.SetString(get_text_by_id(611343).format(left_times))
        cur_prog = global_data.player.get_task_prog(self._login_task_id)
        self.panel.temp_item_7.lab_day.SetString('DAY%d' % max(cur_prog, 1))
        global_data.emgr.refresh_activity_redpoint.emit()

    def _set_question_info(self):

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            conf = confmgr.get('c_activity_config', self._activity_type, default={})
            title_text_id = int(conf.get('cNameTextID', 1))
            desc_text_id = int(conf.get('cRuleTextID', 1))
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            if loop_activity_data.is_loop_activity(self._activity_type):
                act_start, act_end = loop_activity_data.get_loop_activity_open_time(self._activity_type)
                act_start_str = time_utility.get_time_string('%Y.%m.%d', act_start)
                act_end_str = time_utility.get_time_string('%Y.%m.%d', act_end)
                time_str = '{}-{}'.format(act_start_str, act_end_str)
                rule_text = get_text_by_id(desc_text_id).format(time_str)
            else:
                rule_text = desc_text_id
            dlg.set_show_rule(title_text_id, rule_text)

    def set_show(self, show, is_init=False):
        super(ActivityGoLottery, self).set_show(show, is_init)
        if show:
            self.panel.PlayAnimation('show')

    def _init_reward_items(self):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN
        from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_pic_by_item_no
        task_conf = get_task_conf_by_id(self._login_task_id)
        reward_id = task_conf.get('prog_rewards', [])[0][1]
        exclude_type = (L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN)
        reward_items = confmgr.get('preview_%s' % reward_id, 'turntable_goods_info', default=())
        skin_items = []
        for item_id, item_num in reward_items:
            item_id = int(item_id)
            if get_lobby_item_type(item_id) in exclude_type:
                skin_items.append(item_id)
                continue
            idx = len(self._idx_to_item)
            self._idx_to_item.append(item_id)
            self._item_to_idx[item_id] = idx
            item_widget = getattr(self.panel, 'temp_item_%d' % (idx + 1))
            pic_path = get_lobby_item_pic_by_item_no(item_id)
            item_widget.img_reward.SetDisplayFrameByPath('', pic_path)
            item_widget.lab_num.SetString('x%d' % item_num)

            @item_widget.nd_click.callback()
            def OnClick(btn, touch, item_id=item_id, item_num=item_num):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, item_num=item_num)
                return

        @self.panel.temp_item_7.nd_click.callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.ItemPreviewUI import ItemPreviewUI
            ItemPreviewUI(None, title=611312, item_list=skin_items)
            return

    def _init_turntable_widget(self):
        from logic.comsys.activity.widget.TurntableWidget import TurntableWidget
        ext_conf = {'order_item': [ getattr(self.panel, 'temp_item_%d' % (i + 1)) for i in range(6) ],'reward_reason': 'ALL_TASK_PROG_REWARD-' + self._login_task_id
           }
        self.widget_map['turntable'] = TurntableWidget(self.panel, self._activity_type, ext_conf)

    def _on_receive_reward(self, items, chips=None, reason=None):
        if reason != 'ALL_TASK_PROG_REWARD-' + self._login_task_id:
            return
        else:
            item_key = int(six_ex.keys(items)[0])
            idx = self._item_to_idx.get(item_key)
            node_name = 'temp_item_7' if idx is None else 'temp_item_%d' % (idx + 1)
            item_widget = getattr(self.panel, node_name)
            self.widget_map['turntable'].set_final_item(idx, item_widget)
            return

    def _init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type, {'completion': True})