# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineShareUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from common.cfg import confmgr
from logic.gutils.skin_define_utils import get_main_skin_id, init_action_list, delete_action_list
import copy
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.framework import Functor
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.text_utils import check_review_name, check_emoji_name
from logic.gcommon.common_const import chat_const
from logic.gutils.share_utils import is_share_enable

class SkinDefineShareUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_define_display'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn',
       'temp_btn_use.btn_common_big.OnClick': 'on_click_share',
       'btn_action.OnClick': 'on_click_action'
       }

    def on_init_panel(self, *args, **kwargs):
        super(SkinDefineShareUI, self).on_init_panel()
        self._callback = None
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('loop')
        self.screen_capture_helper = ScreenFrameHelper()
        self.action_conf = copy.deepcopy(confmgr.get('skin_define_action'))
        self.no_action_tag = True
        self.skin_id = 1
        self.title_widget = None
        self.input_box = None
        return

    def setBackFunctionCallback(self, callback):
        self._callback = callback

    def set_mecha_info(self, mecha_id, skin_id, mecha_text, skin_text):
        self.mecha_id = mecha_id
        self.skin_id = skin_id
        self.panel.lab_mech_name.SetString(mecha_text)
        self.panel.lab_skin_name.SetString(skin_text)
        self.init_action_list()
        self.is_guided_action = global_data.achi_mgr.get_cur_user_archive_data('skin_define_share_action')
        if not self.is_guided_action and not self.no_action_tag:
            global_data.ui_mgr.show_ui('SkinDefineGuideShareActionUI', 'logic.comsys.mecha_display')
            self.is_guided_action = True

    def set_action_list_vis(self, is_visible):
        self.panel.btn_action.setVisible(is_visible)
        self.panel.actione_list.setVisible(is_visible)

    def on_click_action(self, *args):
        if self.no_action_tag:
            return
        if self.panel.actione_list.isVisible():
            self.hide_action_list()
        else:
            self.show_action_list()

    def show_action_list(self):
        self.panel.actione_list.setVisible(True)
        self.panel.btn_action.img_icon.setRotation(180)

    def hide_action_lsit(self):
        self.panel.actione_list.setVisible(False)
        self.panel.btn_action.img_icon.setRotation(0)

    def init_action_list(self):
        action_list = self.action_conf.get(str(self.skin_id), {}).get('cAction', [])
        if not action_list:
            action_list = self.action_conf.get(str(self.mecha_id), {}).get('cAction', [])
            if not action_list:
                log_error('\xe6\x90\x9e\xe9\x94\xa4\xe5\xad\x90\xef\xbc\x9f \xe8\xa1\xa8\xe9\x83\xbd\xe4\xb8\x8d\xe5\xa1\xab\xef\xbc\x9f')
                self.no_action_tag = True
                self.set_action_list_vis(False)
                return
        self.no_action_tag = False
        init_action_list(self, action_list)

    def on_click_share(self, *args):
        if self.screen_capture_helper:

            def custom_cb(*args):
                share_ui = global_data.ui_mgr.get_ui('ShareUI')
                if not share_ui:
                    print('SkinDefineShareUI cant get ShareUI GAOCHUIZI?')
                    return
                share_ui.panel.pnl_list_share.setVisible(is_share_enable())
                btn_infos = [
                 {'template_name': 'common/i_common_button_2','click_cb': self.on_click_friend_btn,'btn_name': 'btn_common',
                    'btn_text': 10259},
                 {'template_name': 'common/i_common_button_2','click_cb': self.on_click_chat_btn,'btn_name': 'btn_common',
                    'btn_text': 800150}]
                if share_ui and share_ui.is_valid():
                    share_ui.add_custom_button(btn_infos, is_head=True)

            self.screen_capture_helper.take_screen_shot([], self.panel, custom_cb=custom_cb)

    def on_resolution_changed(self):
        global_data.ui_mgr.close_ui('ShareUI')

    def on_click_back_btn(self, *args):
        delete_action_list(self)
        self.close()

    def on_click_friend_btn(self, *args):
        share_ui = global_data.ui_mgr.get_ui('ShareUI')
        if not share_ui:
            print('SkinDefineShareUI cant get ShareUI')
            return
        share_ui.on_click_friend_btn(self.on_click_friend)

    def on_click_friend(self, f_data, *args):
        if not self.check_share_content():
            return
        self.open_title_widget(self.skin_id, f_data['uid'], f_data['char_name'], f_data['lv'])

    def on_click_chat_btn(self, *args):
        if not self.check_share_content():
            return
        self.open_title_widget(self.skin_id, 0, '', 1)

    def check_share_content(self):
        ui = global_data.ui_mgr.get_ui('SkinDefineUI')
        if not ui:
            return False
        result = ui.check_mecha_status_share_simple()
        if result > 0:
            return True
        return False

    def open_title_widget(self, skin_id, f_uid, f_name, f_lv):
        share_ui = global_data.ui_mgr.get_ui('ShareUI')
        if not share_ui:
            print('SkinDefineShareUI cant get ShareUI')
            return
        if not share_ui.panel or share_ui.panel.IsDestroyed():
            return
        self.title_widget = global_data.uisystem.load_template_create('setting/setting_highlight/i_rename', parent=share_ui.panel)
        self.title_widget.panel.btn_close.BindMethod('OnClick', self.on_click_close_title_widget)
        self.title_widget.PlayAnimation('appear')
        self.title_widget.panel.lab_title.SetString(get_text_by_id(860154))
        self.title_widget.panel.nd_subtitle.setVisible(True)
        self.title_widget.panel.nd_subtitle.lab_subtitle.SetString(get_text_by_id(860155))
        self.input_box = InputBox.InputBox(self.title_widget.panel.inputbox, max_length=20, placeholder=get_text_by_id(860156), need_sp_length_func=True)
        self.input_box.set_rise_widget(self.title_widget)
        self.title_widget.confirm.btn_common_big.SetText(get_text_by_id(81980))
        self.title_widget.confirm.btn_common_big.BindMethod('OnClick', Functor(self.on_click_confirm_share, skin_id, f_uid, f_name, f_lv))

    def on_click_close_title_widget(self, *args):
        if self.title_widget:
            self.title_widget.setVisible(False)
            self.title_widget.Destroy()
            self.title_widget = None
        if self.input_box:
            self.input_box.destroy()
            self.input_box = None
        return

    def on_click_confirm_share(self, skin_id, f_uid, f_name, f_lv, *args):
        title_content = self.input_box.get_text()
        if not title_content:
            title_content = ''
        else:
            if check_emoji_name(title_content):
                global_data.game_mgr.show_tip(get_text_by_id(81979))
                return
            if not check_review_name(title_content):
                global_data.game_mgr.show_tip(get_text_by_id(81979))
                return
        head_frame = global_data.player.get_head_frame()
        head_photo = global_data.player.get_head_photo()
        result = global_data.player.share_mecha_custom_skin(title_content, skin_id, f_uid, (head_frame, head_photo))
        if result and f_uid > 0:
            decal_data = global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), [])
            color_data = global_data.player.get_mecha_color().get(str(skin_id), {})
            extra_data = {'type': chat_const.MSG_TYPE_SKIN_DEFINE,
               'title': title_content,
               'skin_id': skin_id,
               'custom_skin': {'decal': copy.deepcopy(decal_data),'color': copy.deepcopy(color_data)},'name': global_data.player.get_name(),
               'head_info': (
                           head_frame, head_photo)
               }
            global_data.message_data.recv_to_friend_msg(f_uid, f_name, '', f_lv, extra=extra_data)
        share_ui = global_data.ui_mgr.get_ui('ShareUI')
        if not share_ui:
            print('SkinDefineShareUI cant get ShareUI')
            return
        else:
            share_ui.close()
            self.title_widget = None
            self.input_box = None
            return

    def on_finalize_panel(self):
        self.panel.PlayAnimation('disappear')
        if self._callback:
            self._callback()
            self._callback = None
        if self.screen_capture_helper:
            self.screen_capture_helper.destroy()
            self.screen_capture_helper = None
        super(SkinDefineShareUI, self).on_finalize_panel()
        return