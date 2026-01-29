# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaLiveBattleMainUI.py
from __future__ import absolute_import
import time
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_VKB_NO_EFFECT, UI_TYPE_MESSAGE
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil
from logic.comsys.message.ConcertChat import ConcertChat
from logic.gutils.concert_utils import get_sing_start_ts, get_concert_end_ts, get_song_num
from logic.gcommon.common_const import battle_const
from logic.comsys.concert.KizunaLotteryWidgetUI import KizunaLotteryWidgetUI
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase

class ConcertShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_AI_CONCERT_INSIDE'


class KizunaLiveBattleMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_anniversary'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_normal_camera.OnClick': 'on_click_btn_normal_camera',
       'chat_content.btn_pull.OnClick': 'on_click_btn_pull',
       'chat_content.btn_open.OnClick': 'on_click_btn_pull',
       'btn_danmu.OnClick': 'on_click_btn_danmu',
       'btn_danmu_red.OnClick': 'on_click_btn_danmu_red',
       'btn_best_view.OnClick': 'on_click_best_view',
       'btn_exit.OnClick': 'on_click_btn_exit',
       'btn_set.OnClick': 'on_click_btn_set',
       'btn_action_share.OnClick': 'on_click_btn_share',
       'chat_content.btn_close.OnClick': 'on_click_chat_close_btn',
       'btn_gift.OnClick': 'on_click_btn_gift',
       'btn_resolution.OnClick': 'on_click_btn_resolution',
       'btn_refresh.OnClick': 'on_click_btn_refresh',
       'btn_red_packet.OnClick': 'on_click_btn_red_packet'
       }
    GLOBAL_EVENT = {'update_concert_data_info_event': 'update_concert_data_info',
       'change_concert_song_data_event': 'on_update_concert_song_data_ex',
       'concert_video_stuck_event': 'show_reso_change_tips'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'concert_share': {'node': 'nd_action_share.temp_pc'},'concert_best_view': {'node': 'nd_best_view.temp_pc'},'concert_take_photo': {'node': 'layer_camera.temp_pc'},'concert_start_chat': {'node': 'chat_content.btn_open.temp_pc'},'concert_switch_danmu': {'node': 'nd_danmu.temp_pc'},'concert_switch_red_packet_danmu': {'node': 'nd_danmu_red.temp_pc'},'concert_send_red_packet': {'node': 'nd_red_packet.temp_pc'},'concert_resolution': {'node': 'btn_resolution.temp_pc'},'concert_refresh': {'node': 'btn_refresh.temp_pc'},'concert_buy_gift_package': {'node': 'nd_gift.btn_gift.temp_pc'}}
    HOT_KEY_FUNC_MAP = {'concert_share': 'on_keyboard_switch_share',
       'concert_best_view': 'on_keyboard_switch_view',
       'concert_take_photo': 'on_keyboard_take_photo',
       'concert_start_chat': 'on_keyboard_open_chat',
       'concert_switch_danmu': 'on_keyboard_switch_danmu',
       'concert_resolution': 'on_keyboard_concert_resolution',
       'concert_refresh': 'on_keyboard_concert_refresh',
       'concert_switch_red_packet_danmu': 'on_keyboard_switch_red_packet_danmu',
       'concert_send_red_packet': 'on_keyboard_send_red_packet',
       'concert_buy_gift_package': 'on_keyboard_concert_gift'
       }
    TIMER_TAG = 210922
    GIFT_TIMER_TAG = 220818
    GIFT_TIPS_TIMER_TAG = 220811

    def on_init_panel(self, *args, **kwargs):
        super(KizunaLiveBattleMainUI, self).on_init_panel()
        self.is_in_chat = False
        self.need_jump_partmv = False
        self.is_danmu_enable_red = True
        self._last_play_gift_ani_time = 0
        self._timer = 0
        self._song_count = get_song_num()
        if global_data.battle.concert_start_ts <= 0:
            self._sing_start_ts = 0
            self._concert_end_ts = 0
        else:
            self._sing_start_ts = get_sing_start_ts() + global_data.battle.concert_start_ts
            self._concert_end_ts = get_concert_end_ts() + global_data.battle.concert_start_ts
        self._target_time = self._sing_start_ts
        local_gift_time = global_data.game_mode.get_cfg_data('play_data').get('gift_box_conf', {}).get('hide_time', 0)
        self._gift_target_time = local_gift_time + global_data.battle.concert_start_ts
        self.panel.chat_content.PlayAnimation('disappear_chat')
        self.panel.chat_content.FastForwardToAnimationTime('disappear_chat', self.panel.chat_content.GetAnimationMaxRunTime('disappear_chat'))
        self.panel.nd_time_count.setVisible(False)
        self.refresh_gift_time()
        self.register_gift_timer()
        self.refresh_gift_tips_time()
        self.register_gift_tips_timer()
        self._concert_chat = ConcertChat(self)
        self.init_danmu()
        self.init_danmu_red()
        self.panel.PlayAnimation('loop_gift')
        KizunaLotteryWidgetUI()
        self.panel.PlayAnimation('show_tips')
        self.panel.FastForwardToAnimationTime('show_tips', 0)
        self.last_refresh_time = 0

    def update_concert_data_info(self):
        self._sing_start_ts = get_sing_start_ts()
        if global_data.battle.concert_start_ts <= 0:
            self._sing_start_ts = 0
        else:
            self._sing_start_ts = get_sing_start_ts() + global_data.battle.concert_start_ts
            self._concert_end_ts = get_concert_end_ts() + global_data.battle.concert_start_ts
        local_gift_time = global_data.game_mode.get_cfg_data('play_data').get('gift_box_conf', {}).get('hide_time', 0)
        self._gift_target_time = local_gift_time + global_data.battle.concert_start_ts
        self.check_start_or_end_count_down(global_data.battle.concert_stage)
        self.check_introduce_ui_count_down()

    def on_update_concert_song_data_ex(self, stage, song_idx, song_end_ts):
        self.on_update_concert_song_data(stage, song_idx, song_end_ts)
        if self.need_jump_partmv:
            PartConcertMVMgr = global_data.game_mgr.scene.get_com('PartConcertMVMgr')
            PartConcertMVMgr.force_reset()
            self.need_jump_partmv = False

    def on_update_concert_song_data(self, stage, song_idx, song_end_ts):
        self.check_start_or_end_count_down(stage)
        self.check_introduce_ui_count_down()

    def check_start_or_end_count_down(self, stage):
        if not self._sing_start_ts:
            self.panel.nd_time_count.setVisible(False)
            self.unregister_timer()
            return
        if stage == battle_const.CONCERT_STOP_RELAX_STAGE:
            self.panel.nd_time_count.setVisible(True)
            self._target_time = self._concert_end_ts
            self.panel.img_thanks.setVisible(True)
            self.panel.lab_open.SetString(601214)
            self.refresh_time()
            self.unregister_timer()
            self.register_timer()
        elif stage < battle_const.CONCERT_SING_STAGE:
            start_ts = self._sing_start_ts
            server_time = tutil.get_server_time()
            if server_time < start_ts - 10:
                self.unregister_timer()
                self.register_timer()
                self.panel.nd_time_count.setVisible(True)
                self._target_time = self._sing_start_ts
                self.panel.img_thanks.setVisible(False)
                self.refresh_time()
                self.panel.lab_open.SetString(2296)
            else:
                self.panel.nd_time_count.setVisible(False)
                self.unregister_timer()
        else:
            self.panel.nd_time_count.setVisible(False)
            self.unregister_timer()

    def init_danmu(self):
        init_dammu_enable = True
        self.panel.PlayAnimation('danmu_on')
        self.set_danmu_enable(init_dammu_enable)

    def set_danmu_enable(self, is_enable):
        if is_enable:
            global_data.ui_mgr.show_ui('DanmuLinesUI', 'logic.comsys.observe_ui')
        dlg = global_data.ui_mgr.get_ui('DanmuLinesUI')
        if dlg is not None:
            dlg.enable_danmu(is_enable)
        self.is_danmu_enable = is_enable
        return

    def init_danmu_red(self):
        self.panel.PlayAnimation('danmu_red_on')
        self.set_danmu_red_enable(True)

    def set_danmu_red_enable(self, is_enable):
        self.is_danmu_enable_red = is_enable
        dlg = global_data.ui_mgr.get_ui('DanmuLinesUI')
        if dlg is not None:
            dlg.enable_danmu_of_tag('red_packet', is_enable)
        return

    def on_finalize_panel(self):
        super(KizunaLiveBattleMainUI, self).on_finalize_panel()
        global_data.ui_mgr.close_ui('KizunaLotteryWidgetUI')
        self.destroy_widget('_concert_chat')
        self.set_danmu_enable(False)
        self.unregister_timer()
        self.unregister_count_timer()
        self.unregister_gift_timer()
        self.unregister_gift_tips_timer()

    def check_introduce_ui_count_down(self):
        server_time = tutil.get_server_time()
        concert_intro_time = global_data.achi_mgr.get_cur_user_archive_data('concert_intro_time', 0)
        if self._sing_start_ts - concert_intro_time > 60:
            if 10 < self._sing_start_ts - server_time < 60:
                self.show_introduce_ui()
            elif self._sing_start_ts - server_time > 60:

                def callback():
                    self._timer = 0
                    self.show_introduce_ui()

                self.register_count_timer(self._sing_start_ts - server_time - 60, callback)
        else:
            self.unregister_count_timer()

    def register_count_timer(self, countdown, callback):
        from common.utils.timer import CLOCK
        self.unregister_count_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=callback, interval=countdown, mode=CLOCK, times=1)

    def unregister_count_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def show_introduce_ui(self):
        server_time = tutil.get_server_time()
        global_data.achi_mgr.set_cur_user_archive_data('concert_intro_time', server_time)
        from logic.comsys.concert.KizunaShowtimeIntroUI import KizunaShowtimeIntroUI
        ui = KizunaShowtimeIntroUI()
        if ui:
            ui.set_close_countdown(self._sing_start_ts - server_time - 5)

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act.setTag(self.TIMER_TAG)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)

    def register_gift_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.refresh_gift_time)]))
        self.panel.runAction(act)
        act.setTag(self.GIFT_TIMER_TAG)

    def unregister_gift_timer(self):
        self.panel.stopActionByTag(self.GIFT_TIMER_TAG)

    def register_gift_tips_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(2),
         cc.CallFunc.create(self.refresh_gift_tips_time)]))
        self.panel.runAction(act)
        act.setTag(self.GIFT_TIPS_TIMER_TAG)

    def unregister_gift_tips_timer(self):
        self.panel.stopActionByTag(self.GIFT_TIPS_TIMER_TAG)

    def refresh_gift_tips_time(self):
        if not global_data.battle:
            return
        gift_tips_list = global_data.game_mode.get_cfg_data('play_data').get('gift_tips_list', [])
        server_time = tutil.get_server_time()
        pass_time = server_time - global_data.battle.concert_start_ts
        for tips_time, tid in gift_tips_list:
            if 5 > tips_time - pass_time > 0 and server_time - self._last_play_gift_ani_time > 5:
                if not self.panel.IsPlayingAnimation('show_tips_gift'):
                    self.panel.lab_tips_gift.SetString(tid)
                    self.panel.PlayAnimation('show_tips_gift')
                    self._last_play_gift_ani_time = server_time

    def refresh_time(self):
        server_time = tutil.get_server_time()
        left_time = int(self._target_time - server_time)
        if left_time <= 10:
            self.panel.nd_time_count.setVisible(False)
            return
        self.panel.lab_time.SetString(tutil.get_readable_time_hour_minitue_sec(left_time))

    def refresh_gift_time(self):
        server_time = tutil.get_server_time()
        left_time = int(self._gift_target_time - server_time)
        if left_time < 0:
            self.panel.nd_gift.setVisible(False)
            self.panel.StopAnimation('loop_gift')
            ui = global_data.ui_mgr.get_ui('ConcertGiftBoxUI')
            if ui:
                ui.set_unbuyable()
            return
        self.panel.nd_gift.setVisible(True)
        self.panel.lab_gift_time.SetString(get_text_by_id(609708, [tutil.get_readable_time_hour_minitue_sec(left_time)]))

    def on_click_btn_normal_camera(self, btn, touch):
        from logic.comsys.share.BattleSceneOnlyUI import BattleSceneOnlyUI
        BattleSceneOnlyUI()

    def on_click_btn_pull(self, btn, touch):
        if self.is_in_chat:
            self.on_click_chat_close_btn(btn, touch)
        else:
            self.panel.chat_content.StopAnimation('disappear_chat')
            self.panel.chat_content.PlayAnimation('appear_chat')
            self.panel.chat_content.btn_open.setVisible(False)
            self.is_in_chat = True
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def on_click_chat_close_btn(self, btn, t):
        self.panel.chat_content.StopAnimation('appear_chat')
        self.panel.chat_content.PlayAnimation('disappear_chat')
        self.panel.chat_content.btn_open.setVisible(True)
        self.is_in_chat = False
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def on_click_btn_danmu(self, btn, touch):
        self.set_danmu_enable(not self.is_danmu_enable)
        self.panel.PlayAnimation('danmu_on' if self.is_danmu_enable else 'danmu_off')

    def on_click_btn_danmu_red(self, btn, touch):
        self.set_danmu_red_enable(not self.is_danmu_enable_red)
        self.panel.PlayAnimation('danmu_on_red' if self.is_danmu_enable_red else 'danmu_off_red')

    def on_click_best_view(self, btn, touch):
        from logic.vscene.parts.camera.FreeflyNonAOICameraController import FreeflyNonAOICameraController
        cam_controller = FreeflyNonAOICameraController()
        if not cam_controller.check_can_enable():
            return
        from logic.comsys.concert.KizunaConcertViewUI import KizunaConcertViewUI
        KizunaConcertViewUI()

    def on_click_btn_exit(self, btn, touch):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def on_confirm_quit():
            self.close()
            if global_data.player and global_data.player.logic:
                global_data.player.quit_battle(True)

        SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(82357), confirm_callback=on_confirm_quit)

    def on_click_btn_set(self, btn, touch):
        if global_data.player:
            global_data.ui_mgr.show_ui('MainSettingUI', 'logic.comsys.setting_ui')

    def on_click_btn_share(self, btn, touch):
        from logic.gutils import task_utils, item_utils, jump_to_ui_utils
        import random

        def update_func(share_panel):
            share_panel.nd_logo.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/activity_202212/txt_anniversary_title.png')
            share_panel.pnl_bg.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/share/bg_share_anniversary2023.png')

        from logic.gutils.jump_to_ui_utils import jump_to_general_share
        jump_to_general_share('share/i_share_game_task', update_func=update_func)

    def on_click_btn_refresh(self, btn, touch):
        cur_time = time.time()
        if cur_time - self.last_refresh_time > 1:
            global_data.emgr.refresh_concert_mv_event.emit()
        self.last_refresh_time = cur_time

    def on_keyboard_switch_share(self, msg, keycode):
        self.on_click_btn_share(None, None)
        return

    def on_keyboard_switch_view(self, msg, keycode):
        self.on_click_best_view(None, None)
        return

    def on_keyboard_take_photo(self, msg, keycode):
        self.on_click_btn_normal_camera(None, None)
        return

    def on_keyboard_open_chat(self, msg, keycode):
        if not self.is_in_chat:
            self.on_click_btn_pull(None, None)
        return

    def on_keyboard_switch_danmu(self, msg, keycode):
        self.on_click_btn_danmu(None, None)
        return

    def on_keyboard_concert_resolution(self, msg, keycode):
        self.on_click_btn_resolution(None, None)
        return

    def on_keyboard_concert_refresh(self, msg, keycode):
        self.on_click_btn_refresh(None, None)
        return

    def on_keyboard_switch_red_packet_danmu(self, msg, keycode):
        self.on_click_btn_danmu_red(None, None)
        return

    def on_keyboard_send_red_packet(self, msg, keycode):
        self.on_click_btn_red_packet(None, None)
        return

    def on_keyboard_concert_gift(self, msg, keyboard):
        if not self.panel.nd_gift.isVisible():
            return
        else:
            self.on_click_btn_gift(None, None)
            return

    def on_hot_key_state_opened(self):
        self.panel.nd_custom.setVisible(False)

    def on_hot_key_state_closed(self):
        self.panel.nd_custom.setVisible(True)

    def jump_to_song_show(self, song_idx, is_force, sec_offset=0):
        global_data.concert_time_offset = sec_offset
        msg = '@interpreter user.get_battle().sing_song(%d, %s, %d)' % (song_idx, is_force, sec_offset)
        self.need_jump_partmv = True
        import game
        game.on_debug_input(msg)

    def on_click_btn_gift(self, btn, touch):
        if not global_data.player:
            return
        if not global_data.battle:
            return
        from logic.comsys.concert.ConcertGiftBoxUI import ConcertGiftBoxUI
        ConcertGiftBoxUI()

    def on_click_btn_resolution(self, btn, touch):
        if not global_data.player:
            return
        from logic.comsys.concert.KizunaResolutionUI import KizunaResolutionUI
        KizunaResolutionUI()

    def show_reso_change_tips(self):
        self.show_reso_tips(633936)

    def show_reso_tips(self, text_id):
        if self.panel.IsPlayingAnimation('show_tips'):
            return
        self.panel.lab_reso_tips.SetString(text_id)
        self.panel.PlayAnimation('show_tips')

    def on_click_btn_red_packet(self, btn, touch):
        if not global_data.player:
            return
        from logic.comsys.concert.ConcertRedPacketSendUI import ConcertRedPacketSendUI
        ConcertRedPacketSendUI()