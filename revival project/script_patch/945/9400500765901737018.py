# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/NewRoleChargeWidgetNew.py
from __future__ import absolute_import
from six.moves import range
import six
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import jump_to_ui_utils
import logic.gcommon.time_utility as tutil
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from cocosui import cc, ccui, ccs
from common.platform.dctool import interface
from logic.gutils.mall_utils import is_pc_global_pay, is_steam_pay, get_goods_item_reward_id, get_goods_item_task_id, buy_num_limit_by_all, limite_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price
from logic.gutils.template_utils import init_tempate_mall_i_item, get_left_info
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.common_utils.local_text import get_text_by_id

class NewRoleChargeWidgetNew(object):

    def on_init_panel(self, panel, parent_ui_cls_name='ChargeUINew'):
        self.panel = panel
        self._timer = 0
        self._timer_cb = {}
        self.is_pc_global_pay = is_pc_global_pay()
        self._goods_list = [
         '20603504', '20603502', '20603503']
        self._na_names = [
         609041, 609042, 609043]
        self._ch_names = [607474, 607475, 608543]
        self._na_desc = []
        self._ch_desc = [
         608544, 608545, 608546]
        self._na_icons = [
         'gui/ui_res_2/charge/icon_gifts_new_1.png', 'gui/ui_res_2/charge/icon_gifts_new_2.png', 'gui/ui_res_2/charge/icon_gifts_new_3.png']
        self._ch_icons = ['gui/ui_res_2/charge/icon_gifts_beginner_1.png', 'gui/ui_res_2/charge/icon_gifts_beginner_2.png', 'gui/ui_res_2/charge/icon_gifts_beginner_3.png']
        self._na_shadows = [
         'gui/ui_res_2/charge/new_player_gifts/img_shadow2.png', 'gui/ui_res_2/charge/new_player_gifts/img_shadow3.png', 'gui/ui_res_2/charge/new_player_gifts/img_shadow.png']
        self._ch_shadows = ['gui/ui_res_2/charge/new_player_gifts/img_shadow2.png', 'gui/ui_res_2/charge/new_player_gifts/img_shadow3.png', 'gui/ui_res_2/charge/new_player_gifts/img_shadow.png']
        self._na_tags = [
         607436, 12111]
        self._ch_tags = [81048, 12151]
        if not G_IS_NA_PROJECT:
            self._names = self._ch_names
            self._desc = self._ch_desc
            self._icons = self._ch_icons
            self._shadows = self._ch_shadows
            self._tags = self._ch_tags
        else:
            self._names = self._na_names
            self._desc = self._na_desc
            self._icons = self._na_icons
            self._shadows = self._na_shadows
            self._tags = self._na_tags
        self._parent_ui_cls_name = parent_ui_cls_name
        self.panel.ReConfPosition()
        from logic.comsys.activity.NewAlphaPlan.AlphaPlanMainUI import AlphaPlanMainUI
        if parent_ui_cls_name == AlphaPlanMainUI.__name__:
            X, Y = self.panel.GetPosition()
            self.panel.SetPosition(X + 84, Y)
        self.init_event()
        self.register_timer()
        self.init_widget()
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(3.0),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]
        self.panel.runAction(cc.Sequence.create(action_list))
        if global_data.ui_lifetime_log_mgr:
            page_name = '{}_{}'.format(self._parent_ui_cls_name, self.__class__.__name__)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(self._parent_ui_cls_name, page_name)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_task_reward,
           'receive_task_reward_succ_event': self.refresh_task_reward,
           'buy_good_success': self.refresh_goods_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_reward_list(self, nd_list, goods_id):
        multiply = get_text_by_id(602012)
        reward_id = get_goods_item_reward_id(goods_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        acts = []
        nd_list.DeleteAllSubItem()
        for index, (item_no, item_count) in enumerate(reward_list):
            reward_item = nd_list.AddTemplateItem()
            init_tempate_mall_i_item(reward_item.nd_item, item_no, 1, show_tips=True, show_rare_vx=True)
            reward_item.lab_name.SetString(get_lobby_item_name(item_no))
            reward_item.lab_num.SetString(multiply + str(item_count))
            acts.append(cc.CallFunc.create(lambda item=reward_item: item.PlayAnimation('show')))
            acts.append(cc.DelayTime.create(0.06))

        self.panel.runAction(cc.Sequence.create(acts))

    def on_finalize_panel(self):
        self.panel and self.panel.stopAllActions()
        self.panel = None
        self.unregister_timer()
        self.process_event(False)
        if global_data.ui_lifetime_log_mgr:
            page_name = '{}_{}'.format(self._parent_ui_cls_name, self.__class__.__name__)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(self._parent_ui_cls_name, page_name)
        return

    def set_show(self, show):
        if self.panel:
            self.panel.setVisible(show)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def init_widget(self):
        for i in range(3):
            charge_item = self.panel.charge_list.GetItem(i)
            charge_item.nd_gift_common.setVisible(False)
            charge_item.nd_gift_special.setVisible(False)

        def callback():
            if not self.panel.lab_time:
                return
            now_time = tutil.get_server_time()
            expire_ts = global_data.player.get_newbie_gift_expire_ts()
            left_time = expire_ts - now_time
            if left_time <= 0 and activity_utils.has_new_role_12_goods_reward(all_done=True):
                self.panel.lab_time.SetString(607454)
            elif left_time <= 0:
                self.panel.lab_time.SetString(606071)
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))

        self._timer_cb[0] = callback
        callback()
        goods_id = self._goods_list[0]
        charge_item = self.panel.charge_list.GetItem(0)
        charge_item.lab_title_1.SetString(self._names[0])
        charge_item.nd_gift_common.pnl_main_special.lab_text1.SetString(self._desc[0])
        charge_item.img_item_common.SetDisplayFrameByPath('', self._icons[0])
        nd_list = charge_item.list_item_1
        task_id = get_goods_item_task_id(goods_id)
        children_tasks = task_utils.get_children_task(task_id)
        total_prog = task_utils.get_total_prog(task_id)
        cur_prog = global_data.player.get_task_prog(task_id)
        has_bought = limite_pay(goods_id)
        can_receive_task = []
        nd_list.DeleteAllSubItem()

        def init_sub_task_end():
            self.play_charge_item_anim(charge_item, False)
            self.refresh_goods_reward()

        def init_sub_task--- This code section failed: ---

 191       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  UNARY_NOT        
           7  POP_JUMP_IF_TRUE     29  'to 29'
          10  LOAD_DEREF            1  'nd_list'
          13  UNARY_NOT        
          14  POP_JUMP_IF_TRUE     29  'to 29'
          17  LOAD_DEREF            1  'nd_list'
          20  LOAD_ATTR             1  'IsDestroyed'
          23  CALL_FUNCTION_0       0 
        26_0  COME_FROM                '14'
        26_1  COME_FROM                '7'
          26  POP_JUMP_IF_FALSE    33  'to 33'

 192      29  LOAD_CONST            0  ''
          32  RETURN_END_IF    
        33_0  COME_FROM                '26'

 194      33  LOAD_DEREF            1  'nd_list'
          36  LOAD_ATTR             2  'AddTemplateItem'
          39  CALL_FUNCTION_0       0 
          42  STORE_FAST            1  'nd_day'

 196      45  LOAD_FAST             1  'nd_day'
          48  LOAD_ATTR             3  'lab_day'
          51  LOAD_ATTR             4  'setString'
          54  LOAD_GLOBAL           5  'get_text_by_id'
          57  LOAD_CONST            1  604004
          60  CALL_FUNCTION_1       1 
          63  LOAD_ATTR             6  'format'
          66  LOAD_ATTR             2  'AddTemplateItem'
          69  BINARY_ADD       
          70  CALL_FUNCTION_1       1 
          73  CALL_FUNCTION_1       1 
          76  POP_TOP          

 197      77  LOAD_DEREF            2  'has_bought'
          80  POP_JUMP_IF_TRUE    102  'to 102'

 198      83  LOAD_FAST             1  'nd_day'
          86  LOAD_ATTR             7  'img_today'
          89  LOAD_ATTR             8  'setVisible'
          92  LOAD_GLOBAL           9  'False'
          95  CALL_FUNCTION_1       1 
          98  POP_TOP          
          99  JUMP_FORWARD         26  'to 128'

 200     102  LOAD_FAST             1  'nd_day'
         105  LOAD_ATTR             7  'img_today'
         108  LOAD_ATTR             8  'setVisible'
         111  LOAD_FAST             0  'i'
         114  LOAD_DEREF            3  'cur_prog'
         117  LOAD_CONST            2  1
         120  BINARY_SUBTRACT  
         121  COMPARE_OP            2  '=='
         124  CALL_FUNCTION_1       1 
         127  POP_TOP          
       128_0  COME_FROM                '99'

 201     128  LOAD_GLOBAL          10  'task_utils'
         131  LOAD_ATTR            11  'get_task_reward'
         134  LOAD_DEREF            4  'children_tasks'
         137  LOAD_FAST             0  'i'
         140  BINARY_SUBSCR    
         141  CALL_FUNCTION_1       1 
         144  STORE_FAST            2  'reward_id'

 202     147  LOAD_GLOBAL          12  'template_utils'
         150  LOAD_ATTR            13  'init_common_reward_list'
         153  LOAD_FAST             1  'nd_day'
         156  LOAD_ATTR            14  'list_items'
         159  LOAD_FAST             2  'reward_id'
         162  CALL_FUNCTION_2       2 
         165  POP_TOP          

 203     166  LOAD_FAST             1  'nd_day'
         169  LOAD_ATTR            14  'list_items'
         172  STORE_FAST            3  'list_item'

 204     175  LOAD_FAST             3  'list_item'
         178  LOAD_ATTR            15  'DeleteAllSubItem'
         181  CALL_FUNCTION_0       0 
         184  POP_TOP          

 205     185  LOAD_FAST             2  'reward_id'
         188  POP_JUMP_IF_FALSE   365  'to 365'

 206     191  LOAD_GLOBAL          16  'confmgr'
         194  LOAD_ATTR            17  'get'
         197  LOAD_CONST            3  'common_reward_data'
         200  LOAD_GLOBAL          18  'str'
         203  LOAD_FAST             2  'reward_id'
         206  CALL_FUNCTION_1       1 
         209  CALL_FUNCTION_2       2 
         212  STORE_FAST            4  'reward_conf'

 207     215  LOAD_FAST             4  'reward_conf'
         218  POP_JUMP_IF_TRUE    238  'to 238'

 208     221  LOAD_GLOBAL          19  'log_error'
         224  LOAD_CONST            4  'reward_id is not exist in common_reward_data'
         227  LOAD_FAST             2  'reward_id'
         230  CALL_FUNCTION_2       2 
         233  POP_TOP          

 209     234  LOAD_CONST            0  ''
         237  RETURN_END_IF    
       238_0  COME_FROM                '218'

 210     238  LOAD_FAST             4  'reward_conf'
         241  LOAD_ATTR            17  'get'
         244  LOAD_CONST            5  'reward_list'
         247  BUILD_LIST_0          0 
         250  CALL_FUNCTION_2       2 
         253  STORE_FAST            5  'reward_list'

 211     256  LOAD_GLOBAL          20  'len'
         259  LOAD_FAST             5  'reward_list'
         262  CALL_FUNCTION_1       1 
         265  STORE_FAST            6  'reward_count'

 212     268  SETUP_LOOP           94  'to 365'
         271  LOAD_GLOBAL          21  'range'
         274  LOAD_FAST             6  'reward_count'
         277  CALL_FUNCTION_1       1 
         280  GET_ITER         
         281  FOR_ITER             77  'to 361'
         284  STORE_FAST            7  'idx'

 213     287  LOAD_FAST             5  'reward_list'
         290  LOAD_FAST             7  'idx'
         293  BINARY_SUBSCR    
         294  UNPACK_SEQUENCE_2     2 
         297  STORE_FAST            8  'item_no'
         300  STORE_FAST            9  'item_num'

 214     303  LOAD_FAST             3  'list_item'
         306  LOAD_ATTR             2  'AddTemplateItem'
         309  CALL_FUNCTION_0       0 
         312  STORE_FAST           10  'reward_item'

 215     315  LOAD_GLOBAL          22  'init_tempate_mall_i_item'

 216     318  LOAD_FAST            10  'reward_item'
         321  LOAD_FAST             8  'item_no'
         324  LOAD_FAST             9  'item_num'

 217     327  LOAD_DEREF            2  'has_bought'
         330  JUMP_IF_FALSE_OR_POP   342  'to 342'
         333  LOAD_FAST             0  'i'
         336  LOAD_DEREF            3  'cur_prog'
         339  COMPARE_OP            0  '<'
       342_0  COME_FROM                '330'
         342  LOAD_CONST            6  'show_tips'
         345  LOAD_GLOBAL          23  'True'
         348  LOAD_CONST            7  'show_rare_vx'
         351  LOAD_GLOBAL          23  'True'
         354  CALL_FUNCTION_516   516 
         357  POP_TOP          
         358  JUMP_BACK           281  'to 281'
         361  POP_BLOCK        
       362_0  COME_FROM                '268'
         362  JUMP_FORWARD          0  'to 365'
       365_0  COME_FROM                '268'

 218     365  LOAD_FAST             1  'nd_day'
         368  LOAD_ATTR            24  'PlayAnimation'
         371  LOAD_CONST            8  'show'
         374  CALL_FUNCTION_1       1 
         377  POP_TOP          

 219     378  LOAD_FAST             0  'i'
         381  LOAD_GLOBAL          20  'len'
         384  LOAD_DEREF            4  'children_tasks'
         387  CALL_FUNCTION_1       1 
         390  LOAD_CONST            2  1
         393  BINARY_SUBTRACT  
         394  COMPARE_OP            0  '<'
         397  POP_JUMP_IF_FALSE   423  'to 423'

 220     400  LOAD_GLOBAL          25  'global_data'
         403  LOAD_ATTR            26  'game_mgr'
         406  LOAD_ATTR            27  'next_exec'
         409  LOAD_DEREF            5  'init_sub_task'
         412  LOAD_DEREF            2  'has_bought'
         415  BINARY_ADD       
         416  CALL_FUNCTION_2       2 
         419  POP_TOP          
         420  JUMP_FORWARD         16  'to 439'

 222     423  LOAD_GLOBAL          25  'global_data'
         426  LOAD_ATTR            26  'game_mgr'
         429  LOAD_ATTR            27  'next_exec'
         432  LOAD_DEREF            6  'init_sub_task_end'
         435  CALL_FUNCTION_1       1 
         438  POP_TOP          
       439_0  COME_FROM                '420'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70

        global_data.game_mgr.next_exec(global_data.game_mgr.next_exec, global_data.game_mgr.next_exec, init_sub_task, 0)

    def play_charge_item_anim(self, charge_item, is_special):
        show_anim, loop_anim = ('show', 'loop')
        if is_special:
            show_anim, loop_anim = ('show_02', 'loop_02')
        action_list = [cc.CallFunc.create(lambda : charge_item.PlayAnimation(show_anim)),
         cc.DelayTime.create(2.5),
         cc.CallFunc.create(lambda : charge_item.PlayAnimation(loop_anim))]
        charge_item.runAction(cc.Sequence.create(action_list))

    def refresh_btns(self):
        if not self.panel:
            return
        count = self.panel.charge_list.GetItemCount()
        for i in range(count):
            item_widget = self.panel.charge_list.GetItem(i)
            btn = item_widget.btn_buy_special
            btn_vx = btn.vx_button
            if i == 0:
                btn = item_widget.btn_buy_common
                btn_vx = btn.vx_button
            if not btn.btn_buy.IsEnable():
                btn_vx.setVisible(False)

    def refresh_goods_reward(self):
        if not self.panel:
            return
        self.refresh_task_reward()
        now_time = tutil.get_server_time()
        expire_ts = global_data.player.get_newbie_gift_expire_ts()
        left_time = expire_ts - now_time
        goods_lists = [
         'NEW_ROLE_6_GOODS' if G_IS_NA_PROJECT else 'NEW_ROLE_12_GOODS',
         'NEW_ROLE_30_GOODS']
        price_before = [
         '\xef\xbf\xa556', '\xef\xbf\xa586']
        icons = [self._icons[1], self._icons[2]]
        shadows = [self._shadows[1], self._shadows[2]]
        for i, goods_list in enumerate(goods_lists):
            item_widget = self.panel.charge_list.GetItem(i + 1)
            item_widget.lab_title_2.SetString(self._names[i + 1])
            item_widget.nd_gift_special.pnl_main_special.lab_text1.SetString(self._desc[i + 1])
            item_widget.img_item_special.SetDisplayFrameByPath('', icons[i])
            item_widget.img_item_special.img_shadow.SetDisplayFrameByPath('', shadows[i])
            show_pnl_info = bool(i == 1 and global_data.player.get_reward_count(six.text_type('14010007')) == 0)
            item_widget.pnl_info.setVisible(show_pnl_info)
            goods_id = self._goods_list[i + 1]
            self.init_reward_list(item_widget.list_item_2, goods_id)
            self.play_charge_item_anim(item_widget, True)
            has_bought = limite_pay(goods_id)
            item_widget.lab_limit_special.SetString(81172)
            btn_buy = item_widget.btn_buy_special.btn_buy
            lab_price = btn_buy.lab_price_common.lab_price
            lab_price.lab_price_before.SetString(price_before[i])
            if has_bought:
                btn_buy.SetEnable(False)
                lab_price.setVisible(False)
                btn_buy.SetText(12014)
            else:
                goods_info = global_data.lobby_mall_data.get_activity_sale_info(goods_list)
                if not goods_info:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText('******')
                elif left_time <= 0:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText(81154)
                else:
                    btn_buy.SetEnable(True)
                    lab_price.setVisible(True)
                    btn_buy.SetText('')
                    if self.is_pc_global_pay or is_steam_pay():
                        price_txt = get_pc_charge_price_str(goods_info)
                    else:
                        key = goods_info['goodsid']
                        price_txt = get_charge_price_str(key)
                    lab_price.SetString(adjust_price(str(price_txt)))

                    @btn_buy.unique_callback()
                    def OnClick(btn, touch, _goods_info=goods_info):
                        if self.is_pc_global_pay:
                            jump_to_ui_utils.jump_to_web_charge()
                        elif _goods_info:
                            global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

        self.refresh_btns()

    def refresh_task_reward(self, *args):
        if not self.panel:
            return
        goods_id = self._goods_list[0]
        task_id = get_goods_item_task_id(goods_id)
        children_tasks = task_utils.get_children_task(task_id)
        charge_item = self.panel.charge_list.GetItem(0)
        nd_list = charge_item.list_item_1
        if nd_list.GetItemCount() < len(children_tasks):
            return
        total_prog = task_utils.get_total_prog(task_id)
        cur_prog = global_data.player.get_task_prog(task_id)
        has_bought = limite_pay(goods_id)
        can_receive_task = []

        def init_sub_task_end():
            if not self.panel or not charge_item or charge_item.IsDestroyed():
                return
            btn_buy = charge_item.btn_buy_common.btn_buy
            lab_price = btn_buy.lab_price_common.lab_price
            lab_price.lab_price_before.SetString('\xef\xbf\xa536')
            if not has_bought:
                charge_item.lab_limit_common.SetString(81172)
                goods_info = global_data.lobby_mall_data.get_activity_sale_info('NEW_ROLE_12_GOODS' if G_IS_NA_PROJECT else 'NEW_ROLE_6_GOODS')
                if not goods_info:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText('******')
                else:
                    btn_buy.SetEnable(True)
                    lab_price.setVisible(True)
                    btn_buy.SetText('')
                    if self.is_pc_global_pay or is_steam_pay():
                        price_txt = get_pc_charge_price_str(goods_info)
                    else:
                        key = goods_info['goodsid']
                        price_txt = get_charge_price_str(key)
                    lab_price.SetString(adjust_price(str(price_txt)))

                    @btn_buy.unique_callback()
                    def OnClick(btn, touch, _goods_info=goods_info):
                        if self.is_pc_global_pay:
                            jump_to_ui_utils.jump_to_web_charge()
                        elif _goods_info:
                            global_data.player and global_data.player.pay_order(_goods_info['goodsid'])

            else:
                can_receive_count = len(can_receive_task)
                charge_item.lab_limit_common.SetString(get_text_by_id(607411).format(get_text_by_id(556685).format(can_receive_count)))
                if can_receive_task and can_receive_count > total_prog - cur_prog:
                    btn_buy.SetEnable(True)
                    lab_price.setVisible(False)
                    btn_buy.SetText(80930)
                else:
                    btn_buy.SetEnable(False)
                    lab_price.setVisible(False)
                    btn_buy.SetText(606011)

                @btn_buy.unique_callback()
                def OnClick(btn, touch):
                    for sub_task_id in can_receive_task:
                        global_data.player.receive_task_reward(sub_task_id)

            self.refresh_btns()

        def init_sub_task--- This code section failed: ---

 415       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  UNARY_NOT        
           7  POP_JUMP_IF_TRUE     29  'to 29'
          10  LOAD_DEREF            1  'nd_list'
          13  UNARY_NOT        
          14  POP_JUMP_IF_TRUE     29  'to 29'
          17  LOAD_DEREF            1  'nd_list'
          20  LOAD_ATTR             1  'IsDestroyed'
          23  CALL_FUNCTION_0       0 
        26_0  COME_FROM                '14'
        26_1  COME_FROM                '7'
          26  POP_JUMP_IF_FALSE    33  'to 33'

 416      29  LOAD_CONST            0  ''
          32  RETURN_END_IF    
        33_0  COME_FROM                '26'

 418      33  LOAD_DEREF            2  'children_tasks'
          36  LOAD_FAST             0  'i'
          39  BINARY_SUBSCR    
          40  STORE_FAST            1  'sub_task_id'

 419      43  LOAD_DEREF            1  'nd_list'
          46  LOAD_ATTR             2  'GetItem'
          49  LOAD_FAST             0  'i'
          52  CALL_FUNCTION_1       1 
          55  STORE_FAST            2  'nd_day'

 420      58  LOAD_FAST             2  'nd_day'
          61  LOAD_ATTR             3  'lab_day'
          64  LOAD_ATTR             4  'setString'
          67  LOAD_GLOBAL           5  'get_text_by_id'
          70  LOAD_CONST            1  604004
          73  CALL_FUNCTION_1       1 
          76  LOAD_ATTR             6  'format'
          79  LOAD_ATTR             2  'GetItem'
          82  BINARY_ADD       
          83  CALL_FUNCTION_1       1 
          86  CALL_FUNCTION_1       1 
          89  POP_TOP          

 421      90  LOAD_FAST             2  'nd_day'
          93  LOAD_ATTR             7  'img_today'
          96  LOAD_ATTR             8  'setVisible'
          99  LOAD_DEREF            3  'has_bought'
         102  JUMP_IF_FALSE_OR_POP   118  'to 118'
         105  LOAD_FAST             0  'i'
         108  LOAD_DEREF            4  'cur_prog'
         111  LOAD_CONST            2  1
         114  BINARY_SUBTRACT  
         115  COMPARE_OP            2  '=='
       118_0  COME_FROM                '102'
         118  CALL_FUNCTION_1       1 
         121  POP_TOP          

 422     122  LOAD_GLOBAL           9  'task_utils'
         125  LOAD_ATTR            10  'get_task_reward'
         128  LOAD_FAST             1  'sub_task_id'
         131  CALL_FUNCTION_1       1 
         134  STORE_FAST            3  'reward_id'

 423     137  LOAD_GLOBAL          11  'template_utils'
         140  LOAD_ATTR            12  'init_common_reward_list'
         143  LOAD_FAST             2  'nd_day'
         146  LOAD_ATTR            13  'list_items'
         149  LOAD_FAST             3  'reward_id'
         152  CALL_FUNCTION_2       2 
         155  POP_TOP          

 424     156  LOAD_GLOBAL          14  'global_data'
         159  LOAD_ATTR            15  'player'
         162  LOAD_ATTR            16  'has_receive_reward'
         165  LOAD_FAST             1  'sub_task_id'
         168  CALL_FUNCTION_1       1 
         171  STORE_FAST            4  'has_rewarded'

 425     174  LOAD_FAST             4  'has_rewarded'
         177  POP_JUMP_IF_TRUE    196  'to 196'

 426     180  LOAD_DEREF            5  'can_receive_task'
         183  LOAD_ATTR            17  'append'
         186  LOAD_FAST             1  'sub_task_id'
         189  CALL_FUNCTION_1       1 
         192  POP_TOP          
         193  JUMP_FORWARD          0  'to 196'
       196_0  COME_FROM                '193'

 427     196  LOAD_FAST             2  'nd_day'
         199  LOAD_ATTR            13  'list_items'
         202  STORE_FAST            5  'list_item'

 428     205  LOAD_FAST             5  'list_item'
         208  LOAD_ATTR            18  'DeleteAllSubItem'
         211  CALL_FUNCTION_0       0 
         214  POP_TOP          

 429     215  LOAD_FAST             3  'reward_id'
         218  POP_JUMP_IF_FALSE   416  'to 416'

 430     221  LOAD_GLOBAL          19  'confmgr'
         224  LOAD_ATTR            20  'get'
         227  LOAD_CONST            3  'common_reward_data'
         230  LOAD_GLOBAL          21  'str'
         233  LOAD_FAST             3  'reward_id'
         236  CALL_FUNCTION_1       1 
         239  CALL_FUNCTION_2       2 
         242  STORE_FAST            6  'reward_conf'

 431     245  LOAD_FAST             6  'reward_conf'
         248  POP_JUMP_IF_TRUE    268  'to 268'

 432     251  LOAD_GLOBAL          22  'log_error'
         254  LOAD_CONST            4  'reward_id is not exist in common_reward_data'
         257  LOAD_FAST             3  'reward_id'
         260  CALL_FUNCTION_2       2 
         263  POP_TOP          

 433     264  LOAD_CONST            0  ''
         267  RETURN_END_IF    
       268_0  COME_FROM                '248'

 434     268  LOAD_FAST             6  'reward_conf'
         271  LOAD_ATTR            20  'get'
         274  LOAD_CONST            5  'reward_list'
         277  BUILD_LIST_0          0 
         280  CALL_FUNCTION_2       2 
         283  STORE_FAST            7  'reward_list'

 435     286  LOAD_GLOBAL          23  'len'
         289  LOAD_FAST             7  'reward_list'
         292  CALL_FUNCTION_1       1 
         295  STORE_FAST            8  'reward_count'

 436     298  SETUP_LOOP          115  'to 416'
         301  LOAD_GLOBAL          24  'range'
         304  LOAD_FAST             8  'reward_count'
         307  CALL_FUNCTION_1       1 
         310  GET_ITER         
         311  FOR_ITER             98  'to 412'
         314  STORE_FAST            9  'idx'

 437     317  LOAD_FAST             7  'reward_list'
         320  LOAD_FAST             9  'idx'
         323  BINARY_SUBSCR    
         324  UNPACK_SEQUENCE_2     2 
         327  STORE_FAST           10  'item_no'
         330  STORE_FAST           11  'item_num'

 438     333  LOAD_FAST             5  'list_item'
         336  LOAD_ATTR            25  'AddTemplateItem'
         339  CALL_FUNCTION_0       0 
         342  STORE_FAST           12  'reward_item'

 439     345  STORE_FAST            6  'reward_conf'
         348  COMPARE_OP            2  '=='
         351  POP_JUMP_IF_FALSE   372  'to 372'
         354  LOAD_FAST             9  'idx'
         357  LOAD_CONST            6  ''
         360  COMPARE_OP            2  '=='
       363_0  COME_FROM                '351'
         363  POP_JUMP_IF_FALSE   372  'to 372'
         366  LOAD_DEREF            3  'has_bought'
         369  JUMP_FORWARD          3  'to 375'
         372  LOAD_FAST             4  'has_rewarded'
       375_0  COME_FROM                '369'
         375  STORE_FAST           13  'is_get'

 440     378  LOAD_GLOBAL          26  'init_tempate_mall_i_item'

 441     381  LOAD_FAST            12  'reward_item'
         384  LOAD_FAST            10  'item_no'
         387  LOAD_FAST            11  'item_num'
         390  LOAD_FAST            13  'is_get'
         393  LOAD_CONST            7  'show_tips'
         396  LOAD_GLOBAL          27  'True'
         399  LOAD_CONST            8  'show_rare_vx'
         402  LOAD_GLOBAL          27  'True'
         405  CALL_FUNCTION_516   516 
         408  POP_TOP          
         409  JUMP_BACK           311  'to 311'
         412  POP_BLOCK        
       413_0  COME_FROM                '298'
         413  JUMP_FORWARD          0  'to 416'
       416_0  COME_FROM                '298'

 442     416  LOAD_FAST             0  'i'
         419  LOAD_GLOBAL          23  'len'
         422  LOAD_DEREF            2  'children_tasks'
         425  CALL_FUNCTION_1       1 
         428  LOAD_CONST            2  1
         431  BINARY_SUBTRACT  
         432  COMPARE_OP            0  '<'
         435  POP_JUMP_IF_FALSE   461  'to 461'

 443     438  LOAD_GLOBAL          14  'global_data'
         441  LOAD_ATTR            28  'game_mgr'
         444  LOAD_ATTR            29  'next_exec'
         447  LOAD_DEREF            6  'init_sub_task'
         450  LOAD_DEREF            2  'children_tasks'
         453  BINARY_ADD       
         454  CALL_FUNCTION_2       2 
         457  POP_TOP          
         458  JUMP_FORWARD         16  'to 477'

 445     461  LOAD_GLOBAL          14  'global_data'
         464  LOAD_ATTR            28  'game_mgr'
         467  LOAD_ATTR            29  'next_exec'
         470  LOAD_DEREF            7  'init_sub_task_end'
         473  CALL_FUNCTION_1       1 
         476  POP_TOP          
       477_0  COME_FROM                '458'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 83

        global_data.game_mgr.next_exec(init_sub_task, 0)