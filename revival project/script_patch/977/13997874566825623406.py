# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/LobbyItemInscrDescUI.py
from __future__ import absolute_import
import copy
from common.uisys.basepanel import BasePanel
from cocosui import cc, ccui, ccs
import common.const.uiconst
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name, get_lobby_item_desc, get_lobby_item_type_name_by_type
from common.cfg import confmgr
from logic.gutils import inscription_utils
from logic.gutils import mall_utils
from logic.gcommon.cdata.mecha_component_data import get_mecha_component_price
from logic.gcommon.cdata.mecha_component_conf import get_give_com_level

class LobbyItemInscrDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/inscription/i_item_inscription'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    BORDER_INDENT = 24
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'nd_bg.OnBegin': 'hide_item_desc_info'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        pass

    def show_item_desc_info(self, item_no, wpos, directly_world_pos=None, extra_info=None, item_num=0):
        self.panel.PlayAnimation('appear')
        self._com_item_no = item_no
        from logic.client.const import mall_const
        self.panel.lab_item_name.SetString(get_lobby_item_name(item_no))
        self.panel.lab_sort.SetString(inscription_utils.get_com_sort_name(item_no))
        if extra_info is None:
            extra_info = {}
        has_own = global_data.player.has_owned_component(item_no)
        hide_button = extra_info.get('hide_button')
        if hide_button or has_own:
            self.panel.temp_btn_buy.setVisible(False)
            self.panel.img_bar.SetContentSize('100%20', '100%-30')
        else:
            self.panel.img_bar.InitConfContentSize()
            self.panel.temp_btn_buy.setVisible(True)
            unlock_lv = get_give_com_level(item_no)
            is_lock = unlock_lv > global_data.player.get_lv() if unlock_lv is not None else True
            self.panel.temp_cost.setVisible(not is_lock)
            self.panel.lab_lock.setVisible(is_lock)
            self.panel.temp_btn_buy.btn_common.SetShowEnable(not is_lock)
            self.panel.lab_lock.SetString(get_text_by_id(81872, {'lv': unlock_lv}))
            from logic.gutils.template_utils import splice_price, init_price_template, get_money_rich_text_ex
            from logic.gutils import mall_utils
            price_info = inscription_utils.get_component_buy_price(item_no, 1)
            init_price_template(price_info, self.panel.temp_cost, mall_const.DARK_PRICE_COLOR)

            @self.panel.temp_btn_buy.btn_common.callback()
            def OnClick(btn, touch):
                if unlock_lv > global_data.player.get_lv():
                    global_data.game_mgr.show_tip(get_text_by_id(81872, {'lv': unlock_lv}))
                    return
                if global_data.player.has_owned_component(item_no):
                    return
                if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                    global_data.game_mgr.show_tip(get_text_by_id(81873))
                    return
                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                price_info_list = [
                 price_info]
                dlg = SecondConfirmDlg2()

                def on_cancel():
                    dlg.close()

                def on_confirm():
                    dlg.close()
                    if mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                        global_data.player.buy_mecha_component(item_no)

                price_text = get_money_rich_text_ex(price_info_list)
                dlg.confirm(content=get_text_by_id(81983, {'cost': price_text,'item_name': get_lobby_item_name(item_no)}), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)
                self.close()

        inscr_buff_list = inscription_utils.get_component_id_buff_list(item_no)
        if len(inscr_buff_list) <= 1:
            self.panel.nd_desc_2.setVisible(False)
        else:
            self.panel.nd_desc_2.setVisible(True)
        for idx, component_buff_info in enumerate(inscr_buff_list):
            _component_id, inscr_buff_id, buff_value = component_buff_info
            text_id = confmgr.get('inscription_data', str(inscr_buff_id), 'descTid', default='')
            detailTid = confmgr.get('inscription_data', str(inscr_buff_id), 'descDetailTid', default='')
            ui_item = getattr(self.panel, 'nd_desc_%d' % (idx + 1))
            if ui_item:
                ui_item.temp_stat.GetItem(0).lab_content.SetString(text_id)
                ui_item.temp_stat.GetItem(0).lab_num.SetString(inscription_utils.format_buff_value(buff_value))
                ui_item.lab_desc.SetString(detailTid)

        temp_ui_item = self.panel.temp_item.GetItem(0)
        inscription_utils.init_component_slot_temp(temp_ui_item, item_no)
        if not directly_world_pos:
            self.panel.setAnchorPoint(cc.Vec2(1.06, -0.1))
            pos = self.panel.GetParent().convertToNodeSpace(wpos)
        else:
            pos = self.panel.GetParent().convertToNodeSpace(directly_world_pos)
            cur_screen_size = global_data.ui_mgr.design_screen_size
            center_x, center_y = cur_screen_size.width / 2, cur_screen_size.height / 2
            if pos.x < center_x:
                anchor_x = -0.06
            else:
                anchor_x = 1.06
            if pos.y < center_y:
                anchor_y = 0.05
            else:
                anchor_y = 0.95
            self.panel.setAnchorPoint(cc.Vec2(anchor_x, anchor_y))
        self.panel.setPosition(pos.x, pos.y)
        self.show()
        self.panel.setOpacity(0)
        return

    def hide_item_desc_info(self, *args):
        self.hide()

    def ui_vkb_custom_func(self):
        self.hide_item_desc_info()