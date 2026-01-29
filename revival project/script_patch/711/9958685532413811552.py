# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/ConcertMVMgr.py
from __future__ import absolute_import
from __future__ import print_function
import math3d
import math
import time
import cclive
import render
import game3d
import os
import C_file
import six
from random import randint
from common.daemon_thread import DaemonThreadPool
import world
import common.utils.timer as timer
import exception_hook
from logic.manager_agents.manager_decorators import sync_exec
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
s_tv_info = (
 (
  (2.37, 70.3, 381.76), (0, 180.0, 0), (1.24, 1.37, 1.24)),)
s_cc_sound_volume_scale = 2.5
s_mv_model = 'model_new/scene/items/common/items_common_led_01.gim'
s_mv_wait_pic = 'gui/ui_res_2/share/bg_share_anniversary2022_1.png'

class ConcertMVPlayer(object):

    def __init__(self, prs_info=s_tv_info, model_path=s_mv_model, wait_pic=s_mv_wait_pic):
        self._time_conf_list = []
        self.prs_info = prs_info
        self.model_path = model_path
        self.wait_pic = wait_pic
        self.cclive_player = None
        self.mv_model = None
        self.mv_wait_model = None
        self.extra_screens_conf = {}
        self.extra_screens_dict = {}
        self.cur_kv_pic = ''
        self.is_mv_ready = False
        self.is_bind_mv_model = False
        self.video_name = ''
        self.hashed_video_path = ''
        self.part_index = 0
        self.part_time = 0
        self.all_time = 0
        self.is_need_seek_to = False
        self.seek_to_downcount = 0
        self.cur_mv_path = None
        self.mv_start_time = 0.0
        self.save_cc_sound_volume = 0.0
        self.check_progress_downcount = 0
        self.check_anim_progress_downcount = 1
        self.max_check_progress_count = 0
        self.is_check_progress = False
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            self.seek_scale = 1000000.0
        else:
            self.seek_scale = 1000.0
        global_data.emgr.cc_sound_volume_change += self.on_sound_volume_change
        self._mp4_video_index_set = set()
        self._wait_model_index_set = set()
        self._mp4_resolution_map = {}
        self._mp4_reso = None
        self._reso_changed = False
        self.prev_players = []
        self._gap_time_list = []
        self._gap_sample_count_down = 1.0
        self.last_seek_time = 0
        self._sound_switch = 1
        self._mirror_reflect = None
        return

    def set_play_time_conf(self, time_conf):
        self._time_conf_list = time_conf
        for idx, t_res_path in enumerate(self._time_conf_list):
            t, res_path_info = t_res_path
            if type(res_path_info) not in [list, tuple]:
                res_paths = [
                 res_path_info]
            else:
                res_paths = res_path_info
            for res_path in res_paths:
                if res_path.endswith('.mp4') or res_path.endswith('.mp3') or res_path.startswith('http'):
                    self._mp4_video_index_set.add(idx)
                if res_path.endswith('.png'):
                    self._wait_model_index_set.add(idx)

        self._wait_model_index_set.add(len(self._time_conf_list) - 1)

    def set_time(self, all_time):
        self.all_time = all_time
        self.part_index, self.part_time = self.calculate_index_and_time_ex(self._time_conf_list)
        self.refresh_all()

    def create_mv_model(self):
        for _, screen_player in six.iteritems(self.extra_screens_dict):
            screen_player.create_mv_model()

        def create_cb(model):
            self.mv_model = model
            if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
                model.all_materials.set_technique(1, 'shader/g93shader/effect_g93_cclive.nfx::TShader')
            rot = self.prs_info[0][1]
            rot_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180.0, math.pi * rot[1] / 180.0, math.pi * rot[2] / 180.0))
            model.world_rotation_matrix = rot_matrix
            model.scale = math3d.vector(*self.prs_info[0][2])
            self.bind_mv_model_tex()
            model_vis = bool(self.part_index not in self._wait_model_index_set)
            self.mv_model.visible = model_vis
            global_data.emgr.update_concert_copy_mv_model_visible.emit(model_vis)
            if self._mirror_reflect is not None:
                self.mv_model.mirror_reflect = self._mirror_reflect
            return

        global_data.model_mgr.create_model_in_scene(self.model_path, math3d.vector(*self.prs_info[0][0]), on_create_func=create_cb)

        def create_cb_mv_wait(model):
            self.mv_wait_model = model
            rot = self.prs_info[0][1]
            rot_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180.0, math.pi * rot[1] / 180.0, math.pi * rot[2] / 180.0))
            model.world_rotation_matrix = rot_matrix
            model.scale = math3d.vector(*self.prs_info[0][2])
            self.refresh_kv_pic()
            model_vis = bool(self.part_index in self._wait_model_index_set)
            self.mv_wait_model.visible = model_vis
            global_data.emgr.update_concert_copy_kv_model_visible.emit(model_vis)
            if self._mirror_reflect is not None:
                self.mv_wait_model.mirror_reflect = self._mirror_reflect
            return

        global_data.model_mgr.create_model_in_scene(self.model_path, math3d.vector(*self.prs_info[0][0]), on_create_func=create_cb_mv_wait)

    def get_show_mv_bg(self):
        if self.part_index < len(self._time_conf_list):
            _, res = self._time_conf_list[self.part_index]
            if type(res) in [list, tuple]:
                for _i in res:
                    if _i.endswith('.png'):
                        return _i

            elif res.endswith('.png'):
                return res
        return self.wait_pic

    def destroy(self):
        self._mp4_resolution_map = {}
        if self.mv_model and self.mv_model.valid:
            self.mv_model.destroy()
        self.mv_model = None
        if self.mv_wait_model and self.mv_wait_model.valid:
            self.mv_wait_model.destroy()
        self.mv_wait_model = None
        if self.extra_screens_dict:
            for screen_id, screen_player in six.iteritems(self.extra_screens_dict):
                screen_player.destroy()

            self.extra_screens_dict = {}
        global_data.emgr.cc_sound_volume_change -= self.on_sound_volume_change
        if self.cclive_player:
            self.cclive_player.stop()
            log_error('destroy cclive:stop')
            self.cclive_player = None
        return

    def reset_event(self):
        self.cclive_player.error_callback = self.error_callback
        self.cclive_player.video_ready_callback = self.video_ready_callback
        self.cclive_player.video_complete_callback = self.video_complete_callback
        self.cclive_player.seek_complete_callback = self._seek_to_complete_cb
        self.cclive_player.report_stat_callback = self._report_stat_callback
        self.cclive_player.free_flow_callback = self.free_flow_callback

    def free_flow_callback(*args):
        print('free_flow_callback')

    def _report_stat_callback(*args):
        print('_report_stat_callback')

    def error_callback(self, *args):
        print('erro with args', args)

    def _seek_to_complete_cb(self, *args):
        print('seek complete cb')

    def video_ready_callback(self, *args):
        print('video_ready_callback')
        self.is_mv_ready = True
        self.bind_mv_model_tex()
        self.is_need_seek_to = True
        self.seek_to_downcount = 20

    def bind_mv_model_tex(self):
        if not self.is_bind_mv_model and self.is_mv_ready and self.mv_model and self.mv_model.valid:
            provider = self.cclive_player.fetch_data_provider()
            if provider:
                render_tex = render.texture('cclive', data_provider=provider)
                self.mv_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', render_tex)
                global_data.emgr.bind_concert_copy_mv_model_tex.emit(render_tex)
                self.is_bind_mv_model = True

    def video_complete_callback(self, *args):
        print('video_complete_callback, player will be stop,so must reset it!!!(in fact, the video may not be finished)')
        if self.cclive_player:
            if self.cclive_player.current_position <= self.cclive_player.duration * 0.99:
                self.updata_part_media(0, is_force=True)
                return
        self.updata_part_media(0)

    def on_sound_volume_change(self, volume):
        self.save_cc_sound_volume = volume
        if not self.cclive_player:
            return
        if not self.is_check_progress:
            self.cclive_player.set_volume(volume * s_cc_sound_volume_scale * self._sound_switch)
            print('self.cclive_player.set_volume( on_sound_volume_change', volume * s_cc_sound_volume_scale)

    def remove_played_video(self):
        mp4_name_set = set()
        for t, media_path in self._time_conf_list:
            if type(media_path) not in [list, tuple]:
                media_paths = [
                 media_path]
            else:
                media_paths = media_path
            for media_p in media_paths:
                if 'http' not in media_p and (media_p.endswith('.mp4') or media_p.endswith('.mp3')):
                    mp4_name_set.add(media_p)

        for name in mp4_name_set:
            hashed_video_name = str(abs(int(hash(name))))
            hashed_full_path = os.path.join(game3d.get_doc_dir(), hashed_video_name)
            try:
                if os.path.exists(hashed_full_path):
                    os.remove(hashed_full_path)
            except:
                pass

    def refresh_mv(self):
        mp4_path_or_list = self._time_conf_list[self.part_index][1]
        if type(mp4_path_or_list) not in [list, tuple]:
            mp4_path_list = [mp4_path_or_list] if 1 else mp4_path_or_list
            mp4_path = ''
            for p in mp4_path_list:
                if p.startswith('http') or p.endswith('mp4') or p.endswith('mp3'):
                    mp4_path = p

            if self.part_index in self._mp4_video_index_set:
                mp4_path = self.get_adjusted_mp4_resolution_address(mp4_path)
                mp4_path.startswith('http') or self.play_local_mp4(mp4_path)
            else:
                self.cur_mv_path = None
                self.on_video_load_finish(mp4_path, from_http=True)
        else:
            if self.cclive_player:
                self.cclive_player.stop()
                log_error('refresh_mv cclive:stop')
            self.cur_mv_path = None
        return

    def refresh_all(self):
        self.refresh_mv()
        self.refresh_kv_pic()
        if self.mv_model:
            model_vis = bool(self.part_index not in self._wait_model_index_set)
            self.mv_model.visible = model_vis
            global_data.emgr.update_concert_copy_mv_model_visible.emit(model_vis)
        if self.mv_wait_model:
            model_vis = bool(self.part_index in self._wait_model_index_set)
            self.mv_wait_model.visible = model_vis
            global_data.emgr.update_concert_copy_kv_model_visible.emit(model_vis)
        self.max_check_progress_count = 0

    def play_local_mp4(self, mp4_path):
        print('play_local_mp4', mp4_path)
        self.video_name = mp4_path
        hashed_video_name = str(abs(int(hash(mp4_path))))
        hashed_full_path = os.path.join(game3d.get_doc_dir(), hashed_video_name)
        self.hashed_full_path = hashed_full_path
        if os.path.exists(hashed_full_path):
            self.on_video_load_finish(hashed_full_path)
        else:
            DaemonThreadPool().add_threadpool(self.thread_load_video, None, self.video_name, hashed_full_path)
        return

    def thread_load_video(self, video_name, hashed_full_path):

        def cb(res):
            self.on_video_load_finish(res)

        if not C_file.find_res_file(video_name, ''):
            res = None
        else:
            video_data = C_file.get_res_file(video_name, '')
            if not os.path.exists(game3d.get_doc_dir()):
                os.makedirs(game3d.get_doc_dir())
            try:
                with open(hashed_full_path, 'wb') as f:
                    f.write(video_data)
                res = hashed_full_path
            except Exception as e:
                exception_hook.post_error('partmv [play video] copy video data with exception {}:{}'.format(video_name, str(e)))
                res = None

        game3d.delay_exec(1, cb, (res,))
        return

    def reset_player(self):
        if self.cclive_player:
            self.cclive_player.stop()
            log_error('reset_player cclive:stop')
            self.prev_players.append(self.cclive_player)
            self.cclive_player = None
            self.recyle_players()
        return

    @sync_exec
    def recyle_players(self):
        self.prev_players = []

    def init_player(self):
        if self.cclive_player:
            self.reset_player()
        self.cclive_player = cclive.player()
        self.reset_event()

    def on_video_load_finish(self, full_path, from_http=False):
        log_error('on_video_load_finish', full_path)
        if self.cur_mv_path != full_path:
            log_error('on_video_load_finish cclive:stop')
            self.init_player()
            self.cclive_player.play_vod(full_path)
            self.cur_mv_path = full_path
            self.mv_start_time = time.time()
            self.is_bind_mv_model = False
            ui = global_data.ui_mgr.get_ui('WizardTrace')
            ui and ui.send_message("play_vod: '%s'" % full_path)
        self.is_check_progress = True
        self.last_seek_time = 0
        self._gap_time_list = []
        self.is_need_seek_to = True
        self.seek_to_downcount = 20

    def refresh_kv_pic(self):
        if self.mv_wait_model and self.mv_wait_model.valid:
            kv_pic = self.get_show_mv_bg()
            if kv_pic != self.cur_kv_pic:
                tex = render.texture(kv_pic)
                self.mv_wait_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex)
                self.cur_kv_pic = kv_pic
                global_data.emgr.bind_concert_copy_kv_model_pic.emit(kv_pic)

    def updata_part_media(self, dt, is_force=False):
        need_refresh, self.part_index, self.part_time = self.updata_time(dt, self.part_index, self.part_time, self._time_conf_list)
        if need_refresh or is_force:
            self.refresh_mv()
            self.refresh_kv_pic()
            if self.mv_model:
                model_vis = bool(self.part_index not in self._wait_model_index_set)
                self.mv_model.visible = model_vis
                global_data.emgr.update_concert_copy_mv_model_visible.emit(model_vis)
            if self.mv_wait_model:
                model_vis = bool(self.part_index in self._wait_model_index_set)
                self.mv_wait_model.visible = model_vis
                global_data.emgr.update_concert_copy_kv_model_visible.emit(model_vis)

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
        if self.part_index in self._mp4_video_index_set and self.cclive_player and self.is_mv_ready:
            if time.time() - self.mv_start_time > 3:
                self.check_anim_progress_downcount -= cur_dt
                if self.check_anim_progress_downcount <= 0:
                    self.sync_mv_time_func()
                    self.check_anim_progress_downcount = 1.0
            self.check_is_stuck(cur_dt)
            self.check_progress_downcount -= cur_dt
            if self.check_progress_downcount <= 0:
                if self.is_check_progress:
                    self.check_progress_downcount = 1.0
                else:
                    self.check_progress_downcount = 5.0
                if self.cclive_player.duration <= 0:
                    return
                if not self.is_bind_mv_model and self._reso_changed:
                    self.bind_mv_model_tex()
                    self._reso_changed = False
                interval_time = self.cclive_player.current_position / self.seek_scale - self.part_time
                if abs(interval_time) < 5.0 and self.max_check_progress_count > 10:
                    if self.is_check_progress:
                        self.is_check_progress = False
                        self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale * self._sound_switch)
                        print('self.cclive_player.set_volume(', self.save_cc_sound_volume * s_cc_sound_volume_scale)
                    return
                self.max_check_progress_count += 1
                if time.time() - self.mv_start_time < 5:
                    if interval_time < -1.5 or interval_time > 5.0:
                        if self.cclive_player.duration > 0:
                            self.cclive_seek_to(self.part_time)
                            self.last_seek_time = self.part_time
                    elif interval_time > 1.5:
                        if self.cclive_player:
                            self.cclive_player.pause()

                            def callback():
                                if self.cclive_player and self.part_index in self._mp4_video_index_set:
                                    self.cclive_player.resume()
                                    if self.is_check_progress:
                                        self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale * self._sound_switch)
                                        print('self.cclive_player.set_volume(', self.save_cc_sound_volume * s_cc_sound_volume_scale)

                            global_data.game_mgr.register_logic_timer(callback, interval=interval_time, times=1, mode=timer.CLOCK)
                            self.check_progress_downcount = interval_time + 1.0
                    elif self.is_check_progress:
                        self.is_check_progress = False
                        self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale * self._sound_switch)
                        print('self.cclive_player.set_volume(', self.save_cc_sound_volume * s_cc_sound_volume_scale)

    def cclive_seek_to(self, s_time):
        if self.cclive_player:
            self.cclive_player.seek_to(int(s_time * self.seek_scale))

    def sync_mv_time_func(self):
        if self.part_index in self._mp4_video_index_set and self.cclive_player and self.is_mv_ready:
            mv_time = self.cclive_player.current_position / self.seek_scale
            global_data.emgr.sync_concert_mv_time_event.emit(mv_time)

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

    def set_resolution_map_dict(self, reso_map):
        self._mp4_resolution_map = reso_map

    def set_mp4_resolution_level(self, reso, need_refresh=True):
        self._reso_changed = reso != self._mp4_reso and self._mp4_reso is not None
        self._mp4_reso = reso
        if need_refresh:
            self.refresh_mv()
        return

    def get_adjusted_mp4_resolution_address(self, mp4_address):
        if not self._mp4_reso:
            return mp4_address
        mp4_address = mp4_address.strip()
        if mp4_address not in self._mp4_resolution_map:
            return mp4_address
        ret = self._mp4_resolution_map.get(mp4_address, {}).get(self._mp4_reso, mp4_address)
        return ret

    def check_is_stuck(self, dt):
        if not self.cclive_player:
            return
        if time.time() - self.mv_start_time > 5:
            self._gap_sample_count_down -= dt
            if self._gap_sample_count_down <= 0:
                self._gap_sample_count_down = 1.0
                interval_time = abs(self.cclive_player.current_position / self.seek_scale - self.part_time)
                self._gap_time_list.append(interval_time)
                if len(self._gap_time_list) > 3:
                    self._gap_time_list = self._gap_time_list[-3:]
                    if self._gap_time_list[2] > self._gap_time_list[1] > self._gap_time_list[0] and self._gap_time_list[2] - self._gap_time_list[0] > 0.5:
                        if self.cclive_player.current_position < self.cclive_player.duration * 0.98:
                            global_data.emgr.concert_video_stuck_event.emit()

    def set_sound_switch(self, val):
        self._sound_switch = val
        if self._sound_switch <= 0.01:
            if self.cclive_player:
                self.cclive_player.set_volume(self._sound_switch)

    def get_sound_switch(self):
        return self._sound_switch

    def set_extra_screens(self, screen_confs):
        from logic.vscene.part_sys.Concert.ExtraCopyScreen import ExtraCopyScreen
        self.extra_screens_conf = screen_confs
        for screen_id, screen_conf in six.iteritems(screen_confs):
            copy_screen = ExtraCopyScreen(screen_conf.get('prs'), screen_conf.get('model_path'))
            self.extra_screens_dict[screen_id] = copy_screen

    def set_mirror_reflect(self, reflect):
        self._mirror_reflect = reflect
        if self.mv_model and self.mv_model.valid:
            self.mv_model.mirror_reflect = reflect
        if self.mv_wait_model and self.mv_wait_model.valid:
            self.mv_wait_model.mirror_reflect = reflect