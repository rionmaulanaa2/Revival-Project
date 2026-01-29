# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/sdk/FaceCertificationUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
FACE_STAGE_LOGIN = 0
FACE_STAGE_CHARGE = 1

class FaceCertificationUI(BasePanel):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    PANEL_CONFIG_NAME = 'common/tips_window_identify'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    LAB = {'title': 609530,
       'con1': (609531, 609537),
       'con2': (609534, 609538),
       'btn1': (609532, 609535),
       'btn2': (609533, 609536)
       }

    def on_init_panel(self, stage=0, *args, **kwargs):
        super(FaceCertificationUI, self).on_init_panel()
        self.init_param(stage)
        self.init_lab()
        self.init_ui_events()
        self.process_events(True)
        global_data.player.get_face_certification_token()

    def init_param(self, stage):
        self.stage = stage
        if global_data.is_inner_server:
            global_data.channel.set_prop_int('AI_TEST_MODE', 1)
        else:
            global_data.channel.set_prop_int('AI_TEST_MODE', 0)

    def init_lab(self):
        self.panel.temp_window.lab_headline.SetString(get_text_by_id(self.LAB['title']))
        self.panel.temp_window.lab_content.SetString(get_text_by_id(self.LAB['con1'][self.stage]))
        self.panel.temp_window.lab_btn_content.SetString(get_text_by_id(self.LAB['btn1'][0]))
        self.panel.temp_window.temp_not_yet.btn_common_big.SetText(get_text_by_id(self.LAB['btn2'][0]))

    def init_ui_events(self):

        @self.panel.temp_not_yet.btn_common_big.unique_callback()
        def OnClick(btn, layer, *args):
            self.on_click_cancel()

        @self.panel.lab_btn_content.nd_auto_fit.btn_confirm.unique_callback()
        def OnClick(btn, layer, *args):
            self.on_click_confirm()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_identify(self):
        token_data = global_data.player.get_face_certification_token()
        if token_data != -1:
            pass
        else:
            return
        command = {'token': token_data,
           'methodId': 'startIdentify'
           }
        global_data.channel.extend_func_by_dict(command)
        self.close()

    def on_click_confirm(self, *args):
        print('confirm')
        token = global_data.player.get_face_certification_token(callback=self.start_identify)
        if token == -1:
            self.panel.lab_btn_content.nd_auto_fit.btn_confirm.SetEnable(False)
            self.panel.temp_not_yet.btn_common_big.SetEnable(False)
            self.panel.DelayCall(3, lambda : self.close())
            return
        self.panel.lab_btn_content.nd_auto_fit.btn_confirm.SetEnable(False)
        self.panel.temp_not_yet.btn_common_big.SetEnable(False)
        self.start_identify()

    def on_click_cancel(self, *args):
        self.panel.temp_window.lab_content.SetString(get_text_by_id(self.LAB['con2'][self.stage]))
        self.panel.temp_window.lab_btn_content.SetString(get_text_by_id(self.LAB['btn1'][1]))
        self.panel.temp_window.temp_not_yet.btn_common_big.SetText(get_text_by_id(self.LAB['btn2'][1]))

        @self.panel.temp_not_yet.btn_common_big.unique_callback()
        def OnClick(btn, layer, *args):
            self.on_click_back()

        @self.panel.lab_btn_content.nd_auto_fit.btn_confirm.unique_callback()
        def OnClick(btn, layer, *args):
            self.on_click_confirm_next()

    def on_click_confirm_next(self, *args):
        self.close()

    def on_click_back(self, *args):
        self.init_lab()
        self.init_ui_events()

    def on_finalize_panel(self):
        self.process_events(False)
        super(FaceCertificationUI, self).on_finalize_panel()