# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVETalentConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import init_talent_item, get_attr_desc_text
from logic.gutils.item_utils import get_money_icon, get_lobby_item_name
from logic.gutils.template_utils import splice_price
from logic.gcommon.const import SHOP_PAYMENT_PVE_COIN, SHOP_PAYMENT_ITEM_PVE_COIN

class PVETalentConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/open_pve_talent_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'img_window_bg.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_click_close_btn(self, *args):
        self.close()

    def on_init_panel(self, talent_id, *args, **kwargs):
        self.init_parameters(talent_id)
        self.process_events(True)
        self.init_ui()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_pve_talent_event': self.close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self, talent_id):
        self._talent_id = talent_id

    def on_finalize_panel(self):
        self.process_events(False)
        self._talent_id = None
        return

    def init_ui(self):
        self._init_talent_item()
        self._init_buy_btn()
        self._init_price_view()
        self._init_upgrade_panel()

    def _init_talent_item(self):
        temp_item = self.panel.img_window_bg.temp_item
        temp_item.SetTouchEnabledRecursion(False)
        init_talent_item(temp_item, self._talent_id)

    def _init_buy_btn(self):

        @self.panel.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.close()

        @self.panel.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            have_item_counts = global_data.player.get_item_num_by_no(SHOP_PAYMENT_PVE_COIN)
            cost_price = global_data.player.get_talent_cost(self._talent_id)
            if have_item_counts >= cost_price:
                global_data.player.up_talent_level(self._talent_id)
            else:
                from logic.comsys.mall_ui.LotteryTicketBuyConfirmUI import LotteryTicketBuyConfirmUI
                LotteryTicketBuyConfirmUI(goods_id=cost_item)

    def _init_price_view(self):
        price_item = self.panel.temp_price
        cost_item = SHOP_PAYMENT_ITEM_PVE_COIN
        cost_price = global_data.player.get_talent_cost(self._talent_id)
        icon_path = get_money_icon(cost_item)
        price_item.img_price.SetDisplayFrameByPath('', icon_path)
        have_item_counts = global_data.player.get_item_num_by_no(SHOP_PAYMENT_PVE_COIN)
        lab_price = price_item.lab_price
        lab_price.setString(str(cost_price))
        lab_price.lab_price_before.setVisible(False)
        if have_item_counts >= cost_price:
            lab_price.SetColor('#BC')
        else:
            lab_price.SetColor('#SR')

    def _init_upgrade_panel(self):
        talent_conf = confmgr.get('talent_data', self._talent_id)
        talend_effect_conf = confmgr.get('talent_effect_data', str(self._talent_id))
        talent_level = global_data.player.get_talent_level_by_id(self._talent_id)
        self.panel.lab_title2.setString(get_text_by_id(378).format(get_text_by_id(talent_conf['name_id'])))
        self.panel.lab_tips.setString(get_text_by_id(379).format(get_lobby_item_name(SHOP_PAYMENT_PVE_COIN)))
        show_level = talent_level if talent_level > 0 else 1
        talent_text = get_attr_desc_text(talend_effect_conf.get('desc_id'), talend_effect_conf.get('desc_params'), show_level)
        self.panel.img_window_bg.lab_content.SetString(talent_text)