# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVECareerProgressUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from common.uisys.basepanel import BasePanel
from logic.gutils import career_utils, task_utils
from logic.gutils.career_utils import has_got_badge, get_badge_icon_path, get_badge_bg_path
from logic.gutils.pve_lobby_utils import get_pve_career_task_state, get_pve_career_degree, get_pve_career_format_text
from logic.comsys.effect import ui_effect
from common.utilities import get_rome_num
from logic.gcommon import time_utility
from common.cfg import confmgr

class PVECareerProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/ac/open_ac_pve_describe'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE

    def __init__(self, task_id, task_level):
        super(PVECareerProgressUI, self).__init__()
        self.init_params(task_id, task_level)
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self, task_id, task_level):
        self._task_id = task_id
        self._task_level = task_level
        self._prog_reward_list = task_utils.get_prog_rewards(self._task_id)
        if self._prog_reward_list:
            self._prog = self._prog_reward_list[self._task_level - 1][0]

    def init_ui(self):
        self._refresh_badge()

    def init_ui_event(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            status = get_pve_career_task_state(self._task_id, self._task_level)
            if status == ITEM_UNRECEIVED:
                if self._prog_reward_list:
                    global_data.player.receive_task_prog_reward(self._task_id, self._prog)
                else:
                    global_data.player.receive_task_reward(self._task_id)

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.close()

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.close()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._update_btn_state,
           'receive_task_prog_reward_succ_event': self._update_btn_state
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _refresh_badge(self):
        task_conf = task_utils.get_task_conf_by_id(self._task_id)
        status = get_pve_career_task_state(self._task_id, self._task_level)
        has_receive = status == ITEM_RECEIVED
        if task_conf.get('is_mecha_icon'):
            self.panel.icon.setVisible(False)
            icon = self.panel.item
            icon.setVisible(True)
        else:
            self.panel.item.setVisible(False)
            icon = self.panel.icon
            icon.setVisible(True)
        icon_path = get_badge_icon_path(self._task_id)
        icon.SetDisplayFrameByPath('', icon_path)
        ui_effect.set_dark(icon, not has_receive)
        frame = self.panel.frame
        task_degree = get_pve_career_degree(self._task_id, self._task_level)
        bg_path = get_badge_bg_path(self._task_id, task_degree - 1)
        frame.SetDisplayFrameByPath('', bg_path)
        ui_effect.set_dark(frame, not has_receive)
        self.panel.lab_name.SetString(get_text_by_id(task_conf.get('badge_name_id')).format(get_rome_num(task_degree)))
        if self._prog_reward_list:
            self.panel.lab_describe.setString(career_utils.get_badge_desc_text_by_lv(self._task_id, self._task_level))
        else:
            self.panel.lab_describe.setString(get_pve_career_format_text(self._task_id, self._task_level))
        if self._prog_reward_list:
            ts = global_data.player.get_task_prog_rec_time(self._task_id, self._prog)
        else:
            ts = global_data.player.get_task_reward_rec_time(self._task_id)
        time_text = time_utility.get_server_time_str_from_ts(ts, format='%Y.%m.%d %H:%M')
        lab_time = self.panel.lab_time
        lab_time.SetString(time_text)
        lab_time.setVisible(has_receive)

        @self.panel.btn_box.unique_callback()
        def OnClick(btn, touch):
            if self._prog_reward_list:
                reward_id = self._prog_reward_list[self._task_level - 1][1]
            else:
                reward_id = task_utils.get_task_reward(self._task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_id = reward_list[0][0]
            item_num = reward_list[0][1]
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            wpos = btn.ConvertToWorldSpace(x, y)
            global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, item_num=item_num)
            return

        self._update_btn_state()

    def _update_btn_state(self, *args):
        btn_get = self.panel.btn_get
        nd_progress = self.panel.nd_progress
        if global_data.player:
            status = get_pve_career_task_state(self._task_id, self._task_level)
            if status == ITEM_RECEIVED:
                btn_get.setVisible(True)
                btn_get.SetShowEnable(False)
                nd_progress.setVisible(False)
            elif status == ITEM_UNRECEIVED:
                btn_get.setVisible(True)
                btn_get.SetShowEnable(True)
                nd_progress.setVisible(False)
            else:
                btn_get.setVisible(False)
                nd_progress.setVisible(True)
                max_prog = career_utils.get_badge_max_prog_by_lv(self._task_id, self._task_level)
                cur_prog = career_utils.get_badge_ongoing_max_cur_prog(self._task_id)
                cur_prog = min(cur_prog, max_prog)
                self.panel.lab_progress.SetString('%d/%d' % (cur_prog, max_prog))
        else:
            btn_get.setVisible(False)
            nd_progress.setVisible(False)

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVECareerProgressUI, self).on_finalize_panel()