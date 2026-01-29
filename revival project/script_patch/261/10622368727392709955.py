# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/sdk/AILabTestUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id

class AILabTestUI(BasePanel):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    PANEL_CONFIG_NAME = 'test/ninebuttons'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close',
       'btn_01.OnClick': 'oc_import',
       'btn_02.OnClick': 'oc_init',
       'btn_03.OnClick': 'oc_init_vm',
       'btn_reg_1.OnClick': 'oc_start_register_1',
       'btn_reg_2.OnClick': 'oc_start_register_2',
       'btn_reg_0.OnClick': 'oc_stop_register',
       'btn_rec.OnClick': 'oc_start_recongnize',
       'btn_rec_0.OnClick': 'oc_stop_recongnize',
       'btn_get.OnClick': 'oc_get_cache',
       'btn_delete_1.OnClick': 'oc_delete_cache_1',
       'btn_delete_2.OnClick': 'oc_delete_cache_2'
       }
    LAB = {}

    def on_init_panel(self, *args, **kwargs):
        super(AILabTestUI, self).on_init_panel()

    def on_click_close(self, *args):
        self.close()

    def oc_import(self, *args):
        from logic.comsys.chat.VoiceAILab import VoiceAILab
        VoiceAILab()

    def oc_init(self, *args):
        global_data.voice_ailab.init_ailab()
        global_data.voice_ailab.request_permission()

    def oc_init_vm(self, *args):
        global_data.voice_ailab.init_vm()

    def oc_start_register_1(self, *args):
        global_data.voice_ailab.start_register(1)

    def oc_start_register_2(self, *args):
        global_data.voice_ailab.start_register(2)

    def oc_stop_register(self, *args):
        global_data.voice_ailab.stop_register()

    def oc_start_recongnize(self, *args):
        global_data.voice_ailab.start_recongnize()

    def oc_stop_recongnize(self, *args):
        global_data.voice_ailab.stop_recongnize()

    def oc_get_cache(self, *args):
        global_data.voice_ailab.get_cache_cmd()

    def oc_delete_cache_1(self, *args):
        global_data.voice_ailab.delete_voice_cmd(1)

    def oc_delete_cache_2(self, *args):
        global_data.voice_ailab.delete_voice_cmd(2)

    def on_finalize_panel(self):
        super(AILabTestUI, self).on_finalize_panel()