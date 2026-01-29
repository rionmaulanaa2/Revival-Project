# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/MVPShareCreator.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class MVPShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_MVP'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(MVPShareCreator, self).create(parent)

    def destroy(self):
        super(MVPShareCreator, self).destroy()

    def get_ui_bg_sprite(self):
        return self.panel.img_bg_cover

    def update_ui_bg_sprite(self):
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()

    def set_mvp_info(self, mvp_info, is_winner_mvp):
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        from logic.gutils import dress_utils
        mecha_fashion = mvp_info.get('mecha_fashion', {})
        mecha_fashion_id = mecha_fashion.get(FASHION_POS_SUIT, {})
        if not mecha_fashion_id:
            item_no = global_data.player.get_lobby_selected_mecha_item_id()
            clothing_id = global_data.player.get_mecha_fashion(item_no)
            if clothing_id:
                item_no = clothing_id
            else:
                item_no = 201800100
            mecha_fashion_id = item_no
        mecha_pic_path = 'gui/ui_res_2/battle_mech_call_pic/{}.png'.format(mecha_fashion_id)
        fashion_id = mvp_info.get('fashion', {}).get(FASHION_POS_SUIT, 201001100)
        role_pic_path = 'gui/ui_res_2/pic/{}.png'.format(fashion_id)
        self.panel.img_mecha.SetDisplayFrameByPath('', mecha_pic_path)
        self.panel.img_driver.SetDisplayFrameByPath('', role_pic_path)
        self.panel.lab_player_name.setString(str(mvp_info.get('role_name', '')))
        from common.cfg import confmgr
        from logic.gutils import mecha_skin_utils
        from logic.gutils import item_utils
        item_no = mecha_fashion_id
        ui_display_conf = confmgr.get('ui_display_conf', self.__class__.__name__, 'Content', default={})
        is_ss = mecha_skin_utils.is_ss_level_skin(item_no)
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        mecha_id = dress_utils.mecha_lobby_id_2_battle_id(belong_no)
        node_ui_conf = ui_display_conf.get(str(item_no)) or ui_display_conf.get(str(mecha_id))
        self.set_node_by_ui_conf(self.panel.img_mecha, node_ui_conf, is_ss)
        if is_winner_mvp:
            self.panel.lab_mvp_form.SetString(860196)
        else:
            self.panel.lab_mvp_form.SetString(860197)

    def set_battle_score(self, battle_info_list):
        num = len(battle_info_list)
        self.panel.list_info.SetInitCount(num)
        for i in range(num):
            ui_item = self.panel.list_info.GetItem(i)
            if ui_item:
                ui_item.img_icon.SetDisplayFrameByPath('', battle_info_list[i][0])
                ui_item.lab_name.SetString(battle_info_list[i][1])
                ui_item.lab_num.SetString(battle_info_list[i][2])

    def set_node_by_ui_conf(self, nd_img, node_ui_conf, is_ss):
        if node_ui_conf:
            pos = is_ss or node_ui_conf.get('NodePos') if 1 else node_ui_conf.get('SSNodePos')
            if pos:
                nd_img.SetPosition(*pos)
            else:
                nd_img.ReConfPosition()
        else:
            nd_img.ReConfPosition()