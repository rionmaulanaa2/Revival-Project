# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/ConcertMusicPlayer.py
from __future__ import print_function

class ConcertMusicPlayer(object):

    def __init__(self):
        self.music_id = None
        self._time_conf_list = []
        self.all_time = 0
        self.part_time = 0
        self.part_index = 0
        self.music_path = ''
        return

    def destroy(self):
        self._time_conf_list = []

    def set_music_time_conf(self, time_conf):
        self._time_conf_list = time_conf

    def calculate_index_and_time_ex(self, data_list):
        cur_index = 0
        for index, data in enumerate(data_list):
            if self.all_time >= data[0]:
                cur_index = index
            else:
                break

        if cur_index >= len(data_list):
            cur_index = len(data_list) - 1
        cur_time = self.all_time - data_list[cur_index][0] - 1
        if cur_time < 0:
            cur_time = 0
        return (cur_index, cur_time)

    def set_time(self, t):
        self.all_time = t
        self.part_index, self.part_time = self.calculate_index_and_time_ex(self._time_conf_list)
        self.refresh_mv()

    def updata_time(self, dt, index, part_time, data_list):
        need_refresh = False
        part_time += dt
        while index + 1 < len(data_list) and self.all_time > data_list[index + 1][0]:
            part_time = self.all_time - data_list[index + 1][0]
            index += 1
            need_refresh = True
            if index >= len(data_list):
                index = 0

        return (
         need_refresh, index, part_time)

    def on_update(self, cur_dt):
        self.all_time += cur_dt
        self.updata_part_media(cur_dt)
        if self.music_path:
            if not global_data.sound_mgr.get_playing_music():
                self.refresh_mv()

    def updata_part_media(self, dt):
        need_refresh, self.part_index, self.part_time = self.updata_time(dt, self.part_index, self.part_time, self._time_conf_list)
        if need_refresh:
            self.refresh_mv()

    def refresh_mv(self):
        music_path = self._time_conf_list[self.part_index][1]
        print('refresh_mv', music_path)
        if music_path:
            global_data.sound_mgr.play_music(music_path)
            global_data.sound_mgr.reset_volume()
            self.music_path = music_path
            ms_time = self.part_time * 1000
            if self.part_index + 1 < len(self._time_conf_list):
                music_length = self._time_conf_list[self.part_index + 1][0] - self._time_conf_list[self.part_index][0]
                global_data.sound_mgr.seek_music_to(self.part_time / float(music_length))
            else:
                log_error('please add a stop time for music clip!!! need music length to calc percentage!', music_path)
        else:
            self.music_path = None
            global_data.sound_mgr.stop_music()
        return