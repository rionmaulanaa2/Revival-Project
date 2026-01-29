# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202312/DailyChristmasTaskUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
from common.const import uiconst
from logic.comsys.activity.widget import widget

@widget('AsyncChristmasBtnTaskListWidget')
class DailyChristmasTaskUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202312/christmas_turntable/open_christmas_turntable'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    ACTIVITY_TYPE = activity_const.ACTIVITY_CHRISTMAS_TURNABLE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }
    GLOBAL_EVENT = {'task_prog_changed': 'refresh_task',
       'receive_task_reward_succ_event': 'refresh_task',
       'receive_task_prog_reward_succ_event': 'refresh_task'
       }

    def init_parameters(self):
        super(DailyChristmasTaskUI, self).init_parameters()

    def on_init_panel(self):
        self._activity_type = self.ACTIVITY_TYPE
        self._selected_tab_index = 0
        from common.cfg import confmgr
        from logic.gutils import task_utils
        conf = confmgr.get('c_activity_config', self._activity_type)
        _fixed_task_id = conf.get('cTask', '')
        challenge_tasks = conf.get('cUiData', {}).get('challenge_tasks', [])
        challenge_tasks = [ str(t) for t in challenge_tasks ]
        children_tasks = task_utils.get_children_task(_fixed_task_id)
        first_tab_tasks = [ t for t in children_tasks if t not in challenge_tasks ]
        self.tab_data = [{'text': get_text_by_id(634945),'tasks': first_tab_tasks}, {'text': get_text_by_id(709308),'tasks': challenge_tasks}]
        self.init_tab_list()
        super(DailyChristmasTaskUI, self).on_init_panel()

    def post_init_widget(self):
        first_tab = self.panel.list_tab.GetItem(0)
        if first_tab:
            first_tab.btn_tab.OnClick(None)
        return

    def on_finalize_panel(self):
        pass

    def refresh_panel(self):
        pass

    def on_click_btn_close(self, *args):
        self.close()

    def init_tab_list(self):
        tab_data = self.tab_data
        self.panel.list_tab.SetInitCount(len(tab_data))
        self.refresh_rp()
        for idx in range(len(tab_data)):
            item_widget = self.panel.list_tab.GetItem(idx)
            item_widget.btn_tab.SetText(tab_data[idx]['text'])

            @item_widget.btn_tab.unique_callback()
            def OnClick(btn, touch, sel_idx=idx):
                print ('OnClick', sel_idx)
                for _item in self.panel.list_tab.GetAllItem():
                    _item.btn_tab.SetSelect(False)

                if sel_idx == 0:
                    self.panel.lab_tips_task.setVisible(True)
                else:
                    self.panel.lab_tips_task.setVisible(False)
                self.panel.list_tab.GetItem(sel_idx).btn_tab.SetSelect(True)
                self._selected_tab_index = sel_idx
                tasks = self.tab_data[sel_idx]['tasks']
                self._widgets['AsyncChristmasBtnTaskListWidget'].set_task_id(None, None, tasks)
                return

    def refresh_rp(self, *args, **kargs):
        tab_data = self.tab_data
        for idx in range(len(tab_data)):
            item_widget = self.panel.list_tab.GetItem(idx)
            tasks = tab_data[idx]['tasks']
            item_widget.temp_red.setVisible(False)
            for task_id in tasks:
                if global_data.player.has_unreceived_task_reward(task_id):
                    item_widget.temp_red.setVisible(True)
                    break

    def refresh_task(self, *args, **kargs):
        self.refresh_rp()