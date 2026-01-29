# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/SkinDefineWidget.py
from __future__ import absolute_import
import six
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.comsys.common_ui.ScaleableVerContainer import ScaleableVerContainer
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils
from logic.client.const import mall_const
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
import cc
from logic.gcommon.item import lobby_item_type
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper
from logic.gutils import red_point_utils

class SkinListWidget(object):

    def __init__(self, panel):
        self._show_skin_list = []
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        self.panel = panel
        self._selected_index = 0
        self._list_sview = InfiniteScrollHelper(self.panel.list_skin, self.panel, up_limit=500, down_limit=500)
        self._list_sview.set_template_init_callback(self.init_dress_item)

    def set_skin_select_callback(self, callback):
        self._skin_select_callback = callback

    def destroy(self):
        self._selected_index = None
        self._show_skin_list = []
        self.panel = None
        self.role_skin_config = None
        self._skin_select_callback = None
        return

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def _skin_up_select_callback(self, selected_index, with_callback=True):
        if self._selected_index is not None:
            nd = self._list_sview.get_list_item(self._selected_index)
            if nd:
                nd.nd_choose.setVisible(False)
        skin_id = self._show_skin_list[selected_index]
        self._selected_index = selected_index
        nd = self._list_sview.get_list_item(self._selected_index)
        if nd:
            nd.nd_choose.setVisible(True)
        if self._skin_select_callback and with_callback:
            self._skin_select_callback(skin_id)
        return

    def update_show_list(self, _show_skin_list):
        if _show_skin_list == self._show_skin_list:
            return
        self._show_skin_list = _show_skin_list
        self._list_sview.update_data_list(_show_skin_list)
        self._list_sview.center_with_index(self._selected_index, self.init_dress_item)
        self._list_sview.refresh_showed_item()
        self._list_sview.update_scroll_view()

    def init_dress_item(self, skin_item, item_no):
        item_utils.update_limit_btn(item_no, skin_item.temp_limit)
        name_text = item_utils.get_lobby_item_name(item_no)
        skin_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(skin_item, item_no)
        skin_cfg = self.role_skin_config.get(str(item_no))
        if skin_cfg:
            item_utils.check_skin_tag(skin_item.nd_kind, item_no)
            skin_half_imge_role = skin_cfg.get('half_img_role')
            if skin_half_imge_role is not None:
                skin_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_role)
        template_utils.show_remain_time(skin_item.nd_time, skin_item.nd_time.lab_time, item_no)
        own = global_data.player.has_item_by_no(item_no) if global_data.player else False
        skin_item.nd_lock.setVisible(not own)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
        red_point_utils.show_red_point_template(skin_item.nd_new, show_new)
        if skin_item.nd_xingyuan:
            top_skin_id = dress_utils.get_top_skin_id_by_skin_id(item_no)
            if top_skin_id is not None:
                skin_item.nd_xingyuan.setVisible(str(top_skin_id) != str(item_no))

        @skin_item.btn.callback()
        def OnClick(btn, touch):
            if item_no in self._show_skin_list:
                idx = self._show_skin_list.index(item_no)
                self._skin_up_select_callback(idx)

        return

    def force_select_clothing_by_skin_id(self, skin_id, with_select_callback):
        if skin_id in self._show_skin_list:
            selected_index = self._show_skin_list.index(skin_id)
            self._list_sview.center_with_index(selected_index, self.init_dress_item)
            self._skin_up_select_callback(selected_index, with_select_callback)

    def get_skin_id_to_ui_item_dict(self):
        refresh_list = self._list_sview.get_view_list()
        _skin_id_to_item = {}
        for item_widget, data in refresh_list:
            _skin_id_to_item[data] = item_widget

        return _skin_id_to_item

    def update_skin_id_show(self, item_no):
        if item_no in self._show_skin_list:
            idx = self._show_skin_list.index(item_no)
            ui_item = self._list_sview.get_list_item(idx)
            if ui_item:
                self.init_dress_item(ui_item, item_no)

    def update_all_skin(self):
        for index, item_no in enumerate(self._show_skin_list):
            ui_item = self._list_sview.get_list_item(index)
            if ui_item:
                self.init_dress_item(ui_item, item_no)


class SkinDefineWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'refresh_item_red_point': self.refresh_all_items_rp,
           'player_item_update_event_with_id': self.on_buy_good_success,
           'weapon_sfx_change': self.weapon_sfx_change
           }
        super(SkinDefineWidget, self).__init__(parent, panel)
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        self.top_role_skin_conf = confmgr.get('top_role_skin_conf')
        self.role_id = 0
        self.top_skin_id = 0
        self.chosen_item = None
        self.preview_item = None
        self._has_init = False
        self._skin_list_widget = SkinListWidget(self.panel)
        self._skin_list_widget.set_skin_select_callback(self._skin_up_select_callback)
        self.panel.btn_buy.btn_common.BindMethod('OnClick', self._on_click_dress_skin)
        return

    def destroy(self):
        if self._skin_list_widget:
            self._skin_list_widget.destroy()
            self._skin_list_widget = None
        super(SkinDefineWidget, self).destroy()
        return

    def _skin_up_select_callback(self, skin_id):
        self.try_on_skin(skin_id)
        self.update_btn_buy()

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def show_panel(self, flag):
        self.panel.setVisible(flag)

    def refresh_all_content(self):
        self.refresh_ui_show()
        new_skin_id = self.parent.get_chosen_skin()
        new_preview_item = self.parent.get_preview_skin_id()
        self.chosen_item = new_skin_id
        if new_preview_item != self.preview_item:
            self.jump_to_skin(new_preview_item)
        self.update_btn_buy()

    def set_role_id(self, role_id, top_skin_id):
        self.role_id = role_id
        self.top_skin_id = top_skin_id

    def refresh_all_items_rp(self):
        skin_id_to_item = self._skin_list_widget.get_skin_id_to_ui_item_dict()
        for item_no, item_widget in six.iteritems(skin_id_to_item):
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            item_widget and red_point_utils.show_red_point_template(item_widget.nd_new, show_new)

    def refresh_own_count(self):
        has_func = global_data.player.has_item_by_no if global_data.player else (lambda : 0)
        own_count = 0
        data_list = self.top_role_skin_conf.get(str(self.top_skin_id), [])
        for item_no in data_list:
            own = has_func(item_no)
            if own:
                own_count += 1

        self.panel.lab_number.setString('%d/%d' % (own_count, len(data_list)))

    def try_on_skin(self, skin_id):
        if self.preview_item == skin_id:
            return False
        self.preview_item = skin_id
        self.parent.change_preview_skin(skin_id)
        self.req_del_item_redpoint(skin_id)
        return True

    def req_del_item_redpoint(self, skin_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_id)

    def update_btn_buy(self):
        btn = self.panel.btn_buy
        item_no = self.preview_item
        skin_data = global_data.player.get_item_by_no(item_no)
        role_data = global_data.player.get_item_by_no(self.role_id)
        self.panel.temp_price.setVisible(False)
        self.panel.lab_get_method.setVisible(False)
        if skin_data is None:
            btn.btn_common.SetEnable(True)
            goods_id = self.role_skin_config.get(str(item_no), {}).get('goods_id')
            price = mall_utils.get_mall_item_price(goods_id)
            unowned_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(goods_id)
            from logic.gutils.mall_utils import get_goods_item_open_date, check_limit_time_lottery_open_info
            open_date_range = get_goods_item_open_date(str(item_no))
            opening, _ = check_limit_time_lottery_open_info(open_date_range)
            if not opening:
                btn.btn_common.SetEnable(False)
                btn.btn_common.SetText(80828)
                access_txt = item_utils.get_item_access(str(item_no))
                if access_txt:
                    self.panel.lab_get_method.SetString(access_txt)
                    self.panel.lab_get_method.setVisible(True)
            elif unowned_item_nos:
                self.panel.temp_price.setVisible(False)
                btn.btn_common.SetEnable(False)
                name_text = item_utils.get_lobby_item_name(unowned_item_nos[0])
                self.panel.lab_get_method.setVisible(True)
                self.panel.lab_get_method.SetString(get_text_by_id(81606, {'skin_name': name_text}))
                btn.btn_common.SetText(80828)
            elif item_utils.can_jump_to_ui(item_no):
                self.panel.lab_get_method.setVisible(True)
                self.panel.lab_get_method.SetString(item_utils.get_item_access(item_no))
                btn.btn_common.SetText(2222)
            elif price:
                template_utils.init_price_view(self.panel.temp_price, goods_id, mall_const.DEF_PRICE_COLOR)
                self.panel.temp_price.setVisible(True)
                btn.btn_common.SetText(get_text_by_id(14005))
            else:
                btn.btn_common.SetEnable(False)
                btn.btn_common.SetText(80828)
                access_txt = item_utils.get_item_access(str(item_no))
                if access_txt:
                    self.panel.lab_get_method.SetString(access_txt)
                    self.panel.lab_get_method.setVisible(True)
        else:
            btn.btn_common.SetEnable(False)
            if role_data is None:
                btn.btn_common.SetText(get_text_by_id(2215))
            elif self.chosen_item == item_no:
                btn.btn_common.SetText(get_text_by_id(14007))
            else:
                btn.btn_common.SetText(get_text_by_id(14006))
                btn.btn_common.SetEnable(True)
        return

    def on_hide(self):
        pass

    def refresh_ui_show(self):
        data_list = self.top_role_skin_conf.get(str(self.top_skin_id), [])
        if not data_list:
            data_list = [
             int(self.top_skin_id)]
        self._skin_list_widget.update_show_list(data_list)
        self._has_init = True
        self.refresh_own_count()

    def on_dress_change(self, new_skin_id):
        self.chosen_item = new_skin_id
        if new_skin_id != self.preview_item:
            self.jump_to_skin(new_skin_id)
        self.update_btn_buy()

    def jump_to_skin(self, skin_id):
        from logic.gutils import item_utils
        item_type = item_utils.get_lobby_item_type(skin_id)
        if item_type not in [lobby_item_type.L_ITEM_TYPE_ROLE_SKIN]:
            return
        if not self._has_init:
            self.refresh_ui_show()
        self._skin_list_widget.force_select_clothing_by_skin_id(skin_id, with_select_callback=True)
        self.update_btn_buy()

    def get_preview_skin_id(self):
        return self.parent.get_preview_skin_id()

    def _on_click_dress_skin(self, *args):
        skin_data = global_data.player.get_item_by_no(self.preview_item)
        if skin_data is None:
            goods_id = self.role_skin_config.get(str(self.preview_item), {}).get('goods_id')
            price = mall_utils.get_mall_item_price(goods_id)
            if price and not item_utils.is_jump_to_lottery(self.preview_item):
                role_or_skin_buy_confirmUI(goods_id)
            else:
                item_utils.jump_to_ui(self.preview_item)
        else:
            global_data.player.install_role_skin_scheme(self.role_id, self.top_skin_id, self.preview_item, {FASHION_POS_SUIT: self.preview_item})
        return

    def on_buy_good_success(self, item_no):
        if self._skin_list_widget:
            self._skin_list_widget.update_skin_id_show(item_no)
        self.update_btn_buy()
        self.refresh_own_count()

    def weapon_sfx_change(self, item_no, value):
        if self._skin_list_widget:
            self._skin_list_widget.update_skin_id_show(item_no)