# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/InteractFunctionWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from functools import cmp_to_key
from logic.gutils import items_book_utils
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.items_book_ui.ItemCategoryListWidget import ItemCategoryListWidget
from logic.comsys.items_book_ui.SkinItemListWidget import SkinItemListWidget
from logic.client.const import items_book_const
from common.framework import Functor
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from logic.gutils import red_point_utils
from logic.gutils import mall_utils
from logic.comsys.items_book_ui.InteractionGetUseBuyWidget import InteractionGetUseBuyWidget
from logic.comsys.items_book_ui.RoundSelectWidget import RoundSelectWidget
from logic.comsys.items_book_ui.ListSelectWidget import ListSelectWidget
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
from logic.gutils import lobby_model_display_utils
from common.cfg import confmgr
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.item import lobby_item_type
from logic.gcommon.common_const import role_const
from logic.gutils.template_utils import set_ui_show_picture
from logic.gutils.mecha_skin_utils import get_mecha_skin_no_by_item_no
from logic.gutils.interaction_utils import get_mecha_ex_icon_path
OUTLINE_ICON_PATH = 'gui/ui_res_2/catalogue/outline/%s.png'
DRAG_DELTA = 0.05
DRAG_TAN = 1.303

class PersonalizationClassBase(object):

    def __init__(self, panel, parent):
        self.panel = panel
        self.parent = parent
        self._show_type = None
        return

    def set_data_dic(self, data_dict):
        pass

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def show_item_detail(self, item_no):
        pass

    def destroy(self):
        self.panel = None
        self.parent = None
        return

    @property
    def show_type(self):
        return self._show_type

    @show_type.setter
    def show_type(self, val):
        self._show_type = val


class InteractTypeBase(PersonalizationClassBase):

    def __init__(self, panel, parent):
        super(InteractTypeBase, self).__init__(panel, parent)
        self.panel = panel
        self.parent = parent
        self.selected_role_id = role_const.INTERACTION_KEY
        self.role_interaction_info = {}
        self._show_type = None
        return

    def set_data_dic(self, data_dict):
        self.role_interaction_info = data_dict

    @property
    def interaction_state(self):
        return self.parent.interaction_state

    def destroy(self):
        super(InteractTypeBase, self).destroy()
        self.role_interaction_info = {}

    def update_scene(self):
        pass


class InteractGestureType(InteractTypeBase):

    def __init__(self, panel, parent):
        super(InteractGestureType, self).__init__(panel, parent)

    def on_enter(self):
        self.init_scene()

    def on_leave(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def show_item_detail(self, item_no):
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        if not self.panel:
            return
        else:
            self.panel.lab_name.setVisible(valid)
            self.panel.lab_describe.setVisible(valid)
            if not valid:
                return
            self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name_by_config_name('GestureConfig', item_no))
            self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
            role_id = items_book_utils.get_interaction_belong_to_role(item_no)
            if not role_id:
                role_id = self.selected_role_id
            role_data = global_data.player.get_item_by_no(role_id)
            default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')
            fashion_data = role_data.get_fashion() if role_data else {}
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT, default_skin)
            show_anim = self.role_interaction_info[str(item_no)]['action_name']
            end_anim = self.role_interaction_info[str(item_no)].get('idle_name', None)
            is_manage = self.interaction_state != items_book_const.INTERACTION_STATE_DISPLAY
            model_data = lobby_model_display_utils.get_items_book_interaction_model_data(role_id, dressed_clothing_id, show_anim, is_manage, end_anim)
            global_data.emgr.change_model_display_scene_item.emit(model_data)
            return

    def init_scene(self):
        config_index = lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY else lobby_model_display_const.ITEMBOOKS_GESTURE_MANAGE
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, config_index, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def update_scene(self):
        self.init_scene()


class InteractMechaGestureType(InteractTypeBase):

    def __init__(self, panel, parent):
        super(InteractMechaGestureType, self).__init__(panel, parent)

    def on_enter(self):
        self.init_scene()

    def on_leave(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def show_item_detail(self, item_no):
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        if not self.panel:
            return
        self.panel.lab_name.setVisible(valid)
        self.panel.lab_describe.setVisible(valid)
        if not valid:
            return
        self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name_by_config_name('MechaGestureConfig', item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        mecha_id = items_book_utils.get_interaction_belong_to_role(item_no)
        if not mecha_id:
            mecha_id = self.selected_role_id
        from logic.gutils.dress_utils import get_mecha_default_fashion
        default_skin_id = get_mecha_default_fashion(mecha_id)
        show_anim = self.role_interaction_info[str(item_no)]['action_name']
        end_anim = show_anim
        is_manage = self.interaction_state != items_book_const.INTERACTION_STATE_DISPLAY
        model_data = lobby_model_display_utils.get_items_book_interaction_model_data(mecha_id, default_skin_id, show_anim, is_manage, end_anim)
        global_data.emgr.change_model_display_scene_item.emit(model_data)

    def init_scene(self):
        config_index = lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY else lobby_model_display_const.ITEMBOOKS_GESTURE_MANAGE
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, config_index, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def update_scene(self):
        self.init_scene()


class InteractEmojiType(InteractTypeBase):

    def __init__(self, panel, parent):
        super(InteractEmojiType, self).__init__(panel, parent)

    def show_item_detail(self, item_no):
        if not self.panel:
            return
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        self.panel.lab_name.setVisible(valid)
        self.panel.lab_describe.setVisible(valid)
        if not valid:
            return
        self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name_by_config_name('EmojiConfig', item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        role_id = items_book_utils.get_interaction_belong_to_role(item_no)
        if role_id or global_data.player:
            role_id = global_data.player.get_role() if 1 else int(self.selected_role_id)
        role_data = global_data.player.get_item_by_no(role_id) if global_data.player else {}
        default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')
        fashion_data = role_data.get_fashion() if role_data else {}
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT, default_skin)
        show_anim = 's_emptyhand_idle'
        end_anim = 's_emptyhand_idle'
        is_manage = self.interaction_state != items_book_const.INTERACTION_STATE_DISPLAY
        model_data = lobby_model_display_utils.get_items_book_interaction_model_data(role_id, dressed_clothing_id, show_anim, is_manage, end_anim)
        model_data[0]['emoji_id'] = item_no
        global_data.emgr.change_model_display_scene_item.emit(model_data)

    def init_scene(self):
        config_index = lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY else lobby_model_display_const.ITEMBOOKS_GESTURE_MANAGE
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, config_index, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def on_enter(self):
        self.init_scene()

    def on_leave(self):
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def update_scene(self):
        self.init_scene()


class InteractSprayType(InteractTypeBase):

    def __init__(self, panel, parent):
        super(InteractSprayType, self).__init__(panel, parent)

    def show_item_detail(self, item_no):
        valid = bool(item_no) and str(item_no) in self.role_interaction_info
        if not self.panel:
            return
        self.panel.lab_name.setVisible(valid)
        self.panel.lab_describe.setVisible(valid)
        self.panel.img_item.setVisible(valid)
        if not valid:
            return
        self.panel.lab_name.SetString(items_book_utils.get_filter_item_show_name_by_config_name('SprayConfig', item_no))
        self.panel.lab_describe.SetString(item_utils.get_lobby_item_desc(item_no))
        self.panel.img_item.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_no))

    def on_enter(self):
        self.init_scene()

    def on_leave(self):
        self.panel.img_item.setVisible(False)

    def init_scene(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.WEAPON_SHOW, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return


class InteractKillSfxType(PersonalizationClassBase):

    def set_data_dic(self, data_dict):
        self.data_dict = data_dict

    def destroy(self):
        super(InteractKillSfxType, self).destroy()
        self.data_dict = {}

    def is_panel_visible(self):
        ui_parent = global_data.ui_mgr.get_ui('ItemsBookMainUI')
        return ui_parent and ui_parent.panel.isVisible()

    def on_leave(self):
        self.panel.StopTimerAction()
        global_data.emgr.change_model_display_scene_tag_effect.emit('')

    def on_enter(self):
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.ITEMBOOKS_GESTURE_DISPLAY, scene_content_type=scene_const.SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def show_item_detail(self, item_no):
        self._show_sfx(item_no)

    def _show_sfx(self, sfx_item_no):
        if not self.is_panel_visible():
            return
        else:
            conf = self.data_dict.get(str(sfx_item_no), {})
            sfx_path = conf.get('sfx_path', '')
            sfx_scale = conf.get('sfx_scale', 1.0)
            one_time = conf.get('time', 5550 / 1000.0)
            offset = conf.get('sfx_offset', None)

            def single_show():
                if sfx_path:
                    global_data.emgr.change_model_display_scene_tag_effect.emit(sfx_path, sfx_scale=sfx_scale, offset=offset)

            single_show()

            def start_loop():
                if self.panel:
                    self.panel.StopTimerAction()
                    self.panel.TimerAction(lambda t: single_show(), duration_sec=10000000, interval=one_time)

            start_loop()
            return


class InteractFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(InteractFunctionWidget, self).__init__(parent, panel)
        self.is_auto_mode = False
        self.interaction_state = self.get_parent_interaction_state() or items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        self.is_showing_empty = False
        self.auto_match_list = []
        self.selected_role_id = role_const.INTERACTION_KEY
        self.show_item_no = None
        self.data_list = []
        self.data_dict = {}
        self.init_widget()
        self.init_button_event()
        return

    def destroy(self):
        super(InteractFunctionWidget, self).destroy()
        self.data_list = []
        self.data_dict = {}
        if self.cur_interact_type_widget:
            self.cur_interact_type_widget.destroy()
            self.cur_interact_type_widget = None
        return

    def set_data(self, data_list, data_dict):
        self.data_list = data_list
        self.data_dict = data_dict
        self.update_auto_match_list()

    def on_update_scene(self):
        if self.cur_interact_type_widget:
            self.cur_interact_type_widget.update_scene()

    def on_clear_effect(self):
        if self.cur_interact_type_widget:
            self.cur_interact_type_widget.on_leave()

    def get_interaction_state(self):
        return self.interaction_state

    def set_interaction_state(self, state):
        self.interaction_state = state

    def get_parent_interaction_state(self):
        return self.parent.interaction_state

    def update_parent_interaction_state(self):
        self.parent.interaction_state = self.interaction_state

    def init_widget(self):
        self.init_desc_item()
        self.reset_descs()
        self.cur_interact_type_widget = None
        self.init_auto_emoji_widget()
        self._round_select_widget = RoundSelectWidget(self, self.panel.temp_round)
        self.init_switch_emoji_mode_widget()
        return

    def init_auto_emoji_widget(self):
        auto_emoji_config = confmgr.get('auto_emoji', default={})
        moment_list = auto_emoji_config.get('moment_list', [])
        self.panel.temp_list.setVisible(False)
        item_list = self.panel.temp_list.nd_expression_auto.list_expression_auto
        item_list.SetInitCount(len(moment_list))
        for idx, ui_item in enumerate(item_list.GetAllItem()):
            moment_id = moment_list[idx]
            moment_info = auto_emoji_config.get(moment_id)
            name_text_id = moment_info.get('iTextID')
            ui_item.lab_scene.SetString(name_text_id)

        self._list_select_widget = ListSelectWidget(self, item_list)

    def init_button_event(self):
        self.panel.btn_manage.BindMethod('OnClick', self.on_click_manage)
        self.panel.btn_quick_manage.BindMethod('OnClick', self.on_click_quick_match)

    def on_click_manage(self, *args):
        if not self.panel:
            return
        display_state = items_book_const.INTERACTION_STATE_DISPLAY
        new_state = display_state if self.interaction_state != display_state else items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        self.panel.btn_manage.SetText(items_book_utils.get_manage_state_text_id(new_state))
        self.panel.btn_manage.SetSelect(new_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY)
        self.interaction_state = new_state
        self.update_parent_interaction_state()
        self.update_role_data(state_changed=True)

    def get_item_icon(self, item_no):
        mecha_skin_no = get_mecha_skin_no_by_item_no(item_no)
        if item_utils.get_lobby_item_type(item_no) == lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE:
            path = item_utils.get_interact_mecha_img(item_no)
        else:
            path = get_mecha_ex_icon_path(mecha_skin_no) if mecha_skin_no else item_utils.get_lobby_item_pic_by_item_no(item_no)
        return path

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.data_list) and self.data_list[index] is not None
        if valid:
            item_widget.nd_kind.setVisible(True)
            item_widget.img_level.setVisible(True)
            item_widget.nd_content.setVisible(True)
            item_widget.bar.SetEnable(True)
            item_no = self.data_list[index]
            path = self.get_item_icon(item_no)
            item_widget.item.SetDisplayFrameByPath('', path)
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
            item_widget.choose.setVisible(False)
            if global_data.player:
                interaction_data = global_data.player.get_role_interaction_data(self.selected_role_id, self.is_auto_mode)
            else:
                interaction_data = {}
            is_using = int(item_no) in six_ex.values(interaction_data)
            item_widget.img_using.setVisible(is_using)
            can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
            item_widget.img_lock.setVisible(not can_use)
            item_utils.check_skin_tag(item_widget.nd_kind, item_no)
            item_utils.check_skin_bg_tag(item_widget.img_level, item_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            red_point_utils.show_red_point_template(item_widget.nd_new, False)
            item_widget.bar.SetSwallowTouch(False)
            item_widget.bar.SetNoEventAfterMove(False)
            self.bind_widget_event(item_widget, index)
            if not global_data.player:
                return
            has_item = global_data.player.get_item_by_no(int(item_no))
            show_new = bool(has_item) and has_item.rp
            red_point_utils.show_red_point_template(item_widget.nd_new, show_new)
            role_id = items_book_utils.get_interaction_belong_to_role(item_no, only_one_role=True)
            if role_id:
                item_widget.img_driver_tag.setVisible(True)
                from logic.gutils.item_utils import get_role_tag_by_role_id
                item_widget.img_driver_tag.SetDisplayFrameByPath('', get_role_tag_by_role_id(role_id))
            else:
                item_widget.img_driver_tag.setVisible(False)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
            item_widget.img_driver_tag.setVisible(False)
        item_widget.nd_empty.setVisible(not valid)
        return

    def bind_widget_event(self, item_widget, index):
        if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY:
            item_widget.bar.BindMethod('OnClick', Functor(self.on_select_item, index))
            item_widget.bar.UnBindMethod('OnBegin')
            item_widget.bar.UnBindMethod('OnDrag')
            item_widget.bar.UnBindMethod('OnEnd')
            item_widget.bar.UnBindMethod('OnCancel')
        else:
            item_widget.bar.BindMethod('OnClick', Functor(self.on_select_manage_item, index))
            item_widget.bar.BindMethod('OnBegin', Functor(self.on_begin_select_item, self.data_list[index]))
            item_widget.bar.BindMethod('OnDrag', Functor(self.on_drag_select_item, self.data_list[index]))
            item_widget.bar.BindMethod('OnEnd', Functor(self.on_end_select_item, None, self.data_list[index]))
            item_widget.bar.BindMethod('OnCancel', Functor(self.on_end_select_item, None, self.data_list[index]))
        return

    def on_select_item(self, index, *args):
        if not self.panel:
            return
        if index >= len(self.data_list):
            return
        if self.sel_before_cb:
            self.sel_before_cb(self.get_parent_selected_item_index(), index)
        item_no = self.data_list[index]
        item_widget = self.panel.list_item.GetItem(index)
        if not item_widget or item_widget.IsDestroyed():
            return
        red_point_utils.show_red_point_template(item_widget.nd_new, False)
        self.show_item_detail(item_no)
        global_data.player.req_del_item_redpoint(int(item_no))
        if self.sel_callback:
            self.sel_callback()

    def on_select_manage_item(self, index, btn, touch, *args):
        if index >= len(self.data_list):
            return
        else:
            item_no = self.data_list[index]
            if items_book_utils.is_interaction_item_setted(item_no, self.selected_role_id, self.is_auto_mode):
                self.get_cur_select_widget().update_parent_selected_item_no(None)
                self.unselect_item()
                self.parent.set_last_view_item_no(item_no)
                self.show_item_detail(item_no)
                return
            if bool(touch):
                self.get_cur_select_widget().update_parent_selected_item_no(self.data_list[index])
                self.on_select_item(index)
            else:
                self.parent.set_last_view_item_no(item_no)
                self.show_item_detail(item_no)
            return

    def on_begin_select_item(self, item_no, btn, touch, *args):
        self.unselect_item()
        self.get_cur_select_widget().update_parent_selected_item_no(None)
        can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
        if self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
            self.on_end_select_item(None, item_no, btn, touch, *args)
            return
        else:
            if can_use:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM
            else:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
            btn.SetNoEventAfterMove(False)
            return True

    def on_drag_select_item(self, item_no, btn, touch, *args):
        if not self.parent:
            return
        else:
            if self.interaction_state != items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
                self.on_end_select_item(None, item_no, btn, touch)
                return
            if not self.panel.drag_item.isVisible() and not btn.GetSwallowTouch():
                pos = touch.getLocation()
                beg_pos = touch.getStartLocation()
                dx = pos.x - beg_pos.x
                dy = pos.y - beg_pos.y
                if abs(dx) + abs(dy) < DRAG_DELTA * 1.1:
                    return
                if abs(dx) >= abs(dy):
                    btn.SetSwallowTouch(True)
                    self.show_drag_item(item_no)
                else:
                    btn.SetSelect(False)
                    btn.SetEnableTouch(False)
                    btn.SetEnableTouch(True)
                    btn.SetSwallowTouch(False)
                    return
            wpos = touch.getLocation()
            self.on_drag_item(item_no, wpos)
            if not btn.GetSwallowTouch():
                btn.SetSwallowTouch(True)
            return

    def on_end_select_item(self, index, item_no, btn, touch, *args):
        if not self.panel:
            return
        else:
            if not self.panel.nd_interact.isVisible():
                return
            btn.SetSwallowTouch(False)
            self.panel.drag_item.setVisible(False)
            if self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_MOVE_ITEM:
                self.interaction_state = items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
                wpos = touch.getLocation()
                drag_index = self.on_drag_item(item_no, wpos)
                if index is not None and drag_index is None:
                    self.on_drag_set_interaction(index, 0)
                elif drag_index is not None:
                    self.on_drag_set_interaction(drag_index, item_no)
                self.get_cur_select_widget().update_parent_selected_item_no(None)
            return

    def unselect_item(self, *args):
        if not self.panel:
            return
        else:
            selected_item_index = self.get_parent_selected_item_index()
            prev_item = self.panel.list_item.GetItem(selected_item_index)
            if prev_item:
                prev_item.setLocalZOrder(0)
                prev_item.choose.setVisible(False)
            self.set_parent_selected_item_index(None)
            return

    def on_drag_item(self, item_no, wpos):
        lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
        self.panel.drag_item.setPosition(lpos)
        item_index = self.get_cur_select_widget().check_drag_pos(wpos)
        return item_index

    def show_drag_item(self, item_no):
        self.panel.drag_item.setVisible(True)
        path = self.get_item_icon(item_no)
        self.panel.drag_item.SetDisplayFrameByPath('', path)
        self.parent.set_last_view_item_no(item_no)
        self.show_item_detail(item_no)

    def get_cur_select_widget(self):
        if not self.is_auto_mode:
            return self._round_select_widget
        return self._list_select_widget

    def on_drag_set_interaction(self, idx, item_no):
        global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, item_no)

    def reset_descs(self):
        self.panel.lab_name.setVisible(False)
        self.panel.lab_describe.setVisible(False)
        if hasattr(self.panel, 'img_item') and self.panel.img_item:
            self.panel.img_item.setVisible(False)

    def quick_match_items(self):
        player = global_data.player
        if self.selected_role_id is None or self.data_list is None:
            return
        else:
            if not player:
                return
            role_interaction_data = player.get_role_interaction_data(self.selected_role_id, self.is_auto_mode)
            item_idx = 0
            item_count = len(self.data_list)
            using_interaction_data = set(six_ex.values(role_interaction_data))
            if self.is_auto_mode:
                self.quick_fill_list_select_widget(role_interaction_data, using_interaction_data, item_count)
            else:
                self.quick_fill_round_select_widget(role_interaction_data, using_interaction_data, item_count)
            return

    def quick_fill_round_select_widget(self, role_interaction_data, using_interaction_data, item_count):
        item_idx = 0
        for idx in range(0, 8):
            if idx in role_interaction_data and role_interaction_data[idx] != 0:
                continue
            while item_idx < item_count:
                item_no = self.auto_match_list[item_idx]
                if not item_no:
                    continue
                item_idx += 1
                can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
                is_using = int(item_no) in using_interaction_data
                if can_use and not is_using:
                    global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, item_no)
                    global_data.player.req_del_item_redpoint(int(item_no))
                    break

    def quick_fill_list_select_widget(self, role_interaction_data, using_interaction_data, item_count):
        auto_emoji_config = confmgr.get('auto_emoji', default={})
        moment_list = auto_emoji_config.get('moment_list', [])
        item_idx = 0
        item_list = self.panel.temp_list.nd_expression_auto.list_expression_auto
        moment_count = item_list.GetItemCount()
        for idx in range(0, moment_count):
            moment_id = moment_list[idx]
            if moment_id in role_interaction_data and role_interaction_data[moment_id] != 0:
                continue
            while item_idx < item_count:
                item_no = self.auto_match_list[item_idx]
                item_idx += 1
                can_use, _ = mall_utils.item_can_use_by_item_no(item_no)
                is_using = int(item_no) in using_interaction_data
                if can_use and not is_using:
                    global_data.player.try_set_interaction_data(int(self.selected_role_id), moment_id, item_no)
                    global_data.player.req_del_item_redpoint(int(item_no))
                    break

    def on_click_set_interaction(self, idx):
        if not self.panel.nd_interact.isVisible:
            return
        else:
            selected_item_index = self.get_parent_selected_item_index()
            if selected_item_index is None:
                return
            global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, self.data_list[self.get_parent_selected_item_index()])
            self.set_parent_selected_item_index(None)
            self.update_role_data(self.selected_role_id)
            self.get_cur_select_widget().update_parent_selected_item_no(None)
            return

    def update_role_data(self, role_id=None, state_changed=False, data_changed=False):
        role_id = self.selected_role_id
        role_change = role_id != self.selected_role_id
        is_init = state_changed or role_id != self.selected_role_id or not self.inited
        self.inited = True
        self.selected_role_id = role_id
        if is_init or data_changed:
            self._round_select_widget.udpate_selected_role_id(self.selected_role_id)
            self._list_select_widget and self._list_select_widget.udpate_selected_role_id(self.selected_role_id)
        if role_change or state_changed:
            self.get_cur_select_widget().update_parent_selected_item_no(None)
        if state_changed:
            self.on_state_changed()
        return

    def on_delete_interaction(self, idx):
        global_data.player.try_set_interaction_data(int(self.selected_role_id), idx, 0)

    def on_change_interaction_data(self, role_id):
        if str(role_id) != str(self.selected_role_id):
            return
        self.update_role_data(self.selected_role_id, data_changed=True)

    def on_state_changed(self):
        ani = self.get_animation_name()
        self.panel.PlayAnimation(ani)
        self.update_scene()

    def get_animation_name(self):
        if self.get_interaction_state() == items_book_const.INTERACTION_STATE_DISPLAY:
            if self.is_auto_mode:
                ani = 'disappear_manage_list'
            else:
                ani = 'disappear_manage'
        elif self.is_auto_mode:
            ani = 'show_manage_list'
        else:
            ani = 'show_manage'
        return ani

    def update_scene(self):
        if self.cur_interact_type_widget:
            self.cur_interact_type_widget.update_scene()
        selected_item_index = self.get_parent_selected_item_index()
        if selected_item_index is not None and selected_item_index < len(self.data_list):
            self.show_item_detail(self.data_list[selected_item_index])
        elif self.show_item_no:
            self.show_item_detail(self.show_item_no)
        return

    def on_data_exist(self):
        is_manage = self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY
        if self.is_showing_empty:
            if is_manage:
                ani_name = 'show_manage'
            else:
                ani_name = 'disappear_manage_list' if self.is_auto_mode else 'disappear_manage'
            self.panel.PlayAnimation(ani_name)
        self.panel.nd_interact.setVisible(True)
        self.is_showing_empty = False

    def on_data_empty(self):
        self.is_showing_empty = True
        self.panel.StopAnimation('show_manage')
        self.panel.StopAnimation('show_manage')
        self.panel.StopAnimation('show_manage_list')
        self.panel.StopAnimation('disappear_manage_list')
        self.panel.temp_round.setVisible(False)
        self.panel.temp_list.setVisible(False)
        self.panel.nd_interact.setVisible(False)
        if self.panel.img_item:
            self.panel.img_item.setVisible(False)
        self.on_clear_effect()

    def init_desc_item(self):
        self.panel.nd_empty.setVisible(False)
        if self.interaction_state == items_book_const.INTERACTION_STATE_DISPLAY:
            self.panel.btn_quick_manage.setVisible(False)
            self.panel.temp_round.setPosition(self.panel.temp_origin.getPosition())
            self.panel.temp_round.setVisible(False)
            self.panel.temp_round.setOpacity(255)
            if self.panel.img_item:
                self.panel.img_item.setPosition(self.panel.img_origin.getPosition())
                self.panel.img_item.setVisible(True)
                self.panel.img_item.setOpacity(255)
        else:
            self.panel.btn_quick_manage.setVisible(True)
            self.panel.PlayAnimation('show_manage')
        self.panel.btn_manage.EnableCustomState(True)
        self.panel.btn_manage.SetText(items_book_utils.get_manage_state_text_id(self.interaction_state))
        self.panel.btn_manage.SetSelect(self.interaction_state == items_book_const.INTERACTION_STATE_MANAGE_DISPLAY)

    def show_item_detail(self, item_no):
        self.show_item_no = item_no
        if item_no == None:
            return
        else:
            old_item_type = None
            if self.cur_interact_type_widget:
                old_item_type = self.cur_interact_type_widget.show_type
            new_item_type = item_utils.get_lobby_item_type(item_no)
            enter_type_show_dict = {lobby_item_type.L_ITEM_TYPE_GESTURE: InteractGestureType,
               lobby_item_type.L_ITEM_TYPE_MECHA_GESTURE: InteractMechaGestureType,
               lobby_item_type.L_ITEM_TYPE_SPRAY: InteractSprayType,
               lobby_item_type.L_ITEM_TYPE_EMOTICON: InteractEmojiType
               }
            if old_item_type != new_item_type:
                if self.cur_interact_type_widget:
                    self.cur_interact_type_widget.on_leave()
                    self.cur_interact_type_widget.destroy()
                    self.cur_interact_type_widget = None
                self.cur_interact_type_widget = enter_type_show_dict[new_item_type](self.panel, self)
                self.cur_interact_type_widget.show_type = new_item_type
                self.cur_interact_type_widget.set_data_dic(self.data_dict)
                self.cur_interact_type_widget.on_enter()
                self.cur_interact_type_widget.show_item_detail(item_no)
            else:
                if not self.cur_interact_type_widget:
                    self.cur_interact_type_widget = enter_type_show_dict[new_item_type](self.panel, self)
                    self.cur_interact_type_widget.show_type = new_item_type
                    self.cur_interact_type_widget.set_data_dic(self.data_dict)
                    self.cur_interact_type_widget.on_enter()
                self.cur_interact_type_widget.show_item_detail(item_no)
            return

    def update_auto_match_list(self):
        self.auto_match_list = sorted([ i for i in self.data_list if i ], key=cmp_to_key(self.cmp_auto_match_item))

    def cmp_auto_match_item(self, item_no1, item_no2):
        item_no1 = 0 if item_no1 is None else item_no1
        item_no2 = 0 if item_no2 is None else item_no2
        rare_degree1 = item_utils.get_item_rare_degree(item_no1) if item_no1 else -999
        rare_degree2 = item_utils.get_item_rare_degree(item_no2) if item_no2 else -999
        degree_cmp_res = six_ex.compare(rare_degree2, rare_degree1)
        if degree_cmp_res != 0:
            return degree_cmp_res
        else:
            return six_ex.compare(int(item_no1), int(item_no2))

    def on_click_quick_match(self, *args):
        self.quick_match_items()

    def init_switch_emoji_mode_widget(self):
        list_tab = self.panel.nd_tab.list_tab
        list_tab.SetInitCount(2)
        btn_manual = list_tab.GetItem(0).btn_tab
        btn_auto = list_tab.GetItem(1).btn_tab
        btn_manual.lab_tab.SetString(609660)
        btn_auto.lab_tab.SetString(609661)

        @btn_manual.unique_callback()
        def OnClick(btn, touch, _btn_manual=btn_manual, _btn_auto=btn_auto):
            self.on_click_btn_manual(_btn_manual, _btn_auto)

        @btn_auto.unique_callback()
        def OnClick(btn, touch, _btn_manual=btn_manual, _btn_auto=btn_auto):
            self.on_click_btn_auto(_btn_manual, _btn_auto)

        self.on_click_btn_manual(btn_manual, btn_auto)

    def on_click_btn_manual(self, btn_manual, btn_auto):
        self.is_auto_mode = False
        self.panel.temp_round.setVisible(True)
        self.panel.temp_list.setVisible(False)
        btn_manual.SetSelect(True)
        btn_auto.SetSelect(False)
        self.update_interaction_list(True, 0)

    def on_click_btn_auto(self, btn_manual, btn_auto):
        self.is_auto_mode = True
        self.panel.temp_round.setVisible(False)
        self.panel.temp_list.setVisible(True)
        btn_auto.SetSelect(True)
        btn_manual.SetSelect(False)
        self.update_interaction_list(True, 0)

    def update_interaction_list(self, is_init, select_index):
        self.parent.update_skin_list(is_init, select_index)

    def switch_auto_mode(self, is_enable):
        self.panel.list_tab.setVisible(is_enable)
        if not is_enable:
            if self.is_auto_mode:
                self.is_auto_mode = False
                self.panel.temp_round.setVisible(True)
                self.panel.temp_list.setVisible(False)
                list_tab = self.panel.nd_tab.list_tab
                if len(list_tab.GetAllItem()) >= 2:
                    btn_manual = list_tab.GetItem(0).btn_tab
                    btn_auto = list_tab.GetItem(1).btn_tab
                    btn_manual.SetSelect(True)
                    btn_auto.SetSelect(False)