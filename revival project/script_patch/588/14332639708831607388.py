# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/LocateDialog.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER

class LocateDialog(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/i_window_common_small_locate'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window_bg'

    def on_init_panel(self, *args, **kargs):
        super(LocateDialog, self).on_init_panel()
        self._adcode = None
        self.panel.lab_content_2.SetString(15079)

        @self.panel.temp_btn_go.btn_common.callback()
        def OnClick(*args):
            self.close()

        @self.panel.temp_btn_get.btn_common.callback()
        def OnClick(*args):
            self.close()
            if self._adcode != None and global_data.player.rank_adcode != self._adcode:
                global_data.player.request_set_rank_adcode(self._adcode)
            return

        global_data.emgr.message_on_regeo_location += self.on_regeo_location
        global_data.channel.regeo_location()
        return

    def on_regeo_location(self, result):
        from logic.gcommon.cdata import adcode_data
        from logic.comsys.rank.LocateDialog import LocateDialog
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        if not result:
            NormalConfirmUI2(content=get_text_by_id(15077))
            return
        self._adcode = result['adcode']
        country, province, city, district = adcode_data.get_adcode_region(str(self._adcode))
        text = '{} {}'.format(province, city)
        self.panel.lab_content_2.SetString(text)

    def on_finalize_panel(self):
        global_data.emgr.message_on_regeo_location -= self.on_regeo_location