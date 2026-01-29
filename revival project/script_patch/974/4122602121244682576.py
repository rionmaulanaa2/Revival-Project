# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PetMainUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER, UI_VKB_CLOSE
from common.cfg import confmgr
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_const import scene_const
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no, check_skin_tag, is_itemtype_in_serving, get_pet_rare_degree_pic_by_item_no, get_item_rare_degree
from logic.gutils.items_book_utils import get_items_skin_conf
from logic.client.const.items_book_const import PET_ID
from common.framework import Functor
from logic.gutils import lobby_model_display_utils
import math3d
from logic.gcommon.common_const.ui_operation_const import ENABLE_PET_TRANSPARENT, ENABLE_PET_INTERACT_IN_BATTLE
from logic.gcommon.common_const.shop_const import PET_DAILY_EXP
from logic.gutils import mall_utils, item_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from functools import cmp_to_key
from .PetItemListWidget import PetItemListWidget
from .PetLevelWidget import PetLevelWidget
from .PetSkillWidget import PetSkillWidget
from .PetSubSkinWidget import PetSubSkinWidget
PET_ITEM_NO = 11001
SPEC_ANIM_TAG = 99
PET_OFF_POS_HIDE = [-5, 0, 0]
PET_OFF_POS_SHOW = [-20, 0, 0]
ROTATE_FACTOR = 850

class PetMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'pet/pet_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    GLOBAL_EVENT = {'display_model_end_show_anim': 'model_end_show_anim',
       'pet_daily_state_changed': 'on_pet_daily_state_changed',
       'pet_choosen_changed': 'on_pet_choosen_changed',
       'pet_sub_skin_changed': 'on_pet_sub_skin_changed'
       }

    @property
    def cur_skin_id(self):
        if not self._sub_skin_widget:
            return
        return self._sub_skin_widget.get_skin_id()

    def on_init_panel(self, *args, **kargs):
        self.panel.nd_left.pnl.list_item.SetInitCount(5)
        self.init_parameters()
        self.init_scene()
        self.init_panel()
        super(PetMainUI, self).on_init_panel()

    def init_parameters(self):
        self.is_in_expand_mode = True
        self.data_dict = confmgr.get('c_pet_info', default={})
        self.daily_state = global_data.player.get_pet_daily_state()
        choosen_pet = global_data.player and global_data.player.get_choosen_pet()
        self.skin_config_dict = get_items_skin_conf(PET_ID)
        self.cur_skin_level = 0
        self.max_level = 6
        valid_skin_list = []
        inner_skin_list = []
        self.cur_model_skin_id = None
        self.panel_hide = False
        self.interact_visible = not global_data.player.get_setting(ENABLE_PET_INTERACT_IN_BATTLE)
        self.transparent_visible = global_data.player.get_setting(ENABLE_PET_TRANSPARENT)
        self.enemy_visible = not global_data.player.get_pet_enemy_visible()
        for skin_id in six_ex.keys(self.data_dict):
            if not is_itemtype_in_serving(skin_id):
                continue
            base_skin = self.data_dict.get(str(skin_id), {}).get('base_skin', skin_id)
            if str(base_skin) != str(skin_id):
                continue
            if self.skin_config_dict.get(skin_id, {}).get('inner_skin', 0):
                inner_skin_list.append(skin_id)
            else:
                valid_skin_list.append(skin_id)

        self.skin_list = valid_skin_list
        self.skin_list = sorted(self.skin_list, key=cmp_to_key(self.cmp_function))
        self.cur_skin_idx = self.skin_list.index(str(choosen_pet)) if str(choosen_pet) in self.skin_list else 0
        return

    def destroy(self):
        self.on_finalize_panel()

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def init_panel(self):

        @self.panel.btn_hide.unique_callback()
        def OnClick(btn, touch):
            self.on_click_hide_btn(btn, touch)

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.on_click_close_btn(btn, touch)

        @self.panel.temp_btn_use.btn.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            skin_id = self.cur_skin_id
            if not skin_id:
                return
            skin_id = self.data_dict.get(str(skin_id), {}).get('base_skin', skin_id)
            real_skin_id = global_data.player.get_pet_sub_skin_choose(skin_id)
            global_data.player.set_choosen_pet(real_skin_id)

        @self.panel.temp_btn_cancel.btn.unique_callback()
        def OnClick(btn, touch):
            if not self.cur_skin_id:
                return
            global_data.player and global_data.player.reset_choosen_pet()

        @self.panel.temp_btn_go.btn.unique_callback()
        def OnClick(btn, touch):
            skin_id = self.cur_skin_id
            if not skin_id:
                return
            item_utils.jump_to_ui(skin_id)

        @self.panel.nd_mech_pet.unique_callback()
        def OnDrag(layer, touch):
            self.on_rotate_drag(layer, touch)

        self.panel.btn_free.lab_exp.SetString('+{}'.format(PET_DAILY_EXP))
        self.panel.btn_free.setVisible(not self.daily_state)

        @self.panel.btn_free.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2(content=get_text_by_id(634881, (get_lobby_item_name(self.cur_skin_id), PET_DAILY_EXP, PET_DAILY_EXP)), cancel_text=19002, on_confirm=callback)

        def callback():
            if global_data.player:
                self.panel.btn_free.SetEnable(False)
                global_data.player.get_pet_daily_reward(self.cur_skin_id)

        @self.panel.btn_setting.unique_callback()
        def OnClick(btn, touch):
            self.close()
            from logic.gutils.jump_to_ui_utils import jump_to_pve_pet
            jump_to_pve_pet()

        @self.panel.btn_skill_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(860356, 860357)

        @self.panel.btn_sub_skin_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(860432, 860433)

        self._skin_list_widget = PetItemListWidget(self, self.panel.nd_left.pnl.list_item, self.on_create_skin_item, 6)
        self._level_widget = PetLevelWidget(self.panel, self.on_click_level_btn)
        self._skill_widget = PetSkillWidget(self.panel)
        self._sub_skin_widget = PetSubSkinWidget(self, self.panel)
        self.btn_type.setVisible(False)
        self.pnl_type.setVisible(False)
        self.setting_option_list = [{'text': 83403,'visible': self.get_enemy_visible,'onclick': self.on_click_enemy}, {'text': 634909,'visible': self.get_transparent_visible,'onclick': self.on_click_transparent}, {'text': 634997,'visible': self.get_interact_visible,'onclick': self.on_click_interact}]
        self.pnl_setting.list_choice_setting.SetInitCount(len(self.setting_option_list))
        for i, item in enumerate(self.pnl_setting.list_choice_setting.GetAllItem()):
            item.lab_btn.SetString(self.setting_option_list[i]['text'])
            item.icon_checked.SetDisplayFrameByPath('', 'gui/ui_res_2/pet/icon_pet_checked.png' if self.setting_option_list[i]['visible']() else 'gui/ui_res_2/pet/icon_pet_unchecked.png')

            @item.btn.unique_callback()
            def OnClick(btn, touch, item=item, idx=i):
                self.setting_option_list[idx]['onclick'](item=item)

        self.pnl_setting.setVisible(False)

        @self.nd_mid.btn_setting.unique_callback()
        def OnClick(btn, touch):
            self.pnl_setting.setVisible(not self.pnl_setting.isVisible())
            self.panel.nd_mid.btn_setting.icon_arrow.setRotation(180 if self.pnl_setting.isVisible() else 0)

        self._skin_list_widget.update_skin_data(self.skin_list, init_index=self.cur_skin_idx)
        self.panel.icon_arrow_left.setRotation(0)

    def show(self):
        self.hide_main_ui()
        super(PetMainUI, self).show()

    def hide(self):
        super(PetMainUI, self).hide()
        self.show_main_ui()

    def do_show_panel(self):
        self.refresh_panel()
        super(PetMainUI, self).do_show_panel()

    def do_hide_panel(self):
        self.panel_hide = True
        super(PetMainUI, self).do_hide_panel()

    def on_resolution_changed(self):
        super(PetMainUI, self).on_resolution_changed()
        if self.is_in_expand_mode:
            self.panel.PlayAnimation('show')
        else:
            self.panel.PlayAnimation('hide')

    def on_finalize_panel(self):
        self._skin_list_widget.destroy()
        self._skin_list_widget = None
        self._level_widget.destroy()
        self._level_widget = None
        self._skill_widget.destroy()
        self._skill_widget = None
        self._sub_skin_widget.destroy()
        self._sub_skin_widget = None
        if not global_data.ui_mgr.get_ui('MallMainUI'):
            global_data.emgr.close_model_display_scene.emit()
            global_data.emgr.leave_current_scene.emit()
            global_data.emgr.reset_rotate_model_display.emit()
        self.show_main_ui()
        return

    def on_click_hide_btn(self, btn, touch):
        if not self.panel:
            return
        self.expand_panel()

    def expand_panel(self):
        if self.is_in_expand_mode:
            self.panel.nd_left.pnl.list_item.SetNumPerUnit(1)
            self.panel.PlayAnimation('hide')
            self.panel.icon_arrow_left.setRotation(180)
        else:
            self.panel.nd_left.pnl.list_item.SetNumPerUnit(3)
            self.panel.PlayAnimation('show')
            self.panel.icon_arrow_left.setRotation(0)
        self.update_expand_camera(need_slerp=True)
        self.is_in_expand_mode = not self.is_in_expand_mode
        self.panel.nd_left.pnl.list_item.FitViewSizeToContainerSize()

    def on_click_close_btn(self, btn, touch):
        self.close()

    def on_select_sub_skin(self, main_skin_id, sub_skin_id):
        if main_skin_id not in self.skin_list:
            return
        self._level_widget.update_skin_id(sub_skin_id)
        self._skill_widget.update_skin_id(sub_skin_id)
        self.show_model(sub_skin_id)
        self.refresh_btn()

    def on_create_skin_item(self, lst, index, item):
        valid = index < len(self.skin_list)
        if valid:
            skin_no = self.skin_list[index]
            real_skin_no = skin_no
            if global_data.player:
                real_skin_no = global_data.player.get_pet_sub_skin_choose(skin_no)
            item.img_itm.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(real_skin_no))
            item.lab_name.SetString(get_lobby_item_name(real_skin_no))
            item_fashion_no = global_data.player and global_data.player.get_choosen_pet()
            item.nd_tag.setVisible(item_fashion_no == int(real_skin_no))
            item.nd_lock.setVisible(not global_data.player.has_item_by_no(int(real_skin_no)))
            check_skin_tag(item.temp_level, real_skin_no)
            item.bar.SetDisplayFrameByPath('', get_pet_rare_degree_pic_by_item_no(real_skin_no))
            item.btn_choose.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            show_new = global_data.lobby_red_point_data.get_rp_by_no(real_skin_no)
            item.img_new.setVisible(show_new)
        else:
            item.bar.setVisible(False)

    def on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        if self.is_in_expand_mode:
            self.expand_panel()
        prev_index = self.cur_skin_idx
        self.cur_skin_idx = index
        self._sub_skin_widget.update_skin_id(self.skin_list[index])
        self.refresh_btn()
        skin_no = self.cur_skin_id
        self.max_level = self.data_dict[str(skin_no)].get('max_level', 6)
        skin_item = global_data.player.get_item_by_no(int(skin_no))
        item = self.panel.nd_left.pnl.list_item.GetItem(index)
        self.panel.btn_free.setVisible(bool(not self.daily_state and skin_item and skin_item.level < self.max_level))
        prev_item = self.panel.nd_left.pnl.list_item.GetItem(prev_index)
        if prev_item:
            prev_item.setLocalZOrder(0)
            prev_item.btn_choose.SetSelect(False)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_no)
            item.img_new.setVisible(False)
        item.setLocalZOrder(2)
        item.btn_choose.SetSelect(True)
        self._level_widget.update_skin_id(skin_no)
        self._skill_widget.update_skin_id(skin_no)

    def try_select_skin_item_by_id(self, skin_no):
        if skin_no not in self.skin_list:
            return
        if not self.skin_list:
            return
        skin_index = self.skin_list.index(skin_no)
        if not 0 <= skin_index < len(self.skin_list):
            return
        self.on_click_skin_item(skin_index)

    def cmp_function(self, skin1, skin2):
        item1 = global_data.player.get_item_by_no(int(skin1))
        item2 = global_data.player.get_item_by_no(int(skin2))
        if item1 and item2 is None:
            return -1
        else:
            if item2 and item1 is None:
                return 1
            rare_degree1 = get_item_rare_degree(skin1, 1)
            if rare_degree1 == 5:
                rare_degree1 = 6
            elif rare_degree1 == 6:
                rare_degree1 = 5
            rare_degree2 = get_item_rare_degree(skin2, 1)
            if rare_degree2 == 5:
                rare_degree2 = 6
            else:
                if rare_degree2 == 6:
                    rare_degree2 = 5
                if rare_degree1 > rare_degree2:
                    return -1
                if rare_degree2 > rare_degree1:
                    return 1
                if int(skin1) > int(skin2):
                    return -1
                if int(skin1) < int(skin2):
                    return 1
            return 0
            return

    def on_click_level_btn(self, level):
        skin_id = self.cur_skin_id
        if not skin_id:
            return
        else:
            skin_config = self.data_dict.get(str(skin_id), {})
            anim_name = self.skin_config_dict[str(skin_id)].get('spec_show_anim', {}).get(str(level + 1), None)
            if anim_name is None and level > 0:
                for i in range(1, 4):
                    anim_info = skin_config.get('interact_anim{}'.format(i), {})
                    if not anim_info:
                        break
                    unlock_level = anim_info[2].get('level', 1)
                    if level + 1 == unlock_level:
                        anim_name = anim_info[0]
                        break

            if self.cur_model_skin_id == skin_id and self.cur_skin_level == level + 1:
                if anim_name:
                    anim_name = self.skin_config_dict[str(skin_id)].get('anim_replace', {}).get(anim_name, anim_name)
                    global_data.emgr.change_model_display_anim_directly.emit(anim_name, is_back_to_end_show_anim=True, anim_arg=[0])
                    self.panel.stopActionByTag(SPEC_ANIM_TAG)
                return
            if self.cur_skin_level > 0:
                item = self.panel.list_tab.GetItem(self.cur_skin_level - 1)
                if item:
                    item.btn_unlock.SetSelect(False)
                    item.btn_lock.SetSelect(False)
            self.cur_skin_level = level + 1
            item = self.panel.list_tab.GetItem(level)
            if item:
                item.btn_unlock.SetSelect(True)
                item.btn_lock.SetSelect(True)
                self.show_model(skin_id, spec_anim=anim_name)
            return

    def show_model(self, skin_no, spec_anim=None):
        skin_conf = self.data_dict.get(str(skin_no), {})
        if not skin_conf:
            return
        else:
            anim_replace = self.skin_config_dict[str(skin_no)].get('anim_replace', {})
            replaced_spec_anim = skin_conf['idle_anim2'][0] if spec_anim is None else spec_anim
            self.cur_special_anim_name = replaced_spec_anim = anim_replace.get(replaced_spec_anim, replaced_spec_anim)
            self.special_anim_inter = self.skin_config_dict[str(skin_no)].get('anim_inter', 5)
            self.panel.stopActionByTag(SPEC_ANIM_TAG)
            prev_skin_id = self.cur_model_skin_id
            self.cur_model_skin_id = skin_no
            model_data = lobby_model_display_utils.get_lobby_model_data(skin_no, pet_level=self.cur_skin_level)
            model_data[0]['can_rotate_on_show'] = True
            model_data[0]['off_position'] = PET_OFF_POS_SHOW if self.is_in_expand_mode else PET_OFF_POS_HIDE
            if prev_skin_id == skin_no:
                model_data[0]['show_anim'] = '' if spec_anim is None else replaced_spec_anim
            idle_anim = skin_conf['idle_anim'][0]
            model_data[0]['end_anim'] = anim_replace.get(idle_anim, idle_anim)
            model_data[0]['add_sub_mesh_to_shadow'] = True
            global_data.emgr.change_model_display_scene_item.emit(model_data)
            return

    def model_end_show_anim(self, *args):
        if self.panel_hide:
            return
        self.panel.SetTimeOut(self.special_anim_inter, Functor(global_data.emgr.change_model_display_anim_directly.emit, self.cur_special_anim_name, is_back_to_end_show_anim=True, anim_arg=[0]), SPEC_ANIM_TAG)

    def update_expand_camera(self, need_slerp=False):
        model_offset = self.get_off_position()
        global_data.emgr.change_model_display_off_position.emit(model_offset, is_slerp=need_slerp)
        self._model_offset = math3d.vector(*model_offset)

    def get_off_position(self, off=True):
        if self.is_in_expand_mode:
            off_position = [
             -5, 0, 0]
        else:
            off_position = [
             -20, 0, 0]
        return off_position

    def on_click_interact(self, item):
        self.interact_visible = not self.interact_visible
        item.icon_checked.SetDisplayFrameByPath('', 'gui/ui_res_2/pet/icon_pet_checked.png' if self.interact_visible else 'gui/ui_res_2/pet/icon_pet_unchecked.png')
        global_data.player.write_setting(ENABLE_PET_INTERACT_IN_BATTLE, not self.interact_visible, True)

    def get_interact_visible(self):
        return self.interact_visible

    def on_click_transparent(self, item):
        self.transparent_visible = not self.transparent_visible
        global_data.player.write_setting(ENABLE_PET_TRANSPARENT, self.transparent_visible, True)
        item.icon_checked.SetDisplayFrameByPath('', 'gui/ui_res_2/pet/icon_pet_checked.png' if self.transparent_visible else 'gui/ui_res_2/pet/icon_pet_unchecked.png')

    def get_transparent_visible(self):
        return self.transparent_visible

    def on_click_enemy(self, item):
        self.enemy_visible = not self.enemy_visible
        global_data.player.set_pet_enemy_visible(not self.enemy_visible)
        item.icon_checked.SetDisplayFrameByPath('', 'gui/ui_res_2/pet/icon_pet_checked.png' if self.enemy_visible else 'gui/ui_res_2/pet/icon_pet_unchecked.png')

    def get_enemy_visible(self):
        return self.enemy_visible

    def on_pet_daily_state_changed(self, state):
        if self.daily_state ^ state:
            self.daily_state = state
            self.panel.btn_free.SetEnable(True)
            self.panel.btn_free.setVisible(not state)

    def on_pet_choosen_changed(self, choosen_pet_id):
        self.refresh_btn()
        for i, pet_id in enumerate(self.skin_list):
            self.panel.nd_left.pnl.list_item.GetItem(i).nd_tag.setVisible(int(pet_id) == choosen_pet_id)

    def on_pet_sub_skin_changed(self, base_skin, sub_skin):
        if base_skin not in self.skin_list:
            return
        else:
            index = self.skin_list.index(base_skin)
            item = self.nd_left.pnl.list_item.GetItem(index)
            self.on_create_skin_item(None, index, item)
            return

    def refresh_btn(self):
        skin_id = self.cur_skin_id
        base_skin_id = self.data_dict.get(str(skin_id), {}).get('base_skin', skin_id)
        item_can_use, _ = mall_utils.item_can_use_by_item_no(skin_id)
        cur_pet_id = global_data.player and global_data.player.get_choosen_pet()
        base_pet_id = self.data_dict.get(str(cur_pet_id), {}).get('base_skin', cur_pet_id)
        is_using = str(base_pet_id) == str(base_skin_id)
        self.panel.temp_btn_use.btn.setVisible(item_can_use and not is_using)
        self.temp_btn_cancel.setVisible(is_using)
        can_jump = not item_can_use
        jump_txt = item_utils.get_item_access(skin_id)
        if self.panel.temp_btn_go:
            enable = item_utils.can_jump_to_ui(skin_id) and can_jump
            self.temp_btn_go.btn.SetEnable(enable)
            self.temp_btn_go.btn.SetText(get_text_by_id(2222 if enable else 80828))
            self.temp_btn_go.setVisible(can_jump and bool(jump_txt))
            jump_txt = jump_txt if enable else jump_txt + get_text_by_id(635079)
            self.panel.lab_get_method.SetString(jump_txt or '')

    def refresh_panel(self):
        if self.panel_hide:
            self.init_scene()
            self.show_model(self.cur_skin_id)
            self.panel_hide = False
            for index, item in enumerate(self.panel.nd_left.pnl.list_item.GetAllItem()):
                if index >= len(self.skin_list):
                    break
                skin_no = self.skin_list[index]
                item_fashion_no = global_data.player and global_data.player.get_choosen_pet()
                item.nd_tag.setVisible(item_fashion_no == int(skin_no))
                item.nd_lock.setVisible(not global_data.player.has_item_by_no(int(skin_no)))

    def on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)