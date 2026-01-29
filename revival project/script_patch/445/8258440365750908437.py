# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
import logic.gcommon.const as gconst
from logic.comsys.common_ui.WidgetCommonComponent import WidgetCommonComponent
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gcommon.common_const.scene_const import SCENE_SKIN_DEFINE
from logic.client.const.lobby_model_display_const import SKIN_DEFINE
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path, battle_id_to_mecha_lobby_id, get_mecha_model_offset_y
import math3d
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import show_remain_time, init_price_view
from logic.gcommon.item.item_const import FASHION_POS_SUIT
import cc
from common.utils.cocos_utils import ccp
from common.utils.ui_utils import get_scale
from logic.gutils.skin_define_utils import get_main_skin_id, get_default_skin_define_anim
from logic.gutils import mall_utils
from logic.comsys.mecha_display.SkinDefineBuyUI import SkinDefineBuyUI
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.vscene.parts.camera.camera_controller.model_decal_cam_ctrl import MAX_RADIUS, MIN_RADIUS
from logic.comsys.mecha_display.SkinDefineColorWidget import SkinDefineColorWidget
from logic.comsys.mecha_display.SkinDefineDecalWidget import SkinDefineDecalWidget
from logic.comsys.mecha_display.MechaDiyInfoWidget import MechaDiyInfoWidget
from logic.comsys.mecha_display.SkinDefinePoseWidget import SkinDefinePoseWidget
from logic.gutils import red_point_utils

class SkinDefineUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/skin_define'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': '_on_click_back',
       'btn_details.OnClick': '_on_click_details'
       }
    LEFT_TAB = ('color', 'applique', 'effect', 'pose')
    TAB_WIDGETS = (SkinDefineColorWidget, SkinDefineDecalWidget, MechaDiyInfoWidget, SkinDefinePoseWidget)
    DELAY_TAG = 20200317
    selected_plan_idx = -1

    def on_init_panel(self, mecha_id, show_model_id, close_cb=None, default_tag_id=2, switch_to_widget_cb=None, *args, **kwargs):
        super(SkinDefineUI, self).on_init_panel()
        self.widgets_helper = None
        self.color_widget = None
        self.decal_widget = None
        self.effect_widget = None
        self._disappearing = False
        self.switch_to_widget_cb = switch_to_widget_cb
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self.init_parameters(mecha_id, show_model_id)
        self.process_events(True)
        self.init_widget(default_tag_id)
        self.init_ui_events()
        self._close_cb = close_cb
        global_data.player.set_need_update_skin_define(False)
        return

    def on_resolution_changed(self):
        cur_widget = self.widgets_helper.get_cur_widget()
        if cur_widget:
            cur_widget.on_resolution_changed()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_buy_goods_success,
           'mecha_main_skin_scheme_change_event': self.on_mecha_main_skin_scheme_change,
           'skin_define_batch_buy_event': self.on_batch_buy_update,
           'mall_init_sub_ui_price_widget': self.hide_top_price_widget,
           'mall_clear_sub_ui_price_widget': self.show_top_price_widget,
           'camera_decal_scl_event': self.on_camera_scl,
           'del_item_red_point': self.refresh_red_point,
           'del_item_red_point_list': self.refresh_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self, mecha_id, show_model_id):
        self.cur_model = None
        self.mecha_id = mecha_id
        self.model_id = show_model_id
        self._is_plan_show = False
        self.list_tab = []
        self.tag_btn_dict = {}
        self.mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self.mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self.batch_buy_item_list = []
        self._touch_start_dist = 0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self.FAR_MAX_SCL = 0.68
        self.FAR_MIN_SCL = 0.2
        self.NER_MAX_SCL = 1.5
        self.NER_MIN_SCL = 0.5
        self.MAX_SCL = self.FAR_MAX_SCL
        self.MIN_SCL = self.FAR_MIN_SCL
        return

    def init_widget(self, default_tag_id=0):
        self.price_top_widget = PriceUIWidget(self, list_money_node=self.panel.list_price)
        self.price_top_widget.show_money_types([
         '%d_%d' % (gconst.SHOP_PAYMENT_ITEM, gconst.SHOP_ITEM_COLOR),
         gconst.SHOP_PAYMENT_GOLD, gconst.SHOP_PAYMENT_DIAMON, gconst.SHOP_PAYMENT_YUANBAO])
        self.widget_data = [
         {'text': 866028,
            'widget_func': self.init_color_widget,
            'widget_template': 'mech_display/i_skin_define_color',
            'has_red_point_func': False,
            'widget_cls': SkinDefineColorWidget,
            'tag_name': 'color'
            },
         {'text': 866029,
            'widget_func': self.init_decal_widget,
            'widget_template': 'mech_display/i_skin_define_applique',
            'has_red_point_func': False,
            'widget_cls': SkinDefineDecalWidget,
            'tag_name': 'applique'
            },
         {'text': 80863,
            'widget_func': self.init_effect_widget,
            'widget_template': 'mech_display/i_mech_info_diy',
            'has_red_point_func': True,
            'widget_cls': MechaDiyInfoWidget,
            'tag_name': 'effect'
            },
         {'text': 906651,
            'widget_func': self.init_pose_widget,
            'widget_template': 'mech_display/i_mech_pose',
            'has_red_point_func': False,
            'widget_cls': SkinDefinePoseWidget,
            'tag_name': 'pose'
            }]
        self.widgets_helper = WidgetCommonComponent(self.panel.nd_content, self.widget_data)
        self.widgets_helper.set_widget_switch_func(self.on_switch_widget)
        self.panel.nd_left_tab.nd_cut.nd_drag.list_tab.SetInitCount(len(self.widget_data))
        self.list_tab = [ self.panel.nd_left_tab.nd_cut.nd_drag.list_tab.GetItem(i) for i in range(len(self.widget_data)) ]
        self.tag_btn_dict = {}
        for idx, tag in enumerate(self.LEFT_TAB):
            tag_name = self.widget_data[idx].get('text')
            tag_btn = self.list_tab[idx]
            self.tag_btn_dict[tag] = tag_btn
            tag_btn.btn.SetText(tag_name)

            @tag_btn.btn.unique_callback()
            def OnClick(_btn, _touch, _idx=idx, *args):
                if global_data.ui_mgr.get_ui('SkinDefineShareUI'):
                    return
                if global_data.ui_mgr.get_ui('FullScreenBackUI'):
                    return
                if not global_data.player.mecha_custom_skin_open():
                    global_data.game_mgr.show_tip(get_text_by_id(81963))
                    return
                if _idx == 1:
                    if not global_data.feature_mgr.is_support_model_decal():
                        global_data.game_mgr.show_tip(get_text_by_id(81937))
                        return
                    if global_data.emgr.get_decal_stage.emit()[0] != 0:
                        global_data.game_mgr.show_tip(get_text_by_id(611611))
                        return
                self.tag_btn_dict[self.LEFT_TAB[_idx]].PlayAnimation('click')
                self.widgets_helper.on_switch_to_widget(_idx)

        self.default_tag_id = default_tag_id

    def init_color_widget(self, nd):
        return SkinDefineColorWidget(self, nd, self.model_id)

    def init_decal_widget(self, nd):
        return SkinDefineDecalWidget(self, nd)

    def init_effect_widget(self, nd):
        return MechaDiyInfoWidget(self, nd, self.mecha_id)

    def init_pose_widget(self, nd):
        return SkinDefinePoseWidget(self, nd, self.mecha_id)

    def on_switch_widget(self, index, widget, is_show):
        self.panel.stopActionByTag(self.DELAY_TAG)
        btn_nd = self.tag_btn_dict[self.LEFT_TAB[index]]
        btn_nd.btn.SetSelect(is_show)
        if is_show:
            btn_nd.PlayAnimation('click')
            widget.panel.PlayAnimation('appear')
        else:
            widget.panel.PlayAnimation('disappear')
        widget.update_widget(is_show)
        self.refresh_red_point()

    def init_ui_events(self):

        @self.panel.btn_manage.btn_common.unique_callback()
        def OnClick(layer, touch, *args):
            if not self._is_plan_show:
                self._update_plan()
                self.panel.PlayAnimation('show_plan')
            else:
                self.panel.PlayAnimation('disappear_plan')
            self._is_plan_show = not self._is_plan_show

        @self.panel.btn_equiped_close.unique_callback()
        def OnClick(layer, touch, *args):
            self._switch_plan_item(-1)
            self.panel.PlayAnimation('disappear_plan')
            if self._is_plan_show:
                self._is_plan_show = False

        self.check_mecha_status()
        self.init_touch_event()

    def is_plan_show(self):
        return self._is_plan_show

    def do_show_panel(self):
        super(SkinDefineUI, self).do_show_panel()
        self.process_events(True)
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self.do_switch_scene()
        self.panel.PlayAnimation('appear')
        self._disappearing = False
        if self.tag_btn_dict:
            for _, btn_nd in six.iteritems(self.tag_btn_dict):
                btn_nd.PlayAnimation('appear')

        cur_widget = self.widgets_helper.get_cur_widget()
        if cur_widget and hasattr(cur_widget, 'do_show_widget'):
            cur_widget.do_show_widget()
        guide_color_ui = global_data.ui_mgr.get_ui('SkinDefineGuideColorUI')
        if guide_color_ui:
            guide_color_ui.panel.setVisible(True)
        guide_decal_ui = global_data.ui_mgr.get_ui('SkinDefineGuideDecalUI')
        if guide_decal_ui:
            guide_decal_ui.panel.setVisible(True)

    def do_hide_panel(self):
        super(SkinDefineUI, self).do_hide_panel()
        self.process_events(False)
        self.show_main_ui()
        cur_widget = self.widgets_helper.get_cur_widget()
        if cur_widget and hasattr(cur_widget, 'do_hide_widget'):
            cur_widget.do_hide_widget()

    def show_top_price_widget(self):
        self.price_top_widget.list_money.setVisible(True)

    def hide_top_price_widget(self):
        self.price_top_widget.list_money.setVisible(False)

    def do_switch_scene(self):
        new_scene_type = SCENE_SKIN_DEFINE
        display_type = SKIN_DEFINE

        def on_load_scene(*args):
            camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
            if not camera_ctrl:
                return
            else:
                y = 11.01
                y_offset = confmgr.get('skin_define_camera').get(str(self.mecha_id), {}).get('iYOffset', None)
                if not y_offset:
                    log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
                else:
                    y = y_offset
                camera_ctrl.decal_camera_ctrl.center_pos = math3d.vector(0, y, 0)
                camera_ctrl.decal_camera_ctrl._is_active = True
                camera = global_data.game_mgr.scene.active_camera
                camera.position = math3d.vector(0, y, 0)
                camera_ctrl.decal_camera_ctrl.default_pos = math3d.vector(0, y, 0)
                return

        global_data.emgr.show_lobby_relatived_scene.emit(new_scene_type, display_type, finish_callback=on_load_scene, belong_ui_name='SkinDefineUI')
        self.init_model(self.model_id)

    def init_model(self, model_id):
        if self.cur_model and self.cur_model.valid:
            return
        else:

            def on_load_model(model):
                global_data.emgr.handle_skin_define_model.emit(get_default_skin_define_anim(model_id), index=0)
                self.cur_model = model
                self.widgets_helper.on_switch_to_widget(self.default_tag_id)
                if self.switch_to_widget_cb and callable(self.switch_to_widget_cb):
                    self.switch_to_widget_cb()

            item_type = item_utils.get_lobby_item_type(model_id)
            b_show_model = item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN)
            if b_show_model and item_type == L_ITEM_TYPE_MECHA_SKIN:
                model_data = get_lobby_model_data(model_id, is_get_player_data=False, consider_second_model=False)
                model_path = get_mecha_model_path(None, model_id)
                submesh_path = get_mecha_model_h_path(None, model_id, False)
                if global_data.decal_lod:
                    idx = submesh_path.find('h.gim')
                    submesh_path = submesh_path[0:idx] + global_data.decal_lod
                for data in model_data:
                    data['mpath'] = model_path
                    data['sub_mesh_path_list'] = [submesh_path]
                    data['skin_id'] = model_id
                    data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(model_id)), [])
                    data['color_dict'] = global_data.player.get_mecha_color().get(str(model_id), {})

                global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)
            return

    def _on_click_back(self, *args):
        result_color = False
        result_decal = False
        if self.color_widget:
            result_color = self.color_widget.check_preview_new_skin()
        if self.decal_widget:
            if self.decal_widget.check_preview_new_decal() >= 1:
                result_decal = True if 1 else False
            twice_confirm = result_color or result_decal
            twice_confirm or self._on_quit()
        else:

            def on_cancel():
                pass

            ui = SecondConfirmDlg2(parent=self.panel)
            ui.confirm(content=get_text_by_id(81902), confirm_callback=self._on_quit, cancel_callback=on_cancel)
            ui.panel.setVisible(True)

    def _on_quit(self):
        if not self.panel:
            return
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def finished(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.SetTimeOut(anim_time, finished)
        self.panel.PlayAnimation('disappear')
        widget = self.widgets_helper.get_cur_widget()
        if widget:
            widget.update_widget(is_show=False)
        global_data.emgr.refresh_avatar_model_custom_skin.emit()
        global_data.player.set_need_update_skin_define(True)

    def _update_plan(self):
        self.panel.temp_list_plan.list_plan.DeleteAllSubItem()
        plan_count = 3
        self.panel.temp_list_plan.list_plan.SetInitCount(plan_count)
        for idx, nd in enumerate(self.panel.temp_list_plan.list_plan.GetAllItem()):
            nd.nd_empty.setVisible(True)

            @nd.btn_plan.unique_callback()
            def OnClick(_layer, _touch, _idx=idx, *args):
                self._on_click_plan_item(_layer, _idx, *args)

    def _on_click_plan_item(self, nd, idx, *args):
        if nd.nd_choose.isVisible():
            return
        if idx == self.selected_plan_idx:
            return
        self._switch_plan_item(idx)

        @nd.nd_choose.btn_save.unique_callback()
        def OnClick(_layer, _touch, _idx=idx, *args):
            self._on_click_save_plan(_layer, _idx)

        @nd.nd_choose.btn_use.unique_callback()
        def OnClick(_layer, _touch, _idx=idx, *args):
            self._on_click_apply_plan(_idx)

    def _switch_plan_item(self, idx):
        if idx != self.selected_plan_idx:
            if self.selected_plan_idx != -1:
                self.panel.temp_list_plan.list_plan.GetItem(self.selected_plan_idx).nd_choose.setVisible(False)
            self.selected_plan_idx = idx
            if idx != -1:
                self.panel.temp_list_plan.list_plan.GetItem(idx).nd_choose.setVisible(True)

    def _on_click_save_plan(self, nd_item, idx):
        pass

    def _on_click_apply_plan(self, idx):
        pass

    def _on_click_rename_plan(self, nd_item):
        global_data.ui_mgr.show_ui('SkinDefinePlanRenameWidget', 'logic.comsys.mecha_display')

    def on_camera_scl(self, dis):
        per = (dis - MIN_RADIUS) * 1.0 / (MAX_RADIUS - MIN_RADIUS)
        self.MAX_SCL = self.NER_MAX_SCL - (self.NER_MAX_SCL - self.FAR_MAX_SCL) * per
        self.MIN_SCL = (self.FAR_MIN_SCL - self.NER_MIN_SCL) * per + self.NER_MIN_SCL
        if self.decal_widget:
            self.decal_widget.on_camera_scl()

    def on_mecha_main_skin_scheme_change(self, mecha_id, fashion_id, scheme):
        if mecha_id != self.mecha_id:
            return
        new_skin_id = scheme.get(FASHION_POS_SUIT, fashion_id)
        if self.color_widget:
            self.color_widget.on_dress_change(new_skin_id)
        self.check_mecha_status()

    def on_buy_goods_success(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return
        self.check_mecha_status()
        self.try_deploy_preview_item()

    def check_mecha_status(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return
        else:
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self.mecha_id)
            item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
            nd_buy_show = False
            temp_btn_use_show = False
            temp_btn_use_enable = False
            temp_btn_use_text = None
            self.panel.lab_get_method.setVisible(False)
            if item_data is not None:
                main_skin_id = get_main_skin_id(self.model_id)
                skin_item_data = global_data.player.get_item_by_no(main_skin_id)
                has_main_skin = skin_item_data is not None
                if has_main_skin and not self.check_preview_new_items():
                    pass
                else:
                    is_skin_can_buy = True
                    skin_id = self.model_id
                    skin_item_data = global_data.player.get_item_by_no(skin_id)
                    has_skin = skin_item_data is not None
                    if not has_skin:
                        goods_id = self.mecha_skin_conf.get(str(skin_id)).get('goods_id')
                        price = mall_utils.get_mall_item_price(goods_id)
                        is_skin_can_buy = bool(price)
                    own_dict, no_own_dict, can_buy_dict, no_can_buy_dict, _, _ = self.get_define_items_buy_info()
                    if has_skin and not (no_own_dict['color'] or no_own_dict['decal']):
                        temp_btn_use_show = True
                        temp_btn_use_enable = True
                        temp_btn_use_text = 860096
                    else:
                        if not is_skin_can_buy or no_can_buy_dict['color'] or no_can_buy_dict['decal']:
                            self.panel.lab_get_method.SetString(860076)
                            self.panel.lab_get_method.setVisible(True)
                            self.panel.lab_get_method.SetColor('#BR')
                        temp_btn_use_show = True
                        temp_btn_use_enable = True
                        temp_btn_use_text = 81928
            else:
                goods_id = self.mecha_info_conf.get(str(self.mecha_id)).get('goods_id')
                if goods_id is not None:
                    temp_btn_use_enable = True
                    temp_btn_use_show = True
                    if item_utils.can_jump_to_ui(goods_id):
                        access_id = item_utils.get_item_access(goods_id)
                        self.lab_get_method.setVisible(True)
                        self.lab_get_method.SetString(access_id)
                        temp_btn_use_text = 2222
                    else:
                        temp_btn_use_show = False
                        nd_buy_show = True
                        temp_btn_use_enable = True
                        temp_btn_use_text = 14004
                        init_price_view(self.panel.nd_buy.temp_price, goods_id)
                else:
                    temp_btn_use_text = 14008
            self.panel.nd_buy.setVisible(nd_buy_show)
            self.panel.temp_btn_use.setVisible(temp_btn_use_show)
            self.panel.temp_btn_use.btn_common.SetEnable(temp_btn_use_enable)
            if temp_btn_use_text:
                text_node = self.panel.temp_btn_use.btn_common if temp_btn_use_show else self.panel.nd_buy.temp_btn_buy.btn_common
                text_node.SetText(get_text_by_id(temp_btn_use_text))
            if nd_buy_show:

                @self.panel.temp_btn_buy.btn_common.unique_callback()
                def OnClick(_btn, _touch, *args):
                    if global_data.ui_mgr.get_ui('SkinDefineShareUI'):
                        return
                    else:
                        if global_data.ui_mgr.get_ui('FullScreenBackUI'):
                            return
                        _goods_id = self.mecha_info_conf.get(str(self.mecha_id)).get('goods_id')
                        if _goods_id is not None:
                            from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
                            role_or_skin_buy_confirmUI(_goods_id)
                        return

            if temp_btn_use_show:

                @self.panel.temp_btn_use.btn_common.unique_callback()
                def OnClick(_btn, _touch, *args):
                    if global_data.ui_mgr.get_ui('SkinDefineShareUI'):
                        return
                    if global_data.ui_mgr.get_ui('FullScreenBackUI'):
                        return
                    self._on_click_btn_use()

            return

    def check_mecha_status_share_simple(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return -1
        else:
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self.mecha_id)
            item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
            if item_data is not None:
                skin_item_data = global_data.player.get_item_by_no(self.model_id)
                has_main_skin = skin_item_data is not None
                if not has_main_skin:
                    global_data.game_mgr.show_tip(get_text_by_id(81974))
                    return -3
                decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(self.model_id)), [])
                color_dict = global_data.player.get_mecha_color().get(str(self.model_id), {})
                if not decal_list and not color_dict:
                    global_data.game_mgr.show_tip(get_text_by_id(81971))
                    return -4
                if self.check_preview_new_items():
                    global_data.game_mgr.show_tip(get_text_by_id(81967))
                    return 2
                return 1
            global_data.game_mgr.show_tip(get_text_by_id(81975))
            return -2
            return

    def check_preview_new_items(self):
        new_color = False
        new_decal = False
        if self.color_widget:
            new_color = self.color_widget.check_preview_new_skin()
        if self.decal_widget:
            new_decal = self.decal_widget.check_preview_new_decal()
        return new_color or new_decal

    def get_define_items_buy_info(self):
        own_dict = {'color': {},'decal': {}}
        no_own_dict = {'color': {},'decal': {}}
        can_buy_dict = {'color': {},'decal': {}}
        no_can_buy_dict = {'color': {},'decal': {}}
        color_idx_dict = {}
        decal_idx_dict = {}
        if self.color_widget:
            new_color_dict, color_idx_dict = self.color_widget.check_preview_new_color_tunnel()
            if new_color_dict:
                for cost_item_id, color_info in six.iteritems(new_color_dict):
                    own_num = global_data.player.get_item_num_by_no(cost_item_id)
                    num = color_info['num']
                    slider_list = color_info['slider_nos']
                    if own_num >= num:
                        own_dict['color'][cost_item_id] = color_info
                    else:
                        own_dict['color'][cost_item_id] = {}
                        own_dict['color'][cost_item_id]['num'] = own_num
                        own_dict['color'][cost_item_id]['slider_nos'] = slider_list[:own_num]
                        no_own_dict['color'][cost_item_id] = {}
                        no_own_dict['color'][cost_item_id]['num'] = num - own_num
                        no_own_dict['color'][cost_item_id]['slider_nos'] = slider_list[own_num:]

        if self.decal_widget:
            new_decal_dict, decal_idx_dict = self.decal_widget.check_preview_new_decal_dict()
            if new_decal_dict:
                for item_id, num in six.iteritems(new_decal_dict):
                    own_num = global_data.player.get_item_num_by_no(item_id)
                    if own_num >= num:
                        own_dict['decal'][item_id] = num
                    else:
                        own_dict['decal'][item_id] = own_num
                        no_own_dict['decal'][item_id] = num - own_num

        for cost_item_id, color_info in six.iteritems(no_own_dict['color']):
            goods_id = cost_item_id
            price = mall_utils.get_mall_item_price(str(goods_id))
            if price:
                can_buy_dict['color'][cost_item_id] = color_info
            else:
                no_can_buy_dict['color'][cost_item_id] = color_info

        for decal_id, num in six.iteritems(no_own_dict['decal']):
            goods_id = decal_id
            price = mall_utils.get_mall_item_price(str(goods_id))
            if price:
                can_buy_dict['decal'][decal_id] = num
            else:
                no_can_buy_dict['decal'][decal_id] = num

        return (
         own_dict, no_own_dict, can_buy_dict, no_can_buy_dict, color_idx_dict, decal_idx_dict)

    def _on_click_btn_use(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return
        else:
            goods_id = self.mecha_info_conf.get(str(self.mecha_id)).get('goods_id')
            item_data = global_data.player.get_item_by_no(int(goods_id))
            if item_data is not None:
                self._on_buy_use_all()
            elif item_utils.can_jump_to_ui(goods_id):
                item_utils.jump_to_ui(goods_id)
            return

    def _on_buy_use_all(self):
        main_skin_id = get_main_skin_id(self.model_id)
        skin_item_data = global_data.player.get_item_by_no(main_skin_id)
        has_main_skin = skin_item_data is not None
        if not has_main_skin:

            def on_confirm():
                if item_utils.can_jump_to_ui(str(main_skin_id)):
                    item_utils.jump_to_ui(str(main_skin_id))
                else:
                    goods_id = self.mecha_skin_conf.get(str(main_skin_id)).get('goods_id')
                    price = mall_utils.get_mall_item_price(goods_id)
                    if price:
                        from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
                        role_or_skin_buy_confirmUI(goods_id)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(81903))

            def on_cancel():
                pass

            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(81904), confirm_callback=on_confirm, cancel_callback=on_cancel)
            return
        else:
            show_buy_item_data_list = []
            skin_id = self.model_id
            skin_item_data = global_data.player.get_item_by_no(skin_id)
            has_skin = skin_item_data is not None
            if not has_skin:
                show_buy_item_data_list.append({'item_no': skin_id,'quantity': 1,'own': 0,'belong': 'skin'})
            own_dict, no_own_dict, can_buy_dict, no_can_buy_dict, color_idx_dict, decal_idx_dict = self.get_define_items_buy_info()
            if own_dict['color']:
                for cost_item_id, color_info in six.iteritems(own_dict['color']):
                    num = color_info['num']
                    slider_list = color_info['slider_nos']
                    for i in range(0, num):
                        slider_no = slider_list[i]
                        tunnel_idx = color_idx_dict[slider_no]
                        show_buy_item_data_list.append({'item_no': cost_item_id,'quantity': 1,'own': 1,'slider_no': slider_no,'belong': 'color','idx': tunnel_idx})

            if no_own_dict['color']:
                for cost_item_id, color_info in six.iteritems(no_own_dict['color']):
                    num = color_info['num']
                    slider_list = color_info['slider_nos']
                    for i in range(0, num):
                        slider_no = slider_list[i]
                        tunnel_idx = color_idx_dict[slider_no]
                        show_buy_item_data_list.append({'item_no': cost_item_id,'quantity': 1,'own': 0,'slider_no': slider_no,'belong': 'color','idx': tunnel_idx})

            if own_dict['decal']:
                for item_no, num in six.iteritems(own_dict['decal']):
                    for i in range(0, num):
                        index = decal_idx_dict[item_no][i]
                        show_buy_item_data_list.append({'item_no': item_no,'quantity': 1,'own': 1,'belong': 'decal','idx': index})

            if no_own_dict['decal']:
                for item_no, num in six.iteritems(no_own_dict['decal']):
                    start_idx = 0
                    own_num = own_dict['decal'].get(item_no, None)
                    if own_num:
                        start_idx = own_num
                    for i in range(0, num):
                        index = decal_idx_dict[item_no][i + start_idx]
                        show_buy_item_data_list.append({'item_no': item_no,'quantity': 1,'own': 0,'belong': 'decal','idx': index})

            if show_buy_item_data_list:
                ui = global_data.ui_mgr.get_ui('SkinDefineBuyUI')
                if ui:
                    ui.close()
                ui = SkinDefineBuyUI()
                if ui:
                    ui.set_item_remove_callback(self.on_remove_item_when_view_buy_list)
                    ui.set_batch_buy_callback(self.on_about_to_buy_callback)
                    ui.init_buy_list_item(show_buy_item_data_list)
                    show_expire_tip = False
                    cur_mecha_item_id = battle_id_to_mecha_lobby_id(self.mecha_id)
                    mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
                    if mecha_item_data.get_expire_time() > 0:
                        show_expire_tip = True
                    if has_skin:
                        if skin_item_data.get_expire_time() > 0:
                            show_expire_tip = True
                    if show_expire_tip:
                        global_data.game_mgr.show_tip(get_text_by_id(81940))
            else:
                self.try_deploy_preview_item()
            return

    def try_deploy_preview_item(self):
        if not global_data.player.get_item_by_no(self.model_id):
            return
        else:
            fashion_id = global_data.player.get_mecha_fashion(battle_id_to_mecha_lobby_id(self.mecha_id))
            if self.model_id != fashion_id:
                global_data.player.install_mecha_main_skin_scheme(self.mecha_id, get_main_skin_id(self.model_id), {FASHION_POS_SUIT: self.model_id})
            if self.effect_widget and self.widgets_helper.get_cur_widget() == self.effect_widget:
                self.effect_widget.mock_click_use_effect()
            return

        effect_widget = self.widgets_helper.get_widget_by_index(self.LEFT_TAB.index('effect'))
        effect_widget and effect_widget.mock_click_use_effect()

    def on_remove_item_when_view_buy_list(self, item_no):
        pass

    def on_about_to_buy_callback(self, batch_buy_item_list, buy_color_list, own_color_list, buy_decal_list, own_decal_list):
        self.batch_buy_item_list = batch_buy_item_list
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self.batch_buy_item_list)
        tunnel_list = []
        if buy_color_list:
            for _, _, tunnel_idx in buy_color_list:
                tunnel_list.append(tunnel_idx)

        if own_color_list:
            for _, _, tunnel_idx in own_color_list:
                tunnel_list.append(tunnel_idx)

        if tunnel_list:
            global_data.emgr.upload_color_data.emit(tunnel_list)
        decal_idx_list = []
        if buy_decal_list:
            for _, _, idx in buy_decal_list:
                decal_idx_list.append(idx)

        if own_decal_list:
            for _, _, idx in own_decal_list:
                decal_idx_list.append(idx)

        if decal_idx_list:
            global_data.emgr.upload_decal_data.emit(decal_idx_list)

    def clear_buy_reward_blocking(self):
        self.batch_buy_item_list = []
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self.batch_buy_item_list)

    def on_batch_buy_update(self):
        self.on_buy_goods_success()
        global_data.game_mgr.show_tip(get_text_by_id(81927))

    def _on_click_details(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        title, rule = (81914, 81915)
        dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

    def _on_click_reset_camera(self, *args):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if not camera_ctrl:
            return
        else:
            camera_ctrl.decal_camera_ctrl.init_paramter()
            y = 10.0
            y_offset = confmgr.get('skin_define_camera').get(str(self.mecha_id), {}).get('iYOffset', None)
            if not y_offset:
                log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
            else:
                y = y_offset
            camera_ctrl.decal_camera_ctrl.center_pos = math3d.vector(0, y, 0)
            camera_ctrl.decal_camera_ctrl._is_active = True
            camera = global_data.game_mgr.scene.active_camera
            camera.position = math3d.vector(0, y, 0)
            camera_ctrl.decal_camera_ctrl.default_pos = math3d.vector(0, y, 0)
            return

    def on_finalize_panel(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.cur_model = None
        global_data.emgr.change_model_display_scene_item.emit(None)
        if global_data.feature_mgr.is_support_model_decal():
            global_data.emgr.exit_decal_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        if self.batch_buy_item_list:
            self.batch_buy_item_list = []
            global_data.emgr.set_reward_show_blocking_item_no_event.emit(self.batch_buy_item_list)
        self._is_plan_show = False
        self.model_id = None
        self.selected_plan_idx = -1
        self.list_tab = []
        self.tag_btn_dict = {}
        self._touch_start_dist = 0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self.process_events(False)
        self.destroy_widget('widgets_helper')
        self.color_widget = None
        self.decal_widget = None
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        global_data.ui_mgr.close_ui('SkinDefineBuyUI')
        global_data.ui_mgr.close_ui('SkinDefineGuideColorUI')
        global_data.ui_mgr.close_ui('SkinDefineGuideDecalUI')
        self.show_main_ui()
        if self._close_cb:
            self._close_cb()
        super(SkinDefineUI, self).on_finalize_panel()
        return

    def refresh_red_point(self, *args):
        for data in self.widget_data:
            if data.get('has_red_point_func', False):
                tag_name = data.get('tag_name')
                widget_cls = data.get('widget_cls')
                red_point = widget_cls.check_red_point()
                tab_btn = self.tag_btn_dict.get(tag_name)
                tab_btn and red_point_utils.show_red_point_template(tab_btn.btn.temp_reddot, red_point)

    @staticmethod
    def check_red_point():
        for widget_cls in SkinDefineUI.TAB_WIDGETS:
            if widget_cls.check_red_point():
                return True

        return False

    def ui_vkb_custom_func(self):
        self._on_click_back()

    def init_touch_event(self):
        touch_layer = self.panel.nd_mech_touch
        touch_layer.EnableDoubleClick(False)
        touch_layer.BindMethod('OnBegin', self._on_nd_touch_begin)
        touch_layer.BindMethod('OnDrag', self._on_nd_touch_drag)
        touch_layer.BindMethod('OnEnd', self._on_nd_touch_end)

    def _on_nd_touch_begin(self, layer, touch):
        if len(self._nd_touch_IDs) >= 2:
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            layer.SetSwallowTouch(True)
            pts = six_ex.values(self._nd_touch_poses)
            self._touch_start_dist = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        else:
            layer.SetSwallowTouch(False)
        return True

    def _on_nd_touch_drag(self, layer, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            return
        if len(self._nd_touch_IDs) == 1:
            pass
        elif len(self._nd_touch_IDs) >= 2:
            self._nd_touch_poses[tid] = touch_wpos
            pts = six_ex.values(self._nd_touch_poses)
            vec = cc.Vec2(pts[0])
            vec.subtract(pts[1])
            cur_dist = vec.getLength()
            ratio = cur_dist - self._touch_start_dist
            global_data.emgr.skin_define_camera_scale.emit(ratio)

    def _on_nd_touch_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]