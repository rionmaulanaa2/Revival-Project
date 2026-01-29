# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/ThrowRockerUI.py
from __future__ import absolute_import
import six
from six.moves import range
import cc
import time
from data import hot_key_def
from data.item_use_var import THROW_ID_LIST
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.gutils import item_utils
from logic.gutils.hot_key_utils import set_hot_key_common_tip
from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE
from logic.client.const import game_mode_const
from common.const import uiconst
import logic.gcommon.time_utility as tutil
import math

class ThrowRockerBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'bg_layer.OnBegin': '_on_begin_bg_layer'
       }
    IS_PLAY_OPEN_SOUND = False
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self):
        self._cur_item_data = {}
        self._in_using_item_id = None
        self._enable_scroll = False
        self._cur_sel_item_idx = None
        self._tmp_item_data_dict = {}
        self._usable_item_id_list = THROW_ID_LIST
        self._player = None
        self._last_bind_player = None
        self._is_in_mecha = False
        self._cur_mouse_dist = 0
        self._prev_interact_extra_item_time = time.time()
        self._max_extra_drag_inactive_interval = 10
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._check_extra_item_inactive),
         cc.DelayTime.create(1.0)])))
        self.panel.sv_throw_list.SetInitCount(0)
        self._init_custom_com()
        self._init_node_visible()
        self.init_discard_widget()
        global_data.emgr.scene_camera_target_setted_event += self._on_player_setted
        global_data.emgr.update_item_lost_time += self._update_item_lost_time
        self._on_player_setted()
        self._init_throw_btn()
        return

    def init_discard_widget(self):
        from logic.gutils.new_template_utils import DiscardWidget
        self.discard_widget = DiscardWidget(self.panel, self.panel.drag_item, self.panel.discard)
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type(game_mode_const.Forbid_Discard):
            self.discard_widget.set_enable(False)
        from common.utils.ui_utils import get_scale
        self._click_dist = get_scale('10w')

    def _init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def _init_node_visible(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
            self.panel.btn_change_throw.setVisible(False)
            self.panel.quantity.setVisible(False)

    def _on_player_setted(self):
        self._unbind_player()
        player = global_data.cam_lplayer
        if not player:
            return
        else:
            self._bind_player_event(player, True)
            self._player = player
            if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                self._usable_item_id_list = []
            control_target = player.ev_g_control_target()
            mode_type = global_data.game_mode.get_mode_type()
            is_pve_mode = global_data.game_mode and game_mode_const.is_mode_type(mode_type, (game_mode_const.GAME_MODE_PVE, game_mode_const.GAME_MODE_PVE_EDIT))
            if not is_pve_mode and control_target and control_target.logic.sd.ref_is_mecha and not control_target.logic.ev_g_is_mechatran():
                self.panel.nd_change_throw.setVisible(False)
                self._is_in_mecha = True
            else:
                self._is_in_mecha = False
                self.panel.nd_change_throw.setVisible(True)
                self._refresh_all_ui()
                if global_data.player and global_data.player.in_local_battle():
                    self._in_using_item_id = None
            if not self._can_interact():
                self.panel.drag_item.setVisible(False)
                self.panel.discard.setVisible(False)
            return

    def _unbind_player(self):
        if self._player and self._player.is_valid():
            self._bind_player_event(self._player, False)
        self._player = None
        return

    def _refresh_all_ui(self, *args):
        cur_shot_cut = self._player.share_data.ref_throw_item_shortcut
        self._on_shortcut_changed(cur_shot_cut)
        self._update_ui_data()
        self._update_scroll_node()

    def _update_ui_data(self):
        self._throw_item_data_dict = {}
        if self._player:
            for item_id in self._usable_item_id_list:
                self._throw_item_data_dict[item_id] = self._player.ev_g_item_count(item_id)

        self._tmp_item_data_dict = dict(self._throw_item_data_dict)
        cur_item_id = self._cur_item_data.get('item_id', -1)
        if cur_item_id in self._tmp_item_data_dict:
            del self._tmp_item_data_dict[cur_item_id]

    def _get_item_id_by_scroll_index(self, index):
        item_id = None
        if index < len(self._extra_item_list):
            sel_item_id = self._extra_item_list[index]
            if self._throw_item_data_dict.get(sel_item_id, 0) > 0:
                item_id = sel_item_id
        return item_id

    def _try_use_item(self, item_id):
        if not self._can_interact() or not item_id or self._player.sd.ref_is_mecha:
            return
        if not self._player.ev_g_status_check_pass(ST_USE_ITEM):
            if self._player.ev_g_get_state(ST_SKATE_MOVE):
                self._player.send_event('E_TRY_STOP_SKATE')
            return
        if self._in_using_item_id and item_id == self._in_using_item_id:
            return
        if self._in_using_item_id:
            self._player.send_event('E_ITEMUSE_CANCEL', self._in_using_item_id)
            return
        self._player.send_event('E_ITEMUSE_TRY', item_id)

    def _show_scroll_panel(self):
        if not self._player:
            return
        else:
            self._update_scroll_node()
            self.panel.bg_layer.setVisible(True)
            self._enable_scroll = True
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, False)
            if self.panel.btn_change_throw:
                self.panel.btn_change_throw.setVisible(False)
            self._interact_with_extra_throw_item()
            self._set_scroll_panel_vis()
            return

    def _set_scroll_panel_vis(self):
        if self.panel.btn_change_throw:
            self.panel.btn_change_throw.setVisible(False)
        self.panel.sv_throw_list.setVisible(True)
        self.panel.nd_dec_throw.setVisible(True)

    def _hide_scroll_panel(self):
        if self.panel.btn_change_throw:
            if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                self.panel.btn_change_throw.setVisible(True)
        self.panel.sv_throw_list.setVisible(False)
        self.panel.nd_dec_throw.setVisible(False)
        self._enable_scroll = False
        self.panel.bg_layer.setVisible(False)
        self.unregister_mouse_scroll_event()

    def _cal_sel_item_idx(self, cur_pos):
        allItems = self.sv_throw_list.GetAllItem()
        for idx, ui_item in enumerate(allItems):
            if ui_item.IsPointIn(cur_pos):
                return idx

        return None

    def _set_extra_item_sel(self, idx, sel):
        if not self._can_interact():
            sel = False

        def sel_func(ui_item):
            ui_item.choose.setVisible(sel)
            if global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
                ui_item.btn.temp_pc.setVisible(sel)
                set_hot_key_common_tip(ui_item.btn.temp_pc, hot_key_def.USE_CUR_THROW_ITEM)
            if sel:
                self._interact_with_extra_throw_item()

        ui_item = self.panel.sv_throw_list.GetItem(idx)
        if ui_item:
            sel_func(ui_item)

    def _update_scroll_node(self):
        valid_list = [ did for did, d_count in six.iteritems(self._tmp_item_data_dict) if d_count > 0 ]
        valid_list.sort()
        self._extra_item_list = valid_list
        btn_show_lst_vis = False if len(self._extra_item_list) <= 0 else True
        self._update_scroll_nd()
        self._update_scroll_hotkey_nd()
        if len(self._extra_item_list) > 0:
            if self._enable_scroll:
                self._set_scroll_panel_vis()
        else:
            self._hide_scroll_panel()
        if self.panel.btn_change_throw:
            self.panel.btn_change_throw.setVisible(btn_show_lst_vis)

    def _update_scroll_nd(self):
        len_data_list = len(self._extra_item_list)
        sv_node = self.panel.sv_throw_list
        sv_node.SetInitCount(len_data_list)
        for idx in range(len_data_list):
            ui_item = sv_node.GetItem(idx)
            item_id = self._extra_item_list[idx]
            self._init_item_node(idx, ui_item, {'item_id': item_id,'count': self._tmp_item_data_dict[item_id]})
            if idx != len_data_list - 1:
                line_vis = True if 1 else False
                ui_item.line.setVisible(line_vis)

        _, sh = sv_node.GetContentSize()
        sw, _ = self.panel.nd_dec_throw.GetContentSize()
        self.panel.nd_dec_throw.SetContentSize(sw, sh)
        children = self.panel.nd_dec_throw.GetChildren()
        for child in children:
            child.ResizeAndPosition()

    def _on_shortcut_changed(self, item_id, *args):
        if item_id:
            item_count = self._player.ev_g_item_count(item_id)
            self._cur_item_data = {'item_id': item_id,'num': item_count}
            self._set_quick_item(self._cur_item_data)
        else:
            self._cur_item_data = {}
        visible = self._cur_item_data and self._cur_item_data.get('item_id') in self._usable_item_id_list
        self.panel.nd_change_throw.setVisible(bool(visible and not self._is_in_mecha))

    def _on_item_data_changed(self, item_data):
        if item_data is None:
            need_refresh = True if 1 else False
            if item_data['item_id'] in self._usable_item_id_list:
                need_refresh = True
                tmp_data = self._tmp_item_data_dict
                item_id = item_data['item_id']
                pic_path = item_utils.get_item_pic_by_item_no(item_id)
                if item_id in tmp_data and tmp_data[item_id] < item_data.get('count', 0):
                    self.panel.vx_item.SetDisplayFrameByPath('', pic_path)
                    self.panel.PlayAnimation('get_tools')
            ui_updated = self._choose_throw_shortcut(item_data)
            ui_updated or self._update_ui_data()
        if need_refresh and not ui_updated:
            self._update_scroll_node()
            if self._cur_item_data and item_data['item_id'] == self._cur_item_data.get('item_id'):
                self._on_shortcut_changed(self._cur_item_data.get('item_id'))
        return

    def _set_quick_item(self, item_data):
        item_no = item_data.get('item_id')
        num = item_data.get('num', 0)
        pic_path = item_utils.get_item_pic_by_item_no(item_no)
        self.panel.item.SetDisplayFrameByPath('', pic_path)
        self.panel.quantity.setString(str(num))

    def _init_item_node(self, index, ui_item, data):
        item_count = data.get('count', 0)
        item_id = data.get('item_id', 0)
        self.discard_widget.init_btn(ui_item.btn, is_scrollable=False)
        ui_item.btn.SetSelect(True)
        pic_path = item_utils.get_item_pic_by_item_no(item_id)
        ui_item.item.SetDisplayFrameByPath('', pic_path)
        if item_count > 0:
            ui_item.item.SetColor('#SW')
            ui_item.num.SetColor('#DW')
        ui_item.num.setString(str(item_count))
        ui_item.choose.setVisible(False)
        ui_item.icon_mech_tool.setVisible(False)

        @ui_item.btn.unique_callback()
        def OnClick(btn, touch):
            if btn.GetMovedDistance() < self._click_dist:
                self._on_click_item_btn(index)

        @ui_item.btn.unique_callback()
        def OnBegin(btn, touch):
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, False)
            self._cur_sel_item_idx = index
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, True)
            self._interact_with_extra_throw_item()
            return True

        @ui_item.btn.unique_callback()
        def OnEnd(btn, touch):
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, False)
            if self._can_interact():
                self.discard_widget.OnEnd(btn, touch, item_id, item_count, [self.panel.sv_throw_list], is_scrollable=False)
            return

        @ui_item.btn.unique_callback()
        def OnDrag(layer, touch):
            if self._can_interact():
                self.discard_widget.OnDrag(ui_item.btn, touch, item_id, [self.panel.sv_throw_list], is_scrollable=False)

    def _on_click_item_btn(self, index):
        if not self._can_interact():
            return
        else:
            if self._enable_scroll:
                item_id = self._get_item_id_by_scroll_index(index)
                if self._cur_sel_item_idx is not None:
                    self._set_extra_item_sel(self._cur_sel_item_idx, False)
                self._hide_scroll_panel()
                if item_id:
                    self._set_throw_shortcut(item_id)
                    self._try_use_item(item_id)
            return

    def _set_throw_shortcut(self, item_id):
        if item_id is not None and self._player and self._player.is_valid():
            self._player.share_data.ref_throw_item_shortcut = item_id
            self._refresh_all_ui()
            if self._cur_item_data:
                self._player.send_event('E_CALL_SYNC_METHOD', 'set_throw_item_shortcut', (item_id,))
        return

    def _bind_player_event(self, target, bind):
        event_lst = [
         [
          'E_ITEM_DATA_CHANGED', self._on_item_data_changed, 0],
         [
          'E_SHOW_USE_PROGRESS', self._on_item_use_progress, 0],
         [
          'E_ITEMUSE_CANCEL_RES', self._on_item_use_cancel, 0],
         [
          'E_ITEMUSE_ON', self._on_item_used, 0]]
        if bind:
            if self._last_bind_player != target:
                self._last_bind_player = target
                for event_name, func, priority in event_lst:
                    target.regist_event(event_name, func, priority)

        else:
            self._last_bind_player = None
            for event_name, func, priority in event_lst:
                target.unregist_event(event_name, func)

        return

    def _on_item_use_progress(self, item_id, *arg):
        if item_id not in self._usable_item_id_list:
            return
        self._in_using_item_id = item_id
        item_count = self._player.ev_g_item_count(item_id)
        self._set_quick_item({'item_id': item_id,'num': item_count})

    def _on_item_use_cancel(self, item_id=None):
        self._in_using_item_id = None
        if not self._player:
            return
        else:
            self._refresh_all_ui()
            return

    def _on_item_used(self, item_id, item_cd=None, item_limit=None):
        self._on_item_use_cancel(item_id)

    def _on_begin_bg_layer(self, *args):
        if self._enable_scroll:
            self._hide_scroll_panel()
        return True

    def _can_interact(self):
        if not global_data.player or not global_data.player.logic:
            return False
        if not self._player:
            return False
        return global_data.player.logic.id == self._player.id

    def _interact_with_extra_throw_item(self):
        self._prev_interact_extra_item_time = time.time()

    def _check_extra_item_inactive(self):
        if not self._enable_scroll:
            return
        if time.time() - self._prev_interact_extra_item_time >= self._max_extra_drag_inactive_interval:
            if self._enable_scroll:
                self._hide_scroll_panel()

    def _init_throw_btn(self):
        self.discard_widget.init_btn(self.panel.change_throw, is_scrollable=False)

        @self.panel.change_throw.unique_callback()
        def OnBegin(btn, touch):
            return self._throw_btn_on_begin(touch)

        @self.panel.change_throw.unique_callback()
        def OnEnd(btn, touch):
            if not self._player:
                return
            else:
                if not self.panel.drag_item.isVisible():
                    self._throw_btn_on_end(btn, touch)
                if not self._can_interact():
                    return
                if self._cur_item_data:
                    self.discard_widget.OnEnd(self.panel.change_throw, touch, self._cur_item_data.get('item_id', 0), self._cur_item_data.get('num', 0), [
                     self.panel.change_throw], is_scrollable=False)
                else:
                    self.discard_widget.OnEnd(self.panel.change_throw, touch, None, 0, [
                     self.panel.change_throw], is_scrollable=False)
                return

        self.panel.change_throw.SetPressEnable(True)

        @self.panel.change_throw.unique_callback()
        def OnPressed(btn):
            if not self._player:
                return
            self._throw_btn_on_pressed()

        @self.panel.change_throw.unique_callback()
        def OnDrag(btn, touch):
            if not self._player:
                return
            self._throw_btn_on_drag(touch)
            if not self._can_interact():
                return
            if self._cur_item_data:
                self.discard_widget.OnDrag(btn, touch, self._cur_item_data.get('item_id'), non_discard_list=[
                 self.panel.change_throw], is_scrollable=False)

        @self.panel.btn_change_throw.unique_callback()
        def OnClick(btn, touch):
            self._show_scroll_panel()

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self._hide_scroll_panel()

    def _throw_btn_on_begin(self, touch):
        self._btn_touch_begin_pos = touch.getLocation()
        return True

    def _throw_btn_on_end(self, btn, touch):
        if not self._can_interact():
            return
        else:
            cur_pos = touch.getLocation()
            item_id = None
            if btn.IsPointIn(cur_pos):
                if self._cur_item_data:
                    item_id = self._cur_item_data.get('item_id')
            elif self._enable_scroll and self._cur_sel_item_idx is not None:
                item_id = self._get_item_id_by_scroll_index(self._cur_sel_item_idx)
            if len(self._extra_item_list) > 0:
                self._hide_scroll_panel()
            self._try_use_item(item_id)
            return

    def _throw_btn_on_pressed(self):
        if self._in_using_item_id is not None:
            return
        else:
            if len(self._extra_item_list) > 0:
                self._show_scroll_panel()
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, False)
            sel_idx = self._cal_sel_item_idx(self._btn_touch_begin_pos)
            self._cur_sel_item_idx = sel_idx
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, True)
            return

    def _throw_btn_on_drag(self, touch):
        if not self._enable_scroll:
            self._btn_touch_begin_pos = touch.getLocation()
        else:
            cur_pos = touch.getLocation()
            sel_idx = self._cal_sel_item_idx(cur_pos)
            if sel_idx is not None:
                self._interact_with_extra_throw_item()
            if sel_idx == self._cur_sel_item_idx:
                return
        if self._cur_sel_item_idx is not None:
            self._set_extra_item_sel(self._cur_sel_item_idx, False)
        self._cur_sel_item_idx = sel_idx
        if self._cur_sel_item_idx is not None:
            self._set_extra_item_sel(self._cur_sel_item_idx, True)
        return

    def _choose_throw_shortcut(self, item_data_changed):
        if item_data_changed and not item_data_changed.get('refresh', True):
            return False
        if not self._player:
            return False
        if item_data_changed['item_id'] not in self._usable_item_id_list:
            return False
        all_other_items = self._player.ev_g_others()
        item_set = set()
        for item in six.itervalues(all_other_items):
            item_set.add(item['item_id'])

        new_shortcut = 0
        for item_id in self._usable_item_id_list:
            if item_id in item_set:
                new_shortcut = item_id
                break

        now_shortcut = self._player.share_data.ref_throw_item_shortcut
        self._player.share_data.ref_throw_item_shortcut = new_shortcut
        self._refresh_all_ui()
        if new_shortcut != now_shortcut:
            self._player.send_event('E_CALL_SYNC_METHOD', 'set_throw_item_shortcut', (new_shortcut,))
        return True

    def keyboard_use_item(self, item_id, msg, keycode):
        self._try_use_item(item_id)

    def keyboard_use_item_by_func(self, func_name, msg, keycode):
        if not self._can_interact():
            return False
        if not self._enable_scroll:
            return False
        key_to_drug = [(self.NORMAL_LIST_HOT_KEY_FUNC_NAME, self.normal_drug_list),
         [
          self.OTHER_LIST_HOT_KEY_FUNC_NAME, self.other_drug_list]]
        for key_drug in key_to_drug:
            key_list, drug_list = key_drug
            if func_name in key_list:
                index = key_list.index(func_name)
                if index < len(drug_list):
                    drug_id = drug_list[index]
                    self._hide_scroll_panel()
                    self._try_use_item(drug_id)
                    return

        if self._player:
            self._player.send_event('E_SHOW_MESSAGE', get_text_local_content(920707))
        return False

    def _keyboard_use_cur_item(self, msg, keycode):
        if not self._can_interact():
            return
        else:
            if self._enable_scroll and self._cur_sel_item_idx is not None:
                drug_item_id = self._get_item_id_by_scroll_index(self._cur_sel_item_idx)
                if len(self._extra_item_list) > 0:
                    self._hide_scroll_panel()
                self._try_use_item(drug_item_id)
            elif self._cur_item_data:
                drug_item_id = self._cur_item_data.get('item_id')
                self._try_use_item(drug_item_id)
            return

    def _keyboard_open_throw_panel(self, msg, keycode):
        if not self._enable_scroll:
            if len(self._extra_item_list) > 0:
                self._show_scroll_panel()
                self.register_mouse_scroll_event()
                self._cur_sel_item_idx = len(self._extra_item_list) - 1
                self._set_extra_item_sel(self._cur_sel_item_idx, True)
        else:
            self._hide_scroll_panel()
            if self._cur_sel_item_idx is not None:
                self._set_extra_item_sel(self._cur_sel_item_idx, False)
                self._cur_sel_item_idx = None
        return

    def check_can_mouse_scroll(self):
        if not self.panel.isVisible():
            return False
        if not self._enable_scroll:
            return False
        if not self._can_interact():
            return False
        return True

    def _keyboard_item_scroll_up(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, self.ui_scroll_sensitivity, None)
            return

    def _keyboard_item_scroll_down(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, -self.ui_scroll_sensitivity, None)
            return

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        dist = -delta
        self._cur_mouse_dist += dist
        old_sel_drug_index = self._cur_sel_item_idx
        if abs(self._cur_mouse_dist) >= self.ui_scroll_sensitivity:
            changed_index = int(self._cur_mouse_dist / self.ui_scroll_sensitivity)
            changed_index = max(-1, changed_index)
            self._cur_mouse_dist = 0
            self._cur_sel_item_idx += changed_index
            self._cur_sel_item_idx %= len(self._extra_item_list)
        if old_sel_drug_index != self._cur_sel_item_idx:
            self._set_extra_item_sel(old_sel_drug_index, False)
            self._set_extra_item_sel(self._cur_sel_item_idx, True)

    def ui_vkb_custom_func(self):
        if self._enable_scroll:
            self._hide_scroll_panel()
            return True
        else:
            return False

    def on_hot_key_opened_state(self):
        super(ThrowRockerBaseUI, self).on_hot_key_opened_state()
        self._update_scroll_hotkey_nd()

    def on_hot_key_closed_state(self):
        super(ThrowRockerBaseUI, self).on_hot_key_closed_state()
        self._update_scroll_hotkey_nd()
        self._hide_scroll_panel()

    def register_mouse_scroll_event(self):
        super(ThrowRockerBaseUI, self).register_mouse_scroll_event()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def unregister_mouse_scroll_event(self):
        super(ThrowRockerBaseUI, self).unregister_mouse_scroll_event()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def _update_scroll_hotkey_nd(self):
        if not self._player:
            return
        sv_node = self.panel.sv_throw_list
        if global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            count = sv_node.GetItemCount()
            for idx in range(count):
                ui_item = sv_node.GetItem(idx)
                ui_item.temp_pc_use.setVisible(True)

        else:
            count = sv_node.GetItemCount()
            for idx in range(count):
                ui_item = sv_node.GetItem(idx)
                ui_item.temp_pc_use.setVisible(False)

    def on_finalize_panel(self):
        super(ThrowRockerBaseUI, self).on_finalize_panel()
        self._unbind_player()
        self.destroy_widget('custom_ui_com')
        self.destroy_widget('discard_widget')

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


class ThrowRockerUI(ThrowRockerBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_throw'