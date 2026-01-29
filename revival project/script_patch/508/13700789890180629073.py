# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/PersonRoleInfoShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class PersonRoleInfoShareCreator(ShareTemplateBase):
    KIND = 'PERSON_ROLE_SHARE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(PersonRoleInfoShareCreator, self).create(parent)

    def get_ui_bg_sprite(self):
        return self.panel.img_bg

    def update_ui_bg_sprite(self):
        from logic.gutils.share_utils import get_share_size
        sz = get_share_size()
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        self.panel.setScale(scale)
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()
        self.panel.img_bg.SetPosition('50%', '50%')
        bg_scale = global_data.ui_mgr.design_screen_size.width / self.panel.img_bg.getContentSize().width
        self.panel.img_bg.setScale(bg_scale)

    @async_disable_wrapper
    def set_watermark(self, need):
        if not need:
            self.panel.img_logo.setVisible(False)
            self.panel.img_qr_code.setVisible(False)
            if self.panel.img_qr_bg:
                self.panel.img_qr_bg.setVisible(False)
        else:
            self.panel.img_logo.setVisible(True)
            from logic.gutils.share_utils import is_share_qr_code_enable
            self.panel.img_qr_code.setVisible(is_share_qr_code_enable())
            if self.panel.img_qr_bg:
                self.panel.img_qr_bg.setVisible(is_share_qr_code_enable())

    def set_white_lab_color_and_outline(self):
        self.panel.lab_name.SetColor('#SW')
        self.panel.lab_id.SetColor('#SW')
        self.panel.lab_name.EnableShadow('#SK', 255, {'width': 2,'height': -2})

    @async_disable_wrapper
    def add_battle_record(self, item_no):
        from logic.gutils.share_utils import set_mecha_share_battle_stat
        set_mecha_share_battle_stat(self.base_node.list_info, item_no)

    def set_show_record(self, is_show):
        self.base_node.list_info.setVisible(is_show)

    @async_disable_wrapper
    def show_share_detail(self, item_no, is_get=True):
        from logic.gutils.share_utils import show_share_details
        show_share_details(self.base_node, item_no, is_get)

    @async_disable_wrapper
    def add_ex_privilege_record(self, temp_skin_id):
        from logic.gutils.mecha_utils import set_mecha_honour_view
        set_mecha_honour_view(self.panel.temp_honour, temp_skin_id)

    def set_show_ex_privilege(self, is_show):
        nd_info_mecha = self.panel.nd_info_mecha
        nd_info_mecha.setVisible(is_show)
        nd_info_mecha.nd_content_mecha.setVisible(False)
        nd_info_mecha.nd_honour.setVisible(is_show)

    def test(self):
        from logic.gutils import task_utils, item_utils, jump_to_ui_utils
        jump_to_ui_utils.jump_to_share()