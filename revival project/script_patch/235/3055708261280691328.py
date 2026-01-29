# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivityVeteranRecall.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.item.item_const import ITEM_NO_CB_POINT
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils.template_utils import init_tempate_mall_i_simple_item
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.comsys.mall_ui import BuyConfirmUIInterface
from logic.gutils import role_head_utils
from logic.comsys.activity.ActivitySummer.VeteranRecallSubUI import VeteranRecallSubUI
from math import ceil, floor
import cc
from logic.gcommon import time_utility

class ActivityVeteranRecall(ActivityBase):
    UZI_ID = 208101116
    END_TIME = 1628110800

    def __init__(self, dlg, activity_type):
        super(ActivityVeteranRecall, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_events(True)
        self.req_del_red_poiont()

    def init_parameters(self):
        self.cur_points = global_data.player.get_item_num_by_no(ITEM_NO_CB_POINT)
        self.role_dict = global_data.player._reply_lost_roles
        self.send_mgs_uids = global_data.player.send_msg_uids
        self.team_dict = global_data.player.lost_role_team_times
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self.ex_item_list = self.activity_conf.get('cUiData').get('item_list')
        self.ex_mall_item_list = self.activity_conf.get('cUiData').get('mall_item_list')
        self.cb_point = self.activity_conf.get('cUiData').get('cb_point')
        self.nd_points = self.panel.nd_content.nd_exchange.nd_reward.lab_exchange_num
        self.nd_item_list = self.panel.nd_content.nd_exchange.nd_reward.list_item
        self.btn_recall = self.panel.nd_content.nd_player.nd_player_01.btn_recall
        self.btn_team = self.panel.nd_content.nd_player.nd_player_01.btn_team
        self.nd_recall = self.panel.nd_content.nd_player.nd_player_01.nd_recall
        self.nd_team = self.panel.nd_content.nd_player.nd_player_01.nd_team
        self.nd_empty = self.panel.nd_content.nd_player.nd_player_01.img_empty
        self.btn_refresh = self.nd_recall.btn_refresh

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_player_item_update,
           'buy_good_success': self.on_buy_goods_success,
           'reply_lost_roles_event': self.on_refresh_lost_roles,
           'send_lost_role_recall': self.on_send_recall,
           'update_recall_team_times': self.on_update_team
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        super(ActivityVeteranRecall, self).on_init_panel()
        self.panel.RecordAnimationNodeState('loop')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(1.6),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
        self.upload_open_log()
        self.init_ui_events()
        self.init_item_list()
        self.btn_recall.OnClick(TouchMock())
        self.request_team_info()

    def upload_open_log(self):
        global_data.player.on_open_lost_role_widget()

    def request_team_info(self):
        for uid in six_ex.keys(self.team_dict):
            global_data.player.request_player_simple_inf(int(uid))

    def init_ui_events(self):
        self.panel.nd_title.lab_time.SetString(609744)

        @self.panel.nd_title.btn_question.unique_callback()
        def OnClick(_btn, _touch, *args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, rule = (609679, 609746)
            dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

        self.nd_points.SetString(str(self.cur_points))
        self.panel.nd_content.nd_exchange.nd_reward_01.lab_name.SetString(get_text_by_id(21011) + ' ' + get_lobby_item_name(self.UZI_ID))

        @self.panel.nd_content.nd_exchange.nd_reward_01.btn_detail.unique_callback()
        def OnClick(_btn, _touch, *args):
            jump_to_display_detail_by_item_no(208101116)

        self.nd_recall.lab_tips.SetString(get_text_by_id(609733).format(str(self.cb_point)))

        @self.btn_recall.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.btn_recall.SetSelect(True)
            self.nd_recall.setVisible(True)
            self.btn_team.SetSelect(False)
            self.nd_team.setVisible(False)
            self.update_recall_list()

        @self.btn_refresh.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.refresh_recall_list()

        @self.btn_team.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.btn_recall.SetSelect(False)
            self.nd_recall.setVisible(False)
            self.btn_team.SetSelect(True)
            self.nd_team.setVisible(True)
            self.update_team_list()

    def init_item_list(self):
        self.nd_item_list.DeleteAllSubItem()
        self.nd_item_list.SetInitCount(len(self.ex_item_list))
        for index, ui_item in enumerate(self.nd_item_list.GetAllItem()):
            item_no = self.ex_item_list[index]
            goods_id = self.ex_mall_item_list[index]
            item_num = mall_utils.get_goods_num(str(goods_id))
            init_tempate_mall_i_simple_item(ui_item.temp_item, item_no, item_num)
            _, _, num_info = mall_utils.buy_num_limit_by_all(str(goods_id))
            if num_info:
                left_num, max_num = num_info
                ui_item.lab_limit.SetString(get_text_by_id(607206).format(str(left_num)))
            else:
                ui_item.lab_limit.SetString('')
            left_num = num_info[0] if num_info else 0
            if left_num <= 0:
                ui_item.lab_exchange_need.setVisible(False)
                ui_item.lab_finish.setVisible(True)
                ui_item.lab_limit.setVisible(False)
            else:
                ui_item.lab_exchange_need.setVisible(True)
                ui_item.lab_finish.setVisible(False)
                ui_item.lab_limit.setVisible(True)
                price_info = mall_utils.get_mall_item_price(str(goods_id))
                if price_info:
                    price = price_info[0].get('real_price')
                    ui_item.lab_exchange_need.SetString(str(price))
                can_buy_num = mall_utils.get_mall_item_can_buy_num(str(goods_id))
                if can_buy_num <= 0:
                    ui_item.img_lock.setVisible(True)
                    ui_item.pnl_bg.setVisible(True)
                    ui_item.img_get.setVisible(False)
                else:
                    ui_item.img_lock.setVisible(False)
                    ui_item.pnl_bg.setVisible(False)
                    ui_item.img_get.setVisible(True)
                    ui_item.PlayAnimation('loop_get')

                @ui_item.temp_item.btn_choose.unique_callback()
                def OnClick(_btn, _touch, _goods_id=goods_id):
                    BuyConfirmUIInterface.groceries_buy_confirmUI(str(_goods_id))

    def check_finish(self):
        cur_time = time_utility.time()
        if cur_time > self.END_TIME:
            return True
        return False

    def update_recall_list(self):
        self.nd_recall.list_recall.DeleteAllSubItem()
        if self.check_finish():
            self.nd_empty.setVisible(True)
            self.nd_empty.lab_empty.SetString(get_text_by_id(81796))
            return
        list_len = len(self.role_dict)
        if not list_len or list_len == 0:
            self.nd_empty.setVisible(True)
            return
        self.nd_empty.setVisible(False)
        self.nd_recall.list_recall.SetInitCount(list_len)
        for index, ui_item in enumerate(self.nd_recall.list_recall.GetAllItem()):
            role_data = self.role_dict[index]
            role_frame = role_data['head_frame']
            role_photo = role_data['head_photo']
            uid = role_data['uid']
            role_head_utils.init_role_head_auto(ui_item.temp_head, uid, show_tips=True, head_frame=role_frame, head_photo=role_photo)
            role_name = role_data['char_name']
            ui_item.temp_head.lab_name.SetString(role_name)
            self.send_mgs_uids = global_data.player.send_msg_uids
            self.team_dict = global_data.player.lost_role_team_times
            if uid not in self.send_mgs_uids.get('qq_wc', []) and uid not in self.send_mgs_uids.get('msg', []):

                @ui_item.btn_recall.unique_callback()
                def OnClick(_btn, _touch, _role_data=role_data, *args):
                    self._on_click_recall(_role_data)

                global_data.message_data.get_player_inf(1, uid)
            elif str(uid) in self.team_dict:
                ui_item.btn_recall.setVisible(False)
                ui_item.nd_done.setVisible(True)
            else:
                ui_item.btn_recall.setVisible(False)
                ui_item.btn_sent.setVisible(True)

                @ui_item.btn_sent.unique_callback()
                def OnClick(_btn, _touch, _role_data=role_data, *args):
                    self._on_click_recall(_role_data)

    def _on_click_recall(self, _role_data):
        ui = global_data.ui_mgr.get_ui('VeteranRecallSubUI')
        if ui:
            ui.close()
        ui = VeteranRecallSubUI()
        ui.set_role_data(_role_data)

    def on_refresh_lost_roles(self):
        global_data.game_mgr.show_tip(get_text_by_id(609775))
        self.role_dict = global_data.player._reply_lost_roles
        self.update_recall_list()

    def refresh_recall_list(self):
        global_data.game_mgr.show_tip(get_text_by_id(609776))
        global_data.player.req_lost_roles()

    def update_team_list(self):
        self.nd_team.nd_progress.setVisible(False)
        self.nd_team.list_team.DeleteAllSubItem()
        if self.check_finish():
            self.nd_empty.setVisible(True)
            self.nd_empty.lab_empty.SetString(get_text_by_id(81796))
            return
        list_len = len(self.team_dict)
        if not list_len or list_len == 0:
            self.nd_empty.setVisible(True)
            self.nd_team.btn_left.setVisible(False)
            self.nd_team.btn_right.setVisible(False)
            return
        for uid in six_ex.keys(self.team_dict):
            role_data = global_data.message_data.get_player_inf(1, int(uid))
            if not role_data:
                list_len -= 1

        if list_len <= 0:
            self.nd_empty.setVisible(True)
            return
        self.nd_empty.setVisible(False)
        self.nd_team.list_team.SetInitCount(list_len)
        for index, ui_item in enumerate(self.nd_team.list_team.GetAllItem()):
            ui_item.btn_recall.setVisible(False)
            uid = six_ex.keys(self.team_dict)[index]
            role_data = global_data.message_data.get_player_inf(1, int(uid))
            if not role_data:
                continue
            role_frame = role_data['head_frame']
            role_photo = role_data['head_photo']
            role_head_utils.init_role_head_auto(ui_item.temp_head, int(uid), show_tips=True, head_frame=role_frame, head_photo=role_photo)
            role_name = role_data['char_name']
            ui_item.temp_head.lab_name.SetString(role_name)
            ui_item.lab_team.SetString(get_text_by_id(609734).format(str(self.team_dict.get(uid, 0)), str(5)))
            ui_item.lab_team.setVisible(True)

        self.nd_team.btn_left.setVisible(True)
        self.nd_team.btn_right.setVisible(True)

        @self.nd_team.btn_left.unique_callback()
        def OnClick(_btn, _touch, *args):
            offset = self.nd_team.list_team.GetContentOffset()
            gap = self.nd_team.list_team.GetHorzIndent()
            w = self.nd_team.list_team.GetItem(0).GetContentSize()[0] + gap
            count = (offset.x + w) / w
            count = floor(count)
            pos = cc.Vec2(count * w, offset.y)
            self.nd_team.list_team.SetContentOffsetInDuration(pos, 0.3, False, bound_check=True, over_edge=False)

        @self.nd_team.btn_right.unique_callback()
        def OnClick(_btn, _touch, *args):
            offset = self.nd_team.list_team.GetContentOffset()
            gap = self.nd_team.list_team.GetHorzIndent()
            w = self.nd_team.list_team.GetItem(0).GetContentSize()[0] + gap
            count = (offset.x - w) / w
            count = floor(count)
            pos = cc.Vec2(count * w, offset.y)
            self.nd_team.list_team.SetContentOffsetInDuration(pos, 0.3, False, bound_check=True, over_edge=False)

    def on_player_item_update(self):
        self.cur_points = global_data.player.get_item_num_by_no(ITEM_NO_CB_POINT)
        self.nd_points.SetString(str(self.cur_points))
        self.on_buy_goods_success()

    def on_buy_goods_success(self):
        self.init_item_list()

    def on_send_recall(self):
        self.role_dict = global_data.player._reply_lost_roles
        self.send_mgs_uids = global_data.player.send_msg_uids
        self.update_recall_list()

    def on_update_team(self):
        self.team_dict = global_data.player.lost_role_team_times
        self.update_team_list()

    def req_del_red_poiont(self):
        global_data.player.cancel_lost_role_red_point()
        global_data.emgr.refresh_activity_redpoint.emit()

    def on_finalize_panel(self):
        self.panel.StopAnimation('loop')
        self.panel.RecoverAnimationNodeState('loop')
        self.process_events(False)
        super(ActivityVeteranRecall, self).on_finalize_panel()