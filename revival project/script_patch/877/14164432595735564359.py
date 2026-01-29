# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEShopMechaChooseWidget.py
from __future__ import absolute_import
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from .PVEMainUIWidgetUI.PVEMechaChooseWidget import PVEMechaChooseWidget
from logic.gcommon.common_const.pve_const import PVE_MECHA_NEW_CACHE
from common.cfg import confmgr
from logic.gutils.mecha_utils import get_mecha_lst
import six_ex

class PVEShopMechaChooseWidget(PVEMechaChooseWidget):

    def init_params(self):
        super(PVEShopMechaChooseWidget, self).init_params()
        _, _, self.intimacy_share_mecha_lst = get_mecha_lst()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_show_changed': self._update_pve_mecha_item_choose,
           'player_item_update_event': self._update_pve_mecha_item,
           'pay_order_succ_event': self._update_pve_mecha_item,
           'update_skin_share_state': self._update_pve_mecha_item,
           'on_pve_main_model_load_complete': self._on_pve_main_model_load_complete
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _init_mecha_item(self, mecha_item, cur_index):
        mecha_id = self._open_mecha_id_list[cur_index]
        mecha_id = int(mecha_id)
        self._mecha_id_2_item[mecha_id] = mecha_item
        btn_mecha = mecha_item.nd_select.nd_btn.btn_mecha
        btn_mecha.EnableCustomState(True)
        pve_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
        icon_path = 'gui/ui_res_2/item/mecha/%d.png' % pve_mecha_id
        nd_cut = btn_mecha.nd_cut
        nd_cut.img_mecha.SetDisplayFrameByPath('', icon_path)
        nd_cut.img_mecha_shadow.SetDisplayFrameByPath('', icon_path)
        is_intimacy_share = mecha_id in self.intimacy_share_mecha_lst
        btn_mecha.nd_share_tips.setVisible(is_intimacy_share)
        has_mecha = bool(global_data.player and global_data.player.get_item_by_no(pve_mecha_id)) or is_intimacy_share
        img_lock = btn_mecha.img_lock
        if not has_mecha:
            img_lock.setVisible(True)
            img_lock.lab_not_have.setVisible(True)
        else:
            img_lock.setVisible(False)
            img_lock.lab_not_have.setVisible(False)
        mecha_id = self._open_mecha_id_list[cur_index]
        mecha_id = int(mecha_id)
        btn_mecha = mecha_item.nd_select.nd_btn.btn_mecha
        cur_use_mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type() if global_data.player and global_data.player.logic else 8001
        if mecha_id == cur_use_mecha_id:
            btn_mecha.nd_tag_in_code.setVisible(True)
        else:
            btn_mecha.nd_tag_in_code.setVisible(False)
        pve_mecha_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_MECHA_NEW_CACHE, [])
        if mecha_id not in pve_mecha_cache and has_mecha:
            btn_mecha.img_new.setVisible(True)
        else:
            btn_mecha.img_new.setVisible(False)
        if pve_mecha_id == battle_id_to_mecha_lobby_id(cur_use_mecha_id):
            self._del_mecha_item_new(btn_mecha, pve_mecha_id)
            self._cur_select_item = btn_mecha
            btn_mecha.SetSelect(True)
            btn_mecha.img_frame_choose.setVisible(True)
        else:
            btn_mecha.SetSelect(False)
            btn_mecha.img_frame_choose.setVisible(False)
        self._init_img_mecha_position(nd_cut, mecha_id)

        @btn_mecha.callback()
        def OnClick(btn, touch, mecha_id=mecha_id):
            self._on_btn_mecha_clicked(btn, mecha_id)

    def _on_btn_mecha_clicked(self, btn, mecha_id):
        if self._cur_select_item == btn:
            return
        mecha_item_no = battle_id_to_mecha_lobby_id(int(mecha_id))
        is_intimacy_share = mecha_id in self.intimacy_share_mecha_lst
        has_mecha = bool(global_data.player and global_data.player.get_item_by_no(mecha_item_no)) or is_intimacy_share
        if not has_mecha:
            global_data.game_mgr.show_tip(get_text_by_id(19841))
            return
        self._del_mecha_item_new(btn, mecha_id)
        global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)

    def _update_pve_mecha_item(self, *args):
        for mecha_id, item in six_ex.items(self._mecha_id_2_item):
            if item and item.isValid():
                img_lock = item.nd_select.nd_btn.btn_mecha.img_lock
                nd_intimacy = item.nd_select.nd_btn.btn_mecha.nd_share_tips
                pve_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
                is_intimacy_share = mecha_id in self.intimacy_share_mecha_lst
                has_mecha = bool(global_data.player and global_data.player.get_item_by_no(pve_mecha_id)) or is_intimacy_share
                if not has_mecha:
                    img_lock.setVisible(True)
                    img_lock.lab_not_have.setVisible(True)
                else:
                    img_lock.setVisible(False)
                    img_lock.lab_not_have.setVisible(False)
                nd_intimacy and nd_intimacy.setVisible(is_intimacy_share)