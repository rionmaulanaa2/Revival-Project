# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRankRush.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils, jump_to_ui_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils.mall_utils import is_steam_pay
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_date_str
from logic.gutils.task_utils import get_task_conf_by_id
from logic.gcommon.cdata import dan_data
from logic.gutils import template_utils
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2

class ActivityRankRush(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityRankRush, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.activity_conf = conf
        ui_data = conf.get('cUiData', {})
        self.recommend_dan = ui_data.get('recommend_dan', {})
        self.task_list = ui_data.get('task', [])
        if not is_steam_pay() and not G_IS_NA_USER:
            self.goods_id = ui_data.get('goods_id', '') if 1 else ui_data.get('goods_id_steam', '')
            self.goods_info = None
            self.goods_list_name = ui_data.get('goods_list_name', '')
            self.cur_choose_idx = None
            self.last_choose_item = None
            return self.goods_list_name or None
        else:
            self.is_pc_global_pay = mall_utils.is_pc_global_pay()
            if global_data.lobby_mall_data and global_data.player:
                self.goods_info = global_data.lobby_mall_data.get_activity_sale_info(self.goods_list_name)
            return

    def on_init_panel(self):
        self.init_btn()
        self.update_widget()
        self.init_describe()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_widget,
           'task_prog_changed': self.update_widget,
           'buy_good_success': self.on_buy_goods
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_btn(self):

        @self.panel.nd_page_2.temp_btn_improve.btn_major.unique_callback()
        def OnClick(btn, touch):
            jump_to_mode_choose(PLAY_TYPE_DEATH)

        self.panel.nd_page_3.list_btn.SetInitCount(2)
        btn_receive = self.panel.nd_page_3.list_btn.GetItem(0)
        btn_receive_pay = self.panel.nd_page_3.list_btn.GetItem(1)

        @btn_receive.btn_major.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            self.on_click_receive_btn(global_data.player.rush_rank_task)

        @btn_receive_pay.btn_major.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            if self.is_unlock_rebate():
                self.on_click_receive_btn(global_data.player.rush_rank_task)
            else:
                self.on_click_btn_buy()

    def update_choose_dan_btn(self):
        self.panel.nd_page_1.temp_btn_confirm.btn_major.SetEnable(self.cur_choose_idx is not None)

        @self.panel.nd_page_1.temp_btn_confirm.btn_major.unique_callback()
        def OnClick(btn, touch):
            if self.cur_choose_idx is None or not global_data.player:
                return
            else:

                def confirm_callback():
                    global_data.player.choose_season_rush_rank_task(self.task_list[self.cur_choose_idx])
                    self.panel.nd_page_1.setVisible(False)
                    self.panel.nd_page_2.setVisible(True)
                    self.panel.PlayAnimation('show_page_2')
                    self.update_widget()

                NormalConfirmUI2(on_confirm=confirm_callback, content=get_text_by_id(83475), cancel_text=get_text_by_id(90005))
                return

        return

    def update_receive_reward_btn(self):
        if not global_data.player:
            return
        else:
            task_id = global_data.player.rush_rank_task
            status = global_data.player.get_task_reward_status(task_id)
            btn_receive = self.panel.nd_page_3.list_btn.GetItem(0)
            btn_receive_pay = self.panel.nd_page_3.list_btn.GetItem(1)
            btn_receive.btn_major.SetEnable(status == ITEM_UNRECEIVED)
            pay_enable = bool(status == ITEM_UNRECEIVED and (self.goods_info is not None or self.is_unlock_rebate()))
            btn_receive_pay.btn_major.SetEnable(pay_enable)
            if not self.goods_info and not self.is_unlock_rebate():
                btn_receive_pay.btn_major.SetText('******')
                return
            if not self.is_unlock_rebate():
                if self.is_pc_global_pay or mall_utils.is_steam_pay():
                    price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
                else:
                    price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
                btn_receive_pay.btn_major.SetText('{}\xe5\x8f\x8c\xe5\x80\x8d\xe9\xa2\x86\xe5\x8f\x96'.format(mall_utils.adjust_price(str(price_txt))))
            else:
                btn_receive_pay.btn_major.SetText('\xe5\x8f\x8c\xe5\x80\x8d\xe9\xa2\x86\xe5\x8f\x96')
            return

    def update_widget(self, *args):
        icon_pic_path = 'gui/ui_res_2/activity/activity_202309/rank_present/icon_rank_present_tier_{}.png'
        bar_pic_path = 'gui/ui_res_2/activity/activity_202309/rank_present/bar_rank_present_small_{}.png'
        if not global_data.player:
            return
        self.update_choose_dan_btn()
        self.update_receive_reward_btn()
        dan_info = global_data.player.get_dan_info().get('survival_dan', {})
        cur_dan = dan_info.get('dan', dan_data.BROZE)
        status = global_data.player.get_task_reward_status(global_data.player.rush_rank_task)
        if status in [ITEM_RECEIVED, ITEM_UNRECEIVED]:
            self.panel.bar_tips.setVisible(False)
            self.panel.lab_tips.setVisible(False)
        else:
            self.panel.bar_tips.setVisible(True)
            self.panel.lab_tips.setVisible(True)
            rec = self.recommend_dan.get(str(cur_dan), dan_data.LEGEND)
            dan_conf = dan_data.data.get(rec, {})
            self.panel.bar_tips.lab_suggest.setString(get_text_by_id(83465).format(get_text_by_id(dan_conf.get('name', 0))))
        if global_data.player.rush_rank_task:
            status = global_data.player.get_task_reward_status(global_data.player.rush_rank_task)
            task_reward_list = confmgr.get('common_reward_data', str(get_task_conf_by_id(str(global_data.player.rush_rank_task)).get('select_rewards', [])[0]), 'reward_list', default=[])
            self.panel.nd_page_1.setVisible(False)
            self.panel.nd_page_2.setVisible(status == ITEM_UNGAIN)
            self.panel.nd_page_3.setVisible(status != ITEM_UNGAIN)
            self.panel.nd_reward.setVisible(True)
            self.panel.nd_reward.bar_reward.list_reward.SetInitCount(min(len(task_reward_list), 3))
            list_item_2 = self.panel.nd_page_2.list_item
            list_item_2.SetInitCount(2)
            cur_dan_item = list_item_2.GetItem(0)
            dan_conf = dan_data.data.get(cur_dan, {})
            cur_dan_item.lab_tier.setString(get_text_by_id(dan_conf.get('name', 0)))
            cur_dan_item.icon_tier.SetDisplayFrameByPath('', icon_pic_path.format(min(cur_dan, dan_data.LEGEND) - 1))
            cur_dan_item.bar.SetDisplayFrameByPath('', bar_pic_path.format(min(cur_dan, dan_data.LEGEND) - 1))
            tar_get_dan = self.task_list.index(global_data.player.rush_rank_task) + 2
            target_dan_item = list_item_2.GetItem(1)
            dan_conf = dan_data.data.get(tar_get_dan, {})
            target_dan_item.lab_tier.setString(get_text_by_id(dan_conf.get('name', 0)))
            target_dan_item.icon_tier.SetDisplayFrameByPath('', icon_pic_path.format(min(tar_get_dan, dan_data.LEGEND) - 1))
            target_dan_item.bar.SetDisplayFrameByPath('', bar_pic_path.format(min(tar_get_dan, dan_data.LEGEND) - 1))
            self.panel.nd_page_2.lab_tips_need.setString(get_text_by_id(83467).format(self.get_point_remain()))
            target_dan_item = self.panel.nd_page_3.temp_tier
            dan_conf = dan_data.data.get(tar_get_dan, {})
            target_dan_item.lab_tier.setString(get_text_by_id(dan_conf.get('name', 0)))
            target_dan_item.icon_tier.SetDisplayFrameByPath('', icon_pic_path.format(min(tar_get_dan, dan_data.LEGEND) - 1))
            target_dan_item.bar.SetDisplayFrameByPath('', bar_pic_path.format(min(tar_get_dan, dan_data.LEGEND) - 1))
            for j, reward_item in enumerate(self.panel.nd_reward.bar_reward.list_reward.GetAllItem()):
                item_no, item_num = task_reward_list[j]
                template_utils.init_tempate_mall_i_item(reward_item, item_no, item_num, show_tips=True)

        else:
            self.panel.nd_page_1.setVisible(True)
            self.panel.nd_page_2.setVisible(False)
            self.panel.nd_page_3.setVisible(False)
            self.panel.nd_reward.setVisible(False)
            dan_list_item = self.panel.nd_page_1.list_item
            dan_list_item.SetInitCount(6)
            for i, item in enumerate(dan_list_item.GetAllItem()):
                if i >= len(self.task_list):
                    return
                task_id = self.task_list[i]
                task_reward_list = confmgr.get('common_reward_data', str(get_task_conf_by_id(str(task_id)).get('select_rewards', [])[0]), 'reward_list', default=[])
                item_dan = i + 2
                recommend_dan = self.recommend_dan.get(str(cur_dan), 0)
                dan_conf = dan_data.data.get(item_dan, {})
                item.lab_tier.setString(get_text_by_id(dan_conf.get('name', 0)))
                item.img_now.setVisible(cur_dan == item_dan)
                item.img_recommend.setVisible(recommend_dan == item_dan)
                item.bar.list_item.SetInitCount(min(len(task_reward_list), 3))
                for j, reward_item in enumerate(item.list_item.GetAllItem()):
                    item_no, item_num = task_reward_list[j]
                    template_utils.init_tempate_mall_i_item(reward_item, item_no, item_num, show_tips=True)

                item.btn_choose.SetEnable(True)
                item.btn_choose.setVisible(True)

                @item.btn_choose.unique_callback()
                def OnClick(btn, touch, idx=i, item=item):
                    if item == self.last_choose_item:
                        return
                    self.cur_choose_idx = idx
                    item.btn_choose.SetSelect(True)
                    self.panel.nd_page_1.temp_btn_confirm.btn_major.SetEnable(True)
                    if self.last_choose_item:
                        self.last_choose_item.btn_choose.SetSelect(False)
                    self.last_choose_item = item

    def on_click_receive_btn(self, task_id):
        status = global_data.player.get_task_reward_status(task_id)
        print ('on_click_receive_btn', task_id, status)
        if status == ITEM_UNRECEIVED:
            select_rewards = get_task_conf_by_id(str(task_id)).get('select_rewards', [])
            global_data.player.receive_task_reward(task_id, {'reward_id': select_rewards[1] if self.is_unlock_rebate() else select_rewards[0]})

    def init_describe(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

    def receive_double_reward(self, *args):
        if not global_data.player:
            return
        task_id = global_data.player.rush_rank_task
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_UNRECEIVED and self.is_unlock_rebate():
            select_rewards = get_task_conf_by_id(str(task_id)).get('select_rewards', [])
            global_data.player.receive_task_reward(task_id, {'reward_id': select_rewards[1]})

    def on_buy_goods(self, *args):
        self.receive_double_reward()
        self.update_widget()

    def on_click_btn_buy(self, *args):
        if self.is_pc_global_pay:
            jump_to_ui_utils.jump_to_web_charge()
        elif self.goods_info:
            global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

    def is_unlock_rebate(self):
        player = global_data.player
        if not player:
            return False
        bought_num = player.buy_num_all_dict.get(self.goods_id, 0)
        return bought_num > 0

    def get_point_remain(self):
        if not global_data.player:
            return
        point_per_star = 100
        target_dan = self.task_list.index(global_data.player.rush_rank_task) + 2
        dan_info = global_data.player.get_dan_info().get('survival_dan', {})
        cur_dan = dan_info.get('dan', dan_data.BROZE)
        cur_lv = dan_info.get('lv', 1)
        if cur_dan >= dan_data.LEGEND:
            return 0
        cur_star = dan_info.get('star', 0)
        cur_point = dan_info.get('league_point', 0)
        dan_diff_point = 0
        for i in range(cur_dan, target_dan):
            dan_diff_point += dan_data.get_lv_num(i) * (dan_data.get_star_num(i) + 1) * 100

        return max(dan_diff_point - (dan_data.get_lv_num(cur_dan) - cur_lv) * (dan_data.get_star_num(cur_dan) + 1) * point_per_star - cur_star * point_per_star - cur_point, 0)

    @staticmethod
    def show_tab_rp(activity_type, *args):
        if global_data.player and global_data.player.rush_rank_task:
            reward_status = global_data.player.get_task_reward_status(global_data.player.rush_rank_task)
            if reward_status == ITEM_UNRECEIVED:
                return True
        return False