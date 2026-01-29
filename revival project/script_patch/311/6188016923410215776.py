# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummerPeakWeekendMatch.py
from __future__ import absolute_import
import six
from .ActivityPeakWeekendMatch import ActivityPeakWeekendMatch
from common.cfg import confmgr
from logic.gcommon.cdata.round_competition import get_nearliest_competition_conf
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivitySummerPeakWeekendMatch(ActivityPeakWeekendMatch):

    def on_init_panel(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        lab_time_conf = conf.get('lab_time_text', {})
        lab_conf = conf.get('lab_text', {})
        lab_region_text = conf.get('lab_region_text', {})
        item = self.panel.list_rule.GetItem(0)
        item.lab_describe.SetString('')
        if lab_time_conf:
            host_num = global_data.channel.get_host_num()
            for text_id, host_num_list in six.iteritems(lab_time_conf):
                if host_num in host_num_list:
                    item.lab_describe.SetString(get_text_by_id(19360).format(int(text_id)))
                    return

            item.lab_describe.SetString(get_text_by_id(19360).format(12))
        if lab_conf and lab_region_text:
            host_num = global_data.channel.get_host_num()
            for region, host_num_list in six.iteritems(lab_conf):
                if host_num in host_num_list:
                    text_ids = lab_region_text.get(region, [])
                    text = '\n'.join([ get_text_by_id(text_id) for text_id in text_ids ])
                    item.lab_describe.SetString(text)
                    return

        size_text = item.lab_describe.getContentSize()
        item.lab_describe.formatText()
        sz = item.lab_describe.GetTextContentSize()
        old_sz = item.getContentSize()
        item.setContentSize(cc.Size(old_sz.width, sz.height + 20))
        item.RecursionReConfPosition()
        old_inner_size = self.panel.list_rule.GetInnerContentSize()
        self.panel.list_rule.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.list_rule.GetContainer()._refreshItemPos()
        self.panel.list_rule._refreshItemPos()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)