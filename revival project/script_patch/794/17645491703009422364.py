# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/christmas/ChristmasParty.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.gcommon.common_const.activity_const import ACTIVITY_CHRISTMAS_PARTY1
from logic.gutils import task_utils, item_utils, activity_utils, template_utils
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from common.const import uiconst

class ChristmasParty(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_201912/winter_collect'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    NEED_GAUSSIAN_BLUR = True
    UI_ACTION_EVENT = {'nd_close.OnClick': 'close',
       'btn_check.OnClick': 'on_click_rule'
       }

    def on_init_panel(self, *args):
        self._load_activity_info()
        self._lock_path = 'gui/ui_res_2/activity/activity_201912/img_winter_collect_0%d_lock.png'
        self._unlock_path = 'gui/ui_res_2/activity/activity_201912/img_winter_collect_0%d_unlock.png'
        self._item_to_nd = {}
        self._init_item_list()
        self._update_collect_progress()
        self._update_receive_state()
        self._bind_event(True)
        self.hide_main_ui()
        self.PlayAnimation('appear')

    def _load_activity_info(self):
        parent_task_id = confmgr.get('c_activity_config', ACTIVITY_CHRISTMAS_PARTY1, 'cTask', default=0)
        self._parent_task_info = task_utils.get_task_conf_by_id(parent_task_id)
        c1_tid, c2_tid, c3_tid = self._parent_task_info.get('children_task')
        self._c1_task_info = task_utils.get_task_conf_by_id(c1_tid)
        self._c2_task_info = task_utils.get_task_conf_by_id(c2_tid)
        self._c3_task_info = task_utils.get_task_conf_by_id(c3_tid)

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('GameRuleDescUI')
        self._bind_event(False)
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()

    def do_show_panel(self):
        super(ChristmasParty, self).do_show_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def do_hide_panel(self):
        super(ChristmasParty, self).do_hide_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def _bind_event(self, bind):
        e_conf = {'update_task_content_event': self.on_add_progress,
           'receive_task_reward_succ_event': self.on_receive_ret
           }
        global_data.emgr.bind_events(e_conf) if bind else global_data.emgr.unbind_events(e_conf)

    def _init_item_list(self):
        item_list = self._c1_task_info.get('extra_params', {}).get('collections', ())
        self.panel.list_role.SetInitCount(len(item_list))
        for i, item_id in enumerate(item_list):
            role_nd = self.panel.list_role.GetItem(i)
            role_nd.img_role.SetDisplayFrameByPath('', self._lock_path % (i + 1))
            role_nd.lab_name.SetString(item_utils.get_lobby_item_name(item_id))
            role_nd.temp_btn_get.setVisible(True)
            role_nd.nd_get.setVisible(False)

            @role_nd.temp_btn_get.btn_common.callback()
            def OnClick(b, t, item_id=item_id):
                item_utils.jump_to_ui(item_id)

        from logic.gcommon.time_utility import get_server_time
        now = get_server_time()
        left_time = int(max(self._parent_task_info.get('end_time', now) - now, 0))
        template_utils.show_left_time(self.panel.lab_details, left_time, get_text_by_id(607165) + '      ')
        self.panel.lab_describe.SetString(607166)
        reward_id = self._c3_task_info.get('reward', 0)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        _, item_no = reward_conf['reward_list'][0]
        self.panel.lab_num.SetString('x' + str(item_no))

    def _update_collect_progress(self):
        task_id = self._c1_task_info['task_id']
        target_collections = self._c1_task_info.get('extra_params', {}).get('collections', ())
        collected_item_list = global_data.player.get_task_content(task_id, 'collections') or ()
        for i, item_id in enumerate(target_collections):
            role_nd = self.panel.list_role.GetItem(i)
            if item_id in collected_item_list:
                role_nd.temp_btn_get.setVisible(False)
                role_nd.nd_get.setVisible(True)
                role_nd.img_role.SetDisplayFrameByPath('', self._unlock_path % (i + 1))

        collected_num = len(collected_item_list)
        collection_num = len(target_collections)
        self.panel.lab_collect.SetString(get_text_by_id(607164) + '  #BB%d#BC / %d' % (collected_num, collection_num))
        self.panel.progress_exp.SetPercent(collected_num * 100 / collection_num)

    def _update_receive_state(self):
        self._update_box_state(self.panel.nd_box_1, self._c2_task_info, 'get_tips1')
        self._update_box_state(self.panel.nd_box_2, self._c1_task_info, 'get_tips2')
        self._update_weekly_coin_status()

    def _update_box_state(self, box_nd, task_conf, animation):
        task_id = task_conf.get('task_id', 0)
        receive_state = global_data.player.get_task_reward_status(task_id)
        box_nd.nd_get.setVisible(False)
        box_nd.nd_vx.setVisible(False)
        self.StopAnimation(animation)
        if receive_state == ITEM_UNGAIN:
            box_nd.BindMethod('OnClick', lambda b, t, tid=task_id: self.OnClick_preview(tid))
        elif receive_state == ITEM_UNRECEIVED:
            box_nd.nd_vx.setVisible(True)
            self.PlayAnimation(animation)
            box_nd.BindMethod('OnClick', lambda b, t, tid=task_id: global_data.player.receive_task_reward(tid))
        elif receive_state == ITEM_RECEIVED:
            box_nd.nd_get.setVisible(True)
            box_nd.BindMethod('OnClick', lambda b, t, tid=task_id: self.OnClick_preview(tid))

    def OnClick_preview(self, task_id):
        if task_id == self._c1_task_info.get('task_id', 0):
            self.preview_alternative_reward()
        elif task_id == self._c2_task_info.get('task_id', 0):
            self.preview_fixed_reward()

    def preview_fixed_reward(self):
        reward_id = self._c2_task_info.get('reward', 0)
        btn = self.panel.nd_box_1
        x, y = btn.GetPosition()
        wpos = btn.GetParent().ConvertToWorldSpace(x, y)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)

    def preview_alternative_reward(self):
        reward_id = self._c1_task_info.get('reward', 0)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        item_id, _ = reward_conf['reward_list'][0]
        ui = global_data.ui_mgr.show_ui('MultiRewardPreview', 'logic.comsys.reward')
        ui and ui.set_item_id(item_id)

    def _update_weekly_coin_status(self):
        task_id = self._c3_task_info['task_id']
        btn = self.panel.temp_get
        btn.lab_btn.setVisible(False)
        has_received = global_data.player.has_receive_reward(task_id)
        btn.btn_common.SetEnable(not has_received)
        btn.temp_red.setVisible(not has_received)
        btn.btn_common.SetText(80866 if has_received else 80930)

        @btn.btn_common.callback()
        def OnClick(b, t, task_id=task_id):
            if global_data.player:
                global_data.player.receive_task_reward(task_id)
                btn.btn_common.SetEnable(False)

    def on_add_progress(self, task_id):
        self._update_collect_progress()

    def on_receive_ret(self, task_id):
        self._update_receive_state()

    def on_click_rule(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_local_content(607171), get_text_local_content(607173))