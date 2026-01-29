# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGrowthFund.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import jump_to_ui_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.gutils import mall_utils
from cocosui import cc

class ActivityGrowthFund(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGrowthFund, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_resolution_changed(self):
        self.panel.progress_bar._UpdateTailFramePosition()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self._parent_task_id = conf.get('cTask', '')
        self._children_task_list = task_utils.get_children_task(self._parent_task_id)
        self.task_to_index = {}
        self.goods_info = None
        self.goods_id = '20603505'
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        if global_data.lobby_mall_data and global_data.player:
            self.goods_info = global_data.lobby_mall_data.get_activity_sale_info('GROWTH_FUND_GOODS')
            if self.goods_info:
                key = self.goods_info['goodsid']
                goods_id = global_data.player.get_goods_info(key).get('cShopGoodsId')
                if goods_id:
                    self.goods_id = goods_id
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_task_progress,
           'buy_good_success': self._referesh_task,
           'player_info_update_event': self._on_player_info_update,
           'resolution_changed': self.on_resolution_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.panel.PlayAnimation('show1')
        act0 = cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show1'))

        def _ani():
            self.panel.PlayAnimation('loop1')
            self.panel.PlayAnimation('loop2')

        act1 = cc.CallFunc.create(_ani)
        self.panel.runAction(cc.Sequence.create([act0, act1]))
        self._referesh_task()
        self._on_player_info_update()
        self.refresh_growth_fund_goods()

    def refresh_growth_fund_goods(self):
        if self.goods_info:
            self.panel.btn_buy.SetEnable(True)
            if self.is_pc_global_pay or mall_utils.is_steam_pay():
                price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
            else:
                price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
            self.panel.btn_buy.SetText(mall_utils.adjust_price(str(price_txt)))

            @self.panel.btn_buy.unique_callback()
            def OnClick(btn, touch):
                if self.is_pc_global_pay:
                    jump_to_ui_utils.jump_to_web_charge()
                elif self.goods_info:
                    global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

        else:
            self.panel.btn_buy.SetEnable(False)
            self.panel.btn_buy.SetText('******')

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            player.receive_all_task_reward(self._parent_task_id)

    def refresh_red_point(self):
        count = activity_utils.get_redpoint_count_by_type(self._activity_type)
        self.panel.btn_get.SetEnable(count > 0)

    def _referesh_task(self):
        for i, task_id in enumerate(self._children_task_list):
            self.task_to_index[task_id] = i

        self.panel.list_item.BindMethod('OnCreateItem', self._update_task_ui)
        self.panel.list_item.DeleteAllSubItem()
        self.panel.list_item.SetInitCount(len(self._children_task_list))
        self.panel.list_item.scroll_Load()
        unlock_activity = self._unlock_activity()
        self.panel.btn_buy.setVisible(not unlock_activity)
        self.panel.btn_get.setVisible(unlock_activity)
        self.refresh_red_point()
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_player_info_update(self, *args):
        player = global_data.player
        if not player:
            return
        else:
            lv = player.get_lv()
            self.panel.lab_lv_num.SetString('lv' + str(lv))
            from logic.gutils.lv_template_utils import get_cur_lv_percentage
            exp_percent = get_cur_lv_percentage(lv, player.get_exp())
            self.panel.progress_bar.SetPercentage(exp_percent * 100)
            unlock_activity = self._unlock_activity()
            self.panel.btn_buy.setVisible(not unlock_activity)
            self.panel.btn_get.setVisible(unlock_activity)
            self.refresh_red_point()
            for i in range(self.panel.list_item.GetItemCount()):
                item_widget = self.panel.list_item.GetItem(i)
                if not item_widget:
                    continue
                self._update_task_ui(None, i, item_widget)

            return

    def _on_update_task_progress(self, task_id):
        if task_id not in self._children_task_list:
            return
        else:
            unlock_activity = self._unlock_activity()
            self.panel.btn_buy.setVisible(not unlock_activity)
            self.panel.btn_get.setVisible(unlock_activity)
            self.refresh_red_point()
            index = self._children_task_list.index(task_id)
            item_widget = self.panel.list_item.GetItem(index)
            if not item_widget:
                return
            self._update_task_ui(None, index, item_widget)
            global_data.emgr.refresh_activity_redpoint.emit()
            return

    def _get_task_reward_list(self, task_id):
        reward_id = str(task_utils.get_task_reward(task_id))
        reward_list = confmgr.get('common_reward_data', reward_id, 'reward_list', default=[])
        return reward_list

    def _unlock_activity(self):
        if not self.goods_id:
            return False
        player = global_data.player
        if not player:
            return False
        bought_num = player.buy_num_all_dict.get(self.goods_id, 0)
        return bought_num > 0

    def _update_task_ui(self, nd_list, index, item_widget):
        player = global_data.player
        if not player:
            return
        else:
            unlock_activity = self._unlock_activity()
            self.panel.btn_buy.setVisible(not unlock_activity)
            self.panel.btn_get.setVisible(unlock_activity)
            task_id = self._children_task_list[index]
            player.is_task_finished(task_id)
            reward_list = self._get_task_reward_list(task_id)
            total_prog = task_utils.get_task_conf_by_id(task_id).get('total_prog', 0)
            lv = player.get_lv()
            if not reward_list:
                return
            item_widget.lab_num_1.SetString(str(total_prog))
            btn = item_widget.btn_cell
            item_widget.img_got_mask.setVisible(False)
            item_widget.img_lock_2.setVisible(False)
            item_widget.img_lock_2.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_locking02.png')
            btn.SetSelect(False)
            btn.EnableCustomState(False)
            item_widget.nd_flash.setVisible(False)
            item_widget.nd_particle.setVisible(False)
            pic1 = 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_goods_01.png'
            pic2 = 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_goods_02.png'
            pic3 = 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_goods_03.png'
            btn.UnBindMethod('OnClick')
            show_tips = False
            item_unreceived = False
            if unlock_activity:
                btn.SetFrames('', [pic1, pic1, pic1], False, None)
                receive_state = player.get_task_reward_status(task_id)
                if receive_state == ITEM_UNGAIN:
                    show_tips = True
                    item_widget.lab_num_1.SetColor(10659549)
                    item_widget.lab_lv.SetColor(10659549)
                elif receive_state == ITEM_UNRECEIVED:
                    item_unreceived = True
                    btn.SetFrames('', [pic1, pic3, pic1], False, None)
                    btn.SetSelect(True)
                    item_widget.lab_num_1.SetColor(16756241)
                    item_widget.lab_lv.SetColor(16756241)
                    btn.BindMethod('OnClick', lambda b, t, tid=task_id: player.receive_task_reward(tid))
                    item_widget.nd_flash.setVisible(True)
                    item_widget.nd_particle.setVisible(True)
                    item_widget.PlayAnimation('loop')
                elif receive_state == ITEM_RECEIVED:
                    item_widget.img_got_mask.setVisible(True)
                    item_widget.img_lock_2.setVisible(True)
                    item_widget.img_lock_2.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_tick.png')
                    item_widget.lab_num_1.SetColor(10659549)
                    item_widget.lab_lv.SetColor(10659549)
            else:
                btn.SetFrames('', [pic1, pic1, pic1], False, None)
                item_widget.img_lock_2.setVisible(True)
                gain = lv >= total_prog
                show_tips = True
                if gain:
                    btn.SetFrames('', [pic1, pic2, pic1], False, None)
                    btn.SetSelect(True)
                    item_widget.lab_num_1.SetColor(14876214)
                    item_widget.lab_lv.SetColor(14876214)
                    item_widget.img_lock_2.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_new_domestic/growth_fund//pnl_fund_locking.png')
                else:
                    item_widget.lab_num_1.SetColor(10659549)
                    item_widget.lab_lv.SetColor(10659549)
            for i, reward_info in enumerate(reward_list[:2]):
                i += 1
                item_no, item_num = reward_info
                nd_item = getattr(item_widget, 'item%d' % i)
                nd_num = getattr(item_widget, 'num%d' % i)
                template_utils.init_tempate_mall_i_item(nd_item, item_no, show_rare_degree=False, show_tips=show_tips)
                nd_num and nd_num.SetString(str(item_num))
                nd_num.SetColor('#SW' if item_unreceived else 10659549)
                nd_frame = getattr(item_widget, 'frame_0%d' % i)
                if nd_frame:
                    path = 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_item_02.png' if item_unreceived else 'gui/ui_res_2/activity/activity_new_domestic/growth_fund/pnl_fund_item01.png'
                    nd_frame.SetDisplayFrameByPath('', path)

            return