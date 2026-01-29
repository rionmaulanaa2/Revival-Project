# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityReservation.py
from __future__ import absolute_import
import six
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_const import activity_const

class ActivityReservation(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityReservation, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self.ui_data = confmgr.get('c_activity_config', activity_const.ACTIVITY_RESERVATION, 'cUiData', default={})

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        rewards = self.ui_data['rewards']
        item_index = 1
        for item_no, num in six.iteritems(rewards):
            img_name_node = getattr(self.panel, 'img_reward_%d' % item_index)
            lab_name_node = getattr(self.panel, 'lab_num_%d' % item_index)
            img_name_node.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))
            lab_name_node.SetString('x' + str(num))
            reward_node = getattr(self.panel, 'nd_reward_%d' % item_index)

            @reward_node.callback()
            def OnClick(layer, touch, item_no=item_no):
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

            item_index += 1

        btn = self.panel.btn_go

        @btn.unique_callback()
        def OnClick(btn, touch):
            self.goto_reservation()

        btn = self.panel.btn_details

        @btn.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_local_content(608077), get_text_local_content(608078))

    def goto_reservation(self):
        self.exec_custom_func(0)