# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/CharacterChooseUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import ccp
from common.const import uiconst

class CharacterChooseUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'create/choose_person'
    UI_ACTION_EVENT = {'top.btn_back.OnClick': 'on_click_btn_back',
       'btn_confirm.btn_common_big.OnClick': 'on_click_btn_confirm'
       }

    def on_click_btn_back(self, *args):
        global_data.emgr.character_choose_cancel.emit()

    def on_click_btn_confirm(self, *args):
        global_data.emgr.character_choose_confirm.emit()
        print('click btn confirm')