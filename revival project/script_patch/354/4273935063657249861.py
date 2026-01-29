# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESelectLevelMechaWidget.py
from __future__ import absolute_import
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_active_mecha_id_list
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id, DEFAULT_CLOTHING_ID
from .PVESelectLevelSkinWidget import PVESelectLevelSkinWidget
from logic.gutils.pve_utils import update_model_and_cam_pos
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from common.cfg import confmgr
from logic.gcommon.const import SKIN_SHARE_TYPE_PRIV
OFF_POSITION = [
 -7, 0, 0]
OFF_MODEL_POSITION = [-14, 0, 0]
NORMAL_POSITION = [-130, 0, 0]

class PVESelectLevelMechaWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self.panel = panel
        self.init_parameters()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_parameters(self):
        self._skin_widget = None
        self.cur_mecha_id = None
        self.is_showing_skin_widget = False
        return

    def init_ui(self):
        mecha_id = global_data.player.get_pve_select_mecha_id() if global_data.player else 8001
        self._update_lab_name(mecha_id)

    def init_ui_event(self):

        @self.panel.btn_confirm.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            skin_choose_widget = self.get_skin_choose_widget()
            if not skin_choose_widget:
                return
            mecha_id, clothing_id = skin_choose_widget.get_current_id()
            is_share, _ = global_data.player.is_share_mecha_skin(clothing_id)
            top_clothing_id = get_main_skin_id(clothing_id)
            if is_share:
                fashion_data = global_data.player.get_share_mecha_fashion_data(clothing_id)
                global_data.player.set_chosen_pve_share_fashion(fashion_data)
            else:
                global_data.player.set_chosen_pve_share_fashion({})
                global_data.player.install_mecha_main_skin_scheme(mecha_id, top_clothing_id, {FASHION_POS_SUIT: clothing_id})
            if mecha_id != global_data.player.get_pve_select_mecha_id():
                global_data.player.pve_select_mecha(mecha_id)
            update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
            self.is_showing_skin_widget = False
            self._parent.PlayAnimation('revert')

        @self.panel.btn_left_mecha.callback()
        def OnClick(btn, touch):
            self.on_click_btn_left()

        @self.panel.btn_right_mecha.callback()
        def OnClick(btn, touch):
            self.on_click_btn_right()

        @self.panel.btn_switch.callback()
        def OnClick(btn, touch):
            self.on_click_btn_switch()

    def on_force_click_btn_confirm(self, *args):
        update_model_and_cam_pos(NORMAL_POSITION, NORMAL_POSITION)
        self.is_showing_skin_widget = False
        self._parent.PlayAnimation('revert')

    def on_click_btn_left(self):
        open_mecha_list = get_pve_active_mecha_id_list()
        if self.cur_mecha_id in open_mecha_list:
            index = open_mecha_list.index(self.cur_mecha_id)
        else:
            index = 1
        if index == 0:
            last_index = len(open_mecha_list) - 1 if 1 else index - 1
            mecha_id = open_mecha_list[last_index]
            self.is_showing_skin_widget or global_data.player and global_data.player.pve_select_mecha(mecha_id)
        global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)

    def on_click_btn_right(self):
        open_mecha_list = get_pve_active_mecha_id_list()
        if self.cur_mecha_id in open_mecha_list:
            index = open_mecha_list.index(self.cur_mecha_id)
        else:
            index = len(open_mecha_list) - 1
        if index == len(open_mecha_list) - 1:
            next_index = 0 if 1 else index + 1
            mecha_id = open_mecha_list[next_index]
            self.is_showing_skin_widget or global_data.player and global_data.player.pve_select_mecha(mecha_id)
        global_data.emgr.on_pve_mecha_show_changed.emit(mecha_id)

    def on_click_btn_switch(self):
        self._parent.PlayAnimation('switch')
        self.is_showing_skin_widget = True
        update_model_and_cam_pos(OFF_POSITION, OFF_MODEL_POSITION)
        if not self._skin_widget:
            self._skin_widget = PVESelectLevelSkinWidget(self._parent, self.panel.nd_skin)
            self._update_pve_mecha_skin_item()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_changed': [
                                  self._update_lab_name, self._update_pve_mecha_skin_item],
           'on_pve_mecha_show_changed': [
                                       self._update_lab_name, self._update_pve_mecha_skin_item],
           'on_pve_select_skin_widget_hide': self.on_pve_select_skin_widget_hide,
           'on_pve_mecha_skin_changed': self._update_pve_mecha_skin_item,
           'player_item_update_event': self._update_pve_mecha_skin_item,
           'pay_order_succ_event': self._update_pve_mecha_skin_item,
           'update_skin_share_state': self._update_pve_mecha_skin_item
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _update_lab_name(self, mecha_id):
        self.cur_mecha_id = mecha_id
        self.panel.lab_name_mecha.SetString(get_mecha_name_by_id(self.cur_mecha_id))

    def on_pve_select_skin_widget_hide(self):
        self.is_showing_skin_widget = False

    def get_skin_choose_widget(self):
        if self._skin_widget:
            return self._skin_widget.get_skin_choose_widget()
        else:
            return None

    def _update_pve_mecha_skin_item(self, *args):
        skin_choose_widget = self.get_skin_choose_widget()
        if not skin_choose_widget:
            self.panel.btn_confirm.setVisible(False)
            return
        else:
            mecha_id, clothing_id = skin_choose_widget.get_current_id()
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
            clothing_data = global_data.player.get_item_by_no(clothing_id) if global_data.player else None
            if global_data.player:
                is_share, share_type = global_data.player.is_share_mecha_skin(clothing_id)
                is_intimacy_share_mecha = global_data.player.is_intimacy_share_mecha(cur_mecha_item_id)
            else:
                is_share, share_type = False, None
                is_intimacy_share_mecha = False
            if is_share and share_type == SKIN_SHARE_TYPE_PRIV:
                is_teammate_lobby_skin = global_data.player.is_teammate_lobby_skin(clothing_id)
                is_share = bool(is_share and not is_teammate_lobby_skin)
            is_default_skin = False
            if int(default_skin) == int(clothing_id):
                clothing_data = global_data.player.get_item_by_no(cur_mecha_item_id) if global_data.player else None
                is_default_skin = True
            is_owned_mecha = bool(global_data.player and global_data.player.get_item_by_no(cur_mecha_item_id)) or is_intimacy_share_mecha
            is_owned_skin = bool(clothing_data) or is_share
            is_owned = is_owned_mecha and (is_default_skin or is_owned_skin)
            pve_mecha_id = global_data.player.get_pve_select_mecha_id() if global_data.player else None
            pve_mecha_item_id = global_data.player.get_pve_selected_mecha_item_id() if global_data.player else None
            fashion_id = global_data.player.get_pve_using_mecha_skin(pve_mecha_item_id) if global_data.player else DEFAULT_CLOTHING_ID
            is_use = mecha_id == pve_mecha_id and clothing_id == fashion_id
            self.panel.btn_confirm.setVisible(is_owned and not is_use)
            self.panel.lab_status.setVisible(is_use)
            return

    def destroy(self):
        self.process_events(False)
        if self._skin_widget:
            self._skin_widget.destroy()
            self._skin_widget = None
        self.cur_mecha_id = None
        self.is_showing_skin_widget = None
        return