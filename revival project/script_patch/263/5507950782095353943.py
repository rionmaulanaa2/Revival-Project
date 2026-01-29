# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/ExtNpk/ExtDownloadInfoUI.py
from __future__ import absolute_import
import time
from common.utils import network_utils
from common.utils import ui_path_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_2, UI_VKB_NO_EFFECT
from ext_package.ext_ingame_manager import ExtInGameManager
from logic.comsys.archive.archive_manager import ArchiveManager
from ext_package.ext_package_utils import get_left_available_space
from ext_package.ext_package_const import EXT_NET_SETTING, EXT_DL_FULL_SPEED, EXT_IN_GAME_DL_NPK, EXT_MANUAL_ARCHIVE_NAME_DICT, EXT_IN_GAME_DL_ERROR, EXT_IN_GAME_DL_FINISHED, EXT_IN_GAME_DL_VERIFY, EXT_IN_GAME_DL_WAITING_WIFI, EXT_MANUAL_NAME_INFO, EXT_KONGDAO_SCENE_NAME, get_pve_name, EXT_DL_KONGDAO, EXT_DL_PVE2, EXT_DL_PVE3, EXT_NEW_USING, EXT_OLD_USING, EXT_NAME_DICT

class ExtDownloadInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/download_package/download_package_process'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'net_login_reconnect_event': 'close'
       }
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_close',
       'nd_get.btn_get.OnClick': '_on_click_net',
       'btn_download.OnClick': '_on_click_download',
       'btn_speed.OnClick': '_on_choose_speed',
       'nd_download_map.btn_get.OnClick': '_on_choose_kongdao',
       'nd_download_pve2.btn_get.OnClick': '_on_choose_pve2',
       'nd_download_pve3.btn_get.OnClick': '_on_choose_pve3'
       }

    def on_init_panel(self, *args, **kargs):
        self._ext_manager = ExtInGameManager()
        self._archive_data = ArchiveManager().get_archive_data('setting')
        self.spd_modify_time = 0
        self._space_up_time = 0
        self.panel.lab_all.setString('')
        self.panel.btn_download.setVisible(False)
        only_wifi = self._archive_data.get_field(EXT_NET_SETTING, True)
        self.panel.nd_get.img_get.setVisible(only_wifi)
        dl_full_speed = self._archive_data.get_field(EXT_DL_FULL_SPEED, False)
        self.panel.img_speed.setVisible(dl_full_speed)
        dl_kongdao = self._archive_data.get_field(EXT_DL_KONGDAO, False)
        dl_pve2 = self._archive_data.get_field(EXT_DL_PVE2, False)
        dl_pve3 = self._archive_data.get_field(EXT_DL_PVE3, False)
        self.panel.nd_download_map.img_get.setVisible(dl_kongdao)
        self.panel.nd_download_pve2.img_get.setVisible(dl_pve2)
        self.panel.nd_download_pve3.img_get.setVisible(dl_pve3)
        self._int_ext_state(EXT_KONGDAO_SCENE_NAME, self.panel.nd_download_map, False)
        self._int_ext_state(get_pve_name(2), self.panel.nd_download_pve2, False)
        self._int_ext_state(get_pve_name(3), self.panel.nd_download_pve3, False)
        from common.utils import timer
        self._timer = global_data.game_mgr.register_logic_timer(self._update_state, interval=0.3, times=-1, mode=timer.CLOCK)
        self.panel.lab_loading_2.SetString('')
        self.panel.lab_loading_3.SetString('')
        self._update_state()
        self._init_description()

    def _init_description(self):
        self._des_info = (
         (
          345, 346, ui_path_utils.EXT_SKIN_PIC, ui_path_utils.EXT_SKIN_BAR_NAME_PIC,
          ui_path_utils.EXT_SKIN_BAR_NET_PIC, ui_path_utils.EXT_SKIN_BAR_TIP_PIC),
         (
          347, 348, ui_path_utils.EXT_KONGDAO_PIC, ui_path_utils.EXT_KONGDAO_BAR_NAME_PIC,
          ui_path_utils.EXT_KONGDAO_BAR_NET_PIC, ui_path_utils.EXT_KONGDAO_BAR_TIP_PIC),
         (
          349, 350, ui_path_utils.EXT_AUDIO_PIC, ui_path_utils.EXT_AUDIO_BAR_NAME_PIC,
          ui_path_utils.EXT_AUDIO_BAR_NET_PIC, ui_path_utils.EXT_AUDIO_BAR_TIP_PIC))
        self._desc_idx = 0

        def choose_desc():
            desc_idx = self._desc_idx % 3
            if self.panel and self.panel.isValid():
                self.panel.bar_text.SetDisplayFrameByPath('', self._des_info[desc_idx][3])
                self.panel.bar_loading.SetDisplayFrameByPath('', self._des_info[desc_idx][4])
                self.panel.nd_get.lab_state.nd_auto_fit.bar_tips.SetDisplayFrameByPath('', self._des_info[desc_idx][5])
                self.panel.lab_text.SetString(self._des_info[desc_idx][0])
                self.panel.lab_loading_2.SetString(self._des_info[desc_idx][0])
                self.panel.lab_loading_3.SetString(self._des_info[desc_idx][1])
                self.panel.img_kv.SetDisplayFrameByPath('', self._des_info[desc_idx][2])
                self._desc_idx += 1

        choose_desc()
        from cocosui import cc
        act = self.runAction(cc.RepeatForever.create(cc.Sequence.create([cc.CallFunc.create(choose_desc), cc.DelayTime.create(3)])))

    def _on_click_net(self, *args):
        only_wifi = self.panel.nd_get.img_get.isVisible()
        self.panel.nd_get.img_get.setVisible(not only_wifi)
        self._archive_data.set_field(EXT_NET_SETTING, not only_wifi)

    def _on_choose_speed(self, *args):
        is_full_speed = self.panel.img_speed.isVisible()
        self.panel.img_speed.setVisible(not is_full_speed)
        self._archive_data.set_field(EXT_DL_FULL_SPEED, not is_full_speed)

    def _on_choose_kongdao(self, *args):
        self._int_ext_state(EXT_KONGDAO_SCENE_NAME, self.panel.nd_download_map, True)

    def _on_choose_pve2(self, *args):
        self._int_ext_state(get_pve_name(2), self.panel.nd_download_pve2, True)

    def _on_choose_pve3(self, *args):
        self._int_ext_state(get_pve_name(3), self.panel.nd_download_pve3, True)

    def _int_ext_state(self, ext_name, in_node, is_click):
        ext_st = self._ext_manager.get_ext_state(ext_name)
        if ext_st in (EXT_OLD_USING, EXT_NEW_USING):
            self._set_manual_finish(ext_st, ext_name, in_node)
        elif is_click:
            in_node.lab_download.SetString(EXT_MANUAL_NAME_INFO.get(ext_name, 333))
            set_vis = not in_node.img_get.isVisible()
            in_node.img_get.setVisible(set_vis)
            self._archive_data.set_field(EXT_MANUAL_ARCHIVE_NAME_DICT.get(ext_name, 'ext_dl_manual_set'), set_vis)
            self._ext_manager.start_download_manual_ext_npk(ext_name, set_vis)
        else:
            in_node.lab_download.SetString(EXT_MANUAL_NAME_INFO.get(ext_name, 333))
            choose_dl = self._archive_data.get_field(EXT_MANUAL_ARCHIVE_NAME_DICT.get(ext_name, 'ext_dl_manual'), False)
            in_node.img_get.setVisible(choose_dl)

    def _set_manual_finish(self, ext_st, ext_name, in_node):
        name_id = EXT_NAME_DICT.get(ext_name, 330)
        second_id = 238 if ext_st == EXT_OLD_USING else 333
        _text = '{}:{}'.format(get_text_by_id(name_id), get_text_by_id(second_id))
        in_node.lab_download.SetString(_text)
        in_node.btn_get.SetEnable(False)
        in_node.img_get.setVisible(True)

    def _update_manual_node(self):
        node_dict = {EXT_KONGDAO_SCENE_NAME: self.panel.nd_download_map,
           get_pve_name(2): self.panel.nd_download_pve2,
           get_pve_name(3): self.panel.nd_download_pve3
           }
        for ext_name in node_dict:
            ext_st = self._ext_manager.get_ext_state(ext_name)
            if ext_st in (EXT_OLD_USING, EXT_NEW_USING):
                node = node_dict[ext_name]
                self._set_manual_finish(ext_st, ext_name, node)

    def _on_close(self, *args):
        self._unregister_timer()
        self.close()

    def _update_state(self):
        net_work_type = network_utils.g93_get_network_type()
        state, prog_num, tip_txt = self._ext_manager.get_state_and_progress()
        prog_num = int(prog_num * 100)
        prog_num = min(100, prog_num)
        self.panel.btn_download.setVisible(False)
        self.panel.lab_tips_2.SetString(str(tip_txt))
        if state == EXT_IN_GAME_DL_NPK:
            self.set_prog_show(True)
            dl_text_id = 342 if net_work_type == network_utils.TYPE_WIFI else 341
            self.panel.lab_tips_2.SetString(get_text_by_id(dl_text_id) + str(tip_txt))
            self.panel.nd_process.prog_process.SetPercentage(prog_num)
            speed, total_size = self._ext_manager.get_now_speed_and_size()
            cnt_time = time.time()
            if cnt_time - self.spd_modify_time > 1.0:
                self.spd_modify_time = cnt_time
                unit = 'MB'
                if speed < 0.1:
                    speed = speed * 1024
                    unit = 'KB'
                total_size_mb = total_size * 1.0 / 1048576.0
                total_size_mb = max(0.1, total_size_mb)
                downloaded_size_mb = total_size_mb * (prog_num * 1.0 / 100)
                if speed > 0:
                    text = get_text_by_id(90021, (prog_num, downloaded_size_mb, total_size_mb, speed, unit))
                else:
                    text = get_text_by_id(90020, (prog_num, downloaded_size_mb, total_size_mb))
                self.panel.lab_all.setString(text)
        elif state == EXT_IN_GAME_DL_ERROR:
            self.panel.lab_all.setString('')
            self.set_prog_show(False)
            self.panel.btn_download.setVisible(True)
        elif state == EXT_IN_GAME_DL_FINISHED:
            self.panel.lab_all.setString('')
            self.set_prog_show(True)
            self.panel.nd_process.prog_process.SetPercentage(100)
        elif state == EXT_IN_GAME_DL_VERIFY:
            self.panel.lab_all.setString('')
            self.set_prog_show(True)
            self.panel.nd_process.prog_process.SetPercentage(prog_num)
        elif state == EXT_IN_GAME_DL_WAITING_WIFI:
            self.panel.lab_all.setString('')
            self.set_prog_show(False)
            self.panel.btn_download.setVisible(True)
            self.panel.nd_process.prog_process.SetPercentage(0)
        else:
            self.panel.lab_all.setString('')
            self.set_prog_show(False)
            self.panel.nd_process.prog_process.SetPercentage(0)
        self._update_manual_node()
        self._update_space()

    def _update_space(self):
        try:
            now_time = time.time()
            if now_time - self._space_up_time < 2:
                return
            self._space_up_time = now_time
            mega_bytes = get_left_available_space()
            if mega_bytes >= 0:
                pre_text = get_text_by_id(353)
                if mega_bytes > 1024:
                    mem_txt = '{}:{:.1f}G'.format(pre_text, mega_bytes / 1024.0)
                else:
                    mem_txt = '{}:{}MB'.format(pre_text, int(mega_bytes))
                self.panel.lab_memory.SetString(mem_txt)
        except Exception as e:
            pass

    def set_prog_show(self, vis):
        self.panel.bar_download.setVisible(vis)
        self.panel.prog_process.setVisible(vis)

    def _on_click_download(self, *args):
        if not self._ext_manager:
            return

        def confirm_mobile_cb(*args):
            from ext_package.ext_package_utils import set_ext_only_wifi_archive
            set_ext_only_wifi_archive(False)
            ExtInGameManager().start_download_auto_npk(True)

        if network_utils.g93_get_network_type() != network_utils.TYPE_WIFI:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(241), confirm_callback=confirm_mobile_cb)
        else:
            self._ext_manager.start_download_auto_npk(True)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def on_finalize_panel(self):
        self._ext_manager = None
        self._unregister_timer()
        return