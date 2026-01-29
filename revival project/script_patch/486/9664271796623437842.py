# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/ExtNpk/ExtDownloaderWidget.py
from __future__ import absolute_import
import time
from common.utils import network_utils
from common.uisys.BaseUIWidget import BaseUIWidget
from ext_package.ext_ingame_manager import ExtInGameManager
from ext_package.ext_package_utils import is_ext_only_wifi_download, get_left_available_space
from ext_package import ext_package_const as ext_c
from ext_package.ext_package_utils import cout_info
from logic.comsys.archive.archive_manager import ArchiveManager
LOG_CHANNEL = 'ext_dl_widget'
ACT_TAG = 100
NET_CHECK_TIME = 2

class ExtDownloaderWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, *args, **kwargs):
        super(ExtDownloaderWidget, self).__init__(parent_ui, panel, *args, **kwargs)
        self._timer = 0
        self._left_space_txt = None
        self._ext_manager = ExtInGameManager()
        self._space_up_time = 0
        self._network_check_time = time.time()
        self._net_type = network_utils.g93_get_network_type()
        self._archive_data = ArchiveManager().get_archive_data('setting')
        self._init_panel()
        global_data.emgr.net_login_reconnect_event += self._on_reconnected
        return

    def _init_panel(self):

        @self.panel.btn_download_1.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('ExtDownloadInfoUI', 'logic.comsys.lobby.ExtNpk')

        self._begin_dl_logic()

    def _begin_dl_logic(self):
        self._unregister_timer()
        if self._ext_manager:
            self._ext_manager.stop_all_download()
        if not (self.panel and self.panel.isValid()):
            return
        if not self._ext_manager.need_download_ext():
            self.panel.setVisible(False)
        else:
            state, _, _ = self._ext_manager.get_state_and_progress()
            if state == ext_c.EXT_IN_GAME_DL_FINISHED:
                cout_info(LOG_CHANNEL, 'ext ingame mgr state is finish, no need dl')
                self._update_state(False)
            else:
                from common.utils import timer
                self._timer = global_data.game_mgr.register_logic_timer(self._update_state, interval=1, times=-1, mode=timer.CLOCK)
                only_wifi = self._archive_data.get_field(ext_c.EXT_NET_SETTING, True)
                if network_utils.g93_get_network_type() != network_utils.TYPE_WIFI and only_wifi:
                    self.panel.setVisible(False)
                    self._ext_manager.start_download_auto_npk(True, self._analyze_cb)
                else:
                    self._confirm_download()

    def _on_reconnected(self):
        self._begin_dl_logic()

    def _update_state(self, check_net=True):
        if not (self.panel and self.panel.isValid()):
            return
        state, prog_num, tip_txt = self._ext_manager.get_state_and_progress()
        if prog_num > 0:
            self.panel.bar_bumber.setVisible(True)
            self.panel.lab_number_1.setVisible(True)
            prog_num = min(int(prog_num * 100), 100)
            self.panel.lab_number_1.SetString('{}%'.format(prog_num))
        else:
            self.panel.bar_bumber.setVisible(False)
            self.panel.lab_number_1.setVisible(False)
        if state == ext_c.EXT_IN_GAME_DL_NPK:
            net_text = get_text_by_id(338) if self._net_type != network_utils.TYPE_WIFI else get_text_by_id(339)
            space_text = self._get_space_txt()
            tip_txt = '{},{}'.format(net_text, space_text) if space_text else net_text
        elif state == ext_c.EXT_IN_GAME_DL_FINISHED:
            check_net = False
        self.panel.lab_tips.setVisible(True)
        self.panel.lab_tips.SetString(tip_txt)
        now_time = time.time()
        if check_net and now_time - self._network_check_time > NET_CHECK_TIME and state != ext_c.EXT_IN_GAME_DL_FINISHED:
            self._net_type = network_utils.g93_get_network_type()
            self._network_check_time = now_time
            is_in_downloading = self._ext_manager.is_in_downloading_process()
            if self._net_type == network_utils.TYPE_WIFI:
                if not is_in_downloading:
                    self._confirm_download()
            else:
                only_wifi = self._archive_data.get_field(ext_c.EXT_NET_SETTING, True)
                if only_wifi:
                    if state == ext_c.EXT_IN_GAME_DL_NPK:
                        self._ext_manager.stop_all_download()
                        self._ext_manager.set_state(ext_c.EXT_IN_GAME_DL_WAITING_WIFI)
                elif self._net_type != network_utils.TYPE_INVALID:
                    if not is_in_downloading:
                        self._confirm_download()

    def _get_space_txt(self):
        try:
            now_time = time.time()
            if now_time - self._space_up_time < 3 and self._left_space_txt is not None:
                return self._left_space_txt
            self._space_up_time = now_time
            mega_bytes = get_left_available_space()
            if mega_bytes >= 0:
                pre_text = get_text_by_id(353)
                if mega_bytes > 1024:
                    mem_txt = '{}:{:.1f}G'.format(pre_text, mega_bytes / 1024.0)
                else:
                    mem_txt = '{}:{}MB'.format(pre_text, int(mega_bytes))
                self._left_space_txt = mem_txt
            else:
                self._left_space_txt = ''
        except Exception as e:
            cout_info(LOG_CHANNEL, 'get space except:{}'.format(str(e)))
            self._left_space_txt = ''

        return self._left_space_txt

    def _analyze_cb(self, *args):
        if self.panel and self.panel.isValid():
            self.panel.setVisible(True)
            from logic.gcommon.common_utils.local_text import get_text_by_id
            from logic.comsys.common_ui.NormalConfirmUI import ExtNpkDownloadConfirmUI
            npk_size = self._ext_manager.get_download_ext_npk_size() / 1024.0 / 1024.0
            npk_size_str = '{:2}M'.format(int(npk_size))
            text_str = get_text_by_id(90054).format(npk_size_str)
            ExtNpkDownloadConfirmUI(text=text_str, confirm_cb=self._confirm_download_when_no_wifi)

    def _confirm_download_when_no_wifi(self, *args):
        only_wifi = self._archive_data.get_field(ext_c.EXT_NET_SETTING, True)
        if only_wifi:
            self._archive_data.set_field(ext_c.EXT_NET_SETTING, False)
        self._confirm_download()

    def _confirm_download(self, *args):
        if not (self.panel and self.panel.isValid()):
            return
        self.panel.setVisible(True)
        self.panel.lab_tips.setVisible(False)
        self._ext_manager.start_download_auto_npk(True)
        self._update_state(False)

    def _unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def destroy(self):
        global_data.ui_mgr.close_ui('ExtNpkDownloadConfirmUI')
        global_data.emgr.net_reconnect_event -= self._on_reconnected
        cout_info(LOG_CHANNEL, 'destroy ui then stop all download')
        self._ext_manager.stop_all_download()
        self._unregister_timer()
        super(ExtDownloaderWidget, self).destroy()