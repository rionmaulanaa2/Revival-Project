# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_ui.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import os
import time
import queue
import render
import game3d
from . import downloader
from .patch_log import log_info, log_error
from cocosui import cc, ccui, ccs
from .patch_utils import show_confirm_box, PATCH_UI_LAYER, normalize_widget
from . import patch_utils
import social
from patch.patch_lang import get_patch_text_id, get_patch_text_id_only_exist, get_multi_lang_instane, init_steam_language
from patch.patch_path import get_log_state_path, create_patch_temp_folder
from . import network_utils
import package_utils
from . import revert
import threading
import six.moves.builtins
import C_file
import random
import json
from patch import patch_const, patch_dctool
import version
RETRY_TIMES = 3
MAGIC_STRING = 'netease-game:g93+inner/state<code>ace!for$test^magic*number}this{number.should,not)be&known'

class PatchUI(object):
    instance = None

    def __init__(self, finished_callback):
        super(PatchUI, self).__init__()
        six.moves.builtins.__dict__['PATCH_UI_INSTANCE'] = self
        self._platform_name = game3d.get_platform()
        self._npk_version = version.get_npk_version()
        if not self.check_file_system():
            return
        else:
            self.init_android_priority()
            self.init_data()
            self.network_confirm = False
            self.patch_confirm = False
            try:
                patch_utils.init_wretched_config()
            except Exception as e:
                print('Except: init wretched config:', str(e))

            self.finished_callback = finished_callback
            self.use_orbit = False
            self.widget = None
            self.valid = True
            self._npk_dl_retry_count = 0
            self._npk_add_retry_count = 0
            self._support_astc = True
            self._support_ui_astc = True
            self._support_completion_npk = True
            self._init_package_property()

            def init_sdk_callback(*args):
                self.init_widget()

            channel = social.get_channel()
            if self._platform_name == game3d.PLATFORM_WIN32:
                self.use_orbit = False
                init_sdk_callback()
            elif channel.is_init:
                init_sdk_callback()
            else:
                channel.init_sdk_callback = init_sdk_callback
            return

    def init_android_priority(self):
        priority_failed = six.moves.builtins.__dict__.get('PRIORITY_FAILED', False)
        if self._platform_name == game3d.PLATFORM_ANDROID and priority_failed:

            def write_cacert(in_has_permission, info):
                doc = game3d.get_doc_dir()
                try:
                    import os
                    if not os.path.exists(doc):
                        os.makedirs(doc)
                    ccp = '{}/cacert.pem'.format(doc)
                    if not os.path.exists(ccp):
                        d = C_file.get_res_file('cacert.pem', '')
                        with open(ccp, 'wb') as tmp_file:
                            tmp_file.write(d)
                except Exception as e:
                    patch_utils.send_script_error('[init_android_priority_v2] doc:{} has_permission:{} except:{} info:{}'.format(doc, in_has_permission, str(e), info))

            def request_permission():
                prompt_for_permission = True
                prompt_title = get_patch_text_id(3119)
                prompt_msg = get_patch_text_id(3003)
                prompt_btn_close = get_patch_text_id(3004)
                prompt_btn_setting = get_patch_text_id(3005)

                def save_callback(*args):
                    pass

                game3d.save_image_to_gallery('', save_callback, '', '', prompt_for_permission, prompt_title, prompt_msg, prompt_btn_close, prompt_btn_setting)

            permission = 'android.permission.WRITE_EXTERNAL_STORAGE'
            if hasattr(game3d, 'check_client_permission') and hasattr(game3d, 'check_client_should_request_permission'):
                has_permission = game3d.check_client_permission(permission, False)
                if has_permission:
                    write_cacert(has_permission, 'already has permission')
                else:

                    def cb--- This code section failed: ---

 125       0  LOAD_CONST            0  ''
           3  LOAD_DEREF            0  'game'
           6  STORE_ATTR            1  'on_write_storage_permission_cb'

 126       9  STORE_ATTR            1  'on_write_storage_permission_cb'
          12  COMPARE_OP            2  '=='
          15  POP_JUMP_IF_FALSE    34  'to 34'

 127      18  LOAD_DEREF            1  'write_cacert'
          21  LOAD_GLOBAL           2  'True'
          24  LOAD_CONST            2  'player agree permission'
          27  CALL_FUNCTION_2       2 
          30  POP_TOP          
          31  JUMP_FORWARD         13  'to 47'

 129      34  LOAD_DEREF            1  'write_cacert'
          37  LOAD_GLOBAL           3  'False'
          40  LOAD_CONST            3  'player refuse permission'
          43  CALL_FUNCTION_2       2 
          46  POP_TOP          
        47_0  COME_FROM                '31'
          47  LOAD_CONST            0  ''
          50  RETURN_VALUE     

Parse error at or near `STORE_ATTR' instruction at offset 9

                    import game
                    game.on_write_storage_permission_cb = cb
                    write_cacert(False, 'try before request')
                    request_permission()
            else:
                request_permission()
                write_cacert(None, 'game3d has no check_client_permission, too old engine')
        return

    def init_data(self):
        self.network_type_update_count = 0
        self._is_pause = False
        self.spd_modify_time = 0
        self._space_up_time = 0
        self._drpf_up_time = time.time()
        self.cnt_state = patch_utils.DST_INIT
        self.new_package_handle_time = 0
        self.new_package_reverting = False
        self.cnt_image_widget = None
        self.replace_image_widget = None
        self._last_select_image_id = None
        self._img_bg_config = None
        self._patch_title_config = None
        self._patch_content_config = None
        self.last_image_replace_time = 0
        self.last_reset_winsize_time = 0
        self.last_pc_heart_beat_time = 0
        self._is_video_bg = False
        return

    def update_pc_heat_beat(self):
        try:
            if self._platform_name != game3d.PLATFORM_WIN32:
                return
            cnt_time = time.time()
            if cnt_time - self.last_pc_heart_beat_time < 30:
                return
            self.last_pc_heart_beat_time = cnt_time
            patch_dctool.get_dctool_instane().send_patch_heart_beat_info()
        except:
            pass

    def check_file_system(self):
        print('check filesystem')
        print('find res file:', C_file.find_res_file('gui/template/login/login.json', ''))
        if not C_file.find_res_file('gui/template/login/login.json', ''):
            text_id = 90032
            try:
                print('start obb_analyze')
                check_res = patch_utils.obb_analyze()
                if check_res == patch_utils.OBB_CHECK_RES_FILE_NOT_EXIST:
                    text_id = 90101
            except:
                pass

            print('warning t id', text_id)
            game3d.show_msg_box(get_patch_text_id(text_id), get_patch_text_id(90013), game3d.exit, None, get_patch_text_id(90013), get_patch_text_id(90003))
            return False
        else:
            print('find npk_version file:', C_file.find_res_file('npk_version.config', ''))
            self._npk_version = version.get_npk_version()
            if self._npk_version == -2:
                patch_utils.send_script_error('get_npk_version_except')
                game3d.show_msg_box(get_patch_text_id(90101), get_patch_text_id(90013), game3d.exit, None, get_patch_text_id(90013), get_patch_text_id(90003))
                return False
            return True

    def init_widget(self, is_init_steam_language=False):
        channel = social.get_channel()
        if channel and channel.name and channel.name == 'steam' and not is_init_steam_language:
            try:

                def extend_function_callback(json_dict, *args):
                    json_dict = json.loads(json_dict)
                    methodId = json_dict.get('methodId', '')
                    if methodId == 'GetSteamUILanguage':
                        channel.extend_callback = None
                        init_steam_language(json_dict.get('language'))
                        self.init_widget(True)
                    return

                channel.extend_callback = extend_function_callback
                data = {'methodId': 'GetSteamUILanguage'
                   }
                json_data = json.dumps(data)
                channel.extend_func(json_data)
                return
            except:
                print('get steam lanuage from unisdk failed!')

        PatchUI.instance = self
        self.last_update_check_time = time.time()
        self.last_check_count = 0
        self.retry_count = 0
        self._frame = 0
        self.retqueue = queue.Queue()
        channel = social.get_channel()
        if channel.is_downloader_enable():
            self.downloader = downloader.OrbitDownloader(self.retqueue)
        else:
            self.downloader = downloader.Downloader(self.retqueue)
        self.download_start_time = 0
        self.reach_ui_time = time.time()
        self.log_download_rec = []
        self.create()
        new_package = six.moves.builtins.__dict__.get('NEW_PACKAGE_FLAG', False)
        new_package_reverted = six.moves.builtins.__dict__.get('NEW_PACKAGE_REVERTED', False)
        if new_package and not new_package_reverted:
            print('[patch_ui] revert')
            self.new_package_revert()
        else:
            try:
                self.downloader.patch_dctool.check_activation()
            except:
                try:
                    self.downloader.err_queue.put('[ERROR] CHECK ACTIVATION FAILED')
                except:
                    pass

            self.start_logic()

    def play_video(self):
        if not hasattr(patch_const, 'ENABLE_PATCH_VIDEO') or not patch_const.ENABLE_PATCH_VIDEO:
            return
        if not hasattr(patch_const, 'PATCH_VIDEO_NAME') or not C_file.find_res_file(patch_const.PATCH_VIDEO_NAME, ''):
            return
        try:
            from . import patch_video
            patch_inst = patch_video.get_patch_video_instance()
            if patch_inst.is_playing():
                self._is_video_bg = True
                self._on_video_ready()
                patch_inst.set_video_ready_cb(self._on_video_ready)
                patch_inst.set_stop_callback(self._on_video_stop)
            else:
                patch_inst.play_video(patch_const.PATCH_VIDEO_NAME, self._on_video_stop, 0, video_ready_cb=self._on_video_ready, is_mute=False)
        except Exception as e:
            print('patch ui play video exception:', str(e))

    def _on_video_stop(self, *args):
        try:
            self._is_video_bg = False
            self.last_image_replace_time = 0
            if not self.widget:
                return
            self.widget.setOpacity(255)
            if self.cnt_image_widget:
                self.cnt_image_widget.setOpacity(255)
            else:
                self.widget.image_bg.setOpacity(255)
        except Exception as e:
            print('patch ui on video stop except:', str(e))

    def _begin_play_video(self, *args):
        if not self.widget:
            return
        self._is_video_bg = True
        self.set_content_info_visible(False)
        if self.cnt_image_widget:
            self.cnt_image_widget.stopAllActions()
            self.cnt_image_widget.setOpacity(0)
        if self.replace_image_widget:
            self.replace_image_widget.stopAllActions()
            self.replace_image_widget.setOpacity(0)

    def _on_video_ready(self, *args):
        try:
            if self.widget:
                self.widget.setOpacity(0)
                self.widget.image_bg.setOpacity(0)
            self._begin_play_video()
        except Exception as e:
            print('patch ui on video ready except:', str(e))

    def _init_package_property(self):
        try:
            engine_ver = int(version.get_engine_svn())
            if self._platform_name == game3d.PLATFORM_ANDROID:
                if engine_ver < 1133273:
                    self._support_astc = True
                else:
                    self._support_astc = render.is_android_support_astc()
            else:
                self._support_astc = patch_utils.is_ios_support_astc()
            if not self._support_astc:
                if engine_ver < 819872:
                    self._support_astc = True
        except Exception as e:
            print('[Except] [patch_ui]:{}'.format(str(e)))
            self._support_astc = True

        try:
            is_android_dds_package = patch_utils.is_android_dds_package()
        except Exception as e:
            print('[Except] [patch_ui] get android dds flag except:{}'.format(str(e)))
            is_android_dds_package = False

        if is_android_dds_package:
            self._support_astc = True
        is_mobile = self._platform_name in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID)
        self._support_completion_npk = self._npk_version > 0 and is_mobile
        ui_astc_feature_ready = game3d.is_feature_ready('UI_ASTC')
        self._support_ui_astc = not is_android_dds_package and is_mobile and ui_astc_feature_ready
        if self._support_ui_astc and not self._support_astc:
            try:
                C_file.set_etc2_res_flag(True)
            except Exception as e:
                print('[Except] [patch_ui] set etc flag except:{}'.format(str(e)))

        if ui_astc_feature_ready:
            if is_android_dds_package or not is_mobile:
                try:
                    cc.FileUtils.getInstance().setTextureSuffix(['.png', '.dds'])
                except Exception as e:
                    print('[Except] [patch_ui] set ui texture suffix except:{}'.format(str(e)))

                try:
                    render.set_texture_suffix('.dds')
                except Exception as e:
                    print('[Except] [patch_ui] set_texture_suffix except:{}'.format(str(e)))

            elif is_mobile and not self._support_astc:
                try:
                    cc.FileUtils.getInstance().setTextureSuffix(['.ktx', '_astc.ktx'])
                except Exception as e:
                    print('[Except] [patch_ui] set ui texture suffix except:{}'.format(str(e)))

    def start_logic(self):
        self.downloader.set_support_astc(self._support_astc)
        self.downloader.set_support_new_ui_astc_patch(self._support_astc and self._support_ui_astc)
        npk_inited = six.moves.builtins.__dict__.get('NPK_INITED', False)
        game_init_mode = package_utils.get_game_init_mode()
        ignore_npk = game_init_mode == package_utils.GAME_INIT_WITH_PATCH
        platform_need_npk = self._platform_name in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS)
        print('[patch_ui] npk:', npk_inited, game_init_mode, ignore_npk, platform_need_npk, self._support_completion_npk, self._support_astc)
        info_str = 'npk_init:{},game_mode:{},ignore_npk:{},com_npk:{},astc:{}'.format(npk_inited, game_init_mode, ignore_npk, self._support_completion_npk, self._support_astc)
        patch_dctool.get_dctool_instane().send_patch_process_info_info({'stage': 'start logic','info': info_str})
        if platform_need_npk and not npk_inited and not ignore_npk:
            self.downloader.set_npk_version(self._npk_version)
            self.downloader.set_game_init_mode(game_init_mode)
            self.downloader.set_support_completion_npk(self._support_completion_npk)
            self.init_npk(True, self._support_completion_npk)
        else:
            self.init_patch(False)

    def logic(self):
        self.update_logs()
        if self.new_package_reverting:
            self.init_logic()
            return
        if self._is_pause or revert.REVERTING:
            return
        while 1:
            try:
                callback, args = self.retqueue.get_nowait()
                callback(*args)
            except queue.Empty:
                break

        if self.widget:
            self.update_pc_heat_beat()
            self.update_check_info()
            self.update_prog()
            self.replace_bg()
            self.reset_resolution()
            self._update_space()

    def init_resolution(self):
        director = cc.Director.getInstance()
        scene = director.getRunningScene()
        if not scene:
            scene = cc.Scene.create()
            director.runWithScene(scene)
        view = director.getOpenGLView()
        real_size = view.getFrameSize()
        fit_policy = None
        if real_size.width / real_size.height > 1136.0 / 640:
            fit_policy = cc.RESOLUTIONPOLICY_FIXED_HEIGHT
        else:
            fit_policy = cc.RESOLUTIONPOLICY_FIXED_WIDTH
        view.setDesignResolutionSize(1136, 640, fit_policy)
        try:
            width, height, depth, windowType, multisample = game3d.get_window_size()
            if hasattr(game3d, 'set_window_size_force'):
                game3d.set_window_size_force(width, height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(width, height, 32, 1, 0, False)
            else:
                game3d.set_window_size(width, height, 32, 1, 0, False)
            print('set window size', width, height)
        except:
            pass

        return scene

    def new_package_revert(self):
        self.widget.lab_download_info.setString(get_patch_text_id(90046))
        self.hide_prog_info_ui()
        self.new_package_handle_time = time.time()
        self.new_package_reverting = True
        t = threading.Thread(target=self.new_package_revert_thread_func)
        t.setDaemon(True)
        t.start()

    def init_logic(self, *args):
        if not self.widget:
            return
        max_diff_time = 20
        ninety_percent_time = 18.0
        cnt_time = time.time()
        time_diff = cnt_time - self.new_package_handle_time
        cnt_percent = 0
        try:
            if time_diff < ninety_percent_time:
                cnt_percent = time_diff * 100.0 / max_diff_time
            else:
                cnt_percent = (0.9 + 0.1 * (time_diff - ninety_percent_time) / (max_diff_time * 2)) * 100
                cnt_percent = min(cnt_percent, 100)
        except Exception as e:
            print('[Except] init_logic:{}'.format(str(e)))

        self.set_percent(cnt_percent)
        text = get_patch_text_id(90046)
        text += '.' * (int(time_diff) % 7)
        self.widget.lab_download_info.setString(text)

    def new_package_revert_thread_func(self):
        ret = revert.revert()
        need_confirm = False
        if ret is None or ret:
            six.moves.builtins.__dict__['NEW_PACKAGE_REVERTED'] = True
            C_file.set_fileloader_enable('week', True)
        elif hasattr(revert, 'REVERT_FAIL_TIMES'):
            revert.REVERT_FAIL_TIMES += 1
            if revert.REVERT_FAIL_TIMES > 3:
                revert.REVERT_FAIL_TIMES = 0
                need_confirm = True
        C_file.reload_file_system()
        self.new_package_reverting = False
        if need_confirm:
            self.retqueue.put((self.show_revert_confirm, ()))
        else:
            self.retqueue.put((self.reload_patch_phase, (True,)))
        return

    def show_revert_confirm(self):

        def ok_cb():

            def restart_func--- This code section failed: ---

 532       0  LOAD_GLOBAL           0  'render'
           3  LOAD_ATTR             1  'set_post_logic'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_1       1 
          12  POP_TOP          

 533      13  LOAD_DEREF            0  'self'
          16  LOAD_ATTR             3  '_platform_name'
          19  LOAD_GLOBAL           4  'game3d'
          22  LOAD_ATTR             5  'PLATFORM_WIN32'
          25  COMPARE_OP            2  '=='
          28  POP_JUMP_IF_FALSE   158  'to 158'

 534      31  LOAD_GLOBAL           4  'game3d'
          34  LOAD_ATTR             6  'get_root_dir'
          37  CALL_FUNCTION_0       0 
          40  LOAD_CONST            1  '\\..\\launcher.exe'
          43  BINARY_ADD       
          44  STORE_FAST            0  'bin_launcher_path'

 535      47  LOAD_GLOBAL           7  'os'
          50  LOAD_ATTR             8  'path'
          53  LOAD_ATTR             9  'exists'
          56  LOAD_FAST             0  'bin_launcher_path'
          59  CALL_FUNCTION_1       1 
          62  POP_JUMP_IF_FALSE   127  'to 127'

 536      65  LOAD_GLOBAL          10  'hasattr'
          68  LOAD_GLOBAL           4  'game3d'
          71  LOAD_CONST            2  'is_feature_ready'
          74  CALL_FUNCTION_2       2 
          77  POP_JUMP_IF_FALSE   111  'to 111'
          80  LOAD_GLOBAL           4  'game3d'
          83  LOAD_ATTR            11  'is_feature_ready'
          86  LOAD_CONST            3  'OpenExeWithParm'
          89  CALL_FUNCTION_1       1 
        92_0  COME_FROM                '77'
          92  POP_JUMP_IF_FALSE   111  'to 111'

 537      95  LOAD_GLOBAL           4  'game3d'
          98  LOAD_ATTR            12  'open_exe'
         101  LOAD_ATTR             4  'game3d'
         104  CALL_FUNCTION_2       2 
         107  POP_TOP          
         108  JUMP_ABSOLUTE       155  'to 155'

 539     111  LOAD_GLOBAL           4  'game3d'
         114  LOAD_ATTR            13  'open_url'
         117  LOAD_FAST             0  'bin_launcher_path'
         120  CALL_FUNCTION_1       1 
         123  POP_TOP          
         124  JUMP_ABSOLUTE       227  'to 227'

 541     127  LOAD_DEREF            0  'self'
         130  LOAD_ATTR            14  'retqueue'
         133  LOAD_ATTR            15  'put'
         136  LOAD_DEREF            0  'self'
         139  LOAD_ATTR            16  'reload_patch_phase'
         142  LOAD_GLOBAL          17  'True'
         145  BUILD_TUPLE_1         1 
         148  BUILD_TUPLE_2         2 
         151  CALL_FUNCTION_1       1 
         154  POP_TOP          
         155  JUMP_FORWARD         69  'to 227'

 542     158  LOAD_DEREF            0  'self'
         161  LOAD_ATTR             3  '_platform_name'
         164  LOAD_GLOBAL           4  'game3d'
         167  LOAD_ATTR            18  'PLATFORM_ANDROID'
         170  COMPARE_OP            2  '=='
         173  POP_JUMP_IF_FALSE   199  'to 199'

 543     176  LOAD_GLOBAL           4  'game3d'
         179  LOAD_ATTR            19  'restart'
         182  CALL_FUNCTION_0       0 
         185  POP_TOP          

 544     186  LOAD_GLOBAL           4  'game3d'
         189  LOAD_ATTR            20  'exit'
         192  CALL_FUNCTION_0       0 
         195  POP_TOP          
         196  JUMP_FORWARD         28  'to 227'

 546     199  LOAD_DEREF            0  'self'
         202  LOAD_ATTR            14  'retqueue'
         205  LOAD_ATTR            15  'put'
         208  LOAD_DEREF            0  'self'
         211  LOAD_ATTR            16  'reload_patch_phase'
         214  LOAD_GLOBAL          17  'True'
         217  BUILD_TUPLE_1         1 
         220  BUILD_TUPLE_2         2 
         223  CALL_FUNCTION_1       1 
         226  POP_TOP          
       227_0  COME_FROM                '196'
       227_1  COME_FROM                '155'
         227  LOAD_CONST            0  ''
         230  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 104

            render.set_post_logic(restart_func)

        def exit_game():
            game3d.exit()

        msg_txt = get_patch_text_id(90141)
        title_txt = get_patch_text_id(90001)
        game3d.show_msg_box(msg_txt, title_txt, ok_cb, exit_game, get_patch_text_id(90004), get_patch_text_id(90013))

    def reload_patch_phase(self, *args):
        self.destroy()

        def post_logic():
            render.set_logic(None)
            render.set_post_logic(None)
            render.set_render(None)
            import init
            init.stop()
            init.init()
            init.start()
            return

        render.set_render(None)
        render.set_logic(None)
        render.set_post_logic(post_logic)
        return

    def revert_game(self):
        if not self.widget:
            return False
        self.hide_prog_info_ui()
        package_utils.reset_package_info()
        self.widget.lab_download_info.setString(get_patch_text_id(90037))
        return revert.revert_and_exit_game()

    def create(self):
        try:
            get_multi_lang_instane()
        except:
            pass

        scene = self.init_resolution()
        reader = ccs.GUIReader.getInstance()
        widget = reader.widgetFromJsonFile('gui/patch_ui/patch.json')
        widget = normalize_widget(widget)
        scene.addChild(widget, PATCH_UI_LAYER)
        self.widget = widget
        self.init_ui(scene, widget)
        self.init_version()
        render.logic = self.logic
        render.set_logic(self.logic)

    def get_image_bg_config(self):
        try:
            if self._img_bg_config:
                return self._img_bg_config
            if self.is_na_package():
                self._img_bg_config = json.loads(C_file.get_res_file('confs/na_patch_bg_img_config.json', ''))
            else:
                self._img_bg_config = json.loads(C_file.get_res_file('confs/patch_bg_img_config.json', ''))
        except:
            self._img_bg_config = {}

        return self._img_bg_config

    def get_patch_title_config(self):
        try:
            if self._patch_title_config:
                return self._patch_title_config
            if self.is_na_package():
                self._patch_title_config = json.loads(C_file.get_res_file('confs/na_patch_content_title.json', ''))
            else:
                self._patch_title_config = json.loads(C_file.get_res_file('confs/patch_content_title.json', ''))
        except:
            self._patch_title_config = {}

        return self._patch_title_config

    def get_patch_content_config(self):
        try:
            if self._patch_content_config:
                return self._patch_content_config
            if self.is_na_package():
                self._patch_content_config = json.loads(C_file.get_res_file('confs/na_patch_content_info.json', ''))
            else:
                self._patch_content_config = json.loads(C_file.get_res_file('confs/patch_content_info.json', ''))
        except:
            self._patch_content_config = {}

        return self._patch_content_config

    def reset_resolution(self):
        try:
            if not self.last_reset_winsize_time:
                self.last_reset_winsize_time = time.time()
            cnt_time = time.time()
            if cnt_time - self.last_reset_winsize_time < 20:
                return
            self.last_reset_winsize_time = cnt_time
            width, height, depth, windowType, multisample = game3d.get_window_size()
            if hasattr(game3d, 'set_window_size_force'):
                game3d.set_window_size_force(width, height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(width, height, 32, 1, 0, False)
            else:
                game3d.set_window_size(width, height, 32, 1, 0, False)
            print('reset window size', width, height)
        except Exception as e:
            patch_utils.send_script_error('[reset_resolution] ' + str(e))

    def set_content_info_visible(self, visible):
        try:
            self.widget.pnl_story.setVisible(visible)
        except:
            pass

    def set_content_info(self, title, content):
        try:
            self.widget.pnl_story.lab_story_title.setString(title)
            self.widget.pnl_story.lab_story_content.setString(content)
        except:
            pass

    def update_content(self, replace_image_id):
        title_config = self.get_patch_title_config()
        content_config = self.get_patch_content_config()
        title_id = title_config.get(replace_image_id, 0)
        content_id = content_config.get(replace_image_id, 0)
        if title_id and content_id:
            self.set_content_info_visible(True)
            self.set_content_info(get_patch_text_id(title_id), get_patch_text_id(content_id))
        else:
            self.set_content_info_visible(False)

    def replace_bg(self):
        if self._is_video_bg:
            return
        try:
            is_init = False
            if not self.last_image_replace_time:
                self.last_image_replace_time = 0
                is_init = True
            cnt_time = time.time()
            if cnt_time - self.last_image_replace_time < 10:
                return
            self.last_image_replace_time = cnt_time
            img_config = self.get_image_bg_config()
            if not img_config:
                return
            replace_image_id = random.choice(six_ex.keys(img_config))
            if replace_image_id == self._last_select_image_id:
                return
            self._last_select_image_id = replace_image_id
            self.update_content(replace_image_id)
            replace_image = img_config[replace_image_id]
            if not C_file.find_res_file(replace_image, ''):
                if self._platform_name in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID) and replace_image.endswith('.png'):
                    platform_img = replace_image[:-4] + '.ktx'
                    if not C_file.find_res_file(platform_img, ''):
                        return
                else:
                    return
            widget = self.widget
            if not self.replace_image_widget:
                self.replace_image_widget = widget.image_bg.clone()
                self.cnt_image_widget = widget.image_bg
                self.widget.addChild(self.replace_image_widget, 1)
            self.cnt_image_widget.stopAllActions()
            self.replace_image_widget.stopAllActions()
            self.replace_image_widget.loadTexture(replace_image)
            director = cc.Director.getInstance()
            view = director.getOpenGLView()
            vsize = view.getVisibleSize()
            image_bg_size = self.replace_image_widget.getContentSize()
            width_ratio = vsize.width / image_bg_size.width
            height_ratio = vsize.height / image_bg_size.height
            max_ratio = max(width_ratio, height_ratio)
            self.replace_image_widget.setScale(max_ratio)
            if is_init:
                self.replace_image_widget.setOpacity(255)
                self.cnt_image_widget.setOpacity(0)
            else:
                self.replace_image_widget.setOpacity(0)
                self.cnt_image_widget.setOpacity(255)
                fadein_action = cc.FadeTo.create(1.0, 255)
                fadeout_action = cc.FadeTo.create(1.0, 0)
                self.cnt_image_widget.runAction(fadeout_action)
                self.replace_image_widget.runAction(fadein_action)
            temp_widget = self.replace_image_widget
            self.replace_image_widget = self.cnt_image_widget
            self.cnt_image_widget = temp_widget
        except Exception as e:
            print('[Patch] [Except] : {}'.format(str(e)))

    def init_ui(self, scene, widget):
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        vsize = view.getVisibleSize()
        self.init_img_bg()
        image_bg_size = widget.image_bg.getContentSize()
        try:
            width_ratio = vsize.width / image_bg_size.width
            height_ratio = vsize.height / image_bg_size.height
        except Exception as e:
            print('[patch_ui] cal ratio except:', str(e))
            width_ratio = vsize.width / 1624.0
            height_ratio = vsize.height / 750.0

        max_ratio = max(width_ratio, height_ratio)
        widget.image_bg.setScale(max_ratio)
        content_size = widget.pnl_prog.img_buttom.getContentSize()
        content_size.width = vsize.width
        widget.pnl_prog.img_buttom.setContentSize(content_size)
        prog_ratio = 0.9
        text_ratio = (1 - prog_ratio) * 0.5
        content_size = widget.prog_download.getContentSize()
        content_size.width = vsize.width * prog_ratio
        widget.prog_download.setContentSize(content_size)
        content_size = widget.img_prog_bg.getContentSize()
        content_size.width = vsize.width * prog_ratio
        widget.img_prog_bg.setContentSize(content_size)
        margin = widget.lab_download_info.getLayoutParameter().getMargin()
        margin.left = text_ratio * vsize.width
        widget.lab_download_info.getLayoutParameter().setMargin(margin)
        margin = widget.lab_download_prog.getLayoutParameter().getMargin()
        margin.right = text_ratio * vsize.width
        widget.lab_download_prog.getLayoutParameter().setMargin(margin)
        margin = widget.lab_version.getLayoutParameter().getMargin()
        margin.left = text_ratio * vsize.width
        widget.lab_version.getLayoutParameter().setMargin(margin)
        widget.btn_repair.lab_repair.setString(get_patch_text_id(90003))
        widget.btn_feedback.lab_feedback.setString(get_patch_text_id(80140))
        widget.prog_download.setPercent(100)
        try:
            widget.lab_memory.setString('')
            margin = widget.lab_memory.getLayoutParameter().getMargin()
            margin.left = text_ratio * vsize.width
            widget.lab_memory.getLayoutParameter().setMargin(margin)
            widget.btn_notice.lab_notice.setString(get_patch_text_id(80161))
        except Exception as e:
            pass

        widget.lab_download_info.setString('')
        self.udpate_strange_screen_pos(widget, vsize)
        self.init_event(widget)
        self.replace_bg()
        self._create_bg_ui(scene, vsize)

    def udpate_strange_screen_pos(self, widget, v_size):
        try:
            import profiling
            model_name = profiling.get_device_model() or ''
            model_name = model_name.lower()
            adjust_config = json.loads(C_file.get_res_file('confs/c_screen_adapt.json', ''))
            final_config = {}
            if adjust_config:
                for k, v in six.iteritems(adjust_config):
                    final_config[k.lower()] = v

            model_config = final_config.get(model_name, {})
            if not model_config:
                res = game3d.is_notch_screen()
                is_notch = False
                if not isinstance(res, bool):
                    is_notch, left, right, top, down = res
                else:
                    is_notch = res
                if is_notch:
                    if self._platform_name == game3d.PLATFORM_ANDROID:
                        model_config = final_config.get('android_default', {})
                    else:
                        model_config = final_config.get('iphone_default', {})
            offset = model_config.get('WIDTH_EDGE_OFFSET', 0.0)
            margin = widget.btn_feedback.getLayoutParameter().getMargin()
            margin.right = margin.right + offset * v_size.width
            widget.btn_feedback.getLayoutParameter().setMargin(margin)
            margin = widget.btn_repair.getLayoutParameter().getMargin()
            margin.right = margin.right + offset * v_size.width
            widget.btn_repair.getLayoutParameter().setMargin(margin)
            margin = widget.btn_notice.getLayoutParameter().getMargin()
            margin.right = margin.right + offset * v_size.width
            widget.btn_notice.getLayoutParameter().setMargin(margin)
        except:
            pass

    def is_na_package(self):
        try:
            is_na = self.downloader.patch_dctool.get_project_id().endswith('na')
            channel = social.get_channel()
            is_steam_channel = channel and channel.name == 'steam'
            ret = is_na and not is_steam_channel
            return ret
        except:
            return False

    def init_img_bg(self):
        try:
            if not self.is_na_package():
                self.widget.image_bg.loadTexture('gui/ui_res_2/common/bg/bg_hall.png')
        except:
            pass

    def init_event(self, widget):
        try:
            widget.btn_repair.addTouchEventListener(self.on_click_repair_btn)
            widget.btn_feedback.addTouchEventListener(self.on_click_feedback_btn)
            widget.btn_notice.addTouchEventListener(self._on_click_btn_notice)
        except:
            pass

    def destroy(self):
        if self.widget:
            self.widget.removeFromParent()
            self.widget = None
        return

    def destroy_logic(self):
        render.logic = None
        render.set_logic(None)
        return

    def start_download_patch(self):
        patch_size = self.downloader.get_patch_size()
        self.download_start_time = time.time()
        self.init_prog_ui()

        def ok_cb():
            upload_info = {'BEGIN_DL_PATCH': 'size:{}'.format(patch_size)}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
            self.downloader.download_patch_files(self.on_download_patch_finished)
            self.rec_patch_download_info(self.reach_ui_time, self.download_start_time, self.download_start_time, 0)

        def cc_cb():
            upload_info = {'stage': 'download patch','info': 'player cancel download patch because of no space'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
            game3d.exit()

        ignore_space_check = six.moves.builtins.__dict__.get('IGNORE_PATCH_SPACE_CHECK', False)
        need_remind_space = False
        if self._platform_name == game3d.PLATFORM_ANDROID and hasattr(game3d, 'get_available_memory'):
            try:
                available_memory = game3d.get_available_memory()
                patch_size_m = patch_size * 1.0 / 1024.0 / 1024.0
                if available_memory - 20 < patch_size_m:
                    process_info = {'stage': 'download patch','info': 'no enough space, has:{}, need:{}'.format(available_memory, patch_size_m)}
                    patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                    need_remind_space = True
            except Exception as e:
                log_error('[patch] get available memory except:{}'.format(str(e)))

        need_remind_space = False
        if need_remind_space and not ignore_space_check:
            text = get_patch_text_id(277)
            show_confirm_box(ok_cb, cc_cb, text, get_patch_text_id(90004), get_patch_text_id(90005))
        else:
            ok_cb()

    def init_version(self):
        ver_str = self.downloader.get_cur_ver_str()
        text = get_patch_text_id(90006, ver_str)
        self.widget.lab_version.setString(text)

    def init_prog_ui(self):
        self.set_percent(100)
        self.widget.lab_download_prog.setString(get_patch_text_id(90007))

    def check_network(self):

        def confirm_go_to_setting():
            game3d.go_to_setting()

        def cancel_go_to_setting():
            pass

        if self._platform_name == game3d.PLATFORM_IOS:
            if network_utils.g93_get_network_auth() == network_utils.AUTH_RESTRICT:
                show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, get_patch_text_id(3112), get_patch_text_id(80284), get_patch_text_id(19002))
                return False
        return True

    def patchlist_download_callback(self, ret, cb_process_info=None):
        if ret == 1:
            size = self.downloader.get_patch_size()
            size = size / 1024.0 / 1024.0
            if size < 0.01:
                size = 0.01
            self._show_discrete_info()
            nt_type = network_utils.g93_get_network_type()
            if self.patch_confirm or not self.network_confirm and nt_type != network_utils.TYPE_WIFI:

                def ok_cb():
                    self.network_confirm = True
                    self.start_download_patch()

                def cc_cb():
                    upload_info = {'REFUSE_DOWNLOAD_PATCH': 'player cancel download patch'}
                    patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
                    game3d.exit()

                text = get_patch_text_id(90008, size)
                show_confirm_box(ok_cb, cc_cb, text, get_patch_text_id(90004), get_patch_text_id(90005))
            else:
                self.start_download_patch()
        elif ret == 0:
            process_info = {'ANALYZE_PATCH_LIST_NO_NEED_PATCH': 'patch list tell no need patch'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            self.destroy_and_callback()
        elif ret == -1:

            def ok_func():
                self.init_patch()

            def cancel_func():
                game3d.exit()

            self.rec_patch_download_info(self.reach_ui_time, time.time(), time.time(), -1)
            hint_text = get_patch_text_id(90042)
            try:
                met_flist_error = self.downloader.is_flist_error()
                if met_flist_error:
                    hint_text = get_patch_text_id(90142)
            except:
                pass

            if cb_process_info:
                try:
                    full_error_log = 'stage:{0} error:{1}'.format(cb_process_info.get('stage', 'null'), cb_process_info.get('error', 'null'))
                    log_error(full_error_log)
                    error_tips = cb_process_info.get('error_tips')
                    if error_tips:
                        hint_text = error_tips
                    error_code = cb_process_info.get('error_code')
                    if error_code:
                        hint_text = hint_text + get_patch_text_id(90107, error_code)
                except:
                    pass

            show_confirm_box(ok_func, cancel_func, hint_text, get_patch_text_id(90010), get_patch_text_id(90013))
            self.check_network()
        elif ret == 2:
            self.downloader.download_patchlist(self.patchlist_download_callback)

    def init_patch(self, need_confirm=True):
        self.set_percent(100)
        self.hide_prog_info_ui()
        self.patch_confirm = need_confirm
        if need_confirm:
            self.retry_count = 0
        if not create_patch_temp_folder():
            self.on_patch_runtime_error()
            return
        if network_utils.g93_get_network_type() != network_utils.TYPE_INVALID:
            self.downloader.download_patchlist(self.patchlist_download_callback)
            process_info = {'DL_PATH_LIST_BEGIN': 'begin download patch list'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        else:
            process_info = {'DL_PATH_LIST_NETWORK_INVALID': 'download patch list failed for network invalid'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            cb_info = {'error': 'network invalid',
               'error_code': patch_utils.PATCH_ERROR_NETWORK_INVALID,
               'error_tips': get_patch_text_id(90106)
               }
            self.retqueue.put((self.patchlist_download_callback, (-1, cb_info)))

    def on_patch_runtime_error(self):
        import traceback
        traceback.print_stack()
        revert.revert_to_original_version_noerror()

    def init_npk(self, need_confirm=True, support_completion_npk=True):
        self.hide_prog_info_ui()
        self.set_percent(100)
        if not create_patch_temp_folder():
            self.on_patch_runtime_error()
            return
        self.init_npk_callback_handlers()
        if support_completion_npk:
            self.downloader.download_npklist(self.npk_callback_dispatcher)
        else:
            self.downloader.check_npk_old(self.npk_callback_dispatcher)

    def init_npk_callback_handlers(self):
        self.npk_callback_handlers = {patch_utils.NPK_STATE_DLD_FILE_ERROR: self.npk_state_dld_file_error_callback,
           patch_utils.NPK_STATE_CHECK_OK: self.npk_state_check_ok_callback,
           patch_utils.NPK_STATE_DLD_FILE_SUCCESS: self.npk_state_dld_file_success_callback,
           patch_utils.NPK_STATE_DLD_INFO_FILE_ERROR: self.npk_state_dld_info_file_error_callback,
           patch_utils.NPK_STATE_DLD_INFO_FILE_SUCCESS: self.npk_state_dld_info_file_success_callback,
           patch_utils.NPK_STATE_FILE_MISS_OR_ERROR: self.npk_state_file_miss_or_error_callback,
           patch_utils.NPK_STATE_INFO_MISS_OR_ERROR: self.npk_state_info_miss_or_error_callback,
           patch_utils.NPK_STATE_DLD_LIST_FILE_ERROR: self.npk_state_dld_list_file_error_callback,
           patch_utils.NPK_STATE_DLD_LIST_FILE_SUCCESS: self.npk_state_dld_list_file_success_callback,
           patch_utils.NPK_STATE_DLD_LIST_FILE_REDIRECT: self.npk_state_dld_list_file_redirect_callback,
           patch_utils.NPK_STATE_DLD_LIST_FILE_RETRY: self.npk_state_dld_list_file_redirect_callback,
           patch_utils.NPK_STATE_LIST_NO_MATCHED: self.npk_state_list_no_matched_callback,
           patch_utils.NPK_STATE_COPY_PD_FILE_FINISHED: self.npk_state_copy_pd_file_finished_callback
           }

    def npk_callback_dispatcher(self, ret):
        print('npk callback with return', ret)
        if ret not in self.npk_callback_handlers:
            self.on_patch_runtime_error()
        else:
            self.npk_callback_handlers[ret]()

    def npk_state_dld_list_file_redirect_callback(self):
        self.downloader.download_npklist(self.npk_callback_dispatcher)

    def npk_state_dld_list_file_error_callback(self):

        def ok_func():
            self.downloader.download_npklist(self.npk_callback_dispatcher)

        def cancel_func():
            game3d.exit()

        text_id = 90056 if self.downloader.get_space_flag() else 90042
        show_confirm_box(ok_func, cancel_func, get_patch_text_id(text_id), get_patch_text_id(90010), get_patch_text_id(90013))
        self.check_network()

    def _delay_check_npk_info(self):
        self.downloader.check_npk_info(self.npk_callback_dispatcher)

    def npk_state_dld_list_file_success_callback(self):
        process_info = {'NPKLIST_ANALYZE_SUCCESS': 'begin check npk info'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        game3d.delay_exec(30, self._delay_check_npk_info)

    def npk_state_check_ok_callback(self):
        from . import patch_video
        patch_video.destroy_patch_video_instance()
        process_info = {'CHECK_NPK_FILE_DONE': 'npk check is ok, add npk to file system'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        ret = self.downloader.init_npk_filesystem()
        if ret:
            six.moves.builtins.__dict__['NPK_INITED'] = True
            self.init_patch(False)
        else:
            self._npk_add_retry_count += 1
            if self._npk_add_retry_count > 5:
                self._npk_add_retry_count = 0
                game3d.show_msg_box(get_patch_text_id(90142), get_patch_text_id(90013), game3d.exit, self._delay_check_npk_info, get_patch_text_id(90013), get_patch_text_id(90010))
            else:
                game3d.delay_exec(500, self._delay_check_npk_info)

    def npk_state_info_miss_or_error_callback(self):
        print('[patch] has not local npk info')
        process_info = {'CHECK_NPK_NO_INFO': 'has no npk info, begin download'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        self.downloader.download_npkinfo(self.npk_callback_dispatcher)

    def npk_state_dld_info_file_error_callback(self):

        def ok_func():
            process_info = {'DL_NPK_INFO_FAIL_RETRY': 'player retry download npk info'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            self.downloader.download_npkinfo(self.npk_callback_dispatcher)

        def cancel_func():
            process_info = {'DL_NPK_INFO_FAIL_EXIT': 'download npk info failed, player exit game'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            game3d.exit()

        text_id = 90056 if self.downloader.get_space_flag() else 90042
        show_confirm_box(ok_func, cancel_func, get_patch_text_id(text_id), get_patch_text_id(90010), get_patch_text_id(90013))
        self.check_network()

    def npk_state_file_miss_or_error_callback(self):
        print('do download npk files')
        self.do_download_npkfiles()
        self.play_video()

    def do_download_npkfiles(self):
        try:
            patch_utils.del_com_npk_md5_checked_flag()
        except Exception as e:
            print('[PATCH] del com npk checked flag except:', str(e))

        def ok_func():
            upload_info = {'CONFIRM_DOWNLOAD_NPK': 'confirm download'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
            self.downloader.copy_pdfiles(self.npk_callback_dispatcher)

        def cancel_func():
            upload_info = {'EXIT_DOWNLOAD_NPK': 'cancel download'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
            game3d.exit()

        npk_size = self.downloader.get_real_stand_npk_download_size()
        txt_additional = ''
        npk_size = npk_size * 1.0 / 1048576.0
        if npk_size < 0.01:
            npk_size = 0.01
        text = get_patch_text_id(90043, npk_size, txt_additional)
        ignore_space_check = six.moves.builtins.__dict__.get('IGNORE_NPK_SPACE_CHECK', False)
        need_confirm_space = False
        if self._platform_name == game3d.PLATFORM_ANDROID and hasattr(game3d, 'get_available_memory'):
            try:
                available_memory = game3d.get_available_memory()
                if available_memory - 200 < npk_size:
                    need_confirm_space = True
                    process_info = {'stage': 'download npk files',
                       'info': 'has no enough memory:{}, need:{}'.format(available_memory, npk_size)
                       }
                    patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                    if not ignore_space_check:
                        add_text = get_patch_text_id(276)
                        text += '\n' + add_text
            except:
                pass

        if need_confirm_space:
            show_confirm_box(ok_func, cancel_func, text, get_patch_text_id(90004), get_patch_text_id(90005))
        else:
            ok_func()

    def npk_state_copy_pd_file_finished_callback(self):
        upload_info = {'REAL_DOWNLOAD_NPK': 'start download'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
        self.downloader.download_npkfiles(self.npk_callback_dispatcher)

    def npk_state_dld_info_file_success_callback(self):
        process_info = {'DL_NPK_INFO_SUCCESS': 'download npk info success, begin check npk info'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        game3d.delay_exec(30, self._delay_check_npk_info)

    def npk_state_dld_file_error_callback(self):
        space_flag = self.downloader.get_space_flag()

        def ok_func():
            process_info = {'DOWNLOAD_NPK_FAILED_RETRY': 'retry download npk, no space:{}'.format(space_flag)}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            game3d.delay_exec(30, self._delay_check_npk_info)

        def cancel_func():
            process_info = {'DOWNLOAD_NPK_FAILED_EXIT': 'download fail exit, no space:{}'.format(space_flag)}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            game3d.exit()

        text_id = 90056 if space_flag else 90044
        self._npk_dl_retry_count += 1
        if self._npk_dl_retry_count > RETRY_TIMES or space_flag:
            self._npk_dl_retry_count = 1
            show_confirm_box(ok_func, cancel_func, get_patch_text_id(text_id), get_patch_text_id(90010), get_patch_text_id(90013))
        else:
            ok_func()

    def npk_state_dld_file_success_callback(self):
        process_info = {'DOWNLOAD_NPK_SUCCESS': 'download npk success, begin check npk info'}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
        game3d.delay_exec(30, self._delay_check_npk_info)

    def npk_state_list_no_matched_callback(self):
        text = get_patch_text_id(3130) + '\n' + get_patch_text_id(90026)

        def ok_cb():
            print('[patch_ui] confirm revert game for not matched npk list, url is:', self.downloader.get_npk_list_url())
            import package_utils
            package_utils.reset_package_info()
            package_utils.del_game_init_mode_file()
            game3d.restart()
            game3d.exit()

        def cc_cb():
            print('[downloader] cancel revert game for not matched npk list, url is:', self.downloader.get_npk_list_url())
            game3d.exit()

        show_confirm_box(ok_cb, cc_cb, text, get_patch_text_id(90004), get_patch_text_id(90005))

    def show_prog_info_ui(self):
        self.widget.lab_download_prog.setVisible(True)

    def hide_prog_info_ui(self):
        self.widget.lab_download_prog.setString('')

    def rec_patch_download_info(self, reach_ui_time, start_time, end_time, donwload_state):
        try:
            with open(get_log_state_path(), 'a+') as f:
                f.write('%d %d %d %d\n' % (int(reach_ui_time), int(start_time), int(end_time), int(donwload_state)))
                f.close()
        except:
            pass

    def on_download_patch_finished(self, ret, cb_info=None):
        finish_time = time.time()
        if ret:
            try:
                patch_utils.drpf_check_update(patch_dctool.PATCH_UPDATE_PHASE_OK)
            except:
                pass

            process_info = {'PATCH_DL_AND_ANALYZE_SUCCESS': 'patch done!'}
            patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
            package_utils.modify_package_info()
            C_file.set_fileloader_enable('week', True)
            C_file.reload_file_system()
            self.rec_patch_download_info(self.reach_ui_time, self.download_start_time, finish_time, 1)
            self.reload_patch_phase()
        else:
            try:
                patch_utils.drpf_check_update(patch_dctool.PATCH_UPDATE_PAHSE_FAILED)
            except:
                pass

            self.rec_patch_download_info(self.reach_ui_time, self.download_start_time, finish_time, -1)

            def retry_func(need_confirm=True):
                if self.downloader.patch_error_list:
                    try:
                        error_len = len(self.downloader.patch_error_list)
                        download_id = self.downloader.patch_download_id_str
                        self.downloader.patch_dctool.on_download_patch_failed(self.downloader.patch_error_list[0][2], download_id, 'download patch finished', error_len, self.downloader.get_patch_version())
                        process_info = {'stage': 'download patch retry',
                           'error_len': error_len,'retry_time': self.retry_count,'first_error_file': self.downloader.patch_error_list[0][0],
                           'download_id': download_id}
                        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                    except:
                        pass

                self.init_patch(need_confirm)

            def ok_func():
                process_info = {'DOWNLOAD_PATCH_FAILED_RETRY': 'player confirm retry download patch'}
                patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                retry_func(True)

            def cancel_func():
                process_info = {'DOWNLOAD_PATCH_FAILED_EXIT': 'player cancel retry download patch'}
                patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                game3d.exit()

            self.retry_count += 1
            if self.retry_count > RETRY_TIMES:
                hint_text = get_patch_text_id(90012)
                if self.downloader.patch_error_list:
                    try:
                        error_len = len(self.downloader.patch_error_list)
                        first_error_file = self.downloader.patch_error_list[0][0]
                        log_error('patch_error_list len:{0}, first_error_file:[{1}]'.format(error_len, first_error_file))
                        hint_text = get_patch_text_id(90108)
                    except:
                        pass

                elif cb_info:
                    error_tips = cb_info.get('error_tips')
                    if error_tips:
                        hint_text = error_tips
                show_confirm_box(ok_func, cancel_func, hint_text, get_patch_text_id(90010), get_patch_text_id(90013))
            else:
                retry_func(False)

    def update_check_info(self):
        cur_time = time.time()
        check_time = 3.0 if self.downloader.state == patch_utils.DST_COPY else 0.8
        if cur_time - self.last_update_check_time < check_time:
            return
        self.last_update_check_time = cur_time
        state_text_id_map = {patch_utils.DST_PLIST: 90016,
           patch_utils.DST_FLIST: 90017,
           patch_utils.DST_FILES: 90018,
           patch_utils.DST_COPY: (
                                [
                                 (90060, 90101), (90112, 90136)], 90019),
           patch_utils.DST_FLIST_CHECK: 90036,
           patch_utils.DST_NPK_CHECK: 90039,
           patch_utils.DST_NPK_LIST_DLD: 90040,
           patch_utils.DST_NPK_INFO: 90041,
           patch_utils.DST_NPK_FILES: 90045
           }
        text_id = state_text_id_map.get(self.downloader.state, 90023)
        if isinstance(text_id, tuple) and len(text_id) == 2 and isinstance(text_id[0], list):
            random_text_idx = random.randint(0, len(text_id[0]) - 1)
            random_text_id = random.randint(*text_id[0][random_text_idx])
            random_text = get_patch_text_id_only_exist(random_text_id)
            text_id = random_text_id if random_text else text_id[1]
        text = get_patch_text_id(text_id)
        text += '.' * (self.last_check_count % 5)
        self.last_check_count += 1
        self.widget.lab_download_info.setString(text)

    def calc_estimate_download_prog(self):
        if not self.downloader.is_donwloading():
            return 0
        estimate_download_time = 30
        cnt_time = time.time()
        donwload_start_time = self.downloader.downloader_agent.download_start_time
        estimate_prog = int((cnt_time - donwload_start_time) * 100.0 / estimate_download_time)
        return estimate_prog

    def update_prog(self):
        self.update_network()
        prog = int(self.downloader.get_prog() * 100)
        dl_state = self.downloader.state
        if dl_state in (patch_utils.DST_PLIST, patch_utils.DST_FLIST):
            prog = max(prog, self.calc_estimate_download_prog())
        prog = min(100, prog)
        self.set_percent(prog)
        text = ''
        if not self.downloader.is_donwloading():
            if dl_state == patch_utils.DST_COPY:
                self._frame = (self._frame + 1) % 90
                text = get_patch_text_id(90022, '.' * (self._frame // 30 + 1), prog)
            elif self.downloader.state == patch_utils.DST_PATCH_NPK_UPDATE:
                text = get_patch_text_id(90139, prog) if prog > 0 else get_patch_text_id(90023)
            elif self.downloader.state == patch_utils.DST_PATCH_NPK_VERIFY:
                text = get_patch_text_id(90140, prog) if prog > 0 else get_patch_text_id(90023)
            elif self.downloader.state == patch_utils.DST_COPY_PD_FILE:
                text = '\xe5\xa4\x8d\xe5\x88\xb6\xe9\xa2\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe8\xb5\x84\xe6\xba\x90\xe5\x8c\x85: {}%'.format(prog)
            else:
                text = get_patch_text_id(90038, prog) if prog > 0 else get_patch_text_id(90023)
            self.widget.lab_download_prog.setString(text)
        elif dl_state in (patch_utils.DST_PLIST, patch_utils.DST_FLIST, patch_utils.DST_NPK_LIST_DLD, patch_utils.DST_NPK_INFO):
            self.hide_prog_info_ui()
        else:
            speed = self.downloader.get_speed()
            cnt_time = time.time()
            if cnt_time - self.spd_modify_time > 1.0:
                self.spd_modify_time = cnt_time
                unit = 'MB'
                if speed < 0.1:
                    speed = speed * 1024
                    unit = 'KB'
                total_size_mb = self.downloader.downloader_agent.total_size * 1.0 / 1048576.0
                total_size_mb = max(0.1, total_size_mb)
                downloaded_size_mb = total_size_mb * (prog * 1.0 / 100)
                text = get_patch_text_id(90021, prog, downloaded_size_mb, total_size_mb, speed, unit) if speed > 0 else get_patch_text_id(90020, prog, downloaded_size_mb, total_size_mb)
                self.widget.lab_download_prog.setString(text)
                if patch_const.ENABLE_DOWNLOAD_DRPF_UP:
                    if cnt_time - self._drpf_up_time > patch_const.PACKAGE_DRPF_UP_TIME:
                        self._drpf_up_time = cnt_time
                        drpf_key = 'DOWNLOADING_COMPLETE_NPK' if dl_state == patch_utils.DST_NPK_FILES else 'DOWNLOADING_PATCH'
                        process_info = {drpf_key: prog,'state': dl_state,'prog': prog,'total_size': total_size_mb}
                        patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)

    def _update_space(self):
        try:
            now_time = time.time()
            if now_time - self._space_up_time < patch_const.SPACE_UP_TIME:
                return
            self._space_up_time = now_time
            mega_bytes = -1
            if self._platform_name == game3d.PLATFORM_IOS:
                if hasattr(game3d, 'get_total_memory'):
                    available_mem = game3d.get_available_memory()
                    if available_mem >= 0:
                        mega_bytes = available_mem
            elif self._platform_name == game3d.PLATFORM_ANDROID:
                dir_name = os.path.dirname(game3d.get_doc_dir())
                if os.path.exists(dir_name) and hasattr(game3d, 'is_feature_ready') and game3d.is_feature_ready('PathMemoryGet'):
                    mega_bytes = game3d.get_path_available_memory(dir_name)
                else:
                    mega_bytes = game3d.get_available_memory()
            if mega_bytes >= 0:
                if mega_bytes > 1024:
                    mem_txt = '{:.1f}G'.format(mega_bytes / 1024.0)
                else:
                    mem_txt = '{}MB'.format(int(mega_bytes))
                pre_text = get_patch_text_id_only_exist(353)
                if pre_text:
                    mem_txt = pre_text + ':' + mem_txt
                self.widget.lab_memory.setString(mem_txt)
            else:
                self.widget.lab_memory.setString('')
        except Exception as e:
            log_error('[Patch] update space except:{}'.format(str(e)))

    def update_logs(self):
        while self.downloader.err_queue.qsize() > 0:
            err = self.downloader.err_queue.get()
            patch_utils.send_script_error(err)
            log_error(err)

        msg_queue_log_limit = 3000
        cnt_count = 0
        while self.downloader.msg_queue.qsize() > 0:
            msg = self.downloader.msg_queue.get()
            cnt_count += 1
            if msg_queue_log_limit <= cnt_count:
                break

    def set_percent(self, p):
        self.widget.prog_download.setPercent(p)

    def update_network(self):
        self.network_type_update_count -= 1
        if self.network_type_update_count <= 0:
            self.downloader.set_network_type(network_utils.g93_get_network_type())
            self.network_type_update_count = 30

    def destroy_and_callback(self):
        self.valid = False
        C_file.set_fileloader_enable('week', True)
        C_file.reload_file_system()
        game3d.delay_exec(100, self.delay_destroy_and_callback)

    def delay_destroy_and_callback(self):
        if hasattr(patch_utils, 'save_patched_log'):
            patch_utils.save_patched_log()
        package_utils.modify_package_info()
        self.destroy_logic()
        if self._platform_name == game3d.PLATFORM_WIN32:
            import os
            bin_patch_path = game3d.get_root_dir() + '\\bin_patch'
            has_new_bin_patch = os.path.exists(bin_patch_path)
            if has_new_bin_patch:
                if os.listdir(bin_patch_path):
                    bin_launcher_path = game3d.get_root_dir() + '\\..\\launcher.exe'
                    has_bin_launcher = os.path.exists(bin_launcher_path)
                    if has_bin_launcher:
                        try:
                            bin_channel = patch_dctool.get_dctool_instane().pc_engine_channel_name
                            bin_patch_launcher = os.path.join(bin_patch_path, bin_channel, 'launcher.exe')
                            if os.path.exists(bin_patch_launcher):
                                import shutil
                                shutil.copy(bin_patch_launcher, bin_launcher_path)
                                os.remove(bin_patch_launcher)
                        except Exception as e:
                            print('[ERROR] bin_patch_launcher path is wrong! {}'.format(str(e)))

                        package_utils.write_bin_patch_flag()
                        game3d.open_url(bin_launcher_path)
                        return
                else:
                    os.rmdir(bin_patch_path)
        try:
            if not patch_utils.is_support_base_package():
                from patch import patch_announce
                patch_announce.destroy_patch_announce_instance()
                if self.widget:
                    self.set_percent(100)
                    text = get_patch_text_id(337)
                    self.widget.lab_download_info.setString(text)
                    self.widget.lab_download_prog.setString('')
            if self.widget:
                self.widget.btn_repair.setVisible(False)
                self.widget.btn_feedback.setVisible(False)
                self.widget.btn_notice.setVisible(False)
        except Exception as e:
            print('[PATCH] destroy patch announce except:', str(e))

        if self.finished_callback:
            self.finished_callback()

    def on_click_repair_btn(self, w, e):
        if self.new_package_reverting:
            return
        if self._is_pause:
            return
        if not self.valid:
            return
        if e != ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            return
        self._is_pause = True
        text = get_patch_text_id(90002)

        def ok_cb():
            with self.downloader.lock:
                self.downloader.stop_downloader()
                ret = self.revert_game()
                if not ret:
                    self._is_pause = False

        def cancel_cb():
            self._is_pause = False

        game3d.show_msg_box(text, get_patch_text_id(90001), ok_cb, cancel_cb, get_patch_text_id(90003), get_patch_text_id(90005))

    def on_click_feedback_btn(self, w, e):
        if e == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            from logic.comsys.feedback import echoes
            echoes.show_feedback_view(echoes.PATCH)

    def _on_click_btn_notice(self, w, e):
        try:
            if not self.valid:
                return
            if e != ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
                return
            if patch_const.ENABLE_PATCH_ANNOUNCE:
                from . import patch_announce
                patch_announce.get_patch_announce_instance()
        except Exception as e:
            print('[PATCH] click notice except:', str(e))

    def _create_bg_ui(self, scene, design_size):
        try:
            if six.moves.builtins.__dict__.get('PATCH_BG_LAYER', None) is not None:
                return
            bg_layer = ccui.Layout.create()
            bg_layer.setAnchorPoint(cc.Vec2(0.5, 0.5))
            bg_layer.setContentSize(cc.Size(design_size.width, design_size.height))
            bg_layer.setPosition(cc.Vec2(design_size.width * 0.5, design_size.height * 0.5))
            bg_layer.setOpacity(255)
            bg_layer.setBackGroundColorType(1)
            bg_layer.setBackGroundColor(cc.Color3B(0, 0, 0))
            scene.addChild(bg_layer, 0)
            six.moves.builtins.__dict__['PATCH_BG_LAYER'] = bg_layer
        except Exception as e:
            print('[PATCH] create bg ui except:', str(e))

        return

    def _show_discrete_info(self):
        try:
            discrete_dl_num, zip_dl_num = self.downloader.get_download_num_info()
            print('dl: {} {}'.format(discrete_dl_num, zip_dl_num))
            if self._platform_name != game3d.PLATFORM_WIN32 and discrete_dl_num > 8000 and not hasattr(self.widget, 'discrete_num_node'):
                show_text = get_patch_text_id(90144)
                director = cc.Director.getInstance()
                view = director.getOpenGLView()
                vsize = view.getVisibleSize()
                label_node = cc.Label.createWithTTF(show_text, 'gui/fonts/fzdys.ttf', 18, cc.Size(980, 0), cc.TEXTHALIGNMENT_CENTER, cc.TEXTVALIGNMENT_TOP)
                label_node.setPosition(cc.Vec2(vsize.width / 2.0, vsize.height - 2))
                label_node.setColor(cc.Color3B(255, 255, 255))
                label_node.setAnchorPoint(cc.Vec2(0.5, 1))
                self.widget.addChild(label_node, 2)
                setattr(self.widget, 'discrete_num_node', label_node)
                bar_img = cc.Sprite.create('gui/patch_ui/uires/pnl_normal.png')
                org_size = bar_img.getContentSize()
                bar_img.setScale(1500 / org_size.width, (label_node.getContentSize().height + 4) / org_size.height)
                bar_img.setAnchorPoint(cc.Vec2(0.5, 1))
                bar_img.setPosition(cc.Vec2(vsize.width / 2.0, vsize.height))
                self.widget.addChild(bar_img, 1)
        except Exception as e:
            print('[PATCH] show discrete info except:', str(e))