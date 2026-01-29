# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivitySpringFestivalLottery.py
from __future__ import absolute_import
import cc
import six
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils.client_utils import post_method
from logic.comsys.activity.widget import widget
from logic.gutils import item_utils

@widget('PriceWidget', 'TaskListWidget', 'DescribeWidget', 'CommonCountdownWidget')
class ActivitySpringFestivalLottery(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySpringFestivalLottery, self).__init__(dlg, activity_type)
        self.panel.act_list = self.panel.list_task
        self.panel.left_time = self.panel.lab_time
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self.use_items = ui_data.get('use_items', [])
        self.items_info = ui_data.get('items_info', [])
        self.item_ani_name = 'tips'
        self.need_skip_anim = False

    def on_init_panel(self):
        list_item = self.panel.list_item
        for idx, ui_item in enumerate(list_item.GetAllItem()):
            ui_item.RecordAnimationNodeState(self.item_ani_name)
            temp_btn = ui_item.temp_btn.btn_common
            item_no, cost, goods_id, text_id, open_ani_name = self.use_items[idx]
            self.panel.RecordAnimationNodeState(open_ani_name)

            @temp_btn.unique_callback()
            def OnClick(btn, touch, idx=idx):
                item_no, cost, goods_id, _, _ = self.use_items[idx]
                if not global_data.player:
                    return
                cost_item_amount = global_data.player.get_item_num_by_no(item_no)
                if cost_item_amount >= cost:
                    self.open_card(idx)
                else:
                    global_data.game_mgr.show_tip(635505)
                    from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                    groceries_buy_confirmUI(str(goods_id))

            btn_show = ui_item.btn_show

            @btn_show.unique_callback()
            def OnClick(btn, touch, idx=idx):
                item_no, cost, goods_id, _, _ = self.use_items[idx]
                from logic.comsys.mecha_display.LobbyItemPreviewUI import LobbyItemPreviewUI
                ui = LobbyItemPreviewUI(None, item_no, True)
                return

        @self.panel.btn_click.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('SpringCardFragmentUI', 'logic.comsys.activity.SpringFestival')
            dlg.set_activity_type(self._activity_type)

        self._on_update_reward()

        @self.panel.btn_skip.unique_callback()
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            self.on_set_skip_anim_flag(btn)

        self.on_set_skip_anim_flag(self.panel.btn_skip)

        @self.panel.btn_reward_1.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            jump_to_display_detail_by_item_no(201800444)

        @self.panel.btn_reward_2.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            jump_to_display_detail_by_item_no(201003132)

    def on_set_skip_anim_flag(self, btn):
        btn.SetSelect(self.need_skip_anim)
        btn.icon_tick and btn.icon_tick.setVisible(self.need_skip_anim)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'player_item_update_event': self._on_item_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        super(ActivitySpringFestivalLottery, self).refresh_panel()
        self._on_update_reward()

    @post_method
    def _on_update_reward(self, *args):
        if not global_data.player or not self.panel:
            return
        list_item = self.panel.list_item
        for idx, ui_item in enumerate(list_item.GetAllItem()):
            item_no, cost, _, text_id, _ = self.use_items[idx]
            cost_item_amount = global_data.player.get_item_num_by_no(item_no)
            ui_item.lab_got.SetString(get_text_by_id(text_id).format(str(cost_item_amount)))
            cost_item_amount = global_data.player.get_item_num_by_no(item_no)
            show_loop_ani = cost_item_amount >= cost
            if show_loop_ani:
                if not ui_item.IsPlayingAnimation(self.item_ani_name):
                    ui_item.PlayAnimation(self.item_ani_name)
            else:
                ui_item.StopAnimation(self.item_ani_name)
                ui_item.RecoverAnimationNodeState(self.item_ani_name)

        self.refresh_red_point()

    def _on_item_update(self):
        global_data.emgr.player_money_info_update_event.emit()
        self._on_update_reward()

    def open_card(self, idx):
        list_item = self.panel.list_item
        for _idx, ui_item in enumerate(list_item.GetAllItem()):
            item_no, cost, _, text_id, open_ani_name = self.use_items[_idx]
            self.panel.StopAnimation(open_ani_name)
            self.panel.RecoverAnimationNodeState(open_ani_name)

        item_no, _, _, _, open_ani_name = self.use_items[idx]

        def _open(item_no=item_no):
            if not global_data.player:
                return
            item = global_data.player.get_item_by_no(item_no)
            usage = item_utils.get_lobby_item_usage(item_no)
            if item:
                item_data = {'id': item.id,'item_no': item.item_no,'quantity': 1
                   }
                item_utils.try_use_lobby_item(item_data, usage)

        if self.need_skip_anim:
            _open()
        else:
            show_in_t = self.panel.GetAnimationMaxRunTime(open_ani_name)
            self.panel.PlayAnimation(open_ani_name)
            ac_list = []
            ac_list.extend([
             cc.DelayTime.create(show_in_t),
             cc.CallFunc.create(_open)])
            self.panel.stopAllActions()
            self.panel.runAction(cc.Sequence.create(ac_list))

    def refresh_red_point(self):
        show_red = False
        for idx, info in enumerate(self.items_info):
            goods_id, item_id, fragment_item_info, _, _ = info
            fragment_item_id, combine_num, decomposition_num = fragment_item_info
            if global_data.player:
                has_num = global_data.player.get_item_num_by_no(fragment_item_id)
                num0 = int(has_num / combine_num)
                num1 = global_data.player.get_item_num_by_no(item_id)
                show_red = show_red or num0 > 0
                show_red = show_red or num1 > 0

        if self.panel and self.panel.btn_click and self.panel.btn_click.temp_red:
            self.panel.btn_click.temp_red.setVisible(show_red)