# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/mall_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'mall_red_point_update',
 'lobby_mall_red_point_update',
 'select_mall_goods',
 'mall_new_recommendation_update',
 'mall_goods_discount_status_update',
 'mall_goods_discount_rp_update',
 'mall_new_arrivals_update',
 'mall_dec_set_rp_update',
 'mall_init_sub_ui_price_widget',
 'mall_clear_sub_ui_price_widget',
 'update_meow_capacity_lv']
regist_event(EVENT_LIST)