# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_aab.py
from __future__ import absolute_import
from __future__ import print_function
import time
import render
import game3d
import social
import playassetdelivery
from cocosui import cc, ccs
from patch import patch_dctool
from patch.patch_lang import get_patch_text_id
from .patch_utils import PATCH_UI_LAYER, normalize_widget
M_BYTES = 1048576.0
DOWNLOAD_COMPLETED = playassetdelivery.SDK_DL_DOWNLOAD_COMPLETED
DOWNLOADING = playassetdelivery.SDK_DL_DOWNLOADING
WAITING_WIFI = playassetdelivery.SDK_DL_WAITING_FOR_WIFI
FAILED_DL_STATUS = (
 playassetdelivery.SDK_DL_INFO_FAILED, playassetdelivery.SDK_DL_DOWNLOAD_FAILED,
 playassetdelivery.SDK_DL_DOWNLOAD_CANCELED, playassetdelivery.SDK_DL_NOT_INSTALLED,
 playassetdelivery.SDK_DL_REMOVAL_FAILED)
PACK_ST_INSTALLED = playassetdelivery.AP_INSTALLED
PENDING_DL_STATUS = (
 playassetdelivery.SDK_DL_UNKNOWN, playassetdelivery.SDK_DL_DOWNLOAD_PENDING,
 playassetdelivery.SDK_DL_TRANSFERRING, playassetdelivery.SDK_DL_WAITING_FOR_WIFI,
 playassetdelivery.SDK_DL_INFO_PENDING, playassetdelivery.SDK_DL_REMOVAL_PENDING)
ERROR_LST = {playassetdelivery.SDK_AP_INSUFFICIENT_STORAGE: 177,
   playassetdelivery.SDK_AP_NETWORK_ERROR: 272,
   playassetdelivery.SDK_AP_ACCESS_DENIED: 265,
   playassetdelivery.SDK_AP_PLAY_STORE_NOT_FOUND: 266,
   playassetdelivery.SDK_AP_APP_UNAVAILABLE: 266
   }
DRPF_TIME = 20
REQUEST_DOWNLOAD_TIME = 6
NO_NEED_UP_ERRORS = (
 playassetdelivery.SDK_AP_INSUFFICIENT_STORAGE, playassetdelivery.SDK_AP_NETWORK_ERROR)

class AABPackageUI(object):

    def __init__(self, finished_callback):
        super(AABPackageUI, self).__init__()
        import six.moves.builtins
        six.moves.builtins.__dict__['aab_finish'] = False
        six.moves.builtins.__dict__['AAB_UI_INSTANCE'] = self
        self._finished_callback = finished_callback
        self._widget = None
        self._root_node = None
        self._uninstall_packs = []
        self._all_pack_completed = False
        self._last_reset_win_size_time = 0
        self._last_drpf_time = 0
        self._last_logic_time = 0
        self._last_rq_dl_time = time.time()
        self._last_record_mb = 0
        self._last_record_time = time.time()
        self._prog_decorate_nd = None
        self._prog_nd_width = 672
        self._init_play_asset()
        return

    def _init_play_asset(self):
        from . import aab_listener
        aab_listener.listen_aab()
        playassetdelivery.enable_auto_show_cellular_confirm(True)
        all_asset_pack_info = playassetdelivery.get_all_asset_pack_info()
        need_install_names = []
        if all_asset_pack_info:
            for asset_pack in all_asset_pack_info:
                pack_state = asset_pack.state
                pack_name = asset_pack.name
                down_state = asset_pack.download_state
                error_reason = asset_pack.error_reason
                print('[AABPackageUI] init_play_asset:', pack_name, asset_pack.type, pack_state, down_state, error_reason, asset_pack.path, asset_pack.total_bytes, asset_pack.downloaded_bytes)
                if down_state != DOWNLOAD_COMPLETED:
                    self._uninstall_packs.append(pack_name)
                    if pack_state == playassetdelivery.AP_UNINSTALLED:
                        need_install_names.append(pack_name)

        for pack_name in need_install_names:
            print('[AABPackageUI] install asset pack:', pack_name, playassetdelivery.install_asset_pack(pack_name))

        def init_sdk_callback(*args):
            channel.init_sdk_callback = None
            self._create()
            return

        channel = social.get_channel()
        if channel.is_init:
            self._create()
        else:
            channel.init_sdk_callback = init_sdk_callback

    def _create(self):
        patch_dctool.get_dctool_instane().send_activation_info()
        patch_dctool.get_dctool_instane().send_aab_begin_info()
        if not self._uninstall_packs:
            info_dict = {'aab_info': 'all pack is download completed state, then patch'}
            patch_dctool.get_dctool_instane().send_aab_stage_info(info_dict)
            self._all_pack_completed = True
            print('quite aab in create')
            self.quite_aab()
            return
        try:
            from patch.patch_lang import get_multi_lang_instane
            get_multi_lang_instane()
        except:
            pass

        scene = self._init_resolution()
        reader = ccs.GUIReader.getInstance()
        widget = reader.widgetFromJsonFile('gui/patch_ui/patch_aab.json')
        widget = normalize_widget(widget)
        scene.addChild(widget, PATCH_UI_LAYER)
        self._widget = widget
        self._init_ui(scene, widget)
        render.logic = self._logic
        render.set_logic(self._logic)

    def _init_ui(self, scene, widget):
        try:
            director = cc.Director.getInstance()
            view = director.getOpenGLView()
            v_size = view.getVisibleSize()
            self._root_node = widget.image_bg
            root_size = self._root_node.getContentSize()
            width_ratio = v_size.width / root_size.width
            height_ratio = v_size.height / root_size.height
            max_ratio = min(width_ratio, height_ratio)
            self._root_node.setScale(max_ratio)
            self._root_node.lab_name.setString(get_patch_text_id(1111))
            self._root_node.lab_data_packet.setString(get_patch_text_id(264))
            self._root_node.lab_desc.setString(get_patch_text_id(268))
            self._root_node.prog_download.setPercent(0)
            self._root_node.lab_download.setString(get_patch_text_id(235))
            self._root_node.lab_progress.setString('')
            self._init_event(self._root_node)
        except:
            self._root_node = None

        try:
            self._prog_decorate_nd = self._root_node.prog_download.img_news_keychain
            self._prog_nd_width = self._root_node.prog_download.getContentSize().width
        except:
            pass

        return

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

    def _logic(self):
        if self._widget:
            self._reset_resolution()
        if self._all_pack_completed:
            return
        if time.time() - self._last_logic_time < 1:
            return
        self._last_logic_time = time.time()
        finished = True
        all_downloaded_bytes = 0
        all_total_bytes = 0
        is_requesting_data = False
        is_downloading = False
        suspend_by_wifi = False
        download_false = False
        error_code_lst = set()
        all_asset_pack_info = playassetdelivery.get_all_asset_pack_info()
        download_states = []
        download_fail_packs = []
        if all_asset_pack_info:
            for asset_pack in all_asset_pack_info:
                download_state = asset_pack.download_state
                download_states.append(download_state)
                if not (download_state == DOWNLOAD_COMPLETED and asset_pack.state == PACK_ST_INSTALLED):
                    finished = False
                pack_total_bytes = asset_pack.total_bytes
                all_total_bytes += pack_total_bytes
                all_downloaded_bytes += asset_pack.downloaded_bytes
                if download_state == DOWNLOADING:
                    is_downloading = True
                elif download_state == WAITING_WIFI:
                    suspend_by_wifi = True
                elif download_state in PENDING_DL_STATUS:
                    is_requesting_data = True
                elif download_state in FAILED_DL_STATUS:
                    download_fail_packs.append(asset_pack.name)
                    download_false = True
                sdk_error_code = asset_pack.error_reason
                if sdk_error_code in ERROR_LST:
                    error_code_lst.add(sdk_error_code)

        if is_downloading:
            download_txt_id = 267
        elif suspend_by_wifi:
            download_txt_id = 236
        elif is_requesting_data:
            download_txt_id = 278
        elif download_false:
            download_txt_id = 269
        else:
            download_txt_id = 267
        if self._root_node and self._root_node.lab_download:
            self._root_node.lab_download.setString(get_patch_text_id(download_txt_id))
        error_txt_lst = []
        if error_code_lst:
            for error_code in error_code_lst:
                error_txt_lst.append(get_patch_text_id(ERROR_LST[error_code]))

        if error_txt_lst:
            error_txt = ';'.join(error_txt_lst) if 1 else ''
            if self._root_node and self._root_node.lab_error:
                self._root_node.lab_error.setString(error_txt)
            if download_fail_packs and time.time() - self._last_rq_dl_time > REQUEST_DOWNLOAD_TIME:
                for tmp_pack_name in download_fail_packs:
                    print('[AABPackageUI] request dl:', tmp_pack_name)
                    playassetdelivery.install_asset_pack(tmp_pack_name)

                self._last_rq_dl_time = time.time()
            need_hide = is_requesting_data and not is_downloading
            self._update_progress(all_downloaded_bytes, all_total_bytes, need_hide)
            if time.time() - self._last_drpf_time > DRPF_TIME:
                info_dict = {'aab_info': 'downloading:{0}-{1},error:{2},state:{3}'.format(all_downloaded_bytes, all_total_bytes, error_code_lst, download_states)}
                patch_dctool.get_dctool_instane().send_aab_stage_info(info_dict)
                self._last_drpf_time = time.time()
            return finished or None
        print('quit aab in logic')
        self.quite_aab()

    def _update_progress(self, downloaded_bytes, total_bytes, need_hide=False):
        if not self._widget:
            return
        try:
            if total_bytes > 0:
                progress_num = int(downloaded_bytes * 100.0 / total_bytes)
                progress_num = min(100, progress_num)
            else:
                progress_num = 100
            downloaded_size_mb = downloaded_bytes / M_BYTES
            total_m_bytes = total_bytes / M_BYTES
        except:
            progress_num = 100
            downloaded_size_mb = 0
            total_m_bytes = 0

        try:
            if self._last_record_mb <= 0:
                dl_speed = 0
            else:
                delta_time = time.time() - self._last_record_time
                delta_mb = downloaded_size_mb - self._last_record_mb
                dl_speed = 0 if delta_time <= 0 or delta_mb <= 0 else delta_mb / delta_time
        except:
            dl_speed = 0

        self._last_record_mb = downloaded_size_mb
        self._last_record_time = time.time()
        unit = 'MB'
        if dl_speed < 0.1:
            dl_speed = dl_speed * 1024
            unit = 'KB'
        if dl_speed > 0:
            txt_pro = get_patch_text_id(90021, progress_num, downloaded_size_mb, total_m_bytes, dl_speed, unit)
        else:
            txt_pro = get_patch_text_id(90020, progress_num, downloaded_size_mb, total_m_bytes)
        if self._root_node:
            self._root_node.lab_progress.setString(txt_pro)
            self._root_node.prog_download.setPercent(progress_num)
            self._root_node.prog_download.setVisible(not need_hide)
            self._root_node.lab_progress.setVisible(not need_hide)
            self._root_node.img_prog_bg.setVisible(not need_hide)
            if self._prog_decorate_nd:
                new_pos_x = progress_num / 100.0 * self._prog_nd_width
                self._prog_decorate_nd.setVisible(True)
                self._prog_decorate_nd.setPosition(cc.Vec2(new_pos_x, 0))

    def _reset_resolution(self):
        try:
            if not self._last_reset_win_size_time:
                self._last_reset_win_size_time = time.time()
            cnt_time = time.time()
            if cnt_time - self._last_reset_win_size_time < 20:
                return
            self._last_reset_win_size_time = cnt_time
            width, height, depth, windowType, multi_sample = game3d.get_window_size()
            if hasattr(game3d, 'set_window_size_force'):
                game3d.set_window_size_force(width, height + 3, 32, 1, 0, False)
                game3d.set_window_size_force(width, height, 32, 1, 0, False)
            else:
                game3d.set_window_size(width, height, 32, 1, 0, False)
            print('reset window size', width, height)
        except Exception as e:
            pass

    def _init_event(self, widget):
        widget.btn_close.addTouchEventListener(self._on_click_close_btn)

    def _on_click_close_btn(self, w, e):
        import ccui
        if e != ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            return

        def ok_cb():
            import game3d
            game3d.exit()

        def cancel_cb():
            pass

        text = get_patch_text_id(268)
        game3d.show_msg_box(text, get_patch_text_id(90001), ok_cb, cancel_cb, get_patch_text_id(90004), get_patch_text_id(90005))

    def _destroy_logic(self):
        render.logic = None
        render.set_logic(None)
        return

    def _destroy_widget(self):
        self._root_node = None
        if self._widget:
            self._widget.removeFromParent()
            self._widget = None
        return

    def quite_aab(self, *args):
        print('quite aab')
        import six.moves.builtins
        six.moves.builtins.__dict__['aab_finish'] = True
        patch_dctool.get_dctool_instane().send_aab_finish_info()
        self._destroy_logic()
        self._destroy_widget()

        def post_logic(finish_cb=self._finished_callback):
            render.set_post_logic(None)
            render.set_render(None)
            if finish_cb:
                finish_cb()
            return

        render.set_post_logic(post_logic)