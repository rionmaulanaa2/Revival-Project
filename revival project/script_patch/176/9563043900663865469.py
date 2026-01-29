# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryMechaPreviewAdvancedAppearanceWidget.py
from __future__ import absolute_import
from logic.comsys.common_ui.MechaPreviewAdvancedAppearanceWidget import MechaPreviewAdvancedAppearanceWidget
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_PET_SKIN
from logic.gutils.mecha_skin_utils import is_mecha_skin_customable, is_ss_level_skin
from logic.gutils.item_utils import check_is_improvable_skin
from logic.gutils.mecha_skin_utils import get_mecha_conf_ex_weapon_sfx_id
from logic.gutils.pet_utils import is_ss_pet

class LotteryMechaPreviewAdvancedAppearanceWidget(MechaPreviewAdvancedAppearanceWidget):

    def __init__(self, parent, nd_btn, need_consider_equipment, need_play_ex_anim=False, show_anim_cb=None):
        super(LotteryMechaPreviewAdvancedAppearanceWidget, self).__init__(parent, nd_btn, need_consider_equipment, need_play_ex_anim)
        self._show_anim_cb = show_anim_cb

    def refresh_show_model(self, skin_id, skin_type, force_update=False):
        if self.skin_id == skin_id and not force_update:
            return
        old_skin_id = self.skin_id
        self.skin_id = skin_id
        if skin_type == L_ITEM_TYPE_MECHA_SKIN:
            self.inner_visible = is_mecha_skin_customable(skin_id) and not self._check_equip_shiny_weapon(skin_id)
        elif skin_type == L_ITEM_TYPE_ROLE_SKIN:
            self.inner_visible = check_is_improvable_skin(skin_id) and not self._check_equip_shiny_weapon(skin_id)
        elif skin_type == L_ITEM_TYPE_PET_SKIN:
            self.inner_visible = is_ss_pet(skin_id)
        else:
            self.inner_visible = False
        self._refresh_visible_state()
        if old_skin_id != skin_id:
            self._set_select(False)
        if self.inner_visible:
            icon_splus_ex = self.nd_btn.icon_splus_ex
            lab_splus_ex = self.nd_btn.lab_splus_ex
            icon_ex = self.nd_btn.icon_ex
            lab_change = self.nd_btn.lab_change
            if is_ss_level_skin(skin_id):
                if self.need_play_ex_anim and not self.archive_data.get(skin_id, False):
                    self._show_ex_loop_tips(True)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_ex.png')
                lab_splus_ex and lab_splus_ex.SetString(611644)
                icon_ex and icon_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/lottery/icon_lottery_main_ex.png')
                lab_change and lab_change.SetString(611644)
                self.set_nd_tips_text(611645)
            elif is_ss_pet(skin_id):
                if self.need_play_ex_anim and not self.archive_data.get(skin_id, False):
                    self._show_ex_loop_tips(True)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_ex.png')
                lab_splus_ex and lab_splus_ex.SetString(860436)
                lab_change and lab_change.SetString(860436)
                icon_ex and icon_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/lottery/icon_lottery_main_ex.png')
                self.set_nd_tips_text(860438)
            else:
                self._show_ex_loop_tips(False)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_splus.png')
                lab_splus_ex and lab_splus_ex.SetString(611643)
                lab_change and lab_change.SetString(611643)
                icon_ex and icon_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_s_plus.png')
                self.set_nd_tips_text(611645)
            if skin_type == L_ITEM_TYPE_MECHA_SKIN:
                self.shiny_weapon_id = get_mecha_conf_ex_weapon_sfx_id(skin_id)

    def _refresh_visible_state(self):
        if self._show_anim_cb and self.inner_visible and self.outer_visible:
            self._show_anim_cb()
        else:
            self.nd_btn.setVisible(self.inner_visible and self.outer_visible)