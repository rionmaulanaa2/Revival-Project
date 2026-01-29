# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGlShare.py
from __future__ import absolute_import
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.ActivityTemplate import ActivityGlobalTemplate

class ActivityGlShare(ActivityGlobalTemplate):
    ACTIVITY_TYPE = activity_const.ACTIVITY_GL_SHARE
    TIMES_SUFFIX = 608089

    def __init__(self, dlg, activity_type):
        super(ActivityGlShare, self).__init__(dlg, activity_type)
        self._init_ui_event()

    def _init_ui_event(self):

        @self.panel.btn_share.unique_callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_activity
            jump_to_activity('104')

    def set_show(self, show, is_init=False):
        super(ActivityGlShare, self).set_show(show)
        if show:
            self.second_callback()