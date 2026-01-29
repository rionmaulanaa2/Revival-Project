# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPhoneBinding.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel

class ActivityPhoneBinding(object):
    TEMPLATE = 'activity/i_phone_binding'

    def __init__(self):
        super(ActivityPhoneBinding, self).__init__()
        self.on_init_panel()

    def on_init_panel(self):
        self.panel = global_data.uisystem.load_template_create(self.TEMPLATE)
        self.panel.lab_tips.SetString('#SD\xe4\xba\xb2\xe7\x88\xb1\xe7\x9a\x84\xe5\x86\x85\xe6\xb5\x8b\xe7\x8e\xa9\xe5\xae\xb6:#r    \xe7\xbb\x91\xe5\xae\x9a\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x9c\x89\xe6\x95\x88\xe4\xbf\x9d\xe9\x9a\x9c\xe6\x82\xa8\xe7\x9a\x84\xe8\xb4\xa6\xe5\x8f\xb7\xe5\xae\x89\xe5\x85\xa8\xef\xbc\x8c\xe6\x96\xb9\xe4\xbe\xbf\xe6\x82\xa8\xe5\xbf\xab\xe9\x80\x9f\xe8\xa7\xa3\xe5\x86\xb3\xe6\xb8\xb8\xe6\x88\x8f\xe4\xb8\xad\xe7\x9a\x84\xe5\x90\x84\xe7\xa7\x8d\xe9\x97\xae\xe9\xa2\x98\xef\xbc\x8c\xe5\x90\x8c\xe6\x97\xb6\xe4\xb9\x9f\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x86\x8d\xe7\xac\xac\xe4\xb8\x80\xe6\x97\xb6\xe9\x97\xb4\xe4\xb8\xba\xe6\x82\xa8\xe5\xb8\xa6\xe6\x9d\xa5\xe6\xb8\xb8\xe6\x88\x8f#SW\xe6\xad\xa3\xe5\xbc\x8f\xe4\xb8\x8a\xe7\xba\xbf\xe7\x9a\x84\xe9\x80\x9a\xe7\x9f\xa5#n#SD\xef\xbc\x8c\xe8\xbf\x99\xe5\xb0\xb1\xe6\x98\xaf\xe7\xbb\x91\xe5\xae\x9a\xe6\x89\x8b\xe6\x9c\xba\xef\xbc\x8c\xe9\xa2\x86\xe5\x8f\x96\xe4\xb8\x93\xe5\xb1\x9e\xe7\x9a\x84\xe6\xb8\xb8\xe6\x88\x8f\xe5\xa5\x96\xe5\x8a\xb1\xe5\x90\xa7\xef\xbc\x81')

        @self.panel.btn_bind.btn_common_big.callback()
        def OnClick(*args):
            from logic.gcommon.common_const.activity_const import ACTIVITY_BIND_MOBILE
            from logic.comsys.activity.PhoneBindUI import PhoneBindUI
            from logic.comsys.activity.PhoneUnBindUI import PhoneUnBindUI
            cur_phone = global_data.player.get_cur_bind_phone()
            if global_data.player.has_activity(ACTIVITY_BIND_MOBILE):
                from logic.comsys.activity.PhoneBindUI import PhoneBindUI
                PhoneBindUI(self.panel, cur_phone)
            elif cur_phone is None or cur_phone == '':
                PhoneBindUI(self.panel)
            else:
                PhoneUnBindUI(self.panel, cur_phone)
            return

    def on_finalize_panel(self):
        pass

    def get_widget(self):
        return self.panel