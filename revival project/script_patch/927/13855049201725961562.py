# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVESellUI.py
from __future__ import absolute_import
import six
from logic.gutils.template_utils import splice_price, FrameLoaderTemplate
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text, get_bless_can_sell, set_bless_elem_type_icon, get_bless_elem_res, get_bless_elem_desc, get_bless_elem_attr_conf, DEFAULT_BLESS_PANEL
from mobile.common.EntityManager import EntityManager
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const.pve_const import BLESS_SELL_PRICE
from common.cfg import confmgr
import six_ex

class PVESellUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/shop/pve_sell_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_sell.OnClick': 'on_click_sell'
       }

    def on_init_panel(self, shop_eid, *args):
        super(PVESellUI, self).on_init_panel(*args)
        self.init_params(shop_eid)
        self.init_widget()

    def init_params(self, shop_eid):
        self._shop_eid = shop_eid
        self._bless_conf = confmgr.get('bless_data', default=None)
        self._bless_data = None
        self._cur_select_id = -1
        self._is_showing_display_item = False
        self._frame_loader_template = None
        return

    def init_widget(self):
        if not global_data.player or not global_data.player.logic:
            return
        shop = EntityManager.getentity(self._shop_eid)
        if not shop:
            return
        self._init_bless_list()
        self._init_info_widget()
        self.panel.lab_money.SetString(str(global_data.player.logic.ev_g_crystal_stone()))
        self.panel.btn_sell.SetEnableTouch(True)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_update_crystal_num': self._update_crystal,
           'pve_remove_bless_event': self.on_pve_remove_bless_event,
           'pve_update_bless_event': self.on_pve_update_bless_event
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def destroy_frame_loader_template(self):
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        return

    def on_finalize_panel(self):
        self.process_events(False)
        self.destroy_frame_loader_template()
        super(PVESellUI, self).on_finalize_panel()

    def _init_info_widget(self):
        self._cur_select_id = -1
        self.panel.nd_empry.setVisible(len(self._bless_data) == 0)
        self.panel.btn_sell.setVisible(False)
        self.panel.lab_price_sell.setVisible(False)
        self.panel.temp_energy.setVisible(False)
        self._update_price_widget()
        self.panel.lab_got.SetString(get_text_by_id(530).format(len(self._bless_data)))
        self.panel.btn_sell.SetEnable(False)
        self._is_showing_display_item = False

    def _init_completed(self):
        self.process_events(True)

    def _init_bless_list(self):
        self._bless_data = [ bless_id for bless_id in six_ex.keys(global_data.player.logic.ev_g_choosed_blesses()) ]
        self._bless_data.sort()
        self.destroy_frame_loader_template()
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_item, len(self._bless_data), self._init_bless_item, self._init_completed)

    def _init_bless_item(self, item, cur_index):
        bless_data = self._bless_data
        bless_id = self._bless_data[cur_index]
        bless_conf = self._bless_conf[str(bless_id)]
        set_bless_elem_type_icon(item.icon_type, bless_id)
        bar = item.bar
        bar.img_item.SetDisplayFrameByPath('', bless_conf['icon'])
        bar.lab_name.SetString(get_text_by_id(bless_conf['name_id']))
        btn_choose = bar.btn_choose
        btn_choose.EnableCustomState(True)

        @btn_choose.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player or not global_data.player.logic:
                return
            if not global_data.cam_lplayer:
                return
            bless_level = global_data.cam_lplayer.ev_g_bless_level(int(bless_id))
            self._switch_select_item(bless_id)
            self._update_price_widget(bless_id, bless_level)
            self.panel.btn_sell.setVisible(True)
            self.panel.lab_price_sell.setVisible(True)
            self.panel.temp_energy.setVisible(True)
            self._init_bless_display_item(bless_conf, bless_level)
            self._is_showing_display_item = True

        if cur_index == 0:
            btn_choose.OnClick(None)
        return

    def _switch_select_item(self, bless_id):
        bless_data = self._bless_data
        index = self._bless_data.index(bless_id)
        if index == self._cur_select_id:
            return
        item = self.panel.list_item.GetItem(self._cur_select_id)
        item.btn_choose.SetSelect(False)
        cur_item = self.panel.list_item.GetItem(index)
        cur_item.btn_choose.SetSelect(True)
        self._cur_select_id = index

    def _update_price_widget(self, bless_id=None, bless_level=None):
        if bless_id and bless_level and get_bless_can_sell(bless_id):
            self.panel.lab_price_sell.setString(str(BLESS_SELL_PRICE * bless_level))
            self.panel.btn_sell.SetShowEnable(True)
        else:
            self.panel.lab_price_sell.setString('0')
            self.panel.btn_sell.SetShowEnable(False)

    def _init_bless_display_item(self, bless_conf, bless_level):
        temp_bless = self.panel.temp_energy
        temp_bless.lab_name.SetString(bless_conf['name_id'])
        temp_bless.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
        desc_id = bless_conf['desc_id']
        attr_conf = bless_conf.get('attr_text_conf', [])
        temp_bless.lab_introduce.SetString(get_effect_desc_text(desc_id, attr_conf, bless_level))
        list_dot = temp_bless.list_dot
        max_level = bless_conf.get('max_level', 1)
        if max_level == 1:
            list_dot.setVisible(False)
        else:
            list_dot.setVisible(True)
            list_dot.DeleteAllSubItem()
            list_dot.SetInitCount(max_level)
            for i, btn in enumerate(list_dot.GetAllItem()):
                if i < bless_level:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(True)
                else:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(False)

        elem_id = bless_conf.get('elem_id', None)
        if elem_id:
            elem_desc_id = get_bless_elem_desc(elem_id)
            elem_attr_conf = get_bless_elem_attr_conf(elem_id)
            elem_icon, elem_pnl_icon = get_bless_elem_res(elem_id, ['icon', 'panel'])
            bar_describe = temp_bless.bar_describe
            bar_describe.setVisible(True)
            bar_describe.lab_describe.SetString(get_effect_desc_text(elem_desc_id, elem_attr_conf, 1))
            temp_bless.bar.SetFrames('', [elem_pnl_icon, elem_pnl_icon, elem_pnl_icon])
            temp_bless.icon_type.setVisible(True)
            temp_bless.icon_type.SetDisplayFrameByPath('', elem_icon)
        else:
            temp_bless.bar_describe.setVisible(False)
            pic = DEFAULT_BLESS_PANEL
            temp_bless.bar.SetFrames('', [pic, pic, pic])
            temp_bless.icon_type.setVisible(False)
        return

    def on_pve_remove_bless_event(self, remove_bless_id):
        bless_data = self._bless_data
        if remove_bless_id not in self._bless_data:
            return
        index = self._bless_data.index(remove_bless_id)
        self._bless_data.remove(remove_bless_id)
        self.panel.list_item.DeleteItemIndex(index, True)
        self._init_info_widget()
        self._select_first_item()

    def on_pve_update_bless_event(self, update_bless_id):
        if not global_data.cam_lplayer:
            return
        if update_bless_id not in self._bless_data:
            index = len(self._bless_data)
            item = self.panel.list_item.AddTemplateItem()
            self._bless_data.append(update_bless_id)
        else:
            index = self._bless_data.index(update_bless_id)
            item = self.panel.list_item.GetItem(index)
            if self._is_showing_display_item:
                bless_conf = self._bless_conf[str(update_bless_id)]
                bless_level = global_data.cam_lplayer.ev_g_bless_level(int(update_bless_id))
                self._init_bless_display_item(bless_conf, bless_level)
                self._update_price_widget(update_bless_id, bless_level)
        self.panel.nd_empry.setVisible(len(self._bless_data) == 0)
        self.panel.lab_got.SetString(get_text_by_id(530).format(len(self._bless_data)))
        self._init_bless_item(item, index)
        self._select_first_item()

    def _select_first_item(self, *args):
        first_item = self.panel.list_item.GetItem(0)
        if first_item:
            first_item.btn_choose.OnClick(None)
        return

    def _update_crystal(self, *args):
        self.panel.lab_money.SetString(str(global_data.player.logic.ev_g_crystal_stone()))

    def on_click_sell(self, *args):
        if self._cur_select_id == -1:
            return
        bless_id = self._bless_data[self._cur_select_id]
        if not get_bless_can_sell(bless_id):
            bless_conf = self._bless_conf[str(bless_id)]
            global_data.game_mgr.show_tip(get_text_by_id(522).format(bless=get_text_by_id(bless_conf['name_id'])))
            return
        shop = EntityManager.getentity(self._shop_eid)
        if not shop:
            return
        shop.logic.send_event('E_CALL_SYNC_METHOD', 'sell_pve_bless', (global_data.player.logic.id, bless_id), True, True)

    def on_close(self, *args):
        self.close()