# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/QualityLevelInitialUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import DIALOG_LAYER_ZORDER_1
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from common.const import uiconst

class QualityLevelInitialUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/tips_window_quality'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    QUALITY_LEVEL_COUNT = 4
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_btn_go.btn_common.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        self.panel.PlayAnimation('in')
        list_quality_choose = self.panel.nd_quality_choose.choose.list_quality_choose
        list_quality_choose.SetInitCount(self.QUALITY_LEVEL_COUNT)
        self.cur_choose_item = None
        self.cur_chose_index = None
        for index in range(self.QUALITY_LEVEL_COUNT):
            item = list_quality_choose.GetItem(index)
            self.add_quality_item(item, index)

        self.refresh_all_btn()
        return

    def add_quality_item(self, item, index):

        @item.btn.callback()
        def OnClick(*args):
            if item == self.cur_choose_item:
                return
            self.select_item(item, index)

    def select_item(self, item, index=None):
        item.btn.choose.setVisible(True)
        if self.cur_choose_item != None:
            self.cur_choose_item.btn.choose.setVisible(False)
        self.cur_choose_item = item
        if index is not None:
            self.cur_chose_index = index
            self.on_set_quality_level(index)
        return

    def refresh_all_btn(self):
        setting_val = global_data.player.get_setting_2(uoc.QUALITY_LEVEL_KEY)
        list_quality_choose = self.panel.nd_quality_choose.choose.list_quality_choose
        for index in range(self.QUALITY_LEVEL_COUNT):
            if setting_val == index:
                item = list_quality_choose.GetItem(index)
                self.cur_chose_index = index
                self.select_item(item)
                break

    def on_set_quality_level(self, level):
        import logic.vscene.global_display_setting as gds
        import device_compatibility
        display_setting = gds.GlobalDisplaySeting()
        old_quality = display_setting.get_quality()
        if old_quality != level:
            perf_flag = device_compatibility.get_device_perf_flag()
            if perf_flag in (device_compatibility.PERF_FLAG_ANDROID_LOW, device_compatibility.PERF_FLAG_IOS_LOW) and level > old_quality:

                def cancel_callback():
                    self.refresh_all_btn()

                def confirm_callback():
                    display_setting.set_quality(level)
                    self._write_setting(uoc.QUALITY_LEVEL_KEY, level, False)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(2324), confirm_callback=confirm_callback, cancel_callback=cancel_callback, click_blank_close=False)
            else:
                display_setting.set_quality(level)
                self._write_setting(uoc.QUALITY_LEVEL_KEY, level, False)

    def _write_setting(self, key, contact, upload):
        if global_data.is_pc_mode:
            upload = False
        if global_data.player:
            ret = global_data.player.write_setting_2(key, contact, sync_to_server=upload)
        else:
            ret = False
        return ret

    def on_finalize_panel(self):
        pass

    def on_click_close_btn(self, *args):
        self._write_setting(uoc.QUALITY_LEVEL_KEY, self.cur_chose_index, False)
        self.close()