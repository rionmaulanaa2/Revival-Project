# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/InputBox.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from cocosui import cc, ccui, ccs
import common.const.uiconst
import common.utilities
import game3d
from common.utils.cocos_utils import ccc3bToHex
from logic.gcommon.common_utils.local_text import get_text_by_id
g_special_devices = [
 'asus_x00qd']
g_full_screen_inputbox_devices = [
 'sm-a700fd', 'pixel 3', 'pixel 2']
g_waterfall_screen_y_offset_devices = {
 'lio-al00', 'lio-an00', 'noh-an00', 'nop-an00', 'mi 9'}
g_save_vkb_height = -1

class InputBox(object):

    def __init__(self, pnl_input, max_length=50, send_callback=None, cancel_callback=None, input_callback=None, placeholder=None, start_input_cb=None, max_input_cb=None, clear_btn_cb=None, need_sp_length_func=False, detach_after_enter=True, detach_callback=None):
        self._pnl_input = pnl_input
        self._max_length = max_length
        self._send_callback = send_callback
        self._detach_callback = detach_callback
        self._cancel_callback = cancel_callback
        self._input_callback = input_callback
        self._start_input_cb = start_input_cb
        self._max_input_cb = max_input_cb
        self._clear_btn_cb = clear_btn_cb
        self._input_box = self._pnl_input.layerout.input_box
        if placeholder != None:
            self._placeholder = placeholder if 1 else get_text_by_id(2137).format(num=max_length)
            self._input_box.SetPlaceHolder(self._placeholder)
            self._input_pos_x, self._input_pos_y = self._input_box.GetPosition()
            self._size_width = self._pnl_input.getContentSize().width
            self._enable_input = True
            self.is_binded_event = False
            self._is_attach_with_ime = False
            self.need_sp_length_func = need_sp_length_func
            self._detach_after_enter = detach_after_enter
            self._input_box_x_offset = 0.0
            self._input_box_y_offset = 0.0
            self._input_type = 0
            size = self._pnl_input.getContentSize()
            self._pnl_input.layerout.input_box.setMaxLengthEnabled(True)
            self._pnl_input.layerout.input_box.setMaxLength(max_length + 1)
            self.cal_input_box_offset()
            self.cal_resolution_parameter()
            self._replace_key = ''
            self._replace_text = ''
            self.cur_scene_rotation = None
            self.cur_input_box_height = 0
            self.init_popup_panel_keyborad()
            self.is_full_screen_inputbox() or self.set_enable_pop_up_keyboard(True)
        else:
            self.set_enable_pop_up_keyboard(False)
        self._pnl_input_bottom_wpos = None
        self.init_ime_callback()
        self.process_event(True)

        @self._input_box.callback()
        def OnEditChanged(input_box, text):
            if global_data.test_pc_mode:
                print('input_box:', input_box, text, text.endswith('\n'), text.endswith('\r'))
            if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc:
                if text.endswith('\n') or text.endswith('\r'):
                    text = text.rstrip('\n')
                    text = text.rstrip('\r')
                    self.set_text(text)
                    if self._detach_after_enter:
                        self.detachWithIME()
                    elif not self.is_enable_popup_panel_keyboard:
                        self._input_box.OnEditReturn(self.get_text())
                    return
                text = self.exclude_special_characters(text)
                self._input_box.SetText(text)
            if self._clear_btn_cb and text:
                self._pnl_input.btn_clear.setVisible(True)
            else:
                self._pnl_input.btn_clear.setVisible(False)
            length = self.get_text_len(text)
            if length > self._max_length:
                text = self.get_sub_utf8_text(text)
                self._input_box.SetText(text)
                if self._max_input_cb:
                    self._max_input_cb(length, self._max_length)
            self.adjust_text_input()
            if self._input_callback:
                self._input_callback(text)

        @self._input_box.callback()
        def OnEditReturn(input_box, text):
            if global_data.test_pc_mode:
                print('input_box OnEditReturn:', input_box, text, text.endswith('\n'), text.endswith('\r'))
            if self._send_callback:
                self._send_callback()

        @self._pnl_input.touch_layer.unique_callback()
        def OnClick(input_box, touch):
            if not self._enable_input:
                return
            if self._start_input_cb:
                self._start_input_cb()
            if self.is_enable_popup_panel_keyboard:
                self.show_vkb()
            else:
                self._input_box.attachWithIME(False)
                if self._is_attach_with_ime:
                    if hasattr(self._input_box, 'setCursorFromPoint') and self._input_box.setCursorFromPoint and touch:
                        self._input_box.setCursorFromPoint(touch.getLocation())

        if clear_btn_cb:

            @self._pnl_input.touch_layer.btn_clear.callback()
            def OnClick(*args):
                self._input_box.SetText('')
                self._pnl_input.touch_layer.OnClick(None)
                self._pnl_input.btn_clear.setVisible(False)
                self._clear_btn_cb()
                return

        self._input_box.SetText('1')
        self._input_box.SetText('')
        self.adjust_text_input()
        global_data.emgr.pc_paste_text += self._on_pc_paste_text
        return

    def cal_input_box_offset(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and global_data.channel and global_data.channel.get_os_ver() == '8.0.0':
            device_name = global_data.deviceinfo.get_device_model_name()
            if device_name in g_special_devices:
                self._input_box_x_offset = global_data.really_window_size[0] * 0.033
        device_name = global_data.deviceinfo.get_device_model_name()
        if device_name in g_waterfall_screen_y_offset_devices:
            self._input_box_y_offset = global_data.really_window_size[1] * 0.02

    def is_full_screen_inputbox(self):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            device_name = global_data.deviceinfo.get_device_model_name()
            if device_name in g_full_screen_inputbox_devices:
                return True
            if 'vivo' == global_data.deviceinfo.get_device_manufacturer().lower():
                return not global_data.feature_mgr.is_vivo_inputview_wrong_position_fixed()
        return False

    def cal_resolution_parameter(self):
        self.design_size = cc.Director.getInstance().getOpenGLView().getDesignResolutionSize()
        if game3d.PLATFORM_WIN32 == game3d.get_platform():
            orig_width, orig_height, _, _, _ = game3d.get_window_size()
        else:
            orig_width = global_data.really_window_size[0]
            orig_height = global_data.really_window_size[1]
        self.design_scale_y = self.design_size.height / float(orig_height)
        self.design_scale_x = self.design_size.width / float(orig_width)

    def enable_input(self, enable):
        self._enable_input = enable

    def get_text(self):
        text = self._input_box.getString()
        return text

    def set_text(self, text):
        self._input_box.setString(text)
        self.adjust_text_input()

    def set_text_no_refresh(self, text):
        self._input_box.setString(text)

    def set_replace_text(self, replace_key, replace_text):
        self._replace_key = replace_key
        self._replace_text = replace_text

    def get_replace_key_and_text(self):
        return (
         self._replace_key, self._replace_text)

    def get_replace_key(self):
        return self._replace_key

    def clean_replace_text(self):
        self._replace_key = ''
        self._replace_text = ''

    def change_input_width(self):
        self._size_width = self._pnl_input.getContentSize().width
        self._pnl_input.ChildResizeAndPosition()
        text = self.get_text()
        if text:
            self._input_box.SetText('')
            self.set_text(text)
        else:
            self._input_box.SetText('1')
            self.set_text('')

    def adjust_text_input(self):
        width, _ = self._input_box.GetContentSize()
        if width > self._size_width and self._input_box.getString() != '':
            if game3d.get_platform() == game3d.PLATFORM_WIN32 and hasattr(self._input_box, 'getCursorWorldPosition') and self._input_box.getCursorWorldPosition and self._is_attach_with_ime:
                last_pos_x = self._input_box.getPosition().x + width
                if last_pos_x < self._size_width:
                    self._input_box.setPosition(cc.Vec2(self._input_pos_x - (width - self._size_width), self._input_pos_y))
                world_distance = self.get_cursor_bounding_box_offset()
                if not world_distance:
                    return
                org = self._input_box.getParent().convertToNodeSpace(cc.Vec2(0, 0))
                ldistance = self._input_box.getParent().convertToNodeSpace(cc.Vec2(world_distance, 0))
                old_pos = self._input_box.getPosition()
                self._input_box.setPosition(cc.Vec2(old_pos.x - (ldistance.x - org.x), old_pos.y))
            else:
                self._input_box.setPosition(cc.Vec2(self._input_pos_x - (width - self._size_width), self._input_pos_y))
        else:
            self._input_box.setPosition(cc.Vec2(self._input_pos_x, self._input_pos_y))

    def detachWithIME(self, with_send_callback=True):
        if with_send_callback:
            if not self.is_enable_popup_panel_keyboard:
                self._input_box.OnEditReturn(self.get_text())
        self._input_box.didNotSelectSelf()

    def detachWithIMEWithSendCallback(self):
        self._input_box.OnEditReturn(self.get_text())
        self._input_box.didNotSelectSelf()

    def setPasswordEnabled(self, enable):
        self._input_box.setPasswordEnabled(enable)

    def setCustomBgEnable(self, enable):
        self._pnl_input.img_bottom.setVisible(not enable)

    def destroy(self):
        if self._is_attach_with_ime:
            self._input_box.didNotSelectSelf()
            self.on_detach_with_ime()
        if self.is_keyboard_in_pop:
            game3d.hide_inputview()
            self.is_keyboard_in_pop = False
        self._send_callback = None
        self._detach_callback = None
        self._cancel_callback = None
        self._input_callback = None
        self._start_input_cb = None
        self.process_vkb_event(False)
        self.process_event(False)
        self.set_rise_widget(None)
        global_data.emgr.pc_paste_text -= self._on_pc_paste_text
        return

    def hide(self):
        if self.is_keyboard_in_pop:
            game3d.hide_inputview()
            self.is_keyboard_in_pop = False

    def init_popup_panel_keyborad(self):
        self.is_enable_popup_panel_keyboard = False
        self.is_binded_vkb_event = False
        self.is_keyboard_in_pop = False
        scale = self._input_box.GetNodeToWorldScale()
        self._scale_x = scale.x
        self._scale_y = scale.y
        _pnl_input = self._pnl_input
        size = _pnl_input.getContentSize()
        pos0 = _pnl_input.convertToWorldSpace(cc.Vec2(0, 0))
        pos3 = _pnl_input.convertToWorldSpace(cc.Vec2(size.width, size.height))
        self._world_height = abs(pos3.y - pos0.y)
        dpi = game3d.get_window_dpi()[1]
        font_size = self._input_box.getFontSize() * 1.0
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            self._ui_font_size = font_size * self._scale_y / dpi * 163.0 / self.design_scale_y
        else:
            self._ui_font_size = font_size * self._scale_y / self.design_scale_y
        self._rise_widget = None
        self._widget_pos = None
        return

    def set_enable_pop_up_keyboard(self, is_enable):
        if game3d.get_platform() == game3d.PLATFORM_ANDROID or game3d.get_platform() == game3d.PLATFORM_IOS:
            self.is_enable_popup_panel_keyboard = is_enable

    def set_rise_widget(self, _rise_widget, _widget_pos=None, _pnl_input_buttom_wpos=None):
        self._rise_widget = _rise_widget
        if self._rise_widget:
            if not _widget_pos:
                self._widget_pos = self._rise_widget.getPosition()
            else:
                self._widget_pos = _widget_pos
            if _pnl_input_buttom_wpos:
                self._pnl_input_bottom_wpos = _pnl_input_buttom_wpos
            else:
                self._pnl_input_bottom_wpos = self._pnl_input.ConvertToWorldSpacePercentage(0, 0)
        else:
            self._widget_pos = None
        return

    def show_vkb(self):
        s = self.get_text()
        is_hint = False
        c_4b = self._input_box.GetTextColor()
        color = ccc3bToHex(c_4b)
        self.process_vkb_event(True)
        x, y, w, h = self.get_inputview_xywh()
        game3d.show_inputview(s, self._input_type, self.on_finish_input, self.on_input_change, is_hint, int(x), int(y), int(w), int(h), self._input_box.getFontName(), float(self._ui_font_size), six_ex.long_type(color))
        self.is_keyboard_in_pop = True
        self._input_box.stopAllActions()
        act = cc.Sequence.create([cc.Hide.create()])
        self._input_box.runAction(act)
        self.cur_scene_rotation = game3d.get_rotation()

    def on_vkb_show(self, phy_window_rect):
        global g_save_vkb_height
        if not (self._pnl_input and self._pnl_input.isValid()):
            return
        else:
            if self.cur_scene_rotation is not None and self.cur_scene_rotation != game3d.get_rotation():
                game3d.hide_inputview()
                return
            if phy_window_rect:
                if phy_window_rect[3] > g_save_vkb_height:
                    g_save_vkb_height = phy_window_rect[3]
                height = phy_window_rect[3]
                if self.cur_input_box_height == height:
                    return
                self.cur_input_box_height = height
                self.set_vkb_height(height)
            return

    def set_vkb_height(self, vkb_height, is_delay=False):
        print('!!!!set_vkb_height=%s' % vkb_height)
        self._rise_panel(vkb_height)
        x, y, w, h = self.get_inputview_xywh()
        game3d.set_inputview_location(int(x), int(y), int(w), int(h))

    def _rise_panel(self, vkb_height):
        if self._rise_widget is not None and self._rise_widget.get() and self._rise_widget.isValid():
            if self._pnl_input_bottom_wpos:
                input_bottom_wpos = self._pnl_input_bottom_wpos
            else:
                input_bottom_wpos = self._pnl_input.ConvertToWorldSpacePercentage(0, 0)
            height_w_offset = vkb_height * self.design_scale_y - input_bottom_wpos.y + self._world_height / 2
            if height_w_offset > 0:
                w_parent = self._rise_widget.getParent()
                height_l_offset = w_parent.convertToNodeSpace(cc.Vec2(self._widget_pos.x, height_w_offset)).y - w_parent.convertToNodeSpace(cc.Vec2(self._widget_pos.x, 0)).y
                if self._pnl_input_bottom_wpos:
                    self._rise_widget.setPosition(self._widget_pos.x, height_l_offset + self._widget_pos.y)
                else:
                    lpos = self._rise_widget.getPosition()
                    self._rise_widget.setPosition(self._widget_pos.x, height_l_offset + lpos.y)
        return

    def on_input_change(self, text):
        if not self._input_box.isValid():
            return
        if text == self.get_text():
            return
        length = self.get_text_len(text)
        if length > self._max_length:
            text = self.get_sub_utf8_text(text)
            self._input_box.SetText(text)
            if self._max_input_cb:
                self._max_input_cb(length, self._max_length)
        self._input_box.SetText(text)
        self.adjust_text_input()
        if self._input_callback:
            self._input_callback(text)

    def on_finish_input(self, text, is_confirm, is_reset_pos=True):
        if not (self._pnl_input and self._pnl_input.isValid()):
            return
        else:
            length = self.get_text_len(text)
            if length > self._max_length:
                text = self.get_sub_utf8_text(text)
            if game3d.get_platform() == game3d.PLATFORM_ANDROID or game3d.get_platform() == game3d.PLATFORM_IOS:
                self.set_text(text)
                self._input_box.setVisible(True)
                if self._send_callback and is_confirm:
                    self._send_callback()
                elif self._cancel_callback:
                    self._cancel_callback()
            else:
                self.set_text(text)
                self._input_box.setVisible(True)
                if self._send_callback:
                    self._send_callback()
            if self._rise_widget and self._rise_widget.isValid() and self._widget_pos and is_reset_pos:
                self._rise_widget.setPosition(self._widget_pos)
            self.is_keyboard_in_pop = False
            self.process_vkb_event(False)
            self.cur_scene_rotation = None
            self.cur_input_box_height = None
            if self._clear_btn_cb and text:
                self._pnl_input.btn_clear.setVisible(True)
            else:
                self._pnl_input.btn_clear.setVisible(False)
            return

    def process_vkb_event(self, is_bind):
        if is_bind:
            if not self.is_binded_vkb_event:
                global_data.emgr.kb_on_vkb_event += self.on_vkb_show
                self.is_binded_vkb_event = True
        elif self.is_binded_vkb_event:
            global_data.emgr.kb_on_vkb_event -= self.on_vkb_show
            self.is_binded_vkb_event = False

    def process_event(self, is_bind):
        if is_bind:
            if not self.is_binded_event:
                global_data.emgr.resolution_changed += self.on_resolution_changed
                global_data.emgr.mouse_cursor_lock_event += self.on_cursor_locked
                global_data.emgr.all_ui_visibility_changed_event += self.on_all_ui_visibility_changed
                self.is_binded_event = True
        elif self.is_binded_event:
            global_data.emgr.resolution_changed -= self.on_resolution_changed
            global_data.emgr.mouse_cursor_lock_event -= self.on_cursor_locked
            global_data.emgr.all_ui_visibility_changed_event -= self.on_all_ui_visibility_changed
            self.is_binded_event = False

    def get_inputview_xywh(self):
        _pnl_input = self._pnl_input
        size = _pnl_input.getContentSize()
        pos0 = _pnl_input.convertToWorldSpace(cc.Vec2(0, 0))
        pos1 = _pnl_input.convertToWorldSpace(cc.Vec2(size.width, 0))
        pos2 = _pnl_input.convertToWorldSpace(cc.Vec2(0, size.height))
        pos3 = _pnl_input.convertToWorldSpace(cc.Vec2(size.width, size.height))
        min_posy = min(pos0.y, pos1.y, pos2.y, pos3.y)
        max_posy = max(pos0.y, pos1.y, pos2.y, pos3.y)
        min_posx = min(pos0.x, pos1.x, pos2.x, pos3.x)
        max_posx = max(pos0.x, pos1.x, pos2.x, pos3.x)
        x = min_posx / self.design_scale_x + self._input_box_x_offset
        y = (self.design_size.height - max_posy) / self.design_scale_y + self._input_box_y_offset
        w = (max_posx - min_posx) / self.design_scale_x
        h = (max_posy - min_posy) / self.design_scale_y
        return (
         int(x), int(y), int(w), int(h))

    def get_text_len(self, text):
        if self.need_sp_length_func:
            length = common.utilities.get_utf8_length_special(text)
        else:
            length = common.utilities.get_utf8_length(text)
        return length

    def get_sub_utf8_text(self, text):
        if self.need_sp_length_func:
            _, text = common.utilities.sub_utf8_special(text, self._max_length)
        else:
            _, text = common.utilities.sub_utf8(text, self._max_length)
        return text

    def init_ime_callback(self):
        self._input_box.addEventListener(self.event_callback)

    def on_resolution_changed(self):
        if not self._input_box or not self._input_box.isValid():
            return
        self.cal_resolution_parameter()
        if self._is_attach_with_ime:
            self.update_ime_pos()
        original_txt = self.get_text()
        self._input_box.SetText('1')
        self._input_box.SetText(original_txt)
        self.adjust_text_input()

    def on_cursor_locked(self, is_lock):
        if is_lock and self._is_attach_with_ime:
            if self._input_box and self._input_box.isValid():
                self._input_box.didNotSelectSelf()

    def check_inputbox_should_release(self):
        if not self._pnl_input.IsVisible() and self._is_attach_with_ime:
            if self._input_box and self._input_box.isValid():
                self._input_box.didNotSelectSelf()

    def on_all_ui_visibility_changed(self):
        if not (self._pnl_input.isValid() and self._pnl_input.IsVisible()):
            self.hide()

    def update_ime_pos(self):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            x, y, w, h = self.get_inputview_xywh()
            desktop_sz_w, desktop_sz_h = game3d.get_desktop_size()
            posx, posy = game3d.get_window_pos()
            import nxapp
            if hasattr(nxapp, 'set_imm_compositionwindow_pos'):
                SUPPOSED_COMPOSITION_HEIGHT = 100
                if posy + y + h < desktop_sz_h - SUPPOSED_COMPOSITION_HEIGHT:
                    nxapp.set_imm_compositionwindow_pos(x, y + h)
                else:
                    nxapp.set_imm_compositionwindow_pos(x, int(y - 1.5 * h))

    def event_callback(self, textfield, event_type):
        if event_type == ccui.TEXTFIELD_EVENTTYPE_ATTACH_WITH_IME:
            self._is_attach_with_ime = True
            global_data.is_attach_with_ime = True
            global_data.emgr.textfield_eventtype_attach_with_ime_event.emit()
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.on_ime_open()
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.switch_imm_switch(True)
            self.update_ime_pos()
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                self._pnl_input.touch_layer.stopAllActions()
                self._pnl_input.touch_layer.runAction(cc.RepeatForever.create(cc.Sequence.create([
                 cc.DelayTime.create(1.0),
                 cc.CallFunc.create(self.check_inputbox_should_release)])))
        elif event_type == ccui.TEXTFIELD_EVENTTYPE_DETACH_WITH_IME:
            self.on_detach_with_ime()
        elif event_type == ccui.TEXTFIELD_EVENTTYPE_INSERT_TEXT:
            self._input_box.OnEditChanged(self.get_text())
        elif event_type == ccui.TEXTFIELD_EVENT_DELETE_BACKWARD:
            self._input_box.OnEditChanged(self.get_text())
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            if hasattr(ccui, 'TEXTFIELD_EVENT_UPDATE_CURSOR') and event_type == ccui.TEXTFIELD_EVENT_UPDATE_CURSOR:
                self.adjust_text_input()

    def on_detach_with_ime(self):
        self._pnl_input.touch_layer.stopAllActions()
        self._is_attach_with_ime = False
        global_data.is_attach_with_ime = False
        if self._detach_callback:
            self._detach_callback()
        self.adjust_text_input()
        global_data.emgr.textfield_eventtype_detach_with_ime_event.emit()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.on_ime_close()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.switch_imm_switch(False)

    def get_cursor_bounding_box_offset(self):
        if hasattr(self._input_box, 'getCursorWorldPosition') and self._input_box.getCursorWorldPosition:
            world_pos = self._input_box.getCursorWorldPosition()
            _pnl_input = self._pnl_input
            size = _pnl_input.getContentSize()
            pos0 = _pnl_input.convertToWorldSpace(cc.Vec2(0, 0))
            pos1 = _pnl_input.convertToWorldSpace(cc.Vec2(size.width, 0))
            pos2 = _pnl_input.convertToWorldSpace(cc.Vec2(0, size.height))
            pos3 = _pnl_input.convertToWorldSpace(cc.Vec2(size.width, size.height))
            cursor_width = 1
            min_posx = min(pos0.x, pos1.x, pos2.x, pos3.x) + cursor_width
            max_posx = max(pos0.x, pos1.x, pos2.x, pos3.x) - cursor_width
            if max_posx >= world_pos.x >= min_posx:
                return 0
            else:
                if world_pos.x < min_posx:
                    return world_pos.x - min_posx
                return world_pos.x - max_posx

        else:
            return 0

    @classmethod
    def exclude_special_characters(cls, utf8_str):
        exclude_byte_indices = set()
        i = 0
        j = len(utf8_str)
        while i < j:
            k = ord(utf8_str[i])
            if k <= 127:
                if k <= 31 or k == 127:
                    if not (k == 10 or k == 13):
                        exclude_byte_indices.add(i)
                i += 1
            elif k < 224:
                i += 2
            elif k < 240:
                i += 3
            elif k < 248:
                i += 4
            elif k < 252:
                i += 5
            else:
                i += 6

        return ''.join((b for idx, b in enumerate(utf8_str) if idx not in exclude_byte_indices))

    @classmethod
    def splice_multi_line_text(cls, utf8_str):
        ret_str = ''
        i = 0
        j = len(utf8_str)
        while i < j:
            k = ord(utf8_str[i])
            if k <= 127:
                if k == 13:
                    if i + 1 != j and i + 2 != j:
                        pass
                    else:
                        ret_str += utf8_str[i]
                elif k == 10:
                    if i + 1 != j:
                        ret_str += '\\n'
                    else:
                        ret_str += utf8_str[i]
                else:
                    ret_str += utf8_str[i]
                i += 1
            elif k < 224:
                ret_str += utf8_str[i:i + 2]
                i += 2
            elif k < 240:
                ret_str += utf8_str[i:i + 3]
                i += 3
            elif k < 248:
                ret_str += utf8_str[i:i + 4]
                i += 4
            elif k < 252:
                ret_str += utf8_str[i:i + 5]
                i += 5
            else:
                ret_str += utf8_str[i:i + 6]
                i += 6

        return ret_str

    def _on_pc_paste_text(self, text):
        text = self.splice_multi_line_text(text)
        if not self._is_attach_with_ime:
            return
        self._input_box.InsertText(text)

    def set_max_length(self, max_length):
        self._max_length = max_length
        self._pnl_input.layerout.input_box.setMaxLength(max_length + 1)
        self._placeholder = get_text_by_id(2137).format(num=max_length)
        self._input_box.SetPlaceHolder(self._placeholder)

    def set_input_type(self, input_type):
        self._input_type = input_type