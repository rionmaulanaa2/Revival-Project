# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseMechaModuleUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gutils import template_utils
from logic.gcommon.common_const import mecha_const
from logic.gutils.mecha_module_utils import init_module_temp_item, get_module_card_name_and_desc, get_module_item_bar_pic
from logic.gcommon import time_utility as tutil
from common.framework import Functor
from common.const import uiconst

class ExerciseMechaModuleUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_module_set'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_module_preview.OnClick': 'on_click_preview_to_config',
       'btn_close.OnClick': 'on_click_config_to_preview',
       'btn_delete.OnClick': 'on_click_delete_all_module'
       }
    HOT_KEY_FUNC_MAP = {'exercise_mecha_module': 'on_switch_preview_and_config_PC'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'exercise_mecha_module': {'node': 'btn_module_preview.temp_pc'},'exercise_mecha_module_close': {'node': 'nd_module_set.temp_pc_1'}}
    selected_slot_idx = -1
    selected_item_idx = [-2, -1, -1, -1, -1]
    selected_lv = [-2, 3, 3, 3, 3]
    SLOT_NAME_TEXT_ID = {mecha_const.MODULE_ATTACK_SLOT: 18197,mecha_const.MODULE_DEFEND_SLOT: 18198,
       mecha_const.MODULE_MOVE_SLOT: 18199,
       mecha_const.SP_MODULE_SLOT: 18200
       }
    SLOT_LV_TO_ITEM = (
     (-1, -1, -1, -1),
     (-1, 9912, 9913, 9908),
     (-1, 9914, 9915, 9909),
     (-1, 9916, 9917, 9910),
     (-1, 9911, 9911, 9911))
    TIP_ICON_PATH = {'empty_tip': 'gui/ui_res_2/battle_train/icon_add.png','change_tip': 'gui/ui_res_2/battle_train/icon_change.png'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseMechaModuleUI, self).on_init_panel()
        self.btn_group_lv = (None, self.panel.btn_green, self.panel.btn_blue, self.panel.btn_purple)
        self._module_slot_to_ui_item_dict = {}
        self.process_event(True)
        self._sp_module_last_switch_time = None
        self._pc_switch_tag = True
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted,
           'observer_module_changed_event': self.init_module_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self, *args):
        if global_data.cam_lplayer:
            self.init_module_ui()
        self.on_ctrl_target_changed()

    def switch_to_mecha(self):
        self.on_click_config_to_preview()
        super(ExerciseMechaModuleUI, self).switch_to_mecha()
        ui = global_data.ui_mgr.get_ui('ExerciseWeaponListUI')
        if ui:
            ui.close()
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count('ExerciseWeaponConfUI')

    def switch_to_non_mecha(self):
        self.panel.btn_module_preview.setVisible(False)
        self.panel.nd_module_set.setVisible(False)
        super(ExerciseMechaModuleUI, self).switch_to_non_mecha()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count('ExerciseMechaModuleUI')

    def on_click_preview_to_config(self, *args, **kwargs):
        if not self._in_mecha_state:
            return
        self.panel.btn_module_preview.setVisible(False)
        self.panel.nd_module_set.setVisible(True)
        self.panel.img_list.setVisible(False)
        self.selected_slot_idx = -1
        self.switch_selected_btn_slot()
        self._pc_switch_tag = False

    def on_click_config_to_preview(self, *args, **kwargs):
        if not self._in_mecha_state:
            return
        self.panel.nd_module_set.setVisible(False)
        self.panel.btn_module_preview.setVisible(True)
        self._pc_switch_tag = True

    def on_switch_preview_and_config_PC(self, *args, **kwargs):
        if not self._in_mecha_state:
            return
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        if self._pc_switch_tag:
            trigger_ui_btn_event('ExerciseMechaModuleUI', 'btn_module_preview', need_check_vis=True)
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
        else:
            trigger_ui_btn_event('ExerciseMechaModuleUI', 'btn_close', need_check_vis=True)
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def init_module_ui(self):
        self.init_part_preview()
        self.init_part_detail()

    def init_part_preview(self):
        if not global_data.cam_lplayer:
            return
        max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
        self.panel.list_module_preview.SetInitCount(max_module_num)
        self.update_part_preview()

    def update_part_preview(self):
        if not global_data.cam_lplayer:
            return None
        else:
            self._module_slot_to_ui_item_dict = {}
            cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
            max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
            for show_slot in range(1, max_module_num + 1):
                item_idx = show_slot - 1
                ui_item = self.panel.list_module_preview.GetItem(item_idx)
                if ui_item:
                    card_id, item_id = cur_module_config.get(show_slot, (None, None))
                    _, card_lv = global_data.cam_lplayer.ev_g_module_item_slot_lv(item_id)
                    self.init_module_item(ui_item, card_id, show_slot, card_lv)
                    self._module_slot_to_ui_item_dict[show_slot] = ui_item

            return None

    def init_part_detail(self):
        if not global_data.cam_lplayer:
            return
        max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
        list_module = self.panel.nd_module_set.img_panel.list_module
        list_module.SetInitCount(max_module_num)
        for slot in range(1, max_module_num + 1):
            index = slot - 1
            if slot == mecha_const.SP_MODULE_SLOT:
                is_sp = True if 1 else False
                ui_item = list_module.GetItem(index)
                ui_item.btn_module.SetSelect(False)

                @ui_item.btn_module.callback()
                def OnClick(_btn, _touch, _idx=index, _slot=slot, _is_sp=is_sp):
                    self.on_click_show_slot_item(_idx, _slot, _is_sp)

        self.update_part_detail()
        self.switch_selected_btn_slot()

    def update_part_detail(self):
        if not global_data.cam_lplayer:
            return
        else:
            cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
            max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
            ty_list = [mecha_const.MODULE_ATTACK_SLOT, mecha_const.MODULE_DEFEND_SLOT, mecha_const.MODULE_MOVE_SLOT, mecha_const.SP_MODULE_SLOT]
            for show_slot in range(1, max_module_num + 1):
                item_idx = show_slot - 1
                ui_item = self.panel.nd_module_set.img_panel.list_module.GetItem(item_idx)
                if ui_item:
                    card_id, item_id = cur_module_config.get(show_slot, (None, None))
                    _, card_lv = global_data.cam_lplayer.ev_g_module_item_slot_lv(item_id)
                    self.set_name_and_details(ui_item.lab_module, None, card_id)
                    slot = ty_list[item_idx]
                    self.init_module_icon(ui_item, slot, card_id, card_lv, 'small_')
                    ui_item.lab_type.SetString(self.SLOT_NAME_TEXT_ID.get(slot, 18197))
                    tip_icon_path = self.TIP_ICON_PATH.get('empty_tip') if card_id is None else self.TIP_ICON_PATH.get('change_tip')
                    ui_item.img_set.SetDisplayFrameByPath('', tip_icon_path)

            return

    def init_module_item(self, ui_item, card_id, show_slot, card_lv):
        self.init_module_temp_item(ui_item, show_slot, card_id, card_lv)
        ui_item.img_module.setVisible(False)

    def init_module_temp_item(self, ui_temp_item, show_slot, card_id, card_level):
        init_module_temp_item(ui_temp_item, show_slot, card_id, card_level, 'small_')
        if card_level:
            ui_temp_item.img_skill.setVisible(True)

    def init_module_icon(self, ui_item, slot, card_id, card_lv, prefix=''):
        ui_item.img_frame.SetDisplayFrameByPath('', get_module_item_bar_pic(slot, card_lv, prefix))
        mecha_talent_path = template_utils.get_module_show_slot_pic(slot, card_id, card_lv)
        ui_item.img_module.SetDisplayFrameByPath('', mecha_talent_path)

    def init_module_icon_with_lv(self, ui_item, slot, card_id, card_lv, prefix=''):
        ui_item.img_frame.SetDisplayFrameByPath('', get_module_item_bar_pic(slot, card_lv if card_lv is not None else self.selected_lv[slot], prefix))
        mecha_talent_path = template_utils.get_module_show_slot_pic(slot, card_id, card_lv if card_lv is not None else self.selected_lv[slot])
        ui_item.img_module.SetDisplayFrameByPath('', mecha_talent_path)
        return

    def init_module_sp_icon(self, ui_item, slot, card_id, prefix=''):
        card_lv = 1
        ui_item.img_frame.SetDisplayFrameByPath('', get_module_item_bar_pic(slot, card_lv, prefix))
        mecha_talent_path = template_utils.get_module_show_slot_pic(slot, card_id, card_lv)
        ui_item.img_module.SetDisplayFrameByPath('', mecha_talent_path)

    def set_name_and_details(self, name_nd, details_nd, card_id):
        if card_id is None or card_id == 0:
            name_nd.SetString(5066)
            return
        else:
            card_name_desc, card_effect_desc = get_module_card_name_and_desc(card_id, None)
            name_nd.SetString(card_name_desc)
            if details_nd:
                details_nd.SetString(card_effect_desc)
            return

    def switch_selected_btn_slot(self):
        list_module = self.panel.nd_module_set.img_panel.list_module
        for idx in range(0, mecha_const.MODULE_MAX_SLOT_COUNT):
            if idx == self.selected_slot_idx:
                list_module.GetItem(idx).btn_module.SetSelect(True)
            else:
                list_module.GetItem(idx).btn_module.SetSelect(False)

    def on_click_show_slot_item(self, select_idx, slot, is_sp):
        if not self._in_mecha_state:
            return None
        else:
            img_list = self.panel.nd_module_set.img_list
            img_list.nd_screen.setVisible(not is_sp)
            if img_list.isVisible() and select_idx == self.selected_slot_idx:
                img_list.setVisible(False)
                self.panel.nd_module_set.img_panel.list_module.GetItem(select_idx).btn_module.SetSelect(False)
                self.selected_slot_idx = -1
                self.switch_selected_btn_slot()
                return None
            cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
            cur_card_id, cur_item_id = cur_module_config.get(slot, (None, None))
            _, cur_card_lv = global_data.cam_lplayer.ev_g_module_item_slot_lv(cur_item_id)
            img_list.setVisible(True)
            cur_mech_id = global_data.mecha.logic.share_data.ref_mecha_id
            all_slot_choices = global_data.player.get_module_card_choices_config(cur_mech_id)
            slot_choices = all_slot_choices.get(slot, [])
            img_list.list_module.SetInitCount(len(slot_choices))
            all_item = img_list.list_module.GetAllItem()
            for idx, card_id in enumerate(slot_choices):
                ui_item = all_item[idx]
                self.set_name_and_details(ui_item.lab_module, ui_item.img_bar.lab_describe, card_id)
                if is_sp:
                    self.init_module_sp_icon(ui_item, slot, card_id, 'small_')
                else:
                    self.init_module_icon_with_lv(ui_item, slot, card_id, cur_card_lv, 'small_')
                if card_id == cur_card_id:
                    ui_item.btn_module.SetSelect(True)
                    self.selected_item_idx[slot] = idx
                    self.selected_lv[slot] = cur_card_lv
                else:
                    ui_item.btn_module.SetSelect(False)

                @ui_item.btn_module.callback()
                def OnClick(_btn, _touch, _idx=idx, _slot=slot):
                    self.on_click_switch_slot_item(_idx, _slot)

            self.add_btn_group_lv_callback(slot)
            self.selected_slot_idx = select_idx
            self.switch_selected_btn_slot()
            self.switch_selected_btn_item(slot)
            self.switch_selected_btn_lv(slot)
            return None

    def switch_selected_btn_item(self, slot):
        list_module = self.panel.nd_module_set.img_list.list_module
        for idx in range(0, list_module.GetItemCount()):
            if idx == self.selected_item_idx[slot]:
                list_module.GetItem(idx).btn_module.SetSelect(True)
                list_module.GetItem(idx).img_tick.setVisible(True)
            else:
                list_module.GetItem(idx).btn_module.SetSelect(False)
                list_module.GetItem(idx).img_tick.setVisible(False)

    def on_click_switch_slot_item(self, select_idx, slot):
        if not self._in_mecha_state:
            return
        if select_idx == self.selected_item_idx[slot]:
            return
        if slot == mecha_const.SP_MODULE_SLOT and self._sp_module_last_switch_time and tutil.get_server_time() - self._sp_module_last_switch_time < mecha_const.EXERCISE_SP_MODULE_SWITCH_CD:
            global_data.game_mgr.show_tip(get_text_by_id(18233).format(mecha_const.EXERCISE_SP_MODULE_SWITCH_CD))
            return
        self.selected_item_idx[slot] = select_idx
        self.switch_selected_btn_item(slot)
        cur_mech_id = global_data.mecha.logic.share_data.ref_mecha_id
        all_slot_choices = global_data.player.get_module_card_choices_config(cur_mech_id)
        slot_choices = all_slot_choices.get(slot, [])
        new_card_id = slot_choices[select_idx]
        modules_dict = self.create_modules_dict_with_card(slot, new_card_id)
        self._send_module_conf(modules_dict)
        if slot == mecha_const.SP_MODULE_SLOT:
            self._sp_module_last_switch_time = tutil.get_server_time()

    def switch_selected_btn_lv(self, slot):
        for idx in range(1, len(self.btn_group_lv)):
            self.btn_group_lv[idx].img_tick.setVisible(True if idx == self.selected_lv[slot] else False)

    def add_btn_group_lv_callback(self, slot):
        for idx, btn in enumerate(self.btn_group_lv):
            if not btn:
                continue
            btn.BindMethod('OnClick', Functor(self.on_click_switch_slot_lv, idx, slot))

    def on_click_switch_slot_lv(self, select_lv, slot, *args):
        if not self._in_mecha_state:
            return
        if select_lv == self.selected_lv[slot]:
            return
        self.selected_lv[slot] = select_lv
        self.switch_selected_btn_lv(slot)
        img_list = self.panel.nd_module_set.img_list
        cur_mech_id = global_data.mecha.logic.share_data.ref_mecha_id
        all_slot_choices = global_data.player.get_module_card_choices_config(cur_mech_id)
        slot_choices = all_slot_choices.get(slot, [])
        all_item = img_list.list_module.GetAllItem()
        for idx, card_id in enumerate(slot_choices):
            ui_item = all_item[idx]
            self.init_module_icon_with_lv(ui_item, slot, card_id, select_lv, 'small_')

        if self.selected_item_idx[slot] == -1:
            return
        modules_dict = self.create_modules_dict_with_lv(slot, self.SLOT_LV_TO_ITEM[slot][select_lv])
        self._send_module_conf(modules_dict)

    def create_modules_dict_with_card(self, slot, new_card_id):
        modules_dict = {}
        cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
        for slot_idx in cur_module_config:
            cur_card_id, cur_item_id = cur_module_config.get(slot_idx, (None, None))
            dict_item = {'card_id': cur_card_id,'module_id': cur_item_id}
            modules_dict[slot_idx] = dict_item

        if slot in modules_dict:
            modules_dict[slot]['card_id'] = new_card_id
        else:
            modules_dict[slot] = {'card_id': new_card_id,'module_id': self.SLOT_LV_TO_ITEM[slot][self.selected_lv[slot]]}
        return modules_dict

    def create_modules_dict_with_lv(self, slot, new_item_id):
        modules_dict = {}
        cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
        for slot_idx in cur_module_config:
            cur_card_id, cur_item_id = cur_module_config.get(slot_idx, (None, None))
            dict_item = {'card_id': cur_card_id,'module_id': cur_item_id}
            modules_dict[slot_idx] = dict_item

        if slot not in modules_dict:
            cur_mech_id = global_data.mecha.logic.share_data.ref_mecha_id
            all_slot_choices = global_data.player.get_module_card_choices_config(cur_mech_id)
            slot_choices = all_slot_choices.get(slot, [])
            if self.selected_item_idx[slot] != -1:
                card_id = slot_choices[self.selected_item_idx[slot]]
            else:
                card_id = slot_choices[0]
            modules_dict[slot] = {'card_id': card_id,'module_id': None}
        modules_dict[slot]['module_id'] = new_item_id
        return modules_dict

    def on_click_delete_all_module(self, *args):
        self.selected_slot_idx = -1
        for idx in range(1, mecha_const.MODULE_MAX_SLOT_COUNT + 1):
            self.selected_item_idx[idx] = -1
            self.selected_lv[idx] = 3

        self.switch_selected_btn_slot()
        self.switch_selected_btn_item(0)
        self.switch_selected_btn_lv(0)
        self.panel.img_list.setVisible(False)
        modules_dict = {}
        self._send_module_conf(modules_dict)

    def _send_module_conf(self, modules_dict):
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_CALL_SYNC_METHOD', 'update_mecha_module_config', (modules_dict,))
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self._sp_module_last_switch_time = None
        self._pc_switch_tag = True
        super(ExerciseMechaModuleUI, self).on_finalize_panel()
        return