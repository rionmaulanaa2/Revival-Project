# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202209/ActivitySeasonShare.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS, get_simply_time
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_RECEIVED
from logic.gutils.client_utils import post_ui_method
import cc
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class SeasonWarmupShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_SEASON_WARMUP'

    def __init__(self):
        super(SeasonWarmupShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, task_count=4, show_indexes=(), activity_type=None, txt_cd='', tmpl=None, init_cb=None):
        super(SeasonWarmupShareCreator, self).create(parent, tmpl)
        self.task_count = task_count
        self.show_indexes = show_indexes
        self._activity_type = activity_type
        self.init_cb = init_cb
        self.txt_cd = txt_cd
        panel = self.panel.temp_activity
        panel.lab_title_tips.SetString(get_text_by_id(611637, [task_count]))
        panel.lab_share_tips.SetString(get_text_by_id(611635, [task_count]))
        panel.lab_reward_tips.SetString(get_text_by_id(611636, [task_count]))
        panel.temp_btn_share.setVisible(False)
        for i in range(task_count):
            nd = getattr(panel, 'temp_%d' % (i + 1))
            if nd:
                self.init_share_temp(nd, i in self.show_indexes)

        self.panel.temp_activity.lab_time.SetString(txt_cd)
        if callable(init_cb):
            init_cb()

    def refresh_cd_txt(self, txt_cd):
        self.txt_cd = txt_cd
        self.panel.temp_activity.lab_time.SetString(txt_cd)

    def init_share_temp(self, ui_item, is_vis):
        ui_item.bar_tips.setVisible(False)
        ui_item.bar_prog.setVisible(False)
        ui_item.SetSelect(is_vis)

    def destroy(self):
        super(SeasonWarmupShareCreator, self).destroy()
        self.init_cb = None
        return

    def recreate_panel(self):
        self.destroy_panel()
        self.create(parent=None, task_count=self.task_count, show_indexes=self.show_indexes, activity_type=self._activity_type, txt_cd=self.txt_cd, init_cb=self.init_cb)
        return


class ActivitySeasonShare(ActivityTemplate):

    def on_init_panel(self):
        super(ActivitySeasonShare, self).on_init_panel()
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        children_tasks = task_utils.get_children_task(self._task_id)
        self._children_tasks = children_tasks
        self.ui_data = activity_conf.get('cUiData', {})
        self.widget_map = {}
        self._share_content = None
        self.panel.lab_title_tips.SetString(get_text_by_id(611637, [len(children_tasks)]))
        self.panel.lab_share_tips.SetString(get_text_by_id(611635, [len(children_tasks)]))
        self.panel.lab_reward_tips.SetString(get_text_by_id(611636, [len(children_tasks)]))
        self.init_countdown_widget()
        self.refresh_list()

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        @self.panel.temp_btn_share.btn_common_big.callback()
        def OnClick(btn, touch):
            self.on_share()

        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'task_prog_changed': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    @post_ui_method
    def _on_update_reward(self, *args):
        self.refresh_list()
        self.refresh_share()

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        ex_data = {'txt_id': 906607}
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type, ex_data)

    def on_finalize_panel(self):
        super(ActivitySeasonShare, self).on_finalize_panel()
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        self.activity_conf = {}
        if self._share_content:
            self._share_content.destroy()
            self._share_content = None
        return

    def refresh_list(self):
        total_cur_prog = global_data.player.get_task_prog(self._task_id)
        total_prog = task_utils.get_total_prog(self._task_id)
        if total_cur_prog == total_prog:
            self.panel.nd_game.setVisible(False)
            self.panel.img_pic.setVisible(True)
            for task_id in self._children_tasks:
                if global_data.player.has_unreceived_task_reward(task_id):
                    global_data.player.receive_task_reward(task_id)

        else:
            self.panel.nd_game.setVisible(True)
            self.panel.img_pic.setVisible(False)
            task_count = len(self._children_tasks)
            for i in range(task_count):
                nd = getattr(self.panel, 'temp_%d' % (i + 1))
                if nd:
                    self.init_share_temp(nd, self._children_tasks[i], i)
                else:
                    log_error('can not find nd for task index ', i)

            if total_cur_prog > 0:
                self.panel.temp_4.setLocalZOrder(1)
            else:
                self.panel.temp_4.setLocalZOrder(-1)

    def init_share_temp(self, ui_item, task_id, index):
        btn_puzzle = ui_item
        btn_puzzle.EnableCustomState(True)
        ui_item.EnableCustomState(True)
        total_cur_prog = global_data.player.get_task_prog(self._task_id)
        total_prog = task_utils.get_total_prog(self._task_id)
        single_cur_prog = global_data.player.get_task_prog(task_id)
        single_prog = task_utils.get_total_prog(task_id)
        has_share_task = ActivitySeasonShare.check_can_share_task(task_id)
        is_open = index == total_cur_prog and has_share_task
        is_task_done = single_cur_prog >= single_prog
        status = global_data.player.get_task_reward_status(task_id)
        if global_data.player.has_unreceived_task_reward(task_id):
            global_data.player.receive_task_reward(task_id)
        if is_task_done:
            ui_item.bar_prog and ui_item.bar_prog.setVisible(True)
            ui_item.lab_prog and ui_item.lab_prog.SetString('%s/%s' % (index + 1, total_prog))
            ui_item.bar_tips and ui_item.bar_tips.setVisible(False)
            btn_puzzle.SetSelect(True)
        elif not is_open:
            ui_item.bar_prog and ui_item.bar_prog.setVisible(False)
            ui_item.bar_tips and ui_item.bar_tips.setVisible(False)
        elif is_open:
            ui_item.bar_prog and ui_item.bar_prog.setVisible(False)
            ui_item.bar_tips and ui_item.bar_tips.setVisible(True)
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            reward_count = len(reward_list)
            ret = ''
            for idx in range(reward_count):
                item_no, item_num = reward_list[idx]
                pic = get_lobby_item_pic_by_item_no(item_no)
                ret += '#SW<img="%s", scale=0>#nX%d' % (pic, item_num)

            ui_item.lab_rich.SetString(get_text_by_id(611638).format(ret))

            @btn_puzzle.callback()
            def OnClick(btn, touch):
                if global_data.player.has_unreceived_task_reward(task_id):
                    global_data.player.receive_task_reward(task_id)
                else:
                    self.on_share()

        else:
            log_error('wrong status')

    def on_share(self):
        from logic.comsys.share.ShareUI import ShareUI
        share_ui = ShareUI(parent=self.panel)

        def init_cb():
            share_ui = global_data.ui_mgr.get_ui('ShareUI')
            if share_ui and share_ui.is_valid():
                share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                def share_inform_func():
                    if global_data.player:
                        global_data.player.share_activity('activity_%s' % self._activity_type)
                        global_data.player.share()

                share_ui.set_share_inform_func(share_inform_func)
                if global_data.is_pc_mode:
                    global_data.player.share_activity('activity_%s' % self._activity_type)
                    global_data.player.share()

        if not getattr(self, '_share_content', None):
            self._share_content = SeasonWarmupShareCreator()
            task_count = task_utils.get_total_prog(self._task_id)
            total_cur_prog = global_data.player.get_task_prog(self._task_id)
            index = min(total_cur_prog, task_count - 1)
            has_share_task = ActivitySeasonShare.check_can_share_task(self._children_tasks[index])
            if has_share_task:
                show_indexes = [ i for i in range(task_count) if i <= total_cur_prog ]
            else:
                show_indexes = [ i for i in range(task_count) if i < total_cur_prog ]
            txt_cd = self.panel.lab_time.getString()
            self._share_content.create(parent=None, task_count=task_count, show_indexes=show_indexes, activity_type=self._activity_type, txt_cd=txt_cd, init_cb=init_cb)
        else:
            self._share_content.refresh_cd_txt(self.panel.lab_time.getString())
            init_cb()
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def refresh_share(self, *args):
        if global_data.player.has_unreceived_task_reward(self._task_id):
            global_data.player.receive_all_task_reward(self._task_id)
        self._refresh_share_btn(global_data.player.has_unreceived_task_reward(self._task_id))

    def _refresh_share_btn(self, has_shared):
        self.panel.temp_btn_share.setVisible(not has_shared)

    @staticmethod
    def check_can_share_task--- This code section failed: ---

 251       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'logic.gcommon.time_utility'
           9  LOAD_ATTR             1  'gcommon'
          12  LOAD_ATTR             2  'time_utility'
          15  STORE_FAST            1  'tutil'

 252      18  LOAD_GLOBAL           3  'global_data'
          21  LOAD_ATTR             4  'player'
          24  LOAD_ATTR             5  'get_task_content'
          27  LOAD_ATTR             2  'time_utility'
          30  LOAD_CONST            1  ''
          33  CALL_FUNCTION_3       3 
          36  STORE_FAST            2  'last_share_day'

 253      39  LOAD_FAST             1  'tutil'
          42  LOAD_ATTR             6  'get_rela_day_no'
          45  LOAD_CONST            3  'rt'
          48  LOAD_FAST             1  'tutil'
          51  LOAD_ATTR             7  'CYCLE_DATA_REFRESH_TYPE_2'
          54  CALL_FUNCTION_256   256 
          57  STORE_FAST            3  'now_day'

 254      60  LOAD_FAST             2  'last_share_day'
          63  LOAD_FAST             3  'now_day'
          66  COMPARE_OP            5  '>='
          69  POP_JUMP_IF_FALSE    76  'to 76'

 255      72  LOAD_GLOBAL           8  'False'
          75  RETURN_END_IF    
        76_0  COME_FROM                '69'

 256      76  LOAD_GLOBAL           9  'True'
          79  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 33

    @staticmethod
    def check_if_left_reward(task_id):
        children_task_list = task_utils.get_children_task(task_id)
        for task_id in children_task_list:
            reward_status = global_data.player.get_task_reward_status(task_id)
            if reward_status != ITEM_RECEIVED:
                return True

        return False

    @staticmethod
    def show_tab_rp(task_id):
        children_task_list = task_utils.get_children_task(task_id)
        task_count = task_utils.get_total_prog(task_id)
        total_cur_prog = global_data.player.get_task_prog(task_id)
        index = min(total_cur_prog, task_count - 1)
        cur_child_task = children_task_list[index]
        task_utils.get_children_task(task_id)
        if ActivitySeasonShare.check_can_share_task(cur_child_task) and ActivitySeasonShare.check_if_left_reward(task_id):
            return True
        False