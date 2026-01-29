# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/ActivityNewReturnDiscount.py
from __future__ import absolute_import
import six
from six.moves import range
import cc
import math
from common.cfg import confmgr
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_name, get_skin_rare_degree_icon, can_jump_to_ui, jump_to_ui, jump_to_ui_new
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_GIFTPACKAGE
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gutils.trigger_gift_utils import get_discount_text_with_lang
from logic.gcommon.time_utility import get_server_time
from logic.comsys.activity.ActivityTemplate import ActivityBase
GOODS_ID_RETURN_TICKETS_BOX = '700100033'

class ActivityNewReturnDiscount(ActivityBase):
    LAB_LEFT_TIME_NAME = 'lab_rest_time'

    def __init__(self, dlg, activity_type):
        super(ActivityNewReturnDiscount, self).__init__(dlg, activity_type)
        self._timer = None
        self._timer_cb = {}
        self._left_time_node = None
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self._before_init_panel()
        return

    def _before_init_panel(self):
        self._goods_info = {}
        self._return_goods_lst = []
        return_goods_lst = global_data.player or [] if 1 else global_data.player.get_return_discount_item()
        for goods_idx, goods_info in enumerate(return_goods_lst):
            goods_id, discount = goods_info
            price_info_lst = mall_utils.get_mall_item_price(goods_id, pick_list=('yuanbao', ))
            if not price_info_lst:
                log_error('goods has no yuanbao price: {}'.format(goods_id))
                continue
            original_price = price_info_lst[0].get('original_price', 0)
            goods_payment = price_info_lst[0].get('goods_payment', None)
            if not original_price or not goods_payment:
                continue
            new_price_info = {'original_price': original_price,
               'discount_price': int(math.ceil(original_price * discount)),
               'goods_payment': goods_payment,
               'real_price': int(math.ceil(original_price * discount))
               }
            self._goods_info[goods_id] = new_price_info
            self._return_goods_lst.append([goods_id, discount, goods_idx])

        self.panel.list_items.DeleteAllSubItem()
        self.panel.list_items.SetInitCount(len(self._goods_info))
        for tmp_item in self.panel.list_items.GetAllItem():
            tmp_item.setVisible(False)

        self._init_reward_lst()
        return

    def on_init_panel(self):
        self._close_time = global_data.player.activity_closetime_data.get(self._activity_type, get_server_time())
        self._process_event(True)
        self._init_ui_event()
        self._left_time_node = self.panel.lab_time
        if self._left_time_node:
            self._register_timer()
            self._timer_cb[0] = lambda : self._refresh_left_time()
            self._refresh_left_time()
        self._custom_init_panel()

    def set_show(self, show, is_init=False):
        super(ActivityNewReturnDiscount, self).set_show(show, is_init)
        if not show:
            return
        self.panel.PlayAnimation('show')

        def play_item_anim(idx):
            item = self.panel.list_items.GetItem(idx)
            item.setVisible(True)

        item_num = self.panel.list_items.GetItemCount()
        act_lst = []
        for idx in range(item_num):
            if idx == 0:
                delay = 0.17 if 1 else 0.03
                act_lst.append(cc.DelayTime.create(delay))
                act_lst.append(cc.CallFunc.create(lambda item_idx=idx: play_item_anim(item_idx)))

        if act_lst:
            self.panel.runAction(cc.Sequence.create(act_lst))

    def _refresh_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = ''
        self._left_time_node.SetString(day_txt)

    def _init_reward_lst(self, *args):
        for idx, goods_info in enumerate(self._return_goods_lst):
            goods_id, discount, real_goods_idx = goods_info
            tmp_item = self.panel.list_items.GetItem(idx)
            goods_name = mall_utils.get_goods_name(goods_id)
            tmp_item.lab_name1.SetString(goods_name)
            goods_item_no = mall_utils.get_goods_item_no(goods_id)
            item_type = get_lobby_item_type(goods_item_no)
            goods_pic = mall_utils.get_goods_pic_path(goods_id)
            tmp_item.img_item.SetDisplayFrameByPath('', goods_pic)
            if goods_item_no and item_type == L_ITEM_TYPE_GIFTPACKAGE:
                tmp_item.btn_search.setVisible(True)

                @tmp_item.btn_search.unique_callback()
                def OnClick(btn, touch, item_param=goods_item_no):
                    jump_to_ui_new(item_param)

            else:
                tmp_item.btn_search.setVisible(False)
            if goods_item_no and item_type in (L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN):
                degree_pic = get_skin_rare_degree_icon(goods_item_no)
                if degree_pic:
                    tmp_item.temp_level.bar_level.SetDisplayFrameByPath('', degree_pic)
                else:
                    tmp_item.temp_level.setVisible(False)
            else:
                tmp_item.temp_level.setVisible(False)
            if item_type == L_ITEM_TYPE_MECHA:
                mecha_id = mecha_lobby_id_2_battle_id(goods_item_no)
                from logic.gutils.new_template_utils import set_mecha_combat_capacity
                set_mecha_combat_capacity(tmp_item.temp_list_tab, mecha_id)
            has_limited = mall_utils.limite_pay(goods_id)
            if goods_item_no and goods_id != GOODS_ID_RETURN_TICKETS_BOX and global_data.player.has_item_by_no(goods_item_no) or goods_id == global_data.player.get_new_return_buy_goods_id():
                has_owned = True
            else:
                has_owned = False
            is_finished = global_data.player.get_new_return_buy_goods_id()
            tmp_item.temp_price.setVisible(False)
            btn_txt = ''
            tmp_item.btn_get.SetEnable(False)
            if has_owned:
                btn_txt = 12136
            elif has_limited:
                btn_txt = 12121
            elif is_finished:
                if goods_item_no:
                    can_jump = can_jump_to_ui(goods_item_no)
                    btn_txt = 80706
                    tmp_item.btn_get.SetEnable(True)

                    @tmp_item.btn_get.unique_callback()
                    def OnClick(btn, touch, lobby_item_no=goods_item_no, can_jump_ui=can_jump):
                        if can_jump_ui:
                            jump_to_ui(lobby_item_no)
                        else:
                            jump_to_ui_new(lobby_item_no)

            else:
                tmp_item.temp_price.setVisible(True)
                tmp_item.btn_get.SetEnable(True)
                new_price_info = self._goods_info[goods_id]
                template_utils.init_price_template(new_price_info, tmp_item.temp_price, color=DARK_PRICE_COLOR)

                @tmp_item.btn_get.unique_callback()
                def OnClick(btn, touch, goods_param=goods_id, goods_idx_param=real_goods_idx):
                    new_price_info = self._goods_info[goods_param]

                    def on_confirm_buy(goods_buy_id, goods_buy_index=goods_idx_param):
                        if global_data.player:
                            global_data.player.buy_return_goods_with_index(goods_buy_index)

                    if goods_idx_param != 0:
                        global_data.ui_mgr.close_ui('RoleAndSkinBuyConfirmUI')
                        from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
                        RoleAndSkinBuyConfirmUI(goods_id=goods_param, pick_list=('yuanbao', ), fixed_price_info=[new_price_info], confirm_buy_func=on_confirm_buy)
                    else:
                        global_data.ui_mgr.close_ui('GroceriesBuyConfirmUI')
                        from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
                        GroceriesBuyConfirmUI(goods_id=str(goods_param), fixed_price_info=[new_price_info], confirm_buy_func=on_confirm_buy)

            tmp_item.btn_get.SetText(btn_txt)
            discount_num = '-{}%'.format(100 - int(discount * 100))
            tmp_item.lab_discount.SetString(discount_num)
            discount_str = get_discount_text_with_lang(discount, get_cur_text_lang())
            tmp_item.lab_discount.SetString(discount_str)

    def _init_ui_event(self):
        pass

    def _register_timer(self):
        from common.utils.timer import CLOCK
        self._unregister_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self._second_callback, interval=1, times=-1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def _second_callback(self):
        for timer_key, cb_func in six.iteritems(self._timer_cb):
            cb_func()

    def _process_event(self, is_bind):
        e_conf = {'buy_good_success_with_list': self._init_reward_lst,
           'task_prog_changed': self._init_reward_lst,
           'update_return_bought_goods_event': self._init_reward_lst
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _custom_init_panel(self):
        pass

    def on_finalize_panel(self):
        self._process_event(False)
        self._unregister_timer()