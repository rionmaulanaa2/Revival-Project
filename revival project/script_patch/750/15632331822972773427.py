# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagUIPC.py
from __future__ import absolute_import
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gutils import template_utils
from .BagBaseUI import BagBaseUI
from .BagHumanWeaponWidget import BagHumanWeaponWidget
from .BagHumanItemWidget import BagHumanItemWidget
from .BagMechaModuleWidget import BagMechaModuleWidget
from .BagMechaItemWidget import BagMechaItemWidget
import cc
SLIDER_BTN_W_NORMAL = 4
SLIDER_BTN_H_BIG = 8
BAG_UI_TYPE_OTHERS = -1
BAG_UI_TYPE_GUN = 0
BAG_UI_TYPE_ITEM = 1
BAG_UI_TYPE_CLOTHING = 2
HUMAN_ITEM_HEIGHT = 78

class BagUIPC(BagBaseUI):
    PANEL_CONFIG_NAME = 'battle_bag/bag_pc'

    def on_init_panel(self, player=None):
        super(BagUIPC, self).on_init_panel(player)
        self.init_slider_widget()

    def init_parameters(self):
        super(BagUIPC, self).init_parameters()
        self._mouse_move_listener = None
        self.cur_mouse_pos = None
        self.slider_start_y = None
        self.slider_end_y = None
        self.init_list_offset_y = None
        self.max_list_offset_y = None
        self.list_move_to_slider_move_ratio = None
        self.is_mouse_enbale_before = False
        return

    def init_widgets(self):
        super(BagUIPC, self).init_widgets()
        self.human_weapon_widget = BagHumanWeaponWidget(self.panel.nd_human, self.clothing_ui_list, self.on_gun_click, self.on_gun_drag, self.on_gun_end, self.on_clothes_click, self.on_clothes_drag, self.on_clothes_end)
        self.mecha_module_widget = BagMechaModuleWidget(self.panel, self.panel.mech_module, self.on_module_click, self.on_module_drag, self.on_module_end)
        method_dict = {'item_click': self.on_item_click,
           'item_drag': self.on_item_drag,
           'item_end': self.on_item_end
           }
        self.human_item_widget = BagHumanItemWidget(self.panel.bag, method_dict)
        method_dict = {'item_click': self.on_item_click,
           'item_drag': self.on_item_drag,
           'item_end': self.on_item_end_mecha
           }
        self.mecha_item_widget = BagMechaItemWidget(self.panel.mech_bag, method_dict)
        self._refresh_rogue_list([])

    def on_player_setted(self, lplayer):
        super(BagUIPC, self).on_player_setted(lplayer)
        if lplayer is not None:
            self.init_slider_widget()
        return

    def appear(self):
        if self._appearing:
            return
        super(BagUIPC, self).appear()
        self.register_mouse_move()
        self.init_slider_widget()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def disappear(self):
        if not self._appearing:
            return
        super(BagUIPC, self).disappear()
        self.unregister_mouse_move()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def _on_item_data_changed(self, item_data):
        super(BagUIPC, self)._on_item_data_changed(item_data)
        self.init_slider_widget()

    def register_mouse_move(self):
        if self._mouse_move_listener:
            return
        self._mouse_move_listener = cc.EventListenerMouse.create()
        self._mouse_move_listener.setOnMouseMoveCallback(self._on_mouse_move)
        self._mouse_move_listener.setOnMouseDownCallback(self._on_mouse_down)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_move_listener, self.panel.get())

    def unregister_mouse_move(self):
        if self._mouse_move_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_move_listener)
            self._mouse_move_listener = None
        return

    def _on_mouse_move(self, event):
        wpos = event.getLocationInView()
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        self.cur_mouse_pos = wpos
        btn_slider = self.panel.bag.nd_slider.slider_bg.btn_slider
        if btn_slider.IsPointIn(wpos):
            btn_slider.SetContentSize(SLIDER_BTN_H_BIG, btn_slider.GetContentSize()[1])
            return
        else:
            btn_slider.SetContentSize(SLIDER_BTN_W_NORMAL, btn_slider.GetContentSize()[1])
            self.panel.item_tips.setVisible(False)
            self.panel.item_tips_2.setVisible(False)
            self.remove_cur_select_state()
            if not self.panel.nd_content.IsPointIn(wpos):
                self.cur_ui = None
                self.cur_ui_type = BAG_UI_TYPE_OTHERS
                self.cur_ui_item_data = None
                return
            for item in self.gun_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item.btn, 'OnClick')
                    event_func(TouchMock())
                    return

            for item in self.clothing_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item.btn, 'OnClick')
                    event_func(TouchMock())
                    return

            for item in self.module_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item, 'OnClick')
                    event_func(TouchMock())
                    return

            for item in self.rogue_gifts_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item, 'OnClick')
                    event_func(TouchMock())
                    return

            human_item_ui_list = self.panel.bag.item_bag.item_list.GetAllItem()
            for item in human_item_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item.btn_bar, 'OnClick')
                    event_func(TouchMock())
                    return

            mecha_item_ui_list = self.panel.mech_bag.item_mech_bag.item_list.GetAllItem()
            for item in mecha_item_ui_list:
                if item.IsPointIn(wpos):
                    event_func = getattr(item.btn_bar, 'OnClick')
                    event_func(TouchMock())
                    return

            return

    def _on_mouse_down(self, event):
        mouse_type = event.getMouseButton()
        if mouse_type == 1:
            if not self.cur_ui_item_data:
                return
            self.use_bag_item(self.cur_ui_item_data)

    def show_item_tips(self, tip_ui, item_data, tip_no=0):
        self.tips_ui_list[1].setVisible(False)
        tip_ui.setVisible(False)
        tip_ui_height = template_utils.init_item_tips_new(tip_ui, item_data) * tip_ui.getScaleY()
        tip_ui_width = tip_ui.GetContentSize()[0] * tip_ui.getScaleX()
        if tip_no == 1:
            tip_show_pos = cc.Vec2(self.cur_mouse_pos.x, self.cur_mouse_pos.y - self._tip_ui_height)
        else:
            tip_show_pos = cc.Vec2(self.cur_mouse_pos.x, self.cur_mouse_pos.y)
            self._tip_ui_height = tip_ui_height
        offset_x, offset_y = template_utils.get_panel_show_all_offset(tip_ui, self.panel, tip_show_pos, 1, tip_ui_width, tip_ui_height)
        if offset_x < 0:
            tip_show_pos.x = tip_show_pos.x - tip_ui_width
        if offset_y > 0:
            tip_show_pos.y = tip_show_pos.y + tip_ui_height
        tip_ui.setPosition(tip_show_pos.x, tip_show_pos.y)
        tip_ui.setVisible(True)

    def init_slider_widget(self):
        item_list = self.panel.bag.item_bag.item_list
        btn_slider = self.panel.bag.nd_slider.slider_bg.btn_slider
        slider_bg = self.panel.bag.nd_slider.slider_bg
        max_move_len = item_list.GetInnerContentSize().height
        cur_show_len = item_list.GetContentSize()[1]
        item_count = item_list.GetItemCount()
        if item_count * HUMAN_ITEM_HEIGHT <= cur_show_len:
            btn_slider.setVisible(False)
            slider_bg.setVisible(False)
            return
        btn_slider.setVisible(True)
        slider_bg.setVisible(True)
        self.slider_start_y, self.slider_end_y = template_utils.init_common_slider(btn_slider, slider_bg, max_move_len, cur_show_len)
        item_list.ScrollToTop()
        self.init_list_offset_y = item_list.GetContentOffset().y
        self.max_list_offset_y = abs(self.init_list_offset_y)
        self.list_move_to_slider_move_ratio = self.max_list_offset_y / abs(self.slider_start_y - self.slider_end_y)
        item_list.BindMethod('OnScrolling', self.on_item_list_scrolling)
        btn_slider.BindMethod('OnDrag', self.on_drag_slider)
        btn_slider.BindMethod('OnBegin', self.on_begin_slider)
        btn_slider.BindMethod('OnEnd', self.on_end_slider)

    def on_begin_slider(self, btn, touch, *args):
        btn.SetContentSize(SLIDER_BTN_H_BIG, btn.GetContentSize()[1])

    def on_drag_slider(self, btn, touch, *args):
        if not btn.isVisible():
            return
        btn.SetContentSize(SLIDER_BTN_H_BIG, btn.GetContentSize()[1])
        cur_slider_pos = btn.GetPosition()
        dy = touch.getDelta().y * 0.8
        slider_pos_y = cur_slider_pos[1] + dy
        if slider_pos_y < self.slider_end_y:
            slider_pos_y = self.slider_end_y
        if slider_pos_y > self.slider_start_y:
            slider_pos_y = self.slider_start_y
        btn.SetPosition(cur_slider_pos[0], slider_pos_y)
        item_list = self.panel.bag.item_bag.item_list
        cur_list_offset = item_list.GetContentOffset()
        cur_list_offset.y -= dy * self.list_move_to_slider_move_ratio
        if cur_list_offset.y > 0:
            cur_list_offset.y = 0
        if cur_list_offset.y < self.init_list_offset_y:
            cur_list_offset.y = self.init_list_offset_y
        item_list.SetContentOffset(cur_list_offset)

    def on_end_slider(self, btn, touch, *args):
        btn.SetContentSize(SLIDER_BTN_W_NORMAL, btn.GetContentSize()[1])

    def on_item_list_scrolling(self, *args):
        btn_slider = self.panel.bag.nd_slider.slider_bg.btn_slider
        item_list = self.panel.bag.item_bag.item_list
        if not btn_slider.isVisible():
            return
        cur_list_offset = item_list.GetContentOffset()
        list_dy = cur_list_offset.y - self.init_list_offset_y
        btn_slider_dy = list_dy / self.list_move_to_slider_move_ratio
        origin_x = btn_slider.GetPosition()[0]
        new_y = self.slider_start_y - btn_slider_dy
        if new_y > self.slider_start_y:
            new_y = self.slider_start_y
        if new_y < self.slider_end_y:
            new_y = self.slider_end_y
        self.panel.bag.nd_slider.slider_bg.btn_slider.SetPosition(origin_x, new_y)

    def mouse_left_click(self, msg, keycode):
        pass

    def mouse_use_bag_item(self, msg, keycode):
        if not self.cur_ui_item_data:
            return
        self.use_bag_item(self.cur_ui_item_data)

    def is_in_empty_area(self, wpos):
        return not (self.panel.mech_bag.IsPointIn(wpos) or self.panel.bag.IsPointIn(wpos) or self.panel.nd_human.IsPointIn(wpos) or self.panel.mech_module.IsPointIn(wpos))

    def is_in_item_area(self, wpos):
        return self.panel.mech_bag.IsPointIn(wpos) or self.panel.item_bag.IsPointIn(wpos)