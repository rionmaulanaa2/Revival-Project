# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoRecord.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from functools import cmp_to_key
import os
import time
import audio
import shutil
from . import video_record_utils as vru
from common.utils import timer
from common.framework import Singleton
from common.platform import is_ios, is_android
from common.daemon_thread import DaemonThreadPool
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.ctypes.HighlightMoment import HighlightMoment
from logic.comsys.archive.archive_manager import ArchiveManager
HIGH_LIGHT_VIDEO_TIME_OUT = 60
WWISE_SOUND_CAPTURE_PLUGIN_ID = 264267658
QUALITY_TO_RESOLUTION_ANDROID = {2: [
     (640, 360), 1],
   3: [
     (720, 640), 1],
   4: [
     (960, 540), 1],
   5: [
     (1280, 720), 0.5]
   }
QUALITY_TO_RESOLUTION_IOS = {2: [
     (640, 360), 1],
   3: [
     (720, 640), 1],
   4: [
     (960, 540), 1],
   5: [
     (1280, 720), 0.5]
   }
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
BIT_RATE = 6000

class VideoRecord(Singleton):

    def get_video_state(self):
        if self._is_processing_video:
            return vru.V_STATE_PROCESSING
        else:
            if self._video_ready:
                return vru.V_STATE_READY
            return vru.V_STATE_NO_VIDEO

    def get_high_and_refine_video_info(self):
        return self._auto_save_info

    def is_video_saved(self, video_path):
        auto_save_time = self._archive_data.get_field(video_path, {}).get(vru.AUTO_TIME_KEY, None)
        if not auto_save_time:
            return True
        else:
            return False

    def manual_save_video(self, video_path, small_cover_info=None, show_tip=True):
        if not self._archive_data.has_field(video_path):
            if show_tip:
                global_data.game_mgr.show_tip(get_text_by_id(2183))
            return False
        if small_cover_info:
            self._archive_data[video_path][vru.SMALL_COVER_KEY] = small_cover_info
        self._archive_data[video_path].pop(vru.AUTO_TIME_KEY, 0)
        self._archive_data.save()
        self.update_auto_list(video_path)
        if show_tip:
            global_data.game_mgr.show_tip(get_text_by_id(2183))
        return True

    def del_video(self, video_path, update_auto_list=True):
        if video_path and self._archive_data.has_field(video_path):
            try:
                info = self._archive_data.get_field(video_path)
                cover_info = info.get(vru.SMALL_COVER_KEY, None)
                if cover_info:
                    _, cover_path, _ = cover_info
                    if os.path.exists(cover_path):
                        os.remove(cover_path)
                if os.path.exists(video_path):
                    os.remove(video_path)
                self._archive_data.del_field(video_path)
                self._archive_data.save()
                if update_auto_list:
                    self.update_auto_list(video_path)
            except Exception as e:
                log_error('[VideoRecord] del auto saved video error: %s' % str(e))

        return

    def update_auto_list(self, v_path):
        if v_path in self._auto_saved_list:
            self._auto_saved_list.remove(v_path)

    def update_cover_info(self, video_path, small_cover_info):
        if not self._archive_data.has_field(video_path):
            return False
        if small_cover_info:
            self._archive_data[video_path][vru.SMALL_COVER_KEY] = small_cover_info
            self._archive_data.save()
        return True

    def record_battle_video(self, battle_e_id, quality=5):
        if not vru.can_record_video():
            return False
        else:
            if self._is_recording and self._recording_battle == battle_e_id:
                log_txt = '[record_battle_video] is_recording %s' % battle_e_id
                self._log_in_inner_server(log_txt)
                return True
            if self._is_recording or self._is_processing_video:
                log_txt = '[record_battle_video] recording_path:%s, is_recording:%s, is_processing:%s' % (self._recording_path, self._is_recording, self._is_processing_video)
                self._log_in_inner_server(log_txt, is_error=True)
                return False
            now_time = int(get_server_time())
            if now_time - self._last_record_time < 1:
                log_txt = '[record_battle_video] record interval less 1 second'
                self._log_in_inner_server(log_txt, is_error=True)
                return False
            if not self.reset_all():
                return False
            video_out_path = vru.TEMP_PATH + '/' + str(now_time) + '.mp4'
            if not vru.clear_and_make_path([vru.TEMP_PATH]):
                self._log_in_inner_server('[record_battle_video] clear_and_make_path failed:%s' % (vru.TEMP_PATH,), is_error=True)
                return False
            if self.start_record(video_out_path, quality):
                self._last_record_time = now_time
                self._on_stop_cb = None
                self._recording_path = video_out_path
                self._record_type = vru.VIDEO_TYPE_BATTLE
                self._recording_battle = battle_e_id
                return True
            return False

    def free_record(self, video_path, on_start_cb=None, on_stop_cb=None, quality=5):
        if not vru.can_record_video():
            return False
        else:
            if self._is_recording:
                return False
            dir_path = os.path.dirname(video_path)
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            except Exception as e:
                self._log_in_inner_server('[free_record] error:%s' % str(e))
                return False

            self._on_start_cb = on_start_cb
            if self.start_record(video_path, quality):
                self._on_stop_cb = on_stop_cb
                self._recording_path = video_path
                self._record_type = vru.VIDEO_TYPE_FREE
                self._recording_battle = None
                self._need_save = True
                return True
            return False

    def stop_free_record(self, need_save=True):
        self._need_save = need_save
        self._on_start_cb = None
        self._stop_record()
        return

    def stop_battle_record(self, video_info, delay_time=0):

        def finish(battle_info=video_info):
            if self._recording_path:
                self._clear_timer()
                self._timer_begin_time = time.time()
                self._timer = global_data.game_mgr.register_logic_timer(self._on_timer_update, interval=1, times=-1, mode=timer.CLOCK)
                self._battle_video_info = battle_info
            else:
                self._reset_record_info()
                self._log_in_inner_server('stop_battle_record: no self._recording_path', is_error=True)
            self._stop_record()

        if delay_time > 0:
            import game3d
            game3d.delay_exec(delay_time * 1000, finish)
        else:
            finish()

    def reset_all(self, del_temp=True):
        self._reset_record_info()
        self._reset_task_info()
        self._stop_record()
        if del_temp:
            try:
                if os.path.exists(vru.TEMP_PATH):
                    shutil.rmtree(vru.TEMP_PATH, True)
            except Exception as e:
                self._log_in_inner_server('reset all error:[%s]' % str(e), is_error=True)
                return False

        return True

    def on_stop_record(self, json_dict):
        self._is_recording = False
        self._is_processing_video = True
        self._recording_battle = None
        video_length = get_server_time() - self._video_start_time
        success = True
        if not self._recording_path or not os.path.exists(self._recording_path):
            success = False
        if self._record_type == vru.VIDEO_TYPE_BATTLE:
            if not self._video_start_time or not self._battle_video_info:
                success = False
        self._log_in_inner_server('[on_stop_record] suc:%s, record_path:%s, start_time:%s, video_info:%s' % (success, self._recording_path, self._video_start_time, bool(self._battle_video_info)))
        global_data.emgr.on_video_stop_event.emit(success)
        if not success:
            if self._on_stop_cb and callable(self._on_stop_cb):
                self._on_stop_cb(False, self._recording_path)
            self._process_failed()
            return
        else:

            def finish_cb(request, ret):
                if self._record_type == vru.VIDEO_TYPE_BATTLE:
                    if ret:
                        self._generate_battle_videos(self._battle_video_info, self._video_start_time, self._recording_path, video_length)
                    else:
                        self._log_in_inner_server('[on_stop_record] md5 cal failed', is_error=True)
                        self._process_failed()
                else:
                    temp_video_info = {}
                    if ret:
                        temp_video_info['path'] = self._recording_path
                        temp_video_info['start_time'] = self._video_start_time
                        temp_video_info['end_time'] = get_server_time()
                        temp_video_info['key'] = vru.FREE_KEY
                        temp_video_info['md5_str'] = self._md5_info.get(self._recording_path, '')
                        self._archive_data[self._recording_path] = temp_video_info
                        self._archive_data.save()
                        vru.upload_record_suc_info_to_sa(vru.FREE_KEY)
                    else:
                        self._log_in_inner_server('[on_stop_record] md5 cal failed', is_error=True)
                    if self._on_stop_cb and callable(self._on_stop_cb):
                        self._on_stop_cb(ret, self._recording_path)
                        self._on_stop_cb = None
                    self.reset_all(del_temp=False)
                return

            if self._record_type == vru.VIDEO_TYPE_FREE and not self._need_save:
                self._on_stop_cb = None
                self.reset_all(del_temp=False)
                return
            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(self._generate_video_md5, finish_cb, self._recording_path)
            else:
                finish_cb(None, True)
            return

    def on_reject_record(self, json_dict):
        global_data.game_mgr.show_tip(get_text_by_id(3150))
        self._log_in_inner_server('[on_reject_record]')
        self._reset_record_info()
        self._stop_record()
        if self._record_type == vru.VIDEO_TYPE_BATTLE:
            global_data.player and global_data.player.call_soul_method('refuse_video_record')

    def on_trim_video(self, json_dict):
        path = json_dict.get('path', '') if is_ios() else json_dict.get('fileOutput', '')
        self._log_in_inner_server('[on_trim_video] result:%s' % (json_dict,))
        if not path or not os.path.exists(path):
            self._process_failed()
            self._log_in_inner_server('[on_trim_video] result:%s, path:%s, exists:%s' % (json_dict, path, os.path.exists(path)), is_error=True)
            return
        else:

            def finish_cb(request, ret):
                if not ret:
                    self._log_in_inner_server('[on_trim_video] md5 cal failed', is_error=True)
                    self._process_failed()
                    return
                self._log_in_inner_server('[on_trim_video] md5 cal success')
                if self._trim_tasks:
                    in_path, out_path, s_time, e_time = self._trim_tasks.pop()
                    self._trim_video(in_path, out_path, s_time, e_time)
                else:
                    vru.clear_and_make_path([vru.MERGE_TEMP_PATH])
                    for key, path_set in six.iteritems(self._trim_path_info):
                        valid_video_lst, start, end = vru.get_valid_merge_info(path_set)
                        self._log_in_inner_server('[generate merge task] key:%s, valid_lst:%s, start:%s, end:%s' % (key, valid_video_lst, start, end))
                        if end != 0:
                            out_path = vru.MERGE_TEMP_PATH + '/{0}_{1}_{2}.mp4'.format(int(start), int(end), key)
                            merge_video_length = 0
                            for v_path in valid_video_lst:
                                merge_video_length += self._video_length_info.get(v_path, 0)

                            self._video_length_info[out_path] = merge_video_length
                            if len(valid_video_lst) > 1:
                                self._merge_tasks.append((valid_video_lst, out_path))
                            elif len(valid_video_lst) == 1:
                                try:
                                    trim_video_path_only = valid_video_lst[0]
                                    shutil.copy(trim_video_path_only, out_path)
                                    os.remove(trim_video_path_only)
                                    md5_str = self._md5_info.pop(trim_video_path_only, '')
                                    self._md5_info[out_path] = md5_str
                                except Exception as e:
                                    self._log_in_inner_server('move trim video to merge path failed: %s' % str(e), is_error=True)

                            self._merge_path_info[key] = (
                             out_path, int(start), int(end))
                            audio_path = vru.prepare_mix_audio(key)
                            if audio_path:
                                video_name_no_file_type = '{0}_{1}_mix_{2}'.format(int(start), int(end), key)
                                video_name = video_name_no_file_type + '.mp4'
                                save_path = os.path.join(vru.MERGE_TEMP_PATH, video_name)
                                self._mix_path_info[key] = (save_path, video_name_no_file_type, int(start), int(end))
                                self._mix_tasks.append((out_path, audio_path, save_path, 0, merge_video_length + 1))

                    if global_data.is_inner_server:
                        for task in self._merge_tasks:
                            self._log_in_inner_server('[merge task] %s' % (task,))

                        for task in self._mix_tasks:
                            self._log_in_inner_server('[mix task] %s' % (task,))

                    if self._merge_tasks:
                        valid_lst, out_path = self._merge_tasks.pop()
                        self._merge_video_method(valid_lst, out_path)
                    elif self._mix_tasks:
                        video_path, audio_path, save_path, start_time, end_time = self._mix_tasks.pop()
                        self._mix_audio(video_path, audio_path, save_path, start_time, end_time)
                    else:
                        self._log_in_inner_server('[on_trim_video] not merge or mix task', is_error=True)
                        self._process_failed()

            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(self._generate_video_md5, finish_cb, path)
            else:
                finish_cb(None, True)
            return

    def on_merge_video(self, json_dict):
        path = json_dict.get('path', '') if is_ios() else json_dict.get('fileOutput', '')
        if is_ios():
            result = True
        elif is_android():
            result = json_dict.get('result', False)
        else:
            result = False
        if not result or not path or not os.path.exists(path):
            self._log_in_inner_server('[on_merge_video] result:%s, path:%s, exists:%s' % (result, path, os.path.exists(path)), is_error=True)
            self._process_failed()
            return
        else:

            def finish_cb(request, ret):
                if not ret:
                    self._log_in_inner_server('[on_merge_video] cal md5 failed', is_error=True)
                    self._process_failed()
                    return
                if self._merge_tasks:
                    valid_lst, out_path = self._merge_tasks.pop()
                    self._merge_video_method(valid_lst, out_path)
                elif self._mix_tasks:
                    video_path, audio_path, save_path, start_time, end_time = self._mix_tasks.pop()
                    self._mix_audio(video_path, audio_path, save_path, start_time, end_time)
                else:
                    self._log_in_inner_server('[on_trim_video] not mix task', is_error=True)
                    self._process_failed()

            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(self._generate_video_md5, finish_cb, path)
            else:
                finish_cb(None, True)
            return

    def on_start_record(self, json_dict):
        if is_ios():
            result = True
        elif is_android():
            result = json_dict.get('result', False)
        else:
            result = False
        if result:
            self._video_start_time = get_server_time()
            self._is_recording = True
            self._log_in_inner_server('[on_start_record] on start record success')
            global_data.game_mgr.show_tip(get_text_by_id(3149))
        else:
            self._process_failed()
            global_data.game_mgr.show_tip(get_text_by_id(3151))
            self._log_in_inner_server('[on_start_record] on start record failed', is_error=True)
        if self._on_start_cb:
            self._on_start_cb(result, self._recording_path)

    def on_mix_audio(self, json_dict):
        self._log_in_inner_server('[on_mix_audio] on mix:%s' % (json_dict,))
        path = json_dict.get('path', '') if is_ios() else json_dict.get('param', {}).get('save_path', '')
        if is_ios():
            result = True
        elif is_android():
            result = True if json_dict.get('result', 1) == 0 else False
        else:
            result = False
        if not result or not path or not os.path.exists(path):
            self._log_in_inner_server('[on_mix_audio] result:%s, path:%s, exists:%s' % (result, path, os.path.exists(path)), is_error=True)
            self._process_failed()
            return
        else:

            def finish_cb(request, ret):
                if not ret:
                    self._log_in_inner_server('[on_mix_audio] cal md5 failed', is_error=True)
                    self._process_failed()
                    return
                else:
                    if self._mix_tasks:
                        video_path, audio_path, save_path, start_time, end_time = self._mix_tasks.pop()
                        self._mix_audio(video_path, audio_path, save_path, start_time, end_time)
                    else:
                        self._check_all_md5(None, True)
                    return

            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(self._generate_video_md5, finish_cb, path)
            else:
                finish_cb(None, True)
            return

    def init(self):
        self._sample_rate = 48000
        self._is_recording = False
        self._recording_path = None
        self._battle_video_info = None
        self._video_start_time = 0
        self._last_record_time = 0
        self._recording_battle = None
        self._trim_tasks = []
        self._merge_tasks = []
        self._mix_tasks = []
        self._trim_path_info = {}
        self._merge_path_info = {}
        self._mix_path_info = {}
        self._auto_save_info = {}
        self._md5_info = {}
        self._video_length_info = {}
        self._is_processing_video = False
        self._timer = None
        self._timer_begin_time = 0
        self._record_type = None
        self._on_stop_cb = None
        self._on_start_cb = None
        self._need_save = True
        self._video_ready = False
        self._chat_msg_cache = []
        self._friend_msg_cache = []
        global_data.emgr.lobby_scene_pause_event += self._lobby_scene_event
        self._archive_data = ArchiveManager().get_archive_data(vru.SETTING_NAME)
        self._auto_saved_list = self._get_auto_save_list()
        return

    def _process_failed(self):
        self.reset_all(False)

    def _reset_record_info(self):
        self._is_processing_video = False
        self._video_ready = False
        self._recording_path = None
        self._battle_video_info = None
        self._video_start_time = 0
        self._clear_timer()
        return

    def _reset_task_info(self):
        self._trim_tasks = []
        self._merge_tasks = []
        self._mix_tasks = []
        self._trim_path_info = {}
        self._merge_path_info = {}
        self._mix_path_info = {}
        self._auto_save_info = {}
        self._md5_info = {}
        self._video_ready = False

    def _generate_video_md5(self, video_path):
        ret, md5_str = vru.cal_video_md5(video_path)
        if ret and md5_str:
            self._md5_info.setdefault(video_path, md5_str)
            return True
        else:
            self._log_in_inner_server('[_generate_video_md5] failed, path:%s' % (video_path,))
            return False

    def _generate_battle_videos(self, battle_video_info, start_time, recording_path, video_length):
        self._log_in_inner_server('[generate_battle_videos] video info:%s, start_time:%s, recording_path:%s, video_len:%s' % (battle_video_info, start_time, recording_path, video_length))
        if not os.path.exists(recording_path) or video_length < 1:
            self._log_in_inner_server('[generate_battle_videos] failed path:%s, exists:%s' % (recording_path, os.path.exists(recording_path)), is_error=True)
            self._process_failed()
            return
        self._reset_task_info()
        highlight_moments = []
        for info in battle_video_info:
            highlight = HighlightMoment()
            highlight.init_from_dict(info)
            highlight_moments.append(highlight)
            if highlight.start >= highlight.end or highlight.end <= start_time:
                continue
            start_trim, end_trim = vru.get_valid_trim_time(highlight.start, highlight.end, start_time, video_length)
            out_path = vru.HIGH_TRIM_TEMP_PATH + '/{0}_{1}_high.mp4'.format(int(highlight.start), int(highlight.end))
            self._log_in_inner_server('[high_trim_task] path:%s, out:%s, start:%s, end:%s' % (recording_path, out_path, start_trim, end_trim))
            self._trim_tasks.append((recording_path, out_path, start_trim, end_trim))
            self._trim_path_info.setdefault(vru.HIGH_KEY, set())
            self._trim_path_info[vru.HIGH_KEY].add(out_path)
            self._video_length_info[out_path] = end_trim - start_trim

        refine_trim_info = vru.get_refine_video_trim_info(highlight_moments, start_time, video_length)
        self._log_in_inner_server('[refine_trim_info] %s' % (refine_trim_info,))
        for out_path, start_trim, end_trim in refine_trim_info:
            self._trim_tasks.append((recording_path, out_path, int(start_trim), int(end_trim)))
            self._trim_path_info.setdefault(vru.REFINE_KEY, set())
            self._trim_path_info[vru.REFINE_KEY].add(out_path)
            self._video_length_info[out_path] = end_trim - start_trim

        if self._trim_tasks and vru.clear_and_make_path([vru.HIGH_TRIM_TEMP_PATH, vru.REFINE_TRIM_TEMP_PATH]):
            in_path, out_path, s_time, e_time = self._trim_tasks.pop()
            self._trim_video(in_path, out_path, s_time, e_time)
        else:
            self._log_in_inner_server('[generate_battle_videos] not trim task or clear and make path error')
            self._process_failed()

    def _on_timer_update(self, *args):
        if time.time() - self._timer_begin_time > HIGH_LIGHT_VIDEO_TIME_OUT:
            if not self._video_ready:
                self._log_in_inner_server('[_on_timer_update]')
                self._process_failed()
            return timer.RELEASE

    def _check_all_md5(self, request, ret):
        if not ret:
            self._log_in_inner_server('[generate_battle_videos] not trim task or clear and make path error')
            self._process_failed()
            return
        else:

            def success_generate_video():
                self._video_ready = True
                self._recording_path = None
                self._is_processing_video = False
                self._auto_save()
                self._clear_timer()
                vru.upload_record_suc_info_to_sa(vru.HIGH_KEY)
                return

            def cal_and_check_md5(*args):
                for video_path, md5_cache_str in six.iteritems(self._md5_info):
                    ret_cal, md5_cal_str = vru.cal_video_md5(video_path)
                    if not ret_cal or md5_cal_str != md5_cache_str:
                        self._log_in_inner_server('[_check_all_md5] failed, md5 check cache [%s] cal [%s]' % (md5_cache_str, md5_cal_str), is_error=True)
                        self._process_failed()
                        return False

                success_generate_video()
                return True

            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(cal_and_check_md5, None)
            else:
                success_generate_video()
            return

    def _clear_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def on_finalize(self):
        self._reset_record_info()
        super(VideoRecord, self).on_finalize()

    def _get_auto_save_list(self):
        auto_save_list = []
        for path, info in self._archive_data:
            auto_save_time = info.get(vru.AUTO_TIME_KEY, 0)
            if auto_save_time and auto_save_time > 0:
                auto_save_list.append(path)

        auto_save_list.sort(key=cmp_to_key(self._cmp_func), reverse=True)
        return auto_save_list

    def _cmp_func(self, path_1, path_2):
        time_1 = self._archive_data[path_1].get(vru.AUTO_TIME_KEY, 0)
        time_2 = self._archive_data[path_2].get(vru.AUTO_TIME_KEY, 0)
        if time_1 > time_2:
            return 1
        return -1

    def _auto_save(self):
        for key in self._mix_path_info:
            video_path, video_name_no_file_type, s_t, e_t = self._mix_path_info[key]
            if not os.path.exists(video_path) or vru.NEED_MD5 and video_path not in self._md5_info:
                continue
            temp_video_info = {}
            md5_str = self._md5_info.get(video_path, '')
            save_name = md5_str if vru.NEED_MD5 else video_name_no_file_type
            if is_ios():
                save_name = save_name + '.mp4' if 1 else save_name
                video_des_path = os.path.join(vru.HIGHLIGHT_PATH, save_name)
                try:
                    if not os.path.exists(vru.HIGHLIGHT_PATH):
                        os.makedirs(vru.HIGHLIGHT_PATH)
                    shutil.copyfile(video_path, video_des_path)
                    temp_video_info['path'] = video_des_path
                    temp_video_info['start_time'] = s_t
                    temp_video_info['end_time'] = e_t
                    temp_video_info['key'] = key
                    temp_video_info['md5_str'] = md5_str
                    temp_video_info[vru.AUTO_TIME_KEY] = get_server_time()
                    self._archive_data[video_des_path] = temp_video_info
                    self._archive_data.save()
                    self._auto_save_info[key] = video_des_path
                    self._auto_saved_list.append(video_des_path)
                except Exception as e:
                    self._log_in_inner_server('save failed:[%s]' % str(e), is_error=True)

        auto_saved_num = len(self._auto_saved_list)
        if auto_saved_num > vru.AUTO_SAVE_NUM:
            self._auto_saved_list.sort(key=cmp_to_key(self._cmp_func), reverse=True)
            for idx in range(vru.AUTO_SAVE_NUM, auto_saved_num):
                auto_save_path = self._auto_saved_list[idx]
                self.del_video(auto_save_path, update_auto_list=False)

            self._auto_saved_list = self._auto_saved_list[0:vru.AUTO_SAVE_NUM]

    def _wwise_audio_cap_cb(self, *args):
        if self._video_start_time > 0:
            data, data_size = args
            global_data.channel.push_game_voice_data(data_size, data, self._sample_rate, 16, 2)

    def start_record(self, video_out_path, quality=5):
        self._sample_rate = audio.set_audio_capture_enable(True, WWISE_SOUND_CAPTURE_PLUGIN_ID, self._wwise_audio_cap_cb, '')
        if self._sample_rate == 0:
            audio.set_audio_capture_enable(False, WWISE_SOUND_CAPTURE_PLUGIN_ID, None, '')
            self._log_in_inner_server(' start record failed:sample_rate == 0', is_error=True)
            return False
        else:
            if is_android():
                data_init = {'methodId': 'initGameVoice','audioSampleRate': self._sample_rate,
                   'channels': 2,
                   'bitsPerSample': 16
                   }
                data_start = {'methodId': 'startRecord',
                   'channel': 'cc',
                   'fileOutput': video_out_path,
                   'quality': quality,
                   'needPermission': False
                   }
                global_data.channel.extend_func_by_dict(data_init)
                global_data.channel.extend_func_by_dict(data_start)
                return True
            if is_ios():
                import render
                render_system_name = render.get_render_system_name()
                use_opengl = 0 if render_system_name in ('METAL', ) else 1
                data_init = {'methodId': 'setup',
                   'channel': 'cc',
                   'useOpenGL': use_opengl
                   }
                data_start = {'methodId': 'startRecord',
                   'channel': 'cc',
                   'fileOutput': video_out_path,
                   'useMetal': 0,
                   'quality': quality,
                   'useGameAudioSource': 1,
                   'muteAudio': False,
                   'extraInfo': '{"useFbo":1,"frame_size":{"frame_width":%d,"frame_height":%d},"encoder_params":{"width":%d,"height":%d,"bitrate":%d}}' % (VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_WIDTH, VIDEO_HEIGHT, BIT_RATE)
                   }
                global_data.channel.extend_func_by_dict(data_init)
                global_data.channel.extend_func_by_dict(data_start)
                return True
            return False
            return

    def _trim_video(self, in_path, out_path, start_time, end_time):
        data = {'methodId': 'trimVideo',
           'channel': 'cc',
           'fileInput': in_path,
           'fileOutput': out_path,
           'start': int(start_time),
           'end': int(end_time)
           }
        self._log_in_inner_server('[trim video] path:%s, out_path:%s, start:%s, end:%s' % (in_path, out_path, start_time, end_time))
        global_data.channel.extend_func_by_dict(data)

    def _stop_record(self):
        audio.set_audio_capture_enable(False, WWISE_SOUND_CAPTURE_PLUGIN_ID, None, '')
        if self._is_recording:
            data = {'methodId': 'stopRecord','channel': 'cc'
               }
            global_data.channel.extend_func_by_dict(data)
        return True

    def _merge_video_method(self, valid_lst, out_path):
        data = {'methodId': 'mergeVideo',
           'fileInputs': valid_lst,
           'channel': 'cc',
           'fileOutput': out_path,
           'flag': 0
           }
        global_data.channel.extend_func_by_dict(data)

    def _mix_audio(self, video_path, audio_path, save_path, start_time, end_time, loop=0):
        if is_android():
            data = {'methodId': 'mixAudio','param': {'video_path': video_path,
                         'audio_path': audio_path,
                         'save_path': save_path,
                         'video_volume': 1.0,
                         'audio_volume': 1.0,
                         'start_time': start_time,
                         'end_time': end_time,
                         'loop': loop
                         }
               }
            global_data.channel.extend_func_by_dict(data)
        elif is_ios():
            data = {'methodId': 'mixAudio','channel': 'cc',
               'video_path': video_path,
               'audio_path': audio_path,
               'save_path': save_path,
               'video_volume': 1.0,
               'audio_volume': 1.0,
               'start_time': start_time,
               'end_time': end_time,
               'loop': loop
               }
            global_data.channel.extend_func_by_dict(data)
        else:
            return False
        return True

    def set_cover_finish_callback(self, func):
        self._cover_finish_cb = func

    def create_video_cover(self, video_path, cover_path, scale, mode=0):
        data = {'methodId': 'createVideoCover',
           'channel': 'cc',
           'videoPath': video_path,
           'imagePath': cover_path,
           'scale': scale,
           'mode': mode
           }
        global_data.channel.extend_func_by_dict(data)
        return True

    def on_create_video_cover(self, json_dict):
        path = json_dict.get('path', '') if is_ios() else json_dict.get('imagePath', '')
        if is_ios():
            result = True
        elif is_android():
            result = json_dict.get('result', False)
        else:
            result = False
        if not result or not path or not os.path.exists(path):
            result = False
        if self._cover_finish_cb and callable(self._cover_finish_cb):
            self._cover_finish_cb(path)

    def _log_in_inner_server(self, msg, is_error=False):
        if global_data.is_inner_server:
            msg = '[VideoRecord] ' + msg
            if is_error:
                log_error(msg)
            else:
                print(msg)

    def add_chat_msg(self, channel, msg, extra_data):
        self._chat_msg_cache.append((channel, msg, extra_data))

    def add_friend_msg(self, f_data, msg, extra_data):
        self._friend_msg_cache.append((f_data, msg, extra_data))

    def _lobby_scene_event(self, pause_flag):
        if pause_flag:
            return
        for channel, msg, extra_data in self._chat_msg_cache:
            vru.send_video_msg_to_world(channel, msg, extra_data)

        for f_data, msg, extra_data in self._friend_msg_cache:
            vru.send_video_msg_to_friend(f_data, msg, extra_data)

        self._chat_msg_cache = []
        self._friend_msg_cache = []
        if self._record_type == vru.VIDEO_TYPE_BATTLE:
            ui = global_data.ui_mgr.get_ui('EndHighlightUI')
            if not ui and not global_data.is_inner_server:
                self.reset_all(True)
            self._stop_record()