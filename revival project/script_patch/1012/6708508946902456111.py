# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonCollectExchange.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget import widget, Widget
from logic.gutils import task_utils
from logic.gutils.client_utils import post_method
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no, jump_to_player_info

@widget('AsyncExchangeListWidget', 'DescribeWidget')
class ActivityCommonCollectExchange(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommonCollectExchange, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._collect_task = conf.get('cTask', '')
        self._gun_item_no = ui_data.get('gun_item_no', '208100409')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._refresh_gun_progress,
           'receive_task_prog_reward_succ_event': self._refresh_gun_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityCommonCollectExchange, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityCommonCollectExchange, self).on_init_panel()
        self.process_event(True)
        if not self.panel.HasRecordedAnimationNodeState('get_tips'):
            self.panel.RecordAnimationNodeState('get_tips')
        self._init_gun_progress()
        self._refresh_gun_progress()

    def refresh_panel(self):
        super(ActivityCommonCollectExchange, self).refresh_panel()
        self._refresh_gun_progress()

    def _init_gun_progress(self):

        @self.panel.btn_gun_see.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import item_utils
            from logic.gcommon.item import lobby_item_type
            item_no = self._gun_item_no
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type == lobby_item_type.L_ITEM_TYPE_VIRTUAL:
                from logic.comsys.role.PlayerInfoUI import TAB_CAREER_MEDAL
                jump_to_player_info(TAB_CAREER_MEDAL)
            else:
                jump_to_display_detail_by_item_no(self._gun_item_no)

        @self.panel.nd_touch.callback()
        def OnClick(btn, touch):
            player = global_data.player
            if player.has_unreceived_task_reward(self._collect_task):
                player.receive_task_reward(self._collect_task)
            elif task_utils.has_unreceived_prog_reward(self._collect_task):
                player.receive_all_task_prog_reward(self._collect_task)
            else:
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                prog_reward_list = task_utils.get_task_prog_rewards(self._collect_task)
                reward_id = prog_reward_list[-1][1]
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                item_no, item_num = reward_list[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return True
            return

    @post_method
    def _refresh_gun_progress(self, *args):
        if not global_data.player or not self.panel:
            return
        player = global_data.player
        if task_utils.get_task_prog_rewards(self._collect_task):
            now_prog = global_data.player.get_task_prog(self._collect_task)
            max_pro = task_utils.get_total_prog(self._collect_task)
            prog = min(int(100 * now_prog / float(max_pro)), 100)
            self.panel.prog_inside.SetPercentage(prog)
            last_reward_is_received = player.has_receive_prog_reward(self._collect_task, max_pro)
            if task_utils.has_unreceived_prog_reward(self._collect_task):
                self.panel.PlayAnimation('get_tips')
            elif last_reward_is_received:
                self.panel.icon_tick.setVisible(True)
                self.panel.StopAnimation('get_tips')
                self.panel.RecoverAnimationNodeState('get_tips')