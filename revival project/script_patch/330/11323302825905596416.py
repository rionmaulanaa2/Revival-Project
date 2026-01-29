# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/ext_package/ext_patch_ui.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import time
import json
import queue
import random
import social
import C_file
import render
import game3d
import six.moves.builtins
import package_utils
from . import ext_package_utils
from cocosui import cc, ccui, ccs
from patch import revert
from patch import patch_utils
from patch import network_utils
from patch import patch_const
from patch.patch_lang import get_patch_text_id
from patch.patch_dctool import get_dctool_instane
from ext_package import ext_package_manager
from ext_package import ext_package_const as ext_c
from .ext_package_utils import cout_info, cout_error
LOG_CHANNEL = 'ext_patch'
RETRY_TIMES = 3
NPK_RETRY_TIMES = 3

class ExtPatchUI(object):
    instance = None

    def __init__(self, finished_callback):
        super(ExtPatchUI, self).__init__()
        self._is_pause = False
        self._spd_modify_time = 0
        self._space_up_time = 0
        self._cnt_state = patch_utils.DST_INIT
        self._platform_name = game3d.get_platform()
        self._cnt_image_widget = None
        self._replace_image_widget = None
        self._last_image_replace_time = time.time()
        self._last_select_image_id = None
        self._last_reset_winsize_time = 0
        self._download_start_time = 0
        self._frame = 0
        self._drpf_up_time = time.time()
        self._retry_count = 0
        self._init_failed_count = 0
        self.spd_modify_time = 0
        self.widget = None
        self._valid = True
        self._img_bg_config = None
        self._ret_queue = queue.Queue()
        self._err_queue = queue.Queue()
        self._msg_queue = queue.Queue()
        self._last_update_check_time = 0
        self._last_check_count = 0
        self._is_real_ext_package = ext_package_utils.is_real_ext_package()
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        self._finished_callback = finished_callback
        self._ext_mgr = ext_package_manager.get_ext_package_instance()
        self._init_widget()
        return

    def _init_widget(self):
        cout_info(LOG_CHANNEL, 'real_ext_package:{} using:{}'.format(self._is_real_ext_package, self._using_ext_info))
        self._replace_patch_ui_instance()
        self._download_start_time = 0
        if self._platform_name == game3d.PLATFORM_WIN32:
            is_enable_orbit = False
        else:
            channel = social.get_channel()
            is_enable_orbit = channel.is_downloader_enable()
        self._ext_mgr.init_ext_patch_downloader_agent(is_enable_orbit, self._ret_queue, self._err_queue, self._msg_queue)
        self._create_ui()
        self._start_logic()

    def _start_logic(self):
        self.init_ext_patch(False)

    def logic(self):
        self._update_logs()
        if self._is_pause or revert.REVERTING:
            return
        while 1:
            try:
                callback, args = self._ret_queue.get_nowait()
                callback(*args)
            except queue.Empty:
                break

        if self.widget:
            self._update_prog_and_info()
            self._replace_bg()
            self._reset_resolution()
            self._update_space()

    def calc_estimate_download_prog(self):
        estimate_download_time = 30
        cnt_time = time.time()
        download_start_time = self._ext_mgr.ext_patch_downloader_agent.download_start_time
        estimate_prog = int((cnt_time - download_start_time) * 100.0 / estimate_download_time)
        return estimate_prog

    def _update_prog_and_info(self):
        manager_state = self._ext_mgr.get_state()
        state_text_id_map = {ext_c.EXT_STATE_DOWNLOAD_NPK_LIST: 203,
           ext_c.EXT_STATE_DL_EXT_NAMES: 203,
           ext_c.EXT_STATE_CONFIG_ANALYZE: 203,
           ext_c.EXT_STATE_DL_MISSING_EXT_CONFIG: 204,
           ext_c.EXT_STATE_DL_MISSING_EXT_NPK: 209,
           ext_c.EXT_STATE_VERIFYING_EXT_NPK: 205,
           ext_c.EXT_STATE_PATCH_INFO_ANALYZE: 335,
           ext_c.EXT_STATE_PATCH_ANALYZE_ZIP: 335,
           ext_c.EXT_STATE_PATCH_DOWNLOADING: 210,
           ext_c.EXT_STATE_PATCH_COPYING: 336
           }
        cur_time = time.time()
        if cur_time - self._last_update_check_time > 0.8:
            self._last_update_check_time = cur_time
            text_id = state_text_id_map.get(manager_state, 90023)
            text = get_patch_text_id(text_id)
            text += '.' * (self._last_check_count % 5)
            self._last_check_count += 1
            if self._valid:
                self.widget.lab_download_info.setString(text)
        prog, need_prog = self._ext_mgr.get_progress()
        prog = int(prog * 100)
        prog = min(100, prog)
        self._set_percent(prog)
        if self._ext_mgr.get_is_downloading() or self._valid:
            if manager_state == ext_c.EXT_STATE_PATCH_NPK_UPDATE:
                text = get_patch_text_id(90139, prog) if prog > 0 else get_patch_text_id(90023)
                self.widget.lab_download_prog.setString(text)
            elif manager_state == ext_c.EXT_STATE_PATCH_NPK_VERIFY:
                if prog > 0:
                    text = get_patch_text_id(90140, prog) if 1 else get_patch_text_id(90023)
                    self.widget.lab_download_prog.setString(text)
                else:
                    self._hide_prog_info_ui()
        elif manager_state not in (ext_c.EXT_STATE_DL_MISSING_EXT_NPK, ext_c.EXT_STATE_PATCH_DOWNLOADING):
            self._hide_prog_info_ui()
        else:
            speed, total_size = self._ext_mgr.get_speed_and_size()
            cnt_time = time.time()
            if cnt_time - self.spd_modify_time > 1.0:
                self.spd_modify_time = cnt_time
                unit = 'MB'
                if speed < 0.1:
                    speed = speed * 1024
                    unit = 'KB'
                total_size_mb = total_size * 1.0 / 1048576.0
                total_size_mb = max(0.1, total_size_mb)
                downloaded_size_mb = total_size_mb * (prog * 1.0 / 100)
                if speed > 0:
                    text = get_patch_text_id(90021, prog, downloaded_size_mb, total_size_mb, speed, unit)
                else:
                    text = get_patch_text_id(90020, prog, downloaded_size_mb, total_size_mb)
                self.widget.lab_download_prog.setString(text)
                if cnt_time - self._drpf_up_time > patch_const.PACKAGE_DRPF_UP_TIME:
                    self._drpf_up_time = cnt_time
                    self._drpf('ExtProg', {'total_size': total_size_mb,'ext_patch_prog': prog})

    def _update_logs(self):
        while self._err_queue.qsize() > 0:
            err = self._err_queue.get()
            patch_utils.send_script_error('{} error:{}'.format(ext_c.DRFP_ERROR_CHANNEL, err))
            cout_error(LOG_CHANNEL, err)

        msg_queue_log_limit = 3000
        cnt_count = 0
        while self._msg_queue.qsize() > 0:
            msg = self._msg_queue.get()
            cout_info(LOG_CHANNEL, msg)
            cnt_count += 1
            if msg_queue_log_limit <= cnt_count:
                break

    def _make_sure_init_success(self):
        self._using_ext_info = ext_package_utils.get_using_ext_info()
        all_config = ext_package_utils.get_ext_package_config_v2()
        if self._using_ext_info is None or all_config is None:
            cout_error(LOG_CHANNEL, 'init_error, using:{} all:{}'.format(self._using_ext_info, all_config))
            return False
        else:
            return True

    def init_ext_patch(self, need_confirm=True):
        cout_info(LOG_CHANNEL, 'start ext patch')
        self._set_percent(100)
        self._hide_prog_info_ui()
        if need_confirm:
            self._retry_count = 0
        if not ext_package_utils.create_extend_folder():
            revert.revert_to_original_version_noerror()
            return
        if not self._make_sure_init_success():
            self._init_failed_count += 1
            if self._init_failed_count > RETRY_TIMES:
                self._init_failed_count = 0
                game3d.show_msg_box(get_patch_text_id(90142), get_patch_text_id(90013), game3d.exit, self.init_ext_patch, get_patch_text_id(90013), get_patch_text_id(90010))
            else:
                game3d.delay_exec(2000, self.init_ext_patch)
            return
        self._ext_mgr.update_config()
        if network_utils.g93_get_network_type() != network_utils.TYPE_INVALID:
            if self._is_real_ext_package and self._using_ext_info:
                self._drpf('NPK_1', {'using': self._using_ext_info,'msg': 'begin npk logic'})
                cout_info(LOG_CHANNEL, '[NPK] 1: download npk list')
                self._ext_mgr.download_ext_npk_list(self._ext_npk_list_download_callback)
            else:
                self._analyze_ext_patch_info()
        else:
            self._ret_queue.put((self._ext_npk_list_download_callback, (ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_ERROR,)))

    def _ext_npk_list_download_callback(self, state):
        if state == ext_c.EXT_STATE_DOWNLOAD_NPK_LIST_FINISHED:
            if len(self._ext_mgr.get_ext_npk_list_info()) == 0:
                self._err_log('[NPK] 1: has no extend npk list')
                game3d.frame_delay_exec(1, self.destroy_and_callback)
            else:
                cout_info(LOG_CHANNEL, '[NPK] 1: npk list dl success')
                game3d.frame_delay_exec(1, self._analyze_ext_npk)
        else:
            cout_info(LOG_CHANNEL, '[NPK] 1: npk list dl error')
            self._show_retry_confirm_box()

    def _analyze_ext_npk(self):
        cout_info(LOG_CHANNEL, '[NPK] 2: analyze ext npk')
        self._drpf('NPK_2', {'msg': 'analyze_ext_npk'})
        self._ext_mgr.ext_npk_config_analyze(self._ext_npk_analyze_callback)

    def _ext_npk_analyze_callback(self, state):
        if state == ext_c.EXT_STATE_CONFIG_ANALYZE_FINISHED:
            if len(self._ext_mgr.get_active_ext_name_lst()) == 0:
                self._err_log('[NPK] 2: has using but active ext is empty')
                game3d.frame_delay_exec(1, self.destroy_and_callback)
            else:
                self._retry_count = 0
                game3d.frame_delay_exec(1, self._analyze_ext_patch_info)
        elif state == ext_c.EXT_STATE_DL_MISSING_EXT_NPK_FAILED:
            cout_info(LOG_CHANNEL, '[NPK] 2: analyze ext config failed')
            self._show_retry_confirm_box(ok_cb=self._ext_mgr.download_missing_npk, text_id=208)
        elif state == ext_c.EXT_STATE_ADD_RES_NPK_FAILED:
            cout_info(LOG_CHANNEL, '[NPK] 2: add npk failed')
            self._show_retry_confirm_box(ok_cb=self._analyze_ext_npk, text_id=90143)
        else:
            cout_info(LOG_CHANNEL, '[NPK] 2: ext analyze error, show confirm box')
            self._show_retry_confirm_box(ok_cb=self._analyze_ext_npk)

    def _analyze_ext_patch_info(self):
        cout_info(LOG_CHANNEL, '[PATCH] 1:analyze ext patch info')
        self._drpf('PATCH_1', {'msg': 'analyze_ext_patch_info'})
        self._ext_mgr.ext_patch_info_analyze(self._ext_patch_analyze_callback)

    def _ext_patch_analyze_callback(self, state):
        self._ret_queue.put((self._do_ext_patch_analyze_info_callback, (state,)))

    def _do_ext_patch_analyze_info_callback(self, state):
        if state == ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED:
            cout_info(LOG_CHANNEL, '[PATCH] 1: dl flist failed')
            self._show_retry_confirm_box(ok_cb=self._analyze_ext_patch_info)
        else:
            if self._ext_mgr.ext_patch_size == 0:
                cout_info(LOG_CHANNEL, '[PATCH] end: size is zero')
                self._drpf('PATCH_END', {'msg': 'size is zero'})
                game3d.frame_delay_exec(1, self.destroy_and_callback)
                return
            if patch_const.ENABLE_ZIP_DOWNLOAD:
                self.analyze_ext_zip_config()
            else:
                self._start_download_ext_patch()

    def analyze_ext_zip_config(self):
        cout_info(LOG_CHANNEL, '[PATCH] 2:analyze ext zip config')
        self._drpf('PATCH_2', {'msg': 'analyze_ext_zip_config'})
        self._ext_mgr.ext_patch_zip_config_analyze(self._analyze_ext_zip_config_cb)

    def _analyze_ext_zip_config_cb(self, state):
        self._ret_queue.put((self._do_analyze_ext_zip_config_cb, (state,)))

    def _do_analyze_ext_zip_config_cb(self, state):
        if state == ext_c.EXT_STATE_PATCH_ANALYZE_ZIP_FINISH:
            cout_info(LOG_CHANNEL, '[PATCH] 2:analyze ext zip config success')
            self._start_download_ext_patch()
        else:
            cout_error(LOG_CHANNEL, '[PATCH] 2:analyze ext zip config failed')
            self._show_retry_confirm_box(ok_cb=self.analyze_ext_zip_config)

    def _start_download_ext_patch(self):
        self._retry_count = 0
        cout_info(LOG_CHANNEL, '[PATCH] 3:start download ext patch')
        self._drpf('PATCH_3', {'msg': 'start_download_ext_patch'})
        self._download_start_time = time.time()
        self._init_prog_ui()
        self._show_prog_info_ui()
        self._ext_mgr.download_ext_patch(self._download_ext_patch_finish_cb)

    def _download_ext_patch_finish_cb(self, state):
        self._ret_queue.put((self._on_download_ext_patch_finish_callback, (state,)))

    def _on_download_ext_patch_finish_callback(self, state):
        space_flag = self._ext_mgr.get_patch_space_flag()
        if state == ext_c.EXT_STATE_PATCH_DOWNLOADED_FAILED:
            cout_error(LOG_CHANNEL, 'download ext patch failed')

            def retry_func(need_confirm=True):
                self.init_ext_patch(need_confirm)

            def ok_func():
                self._drpf('PATCH_3_0', {'msg': 'retry ext patch','space_flag': space_flag})
                retry_func(True)

            def cancel_func():
                self._drpf('PATCH_3_2', {'msg': 'cancel confirm and exit game','space_flag': space_flag})
                game3d.exit()

            if space_flag:
                patch_utils.show_confirm_box(ok_func, cancel_func, get_patch_text_id(90056), get_patch_text_id(90010), get_patch_text_id(90013))
            else:
                self._retry_count += 1
                if self._retry_count > RETRY_TIMES:
                    patch_utils.show_confirm_box(ok_func, cancel_func, get_patch_text_id(90012), get_patch_text_id(90010), get_patch_text_id(90013))
                else:
                    self._drpf('PATCH_3_1', {'msg': 'download_ext_patch_failed, then retry'})
                    retry_func(False)
            self.check_network()
        else:
            self._drpf('PATCH_END', {'msg': 'download ext patch success'})
            cout_info(LOG_CHANNEL, 'download ext patch success')
            C_file.reload_file_system()
            game3d.frame_delay_exec(1, self.destroy_and_callback)

    def _create_ui(self):
        scene = self._init_resolution()
        reader = ccs.GUIReader.getInstance()
        widget = reader.widgetFromJsonFile('gui/patch_ui/patch.json')
        widget = patch_utils.normalize_widget(widget)
        scene.addChild(widget, patch_utils.PATCH_UI_LAYER)
        self.widget = widget
        self._init_ui(scene, widget)
        self._init_version()
        render.logic = self.logic
        render.set_logic(self.logic)

    def _init_ui(self, scene, widget):
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        v_size = view.getVisibleSize()
        image_bg_size = widget.image_bg.getContentSize()
        try:
            width_ratio = v_size.width / image_bg_size.width
            height_ratio = v_size.height / image_bg_size.height
        except Exception as e:
            print('[ext_patch_ui] cal ratio except:', str(e))
            width_ratio = v_size.width / 1624.0
            height_ratio = v_size.height / 750.0

        max_ratio = max(width_ratio, height_ratio)
        widget.image_bg.setScale(max_ratio)
        content_size = widget.pnl_prog.img_buttom.getContentSize()
        content_size.width = v_size.width
        widget.pnl_prog.img_buttom.setContentSize(content_size)
        prog_ratio = 0.9
        text_ratio = (1 - prog_ratio) * 0.5
        content_size = widget.prog_download.getContentSize()
        content_size.width = v_size.width * prog_ratio
        widget.prog_download.setContentSize(content_size)
        content_size = widget.img_prog_bg.getContentSize()
        content_size.width = v_size.width * prog_ratio
        widget.img_prog_bg.setContentSize(content_size)
        margin = widget.lab_download_info.getLayoutParameter().getMargin()
        margin.left = text_ratio * v_size.width
        widget.lab_download_info.getLayoutParameter().setMargin(margin)
        margin = widget.lab_download_prog.getLayoutParameter().getMargin()
        margin.right = text_ratio * v_size.width
        widget.lab_download_prog.getLayoutParameter().setMargin(margin)
        margin = widget.lab_version.getLayoutParameter().getMargin()
        margin.left = text_ratio * v_size.width
        widget.lab_version.getLayoutParameter().setMargin(margin)
        widget.btn_repair.lab_repair.setString(get_patch_text_id(90003))
        widget.btn_feedback.lab_feedback.setString(get_patch_text_id(80140))
        widget.prog_download.setPercent(100)
        widget.lab_download_info.setString('')
        try:
            widget.lab_memory.setString('')
            margin = widget.lab_memory.getLayoutParameter().getMargin()
            margin.left = text_ratio * v_size.width
            widget.lab_memory.getLayoutParameter().setMargin(margin)
            widget.btn_notice.lab_notice.setString(get_patch_text_id(80161))
        except Exception as e:
            pass

        self.udpate_strange_screen_pos(widget, v_size)
        try:
            widget.btn_repair.addTouchEventListener(self.on_click_repair_btn)
            widget.btn_feedback.addTouchEventListener(self.on_click_feedback_btn)
            widget.btn_notice.addTouchEventListener(self._on_click_btn_notice)
        except Exception as e:
            cout_error(LOG_CHANNEL, 'add touch event except:{}'.format(str(e)))

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

    def _init_version(self):
        ver_str = self._ext_mgr.get_cur_ver_str()
        text = get_patch_text_id(90006, ver_str)
        self.widget.lab_version.setString(text)

    def _init_prog_ui(self):
        self._set_percent(100)
        self.widget.lab_download_prog.setString(get_patch_text_id(90018))

    def _init_resolution(self):
        director = cc.Director.getInstance()
        scene = director.getRunningScene()
        if not scene:
            scene = cc.Scene.create()
            director.runWithScene(scene)
        view = director.getOpenGLView()
        real_size = view.getFrameSize()
        if real_size.width / real_size.height > 1136.0 / 640:
            fit_policy = cc.RESOLUTIONPOLICY_FIXED_HEIGHT
        else:
            fit_policy = cc.RESOLUTIONPOLICY_FIXED_WIDTH
        view.setDesignResolutionSize(1136, 640, fit_policy)
        try:
            width, height, depth, windowType, multi_sample = game3d.get_window_size()
            if hasattr(game3d, 'set_window_size_force'):
                game3d.set_window_size_force(width, height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(width, height, 32, 1, 0, False)
            else:
                game3d.set_window_size(width, height, 32, 1, 0, False)
            print('set window size', width, height)
        except:
            pass

        return scene

    def _reset_resolution(self):
        try:
            if not self._last_reset_winsize_time:
                self._last_reset_winsize_time = time.time()
            cnt_time = time.time()
            if cnt_time - self._last_reset_winsize_time < 20:
                return
            self._last_reset_winsize_time = cnt_time
            width, height, depth, windowType, multisample = game3d.get_window_size()
            if hasattr(game3d, 'set_window_size_force'):
                game3d.set_window_size_force(width, height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(width, height, 32, 1, 0, False)
            else:
                game3d.set_window_size(width, height, 32, 1, 0, False)
            print('reset window size', width, height)
        except Exception as e:
            patch_utils.send_script_error('[reset_resolution] ' + str(e))

    def _set_percent(self, p):
        self.widget.prog_download.setPercent(p)

    def on_click_feedback_btn(self, w, e):
        if e == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            from logic.comsys.feedback import echoes
            echoes.show_feedback_view(echoes.PATCH)

    def _on_click_btn_notice(self, w, e):
        try:
            if self._is_pause:
                return
            if not self._valid:
                return
            if e != ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
                return
            if patch_const.ENABLE_PATCH_ANNOUNCE:
                from patch import patch_announce
                patch_announce.get_patch_announce_instance()
        except:
            pass

    def on_click_repair_btn(self, w, e):
        if self._is_pause:
            return
        if not self._valid:
            return
        if e != ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            return
        self._is_pause = True
        text = get_patch_text_id(90026)

        def ok_cb():
            self._ext_mgr.stop_patch_downloader()
            ret = self.revert_game()
            if not ret:
                self._is_pause = False

        def cancel_cb():
            self._is_pause = False

        game3d.show_msg_box(text, get_patch_text_id(90001), ok_cb, cancel_cb, get_patch_text_id(90003), get_patch_text_id(90005))

    def _show_prog_info_ui(self):
        self.widget.lab_download_prog.setVisible(True)

    def _hide_prog_info_ui(self):
        self.widget.lab_download_prog.setString('')

    def _update_space(self):
        try:
            now_time = time.time()
            if now_time - self._space_up_time < patch_const.SPACE_UP_TIME:
                return
            self._space_up_time = now_time
            mega_bytes = ext_package_utils.get_left_available_space()
            if mega_bytes >= 0:
                pre_text = get_patch_text_id(353)
                if mega_bytes > 1024:
                    mem_txt = '{}:{:.1f}G'.format(pre_text, mega_bytes / 1024.0)
                else:
                    mem_txt = '{}:{}MB'.format(pre_text, int(mega_bytes))
                self.widget.lab_memory.setString(mem_txt)
            else:
                self.widget.lab_memory.setString('')
        except Exception as e:
            cout_error(LOG_CHANNEL, 'update space exception:{}'.format(str(e)))

    def get_image_bg_config(self):
        try:
            if not self._img_bg_config:
                self._img_bg_config = json.loads(C_file.get_res_file('confs/patch_bg_img_config.json', ''))
        except:
            self._img_bg_config = {}

        return self._img_bg_config

    def _replace_bg(self):
        try:
            cnt_time = time.time()
            if cnt_time - self._last_image_replace_time < 10:
                return
            self._last_image_replace_time = cnt_time
            img_config = self.get_image_bg_config()
            if not img_config:
                return
            replace_image_id = random.choice(six_ex.keys(img_config))
            if replace_image_id == self._last_select_image_id:
                return
            self._last_select_image_id = replace_image_id
            replace_image = img_config[replace_image_id]
            if not C_file.find_res_file(replace_image, ''):
                if self._platform_name in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID) and replace_image.endswith('.png'):
                    platform_img = replace_image[:-4] + '.ktx'
                    if not C_file.find_res_file(platform_img, ''):
                        return
                else:
                    return
            widget = self.widget
            if not self._replace_image_widget:
                self._replace_image_widget = widget.image_bg.clone()
                self._cnt_image_widget = widget.image_bg
                self.widget.addChild(self._replace_image_widget, 1)
            self._cnt_image_widget.stopAllActions()
            self._replace_image_widget.stopAllActions()
            self._replace_image_widget.loadTexture(replace_image)
            director = cc.Director.getInstance()
            view = director.getOpenGLView()
            vsize = view.getVisibleSize()
            image_bg_size = self._replace_image_widget.getContentSize()
            width_ratio = vsize.width / image_bg_size.width
            height_ratio = vsize.height / image_bg_size.height
            max_ratio = max(width_ratio, height_ratio)
            self._replace_image_widget.setScale(max_ratio)
            self._replace_image_widget.setOpacity(0)
            self._cnt_image_widget.setOpacity(255)
            fadein_action = cc.FadeTo.create(1.0, 255)
            fadeout_action = cc.FadeTo.create(1.0, 0)
            self._cnt_image_widget.runAction(fadeout_action)
            self._replace_image_widget.runAction(fadein_action)
            temp_widget = self._replace_image_widget
            self._replace_image_widget = self._cnt_image_widget
            self._cnt_image_widget = temp_widget
        except Exception as e:
            cout_error(LOG_CHANNEL, 'replace_bg except:{}'.format(str(e)))

    def _err_log(self, error_msg):
        cout_error(LOG_CHANNEL, error_msg)
        patch_utils.send_script_error('{} {}'.format(ext_c.DRFP_ERROR_CHANNEL, error_msg))

    def _show_retry_confirm_box(self, ok_cb=None, text_id=90042, need_check_net=True):
        space_flag = self._ext_mgr.get_patch_space_flag()

        def ok_func():
            if ok_cb:
                game3d.delay_exec(30, ok_cb)
            else:
                game3d.delay_exec(30, self.init_ext_patch, (False,))

        def cancel_func():
            self._drpf('ExtCancelConfirm', {'space_flag': space_flag})
            game3d.exit()

        self._retry_count += 1
        if self._retry_count > RETRY_TIMES:
            self._retry_count = 0
            if space_flag:
                text_id = 90056
            hint_text = get_patch_text_id(text_id)
            patch_utils.show_confirm_box(ok_func, cancel_func, hint_text, get_patch_text_id(90010), get_patch_text_id(90013))
        else:
            ok_func()
        if need_check_net:
            self.check_network()

    def check_network(self):

        def confirm_go_to_setting():
            game3d.go_to_setting()

        def cancel_go_to_setting():
            pass

        if self._platform_name == game3d.PLATFORM_IOS:
            if network_utils.g93_get_network_auth() == network_utils.AUTH_RESTRICT:
                patch_utils.show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, get_patch_text_id(3112), get_patch_text_id(80284), get_patch_text_id(19002))
                return False
        return True

    def revert_game(self):
        self._hide_prog_info_ui()
        package_utils.reset_package_info()
        self.widget.lab_download_info.setString(get_patch_text_id(90037))
        if self._platform_name == game3d.PLATFORM_WIN32:
            game3d.restart()
        game3d.exit()

    def _replace_patch_ui_instance(self):
        prev_patch_ui = six.moves.builtins.__dict__.get('PATCH_UI_INSTANCE', None)
        if prev_patch_ui:
            try:
                prev_patch_ui.destroy()
            except Exception as e:
                cout_error(LOG_CHANNEL, 'replace patch ui with exception:{}'.format(str(e)))

        six.moves.builtins.__dict__['PATCH_UI_INSTANCE'] = self
        return

    def _drpf(self, type_name, info):
        tool_inst = get_dctool_instane()
        if hasattr(tool_inst, 'ext_drpf_info'):
            tool_inst.ext_drpf_info(type_name, info)

    def _end_patch(self):
        if self._ext_mgr:
            self._ext_mgr.destroy_data()
            self._ext_mgr.destroy_callback()
        from patch import patch_path
        patch_path.remove_patch_temp_folder()
        try:
            if self.widget:
                text = get_patch_text_id(337)
                self._set_percent(100)
                self.widget.lab_download_info.setString(text)
                self.widget.lab_download_prog.setVisible(False)
                self.widget.btn_repair.setVisible(False)
                self.widget.btn_feedback.setVisible(False)
                self.widget.btn_notice.setVisible(False)
        except Exception as e:
            cout_error(LOG_CHANNEL, 'end patch except:{}'.format(str(e)))

    def destroy(self):
        if self.widget:
            self.widget.removeFromParent()
        self.widget = None
        self._ext_mgr = None
        return

    def _destroy_logic(self):
        render.logic = None
        render.set_logic(None)
        return

    def destroy_and_callback(self):
        try:
            from patch import patch_announce
            patch_announce.destroy_patch_announce_instance()
        except Exception as e:
            print('[PATCH] destroy patch announce except:', str(e))

        self._destroy_logic()
        self._end_patch()
        self._valid = False
        if self._finished_callback:
            self._finished_callback()
        self._finished_callback = None
        return