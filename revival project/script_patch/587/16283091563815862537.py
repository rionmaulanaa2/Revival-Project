# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Gulag/GulagInfoUI.py
from __future__ import absolute_import
import cc
import math3d
from common.uisys.basepanel import BasePanel
from common.utils.timer import CLOCK
from logic.gcommon import time_utility
from common.const.uiconst import TOP_ZORDER
from common.const.uiconst import UI_VKB_NO_EFFECT
from logic.gcommon.common_const.battle_const import TP_REASON_GULAG_REVIVE, TP_REASON_GULAG_ENTER_GAME, REVIVE_NONE, ST_IDLE, ST_IN_QUEUE, CANCEL_REASON_SURVIVAL_NUM, CANCEL_REASON_TIMEOUT
from logic.gcommon.item.item_const import ITEM_GULOG_REVIVE_COIN
COVER_MAX_TIME = 10
HIDE_COVER_TAG = 124535
TIPS_REFRESH_INTERVAL = 3.0
TIPS_LIST = [17985, 17986]
COUNTDOWN_TYPE_TELEPORT = 0
COUNTDOWN_TYPE_QUEUE = 1
COUNTDOWN_TYPE_ENTER_GAME = 2
COUNTDOWN_TYPE_PREPARE = 3
COUNTDOWN_TYPE_PARACHUTE = 4
COUNTDOWN_TEXT = {COUNTDOWN_TYPE_QUEUE: 17951,
   COUNTDOWN_TYPE_PREPARE: 17956
   }
WIN_ACT_TAG = 114514
TEAMMATE_REVIVE_TEXT = 17960
TEAMMATE_REVIVE_SUB_TEXT = 17961
CANCEL_REASON_TEXT = {CANCEL_REASON_TIMEOUT: 17963,CANCEL_REASON_SURVIVAL_NUM: 17964}

class GulagInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_gulade/battle_gulade_tips'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_rule.OnClick': 'on_click_btn_rule'
       }
    GLOBAL_EVENT = {'enter_gulag_revive_pending': 'on_enter_gulag_revive_pending',
       'gulag_revive_game_in_queue': 'on_revive_game_queue_update',
       'self_enter_gulag_revive_game': 'on_enter_revive_game',
       'gulag_revive_game_settle': 'on_revive_game_settled',
       'gulag_groupmate_revive': 'on_groupmate_revive',
       'scene_cam_observe_player_setted': 'clear_all',
       'on_gulag_force_cancel': 'on_gulag_cancel',
       'cam_lplayer_gulag_state_changed': 'on_player_gulag_state_changed'
       }

    def on_init_panel(self, *args, **kwargs):
        self.countdown_timer_id = None
        self.countdown_end_timestamp = 0
        self.countdown_type = None
        self.panel.pnl_content.setVisible(True)
        self.panel.icon_arrow.setRotation(180)
        self.tp_pos = None
        self.tp_finish_func = []
        self.gulag_game_id = REVIVE_NONE
        self.tips_refresh_timer = None
        self.cur_tip_idx = 0

        @self.panel.nd_tips.callback()
        def OnClick(*args):
            if not self.panel.nd_cover.isVisible():
                return
            self.refresh_tips()
            if self.tips_refresh_timer:
                global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
            self.tips_refresh_timer = global_data.game_mgr.register_logic_timer(self.refresh_tips, TIPS_REFRESH_INTERVAL, times=-1, mode=CLOCK)

        old_sz = self.panel.bar_lab_mode.getPreferredSize()
        self.panel.bar_lab_mode.SetContentSize(self.panel.lab_mode.getTextContentSize().width + 100, old_sz.height)
        self.gulag_canceled = None
        return

    def on_click_btn_rule(self, *args):
        show = not self.panel.pnl_content.isVisible()
        self.panel.pnl_content.setVisible(show)
        self.panel.icon_arrow.setRotation(180 if show else 0)
        if show:
            self.panel.nd_item.SetPosition('3', '100%-188')
        else:
            self.panel.nd_item.SetPosition('3', '100%-50')

    def on_enter_gulag_revive_pending(self, enter_timestamp):
        global_data.ui_mgr.close_ui('SOSUI')
        tp_left_time = enter_timestamp - time_utility.time()
        if tp_left_time <= 0:
            return
        if tp_left_time > 1:
            self.panel.StopAnimation('out_fuho_start')
            self.panel.PlayAnimation('show_fuho_start')
            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(tp_left_time - 1),
             cc.CallFunc.create(lambda : self.panel.StopAnimation('show_fuho_start')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('out_fuho_start')),
             cc.CallFunc.create(lambda : self.set_cover_visible(True))]))
        else:
            self.set_cover_visible(True)

    def on_revive_game_queue_update(self, queue_info):
        if self.countdown_type is None or self.countdown_type == COUNTDOWN_TYPE_QUEUE:
            self.start_countdown(COUNTDOWN_TYPE_QUEUE, queue_info['last_in_queue_timestamp'] + queue_info['max_in_queue_duration'])
        else:
            self.countdown_timestamp_cache = queue_info['last_in_queue_timestamp'] + queue_info['max_in_queue_duration']
        return

    def on_enter_revive_game(self, game_id, game_detail, scene_detail):
        self.panel.nd_repechage.setVisible(False)
        tp_left_time = game_detail['enter_area_timestamp'] - time_utility.time()
        if tp_left_time <= 0:
            return
        self.stop_countdown()
        self.countdown_timestamp_cache = game_detail['fight_timestamp']
        if self.panel.nd_cover.isVisible():
            self.hold_cover = True
            self.panel.stopActionByTag(HIDE_COVER_TAG)
        elif tp_left_time > 1:
            self.panel.nd_return_countdown.img_shadow.lab_title.SetString(17975)
            self.start_countdown(COUNTDOWN_TYPE_ENTER_GAME, game_detail['enter_area_timestamp'] - 1)
        else:
            self.set_cover_visible(True)

    def on_revive_game_settled(self, notify_detail):
        settle_detail = notify_detail['settle_detail']
        parachute_timestamp = notify_detail.get('parachute_timestamp', time_utility.time() + 10)
        left_time = parachute_timestamp - time_utility.time()
        if left_time <= 0:
            return
        self.panel.nd_return_countdown.img_shadow.lab_title.SetString(17958)
        act = []
        if settle_detail.get('is_auto_win', False):
            force_cancel = settle_detail.get('force_cancel', 0)
            if force_cancel:
                self.gulag_canceled = force_cancel
                self.stop_countdown()
                self.panel.nd_repechage_cancle.bar_repechage.lab_title.SetString(17962)
                self.panel.nd_repechage_cancle.bar_repechage.lab_tips.SetString(CANCEL_REASON_TEXT.get(force_cancel, ''))
                self.panel.PlayAnimation('show_fuho_tips')
                if left_time >= 5:
                    act.extend([
                     cc.DelayTime.create(left_time - 3),
                     cc.CallFunc.create(lambda : self.panel.nd_repechage_cancle.setVisible(False)),
                     cc.CallFunc.create(lambda : self.start_countdown(COUNTDOWN_TYPE_PARACHUTE, parachute_timestamp))])
                else:
                    act.extend([
                     cc.DelayTime.create(left_time),
                     cc.CallFunc.create(lambda : self.panel.nd_repechage_cancle.setVisible(False))])
            else:
                self.panel.nd_repechage_cancle.bar_repechage.lab_title.SetString(17961)
                self.panel.nd_repechage_cancle.bar_repechage.lab_tips.SetString('')
                if left_time >= 5:
                    self.panel.PlayAnimation('show_fuho_tips')
                    act.extend([
                     cc.DelayTime.create(left_time - 3),
                     cc.CallFunc.create(lambda : self.panel.nd_repechage_cancle.setVisible(False)),
                     cc.CallFunc.create(lambda : self.start_countdown(COUNTDOWN_TYPE_PARACHUTE, parachute_timestamp))])
                else:
                    self.start_countdown(COUNTDOWN_TYPE_PARACHUTE, parachute_timestamp)
        else:
            win = global_data.cam_lplayer.id == settle_detail['winner_eid']
            if not win:
                return
            self.close_win_ani()
            self.panel.PlayAnimation('win')
            act.extend([
             cc.DelayTime.create(3.3),
             cc.CallFunc.create(self.win_ani_end)])
            if left_time >= 5:
                act.extend([
                 cc.CallFunc.create(self.close_win_ani),
                 cc.CallFunc.create(lambda : self.start_countdown(COUNTDOWN_TYPE_PARACHUTE, parachute_timestamp))])
            else:
                left_time -= 3.3
                if left_time > 0:
                    act.append(cc.DelayTime.create(left_time))
                act.append(cc.CallFunc.create(self.close_win_ani))
        if act:
            self.panel.runAction(cc.Sequence.create(act))

    def win_ani_end(self, *args):
        self.panel.PlayAnimation('loop')
        self.panel.nd_win.BindMethod('OnClick', self.close_win_ani)

    def close_win_ani(self, *args):
        self.panel.nd_win.UnBindMethod('OnClick')
        self.panel.StopAnimation('win')
        self.panel.StopAnimation('loop')
        self.panel.stopActionByTag(WIN_ACT_TAG)
        self.panel.nd_win.setVisible(False)
        self.panel.nd_repechage_cancle.setVisible(False)

    def on_groupmate_revive(self, eid, name):
        if self.gulag_game_id != REVIVE_NONE:
            return
        self.panel.PlayAnimation('show_left_tips')
        self.panel.SetTimeOut(2, lambda : self.panel.nd_repechage_teammate.setVisible(False))
        self.panel.lab_name.SetString(get_text_by_id(TEAMMATE_REVIVE_TEXT, (name,)))
        self.panel.lab_name_left.SetString(get_text_by_id(TEAMMATE_REVIVE_TEXT, (name,)) + get_text_by_id(TEAMMATE_REVIVE_SUB_TEXT))

    def on_gulag_cancel(self, cancel_reason):
        if self.gulag_game_id != REVIVE_NONE:
            return
        else:
            cancel_text = CANCEL_REASON_TEXT.get(cancel_reason, None)
            if cancel_text is None:
                return
            self.gulag_canceled = cancel_reason
            self.stop_countdown()
            self.panel.nd_repechage_cancle.bar_repechage.lab_title.SetString(17962)
            self.panel.nd_repechage_cancle.bar_repechage.lab_tips.SetString(cancel_text)
            self.panel.PlayAnimation('show_fuho_tips')
            self.panel.SetTimeOut(3, lambda : self.panel.nd_repechage_cancle.setVisible(False))
            return

    def on_update_gulag_revive_count(self, can_revive):
        revive_coin = 0
        if global_data.player and global_data.player.logic:
            revive_coin = global_data.player.logic.ev_g_item_count(ITEM_GULOG_REVIVE_COIN)
        free_revive = 1 if can_revive else 0
        revive_count = revive_coin + free_revive
        self.panel.lab_num.setString(get_text_by_id(17980, (revive_count,)))

    def on_player_gulag_state_changed(self, gulag_state, game_id, can_revive, is_canceled):
        self.gulag_game_id = game_id
        self.panel.nd_repechage_rule.setVisible(gulag_state == ST_IN_QUEUE)
        self.on_update_gulag_revive_count(can_revive)

    def on_teleport(self, tp_pos, tp_reason):
        if tp_reason not in (TP_REASON_GULAG_REVIVE, TP_REASON_GULAG_ENTER_GAME):
            return
        else:
            self.set_cover_visible(True)
            if tp_reason == TP_REASON_GULAG_ENTER_GAME:
                self.hold_cover = False
            self.tp_reason = tp_reason
            self.tp_pos = math3d.vector(*tp_pos)
            self.start_countdown(COUNTDOWN_TYPE_TELEPORT, None)
            return

    def start_countdown(self, countdown_type, end_timestamp):
        self.stop_countdown()
        self.countdown_end_timestamp = end_timestamp
        self.countdown_type = countdown_type
        self.countdown_timer_id = global_data.game_mgr.register_logic_timer(self.update_countdown, interval=1, times=-1, mode=CLOCK)
        self.update_countdown()

    def stop_countdown(self):
        self.destroy_countdown_timer()
        self.panel.StopAnimation('show_countdown')
        self.panel.StopAnimation('show_start')
        self.panel.StopAnimation('show_fuho_wait_tips')
        self.panel.nd_repechage_countdown.setVisible(False)
        self.panel.nd_return_countdown.setVisible(False)
        self.panel.nd_fight_countdown.setVisible(False)

    def update_countdown(self):
        end_timestamp = getattr(self, 'countdown_end_timestamp', None)
        if self.countdown_type == COUNTDOWN_TYPE_TELEPORT:
            if getattr(self, 'hold_cover', False):
                return
            if not global_data.battle:
                return
            scn = global_data.battle.get_scene()
            if end_timestamp:
                if time_utility.time() >= end_timestamp:
                    self.countdown_type = None
                    self.set_cover_visible(False)
                    tp_reason = getattr(self, 'tp_reason', None)
                    countdown_ts_cache = getattr(self, 'countdown_timestamp_cache', None)
                    if self.gulag_canceled:
                        pass
                    elif tp_reason == TP_REASON_GULAG_REVIVE:
                        countdown_ts_cache is not None and self.start_countdown(COUNTDOWN_TYPE_QUEUE, countdown_ts_cache)
                    elif tp_reason == TP_REASON_GULAG_ENTER_GAME:
                        self.panel.StopAnimation('show_start')
                        self.panel.nd_start.setVisible(False)
                        if global_data.cam_lplayer:
                            global_data.cam_lplayer.send_event('E_ENTER_GULAG_GAME_FINISH')
                        countdown_ts_cache is not None and self.start_countdown(COUNTDOWN_TYPE_PREPARE, countdown_ts_cache)
            elif scn and scn.check_collision_loaded(self.tp_pos):
                self.countdown_end_timestamp = time_utility.time()
            return
        else:
            if not end_timestamp:
                self.destroy_countdown_timer()
                return
            left_time = int(end_timestamp - time_utility.time())
            if left_time <= 0:
                self.panel.StopAnimation('show_countdown')
                self.panel.StopAnimation('show_start')
                self.panel.StopAnimation('show_fuho_wait_tips')
                self.panel.nd_repechage_countdown.setVisible(False)
                self.panel.nd_return_countdown.setVisible(False)
                self.panel.nd_fight_countdown.setVisible(False)
                if self.countdown_type == COUNTDOWN_TYPE_ENTER_GAME:
                    self.set_cover_visible(True)
                elif self.countdown_type == COUNTDOWN_TYPE_PREPARE:
                    self.panel.PlayAnimation('show_start')
                    self.panel.SetTimeOut(3, lambda : self.panel.nd_start.setVisible(False))
                self.destroy_countdown_timer()
                return
            if self.countdown_type in (COUNTDOWN_TYPE_PARACHUTE, COUNTDOWN_TYPE_ENTER_GAME):
                if not self.panel.nd_return_countdown.isVisible():
                    self.panel.PlayAnimation('show_countdown')
                else:
                    self.panel.PlayAnimation('count_return')
                self.panel.lab_count_return.SetString(str(left_time))
                self.panel.vx_lab_count_return.SetString(str(left_time))
            elif self.countdown_type == COUNTDOWN_TYPE_PREPARE:
                self.panel.nd_fight_countdown.setVisible(not self.panel.nd_cover.isVisible())
                self.panel.lab_count_fight.SetString(get_text_by_id(COUNTDOWN_TEXT[self.countdown_type], (left_time,)))
            elif self.countdown_type == COUNTDOWN_TYPE_QUEUE:
                self.panel.lab_countdown.SetString(get_text_by_id(COUNTDOWN_TEXT[self.countdown_type], (left_time,)))
                if not self.panel.nd_repechage_countdown.isVisible() and not self.panel.nd_cover.isVisible():
                    self.panel.PlayAnimation('show_fuho_wait_tips')
            return

    def destroy_countdown_timer(self):
        self.countdown_type = None
        if self.countdown_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.countdown_timer_id)
            self.countdown_timer_id = None
        return

    def set_cover_visible(self, visible):
        self.panel.nd_cover.setVisible(visible)
        self.panel.stopActionByTag(HIDE_COVER_TAG)
        if visible:
            self.panel.SetTimeOut(COVER_MAX_TIME, lambda : self.panel.nd_cover.setVisible(False), HIDE_COVER_TAG)
        global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
        self.tips_refresh_timer = None
        if visible:
            self.panel.PlayAnimation('tips')
            self.panel.PlayAnimation('show_mode')
            self.tips_refresh_timer = global_data.game_mgr.register_logic_timer(self.refresh_tips, TIPS_REFRESH_INTERVAL, times=-1, mode=CLOCK)
        else:
            self.panel.StopAnimation('tips')
            self.panel.StopAnimation('show_mode')
        return

    def refresh_tips(self, *args):
        self.cur_tip_idx += 1
        self.cur_tip_idx %= len(TIPS_LIST)
        self.panel.lab_tips.SetString(TIPS_LIST[self.cur_tip_idx])

    def clear_all(self, *args):
        self.destroy_countdown_timer()
        global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
        self.tips_refresh_timer = None
        self.panel.nd_repechage_countdown.setVisible(False)
        self.panel.nd_return_countdown.setVisible(False)
        self.panel.nd_fight_countdown.setVisible(False)
        self.panel.nd_start.setVisible(False)
        self.panel.nd_repechage_teammate.setVisible(False)
        self.panel.nd_cover.setVisible(False)
        self.panel.nd_repechage_rule.setVisible(False)
        self.panel.nd_win.setVisible(False)
        return

    def on_finalize_panel(self):
        super(GulagInfoUI, self).on_finalize_panel()
        self.destroy_countdown_timer()
        global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
        self.tips_refresh_timer = None
        return