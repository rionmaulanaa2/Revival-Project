# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEEndInfoUI.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.gutils.item_utils import get_mecha_name_by_id, get_lobby_item_name
from logic.gutils.template_utils import set_ui_show_picture, FrameLoaderTemplate
from logic.gutils.pve_utils import get_bless_elem_res, DEFAULT_BLESS_BAR
from logic.comsys.battle.pve.PVEItemWidget import PVEBlessWidget, PVEItemWidget
from logic.gcommon.common_const.pve_const import EMPTY_WIDGET_PATH
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
import six_ex
LIST_TYPE_ENERGY = 0
LIST_TYPE_SHOP = 1

class PVEEndInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/info/pve_info_shop_and_energy'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, data_list, *args, **kwargs):
        super(PVEEndInfoUI, self).on_init_panel(*args, **kwargs)
        self.init_params(data_list)
        self.init_ui()
        self.init_ui_event()

    def init_params(self, data_list):
        self._data_list = data_list
        self._screen_capture_helper = None
        self._frame_loader_template = None
        self._bless_widget = None
        self._item_widget = None
        return

    def init_ui(self):
        self._init_info_widget()
        self._init_mecha_widget()
        self._init_energy_widget()

    def init_ui_event(self):

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.close()

        @self.panel.btn_next.unique_callback()
        def OnClick(btn, touch):
            self.close()

        def share_cb(*args):
            self.panel.btn_next.setVisible(True)
            self.panel.btn_share.setVisible(True)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.panel.btn_next.setVisible(False)
            self.panel.btn_share.setVisible(False)
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._screen_capture_helper.take_screen_shot([
             self.__class__.__name__], self.panel, custom_cb=share_cb, head_nd_name='nd_player_info_1')

        @self.panel.list_energy.unique_callback()
        def OnScrolling(sender):
            self._update_slider(LIST_TYPE_ENERGY)

        @self.panel.list_mod.unique_callback()
        def OnScrolling(sender):
            self._update_slider(LIST_TYPE_SHOP)

    def _update_slider(self, list_type):
        percent = self.get_slider_info(list_type)
        max_percent = 84.0
        min_percent = 19.0
        percent = min_percent + (max_percent - min_percent) * (percent / 100.0)
        if percent < min_percent:
            percent = min_percent
        if percent > max_percent:
            percent = max_percent
        img_slider = self.panel.bar_energy.nd_slider.img_slider if list_type == LIST_TYPE_ENERGY else self.panel.bar_mod.nd_slider.img_slider
        img_slider.SetPosition('50%', '{}%'.format(100.0 - percent))

    def get_slider_info(self, list_type):
        import common.utilities
        percent = 0.0
        list_item = self.panel.list_energy if list_type == LIST_TYPE_ENERGY else self.panel.list_mod
        in_height = list_item.GetInnerContentSize().height
        out_height = list_item.getContentSize().height
        pos_y = list_item.getInnerContainer().getPositionY()
        if out_height - in_height == 0.0:
            percent = 0.0
        else:
            percent = common.utilities.smoothstep(out_height - in_height, 0.0, pos_y) * 100.0
        return percent

    def _init_img_slider(self):
        self.panel.bar_energy.nd_slider.img_slider.SetPosition('50%', '81%')
        self.panel.bar_mod.nd_slider.img_slider.SetPosition('50%', '81%')

    def _init_info_widget(self):
        empty_widget = global_data.uisystem.load_template_create(EMPTY_WIDGET_PATH, self.panel)
        empty_widget.nd_empty.set_sound_enable(False)

        @empty_widget.nd_empty.unique_callback()
        def OnClick(btn, touch):
            self._bless_widget and self._bless_widget.setVisible(False)
            self._item_widget and self._item_widget.setVisible(False)

        self._bless_widget = PVEBlessWidget(self.panel, False)
        self._bless_widget.setVisible(False)
        self._item_widget = PVEItemWidget(self.panel)
        self._item_widget.setVisible(False)

    def _init_mecha_widget(self):
        mecha_id = self._data_list.get('mecha_id')
        self.panel.lab_name.setString(get_mecha_name_by_id(mecha_id))
        skin_id = self._data_list.get('skin_id')
        set_ui_show_picture(skin_id, mecha_nd=self.panel.temp_pic)

    def _init_energy_widget(self):
        self._energy_list = self._data_list.get('energy_list', [])
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_energy, len(self._energy_list), self._init_energy_item, self._init_shop_widget)

    def _init_energy_item(self, item, cur_index):
        energy_id, energy_level, is_removed_energy = self._energy_list[cur_index]
        bless_conf = confmgr.get('bless_data', str(energy_id), default=None)
        if not bless_conf:
            self.panel.list_energy.RecycleItem(item)
            return
        else:
            item.lab_name.setString(get_text_by_id(bless_conf['name_id']))
            btn_energy = item.btn_energy
            img_item = btn_energy.img_item
            img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
            if is_removed_energy:
                img_item.SetOpacity(100)
            max_level = bless_conf.get('max_level', 1)
            energy_level = min(energy_level, max_level)
            if max_level == 1:
                item.lab_level.setVisible(False)
                item.icon.setVisible(True)
            else:
                item.icon.setVisible(False)
                item.lab_level.setVisible(True)
                item.lab_level.SetString(str(energy_level))
            elem_id = bless_conf.get('elem_id', None)
            if elem_id:
                elem_icon, elem_pnl = get_bless_elem_res(elem_id, ['icon', 'bar'])
                item.icon.SetDisplayFrameByPath('', elem_icon)
                item.bar.SetDisplayFrameByPath('', elem_pnl)
            else:
                item.bar.SetDisplayFrameByPath('', DEFAULT_BLESS_BAR)

            @btn_energy.unique_callback()
            def OnClick(btn, touch):
                if not global_data.player:
                    return
                if not self._bless_widget:
                    return
                if self._item_widget.isVisible():
                    self._item_widget.setVisible(False)
                pve_mecha_base_info = self._data_list.get('pve_mecha_base_info', {})
                self._bless_widget.update_widget(energy_id, energy_level, pve_mecha_base_info)

            return

    def _init_shop_widget(self):
        shop_dict = self._data_list.get('buy_item_cnt', {})
        self._shop_list = six_ex.keys(shop_dict) if isinstance(shop_dict, dict) else shop_dict
        self._shop_list.sort()
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_mod, len(self._shop_list), self._init_shop_item, self._init_img_slider)

    def _init_shop_item(self, item, cur_index):
        item_id = self._shop_list[cur_index]
        item_conf = confmgr.get('pve_shop_data', str(item_id), default=None)
        if not item_conf:
            self.panel.list_mod.RecycleItem(item)
            return
        else:
            item.lab_name.SetString(get_text_by_id(item_conf['name_id']))
            item.img_item.SetDisplayFrameByPath('', item_conf['icon'])
            item.bar_tag.setVisible(bool(item_conf.get('repeat_refresh', 0)))

            @item.btn_item.unique_callback()
            def OnClick(btn, touch):
                if not global_data.player:
                    return
                if not self._item_widget:
                    return
                if self._bless_widget.isVisible():
                    self._bless_widget.setVisible(False)
                self._item_widget.update_widget(item_conf)

            return

    def on_finalize_panel(self):
        self._data_list = None
        self._screen_capture_helper = None
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        if self._bless_widget:
            self._bless_widget.destroy()
            self._bless_widget = None
        if self._item_widget:
            self._item_widget.destroy()
            self._item_widget = None
        super(PVEEndInfoUI, self).on_finalize_panel()
        return