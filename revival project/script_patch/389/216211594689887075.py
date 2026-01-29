# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/MouseKeyboardSettingWidget.py
from __future__ import absolute_import
import six_ex
import six
import cc
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils import hot_key_utils
from logic.vscene.parts.keyboard.HotkeyConfigKeyboard import HotkeyConfigKeyboard, RECORD_RESULT_REPLACE, RECORD_RESULT_UNBIND
import game
from logic.vscene.parts.ctrl.VirtualCodeComplement import MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD
import logic.vscene.parts.ctrl.GamePyHook as game_hook
SET_BTN_NORMAL = 'gui/ui_res_2/pc/setting/btn_normal.png'
SET_BTN_HIGHLIGHT = 'gui/ui_res_2/pc/setting/btn__highlight.png'
SET_BTN_CHOOSE = 'gui/ui_res_2/pc/setting/btn_chose.png'
SET_BTN_NORMAL_FRAMES = [
 SET_BTN_NORMAL, SET_BTN_NORMAL, SET_BTN_NORMAL]
SET_BTN_HIGHLIGHT_FRAMES = [SET_BTN_HIGHLIGHT, SET_BTN_HIGHLIGHT, SET_BTN_HIGHLIGHT]
SET_BTN_CHOOSE_FRAMES = [SET_BTN_CHOOSE, SET_BTN_CHOOSE, SET_BTN_CHOOSE]

class MouseKeyboardSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(MouseKeyboardSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        super(MouseKeyboardSettingWidget, self).on_init_panel(**kwargs)
        self.config_keyboard = HotkeyConfigKeyboard()
        self.config_keyboard.set_record_finish_cb(self._on_finish_hotkey_record_cb)
        self.config_keyboard.set_conflict_against_vk_code_list_provider(self._conflict_against_vk_code_list_provider)
        self.need_config_hint = False
        self.can_click_config_btn = True
        self.set_btn_in_config = None
        self.configurable_set_btns = []
        self.hotkey_name_to_set_btn = {}
        self.prev_conflict_hotkeys = set()
        self._to_bind_hotkeys = {}
        self._init_mouse_listener()
        self.panel.nd_mouse.setVisible(False)
        self._refresh_view()
        return

    def on_before_destroy(self, **kwargs):
        self.config_keyboard.destroy()
        self.config_keyboard = None
        self.need_config_hint = False
        self.can_click_config_btn = True
        self.set_btn_in_config = None
        del self.configurable_set_btns[:]
        self.hotkey_name_to_set_btn.clear()
        self.prev_conflict_hotkeys.clear()
        self._to_bind_hotkeys.clear()
        super(MouseKeyboardSettingWidget, self).on_before_destroy(**kwargs)
        return

    def on_enter_page(self, **kwargs):
        super(MouseKeyboardSettingWidget, self).on_enter_page(**kwargs)
        self.config_keyboard.install()
        self.need_config_hint = True
        self._refresh_apply_btn()
        self._refresh_sync_server_btn_enable()

    def on_exit_page(self, **kwargs):
        super(MouseKeyboardSettingWidget, self).on_exit_page(**kwargs)
        self.config_keyboard.uninstall()

    def on_recover_default(self, **kwargs):
        super(MouseKeyboardSettingWidget, self).on_recover_default(**kwargs)
        self._to_bind_hotkeys.clear()
        hot_key_utils.restore_all_hotkey_bindings()
        self._refresh_view()
        self._refresh_apply_btn()
        self._refresh_sync_server_btn_enable()

    def has_apply_btn(self):
        return True

    def should_btn_sync_server_enabled(self):
        return not self.have_pending_key_bindings() and hot_key_utils.is_hotkey_binding_out_of_sync_with_server()

    def on_sync_to_server(self, **kwargs):
        hot_key_utils.sync_hotkey_binding_to_server()
        self._refresh_sync_server_btn_enable()

    def on_apply(self, **kwargs):
        if self.have_pending_key_bindings():
            for hot_key_name, vk_code_list in six.iteritems(self._to_bind_hotkeys):
                hot_key_utils.bind_hotkey(hot_key_name, vk_code_list, False)

            hot_key_utils.reregister_all_key_bindings()
            self._to_bind_hotkeys.clear()
            self._refresh_apply_btn()
            self._refresh_sync_server_btn_enable()

    def _refresh_apply_btn(self):
        self._set_apply_btn_enabled(self.have_pending_key_bindings())

    def have_pending_key_bindings(self):
        return bool(self._to_bind_hotkeys)

    def _refresh_view(self):
        hotkey_catalog = hot_key_utils.get_sorted_hotkey_catalog()
        del self.configurable_set_btns[:]
        self.hotkey_name_to_set_btn.clear()
        self.panel.list_setting.SetInitCount(len(hotkey_catalog))
        for idx, cat in enumerate(hotkey_catalog):
            item = self.panel.list_setting.GetItem(idx)
            item.key_class.title.SetString(hot_key_utils.get_hotkey_category_name(cat))
            item.key_class.icon.SetDisplayFrameByPath('', hot_key_utils.get_hotkey_category_icon_path(cat))
            hotkey_names = hot_key_utils.get_configurable_hotkeys(cat)
            item.list_keyboard.SetInitCount(len(hotkey_names))
            for _idx, hotkey_name in enumerate(hotkey_names):
                if hotkey_name in self._to_bind_hotkeys:
                    vk_code_list = self._to_bind_hotkeys[hotkey_name]
                    vk_name_list = hot_key_utils.vk_code_list_to_vk_name_list(vk_code_list)
                else:
                    vk_name_list = hot_key_utils.get_hotkey_binding(hotkey_name)
                key_item = item.list_keyboard.GetItem(_idx)
                self.hotkey_name_to_set_btn[hotkey_name] = key_item
                key_item.lab_func.SetString(hot_key_utils.get_hot_key_fun_desc(hotkey_name))
                key_item.img_notice.setVisible(False)
                self._refresh_single_set_btn_core(key_item, vk_name_list)
                if hot_key_utils.is_hotkey_configurable(hotkey_name):
                    key_item.btn_set.SetFrames('', SET_BTN_NORMAL_FRAMES, True, None)
                    self.configurable_set_btns.append(key_item.btn_set)
                else:
                    key_item.btn_set.ClearAllFrames()
                key_item.btn_set.EnableCustomState(True)

                @key_item.btn_set.unique_callback()
                def OnClick(btn, touch, hotkey_name=hotkey_name):
                    if not self.can_click_config_btn:
                        return
                    else:
                        if not hot_key_utils.is_hotkey_configurable(hotkey_name):
                            return
                        if not self.config_keyboard.is_recording():
                            ok = self.config_keyboard.start_recording(hotkey_name)
                            if not ok:
                                return
                            self._clear_prev_conflict_marks()
                            self.set_btn_in_config = btn
                            btn.SetFrames('', SET_BTN_CHOOSE_FRAMES, True, None)
                            if self.need_config_hint:
                                if hot_key_utils.is_hot_key_unset(hotkey_name):
                                    hint_id = 920738
                                else:
                                    hint_id = 920739
                                global_data.game_mgr.show_tip(hint_id)
                                self.need_config_hint = False
                        return

            w, _ = item.GetContentSize()
            _, h_title = item.key_class.GetContentSize()
            _, h_key_list = item.list_keyboard.GetContentSize()
            h = h_title + h_key_list
            item.SetContentSize(w, h)
            item.key_class.ReConfPosition()
            item.list_keyboard.ReConfPosition()

        self.panel.list_setting.RefreshItemPos()
        w, _ = self.panel.GetContentSize()
        if self.panel.nd_mouse.isVisible():
            _, h_title = self.panel.nd_mouse.GetContentSize()
        else:
            h_title = 0
        _, h_key_list = self.panel.list_setting.GetContentSize()
        h = h_title + h_key_list + 40
        self.panel.SetContentSize(w, h)
        self.panel.nd_mouse.ReConfPosition()
        self.panel.nd_keyboard.ReConfPosition()
        if not self.panel.nd_mouse.isVisible():
            x, y = self.panel.nd_keyboard.GetPosition()
            y += self.panel.nd_mouse.GetContentSize()[1]
            self.panel.nd_keyboard.SetPosition(x, y)
        self.parent.panel.content_bar.page.SetContainer(self.panel)
        self.parent.panel.content_bar.page.SetInnerContentSize(w, h)
        self.parent.panel.content_bar.page.ScrollToTop()
        self.parent.adjust_container_pos()
        return

    def _get_key_item(self, hotkey_name):
        if hotkey_name in self.hotkey_name_to_set_btn:
            key_item = self.hotkey_name_to_set_btn[hotkey_name]
            if key_item and key_item.isValid():
                return key_item
            else:
                return None

        else:
            return None
        return None

    def _refresh_single_set_btn(self, hotkey_name, vk_name_list):
        key_item = self._get_key_item(hotkey_name)
        if key_item is None:
            return
        else:
            self._refresh_single_set_btn_core(key_item, vk_name_list)
            return

    def _refresh_single_set_btn_core(self, key_item, vk_name_list):
        mouse_only, vk_name = hot_key_utils.has_mouse_btn_only_raw(vk_name_list)
        if mouse_only:
            mouse_p = hot_key_utils.get_vk_icon_path(vk_name)
            if mouse_p:
                key_item.img_mouse.setVisible(True)
                key_item.img_mouse.SetDisplayFrameByPath('', mouse_p)
                key_item.lab_key.setVisible(False)
                return
        key_item.img_mouse.setVisible(False)
        key_item.lab_key.setVisible(True)
        text = hot_key_utils.get_hot_key_short_display_name_ex_raw(vk_name_list)
        key_item.lab_key.SetString(text)

    def _init_mouse_listener(self):
        listener = cc.EventListenerMouse.create()
        listener.setOnMouseMoveCallback(self._on_mouse_move)
        listener.setOnMouseDownCallback(self._on_mouse_down)
        listener.setOnMouseUpCallback(self._on_mouse_up)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.panel.get())

    def _conflict_against_vk_code_list_provider(self, hotkey_name):
        if hotkey_name in self._to_bind_hotkeys:
            return self._to_bind_hotkeys[hotkey_name]
        return hot_key_utils.get_hotkey_binding_vk_code_list(hotkey_name)

    def _on_finish_hotkey_record_cb(self, result, hotkey_name, vk_code_list, **extras):
        if self.set_btn_in_config and self.set_btn_in_config.isValid():
            self.set_btn_in_config.SetFrames('', SET_BTN_NORMAL_FRAMES, True, None)
        self.set_btn_in_config = None
        self.can_click_config_btn = False
        global_data.game_mgr.post_exec(self._reset_can_click_config_flag)
        if result == RECORD_RESULT_REPLACE:
            if hotkey_name in self._to_bind_hotkeys:
                cur_binding = self._to_bind_hotkeys[hotkey_name]
            else:
                vk_name_list = hot_key_utils.get_hotkey_binding(hotkey_name)
                cur_binding = hot_key_utils.vk_name_list_to_vk_code_list(vk_name_list)
            if cur_binding == vk_code_list:
                return
        change_dict = {}
        if result == RECORD_RESULT_REPLACE:
            change_dict[hotkey_name] = vk_code_list
        elif result == RECORD_RESULT_UNBIND:
            change_dict[hotkey_name] = game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST
        conflict_hotkeys = extras.get('conflict_hotkeys', None)
        self.prev_conflict_hotkeys.clear()
        if conflict_hotkeys:
            self.prev_conflict_hotkeys.add(hotkey_name)
            vk_name_list = hot_key_utils.vk_code_list_to_vk_name_list(vk_code_list)
            format_txt = get_text_by_id(920740)
            key_name_text = hot_key_utils.get_hot_key_short_display_name_ex_raw(vk_name_list)
            for conflict_hotkey_name in conflict_hotkeys:
                change_dict[conflict_hotkey_name] = game_hook.PC_HOTKEY_CUSTOM_UNBIND_VK_CODE_LIST
                hotkey_name_text = hot_key_utils.get_hot_key_fun_desc(conflict_hotkey_name)
                tips_text = format_txt.format(key_name=key_name_text, hotkey_name=hotkey_name_text)
                global_data.game_mgr.show_tip(tips_text)
                self.prev_conflict_hotkeys.add(conflict_hotkey_name)

        self._to_bind_hotkeys.update(change_dict)
        for hotkey_name in six_ex.keys(self._to_bind_hotkeys):
            vk_code_list = self._to_bind_hotkeys[hotkey_name]
            effective_vk_name_list = hot_key_utils.get_hotkey_binding(hotkey_name)
            effective_vk_code_list = hot_key_utils.vk_name_list_to_vk_code_list(effective_vk_name_list)
            if effective_vk_code_list == vk_code_list:
                del self._to_bind_hotkeys[hotkey_name]

        for conflict_hotkey_name in self.prev_conflict_hotkeys:
            self._set_conflict(conflict_hotkey_name, True)

        for to_refresh_hotkey_name in change_dict:
            dst_vk_code_list = change_dict[to_refresh_hotkey_name]
            dst_vk_name_list = hot_key_utils.vk_code_list_to_vk_name_list(dst_vk_code_list)
            self._refresh_single_set_btn(to_refresh_hotkey_name, dst_vk_name_list)

        self._refresh_apply_btn()
        self._refresh_sync_server_btn_enable()
        return

    def _set_conflict(self, hotkey_name, enable):
        key_item = self._get_key_item(hotkey_name)
        if key_item is None:
            return
        else:
            key_item.img_notice.setVisible(enable)
            return

    def _clear_prev_conflict_marks(self):
        for conflict_hotkey_name in self.prev_conflict_hotkeys:
            self._set_conflict(conflict_hotkey_name, False)

    def _reset_can_click_config_flag(self):
        if self.panel and self.panel.isValid():
            self.can_click_config_btn = True

    def _on_mouse_down(self, event):
        self._on_mouse_msg(event, game.MSG_MOUSE_DOWN)

    def _on_mouse_up(self, event):
        self._on_mouse_msg(event, game.MSG_MOUSE_UP)

    def _on_mouse_move(self, event):
        if self.configurable_set_btns:
            wpos = event.getLocationInView()
            from common.utils.cocos_utils import neox_pos_to_cocos
            wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
            for set_btn in self.configurable_set_btns:
                if not set_btn or not set_btn.isValid():
                    continue
                if self.set_btn_in_config == set_btn:
                    continue
                if set_btn.IsPointIn(wpos):
                    set_btn.SetFrames('', SET_BTN_HIGHLIGHT_FRAMES, True, None)
                else:
                    set_btn.SetFrames('', SET_BTN_NORMAL_FRAMES, True, None)

        return

    def _on_mouse_msg(self, event, msg):
        if self.set_btn_in_config:
            wpos = event.getLocationInView()
            from common.utils.cocos_utils import neox_pos_to_cocos
            wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
            if self.set_btn_in_config.IsPointIn(wpos):
                mouse_vk_code = None
                mouse_type = event.getMouseButton()
                if mouse_type == 0:
                    mouse_vk_code = game.MOUSE_BUTTON_LEFT
                elif mouse_type == 1:
                    mouse_vk_code = game.MOUSE_BUTTON_RIGHT
                elif mouse_type == 2:
                    mouse_vk_code = game.MOUSE_BUTTON_MIDDLE
                elif mouse_type == 3:
                    mouse_vk_code = MOUSE_BUTTON_BACK
                elif mouse_type == 4:
                    mouse_vk_code = MOUSE_BUTTON_FORWARD
                if mouse_vk_code is not None:
                    if self.config_keyboard and self.config_keyboard.is_recording():
                        self.config_keyboard.feed_stream(msg, mouse_vk_code)
            elif game.MSG_MOUSE_UP == msg and self.panel.IsPointIn(wpos):
                self.config_keyboard.abort_recording()
        return