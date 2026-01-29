# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/ActivityMechaFree.py
from __future__ import absolute_import
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
import logic.gcommon.const as gconst
from logic.gutils import item_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
import cc

class MechaFreeBase(object):

    def __init__(self, *args, **kwargs):
        self._panel_alone = True

    def _init_panel(self, root_panel=None):
        self._screen_capture_helper = None
        if not root_panel:
            self._root_panel = self.panel
        else:
            self._root_panel = root_panel
        root_panel = self._root_panel
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        root_panel.lab_title.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        import logic.gcommon.time_utility as tutil
        start_date = tutil.get_date_str('%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0), ignore_second=21600)
        root_panel.lab_time.SetString(get_text_by_id(601149, [start_date, finish_date]))

        @root_panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), 601180)
            x, y = root_panel.btn_question.GetPosition()
            wpos = root_panel.btn_question.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        @root_panel.btn_info.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self._on_click_btn_share()

        @root_panel.btn_play.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.lobby import LobbyMatchWidget
            from logic.comsys.lobby.MatchMode import MatchMode
            cur_battle_tid, sel_battle_type, sel_match_mode, sel_play_type = LobbyMatchWidget.get_battle_infos()
            MatchMode(None, sel_play_type, sel_battle_type, sel_match_mode)
            if not self._panel_alone:
                global_data.ui_mgr.close_ui('ActivitySpringFestivalMainUI')
            else:
                global_data.ui_mgr.close_ui('MechaFreeUI')
            return

        root_panel.PlayAnimation('show')
        return

    def _on_click_btn_share(self):
        if not global_data.video_player.is_in_init_state():
            global_data.game_mgr.show_tip(get_text_by_id(82150))
            return
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            from logic.comsys.share.SpringBenefitsShareCreator import SpringBenefitsShareCreator
            self._screen_capture_helper = ScreenFrameHelper()
            share_creator = SpringBenefitsShareCreator()
            share_creator.create()
            share_content = share_creator
            self._screen_capture_helper.set_custom_share_content(share_content)
        if self._screen_capture_helper:

            def custom_cb(*args):
                self._root_panel.btn_info.setVisible(True)
                self._root_panel.btn_play.setVisible(True)
                if not self._panel_alone:
                    self._root_panel.nd_content.SetPosition('50%0', '50%0')
                    self._root_panel.GetParent().GetParent().temp_btn_close.setVisible(True)
                else:
                    self.panel.temp_btn_back.setVisible(True)
                global_data.emgr.show_activity_tab_list.emit(True)

            self._root_panel.btn_info.setVisible(False)
            self._root_panel.btn_play.setVisible(False)
            if not self._panel_alone:
                self._root_panel.nd_content.SetPosition('50%-108', '50%0')
                self._root_panel.GetParent().GetParent().temp_btn_close.setVisible(False)
            else:
                self.panel.temp_btn_back.setVisible(False)
            global_data.emgr.show_activity_tab_list.emit(False)
            if not self._panel_alone:
                self._screen_capture_helper.take_screen_shot(['ActivitySpringFestivalMainUI'], self._root_panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1')
            else:
                self._screen_capture_helper.take_screen_shot(['MechaFreeUI'], self._root_panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1')


class ActivityMechaFree(ActivityBase, MechaFreeBase):

    def on_init_panel(self):
        self._panel_alone = False
        self._init_panel()