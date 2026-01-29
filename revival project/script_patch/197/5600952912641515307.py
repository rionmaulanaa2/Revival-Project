# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/DrugUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from logic.client.const import game_mode_const
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER, UI_VKB_CUSTOM
from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE, ST_SKATE
from logic.gcommon.common_const.ui_operation_const import OPE_POSTURE_KEY
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.cdata import mecha_status_config
from data.item_use_var import USABLE_ID_LIST, MECHA_USABLE_ID_LIST
from logic.gutils import item_utils
import time
import cc
from logic.gutils.hot_key_utils import set_hot_key_common_tip
from data.hot_key_def import USE_CUR_ITEM
from logic.gcommon.item.item_utility import is_neutral_shop_candy
from data import hot_key_def
from common.utils.cocos_utils import ccp
import game
import game3d
from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE
from logic.gcommon import const
from logic.gutils.new_template_utils import is_human_mecha_item
import logic.gcommon.time_utility as tutil
import math
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.time_utility import get_server_time

class DrugUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_medicine_more'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'bg_layer.OnBegin': 'on_begin_bg_layer'
       }
    IS_PLAY_OPEN_SOUND = False
    UI_VKB_TYPE = UI_VKB_CUSTOM
    NORMAL_LIST_HOT_KEY_FUNC_NAME = [ 'use_drug_%d' % (i + 1) for i in range(10) ]
    OTHER_LIST_HOT_KEY_FUNC_NAME = [ 'use_drug_%d' % (i + 10) for i in range(4) ]
    DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG = 31415926
    DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG = 31415927
    HOT_KEY_FUNC_MAP = {'use_cur_item': 'keyboard_use_cur_item',
       'open_drug_panel': 'keyboard_open_drug_panel',
       hot_key_def.ITEM_SCROLL_UP: 'keyboard_item_scroll_up',
       hot_key_def.ITEM_SCROLL_DOWN: 'keyboard_item_scroll_down'
       }
    HOT_KEY_FUNC_MAP.update([ (func, ('keyboard_use_item_by_func', func)) for func in NORMAL_LIST_HOT_KEY_FUNC_NAME ])
    HOT_KEY_FUNC_MAP.update([ (func, ('keyboard_use_item_by_func', func)) for func in OTHER_LIST_HOT_KEY_FUNC_NAME ])
    HOT_KEY_FUNC_MAP_SHOW = {'use_cur_item': {'node': 'medicine_button.temp_pc'},'open_drug_panel': {'node': 'medicine_button.btn_more.temp_pc'}}
    GLOBAL_EVENT = {'improvise_highlight_on_time': '_on_play_improvise_highlight_ui_efx'
       }

    def on_init_panel(self):
        self._cur_shot_cut = None
        self._mecha_state = False
        self._is_on_changed_player_or_state = False
        self.cur_drug_button = self.panel.medicine_button
        self.cur_drug_data = None
        self.in_using_drug = None
        self.enable_drug_scroll = False
        self.show_scroll_medicine_panel = False
        self.cur_sel_drug_idx = None
        self.cur_sel_drug_idx_ex = None
        self.tmp_drug_data_dict = {}
        self.special_item_id = None
        self.usable_item_id_list = USABLE_ID_LIST
        self.player = None
        self.init_discard_widget()
        self.listen_obj = None
        self.next_tip_time = 0
        self._prev_interact_extra_drag_time = time.time()
        self._max_extra_drag_inactive_interval = 10
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._check_extra_drag_inactive),
         cc.DelayTime.create(1.0)])))
        self.panel.RecordAnimationNodeState('renovate')
        self.panel.RecordAnimationNodeState('renovate_loop')
        self.init_custom_com()
        self.init_node_visible()
        self.add_hide_count(self.__class__.__name__)
        import world
        scn = world.get_active_scene()
        emgr = global_data.emgr
        emgr.scene_camera_target_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self._on_scene_observed_player_setted
        emgr.settle_stage_event += self._on_battle_settle
        emgr.update_item_lost_time += self._update_item_lost_time
        self.on_player_setted()
        self.init_drug_btn()
        self.init_mouse_parameter()
        return

    def add_show_count(self, key='_default', count=1, is_check=True):
        super(DrugUI, self).add_show_count(key, count, is_check)

    def add_hide_count(self, key='_default', count=1, no_same_key=True, is_check=True):
        super(DrugUI, self).add_hide_count(key, count, no_same_key, is_check)

    def change_ui_data(self):
        info = []
        nd = getattr(self.panel, 'medicine_button')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        info.append([w_pos, scale, 'temp_use_tips'])
        nd = self.panel.medicine_button.btn_more
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        info.append([w_pos, scale, 'nd_use_small_tips'])
        nd = getattr(self.panel, 'left')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        info.append([w_pos, scale, 'i_guide_carrier'])
        return info

    def init_discard_widget(self):
        from logic.gutils.new_template_utils import DiscardWidget
        self.discard_widget = DiscardWidget(self.panel, self.panel.drag_item, self.panel.discard)
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type(game_mode_const.Forbid_Discard):
            self.discard_widget.set_enable(False)
        from common.utils.ui_utils import get_scale
        self._click_dist = get_scale('10w')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_node_visible(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
            self.panel.medicine_button.quantity.setVisible(False)
            self.panel.medicine_button.btn_more.setVisible(False)

    def on_player_setted(self):
        player = global_data.cam_lplayer
        self.unbind_player()
        if player:
            is_player_changed = self.player == player
            self.player = player
            control_target = self.player.ev_g_control_target()
            mecha_trans_state = control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()
            mecha_state = False
            if control_target and control_target.logic.sd.ref_is_mecha and not mecha_trans_state:
                mecha_state = True
                self.usable_item_id_list = MECHA_USABLE_ID_LIST
            elif global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                mecha_state = False
                self.usable_item_id_list = MECHA_USABLE_ID_LIST
            else:
                mecha_state = False
                self.usable_item_id_list = USABLE_ID_LIST
            is_mecha_stated_changed = mecha_state != self._mecha_state
            self._is_on_changed_player_or_state = is_player_changed or is_mecha_stated_changed
            self._mecha_state = mecha_state
            self.on_change_state(mecha_state is True)
            self.add_show_count(self.__class__.__name__)
            self.bind_drug_event(player)
            self.init_drug_event()
            self.in_using_drug = None
            if global_data.player and global_data.player.in_local_battle():
                self.in_using_drug = None
            self._is_on_changed_player_or_state = False
        else:
            self.player = None
        return

    def unbind_player(self):
        self.listen_hp_change(0)
        if self.player and self.player.is_valid():
            self.unbind_drug_event(self.player)
        self.player = None
        return

    def init_drug_event(self):
        self.update_shortcut()

    def update_shortcut(self, *args):
        cur_shot_cut_id = self.player.ev_g_show_shortcut()
        item_count = self.player.ev_g_item_count(cur_shot_cut_id) if cur_shot_cut_id else 0
        cur_shot_cut = (cur_shot_cut_id, item_count)
        if cur_shot_cut != self._cur_shot_cut or self._is_on_changed_player_or_state:
            self.on_drug_shortcut_changed(cur_shot_cut_id)
            self.update_drug_ui()
            self._cur_shot_cut = cur_shot_cut

    def init_drug_btn(self):
        self.discard_widget.init_btn(self.panel.medicine_button, is_scrollable=False)

        @self.panel.medicine_button.unique_callback()
        def OnEnd(btn, touch):
            if not self.player:
                return
            else:
                if not self.panel.drag_item.isVisible():
                    self.medicine_btn_on_end(btn, touch)
                if not self._can_interact():
                    return
                if self.cur_drug_data:
                    self.discard_widget.OnEnd(self.panel.medicine_button, touch, self.cur_drug_data.get('item_id', 0), self.cur_drug_data.get('num', 0), [
                     self.panel.medicine_button], is_scrollable=False)
                else:
                    self.discard_widget.OnEnd(self.panel.medicine_button, touch, None, 0, [
                     self.panel.medicine_button], is_scrollable=False)
                return

        @self.panel.medicine_button.unique_callback()
        def OnBegin(btn, touch):
            return self.medicine_btn_on_begin(touch)

        self.panel.medicine_button.SetPressEnable(True)

        @self.panel.medicine_button.unique_callback()
        def OnPressed(btn):
            if not self.player:
                return
            self.medicine_btn_on_pressed()

        @self.panel.medicine_button.unique_callback()
        def OnDrag(btn, touch):
            if not self.player:
                return
            self.medicine_btn_on_drag(touch)
            if self.cur_drug_data and self._can_interact():
                self.discard_widget.OnDrag(btn, touch, self.cur_drug_data.get('item_id'), non_discard_list=[self.panel.medicine_button], is_scrollable=False)

        @self.panel.medicine_button.btn_more.unique_callback()
        def OnClick(btn, touch):
            self.show_medicine_scroll_panel()
            if self.special_item_id:
                ui = global_data.ui_mgr.get_ui('GuideUI')
                if ui:
                    nd = self.panel.nd_first.nd_dec_medicine.btn_close
                    w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
                    ui.show_temp_use_more_tips(w_pos)

        @self.panel.nd_first.nd_dec_medicine.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.hide_medicine_scroll_panel()

        @self.panel.nd_other_list.nd_dec_medicine.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.hide_medicine_scroll_panel()

    def medicine_btn_on_end(self, btn, touch):
        if not self._can_interact():
            return
        else:
            cur_pos = touch.getLocation()
            drug_item_id = None
            if btn.IsPointIn(cur_pos):
                if self.cur_drug_data:
                    drug_item_id = self.cur_drug_data.get('item_id')
            elif self.enable_drug_scroll and self.cur_sel_drug_idx is not None:
                drug_item_id = self.get_drug_item_id_from_scroll_panel_index(self.cur_sel_drug_idx)
            if len(self.extra_drug_list) > 0:
                self.hide_medicine_scroll_panel()
            self.try_use_medicine(drug_item_id)
            return

    def get_drug_item_id_from_scroll_panel_index(self, index):
        drug_item_id = None
        if index < len(self.extra_drug_list):
            sel_drug_id = self.extra_drug_list[index]
            if self.drug_data_dict.get(sel_drug_id, 0) > 0:
                drug_item_id = self.extra_drug_list[index]
        return drug_item_id

    def try_use_medicine(self, drug_item_id):
        if not self.player:
            return
        else:
            if not self._can_interact():
                return
            if not self.player.ev_g_status_check_pass(ST_USE_ITEM):
                if self.player.ev_g_get_state(ST_SKATE_MOVE):
                    self.player.send_event('E_TRY_STOP_SKATE')
                return
            cd_end_time = self.player.ev_g_use_item_cd(drug_item_id)
            cur_time = get_server_time()
            if cd_end_time is not None and cur_time < cd_end_time:
                global_data.game_mgr.show_tip(get_text_by_id(610592))
                return
            control_target = self.player.ev_g_control_target()
            if control_target:
                target_type = control_target.logic.__class__.__name__
                if target_type == 'LMecha':
                    if not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                        return
                elif target_type == 'LMechaTrans':
                    if control_target.logic.ev_g_shape_shift() and not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                        return
                elif target_type == 'LMotorcycle':
                    if not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                        return
            if self.in_using_drug and drug_item_id == self.in_using_drug:
                return
            if self.in_using_drug:
                self.player.send_event('E_ITEMUSE_CANCEL', self.in_using_drug)
            elif drug_item_id:
                from logic.gcommon.item import item_utility
                if item_utility.is_mecha_battery(drug_item_id) and not is_human_mecha_item(drug_item_id):
                    mecha = self.player.ev_g_ctrl_mecha()
                    if not mecha:
                        self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(83452))
                        return
                if item_utility.is_summon_item(drug_item_id):
                    if self.player.ev_g_is_jump():
                        return
                    if not self.player.ev_g_control_human() or self.player.ev_g_get_state(ST_SKATE) and not item_utility.is_mechatran_card(drug_item_id):
                        self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
                        return
                if item_utility.is_charger_item(drug_item_id):
                    if self.player.ev_g_in_mecha('Mecha'):
                        self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(18196))
                        return
                if item_utility.is_mechatran_card(drug_item_id):
                    import world
                    pos = self.player.ev_g_position()
                    scn = world.get_active_scene()
                    exclude_ids = self.player.ev_g_human_col_id()
                    is_valid = False
                    if scn and pos:
                        is_valid, pos = item_utils.check_use_mechatran_card_valid(scn, pos, exclude_ids)
                    if not is_valid:
                        self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(18225))
                        return
                self.player.send_event('E_CTRL_USE_DRUG', drug_item_id)
                self.player.send_event('E_ITEMUSE_TRY', drug_item_id)
            return

    def medicine_btn_on_begin(self, touch):
        self.drug_touch_begin_pos = touch.getLocation()
        return True

    def medicine_btn_on_pressed(self):
        if self.in_using_drug is not None:
            return
        else:
            if len(self.extra_drug_list) > 0:
                self.show_medicine_scroll_panel()
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
            sel_idx = self.cal_sel_drug_idx(self.drug_touch_begin_pos)
            self.cur_sel_drug_idx = sel_idx
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, True)
            return

    def show_medicine_scroll_panel(self):
        if not self.player:
            return
        else:
            self.update_drug_ui()
            self.panel.bg_layer.setVisible(True)
            self.show_scroll_medicine_panel = True
            self.enable_drug_scroll = True
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
            self.panel.medicine_button.btn_more.setVisible(False)
            self._interact_with_extra_drug()
            self.set_scroll_panel_vis()
            return

    def set_scroll_panel_vis(self):
        self.panel.nd_first.setVisible(True)
        self.panel.nd_first.nd_dec_medicine.setVisible(True)
        self.panel.nd_first.bg_medicine_more.setVisible(True)
        if self.other_drug_list:
            self.panel.nd_other_list.setVisible(True)
            self.panel.nd_other_list.nd_dec_medicine.setVisible(True)
            self.panel.nd_other_list.bg_medicine_more.setVisible(True)
        else:
            self.panel.nd_other_list.nd_dec_medicine.setVisible(False)
            self.panel.nd_other_list.bg_medicine_more.setVisible(False)

    def hide_medicine_scroll_panel(self):
        self.panel.nd_first.nd_dec_medicine.setVisible(False)
        self.panel.nd_other_list.nd_dec_medicine.setVisible(False)
        self.panel.nd_first.bg_medicine_more.setVisible(False)
        self.panel.nd_other_list.bg_medicine_more.setVisible(False)
        self.cur_drug_button.sp_cur_drug.setVisible(True)
        self.panel.bg_layer.setVisible(False)
        self.show_scroll_medicine_panel = False
        self.enable_drug_scroll = False
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
            self.panel.medicine_button.btn_more.setVisible(True)
        self.unregister_mouse_scroll_event()
        self._set_cur_item_sel(False)
        if self.special_item_id:
            self.special_item_id = None
            ui = global_data.ui_mgr.get_ui('GuideUI')
            if ui:
                ui.panel.temp_use_more_tips.setVisible(False)
        return

    def medicine_btn_on_drag(self, touch):
        if not self.enable_drug_scroll:
            self.drug_touch_begin_pos = touch.getLocation()
        else:
            cur_pos = touch.getLocation()
            sel_idx = self.cal_sel_drug_idx(cur_pos)
            if sel_idx is not None:
                self._interact_with_extra_drug()
            if sel_idx == self.cur_sel_drug_idx:
                return
        if self.cur_sel_drug_idx is not None:
            self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
        self.cur_sel_drug_idx = sel_idx
        if self.cur_sel_drug_idx is not None:
            self.set_extra_drug_sel(self.cur_sel_drug_idx, True)
        return

    def cal_sel_drug_idx(self, cur_pos):
        allItems = self.panel.nd_first.bg_medicine_more.sv_medicine.GetAllItem()
        for idx, ui_item in enumerate(allItems):
            if ui_item.IsPointIn(cur_pos):
                return idx

        allItems2 = self.panel.nd_other_list.bg_medicine_more.sv_medicine.GetAllItem()
        for idx, ui_item in enumerate(allItems2):
            if ui_item.IsPointIn(cur_pos):
                return idx + len(allItems)

        return None

    def set_extra_drug_sel(self, idx, sel):
        if not self._can_interact():
            sel = False

        def sel_func(ui_item):
            ui_item.choose.setVisible(sel)
            if global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
                ui_item.btn.temp_pc.setVisible(sel)
                set_hot_key_common_tip(ui_item.btn.temp_pc, USE_CUR_ITEM)
            else:
                ui_item.btn.temp_pc.setVisible(False)
            if sel:
                self._interact_with_extra_drug()

        sv_medicine = self.panel.nd_first.bg_medicine_more.sv_medicine
        ui_item = sv_medicine.GetItem(idx)
        if ui_item:
            wpos = ui_item.ConvertToWorldSpacePercentage(50, 50)
            if not sv_medicine.IsPointIn(wpos):
                ctrl_height = sv_medicine.GetCtrlSize().height
                sv_height = sv_medicine.getContentSize().height
                container_height = sv_medicine._container.getContentSize().height
                visible_count = sv_height // ctrl_height
                offset_cnt = visible_count - len(self.normal_drug_list) + idx
                offset_h = max(sv_height - container_height, min(offset_cnt, 0) * ctrl_height)
                sv_medicine.SetContentOffset(ccp(0, offset_h))
            sel_func(ui_item)
        else:
            idx = idx - len(self.normal_drug_list)
            ui_item2 = self.panel.nd_other_list.bg_medicine_more.sv_medicine.GetItem(idx)
            if ui_item2:
                sel_func(ui_item2)

    def check_is_in_other_list(self, drug_id):
        return is_neutral_shop_candy(drug_id)

    def update_drug_ui(self):
        if not self.player:
            return
        else:
            self.drug_data_dict = self.get_drug_data()
            cur_drug_item_id = None
            if self.cur_drug_data is not None:
                cur_drug_item_id = self.cur_drug_data['item_id']
            tmp_drug_data_dict = dict(self.drug_data_dict)
            self.tmp_drug_data_dict = dict(self.drug_data_dict)
            if cur_drug_item_id in tmp_drug_data_dict:
                del tmp_drug_data_dict[cur_drug_item_id]
            useful_drug_list = [ did for did, d_count in six.iteritems(tmp_drug_data_dict) if d_count > 0 ]
            extra_drug_list = useful_drug_list
            extra_drug_list.sort()
            self.extra_drug_list = extra_drug_list
            len_extra_drug_list = len(self.extra_drug_list)
            self.other_drug_list = []
            self.normal_drug_list = []
            if len_extra_drug_list >= 5:
                for mid in self.extra_drug_list:
                    if self.check_is_in_other_list(mid):
                        self.other_drug_list.append(mid)
                    else:
                        self.normal_drug_list.append(mid)

                self.extra_drug_list = self.normal_drug_list + self.other_drug_list
            else:
                self.normal_drug_list = self.extra_drug_list
            if self.special_item_id:
                special_index = -1
                for i, item_id in enumerate(self.normal_drug_list):
                    if item_id == self.special_item_id:
                        special_index = i
                        break

                if special_index >= 0:
                    self.normal_drug_list.pop(special_index)
                    self.normal_drug_list.append(self.special_item_id)
            self.update_scroll_nd(self.panel.nd_first, self.normal_drug_list, tmp_drug_data_dict, 0)
            self.update_scroll_nd(self.panel.nd_other_list, self.other_drug_list, tmp_drug_data_dict, len(self.normal_drug_list))
            self.update_scroll_hotkey_nd()
            if self.enable_drug_scroll:
                if len_extra_drug_list <= 0:
                    self.hide_medicine_scroll_panel()
                else:
                    self.set_scroll_panel_vis()
            if len_extra_drug_list <= 0:
                self.panel.medicine_button.btn_more.setVisible(False)
            elif not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                self.panel.medicine_button.btn_more.setVisible(True)
            return

    def update_scroll_nd(self, top_nd, data_list, all_drug_data_dict, previous_data_list_len):
        len_data_list = len(data_list)
        sv_medicine = top_nd.bg_medicine_more.sv_medicine
        offset_before_update = sv_medicine.GetContentOffset().y
        sv_medicine.SetInitCount(len_data_list)
        for idx in range(len_data_list):
            ui_item = sv_medicine.GetItem(idx)
            if len_data_list <= idx:
                self.init_drug_item(idx, ui_item, {}, sv_medicine)
            else:
                mid = data_list[idx]
                self.init_drug_item(idx + previous_data_list_len, ui_item, {'item_id': mid,'count': all_drug_data_dict[mid]}, sv_medicine)
                if idx != len_data_list - 1:
                    ui_item.line.setVisible(True)
                else:
                    ui_item.line.setVisible(False)

        sv_w, sv_h = sv_medicine.GetContentSize()
        design_height = global_data.ui_mgr.design_screen_size.height
        if len_data_list > 0:
            ui_item = sv_medicine.GetItem(0)
            _, ui_h = ui_item.GetContentSize()
            sv_h = ui_h * len_data_list
            max_h = design_height * 0.8
            if sv_h > max_h:
                visible_item_num = int(max_h / ui_h)
                sv_h = ui_h * (visible_item_num + 0.3)
        sv_medicine.SetContentSize(sv_w, sv_h)
        sw, _ = top_nd.nd_dec_medicine.GetContentSize()
        top_nd.nd_dec_medicine.SetContentSize(sw, sv_h)
        children = top_nd.nd_dec_medicine.GetChildren()
        for child in children:
            child.ResizeAndPosition()

        inner_h = sv_medicine.getInnerContainerSize().height
        offset_h = max(sv_h - inner_h, offset_before_update)
        sv_medicine.SetContentOffset(ccp(0, offset_h))

    def update_scroll_hotkey_nd(self):
        nd_key_list = [
         (
          self.panel.nd_first, self.NORMAL_LIST_HOT_KEY_FUNC_NAME),
         [
          self.panel.nd_other_list, self.OTHER_LIST_HOT_KEY_FUNC_NAME]]
        if global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            for top_nd, func_list in nd_key_list:
                sv_medicine = top_nd.bg_medicine_more.sv_medicine
                count = sv_medicine.GetItemCount()
                for idx in range(count):
                    ui_item = sv_medicine.GetItem(idx)
                    if idx < len(func_list):
                        ui_item.temp_pc_use.setVisible(True)
                        set_hot_key_common_tip(ui_item.temp_pc_use.temp_pc, func_list[idx])
                    else:
                        ui_item.temp_pc_use.setVisible(False)

        else:
            for top_nd, start_idx in nd_key_list:
                sv_medicine = top_nd.bg_medicine_more.sv_medicine
                count = sv_medicine.GetItemCount()
                for idx in range(count):
                    ui_item = sv_medicine.GetItem(idx)
                    ui_item.temp_pc_use.setVisible(False)

    def on_drug_shortcut_changed(self, item_id, *args):
        if item_id:
            item_count = self.player.ev_g_item_count(item_id)
            self.set_quick_drug_item({'item_id': item_id,'num': item_count})
        else:
            self.cur_drug_data = None
        self.listen_hp_change(item_id)
        if not self.cur_drug_data:
            self.cur_drug_button.setVisible(False)
        else:
            self.cur_drug_button.setVisible(True)
        return

    def on_item_data_changed(self, item_data):
        self.check_drug_scroll_panel(item_data)

    def check_drug_scroll_panel(self, item_data):
        need_refresh = False
        if item_data is None:
            need_refresh = True
        elif item_data['item_id'] in self.usable_item_id_list:
            need_refresh = True
            drug_data = self.tmp_drug_data_dict
            item_id = item_data['item_id']
            pic_path = item_utils.get_item_pic_by_item_no(item_id)
            if item_id in drug_data and drug_data[item_id] < item_data.get('count', 0):
                self.panel.vx_item.SetDisplayFrameByPath('', pic_path)
                self.panel.PlayAnimation('get_tools')
        if need_refresh:
            self.update_drug_ui()
            if self.cur_drug_data and item_data['item_id'] == self.cur_drug_data.get('item_id'):
                self.on_drug_shortcut_changed(self.cur_drug_data.get('item_id'))
        return

    def set_quick_drug_item(self, drug_data):
        item_no = drug_data.get('item_id')
        num = drug_data.get('num', 0)
        self.cur_drug_data = {'item_id': item_no,'num': num}
        pic_path = item_utils.get_item_pic_by_item_no(item_no)
        self.cur_drug_button.sp_cur_drug.SetDisplayFrameByPath('', pic_path)
        from logic.gcommon.item.item_utility import is_mecha_battery
        if not self.player or not self.player.ev_g_ctrl_mecha() and is_mecha_battery(item_no) and not is_human_mecha_item(item_no):
            self.cur_drug_button.sp_cur_drug.SetColor('#DH')
        else:
            self.cur_drug_button.sp_cur_drug.SetColor('#SW')
        if is_mecha_battery(item_no):
            self.icon_mech_tool.setVisible(True)
        else:
            self.icon_mech_tool.setVisible(False)
        self.cur_drug_button.quantity.setString(str(num))

    def on_change_state(self, mecha_state=True):
        if not mecha_state:
            btn_pic = [
             'gui/ui_res_2/battle/button/btn_tools.png',
             'gui/ui_res_2/battle/button/btn_tools.png']
            hint_pic = 'gui/ui_res_2/battle/button/frame_tools_sel.png'
        else:
            btn_pic = [
             'gui/ui_res_2/battle/mech_main/btn_medicine.png',
             'gui/ui_res_2/battle/mech_main/btn_medicine_2.png']
            hint_pic = 'gui/ui_res_2/battle/mech_main/frame_medicine_sel.png'
        self.cur_drug_button.SetFrames('', btn_pic, False, None)
        self.panel.img_hint.SetDisplayFrameByPath('', hint_pic)
        self.panel.img_hint2.SetDisplayFrameByPath('', hint_pic)
        self.panel.vx_hint.SetDisplayFrameByPath('', hint_pic)
        item_id = self.cur_drug_data or 0 if 1 else self.cur_drug_data.get('item_id', 0)
        self.listen_hp_change(item_id)
        return

    def listen_hp_change(self, item_id):
        new_listen_obj = None
        if item_id in (1612, ):
            new_listen_obj = self.player
        elif item_id in (9902, 9904):
            if self.player:
                control_target = self.player.ev_g_control_target()
                if control_target.__class__.__name__ == 'Mecha':
                    new_listen_obj = control_target.logic
        if new_listen_obj == self.listen_obj:
            return
        else:
            if self.listen_obj:
                self.listen_obj.unregist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
                self.panel.StopAnimation('hint')
                self.panel.img_hint.setVisible(False)
            self.listen_obj = new_listen_obj
            if self.listen_obj:
                self.listen_obj.regist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
                self.on_hp_changed()
            return

    def on_hp_changed(self, hp=0, mod=0):
        if not self.listen_obj:
            return
        percent = self.listen_obj.ev_g_health_percent()
        if percent > 0.4:
            self.panel.StopAnimation('hint')
            self.panel.img_hint.setVisible(False)
        else:
            if not self.panel.IsPlayingAnimation('hint'):
                self.panel.PlayAnimation('hint')
            if mod <= 0 and time.time() > self.next_tip_time:
                self.next_tip_time = time.time() + 10
                global_data.emgr.play_tips_voice.emit('tips_05')

    def get_drug_data(self):
        medical_ids = {}
        for did in self.usable_item_id_list:
            medical_ids[did] = 0

        if self.player:
            for mid in six_ex.keys(medical_ids):
                count = self.player.ev_g_item_count(mid)
                if count is None:
                    count = 0
                medical_ids[mid] = count

        return medical_ids

    def init_drug_item(self, index, ui_item, data, nd_list):
        item_count = data.get('count', 0)
        item_id = data.get('item_id', 0)
        self.discard_widget.init_btn(ui_item.btn)
        ui_item.btn.SetSelect(True)
        from logic.gcommon.item import item_utility
        pic_path = item_utils.get_item_pic_by_item_no(item_id)
        ui_item.item.SetDisplayFrameByPath('', pic_path)
        if item_count > 0:
            ui_item.item.SetColor('#SW')
            ui_item.num.SetColor('#DW')
        ui_item.num.setString(str(item_count))
        if self.cur_sel_drug_idx_ex is not None:
            show_choose = index == self.cur_sel_drug_idx_ex
        else:
            show_choose = False
        ui_item.choose.setVisible(show_choose)
        if item_utility.is_mecha_battery(item_id):
            ui_item.icon_mech_tool.setVisible(True)
            if self.player and (self.player.ev_g_ctrl_mecha() or is_human_mecha_item(item_id)):
                ui_item.item.SetColor('#SW')
            else:
                ui_item.item.SetColor('#DH')
        else:
            ui_item.icon_mech_tool.setVisible(False)

        @ui_item.btn.unique_callback()
        def OnClick(btn, touch):
            if btn.GetMovedDistance() < self._click_dist:
                self.on_click_drug_btn(index)

        @ui_item.btn.unique_callback()
        def OnBegin(btn, touch):
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
            self.cur_sel_drug_idx = index
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, True)
            self._interact_with_extra_drug()
            return True

        @ui_item.btn.unique_callback()
        def OnEnd(btn, touch):
            if self.cur_sel_drug_idx is not None:
                self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
            if self._can_interact():
                self.discard_widget.OnEnd(btn, touch, item_id, item_count, [nd_list])
            return

        @ui_item.btn.unique_callback()
        def OnDrag(layer, touch):
            if self._can_interact():
                self.discard_widget.OnDrag(ui_item.btn, touch, item_id, [nd_list])

        return

    def on_click_drug_btn(self, index):
        if not self._can_interact():
            return
        else:
            if self.enable_drug_scroll:
                drug_item_id = self.get_drug_item_id_from_scroll_panel_index(index)
                if self.cur_sel_drug_idx is not None:
                    self.set_extra_drug_sel(self.cur_sel_drug_idx, False)
                self.hide_medicine_scroll_panel()
                if drug_item_id:
                    self.set_drug_shortcut(drug_item_id)
                    self.try_use_medicine(drug_item_id)
            return

    def set_drug_shortcut(self, drug_item_id):
        if drug_item_id is not None and self.player and self.player.is_valid():
            if self.cur_drug_data is not None:
                self.player.send_event('E_SET_SHOW_SHORTCUT', drug_item_id)
        return

    def on_finalize_panel(self):
        super(DrugUI, self).on_finalize_panel()
        self.unbind_player()
        self.destroy_widget('custom_ui_com')
        self.destroy_widget('discard_widget')

    def bind_drug_event(self, target):
        target.regist_event('E_SET_SHOW_SHORTCUT', self.update_shortcut, 10)
        target.regist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
        target.regist_event('E_SHOW_USE_PROGRESS', self.on_item_use_progress)
        target.regist_event('E_ITEMUSE_CANCEL_RES', self.on_item_use_cancel)
        target.regist_event('E_ITEMUSE_ON', self.on_item_used)
        target.regist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def unbind_drug_event(self, target):
        if target.unregist_event:
            target.unregist_event('E_SET_SHOW_SHORTCUT', self.update_shortcut)
            target.unregist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
            target.unregist_event('E_SHOW_USE_PROGRESS', self.on_item_use_progress)
            target.unregist_event('E_ITEMUSE_CANCEL_RES', self.on_item_use_cancel)
            target.unregist_event('E_ITEMUSE_ON', self.on_item_used)
            target.unregist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def on_item_use_progress(self, item_id, *arg):
        from logic.gutils.item_utils import is_food_item, is_health_item
        from logic.gcommon.item import item_utility
        if not is_health_item(item_id) and not is_food_item(item_id) and not item_utility.is_mecha_battery(item_id) and not item_utility.is_summon_item(item_id) and not item_utility.is_charger_item(item_id):
            return
        self.in_using_drug = item_id
        item_count = self.player.ev_g_item_count(item_id)
        self.set_quick_drug_item({'item_id': item_id,'num': item_count})

    def on_item_use_cancel(self, item_id=None):
        self.in_using_drug = None
        if not self.player:
            return
        else:
            self.update_shortcut()
            return

    def on_item_used(self, item_id, item_cd=None, item_limit=None):
        self.on_item_use_cancel(item_id)

    def on_begin_bg_layer(self, *args):
        if self.enable_drug_scroll:
            self.hide_medicine_scroll_panel()
        return True

    def init_mouse_parameter(self):
        self._cur_mouse_dist = 0

    def _can_interact(self):
        if not global_data.player or not global_data.player.logic:
            return False
        if not self.player:
            return False
        return global_data.player.logic.id == self.player.id

    def keyboard_use_item_by_func(self, func_name, msg, keycode):
        if not self._can_interact():
            return False
        if not self.enable_drug_scroll:
            return False
        key_to_drug = [
         (
          self.NORMAL_LIST_HOT_KEY_FUNC_NAME, self.normal_drug_list),
         [
          self.OTHER_LIST_HOT_KEY_FUNC_NAME, self.other_drug_list]]
        for key_drug in key_to_drug:
            key_list, drug_list = key_drug
            if func_name in key_list:
                index = key_list.index(func_name)
                if index < len(drug_list):
                    drug_id = drug_list[index]
                    self.hide_scroll_panel_and_clean_select_idx()
                    self.set_drug_shortcut(drug_id)
                    self.try_use_medicine(drug_id)
                    return

        if self.player:
            self.player.send_event('E_SHOW_MESSAGE', get_text_local_content(920707))
        return False

    def keyboard_use_cur_item(self, msg, keycode):
        if not self._can_interact():
            return
        else:
            if self.enable_drug_scroll and self.cur_sel_drug_idx_ex is not None and self.cur_sel_drug_idx_ex != len(self.extra_drug_list):
                drug_item_id = self.get_drug_item_id_from_scroll_panel_index(self.cur_sel_drug_idx_ex)
                if len(self.extra_drug_list) > 0:
                    self.hide_scroll_panel_and_clean_select_idx()
                self.set_drug_shortcut(drug_item_id)
                self.try_use_medicine(drug_item_id)
            elif self.cur_drug_data:
                if self.cur_sel_drug_idx_ex is not None and self.cur_sel_drug_idx_ex == len(self.extra_drug_list):
                    self.hide_medicine_scroll_panel()
                drug_item_id = self.cur_drug_data.get('item_id')
                self.try_use_medicine(drug_item_id)
            return

    def keyboard_open_drug_panel(self, msg, keycode):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_CONCERT,)):
            if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_in_mecha('Mecha'):
                return
        if not self.enable_drug_scroll:
            if len(self.extra_drug_list) > 0:
                self.show_medicine_scroll_panel()
                self.register_mouse_scroll_event()
                self.cur_sel_drug_idx = len(self.extra_drug_list) - 1
                self.set_extra_drug_sel(self.cur_sel_drug_idx, True)
                self.cur_sel_drug_idx_ex = self.cur_sel_drug_idx
                self._refresh_cur_item_hotkey_node()
        else:
            self.hide_medicine_scroll_panel()
            self.cur_sel_drug_idx = None
            if self.cur_sel_drug_idx_ex is not None and self.cur_sel_drug_idx_ex != len(self.extra_drug_list):
                self.set_extra_drug_sel(self.cur_sel_drug_idx_ex, False)
            self.cur_sel_drug_idx_ex = None
            self._refresh_cur_item_hotkey_node()
        return

    def check_can_mouse_scroll(self):
        if not self.panel.isVisible():
            return False
        if not self.enable_drug_scroll:
            return False
        if not self._can_interact():
            return False
        return True

    def keyboard_item_scroll_up(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, self.ui_scroll_sensitivity, None)
            return

    def keyboard_item_scroll_down(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, -self.ui_scroll_sensitivity, None)
            return

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        dist = -delta
        self._cur_mouse_dist += dist
        old_sel_drug_index_ex = self.cur_sel_drug_idx_ex
        if abs(self._cur_mouse_dist) >= self.ui_scroll_sensitivity:
            changed_index = int(self._cur_mouse_dist / self.ui_scroll_sensitivity)
            changed_index = max(-1, changed_index)
            self._cur_mouse_dist = 0
            self.cur_sel_drug_idx_ex += changed_index
            self.cur_sel_drug_idx_ex %= len(self.extra_drug_list) + 1
        if old_sel_drug_index_ex != self.cur_sel_drug_idx_ex:
            if self.cur_sel_drug_idx_ex == len(self.extra_drug_list):
                self.set_extra_drug_sel(old_sel_drug_index_ex, False)
                self._set_cur_item_sel(True)
            else:
                if old_sel_drug_index_ex == len(self.extra_drug_list):
                    self._set_cur_item_sel(False)
                else:
                    self.set_extra_drug_sel(old_sel_drug_index_ex, False)
                self.set_extra_drug_sel(self.cur_sel_drug_idx_ex, True)

    def _set_cur_item_sel(self, enable):
        if not self._can_interact():
            enable = False
        self.panel.img_hint2.setVisible(enable)
        self._refresh_cur_item_hotkey_node(enable)

    def _refresh_cur_item_hotkey_node(self, selected=None):
        show = global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable()
        if selected is None:
            selected = False
            if self.cur_sel_drug_idx_ex is not None and self.cur_sel_drug_idx_ex == len(self.extra_drug_list):
                selected = True
        show = show and (not self.show_scroll_medicine_panel or selected)
        self.panel.medicine_button.temp_pc.setVisible(show)
        return

    def _interact_with_extra_drug(self):
        self._prev_interact_extra_drag_time = time.time()

    def _check_extra_drag_inactive(self):
        if not self.enable_drug_scroll:
            return
        if not self._can_interact():
            return
        if time.time() - self._prev_interact_extra_drag_time >= self._max_extra_drag_inactive_interval:
            if self.enable_drug_scroll:
                self.hide_medicine_scroll_panel()

    def ui_vkb_custom_func(self):
        if self.enable_drug_scroll:
            self.hide_medicine_scroll_panel()
            return True
        else:
            return False

    def hide_scroll_panel_and_clean_select_idx(self):
        self.hide_medicine_scroll_panel()
        self.cur_sel_drug_idx = None
        if self.cur_sel_drug_idx_ex is not None and self.cur_sel_drug_idx_ex != len(self.extra_drug_list):
            self.set_extra_drug_sel(self.cur_sel_drug_idx_ex, False)
        self.cur_sel_drug_idx_ex = None
        self._refresh_cur_item_hotkey_node()
        return

    def on_hot_key_opened_state(self):
        super(DrugUI, self).on_hot_key_opened_state()
        self.update_scroll_hotkey_nd()
        self.hide_scroll_panel_and_clean_select_idx()

    def on_hot_key_closed_state(self):
        super(DrugUI, self).on_hot_key_closed_state()
        self.update_scroll_hotkey_nd()
        self.hide_scroll_panel_and_clean_select_idx()

    def register_mouse_scroll_event(self):
        super(DrugUI, self).register_mouse_scroll_event()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def unregister_mouse_scroll_event(self):
        super(DrugUI, self).unregister_mouse_scroll_event()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def _on_scene_observed_player_setted(self, lplayer):
        self.panel.drag_item.setVisible(False)
        self.panel.discard.setVisible(False)
        if lplayer:
            self.add_show_count(self.__class__.__name__)

    def _on_battle_settle(self, *args, **kw):
        pass

    def _stop_all_improvise_highlight_ui_efx(self):
        if not self.panel.HasAnimation('renovate') or not self.panel.HasAnimation('renovate_loop'):
            return
        self.panel.StopAnimation('renovate')
        self.panel.StopAnimation('renovate_loop')
        self.panel.RecoverAnimationNodeState('renovate')
        self.panel.RecoverAnimationNodeState('renovate_loop')

    def _on_play_improvise_highlight_ui_efx(self, left_ready_time):
        if not self.panel.HasAnimation('renovate') or not self.panel.HasAnimation('renovate_loop'):
            return
        self.panel.stopActionByTag(self.DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG)
        self.panel.stopActionByTag(self.DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG)
        self._stop_all_improvise_highlight_ui_efx()
        self.panel.PlayAnimation('renovate')
        renovate_time = self.panel.GetAnimationMaxRunTime('renovate')
        if renovate_time > 0 and renovate_time < left_ready_time:

            def continue_play_loop_cb():
                self.panel.StopAnimation('renovate')
                self.panel.PlayAnimation('renovate_loop')

            self.panel.DelayCallWithTag(renovate_time, continue_play_loop_cb, self.DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG)

        def all_done_cb():
            self._stop_all_improvise_highlight_ui_efx()

        self.panel.DelayCallWithTag(left_ready_time, all_done_cb, self.DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG)

    def is_cur_drug_item(self, item_id):
        if self.cur_drug_data and item_id == self.cur_drug_data['item_id']:
            return True
        return False

    def _update_item_lost_time(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
            item_lost_time = global_data.death_battle_data.get_item_lost_time()
            delay_time = item_lost_time - int(tutil.get_time())
            if delay_time > 0:
                self.on_time_conut(delay_time)

    def on_time_conut(self, delay_time):

        def refresh_time_finsh():
            text = '{}s'.format(str(0))
            self.panel.lab_rest_time.SetString(text)
            self.panel.lab_rest_time.setVisible(False)

        def refresh_time(pass_time):
            left_time = int(math.ceil(delay_time - pass_time))
            text = '{}s'.format(str(left_time))
            self.panel.lab_rest_time.SetString(text)
            if left_time <= 0:
                self.panel.lab_rest_time.StopTimerAction()
                refresh_time_finsh()
                return

        self.panel.lab_rest_time.StopTimerAction()
        if delay_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        self.panel.lab_rest_time.setVisible(True)
        self.panel.lab_rest_time.TimerAction(refresh_time, delay_time, interval=0.1)


class KizunaDrugUI(DrugUI):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/ai_dacall/ai_fireworks'

    def init_custom_com(self):
        pass

    def on_change_state(self, mecha_state=True):
        if not mecha_state:
            btn_pic = [
             'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/button/bar_prop.png',
             'gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/button/bar_prop.png']
            hint_pic = 'gui/ui_res_2/battle/button/frame_tools_sel.png'
        else:
            btn_pic = [
             'gui/ui_res_2/battle/mech_main/btn_medicine.png',
             'gui/ui_res_2/battle/mech_main/btn_medicine_2.png']
            hint_pic = 'gui/ui_res_2/battle/mech_main/frame_medicine_sel.png'
        self.cur_drug_button.SetFrames('', btn_pic, False, None)
        self.panel.img_hint.SetDisplayFrameByPath('', hint_pic)
        self.panel.img_hint2.SetDisplayFrameByPath('', hint_pic)
        self.panel.vx_hint.SetDisplayFrameByPath('', hint_pic)
        item_id = self.cur_drug_data or 0 if 1 else self.cur_drug_data.get('item_id', 0)
        self.listen_hp_change(item_id)
        return