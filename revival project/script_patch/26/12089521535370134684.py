# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaResolutionUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_VKB_CLOSE, UI_TYPE_MESSAGE
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil
from logic.comsys.message.ConcertChat import ConcertChat
from logic.gutils.concert_utils import get_sing_start_ts, get_concert_end_ts, get_song_num
from logic.gcommon.common_const import battle_const
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase
reso_list = [
 'cResoNormal', 'cResoHigh', 'cResoSuper']
reso_name_dict = {'cResoNormal': 2171,
   'cResoHigh': 2172,
   'cResoSuper': 2173
   }

class KizunaResolutionUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/open_kizuna_resolution'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = UI_VKB_CLOSE
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'temp_btn_1.btn_common_big.OnClick': 'on_click_close_btn',
       'temp_btn_2.btn_common_big.OnClick': 'on_click_choose_btn'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(KizunaResolutionUI, self).on_init_panel()
        self._quality = self.get_cur_reso_setting()
        self.last_choose_item = None
        self.init_resolution_list()
        return

    def on_finalize_panel(self):
        self.last_choose_item = None
        return

    def init_resolution_list(self):
        choose_list = self.panel.list_graphics_style
        choose_list.SetInitCount(len(reso_list))
        for index in range(len(reso_list)):
            item = choose_list.GetItem(index)
            self.add_graph_item(item, index)

    def add_graph_item(self, item, index):

        @item.btn.callback()
        def OnClick(*args):
            if item == self.last_choose_item:
                return
            else:
                item.btn.choose.setVisible(True)
                if self.last_choose_item != None:
                    self.last_choose_item.btn.choose.setVisible(False)
                self.last_choose_item = item
                self._quality = reso_list[index]
                return

        text = reso_name_dict[reso_list[index]]
        item.lab_title.SetString(text)
        item.lab_title_sel.SetString(text)
        if self._quality == reso_list[index]:
            item.btn.choose.setVisible(True)
            self.last_choose_item = item

    def get_cur_reso_setting(self):
        conf = global_data.achi_mgr.get_general_archive_data()
        return conf.get_field('video_resolution', 'cResoHigh')

    def on_click_close_btn(self, btn, touch):
        self.close()

    def on_click_choose_btn(self, btn, touch):
        conf = global_data.achi_mgr.get_general_archive_data()
        conf.set_field('video_resolution', self._quality)
        global_data.emgr.change_concert_video_resolution_event.emit()
        self.close()