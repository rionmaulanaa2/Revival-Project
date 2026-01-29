# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityYuanbaoStrike.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.comsys.activity.widget import widget
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price, get_goods_item_task_id
from logic.client.const import mall_const
from logic.gutils.activity_utils import is_activity_in_limit_time
from logic.gutils.jump_to_ui_utils import jump_to_web_charge
from logic.gcommon.item.item_const import ITEM_RECEIVED
from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
import random
import cc
from logic.gcommon.cdata import loop_activity_data

@widget('AsyncYuanbaoStrikeTaskListWidget', 'YuanbaoStrikeDescribeWidget')
class ActivityYuanbaoStrike(ActivityBase):
    STRIKE_TAG = 20240102

    def __init__(self, dlg, activity_type):
        super(ActivityYuanbaoStrike, self).__init__(dlg, activity_type)
        self.init_parameters()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._game_goods_id = str(ui_data.get('goods_id'))
        self._pay_task_id = get_goods_item_task_id(str(self._game_goods_id))
        self._activity_task_id = conf.get('cTask', '')
        self._jelly_goods_info = None
        reward_id = task_utils.get_task_reward(self._pay_task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        self._base_yuanbao_cnt = item_num
        goods_list = getattr(mall_const, ui_data.get('goods_list', ''))
        if not goods_list:
            log_error('!!!!ActivityYuanbaoStrike: Goods list name invalid!!!!')
        self._jelly_goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
        return

    def init_btn_buy(self, *args):
        if not global_data.player:
            return
        btn_buy = self.panel.btn_click
        lab_buy = self.panel.lab_buy
        nd_buy = self.panel.nd_buy
        has_bought = limite_pay(self._game_goods_id)
        has_received = ITEM_RECEIVED == global_data.player.get_task_reward_status(self._pay_task_id)
        if has_bought:
            if has_received:
                btn_buy.SetEnable(False)
                btn_buy.SetText(604029)
            else:
                btn_buy.SetEnable(True)
                btn_buy.SetText(635217)
            nd_buy.setVisible(False)
        elif not self._jelly_goods_info:
            btn_buy.SetEnable(False)
            btn_buy.SetText(12121)
            nd_buy.setVisible(False)
        else:
            if is_pc_global_pay() or is_steam_pay():
                price_txt = get_pc_charge_price_str(self._jelly_goods_info)
            else:
                price_txt = get_charge_price_str(self._jelly_goods_info['goodsid'])
            adjusted_price = adjust_price(str(price_txt))
            btn_buy.SetEnable(True)
            btn_buy.SetText('')
            lab_buy.SetString(get_text_by_id(635214).format(adjusted_price))
            nd_buy.setVisible(True)

    def init_strike_widget(self, times_change=0):
        if loop_activity_data.is_loop_activity(self._activity_type):
            strike_times = global_data.player.get_loop_yuanbao_strike_times()
        else:
            strike_times = global_data.player.get_yuanbao_strike_times()
        yuanbao_num = int(round(self._base_yuanbao_cnt * strike_times))
        self.panel.lab_got.SetString(get_text_by_id(635220).format(yuanbao_num))
        need_vx = times_change > 0
        if not need_vx:
            self.panel.lab_value.SetString('x%.1f' % strike_times)
        else:
            lab_add = self.panel.lab_add
            nd_add = self.panel.nd_add
            if not times_change or not lab_add or not lab_add.isValid():
                return
            lab_add.SetString('+%.1f' % times_change)
            delta_x = random.randint(-20, 20)
            delta_y = random.randint(-20, 20)
            nd_add.SetPosition('50%{}'.format(delta_x), '50%{}'.format(delta_y))
            self.panel.PlayAnimation('tips')
            act_list = [
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('tips')),
             cc.DelayTime.create(max(0.1, self.panel.GetAnimationMaxRunTime('tips') - 0.1)),
             cc.CallFunc.create(lambda : self.set_lab_value(strike_times)),
             cc.CallFunc.create(lambda : global_data.sound_mgr.play_ui_sound('ui_fetters_send_gifts'))]
            act = cc.Sequence.create(act_list)
            self.panel.runAction(act)
            act.setTag(self.STRIKE_TAG)
            global_data.sound_mgr.play_ui_sound('ui_luckyball_burst_golden')

    def set_lab_value(self, strike_times):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.lab_value.SetString('x%.1f' % strike_times)

    def on_init_panel(self):
        super(ActivityYuanbaoStrike, self).on_init_panel()
        self.init_btn_buy()
        self.init_strike_widget()
        self.process_event(True)
        self.panel.PlayAnimation('loop')

        @self.panel.btn_click.unique_callback()
        def OnClick(*args):
            self.on_click_btn_buy()

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.stopActionByTag(self.STRIKE_TAG)
        super(ActivityYuanbaoStrike, self).on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.init_btn_buy,
           'yuanbao_strike_times_change': self.init_strike_widget,
           'receive_task_reward_succ_event': self.init_btn_buy
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_click_btn_buy(self, *args):
        if not global_data.player:
            return
        if loop_activity_data.is_loop_activity(self._activity_type):
            is_activity_end = not loop_activity_data.is_loop_task_open(self._activity_type)
        else:
            is_activity_end = not task_utils.is_task_open(self._activity_task_id)
        has_received = ITEM_RECEIVED == global_data.player.get_task_reward_status(self._pay_task_id)
        if has_received:
            return
        has_bought = limite_pay(self._game_goods_id)
        if is_activity_end and not has_bought:
            global_data.game_mgr.show_tip(607911)
            return
        if has_bought:
            self._do_receive()
        else:
            self._do_buy()

    def _do_buy(self):
        if is_pc_global_pay():
            jump_to_web_charge()
        elif self._jelly_goods_info:
            global_data.player and global_data.player.pay_order(self._jelly_goods_info['goodsid'])

    def _do_receive(self):
        if not global_data.player:
            return
        if not global_data.player.is_all_received_reward(self._activity_task_id):
            LotterySmallSecondConfirmWidget(title_text_id=331, content_text_id=635218, confirm_callback=self._receive_yuanbao)
        else:
            self._receive_yuanbao()

    def _receive_yuanbao(self):
        global_data.player.receive_task_reward(self._pay_task_id)

    @staticmethod
    def show_tab_rp--- This code section failed: ---

 193       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 194       9  LOAD_GLOBAL           2  'False'
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 195      13  LOAD_GLOBAL           0  'global_data'
          16  LOAD_ATTR             1  'player'
          19  STORE_FAST            2  'player'

 196      22  LOAD_GLOBAL           3  'confmgr'
          25  LOAD_ATTR             4  'get'
          28  LOAD_CONST            1  'c_activity_config'
          31  LOAD_CONST            2  'default'
          34  BUILD_MAP_0           0 
          37  CALL_FUNCTION_258   258 
          40  STORE_FAST            3  'conf'

 197      43  LOAD_FAST             3  'conf'
          46  LOAD_ATTR             4  'get'
          49  LOAD_CONST            3  'cUiData'
          52  BUILD_MAP_0           0 
          55  CALL_FUNCTION_2       2 
          58  STORE_FAST            4  'ui_data'

 198      61  LOAD_GLOBAL           5  'str'
          64  LOAD_FAST             4  'ui_data'
          67  LOAD_ATTR             4  'get'
          70  LOAD_CONST            4  'goods_id'
          73  CALL_FUNCTION_1       1 
          76  CALL_FUNCTION_1       1 
          79  STORE_FAST            5  'game_goods_id'

 199      82  LOAD_GLOBAL           6  'get_goods_item_task_id'
          85  LOAD_GLOBAL           5  'str'
          88  LOAD_FAST             5  'game_goods_id'
          91  CALL_FUNCTION_1       1 
          94  CALL_FUNCTION_1       1 
          97  STORE_FAST            6  'pay_task_id'

 200     100  LOAD_FAST             3  'conf'
         103  LOAD_ATTR             4  'get'
         106  LOAD_CONST            5  'cTask'
         109  LOAD_CONST            6  ''
         112  CALL_FUNCTION_2       2 
         115  STORE_FAST            7  'activity_task_id'

 201     118  LOAD_FAST             4  'ui_data'
         121  LOAD_ATTR             4  'get'
         124  LOAD_CONST            7  'free_tasks'
         127  BUILD_LIST_0          0 
         130  CALL_FUNCTION_2       2 
         133  STORE_FAST            8  'free_tasks'

 202     136  LOAD_GLOBAL           7  'limite_pay'
         139  LOAD_FAST             5  'game_goods_id'
         142  CALL_FUNCTION_1       1 
         145  STORE_FAST            9  'has_bought'

 204     148  LOAD_FAST             2  'player'
         151  LOAD_ATTR             8  'has_receive_reward'
         154  LOAD_GLOBAL           5  'str'
         157  LOAD_FAST             6  'pay_task_id'
         160  CALL_FUNCTION_1       1 
         163  CALL_FUNCTION_1       1 
         166  POP_JUMP_IF_FALSE   173  'to 173'

 205     169  LOAD_GLOBAL           2  'False'
         172  RETURN_END_IF    
       173_0  COME_FROM                '166'

 207     173  LOAD_FAST             2  'player'
         176  LOAD_ATTR             9  'has_unreceived_task_reward'
         179  LOAD_GLOBAL           5  'str'
         182  LOAD_FAST             6  'pay_task_id'
         185  CALL_FUNCTION_1       1 
         188  CALL_FUNCTION_1       1 
         191  POP_JUMP_IF_FALSE   198  'to 198'

 208     194  LOAD_GLOBAL          10  'True'
         197  RETURN_END_IF    
       198_0  COME_FROM                '191'

 210     198  LOAD_GLOBAL          11  'loop_activity_data'
         201  LOAD_ATTR            12  'is_loop_activity'
         204  LOAD_FAST             0  'activity_type'
         207  CALL_FUNCTION_1       1 
         210  POP_JUMP_IF_FALSE   231  'to 231'

 211     213  LOAD_GLOBAL          11  'loop_activity_data'
         216  LOAD_ATTR            13  'is_loop_task_open'
         219  LOAD_FAST             0  'activity_type'
         222  CALL_FUNCTION_1       1 
         225  STORE_FAST           10  'is_activity_task_open'
         228  JUMP_FORWARD         15  'to 246'

 213     231  LOAD_GLOBAL          14  'task_utils'
         234  LOAD_ATTR            15  'is_task_open'
         237  LOAD_FAST             7  'activity_task_id'
         240  CALL_FUNCTION_1       1 
         243  STORE_FAST           10  'is_activity_task_open'
       246_0  COME_FROM                '228'

 215     246  LOAD_FAST             9  'has_bought'
         249  POP_JUMP_IF_FALSE   283  'to 283'
         252  LOAD_FAST            10  'is_activity_task_open'
         255  POP_JUMP_IF_FALSE   283  'to 283'
         258  LOAD_FAST             2  'player'
         261  LOAD_ATTR             9  'has_unreceived_task_reward'
         264  LOAD_GLOBAL           5  'str'
         267  LOAD_FAST             7  'activity_task_id'
         270  CALL_FUNCTION_1       1 
         273  CALL_FUNCTION_1       1 
       276_0  COME_FROM                '255'
       276_1  COME_FROM                '249'
         276  POP_JUMP_IF_FALSE   283  'to 283'

 216     279  LOAD_GLOBAL          10  'True'
         282  RETURN_END_IF    
       283_0  COME_FROM                '276'

 218     283  LOAD_GLOBAL           2  'False'
         286  STORE_FAST           11  'has_unreceived_free_task'

 219     289  SETUP_LOOP           45  'to 337'
         292  LOAD_FAST             8  'free_tasks'
         295  GET_ITER         
         296  FOR_ITER             37  'to 336'
         299  STORE_FAST           12  'task_id'

 220     302  LOAD_FAST             2  'player'
         305  LOAD_ATTR             9  'has_unreceived_task_reward'
         308  LOAD_GLOBAL           5  'str'
         311  LOAD_FAST            12  'task_id'
         314  CALL_FUNCTION_1       1 
         317  CALL_FUNCTION_1       1 
         320  POP_JUMP_IF_FALSE   296  'to 296'

 221     323  LOAD_GLOBAL          10  'True'
         326  STORE_FAST           11  'has_unreceived_free_task'

 222     329  BREAK_LOOP       
         330  JUMP_BACK           296  'to 296'
         333  JUMP_BACK           296  'to 296'
         336  POP_BLOCK        
       337_0  COME_FROM                '289'

 224     337  LOAD_FAST             9  'has_bought'
         340  UNARY_NOT        
         341  POP_JUMP_IF_FALSE   360  'to 360'
         344  LOAD_FAST            10  'is_activity_task_open'
         347  POP_JUMP_IF_FALSE   360  'to 360'
         350  LOAD_FAST            11  'has_unreceived_free_task'
       353_0  COME_FROM                '347'
       353_1  COME_FROM                '341'
         353  POP_JUMP_IF_FALSE   360  'to 360'

 225     356  LOAD_GLOBAL          10  'True'
         359  RETURN_END_IF    
       360_0  COME_FROM                '353'

 227     360  LOAD_GLOBAL           2  'False'
         363  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_258' instruction at offset 37