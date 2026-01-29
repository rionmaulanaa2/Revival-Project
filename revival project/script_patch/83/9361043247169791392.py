# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyGiftUseConfirmUI.py
from __future__ import absolute_import
import six
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, NORMAL_LAYER_ZORDER_2
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.cdata.intimacy_data import INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD, get_intimacy_pt
from common.const.property_const import U_ID, C_NAME
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_use_parms
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.cdata.intimacy_gift import gift_map
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI
USE_STEP_CHOOSE = 0
USE_STEP_QUANTITY = 1
USE_STEP_RESULT = 2

class IntimacyGiftUseConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/gift_use_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'buy_good_success_with_list': 'on_buy_good_success'
       }
    TEMPLATE_NODE_NAME = 'temp_bar'

    def show_window(self, data, send_callback=None, not_send_callback=None):
        self.data = data
        self.uid = str(data[U_ID])
        self.send_callback = send_callback
        self.not_send_callback = not_send_callback
        self.intimacy_day_limit = global_data.player.intimacy_day_limit.get(self.uid, {})
        self.sent_amount = {gift_id:INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD - limit for gift_id, limit in six.iteritems(self.intimacy_day_limit)}
        self.use_amount = 0
        self.gift_id = None
        self.panel.lab_gift_player.SetString(get_text_by_id(3244, {'name': str(data[C_NAME])}))
        self.show_nd_choose()
        return

    def show_nd_choose(self):
        self.use_step = USE_STEP_CHOOSE
        self.panel.nd_choose.setVisible(True)
        self.panel.nd_quantity.setVisible(False)
        self.panel.nd_result.setVisible(False)
        self.panel.list_gift.SetInitCount(len(gift_map))
        for idx, gift_id in enumerate(six.iterkeys(gift_map)):
            item = self.panel.list_gift.GetItem(idx)
            init_tempate_mall_i_item(item.temp_item, gift_id, global_data.player.get_item_num_by_no(gift_id), show_tips=True)
            sent_num = self.sent_amount.get(str(gift_id), 0)
            item.lab_limit.SetString(get_text_by_id(3232, {'num': sent_num,'limit': INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD}))
            enable = sent_num < INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD
            item.btn_use.btn_common.SetEnable(enable)
            item.btn_use.btn_common.SetText(81191 if enable else 81920)
            if enable:
                item.btn_use.btn_common.BindMethod('OnClick', lambda btn, touch, gift_id=gift_id: self.show_nd_quantity(gift_id))

    def show_nd_quantity(self, gift_id):
        self.use_step = USE_STEP_QUANTITY
        self.panel.nd_quantity.setVisible(True)
        self.panel.nd_choose.setVisible(False)
        self.panel.nd_result.setVisible(False)
        self.gift_id = gift_id
        init_tempate_mall_i_item(self.panel.temp_item, gift_id)
        self.panel.lab_name.SetString(get_lobby_item_name(gift_id))
        self.panel.lab_details.SetString(get_lobby_item_desc(gift_id))
        self.panel.lab_limit.SetString(get_text_by_id(3232, {'num': self.sent_amount.get(str(gift_id), 0),'limit': INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD}))
        self.num_btn_widget = ItemNumBtnWidget(self.panel.input_quantity)
        item_poccess_num = global_data.player.get_item_num_by_no(gift_id)
        send_limit = self.intimacy_day_limit.get(str(gift_id), INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD)
        gift_max_cnt = min(item_poccess_num, send_limit)
        item_data = {'quantity': gift_max_cnt,
           'min_num': min(gift_max_cnt, 1)
           }

        def on_num_changed(_, num):
            self.use_amount = num

        self.num_btn_widget.init_item(item_data, on_num_changed, min(gift_max_cnt, 1))
        if send_limit == 0:
            self.panel.btn_use.btn_common.SetEnable(False)
            self.panel.btn_use.btn_common.SetText(81920)
        elif item_poccess_num == 0:
            self.panel.btn_use.btn_common.SetEnable(True)
            self.panel.btn_use.btn_common.SetText(14005)
            self.panel.btn_use.btn_common.BindMethod('OnClick', lambda *args: groceries_buy_confirmUI(goods_id=str(gift_map[gift_id])))
        else:
            self.panel.btn_use.btn_common.SetEnable(True)
            self.panel.btn_use.btn_common.SetText(80338)
            self.panel.btn_use.btn_common.BindMethod('OnClick', lambda *args: self.show_nd_result())

    def show_nd_result(self):
        self.use_step = USE_STEP_RESULT
        self.panel.nd_result.setVisible(True)
        self.panel.nd_quantity.setVisible(False)
        self.panel.nd_choose.setVisible(False)
        PlayerInfoManager().add_head_item_auto(self.panel.temp_head, int(self.uid), 0, self.data)
        cur_intimacy = get_intimacy_pt(global_data.player.intimacy_data.get(self.uid, [0, None, None, 0, -1]))
        add_intimacy = get_lobby_item_use_parms(self.gift_id).get('intimacy', 0) * self.use_amount
        self.panel.lab_value_num.SetString(str(cur_intimacy))
        self.panel.lab_value_plus.SetString('+%d' % add_intimacy)
        self.panel.btn_confirm.btn_common.BindMethod('OnClick', self.send_gift)
        return

    def send_gift(self, *args):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        item = global_data.player.get_item_by_no(self.gift_id)
        if not item:
            self.close()
            return
        global_data.player.use_item(item.get_id(), self.use_amount, {'frd_uid': self.data[U_ID],'gift_name': get_lobby_item_name(self.gift_id)})
        global_data.game_mgr.show_tip(get_text_by_id(14002, args={'name': get_lobby_item_name(self.gift_id)}))
        self.close(gift_sent=True)

    def on_buy_good_success(self, goods_list):
        if self.use_step == USE_STEP_QUANTITY:
            goods_id = gift_map[self.gift_id]
            for goods in goods_list:
                if goods[0] == goods_id:
                    self.show_nd_quantity(self.gift_id)
                    return

    def close(self, gift_sent=False, *args):
        super(IntimacyGiftUseConfirmUI, self).close(*args)
        if gift_sent and callable(self.send_callback):
            self.send_callback()
        elif not gift_sent and callable(self.not_send_callback):
            self.not_send_callback()