# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMechaChooseWidget.py
from __future__ import absolute_import
from logic.gutils.pve_utils import get_pve_mecha_id_list
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.common_const.pve_const import PVE_MECHA_NEW_CACHE
from logic.gutils.template_utils import FrameLoaderTemplate
from functools import cmp_to_key
from common.cfg import confmgr
import six_ex

class PVEMechaChooseWidget(object):

    def __init__(self, parent, list_ui):
        self._parent = parent
        self._list_ui = list_ui
        self.init_params()
        self.init_ui()
        self.process_events(True)

    def init_params(self):
        self._frame_loader_template = None
        self._cur_select_mecha_id = None
        self._cur_select_item = None
        self._open_mecha_id_list = get_pve_mecha_id_list()
        self._mecha_id_2_item = {}
        self._can_click_mecha = True
        return

    def init_ui(self):

        def cmp_func(a, b):
            item_no_a = battle_id_to_mecha_lobby_id(int(a))
            item_no_b = battle_id_to_mecha_lobby_id(int(b))
            intimacy_share_a = bool(global_data.player and global_data.player.is_intimacy_share_mecha(item_no_a))
            intimacy_share_b = bool(global_data.player and global_data.player.is_intimacy_share_mecha(item_no_b))
            priority_a = bool(global_data.player and global_data.player.get_item_by_no(item_no_a)) or intimacy_share_a
            priority_b = bool(global_data.player and global_data.player.get_item_by_no(item_no_b)) or intimacy_share_b
            return six_ex.compare(priority_a, priority_b)

        self._open_mecha_id_list.sort(key=cmp_to_key(cmp_func), reverse=True)
        self._frame_loader_template = FrameLoaderTemplate(self._list_ui, len(self._open_mecha_id_list), self._init_mecha_item)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_changed': self._update_pve_select_mecha,
           'on_pve_mecha_show_changed': self._update_pve_mecha_item_choose,
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
        is_intimacy_share = bool(global_data.player and global_data.player.is_intimacy_share_mecha(pve_mecha_id))
        has_mecha = bool(global_data.player and global_data.player.get_item_by_no(pve_mecha_id)) or is_intimacy_share
        img_lock = btn_mecha.img_lock
        nd_intimacy = btn_mecha.nd_share_tips
        if not has_mecha:
            img_lock.setVisible(True)
            img_lock.lab_not_have.setVisible(True)
        else:
            img_lock.setVisible(False)
            img_lock.lab_not_have.setVisible(False)
        nd_intimacy.setVisible(is_intimacy_share)
        if mecha_id == (global_data.player and global_data.player.get_pve_select_mecha_id()):
            btn_mecha.nd_tag_in_code.setVisible(True)
        else:
            btn_mecha.nd_tag_in_code.setVisible(False)
        pve_mecha_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_MECHA_NEW_CACHE, [])
        if mecha_id not in pve_mecha_cache and has_mecha:
            btn_mecha.img_new.setVisible(True)
        else:
            btn_mecha.img_new.setVisible(False)
        if pve_mecha_id == (global_data.player and global_data.player.get_pve_selected_mecha_item_id()):
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

    def _init_img_mecha_position(self, nd_cut, mecha_id):
        ui_display_conf = confmgr.get('ui_display_conf', 'MechaSummonUIItem', 'Content', default={})
        node_ui_conf = ui_display_conf.get(str(mecha_id))
        if node_ui_conf:
            pos = node_ui_conf.get('NodePos')
            if pos:
                nd_cut.img_mecha.SetPosition(*pos)
            else:
                nd_cut.img_mecha.ReConfPosition()
            pos = node_ui_conf.get('ShadowPos')
            if pos:
                nd_cut.img_mecha_shadow.SetPosition(*pos)
            else:
                nd_cut.img_mecha_shadow.ReConfPosition()
            scale = node_ui_conf.get('NodeScale')
            if scale:
                nd_cut.img_mecha.SetScaleCheckRecord(scale)
                nd_cut.img_mecha_shadow.SetScaleCheckRecord(scale)
            else:
                nd_cut.img_mecha.ScaleSelfNode()
                nd_cut.img_mecha_shadow.ScaleSelfNode()
        else:
            nd_cut.img_mecha.ReConfPosition()
            nd_cut.img_mecha_shadow.ReConfPosition()
            nd_cut.img_mecha.ScaleSelfNode()
            nd_cut.img_mecha_shadow.ScaleSelfNode()

    def _on_btn_mecha_clicked(self, btn, mecha_id):
        if not self._can_click_mecha:
            return
        if self._cur_select_item == btn:
            return
        self._del_mecha_item_new(btn, mecha_id)
        global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)
        self._can_click_mecha = False

    def _on_pve_main_model_load_complete(self, *args):
        self._can_click_mecha = True

    def _update_pve_select_mecha(self, mecha_id):
        for _mecha_id, item in six_ex.items(self._mecha_id_2_item):
            if item and item.isValid():
                btn_mecha = item.nd_select.nd_btn.btn_mecha
                if _mecha_id == mecha_id:
                    btn_mecha.nd_tag_in_code.setVisible(True)
                else:
                    btn_mecha.nd_tag_in_code.setVisible(False)

    def _update_pve_mecha_item_choose(self, mecha_id):
        for _mecha_id, item in six_ex.items(self._mecha_id_2_item):
            if item and item.isValid():
                btn_mecha = item.nd_select.nd_btn.btn_mecha
                if _mecha_id == mecha_id:
                    self._cur_select_item = btn_mecha
                    self._cur_select_mecha_id = mecha_id
                    btn_mecha.SetSelect(True)
                    btn_mecha.img_frame_choose.setVisible(True)
                else:
                    btn_mecha.SetSelect(False)
                    btn_mecha.img_frame_choose.setVisible(False)

    def _update_pve_mecha_item(self, *args):
        for mecha_id, item in six_ex.items(self._mecha_id_2_item):
            if item and item.isValid():
                img_lock = item.nd_select.nd_btn.btn_mecha.img_lock
                nd_intimacy = item.nd_select.nd_btn.btn_mecha.nd_share_tips
                pve_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
                is_intimacy_share = bool(global_data.player and global_data.player.is_intimacy_share_mecha(pve_mecha_id))
                has_mecha = bool(global_data.player and global_data.player.get_item_by_no(pve_mecha_id)) or is_intimacy_share
                if not has_mecha:
                    img_lock.setVisible(True)
                    img_lock.lab_not_have.setVisible(True)
                else:
                    img_lock.setVisible(False)
                    img_lock.lab_not_have.setVisible(False)
                nd_intimacy and nd_intimacy.setVisible(is_intimacy_share)

    def _del_mecha_item_new(self, btn_mecha, mecha_id):
        pve_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
        if bool(global_data.player and global_data.player.get_item_by_no(pve_mecha_id)):
            archive_data = global_data.achi_mgr.get_general_archive_data()
            pve_mecha_cache = archive_data.get_field(PVE_MECHA_NEW_CACHE, [])
            if mecha_id not in pve_mecha_cache:
                pve_mecha_cache.append(mecha_id)
                pve_mecha_cache = archive_data.set_field(PVE_MECHA_NEW_CACHE, pve_mecha_cache)
        btn_mecha.img_new.setVisible(False)

    def destroy(self):
        self.process_events(False)
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        self._cur_select_mecha_id = None
        self._cur_select_item = None
        self._open_mecha_id_list = None
        self._mecha_id_2_item = None
        self._can_click_mecha = None
        return