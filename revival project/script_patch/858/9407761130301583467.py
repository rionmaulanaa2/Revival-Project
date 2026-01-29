# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/WeaponDetailsUI.py
from __future__ import absolute_import
from logic.gutils import items_book_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from common.uisys.basepanel import BasePanel
from logic.client.const import items_book_const
from logic.gcommon.item import item_const
from common.cfg import confmgr
from logic.gutils import template_utils
from common.const import uiconst

class WeaponDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'catalogue/weapon_details'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def set_detail_item_no(self, item_no):
        self.refresh_ui(item_no)

    def refresh_ui(self, item_no):
        weapon_config = items_book_utils.get_items_conf(items_book_const.WEAPON_ID)
        weapon_list = weapon_config.get(item_no, {}).get('battle_item_no', [])
        new_weapon_list = []
        for weapon_id in weapon_list:
            item_conf = confmgr.get('item', str(weapon_id))
            item_level = item_conf['iQuality']
            if item_level == item_const.LEGEND_COLORFUL or item_level == item_const.TDM_DARK:
                continue
            new_weapon_list.append(weapon_id)

        list_class = self.panel.list_weapon_details
        count = len(new_weapon_list)
        list_class.SetInitCount(count)
        width_dict = {3: 800,2: 540,
           1: 280
           }
        count = len(new_weapon_list)
        width = width_dict.get(count, 800)
        old_size = self.panel.nd_game_describe.getContentSize()
        self.panel.nd_game_describe.SetContentSize(width, old_size.height)
        self.panel.nd_game_describe.ChildResizeAndPosition()
        list_class.RefreshItemPos()
        if count == 1:
            self.panel.img_partition_line_left.setVisible(False)
            self.panel.img_partition_line_right.setVisible(False)
        elif count == 2:
            self.panel.img_partition_line_left.setVisible(True)
            self.panel.img_partition_line_right.setVisible(False)
        else:
            self.panel.img_partition_line_left.setVisible(True)
            self.panel.img_partition_line_right.setVisible(True)
        all_items = list_class.GetAllItem()
        for index, item_widget in enumerate(all_items):
            weapon_id = new_weapon_list[index]
            item_conf = confmgr.get('item', str(weapon_id))
            item_level = item_conf['iQuality']
            pic = template_utils.get_equipment_quality_pic(item_level)
            color = template_utils.get_equipment_quality_color(item_level)
            item_widget.img_stage.SetDisplayFrameByPath('', pic)
            item_widget.lab_stage.SetString('')
            self.init_item_detail(weapon_id, item_widget.list_data, color)

    def init_item_detail(self, item_no, list_widget, color):
        attr_conf = confmgr.get('gun_attachment_attr', str(item_no))
        if not attr_conf:
            return
        attrs = [
         'iPower', 'iStability', 'iAccuracy', 'iFireRating', 'iRange']
        attr_txt_ids = [80391, 80392, 80218, 80324, 80323]
        list_widget.SetInitCount(len(attrs))
        all_items = list_widget.GetAllItem()
        for index, item_widget in enumerate(all_items):
            attr = attrs[index]
            percent = attr_conf[attr]
            item_widget.power.progress.SetPercent(percent, 0.5)
            item_widget.power.progress.SetColor(color)
            item_widget.power.num.SetString(str(percent))
            item_widget.power.power.SetString(get_text_by_id(attr_txt_ids[index]))