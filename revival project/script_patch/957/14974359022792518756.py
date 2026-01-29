# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/GuangmuFunctionWidget.py
from __future__ import absolute_import
from logic.comsys.items_book_ui.FunctionWidgetBase import FunctionWidgetBase
from logic.gutils.battle_flag_utils import init_battle_flag_template_new, get_battle_info_by_player
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, check_skin_tag, check_skin_bg_tag
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.red_point_utils import show_red_point_template
from logic.gutils.template_utils import show_remain_time
from common.framework import Functor
from .GuangmuGetUseBuyWidget import GuangmuGetUseBuyWidget
from logic.gutils.items_book_utils import get_items_conf_by_config_name
from logic.gutils.new_template_utils import init_player_loading_card
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from logic.client.const.lobby_model_display_const import ITEMBOOKS_GESTURE_MANAGE
from logic.gcommon.common_const.scene_const import SCENE_JIEMIAN_COMMON, SCENE_ITEM_BOOK
TYPE_LOADING = 'loading'
TYPE_TV = 'tv'
TYPE_SKY = 'sky'
LIST_LINE_PIC = 'gui/ui_res_2/mech_display/ex/icon_ex_line_mid.png'
LIST_END_PIC = 'gui/ui_res_2/mech_display/ex/icon_ex_line_down.png'

class GuangmuFunctionWidget(FunctionWidgetBase):

    def __init__(self, parent, panel):
        super(GuangmuFunctionWidget, self).__init__(parent, panel)
        self.selected_effect_list = []
        self.data_dict = {}
        self.own_func = None
        self.process_event(True)
        self.init_param()
        self.init_widget()
        if global_data.player:
            mecha_id = global_data.player.get_lobby_selected_mecha_item_id()
            mecha_item = global_data.player.get_item_by_no(mecha_id)
            mecha_fashion = {}
            if mecha_item:
                mecha_fashion = mecha_item.get_fashion()
            role_id = global_data.player.get_role()
            role_item = global_data.player.get_item_by_no(role_id)
            role_fashion = {}
            if role_item:
                role_fashion = role_item.get_fashion()
            player_info = {'head_photo': global_data.player.get_head_photo(),'head_frame': global_data.player.get_head_frame(),
               'dan_info': global_data.player.get_dan_info(),
               'char_name': global_data.player.get_name(),
               'priv_lv': global_data.player.get_privilege_level(),
               'priv_settings': global_data.player.get_privilege_setting(),
               'rank_use_title_dict': global_data.player.rank_use_title_dict,
               'role_skin': role_fashion.get(FASHION_POS_SUIT, 0),
               'role_skin_weapon_sfx': role_fashion.get(FASHION_POS_WEAPON_SFX, 0),
               'mecha_skin': mecha_fashion.get(FASHION_POS_SUIT, 0),
               'mecha_skin_weapon_sfx': mecha_fashion.get(FASHION_POS_WEAPON_SFX, 0),
               'battle_flag_frame': global_data.player.get_battle_flag_frame()
               }
            init_player_loading_card(self.panel, 0, player_info, self.panel.temp_flag, 0, self.on_click_player_card, True)
        self.panel.list_tab_guangmu.GetItem(0).btn_icon.BindMethod('OnClick', lambda *args: self.on_switch_guangmu_type(TYPE_LOADING))
        self.panel.list_tab_guangmu.GetItem(1).btn_icon.BindMethod('OnClick', lambda *args: self.on_switch_guangmu_type(TYPE_TV))
        self.panel.list_tab_guangmu.GetItem(2).btn_icon.BindMethod('OnClick', lambda *args: self.on_switch_guangmu_type(TYPE_SKY))
        return

    def set_data(self, data_list, data_dict, own_func=None):
        self.selected_effect_list = data_list
        self.data_dict = data_dict
        self.own_func = own_func

    def init_param(self):
        self.page_showing = False
        self._cur_guangmu_type = None
        self._cur_guangmu = None
        self._cur_use_guangmu = None
        self.guangmu_config_dict = get_items_conf_by_config_name('GuangmuConfig')
        self.cur_flag_guangmu = None
        self.cur_bg_guangmu = None
        self.cur_tv_guangmu = None
        self.cur_sky_guangmu = None
        self.cur_sound_id = None
        return

    def init_widget(self):
        self._get_use_buy_widget = GuangmuGetUseBuyWidget(self, self.panel.btn_buy_gm, self.panel.btn_use_gm, self.panel.btn_cancel_gm, self.panel.btn_go_gm, self.panel.temp_price_gm, self.panel.lab_get_method_gm)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_selected_guangmu_changed': self.on_guangmu_change
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_click_player_card(self, ui_item, role_visible, mecha_visible):
        ui_item.nd_role_locate.setVisible(role_visible)
        ui_item.temp_level_role.nd_kind.setVisible(role_visible)
        ui_item.img_role_charm_level.setVisible(role_visible)
        ui_item.bar_charm_role.setVisible(role_visible)
        ui_item.lab_role_skin_name.setVisible(role_visible)
        ui_item.icon_relation.setVisible(role_visible)
        ui_item.lab_value.setVisible(role_visible)
        ui_item.nd_mech_locate.setVisible(mecha_visible)
        ui_item.temp_level_mecha.nd_kind.setVisible(mecha_visible)
        ui_item.img_mecha_charm_level.setVisible(mecha_visible)
        ui_item.bar_charm_mecha.setVisible(mecha_visible)
        ui_item.lab_mecha_skin_name.setVisible(mecha_visible)
        ui_item.temp_tier.setVisible(mecha_visible)
        if ui_item.temp_level_role.nd_kind.isVisible() and ui_item.temp_level_role.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        elif ui_item.temp_level_mecha.nd_kind.isVisible() and ui_item.temp_level_mecha.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        else:
            ui_item.bar_level_bg.setVisible(False)

    def on_guangmu_change(self, guangmu_id):
        self._cur_use_guangmu = guangmu_id
        self._get_use_buy_widget.refresh_widget()
        for index, ui_item in enumerate(self.panel.list_item_long.GetAllItem()):
            valid = index < len(self.selected_effect_list) and self.selected_effect_list[index] is not None
            if not valid:
                continue
            ui_item.img_using.setVisible(str(guangmu_id) == str(self.selected_effect_list[index]))

        return

    def play_guangmu_by_type--- This code section failed: ---

 134       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'format'
           6  LOAD_ATTR             1  'format'
           9  LOAD_FAST             1  'g_type'
          12  CALL_FUNCTION_1       1 
          15  LOAD_CONST            0  ''
          18  CALL_FUNCTION_3       3 
          21  STORE_FAST            2  'func'

 135      24  LOAD_GLOBAL           3  'callable'
          27  LOAD_FAST             2  'func'
          30  CALL_FUNCTION_1       1 
          33  JUMP_IF_FALSE_OR_POP    42  'to 42'
          36  LOAD_FAST             2  'func'
          39  CALL_FUNCTION_0       0 
        42_0  COME_FROM                '33'
          42  POP_TOP          
          43  LOAD_CONST            0  ''
          46  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 18

    def play_loading_guangmu(self):
        self.panel.temp_flag.setVisible(True)
        guangmu_config = self.guangmu_config_dict.get(str(self._cur_guangmu), {})
        if not guangmu_config:
            return
        if self.cur_flag_guangmu != self._cur_guangmu:
            if self.panel.temp_flag.nd_guangmu.guangmu_item:
                self.panel.temp_flag.nd_guangmu.guangmu_item.RemoveFromParent()
            flag_guangmu_path = guangmu_config.get('loading_flag_vx_path')
            if flag_guangmu_path:
                global_data.uisystem.load_template_create(flag_guangmu_path, parent=self.panel.temp_flag.nd_guangmu, name='guangmu_item')
            self.cur_flag_guangmu = self._cur_guangmu
        if self.panel.temp_flag.nd_guangmu.guangmu_item:
            if self.panel.temp_flag.nd_guangmu.guangmu_item.IsPlayingAnimation('show'):
                self.panel.temp_flag.nd_guangmu.guangmu_item.StopAnimation('show')
            self.panel.temp_flag.nd_guangmu.guangmu_item.PlayAnimation('show')
        if self.cur_bg_guangmu != self._cur_guangmu:
            if self.panel.nd_guangmu.temp_guangmu.guangmu_item:
                self.panel.nd_guangmu.temp_guangmu.guangmu_item.RemoveFromParent()
            bg_guangmu_path = guangmu_config.get('loading_bg_vx_path')
            if bg_guangmu_path:
                global_data.uisystem.load_template_create(bg_guangmu_path, parent=self.panel.nd_guangmu.temp_guangmu, name='guangmu_item')
            self.cur_bg_guangmu = self._cur_guangmu
        if self.panel.nd_guangmu.temp_guangmu.guangmu_item:
            if self.panel.nd_guangmu.temp_guangmu.guangmu_item.IsPlayingAnimation('show'):
                self.panel.nd_guangmu.temp_guangmu.guangmu_item.StopAnimation('show')
            self.panel.nd_guangmu.temp_guangmu.guangmu_item.PlayAnimation('show')
        guangmu_sound = guangmu_config.get('loading_sound')
        self.play_guangmu_sound(guangmu_sound)

    def play_guangmu_sound(self, sound_name):
        sound_mgr = global_data.sound_mgr
        if self.cur_sound_id:
            sound_mgr.stop_playing_id(self.cur_sound_id)
            self.cur_sound_id = None
        if sound_name:
            self.cur_sound_id = sound_mgr.post_event_2d_non_opt(sound_name, None)
        return

    def clear_guangmu_by_type--- This code section failed: ---

 182       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'format'
           6  LOAD_ATTR             1  'format'
           9  LOAD_FAST             1  'g_type'
          12  CALL_FUNCTION_1       1 
          15  LOAD_CONST            0  ''
          18  CALL_FUNCTION_3       3 
          21  STORE_FAST            2  'func'

 183      24  LOAD_GLOBAL           3  'callable'
          27  LOAD_FAST             2  'func'
          30  CALL_FUNCTION_1       1 
          33  JUMP_IF_FALSE_OR_POP    42  'to 42'
          36  LOAD_FAST             2  'func'
          39  CALL_FUNCTION_0       0 
        42_0  COME_FROM                '33'
          42  POP_TOP          
          43  LOAD_CONST            0  ''
          46  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 18

    def clear_loading_guangmu(self):
        self.panel.temp_flag.setVisible(False)
        if self.panel.temp_flag.nd_guangmu.guangmu_item:
            self.panel.temp_flag.nd_guangmu.guangmu_item.RemoveFromParent()
        self.cur_flag_guangmu = None
        if self.panel.nd_guangmu.guangmu_item:
            self.panel.nd_guangmu.guangmu_item.RemoveFromParent()
        self.cur_bg_guangmu = None
        return

    def on_switch_guangmu_type(self, g_type, force=False):
        if g_type == self._cur_guangmu_type:
            if not force:
                return
        else:
            self.clear_guangmu_by_type(self._cur_guangmu_type)
        self.play_guangmu_by_type(g_type)
        self._cur_guangmu_type = g_type
        self.panel.list_tab_guangmu.GetItem(0).btn_icon.SetSelect(g_type == TYPE_LOADING)
        self.panel.list_tab_guangmu.GetItem(0).btn_title.SetSelect(g_type == TYPE_LOADING)
        self.panel.list_tab_guangmu.GetItem(1).btn_icon.SetSelect(g_type == TYPE_TV)
        self.panel.list_tab_guangmu.GetItem(1).btn_title.SetSelect(g_type == TYPE_TV)
        self.panel.list_tab_guangmu.GetItem(2).btn_icon.SetSelect(g_type == TYPE_SKY)
        self.panel.list_tab_guangmu.GetItem(2).btn_title.SetSelect(g_type == TYPE_SKY)

    def get_default_select_item_no(self):
        return self._cur_guangmu

    def on_create_skin_item(self, lst, index, item_widget):
        valid = index < len(self.selected_effect_list) and self.selected_effect_list[index] is not None
        if valid:
            item_widget.nd_kind.setVisible(True)
            item_widget.img_level.setVisible(True)
            item_widget.nd_content.setVisible(True)
            item_widget.bar.SetEnable(True)
            skin_no = self.selected_effect_list[index]
            item_widget.item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(skin_no))
            item_widget.lab_name.SetString(get_lobby_item_name(skin_no))
            cur_use_guangmu = None
            if global_data.player:
                cur_use_guangmu = global_data.player.get_selected_guangmu()
            item_widget.img_using.setVisible(str(cur_use_guangmu) == str(skin_no))
            item_can_use, _ = item_can_use_by_item_no(skin_no)
            item_widget.img_lock.setVisible(not item_can_use)
            check_skin_tag(item_widget.nd_kind, skin_no)
            check_skin_bg_tag(item_widget.img_level, skin_no, is_small_item=True)
            item_widget.bar.SetEnable(True)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
            show_red_point_template(item_widget.nd_new, show_new)
            show_remain_time(item_widget.lab_limited, item_widget.lab_limited, skin_no)
            item_widget.bar.SetNoEventAfterMove(True)
            item_widget.bar.BindMethod('OnClick', Functor(self.on_click_skin_item, index))
            item_widget.bar.UnBindMethod('OnBegin')
            item_widget.bar.UnBindMethod('OnDrag')
            item_widget.bar.UnBindMethod('OnEnd')
            item_widget.bar.UnBindMethod('OnCancel')
            item_widget.lab_limited.stopAllActions()
            item_widget.lab_limited.setVisible(False)
        else:
            item_widget.nd_kind.setVisible(False)
            item_widget.img_level.setVisible(False)
            item_widget.nd_content.setVisible(False)
            item_widget.bar.SetEnable(False)
        return

    def on_click_skin_item(self, index, *args):
        if not self.panel or not self.page_showing:
            return
        else:
            if self.sel_before_cb:
                self.sel_before_cb(self.get_parent_selected_item_index(), index)
            self._cur_guangmu = item_no = self.selected_effect_list[index]
            guangmu_config = self.guangmu_config_dict.get(item_no, {})
            has_tv_path = bool(guangmu_config.get('tv_vx_path'))
            has_sky_path = has_tv_path and bool(guangmu_config.get('sky_guangmu_path'))
            btn = self.panel.list_tab_guangmu.GetItem(0)
            btn.setVisible(True)
            btn.img_line_1.SetDisplayFrameByPath('', LIST_LINE_PIC if has_tv_path else LIST_END_PIC)
            btn = self.panel.list_tab_guangmu.GetItem(1)
            btn.setVisible(has_tv_path)
            btn.img_line_1.SetDisplayFrameByPath('', LIST_LINE_PIC if has_sky_path else LIST_END_PIC)
            btn = self.panel.list_tab_guangmu.GetItem(2)
            btn.setVisible(has_sky_path)
            self.on_switch_guangmu_type(TYPE_LOADING, force=True)
            self.panel.lab_name.SetString(get_lobby_item_name(item_no))
            self.panel.lab_name.setVisible(True)
            self.panel.lab_describe.setVisible(False)
            item_widget = self.panel.list_item_long.GetItem(index)
            if item_widget and global_data.lobby_red_point_data.get_rp_by_no(item_no):
                global_data.player.req_del_item_redpoint(item_no)
                show_red_point_template(item_widget.nd_new, False)
            global_data.emgr.select_item_goods.emit(item_no)
            self._get_use_buy_widget.update_target_item_no(item_no, guangmu_config.get('goods_id', None))
            if self.sel_callback:
                self.sel_callback()
            return

    def on_update_scene(self):
        super(GuangmuFunctionWidget, self).on_update_scene()
        self.page_showing = True
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_JIEMIAN_COMMON, ITEMBOOKS_GESTURE_MANAGE, scene_content_type=SCENE_ITEM_BOOK)
        global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def on_clear_effect(self):
        if self.cur_sound_id:
            global_data.sound_mgr.stop_playing_id(self.cur_sound_id)
            self.cur_sound_id = None
        return

    def on_leave_page(self):
        self.page_showing = False

    def destroy(self):
        super(GuangmuFunctionWidget, self).destroy()
        self._get_use_buy_widget.destroy()
        self._get_use_buy_widget = None
        self.process_event(False)
        return