# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMVMgr.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import math3d
import time
import cclive
import render
import game3d
import os
import C_file
from random import randint
from common.daemon_thread import DaemonThreadPool
import world
from logic.gutils.screen_effect_utils import SCREEN_EFFECT_SCALE
from logic.gcommon import time_utility
import common.utils.timer as timer
from common.framework import Functor
import world
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
_HASH_u_AnimationTime = game3d.calc_string_hash('u_AnimationTime')
_HASH_SamplerColorAnimationMap = game3d.calc_string_hash('SamplerColorAnimationMap')
_HASH_Overall_Brightness = game3d.calc_string_hash('Overall_Brightness')
s_mv_model = 'model_new\\scene\\aijiangwutai\\item_ajld_pm_a01.gim'
s_mv_wait_pic = 'model_new\\scene\\aijiangwutai\\textures\\aj_wait.png'
s_mv_end_pic = 'model_new\\scene\\aijiangwutai\\textures\\aj_end_bg.png'
s_spotlight_path = 'model_new\\scene\\aijiangwutai\\item_ajld_lights87.gim'
s_spotlight_info = [
 (
  (852.7, 811.09, 1969.08), 43.5, (1.0, 1.0, 1.0)),
 (
  (851.17, 811.09, 1969.31), 223.5, (1.0, 1.0, -1.0))]
s_sfx_info = {'left_right': (
                (
                 (734.5, 888.64, 2483.1), 191.3, (0.85, 0.87, 0.85)),
                (
                 (1372.3, 888.64, 1880.43), 255.4, (0.85, 0.87, 0.85))),
   'mid': (
         (897.57, 861.66, 2013.45), 0.0, (1.0, 1.0, 1.0)),
   'light': (
           (898.55, 806.7, 2009.6), 133.0, (1.0, 1.0, 1.0))
   }
s_tv_info = [
 (
  (1073.88, 811, 2203.88), 43.35, (1.0, 1.0, 1.0))]
s_aj_pos = (
 (830, 834, 1945), 235.0, (2.0, 2.0, 2.0))
s_mp4_path = 'video/aj/partmv1.mp4'
s_part_inf = [
 (0, ''),
 (
  1800, s_mp4_path),
 (3093, '')]
s_mp4_run_part_index = 1
s_ajld_lights_animations = [
 (0, 'item_ajld_lights87_down', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_01.tga'),
 (1, 'item_ajld_lights87_down', ''),
 (1824, 'item_ajld_lights87_futurebase', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_01.tga'),
 (2007, 'item_ajld_lights87_down', ''),
 (2050, 'item_ajld_lights87_skyhigh', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_02.tga'),
 (2278, 'item_ajld_lights87_down', ''),
 (2359, 'item_ajld_lights87_hereforyou', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_03.tga'),
 (2587, 'item_ajld_lights87_down', ''),
 (2597, 'item_ajld_lights87_awakening', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_04.tga'),
 (2814, 'item_ajld_lights87_down', ''),
 (2875, 'item_ajld_lights87_aiaiai', 'model_new\\scene\\aijiangwutai\\textures\\music_pic\\cat_05.tga'),
 (3067, 'item_ajld_lights87_down', '')]
s_left_right_sfxs = [
 (0, ''),
 (1824, 'effect/fx/scenes/common/music/wutai_future_dzp_01.sfx'),
 (2007, 'effect/fx/scenes/common/music/wutai_qieping_dzp_01.sfx'),
 (2051, 'effect/fx/scenes/common/music/wutai_sky_dzp_01.sfx'),
 (2278, 'effect/fx/scenes/common/music/wutai_qieping_dzp_01.sfx'),
 (2359, 'effect/fx/scenes/common/music/wutai_hereforyou_dzp_01.sfx'),
 (2587, 'effect/fx/scenes/common/music/wutai_qieping_dzp_01.sfx'),
 (2596, 'effect/fx/scenes/common/music/wutai_awakening_dzp_01.sfx'),
 (2814, 'effect/fx/scenes/common/music/wutai_qieping_dzp_01.sfx'),
 (2875, 'effect/fx/scenes/common/music/wutai_ai_dzp_01.sfx'),
 (2968, 'effect/fx/scenes/common/music/wutai_ai_dzp_02.sfx'),
 (2997, 'effect/fx/scenes/common/music/wutai_ai_dzp_01.sfx'),
 (3013, 'effect/fx/scenes/common/music/wutai_ai_dzp_02.sfx'),
 (3043, 'effect/fx/scenes/common/music/wutai_ai_dzp_01.sfx'),
 (3067, 'effect/fx/scenes/common/music/wutai_qieping_dzp_01.sfx'),
 (3093, '')]
s_mid_sfxs = [
 (0, ''),
 (1824, 'effect/fx/scenes/common/music/fenwei_1_tuowei.sfx'),
 (2007, ''),
 (2050, 'effect/fx/scenes/common/music/fenwei_2_qipao.sfx'),
 (2278, ''),
 (2359, 'effect/fx/scenes/common/music/fenwei_hereforyou_lizi.sfx'),
 (2587, ''),
 (2596, 'effect/fx/scenes/common/music/fenwei_3_huangyouyou.sfx'),
 (2814, ''),
 (2875, 'effect/fx/scenes/common/music/fenwei_4_lizi_01.sfx'),
 (3067, '')]
s_light_sfxs = [
 (0, ''),
 (1800, 'effect/fx/scenes/common/music/music_light_01_2.sfx'),
 (1813, ''),
 (2007, 'effect/fx/scenes/common/music/kaichang_aijiang_dengtiaodingzhu.sfx'),
 (2050, ''),
 (2278, 'effect/fx/scenes/common/music/kaichang_aijiang_dengtiaodingzhu.sfx'),
 (2359, ''),
 (2587, 'effect/fx/scenes/common/music/kaichang_aijiang_dengtiaodingzhu.sfx'),
 (2596, ''),
 (2814, 'effect/fx/scenes/common/music/kaichang_aijiang_dengtiaodingzhu.sfx'),
 (2875, ''),
 (3067, 'effect/fx/scenes/common/music/kaichang_aijiang_dengtiaodingzhu.sfx')]
s_screen_sfxs = [
 (0, ''),
 (1824, 'effect/fx/scenes/common/music/fenwei_1_pm.sfx'),
 (2007, ''),
 (2050, 'effect/fx/scenes/common/music/fenwei_2_qipao_pm.sfx'),
 (2278, ''),
 (2359, ''),
 (2587, ''),
 (2596, 'effect/fx/scenes/common/music/fenwei_3_jingtou.sfx'),
 (2814, ''),
 (2875, 'effect/fx/scenes/common/music/fenwei_4_lizi_02.sfx'),
 (3067, ''),
 (3094, 'res/effect/fx/scenes/common/music/kaichang_renwu_lichang_pingmu.sfx')]
s_exec_func = [
 (0, ''),
 (
  1800, 'shut_light', ()),
 (
  1823.5, 'play_change_sfx', ('effect/fx/scenes/common/music/kaichang_renwu_chuchang_1.sfx', )),
 (
  1824, 'open_light', ()),
 (
  1824.1, 'change_human_model', ('2002', 'part1_01')),
 (
  2058.6, 'change_human_model', ('2002', 'part1_02')),
 (
  2358.1, 'play_change_sfx', ('effect/fx/scenes/common/music/kaichang_renwu_qiehuan.sfx', )),
 (
  2359.7, 'change_human_model', ('2001', 'part2')),
 (
  2586.1, 'play_change_sfx', ('effect/fx/scenes/common/music/kaichang_renwu_qiehuan.sfx', )),
 (
  2588.9, 'change_human_model', ('2000_skin_a1', 'part3')),
 (
  2829.8, 'play_change_sfx', ('effect/fx/scenes/common/music/kaichang_renwu_qiehuan.sfx', )),
 (
  2833.2, 'change_human_model', ('2002', 'part4')),
 (
  3091, 'play_change_sfx', ('effect/fx/scenes/common/music/kaichang_renwu_lichang.sfx', )),
 (
  3092, 'change_human_model', ('', '')),
 (
  3092, 'change_mv_wait_pic', ())]
s_cc_sound_volume_scale = 2.5

class PartMVMgr(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartMVMgr, self).__init__(scene, name, need_update=True)
        self.render_tex = None
        self.cclive_player = cclive.player()
        self.mv_model = None
        self.mv_wait_model = None
        self.is_mv_ready = False
        self.is_bind_mv_model = False
        self.disable_collision_delay_exec = None
        self.video_name = ''
        self.hashed_video_path = ''
        self.spot_light_models = []
        self.concert_start_ts = global_data.battle.get_concert_start_ts()
        if self.concert_start_ts > 0:
            self.all_time = time_utility.get_server_time() - self.concert_start_ts
        else:
            self.all_time = 0
        self.animation_all_time = 0
        self.part_index = 0
        self.part_time = 0
        self.animation_index = 1
        self.animation_time = 0
        self.left_right_sfx_ids = []
        self.left_right_sfx_index = 1
        self.mid_sfx_id = None
        self.mid_sfx_index = 1
        self.screen_sfx_id = None
        self.screen_sfx_index = 1
        self.light_sfx_id = None
        self.light_sfx_index = 1
        self.exec_func_index = 0
        self.is_need_seek_to = False
        self.seek_to_downcount = 0
        self.cur_mv_path = None
        self.mv_start_time = 0.0
        self.shut_light_timer = None
        self.save_cc_sound_volume = 0.0
        self.is_light_down = True
        self.human_model = None
        self.human_model_id = None
        self.human_anim_name = None
        self.human_anim_start_time = 0.0
        self.cur_rold_id = None
        self.check_progress_downcount = 0
        self.max_check_progress_count = 0
        self.is_check_progress = False
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            self.seek_scale = 1000000.0
        else:
            self.seek_scale = 1000.0
        self.last_time = global_data.game_time
        global_data.emgr.update_battle_stage += self.on_update_battle_stage
        global_data.emgr.cc_sound_volume_change += self.on_sound_volume_change
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
        pass

    def video_ready_callback(self, *args):
        self.is_mv_ready = True
        self.bind_mv_model_tex()
        self.is_need_seek_to = True
        self.seek_to_downcount = 20

    def bind_mv_model_tex(self):
        if not self.is_bind_mv_model and self.is_mv_ready and self.mv_model and self.mv_model.valid:
            provider = self.cclive_player.fetch_data_provider()
            if provider:
                self.render_tex = render.texture('cclive', data_provider=provider)
                self.mv_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', self.render_tex)
                self.is_bind_mv_model = True

    def video_complete_callback(self, *args):
        pass

    def on_update_battle_stage(self, *args):
        if self.concert_start_ts != global_data.battle.get_concert_start_ts():
            self.concert_start_ts = global_data.battle.get_concert_start_ts()
            self.all_time = time_utility.get_server_time() - self.concert_start_ts
            self.reset_music()

    def force_reset(self):
        from logic.gcommon.common_const import battle_const
        if global_data.battle.concert_stage == battle_const.CONCERT_SING_STAGE:
            from logic.gutils.concert_utils import get_song_len, get_song_start_ts
            song_idx = global_data.battle.song_idx
            song_end_ts = global_data.battle.song_end_ts
            if song_idx is not None and song_idx != -1:
                _song_start_ts = song_end_ts - get_song_len(song_idx)
                song_pass_t = time_utility.get_server_time() - _song_start_ts
                self.all_time = get_song_start_ts(song_idx) + song_pass_t
                self.reset_music()
        else:
            self.concert_start_ts = global_data.battle.get_concert_start_ts()
            self.all_time = time_utility.get_server_time() - self.concert_start_ts
            self.reset_music()
        return

    def on_before_load(self):
        scn = self.scene()
        part_fog_and_light = scn.get_com('PartAutoFogAndLight')
        if part_fog_and_light:
            part_fog_and_light.load_custom_data('ajld_night_shut_light')

    def on_sound_volume_change(self, volume):
        self.save_cc_sound_volume = volume
        if not self.is_check_progress:
            self.cclive_player.set_volume(volume * s_cc_sound_volume_scale)

    def on_enter(self):
        global_data.sound_mgr.reset_volume()
        self.remove_played_video()
        self.reset_event()
        scn = self.scene()

        def create_cb(model):
            self.mv_model = model
            if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
                model.all_materials.set_technique(1, 'shader/g93shader/effect_g93_cclive.nfx::TShader')
            model.world_rotation_matrix = math3d.matrix.make_rotation_y(s_tv_info[0][1] / 180 * 3.14)
            self.bind_mv_model_tex()
            self.mv_model.visible = bool(self.part_index == s_mp4_run_part_index)

        global_data.model_mgr.create_model_in_scene(s_mv_model, math3d.vector(*s_tv_info[0][0]), on_create_func=create_cb)

        def create_cb_mv_wait(model):
            self.mv_wait_model = model
            model.world_rotation_matrix = math3d.matrix.make_rotation_y(s_tv_info[0][1] / 180 * 3.14)
            if self.part_index == len(s_part_inf) - 1:
                tex = render.texture(s_mv_end_pic)
            else:
                tex = render.texture(s_mv_wait_pic)
            model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex)
            self.mv_wait_model.visible = bool(self.part_index != s_mp4_run_part_index)

        global_data.model_mgr.create_model_in_scene(s_mv_model, math3d.vector(*s_tv_info[0][0]), on_create_func=create_cb_mv_wait)
        self.init_spotlight(scn)
        self.reset_music()

    def on_update(self, dt):
        cur_time = global_data.game_time
        cur_dt = cur_time - self.last_time
        self.last_time = cur_time
        self.all_time += cur_dt
        self.updata_part_mp4(cur_dt)
        self.updata_exec_func(cur_dt)
        self.updata_ajld_lights_animations(cur_dt)
        self.update_sfx(cur_dt)
        if self.part_index == s_mp4_run_part_index and self.cclive_player and self.is_mv_ready:
            self.check_progress_downcount -= cur_dt
            if self.check_progress_downcount <= 0:
                if self.is_check_progress:
                    self.check_progress_downcount = 1.0
                else:
                    self.check_progress_downcount = 5.0
                interval_time = self.cclive_player.current_position / self.seek_scale - self.part_time
                if abs(interval_time) < 5.0 and self.max_check_progress_count > 10:
                    if self.is_check_progress:
                        self.is_check_progress = False
                        self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)
                    return
                self.max_check_progress_count += 1
                if interval_time < -1.5 or interval_time > 5.0:
                    self.cclive_seek_to(self.part_time)
                elif interval_time > 1.5:
                    if self.cclive_player:
                        self.cclive_player.pause()

                        def callback():
                            if self.cclive_player and self.part_index == s_mp4_run_part_index:
                                self.cclive_player.resume()
                                if self.is_check_progress:
                                    self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)

                        global_data.game_mgr.register_logic_timer(callback, interval=interval_time, times=1, mode=timer.CLOCK)
                        self.check_progress_downcount = interval_time + 1.0
                elif self.is_check_progress:
                    self.is_check_progress = False
                    self.cclive_player.set_volume(self.save_cc_sound_volume * s_cc_sound_volume_scale)

    def get_sfx_create_callback(self, rotation, scale):

        def create_cb(sfx):
            sfx.world_rotation_matrix = math3d.matrix.make_rotation_y(rotation / 180 * 3.14)
            sfx.scale = scale

        return create_cb

    def update_sfx(self, dt):
        need_refresh_left_right_sfx, self.left_right_sfx_index, _ = self.updata_time(dt, self.left_right_sfx_index, 0, s_left_right_sfxs)
        if need_refresh_left_right_sfx:
            self.refresh_left_right_sfx()
        need_refresh_mid_sfx, self.mid_sfx_index, _ = self.updata_time(dt, self.mid_sfx_index, 0, s_mid_sfxs)
        if need_refresh_mid_sfx:
            self.refresh_mid_sfx()
        need_refresh_screen_sfx, self.screen_sfx_index, _ = self.updata_time(dt, self.screen_sfx_index, 0, s_screen_sfxs)
        if need_refresh_screen_sfx:
            self.refresh_screen_sfx()
        need_refresh_light_sfx, self.light_sfx_index, _ = self.updata_time(dt, self.light_sfx_index, 0, s_light_sfxs)
        if need_refresh_light_sfx:
            self.refresh_light_sfx()

    def refresh_light_sfx(self):
        if self.light_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.light_sfx_id)
            self.light_sfx_id = None
        sfx_path = s_light_sfxs[self.light_sfx_index][1]
        if sfx_path:
            pos = math3d.vector(*s_sfx_info['light'][0])
            scale = math3d.vector(*s_sfx_info['light'][2])
            create_cb = self.get_sfx_create_callback(s_sfx_info['light'][1], scale)
            self.light_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
        return

    def refresh_screen_sfx(self):
        if self.screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.screen_sfx_id)
            self.screen_sfx_id = None
        sfx_path = s_screen_sfxs[self.screen_sfx_index][1]
        if sfx_path:

            def callback(sfx):
                sfx.scale = SCREEN_EFFECT_SCALE

            self.screen_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=callback)
        return

    def refresh_mid_sfx(self):
        if self.mid_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.mid_sfx_id)
            self.mid_sfx_id = None
        sfx_path = s_mid_sfxs[self.mid_sfx_index][1]
        if sfx_path:
            pos = math3d.vector(*s_sfx_info['mid'][0])
            scale = math3d.vector(*s_sfx_info['mid'][2])
            create_cb = self.get_sfx_create_callback(s_sfx_info['mid'][1], scale)
            self.mid_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
        return

    def refresh_left_right_sfx(self):
        for sfx_id in self.left_right_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.left_right_sfx_ids = []
        sfx_path = s_left_right_sfxs[self.left_right_sfx_index][1]
        if sfx_path:
            for index, spotlight in enumerate(s_sfx_info['left_right']):
                pos = math3d.vector(*spotlight[0])
                scale = math3d.vector(*spotlight[2])
                create_cb = self.get_sfx_create_callback(spotlight[1], scale)
                size_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
                self.left_right_sfx_ids.append(size_sfx_id)

    def updata_ajld_lights_animations(self, dt):
        need_refresh, self.animation_index, self.animation_time = self.updata_time(dt, self.animation_index, self.animation_time, s_ajld_lights_animations)
        if need_refresh:
            self.refresh_lights_animation()
        else:
            animation_time = 600.0 if self.is_light_down else self.animation_time
            for spot_model in self.spot_light_models:
                spot_model.all_materials.set_var(_HASH_u_AnimationTime, 'u_AnimationTime', animation_time)

    def refresh_lights_animation(self):
        if self.animation_index < 0:
            return
        else:
            animation_name = s_ajld_lights_animations[self.animation_index][1]
            tex_path = s_ajld_lights_animations[self.animation_index][2]
            cat_texture = None
            if tex_path:
                cat_texture = render.texture(tex_path, False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
            for spot_model in self.spot_light_models:
                spot_model.play_animation(animation_name, -1.0, 0, self.animation_time * 1000.0, 1)
                if cat_texture:
                    self.is_light_down = False
                    spot_model.all_materials.set_texture(_HASH_SamplerColorAnimationMap, 'SamplerColorAnimationMap', cat_texture)
                else:
                    self.is_light_down = True

            return

    def updata_part_mp4(self, dt):
        need_refresh, self.part_index, self.part_time = self.updata_time(dt, self.part_index, self.part_time, s_part_inf)
        if need_refresh:
            self.refresh_mv()
            if self.mv_model:
                self.mv_model.visible = bool(self.part_index == s_mp4_run_part_index)
            if self.mv_wait_model:
                self.mv_wait_model.visible = bool(self.part_index != s_mp4_run_part_index)

    def updata_exec_func(self, dt):
        need_refresh, self.exec_func_index, _ = self.updata_time_exec_func(dt, self.exec_func_index, 0, s_exec_func)
        if need_refresh:
            self.refresh_exec_func()

    def updata_time_exec_func(self, dt, index, part_time, data_list):
        need_refresh = False
        part_time += dt
        all_time = self.all_time
        if self.part_index == s_mp4_run_part_index and self.cclive_player and self.is_mv_ready:
            cclive_all_time = self.cclive_player.current_position / self.seek_scale + 1800.0
            if abs(cclive_all_time - self.all_time) < 5.0:
                all_time = cclive_all_time
        self.animation_all_time = all_time
        if index + 1 < len(data_list) and all_time > data_list[index + 1][0]:
            part_time = all_time - data_list[index + 1][0]
            index += 1
            need_refresh = True
            if index >= len(data_list):
                index = 0
        return (need_refresh, index, part_time)

    def refresh_exec_func(self):
        func_name = s_exec_func[self.exec_func_index][1]
        if func_name:
            args = s_exec_func[self.exec_func_index][2]
            start_time = s_exec_func[self.exec_func_index][0]
            func = getattr(self, func_name)
            if func:
                func(start_time, *args)

    def updata_time(self, dt, index, part_time, data_list):
        need_refresh = False
        part_time += dt
        if index + 1 < len(data_list) and self.all_time > data_list[index + 1][0]:
            part_time = self.all_time - data_list[index + 1][0]
            index += 1
            need_refresh = True
            if index >= len(data_list):
                index = 0
        return (need_refresh, index, part_time)

    def calculate_index_and_time(self, data_list):
        cur_index = 0
        for index, data in enumerate(data_list):
            if self.all_time >= data[0]:
                cur_index = index
            else:
                break

        if cur_index >= len(data_list):
            cur_index = len(data_list) - 1
        cur_time = self.all_time - data_list[cur_index][0]
        return (
         cur_index, cur_time)

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
        return (
         cur_index, cur_time)

    def reset_music(self):
        self.part_index, self.part_time = self.calculate_index_and_time_ex(s_part_inf)
        self.animation_index, self.animation_time = self.calculate_index_and_time(s_ajld_lights_animations)
        self.left_right_sfx_index, _ = self.calculate_index_and_time(s_left_right_sfxs)
        self.mid_sfx_index, _ = self.calculate_index_and_time(s_mid_sfxs)
        self.screen_sfx_index, _ = self.calculate_index_and_time(s_screen_sfxs)
        self.light_sfx_index, _ = self.calculate_index_and_time(s_light_sfxs)
        self.exec_func_index, _ = self.calculate_index_and_time(s_exec_func)
        self.refresh_mv()
        self.refresh_lights_animation()
        self.refresh_left_right_sfx()
        self.refresh_mid_sfx()
        self.refresh_screen_sfx()
        self.refresh_exec_func()
        if self.mv_model:
            self.mv_model.visible = bool(self.part_index == s_mp4_run_part_index)
        if self.mv_wait_model:
            self.mv_wait_model.visible = bool(self.part_index != s_mp4_run_part_index)
        self.max_check_progress_count = 0

    def init_spotlight(self, scn):
        for index, spotlight in enumerate(s_spotlight_info):
            m = world.model(s_spotlight_path, scn)
            m.position = math3d.vector(*spotlight[0])
            m.world_rotation_matrix = math3d.matrix.make_rotation_y(spotlight[1] / 180 * 3.14)
            m.scale = math3d.vector(*spotlight[2])
            m.set_submesh_rendergroup_and_priority(4, world.RENDER_GROUP_TRANSPARENT)
            self.spot_light_models.append(m)

    def refresh_mv(self):
        mp4_path = s_part_inf[self.part_index][1]
        if mp4_path:
            self.play_local_mp4(mp4_path)
        else:
            self.cclive_player.stop()
            self.cur_mv_path = None
        return

    def play_local_mp4(self, mp4_path):
        self.video_name = mp4_path
        hashed_video_name = str(abs(int(hash(mp4_path))))
        hashed_full_path = os.path.join(game3d.get_doc_dir(), hashed_video_name)
        self.hashed_full_path = hashed_full_path
        if os.path.exists(hashed_full_path):
            self.on_video_load_finish(hashed_full_path)
        else:
            DaemonThreadPool().add_threadpool(self.thread_load_video, None, self.video_name, hashed_full_path)
        return

    def remove_played_video(self):
        hashed_video_name = str(abs(int(hash(s_mp4_path))))
        hashed_full_path = os.path.join(game3d.get_doc_dir(), hashed_video_name)
        try:
            if os.path.exists(hashed_full_path):
                os.remove(hashed_full_path)
        except:
            pass

    def on_video_load_finish(self, full_path):
        if self.cur_mv_path != full_path:
            self.cclive_player.stop()
            self.cclive_player.play_vod(full_path)
            self.cur_mv_path = full_path
            self.mv_start_time = time.time()
        self.is_check_progress = True
        self.cclive_player.set_volume(0.0)
        self.is_need_seek_to = True
        self.seek_to_downcount = 20

    def thread_load_video(self, video_name, hashed_full_path):

        def cb(res):
            self.on_video_load_finish(res)

        if not C_file.find_res_file(video_name, ''):
            res = None
        else:
            print('partmv start loading video', video_name)
            video_data = C_file.get_res_file(video_name, '')
            if not os.path.exists(game3d.get_doc_dir()):
                os.makedirs(game3d.get_doc_dir())
            try:
                print('partmv hashed path is', hashed_full_path)
                with open(hashed_full_path, 'wb') as tmp_f:
                    tmp_f.write(video_data)
                res = hashed_full_path
            except Exception as e:
                exception_hook.post_error('partmv [play video] copy video data with exception {}:{}'.format(video_name, str(e)))
                res = None

        game3d.delay_exec(1, cb, (res,))
        return

    def cclive_seek_to(self, time):
        if self.cclive_player:
            self.cclive_player.seek_to(int(time * self.seek_scale))

    def seek_to(self, time):
        self.all_time = time
        self.reset_music()

    def change_mv_wait_pic(self, time):
        if self.mv_wait_model and self.mv_wait_model.valid:
            tex = render.texture(s_mv_end_pic)
            self.mv_wait_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex)

    def shut_light(self, start_time):
        if self.shut_light_timer:
            global_data.game_mgr.unregister_logic_timer(self.shut_light_timer)
        self.save_shut_time = time.time()

        def callback(*args):
            factor = min(1.0 - (time.time() - self.save_shut_time) / 0.8, 0.0)
            mtl = self.scene().get_sky_mtl()
            if mtl:
                mtl.set_var(_HASH_Overall_Brightness, 'Overall_Brightness', factor)

        self.shut_light_timer = global_data.game_mgr.register_logic_timer(callback, interval=1, times=2.0, mode=timer.CLOCK)
        part_fog_and_light = self.scene().get_com('PartAutoFogAndLight')
        if not part_fog_and_light:
            return
        part_fog_and_light.set_custom_data_fadein()

    def open_light(self, start_time):
        if self.shut_light_timer:
            global_data.game_mgr.unregister_logic_timer(self.shut_light_timer)
        self.save_shut_time = time.time()

        def callback(*args):
            factor = max((time.time() - self.save_shut_time) / 0.8, 1.0)
            mtl = self.scene().get_sky_mtl()
            if mtl:
                mtl.set_var(_HASH_Overall_Brightness, 'Overall_Brightness', factor)

        self.shut_light_timer = global_data.game_mgr.register_logic_timer(callback, interval=1, times=2.0, mode=timer.CLOCK)
        part_fog_and_light = self.scene().get_com('PartAutoFogAndLight')
        if not part_fog_and_light:
            return
        part_fog_and_light.recover_custom_fog_data_fadein()

    def change_human_model(self, start_time, rold_id, anim_name):
        self.human_anim_start_time = start_time
        if self.cur_rold_id == rold_id and self.human_model:
            self.play_animation(anim_name, self.animation_all_time - self.human_anim_start_time)
        else:
            if self.human_model_id:
                global_data.model_mgr.remove_model_by_id(self.human_model_id)
                self.human_model_id = None
            if self.human_model:
                global_data.model_mgr.remove_model(self.human_model)
                self.human_model = None
            self.cur_rold_id = rold_id
            if not self.cur_rold_id:
                return
            mpath = 'character/99/%s/h.gim' % rold_id
            sub_mesh_data = 'character/99/%s/parts/h_head.gim' % rold_id
            self.human_anim_name = anim_name
            pos = math3d.vector(*s_aj_pos[0])
            self.human_model_id = global_data.model_mgr.create_model_in_scene(mpath, pos, on_create_func=Functor(self.on_load_model_complete, sub_mesh_data))
        return

    def on_load_model_complete(self, sub_mesh_data, model, *args):
        self.human_model_id = None
        self.human_model = model
        self.human_model.add_mesh(sub_mesh_data)
        if self.cur_rold_id in ('2000_skin_a1', '2001'):
            self.human_model.add_mesh('character/99/%s/parts/hyy/h.gim' % self.cur_rold_id)
        self.human_model.world_rotation_matrix = math3d.matrix.make_rotation_y(s_aj_pos[1] / 180.0 * 3.14)
        self.human_model.scale = math3d.vector(*s_aj_pos[2])
        self.human_model.all_materials.set_macro('UNLIT_ENABLE', 'TRUE')
        self.human_model.all_materials.rebuild_tech()
        obj = self.human_model.get_socket_obj('dianziqin', 0)
        if obj:
            obj.visible = False
        for socket_name in ('yaodai', 'hair'):
            obj = self.human_model.get_socket_obj(socket_name, 0)
            if obj:
                obj.all_materials.set_macro('UNLIT_ENABLE', 'TRUE')
                obj.all_materials.rebuild_tech()

        self.play_animation(self.human_anim_name, self.animation_all_time - self.human_anim_start_time)
        if self.cur_rold_id == '2000_skin_a1':
            self.human_model.set_socket_bound_obj_active('huatong', 0, True, True)

            def callback():
                if self.human_model and self.human_model.valid:
                    obj = self.human_model.get_socket_obj('huatong', 0)

            global_data.game_mgr.register_logic_timer(callback, interval=0.1, times=10, mode=timer.CLOCK)
        return

    def play_change_sfx(self, start_time, sfx_path):
        pos = math3d.vector(*s_aj_pos[0])

        def create_cb(sfx):
            sfx.world_rotation_matrix = math3d.matrix.make_rotation_y(s_aj_pos[1] / 180 * 3.14)

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)

    def play_animation(self, anim_name, anim_time):
        self.human_model.play_animation(anim_name, 1.0, 0, anim_time * 1000.0, 1)

    def on_exit(self):
        if self.light_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.light_sfx_id)
            self.light_sfx_id = None
        if self.screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.screen_sfx_id)
            self.screen_sfx_id = None
        if self.mid_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.mid_sfx_id)
            self.mid_sfx_id = None
        if self.light_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.light_sfx_id)
            self.light_sfx_id = None
        for sfx_id in self.left_right_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.left_right_sfx_ids = []
        global_data.emgr.update_battle_stage -= self.on_update_battle_stage
        global_data.emgr.cc_sound_volume_change -= self.on_sound_volume_change
        if self.cclive_player:
            self.cclive_player.stop()
        return