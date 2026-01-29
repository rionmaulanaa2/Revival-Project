# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGrowthFundNew.py
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

class ActivityGrowthFundNew(ActivityBase):
    IMG_CELL_PICS = {'black': 'gui/ui_res_2/activity/activity_new_domestic/growth_fund_new/pnl_receive_03.png',
       'purple': 'gui/ui_res_2/activity/activity_new_domestic/growth_fund_new/pnl_receive_02.png',
       'yellow': 'gui/ui_res_2/activity/activity_new_domestic/growth_fund_new/pnl_receive_01.png'
       }

    def __init__(self, dlg, activity_type):
        super(ActivityGrowthFundNew, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        global_data.gfn = self

    def on_resolution_changed(self):
        pass

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self._parent_task_id = conf.get('cTask', '')
        self._children_task_list = task_utils.get_children_task(self._parent_task_id)
        self.task_to_index = {}
        self.index_to_task = {}
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
           'buy_good_success': self._buy_good_success,
           'player_info_update_event': self._on_player_info_update,
           'resolution_changed': self.on_resolution_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
        self.init_item_list()
        self._referesh_task()
        self._on_player_info_update()
        self.refresh_growth_fund_goods()
        self.panel.btn_buy.RecursionReConfPosition()

    def init_item_list(self):
        self.panel.list_item.DeleteAllSubItem()
        acts = []
        for i in range(len(self._children_task_list)):
            item = self.panel.list_item.AddTemplateItem()
            item.temp_btn_get.btn_common.BindMethod('OnClick', lambda btn, touch, i=i: self.on_click_btn_get(i))
            acts.extend([
             cc.CallFunc.create(lambda item=item: item.PlayAnimation('show')),
             cc.DelayTime.create(0.03)])

        self.panel.runAction(cc.Sequence.create(acts))

    def on_click_btn_get(self, i):
        task_id = self.index_to_task[i]
        player = global_data.player
        if not player:
            return
        player.receive_task_reward(task_id)
        self._referesh_task()

    def refresh_growth_fund_goods(self):
        if self.goods_info:
            self.panel.btn_buy.SetEnable(True)
            if self.is_pc_global_pay or mall_utils.is_steam_pay():
                price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
            else:
                price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
            self.panel.lab_money_left.SetString(mall_utils.adjust_price(str(price_txt)))

            @self.panel.btn_buy.unique_callback()
            def OnClick(btn, touch):
                if self.is_pc_global_pay:
                    jump_to_ui_utils.jump_to_web_charge()
                elif self.goods_info:
                    global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

        else:
            self.panel.btn_buy.SetEnable(False)
            self.panel.lab_money_left.SetString('******')

    def refresh_red_point(self):
        pass

    def _buy_good_success(self):
        player = global_data.player
        if not player:
            return
        else:
            act = []
            ani_time = None
            for i, task_id in enumerate(self.index_to_task):
                if task_id not in self.task_to_index:
                    continue
                index = self.task_to_index[task_id]
                item_widget = self.panel.list_item.GetItem(index)
                receive_state = player.get_task_reward_status(task_id)
                if receive_state == ITEM_UNRECEIVED:
                    act.append(cc.CallFunc.create(lambda item=item_widget: item.PlayAnimation('show1')))
                    if ani_time is None:
                        ani_time = item_widget.GetAnimationMaxRunTime('show1')

            if ani_time is not None:
                act.extend([
                 cc.DelayTime.create(ani_time),
                 cc.CallFunc.create(self._referesh_task)])
                self.panel.runAction(cc.Sequence.create(act))
            else:
                self._referesh_task()
            return

    def _referesh_task(self):
        player = global_data.player
        if not player:
            return
        unlock_activity = self._unlock_activity()
        self.panel.btn_buy.setVisible(not unlock_activity)
        self.panel.img_exp.setVisible(unlock_activity)
        recv_task = []
        unrecv_task = []
        for task_id in self._children_task_list:
            if player.get_task_reward_status(task_id) == ITEM_RECEIVED:
                recv_task.append(task_id)
            else:
                unrecv_task.append(task_id)

        self.index_to_task = unrecv_task + recv_task
        for i, task_id in enumerate(self.index_to_task):
            self.task_to_index[task_id] = i
            self._update_task_ui(task_id)

        unlock_activity = self._unlock_activity()
        self.panel.btn_buy.setVisible(not unlock_activity)
        self.panel.img_exp.setVisible(unlock_activity)
        self.refresh_red_point()
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_player_info_update(self, *args):
        player = global_data.player
        if not player:
            return
        lv = player.get_lv()
        self.panel.lab_lv_num.SetString('Lv' + str(lv))
        from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp
        self.panel.lab_exp.SetString(str(player.get_exp()) + '/' + str(get_lv_upgrade_need_exp(lv)))
        self._referesh_task()

    def _on_update_task_progress(self, task_id):
        self._referesh_task()

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

    def _update_task_ui(self, task_id):
        if task_id not in self.task_to_index:
            return
        player = global_data.player
        if not player:
            return
        unlock_activity = self._unlock_activity()
        index = self.task_to_index[task_id]
        item_widget = self.panel.list_item.GetItem(index)
        player.is_task_finished(task_id)
        reward_list = self._get_task_reward_list(task_id)
        total_prog = task_utils.get_task_conf_by_id(task_id).get('total_prog', 0)
        item_widget.lab_special.setVisible(total_prog == 1)
        item_widget.nd_level_info.setVisible(total_prog != 1)
        lv = player.get_lv()
        if not reward_list:
            return
        item_widget.lab_level_1.SetString('Lv' + str(total_prog))
        item_widget.img_lock_1.setVisible(not unlock_activity)
        item_widget.img_lock_2.setVisible(not unlock_activity)
        item_widget.img_cell_01.setVisible(False)
        img_cell = item_widget.img_cell
        img_cell.setVisible(True)
        btn_get = item_widget.temp_btn_get
        btn_get.setVisible(True)
        item_widget.nd_get.setVisible(False)
        play_loop_ani = False
        if unlock_activity:
            receive_state = player.get_task_reward_status(task_id)
            if receive_state == ITEM_UNGAIN:
                img_cell.SetDisplayFrameByPath('', self.IMG_CELL_PICS['black'])
                btn_get.btn_common.SetEnable(False)
                btn_get.btn_common.SetText(str(lv) + '/' + str(total_prog))
            elif receive_state == ITEM_UNRECEIVED:
                img_cell.SetDisplayFrameByPath('', self.IMG_CELL_PICS['yellow'])
                btn_get.btn_common.SetEnable(True)
                btn_get.btn_common.SetText(910007)
                play_loop_ani = True
            elif receive_state == ITEM_RECEIVED:
                img_cell.SetDisplayFrameByPath('', self.IMG_CELL_PICS['black'])
                btn_get.setVisible(False)
                item_widget.nd_get.setVisible(True)
        else:
            gain = lv >= total_prog
            if gain:
                img_cell.SetDisplayFrameByPath('', self.IMG_CELL_PICS['purple'])
                btn_get.btn_common.SetEnable(False)
                btn_get.btn_common.SetText(910007)
            else:
                img_cell.SetDisplayFrameByPath('', self.IMG_CELL_PICS['black'])
                btn_get.btn_common.SetEnable(False)
                btn_get.btn_common.SetText(str(lv) + '/' + str(total_prog))
        if play_loop_ani:
            item_widget.PlayAnimation('loop')
        else:
            item_widget.StopAnimation('loop')
        for i, reward_info in enumerate(reward_list[:2]):
            i += 1
            item_no, item_num = reward_info
            nd_item = getattr(item_widget, 'item%d' % i)
            template_utils.init_tempate_mall_i_item(nd_item, item_no, item_num, show_rare_degree=False, show_tips=True)