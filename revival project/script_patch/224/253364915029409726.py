# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaSongbarUI.py
from __future__ import absolute_import
from six.moves import range
import six
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
import cc
from logic.gcommon import time_utility as tutil
import time
import game
import world
from logic.gutils.concert_utils import get_song_lyric, get_song_len, get_song_show_time, get_song_name, get_song_start_ts, get_sing_start_ts, get_zhuchi
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_local_content_ex, LANG_JA, get_cur_text_lang

class LyricsPlayer(object):

    def __init__(self):
        self._lrc_list = []
        self._line_idx = 0
        self._song_no = -1

    @property
    def song_no(self):
        return self._song_no

    @song_no.setter
    def song_no(self, val):
        self._song_no = val

    def destroy(self):
        self._lrc_list = []

    def set_file(self, file_path, append_lyrics=()):
        from . import pylrc
        import C_file
        self._lrc_list = []
        if file_path:
            content = C_file.get_res_file(file_path, '')
            if content:
                self._lrc_list = pylrc.parse(content)
        if append_lyrics:
            self._lrc_list.extend(append_lyrics)
            self._lrc_list = sorted(self._lrc_list)

    def restart(self):
        self._line_idx = 0

    def get_line_by_time(self, sec):
        line = self._line_idx
        num_lines = len(self._lrc_list)
        subs = self._lrc_list
        if line + 1 == num_lines:
            return (line, subs[line])
        else:
            for idx in range(self._line_idx, num_lines):
                if idx + 1 == num_lines or sec < subs[idx + 1].time:
                    self._line_idx = idx
                    return (
                     idx, subs[idx])

            return (-1, None)

    def get_line_by_index(self, idx):
        if idx < len(self._lrc_list):
            return (idx, self._lrc_list[idx])
        else:
            return (-1, None)
            return None


class KizunaSongbarUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_song_bar'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    ENABLE_HOT_KEY_SUPPORT = True
    TIMER_TAG = 210910
    GLOBAL_EVENT = {'change_concert_song_data_event': 'on_update_concert_song_data_ex',
       'into_concert_view_camera_event': 'on_into_concert_view_camera'
       }

    def on_init_panel(self, *args, **kwargs):
        super(KizunaSongbarUI, self).on_init_panel()
        self._song_idx = -1
        self._song_start_ts = -1
        self._timer = 0
        if global_data.battle.concert_start_ts <= 0:
            self._sing_start_ts = 0
            self._concert_start_ts = 0
        else:
            self._sing_start_ts = get_sing_start_ts() + global_data.battle.concert_start_ts
            self._concert_start_ts = global_data.battle.concert_start_ts
        self.panel.RecordAnimationNodeState('disappear')
        self.panel.RecordAnimationNodeState('show', black_dict={'vx_zong': {'visibility'}})
        self.has_send_danmu_line = ''
        self._lyrics_player = LyricsPlayer()
        self._need_show_lyric = False
        self.init_lyrics_shader()
        self.hide()
        self.init_song_show_info()

    def on_finalize_panel(self):
        super(KizunaSongbarUI, self).on_finalize_panel()
        self._lyrics_player.destroy()
        self._lyrics_player = None
        self.unregister_timer()
        self.unregister_count_timer()
        return

    def init_song_show_info(self):
        if global_data.battle:
            bat = global_data.battle
            self.on_update_concert_song_data(bat.concert_stage, bat.song_idx, bat.song_end_ts)

    def update_song_show(self):
        server_time = tutil.get_server_time()
        if self._sing_start_ts and self._sing_start_ts <= server_time or self._song_start_ts > 0:
            if not self.panel.getActionByTag(self.TIMER_TAG):
                self.refresh_time()
                self.register_timer()
                self.panel.nd_progress.setVisible(False)
                self.panel.lab_lyric.SetString('')
                self.show()

    def check_start_show(self):
        if self.panel.isVisible():
            self.panel.StopAnimation('disappear')
            self.panel.RecoverAnimationNodeState('disappear')
            self.panel.PlayAnimation('show')

    def on_update_concert_song_data(self, stage, song_idx, song_end_ts):
        if stage == battle_const.CONCERT_SING_STAGE and song_end_ts:
            self._song_start_ts = song_end_ts - get_song_len(song_idx)
            self._song_idx = song_idx
            self.update_song_show_time(song_idx)
        elif song_idx is not None and song_idx != -1:
            self._song_start_ts = song_end_ts - get_song_len(song_idx)
            self._song_idx = song_idx
        else:
            self._song_start_ts = -1
            self._song_idx = song_idx
        if song_idx is not None and song_idx != -1:
            if self._lyrics_player.song_no != song_idx:
                lyric_path = get_song_lyric(song_idx)
                zhuchi = get_zhuchi(song_idx)
                if lyric_path or zhuchi:
                    self._lyrics_player.set_file(lyric_path, zhuchi)
                    self._lyrics_player.song_no = song_idx
                    self._lyrics_player.restart()
                    self._need_show_lyric = True
                else:
                    self._need_show_lyric = False
                    self.panel.lab_lyric.SetString('')
        self.update_song_show()
        self.update_inout_song(stage, song_idx)
        return

    def on_update_concert_song_data_ex(self, stage, song_idx, song_end_ts):
        if global_data.battle.concert_start_ts <= 0:
            self._sing_start_ts = 0
            self._concert_start_ts = 0
        else:
            self._sing_start_ts = get_sing_start_ts() + global_data.battle.concert_start_ts
            self._concert_start_ts = global_data.battle.concert_start_ts
        self.on_update_concert_song_data(stage, song_idx, song_end_ts)

    def on_into_concert_view_camera(self, is_in):
        self.panel.vx_zong.setVisible(not is_in)

    def update_inout_song(self, stage, song_idx):
        in_song = stage == battle_const.CONCERT_SING_STAGE and song_idx != -1 and song_idx is not None
        server_time = tutil.get_server_time()
        if not in_song:
            self.panel.StopAnimation('show')
            self.panel.RecoverAnimationNodeState('show')
            self.panel.PlayAnimation('disappear')
        else:
            if not self.panel.IsPlayingAnimation('show'):
                self.panel.StopAnimation('disappear')
                self.panel.RecoverAnimationNodeState('disappear')
                self.panel.vx_zong.setOpacity(0)
                self.panel.PlayAnimation('show')
            self.panel.nd_progress.setVisible(True)
            song_len = get_song_len(song_idx)
            song_len_str = tutil.get_delta_time_str(song_len, fmt='%(min)02d:%(sec)02d')
            self.panel.lab_song_time.SetString(song_len_str)
            song_n = get_song_name(song_idx)
            if song_n:
                self.panel.lab_playing.SetString(song_n)
            else:
                self.panel.lab_playing.SetString('')
            song_pass_t = server_time - self._song_start_ts
            song_percent = int(song_pass_t / float(song_len) * 100)
            progress_song = self.panel.progress_song
            progress_song.SetPercent(song_percent)
        return

    def update_song_show_time(self, song_idx):
        if song_idx is None or song_idx == -1:
            return
        else:
            show_time = get_song_show_time(song_idx)
            song_len = get_song_len(song_idx)
            if not show_time:
                self.panel.img_showtime_prog.setVisible(False)
                return
            self.panel.img_showtime_prog.setVisible(True)
            start_percent = show_time[0] / float(song_len)
            end_percent = show_time[1] / float(song_len)
            sz = self.panel.progress_song.getContentSize()
            pos_start = sz.width * start_percent
            pos_end = sz.width * end_percent
            img_showtime_prog = self.panel.img_showtime_prog
            img_showtime_prog.SetPosition(pos_start, '50%0')
            old_sz = img_showtime_prog.getContentSize()
            img_showtime_prog.setContentSize(cc.Size(pos_end - pos_start, old_sz.height))
            self.panel.txt_showtime.ReConfPosition()
            server_time = tutil.get_server_time()
            song_time = server_time - self._song_start_ts
            if song_time < show_time[0] - 5:
                self.panel.txt_showtime.setVisible(True)
                self.register_count_timer(show_time[0] - 5 - song_time, lambda : self.show_showtime_tips())
            elif song_time < show_time[0] - 2:
                self.panel.txt_showtime.setVisible(True)
                self.register_count_timer(show_time[0] - 2 - song_time, lambda : self.show_showtime_tips())
            else:
                self.panel.txt_showtime.setVisible(False)
            return

    def show_showtime_tips(self):
        show_time = get_song_show_time(self._song_idx)
        if not show_time:
            return
        self.setup_show_time_tips(show_time[1] - show_time[0])
        wpos = self.panel.img_showtime_prog.ConvertToWorldSpacePercentage(5, 120)
        old_pos = self.panel.nd_tips.getPosition()
        new_x_pos = self.panel.nd_tips.getParent().convertToNodeSpace(wpos)
        self.panel.nd_tips.setPosition(cc.Vec2(new_x_pos.x, old_pos.y))
        self.panel.nd_tips.setVisible(True)
        self.panel.PlayAnimation('tips')
        self.panel.txt_showtime.setVisible(False)
        self.panel.nd_tips.SetTimeOut(5.0, lambda : self.panel.nd_tips.setVisible(False))

    def setup_show_time_tips(self, showtime_len):
        self.panel.lab_tips_title.SetString(get_text_by_id(82336, (int(showtime_len),)))
        self.panel.lab_tips_words.SetString(get_text_by_id(82349))

    def register_count_timer(self, countdown, callback):
        from common.utils.timer import CLOCK
        self.unregister_count_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=callback, interval=countdown, mode=CLOCK, times=1)

    def unregister_count_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def register_timer(self):
        self.panel.DelayCallWithTag(0.25, self.refresh_time, self.TIMER_TAG)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)

    def refresh_time(self):
        server_time = tutil.get_server_time()
        bat = global_data.battle
        if not (bat and self._sing_start_ts):
            return 0.5
        else:
            song_idx = self._song_idx
            stage = bat.concert_stage
            in_song = stage == battle_const.CONCERT_SING_STAGE and song_idx != -1 and song_idx is not None
            delay = 0.5
            if not in_song:
                if song_idx != -1 and song_idx is not None:
                    song_pass_t = server_time - self._song_start_ts
                    song_len = get_song_len(song_idx)
                    delay = self.check_show_lyric(song_idx, song_pass_t, song_len)
                else:
                    self.panel.lab_lyric.SetString('')
                return delay
            delay = 0.1
            song_pass_t = max(server_time - self._song_start_ts, 0)
            song_len = get_song_len(song_idx)
            delay = self.check_show_lyric(song_idx, song_pass_t, song_len)
            song_percent = int(song_pass_t / float(song_len) * 100)
            progress_song = self.panel.progress_song
            progress_song.SetPercent(song_percent)
            song_pass_str = tutil.get_delta_time_str(song_pass_t, fmt='%(min)02d:%(sec)02d')
            song_len = get_song_len(song_idx)
            song_len_str = tutil.get_delta_time_str(song_len, fmt='%(min)02d:%(sec)02d')
            self.panel.lab_song_time.SetString(song_pass_str + '/' + song_len_str)
            return min(delay, 0.1)
            return

    def check_show_lyric(self, song_idx, song_pass_t, song_len):
        if not self._need_show_lyric:
            return 0.1
        idx, line = self._lyrics_player.get_line_by_time(song_pass_t)
        if line:
            _, next_line = self._lyrics_player.get_line_by_index(idx + 1)
            if next_line:
                line_duration = next_line.time - line.time if 1 else min(song_len - line.time, song_pass_t - song_len)
                if next_line or song_pass_t - line.time > 5:
                    self.panel.lab_lyric.SetString('')
                    return 0.1
            if type(line.text) in six.integer_types:
                self.panel.lab_lyric.SetString(get_text_by_id(line.text))
            else:
                line_text = line.text.strip()
                if line_text and line_text[-1] in ('@', '#'):
                    self.panel.lab_lyric.SetString('')
                elif line_text.isdigit():
                    self.panel.lab_lyric.SetString(int(line_text))
                else:
                    self.panel.lab_lyric.SetString(line_text)
            if line_duration > 0:
                return line_duration
        return 0.1

    def init_lyrics_shader(self):
        pass