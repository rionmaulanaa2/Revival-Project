# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGlRank.py
from __future__ import absolute_import
from six.moves import range
import time
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gcommon.common_const import rank_const, rank_activity_const
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.role_head_utils import init_role_head, init_role_head_auto
from logic.gutils import template_utils
UPDATE_TIME = 60
title_map = {activity_const.ACTIVITY_520_GL_RANK_1: 15093,
   activity_const.ACTIVITY_520_GL_RANK_2: 15094
   }

class ActivityGlRank(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGlRank, self).__init__(dlg, activity_type)
        self._timer = None
        self._times = 0
        self._balance_time = False
        global_data.emgr.message_on_rank_data += self.refresh_rank_content_from_event
        global_data.emgr.receive_rank_reward_success += self._refresh
        global_data.emgr.receive_rank_reward_fail += self._refresh
        self.sub_widget = None
        self._need_ani = True
        self._old_rank = None
        self.init_parameters()
        self.register_timer()
        self.init_ui_event()
        self.init_panel()
        self.second_callback()
        return

    def init_panel(self):
        self.init_rank_reward_list()
        rank_data = global_data.message_data.get_rank_data(self.cur_rank_type)
        if not rank_data or len(rank_data['rank_list']) < 4:
            self.panel.nd_content.setVisible(False)
            self.panel.nd_dec.setVisible(False)
            self.panel.nd_empty.setVisible(True)
        else:
            self.panel.nd_content.setVisible(True)
            self.panel.nd_dec.setVisible(True)
            self.panel.nd_empty.setVisible(False)
            self.refresh_rank_content(self.cur_rank_type)
        self.request_rank_data()
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
        self.panel.lab_describe.SetString(int(desc_id))

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
                self.panel.nd_dec.setVisible(True)
                self.panel.nd_empty.setVisible(False)
                if is_from_event:
                    if self._need_ani:
                        self._need_ani = False
                        self.check_ani(my_rank)
                    if self._old_rank is not None and (self._old_rank <= 3 and my_rank > 3 or self._old_rank > 3 and my_rank >= 3):
                        self.panel.StopAnimation('show_many')
                        self.panel.StopAnimation('show_three')
                        ani_name = 'show_three' if my_rank <= 3 else 'show_many'
                        self.panel.PlayAnimation(ani_name)
            self._old_rank = my_rank
            return

    def refresh_rank_content_from_event(self, rank_type):
        self.refresh_rank_content(rank_type, is_from_event=True)

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(ActivityGlRank, self).set_show(show, is_init)
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
        if my_rank <= 3:
            ani_name = 'show_three' if 1 else 'show_many'
            if self.cur_tab_name_id == self.last_tab_name_id:
                self.panel.StopAnimation('show_many')
                self.panel.StopAnimation('show_three')
                self.panel.PlayAnimation(ani_name)
                self.panel.IsPlayingAnimation('loop') or self.panel.PlayAnimation('loop')
            return
        import cc
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('show_many')
        self.panel.StopAnimation('show_three')
        self.panel.StopAnimation('loop')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : [self.panel.PlayAnimation('show'), self.sub_widget and self.sub_widget.panel.PlayAnimation('show')]),
         cc.DelayTime.create(0.16),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(ani_name)),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))

    def init_parameters(self):
        self.ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self.cur_rank_type = self.ui_data.get('rank_type')
        self.balance_end_ts = rank_activity_const.get_rank_reward_timestamp(self.cur_rank_type, 5)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(self._activity_type), 'iCatalogID', default='')
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def second_callback(self):
        from logic.gutils.activity_utils import get_left_time
        if not self._balance_time:
            left_time = self.get_left_balance_time()
            text_id = 81178
            if left_time > 0:
                self._balance_time = True
                left_time = get_left_time(self._activity_type)
                text_id = 81188
        else:
            left_time = get_left_time(self._activity_type)
            text_id = 81188
        self.refresh_btn_get()
        self._times += 1
        if self._times > UPDATE_TIME + 2:
            self.request_rank_data()

    def get_left_balance_time(self):
        return time_utility.time() - self.balance_end_ts

    def refresh_btn_get(self, *args):
        self.panel.lab_tip.setVisible(False)
        if not self._balance_time:
            text_id = 606010
            enable = False
        else:
            received = global_data.player and global_data.player.is_offer_rank_reward(self.cur_rank_type)
            not_in_rank = global_data.player and global_data.player.is_not_participate_rank(self.cur_rank_type)
            if received:
                text_id = 80866
                enable = False
            elif not_in_rank:
                text_id = 606010
                enable = False
                self.panel.lab_tip.setVisible(True)
                self.panel.lab_tip.SetString(15043)
            else:
                text_id = 606010
                enable = True
        self.panel.btn_get.SetText(text_id)
        self.panel.btn_get.SetEnable(enable)
        self.panel.btn_get.SetShowEnable(enable)

    def _refresh(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.refresh_btn_get()

    def init_ui_event(self):

        @self.panel.btn_rank.callback()
        def OnClick(*args):
            from logic.comsys.rank.GlMainRank import GlMainRank
            ui = GlMainRank(None, self.cur_rank_type)
            title = title_map.get(str(self._activity_type), '')
            ui.set_title(get_text_by_id(title))
            return

        @self.panel.btn_get.callback()
        def OnClick(*args):
            global_data.player and global_data.player.request_offer_rank_reward(self.cur_rank_type)

        def show_game_rule(*args):
            rule = confmgr.get('c_activity_config', str(self._activity_type), 'cRuleTextID', default='')
            title = confmgr.get('c_activity_config', str(self._activity_type), 'cNameTextID', default='')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

        self.panel.lab_describe.SetCallback(show_game_rule)

    def on_finalize_panel(self):
        self.sub_widget = None
        self.unregister_timer()
        global_data.emgr.message_on_rank_data -= self.refresh_rank_content
        global_data.emgr.receive_rank_reward_success -= self._refresh
        global_data.emgr.receive_rank_reward_fail -= self._refresh
        super(ActivityGlRank, self).on_finalize_panel()
        return

    def init_rank_reward_list(self):
        data = rank_activity_const.get_rank_reward_list(self.cur_rank_type)
        reward_info = []
        last_rank = 0
        for idx, info in enumerate(data):
            rank, reward_id = info
            text = get_text_by_id(81182).format(last_rank + 1, rank)
            if idx == len(data) - 1:
                text = get_text_by_id(81183).format(last_rank)
            last_rank = rank
            reward_info.append([text, reward_id])

        self.panel.list_item.SetInitCount(len(reward_info))
        for i in range(len(reward_info)):
            nd_item = self.panel.list_item.GetItem(i)
            if nd_item:
                text, reward_id = reward_info[i]
                nd_item.lab_rank.SetString(text)
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                nd_item.list_item.SetInitCount(len(reward_list))
                for ind, info in enumerate(reward_list):
                    item_no, item_num = info
                    item_temp = nd_item.list_item.GetItem(ind)
                    template_utils.init_tempate_mall_i_item(item_temp, item_no, item_num, show_rare_degree=True, show_tips=True)