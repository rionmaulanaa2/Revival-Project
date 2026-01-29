# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySignPicPuzzle.py
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gutils.client_utils import post_ui_method
from logic.gutils import item_utils
from six.moves import range

class ActivitySignPicPuzzle(ActivityTemplate):

    def on_init_panel(self):
        super(ActivitySignPicPuzzle, self).on_init_panel()
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        children_tasks = task_utils.get_children_task(self._task_id)
        self._children_tasks = children_tasks
        self.ui_data = activity_conf.get('cUiData', {})
        self.widget_map = {}
        self.panel.lab_title_tips.SetString(get_text_by_id(610978))
        self.init_countdown_widget()
        self.refresh_list()
        self.refresh_task_receive_status()
        global_data.emgr.refresh_activity_redpoint.emit()

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        @self.panel.temp_btn_sign.btn_common_big.callback()
        def OnClick(btn, touch):
            self.on_receive_reward()

        self.refresh_list()
        self.refresh_sign()

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
        self.refresh_sign()

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        ex_data = {'txt_id': 906607}
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type, ex_data)

    def on_finalize_panel(self):
        super(ActivitySignPicPuzzle, self).on_finalize_panel()
        for widget in self.widget_map.values():
            widget.on_finalize_panel()

        self.widget_map = None
        self.activity_conf = {}
        return

    def refresh_list(self):
        self.refresh_task_receive_status()
        self.refresh_task_items()
        if len(self.reward_received_task_ids) == 5:
            self.panel.nd_game.setVisible(False)
            self.panel.img_pic.setVisible(True)
            self.panel.img_pic.bar_tips.setVisible(False)
            self.panel.img_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202307/pinganjing_share/img_pinganjing_share_share_all.png')
        elif len(self.reward_received_task_ids) == 4:
            self.panel.nd_game.setVisible(False)
            self.panel.img_pic.setVisible(True)
            total_cur_prog = global_data.player.get_task_prog(self._task_id)
            self.panel.img_pic.bar_tips.setVisible(True if total_cur_prog > 4 else False)
            self.panel.img_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202307/pinganjing_share/img_driver_share_share_all_0.png')
        else:
            self.panel.nd_game.setVisible(True)
            self.panel.img_pic.setVisible(False)
            for i in range(4):
                nd = getattr(self.panel, 'temp_%d' % (i + 1))
                if nd:
                    self.init_share_temp(nd, self._children_tasks[i], i)
                else:
                    log_error('can not find nd for task index ', i)

    def init_share_temp(self, ui_item, task_id, index):
        btn_puzzle = ui_item
        btn_puzzle.EnableCustomState(True)
        ui_item.EnableCustomState(True)
        total_prog = 4
        is_open = task_id in self.reward_unreceived_task_ids
        is_task_done = task_id in self.reward_received_task_ids
        if is_task_done:
            ui_item.bar_prog.setVisible(True)
            ui_item.lab_prog.SetString('%s/%s' % (index + 1, total_prog))
            ui_item.bar_tips.setVisible(False)
            btn_puzzle.SetSelect(True)
        elif not is_open:
            ui_item.bar_prog.setVisible(False)
            ui_item.bar_tips.setVisible(False)
            btn_puzzle.SetSelect(False)
        elif is_open:
            ui_item.bar_prog.setVisible(False)
            ui_item.bar_tips.setVisible(True)
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            reward_count = len(reward_list)
            ret = ''
            for idx in range(reward_count):
                item_no, item_num = reward_list[idx]
                pic = get_lobby_item_pic_by_item_no(item_no)
                ret += '#SW<img="%s", scale=0>#nX%d' % (pic, item_num)

            ui_item.lab_rich.SetString(get_text_by_id(634739))

            @btn_puzzle.callback()
            def OnClick(btn, touch):
                self.on_receive_reward()

        else:
            log_error('wrong status')

    def refresh_task_receive_status(self):
        self.reward_ungain_task_ids = self.get_task_ids_in_receive_status(ITEM_UNGAIN)
        self.reward_unreceived_task_ids = self.get_task_ids_in_receive_status(ITEM_UNRECEIVED)
        self.reward_received_task_ids = self.get_task_ids_in_receive_status(ITEM_RECEIVED)

    def get_task_ids_in_receive_status(self, status):
        ret = []
        children_task = task_utils.get_children_task(self._task_id)
        for task_id in children_task:
            if global_data.player.get_task_reward_status(task_id) == status:
                ret.append(task_id)

        return ret

    def on_receive_reward(self):
        children_task = task_utils.get_children_task(self._task_id)
        for task_id in children_task:
            reward_status = global_data.player.get_task_reward_status(task_id)
            if reward_status == ITEM_UNRECEIVED:
                global_data.player.receive_task_reward(task_id)

        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_sign(self, *args):
        self._refresh_receive_btn(global_data.player.has_unreceived_task_reward(self._task_id))

    def _refresh_receive_btn(self, has_reward_unreceived):
        self.panel.temp_btn_sign.btn_common_big.SetEnable(has_reward_unreceived)
        self.panel.temp_btn_sign.btn_common_big.SetText(604007 if has_reward_unreceived else 604010)

    def refresh_task_items(self):
        last_task_id = 0
        last_task_status = ITEM_UNRECEIVED
        last_task_day_idx = 0
        children_task = task_utils.get_children_task(self._task_id)
        for idx, task_id in enumerate(children_task):
            reward_status = global_data.player.get_task_reward_status(task_id)
            if reward_status == ITEM_UNRECEIVED or reward_status == ITEM_RECEIVED:
                last_task_id = task_id
                last_task_status = reward_status
                last_task_day_idx = idx + 1

        self.panel.lab_sign_tips.SetString(get_text_by_id(634737, [len(children_task), last_task_day_idx]))
        reward_received = True if last_task_status == ITEM_RECEIVED else False
        reward_id = task_utils.get_task_reward(last_task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        for idx, (item_no, item_num) in enumerate(reward_list):
            nd = getattr(self.panel, 'temp_item%d' % (idx + 1))
            if not nd:
                nd = self.panel.temp_item
            self.init_reward_temp(nd, item_no, item_num, reward_received)

    def init_reward_temp(self, ui_item, item_no, item_num, is_get):
        ui_item.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        item_name = item_utils.get_lobby_item_name(item_no)
        ui_item.lab_name.SetString(item_name)
        ui_item.lab_quantity.SetString(str(item_num))
        ui_item.nd_get.setVisible(is_get)

    @staticmethod
    def show_tab_rp(task_id):
        if global_data.player.has_unreceived_task_reward(task_id):
            return True
        return False