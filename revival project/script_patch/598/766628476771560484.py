# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/PVEBagUI.py
from __future__ import absolute_import
from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE, ST_USE_ITEM, ST_SKATE_MOVE, ST_MECHA_DRIVER, ST_MECHA_PASSENGER, ST_SKATE
from logic.gutils import template_utils
from PVEBagBaseUI import PVEBagBaseUI
from logic.gutils import item_utils
from logic.gcommon import const
from BagHumanItemWidget import BagHumanItemMobileWidget
from BagPVEBlessWidget import BagPVEBlessWidget
from common.const.cocos_constant import ONE_MINUS_SRC_ALPHA, ONE
from common.cfg import confmgr
NOT_THROW_ITEM_STATE = [
 ST_SWIM, ST_PARACHUTE]
BAG_UI_TYPE_OTHERS = -1
BAG_UI_TYPE_GUN = 0
BAG_UI_TYPE_ITEM = 1
BAG_UI_TYPE_CLOTHING = 2
BAG_UI_TYPE_MODULE = 3
BAG_UI_SUB_TYPE_HUMAN_ITEM = 11
BAG_UI_SUB_TYPE_MECHA_ITEM = 12

class PVEBagUI(PVEBagBaseUI):
    PANEL_CONFIG_NAME = 'pve/open_pve_bag'

    def init_parameters(self):
        self.lplayer = None
        self._appearing = False
        self._other_ui_visible = True
        self.tips_ui_list = [
         self.panel.item_tips]
        self.cur_ui = None
        self.cur_ui_type = None
        self.cur_ui_sub_type = None
        self.cur_ui_item_data = None
        self.delete_widget = self.panel.delete_small
        return

    def appear(self):
        super(PVEBagUI, self).appear()
        self.hide_item_tips()
        self.remove_cur_select_state()
        self.cur_ui = None
        self.show()
        return

    def disappear(self):
        super(PVEBagUI, self).disappear()
        self.hide_item_tips()
        self.remove_cur_select_state()
        self.cur_ui = None
        self.hide()
        return

    def init_widgets(self):
        super(PVEBagUI, self).init_widgets()
        method_dict = {'item_double_click': self.on_item_double_click,
           'btn_use_click': self.on_item_use_click,
           'btn_discard_click': self.on_item_discrad_click,
           'item_click': self.on_item_click,
           'item_drag': self.on_item_drag,
           'item_end': self.on_item_end
           }
        self.human_item_widget = BagHumanItemMobileWidget(self.panel.bag_human, method_dict)
        self.pve_bless_widget = BagPVEBlessWidget(self.panel, self.on_bless_click)

    def hide_item_tips(self):
        for tip_ui in self.tips_ui_list:
            tip_ui.setVisible(False)

    def hide_item_detail(self):
        self.hide_item_tips()
        self.remove_cur_select_state()
        self.cur_ui = None
        return

    def on_item_click(self, layer, touch, item_data):
        if not item_data:
            return
        else:
            self.remove_cur_select_state()
            cur_item_ui = layer.GetParent()
            cur_item_ui.item_sel.setVisible(True)
            cur_item_ui.pnl_right.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/panel/pnl_item_choose.png')
            cur_item_ui.name.SetColor('#SK')
            cur_item_ui.details.SetColor('#SK')
            self.human_item_widget.process_extra_part(None, cur_item_ui)
            self.cur_ui = cur_item_ui
            self.cur_ui_type = BAG_UI_TYPE_ITEM
            self.cur_ui_sub_type = BAG_UI_SUB_TYPE_HUMAN_ITEM
            self.cur_ui_item_data = item_data
            self.show_item_tips(self.tips_ui_list[0], item_data)
            item_no = item_data.get('item_id') if item_data else 0
            if item_utils.is_health_item(item_no) or item_utils.is_food_item(item_no):
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18082))
                cur_item_ui.extra_part.btn_use.setVisible(True)
            elif item_utils.is_attachment(item_no) or item_utils.is_exoskeleton_attachment(item_no):
                cur_item_ui.extra_part.btn_use.setVisible(True)
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18125))
            else:
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18082))
                cur_item_ui.extra_part.btn_use.setVisible(True)
            self.human_item_widget.on_extra_part_btn_change(self.lplayer, self.cur_ui, self.cur_ui_item_data)
            return

    def on_item_click_mecha(self, layer, touch, item_data):
        if not item_data:
            return
        else:
            self.remove_cur_select_state()
            cur_item_ui = layer.GetParent()
            cur_item_ui.item_sel.setVisible(True)
            cur_item_ui.pnl_right.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/panel/pnl_item_choose.png')
            cur_item_ui.name.SetColor('#SK')
            cur_item_ui.details.SetColor('#SK')
            self.mecha_item_widget.process_extra_part(None, cur_item_ui)
            self.cur_ui = cur_item_ui
            self.cur_ui_type = BAG_UI_TYPE_ITEM
            self.cur_ui_sub_type = BAG_UI_SUB_TYPE_MECHA_ITEM
            self.cur_ui_item_data = item_data
            self.show_item_tips(self.tips_ui_list[0], item_data)
            item_no = item_data.get('item_id') if item_data else 0
            if item_utils.is_health_item(item_no) or item_utils.is_food_item(item_no):
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18082))
                cur_item_ui.extra_part.btn_use.setVisible(True)
            elif item_utils.is_attachment(item_no) or item_utils.is_exoskeleton_attachment(item_no):
                cur_item_ui.extra_part.btn_use.setVisible(True)
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18125))
            else:
                cur_item_ui.extra_part.btn_use.SetText(get_text_local_content(18082))
                cur_item_ui.extra_part.btn_use.setVisible(True)
            self.human_item_widget.on_extra_part_btn_change(self.lplayer, self.cur_ui, self.cur_ui_item_data)
            return

    def on_item_double_click(self, btn, last_pos, cur_pos, item_data):
        if not item_data:
            return
        self.use_bag_item(item_data)

    def on_item_use_click(self, layer, touch, item_data):
        if not item_data:
            return
        self.use_bag_item(item_data)

    def on_item_discrad_click(self, layer, touch, item_data):

        def callback(num, item_data=item_data):
            item_utils.throw_item(self.lplayer, const.BACKPACK_PART_OTHERS, item_data['entity_id'], num, None)
            return

        item_id = item_data.get('item_id', -1)
        item_name = item_utils.get_item_name(item_id)
        self.discard_item(callback, item_name, item_data.get('count', 1))

    def remove_cur_select_state(self):
        if self.cur_ui is None:
            return
        else:
            if self.cur_ui_type == BAG_UI_TYPE_GUN:
                choose = getattr(self.cur_ui, 'choose')
                if choose and choose.isValid():
                    choose.setVisible(False)
            elif self.cur_ui_type == BAG_UI_TYPE_ITEM:
                item_sel = getattr(self.cur_ui, 'item_sel')
                if item_sel and item_sel.isValid():
                    item_sel.setVisible(False)
                else:
                    return
                item_id = self.cur_ui_item_data.get('item_id')
                path = 'box_res' if item_utils.is_package_item(item_id) else 'item'
                item_conf = confmgr.get(path, str(item_id))
                pnl_right = getattr(self.cur_ui, 'pnl_right')
                if pnl_right and pnl_right.isValid():
                    pnl_right.SetDisplayFrameByPath('', template_utils.get_quality_pic_l(item_conf.get('iQuality')))
                else:
                    return
                name = getattr(self.cur_ui, 'name')
                if name and name.isValid():
                    self.cur_ui.name.SetColor('#SW')
                else:
                    return
                details = getattr(self.cur_ui, 'details')
                if details and details.isValid():
                    self.cur_ui.details.SetColor('#SW')
                else:
                    return
                img_line = getattr(self.cur_ui, 'img_line')
                if img_line and img_line.isValid():
                    self.cur_ui.img_line.SetColor('#SW')
                if self.cur_ui_sub_type == BAG_UI_SUB_TYPE_HUMAN_ITEM:
                    self.human_item_widget.process_extra_part(self.cur_ui, None)
                    self.human_item_widget.refresh_item_list_postion()
                elif self.cur_ui_sub_type == BAG_UI_SUB_TYPE_MECHA_ITEM:
                    self.mecha_item_widget.process_extra_part(self.cur_ui, None)
                    self.mecha_item_widget.refresh_item_list_postion()
            elif self.cur_ui_type == BAG_UI_TYPE_CLOTHING:
                img_select = getattr(self.cur_ui, 'img_select')
                if img_select and img_select.isValid():
                    img_select.setVisible(False)
            elif self.cur_ui_type == BAG_UI_TYPE_MODULE:
                module_bar = getattr(self.cur_ui, 'module_bar')
                icon_skill = getattr(self.cur_ui, 'icon_skill')
                if module_bar and module_bar.isValid() and icon_skill and icon_skill.isValid():
                    module_bar.SetBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
                    icon_skill.SetBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
            return

    def is_in_empty_area(self, wpos):
        return not self.panel.drag_region.IsPointIn(wpos)

    def is_in_item_area(self, wpos):
        return self.panel.bag_mech.IsPointIn(wpos) or self.panel.bag_human.IsPointIn(wpos)

    def discard_item(self, callback, item_name, max_count, wpos=None):
        if not self.lplayer:
            return
        if self.lplayer.ev_g_is_in_any_state(NOT_THROW_ITEM_STATE):
            global_data.emgr.battle_show_message_event.emit(get_text_local_content(18135))
            return
        if max_count <= 1:
            callback(max_count)
            return
        from logic.gutils.template_utils import init_common_discard
        init_common_discard(self.panel.discard, max_count, callback)

    def show_delete_widget_item(self, wpos):
        if self.panel.drag_region.IsPointIn(wpos):
            self.delete_widget.setVisible(False)
        else:
            self.delete_widget.setVisible(True)

    def show_delete_widget_gun(self, wpos):
        if self.panel.nd_human.IsPointIn(wpos):
            self.delete_widget.setVisible(False)
        else:
            self.delete_widget.setVisible(True)

    def show_delete_widget_module(self, wpos):
        if self.panel.nd_mech.IsPointIn(wpos):
            self.delete_widget.setVisible(False)
        else:
            self.delete_widget.setVisible(True)

    def show_delete_widget_clothes(self, wpos):
        if self.panel.nd_human.IsPointIn(wpos):
            self.delete_widget.setVisible(False)
        else:
            self.delete_widget.setVisible(True)

    def hide_delete_widget(self):
        self.delete_widget.setVisible(False)

    def _on_rogue_gift_click(self, gift_id):
        self.remove_cur_select_state()
        super(PVEBagUI, self)._on_rogue_gift_click(gift_id)

    def _on_item_data_changed(self, item_data):
        super(PVEBagUI, self)._on_item_data_changed(item_data)
        self.human_item_widget.on_extra_part_btn_change(self.lplayer, self.cur_ui, self.cur_ui_item_data)