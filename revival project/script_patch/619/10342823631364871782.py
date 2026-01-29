# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CamTrkComponent.py
from __future__ import absolute_import
import six
import cython
import world
import time
from common.cfg import confmgr
import math3d
TO_FIRST = 1
TO_LAST = 2
NO_ACTION = 0
NO_ADD = 0
CAN_ADD = 1
RESTART_ADD = 2
from .ICamTrkComponent import ICamTrkComponent

class CamTrkComponent(ICamTrkComponent):

    def __init__(self):
        self._start_trk_id = 0
        self._showing_trk_type = {}
        self._trk_list = []
        self._track_timer_id = None
        self.process_event(True)
        self._is_last_end = False
        self.init_debug_event()
        self.is_in_plot = False
        self._start_time_list = {}
        self._has_screen_lock = False
        self._cur_trans = None
        return

    def get_animation_tag_trk(self, animation_tag):
        res_trk_players = []
        for trk_player in self._trk_list:
            custom_data = trk_player.get_player_custom_data()
            tag = custom_data.get('tag', '')
            if animation_tag == tag:
                res_trk_players.append(trk_player)

        return res_trk_players

    def restart_animation_tag_trk(self, animation_tag):
        restart_list = []
        cur_this_tag_players = self.get_animation_tag_trk(animation_tag)
        if cur_this_tag_players:
            for p in cur_this_tag_players:
                if not p.is_finish():
                    p.restart()
                    restart_list.append(p)

        return restart_list

    def play_preset_trk_animation(self, animation_tag, callback, animation_data=None):
        trk_conf = self.get_trk_data(animation_tag, animation_data)
        if not trk_conf:
            return
        self.play_trk_by_conf(animation_tag, trk_conf, callback)

    def play_trk_by_conf(self, animation_tag, trk_conf, callback):
        add_type = trk_conf.get('add_type', 0)
        trk_type = trk_conf.get('trk_type', '')
        trk_path = trk_conf.get('trk_path', '')
        trk_instance = trk_conf.get('trk_instance', None)
        is_left_hand = True if trk_instance else False
        is_lock_screen = True if trk_conf.get('is_lock_screen', 0) else False
        is_plot = True if trk_conf.get('is_plot', 0) else False
        if trk_conf.get('forbid_follow', 0):
            is_forbid_follow = True if 1 else False
            loop_count = trk_conf.get('loop_count', 0)
            min_play_interval = trk_conf.get('min_play_interval', None)
            start_smooth_time, end_smooth_time = trk_conf.get('smooth_times', [0, 0])
            is_additive = trk_conf.get('not_additive', False) or True if 1 else False
            start_pause_time = trk_conf.get('start_pause_time', 0)
            joint_time = trk_conf.get('join_time', 0)
            end_add_trk_conf = trk_conf.get('end_add_trk', {})
            disable_unrecover_smooth = trk_conf.get('disable_unrecover_smooth', 0)
            time_scale = trk_conf.get('time_scale', 1.0)
            trk_path or trk_instance or log_error('Try to play an empty cam trk %s' % animation_tag)
            return
        else:
            if self.check_trk_can_play(animation_tag, add_type, trk_type, min_play_interval):
                if global_data.show_trk_debug_info:
                    global_data.game_mgr.show_tip(animation_tag)
                if add_type == RESTART_ADD:
                    if self.restart_animation_tag_trk(animation_tag):
                        return

                def _end_callback(trk_pl, is_finish, trk_type=trk_type, animation_tag=animation_tag, is_plot=is_plot):
                    if trk_type in self._showing_trk_type:
                        if animation_tag in self._showing_trk_type[trk_type]:
                            self._showing_trk_type[trk_type].remove(animation_tag)
                    self.on_trk_cancel_or_finish(trk_pl, animation_tag)
                    if callback:
                        callback()

                if not is_plot:
                    trk_player = self.play_track(trk_path or trk_instance, _end_callback, time_scale=time_scale, is_additive=is_additive, is_left_hand=is_left_hand)
                else:
                    self.clear_all_track()
                    self.is_in_plot = True
                    trk_player = self.play_plot(trk_path or trk_instance, _end_callback, is_additive=False)
                    trk_player._is_additive_fov = False
                self._showing_trk_type.setdefault(trk_type, [])
                self._showing_trk_type[trk_type].append(animation_tag)
                trk_player.set_player_custom_data({'tag': animation_tag,'type': trk_type,'is_plot': is_plot})
                trk_player.set_player_scale(trk_conf.get('offset_mul', 1.0), trk_conf.get('rot_mul', 1.0))
                trk_player.set_add_rot(trk_conf.get('add_rot', 0))
                if not disable_unrecover_smooth:
                    final_trans = trk_player.get_trk_final_trans(False)
                    rot = final_trans.rotation.yaw + final_trans.rotation.pitch + final_trans.rotation.roll
                    if final_trans.translation.length > 0.1 or abs(rot) > 0.001:
                        end_smooth_time = max(end_smooth_time, 0.033)
                trk_player.set_smooth_time(max(start_smooth_time, start_pause_time), end_smooth_time)
                if loop_count:
                    trk_player.set_loop_time(loop_count)
                self._trk_list.append(trk_player)
                self._start_time_list[animation_tag] = time.time()
                if is_forbid_follow:
                    global_data.emgr.camera_enable_follow_event.emit(False)
                if is_lock_screen:
                    self._has_screen_lock = True
                    global_data.emgr.screen_locker_event.emit(True, trk_player.get_trk_duration_time())
                if end_add_trk_conf:
                    if not trk_player.has_start():
                        trk_player.on_start()
                    self.parse_additional_trk_conf(trk_player, end_add_trk_conf)
                global_data.emgr.camera_play_added_trk_start.emit(animation_tag)
                if joint_time > 0.01 and self._cur_trans is not None:
                    smooth_trk = self._generate_smooth_track(self._cur_trans, trk_player.get_trk_first_trans(), joint_time)
                    if smooth_trk:
                        trk_player = self.play_track(smooth_trk, None, is_additive=False, is_left_hand=True)
                        trk_player.set_player_custom_data({'tag': '_join'})
                        self._trk_list.append(trk_player)
            return

    def cancel_trk_animation(self, animation_tag, run_callback=False, cancel_failed_cb=None):
        for trk_type, tag_list in six.iteritems(self._showing_trk_type):
            while animation_tag in tag_list:
                tag_list.remove(animation_tag)

        need_remove_list = []
        for trk_player in self._trk_list:
            custom_data = trk_player.get_player_custom_data()
            tag = custom_data.get('tag', '')
            if animation_tag == tag:
                need_remove_list.append(trk_player)

        total_trans = math3d.matrix()
        for trk_player in need_remove_list:
            self._trk_list.remove(trk_player)
            if run_callback:
                trk_player.run_callback(is_finish=False)
            trk_trans, _ = trk_player.get_track(trk_player._cnt_track_time)
            if trk_trans:
                total_trans *= trk_trans

        if not need_remove_list:
            if callable(cancel_failed_cb):
                cancel_failed_cb(animation_tag, run_callback)
            return
        else:
            self.on_trk_cancel_or_finish(None, animation_tag)
            if self.is_in_plot:
                log_error('plot is not support cancel!!!!')
                import traceback
                traceback.print_stack()
                return
            trk_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(animation_tag), None)
            if not trk_conf:
                return
            cancel_act = trk_conf.get('cancel_act', TO_FIRST)
            if cancel_act == NO_ACTION:
                if len(need_remove_list) > 0 and len(self._trk_list) == 0:
                    self._is_last_end = True
                    return
            else:
                cancel_smooth_time = trk_conf.get('cancel_smooth_time', 0)
                if not cancel_smooth_time:
                    return
            smooth_trk = None
            if cancel_act == TO_LAST:
                if len(need_remove_list) == 1:
                    trk_player = need_remove_list[0]
                    smooth_trk = self._generate_smooth_track(total_trans, trk_player.get_trk_final_trans(False), cancel_smooth_time)
                else:
                    smooth_trk = self._generate_smooth_track(total_trans, math3d.matrix(), cancel_smooth_time)
            elif cancel_act == TO_FIRST:
                smooth_trk = self._generate_smooth_track(total_trans, math3d.matrix(), cancel_smooth_time)
            if smooth_trk:
                trk_player = self.play_track(smooth_trk, None, is_additive=False, is_left_hand=True)
                trk_player.set_player_custom_data({'tag': '_cancel'})
                self._trk_list.append(trk_player)
            return

    def play_outer_track(self, tag, callback, custom_data):
        if 'trk_instance' in custom_data:
            self.play_trk_by_conf(tag, custom_data, callback)
        else:
            log_error('play_outer_track failed ,can not find key trk_instance in custom data')

    def check_trk_can_play(self, animation_tag, add_type, trk_type, min_play_interval):
        if self.is_in_plot:
            return False
        else:
            if trk_type in self._showing_trk_type and self._showing_trk_type[trk_type]:
                type_trks = self._showing_trk_type[trk_type]
                if animation_tag in type_trks and len(set(type_trks)) == 1 and add_type == CAN_ADD:
                    if min_play_interval and animation_tag in self._start_time_list:
                        if self._start_time_list[animation_tag] + min_play_interval > time.time():
                            return False
                    return True
                if add_type == RESTART_ADD:
                    return True
                return False
            return True

    def play_track(self, track_file_path, callback, revert=False, time_scale=1.0, is_additive=True, is_left_hand=False):
        from .CameraTrkPlayer import CameraTrkPlayer
        trk_player = CameraTrkPlayer()
        trk_player.play_track(track_file_path, callback, revert, time_scale, is_additive, is_left_hand)
        return trk_player

    def play_plot(self, track_file_path, callback, revert=False, time_scale=1.0, is_additive=False):
        from .CameraTrkPlayer import CamPlotPlayer
        trk_player = CamPlotPlayer()
        trk_player.play_track(track_file_path, callback, revert, time_scale, is_additive)
        return trk_player

    def on_track_update(self):
        finish_trks = []
        trans_list = []
        fov_list = []
        for trk_player in self._trk_list:
            if not trk_player.has_start():
                trk_player.on_start()
            if not trk_player.is_finish():
                trk_trans, fov = trk_player.on_track_update()
                if not trk_trans:
                    continue
                trans_list.append(trk_trans)
                fov_list.append(fov)
            if trk_player.is_finish():
                finish_trks.append(trk_player)

        if trans_list:
            if len(trans_list) > 1:
                rot = math3d.matrix()
                translation = math3d.vector(0, 0, 0)
                for tran in trans_list:
                    rot = rot * tran.rotation
                    translation = translation + tran.translation

                res = math3d.matrix()
                res.do_rotation(rot)
                res.do_translate(translation)
            else:
                res = trans_list[0]
            if fov_list:
                fov_sum = sum([ x for x in fov_list if x is not None ])
            else:
                fov_sum = None
            global_data.emgr.camera_additional_transformation_event.emit(res, fov_sum, self.is_in_plot)
            self._cur_trans = res
        for f_trk in finish_trks:
            f_trk.on_finish()
            if f_trk in self._trk_list:
                self._trk_list.remove(f_trk)

        if self._is_last_end and len(self._trk_list) == 0:
            global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, False)
            global_data.emgr.camera_additional_transformation_end_event.emit()
            self._cur_trans = None
            global_data.emgr.camera_all_trk_play_end.emit()
            self._showing_trk_type = {}
            self._trk_list = []
            self._is_last_end = False
            self.is_in_plot = False
        if len(finish_trks) > 0 and len(self._trk_list) <= 0:
            self._is_last_end = True
        return

    def get_playing_trk_info_list(self):
        trk_info_list = []
        for trk_player in self._trk_list:
            custom_data = trk_player.is_finish() or trk_player.get_player_custom_data()
            tag = custom_data.get('tag', '')
            if trk_player._track_file:
                name = str(trk_player._track_file) if 1 else None
                trk_info_list.append([tag, name])

        return trk_info_list

    def unregister_timer(self):
        if self._track_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._track_timer_id)
            self._track_timer_id = None
        return

    def destroy(self):
        self.unregister_timer()
        self.process_event(False)
        self._start_trk_id = 0
        self._showing_trk_type = {}
        self._trk_list = []

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_infos = {'net_login_reconnect_event': self.on_login_reconnect,
           'net_reconnect_event': self.on_reconnect
           }
        if is_bind:
            emgr.bind_events(event_infos)
        else:
            emgr.unbind_events(event_infos)

    def on_login_reconnect(self, *args):
        self.clear_all_track()

    def on_reconnect(self, *args):
        self.clear_all_track()

    def clear_all_track(self):
        self._showing_trk_type = {}
        self._trk_list = []
        self.is_in_plot = False
        self._is_last_end = False

    def play_preset_trk_animation_simple(self, trk_path, offset_scale, rot_scale, is_lock_screen):
        if not trk_path:
            log_error('Try to play an empty cam trk %s' % trk_path)
            return

        def callback(*args):
            if len(self._trk_list) <= 1:
                global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0)
                global_data.emgr.slerp_into_setupped_camera_event.emit(0.1)

        if not is_lock_screen:
            trk_player = self.play_track(trk_path, callback, is_additive=True)
        else:
            trk_player = self.play_plot(trk_path, callback, is_additive=True)
        trk_player.set_player_scale(offset_scale, rot_scale)
        self._trk_list.append(trk_player)
        trk_player.on_start()

    def init_debug_event(self):
        global_data.emgr.play_preset_trk_animation_simple_event += self.play_preset_trk_animation_simple

    def _generate_smooth_track(self, start_trans, end_trans, duration):
        duration = round(duration * 1000.0 / 33.33333333) * 33.333333333
        from logic.gutils.CameraHelper import track_build
        track = track_build([(0, start_trans), (duration, end_trans)], duration)
        return track

    def on_trk_cancel_or_finish(self, tar_trk_player, trk_tag):
        trk_confs = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content')
        lock_screen_count = 0
        forbid_follow_count = 0
        is_plot = False
        for trk_player in self._trk_list:
            if trk_player != tar_trk_player:
                custom_data = trk_player.get_player_custom_data()
                tag = custom_data.get('tag', '')
                is_plot = is_plot or custom_data.get('is_plot', False)
                trk_conf = trk_confs.get(str(tag), None)
                if trk_conf:
                    lock_screen_count += trk_conf.get('is_lock_screen', 0)
                    forbid_follow_count += trk_conf.get('forbid_follow', 0)

        if forbid_follow_count <= 0.5:
            global_data.emgr.camera_enable_follow_event.emit(True)
        if lock_screen_count <= 0.5 and self._has_screen_lock:
            global_data.emgr.screen_locker_event.emit(False, None)
            self._has_screen_lock = False
        if not is_plot:
            self.is_in_plot = False
        return

    def is_playing_trk(self):
        return len(self._trk_list) > 0

    def get_default_trk_data(self):
        conf = {'bSupSelfAdded': 0,
           'trk_type': -1000,
           'is_lock_screen': False,
           'is_plot': False,
           'is_forbid_follow': False,
           'loop_count': 0,
           'min_play_interval': None,
           'start_smooth_time': 0,
           'end_smooth_time': 0
           }
        return conf

    def get_trk_data(self, animation_tag, animation_data=None):
        if animation_tag.endswith('.trk'):
            if animation_data:
                trk_conf = animation_data
            else:
                trk_conf = self.get_default_trk_data()
            trk_conf['trk_path'] = animation_tag
        else:
            trk_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(animation_tag), None)
            if not trk_conf:
                log_error("Can't find cam trk %s" % animation_tag)
                return
        if animation_data:
            trk_conf = dict(trk_conf)
            trk_conf.update(animation_data)
        return trk_conf

    def parse_additional_trk_conf(self, trk_player, add_trk_conf):
        trk_start_time = add_trk_conf.get('trk_start_time', None)
        trk_real_end_time = add_trk_conf.get('trk_real_end_time', 0)
        is_to_target = add_trk_conf.get('is_to_target', True)
        if trk_start_time is None:
            return
        else:
            if trk_real_end_time:
                trk_end_time = min(trk_real_end_time - trk_player.get_trk_start_smooth_time(), trk_player.get_trk_duration_time())
                tran = trk_player.get_trk_transformation(trk_end_time * 1000)
            else:
                tran = trk_player.get_trk_final_trans()
            end_matrix = add_trk_conf.get('end_mat', math3d.matrix())
            if is_to_target:
                tran_rot = tran.rotation
                tran_rot.inverse()
                added_rot = end_matrix.rotation * tran_rot
                changged_matrix = math3d.matrix()
                changged_matrix.do_rotation(added_rot)
                changged_matrix.do_translate(end_matrix.translation - tran.translation)
            else:
                changged_matrix = end_matrix
            duration = add_trk_conf.get('duration', 0)
            if duration > 0 and tran:
                trk_player.add_trk_addition_trans(trk_start_time, math3d.matrix(), changged_matrix, duration + trk_start_time)
            return

    def out_pos(self, pos):
        if pos:
            return '<%.2f, %.2f, %.2f>' % (pos.x, pos.y, pos.z)
        else:
            return str(None)