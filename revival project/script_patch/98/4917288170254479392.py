# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520MarksmanExchange.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
import cc
ACTIVITY520_ITEM_NO = 50600028

class Activity520MarksmanExchange(ActivityExchange):

    def __init__(self, dlg, activity_type):
        super(Activity520MarksmanExchange, self).__init__(dlg, activity_type)
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            self.ITEM_ID_LST = [
             50700023, 208105414, 50101101]
            self.panel.btn_mila.setVisible(True)
            self.loop_ani = 'loop'
            self.show_ani = 'show'
        else:
            self.ITEM_ID_LST = [
             208105414, 50101101, 50920103]
            self.panel.btn_mila.setVisible(False)
            self.loop_ani = 'loop_na'
            self.show_ani = 'show_na'
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        sub_act_list = self.panel.act_list
        sub_act_list.SetTemplate(self.get_task_list_template())
        from logic.gcommon.common_const.lang_data import LANG_ZHTW, LANG_CN
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        self.panel.nd_dart.setVisible(get_cur_text_lang() in [LANG_CN, LANG_ZHTW])
        return

    def on_finalize_panel(self):
        super(Activity520MarksmanExchange, self).on_finalize_panel()
        self.sub_widget = None
        return

    def init_items(self):
        from logic.gutils.item_utils import get_lobby_item_name
        for idx in range(len(self.ITEM_ID_LST)):
            name_node = getattr(self.panel, 'lab_name_%s' % (idx + 1))
            name_node.SetString(get_lobby_item_name(self.ITEM_ID_LST[idx], need_part_name=False))
            name_btn = getattr(self.panel, 'btn_click_%s' % (idx + 1))
            img_node = getattr(self.panel, 'img_item_%s' % (idx + 1))
            from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
            img_node and img_node.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(self.ITEM_ID_LST[idx]))

            @name_btn.unique_callback()
            def OnClick(btn, touch, item_id=self.ITEM_ID_LST[idx]):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
                return

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        else:
            self._timer_cb[0] = lambda : self.refresh_time(None)
            self.refresh_time(None)
            self.show_list()
            self.refresh_item_num()

            @self.panel.btn_mila.unique_callback()
            def OnClick(btn, touch):
                from logic.gutils import jump_to_ui_utils
                from logic.gcommon.common_const.activity_const import ACTIVITY_520_PRINCESS
                jump_to_ui_utils.jump_to_activity(ACTIVITY_520_PRINCESS)

            @self.panel.btn_question.unique_callback()
            def OnClick(btn, touch, *args):
                desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
                from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
                dlg = GameRuleDescUI()
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

            global_data.player.call_server_method('attend_activity', (self._activity_type,))
            return

    def init_parameters(self):
        super(Activity520MarksmanExchange, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def get_task_list_template(self):
        return 'activity/activity_202105/520/i_task_exchange_marksman'

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(Activity520MarksmanExchange, self).set_show(show, is_init)
        if self.cur_tab_name_id == self.last_tab_name_id:
            if not self.panel.IsPlayingAnimation(self.loop_ani):
                show and self.panel.PlayAnimation(self.loop_ani)
            return
        self.panel.stopAllActions()
        self.panel.StopAnimation(self.show_ani)
        self.panel.StopAnimation(self.loop_ani)
        if show:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(self.show_ani)),
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime(self.show_ani)),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation(self.loop_ani))]))
            if self.sub_widget and self.sub_widget.panel:
                self.sub_widget.panel.PlayAnimation(self.show_ani)

    def refresh_item_num(self):
        item_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(ACTIVITY520_ITEM_NO)
        self.panel.lab_num.SetString(str(item_num))

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                continue
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                continue
            prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
            if not prices:
                continue
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            cost_item_num = price_info.get('real_price')
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                limit_left_num = left_num
                item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            cost_item_amount = global_data.player.get_item_num_by_no(int(cost_item_no))
            if cost_item_amount >= cost_item_num:
                cost_str = '#DB{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            else:
                cost_str = '#SR{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            item_widget.temp_fragment.lab_quantity.setVisible(True)
            item_widget.temp_fragment.lab_quantity.SetString(cost_str)
            exchange_lv = extra_params.get('exchange_lv', None)
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(btn=btn, left_num=left_num, max_num=max_num):
                if limit_left_num <= 0:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                    return
                btn.setVisible(True)
                item_widget.nd_get.setVisible(False)
                enable = left_num > 0 and mall_utils.check_item_money(cost_item_no, cost_item_num, pay_tip=False)
                btn.SetEnable(enable)

            @btn.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id, goods_payment=goods_payment, left_num=left_num, ex_lv=exchange_lv):
                from logic.comsys.mall_ui import BuyConfirmUIInterface
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                else:
                    if ex_lv is not None and global_data.player.get_lv() < ex_lv:
                        item_name = mall_utils.get_goods_name(goods_id)
                        global_data.game_mgr.show_tip(get_text_by_id(608422).format(item=item_name))
                        return
                    if left_num > 1:
                        BuyConfirmUIInterface.groceries_buy_confirmUI(goods_id)
                    else:
                        global_data.player.buy_goods(goods_id, 1, goods_payment)
                    return

            check_btn()

        self.refresh_item_num()
        return

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def transfer_panel_out(self):
        return self.panel