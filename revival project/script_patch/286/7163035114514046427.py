# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySeasonChoose.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gutils.activity_utils import get_left_time
from logic.gutils.template_utils import show_left_time, init_common_reward_list
from logic.gcommon.common_const import activity_const
from logic.gcommon.const import SEASON_RUSHING_STAR, SEASON_RUSHING_KILL
from logic.gcommon.common_const import rank_const, rank_activity_const
from common.uisys.basepanel import BasePanel
from logic.gutils import task_utils
from common.const import uiconst

class ShowAllAwardPanel(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202207/bp_sprint/open_bp_sprint_preview'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_click_close_btn(self, btn, touch):
        self.close()

    def refresh_task_info(self, parent_task_id):
        children_tasks = task_utils.get_children_task(parent_task_id)
        list_nd = self.panel.list_item
        list_nd.SetInitCount(len(children_tasks))
        for index, temp_item_widget in enumerate(list_nd.GetAllItem()):
            temp_item_widget.lab_number.SetString(str(index + 1))
            task_id = children_tasks[index]
            task_conf = task_utils.get_task_conf_by_id(task_id)
            reward_id = task_conf.get('reward')
            prog = task_conf.get('total_prog')
            temp_item_widget.lab_conditions.SetString(get_text_by_id(611463).format(num=prog))
            init_common_reward_list(temp_item_widget.list_reward, reward_id)

    def refresh_rank_info(self, rank_type):
        list_nd = self.panel.list_item
        data = rank_activity_const.get_rank_reward_list(rank_type)
        reward_info = []
        last_rank = 0
        for idx, info in enumerate(data):
            rank, reward_id = info
            text = get_text_by_id(81182).format(last_rank + 1, rank)
            last_rank = rank
            reward_info.append([text, reward_id])

        list_nd.SetInitCount(len(reward_info))
        for index, temp_item_widget in enumerate(list_nd.GetAllItem()):
            temp_item_widget.lab_number.SetString(str(index + 1))
            text, reward_id = reward_info[index]
            temp_item_widget.lab_conditions.SetString(text)
            init_common_reward_list(temp_item_widget.list_reward, reward_id)


class ActivitySeasonChoose(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySeasonChoose, self).__init__(dlg, activity_type)
        self.init_parameters()

    def on_init_panel(self):
        super(ActivitySeasonChoose, self).on_init_panel()
        self.register_timer()
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        emoticon_ids = conf.get('emoticon_ids', [])
        star_rank_task_id = conf.get('star_rank_task_id')
        kill_rank_type = conf.get('kill_rank_type')
        self.merge_activity = conf.get('merge_activity')
        for i in range(len(emoticon_ids)):
            btn = getattr(self.panel, 'nd_item_%d' % (i + 1))

            @btn.unique_callback()
            def OnClick(btn, touch, i=i):
                item_id = emoticon_ids[i]
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info)
                return

        if star_rank_task_id:

            @self.panel.bar_star.btn_preview.unique_callback()
            def OnClick(btn, touch, star_rank_task_id=star_rank_task_id):
                from logic.comsys.activity.ActivitySeasonChoose import ShowAllAwardPanel
                ui = ShowAllAwardPanel()
                ui.refresh_task_info(star_rank_task_id)

        if kill_rank_type:

            @self.panel.bar_kill.btn_preview.unique_callback()
            def OnClick(btn, touch, kill_rank_type=kill_rank_type):
                from logic.comsys.activity.ActivitySeasonChoose import ShowAllAwardPanel
                ui = ShowAllAwardPanel()
                ui.refresh_rank_info(kill_rank_type)

    def init_parameters(self):
        self.last_tab_name_id = None
        self.sub_widget = None
        self._timer = 0
        return

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget
        if not self.sub_widget:
            return

        @self.panel.bar_star.temp_btn_click.btn_major.unique_callback()
        def OnClick(btn, touch):

            def _cb():
                if self.sub_widget and global_data.player:
                    if self.merge_activity:
                        global_data.player.choose_season_rushing_rank_type(SEASON_RUSHING_STAR)
                        self.sub_widget.select_tab(self.merge_activity['star'])

            LotterySmallSecondConfirmWidget(title_text_id=611470, content_text_id=611472, confirm_callback=_cb)

        @self.panel.bar_kill.temp_btn_click.btn_major.unique_callback()
        def OnClick(btn, touch):

            def _cb():
                if self.sub_widget and global_data.player:
                    if self.merge_activity:
                        global_data.player.choose_season_rushing_rank_type(SEASON_RUSHING_KILL)
                        self.sub_widget.select_tab(self.merge_activity['kill_normal'])

            LotterySmallSecondConfirmWidget(title_text_id=611470, content_text_id=611471, confirm_callback=_cb)

        self.sub_widget.set_show(self.get_sub_show())

    def get_sub_show(self):
        return False

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def refresh_left_time(self):
        left_time_delta = get_left_time(self._activity_type)
        show_left_time(self.panel.lab_time_tips, left_time_delta, '')

    def on_finalize_panel(self):
        self.unregister_timer()
        super(ActivitySeasonChoose, self).on_finalize_panel()
        self.sub_widget = None
        return