# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEShopMechaUI.py
from __future__ import absolute_import
from logic.gutils.item_utils import get_lobby_item_name, get_skin_rare_degree_icon
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.mecha_skin_utils import is_default_mecha_skin, get_cur_skin_id
from .PVEShopMechaChooseWidget import PVEShopMechaChooseWidget
from common.uisys.basepanel import BasePanel
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
MECHA_PIC_PATH = 'gui/ui_res_2/battle_mech_call_pic/{}.png'

class PVEShopMechaUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/shop/pve_shop_mecha'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(PVEShopMechaUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self._cur_mecha_id = None
        self._mecha_choose_widget = None
        return

    def init_ui(self):
        self._mecha_choose_widget = PVEShopMechaChooseWidget(self, self.panel.list_mecha)
        self._update_mecha_widget()

    def init_ui_event(self):

        @self.panel.btn_confirm.unique_callback()
        def OnClick(btn, touch):
            if not self._cur_mecha_id:
                return
            if not global_data.player:
                return
            if not global_data.player.logic:
                return
            if not global_data.cam_lplayer:
                return
            if global_data.cam_lplayer.id != global_data.player.id:
                return
            if self._cur_mecha_id == global_data.player.logic.ev_g_get_bind_mecha_type():
                return
            global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', 'request_reset_pve_mecha', (self._cur_mecha_id,))

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_show_changed': self._update_mecha_widget,
           'on_pve_mecha_changed_in_battle': self.close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _update_mecha_widget(self, mecha_id=None):
        pve_selected_mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type() if global_data.player and global_data.player.logic else 8001
        self._cur_mecha_id = mecha_id if mecha_id else pve_selected_mecha_id
        mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        mecha_fashion_id = global_data.player.get_pve_using_mecha_skin(mecha_item_id) if global_data.player else DEFAULT_CLOTHING_ID
        if mecha_fashion_id == DEFAULT_CLOTHING_ID:
            mecha_fashion_id = get_cur_skin_id(self._cur_mecha_id)
        mecha_pic_path = MECHA_PIC_PATH.format(mecha_fashion_id)
        self.panel.pic.SetDisplayFrameByPath('', mecha_pic_path)
        lab_name_mecha = self.panel.bar_name.lab_name_mecha
        nd_skin = self.panel.nd_skin
        if is_default_mecha_skin(mecha_fashion_id, mecha_item_id):
            lab_name_mecha.setVisible(True)
            lab_name_mecha.SetString(get_lobby_item_name(mecha_item_id))
            nd_skin.setVisible(False)
        else:
            lab_name_mecha.setVisible(False)
            nd_skin.setVisible(True)
            nd_skin.lab_name_mecha.SetString(get_lobby_item_name(mecha_item_id))
            nd_skin.lab_name_skin.SetString(get_lobby_item_name(mecha_fashion_id))
            temp_level = nd_skin.temp_level
            degree_pic = get_skin_rare_degree_icon(mecha_fashion_id)
            if degree_pic:
                temp_level.setVisible(True)
                temp_level.bar_level.SetDisplayFrameByPath('', degree_pic)
            else:
                temp_level.setVisible(False)

    def on_finalize_panel(self):
        super(PVEShopMechaUI, self).on_finalize_panel()
        self.process_events(False)
        if self._mecha_choose_widget:
            self._mecha_choose_widget.destroy()
            self._mecha_choose_widget = None
        return