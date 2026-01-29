# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityJumpShare.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.comsys.share import ShareTemplateBase

class ActivityJumpShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityJumpShare, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.ui_data = {}
        self.task_id = ''
        self._activity_type = activity_type

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

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
        self.panel.PlayAnimation('appear')
        btn_share = self.panel.nd_content.btn_share
        btn_jump = self.panel.nd_content.btn_go
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.ui_data = conf.get('cUiData', {})
        self.task_id = conf.get('cTask', '')
        btn_share.BindMethod('OnClick', lambda *args: self.btn_share())
        btn_jump.BindMethod('OnClick', lambda *args: self.btn_jump())

    def btn_jump(self):
        from logic.gutils import jump_to_ui_utils
        func_name = self.ui_data.get('jump_func', 0)
        if func_name:
            func = getattr(jump_to_ui_utils, func_name)
            func and func()

    def btn_share(self):
        self.on_share()

    def on_share(self):
        share_pic = self.ui_data.get('share_pic', 'gui/ui_res_2/activity/activity_202305/open_activity_custom_room/bg_open_activity_custom_room_share.png')
        self.goto_share(share_pic=share_pic, hide_logo=True)

    def goto_share(self, tmpl=None, share_pic=None, hide_logo=False):
        from logic.comsys.share.CommonShareCreator import CommonShareCreator
        share_creator = CommonShareCreator()
        share_creator.create(None, tmpl)
        if share_pic:
            share_creator.set_img_bg(share_pic)
        if hide_logo:
            share_creator.panel.nd_logo.setVisible(False)
        from logic.comsys.share.ShareUI import ShareUI
        share_ui = ShareUI()
        share_ui.set_share_content_raw(share_creator.get_render_texture(), share_content=share_creator)

        def share_inform_func():
            if global_data.player:
                global_data.player.share_activity('activity_' + self._activity_type)
                global_data.player.share()

        share_ui.set_share_inform_func(share_inform_func)
        return