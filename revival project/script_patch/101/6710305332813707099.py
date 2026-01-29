# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CollectInfoSubWidget.py
from __future__ import absolute_import
from logic.gcommon.item import item_const
from common.uisys.BaseUIWidget import BaseUIWidget

class CollectInfoSubWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel):
        super(CollectInfoSubWidget, self).__init__(parent_ui, panel)

    def show(self):
        self.panel.setVisible(True)

    def hide(self):
        self.panel.setVisible(False)

    def is_visible(self):
        if self.panel.IsVisible():
            return True
        return False

    def refresh(self, player_inf):
        skin_nodes = [
         self.panel.nd_mech, self.panel.nd_player, self.panel.nd_others]
        from logic.client.const.role_ui_const import collect_interact_type, collect_skin_item_types
        item_types = collect_skin_item_types
        item_stat = player_inf.get('item_stat', {})
        for idx, skin_node in enumerate(skin_nodes):
            skin_type, s_skin_type = item_types[idx]
            skin_num = item_stat.get(str(skin_type), 0)
            s_skin_num = item_stat.get(str(s_skin_type), 0)
            skin_node.lab_num.setString(str(skin_num))
            skin_node.lab_s_num.setString(str(s_skin_num))

        interact_type = collect_interact_type
        interact_img_name = [
         'graffiti', 'emoji', 'action', 'avatar', 'avatar_frame', 'chat_frame']
        interact_name = [
         81233, 81234, 81235, 81299, 80780, 81159]
        self.panel.list_collect.SetInitCount(len(interact_type))
        for idx, item in enumerate(self.panel.list_collect.GetAllItem()):
            num = item_stat.get(str(interact_type[idx]), 0)
            if interact_type[idx] == item_const.INV_STAT_HEAD_PHOTO and num > 0:
                num -= 1
            path = 'gui/ui_res_2/role/icon_collect_%s.png' % (interact_img_name[idx],)
            item.lab_num.setString(str(num))
            item.name.SetString(interact_name[idx])
            item.img_sort.SetDisplayFrameByPath('', path)