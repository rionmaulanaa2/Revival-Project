# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/LobbyNewbieGuideUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from common.framework import Singleton
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils import task_utils
import cc
BEGIN_EXAM_TIP_TEXT = {0: 5305,
   1: 5306,
   2: 5307,
   3: 5308
   }

class LobbyNewbieGuideMgr(Singleton):
    ALIAS_NAME = 'lobby_newbie_guide_mgr'

    def init(self):
        self.is_binded = False

    def on_finalize(self):
        if self.is_binded:
            self.is_binded = False
            self.process_event(False)
        if global_data.lobby_newbie_guide_archive:
            global_data.lobby_newbie_guide_archive.finalize()

    def guide_ui(self):
        return LobbyNewbieGuideUI()

    def process_event(self, bind):
        emgr = global_data.emgr
        event_handler_list = [{'event_name': 'ui_close_event','handler': 'show_choose_mode_tip_by_ui_close'}, {'event_name': 'begin_guide_after_advance_event','handler': 'show_choose_mode_tip'}, {'event_name': 'show_newbie_stage_entry_tip_event','handler': 'show_newbie_stage_entry_tip'}, {'event_name': 'certificate_ui_select_tag_event','handler': 'show_start_newbie_battle_tip'}, {'event_name': 'certificate_ui_select_tag_event','handler': 'show_newbie_stage_reward_tip'}, {'event_name': 'ui_close_event','handler': 'show_start_match_tip'}]
        for event_handler_data in event_handler_list:
            event_name = event_handler_data.get('event_name')
            event_handler_name = event_handler_data.get('handler')
            if not event_name or not event_handler_name:
                continue
            event_handler = getattr(self, event_handler_name)
            if not event_handler or not callable(event_handler):
                continue
            if bind:
                emgr.bind_events({event_name: event_handler})
            else:
                emgr.unbind_events({event_name: event_handler})

    def start_show_guide(self):
        if not self.is_binded:
            self.process_event(True)
            self.is_binded = True

    def show_choose_mode_tip_by_ui_close(self, ui_name):
        if ui_name != 'QualityLevelInitialUI':
            return
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_choose_mode', 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read('show_choose_mode'):
            return
        self.guide_ui().show_choose_mode_tip()

    def show_choose_mode_tip(self, *args):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_choose_mode', 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read('show_choose_mode'):
            return
        self.guide_ui().show_choose_mode_tip()

    def show_newbie_stage_entry_tip(self, *args):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_newbie_stage_entry', 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read('show_newbie_stage_entry'):
            return
        self.guide_ui().show_newbie_stage_entry_tip()

    def show_start_newbie_battle_tip(self, cur_stage_idx):
        tip_key = 'show_start_newbie_battle_{}'.format(cur_stage_idx)
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get(tip_key, 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read(tip_key):
            return
        self.guide_ui().show_start_newbie_battle_tip(cur_stage_idx)

    def show_newbie_stage_reward_tip(self, cur_stage_idx):
        tip_key = 'show_newbie_stage_reward_{}'.format(cur_stage_idx)
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get(tip_key, 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read(tip_key):
            return
        self.guide_ui().show_newbie_stage_reward_tip(cur_stage_idx)

    def show_start_match_tip(self, ui_name):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_start_match', 0) == 1:
            return
        player = global_data.player
        if not player:
            return
        if player.is_lobby_newbie_guide_read('show_start_match'):
            return
        self.guide_ui().show_start_match_tip(ui_name)


class LobbyNewbieGuideArchive(Singleton):
    ALIAS_NAME = 'lobby_newbie_guide_archive'

    def init(self):
        self.all_lobby_newbie_guide_archive = ArchiveManager().get_archive_data('lobby_newbie_guide')
        self.archive_key = self.init_lobby_newbie_guide_archive_key()

    def on_finalize(self):
        self.all_lobby_newbie_guide_archive.save(encrypt=True)
        super(LobbyNewbieGuideArchive, self).on_finalize()

    def init_lobby_newbie_guide_archive_key(self):
        return '{}_{}'.format(global_data.channel._hostnum, global_data.player.uid)

    def get_lobby_newbie_guide_archive(self):
        return self.all_lobby_newbie_guide_archive.get_field(self.archive_key, {})

    def update_lobby_newbie_guide_archive(self, key, value):
        cur_archive = self.all_lobby_newbie_guide_archive.get_field(self.archive_key, {})
        cur_archive[key] = value
        self.all_lobby_newbie_guide_archive[self.archive_key] = cur_archive
        self.all_lobby_newbie_guide_archive.save(encrypt=True)


class LobbyNewbieGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_beginner'
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    DLG_ZORDER = ui_const.GUIDE_LAYER_ZORDER

    def __init__(self):
        super(LobbyNewbieGuideUI, self).__init__()
        self.cur_show_nd_tip = None
        self.cur_show_nd_bg = None
        return

    def on_init_panel(self, *args, **kwargs):
        self.panel.nd_click.setVisible(False)
        self.panel.nd_unclick.setVisible(False)

    def on_finalize_panel(self):
        super(LobbyNewbieGuideUI, self).on_finalize_panel()
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)

    def hide_all_tips(self):
        if self.cur_show_nd_bg:
            self.cur_show_nd_bg.setVisible(False)
        if self.cur_show_nd_tip:
            self.cur_show_nd_tip.setVisible(False)

    def show_choose_mode_tip(self):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_choose_mode', 0) == 1:
            return
        player = global_data.player
        if player and player.is_lobby_newbie_guide_read('show_choose_mode'):
            return
        if task_utils.is_finished_one_certificate_task():
            return
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if not lobby_ui:
            return
        match_widget = lobby_ui.get_match_widget()
        if not match_widget:
            return
        self.panel.nd_mode.setVisible(True)
        self.panel.nd_click.setVisible(False)
        self.panel.nd_unclick.setVisible(True)
        self.panel.PlayAnimation('tips_mode')
        self.panel.nd_mode.nd_mode_choose.btn_mode_choose.nd_cut.img_mode.SetDisplayFrameByPath('', match_widget.get_img_mode_path())
        self.panel.nd_mode.nd_mode_choose.btn_mode_choose.lab_mode.SetString(match_widget.get_lab_mode_string())
        self.panel.nd_mode.nd_mode_choose.btn_mode_choose.lab_num.SetString(match_widget.get_lab_num_string())
        self.panel.nd_mode.nd_mode_choose.btn_mode_choose.nd_new_mode.setVisible(match_widget.get_nd_new_mode_visible())
        self.panel.nd_mode.nd_mode_choose.img_red.setVisible(match_widget.get_newbie_assessment_redpoint_visible())
        LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_choose_mode', 1)
        player and player.add_read_lobby_newbie_guide('show_choose_mode')
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.block(self.__class__.__name__)

        @self.panel.nd_mode.nd_mode_choose.btn_mode_choose.unique_callback()
        def OnClick(btn, touch):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.nd_mode.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            self.panel.nd_click.setVisible(False)
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if not lobby_ui:
                return
            match_widget = lobby_ui.get_match_widget()
            if not match_widget:
                return
            match_widget.on_click_mode_btn()
            global_data.emgr.show_newbie_stage_entry_tip_event.emit()

    def show_newbie_stage_entry_tip(self, *args):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_newbie_stage_entry', 0) == 1:
            return
        player = global_data.player
        if player and player.is_lobby_newbie_guide_read('show_newbie_stage_entry'):
            return
        if task_utils.is_finished_one_certificate_task():
            return
        self.panel.nd_beginner.setVisible(True)
        self.panel.nd_click.setVisible(False)
        self.panel.nd_unclick.setVisible(True)
        self.panel.PlayAnimation('tips_beginner')
        from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_JA
        is_jp = get_cur_text_lang() == LANG_JA and not global_data.feature_mgr.is_support_TextWithCarriageReturn_Shrink()
        if is_jp:
            self.panel.nd_beginner.nd_beginner_guide.bar_lab.lab_tips.SetFontSize(14)
        LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_newbie_stage_entry', 1)
        player and player.add_read_lobby_newbie_guide('show_newbie_stage_entry')
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.block(self.__class__.__name__)

        @self.panel.nd_beginner.btn_new.unique_callback()
        def OnClick(btn, touch):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.nd_beginner.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            match_mode_ui = global_data.ui_mgr.get_ui('MatchMode')
            if not match_mode_ui:
                return
            match_mode_ui.on_click_local_battle()

    def show_start_newbie_battle_tip(self, cur_stage_idx):
        tip_key = 'show_start_newbie_battle_{}'.format(cur_stage_idx)
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get(tip_key, 0) == 1:
            return
        player = global_data.player
        if player and player.is_lobby_newbie_guide_read(tip_key):
            return
        certificate_ui = global_data.ui_mgr.get_ui('CertificateMainUI')
        if not certificate_ui:
            return
        if certificate_ui.get_cur_task_status() != ITEM_UNGAIN:
            return
        cur_text_id = BEGIN_EXAM_TIP_TEXT.get(cur_stage_idx, 5289)
        self.panel.btn_start.nd_start_guide.bar_lab.lab_tips.SetString(cur_text_id)
        self.panel.btn_start.setVisible(True)
        self.panel.nd_click.setVisible(True)
        self.panel.nd_unclick.setVisible(False)
        self.panel.PlayAnimation('tips_start')
        player and player.add_read_lobby_newbie_guide(tip_key)
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.block(self.__class__.__name__)

        def click_empty_area(*args):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.btn_start.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive(tip_key, 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_choose_mode', 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_newbie_stage_entry', 1)

        self.panel.nd_click.BindMethod('OnClick', click_empty_area)

        @self.panel.btn_start.unique_callback()
        def OnClick(btn, touch):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive(tip_key, 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_choose_mode', 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_newbie_stage_entry', 1)
            certificate_ui = global_data.ui_mgr.get_ui('CertificateMainUI')
            if not certificate_ui:
                return
            certificate_ui.click_cur_start_battle_btn()
            self.panel.btn_start.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)

    def show_newbie_stage_reward_tip(self, cur_stage_idx):
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.3),
         cc.CallFunc.create(lambda : self.show_newbie_stage_reward_tip_core(cur_stage_idx))]))

    def show_newbie_stage_reward_tip_core(self, cur_stage_idx):
        if not self.panel or not self.panel.isValid():
            return
        tip_key = 'show_newbie_stage_reward_{}'.format(cur_stage_idx)
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get(tip_key, 0) == 1:
            return
        player = global_data.player
        if player and player.is_lobby_newbie_guide_read(tip_key):
            return
        certificate_ui = global_data.ui_mgr.get_ui('CertificateMainUI')
        if not certificate_ui:
            return
        if certificate_ui.get_cur_task_status() != ITEM_UNRECEIVED:
            return
        if certificate_ui.get_cur_tag_idx() != cur_stage_idx:
            return
        self.panel.nd_reward.setVisible(True)
        self.panel.nd_click.setVisible(True)
        self.panel.nd_unclick.setVisible(False)
        self.panel.PlayAnimation('tips_reward')
        player and player.add_read_lobby_newbie_guide(tip_key)
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.block(self.__class__.__name__)

        def click_empty_area(*args):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.nd_reward.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive(tip_key, 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_choose_mode', 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_newbie_stage_entry', 1)

        self.panel.nd_click.BindMethod('OnClick', click_empty_area)
        certificate_ui.set_reward_data(self.panel.nd_reward.temp_reward, certificate_ui.get_cur_task_id(), False)

        @self.panel.nd_reward.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive(tip_key, 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_choose_mode', 1)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_newbie_stage_entry', 1)
            certificate_ui = global_data.ui_mgr.get_ui('CertificateMainUI')
            if not certificate_ui:
                return
            self.panel.nd_reward.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            certificate_ui.click_cur_get_reward_btn()

    def show_close_certificate_ui_tip(self, *args):
        certificate_ui = global_data.ui_mgr.get_ui('CertificateMainUI')
        if not certificate_ui:
            return
        if not certificate_ui.is_third_stage_task(args[0]):
            return
        self.panel.nd_close_1.setVisible(True)
        self.panel.nd_click.setVisible(True)
        self.panel.PlayAnimation('tips_close_1')

        @self.panel.nd_close_1.temp_btn_close.btn_back.unique_callback()
        def OnClick(btn, touch):
            self.panel.nd_close_1.setVisible(False)
            self.panel.nd_click.setVisible(False)
            certificate_ui and certificate_ui.close()

    def show_close_match_mode_tip(self, ui_name):
        if ui_name != 'CertificateMainUI':
            return
        match_mode_ui = global_data.ui_mgr.get_ui('MatchMode')
        if not match_mode_ui:
            return
        self.panel.nd_close_2.setVisible(True)
        self.panel.nd_click.setVisible(True)
        self.panel.PlayAnimation('tips_close_2')

        @self.panel.nd_close_2.nd_top.btn_back.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.close_ui('MatchMode')
            self.panel.nd_close_2.setVisible(False)
            self.panel.nd_click.setVisible(False)
            global_data.emgr.show_close_match_mode_tip_end_event.emit()

    def show_start_match_tip(self, ui_name):
        guide_archive = LobbyNewbieGuideArchive().get_lobby_newbie_guide_archive()
        if guide_archive.get('show_start_match', 0) == 1:
            return
        player = global_data.player
        if player and player.is_lobby_newbie_guide_read('show_start_match'):
            return
        if task_utils.is_finished_one_certificate_task():
            return
        if ui_name != 'MatchMode':
            return
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if not lobby_ui:
            return
        match_widget = lobby_ui.get_match_widget()
        if not match_widget:
            return
        self.panel.nd_match.btn_match.lab_match.SetString(match_widget.get_lab_match_string())
        self.panel.nd_match.btn_match.icon_cancel.setVisible(False)
        self.panel.nd_match.setVisible(True)
        self.panel.nd_click.setVisible(False)
        self.panel.nd_unclick.setVisible(True)
        self.panel.PlayAnimation('new_guide')
        self.panel.PlayAnimation('waiting')
        player and player.add_read_lobby_newbie_guide('show_start_match')
        if global_data.is_pc_mode:
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.block(self.__class__.__name__)
        if G_IS_NA_PROJECT:
            self.panel.nd_match.nd_player_guide.bar_lab.lab_tips.SetString(5167)
        else:
            self.panel.nd_match.nd_player_guide.bar_lab.lab_tips.SetString(607221)

        def click_empty_area(*args):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.nd_match.setVisible(False)
            self.panel.nd_click.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_start_match', 1)

        self.panel.nd_unclick.BindMethod('OnClick', click_empty_area)

        @self.panel.nd_match.btn_match.unique_callback()
        def OnClick(*args):
            global_data.escape_mgr_agent and global_data.escape_mgr_agent.unblock(self.__class__.__name__)
            self.panel.nd_match.setVisible(False)
            self.panel.nd_unclick.setVisible(False)
            self.panel.nd_click.setVisible(False)
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if not lobby_ui:
                return
            match_widget = lobby_ui.get_match_widget()
            if not match_widget:
                return
            match_widget.on_click_match_btn()
            LobbyNewbieGuideArchive().update_lobby_newbie_guide_archive('show_start_match', 1)