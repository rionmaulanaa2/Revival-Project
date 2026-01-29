# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonRoleShare.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.client_utils import post_ui_method
from logic.gutils import item_utils
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class RoleShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_ROLE_WARMUP'

    def __init__(self, activity_ui, init_cb):
        super(RoleShareCreator, self).__init__()
        self.activity_ui = activity_ui
        self.init_cb = init_cb

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        if not self.activity_ui:
            return
        super(RoleShareCreator, self).create(parent, tmpl)
        panel = self.panel.temp_activity
        activity_ui = self.activity_ui
        puzzle_prog = activity_ui.ui_data['puzzle_prog']
        voice_prog = activity_ui.ui_data['voice_prog']
        children_tasks = activity_ui._children_tasks
        panel.lab_content.setVisible(True)
        panel.lab_content.SetString(activity_ui.get_voice_text_id())
        panel.temp_btn_share.setVisible(False)
        panel.bar_tips.setVisible(False)
        total_cur_prog = global_data.player.get_task_prog(activity_ui._task_id)
        task_prog = min(len(children_tasks) - 1, total_cur_prog)
        task_id = children_tasks[task_prog]
        has_share_task = ActivityCommonRoleShare.check_can_share_task(task_id)
        share_prog = task_prog if not has_share_task and total_cur_prog < len(children_tasks) else task_prog + 1
        is_voice_valid = share_prog >= voice_prog
        panel.btn_play.SetEnable(is_voice_valid)
        panel.btn_play.SetEnableTouch(False)
        panel.nd_touch.SetEnableTouch(False)
        panel.btn_left.SetEnable(False)
        panel.btn_right.SetEnable(False)
        panel.btn_left.setVisible(False)
        panel.btn_right.setVisible(False)
        panel.lab_reward_tips.SetString(634264 if is_voice_valid else 634255)
        if is_voice_valid:
            panel.img_pic.SetDisplayFrameByPath('', activity_ui.ui_data['final_img'], force_sync=True)
        is_show_pic = share_prog >= puzzle_prog
        panel.nd_game.setVisible(not is_show_pic)
        panel.img_pic.setVisible(is_show_pic)
        if not is_show_pic:
            for i in range(share_prog):
                nd = getattr(panel, 'temp_%d' % (i + 1))
                if nd:
                    nd.SetSelect(True)

            panel.temp_4.setLocalZOrder(1)
        reward_task_id = children_tasks[share_prog - 1]
        reward_id = task_utils.get_task_reward(reward_task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        for idx, (item_no, item_num) in enumerate(reward_list):
            nd = getattr(panel, 'temp_item%d' % (idx + 1))
            self.init_reward_tmp(nd, item_no, item_num)

        show_time_tips = activity_ui.ui_data.get('show_time_tips')
        if show_time_tips:
            panel.lab_tips_time.SetString(show_time_tips)
        self.init_cb()

    def init_reward_tmp(self, ui_item, item_no, item_num):
        ui_item.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no), force_sync=True)
        item_name = item_utils.get_lobby_item_name(item_no)
        ui_item.lab_name.SetString(item_name)
        ui_item.lab_quantity.SetString(str(item_num))

    def destroy(self):
        super(RoleShareCreator, self).destroy()
        self.init_cb = None
        self.activity_ui = None
        return


class ActivityCommonRoleShare(ActivityTemplate):
    VOICE_PLAY = 1
    VOICE_STOP = 2
    VOICE_END = 3

    def on_init_panel(self):
        super(ActivityCommonRoleShare, self).on_init_panel()
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        activity_conf = confmgr.get('c_activity_config', self._activity_type)
        children_tasks = task_utils.get_children_task(self._task_id)
        self._children_tasks = children_tasks
        self.ui_data = activity_conf.get('cUiData', {})
        self._share_content = None
        self._voice_status = ActivityCommonRoleShare.VOICE_END
        self._voice_idx = 0
        self._voice_cb = None
        self.refresh_list()

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cRuleTextID']))

        @self.panel.temp_btn_share.btn_common_big.callback()
        def OnClick(btn, touch):
            self.on_share()

        @self.panel.btn_play.callback()
        def OnClick(btn, touch):
            self.play_voice()

        @self.panel.nd_touch.unique_callback()
        def OnClick(btn, touch):
            self.play_voice()

        @self.panel.btn_left.callback()
        def OnClick(btn, touch):
            if self._voice_status == ActivityCommonRoleShare.VOICE_END:
                self.change_voice(False)
            else:
                self.stop_voice(lambda : self.change_voice(False))

        @self.panel.btn_right.callback()
        def OnClick(btn, touch):
            if self._voice_status == ActivityCommonRoleShare.VOICE_END:
                self.change_voice()
            else:
                self.stop_voice(lambda : self.change_voice())

        return

    def get_voice_text_id(self):
        trigger_type = self.ui_data['voice_type'][self._voice_idx]
        voice_cnf = confmgr.get('game_voice_conf', 'HumanVoice', 'Content', trigger_type)
        if not voice_cnf:
            return ''
        else:
            switch_list = voice_cnf.get('event', None)
            if not switch_list:
                return ''
            switch = switch_list[0]
            voice_cnf = confmgr.get('game_voice_conf', 'VoiceText', 'Content', default={})
            return voice_cnf.get(switch, {}).get('text_id', '')

    def change_voice(self, next=True):
        len_voice = len(self.ui_data['voice_type'])
        if next:
            self._voice_idx = (self._voice_idx + 1) % len_voice
            ani_name = 'lab_right'
        else:
            self._voice_idx = (self._voice_idx - 1 + len_voice) % len_voice
            ani_name = 'lab_left'
        self.panel.lab_content.setVisible(False)
        self.panel.lab_content.SetString(self.get_voice_text_id())
        self.panel.PlayAnimation(ani_name)

    def end_voice(self):
        if self.panel and not self.panel.IsDestroyed():
            self._voice_status = ActivityCommonRoleShare.VOICE_END
            self.panel.StopAnimation('loop_yinbo')
            self.panel.yinbo.setVisible(False)
            self.reset_music()
            if self._voice_cb:
                voice_cb = self._voice_cb
                self._voice_cb = None
                voice_cb()
        return

    def stop_voice(self, end_cb=None):
        if self._voice_status == ActivityCommonRoleShare.VOICE_PLAY:
            self._voice_cb = end_cb
            self._voice_status = ActivityCommonRoleShare.VOICE_STOP
            global_data.game_voice_mgr.stop_voice_by_uid()
            self.panel.StopAnimation('loop_yinbo')
            self.panel.yinbo.setVisible(False)
        elif self._voice_status == ActivityCommonRoleShare.VOICE_STOP:
            self._voice_cb = end_cb

    def play_voice(self):
        if self._voice_status == ActivityCommonRoleShare.VOICE_END:
            if global_data.game_voice_mgr.play_voice_by_uid('HumanVoice', self.ui_data['voice_type'][self._voice_idx], lambda : self.end_voice()):
                self.down_music()
                self.panel.yinbo.setVisible(True)
                self.panel.PlayAnimation('loop_yinbo')
                self._voice_status = ActivityCommonRoleShare.VOICE_PLAY
        else:
            self.stop_voice(lambda : self.play_voice())

    def down_music(self):
        global_data.sound_mgr.set_music_volume(0)

    def reset_music(self):
        global_data.sound_mgr.set_music_volume(global_data.sound_mgr.get_music_volume())

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

    def on_finalize_panel(self):
        super(ActivityCommonRoleShare, self).on_finalize_panel()
        self._voice_cb = None
        self.reset_music()
        self.stop_voice()
        self.activity_conf = {}
        if self._share_content:
            self._share_content.destroy()
            self._share_content = None
        return

    def refresh_list(self):
        total_cur_prog = global_data.player.get_task_prog(self._task_id)
        self.panel.lab_content.SetString(self.get_voice_text_id())
        if global_data.player.is_task_finished(self._task_id):
            self.panel.lab_title_tips.SetString(634252)
        else:
            self.panel.lab_title_tips.SetString(634252)
        is_voice_valid = total_cur_prog >= self.ui_data['voice_prog']
        self.panel.btn_play.SetEnable(is_voice_valid)
        self.panel.btn_left.SetEnable(is_voice_valid)
        self.panel.btn_right.SetEnable(is_voice_valid)
        self.panel.nd_touch.SetEnableTouch(is_voice_valid)
        self.panel.btn_left.setVisible(is_voice_valid)
        self.panel.btn_right.setVisible(is_voice_valid)
        puzzle_prog = self.ui_data['puzzle_prog']
        is_show_pic = total_cur_prog >= puzzle_prog
        self.panel.nd_game.setVisible(not is_show_pic)
        self.panel.img_pic.setVisible(is_show_pic)
        if not is_show_pic:
            for i in range(puzzle_prog):
                nd = getattr(self.panel, 'temp_%d' % (i + 1))
                if nd:
                    self.init_share_temp(nd, self._children_tasks[i], i, total_cur_prog)
                else:
                    log_error('can not find nd for task index ', i)

            if total_cur_prog > 0:
                self.panel.temp_4.setLocalZOrder(1)
            else:
                self.panel.temp_4.setLocalZOrder(-1)
        reward_prog = min(len(self._children_tasks) - 1, total_cur_prog)
        task_id = self._children_tasks[reward_prog]
        if ActivityCommonRoleShare.check_can_share_task(task_id) and len(self._children_tasks) > total_cur_prog:
            reward_task_id = task_id
            is_task_done = False
        else:
            reward_task_id = self._children_tasks[reward_prog - 1 if len(self._children_tasks) > total_cur_prog else reward_prog]
            is_task_done = True
        reward_id = task_utils.get_task_reward(reward_task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        for idx, (item_no, item_num) in enumerate(reward_list):
            nd = getattr(self.panel, 'temp_item%d' % (idx + 1))
            self.init_reward_tmp(nd, item_no, item_num, is_task_done)

        if total_cur_prog > puzzle_prog or total_cur_prog == puzzle_prog and not is_task_done:
            self.panel.bar_tips.setVisible(True)
        else:
            self.panel.bar_tips.setVisible(False)
        if is_voice_valid:
            self.panel.img_pic.SetDisplayFrameByPath('', self.ui_data['final_img'])
            self.panel.lab_rich.SetString(634256)
            self.panel.lab_reward_tips.SetString(634264)
        else:
            self.panel.lab_rich.SetString(634257)
            self.panel.lab_reward_tips.SetString(634255)
        show_time_tips = self.ui_data.get('show_time_tips')
        if show_time_tips:
            self.panel.lab_tips_time.SetString(show_time_tips)
        btn_share = self.panel.temp_btn_share.btn_common_big
        if is_task_done:
            btn_share.SetText(635641)
        else:
            btn_share.SetText(80149)

    def init_reward_tmp(self, ui_item, item_no, item_num, is_get):

        @ui_item.frame.unique_callback()
        def OnClick(btn, touch):
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
            return True

        if is_get:
            paths = list(ui_item.frame.GetFramePaths())
            paths[0] = paths[1] = paths[2]
            ui_item.frame.SetFrames('', paths)
        ui_item.item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
        item_name = item_utils.get_lobby_item_name(item_no)
        ui_item.lab_name.SetString(item_name)
        ui_item.lab_quantity.SetString(str(item_num))
        ui_item.nd_get.setVisible(is_get)

    def init_share_temp(self, ui_item, task_id, index, total_cur_prog):
        ui_item.EnableCustomState(True)
        single_cur_prog = global_data.player.get_task_prog(task_id)
        single_prog = task_utils.get_total_prog(task_id)
        is_task_done = single_cur_prog >= single_prog
        ui_item.SetSelect(is_task_done)

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

        if not getattr(self, '_share_content', None):
            self._share_content = RoleShareCreator(self, init_cb)
            self._share_content.create()
        else:
            self._share_content.recreate_panel()
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    @staticmethod
    def check_can_share_task--- This code section failed: ---

 383       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'logic.gcommon.time_utility'
           9  LOAD_ATTR             1  'gcommon'
          12  LOAD_ATTR             2  'time_utility'
          15  STORE_FAST            1  'tutil'

 384      18  LOAD_GLOBAL           3  'global_data'
          21  LOAD_ATTR             4  'player'
          24  LOAD_ATTR             5  'get_task_content'
          27  LOAD_ATTR             2  'time_utility'
          30  LOAD_CONST            1  ''
          33  CALL_FUNCTION_3       3 
          36  STORE_FAST            2  'last_share_day'

 385      39  LOAD_FAST             1  'tutil'
          42  LOAD_ATTR             6  'get_rela_day_no'
          45  LOAD_CONST            3  'rt'
          48  LOAD_FAST             1  'tutil'
          51  LOAD_ATTR             7  'CYCLE_DATA_REFRESH_TYPE_2'
          54  CALL_FUNCTION_256   256 
          57  STORE_FAST            3  'now_day'

 386      60  LOAD_FAST             2  'last_share_day'
          63  LOAD_FAST             3  'now_day'
          66  COMPARE_OP            5  '>='
          69  POP_JUMP_IF_FALSE    76  'to 76'

 387      72  LOAD_GLOBAL           8  'False'
          75  RETURN_END_IF    
        76_0  COME_FROM                '69'

 388      76  LOAD_GLOBAL           9  'True'
          79  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 33

    @staticmethod
    def show_tab_rp(task_id):
        if global_data.player.is_task_finished(task_id):
            return False
        else:
            children_task_list = task_utils.get_children_task(task_id)
            task_count = task_utils.get_total_prog(task_id)
            total_cur_prog = global_data.player.get_task_prog(task_id)
            index = min(total_cur_prog, task_count - 1)
            cur_child_task = children_task_list[index]
            return ActivityCommonRoleShare.check_can_share_task(cur_child_task)