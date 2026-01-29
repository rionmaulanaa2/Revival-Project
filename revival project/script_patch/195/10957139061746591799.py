# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/item_use/ItemUseConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, get_lobby_item_pic_by_item_no
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class ItemUseConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_use'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_btn_save.btn_common.OnClick': 'on_close',
       'temp_btn_buy.btn_common.OnClick': 'on_use'
       }

    def on_init_panel(self, item_no, item_num=1):
        super(ItemUseConfirmUI, self).on_init_panel()
        self.set_custom_close_func(self.on_close)
        self.item_no = item_no
        self.item_num = item_num
        self.item_widgets = {}
        self.init_widget()
        self.init_event()

    def init_event(self):
        pass

    def on_finalize_panel(self):
        self.set_custom_close_func(None)
        return

    def init_widget(self):
        self.set_item_info()

    def set_item_info(self):
        self.panel.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(self.item_no))
        template_utils.init_mall_item_try_icon(self.panel.icon_try, None, using_item_no=self.item_no)
        iten_name = get_lobby_item_name(self.item_no)
        if self.item_num > 1:
            self.panel.lab_name.SetString(''.join([iten_name, 'X', str(self.item_num)]))
        else:
            self.panel.lab_name.SetString(iten_name)
        return

    def on_use(self, *args):
        usage = item_utils.get_lobby_item_usage(self.item_no)
        if not global_data.player:
            self.close()
            return
        item = global_data.player.get_item_by_no(self.item_no)
        if item:
            item_data = {'id': item.id,'item_no': item.item_no,'quantity': self.item_num
               }
            item_utils.try_use_lobby_item(item_data, usage)
        self.close()

    def on_close(self, *args):
        global_data.game_mgr.show_tip(get_text_local_content(603001))
        self.close()

    def set_title(self, title_str):
        if self.panel and self.panel.temp_bg and self.panel.temp_bg.lab_title:
            self.panel.temp_bg.lab_title.SetString(title_str)

    def set_lab_success(self, success_str):
        if self.panel and self.panel.lab_success:
            self.panel.lab_success.SetString(success_str)