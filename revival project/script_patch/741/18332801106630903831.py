# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineColorWidget.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.dress_utils import get_mecha_model_path, get_mecha_model_h_path
import game3d
from logic.gutils.rgb_hsb_utils import rgb_from_tuple_2_hex, hsb_int_2_float_d, hsb_2_rgb, rgb_2_hsb, rgba_2_hsba, hsba_2_rgba, hsb_float_2_int_m
import copy
from common.utils.cocos_utils import ccc3FromHex
import cc
import math3d
from logic.comsys.common_ui.FullScreenBackUI import FullScreenBackUI
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
import time
from logic.gutils import template_utils, mall_utils, dress_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import mall_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gutils import skin_define_utils
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.mecha_display.SkinDefineShareUI import SkinDefineShareUI
from logic.gutils import red_point_utils

class SkinDefineColorWidget(BaseUIWidget):
    DELAY_TAG = 20200318
    selected_item_idx = -1
    SLIDER_NDS = (
     'temp_color_1', 'temp_color_2', 'temp_color_3', 'temp_color_4', 'temp_color_5', 'temp_color_6')
    HASH_COLOR = {'HASH_CHANGE_COLOR_1': game3d.calc_string_hash('changecolor1'),
       'HASH_CHANGE_COLOR_2': game3d.calc_string_hash('changecolor2'),
       'HASH_CHANGE_COLOR_3': game3d.calc_string_hash('changecolor3'),
       'HASH_CHANGE_COLOR_4': game3d.calc_string_hash('changecolor4'),
       'HASH_CHANGE_COLOR_5': game3d.calc_string_hash('changecolor5'),
       'HASH_CHANGE_COLOR_6': game3d.calc_string_hash('changecolor6')
       }
    MAX_ANGLE = 23
    MIN_ANGLE = -23
    DEFAULT_DUR = 0.03
    ALPHA_0 = 150
    ALPHA_1 = 255
    PATH_0 = 'gui/ui_res_2/mech_display/line_color_origin_nml.png'
    PATH_1 = 'gui/ui_res_2/mech_display/line_color_origin_active.png'

    def __init__(self, parent, panel, cur_clothing_id):
        self.global_events = {'player_item_update_event': self._on_buy_good_success,
           'refresh_item_red_point': self.update_red_point,
           'upload_color_data': self.on_upload_color_data,
           'set_mecha_color_result_event': self.on_set_color_result,
           'skin_define_get_new_skin': self.on_get_new_skin,
           'role_fashion_chagne': self.on_role_fashion_chagne,
           'skin_define_batch_buy_event': self.on_batch_buy_update
           }
        super(SkinDefineColorWidget, self).__init__(parent, panel)
        self.init_params(cur_clothing_id)
        self.init_conf()
        self.update_cur_conf()
        self.init_ui_events()
        self.parent.color_widget = self
        self.is_guided = global_data.achi_mgr.get_cur_user_archive_data('skin_define_color')

    def init_params(self, cur_clothing_id):
        self.is_show = False
        self.skin_type = None
        self.ori_clothing_id = cur_clothing_id
        self.cur_clothing_id = cur_clothing_id
        self.can_reset_tag = False
        self.ori_color_data = {}
        self.cur_color_data = {}
        self._create_skin_idx = 0
        self._async_action = None
        return

    def init_conf(self):
        self.color_conf = confmgr.get('skin_define_color')

    def update_cur_conf(self):
        self.cur_clothing_conf = self.color_conf.get(str(self.cur_clothing_id), None)
        self.skin_type = self.cur_clothing_conf.get('iSkinType')
        if self.skin_type == skin_define_utils.ADDTIONAL_SKIN:
            self.main_clothing_id = self.cur_clothing_conf.get('iOriginalID')
            self.main_clothing_conf = self.color_conf.get(str(self.main_clothing_id), None)
        else:
            self.main_clothing_id = self.cur_clothing_id
            self.main_clothing_conf = self.cur_clothing_conf
        self.own_list = skin_define_utils.get_group_skin_list(self.main_clothing_id)
        self.open_tunnel = self.cur_clothing_conf.get('cOpenTunnel', [])
        mecha_color_data = global_data.player.get_mecha_color()
        self.ori_color_data = copy.deepcopy(mecha_color_data.get(str(self.cur_clothing_id), {}))
        self.cur_color_data = copy.deepcopy(self.ori_color_data)
        return

    def init_ui_events(self):

        @self.panel.btn_clear.unique_callback()
        def OnClick(btn, touch, *args):
            if not global_data.player.mecha_custom_skin_open():
                global_data.game_mgr.show_tip(get_text_by_id(81963))
                return
            if not global_data.feature_mgr.is_support_model_decal():
                global_data.game_mgr.show_tip(get_text_by_id(81937))
                return
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            if self.skin_type == skin_define_utils.DEFAULT_SKIN:
                return
            if not self.can_reset_tag:
                return
            self._on_click_reset()

        @self.panel.btn_full_screen.unique_callback()
        def OnClick(btn, touch, *args):
            if not global_data.player.mecha_custom_skin_open():
                global_data.game_mgr.show_tip(get_text_by_id(81963))
                return
            if not global_data.feature_mgr.is_support_model_decal():
                global_data.game_mgr.show_tip(get_text_by_id(81937))
                return
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')
            ui = FullScreenBackUI(need_guide_action=True)
            if ui:
                ui.setBackFunctionCallback(self.quit_full_screen)
                ui.set_zoom_btn_visible(False)
                ui.set_action_list_vis(True)
                ui.set_mecha_info(self.parent.mecha_id, self.cur_clothing_id)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch, *args):
            if not global_data.player.mecha_custom_skin_open():
                global_data.game_mgr.show_tip(get_text_by_id(81963))
                return
            if not global_data.feature_mgr.is_support_model_decal():
                global_data.game_mgr.show_tip(get_text_by_id(81937))
                return
            if self.parent.widgets_helper.get_cur_widget() != self:
                return
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')
            ui = SkinDefineShareUI()
            if ui:
                ui.setBackFunctionCallback(self.quit_share)
                mecha_text = confmgr.get('mecha_display', 'HangarConfig', 'Content').get(str(self.parent.mecha_id), {}).get('name_mecha_text_id', '')
                skin_text = item_utils.get_lobby_item_name(self.cur_clothing_id)
                ui.set_mecha_info(self.parent.mecha_id, self.cur_clothing_id, mecha_text, skin_text)

        @self.panel.btn_buy.btn_common.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_dress_skin()

    def on_resolution_changed(self):
        if not global_data.player.mecha_custom_skin_open():
            global_data.game_mgr.show_tip(get_text_by_id(81963))
            return
        if not global_data.feature_mgr.is_support_model_decal():
            global_data.game_mgr.show_tip(get_text_by_id(81937))
            return
        if self.parent.widgets_helper.get_cur_widget() != self:
            return
        if global_data.ui_mgr.get_ui('SkinDefineShareUI') or global_data.ui_mgr.get_ui('FullScreenBackUI'):
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')
            if self.parent.is_plan_show():
                self.parent.btn_equiped_close.OnClick(TouchMock())
            self.parent.PlayAnimation('disappear')

    def quit_full_screen(self):
        if self.parent:
            self.parent.PlayAnimation('appear')
        if self.panel and self.panel.isValid():
            self.panel.PlayAnimation('appear')

    def quit_share(self):
        self.quit_full_screen()

    def show(self):
        pass

    def hide(self):
        pass

    def do_show_widget(self):
        pass

    def update_widget(self, is_show):
        self.is_show = is_show
        if is_show:
            self.check_need_guide()
            self.update_list()
            self.update_own_count()
            self.update_btn_buy()
            self.update_sliders()
            self.update_color_scene()
        else:
            self.selected_item_idx = -1
            self.exit_color_scene()

    def check_need_guide(self):
        if not global_data.player.mecha_custom_skin_open():
            return
        if not self.is_guided:
            if not self.open_tunnel:
                return
            global_data.ui_mgr.show_ui('SkinDefineGuideColorUI', 'logic.comsys.mecha_display')
            self.is_guided = True

    def update_color_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if not camera_ctrl:
            return
        else:
            anim = skin_define_utils.get_default_skin_define_anim(self.cur_clothing_id)
            global_data.emgr.handle_skin_define_model.emit(anim, 0)
            y = 10
            y_offset = confmgr.get('skin_define_camera').get(str(self.parent.mecha_id), {}).get('iYOffset', None)
            if not y_offset:
                log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
            else:
                y = y_offset
            pos = math3d.vector(0, y, 0)
            camera_ctrl.decal_camera_ctrl.center_pos = pos
            camera_ctrl.decal_camera_ctrl.default_pos = pos
            camera_ctrl.decal_camera_ctrl._is_active = True
            return

    def exit_color_scene(self):
        camera_ctrl = global_data.game_mgr.scene.get_com('PartSkinDefineCamera')
        if camera_ctrl:
            camera_ctrl.decal_camera_ctrl._is_active = False

    def on_dress_change(self, new_skin_id):
        self.ori_clothing_id = new_skin_id
        self.update_btn_buy(force_on=True)

    def check_preview_new_skin(self):
        if self.ori_clothing_id != self.cur_clothing_id:
            return True
        if self.cur_color_data != self.ori_color_data:
            return True
        return False

    def check_preview_new_color_tunnel--- This code section failed: ---

 316       0  BUILD_MAP_0           0 
           3  STORE_FAST            1  'new_color_dict'

 317       6  BUILD_MAP_0           0 
           9  STORE_FAST            2  'new_color_idx_dict'

 318      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             0  'open_tunnel'
          18  POP_JUMP_IF_TRUE     31  'to 31'

 319      21  LOAD_GLOBAL           1  'False'
          24  LOAD_CONST            0  ''
          27  BUILD_TUPLE_2         2 
          30  RETURN_END_IF    
        31_0  COME_FROM                '18'

 320      31  SETUP_LOOP          353  'to 387'
          34  LOAD_GLOBAL           3  'enumerate'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             0  'open_tunnel'
          43  CALL_FUNCTION_1       1 
          46  GET_ITER         
          47  FOR_ITER            336  'to 386'
          50  UNPACK_SEQUENCE_2     2 
          53  STORE_FAST            3  'idx'
          56  STORE_FAST            4  'tunnel_idx'

 321      59  LOAD_FAST             0  'self'
          62  LOAD_ATTR             4  'cur_color_data'
          65  LOAD_ATTR             5  'get'
          68  LOAD_FAST             4  'tunnel_idx'
          71  LOAD_CONST            0  ''
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            5  'cur_val'

 322      80  LOAD_FAST             0  'self'
          83  LOAD_ATTR             6  'ori_color_data'
          86  LOAD_ATTR             5  'get'
          89  LOAD_FAST             4  'tunnel_idx'
          92  LOAD_CONST            0  ''
          95  CALL_FUNCTION_2       2 
          98  STORE_FAST            6  'ori_val'

 323     101  LOAD_FAST             6  'ori_val'
         104  LOAD_CONST            0  ''
         107  COMPARE_OP            9  'is-not'
         110  POP_JUMP_IF_FALSE   257  'to 257'

 324     113  LOAD_FAST             5  'cur_val'
         116  LOAD_CONST            0  ''
         119  COMPARE_OP            9  'is-not'
         122  POP_JUMP_IF_FALSE   383  'to 383'

 325     125  LOAD_FAST             5  'cur_val'
         128  LOAD_FAST             6  'ori_val'
         131  COMPARE_OP            3  '!='
         134  POP_JUMP_IF_FALSE   254  'to 254'

 326     137  LOAD_FAST             0  'self'
         140  LOAD_ATTR             7  'cur_clothing_conf'
         143  LOAD_ATTR             5  'get'
         146  LOAD_CONST            1  'iCostItemID'
         149  CALL_FUNCTION_1       1 
         152  STORE_FAST            7  'cost_item_id'

 327     155  LOAD_FAST             7  'cost_item_id'
         158  LOAD_FAST             1  'new_color_dict'
         161  COMPARE_OP            7  'not-in'
         164  POP_JUMP_IF_FALSE   197  'to 197'

 328     167  BUILD_MAP_2           2 
         170  LOAD_CONST            2  1
         173  LOAD_CONST            3  'num'
         176  STORE_MAP        
         177  LOAD_FAST             3  'idx'
         180  BUILD_LIST_1          1 
         183  LOAD_CONST            4  'slider_nos'
         186  STORE_MAP        
         187  LOAD_FAST             1  'new_color_dict'
         190  LOAD_FAST             7  'cost_item_id'
         193  STORE_SUBSCR     
         194  JUMP_FORWARD         41  'to 238'

 330     197  LOAD_FAST             1  'new_color_dict'
         200  LOAD_FAST             7  'cost_item_id'
         203  BINARY_SUBSCR    
         204  LOAD_CONST            3  'num'
         207  DUP_TOPX_2            2 
         210  BINARY_SUBSCR    
         211  LOAD_CONST            2  1
         214  INPLACE_ADD      
         215  ROT_THREE        
         216  STORE_SUBSCR     

 331     217  LOAD_FAST             1  'new_color_dict'
         220  LOAD_FAST             7  'cost_item_id'
         223  BINARY_SUBSCR    
         224  LOAD_CONST            4  'slider_nos'
         227  BINARY_SUBSCR    
         228  LOAD_ATTR             8  'append'
         231  LOAD_FAST             3  'idx'
         234  CALL_FUNCTION_1       1 
         237  POP_TOP          
       238_0  COME_FROM                '194'

 332     238  LOAD_FAST             4  'tunnel_idx'
         241  LOAD_FAST             2  'new_color_idx_dict'
         244  LOAD_FAST             3  'idx'
         247  STORE_SUBSCR     
         248  JUMP_ABSOLUTE       254  'to 254'

 334     251  JUMP_ABSOLUTE       383  'to 383'

 336     254  CONTINUE             47  'to 47'

 338     257  LOAD_FAST             5  'cur_val'
         260  LOAD_CONST            0  ''
         263  COMPARE_OP            9  'is-not'
         266  POP_JUMP_IF_FALSE    47  'to 47'

 339     269  LOAD_FAST             0  'self'
         272  LOAD_ATTR             7  'cur_clothing_conf'
         275  LOAD_ATTR             5  'get'
         278  LOAD_CONST            1  'iCostItemID'
         281  CALL_FUNCTION_1       1 
         284  STORE_FAST            7  'cost_item_id'

 340     287  LOAD_FAST             7  'cost_item_id'
         290  LOAD_FAST             1  'new_color_dict'
         293  COMPARE_OP            7  'not-in'
         296  POP_JUMP_IF_FALSE   329  'to 329'

 341     299  BUILD_MAP_2           2 
         302  LOAD_CONST            2  1
         305  LOAD_CONST            3  'num'
         308  STORE_MAP        
         309  LOAD_FAST             3  'idx'
         312  BUILD_LIST_1          1 
         315  LOAD_CONST            4  'slider_nos'
         318  STORE_MAP        
         319  LOAD_FAST             1  'new_color_dict'
         322  LOAD_FAST             7  'cost_item_id'
         325  STORE_SUBSCR     
         326  JUMP_FORWARD         41  'to 370'

 343     329  LOAD_FAST             1  'new_color_dict'
         332  LOAD_FAST             7  'cost_item_id'
         335  BINARY_SUBSCR    
         336  LOAD_CONST            3  'num'
         339  DUP_TOPX_2            2 
         342  BINARY_SUBSCR    
         343  LOAD_CONST            2  1
         346  INPLACE_ADD      
         347  ROT_THREE        
         348  STORE_SUBSCR     

 344     349  LOAD_FAST             1  'new_color_dict'
         352  LOAD_FAST             7  'cost_item_id'
         355  BINARY_SUBSCR    
         356  LOAD_CONST            4  'slider_nos'
         359  BINARY_SUBSCR    
         360  LOAD_ATTR             8  'append'
         363  LOAD_FAST             3  'idx'
         366  CALL_FUNCTION_1       1 
         369  POP_TOP          
       370_0  COME_FROM                '326'

 345     370  LOAD_FAST             4  'tunnel_idx'
         373  LOAD_FAST             2  'new_color_idx_dict'
         376  LOAD_FAST             3  'idx'
         379  STORE_SUBSCR     
         380  JUMP_BACK            47  'to 47'

 347     383  JUMP_BACK            47  'to 47'
         386  POP_BLOCK        
       387_0  COME_FROM                '31'

 348     387  LOAD_FAST             1  'new_color_dict'
         390  LOAD_FAST             2  'new_color_idx_dict'
         393  BUILD_TUPLE_2         2 
         396  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 386

    def update_list(self):
        self._skin_id_to_ui_item = {}
        self.panel.list_skin.RecycleAllItem()
        self._create_skin_idx = 0
        self.clear_async_action()
        self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.create_skin_item)])))

    def clear_async_action(self):
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_skin_item(self):
        start_time = time.time()
        while self._create_skin_idx < len(self.own_list):
            skin_item = self.panel.list_skin.ReuseItem(bRefresh=True)
            if not skin_item:
                skin_item = self.panel.list_skin.AddTemplateItem(bRefresh=True)
            skin_item.nd_choose.setVisible(False)
            item_no = self.own_list[self._create_skin_idx]
            item_config = confmgr.get('lobby_item', str(item_no))
            self._skin_id_to_ui_item[item_no] = skin_item
            self.init_skin_item(skin_item, item_no, self._create_skin_idx)
            self._create_skin_idx += 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        if self.selected_item_idx != -1:
            self.panel.list_skin.GetItem(self.selected_item_idx).nd_choose.setVisible(True)
        else:
            self.selected_item_idx = self.own_list.index(self.cur_clothing_id)
            self.panel.list_skin.GetItem(self.selected_item_idx).nd_choose.setVisible(True)

    def init_skin_item(self, skin_item, item_no, index):
        item_utils.update_limit_btn(item_no, skin_item.temp_limit, skin_item.temp_limit_common)
        name_text = item_utils.get_lobby_item_name(item_no)
        skin_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(skin_item, item_no)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(item_no))
        if skin_cfg:
            item_utils.check_skin_tag(skin_item.nd_kind, item_no)
            skin_half_img_path = skin_cfg.get('half_img_path', None)
            if skin_half_img_path:
                skin_item.img_skin.SetDisplayFrameByPath('', skin_half_img_path)
        template_utils.show_remain_time(skin_item.nd_time, skin_item.nd_time.lab_time, item_no)
        own = global_data.player.has_item_by_no(item_no) if global_data.player else False
        skin_item.nd_lock.setVisible(not own)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
        red_point_utils.show_red_point_template(skin_item.nd_new, show_new)

        @skin_item.btn.unique_callback()
        def OnClick(_layer, _touch, _idx=index, _clothing_id=item_no, *args):
            self._on_click_list_item(_idx, _clothing_id, *args)

        return

    def _on_click_list_item(self, idx, clothing_id, *args):
        self.req_del_red_point(clothing_id)
        if clothing_id == self.cur_clothing_id:
            return
        self.can_reset_tag = False
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.update_model(clothing_id)
        self._switch_list_item(idx)
        self.cur_clothing_id = clothing_id
        self.parent.model_id = clothing_id
        self.update_cur_conf()
        self.update_btn_buy()
        self.parent.check_mecha_status()
        self.check_need_guide()
        self.panel.nd_more_color.setVisible(False)
        self.panel.StopAnimation('loop')
        self.panel.DelayCallWithTag(0.5, self.update_sliders, self.DELAY_TAG)

    def _switch_list_item(self, idx):
        if idx != self.selected_item_idx:
            if self.selected_item_idx != -1:
                self.panel.list_skin.GetItem(self.selected_item_idx).nd_choose.setVisible(False)
            self.selected_item_idx = idx
            if idx != -1:
                self.panel.list_skin.GetItem(idx).nd_choose.setVisible(True)

    def update_model(self, clothing_id):

        def on_load_model(model):
            anim = skin_define_utils.get_default_skin_define_anim(clothing_id)
            global_data.emgr.handle_skin_define_model.emit(anim, 0)
            decal_widget = self.parent.decal_widget
            if decal_widget:
                decal_widget.first_enter_tag = True
            self.parent.cur_model = model

        model_data = get_lobby_model_data(clothing_id, is_get_player_data=False)
        model_path = get_mecha_model_path(None, clothing_id)
        submesh_path = get_mecha_model_h_path(None, clothing_id, False)
        for data in model_data:
            data['mpath'] = model_path
            data['sub_mesh_path_list'] = [submesh_path]
            data['decal_list'] = global_data.player.get_mecha_decal().get(str(skin_define_utils.get_main_skin_id(clothing_id)), [])
            data['color_dict'] = global_data.player.get_mecha_color().get(str(clothing_id), {})

        global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_load_model)
        return

    def update_own_count(self):
        has_func = global_data.player.has_item_by_no if global_data.player else (lambda : 0)
        own_count = 0
        for item_no in self.own_list:
            own = has_func(item_no)
            if own:
                own_count += 1

        self.panel.lab_number.setString('%d / %d' % (own_count, len(self.own_list)))

    def update_btn_buy(self, force_on=False):
        btn = self.panel.btn_buy
        clothing_data = global_data.player.get_item_by_no(self.cur_clothing_id)
        self.panel.temp_price.setVisible(False)
        self.panel.lab_get_method.setVisible(False)
        if force_on:
            self.panel.lab_get_method.setVisible(False)
            btn.btn_common.SetText(get_text_by_id(14007))
            btn.btn_common.SetEnable(False)
            return
        else:
            if clothing_data is None and self.skin_type != skin_define_utils.DEFAULT_SKIN:
                btn.btn_common.SetText(get_text_by_id(14005))
                btn.btn_common.SetEnable(True)
                goods_id = self.parent.mecha_skin_conf.get(str(self.cur_clothing_id)).get('goods_id')
                if item_utils.can_jump_to_ui(str(self.cur_clothing_id)):
                    jump_txt = item_utils.get_item_access(str(self.cur_clothing_id))
                    self.panel.lab_get_method.SetString(jump_txt)
                    self.panel.lab_get_method.setVisible(True)
                    btn.btn_common.SetText(get_text_by_id(2222))
                else:
                    price = mall_utils.get_mall_item_price(goods_id)
                    if price:
                        template_utils.init_price_view(self.panel.temp_price, goods_id, mall_const.DEF_PRICE_COLOR)
                        self.panel.temp_price.setVisible(True)
                    else:
                        btn.btn_common.SetText(get_text_by_id(80828))
                        btn.btn_common.SetEnable(False)
                        access_txt = item_utils.get_item_access(str(self.cur_clothing_id))
                        if access_txt:
                            self.panel.lab_get_method.SetString(access_txt)
                            self.panel.lab_get_method.setVisible(True)
            else:
                self.panel.lab_get_method.setVisible(False)
                cur_mecha_item_id = dress_utils.battle_id_to_mecha_lobby_id(self.parent.mecha_id)
                mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
                if mecha_item_data is not None:
                    fashion_data = mecha_item_data.get_fashion()
                    dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
                    if dressed_clothing_id == self.cur_clothing_id:
                        btn.btn_common.SetText(get_text_by_id(14007))
                        btn.btn_common.SetEnable(False)
                    else:
                        btn.btn_common.SetText(get_text_by_id(14006))
                        btn.btn_common.SetEnable(True)
                else:
                    btn.btn_common.SetText(get_text_by_id(81030))
                    btn.btn_common.SetEnable(False)
            return

    def _on_click_dress_skin(self, *args):
        skin_data = global_data.player.get_item_by_no(self.cur_clothing_id)
        if skin_data is None:
            goods_id = self.parent.mecha_skin_conf.get(str(self.cur_clothing_id)).get('goods_id')
            if item_utils.can_jump_to_ui(str(self.cur_clothing_id)):
                item_utils.jump_to_ui(str(self.cur_clothing_id))
                self.panel.stopActionByTag(self.DELAY_TAG)
            else:
                role_or_skin_buy_confirmUI(goods_id)
        else:
            global_data.player.install_mecha_main_skin_scheme(self.parent.mecha_id, self.main_clothing_id, {FASHION_POS_SUIT: self.cur_clothing_id})
        return

    def update_sliders(self):
        if not self.is_show:
            return
        else:
            self._init_sliders()
            part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
            if not part_md:
                return
            model_list = part_md.get_cur_model_list()
            if not model_list:
                return
            model = model_list[0].get_model()
            if not model:
                return
            if skin_define_utils.has_spec_mat_idx(self.parent.mecha_id):
                if skin_define_utils.is_spec_mat_idx(self.parent.mecha_id, self.cur_clothing_id):
                    model_sub_material = model.get_sub_material(2)
                else:
                    model_sub_material = model.get_sub_material(1)
            else:
                model_sub_material = model.get_sub_material(1)
            if not model_sub_material:
                return
            self.panel.PlayAnimation('nd_more_appear')
            self.panel.PlayAnimation('loop')
            self._update_color_value()
            if self.skin_type == skin_define_utils.DEFAULT_SKIN:
                return
            slider_count = len(self.open_tunnel)
            for idx, ui_item in enumerate(self.slider_items):
                if idx >= slider_count:
                    break
                ui_item.color_name.SetString(get_text_by_id(81906) + str(idx + 1))
                tunnel_idx = self.open_tunnel[idx]
                hsb_val = self.ori_color_data.get(tunnel_idx, None)
                if hsb_val is None:
                    self.list_rgba[idx] = model_sub_material.get_var(self.HASH_COLOR['HASH_CHANGE_COLOR_%d' % tunnel_idx], 'changecolor%d' % tunnel_idx)
                else:
                    hsb_tunnel = self.range_hsb[idx][0]
                    hsb_values = copy.deepcopy(self.default_hsb[idx])
                    hsb_values[hsb_tunnel] = hsb_val
                    hsb_values = hsb_int_2_float_d(hsb_values)
                    rgb = hsb_2_rgb(hsb_values)
                    rgb.append(1.0)
                    self.list_rgba[idx] = rgb
                cur_color = rgb_from_tuple_2_hex(self.list_rgba[idx])
                ui_item.img_color_1.SetColor(cur_color)
                ui_item.img_color_2.SetColor(cur_color)
                self.calc_range(idx)
                start_rgb = rgb_from_tuple_2_hex(hsb_2_rgb(self.start_hsb[idx]))
                end_rgb = rgb_from_tuple_2_hex(hsb_2_rgb(self.end_hsb[idx]))
                ui_item.img_color_progress.setStartColor(ccc3FromHex(start_rgb))
                ui_item.img_color_progress.setEndColor(ccc3FromHex(end_rgb))
                if idx < 3:
                    ui_item.img_color_progress.setVector(cc.Vec2(0, 1))
                else:
                    ui_item.img_color_progress.setVector(cc.Vec2(1, 0))
                if not global_data.player.mecha_custom_skin_open():

                    @ui_item.btn_color.unique_callback()
                    def OnBegin(_btn, _touch, _idx=idx, *args):
                        global_data.game_mgr.show_tip(get_text_by_id(81963))

                    continue
                if not global_data.feature_mgr.is_support_model_decal():

                    @ui_item.btn_color.unique_callback()
                    def OnBegin(_btn, _touch, _idx=idx, *args):
                        global_data.game_mgr.show_tip(get_text_by_id(81937))

                    continue

                @ui_item.btn_color.unique_callback()
                def OnBegin(_btn, _touch, _idx=idx, *args):
                    log_skin_id = self.cur_clothing_id
                    log_open_tunnel = self.open_tunnel
                    log_slider_idx = _idx
                    log_tunnel_idx = self.open_tunnel[_idx]
                    _nd = self.slider_items[_idx]
                    _nd.StopAnimation('disappear_progress')
                    _nd.PlayAnimation('show_progress')
                    _nd.PlayAnimation('loop')
                    self.list_hsba[_idx] = rgba_2_hsba(self.list_rgba[_idx])
                    self.calc_slider_value(_idx)
                    _angle = self.MIN_ANGLE + self.slider_values[_idx] * (self.MAX_ANGLE - self.MIN_ANGLE)
                    _nd.nd_color_btn.setRotation(_angle)
                    default_hsb = self.default_hsb[_idx]
                    hsb_tunnel = self.range_hsb[_idx][0]
                    start_val = self.range_hsb[_idx][1][0]
                    end_val = self.range_hsb[_idx][1][1]
                    default_val = default_hsb[hsb_tunnel]
                    default_slider_value = (default_val - start_val) * 1.0 / (end_val - start_val)
                    default_angle = self.MIN_ANGLE + default_slider_value * (self.MAX_ANGLE - self.MIN_ANGLE)
                    _nd.nd_origin.setRotation(default_angle)
                    _nd.nd_origin.nd_rotate_origin.setRotation(-default_angle)
                    self.default_slider_values[_idx] = default_slider_value
                    if abs(self.slider_values[_idx] - default_slider_value) < self.DEFAULT_DUR:
                        _nd.bar_origin.setOpacity(self.ALPHA_1)
                        _nd.lab_origin.setOpacity(self.ALPHA_1)
                        _nd.icon_origin.setOpacity(self.ALPHA_1)
                        _nd.bar_origin.SetDisplayFrameByPath('', self.PATH_1)
                    else:
                        _nd.bar_origin.setOpacity(self.ALPHA_0)
                        _nd.lab_origin.setOpacity(self.ALPHA_0)
                        _nd.icon_origin.setOpacity(self.ALPHA_0)
                        _nd.bar_origin.SetDisplayFrameByPath('', self.PATH_0)

                @ui_item.btn_color.unique_callback()
                def OnDrag(_btn, _touch, _idx=idx, *args):
                    log_skin_id = self.cur_clothing_id
                    log_open_tunnel = self.open_tunnel
                    log_slider_idx = _idx
                    try:
                        log_tunnel_idx = self.open_tunnel[_idx]
                        log_hsb_tunnel = self.range_hsb[_idx]
                    except Exception as e:
                        print(e)
                        return

                    _nd = self.slider_items[_idx]
                    delta = _touch.getDelta()
                    ratio = delta.y / 237.0
                    self.slider_values[_idx] += ratio
                    if self.slider_values[_idx] > 1.0:
                        self.slider_values[_idx] = 1.0
                    elif self.slider_values[_idx] < 0.0001:
                        self.slider_values[_idx] = 0.0001
                    _angle = self.MIN_ANGLE + self.slider_values[_idx] * (self.MAX_ANGLE - self.MIN_ANGLE)
                    _nd.nd_color_btn.setRotation(_angle)
                    self.calc_hsb_from_slider(_idx)
                    self.list_rgba[_idx] = hsba_2_rgba(self.list_hsba[_idx])
                    _tunnel_idx = self.open_tunnel[_idx]
                    _hash = self.HASH_COLOR['HASH_CHANGE_COLOR_%d' % _tunnel_idx]
                    _attr = 'changecolor%d' % _tunnel_idx
                    _val = tuple(self.list_rgba[_idx])
                    if model and model.valid:
                        model.all_materials.set_var(_hash, _attr, _val)
                    _cur_color = rgb_from_tuple_2_hex(self.list_rgba[_idx])
                    _cur_color and _nd.img_color_1.SetColor(_cur_color)
                    _cur_color and _nd.img_color_2.SetColor(_cur_color)
                    _hsb_info = self.range_hsb[_idx]
                    if _hsb_info is None:
                        import traceback
                        stack = traceback.extract_stack()
                        import exception_hook
                        err_msg = 'Error skindefineColor Drag !\n' + str(stack) + '\n' + 'skin_id: ' + str(self.parent.model_id) + '\n' + 'mecha_id: ' + str(self.parent.mecha_id) + '\n' + 'idx: ' + str(_idx) + '\n' + 'range_hsb' + str(self.range_hsb)
                        exception_hook.post_error(err_msg)
                        return
                    else:
                        try:
                            _hsb_tunnel = self.range_hsb[_idx][0]
                            _cur_hsb_tunnel_val = hsb_float_2_int_m(self.list_hsba[_idx][_hsb_tunnel], _hsb_tunnel)
                        except Exception as e:
                            print(e)
                            return

                        _hsb_min_val = self.range_hsb[_idx][1][0]
                        _hsb_max_val = self.range_hsb[_idx][1][1]
                        if _hsb_min_val > _hsb_max_val:
                            _hsb_min_val, _hsb_max_val = _hsb_max_val, _hsb_min_val
                        if _cur_hsb_tunnel_val > _hsb_max_val:
                            _cur_hsb_tunnel_val = _hsb_max_val
                        elif _cur_hsb_tunnel_val < _hsb_min_val:
                            _cur_hsb_tunnel_val = _hsb_min_val
                        self.cur_color_data[_tunnel_idx] = _cur_hsb_tunnel_val
                        if abs(self.slider_values[_idx] - self.default_slider_values[_idx]) < self.DEFAULT_DUR:
                            _nd.bar_origin.setOpacity(self.ALPHA_1)
                            _nd.lab_origin.setOpacity(self.ALPHA_1)
                            _nd.icon_origin.setOpacity(self.ALPHA_1)
                            _nd.bar_origin.SetDisplayFrameByPath('', self.PATH_1)
                        else:
                            _nd.bar_origin.setOpacity(self.ALPHA_0)
                            _nd.lab_origin.setOpacity(self.ALPHA_0)
                            _nd.icon_origin.setOpacity(self.ALPHA_0)
                            _nd.bar_origin.SetDisplayFrameByPath('', self.PATH_0)
                        self.can_reset_tag = False
                        return

                @ui_item.btn_color.unique_callback()
                def OnEnd(_btn, _touch, _idx=idx, *args):
                    _nd = self.slider_items[_idx]
                    _nd.StopAnimation('show_progress')
                    _nd.PlayAnimation('disappear_progress')
                    if abs(self.slider_values[_idx] - self.default_slider_values[_idx]) < self.DEFAULT_DUR:
                        log_skin_id = self.cur_clothing_id
                        log_open_tunnel = self.open_tunnel
                        log_slider_idx = _idx
                        try:
                            log_tunnel_idx = self.open_tunnel[_idx]
                            log_default_hsb = self.default_hsb[_idx]
                        except Exception as e:
                            print(e)
                            return

                        self.slider_values[_idx] = self.default_slider_values[_idx]
                        _tunnel_idx = self.open_tunnel[_idx]
                        default_hsb = self.default_hsb[_idx]
                        hsb_tunnel = self.range_hsb[_idx][0]
                        default_val = default_hsb[hsb_tunnel]
                        self.cur_color_data[_tunnel_idx] = default_val
                    self.parent.check_mecha_status()
                    self.can_reset_tag = True

            self.can_reset_tag = True
            return

    def _init_sliders(self):
        self.slider_items = []
        for slider_nd in self.SLIDER_NDS:
            nd = getattr(self.panel.nd_more_color, slider_nd)
            nd.setVisible(False)
            self.slider_items.append(nd)

    def _update_color_value(self):
        self.open_tunnel = self.cur_clothing_conf.get('cOpenTunnel', [])
        for idx in range(len(self.open_tunnel)):
            self.slider_items[idx].setVisible(True)

        self.slider_values = [ 0.5 for _ in range(0, 6) ]
        self.list_rgba = [ [] for _ in range(0, 6) ]
        self.list_hsba = [ [] for _ in range(0, 6) ]
        self.default_slider_values = [ 0.5 for _ in range(0, 6) ]
        self.default_hsb = self.cur_clothing_conf.get('cDefaultHSB')
        self.range_hsb = self.cur_clothing_conf.get('cRangeHSB')
        self.start_hsb = [ [] for _ in range(0, 6) ]
        self.end_hsb = [ [] for _ in range(0, 6) ]

    def calc_range(self, index):
        hsb_tunnel = self.range_hsb[index][0]
        range_start = self.range_hsb[index][1][0]
        range_end = self.range_hsb[index][1][1]
        start_hsb = copy.deepcopy(self.default_hsb[index])
        start_hsb[hsb_tunnel] = range_start
        end_hsb = copy.deepcopy(self.default_hsb[index])
        end_hsb[hsb_tunnel] = range_end
        self.start_hsb[index] = hsb_int_2_float_d(start_hsb)
        self.end_hsb[index] = hsb_int_2_float_d(end_hsb)

    def calc_slider_value(self, idx):
        hsb_tunnel = self.range_hsb[idx][0]
        cur_value = self.list_hsba[idx][hsb_tunnel]
        start_value = self.start_hsb[idx][hsb_tunnel]
        end_value = self.end_hsb[idx][hsb_tunnel]
        self.slider_values[idx] = (cur_value - start_value) / (end_value - start_value)

    def calc_hsb_from_slider(self, idx):
        try:
            hsb_tunnel = self.range_hsb[idx][0]
        except IndexError:
            import traceback
            stack = traceback.extract_stack()
            import exception_hook
            err_msg = 'Error calc_hsb_from_slider !\n' + str(stack) + '\n' + 'skin_id: ' + str(self.parent.model_id) + '\n' + 'mecha_id: ' + str(self.parent.mecha_id) + '\n' + 'idx: ' + str(idx) + '\n' + 'range_hsb' + str(self.range_hsb)
            exception_hook.post_error(err_msg)
            return

        start_value = self.start_hsb[idx][hsb_tunnel]
        end_value = self.end_hsb[idx][hsb_tunnel]
        ratio = self.slider_values[idx]
        value = start_value + ratio * (end_value - start_value)
        try:
            self.list_hsba[idx][hsb_tunnel] = value
        except IndexError:
            import exception_hook
            msg = 'SkinDefineColorWidget  <<calc_hsb_from_slider>> skin_id:%s , slider_idx:%s, hsb_tunnel:%s, range_hsb:%s, list_hsba:%s' % (str(self.parent.model_id), str(idx), str(hsb_tunnel), str(self.range_hsb), str(self.list_hsba))
            exception_hook.post_stack(msg)

    def _on_click_reset(self):
        if self.cur_color_data == self.ori_color_data:
            return

        def on_cancel():
            pass

        SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(81933), confirm_callback=self._do_reset, cancel_callback=on_cancel)

    def _do_reset(self):
        part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
        if not part_md:
            return
        else:
            model_list = part_md.get_cur_model_list()
            if not model_list:
                return
            model = model_list[0].get_model()
            if not model:
                return
            slider_count = len(self.open_tunnel)
            for idx, ui_item in enumerate(self.slider_items):
                if idx >= slider_count:
                    break
                self.cur_color_data = copy.deepcopy(self.ori_color_data)
                tunnel_idx = self.open_tunnel[idx]
                hsb_val = self.ori_color_data.get(tunnel_idx, None)
                if hsb_val is None:
                    hsb = hsb_int_2_float_d(self.default_hsb[idx])
                    hsb.append(1.0)
                    self.list_hsba[idx] = hsb
                    self.list_rgba[idx] = hsba_2_rgba(self.list_hsba[idx])
                    cur_color = rgb_from_tuple_2_hex(self.list_rgba[idx])
                    ui_item.img_color_1.SetColor(cur_color)
                    ui_item.img_color_2.SetColor(cur_color)
                    self.calc_slider_value(idx)
                    angle = self.MIN_ANGLE + self.slider_values[idx] * (self.MAX_ANGLE - self.MIN_ANGLE)
                    ui_item.nd_color_btn.setRotation(angle)
                else:
                    hsb_tunnel = self.range_hsb[idx][0]
                    hsb_values = copy.deepcopy(self.default_hsb[idx])
                    hsb_values[hsb_tunnel] = hsb_val
                    hsb_values = hsb_int_2_float_d(hsb_values)
                    rgb = hsb_2_rgb(hsb_values)
                    rgb.append(1.0)
                    self.list_rgba[idx] = rgb
                cur_color = rgb_from_tuple_2_hex(self.list_rgba[idx])
                ui_item.img_color_1.SetColor(cur_color)
                ui_item.img_color_2.SetColor(cur_color)
                self.calc_range(idx)
                start_rgb = rgb_from_tuple_2_hex(hsb_2_rgb(self.start_hsb[idx]))
                end_rgb = rgb_from_tuple_2_hex(hsb_2_rgb(self.end_hsb[idx]))
                ui_item.img_color_progress.setStartColor(ccc3FromHex(start_rgb))
                ui_item.img_color_progress.setEndColor(ccc3FromHex(end_rgb))
                if idx < 3:
                    ui_item.img_color_progress.setVector(cc.Vec2(0, 1))
                else:
                    ui_item.img_color_progress.setVector(cc.Vec2(1, 0))
                _tunnel_idx = self.open_tunnel[idx]
                _hash = self.HASH_COLOR['HASH_CHANGE_COLOR_%d' % _tunnel_idx]
                _attr = 'changecolor%d' % _tunnel_idx
                _val = tuple(self.list_rgba[idx])
                model.all_materials.set_var(_hash, _attr, _val)
                self.parent.check_mecha_status()

            return

    def _on_buy_good_success(self):
        lock_color = global_data.player.get_lock_color()
        lock_decal = global_data.player.get_lock_decal()
        if lock_color or lock_decal:
            return
        self.update_list()
        self.update_own_count()
        self.update_btn_buy()

    def update_red_point(self):
        for idx, ui_item in enumerate(self.panel.list_skin.GetAllItem()):
            clothind_id = self.own_list[idx]
            show_new = global_data.lobby_red_point_data.get_rp_by_no(clothind_id)
            red_point_utils.show_red_point_template(ui_item.nd_new, show_new)

    def req_del_red_point(self, clothing_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
        if show_new:
            global_data.player.req_del_item_redpoint(clothing_id)

    def on_upload_color_data(self, tunnel_list):
        if len(self.open_tunnel) <= 0:
            return
        if not tunnel_list:
            return
        upload_color_data = {}
        for tunnel_idx in tunnel_list:
            cur_val = self.cur_color_data[tunnel_idx]
            upload_color_data[tunnel_idx] = cur_val

        global_data.player.set_mecha_color(self.cur_clothing_id, upload_color_data)

    def on_set_color_result(self):
        mecha_color_data = global_data.player.get_mecha_color()
        self.ori_color_data = copy.deepcopy(mecha_color_data.get(str(self.cur_clothing_id), {}))
        self.parent.check_mecha_status()
        global_data.emgr.player_money_info_update_event.emit()

    def on_get_new_skin(self):
        pass

    def on_role_fashion_chagne(self, *args):
        self.update_btn_buy()

    def on_batch_buy_update(self):
        self._on_buy_good_success()

    def destroy(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.skin_type = None
        self.cur_clothing_id = None
        self.can_reset_tag = False
        self.ori_color_data = {}
        self.cur_color_data = {}
        self._create_skin_idx = 0
        self._async_action = None
        super(SkinDefineColorWidget, self).destroy()
        return

    @staticmethod
    def check_red_point():
        return False