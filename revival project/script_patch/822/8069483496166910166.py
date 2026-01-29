# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineBuyDecalBoxUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_type, init_lobby_bag_item, get_recycle_item_price_tips
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon.item import lobby_item_type
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils
from logic.client.const import mall_const
import logic.gcommon.const as gconst
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.mecha_skin_utils import get_mecha_skin_goods_id
from common.utils.cocos_utils import CCRect
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI

class SkinDefineBuyDecalBoxUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'mech_display/applique_box_choose'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(SkinDefineBuyDecalBoxUI, self).on_init_panel()
        self.init_params()
        self.init_box_list()

    def init_params(self):
        self.decal_conf = confmgr.get('skin_define_pure_decal')
        self.box_data = [
         {'name': 494035,
            'desc': 500401,
            'bar': 'gui/ui_res_2/mall/img_role_define_item_bar_purple.png',
            'img': 'gui/ui_res_2/item/others/50400006.png',
            'item_id': 50400006
            },
         {'name': 494036,
            'desc': 500402,
            'bar': 'gui/ui_res_2/mall/img_role_define_item_bar_yellow.png',
            'img': 'gui/ui_res_2/item/others/50400007.png',
            'item_id': 50400007
            }]
        self.preview_widget = None
        return

    def init_box_list(self):
        all_items = self.list_box.SetInitCount(len(self.box_data))
        for idx, ui_item in enumerate(all_items):
            data = self.box_data[idx]
            ui_item.lab_name.SetString(get_text_by_id(data['name']))
            ui_item.lab_details.SetString(get_text_by_id(data['desc']))
            ui_item.img_bar.SetFrames('', [data['bar'], data['bar'], data['bar']], True, CCRect(34, 25, 166, 199))
            ui_item.img_reward.SetDisplayFrameByPath('', data['img'])
            item_id = data['item_id']

            @ui_item.img_bar.unique_callback()
            def OnClick(_btn, _touch, _id=item_id, *args):
                if _id:
                    if item_utils.can_jump_to_ui(str(_id)):
                        item_utils.jump_to_ui(str(_id))
                        self.close()
                    else:
                        goods_id = _id
                        groceries_buy_confirmUI(str(goods_id))

            @ui_item.btn_preview.unique_callback()
            def OnClick(_btn, _touch, _id=item_id, *args):
                self.open_preview_widget(_id)

    def open_preview_widget(self, box_item_id):
        box_conf = confmgr.get('skin_define_decal_box_preview').get(str(box_item_id), {})
        decal_list = box_conf.get('cList', [])
        if not decal_list:
            return
        if not self.preview_widget:
            self.preview_widget = global_data.uisystem.load_template_create('common/common_gift_preview', parent=self.panel)
            self.preview_widget.btn_close.BindMethod('OnClick', self.on_click_hide_preview_widget)
        self.preview_widget.PlayAnimation('appear')
        self.preview_widget.setVisible(True)
        self.preview_widget.list_review_all.DeleteAllSubItem()
        self.preview_widget.list_review_all.SetInitCount(len(decal_list))
        for idx, ui_item in enumerate(self.preview_widget.list_review_all.GetAllItem()):
            item_id = decal_list[idx]
            item_conf = self.decal_conf.get(str(item_id))
            res_path = item_conf.get('cResPath')
            ui_item.item.SetDisplayFrameByPath('', res_path)
            ui_item.img_frame.SetDisplayFrameByPath('', item_utils.get_lobby_item_rare_degree_pic_by_item_no(str(item_id), 1, True))
            ui_item.btn_choose.SetEnable(False)

    def on_click_hide_preview_widget(self, *args):
        if self.preview_widget:
            self.preview_widget.setVisible(False)

    def on_finalize_panel(self):
        self.init_params()
        super(SkinDefineBuyDecalBoxUI, self).on_finalize_panel()