# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/BuyConfirmUIInterface.py
from __future__ import absolute_import
import six_ex
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
from logic.comsys.mall_ui.GroceriesUseConfirmUI import GroceriesUseConfirmUI
from logic.comsys.mall_ui.ItemSkinBuyConfirmUI import ItemSkinBuyConfirmUI
from logic.comsys.mall_ui.RoleAndSkinTogetherBuyConfirmUI import RoleAndSkinTogetherBuyConfirmUI
from logic.comsys.mall_ui.RecommendGiftBuyConfirmUI import RecommendGiftBuyConfirmUI
from logic.comsys.mall_ui.GroceriesBothBuyConfirmUI import GroceriesBothBuyConfirmUI
from logic.comsys.lottery.LotteryGiftsBuyConfirmUI import LotteryGiftsBuyConfirmUI
from logic.comsys.mall_ui.MeowUpgradeConfirmUI import MeowUpgradeConfirmUI
from logic.gutils import mall_utils

def groceries_buy_confirmUI--- This code section failed: ---

  16       0  LOAD_GLOBAL           0  'mall_utils'
           3  LOAD_ATTR             1  'get_mall_item_price'
           6  LOAD_FAST             0  'goods_id'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            2  'prices'

  17      15  LOAD_FAST             2  'prices'
          18  POP_JUMP_IF_FALSE    80  'to 80'
          21  LOAD_GLOBAL           2  'len'
          24  LOAD_FAST             2  'prices'
          27  CALL_FUNCTION_1       1 
          30  LOAD_CONST            1  2
          33  COMPARE_OP            2  '=='
        36_0  COME_FROM                '18'
          36  POP_JUMP_IF_FALSE    80  'to 80'

  18      39  LOAD_GLOBAL           3  'global_data'
          42  LOAD_ATTR             4  'ui_mgr'
          45  LOAD_ATTR             5  'close_ui'
          48  LOAD_CONST            2  'GroceriesBothBuyConfirmUI'
          51  CALL_FUNCTION_1       1 
          54  POP_TOP          

  19      55  LOAD_GLOBAL           6  'GroceriesBothBuyConfirmUI'
          58  LOAD_CONST            3  'goods_id'
          61  LOAD_CONST            4  'pick_list'
          64  LOAD_FAST             1  'pick_list'
          67  LOAD_CONST            5  'need_show'
          70  LOAD_CONST            0  ''
          73  CALL_FUNCTION_768   768 
          76  POP_TOP          
          77  JUMP_FORWARD         38  'to 118'

  21      80  LOAD_GLOBAL           3  'global_data'
          83  LOAD_ATTR             4  'ui_mgr'
          86  LOAD_ATTR             5  'close_ui'
          89  LOAD_CONST            6  'GroceriesBuyConfirmUI'
          92  CALL_FUNCTION_1       1 
          95  POP_TOP          

  22      96  LOAD_GLOBAL           8  'GroceriesBuyConfirmUI'
          99  LOAD_CONST            3  'goods_id'
         102  LOAD_CONST            4  'pick_list'
         105  LOAD_FAST             1  'pick_list'
         108  LOAD_CONST            5  'need_show'
         111  LOAD_CONST            0  ''
         114  CALL_FUNCTION_768   768 
         117  POP_TOP          
       118_0  COME_FROM                '77'
         118  LOAD_CONST            0  ''
         121  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_768' instruction at offset 73


def lottery_gifts_buy_confirmUI--- This code section failed: ---

  25       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'ui_mgr'
           6  LOAD_ATTR             2  'close_ui'
           9  LOAD_CONST            1  'LotteryGiftsBuyConfirmUI'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  26      16  LOAD_GLOBAL           3  'LotteryGiftsBuyConfirmUI'
          19  LOAD_CONST            2  'achieve_id'
          22  LOAD_CONST            3  'goods_id'
          25  LOAD_FAST             1  'goods_id'
          28  CALL_FUNCTION_512   512 
          31  POP_TOP          

Parse error at or near `CALL_FUNCTION_512' instruction at offset 28


def role_or_skin_buy_confirmUI--- This code section failed: ---

  29       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('confmgr',)
           6  IMPORT_NAME           0  'common.cfg'
           9  IMPORT_FROM           1  'confmgr'
          12  STORE_FAST            4  'confmgr'
          15  POP_TOP          

  30      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('mall_const',)
          22  IMPORT_NAME           2  'logic.client.const'
          25  IMPORT_FROM           3  'mall_const'
          28  STORE_FAST            5  'mall_const'
          31  POP_TOP          

  31      32  LOAD_FAST             4  'confmgr'
          35  LOAD_ATTR             4  'get'
          38  LOAD_CONST            4  'mall_config'
          41  LOAD_GLOBAL           5  'str'
          44  LOAD_FAST             0  'goods_id'
          47  CALL_FUNCTION_1       1 
          50  LOAD_CONST            5  'default'
          53  BUILD_MAP_0           0 
          56  CALL_FUNCTION_258   258 
          59  STORE_FAST            6  'mall_conf'

  32      62  LOAD_FAST             6  'mall_conf'
          65  LOAD_ATTR             4  'get'
          68  LOAD_CONST            6  'item_type'
          71  LOAD_CONST            1  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            7  'goods_type'

  34      80  LOAD_GLOBAL           6  'mall_utils'
          83  LOAD_ATTR             7  'is_recommend_gift_goods'
          86  LOAD_FAST             0  'goods_id'
          89  CALL_FUNCTION_1       1 
          92  POP_JUMP_IF_FALSE   142  'to 142'
          95  LOAD_FAST             7  'goods_type'
          98  LOAD_FAST             5  'mall_const'
         101  LOAD_ATTR             8  'REWARD_TYPE'
         104  COMPARE_OP            2  '=='
       107_0  COME_FROM                '92'
         107  POP_JUMP_IF_FALSE   142  'to 142'

  35     110  LOAD_GLOBAL           9  'global_data'
         113  LOAD_ATTR            10  'ui_mgr'
         116  LOAD_ATTR            11  'close_ui'
         119  LOAD_CONST            7  'RecommendGiftBuyConfirmUI'
         122  CALL_FUNCTION_1       1 
         125  POP_TOP          

  36     126  LOAD_GLOBAL          12  'RecommendGiftBuyConfirmUI'
         129  LOAD_CONST            8  'goods_id'
         132  LOAD_CONST            9  'pick_list'
         135  LOAD_DEREF            0  'pick_list'
         138  CALL_FUNCTION_512   512 
         141  RETURN_END_IF    
       142_0  COME_FROM                '107'

  38     142  LOAD_CONST            0  ''
         145  STORE_FAST            8  'force_together_goods_id'

  39     148  LOAD_FAST             2  'check_top_skin'
         151  POP_JUMP_IF_FALSE   515  'to 515'

  40     154  LOAD_GLOBAL           6  'mall_utils'
         157  LOAD_ATTR            14  'get_goods_item_no'
         160  LOAD_FAST             0  'goods_id'
         163  CALL_FUNCTION_1       1 
         166  STORE_FAST            9  'item_no'

  41     169  LOAD_CONST            1  ''
         172  LOAD_CONST           10  ('dress_utils',)
         175  IMPORT_NAME          15  'logic.gutils'
         178  IMPORT_FROM          16  'dress_utils'
         181  STORE_FAST           10  'dress_utils'
         184  POP_TOP          

  42     185  LOAD_CONST            1  ''
         188  LOAD_CONST           11  ('item_utils',)
         191  IMPORT_NAME          15  'logic.gutils'
         194  IMPORT_FROM          17  'item_utils'
         197  STORE_FAST           11  'item_utils'
         200  POP_TOP          

  43     201  LOAD_FAST            11  'item_utils'
         204  LOAD_ATTR            18  'get_lobby_item_type'
         207  LOAD_FAST             9  'item_no'
         210  CALL_FUNCTION_1       1 
         213  STORE_FAST           12  'item_type'

  44     216  LOAD_CONST            1  ''
         219  LOAD_CONST           12  ('lobby_item_type',)
         222  IMPORT_NAME          19  'logic.gcommon.item'
         225  IMPORT_FROM          20  'lobby_item_type'
         228  STORE_FAST           13  'lobby_item_type'
         231  POP_TOP          

  45     232  LOAD_FAST            12  'item_type'
         235  LOAD_FAST            13  'lobby_item_type'
         238  LOAD_ATTR            21  'L_ITEM_TYPE_ROLE_SKIN'
         241  BUILD_LIST_1          1 
         244  COMPARE_OP            6  'in'
         247  POP_JUMP_IF_FALSE   515  'to 515'

  46     250  LOAD_FAST            10  'dress_utils'
         253  LOAD_ATTR            22  'get_top_skin_id_by_skin_id'
         256  LOAD_FAST             9  'item_no'
         259  CALL_FUNCTION_1       1 
         262  STORE_FAST           14  'top_skin_id'

  47     265  LOAD_FAST            11  'item_utils'
         268  LOAD_ATTR            23  'get_lobby_item_belong_no'
         271  LOAD_FAST             9  'item_no'
         274  CALL_FUNCTION_1       1 
         277  STORE_FAST           15  'belong_role_no'

  48     280  LOAD_FAST            10  'dress_utils'
         283  LOAD_ATTR            24  'get_goods_id_of_role_dress_related_item_no'
         286  LOAD_FAST            14  'top_skin_id'
         289  CALL_FUNCTION_1       1 
         292  STORE_DEREF           1  'top_skin_goods_id'

  50     295  LOAD_GLOBAL           5  'str'
         298  LOAD_FAST            14  'top_skin_id'
         301  CALL_FUNCTION_1       1 
         304  LOAD_GLOBAL           5  'str'
         307  LOAD_FAST             9  'item_no'
         310  CALL_FUNCTION_1       1 
         313  COMPARE_OP            3  '!='
         316  POP_JUMP_IF_FALSE   512  'to 512'

  51     319  LOAD_GLOBAL           6  'mall_utils'
         322  LOAD_ATTR            25  'item_has_owned_by_item_no'
         325  LOAD_FAST            14  'top_skin_id'
         328  CALL_FUNCTION_1       1 
         331  UNARY_NOT        
         332  POP_JUMP_IF_FALSE   482  'to 482'

  52     335  LOAD_GLOBAL           6  'mall_utils'
         338  LOAD_ATTR            25  'item_has_owned_by_item_no'
         341  LOAD_FAST            15  'belong_role_no'
         344  CALL_FUNCTION_1       1 
         347  UNARY_NOT        
       348_0  COME_FROM                '332'
         348  POP_JUMP_IF_FALSE   482  'to 482'

  53     351  LOAD_DEREF            1  'top_skin_goods_id'
         354  POP_JUMP_IF_FALSE   506  'to 506'

  54     357  LOAD_FAST            11  'item_utils'
         360  LOAD_ATTR            26  'get_lobby_item_belong_name'
         363  LOAD_FAST             9  'item_no'
         366  CALL_FUNCTION_1       1 
         369  STORE_FAST           16  'role_name'

  55     372  LOAD_FAST            11  'item_utils'
         375  LOAD_ATTR            27  'get_lobby_item_name'
         378  LOAD_FAST            14  'top_skin_id'
         381  CALL_FUNCTION_1       1 
         384  STORE_FAST           17  'top_skin_name'

  56     387  LOAD_CONST            1  ''
         390  LOAD_CONST           13  ('SecondConfirmDlg2',)
         393  IMPORT_NAME          28  'logic.comsys.common_ui.NormalConfirmUI'
         396  IMPORT_FROM          29  'SecondConfirmDlg2'
         399  STORE_FAST           18  'SecondConfirmDlg2'
         402  POP_TOP          

  58     403  LOAD_CLOSURE          1  'top_skin_goods_id'
         406  LOAD_CLOSURE          0  'pick_list'
         412  LOAD_CONST               '<code_object on_confirm_buy_top_skin_and_role>'
         415  MAKE_CLOSURE_0        0 
         418  STORE_FAST           19  'on_confirm_buy_top_skin_and_role'

  61     421  LOAD_FAST            18  'SecondConfirmDlg2'
         424  CALL_FUNCTION_0       0 
         427  STORE_FAST           20  'ui'

  62     430  LOAD_FAST            20  'ui'
         433  LOAD_ATTR            30  'confirm'
         436  LOAD_CONST           15  'content'
         439  LOAD_GLOBAL          31  'get_text_by_id'
         442  LOAD_CONST           16  608619
         445  BUILD_MAP_2           2 
         448  LOAD_FAST            16  'role_name'
         451  LOAD_CONST           17  'role_name'
         454  STORE_MAP        
         455  LOAD_FAST            17  'top_skin_name'
         458  LOAD_CONST           18  'top_skin_name'
         461  STORE_MAP        
         462  CALL_FUNCTION_2       2 
         465  LOAD_CONST           19  'confirm_callback'

  63     468  LOAD_FAST            19  'on_confirm_buy_top_skin_and_role'
         471  CALL_FUNCTION_512   512 
         474  POP_TOP          

  64     475  LOAD_CONST            0  ''
         478  RETURN_END_IF    
       479_0  COME_FROM                '354'
         479  JUMP_ABSOLUTE       509  'to 509'

  65     482  LOAD_GLOBAL           6  'mall_utils'
         485  LOAD_ATTR            25  'item_has_owned_by_item_no'
         488  LOAD_FAST            14  'top_skin_id'
         491  CALL_FUNCTION_1       1 
         494  POP_JUMP_IF_TRUE    509  'to 509'

  66     497  LOAD_DEREF            1  'top_skin_goods_id'
         500  STORE_FAST            8  'force_together_goods_id'
         503  JUMP_ABSOLUTE       509  'to 509'
         506  JUMP_ABSOLUTE       512  'to 512'
         509  JUMP_ABSOLUTE       515  'to 515'
         512  JUMP_FORWARD          0  'to 515'
       515_0  COME_FROM                '512'

  68     515  LOAD_FAST             8  'force_together_goods_id'
         518  JUMP_IF_TRUE_OR_POP   533  'to 533'
         521  LOAD_GLOBAL           6  'mall_utils'
         524  LOAD_ATTR            32  'get_buy_together_goods_id'
         527  LOAD_FAST             0  'goods_id'
         530  CALL_FUNCTION_1       1 
       533_0  COME_FROM                '518'
         533  STORE_FAST           21  'together_goods_id'

  70     536  LOAD_FAST            21  'together_goods_id'
         539  POP_JUMP_IF_FALSE   640  'to 640'

  72     542  LOAD_GLOBAL           6  'mall_utils'
         545  LOAD_ATTR            33  'get_mall_item_price_gift_item'
         548  LOAD_FAST            21  'together_goods_id'
         551  CALL_FUNCTION_1       1 
         554  UNPACK_SEQUENCE_2     2 
         557  STORE_FAST           22  'price_gift_item_dict'
         560  STORE_FAST           23  'min_gift_close_time'

  73     563  LOAD_GLOBAL          34  'int'
         566  LOAD_FAST             0  'goods_id'
         569  CALL_FUNCTION_1       1 
         572  LOAD_GLOBAL          35  'six_ex'
         575  LOAD_ATTR            36  'values'
         578  LOAD_FAST            22  'price_gift_item_dict'
         581  CALL_FUNCTION_1       1 
         584  COMPARE_OP            6  'in'
         587  POP_JUMP_IF_FALSE   599  'to 599'

  74     590  LOAD_FAST            21  'together_goods_id'
         593  STORE_FAST            0  'goods_id'
         596  JUMP_ABSOLUTE       640  'to 640'

  76     599  LOAD_GLOBAL           9  'global_data'
         602  LOAD_ATTR            10  'ui_mgr'
         605  LOAD_ATTR            11  'close_ui'
         608  LOAD_CONST           20  'RoleAndSkinTogetherBuyConfirmUI'
         611  CALL_FUNCTION_1       1 
         614  POP_TOP          

  77     615  LOAD_GLOBAL          37  'RoleAndSkinTogetherBuyConfirmUI'
         618  LOAD_CONST            8  'goods_id'
         621  LOAD_CONST           21  'together_goods_id'
         624  LOAD_FAST            21  'together_goods_id'
         627  LOAD_CONST            9  'pick_list'
         630  LOAD_DEREF            0  'pick_list'
         633  CALL_FUNCTION_768   768 
         636  RETURN_VALUE     
         637  JUMP_FORWARD          0  'to 640'
       640_0  COME_FROM                '637'

  79     640  LOAD_GLOBAL           9  'global_data'
         643  LOAD_ATTR            10  'ui_mgr'
         646  LOAD_ATTR            11  'close_ui'
         649  LOAD_CONST           22  'RoleAndSkinBuyConfirmUI'
         652  CALL_FUNCTION_1       1 
         655  POP_TOP          

  80     656  LOAD_GLOBAL          38  'RoleAndSkinBuyConfirmUI'
         659  LOAD_CONST            8  'goods_id'
         662  LOAD_CONST            9  'pick_list'
         665  LOAD_DEREF            0  'pick_list'
         668  CALL_FUNCTION_512   512 
         671  STORE_FAST           20  'ui'

  81     674  LOAD_FAST            20  'ui'
         677  LOAD_ATTR            39  'set_close_after_successfully_jump'
         680  LOAD_FAST             3  'close_after_jump'
         683  CALL_FUNCTION_1       1 
         686  POP_TOP          

  82     687  LOAD_FAST            20  'ui'
         690  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_512' instruction at offset 138


def groceries_use_confirmUI--- This code section failed: ---

  85       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'ui_mgr'
           6  LOAD_ATTR             2  'close_ui'
           9  LOAD_CONST            1  'GroceriesUseConfirmUI'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  86      16  LOAD_GLOBAL           3  'GroceriesUseConfirmUI'
          19  LOAD_CONST            2  'goods_id'
          22  LOAD_CONST            3  'pay_num'
          25  LOAD_FAST             1  'pay_num'
          28  CALL_FUNCTION_512   512 
          31  POP_TOP          

Parse error at or near `CALL_FUNCTION_512' instruction at offset 28


def item_skin_buy_confirmUI--- This code section failed: ---

  89       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'ui_mgr'
           6  LOAD_ATTR             2  'close_ui'
           9  LOAD_CONST            1  'ItemSkinBuyConfirmUI'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  90      16  LOAD_GLOBAL           3  'ItemSkinBuyConfirmUI'
          19  LOAD_CONST            2  'goods_id'
          22  LOAD_CONST            3  'pick_list'
          25  LOAD_FAST             1  'pick_list'
          28  CALL_FUNCTION_512   512 
          31  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_512' instruction at offset 28


def meow_upgrade_confirmUI(goods_id):
    global_data.ui_mgr.close_ui('MeowUpgradeConfirmUI')
    MeowUpgradeConfirmUI(goods_id=goods_id)


def tickets_buy_confirmUI--- This code section failed: ---

  97       0  LOAD_GLOBAL           0  'mall_utils'
           3  LOAD_ATTR             1  'get_mall_item_price'
           6  LOAD_FAST             0  'goods_id'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            3  'prices'

  98      15  LOAD_FAST             3  'prices'
          18  POP_JUMP_IF_FALSE    92  'to 92'
          21  LOAD_GLOBAL           2  'len'
          24  LOAD_FAST             3  'prices'
          27  CALL_FUNCTION_1       1 
          30  LOAD_CONST            1  2
          33  COMPARE_OP            2  '=='
        36_0  COME_FROM                '18'
          36  POP_JUMP_IF_FALSE    92  'to 92'

  99      39  LOAD_GLOBAL           3  'global_data'
          42  LOAD_ATTR             4  'ui_mgr'
          45  LOAD_ATTR             5  'close_ui'
          48  LOAD_CONST            2  'GroceriesBothBuyConfirmUI'
          51  CALL_FUNCTION_1       1 
          54  POP_TOP          

 100      55  LOAD_GLOBAL           6  'GroceriesBothBuyConfirmUI'
          58  LOAD_CONST            3  'goods_id'
          61  LOAD_CONST            4  'pick_list'
          64  LOAD_FAST             2  'pick_list'
          67  LOAD_CONST            5  'need_show'
          70  LOAD_CONST            0  ''
          73  LOAD_CONST            6  'init_quantity'
          76  LOAD_FAST             1  'count'
          79  LOAD_CONST            7  'force_change_init_quantity'
          82  LOAD_GLOBAL           8  'True'
          85  CALL_FUNCTION_1280  1280 
          88  POP_TOP          
          89  JUMP_FORWARD         50  'to 142'

 102      92  LOAD_GLOBAL           3  'global_data'
          95  LOAD_ATTR             4  'ui_mgr'
          98  LOAD_ATTR             5  'close_ui'
         101  LOAD_CONST            8  'GroceriesBuyConfirmUI'
         104  CALL_FUNCTION_1       1 
         107  POP_TOP          

 103     108  LOAD_GLOBAL           9  'GroceriesBuyConfirmUI'
         111  LOAD_CONST            3  'goods_id'
         114  LOAD_CONST            4  'pick_list'
         117  LOAD_FAST             2  'pick_list'
         120  LOAD_CONST            5  'need_show'
         123  LOAD_CONST            0  ''
         126  LOAD_CONST            6  'init_quantity'
         129  LOAD_FAST             1  'count'
         132  LOAD_CONST            7  'force_change_init_quantity'
         135  LOAD_GLOBAL           8  'True'
         138  CALL_FUNCTION_1280  1280 
         141  POP_TOP          
       142_0  COME_FROM                '89'
         142  LOAD_CONST            0  ''
         145  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1280' instruction at offset 85