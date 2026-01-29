# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity14DSign.py
from __future__ import absolute_import
from six.moves import range
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import task_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from cocosui import cc, ccui, ccs

class Activity14DSign(ActivityBase):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.total_count = 0
        self._cur_last_day = -1
        self._change_pos = 0
        self.process_event(True)
        self.init_widget(do_update=False)
        self.panel.PlayAnimation('show')

        def callback4():
            self.panel.PlayAnimation('loop3')

        def callback3():
            self.panel.PlayAnimation('loop1')
            self.panel.SetTimeOut(0.033, callback4)

        def callback2():
            self.panel.PlayAnimation('loop')
            self.panel.SetTimeOut(0.067, callback3)

        def callback1():
            self.panel.PlayAnimation('loop2')
            self.panel.SetTimeOut(0.333, callback2)

        self.panel.SetTimeOut(0.3, callback1)

        @self.panel.btn_mark.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(607228, 607227)
            lpos = self.panel.btn_mark.getPosition()
            wpos = self.panel.btn_mark.getParent().convertToWorldSpace(lpos)
            lpos2 = dlg.panel.nd_game_describe.getParent().convertToNodeSpace(wpos)
            dlg.panel.nd_game_describe.setPosition(lpos2)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))

    def _on_update_reward(self, task_id):
        self.init_widget(do_update=True)
        global_data.emgr.refresh_activity_redpoint.emit()

    def init_widget(self, do_update=True):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task_id = int(task_list[0])
        task_list = task_utils.get_children_task(parent_task_id)
        count = len(task_list)
        self.total_count = count
        list_items = self.panel.list_items
        if not do_update:
            list_items.DeleteAllSubItem()
            list_items.SetInitCount(count - 1)
        cur_day = global_data.player.get_task_prog(parent_task_id)
        for i in range(count - 1):
            if i <= count - 2:
                item_widget = list_items.GetItem(i)
            else:
                item_widget = self.panel.temp_item
            if not do_update:
                if i == 6:
                    self._change_pos = item_widget.getPositionX()
            self.show_item(item_widget, i, do_update=do_update)

        list_items.BindMethod('OnScrolling', self._on_list_scrolling)
        if not do_update and cur_day > 0:
            list_items.LocatePosByItem(cur_day - 1)
        self._on_list_scrolling(list_items)
        can_sign_tasks = []
        collect_item_list = []
        collect_item_num = []
        if not do_update:
            list_total_items = self.panel.list_total_items
            list_total_items.DeleteAllSubItem()
            for i in range(count):
                task_id = task_list[i]
                reward_list = task_utils.get_task_reward_list(task_id)
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if not has_rewarded and i <= cur_day - 1:
                    can_sign_tasks.append(task_id)
                item_id, item_num = reward_list[1]
                if item_id not in collect_item_list:
                    collect_item_list.append(item_id)
                    collect_item_num.append(item_num)
                else:
                    index = collect_item_list.index(item_id)
                    collect_item_num[index] += item_num

            for i, item_id in enumerate(collect_item_list):
                item_num = collect_item_num[i]
                reward_item = list_total_items.AddTemplateItem()
                template_utils.init_tempate_mall_i_item(reward_item, item_id, item_num, show_tips=True, force_extra_ani=True)

        @self.panel.btn_temp_sign.btn.unique_callback()
        def OnClick(btn, touch):
            if can_sign_tasks:
                global_data.player.receive_all_task_reward(parent_task_id)

        enable = True if can_sign_tasks else False
        self.panel.btn_temp_sign.btn.SetShowEnable(enable)

    def show_item(self, item_widget, i, do_update=True):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task_id = int(task_list[0])
        task_list = task_utils.get_children_task(parent_task_id)
        cur_day = global_data.player.get_task_prog(parent_task_id)
        item_widget.lab_date.SetString(get_text_by_id(604004, [i + 1]))
        task_id = task_list[i]
        reward_list = task_utils.get_task_reward_list(task_id)
        item_widget.nd_lock.setVisible(False)
        item_widget.nd_tick.setVisible(False)
        item_widget.nd_tag.setVisible(False)
        item_widget.pnl_dark_bg.setVisible(False)
        item_widget.pnl_highlight.setVisible(False)
        item_widget.lab_date.SetColor(16760697)
        has_rewarded = global_data.player.has_receive_reward(task_id)
        if has_rewarded:
            item_widget.nd_tag.setVisible(True)
            item_widget.nd_tick.setVisible(True)
            item_widget.pnl_dark_bg.setVisible(True)
        elif i == cur_day - 1:
            item_widget.lab_date.SetColor('#SW')
            item_widget.pnl_highlight.setVisible(True)
        elif i > cur_day - 1:
            item_widget.nd_lock.setVisible(True)
        can_receive = False
        if not has_rewarded and i <= cur_day - 1:
            can_receive = True
        for j in range(2):
            item_id, item_num = reward_list[j]
            sub_item = item_widget.list_cell.GetItem(j)
            sub_item.lizi.setVisible(can_receive)
            if j == 1:
                item_widget.lab_limit.setVisible(i in (2, 6))
            if do_update:
                continue
            sub_item.lab_num.SetString(str(item_num))
            sub_item.lab_name.SetString(item_utils.get_lobby_item_name(item_id))
            sub_item.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_id))

            @sub_item.btn_item.unique_callback()
            def OnClick(btn, touch, item_id=item_id, item_num=item_num):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, item_num=item_num)
                return

    def _on_list_scrolling(self, slist):
        if slist.getContentSize().width - slist.getInnerContainer().getPositionX() < self._change_pos:
            cur_last_day = 6
        else:
            cur_last_day = self.total_count - 1
        if self._cur_last_day == cur_last_day:
            return
        self._cur_last_day = cur_last_day
        self.show_item(self.panel.temp_item, cur_last_day, do_update=False)

    def on_finalize_panel(self):
        self.process_event(False)