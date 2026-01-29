# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/ChangeMechaUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, DIALOG_LAYER_ZORDER_2
import cc
from common.cfg import confmgr
from common.const import uiconst
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils import skin_define_utils
import logic.gutils.dress_utils as dress_utils
from logic.gutils import mecha_skin_utils
from logic.gutils import item_utils
from logic.gutils.template_utils import show_remain_time
from logic.gutils import red_point_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.common_utils.local_text import get_text_by_id

class ChangeMechaUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/change_mecha'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close',
       'btn_mecha.OnClick': 'on_click_btn_mecha',
       'btn_skin.OnClick': 'on_click_btn_skin'
       }
    GLOBAL_EVENT = {'on_lobby_mecha_changed': 'change_lobby_mecha'
       }

    def on_init_panel(self):
        self.hide_main_ui()
        self.init_parameters()
        self.refresh_mecha_list()

    def on_finalize_panel(self):
        self.show_main_ui()

    def init_parameters(self):
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._open_mecha_lst = [8001]
        self._cur_mecha_id = 0
        self.clothing_selected_index = 0
        self.group_clothing_selected_index = 0
        self.cur_clothing_id = 0

    def init_open_lst(self):
        if not global_data.player:
            self.close()
            return
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            self._open_mecha_lst = []
            for mecha_id in mecha_open_info['opened_order']:
                if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                    self._open_mecha_lst.append(mecha_id)

    def on_click_btn_mecha(self, btn, touch):
        if self.panel.nd_mecha.isVisible():
            return
        self.btn_mecha.SetSelect(True)
        self.btn_skin.SetSelect(False)
        self.panel.nd_mecha.setVisible(True)
        self.panel.nd_skin.setVisible(False)
        self.refresh_mecha_list()

    def on_click_btn_skin(self, btn, touch):
        if self.panel.nd_skin.isVisible():
            return
        if not global_data.player:
            return
        self.btn_mecha.SetSelect(False)
        self.btn_skin.SetSelect(True)
        self.panel.nd_mecha.setVisible(False)
        self.panel.nd_skin.setVisible(True)
        self.refresh_mecha_skin_list()

    def update_title(self):
        img_path = 'gui/ui_res_2/main/select_mecha/img_topbar_mecha_%s.png' % self._cur_mecha_id
        self.panel.img_mecha.SetDisplayFrameByPath('', img_path)
        clothing_id = self.show_skin_list_cnf[self.clothing_selected_index]
        item_config = confmgr.get('lobby_item', str(clothing_id))
        item_no = item_config.get('item_no')
        name_text = item_utils.get_lobby_item_name(item_no)
        if self.clothing_selected_index == 0:
            conf = self._mecha_conf[str(self._cur_mecha_id)]
            name_text = conf.get('name_mecha_text_id', '')
            name_text = get_text_by_id(name_text)
        self.panel.lab_mecha_name.setString(name_text)

    def refresh_mecha_list(self):
        self.btn_mecha.SetSelect(True)
        self.init_open_lst()
        if not self.panel:
            return
        else:
            self.panel.list_mecha.SetInitCount(len(self._open_mecha_lst))
            self._cur_mecha_id = self._open_mecha_lst[0]
            all_item = self.panel.list_mecha.GetAllItem()
            cur_mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
            cur_use_mecha_id = dress_utils.mecha_lobby_id_2_battle_id(cur_mecha_item_id)
            self._cur_mecha_id = cur_use_mecha_id
            for index, ui_item in enumerate(all_item):
                mecha_id = self._open_mecha_lst[index]
                if cur_use_mecha_id == mecha_id:
                    ui_item.nd_choose.setVisible(True)
                conf = self._mecha_conf[str(mecha_id)]
                img_path = 'gui/ui_res_2/main/select_mecha/img_mecha_%s.png' % mecha_id
                btn = ui_item
                btn.SetFrames('', [img_path, img_path, img_path], False, None)
                name = conf.get('name_mecha_text_id', '')
                btn.SetText(name)

                @btn.callback()
                def OnClick(btn, touch, mecha_id=mecha_id):
                    if not global_data.player:
                        return
                    all_item = self.panel.list_mecha.GetAllItem()
                    for index, ui_item in enumerate(all_item):
                        ui_item.nd_choose.setVisible(False)

                    btn.nd_choose.setVisible(True)
                    self.select_origi_mecha(mecha_id)

            return

    def refresh_mecha_skin_list(self):
        all_show_skin_list_cnf = mecha_skin_utils.get_show_skin_list(self._cur_mecha_id)
        self.show_skin_list_cnf = []
        cur_use_mecha_clothing_id = global_data.emgr.lobby_cur_mecha_clothing_id.emit()[0]
        for index, one_conf in enumerate(all_show_skin_list_cnf):
            clothing_id = all_show_skin_list_cnf[index]
            clothing_data = global_data.player.get_item_by_no(clothing_id)
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
            if not clothing_data or not mecha_item_data:
                continue
            is_default_skin = False
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
            if int(default_skin) == int(clothing_id):
                is_default_skin = True
            if is_default_skin:
                is_owned = clothing_data and clothing_data.get_expire_time() < 0
            else:
                is_owned = clothing_data
            if not is_owned:
                continue
            self.show_skin_list_cnf.append(clothing_id)

        self.panel.list_skin.SetInitCount(len(self.show_skin_list_cnf))
        all_item = self.panel.list_skin.GetAllItem()
        self.clothing_selected_index = -1
        for index, ui_item in enumerate(all_item):
            clothing_id = self.show_skin_list_cnf[index]
            item_config = confmgr.get('lobby_item', str(clothing_id))
            if cur_use_mecha_clothing_id == clothing_id:
                self.clothing_selected_index = index
            self.init_clothing_item(item_config, ui_item, clothing_id, index)

        self.update_title()

    def init_clothing_item(self, item_config, clothing_item, clothing_id, idx_in_skin_lst):
        clothing_item.nd_using.setVisible(self.clothing_selected_index == idx_in_skin_lst)
        item_no = item_config.get('item_no')
        name_text = item_utils.get_lobby_item_name(item_no)
        if idx_in_skin_lst == 0:
            conf = self._mecha_conf[str(self._cur_mecha_id)]
            name_text = conf.get('name_mecha_text_id', '')
            name_text = get_text_by_id(name_text)
        clothing_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(clothing_item, clothing_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
        if skin_cfg:
            item_utils.check_skin_tag(clothing_item.nd_kind, clothing_id)
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                clothing_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
        show_remain_time(clothing_item.nd_time, clothing_item.nd_time.lab_time, clothing_id)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
        red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)
        clothing_data = global_data.player.get_item_by_no(clothing_id)
        if clothing_data is None:
            clothing_item.nd_lock.setVisible(True)
        else:
            clothing_item.nd_lock.setVisible(False)

        @clothing_item.nd_card.callback()
        def OnClick(btn, touch, skin_index=idx_in_skin_lst, item_no=clothing_id):
            if not global_data.player:
                return
            all_item = self.panel.list_skin.GetAllItem()
            for index, ui_item in enumerate(all_item):
                ui_item.nd_using.setVisible(False)

            clothing_item.nd_using.setVisible(True)
            self.select_skin_mecha(skin_index)
            global_data.player.req_del_item_redpoint(item_no)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
            red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)

        return

    def get_rel_clothing(self):
        skin_list = self.show_skin_list_cnf
        clothing_id = skin_list[self.clothing_selected_index]
        group_skin_list = skin_define_utils.get_group_skin_list(clothing_id)
        if group_skin_list:
            clothing_id = group_skin_list[self.group_clothing_selected_index]
        return (
         clothing_id, group_skin_list)

    def select_skin_mecha(self, selected_index):
        if selected_index != self.clothing_selected_index:
            skin_list = self.show_skin_list_cnf
            skin_id = skin_list[selected_index]
            self.clothing_selected_index = selected_index
            dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(self._cur_mecha_id)
            self.group_clothing_selected_index = 0
            group_skin_list = skin_define_utils.get_group_skin_list(skin_id)
            if group_skin_list:
                if dressed_clothing_id in group_skin_list:
                    self.group_clothing_selected_index = group_skin_list.index(dressed_clothing_id)
                elif skin_id in group_skin_list:
                    self.group_clothing_selected_index = group_skin_list.index(skin_id)
            self.cur_clothing_id = skin_id
            self._on_click_btn_buy_skin()
            self.update_title()

    def _on_click_btn_buy_skin(self, *args):
        clothing_id, _ = self.get_rel_clothing()
        rel_clothing_id = clothing_id
        top_clothing_id = skin_define_utils.get_main_skin_id(clothing_id)
        global_data.player.install_mecha_main_skin_scheme(self._cur_mecha_id, top_clothing_id, {FASHION_POS_SUIT: rel_clothing_id})

    def select_origi_mecha(self, mecha_id):
        self._cur_mecha_id = mecha_id
        cur_mecha_goods_id = self._mecha_info_conf.get(str(mecha_id), {}).get('goods_id', None)
        item_data = global_data.player.get_item_by_no(int(cur_mecha_goods_id))
        if item_data is not None:
            global_data.player.req_change_lobby_mecha(mecha_id)
        return

    def on_click_btn_enter_1(self, *args):
        self.close()

    def change_lobby_mecha(self):
        cur_mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        global_data.emgr.lobby_mecha_display_reset.emit()