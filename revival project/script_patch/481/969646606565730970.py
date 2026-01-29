# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonExchange.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.mall_ui.LotteryTicketBuyConfirmUI import LotteryTicketBuyConfirmUI
from logic.comsys.activity.widget import widget
import logic.gcommon.const as gconst

@widget('DescribeWidget')
class ActivityCommonExchange(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommonExchange, self).__init__(dlg, activity_type)
        self.price_top_widget = None
        return

    def on_init_panel--- This code section failed: ---

  24       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_activity_config'
           9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             2  '_activity_type'
          15  LOAD_CONST            2  'default'
          18  BUILD_MAP_0           0 
          21  CALL_FUNCTION_258   258 
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            3  'cUiData'
          30  BUILD_MAP_0           0 
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            1  'ui_data'

  25      39  LOAD_GLOBAL           3  'str'
          42  LOAD_FAST             1  'ui_data'
          45  LOAD_CONST            4  'goods_id'
          48  BINARY_SUBSCR    
          49  CALL_FUNCTION_1       1 
          52  STORE_DEREF           0  'goods_id'

  26      55  LOAD_GLOBAL           4  'mall_utils'
          58  LOAD_ATTR             5  'get_goods_item_no'
          61  LOAD_DEREF            0  'goods_id'
          64  CALL_FUNCTION_1       1 
          67  STORE_FAST            2  'goods_item_no'

  27      70  LOAD_GLOBAL           4  'mall_utils'
          73  LOAD_ATTR             6  'get_mall_item_price_list'
          76  LOAD_DEREF            0  'goods_id'
          79  CALL_FUNCTION_1       1 
          82  UNPACK_SEQUENCE_2     2 
          85  STORE_FAST            3  'comsume_item_no'
          88  STORE_FAST            4  'comsume_item_num'

  29      91  LOAD_GLOBAL           7  'template_utils'
          94  LOAD_ATTR             8  'init_tempate_mall_i_item'
          97  LOAD_FAST             0  'self'
         100  LOAD_ATTR             9  'panel'
         103  LOAD_ATTR            10  'list_item'
         106  LOAD_ATTR            11  'GetItem'
         109  LOAD_CONST            5  ''
         112  CALL_FUNCTION_1       1 
         115  LOAD_FAST             3  'comsume_item_no'
         118  LOAD_FAST             4  'comsume_item_num'
         121  LOAD_CONST            6  'show_all_num'
         124  LOAD_GLOBAL          12  'True'
         127  CALL_FUNCTION_259   259 
         130  POP_TOP          

  30     131  LOAD_GLOBAL           7  'template_utils'
         134  LOAD_ATTR             8  'init_tempate_mall_i_item'
         137  LOAD_FAST             0  'self'
         140  LOAD_ATTR             9  'panel'
         143  LOAD_ATTR            10  'list_item'
         146  LOAD_ATTR            11  'GetItem'
         149  LOAD_CONST            7  1
         152  CALL_FUNCTION_1       1 
         155  LOAD_FAST             2  'goods_item_no'
         158  LOAD_CONST            7  1
         161  LOAD_CONST            6  'show_all_num'
         164  LOAD_GLOBAL          12  'True'
         167  CALL_FUNCTION_259   259 
         170  POP_TOP          

  32     171  LOAD_FAST             0  'self'
         174  LOAD_ATTR             9  'panel'
         177  LOAD_ATTR            13  'list_price'
         180  POP_JUMP_IF_FALSE   258  'to 258'

  33     183  LOAD_GLOBAL          14  'PriceUIWidget'
         186  LOAD_GLOBAL           8  'init_tempate_mall_i_item'
         189  LOAD_FAST             0  'self'
         192  LOAD_ATTR             9  'panel'
         195  LOAD_ATTR            13  'list_price'
         198  CALL_FUNCTION_257   257 
         201  LOAD_FAST             0  'self'
         204  STORE_ATTR           15  'price_top_widget'

  34     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR            15  'price_top_widget'
         213  LOAD_ATTR            16  'show_money_types'
         216  LOAD_CONST            9  '%d_%d'
         219  LOAD_GLOBAL          17  'gconst'
         222  LOAD_ATTR            18  'SHOP_PAYMENT_ITEM'
         225  LOAD_FAST             2  'goods_item_no'
         228  BUILD_TUPLE_2         2 
         231  BINARY_MODULO    
         232  LOAD_CONST            9  '%d_%d'
         235  LOAD_GLOBAL          17  'gconst'
         238  LOAD_ATTR            18  'SHOP_PAYMENT_ITEM'
         241  LOAD_FAST             3  'comsume_item_no'
         244  BUILD_TUPLE_2         2 
         247  BINARY_MODULO    
         248  BUILD_LIST_2          2 
         251  CALL_FUNCTION_1       1 
         254  POP_TOP          
         255  JUMP_FORWARD          0  'to 258'
       258_0  COME_FROM                '255'

  36     258  LOAD_FAST             0  'self'
         261  LOAD_ATTR             9  'panel'
         264  LOAD_ATTR            19  'btn_exchange'
         267  POP_JUMP_IF_FALSE   306  'to 306'

  37     270  LOAD_FAST             0  'self'
         273  LOAD_ATTR             9  'panel'
         276  LOAD_ATTR            19  'btn_exchange'
         279  LOAD_ATTR            20  'unique_callback'
         282  CALL_FUNCTION_0       0 
         285  LOAD_CLOSURE          0  'goods_id'
         291  LOAD_CONST               '<code_object OnClick>'
         294  MAKE_CLOSURE_0        0 
         297  CALL_FUNCTION_1       1 
         300  STORE_FAST            5  'OnClick'
         303  JUMP_FORWARD          0  'to 306'
       306_0  COME_FROM                '303'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 198

    def on_finalize_panel(self):
        super(ActivityCommonExchange, self).on_finalize_panel()
        if self.price_top_widget:
            self.price_top_widget.destroy()
            self.price_top_widget = None
        return