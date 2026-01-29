# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/MechaPreviewAdvancedAppearanceWidget.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_PET_SKIN
from logic.gutils.mecha_skin_utils import is_mecha_skin_customable, is_ss_level_skin, get_mecha_skin_shiny_id
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.cfg import confmgr
from logic.gutils.item_utils import check_is_improvable_skin, get_lobby_item_type, get_lobby_item_belong_no
from logic.gutils import dress_utils
from logic.gutils.mecha_skin_utils import get_mecha_conf_ex_weapon_sfx_id
from logic.gutils.pet_utils import is_ss_pet
from logic.gutils.role_skin_utils import get_skin_improved_sfx_item_id, get_improve_skin_body_path

class MechaPreviewAdvancedAppearanceWidget(object):

    def __init__(self, parent, nd_btn, need_consider_equipment, need_play_ex_anim=False):
        self.parent = parent
        self.nd_btn = nd_btn
        self.nd_btn.setVisible(False)
        self.outer_visible = True
        self.inner_visible = False
        self.skin_id = None
        self.shiny_weapon_id = None
        self.need_consider_equipment = need_consider_equipment
        self.need_play_ex_anim = need_play_ex_anim
        self.original_position = nd_btn.getPosition()
        self.ex_loop_tips_visible = False
        self.archive_data = ArchiveManager().get_archive_data('lottery_btn_ex_anim_played')
        self.need_check_role_decoration = True
        self.role_preview_decoration = {}
        self.equip_check_callback = None
        self.is_selected = False

        @global_unique_click(self.nd_btn)
        def OnClick(*args, **kwargs):
            select = not self.is_select()
            self.set_select_result(select)

        return

    def set_select_result(self, select):
        self._set_select(select)
        item_type = get_lobby_item_type(self.skin_id)
        if item_type == L_ITEM_TYPE_ROLE_SKIN:
            global_data.emgr.show_skin_improved_sfx.emit(True if select else False)
            if callable(self.equip_check_callback):
                self.equip_check_callback(self.skin_id)
            self.enable_preview_splus_decoration(True if select else False)
        elif item_type == L_ITEM_TYPE_MECHA_SKIN:
            self._show_ex_loop_tips(False, is_click=True)
            if callable(self.equip_check_callback):
                self.equip_check_callback(self.skin_id)
            global_data.emgr.show_shiny_weapon_sfx.emit(self.skin_id, self.shiny_weapon_id if select else None, select or self.shiny_weapon_id if 1 else None)
        elif item_type == L_ITEM_TYPE_PET_SKIN:
            self._show_ex_loop_tips(False, is_click=True)
            skin_conf = confmgr.get('c_pet_info', str(self.skin_id), default={})
            max_level = skin_conf.get('max_level', 1)
            pet_lv = max_level if select else 1
            self.parent.on_change_show_reward(self.skin_id, pet_level=pet_lv)
        return

    def set_need_check_role_decoration(self, enable):
        self.need_check_role_decoration = enable

    def enable_preview_splus_decoration(self, enable):
        skin_id = self.skin_id
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(self.skin_id)
        default_show_dict = dress_utils.get_skin_default_show_decoration_dict(skin_id)
        improve_skin_id = get_skin_improved_sfx_item_id(skin_id)
        need_refresh_model = get_improve_skin_body_path(improve_skin_id)
        if enable:
            if self.need_check_role_decoration:
                cur_decoration_data = self.get_role_preview_data(skin_id, with_default=False)
            else:
                cur_decoration_data = {}
            top_skin_id = dress_utils.get_top_skin_id_by_skin_id(self.skin_id)
            conf = confmgr.get('role_info', 'RoleSkin', 'Content', str(top_skin_id))
            all_collect_items = conf['skin_improve_collected_items']
            all_skin_items = []
            all_decoration_items = []
            for item_id in all_collect_items:
                if get_lobby_item_type(item_id) == L_ITEM_TYPE_ROLE_SKIN:
                    all_skin_items.append(item_id)
                else:
                    all_decoration_items.append(item_id)

            preview_decoration = {}
            all_decoration_items.sort(key=lambda tid: True if global_data.player.get_item_by_no(tid) else False, reverse=True)
            for dec_id in all_decoration_items:
                lobby_type = get_lobby_item_type(dec_id)
                fashion_pos = dress_utils.get_lobby_type_fashion_pos(lobby_type)
                cur_dec_id = cur_decoration_data.get(fashion_pos)
                can_dress_cur = cur_dec_id and dress_utils.check_valid_decoration(skin_id, cur_dec_id)
                if not can_dress_cur:
                    if fashion_pos not in preview_decoration:
                        if dress_utils.check_valid_decoration(skin_id, dec_id):
                            preview_decoration[fashion_pos] = dec_id
                else:
                    preview_decoration[fashion_pos] = cur_dec_id

            for fashion_pos, default_dec_id in six.iteritems(default_show_dict):
                if fashion_pos not in preview_decoration:
                    if dress_utils.check_valid_decoration(skin_id, default_dec_id):
                        preview_decoration[fashion_pos] = default_dec_id

            if need_refresh_model:
                global_data.emgr.register_display_loaded_callback.emit(lambda preview_decoration=preview_decoration: self.set_preview_decoration(preview_decoration))
            else:
                self.set_preview_decoration(preview_decoration)
            self.role_preview_decoration = preview_decoration
        else:
            revert_dict = {}
            for fashion_pos in six.iterkeys(self.role_preview_decoration):
                revert_dict[fashion_pos] = 0

            if self.need_check_role_decoration:
                dec_dict = self.get_role_preview_data(skin_id, with_default=True)
            else:
                dec_dict = default_show_dict
            for fashion_pos, dec_id in six.iteritems(dec_dict):
                if dec_id:
                    if dress_utils.check_valid_decoration(skin_id, dec_id):
                        revert_dict[fashion_pos] = dec_id

            if need_refresh_model:
                global_data.emgr.register_display_loaded_callback.emit(lambda revert_dict=revert_dict: self.set_preview_decoration(revert_dict))
            else:
                self.set_preview_decoration(revert_dict)

    def get_role_preview_data(self, skin_id, with_default):
        from logic.gcommon.item.item_const import FASHION_DECORATION_TYPE_LIST
        role_id = get_lobby_item_belong_no(skin_id)
        if skin_id == dress_utils.get_role_dress_clothing_id(role_id, check_default=True):
            role_data = global_data.player.get_item_by_no(role_id)
            if not role_data:
                return {}
            decoration_type = FASHION_DECORATION_TYPE_LIST
            get_func = dress_utils.get_role_decroation_id
            decoration_data = {dtype:get_func(role_id, skin_id, dtype) for dtype in decoration_type}
            return decoration_data
        else:
            if global_data.player.check_need_request_role_top_skin_scheme(role_id):
                return {}
            has_set = global_data.player.check_has_set_skin_scheme(role_id, skin_id)
            decoration_data = dress_utils.get_role_fashion_decoration_dict(role_id, skin_id)
            if with_default:
                if not has_set:
                    default_show_dict = dress_utils.get_skin_default_show_decoration_dict(skin_id)
                    return default_show_dict
            return decoration_data

    def set_preview_decoration(self, decoration_dict):
        skin_id = self.skin_id
        from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
        CONDUCT_EVENT = {FASHION_POS_HEADWEAR: 'change_model_display_head',
           FASHION_POS_BACK: 'change_model_display_bag',
           FASHION_POS_SUIT_2: 'change_model_display_suit'
           }
        if FASHION_POS_SUIT_2 in decoration_dict:
            value = decoration_dict[FASHION_POS_SUIT_2]
            decoration_dict = {FASHION_POS_SUIT_2: value}
        for tag, item_no in six.iteritems(decoration_dict):
            if tag in CONDUCT_EVENT:
                global_data.emgr.emit(CONDUCT_EVENT[tag], int(item_no), int(skin_id))
            else:
                self.refresh_other_pendant_info(decoration_dict, int(skin_id))

    def refresh_other_pendant_info(self, preview_decoration, skin_id):
        from logic.gcommon.item.item_const import FASHION_MAIN_PENDANT_LIST, FASHION_OTHER_PENDANT_LIST
        new_pendant_info = {}
        for tag, item_no in six.iteritems(preview_decoration):
            if item_no and tag not in FASHION_MAIN_PENDANT_LIST and tag in FASHION_OTHER_PENDANT_LIST:
                new_pendant_info[tag] = item_no

        pendant_id_list = six_ex.values(new_pendant_info)
        global_data.emgr.emit('change_display_model_other_pendant', pendant_id_list, skin_id)

    def destroy(self):
        self.parent = None
        self.nd_btn = None
        self.equip_check_callback = None
        self.archive_data.save()
        self.archive_data = None
        return

    def _refresh_visible_state(self):
        self.nd_btn.setVisible(self.inner_visible and self.outer_visible)

    def is_visible(self):
        return self.inner_visible and self.outer_visible

    def set_visible(self, visible):
        if self.outer_visible ^ visible:
            self.outer_visible = visible
            self._refresh_visible_state()

    def _set_select(self, flag):
        self.is_selected = flag
        img_choose = self.nd_btn.img_choose
        img_choose and img_choose.setVisible(flag)
        self.nd_btn.nd_tips and self.nd_btn.nd_tips.setVisible(flag)

    def _check_equip_shiny_weapon(self, skin_id):
        if self.need_consider_equipment:
            return get_mecha_skin_shiny_id(skin_id)
        return False

    def _show_ex_loop_tips(self, flag, is_click=False):
        if self.ex_loop_tips_visible ^ flag:
            self.ex_loop_tips_visible = flag
            vx_ex_btn = self.nd_btn.vx_ex_btn
            vx_ex_btn and vx_ex_btn.setVisible(flag)
            if flag:
                self.parent.panel.PlayAnimation('ex_btn')
            else:
                self.parent.panel.StopAnimation('ex_btn')
                if is_click:
                    self.archive_data[self.skin_id] = True

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
            if is_ss_level_skin(skin_id):
                if self.need_play_ex_anim and not self.archive_data.get(skin_id, False):
                    self._show_ex_loop_tips(True)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_ex.png')
                lab_splus_ex and lab_splus_ex.SetString(611644)
                self.set_nd_tips_text(611645)
            elif is_ss_pet(skin_id):
                if self.need_play_ex_anim and not self.archive_data.get(skin_id, False):
                    self._show_ex_loop_tips(True)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_ex.png')
                lab_splus_ex and lab_splus_ex.SetString(860436)
                self.set_nd_tips_text(860438)
            else:
                self._show_ex_loop_tips(False)
                icon_splus_ex and icon_splus_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_mech_display_splus.png')
                lab_splus_ex and lab_splus_ex.SetString(611643)
                self.set_nd_tips_text(611645)
            if skin_type == L_ITEM_TYPE_MECHA_SKIN:
                self.shiny_weapon_id = get_mecha_conf_ex_weapon_sfx_id(skin_id)

    def set_nd_tips_text(self, text_id):
        if self.nd_btn.nd_tips and self.nd_btn.nd_tips.bar_tips and self.nd_btn.nd_tips.bar_tips.lab_tips:
            self.nd_btn.nd_tips.bar_tips.lab_tips.SetString(text_id)

    def set_position(self, same_pos_node=None):
        if same_pos_node is None:
            target_pos = self.original_position
        else:
            target_pos = same_pos_node.getPosition()
        if self.nd_btn.getPosition().y != target_pos.y:
            self.nd_btn.setPosition(target_pos)
            self.nd_btn.ChildResizeAndPosition()
        return

    def set_select(self, sel):
        self._set_select(flag=sel)

    def set_select_with_click(self, target_sel):
        select = self.is_select()
        if target_sel != select:
            self.nd_btn.OnClick()

    def is_select(self):
        return self.is_selected

    def set_equip_check_callback(self, cb):
        self.equip_check_callback = cb