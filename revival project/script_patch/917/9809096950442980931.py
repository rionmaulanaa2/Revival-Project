# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryHistoryWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gutils import template_utils

class LotteryHistoryWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self._init_widgets()
        self._register_callback()
        self.hide()

    @property
    def cur_lottery_id(self):
        return self.parent.cur_lottery_id

    def _init_widgets(self):
        self.panel.list_history.setVisible(True)
        self.panel.nd_empty.setVisible(False)
        self.panel.btn_tips.setVisible(False)

    def _register_callback(self):

        @self.panel.nd_close.unique_callback()
        def OnClick(btn, touch):
            self.hide()

    def show_history(self):
        global_data.player.request_lottery_history(self.cur_lottery_id)
        self.show()
        self.refresh(global_data.player.get_lottery_history(self.cur_lottery_id))

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'lottery_history_updated': self._refresh_lottery_history_widget,
           'lottery_data_ready': self.lottery_data_ready,
           'lottery_history_open': self.show_history
           }
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def destroy(self):
        self.panel = None
        return

    def show(self):
        if self.panel.isVisible():
            return
        self.panel.setVisible(True)

    def hide(self):
        if not self.panel.isVisible():
            return
        self.panel.setVisible(False)

    def refresh(self, history_of_one_kind):
        if history_of_one_kind:
            self.panel.list_history.setVisible(True)
            data_cnt = len(history_of_one_kind)
            for i in range(data_cnt):
                record_idx = i
                item_idx = i
                record = history_of_one_kind[record_idx]
                item_node = self.panel.list_history.GetItem(item_idx)
                if item_node is None:
                    item_node = self.panel.list_history.AddTemplateItem()
                item_node.setVisible(True)
                self._refresh_record_item_node(item_node, record)

            for i in range(self.panel.list_history.GetItemCount() - data_cnt):
                record_idx = i + data_cnt
                item_node = self.panel.list_history.GetItem(record_idx)
                item_node.setVisible(False)

        else:
            self.panel.list_history.setVisible(False)
        self.panel.nd_empty.setVisible(not history_of_one_kind)
        return

    def _refresh_record_item_node(self, item_node, record):
        item_info = record.get('item_dict', None)
        chips_source = record.get('chips_source', {})
        if not item_info:
            return
        else:
            if six.PY2:
                item_id, item_num = next(six.iteritems(item_info))
            else:
                item_id, item_num = next(iter(six.iteritems(item_info)))
            chips_items = chips_source.get(item_id, {})
            chips_id = None
            chips_num = None
            for key, change_list in six.iteritems(chips_items):
                chips_id = key
                chips_num = change_list[0]

            if chips_id is None or chips_num is None:
                item_node.nd_smash_item.setVisible(False)
                template_utils.init_tempate_mall_i_item(item_node.temp_reward, int(item_id), item_num=item_num, show_tips=True, templatePath=item_node.temp_reward.GetTemplatePath())
            else:
                item_node.nd_smash_item.setVisible(True)
                item_node.nd_smash_item.btn_choose.SetSwallowTouch(True)
                template_utils.init_tempate_mall_i_item(item_node.nd_smash_item, int(item_id), item_num=item_num, show_tips=True, templatePath=item_node.nd_smash_item.GetTemplatePath())
                template_utils.init_tempate_mall_i_item(item_node.temp_reward, int(chips_id), item_num=chips_num, show_tips=True, templatePath=item_node.temp_reward.GetTemplatePath())
            return

    def _refresh_lottery_history_widget(self, lottery_id):
        if not lottery_id:
            return
        if lottery_id != self.cur_lottery_id:
            return
        if not self.panel.isVisible():
            return
        self.refresh(global_data.player.get_lottery_history(self.cur_lottery_id))

    def lottery_data_ready(self, bought_successfully=True):
        self.hide()
        if self.cur_lottery_id and global_data.player:
            global_data.player.reset_request_lottery_history_time(self.cur_lottery_id)