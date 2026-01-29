# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/LocateChooseDialog.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils import template_utils
from logic.gcommon.cdata import adcode_data

class LocateChooseDialog(WindowSmallBase):
    PANEL_CONFIG_NAME = 'rank/i_rank_windiow_locate_choose'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window_bg'

    def on_init_panel(self, *args, **kargs):
        super(LocateChooseDialog, self).on_init_panel()
        global_data.emgr.message_on_regeo_location += self.on_regeo_location
        self._adcode = None

        @self.panel.temp_btn_cancel.btn_common.callback()
        def OnClick(*args):
            self.close()

        @self.panel.temp_btn_confirm.btn_common.callback()
        def OnClick(*args):
            self.close()
            if self._adcode != None and global_data.player.rank_adcode != self._adcode:
                global_data.player.request_set_rank_adcode(self._adcode)
            return

        @self.panel.btn_choose.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.list_address.isVisible():
                self.panel.list_address.setVisible(True)
                self.panel.icon_arrow.setRotation(90)
            else:
                self.panel.list_address.setVisible(False)
                self.panel.icon_arrow.setRotation(270)

        region_id = global_data.channel.get_region_id()
        adcodes = adcode_data.get_adcode_by_region_id(region_id)
        locate_list = []
        for adcode in adcodes:
            locate_list.append({'adcode': adcode,'name': adcode_data.data[adcode]})

        def choose(index):
            selected = locate_list[index]
            self.panel.lab_address.SetString(selected.get('name', ''))
            self.panel.list_address.setVisible(False)
            self.panel.icon_arrow.setRotation(270)
            self._adcode = selected.get('adcode')

        def list_close():
            self.panel.icon_arrow.setRotation(270)

        template_utils.init_common_choose_list_2(self.panel.list_address, self.panel.icon_arrow, locate_list, choose, max_height=354, close_cb=list_close)
        return

    def on_regeo_location(self, result):
        from logic.gcommon.cdata import adcode_data
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        if not result:
            NormalConfirmUI2(content=get_text_by_id(15077))
            return
        self._adcode = result['adcode']
        country, province, city, district = adcode_data.get_adcode_region(str(self._adcode))
        self.panel.lab_content_2.SetString(province)

    def on_finalize_panel(self):
        global_data.emgr.message_on_regeo_location -= self.on_regeo_location