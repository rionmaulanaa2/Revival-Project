# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import gc
import game
import social
import world
import game3d
import render
from time import time as get_time
from common.daemon_thread import DaemonThreadPool
from common.cfg import confmgr
from common.framework import SingletonBase
from common.platform import is_ios
from logic.gcommon.common_utils.local_text import get_text_by_id
import six.moves.builtins
import version
import logic.gcommon.time_utility as t_util
from collections import OrderedDict
import os
import profiling
import C_file
import six
import threading
g_can_resize = True
IOS_KDEBUG_TICK_LOGIC = 1000
IOS_KDEBUG_TICK_POST_LOGIC = 1001
MIN_LOGIC_DELTA_TIME = 1 / 35.0
FORCE_DELTA_TIME = 1 / 17.0
UPDATE_PART_1 = 1
UPDATE_PART_2 = 2
UPDATE_PART_3 = 3
UPDATE_PART_4 = 4
reg_timer = None
reg_idx = 0
REG_DUR = 100
start_tag = False
end_tag = False

class Manager(SingletonBase):
    ALIAS_NAME = 'game_mgr'
    BASIC_AGENT = ('basic_manager', 'other_manager')

    def register_basic_agent(self):
        global reg_timer
        global reg_idx
        if reg_timer:
            game3d.cancel_delay_exec(reg_timer)
            reg_timer = None
        reg_idx = 0
        reg_timer = game3d.delay_exec(REG_DUR, self.register_basic_agent_tick)
        return

    def register_basic_agent_tick(self):
        global reg_timer
        global start_tag
        global end_tag
        global reg_idx
        try:
            reg_attr = 'register_{}_agent'.format(self.BASIC_AGENT[reg_idx])
            reg_func = getattr(self, reg_attr, None)
            if reg_func and callable(reg_func):
                start_tag = True
                reg_func()
        except Exception as e:
            print(e)

        if start_tag and not end_tag:
            game3d.delay_exec(REG_DUR, self.register_basic_agent_tick)
            return
        else:
            reg_idx += 1
            if reg_idx < len(self.BASIC_AGENT):
                game3d.delay_exec(REG_DUR, self.register_basic_agent_tick)
            else:
                game3d.unregister_timer(reg_timer)
                reg_timer = None
                self.register_basic_agent_cb()
            return

    def register_basic_agent_cb(self):
        self.init_game_callback()
        self.start()
        if not global_data.ui_mgr:
            game3d.post_hunter_message('manager- ui_mgr', 'mznb: BasicManagerAgent, missing ui_mgr')
        if not global_data.deviceinfo:
            game3d.post_hunter_message('manager- deviceinfo', 'mznb: BasicManagerAgent, missing deviceinfo')
        if global_data.sound_mgr:
            global_data.sound_mgr.start_check_sys_mute()

    def register_basic_manager_agent(self):
        from logic.manager_agents import BasicManagerAgent
        self.register_agent(BasicManagerAgent.BasicManagerAgent)

    def register_io_manager_agent(self):
        from logic.manager_agents import IOManagerAgent
        self.register_agent(IOManagerAgent.IOManagerAgent)

    def register_other_manager_agent(self):
        from logic.manager_agents import TouchManagerAgent
        self.register_agent(TouchManagerAgent.TouchManagerAgent)
        from logic.manager_agents import EscapeManagerAgent
        self.register_agent(EscapeManagerAgent.EscapeManagerAgent)

    def register_ingame_agent(self):
        from logic.manager_agents import DebugManagerAgent
        self.register_agent(DebugManagerAgent.DebugManagerAgent)
        from logic.manager_agents import IngameManagerAgent
        self.register_agent(IngameManagerAgent.IngameManagerAgent)
        from logic.manager_agents import ExSceneManagerAgent
        self.register_agent(ExSceneManagerAgent.ExSceneManagerAgent)

    def register_agent(self, cls):
        global start_tag
        global end_tag
        if cls.ALIAS_NAME in self.agent_dict:
            agent_end_tag = getattr(self.agent_dict[cls.ALIAS_NAME], 'end_tag', None)
            if agent_end_tag is not None:
                if agent_end_tag:
                    pass
        else:
            print('resgister agent', cls.ALIAS_NAME)
            end_tag = False
            self.agent_dict[cls.ALIAS_NAME] = cls()
        agent_end_tag = getattr(self.agent_dict[cls.ALIAS_NAME], 'end_tag', None)
        if agent_end_tag is not None:
            if agent_end_tag:
                start_tag = False
                end_tag = True
        else:
            start_tag = False
            end_tag = True
        return

    def replace_agent(self, cls_name, new_cls, old_cls):
        pass

    def init_game_callback(self):
        self._set_logic(self.logic)
        self._set_logic_sync(self.logic_sync)
        self._post_logic_timer_enable = False
        self._render_timer_enable = False
        self._post_logic_timer.set_addcount_callback(self._init_post_logic)
        self._post_logic_timer.set_deccount_callback(self._on_timer_deled, self._release_post_logic)
        self._render_timer.set_addcount_callback(self._init_render)
        self._render_timer.set_deccount_callback(self._on_timer_deled, self._release_render)
        game.on_exit = self.on_exit
        game.on_background = self.on_background
        game.on_resume = self.on_resume
        game.on_pause = self.on_pause
        game.on_vkb = self.on_vkb
        game.on_will_vkb = self.on_will_vkb
        game.on_window_kill_focus = self.on_window_kill_focus
        game.on_3d_touch_changed = self.on_3d_touch_switch_changed
        game.on_gmbridge_token_overdue = self.on_gmbridge_token_overdue
        game.on_write_storage_permission_cb = self.on_write_storage_permission_cb
        game.on_record_audio_permission_cb = self.on_mic_permission_cb
        game.on_file_missing = self.on_file_missing

    def preload_shader(self):
        import render
        count = render.set_separate_cache_file('shader/preload_shader.xml')
        if count:
            return
        for i in range(count):
            render.cache_shader_separate(i)

    def on_write_storage_permission_cb(self, result_code):
        global_data.emgr.on_write_storage_cb_event.emit(result_code)

    def on_mic_permission_cb(self, result_code):
        if six.moves.builtins.__dict__.get('GAME_ENV_INITED', False):
            global_data.emgr.on_mic_permission_event.emit(result_code)

    def on_file_missing(self, path):
        self._msg_queue_lock.acquire()
        try:
            self._msgs.append('\xe5\xbd\x93\xe5\x89\x8d\xe8\xb5\x84\xe6\xba\x90\xe5\xad\x98\xe5\x9c\xa8\xe7\xbc\xba\xe5\xa4\xb1\xef\xbc\x9a{}'.format(path))
        finally:
            self._msg_queue_lock.release()

    def init_manager(self):
        self.register_basic_agent()
        if global_data.is_debug_mode:
            game3d.env_enable_log(True)
        if global_data.channel:
            global_data.channel.set_prop_str('WEBVIEW_SUPPORT_BACK_KEY', '1')
        six.moves.builtins.__dict__['WEEK_PATCH_REVERTED'] = False

    def init(self):
        self.agent_dict = OrderedDict()
        DaemonThreadPool().create_threadpool()
        self._pre_gen = self._pre_process()
        self._set_logic(self._init_logic)

    def post_init(self):
        self.init_data()
        game3d.delay_exec(100, self.init_manager)

    def _pre_process(self):
        pre_import_list = ('common.utils.ui_utils', 'common.uisys.uisystem', 'common.uisys.uielment.UIObjectBaseCreator')
        for imp_name in pre_import_list:
            try:
                __import__(imp_name)
            except Exception as e:
                print('manager pre import except:', str(e))

            yield False

        from common.uisys.uielment import ui_element_generator
        ui_gen = ui_element_generator()
        for ret in ui_gen:
            yield False

        post_import_list = ('bson', 'common.platform.channel', 'logic.gutils.salog',
                            'mobile.common.proto_python.common_pb2', 'mobile.mobilerpc.AsioChannelClient',
                            'mobile.client.NetService', 'mobile.client.GateClient',
                            'mobile.simplerpc.DirectProxy', 'logic.gutils.ConnectHelper',
                            'common.uisys.UIManager', 'logic.gutils.mall_utils',
                            'logic.gutils.template_utils')
        for imp_name in post_import_list:
            try:
                __import__(imp_name)
            except Exception as e:
                print('manager post import except:', str(e))

            yield False

        import cc
        for i in range(9):
            cc.SpriteFrameCache.getInstance().addSpriteFrames('gui/ui_res_2/emote/emote%d.plist' % i)
            cc.SpriteFrameCache.getInstance().retainSpriteFrames('gui/ui_res_2/emote/emote%d.plist' % i)
            yield False

        from logic.entities import register_entities
        for ret in register_entities():
            yield False

        yield True

    def _init_logic(self):
        try:
            if self._pre_gen:
                ret = next(self._pre_gen)
                if ret:
                    print('[manager] pre gen ret True')
                    self._pre_gen = None
                    game3d.frame_delay_exec(2, self.post_init)
        except Exception as e:
            print('[Except] [manager] pre import gen except:[{}]'.format(str(e)))
            self._pre_gen = None
            import traceback
            traceback.print_exc()
            import exception_hook
            exception_hook.post_error('[manager] upload: ' + traceback.format_exc())

        return

    def start(self):
        self.restart()
        self.init_qa_tools()
        if global_data.is_artist_animation_test:
            animation_tree_loader = world.get_animation_tree_loader()
            if hasattr(animation_tree_loader, 'SetAllAllowMissingAsset'):
                animation_tree_loader.SetAllAllowMissingAsset(True)
        render_system_name = render.get_render_system_name()
        if render_system_name == 'DirectX 9':
            render.enable_technique_map(True)
        self.init_sunshine()

    def init_qa_tools(self):
        self.start_filesystem_stat_upload()

    def start_filesystem_stat_upload(self):
        if not hasattr(game3d, 'enable_filesystem_stat'):
            return
        if self._filesys_stat_upload_timer:
            return
        game3d.enable_filesystem_stat(True)

        def _upload_filesystem_stat():
            import json
            from common.platform.dctool import interface
            channel = social.get_channel()
            if not channel:
                return
            files = game3d.dump_filesystem_stat().split(';')
            if files[-1] == '':
                files.pop()
            if not files:
                return
            json_dict = {'project': interface.get_project_id(),
               'source': 'cloudsys',
               'type': 'filesystem_stat',
               'files': files,
               'platform': game3d.get_platform(),
               'time': int(self.last_fix_logic_update_clock),
               'player_lv': -1
               }
            if global_data.player:
                json_dict['player_lv'] = global_data.player.get_lv()
            json_str = json.dumps(json_dict)
            channel.drpf(json_str)

        self._filesys_stat_upload_timer = self.register_logic_timer(_upload_filesystem_stat, interval=180, mode=2)

    def init_sunshine(self):
        import six.moves.builtins
        args = six.moves.builtins.__dict__.get('START_ARG', None)
        if args:
            from .gutils.sunshine_utils import parse_args
            init_args = parse_args(args)
            starter = init_args.get('starter', None)
            if starter and starter == 'Sunshine':
                from sunshine.Editor.SunshineEditor import SunshineEditor
                SunshineEditor(init_args=init_args)
        return

    def restart(self, need_logout=False):
        self.stop_game(need_logout=need_logout)
        self.start_game()
        self.init_game_callback()

    def try_restart_app(self):
        bin_launcher_path = game3d.get_root_dir() + '\\..\\launcher.exe'
        if game3d.get_platform() == game3d.PLATFORM_WIN32 and os.path.exists(bin_launcher_path):
            game3d.open_url(bin_launcher_path)
        else:
            game3d.restart()
            game3d.exit()

    def stop(self):
        self._set_logic(None)
        self._release_post_logic()
        self._release_render()
        game.on_exit = None
        game.on_background = None
        game.on_resume = None
        game.on_pause = None
        game.on_vkb = None
        game.on_will_vkb = None
        self.stop_game()
        game3d.cancel_all_delay_exec()
        game3d.clear_resource_cache()
        DaemonThreadPool().finalize()
        self.finalize()
        return

    def logic(self):
        if self.is_on_background or not self._enable_logic:
            return
        self.kdebug_range_start(IOS_KDEBUG_TICK_LOGIC)
        clock = get_time()
        if not self.last_fix_logic_update_clock:
            self.last_fix_logic_update_clock = clock
        dt_origin = clock - self.last_fix_logic_update_clock
        dt = dt_origin * game3d.get_global_speed_rate()
        self.last_fix_logic_update_clock = clock
        self._update_global_game_time(clock)
        if dt > 1:
            dt = 1
        self._logic_delta_time_origin += dt_origin
        self._logic_delta_time += dt
        self.update_next_logic_exec_list(dt)
        self.update_delay_exec_list(dt)
        self.update_scene_fix_logic(dt)
        if global_data.enable_split_script:
            self._time_budget = 1.0 / (profiling.get_logic_rate() + 1) * 0.2
            self._update_time_left = self._time_budget
            t_util.on_logic_update(dt_origin)
            self._logic_update_part_1(dt)
            self._logic_update_part_2(dt)
            self._logic_update_part_3(dt)
            self._logic_update_part_4(dt)
            global_data.display_agent.flush_setting()
        elif self._logic_delta_time_origin >= self._logic_frame_cicle and self._logic_delta_time_origin >= self._force_delta_time:
            global_data.logic_real_dt = self._logic_delta_time_origin
            logic_delta_time_origin = self._logic_delta_time_origin
            logic_delta_time = self._logic_delta_time
            self._logic_delta_time_origin = 0
            self._logic_delta_time = 0
            t_util.on_logic_update(logic_delta_time_origin)
            self.logic_update(logic_delta_time)
        if global_data.g_com_sysmgr:
            global_data.g_com_sysmgr.tick(dt)
        self.update_post_logic_exec_list(dt)
        self.update_show_message()
        self.kdebug_range_end(IOS_KDEBUG_TICK_LOGIC)

    def post_logic(self):
        if self._enable_logic:
            self.kdebug_range_start(IOS_KDEBUG_TICK_POST_LOGIC)
            self.post_logic_update()
            self.kdebug_range_end(IOS_KDEBUG_TICK_POST_LOGIC)

    def logic_sync(self):
        for func, args, kwargs in self._sync_exec_list:
            self._logic_sync_doing = True
            try:
                func(*args, **kwargs)
            except:
                self._logic_sync_doing = False
                self._traceback_uploader()

        self._logic_sync_doing = False
        self._sync_exec_list = []

    def render(self):
        self.render_update()

    def on_exit(self):
        try:
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                _path = os.path.join(game3d.get_doc_dir(), 'launcher_count_flag')
                if os.path.exists(_path):
                    os.remove(_path)
        except:
            pass

        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            _path = os.path.join(game3d.get_doc_dir(), 'in_battle_flag')
            if os.path.exists(_path):
                try:
                    os.remove(_path)
                except:
                    pass

        global_data.emgr.app_exit_event.emit()
        global_data.save_all_log()
        self.stop_game(is_exit=True)
        self.unload_scene(True)
        DaemonThreadPool().finalize()

    def on_pause(self):
        self.on_background()

    def on_background(self):
        inst = self
        if not inst.is_on_background:
            clock = get_time()
            inst.into_background_time = clock
            self._update_global_game_time(clock)
            emgr = global_data.emgr
            if emgr:
                emgr.app_background_event.emit()
            global_data.sound_mgr.set_background(True)
            if global_data.ccmini_mgr:
                global_data.ccmini_mgr.notify_home(1)
            inst.is_on_background = True
            game3d.set_keep_screen_on(False)
            self.background_resumed = False

    def on_resume(self):
        inst = self
        if inst.is_on_background:
            inst.is_on_background = False
            global_data.sound_mgr.set_background(False, 2000)
            game3d.set_keep_screen_on(True)
            self.next_exec(self.do_resume)

    def is_ingame_scene(self):
        return self._is_ingame_scene

    def do_resume(self):
        emgr = global_data.emgr
        if emgr:
            emgr.app_resume_event.emit()
        if global_data.ccmini_mgr:
            global_data.ccmini_mgr.notify_home(0)
        if global_data.display_agent:
            global_data.display_agent.on_resume()
        from logic.gutils import deeplink_utils
        deeplink_utils.check_clipboard_text()

        def _resumed():
            self.background_resumed = True

        self.next_exec(_resumed)

    def is_background_resumed(self):
        return self.background_resumed

    def on_vkb(self, rect):
        global_data.emgr.kb_on_vkb_event.emit(rect)

    def on_will_vkb(self, rect):
        global_data.emgr.kb_on_will_vkb_event.emit(rect)

    def on_window_kill_focus(self):
        global_data.emgr.app_lost_focus_event.emit()

    def on_3d_touch_switch_changed(self, is_open, is_first_start):
        global_data.emgr.app_3d_touch_switch_event.emit(is_open)

    def on_gmbridge_token_overdue(self):
        global_data.player.get_custom_service_token()

    def init_data(self):
        from common.event_notifier import EventNotifyer
        from mobile.common.EntityManager import EntityManager
        from logic.gutils.ConnectHelper import ConnectHelper
        from common.utils.timer import Timer
        from common.platform.channel import Channel
        self._entity_manager = EntityManager
        Channel()
        ConnectHelper()
        EventNotifyer()
        from logic import global_event
        self._global_speed_rate = 1
        self.last_fix_logic_update_clock = None
        self._logic_delta_time_origin = 0
        self._logic_delta_time = 0
        self.last_post_logic_update_clock = None
        self.last_render_update_clock = None
        self._logic_timer = Timer()
        self._fix_logic_timer = [Timer(), Timer()]
        self._post_logic_timer = Timer()
        self._render_timer = Timer()
        self.pause_clock = None
        self.resume_clock = None
        self.scene = None
        self.gds = None
        self.post_logic_exec_list = []
        self.next_logic_exec_list = []
        self.finish_logic_exec_list = []
        self.delay_exec_list = []
        self._sync_exec_list = []
        self._logic_sync_doing = False
        self.is_on_background = False
        self.into_background_time = 0
        self.editor_mode = False
        self._dump_type = 0
        self._enable_logic = True
        self._enable_global_speed_rate = True
        self._is_ingame_scene = False
        self._logic_frame_cicle = MIN_LOGIC_DELTA_TIME
        self._force_delta_time = 0
        self._failed_check_count = 0
        self._target_frame_rate = 30
        self._cur_frame_rate = 30
        self._checker_id = 0
        self._update_time_left = 0
        self._time_budget = 100000
        self._dt_part_1 = 0
        self._dt_part_2 = 0
        self._dt_part_3 = 0
        self._dt_part_4 = 0
        self._next_update = UPDATE_PART_1
        self._pingpong_update = 0
        self._simulate_logic_sync = True
        gc.enable()
        gc.set_threshold(1400, 20, 1000)
        import exception_hook
        self._traceback_uploader = exception_hook.traceback_uploader
        self.background_resumed = True
        self.local_editor = None
        self._msg_queue_lock = threading.Lock()
        self._msgs = []
        self._filesys_stat_upload_timer = None
        return

    def start_game(self):
        self.is_started = True
        from common.audio import sound
        sound.init_before_login()
        self._check_need_start()
        self.load_main_scene()

    def _check_need_start(self):
        import logic.res_verification
        if logic.res_verification.check_need_restart():
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2().init_widget(content=get_text_by_id(194), on_confirm=logic.res_verification.restart)
        from patch import patch_utils
        if hasattr(patch_utils, 'clear_patched_file_dict'):
            patch_utils.clear_patched_file_dict()

    def load_main_scene(self):
        if C_file.find_res_file('pc_editor_package_flag.flag', ''):
            global_data.is_local_editor_mode = True
            self.init_ingame_env()
            if game3d.is_release_version():
                self.download_pc_editor_script()
            import editor
            from logic.gutils.editor_utils.local_editor_utils import LocalEditor
            self.local_editor = LocalEditor()
            self.remove_patch_ui()
            return
        if six.moves.builtins.__dict__.get('auto_login') or __debug__:
            self.load_scene(confmgr.get('setting', 'init_scene', default='Main'))
        else:
            self.load_scene('Main')

    def on_load_main_scene(self):
        from logic.gutils import preload_login_conf_utils
        preload_login_conf_utils.preload_conf()

    def remove_patch_ui(self, remove_bg=True):
        patch_ui_instance = six.moves.builtins.__dict__.get('PATCH_UI_INSTANCE', None)
        if patch_ui_instance:
            try:
                patch_ui_instance.destroy()
            except:
                pass

            six.moves.builtins.__dict__['PATCH_UI_INSTANCE'] = None
        if remove_bg and 'PATCH_BG_LAYER' in six.moves.builtins.__dict__:
            patch_bg_layer = six.moves.builtins.__dict__.get('PATCH_BG_LAYER', None)
            if patch_bg_layer:
                try:
                    patch_bg_layer.removeFromParent()
                except Exception as e:
                    print('remove patch bg layer except:', str(e))

            six.moves.builtins.__dict__['PATCH_BG_LAYER'] = None
            del six.moves.builtins.__dict__['PATCH_BG_LAYER']
        return

    def stop_game(self, is_reconnect=False, need_logout=False, is_exit=False):
        from common.utils.timer import Timer
        log_error('AAA stop game', is_reconnect)
        self.clean_entities()
        if not is_reconnect:
            self.unload_scene(is_exit)
        if hasattr(Timer, 'reset_all_timer_group'):
            Timer.reset_all_timer_group()
        self.last_fix_logic_update_clock = None
        self._logic_delta_time_origin = 0
        self._logic_delta_time = 0
        self.last_post_logic_update_clock = None
        self.last_render_update_clock = None
        self._logic_timer = Timer()
        if global_data.bullet_sfx_mgr:
            global_data.bullet_sfx_mgr.refresh_auto_release_timer()
        if self._post_logic_timer:
            self._post_logic_timer.clean()
        if self._render_timer:
            self._render_timer.clean()
        self._post_logic_timer = Timer()
        self._post_logic_timer.set_addcount_callback(self._init_post_logic)
        self._post_logic_timer.set_deccount_callback(self._on_timer_deled, self._release_post_logic)
        self._render_timer = Timer()
        self._render_timer.set_addcount_callback(self._init_render)
        self._render_timer.set_deccount_callback(self._on_timer_deled, self._release_render)
        self.pause_clock = None
        self.resume_clock = None
        self.post_logic_exec_list = []
        self.next_logic_exec_list = []
        self.finish_logic_exec_list = []
        self.delay_exec_list = []
        self._filesys_stat_upload_timer = None
        for k, v in six.iteritems(self.agent_dict):
            v.on_stop_game()

        confmgr.exit()
        log_error('AAA stop game finish', is_reconnect)
        return

    def logic_update(self, dt):
        keys = six_ex.keys(self.agent_dict)
        for k in keys:
            agent = self.agent_dict.get(k, None)
            if agent and agent.need_update:
                try:
                    agent.on_update(dt)
                except:
                    self._traceback_uploader()

        self._logic_timer.update(dt)
        global_data.connect_helper.tick()
        self.update_scene_logic(dt)
        self.update_entities(dt)
        confmgr.check()
        global_data.daemon_thread_pool.update_threadpool(dt)
        global_data.display_agent.flush_setting()
        return

    def _logic_update_part_1(self, dt):
        self._dt_part_1 += dt
        if self._next_update == UPDATE_PART_1 and self._update_time_left > 0:
            start = get_time()
            dt = self._dt_part_1
            self._dt_part_1 = 0
            keys = six_ex.keys(self.agent_dict)
            for k in keys:
                agent = self.agent_dict.get(k, None)
                if agent and agent.need_update:
                    try:
                        agent.on_update(dt)
                    except:
                        self._traceback_uploader()

            global_data.connect_helper.tick()
            end = get_time()
            self._update_time_left -= end - start
            self._next_update = UPDATE_PART_2
        return

    def _logic_update_part_2(self, dt):
        self._dt_part_2 += dt
        if self._next_update == UPDATE_PART_2 and self._update_time_left > 0:
            start = get_time()
            dt = self._dt_part_2
            self._dt_part_2 = 0
            if self.update_entities(dt):
                self._next_update = UPDATE_PART_3
            end = get_time()
            self._update_time_left -= end - start

    def _logic_update_part_3(self, dt):
        self._dt_part_3 += dt
        if self._next_update == UPDATE_PART_3 and self._update_time_left > 0:
            start = get_time()
            dt = self._dt_part_3
            self._dt_part_3 = 0
            self._logic_timer.update(dt)
            end = get_time()
            self._update_time_left -= end - start
            self._next_update = UPDATE_PART_4

    def _logic_update_part_4(self, dt):
        self._dt_part_4 += dt
        if self._next_update == UPDATE_PART_4 and self._update_time_left > 0:
            start = get_time()
            dt = self._dt_part_4
            self._dt_part_4 = 0
            self.update_scene_logic(dt)
            confmgr.check()
            DaemonThreadPool().update_threadpool(dt)
            end = get_time()
            self._update_time_left -= end - start
            self._next_update = UPDATE_PART_1

    def post_logic_update(self, dt=None):
        if self.is_on_background:
            return
        if not dt:
            if not self.last_post_logic_update_clock:
                self.last_post_logic_update_clock = get_time()
            if self.pause_clock and self.resume_clock:
                dt += self.resume_clock - self.pause_clock
            clock = get_time()
            self._update_global_game_time(clock)
            real_dt = clock - self.last_post_logic_update_clock
            dt = real_dt * game3d.get_global_speed_rate()
            self.last_post_logic_update_clock = clock
            dt = min(1, dt)
            global_data.post_logic_real_dt = real_dt
        else:
            global_data.post_logic_real_dt = dt
        global_data.on_post_logic = True
        self._post_logic_timer.update(dt)
        self.update_finish_logic_exec_list(dt)
        global_data.on_post_logic = False

    def render_update(self):
        if self.is_on_background:
            return
        if not self.last_render_update_clock:
            self.last_render_update_clock = get_time()
        clock = get_time()
        self._update_global_game_time(clock)
        dt = (clock - self.last_render_update_clock) * game3d.get_global_speed_rate()
        self.last_render_update_clock = clock
        dt = min(1, dt)
        self._render_timer.update(dt)

    def update_post_logic_exec_list(self, dt):
        tmp_post_func_list = self.post_logic_exec_list
        self.post_logic_exec_list = []
        for item in tmp_post_func_list:
            try:
                func = item[0]
                args = item[1]
                func(*args)
            except:
                self._traceback_uploader()

    def update_show_message(self):
        if global_data.ui_mgr:
            ui = global_data.ui_mgr.get_ui('WizardTrace')
            if ui:
                self._msg_queue_lock.acquire()
                try:
                    for msg in self._msgs:
                        ui.send_message(msg)

                    self._msgs = []
                finally:
                    self._msg_queue_lock.release()

    def update_finish_logic_exec_list(self, dt):
        tmp_finish_func_list = self.finish_logic_exec_list
        self.finish_logic_exec_list = []
        for item in tmp_finish_func_list:
            try:
                func = item[0]
                args = item[1]
                func(*args)
            except:
                self._traceback_uploader()

    def update_next_logic_exec_list(self, dt):
        tmp_next_func_list = self.next_logic_exec_list
        self.next_logic_exec_list = []
        for item in tmp_next_func_list:
            try:
                func = item[0]
                args = item[1]
                func(*args)
            except:
                self._traceback_uploader()

    def update_delay_exec_list(self, dt):
        dels = []
        for item in self.delay_exec_list:
            try:
                item[3] += dt
                if item[3] >= item[2]:
                    func = item[0]
                    args = item[1]
                    func(*args)
                    dels.append(item)
            except:
                self._traceback_uploader()

        for item in dels:
            self.delay_exec_list.remove(item)

    def update_scene_logic(self, dt):
        if self.scene and self.scene.is_loaded():
            self.scene.logic(dt)
        if global_data.ex_scene_mgr_agent:
            global_data.ex_scene_mgr_agent.update_scene_logic(dt)

    def update_scene_fix_logic(self, dt):
        for t in self._fix_logic_timer:
            t.update(dt)

        if self.scene and self.scene.is_loaded():
            self.scene.fix_logic(dt)
        if global_data.ex_scene_mgr_agent:
            global_data.ex_scene_mgr_agent.update_scene_fix_logic(dt)

    def _update_entities_old(self, update_entities, dt):
        for entity in six.itervalues(update_entities):
            try:
                entity.tick(dt)
            except:
                self._traceback_uploader()

        return True

    def _update_entities_new(self, update_entities, dt):
        cur_pingpong = self._pingpong_update
        update_count = 0
        start_time = get_time()
        counts_per_time = max(5, len(update_entities) // 3)
        for entity in six.itervalues(update_entities):
            if entity.is_entity_mark:
                continue
            try:
                if entity.pingpong_update != cur_pingpong:
                    ddt = entity.skip_dt + dt
                    entity.skip_dt = 0
                    entity.pingpong_update = cur_pingpong
                    update_count += 1
                    entity.tick(ddt)
                    if update_count > counts_per_time and get_time() - start_time > self._update_time_left:
                        update_count = 0
                        cur_pingpong = 1 - self._pingpong_update
                        break
                else:
                    entity.skip_dt += dt
            except:
                self._traceback_uploader()

        if cur_pingpong == self._pingpong_update:
            self._pingpong_update = 1 - self._pingpong_update
            return True
        return False

    def update_entities(self, dt):
        EntityManager = self._entity_manager
        update_entities = EntityManager._update_entities
        entities = EntityManager._entities
        if global_data.enable_split_script:
            ret = self._update_entities_new(update_entities, dt)
        else:
            ret = self._update_entities_old(update_entities, dt)
        for entityid in EntityManager._del_update_entity_marks:
            update_entities.pop(entityid, None)

        EntityManager._del_update_entity_marks.clear()
        for entityid in EntityManager._add_update_entity_marks:
            if entityid in entities:
                update_entities[entityid] = entities[entityid]

        EntityManager._add_update_entity_marks.clear()
        return ret

    def update_event(self):
        from common.event_notifier import EventNotifyer
        EventNotifyer().collect_handlers()

    def clean_entities(self):
        if global_data.player:
            from mobile.common.EntityManager import EntityManager
            battle = global_data.player.get_battle() or global_data.player.get_joining_battle()
            if battle:
                battle.destroy()
                battle = None
            if global_data.player:
                global_data.player.destroy()
            EntityManager.clear()
        if global_data.owner_entity:
            global_data.owner_entity.destroy()
            global_data.owner_entity = None
        return

    def post_exec(self, func, *args):
        self.post_logic_exec_list.append((func, args))

    def next_exec(self, func, *args):
        if func is None:
            raise ValueError('func should not be None')
        self.next_logic_exec_list.append((func, args))
        return

    def finish_exec(self, func, *args):
        self.finish_logic_exec_list.append((func, args))

    def delay_exec(self, delay, func, *args):
        self.delay_exec_list.append([func, args, delay, 0])

    def sync_exec(self, func, *args, **kwargs):
        if self._simulate_logic_sync or self._logic_sync_doing:
            func(*args, **kwargs)
        else:
            self._sync_exec_list.append((func, args, kwargs))

    def load_scene(self, scene_type, scene_data=None, callback=None, async_load=True, back_load=False, release=True):
        if scene_data is None:
            scene_data = {}
        if self.scene and self.scene.is_same_scene(scene_type, scene_data):
            if callback:
                callback()
            return True
        else:
            self.post_exec(self.do_load_scene, scene_type, scene_data, callback, async_load, back_load, release)
            self.update_event()
            return

    def release_cur_scene(self):
        if self.scene:
            world.set_active_scene(None)
            self.scene.destroy()
            self.scene = None
        return

    def _naive_do_load_scene(self, scn_cls, scene_type, scene_data, callback, async_load, back_load):
        same_path_scene = False
        if self.scene:
            same_path_scene = self.scene.is_same_scene_path(scene_data)
            self.scene.on_exit()
            if not same_path_scene:
                self.release_cur_scene()
        if not same_path_scene:
            world.set_active_scene(None)
        gc.collect()
        if not same_path_scene:
            self.scene = scn_cls(scene_type, scene_data, callback, async_load, back_load)
            world.set_active_scene(self.scene)
        else:
            self.scene.reinit_scene(scene_type, scene_data, callback)
        return

    def do_load_scene(self, scene_type, scene_data, callback, async_load, back_load, release):
        scn_cls = None
        self._is_ingame_scene = False
        if scene_type in ('Main', 'Intro', 'MainHuawei'):
            from .vscene import login_scene
            scn_cls = login_scene.LoginScene
        else:
            from .vscene import scene
            scn_cls = scene.Scene
            self._is_ingame_scene = True
        if global_data.ex_scene_mgr_agent:
            global_data.ex_scene_mgr_agent.do_load_scene(scn_cls, scene_type, scene_data, callback, async_load, back_load, release)
        else:
            self._naive_do_load_scene(scn_cls, scene_type, scene_data, callback, async_load, back_load)
        return

    def unload_scene(self, is_exit=False):
        if self.scene:
            self.scene.on_exit()
            world.set_active_scene(None)
            if self.scene:
                self.scene.is_exit_destroy = is_exit
                self.scene.destroy()
                self.scene = None
        return

    def reload_scene(self):
        if not self.scene:
            return
        else:
            old_scene_type = self.scene.scene_type
            old_scene_data = self.scene.scene_data
            self.post_exec(self.do_load_scene, old_scene_type, old_scene_data, None, True, False, True)
            return

    def active_cur_scene(self, on_enter=True, scene=None):
        if scene is not None:
            self.scene = scene
        world.set_active_scene(self.scene)
        if on_enter:
            self.scene.on_enter()
        elif hasattr(self.scene, 'apply_global_display_setting'):
            self.scene.apply_global_display_setting()
        return

    def get_cur_scene(self):
        return self.scene

    def get_cur_scene_type(self):
        if self.scene:
            return self.scene.get_type()
        else:
            return None

    def get_logic_timer(self):
        return self._logic_timer

    def get_fix_logic_timer(self, z_order=0):
        return self._fix_logic_timer[z_order]

    def get_post_logic_timer(self):
        return self._post_logic_timer

    def get_render_timer(self):
        return self._render_timer

    def register_logic_timer(self, func, interval, args=None, times=-1, mode=1, timedelta=False):
        args = args if args else ()
        return self._logic_timer.register(None, func, args, interval, times, mode=mode, timedelta=timedelta)

    def unregister_logic_timer(self, timerid):
        if timerid:
            self._logic_timer.unregister(timerid)

    def set_enable_logic(self, enable):
        self._enable_logic = enable

    def get_enable_logic(self):
        return self._enable_logic

    def enable_global_speed_rate(self, enable):
        self._enable_global_speed_rate = enable
        self.apply_speed_rate()

    def set_global_speed_rate(self, rate):
        self._global_speed_rate = rate
        self.apply_speed_rate()

    def get_global_speed_rate(self):
        if self._enable_global_speed_rate:
            return self._global_speed_rate
        else:
            return 1

    def apply_speed_rate(self):
        if self._enable_global_speed_rate:
            game3d.set_global_speed_rate(self._global_speed_rate)
        else:
            game3d.set_global_speed_rate(1)

    def kdebug_range_start(self, key, color=0):
        if hasattr(game3d, 'kdebug_signpost_start') and game3d.get_platform() == game3d.PLATFORM_IOS:
            game3d.kdebug_signpost_start(key, 0, 0, 0, color)

    def kdebug_range_end(self, key, color=0):
        if hasattr(game3d, 'kdebug_signpost_end') and game3d.get_platform() == game3d.PLATFORM_IOS:
            game3d.kdebug_signpost_end(key, 0, 0, 0, color)

    def kdebug_point(self, key, color=0):
        if hasattr(game3d, 'kdebug_signpost') and game3d.get_platform() == game3d.PLATFORM_IOS:
            game3d.kdebug_signpost(key, 0, 0, 0, color)

    def show_tip(self, tip, unpack=False):
        from logic.comsys.common_ui.NoticeUI import NoticeUI
        if unpack:
            tip = unpack_text(tip)
        notice_ui = NoticeUI()
        notice_ui.add_message(tip)

    def _set_logic(self, func):
        render.set_logic(func)
        render.logic = func

    def _set_post_logic(self, func):
        render.set_post_logic(func)
        render.post_logic = func

    def _set_render(self, func):
        render.set_render(func)
        render.render = func

    def _set_logic_sync(self, func):
        if hasattr(render, 'set_script_sync'):
            render.set_script_sync(func)
            self._simulate_logic_sync = False
        else:
            self._simulate_logic_sync = True

    def _init_post_logic(self, *args):
        if not self._post_logic_timer_enable:
            self._set_post_logic(self.post_logic)
            self._post_logic_timer_enable = True

    def _release_post_logic(self):
        if self._post_logic_timer_enable:
            self._set_post_logic(None)
            self._post_logic_timer_enable = False
        return

    def _init_render(self, *args):
        if not self._render_timer_enable:
            self._set_render(self.render)
            self._render_timer_enable = True

    def _release_render(self):
        if self._render_timer_enable:
            self._set_render(None)
            self._render_timer_enable = False
        return

    def _on_timer_deled(self, count, func):
        if count == 0:
            func()

    def show_debug_message(self, message):
        self._msg_queue.put(message)

    def init_ingame_env(self):
        if six.moves.builtins.__dict__.get('GAME_ENV_INITED', False):
            return
        import C_file
        print('start init ingame env')
        recorded_server_version = version.get_server_version()
        connect_server_version = six.moves.builtins.__dict__.get('SERVER_VERSION', 0)
        print('init ingame version', 'connect server version is', connect_server_version, 'recorded server version is', recorded_server_version)
        if connect_server_version < recorded_server_version:
            pass
        recorded_server_version = version.get_server_version()
        if recorded_server_version != connect_server_version:
            log_error('connnect to a server server version not equal to client')
        if six.PY2:
            import redirect
            redirect.REDIRECT_DEBUG = False
        self.register_ingame_agent()
        from logic.vscene.global_display_setting import GlobalDisplaySeting
        self.gds = GlobalDisplaySeting()
        self.gds.set_quality(self.gds.get_quality())
        global_data.display_agent.do_check_reset_resolution()
        six.moves.builtins.__dict__['RECORD_SERVER_VERSION'] = recorded_server_version
        six.moves.builtins.__dict__['GAME_ENV_INITED'] = True

    def start_cprofile_dump(self, dump_type):
        self._dump_type = dump_type
        if global_data.debug_mgr_agent:
            global_data.debug_mgr_agent.start_cprofile_dump()

    def stop_cprofile_dump(self):
        self._dump_type = 0
        if global_data.debug_mgr_agent:
            global_data.debug_mgr_agent.stop_cprofile_dump()

    def check_need_reload_pipeline(self):
        if global_data.is_renderer2:
            return False
        else:
            if six.moves.builtins.__dict__.get('GAME_ENV_INITED', False):
                return False
            mat = global_data.display_agent.get_post_effect_pass_mtl('placeholder', 0)
            if mat is None:
                from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                NormalConfirmUI2().init_widget(content=get_text_by_id(194), on_confirm=self.try_restart_app)
                return True
            return False

    def set_frame_rate(self, value):
        if global_data.enable_45fps and value == 30:
            value = 45
        if is_ios():
            game3d.set_frame_rate(value)
            if hasattr(game3d, 'set_preferred_frames_per_second'):
                game3d.set_preferred_frames_per_second(int(value))
            else:
                game3d.set_frame_interval(max(int(60 / value), 1))
        else:
            game3d.set_frame_rate(value)
        self._target_frame_rate = value
        self._logic_frame_cicle = 0 if value == 30 else MIN_LOGIC_DELTA_TIME
        self._time_budget = 0.2 / value
        global_data.emgr.app_frame_rate_changed_event.emit()
        self.check_frame_rate_limit()

    def check_frame_rate_limit(self):
        self._failed_check_count = 0
        self._cur_frame_rate = 0
        if self._checker_id == 0 and self._target_frame_rate > 30:
            self._checker_id = self._logic_timer.register(func=self._do_check_frame_rate_limit)

    def _do_check_frame_rate_limit(self):
        can_exit = self._target_frame_rate <= 30
        if self.scene and self.scene.is_loaded():
            self._cur_frame_rate = max(game3d.get_frame_rate(), self._cur_frame_rate)
            if self._cur_frame_rate + 5 >= self._target_frame_rate:
                can_exit = True
            else:
                self._failed_check_count += 1
            if self._failed_check_count > 100:
                can_exit = True
                if self._cur_frame_rate > 60:
                    pass
                elif self._cur_frame_rate > 30:
                    self.set_frame_rate(60 if self._target_frame_rate > 45 else 45)
                else:
                    self.set_frame_rate(30)
        if can_exit:
            self._checker_id = 0
            print('final frame rate is {} fps'.format(self._target_frame_rate))
            from common.utils.timer import RELEASE
            return RELEASE

    def enable_low_script_update(self, enable):
        self._force_delta_time = FORCE_DELTA_TIME if enable else 0
        global_data.low_fps_switch_on = enable

    def _update_global_game_time(self, time):
        gd = global_data
        gd.game_time = time
        gd.game_time_server = time + t_util.g_stamp_delta
        gd.game_time_battle = time + t_util.g_stamp_delta_battle
        gd.game_time_wrapped = time + t_util.g_stamp_delta_wrapped

    @staticmethod
    def disable_resource_cache(including_sfx_cache=True):
        global_data.force_disable_model_cache = True
        global_data.force_disable_sfx_cache = including_sfx_cache
        game3d.set_res_object_cache(False)
        game3d.set_resource_cache(False)
        if global_data.feature_mgr.is_support_sfx_data_and_mesh_vertex_data_lru_cache():
            world.enable_sfx_data_cache(False)
            world.enable_mesh_vertex_data_cache(False)
        global_data.sfx_mgr.enable_sfx_pool = False
        global_data.bullet_sfx_mgr.enable_sfx_pool = False
        global_data.model_mgr.enable_model_pool = False
        global_data.enable_res_ref_cache = False

    @staticmethod
    def clear_resource_cache():
        game3d.clear_resource_cache()
        from common.utils.pool_mgr import SfxPoolMgr, BulletSfxPoolMgr, ModelPoolMgr, ResRefPoolMgr
        all_pool_mgr_classes = (
         SfxPoolMgr, BulletSfxPoolMgr, ModelPoolMgr, ResRefPoolMgr)
        for pool_mgr_class in all_pool_mgr_classes:
            while not pool_mgr_class().check_auto_release(0):
                pass

        from logic.gcommon.component.client.ResourceManager import ModelPool
        ModelPool().clear()
        from logic.gutils.mecha_skin_utils import MechaSocketResAgent
        MechaSocketResAgent.CONFIG_MANAGER.clear_cache()

    def enable_editor(self):
        global_data.is_editor_mode = True
        render.set_prefer_origin_path(True)
        from logic.gutils.editor_utils.sfx_editor_utils import SfxEditorSfxMgr, SfxEditorBulletSfxMgr
        global_data.sfx_mgr.remove_all_sfx()
        global_data.bullet_sfx_mgr.remove_all_sfx()
        global_data.sfx_mgr = SfxEditorSfxMgr()
        global_data.bullet_sfx_mgr = SfxEditorBulletSfxMgr()
        self.disable_resource_cache(including_sfx_cache=False)
        self.clear_resource_cache()
        world.set_gis_anim_first(True)
        global_data.test_script_effect_trigger = True
        global_data.mecha_effect_local_cache_disabled = True
        if global_data.is_local_editor_mode:
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_REFRESH_OPTIMIZATION_OPTION')
        else:
            from logic.gutils.ConnectHelper import ConnectHelper
            ConnectHelper().disconnect()

    def debug_break_point(self):
        if True:
            pass

    @staticmethod
    def _download_file_from_url--- This code section failed: ---

1652       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'queue'
           9  STORE_FAST            2  'queue'

1653      12  LOAD_CONST            1  ''
          15  LOAD_CONST            2  ('thread_downloader',)
          18  IMPORT_NAME           1  'patch.downloader_agent'
          21  IMPORT_FROM           2  'thread_downloader'
          24  STORE_FAST            3  'thread_downloader'
          27  POP_TOP          

1654      28  LOAD_FAST             2  'queue'
          31  LOAD_ATTR             3  'Queue'
          34  CALL_FUNCTION_0       0 
          37  STORE_FAST            4  'ret_queue'

1655      40  LOAD_FAST             2  'queue'
          43  LOAD_ATTR             3  'Queue'
          46  CALL_FUNCTION_0       0 
          49  STORE_FAST            5  'err_queue'

1656      52  LOAD_FAST             2  'queue'
          55  LOAD_ATTR             3  'Queue'
          58  CALL_FUNCTION_0       0 
          61  STORE_FAST            6  'msg_queue'

1657      64  LOAD_FAST             1  'file_path'
          67  LOAD_FAST             1  'file_path'
          70  LOAD_FAST             1  'file_path'
          73  BUILD_TUPLE_4         4 
          76  BUILD_LIST_1          1 
          79  STORE_FAST            7  'download_list'

1658      82  LOAD_FAST             3  'thread_downloader'
          85  LOAD_ATTR             4  'ThreadDownloader'
          88  LOAD_FAST             4  'ret_queue'
          91  LOAD_FAST             5  'err_queue'
          94  LOAD_FAST             6  'msg_queue'
          97  CALL_FUNCTION_3       3 
         100  STORE_FAST            8  'downloader'

1659     103  LOAD_FAST             8  'downloader'
         106  LOAD_ATTR             5  'start_download'
         109  LOAD_FAST             7  'download_list'
         112  LOAD_CONST            0  ''
         115  LOAD_CONST            1  ''
         118  CALL_FUNCTION_3       3 
         121  POP_TOP          

1660     122  SETUP_LOOP           19  'to 144'
         125  LOAD_FAST             4  'ret_queue'
         128  LOAD_ATTR             7  'empty'
         131  CALL_FUNCTION_0       0 
         134  POP_JUMP_IF_FALSE   143  'to 143'

1661     137  CONTINUE            125  'to 125'
         140  JUMP_BACK           125  'to 125'
         143  POP_BLOCK        
       144_0  COME_FROM                '122'
         144  LOAD_CONST            0  ''
         147  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_4' instruction at offset 73

    def download_pc_editor_script(self):
        print('================== updating pc editor script...... ==================')
        patch_list_file_path = os.path.join(game3d.get_root_dir(), 'editor_patch_list.txt')
        code_file_path = os.path.join(game3d.get_root_dir(), 'editor\\script.zip')
        try:
            patch_list_url = 'https://g93.update.netease.com/pl/editor'
            self._download_file_from_url(patch_list_url, patch_list_file_path)
            print('pc editor script patch list downloaded')
            with open(patch_list_file_path, 'r') as f:
                text = f.read()
                index = text.find('\n')
                if index == -1:
                    script_url = text
                else:
                    script_url = text[:index]
            file_name = os.path.splitext(os.path.basename(script_url))[0]
            latest_version = file_name.split('_')[1]
            version_file_path = os.path.join(game3d.get_root_dir(), 'editor\\script_version')
            print('latest version is: ', latest_version)
            if not os.path.exists(version_file_path):
                with open(version_file_path, 'w') as f:
                    f.write(latest_version)
            else:
                with open(version_file_path, 'r') as f:
                    old_version = f.read()
                    print('old version is: ', old_version)
                    if old_version == latest_version:
                        print('================== skip download pc editor script ==================')
                        return
            with open(version_file_path, 'w') as f:
                f.write(latest_version)
            print('start downloading pc editor script......')
            self._download_file_from_url(script_url, code_file_path)
            import zipfile
            dir_path = os.path.dirname(code_file_path)
            f = zipfile.ZipFile(code_file_path)
            f.extractall(dir_path)
            f.close()
            print('================== pc editor script updated successfully ==================')
        except:
            print('================== pc editor script updated failed ==================')

        if os.path.exists(patch_list_file_path):
            os.remove(patch_list_file_path)
        if os.path.exists(code_file_path):
            os.remove(code_file_path)