# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/ArtCollectionAnimation.py
from __future__ import absolute_import
from six.moves import range
import common.utils.timer as timer
import math
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
import cc
import math3d
import world
import time
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, ART_COLLECT_SINGLE_SHOW_INDEX
from common.framework import Functor
from logic.client.const import lobby_model_display_const
SINGLE_SHOW_INDEX = ART_COLLECT_SINGLE_SHOW_INDEX
CLOSE_IDLE_ANIM_NAME = 'idle'
OPEN_ANIM_NAME = 'oped'
OPEN_IDLE_ANIM_NAME = 'oped_idle'
LOOP_WAIT_ANIM_NAME = 'xunhuan'
TRK_ACTION_TAG = 1000
ANIMATION_FOV = 45

class ArtCollectionAnimation(object):
    LOTTERY_TYPE_ONE = SINGLE_LOTTERY_COUNT
    LOTTERY_TYPE_TEN = CONTINUAL_LOTTERY_COUNT

    def __init__(self, panel):
        self.panel = panel
        self.is_bind = False
        self._lottery_type = self.LOTTERY_TYPE_ONE
        self._stage_model = None
        self._trk_player = None
        self._is_opened = False
        self._is_get_lottery_result = False
        self._last_camera_state = None
        self.init_event()
        return

    def init_event(self):
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.clear_model()
        self.end_trk()

    def clear_model(self):
        self._stage_model = None
        return

    def set_lottery_type(self, lottery_type):
        self._lottery_type = lottery_type

    def process_event(self, is_bind):
        if is_bind == self.is_bind:
            return
        emgr = global_data.emgr
        econf = {'player_art_collection_one_event': self._on_art_collection_one,
           'reset_art_collection_scene_event': self.reset_to_default
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self.is_bind = is_bind

    def on_load_scene(self, *args):
        scene = world.get_active_scene()
        self._stage_model = scene.get_model('niudan_tai_7')
        self.on_model_load_complete(self._stage_model)

    def reset_to_default(self, is_default=True):
        self._stage_model.play_animation(CLOSE_IDLE_ANIM_NAME)
        global_data.emgr.set_lobby_scene_display_type.emit(lobby_model_display_const.ART_COLLECTION)
        global_data.emgr.lobby_set_models_visible_event.emit(True)
        active_scene = world.get_active_scene()
        if not active_scene:
            return
        camera = active_scene.active_camera
        if not camera:
            return
        if not is_default and self._last_camera_state:
            position = self._last_camera_state.get('position', camera.world_position)
            rotation = self._last_camera_state.get('rotation', camera.rotation_matrix)
            global_data.emgr.change_model_display_scene_cam_trans.emit(position, rotation)
            fov = self._last_camera_state.get('fov', 45)
            camera.fov = fov

    def hidel_all_ball(self):
        if not self._stage_model:
            log_error('[warning] test--hidel_all_ball--_stage_model = None')
            return
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            log_error('[warning] test--hidel_all_ball--hang_ball_model = None')
            return
        for index in range(10):
            bind_point = 'niudan_' + str(index + 1)
            ball_model = hang_ball_model.get_socket_obj(bind_point, 0)
            if not ball_model:
                continue
            ball_model.visible = False

    def show_all_ball(self):
        if not self._stage_model:
            log_error('[warning] test--show_all_ball--_stage_model = None')
            return
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            log_error('[warning] test--show_all_ball--hang_ball_model = None')
            return
        for index in range(10):
            bind_point = 'niudan_' + str(index + 1)
            ball_model = hang_ball_model.get_socket_obj(bind_point, 0)
            if not ball_model:
                continue
            ball_model.visible = True

    def decide_show_ball(self, model, lottery_type):
        if lottery_type == self.LOTTERY_TYPE_ONE:
            for index in range(10):
                bind_point = 'niudan_' + str(index + 1)
                ball_model = model.get_socket_obj(bind_point, 0)
                if not ball_model:
                    continue
                ball_model.visible = index == SINGLE_SHOW_INDEX

        else:
            self.show_all_ball()

    def on_model_load_complete(self, model, *args):
        if not model:
            return
        if not self.panel.isVisible():
            return
        self._stage_model = model
        self.hidel_all_ball()

    def end_trk(self):
        self.panel.stopActionByTag(TRK_ACTION_TAG)
        self._trk_player = None
        return

    def on_track_update(self):
        transform, fov = self._trk_player.on_track_update()
        active_scene = world.get_active_scene()
        camera = active_scene.active_camera
        rotation = camera.rotation_matrix
        global_data.emgr.change_model_display_scene_cam_trans.emit(transform.translation, rotation, False)

    def end_lottery_anim(self, *args):
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            return
        anim_name = self.get_lottery_anim_name()
        hang_ball_model.unregister_event(self.end_lottery_anim, 'end', anim_name)
        global_data.emgr.art_collect_animation_end_event.emit()
        active_scene = world.get_active_scene()
        camera = active_scene.active_camera
        self._last_camera_state = {'fov': camera.fov,'rotation': camera.rotation_matrix,'position': camera.world_position}

    def get_lottery_anim_name(self):
        anim_name = None
        if self._lottery_type == self.LOTTERY_TYPE_TEN:
            anim_name = 'shilianchou'
        else:
            anim_name = 'danchou'
        return anim_name

    def play_success_lottery_anim(self):
        self._is_get_lottery_result = True
        if not self._is_opened:
            return
        self.show_all_ball()
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            return
        anim_name = self.get_lottery_anim_name()
        hang_ball_model.play_animation(anim_name)
        hang_ball_model.register_anim_key_event(anim_name, 'end', self.end_lottery_anim)
        self.start_trk_camera_move()

    def get_lottery_trk(self):
        if self._lottery_type == self.LOTTERY_TYPE_TEN:
            return 'model_new/niudan/xin/camera/shilianchou.trk'
        else:
            return 'model_new/niudan/xin/camera/danchou.trk'

    def end_open_anim(self, *args):
        self._is_opened = True
        self._stage_model.unregister_event(self.end_open_anim, 'end', OPEN_ANIM_NAME)
        if self._is_get_lottery_result:
            self.play_success_lottery_anim()
            return
        if not self._stage_model:
            return
        active_scene = world.get_active_scene()
        camera = active_scene.active_camera
        if not camera:
            return
        self._stage_model.play_animation(OPEN_IDLE_ANIM_NAME)
        hang_ball_model = self._stage_model.get_socket_obj('zhongxin', 0)
        if not hang_ball_model:
            return
        self.decide_show_ball(hang_ball_model, self._lottery_type)
        hang_ball_model.play_animation(LOOP_WAIT_ANIM_NAME)

    def start_trk_camera_move(self):
        track_path = self.get_lottery_trk()
        self._trk_player = CameraTrkPlayer()
        self._trk_player.play_track(track_path, None, is_additive=False, is_left_hand=True, finish_callback=self.end_trk)
        self._trk_player.on_start()
        action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([cc.CallFunc.create(self.on_track_update)])))
        action.setTag(TRK_ACTION_TAG)
        return

    def begin_play_lottery_anim(self, *args):
        if not self._stage_model or not self.panel.isVisible():
            return
        self._stage_model.play_animation(OPEN_ANIM_NAME)
        self._stage_model.register_anim_key_event(OPEN_ANIM_NAME, 'end', self.end_open_anim)

    def get_camera_name(self):
        if self._lottery_type == self.LOTTERY_TYPE_ONE:
            return 'camera_gaojichoujiang_01'
        else:
            return 'camera_gaojichoujiang_03'

    def _on_art_collection_one(self, lottery_type, *args):
        if not self._stage_model:
            return
        ui = global_data.ui_mgr.get_ui('LotteryMainUI')
        if ui:
            ui.hide()
        global_data.sound_mgr.play_ui_sound('ui_lottery_ten_balls')
        global_data.emgr.lobby_set_models_visible_event.emit(False)
        self.set_lottery_type(lottery_type)
        camera_name = self.get_camera_name()
        global_data.emgr.change_model_display_scene_cam.emit(camera_name, False)
        self._is_opened = False
        self._is_get_lottery_result = False
        delay_time = 1.0 / 33.0 * 10.0
        global_data.game_mgr.register_logic_timer(self.begin_play_lottery_anim, delay_time, times=1, mode=timer.CLOCK)
        active_scene = world.get_active_scene()
        camera = active_scene.active_camera
        fov = 30
        if camera:
            fov = camera.fov
        interval = 1.0 / 33.0
        fov_change_speed = (ANIMATION_FOV - fov) / delay_time
        func = Functor(self.update_fov_tick, time.time(), fov, fov_change_speed, delay_time)
        global_data.game_mgr.register_logic_timer(func, interval, times=-1, mode=timer.CLOCK)

    def update_fov_tick(self, start_time, start_fov, fov_change_speed, total_duration):
        active_scene = world.get_active_scene()
        if not active_scene:
            return timer.RELEASE
        camera = active_scene.active_camera
        if not camera:
            return timer.RELEASE
        cur_time = time.time()
        pass_time = cur_time - start_time
        if pass_time >= total_duration:
            fov_change_value = total_duration * fov_change_speed
            fov = start_fov + fov_change_value
            camera.fov = fov
            return timer.RELEASE
        fov_change_value = pass_time * fov_change_speed
        fov = start_fov + fov_change_value
        camera.fov = fov

    def do_show_panel(self):
        pass

    def do_hide_panel(self):
        self.end_trk()