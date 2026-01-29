# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/GlobalAchievementWidget.py
from __future__ import absolute_import
from logic.gutils import template_utils
from common.cfg import confmgr
from .ActivityWidgetBase import ActivityWidgetBase

class GlobalAchievementWidget(ActivityWidgetBase):
    GLOBAL_EVENT = {'message_update_global_reward_receive': 'refresh_reward_content',
       'message_update_global_stat': 'update_server_num'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.refresh_reward_content()
        self.update_server_num()
        self.register_timer()

    def on_finalize_panel(self):
        if self.local_num is not None:
            global_data.player and global_data.player.set_simulate_cache(self.achieve_name, self.local_num)
        self.unregister_timer()
        super(GlobalAchievementWidget, self).on_finalize_panel()
        return

    def init_parameters(self):
        self.children_ids = confmgr.get('c_activity_config', self.activity_id, 'cUiData', 'global_achieve_id', default=[])
        first_id = self.children_ids[0]
        self.parent_id = str(confmgr.get('global_achieve_data', first_id, 'cParentID', default=first_id))
        self.achieve_name = confmgr.get('global_achieve_data', first_id, 'cGStatName', default='share')
        self.share_prog = [ confmgr.get('global_achieve_data', aid, 'iCondValue') for aid in self.children_ids ]
        self.server_num = 0
        self.local_num = 0
        self.increase_num = 0
        self._times = 0
        self._timer = None
        self._is_first_open = True
        return

    def refresh_reward_content(self, *args):
        pass

    def update_progress(self):
        pass

    def update_server_num(self, *args):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            self.update_progress()
            return
        else:
            latest_num = global_stat_data.get(self.parent_id, {}).get(self.achieve_name, 0)
            if latest_num < 0:
                return
            if self._is_first_open:
                import random
                last_cache = global_data.player or 0 if 1 else global_data.player.get_simulate_cache(self.achieve_name)
                if last_cache >= latest_num:
                    last_cache = latest_num
                self.local_num = max(int(last_cache), int(latest_num * 0.99))
                random_num = random.uniform(5000, 15000)
                if latest_num - random_num > 0:
                    self.local_num = max(self.local_num, random_num)
                self._is_first_open = False
            if self.server_num == latest_num:
                return
            self.server_num = latest_num
            if self.extra_conf.get('need_sim', False):
                self.local_num = min(self.server_num, self.local_num)
            else:
                self.local_num = self.server_num
            self.increase_num = (self.server_num - self.local_num) / self.extra_conf.get('sim_interval', 20)
            self.update_progress()
            return

    def second_simulate_up(self, *args):
        self.local_num += self.increase_num
        if self.local_num >= self.server_num:
            self.local_num = self.server_num
        self.update_progress()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def second_callback(self):
        self.second_simulate_up()
        self._times += 1
        if self._times > 10:
            self.update_server_num()
            self._times = 0