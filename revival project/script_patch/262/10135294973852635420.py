# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinImproveExStepWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from common.cfg import confmgr
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils import mall_utils
from logic.gutils import mecha_skin_utils
from logic.gutils.template_utils import init_price_template

class SkinImproveExStepWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel):
        self.global_events = {}
        super(SkinImproveExStepWidget, self).__init__(parent_ui, panel)
        self._parent_ui = parent_ui
        self._previewing_idx = None
        self._cur_clothing_id = None
        return

    def set_clothing_id(self, clothing_id):
        old_clothing_id = self._cur_clothing_id
        self._cur_clothing_id = clothing_id
        self.update_ex_step_list()
        if old_clothing_id != self._cur_clothing_id:
            self.check_shiny_weapon_equip_status()

    def update_ex_step_list(self):
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(self._cur_clothing_id)
        base_ex_weapon_list = self.get_ex_weapon_list(base_skin_id)
        self.panel.list_item.SetInitCount(len(base_ex_weapon_list))
        for idx in range(len(base_ex_weapon_list)):
            self.init_ex_step_widget(idx, base_ex_weapon_list)

        owned_items = [ w_id for w_id in base_ex_weapon_list if global_data.player.get_item_by_no(w_id) ]
        prog = float(len(owned_items)) / len(base_ex_weapon_list) * 100
        self.panel.bar_prog.prog.SetPercentage(prog)
        if prog <= 0:
            self.panel.bar_prog.prog.setVisible(False)
        else:
            self.panel.bar_prog.prog.setVisible(True)
            tail = self.panel.bar_prog.prog.GetTail()
            if tail:
                tail.PlayAnimation('loop')
        self._init_shiny_weapon_status()

    def init_ex_step_widget(self, idx, base_ex_weapon_list):
        from logic.gcommon.common_const.mecha_const import EX_REFINE_UPGRADE_TYPE_COLOR, EX_REFINE_UPGRADE_TYPE_SFX, EX_REFINE_UPGRADE_TYPE_FINAL
        ui_item = self.panel.list_item.GetItem(idx)
        if ui_item:
            is_own = bool(global_data.player.get_item_by_no(base_ex_weapon_list[idx]))
            ui_item.nd_lock.setVisible(not is_own)
            ui_item.nd_got.setVisible(is_own)
            ui_item.btn_choose.EnableCustomState(True)
            lab_name_list = [get_text_by_id(83596),
             get_text_by_id(83597),
             get_text_by_id(83598)]
            ui_item.lab_name.SetString(lab_name_list[idx])

            def get_is_can_buy():
                if idx > 0:
                    pre_ex_weapon = base_ex_weapon_list[idx - 1]
                    pre_is_own = bool(global_data.player.get_item_by_no(pre_ex_weapon))
                    if idx == EX_REFINE_UPGRADE_TYPE_FINAL:
                        _skin_id_lst = mecha_skin_utils.get_mecha_ss_skin_lst(self._cur_clothing_id)
                        is_own_last_cid = bool(global_data.player.get_item_by_no(_skin_id_lst[-1]))
                        if is_own_last_cid and pre_is_own:
                            return (True, '')
                        else:
                            return (
                             False, get_text_by_id(83601))

                    elif not pre_is_own:
                        return (False, get_text_by_id(83599))
                    else:
                        return (
                         True, '')

                else:
                    base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(self._cur_clothing_id)
                    is_own_base_cid = bool(global_data.player.get_item_by_no(base_skin_id))
                    if is_own_base_cid:
                        return (True, '')
                    return (
                     False, get_text_by_id(83600))

            if not is_own:
                self._init_price(self._cur_clothing_id, ui_item.temp_cost)
                is_can_buy, tips = get_is_can_buy()
                ui_item.temp_btn_use.btn_common.SetEnable(is_can_buy)
                ui_item.temp_btn_use.btn_common.SetText('')
                ui_item.temp_btn_use.lab_tips.SetString(tips)
                ui_item.temp_btn_use.temp_cost.setVisible(True)
            else:
                ui_item.temp_btn_use.lab_tips.SetString('')
                ui_item.temp_btn_use.btn_common.SetEnable(False)
                ui_item.temp_btn_use.btn_common.SetText('')
                ui_item.temp_btn_use.temp_cost.setVisible(False)

            @ui_item.btn_choose.callback()
            def OnClick(btn, touch):
                if not self.parent:
                    return
                if not global_data.player:
                    return
                highest_own_index = 0
                for ex_w_indx in range(len(base_ex_weapon_list) - 1, -1, -1):
                    if global_data.player.get_item_by_no(base_ex_weapon_list[ex_w_indx]):
                        highest_own_index = ex_w_indx
                        break

                highest_own_rarity = self.index_to_ex_rarity(highest_own_index)
                _, base_weapon_sfx_ex_rarity = mecha_skin_utils.get_base_skin_equiped_ex_rarity(self._cur_clothing_id)
                old_ex_rarity = base_weapon_sfx_ex_rarity
                if is_own:
                    _is_previewing = self.parent.get_is_preview()
                    if _is_previewing:
                        self.try_preview(self._previewing_idx)
                        if highest_own_rarity and highest_own_rarity > 0:
                            self.parent.try_equip_shiny(highest_own_rarity)
                            self.set_weapon_shiny_index_selected(-1)
                    else:
                        ex_rarity = highest_own_rarity
                        if old_ex_rarity != ex_rarity:
                            _is_equip_shiny = True if ex_rarity and ex_rarity > 0 else False
                        else:
                            _is_equip_shiny = False
                        self.parent.try_equip_shiny(highest_own_rarity)
                        if _is_equip_shiny:
                            self.set_weapon_shiny_index_selected(highest_own_index)
                        else:
                            self.set_weapon_shiny_index_selected(-1)
                else:
                    self.try_preview(max(idx, highest_own_index))
                    _is_previewing = self.parent.get_is_preview()
                    if _is_previewing:
                        if old_ex_rarity != highest_own_rarity:
                            self.parent.try_equip_shiny(highest_own_rarity)
                    elif highest_own_rarity and highest_own_rarity > 0:
                        self.parent.try_equip_shiny(highest_own_rarity)

            @ui_item.temp_btn_use.btn_common.callback()
            def OnClick(btn, touch):
                if not self.parent:
                    return
                if not global_data.player:
                    return
                base_weapon_sfx_id = base_ex_weapon_list[idx]
                is_own = bool(global_data.player.get_item_by_no(base_weapon_sfx_id))
                if is_own:
                    return
                base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(self._cur_clothing_id)
                skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(base_skin_id))
                required_item, required_num = skin_cfg.get('refine_ex_required_item')
                if global_data.player and mall_utils.check_item_money(required_item, required_num, pay_tip=False):
                    base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(self._cur_clothing_id)
                    if idx in (0, 1):
                        global_data.player.call_server_method('try_refined_upgrade_mecha_fashion', (base_skin_id, EX_REFINE_UPGRADE_TYPE_SFX, base_weapon_sfx_id))
                    else:
                        global_data.player.call_server_method('try_refined_upgrade_mecha_fashion', (base_skin_id, EX_REFINE_UPGRADE_TYPE_FINAL, base_weapon_sfx_id))
                else:
                    self.parent._jump_to_lottery(required_item, required_num)

    def _init_price(self, c_id, node):
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(c_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(base_skin_id))
        required_item, required_num = skin_cfg.get('refine_ex_required_item')
        price_info = {'original_price': required_num,
           'discount_price': None,
           'goods_payment': mall_utils.get_item_money_type(required_item)
           }
        init_price_template(price_info, node, color=['#SS', '#SR', '#BC'])
        return (
         required_item, required_num)

    def try_preview(self, idx):
        self._parent_ui.on_ex_improve_preview()
        _is_previewing = self.parent.get_is_preview()
        if self._previewing_idx == idx and _is_previewing:
            self.set_weapon_shiny_index_selected(-1)
            self.parent.set_is_preview(False)
            preview_id = self.parent.get_preview_id()
            ex_weapon_list = self.get_ex_weapon_list(preview_id)
            shiny_id = ex_weapon_list[idx]
            global_data.emgr.show_shiny_weapon_sfx.emit(preview_id, None, shiny_id)
            self.parent.set_parent_shiny_id(None)
            self._previewing_idx = None
        else:
            self.parent.set_is_preview(True)
            self.set_weapon_shiny_index_selected(idx)
            preview_id = self.parent.get_preview_id()
            ex_weapon_list = self.get_ex_weapon_list(preview_id)
            shiny_id = ex_weapon_list[idx]
            if shiny_id:
                global_data.emgr.show_shiny_weapon_sfx.emit(preview_id, shiny_id, self.parent.get_parent_shiny_id())
                self.parent.set_parent_shiny_id(shiny_id)
            self._previewing_idx = idx
        return

    def get_ex_weapon_list(self, c_id):
        ex_step_info = mecha_skin_utils.get_mecha_shiny_weapon_info(c_id)
        ex_weapon_list = sorted(six_ex.keys(ex_step_info), key=lambda x: ex_step_info[x])
        ex_weapon_list = [ int(weapon) for weapon in ex_weapon_list ]
        return ex_weapon_list

    def get_preview_shiny_id(self, preview_id):
        if self._previewing_idx is not None:
            ex_weapon_list = self.get_ex_weapon_list(preview_id)
            shiny_id = ex_weapon_list[self._previewing_idx]
            return shiny_id
        else:
            return 0
            return

    def _init_shiny_weapon_status(self):
        base_weapon_sfx, ex_rarity = self.get_base_skin_ex_rarity()
        if self.parent.get_is_preview():
            parent_shiny_id = self.parent.get_parent_shiny_id() if 1 else 0
            preview_rarity = parent_shiny_id or ex_rarity
        else:
            _skin_id_lst = mecha_skin_utils.get_mecha_ss_skin_lst(self._cur_clothing_id)
            preview_rarity = mecha_skin_utils.get_shiny_rarity_with_same_group_skin(self._cur_clothing_id, parent_shiny_id)
        if preview_rarity >= 1:
            index = self.ex_rarity_to_index(preview_rarity)
            self.set_weapon_shiny_index_selected(index)
        else:
            self.set_weapon_shiny_index_selected(-1)
        ex_weapon_list = self.get_ex_weapon_list(self.parent.get_preview_id())
        for idx, ex_weapon in enumerate(ex_weapon_list):
            ui_item = self.panel.list_item.GetItem(idx)
            pic = 'gui/ui_res_2/mech_display/img_ex_%d.png' % ex_weapon
            ui_item.img_item.SetDisplayFrameByPath('', pic)

    def set_weapon_shiny_index_selected(self, index):
        for item_idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            ui_item.btn_choose.SetSelect(True if item_idx <= index else False)

    def index_to_ex_rarity(self, index):
        return index + 1

    def ex_rarity_to_index(self, ex_rarity):
        return ex_rarity - 1

    def get_base_skin_ex_rarity(self):
        return mecha_skin_utils.get_base_skin_equiped_ex_rarity(self._cur_clothing_id)

    def check_shiny_weapon_equip_status(self):
        _skin_id_lst = mecha_skin_utils.get_mecha_ss_skin_lst(self._cur_clothing_id)
        base_weapon_sfx, base_ex_rarity = self.get_base_skin_ex_rarity()
        current_equip_dict = {}
        skin_id_own_dict = {}
        for skin_id in _skin_id_lst:
            cur_skin_info = global_data.player.get_item_by_no(skin_id)
            skin_id_own_dict[skin_id] = True if cur_skin_info else False
            if cur_skin_info:
                current_equip_dict[skin_id] = cur_skin_info.get_weapon_sfx() if 1 else None

        need_update = False
        for skin_id in _skin_id_lst:
            if skin_id_own_dict.get(skin_id):
                skin_weapon_sfx = current_equip_dict[skin_id]
                if skin_weapon_sfx:
                    skin_ex_rarity = mecha_skin_utils.get_mecha_shiny_weapon_id_rarity(skin_id, skin_weapon_sfx)
                else:
                    skin_ex_rarity = -1
                if skin_ex_rarity != base_ex_rarity:
                    need_update = True
                    break

        if need_update:
            need_equip = bool(base_weapon_sfx)
            equip_info_dict = self.parent.get_equip_shiny_dict_helper(need_equip, base_ex_rarity)
            global_data.player.try_equip_mecha_shiny_weapon(equip_info_dict)
        return

    def on_role_fashion_changed(self):
        if not self.parent.get_is_preview():
            self._previewing_idx = None
        self.update_ex_step_list()
        return