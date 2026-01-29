# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ChargeGiftBoxFailUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_NO_EFFECT, UI_TYPE_CONFIRM
from logic.gutils.mall_utils import get_goods_item_reward_id, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price, is_pc_global_pay
from logic.gutils.template_utils import init_tempate_mall_i_item, set_widget_discount_tag
from common.cfg import confmgr
from logic.gutils.jump_to_ui_utils import jump_to_web_charge

class ChargeGiftBoxFailUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'charge/charge_gift_box_new_fail'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_refuse.btn_common_big.OnClick': 'close',
       'btn_accept.btn_common_big.OnClick': 'on_click_btn_accept'
       }
    GLOBAL_EVENT = {'buy_good_success': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ChargeGiftBoxFailUI, self).on_init_panel()
        self.is_pc_global_pay = is_pc_global_pay()

    def show_panel(self, goods_id, goods_func, tag, goods_info=None, specified_reward_id=None):
        if tag > 0:
            self.nd_tag_pink.setVisible(False)
            self.nd_tag_bones.setVisible(True)
        else:
            self.nd_tag_pink.setVisible(True)
            self.nd_tag_bones.setVisible(False)
        set_widget_discount_tag(self.panel, tag)
        self.goods_id = goods_id
        self.goods_func = goods_func
        if not goods_info:
            self.goods_info = getattr(global_data.lobby_mall_data, goods_func)() if 1 else goods_info
            if not specified_reward_id:
                if self.goods_id is not None:
                    goods_id_reward_id = get_goods_item_reward_id(goods_id)
                    if not goods_id_reward_id:
                        return
                    reward_id = goods_id_reward_id
                else:
                    return
            else:
                reward_id = specified_reward_id
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            return reward_conf or None
        else:
            reward_list = reward_conf.get('reward_list', [])
            reward_count = len(reward_list)
            self.panel.list_item_1.SetInitCount(reward_count)
            for idx, reward in enumerate(reward_list):
                item = self.panel.list_item_1.GetItem(idx)
                item_no, item_num = reward
                init_tempate_mall_i_item(item.temp_reward, item_no, item_num=item_num, show_tips=True)

            if not self.goods_info:
                self.panel.btn_accept.btn_common_big.SetEnable(False)
                self.panel.temp_price.lab_price.SetString('******')
            else:
                self.panel.btn_accept.btn_common_big.SetEnable(True)
                if self.is_pc_global_pay or is_steam_pay():
                    price_txt = get_pc_charge_price_str(self.goods_info)
                else:
                    key = self.goods_info['goodsid']
                    price_txt = get_charge_price_str(key)
                self.panel.temp_price.lab_price.SetString(adjust_price(str(price_txt)))
            self.show()
            if global_data.ui_lifetime_log_mgr:
                global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(self.__class__.__name__)
            return

    def on_click_btn_accept(self, *args):
        from logic.gutils.ui_salog_utils import add_uiclick_salog_lobby
        add_uiclick_salog_lobby('pay_retry')
        if self.is_pc_global_pay:
            jump_to_web_charge()
        else:
            goods_info = self.goods_info or getattr(global_data.lobby_mall_data, self.goods_func)() if 1 else self.goods_info
            if goods_info and global_data.player:
                global_data.player.pay_order(goods_info['goodsid'])

    def on_finalize_panel(self):
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(self.__class__.__name__)