# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/christmas/ChristmasParty2.py
from __future__ import absolute_import
from six.moves import range
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
import logic.gcommon.const as gconst
from cocosui import cc
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.const import SHOP_ITEM_YUANBAO

class ChristmasParty2(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_201912/christmas_mila'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    NEED_GAUSSIAN_BLUR = True
    UI_ACTION_EVENT = {'nd_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected',
       'on_lobby_bag_item_changed_event': 'refresh_item_num',
       'receive_task_reward_succ_event': 'refresh_task_progress',
       'buy_good_success': 'refresh_item_num'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self._tab_panels = {}
        self._cur_index = None
        self._activity_type = '103'
        self._init_task_flag = False
        self._children_tasks = None
        self.hide_main_ui()
        self.panel.PlayAnimation('appear')
        self.init_item_widget()
        self.init_tab()
        return

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('GameRuleDescUI')
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if ui:
            ui.refresh_christmas_red()

    def do_show_panel(self):
        super(ChristmasParty2, self).do_show_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def do_hide_panel(self):
        super(ChristmasParty2, self).do_hide_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def _on_login_reconnected(self, *args):
        self.close()

    def init_item_widget(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        from logic.gcommon.time_utility import get_server_time, ONE_DAY_SECONDS
        now = get_server_time()
        task_conf = task_utils.get_task_conf_by_id(parent_task)
        left_time = int(max(task_conf.get('end_time', now) - now, 0))
        template_utils.show_left_time(self.panel.nd_title.lab_details, left_time, get_text_by_id(607160) + '      ')
        act_name_id = conf['cNameTextID']
        btn_check = self.panel.btn_check

        @btn_check.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn_check.GetPosition()
            wpos = btn_check.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_item()
        self._children_tasks = task_utils.get_children_task(parent_task)
        self.init_small_exchange()

    def on_create_small_exchange(self, ist_item, index, item_widget):
        if self._children_tasks is None:
            return
        else:
            btn = item_widget.temp_btn_get.btn_common
            task_id = self._children_tasks[index + 5]
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid'))
            mall_conf = confmgr.get('mall_config', goods_id, default={})
            exchange_item_no = mall_conf['item_no']

            @btn.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id):
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    global_data.game_mgr.show_tip(get_text_by_id(607175))
                    return
                price_list = mall_utils.get_mall_item_price_list(goods_id)
                item_consumed_count = len(price_list)
                item_consumed_count /= 2
                for i in range(item_consumed_count):
                    item_no = price_list[i * 2]
                    if item_no == SHOP_ITEM_YUANBAO:
                        from logic.gutils.mall_utils import check_yuanbao
                        if not check_yuanbao(price_list[i * 2 + 1]):
                            return

                for i in range(item_consumed_count):
                    item_no = price_list[i * 2]
                    if item_no != SHOP_ITEM_YUANBAO:
                        num = global_data.player.get_item_money(item_no)
                        if num < price_list[i * 2 + 1]:
                            global_data.game_mgr.show_tip(get_text_by_id(607180))
                            return

                left_num = 0
                _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
                if num_info:
                    left_num, _ = num_info
                from logic.comsys.mall_ui import BuyConfirmUIInterface
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                if left_num > 1:
                    BuyConfirmUIInterface.groceries_buy_confirmUI(goods_id)
                else:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    dlg = SecondConfirmDlg2()

                    def on_confirm():
                        dlg.close()
                        global_data.player.buy_goods(goods_id, 1, gconst.SHOP_PAYMENT_ITEM)

                    name = get_lobby_item_name(exchange_item_no)
                    c = get_text_by_id(12115).format(item=name)
                    dlg.confirm(content=c, confirm_callback=on_confirm)

            do_remind = [
             global_data.player.has_exchange_reminder(goods_id)]

            @item_widget.btn_tick.unique_callback()
            def OnClick(btn, touch, do_remind=do_remind, goods_id=goods_id):
                do_remind[0] = not do_remind[0]
                btn.SetSelect(do_remind[0])
                global_data.player.add_exchange_reminder(goods_id, do_remind[0])
                self.refresh_small_exchange_red()

            item_widget.btn_tick.SetSelect(do_remind[0])
            self.show_small_exchange(index, item_widget)
            return

    def small_exchange_red(self):
        return activity_utils.get_can_mulit_exchange_count_by_task('1301000')

    def refresh_small_exchange_red(self):
        if not self._tab_panels:
            return
        if self.small_exchange_red():
            self._tab_panels[0].btn_top.img_red.setVisible(True)
        else:
            self._tab_panels[0].btn_top.img_red.setVisible(False)

    def init_small_exchange(self):
        if self._children_tasks is None:
            return
        else:
            nd_list = self.panel.nd_list.list_exchange
            nd_list.BindMethod('OnCreateItem', self.on_create_small_exchange)
            nd_list.SetInitCount(9)
            return

    def init_small_task(self):
        if self._children_tasks is None:
            return
        else:
            nd_list = self.panel.nd_list.list_task
            nd_list.SetInitCount(5)
            for i in range(5):
                item_widget = nd_list.GetItem(i)
                task_id = self._children_tasks[i]
                btn = item_widget.temp_btn_get.btn_common

                @btn.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    if not activity_utils.is_activity_in_limit_time(self._activity_type):
                        return
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            self.show_small_task()
            return

    def show_small_exchange(self, index, item_widget):
        if self._children_tasks is None:
            return
        else:
            task_id = self._children_tasks[index + 5]
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid'))
            price_list = mall_utils.get_mall_item_price_list(goods_id)
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            if len(price_list) == 4:
                item_widget.lab_1.SetString('+')
                item_widget.lab_2.setVisible(True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_1, price_list[0], show_tips=True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_2, price_list[2], show_tips=True)
                cost_str = '{0}'.format(price_list[1])
                item_widget.temp_reward_1.lab_quantity.setVisible(True)
                item_widget.temp_reward_1.lab_quantity.SetString(cost_str)
                cost_str = '{0}'.format(price_list[3])
                item_widget.temp_reward_2.lab_quantity.setVisible(True)
                item_widget.temp_reward_2.lab_quantity.SetString(cost_str)
                item_widget.temp_reward_3.setVisible(True)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_3, target_item_no, target_item_num, show_tips=True)
            else:
                item_widget.lab_1.SetString('=')
                item_widget.lab_2.setVisible(False)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_1, price_list[0], show_tips=True)
                cost_str = '{0}'.format(price_list[1])
                item_widget.temp_reward_1.lab_quantity.setVisible(True)
                item_widget.temp_reward_1.lab_quantity.SetString(cost_str)
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward_2, target_item_no, target_item_num, show_tips=True)
                item_widget.temp_reward_3.setVisible(False)
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                limit_left_num = left_num
                item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(btn=btn, left_num=left_num):
                if limit_left_num <= 0:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                    return
                btn.setVisible(True)
                item_widget.nd_get.setVisible(False)
                enable = left_num > 0
                btn.SetEnable(enable)

            check_btn()
            return

    def show_small_task(self):
        nd_list = self.panel.nd_list.list_task
        for i in range(5):
            item_widget = nd_list.GetItem(i)
            task_id = self._children_tasks[i]
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times > 0:
                item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
            else:
                item_widget.lab_num.SetString('')
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        btn.SetText(text_id)
                        btn.SetEnable(True)
                    else:
                        btn.SetEnable(False)
                else:
                    btn.setVisible(True)
                    btn.SetEnable(True)

            check_btn()

    def small_task_red(self):
        return task_utils.has_christmas_task_reward()

    def refresh_small_task_red(self):
        if not self._tab_panels:
            return
        if self.small_task_red():
            self._tab_panels[1].btn_top.img_red.setVisible(True)
        else:
            self._tab_panels[1].btn_top.img_red.setVisible(False)

    def init_tab(self):
        list_tab = self.panel.nd_tab.pnl_list_tab
        list_tab.DeleteAllSubItem()
        for i in range(2):
            panel = list_tab.AddTemplateItem()
            if i == 0:
                panel.lab.SetString(get_text_by_id(12074))
            else:
                panel.lab.SetString(get_text_by_id(80841))
            self._tab_panels[i] = panel

            @panel.btn_top.callback()
            def OnClick(btn, touch, index=i):
                self.touch_tab_by_index(index)

        self.touch_tab_by_index(0)
        self.refresh_small_exchange_red()
        self.refresh_small_task_red()

    def touch_tab_by_index(self, index):
        if self._cur_index == index:
            return
        self._cur_index = index
        if index == 0:
            self.panel.nd_list.list_exchange.setVisible(True)
            self.panel.nd_list.list_task.setVisible(False)
            self._tab_panels[0].btn_top.SetSelect(True)
            self._tab_panels[1].btn_top.SetSelect(False)
        else:
            if not self._init_task_flag:
                self._init_task_flag = True
                self.init_small_task()
            self.panel.nd_list.list_exchange.setVisible(False)
            self.panel.nd_list.list_task.setVisible(True)
            self._tab_panels[0].btn_top.SetSelect(False)
            self._tab_panels[1].btn_top.SetSelect(True)

    def refresh_item_num(self, *_):
        self.show_item()
        nd_list = self.panel.nd_list.list_exchange
        all_items = nd_list.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.show_small_exchange(index, widget)

        self.refresh_small_exchange_red()

    def refresh_task_progress(self, *_):
        if not self._init_task_flag:
            return
        self.show_small_task()
        self.refresh_small_task_red()

    def enter_screen(self):
        super(ChristmasParty2, self).enter_screen()
        nd_list = self.panel.nd_list.list_exchange
        all_items = nd_list.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.show_small_exchange(index, widget)

    def show_item(self):
        num = global_data.player.get_item_num_by_no(50600017)
        self.panel.nd_own.lab_own.SetString(get_text_by_id(607161).format(str(num)))