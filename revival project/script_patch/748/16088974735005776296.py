# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityVoteReturn.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from random import randint
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.client_utils import post_ui_method
from logic.comsys.activity.widget import widget
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gutils import item_utils
from common.cfg import confmgr
import cc
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_name
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils import template_utils
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.item_utils import RARE_DEGREE_ICON, get_item_rare_degree
import logic.gutils.delay as delay
REFRESH_TIME = 5

@widget('DescribeWidget')
class ActivityVoteReturn(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityVoteReturn, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._ui_data = conf.get('cUiData', {})
        self.refresh_handler = None
        self.process_event(True)
        return

    def on_init_panel(self):
        self.init_data()
        self.init_btn()
        self.init_skin_list()

    def on_finalize_panel(self):
        if self.refresh_handler:
            delay.cancel(self.refresh_handler)
        self.refresh_handler = None
        self.process_event(False)
        global_data.ui_mgr.close_ui('PrizePoolPanel')
        global_data.ui_mgr.close_ui('VoteTaskPanel')
        super(ActivityVoteReturn, self).on_finalize_panel()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.refresh_skin_list,
           'receive_task_reward_succ_event': self.refresh_skin_list,
           'receive_task_prog_reward_succ_event': self.refresh_skin_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_data(self):
        self._fixed_task_id = self._ui_data.get('taskid', None)
        self._random_task_id = self._ui_data.get('daily_random', None)
        self._prize_pool = self._ui_data.get('lottery_item', [])
        self._gstatename_list = self._ui_data.get('gstatename_list', ['ss_choose_1', 'ss_choose_2', 'ss_choose_3', 'ss_choose_4'])
        self._vote_end_time = self._ui_data.get('vote_end_time')
        self._vote_item_id = self._ui_data.get('vote_item_id')
        self._vote_num = {}
        self._vote_item_num = 0
        return

    def init_btn(self):
        if self.panel.btn_get:

            @self.panel.btn_get.callback()
            def OnClick(btn, touch):
                ui = VoteTaskPanel()
                ui.set_task_id(self._fixed_task_id, self._random_task_id)

    def init_skin_list(self):
        skin_list = self.panel.list_item
        skin_list.SetInitCount(len(self._prize_pool))
        for i, item_list in enumerate(self._prize_pool):
            item_widget = skin_list.GetItem(i)
            mecha_name = item_utils.get_lobby_item_name(self._prize_pool[i][0][0])
            item_widget.lab_name.SetString(mecha_name)
            item_widget.img_mask.setVisible(False)
            item_widget.nd_top.setVisible(False)

            @item_widget.btn_show.callback()
            def OnClick(btn, touch, prize_pool=self._prize_pool[i]):
                ui = PrizePoolPanel()
                ui.set_prize_pool(prize_pool)

            @item_widget.btn_vote.callback()
            def OnClick(btn, touch, vote_item_id=self._vote_item_id, gstatename=self._gstatename_list[i]):
                if self._vote_item_num > 0:
                    global_data.player.do_vote(vote_item_id, 1, gstatename)

        self.refresh_skin_list()

    def is_vote_over(self):
        from logic.gcommon import time_utility
        now = time_utility.time()
        return not self._vote_end_time or now >= self._vote_end_time

    @post_ui_method
    def refresh_skin_list(self, *args):
        if not global_data.player or not self.panel:
            return
        self.refresh_vote_num()
        self.refresh_vote_status()
        self.refresh_red_point()
        self.reset_refresh_timer()

    def refresh_vote_num(self):
        self._vote_item_num = global_data.player.get_item_num_by_no(self._vote_item_id)
        self.panel.lab_total.SetString(get_text_by_id(634606).format(self._vote_item_num))
        skin_list = self.panel.list_item
        for i, gstat in enumerate(self._gstatename_list):
            self._vote_num[gstat] = global_data.player.get_vote_data(gstat)
            item_widget = skin_list.GetItem(i)
            item_widget.bar_number_1.setVisible(False)
            item_widget.bar_number_2.setVisible(True)
            item_widget.bar_number_2.lab_number.SetString(get_text_by_id(634602).format(self._vote_num[gstat]))
            item_widget.btn_vote.SetEnable(self._vote_item_num > 0)

        rank_list = sorted(six_ex.keys(self._vote_num), key=lambda x: [self._vote_num[x], x], reverse=True)
        if rank_list and rank_list[0]:
            first_item_widget = skin_list.GetItem(self._gstatename_list.index(rank_list[0]))
            first_item_widget.bar_number_2.setVisible(False)
            first_item_widget.bar_number_1.setVisible(True)
            first_item_widget.bar_number_1.lab_number.SetString(first_item_widget.bar_number_2.lab_number.GetString())
            first_item_widget.bar_number_1.lab_rank.SetString('1')
        for i, gstat in enumerate(rank_list):
            item_widget = skin_list.GetItem(self._gstatename_list.index(gstat))
            item_widget.bar_number_2.lab_rank.SetString(str(i + 1))

    def refresh_vote_status(self):
        vote_status = self.is_vote_over()
        self.panel.btn_get.setVisible(not vote_status)
        self.panel.lab_total.setVisible(not vote_status)
        self.panel.lab_tips.setVisible(vote_status)
        if vote_status:
            skin_list = self.panel.list_item
            for i in range(len(skin_list.GetAllItem())):
                item_widget = skin_list.GetItem(i)
                item_widget.btn_vote.SetEnable(False)
                item_widget.btn_vote.setVisible(False)
                if item_widget.bar_number_2.lab_rank.GetString() != '1':
                    item_widget.bar_number_2.lab_number.SetString(get_text_by_id(168).format(item_widget.bar_number_2.lab_rank.GetString()))
                    item_widget.img_mask.setVisible(True)
                    item_widget.nd_top.setVisible(False)
                else:
                    item_widget.nd_top.setVisible(True)
                    item_widget.img_mask.setVisible(False)
                    item_widget.bar_number_1.lab_number.SetString(get_text_by_id(634022))

        else:
            skin_list = self.panel.list_item
            for i in range(len(skin_list.GetAllItem())):
                item_widget = skin_list.GetItem(i)
                item_widget.btn_vote.SetEnable(True)
                item_widget.btn_vote.setVisible(True)

    def refresh_red_point(self):
        from logic.gcommon.item.item_const import ITEM_UNRECEIVED
        if self.is_vote_over():
            return
        global_data.emgr.refresh_activity_redpoint.emit()
        task_list = task_utils.get_children_task(self._fixed_task_id)
        for task_id in task_list:
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                self.panel.temp_red.setVisible(True)
                return

        self.panel.temp_red.setVisible(False)

    def reset_refresh_timer(self):
        if self.refresh_handler:
            delay.cancel(self.refresh_handler)
        self.refresh_handler = None
        self.refresh_handler = delay.call(REFRESH_TIME, lambda : self.refresh_skin_list_by_timer())
        return

    def refresh_skin_list_by_timer(self):
        self.refresh_handler = None
        self.refresh_skin_list()
        return


class PrizePoolPanel(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202301/ss_choose/open_ss_choose_preview'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE

    def on_init_panel(self):
        super(PrizePoolPanel, self).on_init_panel()

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

    def set_prize_pool(self, prize_pool):
        self._prize_pool = prize_pool
        self.refresh_prize_pool_list()

    def refresh_prize_pool_list(self):
        self.panel.list_item.SetInitCount(len(self._prize_pool))
        for i, item_list in enumerate(self._prize_pool):
            item_widget = self.panel.list_item.GetItem(i)
            item_widget.list_reward.SetInitCount(len(self._prize_pool[i]))
            if self._prize_pool[i]:
                item_widget.temp_level.bar_level.SetDisplayFrameByPath('', RARE_DEGREE_ICON[get_item_rare_degree(int(self._prize_pool[i][0]))])
            for idx, item_no in enumerate(self._prize_pool[i]):
                reward_item = item_widget.list_reward.GetItem(idx)
                init_tempate_mall_i_item(reward_item, item_no, 1, show_tips=True)


class VoteTaskPanel(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202301/ss_choose/open_ss_choose_task'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    GLOBAL_EVENT = {'task_prog_changed': '_on_update_task',
       'receive_task_reward_succ_event': '_on_update_task',
       'receive_task_prog_reward_succ_event': '_on_update_task'
       }

    def on_init_panel(self):
        super(VoteTaskPanel, self).on_init_panel()

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

    def set_task_id(self, fixed_task_id, random_task_id):
        self._fixed_task_id = fixed_task_id
        self._random_task_id = random_task_id
        self.refresh_panel()

    @post_ui_method
    def _on_update_task(self, *args):
        self.refresh_panel()

    def refresh_panel(self):
        self._refresh_task_list()
        self._refresh_list_content()
        self._refresh_list_status()

    def _refresh_task_list(self):
        player = global_data.player
        fixed_task_list = task_utils.get_children_task(self._fixed_task_id)
        if not fixed_task_list:
            log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe5\x9b\xba\xe5\xae\x9a\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._fixed_task_id)
            fixed_task_list = [self._fixed_task_id]
        if self._random_task_id:
            random_refresh_type = task_utils.get_task_fresh_type(self._random_task_id)
            random_task_list = player.get_random_children_tasks(random_refresh_type, self._random_task_id)
            if not random_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._random_task_id)
                random_task_list = []
            task_list = fixed_task_list + random_task_list
        else:
            task_list = fixed_task_list
        self._task_list = task_list

    def _refresh_list_content(self):
        sub_list = self.panel.list_item
        sub_list.SetInitCount(len(self._task_list))
        for i, task_id in enumerate(self._task_list):
            item_widget = sub_list.GetItem(i)
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

    def _refresh_list_status(self):
        sub_list = self.panel.list_item
        for i, task_id in enumerate(self._task_list):
            task_id = str(task_id)
            item_widget = sub_list.GetItem(i)
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            reward_id = task_utils.get_task_reward(task_id)
            if reward_id is None:
                is_prog_task = True if 1 else False
                cur_prog = global_data.player.get_task_prog(task_id)
                if is_prog_task:
                    prog_rewards = task_utils.get_task_prog_rewards(task_id)
                    max_prog = prog_rewards[-1][0]
                    for prog, reward_id in prog_rewards:
                        if not global_data.player.has_receive_prog_reward(task_id, prog):
                            if cur_prog >= prog:
                                status = ITEM_UNRECEIVED
                            else:
                                status = ITEM_UNGAIN
                            break
                    else:
                        status = ITEM_RECEIVED

                    total_prog = prog
                    task_parm_dict = {'prog': total_prog}
                else:
                    task_parm_dict = None
                    max_prog = total_prog = task_utils.get_total_prog(task_id)
                    status = global_data.player.get_task_reward_status(task_id)
                self.__update_lab_num(item_widget, total_prog, cur_prog)
                btn = item_widget.temp_btn_get.btn_common
                item_widget.nd_get.setVisible(False)
                self._update_receive_btn(task_id, status, item_widget)

                @btn.unique_callback()
                def OnClick(btn, touch, _task_id=task_id, _cur_prog=cur_prog, _total_prog=total_prog, _max_prog=max_prog, _is_prog_task=is_prog_task):
                    if _cur_prog < _total_prog:
                        jump_conf = task_utils.get_jump_conf(_task_id)
                        item_utils.exec_jump_to_ui_info(jump_conf)
                    else:
                        if _is_prog_task:
                            global_data.player.receive_task_prog_reward(_task_id, _total_prog)
                        else:
                            global_data.player.receive_task_reward(_task_id)
                        if _max_prog == _total_prog:
                            btn.SetText(80866)
                            btn.SetEnable(False)

        return

    def __update_lab_num(self, item_widget, total_times, cur_times):
        if total_times > 1:
            item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('')

    def _update_receive_btn(self, task_id, status, ui_item):
        btn_receive = ui_item.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                update_task_list_btn(btn_receive, BTN_ST_GO, {'btn_text': jump_conf.get('unreach_text', '')})
            else:
                update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)