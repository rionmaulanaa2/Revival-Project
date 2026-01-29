# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/NormalConfirmUI.py
from __future__ import absolute_import
import six_ex
import logic.gcommon.time_utility as tutil
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER, DIALOG_LAYER_ZORDER_1, UI_TYPE_CONFIRM, TOP_ZORDER, NORMAL_LAYER_ZORDER, DISCONNECT_ZORDER, SECOND_CONFIRM_LAYER
from common.const import uiconst
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
import math
PROMPT_YUEKA_DAILY_LOTTERY = 'prompt_yueka_daily_lottery'

def get_next_prompt_time--- This code section failed: ---

  20       0  LOAD_GLOBAL           0  'tutil'
           3  LOAD_ATTR             1  'get_time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            1  'now'

  21      12  LOAD_GLOBAL           2  'global_data'
          15  LOAD_ATTR             3  'achi_mgr'
          18  LOAD_ATTR             4  'get_cur_user_archive_data'
          21  LOAD_ATTR             1  'get_time'
          24  LOAD_FAST             1  'now'
          27  CALL_FUNCTION_257   257 
          30  STORE_FAST            2  'end_time'

  23      33  LOAD_FAST             1  'now'
          36  LOAD_FAST             2  'end_time'
          39  COMPARE_OP            5  '>='
          42  POP_JUMP_IF_FALSE    49  'to 49'

  24      45  LOAD_GLOBAL           5  'True'
          48  RETURN_END_IF    
        49_0  COME_FROM                '42'

  26      49  LOAD_GLOBAL           6  'False'
          52  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 27


def set_next_prompt_time(key, interval):
    now = tutil.get_time()
    global_data.achi_mgr.set_cur_user_archive_data(key, now + interval)


class NormalConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/i_friend_gold_feedback'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_cancel',
       'btn_2.btn_common.OnClick': 'on_confirm',
       'btn_1.btn_common.OnClick': 'on_cancel'
       }

    def on_init_panel(self, text, title_id=None, show_cancel_btn=False, confirm_cb=None, cancel_cb=None):
        if title_id is not None:
            self.TITLE_TEXT_ID = title_id
        super(NormalConfirmUI, self).on_init_panel()
        self.panel.lab_name_title.SetString(text)
        self.panel.btn_done.setVisible(not show_cancel_btn)
        self.panel.nd_two.setVisible(show_cancel_btn)
        self.confirm_cb = confirm_cb
        self.cancel_cb = cancel_cb
        self.set_custom_close_func(self.on_cancel)
        return

    def on_confirm(self, *args):
        if callable(self.confirm_cb):
            self.confirm_cb()
        self.close()

    def on_cancel(self, *args):
        if callable(self.cancel_cb):
            self.cancel_cb()
        self.close()


class ExtNpkDownloadConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/download_package/download_package_tips'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_cancel',
       'btn_yes.OnClick': 'on_confirm',
       'btn_no.OnClick': 'on_cancel'
       }

    def on_init_panel(self, text='', confirm_cb=None, cancel_cb=None):
        self.panel.lab_tips_2.SetString(241)
        self.panel.lab_tips_1.SetString(text)
        self.confirm_cb = confirm_cb
        self.cancel_cb = cancel_cb

    def on_confirm(self, *args):
        if callable(self.confirm_cb):
            self.confirm_cb()
        self.close()

    def call_cancel_cb(self, *args):
        self.close()

    def on_cancel(self, *args):
        SecondConfirmDlg2().confirm(content=get_text_by_id(340), confirm_callback=self.call_cancel_cb)

    def on_finalize_panel(self):
        self.confirm_cb = None
        self.cancel_cb = None
        return


class NormalConfirmUI2(BasePanel):
    PANEL_CONFIG_NAME = 'common/normal_confirm_2'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True
    IS_FULLSCREEN = True

    def on_init_panel(self, **kwargs):
        self.no_more_prompt = {}
        self.no_more_prompt_flag = True
        self.init_event()
        self.init_widget(**kwargs)

    def on_finalize_panel(self):
        if self.no_more_prompt and self.no_more_prompt_flag:
            key = six_ex.keys(self.no_more_prompt)[0]
            interval = self.no_more_prompt[key]
            set_next_prompt_time(key, interval)

    def init_event(self):
        pass

    def init_widget(self, **kwargs):
        on_confirm = kwargs.get('on_confirm', None)

        @self.panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.close()
            if on_confirm:
                on_confirm()

        content = kwargs.get('content', None)
        if content:
            self.set_content_string(content)
        confirm_text = kwargs.get('confirm_text', '')
        if confirm_text:
            self.panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(confirm_text)
        cancel_text = kwargs.get('cancel_text', '')
        if cancel_text:

            @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                self.close()

            self.panel.temp_second_confirm.temp_btn_1.setVisible(True)
            self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(cancel_text)
        self.no_more_prompt = kwargs.get('no_more_prompt', {})
        if self.no_more_prompt:
            key = six_ex.keys(self.no_more_prompt)[0]
            interval = self.no_more_prompt[key]
            self.panel.temp_second_confirm.choose_show.setVisible(True)
            self.no_more_prompt_flag = True

            @self.panel.temp_second_confirm.choose_show.btn.unique_callback()
            def OnClick(btn, touch):
                self.no_more_prompt_flag = not self.no_more_prompt_flag
                self.panel.temp_second_confirm.choose_show.choose.setVisible(self.no_more_prompt_flag)

            self.panel.temp_second_confirm.choose_show.choose.setVisible(self.no_more_prompt_flag)
        return

    def set_content_string(self, content_text):
        self.panel.temp_second_confirm.lab_content.SetString(content_text)


class TopLevelConfirmUI2(NormalConfirmUI2):
    DLG_ZORDER = TOP_ZORDER


class LobbyConfirmUI2(BasePanel):
    PANEL_CONFIG_NAME = 'common/normal_confirm_2'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True
    IS_FULLSCREEN = True
    GLOBAL_EVENT = {'lobby_scene_pause_event': '_lobby_scene_event'
       }

    def on_init_panel(self, **kwargs):
        self.init_widget(**kwargs)
        cur_scene = global_data.game_mgr.scene
        from logic.gutils.scene_utils import is_in_lobby
        if not is_in_lobby(cur_scene.scene_type):
            self.add_hide_count()

    def _lobby_scene_event(self, pause_flag):
        if not pause_flag:
            self.clear_show_count_dict()

    def init_widget(self, **kwargs):

        @self.panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            on_confirm = kwargs.get('on_confirm', None)
            self.close()
            if on_confirm:
                on_confirm()
            return

        content = kwargs.get('content', None)
        if content:
            self.set_content_string(content)
        confirm_text = kwargs.get('confirm_text', '')
        if confirm_text:
            self.panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(confirm_text)
        cancel_text = kwargs.get('cancel_text', '')
        if cancel_text:

            @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                self.close()

            self.panel.temp_second_confirm.temp_btn_1.setVisible(True)
            self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(cancel_text)
        return

    def set_content_string(self, content_text):
        self.panel.temp_second_confirm.lab_content.SetString(content_text)


class SecondConfirmDlg2(BasePanel):
    PANEL_CONFIG_NAME = 'common/normal_second_confirm_2'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    IS_FULLSCREEN = True
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        self._not_show_cb = None
        return

    def confirm(self, title='', content='', cancel_text=19002, cancel_callback=None, confirm_text=19001, confirm_callback=None, unique_callback=None, unique_key='', click_blank_close=True, cancel_auto_close=True, confirm_auto_close=True, not_show_cb=None, not_show_text=None):
        panel = self.panel
        panel.temp_second_confirm.lab_content.SetString(content)
        self._not_show_cb = not_show_cb

        @panel.unique_callback()
        def OnClick(layer, touch):
            if unique_callback:
                unique_callback()
            elif click_blank_close:
                self.close()

        @panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if cancel_auto_close:
                self.close()
            if cancel_callback:
                cancel_callback()
            if unique_key:
                global_data.emgr.second_confirm_event.emit(unique_key, False)

        panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(cancel_text)

        @panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if confirm_auto_close:
                self.close()
            if confirm_callback:
                confirm_callback()
            if unique_key:
                global_data.emgr.second_confirm_event.emit(unique_key, True)

        panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(confirm_text)
        not_show_node = panel.temp_second_confirm.choose_show
        if not_show_cb:
            not_show_node.setVisible(True)
            not_show_node.btn.SetSwallowTouch(True)
            self.panel.temp_second_confirm.choose_show.choose.setVisible(False)
            if not_show_text:
                not_show_node.text.SetString(not_show_text)

            @not_show_node.btn.unique_callback()
            def OnClick(btn, touch):
                vis = not_show_node.choose.isVisible()
                not_show_node.choose.setVisible(not vis)

        else:
            not_show_node.setVisible(False)

    def set_show_price(self, confirm_price_list, cancel_price_list):
        from logic.gutils.template_utils import splice_price
        from logic.client.const import mall_const
        if cancel_price_list:
            self.panel.temp_second_confirm.temp_btn_1.temp_price.setVisible(True)
            splice_price(self.panel.temp_second_confirm.temp_btn_1.temp_price, cancel_price_list, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_second_confirm.temp_btn_1.temp_price.setVisible(False)
        if confirm_price_list:
            self.panel.temp_second_confirm.temp_btn_2.temp_price.setVisible(True)
            splice_price(self.panel.temp_second_confirm.temp_btn_2.temp_price, confirm_price_list, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_second_confirm.temp_btn_2.temp_price.setVisible(False)

    def close(self, *args):
        if self._not_show_cb and callable(self._not_show_cb):
            not_show = self.panel.temp_second_confirm.choose_show.choose.isVisible()
            self._not_show_cb(not_show)
        super(SecondConfirmDlg2, self).close(*args)


class SecondConfirmDlg3(SecondConfirmDlg2):
    PANEL_CONFIG_NAME = 'common/normal_second_confirm_3'

    def set_btn_3(self, text, callback, auto_close=True):
        panel = self.panel

        @panel.temp_second_confirm.temp_btn_3.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if auto_close:
                self.close()
            if callback:
                callback()

        panel.temp_second_confirm.temp_btn_3.btn_common_big.SetText(text)

    def confirm(self, title='', content='', cancel_text=19002, cancel_callback=None, confirm_text=19001, confirm_callback=None, unique_callback=None, unique_key='', click_blank_close=True, cancel_auto_close=True, confirm_auto_close=True, not_show_cb=None, not_show_text=None, confirm_text_2=19001, confirm_callback_2=None):
        super(SecondConfirmDlg3, self).confirm(title, content, cancel_text, cancel_callback, confirm_text, confirm_callback, unique_callback, unique_key, click_blank_close, cancel_auto_close, confirm_auto_close, not_show_cb, not_show_text)
        panel = self.panel

        @panel.temp_second_confirm.temp_btn_3.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if confirm_auto_close:
                self.close()
            if confirm_callback_2:
                confirm_callback_2()
            if unique_key:
                global_data.emgr.second_confirm_event.emit(unique_key, True)

        panel.temp_second_confirm.temp_btn_3.btn_common_big.SetText(confirm_text_2)

    def set_show_price(self, confirm_price_list=None, confirm_price_list_2=None, cancel_price_list=None):
        from logic.gutils.template_utils import splice_price
        from logic.client.const import mall_const
        if cancel_price_list:
            self.panel.temp_second_confirm.temp_btn_1.temp_price.setVisible(True)
            splice_price(self.panel.temp_second_confirm.temp_btn_1.temp_price, cancel_price_list, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_second_confirm.temp_btn_1.temp_price.setVisible(False)
        if confirm_price_list:
            self.panel.temp_second_confirm.temp_btn_2.temp_price.setVisible(True)
            splice_price(self.panel.temp_second_confirm.temp_btn_2.temp_price, confirm_price_list, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_second_confirm.temp_btn_2.temp_price.setVisible(False)
        if confirm_price_list_2:
            self.panel.temp_second_confirm.temp_btn_3.temp_price.setVisible(True)
            splice_price(self.panel.temp_second_confirm.temp_btn_3.temp_price, confirm_price_list_2, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_second_confirm.temp_btn_3.temp_price.setVisible(False)


class SecondConfirmDlgForBind(SecondConfirmDlg2):
    PANEL_CONFIG_NAME = 'common/normal_second_confirm_2'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_TYPE = UI_TYPE_CONFIRM
    IS_FULLSCREEN = True

    def on_init_panel(self):
        pass

    def confirm(self, title='', content='', cancel_text=19002, cancel_callback=None, confirm_text=19001, confirm_callback=None, unique_callback=None, unique_key=''):
        super(SecondConfirmDlgForBind, self).confirm(title, content, cancel_text, cancel_callback, confirm_text, confirm_callback, unique_callback)
        panel = self.panel

        @panel.unique_callback()
        def OnClick(layer, touch):
            pass


class LoginReconnectConfirmDlg(SecondConfirmDlg2):
    DLG_ZORDER = DISCONNECT_ZORDER


class LoginIntimacyEventOpenConfirmDlg(SecondConfirmDlg2):
    pass


class ExitConfirmDlg(SecondConfirmDlg2):
    DLG_ZORDER = DISCONNECT_ZORDER


class BusyReconnectBg(BasePanel):
    PANEL_CONFIG_NAME = 'login/login_linking'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        import time
        global_data.busy_reconnect_bg_time = [
         time.time(), 0]
        self.hide_main_ui()
        self.panel.PlayAnimation('login')

    def on_finalize_panel(self):
        import time
        if global_data.busy_reconnect_bg_time:
            global_data.busy_reconnect_bg_time[1] = time.time()
        self.show_main_ui()


class SecondConfirmDlgForBuy(SecondConfirmDlg2):

    def on_init_panel(self):
        super(SecondConfirmDlgForBuy, self).on_init_panel()
        self.price_top_widget = None
        return

    def confirm--- This code section failed: ---

 438       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'SecondConfirmDlgForBuy'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'confirm'
          15  LOAD_FAST             1  'title'
          18  LOAD_FAST             2  'content'
          21  LOAD_FAST             3  'cancel_text'
          24  LOAD_FAST             4  'cancel_callback'
          27  LOAD_FAST             5  'confirm_text'

 439      30  LOAD_FAST             6  'confirm_callback'
          33  LOAD_FAST             7  'unique_callback'
          36  LOAD_FAST             8  'unique_key'
          39  LOAD_CONST            1  'click_blank_close'
          42  LOAD_FAST             9  'click_blank_close'
          45  CALL_FUNCTION_264   264 
          48  POP_TOP          

 440      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             3  'panel'
          55  STORE_FAST           11  'panel'

 442      58  LOAD_FAST            10  'money_type_list'
          61  POP_JUMP_IF_FALSE   148  'to 148'

 443      64  LOAD_CONST            2  ''
          67  LOAD_CONST            3  ('PriceUIWidget',)
          70  IMPORT_NAME           4  'logic.comsys.mall_ui.PriceUIWidget'
          73  IMPORT_FROM           5  'PriceUIWidget'
          76  STORE_FAST           12  'PriceUIWidget'
          79  POP_TOP          

 444      80  LOAD_FAST             0  'self'
          83  LOAD_ATTR             3  'panel'
          86  LOAD_ATTR             6  'temp_second_confirm'
          89  LOAD_ATTR             7  'nd_top_price'
          92  LOAD_ATTR             8  'setVisible'
          95  LOAD_GLOBAL           9  'True'
          98  CALL_FUNCTION_1       1 
         101  POP_TOP          

 445     102  LOAD_FAST            12  'PriceUIWidget'
         105  LOAD_FAST             4  'cancel_callback'
         108  LOAD_FAST             0  'self'
         111  LOAD_ATTR             3  'panel'
         114  LOAD_ATTR             6  'temp_second_confirm'
         117  LOAD_ATTR            10  'list_price'
         120  CALL_FUNCTION_257   257 
         123  LOAD_FAST             0  'self'
         126  STORE_ATTR           11  'price_top_widget'

 446     129  LOAD_FAST             0  'self'
         132  LOAD_ATTR            11  'price_top_widget'
         135  LOAD_ATTR            12  'show_money_types'
         138  LOAD_FAST            10  'money_type_list'
         141  CALL_FUNCTION_1       1 
         144  POP_TOP          
         145  JUMP_FORWARD          0  'to 148'
       148_0  COME_FROM                '145'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 120

    def on_finalize_panel(self):
        if self.price_top_widget:
            self.price_top_widget.destroy()
            self.price_top_widget = None
        return


class SecondConfirmDlgWithCalm(SecondConfirmDlg2):

    def on_init_panel(self):
        super(SecondConfirmDlgWithCalm, self).on_init_panel()
        self.init_confirm_btn_with_calm()

    def init_confirm_btn_with_calm(self):
        if not self.panel or not self.panel.temp_second_confirm:
            return
        btn_confirm = self.panel.temp_second_confirm.temp_btn_2
        if not btn_confirm:
            return
        btn_confirm.btn_common_big.SetEnable(False)

        def count_down(pass_time):
            left_time = 3 - pass_time
            left_time = int(math.ceil(left_time))
            if left_time >= 0:
                confirm_str = get_text_by_id(633709).format(left_time)
                btn_confirm.btn_common_big.SetText(confirm_str)

        def count_down_end():
            btn_confirm.btn_common_big.SetEnable(True)
            confirm_str = get_text_by_id(80305)
            btn_confirm.btn_common_big.SetText(confirm_str)

        count_down(0)
        btn_confirm.TimerAction(count_down, 3, callback=count_down_end, interval=1)

    def confirm(self, title='', content='', cancel_text=19002, cancel_callback=None, confirm_text=19001, confirm_callback=None, unique_callback=None, unique_key='', click_blank_close=True, cancel_auto_close=True, confirm_auto_close=True, not_show_cb=None, not_show_text=None):
        super(SecondConfirmDlgWithCalm, self).confirm(title, content, cancel_text, cancel_callback, confirm_text, confirm_callback, unique_callback, unique_key, click_blank_close, cancel_auto_close, confirm_auto_close, not_show_cb, not_show_text)
        panel = self.panel

        @panel.unique_callback()
        def OnClick(layer, touch):
            pass