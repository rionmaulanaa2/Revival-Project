# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/TestUI.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from common.uisys.basepanel import BasePanel
from logic.comsys.unpack_reader.UnpackGuiReader import UnpackGuiReader
import game3d
from common.const import uiconst

class TestUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test_download_banner'

    def on_init_panel(self, *args):
        self.replace_filename_dict = {'gui/ui_res_unpack/activity_201906/img_boardcast_1.png': 'img1',
           'gui/ui_res_unpack/activity_201906/img_boardcast_2.png': 'img2'
           }
        self.platform_filename_dict = {}
        self.init_event()
        replace_files = six_ex.keys(self.replace_filename_dict)
        for k in replace_files:
            new_k = k
            if game3d.get_platform() != game3d.PLATFORM_WIN32:
                new_k = k[:-4] + '.ktx'
            self.platform_filename_dict[new_k] = k
            UnpackGuiReader().add_loading_file(new_k)

    def init_event(self):
        global_data.emgr.on_unpack_gui_ready += self.on_unpack_gui_ready

    def on_unpack_gui_ready(self, filename):
        print('filename loaded ready')
        if filename in self.platform_filename_dict:
            filename = self.platform_filename_dict[filename]
        if filename in self.replace_filename_dict:
            img_widget = getattr(self.panel, self.replace_filename_dict[filename], None)
            if img_widget:
                img_widget.SetDisplayFrameByPath('', filename)
        return