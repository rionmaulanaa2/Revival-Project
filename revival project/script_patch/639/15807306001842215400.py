# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallMeowItemListWidget.py
from __future__ import absolute_import
import six_ex
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.comsys.mall_ui.MallCommonItemListWidget import MallCommonItemListWidget
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_WALL_PICTURE
from common.cfg import confmgr
from logic.gutils import template_utils

class MallMeowItemListWidget(MallCommonItemListWidget):
    if G_IS_NA_PROJECT:
        TYPE_TXT_IDS = [
         12183, 12184, 12185, 12186, 80934, 12187]
        TYPES = ['all', L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_WALL_PICTURE, 'other']
        CMP_TYPE = (L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_MECHA_SP_ACTION, L_ITEM_TYPE_WALL_PICTURE)
    else:
        TYPE_TXT_IDS = [
         12183, 12184, 12185, 12186, 12187]
        TYPES = ['all', L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_MECHA_SP_ACTION, 'other']
        CMP_TYPE = (L_ITEM_TYPE_LOBBY_SKIN, L_ITEM_TYPE_MUSIC, L_ITEM_TYPE_MECHA_SP_ACTION)

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)
        new_items = []
        if self.cur_tab_index is not None:
            tab_type = self.TYPES[self.cur_tab_index]
            if tab_type == 'all':
                new_items = items
            else:
                for goods_id in items:
                    item_no = mall_utils.get_goods_item_no(goods_id)
                    i_type = item_utils.get_lobby_item_type(item_no)
                    if tab_type == i_type or tab_type == 'other' and i_type not in self.TYPES:
                        new_items.append(goods_id)

        else:
            new_items = items
        return mall_utils.sort_meow_goods_ids(new_items)

    def cb_create_item(self, index, item_widget):
        goods_id = self.goods_items[index]
        extra_info = {}
        if self.panel.GetTemplatePath() == 'mall/i_mall_content_item':
            extra_info['money_icon_scale'] = 1
        conf = confmgr.get('mall_config', goods_id, default={})
        init_item_func_name = conf.get('cGoodsInfo', {}).get('init_item_func')
        if init_item_func_name:
            init_item_func = getattr(template_utils, init_item_func_name)
            init_item_func and init_item_func(item_widget, goods_id, is_show_kind=False, extra_info=extra_info)
        else:
            template_utils.init_mall_groceries_item(item_widget, goods_id, is_show_kind=False, extra_info=extra_info)
        item_id = mall_utils.get_goods_item_no(goods_id)
        item_type = item_utils.get_lobby_item_type(item_id)
        if item_type == L_ITEM_TYPE_MECHA_SP_ACTION:
            item_widget.img_base.setVisible(True)
        if item_type in self.CMP_TYPE:
            item_widget.btn_preview.setVisible(True)

            @item_widget.btn_preview.unique_callback()
            def OnClick(btn, touch, item_no=item_id):
                if item_no:
                    from logic.gutils.jump_to_ui_utils import jump_to_lobby_skin_preview
                    show_type = self.TYPES[self.cur_tab_index]
                    if type(show_type) is int:
                        show_types = (
                         show_type,)
                    else:
                        show_types = None
                    jump_to_lobby_skin_preview(item_no, show_types)
                return

        else:
            item_widget.btn_preview.setVisible(False)
        limite_by_day, _, _ = mall_utils.buy_num_limite_by_day(goods_id)
        limite_by_week, _, _ = mall_utils.buy_num_limite_by_week(goods_id)
        item_widget.nd_sold_out.setVisible(limite_by_day or limite_by_week)
        if goods_id is None:
            item_widget.bar.SetEnable(False)
        else:
            item_widget.bar.SetEnable(True)

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id):
                if mall_utils.item_has_owned_by_goods_id(goods_id):
                    return
                conf = confmgr.get('mall_config', goods_id, default={})
                confirmUI_name = conf.get('cGoodsInfo', {}).get('confirmUI')
                if confirmUI_name:
                    from logic.comsys.mall_ui import BuyConfirmUIInterface
                    confirmUI = getattr(BuyConfirmUIInterface, confirmUI_name)
                    confirmUI and confirmUI(goods_id)
                else:
                    from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                    groceries_buy_confirmUI(goods_id)

        return