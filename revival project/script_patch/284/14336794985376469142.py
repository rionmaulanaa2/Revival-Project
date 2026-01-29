# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFriendHelp.py
from __future__ import absolute_import
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.rank.FriendHelpRankWidget import FriendHelpRankWidget
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const as iconst
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_DISCOUNT
from logic.gutils import item_utils as iutils
from logic.comsys.share.FriendHelpShareUI import FriendHelpShareUI
from common.utils.timer import CLOCK
RANK_STATUS = 0
TASK_STATUS = 1

class ActivityFriendHelp(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityFriendHelp, self).__init__(dlg, activity_type)

    def on_init_panel(self):
        self.init_parameters()
        self.init_widget()
        self.init_event()

    def on_finalize_panel(self):
        if self.rank_widget:
            self.rank_widget.destroy()
        self.task_dict = None
        global_data.emgr.receive_task_reward_succ_event -= self.update_reward_st
        return

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            log_error('[ERROR] activity [%s] task [%s] has no chidren task' % (activity_type, conf['cTask']))
            return
        else:
            self.parent_task = task_list[0]
            self.status = TASK_STATUS
            self.rank_widget = None
            self.task_dict = {}
            return

    def init_event(self):

        @self.panel.btn_personal_help.unique_callback()
        def OnClick(btn, touch):
            if self.status == TASK_STATUS:
                self.panel.StopAnimation('change')
                self.panel.PlayAnimation('revert')
                self.status = RANK_STATUS
                self.panel.btn_personal_help.SetText(606090)
            else:
                self.panel.StopAnimation('revert')
                self.panel.PlayAnimation('change')
                self.panel.PlayAnimation('show')
                self.status = TASK_STATUS
                self.panel.btn_personal_help.SetText(606091)
            return True

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(606088, 606089)

        global_data.emgr.receive_task_reward_succ_event += self.update_reward_st
        global_data.emgr.update_frd_thumbup += self.update_frd_thumbup

    def refresh_panel(self):
        self.on_init_panel()

    def init_widget(self):
        global_data.player.request_friendhelp_count()
        if global_data.channel.is_japan_korea_server():
            self.panel.PlayAnimation('revert')
            max_time = self.panel.GetAnimationMaxRunTime('revert')
            self.panel.FastForwardToAnimationTime('revert', max_time)
            self.status = RANK_STATUS
            self.init_rank_widget()
            self.panel.btn_personal_help.SetText(606090)
        else:
            self.panel.PlayAnimation('change')
            self.panel.PlayAnimation('show')
            max_time = self.panel.GetAnimationMaxRunTime('change')
            self.panel.FastForwardToAnimationTime('change', max_time)
            self.panel.btn_personal_help.setVisible(False)
            self.status = TASK_STATUS
            self.panel.btn_personal_help.SetText(606091)
        self.init_task_widget()

    def init_task_widget(self):
        self.panel.nd_content2.list_reward.DeleteAllSubItem()
        children_task = task_utils.get_children_task(self.parent_task)
        if not children_task:
            return
        for child_task in children_task[:-1]:
            nd_item = self.panel.nd_content2.list_reward.AddTemplateItem()
            self.task_dict[child_task] = nd_item.btn
            self.init_help_reward_item(nd_item, child_task)

        big_reward_task = children_task[-1]
        self.task_dict[big_reward_task] = self.panel.nd_content2.btn_big
        self.init_big_reward_btn(self.panel.nd_content2.btn_big, big_reward_task)
        self.panel.nd_content2.lab_my_time_text.lab_my_times.SetString(str(global_data.player.get_frd_thumbup()))

        @self.panel.btn_invitation_help.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('FriendHelpShareUI', 'logic.comsys.share')
            return False

    def init_help_reward_item(self, nd_item, task_id):
        reward_id = task_utils.get_task_reward(task_id)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        if not reward_list:
            return
        item_id, item_num = reward_list[0]
        help_count = task_utils.get_total_prog(task_id)
        nd_item.img_item.SetDisplayFrameByPath('', iutils.get_lobby_item_pic_by_item_no(item_id))
        if item_num > 1:
            nd_item.lab_quantity.setVisible(True)
            nd_item.lab_quantity.SetString(get_text_by_id(602012) + str(item_num))
        nd_item.nd_number_of_times.lab_times.SetString(str(help_count))
        if iutils.get_lobby_item_type(item_id) == L_ITEM_TYPE_DISCOUNT:
            discount = iutils.get_lobby_item_use_parms(item_id, {}).get('discount', 0)
            if discount:
                nd_item.bar_discount.setVisible(True)
                nd_item.lab_discount.SetString('%d%%' % (100 - 100 * discount))
        self.update_reward_st(task_id)

        @nd_item.btn.unique_callback()
        def OnClick(btn, touch):
            reward_st = global_data.player.get_task_reward_status(task_id)
            if reward_st == iconst.ITEM_UNRECEIVED:
                global_data.player.receive_task_reward(task_id)
            elif reward_st != iconst.ITEM_UNRECEIVED:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position)
            return True

    def init_big_reward_btn(self, nd_btn, task_id):
        help_count = task_utils.get_total_prog(task_id)
        nd_btn.nd_number_of_times.lab_times.SetString(str(help_count))
        self.update_reward_st(task_id)
        reward_id = task_utils.get_task_reward(task_id)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        if not reward_list:
            return
        item_id, item_num = reward_list[0]

        @nd_btn.unique_callback()
        def OnClick(btn, touch):
            reward_st = global_data.player.get_task_reward_status(task_id)
            if reward_st == iconst.ITEM_UNRECEIVED:
                global_data.player.receive_task_reward(task_id)
            return True

        @nd_btn.unique_callback()
        def OnBegin(btn, touch):
            reward_st = global_data.player.get_task_reward_status(task_id)
            if reward_st != iconst.ITEM_UNRECEIVED:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, directly_world_pos=position)
            return True

        @nd_btn.unique_callback()
        def OnEnd(btn, touch):
            reward_st = global_data.player.get_task_reward_status(task_id)
            if reward_st != iconst.ITEM_UNRECEIVED:
                global_data.emgr.hide_item_desc_ui_event.emit()
            return True

    def update_reward_st(self, task_id, *args):
        task_btn = self.task_dict.get(task_id, None)
        if not task_btn:
            return
        else:
            self.update_help_reward_st(task_btn, task_id)
            self.check_task_red_point()
            global_data.player.read_activity_list(self._activity_type)
            return

    def update_help_reward_st(self, nd_btn, task_id):
        reward_st = global_data.player.get_task_reward_status(task_id)
        if reward_st == iconst.ITEM_UNGAIN:
            nd_btn.SetShowEnable(False)
            nd_btn.SetText(get_text_by_id(81173))
        elif reward_st == iconst.ITEM_UNRECEIVED:
            nd_btn.SetShowEnable(True)
            nd_btn.SetSelect(True)
            nd_btn.SetText(get_text_by_id(80930))
        elif reward_st == iconst.ITEM_RECEIVED:
            nd_btn.SetShowEnable(False)
            nd_btn.nd_number_of_times.bar_price_forbid.setVisible(True)
            nd_btn.nd_number_of_times.bar_price_nml.setVisible(False)
            nd_btn.img_received.setVisible(True)
            nd_btn.SetText(get_text_by_id(80866))
            nd_btn.nd_number_of_times.lab_times.SetColor('#SW')
            nd_btn.nd_number_of_times.lab_times.lab.SetColor('#SW')

    def init_rank_widget(self):
        self.rank_widget = FriendHelpRankWidget(self.panel.nd_content1.nd_move.nd_list, self.panel)
        self.panel.nd_tittle.lab_number.SetString(str(global_data.player.get_frd_thumbup()))
        self.rank_widget.refresh_rank_content(rank_const.RANK_TYPE_FRIEND_HELP)

        @self.panel.btn_reward_preview.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(606083, 606084)

    def update_frd_thumbup(self):
        self.panel.nd_tittle.lab_number.SetString(str(global_data.player.get_frd_thumbup()))
        self.panel.nd_content2.lab_my_time_text.lab_my_times.SetString(str(global_data.player.get_frd_thumbup()))

    def check_task_red_point(self):
        if global_data.player.has_unreceived_task_reward(self.parent_task):
            self.panel.btn_personal_help.img_reddot.setVisible(True)
        else:
            self.panel.btn_personal_help.img_reddot.setVisible(False)