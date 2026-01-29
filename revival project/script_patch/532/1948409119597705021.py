# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202111/ActivityCampChoose.py
from __future__ import absolute_import
from logic.gutils import activity_utils
from logic.comsys.activity.ActivitySimpleJump import ActivitySimpleJump
from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
from common.cfg import confmgr
from logic.client.const import share_const

class ShareBubbleUI(CommonShareBubbleUI):

    def get_exclude_platforms(self):
        return [
         share_const.APP_SHARE_MOBILE_QZONE, share_const.APP_SHARE_WEIXIN_MOMENT]


class ActivityCampChoose(ActivitySimpleJump):

    def on_init_panel(self):
        super(ActivityCampChoose, self).on_init_panel()
        k = self.__class__.__name__
        global_data.achi_mgr.get_user_archive_data(global_data.player.uid).set_field(str(k), 1)
        global_data.emgr.refresh_activity_redpoint.emit()
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(activity_type, self.__class__.__name__)

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            self.on_click_btn_question()

    def on_finalize_panel(self):
        super(ActivityCampChoose, self).on_finalize_panel()
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def btn_jump(self):
        data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        args = data.get('args')
        url = args[0]

        def share_cb(*argv):
            pass

        share_message = get_text_by_id(610162)
        share_title = get_text_by_id(610164)
        if url:
            ui = ShareBubbleUI(share_link=url, share_title=share_title, share_message=share_message, desc=share_message, share_cb=share_cb)
            nd = self.panel.btn_go
            lpos = nd.getPosition()
            world_pos = nd.getParent().convertToWorldSpace(lpos)
            ui.panel.lab_tips.SetString(610163)
            lpos = ui.getParent().convertToNodeSpace(world_pos)
            ui and ui.setPosition(lpos)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(193))

    def on_click_btn_question(self):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(610164), get_text_by_id(int(610165)))