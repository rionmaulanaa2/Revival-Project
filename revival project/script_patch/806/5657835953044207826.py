# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/realname/RealNameRegisterUI.py
from __future__ import absolute_import
import six
from logic.comsys.common_ui import InputBox
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gutils import template_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.comsys.chat import chat_link

class RealNameRegisterUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/real_name_register'
    DLG_ZORDER = uiconst.DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    UI_TYPE = uiconst.UI_TYPE_NORMAL
    UI_ACTION_EVENT = {'btn_language.OnClick': 'on_click_language',
       'temp_register.btn_common_big.OnClick': 'on_click_register'
       }
    GLOBAL_EVENT = {'regist_realname_result': 'on_register_realname_result'
       }

    def on_init_panel(self, confirm_cb, close_cb=None, *args, **kwargs):
        super(RealNameRegisterUI, self).on_init_panel(*args, **kwargs)
        self.region_id = None
        self.close_cb = close_cb
        self.confirm_cb = confirm_cb
        self.ui_vkb_custom_func = self.on_click_close_btn
        self._is_requesting_realname_result = False
        self.init_widget()
        return

    def on_finalize_panel(self):
        super(RealNameRegisterUI, self).on_finalize_panel()

    def init_widget(self):
        self.panel.tenp_bg.lab_title.SetString(81992)

        def touch_callback(dict_str, ele, touch, touch_event):
            chat_link.link_touch_callback(dict_str)

        msg = get_text_by_id(81991)
        msg = chat_link.linkstr_to_richtext(msg)
        self.panel.lab_tips.SetString(msg)
        self.panel.lab_tips.SetCallback(touch_callback)
        self.panel.lab_id.SetString(81990)
        self.panel.lab_country.SetString(81989)
        self.panel.temp_register.btn_common_big.SetText(get_text_by_id(81988))
        template_utils.init_common_panel(self.panel.tenp_bg, None, on_close=self.on_click_close_btn)
        self.name_box = InputBox.InputBox(self.panel.input_box_name, placeholder=get_text_by_id(81987))
        self.id_number_box = InputBox.InputBox(self.panel.input_box_number, placeholder=get_text_by_id(81986))
        self.name_box.set_rise_widget(self.panel)
        self.id_number_box.set_rise_widget(self.panel)
        self.init_country_list()
        return

    def init_country_list(self):
        country_list = []
        CHINA_AREA_CODE = 86
        china_opt_idx = -1
        area_code_conf = confmgr.get('phone_area_code', 'AreaCode', 'Content')
        for idx, info in enumerate(six.itervalues(area_code_conf)):
            area_name = info['area_name']
            region_id = info['code']
            code_str = '+{}'.format(region_id)
            country_list.append({'name': [area_name, code_str],'region_id': region_id})
            if region_id == CHINA_AREA_CODE:
                china_opt_idx = idx

        def choose(index):
            selected = country_list[index]
            self.region_id = selected.get('region_id')
            self.panel.btn_language.lab_nation.SetString(selected.get('name')[0])
            self.nation_list.setVisible(False)
            self.panel.btn_language.img_icon.setRotation(0)

        @self.panel.nation_list.nd_close.callback()
        def OnClick(btn, touch):
            self.nation_list.setVisible(False)
            self.panel.btn_language.img_icon.setRotation(0)

        template_utils.init_common_choose_list_2(self.panel.nation_list, self.panel.btn_language.img_icon, country_list, callback=choose, max_height=600)
        self.panel.nation_list.option_list.ScrollToBottom()
        choose(china_opt_idx)

    def on_click_register(self, btn, touch):
        name = self.name_box.get_text()
        id_num = self.id_number_box.get_text()
        if not name:
            NormalConfirmUI2().set_content_string(81987)
            return
        if not id_num:
            NormalConfirmUI2().set_content_string(81986)
            return
        if self._is_requesting_realname_result:
            global_data.game_mgr.show_tip(609400)
            return
        self.confirm_cb(name, id_num, self.region_id)
        self._is_requesting_realname_result = True

    def on_click_language(self, btn, touch):
        self.panel.nation_list.setVisible(True)
        self.panel.btn_language.img_icon.setRotation(180)

    def on_click_close_btn(self):
        self.close_cb and self.close_cb({'success': False})
        self.close()

    def on_register_realname_result(self, success, message):
        if not self._is_requesting_realname_result:
            return
        self._is_requesting_realname_result = False

        def confirm_cb():
            if success:
                self.close_cb and self.close_cb({'success': True})
                self.close()

        NormalConfirmUI2(on_confirm=confirm_cb).set_content_string(message)