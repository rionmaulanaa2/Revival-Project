# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CDKeyInputUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.uielment.CCRichText import CCRichText
import cc
import game3d
CODE_SUCCESS = 200
CODE_SN_NOT_EXIT = 402
CODE_SN_EXPIRED = 406
CODE_SN_ALREADY_USED = 409
CODE_SN_INVALID = 415
CODE_EXCEED_MAX_RETRY = 417
CODE_FORBIDDEN = 419
CODE_NOT_PUBLISH = 420
CODE_ACTIVE_FAIL = 501
TEXT_MAP = {CODE_SUCCESS: 80597,
   CODE_SN_NOT_EXIT: 80598,
   CODE_SN_EXPIRED: 609373,
   CODE_SN_ALREADY_USED: 609371,
   CODE_SN_INVALID: 609372,
   CODE_NOT_PUBLISH: 609374,
   CODE_FORBIDDEN: 609375,
   CODE_ACTIVE_FAIL: 609376,
   CODE_EXCEED_MAX_RETRY: 80600
   }
CODE_MAX_LENGTH = 10
CD_KEY_PREFIX = 'wy'
from common.const import uiconst

class CDKeyInputUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/active_code_verify'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_panel.btn_close.OnClick': 'on_click_close_btn',
       'temp_btn_sure.btn_common_big.OnClick': 'on_btn_ok',
       'temp_input1.btn_clear.OnClick': 'on_btn_clear'
       }
    ST_NONE = 0
    ST_INPUT = 1
    ST_VERIFY_PROCESS = 2
    ST_VERIFY_DONE = 3
    ST_VERIFY_FAIELD = 400

    def on_init_panel(self, **kwargs):
        self.panel.setLocalZOrder(self.DLG_ZORDER)
        self.init_input_box()
        self.init_parameters()
        self.on_confirm_callback = kwargs.get('on_confirm', lambda sn: None)
        self.on_close_callback = kwargs.get('on_close', lambda : None)
        self.panel.PlayAnimation('show')

    def init_input_box(self):
        self._input_1 = InputBox.InputBox(self.temp_input1, placeholder='XXXXXXXX', send_callback=self._send_callback, cancel_callback=self._cancel_callback, start_input_cb=self._start_input_callback)
        self._input_1.set_rise_widget(self.panel)

    def init_parameters(self):
        self._st = self.ST_INPUT

    def on_finalize_panel(self):
        pass

    def show_effect_gaosi(self):
        self.close_effect_gaosi()
        from logic.comsys.effect.ui_effect import GaussianEffect
        self._effect_gaosi = GaussianEffect(self.panel.pnl_bg, self.panel.pnl_gaosi)
        self._effect_gaosi.start()

    def close_effect_gaosi--- This code section failed: ---

 104       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_effect_gaosi'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 105      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 106      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  '_effect_gaosi'
          22  JUMP_IF_FALSE_OR_POP    37  'to 37'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             1  '_effect_gaosi'
          31  LOAD_ATTR             2  'destroy'
          34  CALL_FUNCTION_0       0 
        37_0  COME_FROM                '22'
          37  POP_TOP          

 107      38  LOAD_CONST            0  ''
          41  LOAD_FAST             0  'self'
          44  STORE_ATTR            1  '_effect_gaosi'
          47  LOAD_CONST            0  ''
          50  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def set_state(self, i_state):
        self._st = i_state

    def on_click_close_btn(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        dlg = SecondConfirmDlg2()
        dlg.panel.setLocalZOrder(self.DLG_ZORDER + 1)
        dlg.confirm(content=get_text_by_id(80601), confirm_text=get_text_by_id(80305), confirm_callback=lambda : self.close_confirm())

    def close_confirm(self):
        import game3d
        game3d.exit()

    def on_btn_clear(self, *args):
        self._input_1.set_text('')
        self.temp_input1.btn_clear.setVisible(False)

    def on_btn_ok(self, *args):
        if self._st != self.ST_INPUT:
            return
        sn = self._input_1.get_text().lower()
        if not self.check_sn(sn):
            global_data.game_mgr.show_tip(get_text_by_id(80598))
            return
        if self.on_confirm_callback:
            self.on_confirm_callback(sn, callback=self._verify_cb)

    def _verify_cb(self, ret_code, msg):
        if ret_code == CODE_SUCCESS:
            global_data.game_mgr.show_tip(get_text_by_id(self.get_ret_text_id(ret_code)))
            self.close()
            return
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        dlg = NormalConfirmUI2()
        dlg.set_content_string(self.get_ret_text_id(ret_code))
        dlg.panel.setLocalZOrder(self.DLG_ZORDER + 1)

    def rich_callback(self, cb_string):
        if hasattr(self, cb_string):
            getattr(self, cb_string)()

    def on_link_cb(self):
        import game3d
        url = get_text_by_id(80539)
        game3d.open_url(url)

    def check_sn(self, sn):
        if len(sn) != CODE_MAX_LENGTH:
            return False
        return True

    def _send_callback(self):
        if len(self._input_1.get_text()) > 0:
            self.temp_input1.btn_clear.setVisible(True)
        else:
            self.temp_input1.btn_clear.setVisible(False)

    def _cancel_callback(self):
        if len(self._input_1.get_text()) > 0:
            self.temp_input1.btn_clear.setVisible(True)
        else:
            self.temp_input1.btn_clear.setVisible(False)

    def _start_input_callback(self):
        self.temp_input1.btn_clear.setVisible(False)

    def try_focus_input--- This code section failed: ---

 201       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'game3d'
           9  STORE_FAST            2  'game3d'

 202      12  LOAD_GLOBAL           1  'hasattr'
          15  LOAD_GLOBAL           2  'get_platform'
          18  LOAD_FAST             1  'input_id'
          21  BINARY_MODULO    
          22  CALL_FUNCTION_2       2 
          25  POP_JUMP_IF_FALSE   101  'to 101'

 203      28  LOAD_FAST             2  'game3d'
          31  LOAD_ATTR             2  'get_platform'
          34  CALL_FUNCTION_0       0 
          37  LOAD_FAST             2  'game3d'
          40  LOAD_ATTR             3  'PLATFORM_WIN32'
          43  COMPARE_OP            2  '=='
          46  POP_JUMP_IF_FALSE    78  'to 78'

 204      49  LOAD_GLOBAL           4  'getattr'
          52  LOAD_GLOBAL           2  'get_platform'
          55  LOAD_FAST             1  'input_id'
          58  BINARY_MODULO    
          59  CALL_FUNCTION_2       2 
          62  LOAD_ATTR             5  '_input_box'
          65  LOAD_ATTR             6  'attachWithIME'
          68  LOAD_GLOBAL           7  'False'
          71  CALL_FUNCTION_1       1 
          74  POP_TOP          
          75  JUMP_ABSOLUTE       101  'to 101'

 206      78  LOAD_GLOBAL           4  'getattr'
          81  LOAD_GLOBAL           2  'get_platform'
          84  LOAD_FAST             1  'input_id'
          87  BINARY_MODULO    
          88  CALL_FUNCTION_2       2 
          91  LOAD_ATTR             8  'show_vkb'
          94  CALL_FUNCTION_0       0 
          97  POP_TOP          
          98  JUMP_FORWARD          0  'to 101'
       101_0  COME_FROM                '98'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 22

    def get_ret_text_id(self, ret_code):
        return TEXT_MAP.get(ret_code, 609376)