# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/VideoShareConfirmUI.py
from __future__ import absolute_import
from __future__ import print_function
import os
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils.text_utils import check_review_words
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.comsys.video import video_record_utils as vru

class VideoShareConfirmUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'setting/setting_highlight/confirm_share'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'nd_content.btn_done.btn_common.OnClick': '_on_click_send_btn',
       'nd_load.btn_cancel.btn_common.OnClick': '_on_click_cancel_btn'
       }

    def init_video_info(self, video_info, upload_cb):
        self._video_info = video_info
        self._upload_cb = upload_cb
        self._last_up_record = None
        self._refresh_show(self._video_info)
        return

    def on_init_panel(self, *args, **kwargs):
        super(VideoShareConfirmUI, self).on_init_panel(*args, **kwargs)
        self._upload_cb = None
        self._cancel_clicked = False
        self.set_custom_close_func(self._on_click_back_btn)
        self._input_box = InputBox(self.panel.nd_content.inputbox, max_length=20, placeholder=3122)
        self._input_box.set_rise_widget(self.panel)
        self._video_info = None
        self.panel.nd_load.setVisible(False)
        return

    def _refresh_show(self, info):
        video_path = info.get('path', '')
        cover_info = info.get(vru.SMALL_COVER_KEY, None)
        if not video_path or not cover_info:
            return
        else:
            cover_name, cover_path, _ = cover_info
            if not os.path.exists(video_path) or not os.path.exists(cover_path):
                return
            vru.cal_and_set_cover_node(cover_name, self.panel.nd_video)
            return

    def _on_click_send_btn(self, *args):
        if not global_data.player or not self._video_info:
            return
        else:
            valid, msg = self._get_msg()
            if not valid:
                return
            self._cancel_clicked = False
            if self._last_up_record:
                status, record_names = self._last_up_record
                if status and self._upload_cb and callable(self._upload_cb):
                    self._upload_cb(status, record_names, msg)
                    self.close()
                    return

            def finish_cb(request, cal_ret):
                if cal_ret:
                    video_path = self._video_info.get('path', '')
                    _, cover_path, _ = self._video_info[vru.SMALL_COVER_KEY]
                    global_data.player.try_upload_video(video_path, cover_path, self._upload_callback, vru.SHARE_STORE_TIME)
                    self.panel.nd_load.setVisible(True)
                    self.panel.PlayAnimation('loading')

            from common.daemon_thread import DaemonThreadPool
            if vru.NEED_MD5:
                DaemonThreadPool().add_threadpool(self._check_video_and_cover, finish_cb)
            else:
                finish_cb(None, True)
            return

    def _check_video_and_cover(self):
        video_path = self._video_info.get('path', '')
        cover_info = self._video_info.get(vru.SMALL_COVER_KEY, None)
        if not video_path or not cover_info:
            return False
        else:
            _, cover_path, cover_md5_str = cover_info
            if not os.path.exists(video_path) or not os.path.exists(cover_path):
                return False
            check_info = (
             (
              video_path, self._video_info.get('md5_str', '')),
             (
              cover_path, cover_md5_str))
            for path, md5_str in check_info:
                ret, md5_cal = vru.cal_video_md5(path)
                check_valid = ret and md5_cal and md5_cal == md5_str
                if not check_valid:
                    return False

            return True

    def _upload_callback(self, status, error, record_names):
        self._last_up_record = (
         status, record_names)
        if global_data.is_inner_server:
            print('[VideoShareConfirmUI] [_upload_callback] status:[%s] error:[%s] record_names:[%s]' % (status, error, record_names))
        if not self.panel or not self.panel.isValid():
            return
        self.panel.StopAnimation('loading')
        self.panel.nd_load.setVisible(False)
        valid, msg = self._get_msg()
        if self._cancel_clicked and valid:
            return
        if self._upload_cb and callable(self._upload_cb) and valid:
            self._upload_cb(status, record_names, msg)
            self.close()

    def _get_msg(self):
        msg = self._input_box.get_text()
        ret, _ = check_review_words(msg)
        if not ret:
            global_data.game_mgr.show_tip(get_text_by_id(10045))
            return (
             False, msg)
        return (True, msg)

    def _on_click_cancel_btn(self, btn, touch):
        self._cancel_upload()

    def _on_click_back_btn(self, *args):
        self._cancel_upload()
        self.close()

    def _cancel_upload(self):
        self.panel.StopAnimation('loading')
        self.panel.nd_load.setVisible(False)
        self._cancel_clicked = True
        log_error('[VideoShareConfirmUI] not implement cancel upload')

    def on_finalize_panel(self):
        self._video_info = None
        self._upload_cb = None
        super(VideoShareConfirmUI, self).on_finalize_panel()
        return