# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/InscriptionMainUI.py
from __future__ import absolute_import
import cc
import logic.gcommon.const as gconst
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.utils.redpoint_check_func import check_inscription_all_mecha_module_red_point, check_inscription_module_red_point
from logic.client.const import lobby_model_display_const
from logic.gcommon.item import lobby_item_type
from logic.gcommon.common_const import mecha_const, scene_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_NONE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.comsys.mecha_display.MechaLobbyModuleWidget import MechaLobbyModuleWidget
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import mecha_skin_utils
from logic.gutils import lobby_model_display_utils
import world
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_path
from logic.gutils.template_utils import init_price_view, show_remain_time, init_foldable_menu
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_DISPLAY_PIC, ROTATE_FACTOR
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from logic.gutils.system_unlock_utils import is_sys_unlocked, show_sys_unlock_tips, SYSTEM_INSCRIPTION
from logic.gutils import red_point_utils
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
from common.const import uiconst
MECHA_VIEW_MODEL = 0
MECHA_VIEW_PIC = 1

class InscriptionMechaList(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/inscription/i_inscription_name'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_change.OnClick': 'on_click_choose_btn'
       }
    GLOBAL_EVENT = {'player_item_update_event': '_on_buy_good_success',
       'del_item_red_point': 'refresh_red_point',
       'del_item_red_point_list': 'refresh_red_point',
       'update_proficiency_reward_event': 'refresh_red_point',
       'update_mecha_module_plan_result_event': 'refresh_red_point',
       'on_update_mecha_module_plans': 'refresh_red_point',
       'mecha_component_update_event': 'on_refresh_rp',
       'mecha_component_slot_unlocked_event': 'on_refresh_rp',
       'mecha_component_change_active_page': 'on_refresh_rp'
       }

    def on_init_panel(self, *args, **kwargs):
        global_data.redpoint_mgr.register_redpoint(self.panel.temp_red, '8')
        self._show_rank_list = False
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self.init_open_lst()
        self.refresh_mecha_list()

        @self.panel.callback()
        def OnClick(btn, touch):
            self.on_click_nd_change(btn, touch)

        self.hide()

    def init_open_lst(self):
        if not global_data.player:
            self.close()
            return
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            self._open_mecha_lst = []
            self._all_mecha_lst = []
            for mecha_id in mecha_open_info['opened_order']:
                self._all_mecha_lst.append(mecha_id)
                if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                    self._open_mecha_lst.append(mecha_id)

        self._all_mecha_lst = sorted(self._all_mecha_lst, key=lambda x: (x not in self._open_mecha_lst, x))

    def on_finalize_panel(self):
        self._switch_cb = None
        self._mecha_conf = None
        return

    def set_mecha_change_callback(self, cb):
        self._switch_cb = cb

    def on_click_choose_btn(self, btn, touch):
        self._show_rank_list = not self._show_rank_list
        if self._show_rank_list:
            self.panel.PlayAnimation('change')
            self.refresh_mecha_list()
        else:
            self.hide_mecha_list()

    def on_click_nd_change(self, btn, touch):
        if self.panel.btn_change.IsPointIn(touch.getLocation()):
            return
        self.hide_mecha_list()

    def _on_buy_good_success(self):
        if self._show_rank_list:
            self.refresh_mecha_list()

    def hide_mecha_list(self):
        self.panel.StopAnimation('change')
        self._show_rank_list = False
        self.panel.nd_rank_list.setVisible(False)

    def on_refresh_rp(self, *args):
        self.refresh_mecha_list()

    def refresh_red_point(self, *args, **kwarg):
        self.refresh_mecha_list()

    def refresh_mecha_list(self):
        from common.utils.redpoint_check_func import check_mecha_component_page_has_empty_slot
        has_red_point = False
        self.panel.list_rank_list.SetInitCount(len(self._all_mecha_lst))
        all_item = self.panel.list_rank_list.GetAllItem()
        for index, ui_item in enumerate(all_item):
            mecha_id = self._all_mecha_lst[index]
            conf = self._mecha_conf[str(mecha_id)]
            img_path = icon_path = 'gui/ui_res_2/mech_display/img_mech%s.png' % mecha_id
            ui_item.mech_head.SetDisplayFrameByPath('', img_path)
            ui_item.lab_mech_name.SetString(conf.get('name_mecha_text_id', ''))
            has_empty_slot = check_mecha_component_page_has_empty_slot(mecha_id)
            has_module_red_p = check_inscription_module_red_point(mecha_id)
            has_single_red_point = has_empty_slot or has_module_red_p
            if has_single_red_point:
                has_red_point = True
            red_point_utils.show_red_point_template(ui_item.temp_red, has_single_red_point)
            ui_item.mech_head_shade.SetDisplayFrameByPath('', img_path)
            ui_item.img_lock.setVisible(mecha_id not in self._open_mecha_lst)

            @ui_item.btn_shose_mech.callback()
            def OnBegin(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                return True

            @ui_item.btn_shose_mech.callback()
            def OnEnd(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                pass

            @ui_item.btn_shose_mech.callback()
            def OnCancel(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                pass

            @ui_item.btn_shose_mech.callback()
            def OnClick(btn, touch, mecha_id=mecha_id):
                self.hide_mecha_list()
                if self._switch_cb:
                    self._switch_cb(mecha_id)

        red_point_utils.show_red_point_template(self.panel.nd_mecha_choose.temp_red, has_red_point)

    def switch_cur_mecha(self, mecha_id):
        self.show()
        img_path = icon_path = 'gui/ui_res_2/mech_display/img_mech%s.png' % mecha_id
        self.panel.item.SetDisplayFrameByPath('', img_path)
        conf = self._mecha_conf[str(mecha_id)]
        mecha_name = conf.get('name_mecha_text_id', '')
        self.panel.lab_mecha_name.SetString(mecha_name)
        is_own = global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id))
        self.panel.lab_mecha_no.setVisible(not is_own)


class InscriptionMainUI(BasePanel):
    RECONSTRUCT_WIDGET_IND = 0
    INSCR_BAG_WIDGET_IND = 1
    INSCR_MODULE_IND = 2
    PANEL_CONFIG_NAME = 'mech_display/inscription/inscription_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    BG_CONFIG_NAME = 'mech_display/inscription/bg_bag'
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': '_on_click_back_btn',
       'btn_back.OnClick': '_on_click_inner_back_btn'
       }
    GLOBAL_EVENT = {'on_lobby_mecha_changed': 'change_lobby_mecha',
       'show_to_gain_method_page_event': 'show_to_gain_method_page',
       'del_item_red_point': 'refresh_red_point',
       'del_item_red_point_list': 'refresh_red_point',
       'update_proficiency_reward_event': 'refresh_red_point',
       'update_mecha_module_plan_result_event': 'refresh_red_point',
       'on_update_mecha_module_plans': 'refresh_red_point'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_param()
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self.init_parameters()
        self.init_open_lst()
        self.init_tab_list()
        self.panel.temp_btn_back.btn_back.set_click_sound_name('ui_click_mecha_back')
        self._mecha_list_ui = InscriptionMechaList()
        self.add_associate_vis_ui(self._mecha_list_ui.__class__.__name__)
        self._mecha_list_ui.set_mecha_change_callback(self.show_mecha_details)
        bg_panel = self.get_bg_panel()
        if bg_panel:
            bg_panel.panel.img_bg.setVisible(False)

    def set_close_cb(self, cb):
        self._close_cb = cb

    def on_finalize_panel(self):
        if self._mecha_list_ui:
            self.remove_associate_vis_ui(self._mecha_list_ui.__class__.__name__)
            global_data.ui_mgr.close_ui(self._mecha_list_ui.__class__.__name__)
            self._mecha_list_ui = None
        self._temp_btn_back_callback = None
        self.tab_list_data = []
        self._mecha_info_conf = None
        self._mecha_skin_conf = None
        self.destroy_widget('widgets_helper')
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        global_data.game_mgr.scene.enable_blur_with_mask(False)
        self.show_main_ui()
        if callable(self._close_cb):
            self._close_cb()
        return

    def init_open_lst(self):
        if not global_data.player:
            self.close()
            return
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            self._open_mecha_lst = []
            self._all_mecha_lst = []
            for mecha_id in mecha_open_info['opened_order']:
                self._all_mecha_lst.append(mecha_id)
                if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                    self._open_mecha_lst.append(mecha_id)

        self._all_mecha_lst = sorted(self._all_mecha_lst, key=lambda x: (x not in self._open_mecha_lst, x))

    def is_reconstruct_opened(self):
        if not global_data.player.has_open_inscription(False) or not global_data.player.has_open_inscription():
            return False
        return True

    def init_parameters(self):
        self.RECONSTRUCT_WIDGET_IND = 0
        self.INSCR_BAG_WIDGET_IND = 1
        self.INSCR_MODULE_IND = 2
        self._tab_sel_index = None
        self.widgets_helper = None
        self._is_reversed_menu = False
        if self.is_reconstruct_opened():
            self._default_page = self.RECONSTRUCT_WIDGET_IND
        else:
            self._default_page = self.INSCR_MODULE_IND
        self.tab_list_data = [
         {'text': 81943,
            'widget_func': self.init_mecha_reconstruct_widget,
            'widget_template': 'mech_display/inscription/i_mech_info_inscription'
            },
         {'text': 868028,
            'widget_func': self.init_mecha_inscr_bag_widget,
            'widget_template': 'mech_display/inscription/i_inscription_bag'
            },
         {'text': 29925,
            'widget_func': self.init_mecha_module_widget,
            'widget_template': 'mech_display/i_mech_info_module',
            'red_point_func': check_inscription_module_red_point
            }]
        return

    def init_tab_list(self):
        from logic.comsys.common_ui.WidgetCommonComponent import WidgetCommonComponent
        menu_conf = [{'data': {'text': 81779},'list_template': 'common/i_left_second_small_tab_list','force_open': self.is_reconstruct_opened(),'menu_list': [{'data': self.tab_list_data[self.RECONSTRUCT_WIDGET_IND]}, {'data': self.tab_list_data[self.INSCR_BAG_WIDGET_IND]}]}, {'data': self.tab_list_data[self.INSCR_MODULE_IND]}]

        def init_func(item_widget, conf):
            text = conf.get('data', {}).get('text', '')
            item_widget.lab_tab.SetString(text)
            menu_list = conf.get('menu_list', [])
            if menu_list:
                item_widget.img_arrow.setVisible(True)
            else:
                item_widget.img_arrow.setVisible(False)

        def init_sub_func(item_widget, conf):
            item_widget.button.SetSelect(False)
            item_widget.button.SetText(conf['data']['text'])
            info = conf['data']
            redpoint_id = info.get('redpoint_id', '')
            if redpoint_id:
                global_data.redpoint_mgr.register_redpoint(item_widget.button.img_red, redpoint_id)

        def select_cb(item_widget, conf, only_status=False):
            item_widget.btn_tab.SetSelect(True)
            item_widget.lab_tab.SetFontSize(20)
            item_widget.lab_tab.SetColorCheckRecord('#SW')
            if only_status:
                return
            menu_list = conf.get('menu_list', [])
            if menu_list:
                sub_conf = menu_list[0]
                sub_conf['button.OnClick']()
            else:
                data = conf.get('data', {})
                if self.widgets_helper and data in self.tab_list_data:
                    index = self.tab_list_data.index(data)
                    self._click_valid_tab(index)
                self.refresh_menu_status()

        def unselect_cb(item_widget, conf):
            item_widget.btn_tab.SetEnable(True)
            item_widget.btn_tab.SetSelect(False)
            item_widget.lab_tab.SetFontSize(20)
            item_widget.lab_tab.ReConfColor()

        def sub_select_cb(item_widget, conf):
            item_widget.button.SetSelect(True)
            data = conf.get('data', {})
            if self.widgets_helper and data in self.tab_list_data:
                index = self.tab_list_data.index(data)
                self._click_valid_tab(index)
            self.refresh_menu_status()

        def sub_unselect_cb(item_widget, conf):
            item_widget.button.SetSelect(False)

        def OnClick(*args, **kwargs):
            if not self.is_reconstruct_opened():
                if not global_data.player.has_open_inscription(False):
                    global_data.game_mgr.show_tip(get_text_by_id(2139))
                elif not global_data.player.has_open_inscription():
                    show_sys_unlock_tips(SYSTEM_INSCRIPTION)
                return False
            return True

        for i, conf in enumerate(menu_conf):
            conf['init_func'] = init_func
            conf['select_cb'] = select_cb
            conf['unselect_cb'] = unselect_cb
            if i == 0:
                conf['btn_tab.OnClick'] = OnClick
            else:
                conf['btn_tab.OnClick'] = 1
            for sub_conf in conf.get('menu_list', []):
                sub_conf['init_func'] = init_sub_func
                sub_conf['select_cb'] = sub_select_cb
                sub_conf['unselect_cb'] = sub_unselect_cb
                sub_conf['button.OnClick'] = 1

        if not self.is_reconstruct_opened():
            menu_conf.reverse()
            self._is_reversed_menu = True
        self._menu_conf = menu_conf
        self.panel.list_tab.DeleteAllSubItem()
        init_foldable_menu(self.panel.list_tab, menu_conf)
        self.widgets_helper = WidgetCommonComponent(self.panel.nd_content, self.tab_list_data)
        self.widgets_helper.set_widget_switch_func(self.on_widget_switch)

    def get_inscr_list_tab_btn(self):
        if not global_data.player.has_open_inscription():
            return
        nd_top = self._is_reversed_menu or self.panel.list_tab.GetItem(1) if 1 else self.panel.list_tab.GetItem(2)
        if nd_top:
            return nd_top.GetItem(1)

    def refresh_menu_status(self):
        if not self._menu_conf:
            return
        else:
            if self._tab_sel_index == None:
                return
            select_data = self.tab_list_data[self._tab_sel_index]
            for conf in self._menu_conf:
                data = conf['data']
                menu_item_widget = conf.get('menu_item_widget')
                menu1_select = False
                if data == select_data:
                    menu1_select = True
                else:
                    for sub_conf in conf.get('menu_list', []):
                        sub_data = sub_conf['data']
                        if sub_data == select_data:
                            menu1_select = True
                        else:
                            sub_conf['unselect_cb'](sub_conf.get('menu_item_widget'), sub_conf)

                if menu1_select:
                    conf['select_cb'](menu_item_widget, conf, only_status=True)
                else:
                    conf['unselect_cb'](menu_item_widget, conf)

            return

    def switch_to_menu(self, index):
        if not self._menu_conf:
            return
        select_data = self.tab_list_data[index]
        for conf in self._menu_conf:
            data = conf['data']
            if data == select_data:
                conf['btn_tab.OnClick']()
                return
            for sub_conf in conf.get('menu_list', []):
                sub_data = sub_conf['data']
                if sub_data == select_data:
                    conf['btn_tab.OnClick']()
                    sub_conf['button.OnClick']()
                    return

    def refresh_red_point(self, *args, **kwarg):
        for conf in self._menu_conf:
            data = conf['data']
            red_point_func = data.get('red_point_func', None)
            item_widget = conf['menu_item_widget']
            if red_point_func and red_point_func(self._cur_mecha_id):
                show_rp = True if 1 else False
                red_point_utils.show_red_point_template(item_widget.temp_red, show_rp)
                for sub_conf in conf.get('menu_list', []):
                    sub_data = sub_conf['data']
                    red_point_func = sub_data.get('red_point_func', None)
                    red_point_id = sub_data.get('redpoint_id')
                    if red_point_id:
                        continue
                    sub_item_widget = sub_conf['menu_item_widget']
                    if red_point_func and red_point_func():
                        show_rp = True if 1 else False
                        red_point_utils.show_red_point_template(sub_item_widget.img_red, show_rp)

        return

    def _click_valid_tab(self, index):
        self.panel.img_bar_shadow.setVisible(index in [self.INSCR_BAG_WIDGET_IND])
        has_disposable_scene = [
         self.RECONSTRUCT_WIDGET_IND, self.INSCR_MODULE_IND]
        bg_panel = self.get_bg_panel()
        if bg_panel:
            bg_panel.panel.img_shade_left.setVisible(index in has_disposable_scene)
            bg_panel.panel.img_shade_right.setVisible(index in has_disposable_scene)
        old_index = self._tab_sel_index
        self._tab_sel_index = index
        if self.widgets_helper.get_cur_index() == index:
            return
        else:
            if index == self.INSCR_BAG_WIDGET_IND:
                self.set_temp_btn_back_callback(lambda : self.select_type(self.RECONSTRUCT_WIDGET_IND))
            else:
                self.set_temp_btn_back_callback(None)
            if self.widgets_helper:
                self.widgets_helper.on_switch_to_widget(index)
            if index == self.INSCR_MODULE_IND:
                global_data.emgr.operate_sfx_model.emit(0, {'vertex_color_mask': MECHA_PART_MAP[MECHA_PART_NONE]})
            self.refresh_cur_tab_cam(old_index, index)
            return

    def init_mecha_reconstruct_widget(self, nd):
        from logic.comsys.mecha_display.MechaReconstructWidget import MechaReconstructWidget
        inst = MechaReconstructWidget(self, nd, self._cur_mecha_id)
        return inst

    def init_mecha_inscr_bag_widget(self, nd):
        from logic.comsys.mecha_display.MechaInscriptionBagWidget import MechaInscriptionBagWidget
        inst = MechaInscriptionBagWidget(self, nd, self._cur_mecha_id)
        return inst

    def init_mecha_inscr_store_widget(self, nd):
        from logic.comsys.mecha_display.MechaInscriptionStoreWidget import MechaInscriptionStoreWidget
        inst = MechaInscriptionStoreWidget(self, nd, self._cur_mecha_id)
        return inst

    def init_mecha_module_widget(self, nd):
        from logic.comsys.mecha_display.MechaLobbyModuleWidget import MechaLobbyModuleWidget
        widget = MechaLobbyModuleWidget(self, nd, self._cur_mecha_id)
        widget.init_widget(self._cur_mecha_id)
        return widget

    def on_click_back_btn(self, btn, touch):
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.on_click_close_btn()

    def on_click_close_btn(self):
        self.close()

    def _on_show_last_mecha(self, *args):
        if self._cur_mecha_id in self._all_mecha_lst:
            index = self._all_mecha_lst.index(self._cur_mecha_id)
        else:
            index = 1
        last_index = len(self._all_mecha_lst) - 1 if index == 0 else index - 1
        self.show_mecha_details(self._all_mecha_lst[last_index])

    def init_param(self):
        self.disappearing = False
        self._mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._cur_mecha_goods_id = None
        self._open_mecha_lst = [
         8001]
        self._cur_mecha_id = None
        self._cur_mecha_cam_data = None
        self._cur_cam_mode = CAM_MODE_FAR
        self.clothing_selected_index = 0
        self.cur_clothing_id = 0
        self._has_load_scene = False
        self._close_cb = None
        return

    def _on_show_next_mecha(self, *args):
        if self._cur_mecha_id in self._all_mecha_lst:
            index = self._all_mecha_lst.index(self._cur_mecha_id)
        else:
            index = len(self._all_mecha_lst) - 1
        next_index = 0 if index == len(self._all_mecha_lst) - 1 else index + 1
        self.show_mecha_details(self._all_mecha_lst[next_index])

    def show_mecha_details(self, mecha_id=None):
        if not mecha_id:
            if self._cur_mecha_id:
                mecha_id = self._cur_mecha_id
            else:
                mecha_id = global_data.player.get_lobby_selected_mecha_id()
        if self._cur_mecha_id == mecha_id:
            return
        self._cur_mecha_id = mecha_id
        self._cur_mecha_cam_data = lobby_model_display_utils.get_mecha_display_cam_data(str(mecha_id))
        self._cur_mecha_goods_id = self._mecha_info_conf.get(str(mecha_id), {}).get('goods_id')
        self.clothing_selected_index = 0
        self.change_lobby_model_display(mecha_id)

        def _cb():
            self.refresh_red_point()
            if self.widgets_helper:
                if self.widgets_helper.cur_index is None:
                    self.switch_to_menu(self._default_page)
                cur_widget = self.widgets_helper.get_cur_widget()
                if cur_widget:
                    cur_widget.on_switch_to_mecha_type(self._cur_mecha_id)
            if self._mecha_list_ui:
                self._mecha_list_ui.switch_cur_mecha(self._cur_mecha_id)
            return

        self.StopTimerActionByTag(99)
        self.panel.SetTimeOut(0.1, _cb, 99)

    def refresh_cur_tab_cam(self, old_index, index):
        has_disposable_scene = [
         self.RECONSTRUCT_WIDGET_IND, self.INSCR_MODULE_IND]
        if index in has_disposable_scene:
            scene = world.get_active_scene()
            cam_hanger = scene.get_preset_camera('camera_display_01')
            wpos = cam_hanger.translation
            wrot = cam_hanger.rotation
            offset = 20 if index == self.INSCR_MODULE_IND else 0
            is_slerp = True if old_index in has_disposable_scene else False
            global_data.emgr.change_model_display_scene_cam_trans.emit(wpos + wrot.right * offset, None, is_slerp)
        return

    def set_cur_clothing_id(self, clothing_id):
        old_clothing_id = self.cur_clothing_id
        self.cur_clothing_id = clothing_id

    def load_scene(self):
        if self._has_load_scene:
            return
        self._has_load_scene = True
        display_type = lobby_model_display_const.SCENE_MECHA_RECONSTRUCT
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_MECHA_RECONSTRUCT, display_type)

    def get_show_cloth_id(self):
        skin_list = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(self._cur_mecha_id), 'skins', default=[])
        clothing_id = skin_list[0]
        return clothing_id

    def change_mecha_model(self, mecha_id, clothing_id, shiny_id):
        mpath = get_mecha_model_path(mecha_id, clothing_id)
        submesh_path = get_mecha_model_h_path(mecha_id, clothing_id)
        item_no = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no, is_get_player_data=False, consider_second_model=False)
        for data in model_data:
            data['mpath'] = mpath
            data['sub_mesh_path_list'] = [submesh_path]
            if not data['mecha_end_ani']:
                continue
            data['show_anim'] = data['mecha_end_ani']
            data['end_anim'] = data['mecha_end_ani']
            data['skin_id'] = clothing_id
            if shiny_id:
                data['shiny_preview'] = shiny_id
            model_scale = 3.0
            if mecha_id == 8011:
                model_scale = 2.5
            data['show_anim'] = data['end_anim']
            data['show_sfx_model'] = True
            data['model_scale'] = model_scale
            data['off_euler_rot'] = [0, -90, 0]

        global_data.emgr.change_model_display_scene_item.emit(model_data)

    def change_lobby_model_display(self, mecha_id, shiny_id=None, force_refresh=False):
        clothing_id = self.get_show_cloth_id()
        old_clothing_id = self.cur_clothing_id
        if not force_refresh and clothing_id == old_clothing_id:
            return
        self.cur_clothing_id = clothing_id
        self.load_scene()
        self.change_mecha_model(mecha_id, clothing_id, shiny_id)

    def _on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        global_data.emgr.reset_rotate_model_display.emit()
        self.close()

    def _on_click_inner_back_btn(self, *args):
        if callable(self._temp_btn_back_callback):
            self._temp_btn_back_callback()
            return

    def on_widget_switch(self, index, widget, is_show):
        if is_show:
            if index in [self.RECONSTRUCT_WIDGET_IND, self.INSCR_MODULE_IND]:
                self._mecha_list_ui.add_show_count('correct_index')
                node = self._mecha_list_ui.panel
                node.retain()
                node.RemoveFromParent()
                if index == self.RECONSTRUCT_WIDGET_IND:
                    widget.panel.nd_mecha_list.AddChild('', node, 0)
                    import cc
                    lpos = widget.panel.nd_mecha_list_real.getPosition()
                    wpos = widget.panel.nd_mecha_list.getParent().convertToWorldSpace(lpos)
                    lpos2 = widget.panel.nd_mecha_list.getParent().convertToNodeSpace(wpos)
                    widget.panel.nd_mecha_list.setPosition(lpos2)
                    sz = widget.panel.nd_mecha_list.getContentSize()
                    node.setPosition(cc.Vec2(sz.width / 2.0, sz.height / 2.0))
                else:
                    widget.panel.AddChild('', node, 1)
                    node.SetPosition('50%', '50%')
                node.release()
            else:
                self._mecha_list_ui.add_hide_count('correct_index')
            bg_panel = self.get_bg_panel()
            if bg_panel:
                if index in [self.INSCR_BAG_WIDGET_IND]:
                    bg_panel.panel.img_bg.setVisible(True)
                    pic = 'gui/ui_res_2/mech_display/inscription/bg_bag_pnl.png'
                    bg_panel.panel.img_bg.SetDisplayFrameByPath('', pic)
                else:
                    bg_panel.panel.img_bg.setVisible(False)
            widget.on_switch_to_mecha_type(self._cur_mecha_id)

    def do_show_panel(self):
        super(InscriptionMainUI, self).do_show_panel()
        if self._cur_mecha_id:
            if self.widgets_helper:
                cur_widget = self.widgets_helper.get_cur_widget()
                if cur_widget:
                    cur_widget.on_switch_to_mecha_type(self._cur_mecha_id)
        self.on_reset_lobby_model()
        default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(self._cur_mecha_id), 'default_fashion')

    def do_hide_panel(self):
        super(InscriptionMainUI, self).do_hide_panel()
        self._has_load_scene = False

    def on_reset_lobby_model(self):
        from logic.gcommon.common_const import scene_const
        if self._cur_mecha_id is not None:
            self.change_lobby_model_display(self._cur_mecha_id, force_refresh=True)
        else:
            self.show_mecha_details()
        return

    def change_lobby_mecha(self):
        cur_mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        name_text = item_utils.get_lobby_item_name(cur_mecha_item_id)
        global_data.game_mgr.show_tip(get_text_by_id(14011, {'name': name_text}))

    def switch_view_type(self, view_type, mecha_id, clothing_id, shiny_id):
        self.change_lobby_model_display(mecha_id, shiny_id)

    def switch_to_tab(self, tab_ind):
        if self.widgets_helper:
            self.widgets_helper.on_switch_to_widget(tab_ind)

    def tech_red_point_check_func(self):
        from common.utils.redpoint_check_func import check_mecha_component_page_has_empty_slot
        for mecha_id in self._open_mecha_lst:
            if check_mecha_component_page_has_empty_slot(mecha_id):
                return True

        return False

    def select_type(self, tab_ind, mecha_id=None):
        if not self.widgets_helper:
            return
        if mecha_id:
            self._mecha_list_ui.switch_cur_mecha(mecha_id)
        self.show_mecha_details(mecha_id=mecha_id)
        self.switch_to_menu(tab_ind)

    def select_module_btn(self, module_btn_idx):
        if self.widgets_helper:
            cur_widget = self.widgets_helper.get_cur_widget()
            if cur_widget:
                if isinstance(cur_widget, MechaLobbyModuleWidget):
                    cur_widget.select_module_btn(module_btn_idx)

    def get_cur_widget(self):
        if self.widgets_helper:
            if self.widgets_helper.cur_index is None:
                self.switch_to_menu(self._default_page)
            cur_widget = self.widgets_helper.get_cur_widget()
            return cur_widget
        else:
            return

    def get_cur_widget_index(self):
        if self.widgets_helper:
            return self.widgets_helper.cur_index
        else:
            return None

    def show_to_gain_method_page(self, gain_method, proficiency_level=None):
        if gain_method == mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY:
            global_data.ui_mgr.close_ui('MechaDetails')
            global_data.ui_mgr.show_ui('MallMainUI', 'logic.comsys.mall_ui')
        elif gain_method == mecha_const.MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD:
            from logic.comsys.mecha_display.MechaProficiencyDetailsUI import MechaProficiencyDetailsUI
            ui = MechaProficiencyDetailsUI(None, self._cur_mecha_id)
            ui.locate_proficiency_level(proficiency_level)
        return

    def set_temp_btn_back_callback(self, callback):
        self._temp_btn_back_callback = callback
        if not callback:
            self.panel.btn_back.setVisible(False)
            self.panel.temp_btn_back.setVisible(True)
        else:
            self.panel.btn_back.setVisible(True)
            self.panel.temp_btn_back.setVisible(False)

    def get_tab_sel_index(self):
        return self._tab_sel_index