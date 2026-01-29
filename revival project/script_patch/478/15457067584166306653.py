# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEEndStatisticsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.gcommon.common_const.scene_const import SCENE_PVE_END_STATISTICS_UI
from logic.client.const.lobby_model_display_const import PVE_END_UI
from .PVETeamStatisticsWidget import PVETeamStatisticsWidget
from logic.gcommon.common_const.pve_const import SETTLE_WIN, SETTLE_LOSE, SETTLE_SAVE, PVE_END_BG_PATH
from logic.gcommon.common_const.pve_const import MECHA_DEFAULT_BLESS
from common.cfg import confmgr
from .PVEEndUI import PVEEndUI
import six

class PVEEndStatisticsUI(PVEEndUI):
    DELAY_CLOSE_TAG = 20231106
    PANEL_CONFIG_NAME = 'pve/end/open_pve_end_reward'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self, settle_dict, teammate_settle_dict, *args, **kwargs):
        self.settle_dict = settle_dict
        mecha_id = self.settle_dict.get('mecha_id')
        for _mecha_id, bless_list in six.iteritems(MECHA_DEFAULT_BLESS):
            for bless_id in bless_list:
                if _mecha_id == mecha_id:
                    self.settle_dict['choosed_blesses'].setdefault(bless_id, 1)

        self.teammate_settle_dict = teammate_settle_dict
        self.hide_main_ui()
        self.init_params()
        self.init_ui()
        self.init_ui_events()
        self.do_switch_scene()

    def init_ui(self):
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('appear')
        self.panel.bar_reward.setVisible(False)
        self.panel.nd_reward.setVisible(True)
        self.panel.nd_personal.setVisible(False)
        self.panel.nd_team.setVisible(False)
        self.panel.btn_next.setVisible(False)
        self.panel.btn_quit.setVisible(True)
        self._init_bg()
        self._init_name_widget()
        self._init_title_widget()
        self._init_end_bar()
        self._init_info_widget()

    def init_ui_events(self):

        def share_cb(*args):
            self.panel.btn_quit.setVisible(True)
            self.panel.btn_share.setVisible(True)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.panel.btn_quit.setVisible(False)
            self.panel.btn_share.setVisible(False)
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._screen_capture_helper.take_screen_shot([
             self.__class__.__name__], self.panel, custom_cb=share_cb, head_nd_name='nd_player_info_1')

        @self.panel.btn_quit.unique_callback()
        def OnClick(btn, touch):
            self.play_disappear_anim()

    def do_switch_scene(self):
        new_scene_type = SCENE_PVE_END_STATISTICS_UI
        display_type = PVE_END_UI

        def on_load_scene(*args):
            camera_ctrl = global_data.game_mgr.scene.get_com('PartModelDisplayCamera')
            if not camera_ctrl:
                return
            self.init_model()

        extra_detail = self.settle_dict.get('extra_detail')
        chapter = extra_detail.get('chapter')
        difficulty = self.settle_dict.get('difficulty')
        scene_background_texture = PVE_END_BG_PATH.format(chapter, difficulty)
        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='PVEEndStatisticsUI', scene_content_type=SCENE_PVE_END_STATISTICS_UI, scene_background_texture=scene_background_texture)

    def do_show_panel(self):
        super(PVEEndUI, self).do_show_panel()

    def do_hide_panel(self):
        super(PVEEndUI, self).do_hide_panel()

    def _init_teammate_data_widget(self):
        statistics = self.settle_dict.get('statistics', {})
        extra_detail = self.settle_dict.get('extra_detail')
        game_info = {}
        game_info['rank'] = self.settle_dict.get('rank', 0)
        game_info['survival'] = statistics.get('survival', 0)
        game_info['chapter'] = extra_detail.get('chapter', 0)
        game_info['end_level'] = extra_detail.get('end_level', 0)
        game_info['difficulty'] = self.settle_dict.get('difficulty', 0)
        self._team_statistics_widget = PVETeamStatisticsWidget(self.panel.nd_team.temp_team_data, self.teammate_settle_dict, game_info)

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        super(PVEEndStatisticsUI, self).on_finalize_panel()
        global_data.emgr.change_model_display_scene_item.emit(None)
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        return