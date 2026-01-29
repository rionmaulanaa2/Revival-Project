# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySeasonKill.py
from __future__ import absolute_import
from six.moves import range
import time
import cc
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gcommon.common_const import rank_const, rank_activity_const
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.role_head_utils import init_role_head, init_role_head_auto
from logic.gutils import template_utils
from logic.comsys.rank.GlMainRank import GlMainRank
from common.const.uiconst import NORMAL_LAYER_ZORDER_3
from logic.gutils.template_utils import show_left_time
from logic.gutils.activity_utils import get_left_time
from logic.gutils import task_utils
UPDATE_TIME = 60
RANK_TYPE = 0
KILL_TYPE = 1

class MainRank(GlMainRank):
    PANEL_CONFIG_NAME = 'activity/activity_202207/bp_sprint/open_bp_sprint_window'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3


class ActivitySeasonKill(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySeasonKill, self).__init__(dlg, activity_type)
        self.init_parameters()

    def on_init_panel(self):
        self.cUiData = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.task_id = str(self.cUiData.get('task_id'))

        @self.panel.btn_rank.callback()
        def OnClick(*args):
            ui = MainRank(None, self.cur_rank_type)
            title = self.cUiData.get('title_id')
            ui.set_title(get_text_by_id(title))
            return

        @self.panel.btn_get.callback()
        def OnClick(*args):
            if global_data.player:
                if self.reward_type == RANK_TYPE:
                    global_data.player.request_offer_rank_reward(self.cur_rank_type)
                else:
                    global_data.player.receive_all_task_prog_reward(self.task_id)

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            rule = confmgr.get('c_activity_config', str(self._activity_type), 'cRuleTextID', default='')
            title = confmgr.get('c_activity_config', str(self._activity_type), 'cNameTextID', default='')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

        all_items = self.panel.list_tab.GetAllItem()
        for index, item in enumerate(all_items):
            item.btn_top.EnableCustomState(True)
            item.btn_top.SetSelect(self.reward_type == index)

            @item.btn_top.callback()
            def OnClick(btn, touch, index=index):
                if not self.panel:
                    return
                if self.reward_type == index:
                    return
                nd = self.panel.list_tab.GetItem(self.reward_type)
                nd and nd.btn_top.SetSelect(False)
                if index == RANK_TYPE:
                    self.init_rank_reward_list()
                    btn.SetSelect(True)
                else:
                    self.init_kill_reward_list()
                    btn.SetSelect(True)
                self.reward_type = index
                self.refresh_btn_get()

        self.process_event(True)
        self.register_timer()
        self.second_callback()
        if self.reward_type == RANK_TYPE:
            self.init_rank_reward_list()
        else:
            self.init_kill_reward_list()
        rank_data = global_data.message_data.get_rank_data(self.cur_rank_type)
        if not rank_data or len(rank_data['rank_list']) < 4:
            self.panel.nd_content.setVisible(False)
            self.panel.nd_empty.setVisible(True)
        else:
            self.panel.nd_content.setVisible(True)
            self.panel.nd_empty.setVisible(False)
            self.refresh_rank_content(self.cur_rank_type)
        self.request_rank_data()
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
        self.panel.lab_describe.SetString(int(desc_id))

    def init_parameters(self):
        self.reward_type = RANK_TYPE
        self._timer = None
        self._times = 0
        self._balance_time = False
        self.sub_widget = None
        self._need_ani = True
        self._old_rank = None
        self.ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self.cur_rank_type = self.ui_data.get('rank_type')
        self.balance_end_ts = rank_activity_const.get_rank_reward_timestamp(self.cur_rank_type, 5)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(self._activity_type), 'iCatalogID', default='')
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.sub_widget = None
        self.unregister_timer()
        super(ActivitySeasonKill, self).on_finalize_panel()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_rank_data': self.refresh_rank_content_from_event,
           'receive_rank_reward_success': self._refresh,
           'receive_rank_reward_fail': self._refresh,
           'receive_task_reward_succ_event': self._refresh,
           'receive_task_prog_reward_succ_event': self._refresh,
           'task_prog_changed': self._refresh
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def second_callback(self):
        balance_left_time = self.get_left_balance_time()
        if not self._balance_time:
            if balance_left_time > 0:
                self._balance_time = True
        if self._balance_time:
            left_time_delta = get_left_time(self._activity_type)
            show_left_time(self.panel.lab_time_tips, left_time_delta, '')
            self.panel.lab_tips.SetString(611562)
        else:
            show_left_time(self.panel.lab_time_tips, -balance_left_time, '')
            self.panel.lab_tips.SetString(633700)
        self.refresh_btn_get()
        self._times += 1
        if self._times > UPDATE_TIME + 2:
            self.request_rank_data()

    def request_rank_data(self):
        rank_data = global_data.message_data.get_rank_data(self.cur_rank_type)
        if not rank_data or time.time() - rank_data['save_time'] > UPDATE_TIME:
            global_data.message_data.clean_rank_data(self.cur_rank_type)
            if global_data.player:
                global_data.player.request_rank_list(self.cur_rank_type, 0, rank_const.RANK_ONE_REQUEST_MAX_COUNT, True, True)

    def refresh_rank_content(self, rank_type, is_from_event=False):
        if rank_type != self.cur_rank_type:
            return
        else:
            rank_data = global_data.message_data.get_rank_data(rank_type)
            if not rank_data:
                return
            my_rank = rank_data['player_rank']
            my_data = rank_data['player_data']
            data_lst = rank_data['rank_list']
            if len(data_lst) < 4:
                return
            if my_rank >= 1 and my_rank <= 4:
                end_idx = 4 if 1 else 3
                name_nodes = [ getattr(self.panel, 'lab_name_%s' % x) for x in range(1, 5) ]
                lab_nodes = [ getattr(self.panel, 'lab_%s' % x) for x in range(1, 5) ]
                head_nodes = [ getattr(self.panel, 'temp_head_%s' % x) for x in range(1, 5) ]
                img_me_nodes = [ getattr(self.panel, 'img_me_%s' % x) for x in range(1, 5) ]
                for x in range(0, end_idx):
                    img_me_nodes[x].setVisible(False)
                    data = data_lst[x]
                    uid = data[0]
                    if global_data.player and global_data.player.uid == data[0]:
                        head_frame = global_data.player.get_head_frame()
                        head_photo = global_data.player.get_head_photo()
                        name_nodes[x].setString(global_data.player.get_name() if global_data.player else '')
                        img_me_nodes[x].setVisible(True)
                    else:
                        char_name, role_id, head_frame, head_photo = data[1]
                        name_nodes[x].setString(str(char_name))
                    init_role_head_auto(head_nodes[x], uid, show_tips=True, head_frame=head_frame, head_photo=head_photo)
                    lab_nodes[x].setString(str(data[2][0]))
                    if x == 3:
                        self.panel.lab_rank_4.setString('No.' + str(data[3] + 1))

                if end_idx == 3:
                    self.panel.img_me_4.setVisible(True)
                    self.panel.lab_4.setString(str(my_data[2][0]))
                    head_frame = global_data.player.get_head_frame()
                    head_photo = global_data.player.get_head_photo()
                    self.panel.lab_name_4.setString(global_data.player.get_name() if global_data.player else '')
                    init_role_head(self.panel.temp_head_4, head_frame, head_photo)
                    if my_rank == rank_const.RANK_DATA_OUTSIDE:
                        text = get_text_by_id(15016)
                    elif my_rank == rank_const.RANK_DATA_NONE:
                        text = '-'
                    else:
                        text = 'NO.' + str(my_rank) if my_rank <= 1000 else get_text_by_id(15016)
                    self.panel.lab_rank_4.setString(text)
                self.panel.nd_content.setVisible(True)
                self.panel.nd_empty.setVisible(False)
                if is_from_event:
                    if self._need_ani:
                        self._need_ani = False
                        self.check_ani(my_rank)
                    if self._old_rank is not None and (self._old_rank <= 3 and my_rank > 3 or self._old_rank > 3 and my_rank >= 3):
                        self.panel.StopAnimation('show_many')
                        self.panel.StopAnimation('show_three')
                        ani_name = 'show_three' if my_rank <= 3 and my_rank > 0 else 'show_many'
                        self.panel.PlayAnimation(ani_name)
            self._old_rank = my_rank
            return

    def refresh_rank_content_from_event(self, rank_type):
        self.refresh_rank_content(rank_type, is_from_event=True)

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget
        if not self.sub_widget:
            return
        self.sub_widget.set_show(True)

    def set_show(self, show, is_init=False):
        super(ActivitySeasonKill, self).set_show(show, is_init)
        if show:
            rank_data = global_data.message_data.get_rank_data(self.cur_rank_type)
            if not rank_data:
                self._need_ani = True
                return
            self._need_ani = False
            my_rank = rank_data['player_rank']
            my_data = rank_data['player_data']
            data_lst = rank_data['rank_list']
            self.check_ani(my_rank)

    def check_ani(self, my_rank):
        if my_rank <= 3 and my_rank > 0:
            ani_name = 'show_three' if 1 else 'show_many'
            if self.cur_tab_name_id == self.last_tab_name_id:
                self.panel.StopAnimation('show_many')
                self.panel.StopAnimation('show_three')
                self.panel.PlayAnimation(ani_name)
                self.panel.IsPlayingAnimation('loop') or self.panel.PlayAnimation('loop')
            return
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('show_many')
        self.panel.StopAnimation('show_three')
        self.panel.StopAnimation('loop')
        show_time = self.panel.GetAnimationMaxRunTime('show')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : [self.panel and self.panel.PlayAnimation('show'), self.sub_widget and self.sub_widget.panel and self.sub_widget.panel.PlayAnimation('show')]),
         cc.DelayTime.create(0.16),
         cc.CallFunc.create(lambda : self.panel and self.panel.PlayAnimation(ani_name)),
         cc.DelayTime.create(show_time),
         cc.CallFunc.create(lambda : self.panel and self.panel.PlayAnimation('loop'))]))

    def get_left_balance_time(self):
        return time_utility.time() - self.balance_end_ts

    def refresh_btn_get(self, *args):
        self.panel.lab_tip.setVisible(False)
        all_items = self.panel.list_tab.GetAllItem()
        for item in all_items:
            item.img_red.setVisible(False)

        can_receive = False
        cfg_data = rank_activity_const.get_rank_reward_list(self.cur_rank_type)
        rank_data = global_data.message_data.get_rank_data(self.cur_rank_type)
        if cfg_data and rank_data:
            my_rank = rank_data['player_rank']
            max_rank, reward_id = cfg_data[-1]
            can_receive = my_rank <= max_rank and my_rank > 0
        received = global_data.player and global_data.player.is_offer_rank_reward(self.cur_rank_type)
        not_in_rank = global_data.player and global_data.player.is_not_participate_rank(self.cur_rank_type)
        unreceived = task_utils.has_unreceived_prog_reward(self.task_id)
        self.panel.list_tab.GetItem(RANK_TYPE).img_red.setVisible(can_receive and not not_in_rank and not received and self._balance_time)
        self.panel.list_tab.GetItem(KILL_TYPE).img_red.setVisible(unreceived and not not_in_rank)
        if self.reward_type == RANK_TYPE:
            if received:
                text_id = 80834
                enable = False
            elif not_in_rank:
                text_id = 606010
                enable = False
                self.panel.lab_tip.setVisible(True)
                self.panel.lab_tip.SetString(15043)
            elif not can_receive:
                text_id = 80834
                enable = False
            else:
                text_id = 80834
                enable = True
            if not self._balance_time:
                text_id = 80834
                enable = False
        elif unreceived:
            text_id = 80834
            enable = True
        elif not_in_rank:
            text_id = 606010
            enable = False
            self.panel.lab_tip.setVisible(True)
            self.panel.lab_tip.SetString(15043)
        else:
            text_id = 80834
            enable = False
        self.panel.btn_get.SetText(text_id)
        self.panel.btn_get.SetEnable(enable)
        self.panel.btn_get.SetShowEnable(enable)

    def _refresh(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.refresh_btn_get()
        if self.reward_type != RANK_TYPE:
            self.init_kill_reward_list()

    def init_rank_reward_list(self):
        data = rank_activity_const.get_rank_reward_list(self.cur_rank_type)
        reward_info = []
        last_rank = 0
        for idx, info in enumerate(data):
            rank, reward_id = info
            text = get_text_by_id(81182).format(last_rank + 1, rank)
            last_rank = rank
            reward_info.append([text, reward_id])

        self.panel.list_item.SetInitCount(len(reward_info) + 1)
        nd = self.panel.list_item.GetItem(len(reward_info))
        nd and nd.setVisible(False)
        for i in range(len(reward_info)):
            nd_item = self.panel.list_item.GetItem(i)
            if nd_item:
                nd_item.setVisible(True)
                text, reward_id = reward_info[i]
                nd_item.lab_rank.SetString(text)
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                nd_item.list_item.SetInitCount(len(reward_list))
                for ind, info in enumerate(reward_list):
                    item_no, item_num = info
                    item_temp = nd_item.list_item.GetItem(ind)
                    template_utils.init_tempate_mall_i_item(item_temp, item_no, item_num, show_rare_degree=True, show_tips=True)
                    item_temp.btn_choose.SetClipObject(self.panel.list_item)

    def init_kill_reward_list(self):
        prog_rewards = task_utils.get_prog_rewards(self.task_id)
        reward_info = []
        for idx, info in enumerate(prog_rewards):
            progress, reward_id = info
            text = get_text_by_id(633874).format(progress)
            reward_info.insert(0, [text, reward_id, progress])

        self.panel.list_item.SetInitCount(len(reward_info) + 1)
        nd = self.panel.list_item.GetItem(len(reward_info))
        nd and nd.setVisible(False)
        for i in range(len(reward_info)):
            nd_item = self.panel.list_item.GetItem(i)
            if nd_item:
                nd_item.setVisible(True)
                text, reward_id, progress = reward_info[i]
                has_receive = global_data.player.has_receive_prog_reward(self.task_id, progress)
                nd_item.lab_rank.SetString(text)
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                nd_item.list_item.SetInitCount(len(reward_list))
                for ind, info in enumerate(reward_list):
                    item_no, item_num = info
                    item_temp = nd_item.list_item.GetItem(ind)
                    template_utils.init_tempate_mall_i_item(item_temp, item_no, item_num, isget=has_receive, show_rare_degree=True, show_tips=True)
                    item_temp.btn_choose.SetClipObject(self.panel.list_item)