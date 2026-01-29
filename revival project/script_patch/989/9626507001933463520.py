# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ItemInfoShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from common.cfg import confmgr
from logic.gutils.share_utils import get_share_bg_path

class ItemInfoShareCreator(ShareTemplateBase):
    KIND = 'ITEM_SHARE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(ItemInfoShareCreator, self).create(parent, tmpl)

    def update_share_item_pic(self, item_no):
        base_node = self.base_node
        _sprite = get_share_bg_path(item_no)
        if base_node and _sprite:
            base_node.img_bg.SetDisplayFrameByPath('', _sprite, force_sync=True)

    def update_share_item_num(self, item_no, num_text):
        if not self.panel.lab_num:
            return
        self.panel.lab_num.SetString(num_text)

    @async_disable_wrapper
    def add_battle_record(self, item_no):
        from logic.gutils.share_utils import set_mecha_share_battle_stat
        set_mecha_share_battle_stat(self.panel.pnl_bg.list_info, item_no)

    def set_show_record(self, is_show):
        self.panel.pnl_bg.list_info.setVisible(is_show)

    @async_disable_wrapper
    def show_share_detail(self, item_no, is_get=True):
        from logic.gutils.share_utils import show_share_details
        show_share_details(self.panel.pnl_bg, item_no, is_get)

    def get_ui_bg_sprite(self):
        return self.base_node.img_bg