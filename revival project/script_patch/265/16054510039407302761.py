# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPay.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_ONLY, SERVER_ONLY, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.platform.dctool import interface
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_TRY_PURCHASE, AF_PURCHASE, AF_UNIQUE_PURCHASE, AF_CURRENCY, AF_REVENUE, FB_PLATFORM, AF_PLATFORM
from logic.gcommon.const import SHOP_ITEM_YUANBAO, PAY_TYPE_NILES
import json

class impPay(object):

    def _init_pay_from_dict(self, bdict):
        self.vip_point = bdict.get('vip_point', 0)
        self.goodsid_pay_record = set(bdict.get('goodsid_pay_record', []))
        self.last_pay_time = 0

    def get_vip_point(self):
        return self.vip_point

    def get_goods_info(self, goodsid):
        pay_conf = confmgr.get('pay_config', interface.get_project_id())
        return pay_conf.get(goodsid, {})

    def get_local_region(self):
        import game3d
        country_str = game3d.get_country_code()
        if not country_str:
            return 'US'
        return country_str

    def channel_order_fail(self, goodsid, privateparam):
        log_error('channel_order_fail', goodsid, privateparam)
        goods_type = self.get_goods_info(goodsid).get('type', 0)
        if goods_type in PAY_TYPE_NILES:
            self.nile_pay_ret(-1, privateparam)

    def pay_order(self, goodsid, privateparam=None):
        Appsflyer().advert_track_event(AF_TRY_PURCHASE)
        self.call_server_method('pay_order', {'goodsid': goodsid,'fee_env': global_data.channel.get_fee_env(),'privateparam': privateparam or {}})

    @rpc_method(CLIENT_STUB, (Str('goodsid'), Int('flag'), Dict('extra_info')))
    def pay_order_callback(self, goodsid, flag, extra_info):
        privateparam = extra_info.get('privateparam', None)
        goods_type = self.get_goods_info(goodsid).get('type', 0)
        if flag > 0:
            cur_time = time_utility.get_server_time()
            if cur_time - self.last_pay_time > 3 or G_IS_NA_USER:
                if not global_data.channel.order_product(goodsid, privateparam):
                    if goods_type in PAY_TYPE_NILES:
                        self.nile_pay_ret(-1, privateparam)
                is_no_oc_guarantee = global_data.channel.is_no_order_callback_guarantee_channel()
                if not is_no_oc_guarantee:
                    global_data.ui_mgr.show_ui('Charging', 'logic.comsys.charge_ui')
                self.last_pay_time = cur_time
            else:
                global_data.game_mgr.show_tip(get_text_by_id(609400))
                if goods_type in PAY_TYPE_NILES:
                    self.nile_pay_ret(4, privateparam)
        else:
            if goods_type in PAY_TYPE_NILES:
                self.nile_pay_ret(-1, privateparam)
            if flag == -99:
                tid = 12030
            elif flag == -1:
                tid = 12031
            else:
                if flag == -2:
                    from logic.comsys.mall_ui.PurchaseAgeCheckUI import PurchaseAgeCheckUI
                    PurchaseAgeCheckUI()
                    return
                if flag == -3:
                    pay_limit = extra_info.get('pay_limit', 0)
                    from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                    NormalConfirmUI2().set_content_string(get_text_by_id(81120, {'pay_limit': pay_limit}))
                    return
                if flag == -10:
                    from logic.comsys.charge_ui.PayLimitUI import PayLimitUI
                    PayLimitUI(limit_info=extra_info)
                    return
                tid = 12032
            global_data.game_mgr.show_tip(get_text_local_content(tid))
        return

    @rpc_method(CLIENT_STUB, (Str('order_sn'), Bool('ret'), Dict('revenue_dict'), Bool('has_pay'), Int('yuanbao'), Str('goods_id'), Dict('privateparam')))
    def order_product_ret(self, order_sn, ret, revenue_dict, has_pay, yuanbao, goods_id, privateparam):
        if ret:
            af_revenue_dict = {AF_REVENUE: float(revenue_dict.get('paymoney', 0)),AF_CURRENCY: str(revenue_dict.get('paycurrency', 'CNY'))
               }
            revenue_param = json.dumps(af_revenue_dict)
            Appsflyer().advert_track_event(AF_PURCHASE, revenue_param, platform=AF_PLATFORM)
            firebase_revenue_dict = {'value': float(revenue_dict.get('paymoney', 0)),
               'currency': str(revenue_dict.get('paycurrency', 'CNY'))
               }
            revenue_param = json.dumps(firebase_revenue_dict)
            Appsflyer().advert_track_event(AF_PURCHASE, revenue_param, platform=FB_PLATFORM)
            if not has_pay:
                Appsflyer().advert_track_event(AF_UNIQUE_PURCHASE)
            global_data.emgr.receive_award_succ_event.emit({SHOP_ITEM_YUANBAO: yuanbao})
            self.goodsid_pay_record.add(goods_id)
            global_data.emgr.pay_order_succ_event.emit()
            goods_type = self.get_goods_info(goods_id).get('type', 0)
            if goods_type in PAY_TYPE_NILES:
                self.nile_pay_ret(3, privateparam)
        is_no_oc_guarantee = global_data.channel.is_no_order_callback_guarantee_channel()
        if is_no_oc_guarantee:
            global_data.channel.reset_last_pay_time()
        if global_data.channel.is_slow_order_callback_channel():
            global_data.ui_mgr.close_ui('Charging')

    def check_pc_pay(self):
        self.call_server_method('check_pc_pay', {'fee_env': global_data.channel.get_fee_env()})

    @rpc_method(CLIENT_STUB, (Int('flag'), Dict('extra_info')))
    def pc_pay_order_callback(self, flag, extra_info):
        if flag > 0:
            from logic.gutils.jump_to_ui_utils import jump_to_web_charge_imp
            jump_to_web_charge_imp()
        else:
            if flag == -2:
                from logic.comsys.mall_ui.PurchaseAgeCheckUI import PurchaseAgeCheckUI
                PurchaseAgeCheckUI()
                return
            global_data.game_mgr.show_tip(get_text_local_content(12032))

    def has_pay_goodsid(self, goodsid):
        return goodsid in self.goodsid_pay_record

    @rpc_method(CLIENT_STUB, ())
    def clear_pay_record(self):
        self.goodsid_pay_record = set()