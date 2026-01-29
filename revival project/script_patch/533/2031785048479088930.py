# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/RogueGiftPickUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
from common.uisys.basepanel import BasePanel
from logic.gutils import rogue_utils as r_u

class RogueGiftPickUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/battle_rogue'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_back.OnClick': '_on_btn_back_clicked'
       }
    GLOBAL_EVENT = {'global_pick_rogue_gifts_success': '_on_global_pick_rogue_gifts_success',
       'switch_to_right_aim_camera_event': '_on_switch_to_right_aim_camera_event',
       'on_observer_success_aim_event': '_on_observer_success_aim_event',
       'on_observer_attack_start': '_on_observer_attack_start',
       'avatar_mecha_main_or_sub_atk_start': '_on_avatar_mecha_main_or_sub_atk_start'
       }
    HIDE_UI_LIST = [
     'PickUI']

    def on_init_panel(self):
        super(RogueGiftPickUI, self).on_init_panel()
        self._init_data()
        self._init_view()

    def on_finalize_panel(self):
        super(RogueGiftPickUI, self).on_finalize_panel()
        self.show_main_ui()

    def do_show_panel(self):
        super(RogueGiftPickUI, self).do_show_panel()
        self.hide_main_ui(self.HIDE_UI_LIST)

    def do_hide_panel(self):
        super(RogueGiftPickUI, self).do_hide_panel()
        self.show_main_ui()

    def _init_data(self):
        pass

    def _init_view(self):
        self.panel.nd_list.SetInitCount(3)

    def set_data(self, box_id, gift_ids):
        self._box_id = box_id
        self._refresh_view(gift_ids)

    def _refresh_view(self, gift_ids):
        cnt = self._get_list_cnt()
        data_cnt = len(gift_ids) if gift_ids else 0
        for i in range(cnt):
            item = self._get_list_item(i)
            if i < data_cnt:
                gift_id = gift_ids[i]
            else:
                gift_id = -1
            if gift_id == -1:
                continue
            item.nd_bg.SetDisplayFrameByPath('', r_u.get_gift_bg(gift_id))
            item.img_firm.SetDisplayFrameByPath('', r_u.get_gift_icon(gift_id, big=True))
            item.lab_firm_name.SetString(r_u.get_gift_name_text(gift_id))
            item.lab_firm_name.SetColor(r_u.get_brand_name_color(gift_id))
            item.lab_firm.SetString(r_u.get_gift_desc_text(gift_id))
            got = False
            if global_data.player and global_data.player.logic:
                got = global_data.player.logic.ev_g_has_rogue_gift(gift_id)
            item.nd_get.setVisible(got)

            @item.btn_firm.unique_callback()
            def OnClick(btn, touch, gift_id=gift_id):
                if global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_CHOOSE_ROGUE_GIFT', self._box_id, gift_id)

    def _get_list_item(self, idx):
        return self.panel.nd_list.GetItem(idx)

    def _get_list_cnt(self):
        return self.panel.nd_list.GetItemCount()

    def _is_cam_avatar(self):
        if not global_data.cam_lplayer:
            return False
        else:
            avatar_unit = None
            if global_data.player:
                avatar_unit = global_data.player.logic
            if not avatar_unit:
                return False
            return global_data.cam_lplayer.id == avatar_unit.id

    def _on_btn_back_clicked(self, *args):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_CANCEL_CHOOSE_ROGUE_GIFT', self._box_id)
        self.close()

    def _on_global_pick_rogue_gifts_success(self):
        self.close()

    def _on_switch_to_right_aim_camera_event(self, *args):
        if not self._is_cam_avatar():
            return
        self.close()

    def _on_observer_success_aim_event(self, *args):
        if not self._is_cam_avatar():
            return
        self.close()

    def _on_observer_attack_start(self, *args):
        if not self._is_cam_avatar():
            return
        self.close()

    def _on_avatar_mecha_main_or_sub_atk_start(self, *args):
        self.close()