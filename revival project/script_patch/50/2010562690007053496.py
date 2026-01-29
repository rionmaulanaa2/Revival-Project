# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/plist_tools/PlistPngShowUI.py
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst
import os
import cc

class PlistPngShowUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/test_plist_png'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_back.OnClick': 'on_click_close_btn'
       }

    def on_click_close_btn(self, btn, touch):
        self.close()

    def show_in_ui(self, plist, png):
        from tools.plist_tools.plist_checker import PlistShowChecker
        import cc
        dict_ = cc.FileUtils.getInstance().getValueMapFromFile(plist)
        png_name = dict_.get('metadata', {}).get('realTextureFileName') or dict_.get('metadata', {}).get('textureFileName')
        plist_png = os.path.join(os.path.dirname(plist), png_name)
        panel = self.panel.sv.GetContainer()
        panel.sp.SetDisplayFrameByPath('', plist_png, force_sync=True)
        sp_size = panel.sp.getContentSize()
        png_info = PlistShowChecker.get_plist_png_info(plist, png)
        strTextureRect = png_info.get('textureRect', '')
        textureRotated = png_info.get('textureRotated', False)
        rect = PlistShowChecker.RectFromString(strTextureRect)
        print ('rect', rect)
        if not textureRotated:
            panel.nd_size.SetContentSize(rect.width, rect.height)
        else:
            panel.nd_size.SetContentSize(rect.height, rect.width)
        panel.nd_scale.ChildRecursionRePosition()
        panel.nd_size.SetPosition(rect.x, sp_size.height - rect.y)