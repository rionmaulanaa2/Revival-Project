# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/red_packet/RedPacketCoverChangeUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.red_packet_utils import get_red_packet_cover_info, get_open_packet_cover_list, init_red_packet_cover_item, get_user_setting_red_packet_cover, set_user_setting_red_packet_cover
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from common.const.uiconst import UI_VKB_CLOSE
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
from logic.gutils.jump_to_ui_utils import jump_to_share
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.comsys.share.ShareUI import ShareUI

class RedPacketCoverChangeUI(BasePanel):
    PANEL_CONFIG_NAME = 'chat/red_packet/open_red_packet_setting'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'
       }
    GLOBAL_EVENT = {'buy_good_success': 'on_buy_goods_success'
       }
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        self.regist_main_ui()
        self.open_red_packet_cover_list = get_open_packet_cover_list()
        self.show_red_packet_cover_list = self.open_red_packet_cover_list
        self.own_red_packet_cover_list = []
        self.choose_item = None
        self.choose_item_no = get_user_setting_red_packet_cover()
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self._screen_capture_helper = ScreenFrameHelper()
        self.panel.btn_share.BindMethod('OnClick', lambda btn, touch: self.on_click_btn_share())
        self.init_red_packet_list()
        return

    def init_red_packet_list(self):
        self.panel.list_content.SetInitCount(1)
        self.refresh_show_cover()
        self.refresh_cover_own_list()
        self.refresh_show_red_packet_cover(self.choose_item_no)

    def on_choose_red_packet_cover(self, idx):
        if self.choose_item:
            self.choose_item.btn_choose.SetSelect(False)
        self.choose_item_no = self.show_red_packet_cover_list[idx]
        self.choose_item = self.panel.list_item.GetItem(idx)
        self.choose_item.btn_choose.SetSelect(True)
        self.refresh_show_red_packet_cover(self.show_red_packet_cover_list[idx])
        self.refresh_cover_btn_state()

    def refresh_show_red_packet_cover(self, packet_item_id):
        init_red_packet_cover_item(self.panel.temp_item, packet_item_id)
        self.panel.temp_item.btn_choose.SetEnable(False)
        self.panel.lab_name.SetString(get_lobby_item_name(packet_item_id))
        self.panel.list_content.GetItem(0).lab_describe.SetString(get_lobby_item_desc(packet_item_id))
        if global_data.player:
            has_item = global_data.player.has_item_by_no(int(packet_item_id))
            if has_item:
                self.panel.btn_click.SetText(868026)
                self.panel.btn_click.SetSelect(True)

    def refresh_show_cover(self):
        self.panel.list_item.SetInitCount(len(self.show_red_packet_cover_list))
        for idx in range(len(self.show_red_packet_cover_list)):
            packet_item = self.panel.list_item.GetItem(idx)
            init_red_packet_cover_item(packet_item, self.show_red_packet_cover_list[idx])
            packet_item.btn_choose.SetSelect(False)
            if self.show_red_packet_cover_list[idx] == self.choose_item_no:
                packet_item.btn_choose.SetSelect(True)
                self.choose_item = packet_item
            else:
                packet_item.btn_choose.SetSelect(False)
            packet_item.btn_choose.BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_choose_red_packet_cover(idx))
            if global_data.player:
                has_item = global_data.player.has_item_by_no(int(self.show_red_packet_cover_list[idx]))
                packet_item.nd_lock.setVisible(not bool(has_item))

    def refresh_cover_own_list(self):
        self.own_red_packet_cover_list = []
        for i in range(len(self.open_red_packet_cover_list)):
            if self._own_widget.has_item(self.open_red_packet_cover_list[i]):
                self.own_red_packet_cover_list.append(self.open_red_packet_cover_list[i])

        self.panel.lab_got.SetString(get_text_by_id(80860) + '<color=3B57D9FF>{}</color>/<color=363B51FF>{}</color>'.format(len(self.own_red_packet_cover_list), len(self.open_red_packet_cover_list)))

    def refresh_cover_btn_state(self):
        if not self.choose_item:
            return
        has_item = global_data.player and global_data.player.has_item_by_no(int(self.choose_item_no))
        packet_cover_info = get_red_packet_cover_info(self.choose_item_no)
        if has_item:
            if self.choose_item_no == get_user_setting_red_packet_cover():
                self.panel.btn_click.SetEnable(False)
                self.panel.btn_click.SetText(2213)
            else:
                self.panel.btn_click.SetEnable(True)
                self.panel.btn_click.SetSelect(True)
                self.panel.btn_click.SetText(868026)
                self.panel.btn_click.BindMethod('OnClick', lambda btn, touch: self.on_set_show_used(self.choose_item_no))
        else:
            goods_id = packet_cover_info.get('goods_id')
            if not goods_id:
                self.panel.btn_click.SetEnable(False)
                self.panel.btn_click.SetSelect(False)
            else:
                self.panel.btn_click.SetEnable(True)
                self.panel.btn_click.SetSelect(True)
                self.panel.btn_click.SetText(12017)
                self.panel.btn_click.BindMethod('OnClick', lambda btn, touch, goods=goods_id: RoleAndSkinBuyConfirmUI(goods_id=str(goods)))

    def on_buy_goods_success(self):
        self.refresh_show_cover()
        self.refresh_cover_btn_state()
        global_data.game_mgr.show_tip(81001)

    def on_set_show_used(self, item_no):
        set_user_setting_red_packet_cover(item_no)
        self.refresh_cover_btn_state()

    def on_click_own_btn(self, switch):
        if switch:
            self.refresh_cover_own_list()
            self.show_red_packet_cover_list = self.own_red_packet_cover_list
        else:
            self.show_red_packet_cover_list = self.open_red_packet_cover_list
        self.choose_item = None
        self.refresh_show_cover()
        return

    def on_click_btn_share(self):
        if self._screen_capture_helper:

            def cb(*args):
                pass

            self._screen_capture_helper.take_screen_shot([self.__class__.__name__], self.panel, custom_cb=cb, need_share_ui=True, head_nd_name='nd_player_info_1', need_draw_rt=True)

    def on_click_btn_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.unregist_main_ui()
        if self._own_widget:
            self._own_widget.destroy()
            self._own_widget = None
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        return