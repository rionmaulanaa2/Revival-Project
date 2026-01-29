# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/BigMapUINew.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER, UI_VKB_CUSTOM, UI_TYPE_NORMAL, UI_TYPE_TRANS
from logic.comsys.map.MapBaseUINew import MapBaseUI
from logic.gutils.ui_salog_utils import add_uiclick_add_up_salog
from logic.comsys.chat.JudgeDanmuWidget import JudgeDanmuWidget
from logic.gutils import judge_utils
TOUCH_MODE_ROUTE = 0
TOUCH_MODE_MARK = 1

class BigMapUI(MapBaseUI):
    PANEL_CONFIG_NAME = 'map/map_big_new'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    IS_PLAY_OPEN_SOUND = False
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'btn_show_name.OnClick': '_on_click_btn_show_name'
       }
    UI_VKB_TYPE = UI_VKB_CUSTOM
    HOT_KEY_FUNC_MAP = {'switch_big_map': 'keyboard_switch_big_map'}
    HOT_KEY_FUNC_MAP_SHOW = {'switch_big_map': {'node': 'temp_pc'}}
    GLOBAL_EVENT = {}

    def on_init_panel--- This code section failed: ---

  36       0  LOAD_CONST            0  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  'mark_ctrl_widget'

  37       9  LOAD_CONST            0  ''
          12  LOAD_FAST             0  'self'
          15  STORE_ATTR            2  'touch_layer_widget'

  38      18  LOAD_CONST            0  ''
          21  LOAD_FAST             0  'self'
          24  STORE_ATTR            3  'map_scale_slider'

  39      27  LOAD_CONST            1  300
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            4  'view_dist'

  40      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             5  'set_associated_ui_visible'
          42  LOAD_GLOBAL           6  'False'
          45  CALL_FUNCTION_1       1 
          48  POP_TOP          

  41      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             7  'enable_common_marks_animation'
          55  LOAD_GLOBAL           8  'True'
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          

  42      62  LOAD_GLOBAL           9  'super'
          65  LOAD_GLOBAL          10  'BigMapUI'
          68  LOAD_FAST             0  'self'
          71  CALL_FUNCTION_2       2 
          74  LOAD_ATTR            11  'on_init_panel'
          77  LOAD_FAST             1  'args'
          80  LOAD_FAST             2  'kwargs'
          83  CALL_FUNCTION_VAR_KW_0     0 
          86  POP_TOP          

  43      87  LOAD_FAST             0  'self'
          90  LOAD_ATTR            12  'init_mark_widget'
          93  CALL_FUNCTION_0       0 
          96  POP_TOP          

  44      97  LOAD_FAST             0  'self'
         100  LOAD_ATTR            13  'panel'
         103  LOAD_ATTR            14  'btn_close'
         106  LOAD_ATTR            15  'set_sound_enable'
         109  LOAD_GLOBAL           6  'False'
         112  CALL_FUNCTION_1       1 
         115  POP_TOP          

  46     116  LOAD_GLOBAL          16  'add_uiclick_add_up_salog'
         119  LOAD_CONST            2  'open_map_cnt'
         122  LOAD_CONST            3  ''
         125  CALL_FUNCTION_2       2 
         128  POP_TOP          

  49     129  LOAD_FAST             0  'self'
         132  LOAD_ATTR            13  'panel'
         135  LOAD_ATTR            17  'btn_show_name'
         138  LOAD_ATTR            18  'SetSelect'
         141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            19  'player_info_widget'
         147  LOAD_ATTR            20  'b_show_player_name'
         150  CALL_FUNCTION_0       0 
         153  CALL_FUNCTION_1       1 
         156  POP_TOP          

  51     157  LOAD_GLOBAL          21  'hasattr'
         160  LOAD_GLOBAL           4  'view_dist'
         163  CALL_FUNCTION_2       2 
         166  POP_JUMP_IF_FALSE   200  'to 200'

  52     169  LOAD_GLOBAL          22  'judge_utils'
         172  LOAD_ATTR            23  'is_ob'
         175  CALL_FUNCTION_0       0 
         178  POP_JUMP_IF_FALSE   200  'to 200'

  53     181  LOAD_FAST             0  'self'
         184  LOAD_ATTR            24  'destroy_widget'
         187  LOAD_CONST            4  'poison_direction'
         190  CALL_FUNCTION_1       1 
         193  POP_TOP          
         194  JUMP_ABSOLUTE       200  'to 200'
         197  JUMP_FORWARD          0  'to 200'
       200_0  COME_FROM                '197'

  55     200  LOAD_GLOBAL          22  'judge_utils'
         203  LOAD_ATTR            23  'is_ob'
         206  CALL_FUNCTION_0       0 
         209  POP_JUMP_IF_FALSE   246  'to 246'
         212  LOAD_GLOBAL          22  'judge_utils'
         215  LOAD_ATTR            25  'get_ob_target_id'
         218  CALL_FUNCTION_0       0 
       221_0  COME_FROM                '209'
         221  POP_JUMP_IF_FALSE   246  'to 246'

  56     224  LOAD_FAST             0  'self'
         227  LOAD_ATTR            26  'center_map_with_player'
         230  LOAD_GLOBAL          22  'judge_utils'
         233  LOAD_ATTR            25  'get_ob_target_id'
         236  CALL_FUNCTION_0       0 
         239  CALL_FUNCTION_1       1 
         242  POP_TOP          
         243  JUMP_FORWARD         85  'to 331'

  58     246  LOAD_FAST             0  'self'
         249  LOAD_ATTR            27  'init_map_offset'
         252  POP_JUMP_IF_FALSE   280  'to 280'

  59     255  LOAD_FAST             0  'self'
         258  LOAD_ATTR            13  'panel'
         261  LOAD_ATTR            28  'sv_map'
         264  LOAD_ATTR            29  'SetContentOffset'
         267  LOAD_FAST             0  'self'
         270  LOAD_ATTR            27  'init_map_offset'
         273  CALL_FUNCTION_1       1 
         276  POP_TOP          
         277  JUMP_FORWARD         51  'to 331'

  61     280  LOAD_FAST             0  'self'
         283  LOAD_ATTR            30  'map_nd'
         286  LOAD_ATTR            31  'CalcPosition'
         289  LOAD_CONST            5  '50%'
         292  LOAD_CONST            5  '50%'
         295  CALL_FUNCTION_2       2 
         298  STORE_FAST            3  'center_pos'

  62     301  LOAD_FAST             0  'self'
         304  LOAD_ATTR            13  'panel'
         307  LOAD_ATTR            28  'sv_map'
         310  LOAD_ATTR            32  'CenterWithPos'
         313  LOAD_FAST             3  'center_pos'
         316  LOAD_CONST            6  ''
         319  BINARY_SUBSCR    
         320  LOAD_FAST             3  'center_pos'
         323  LOAD_CONST            7  1
         326  BINARY_SUBSCR    
         327  CALL_FUNCTION_2       2 
         330  POP_TOP          
       331_0  COME_FROM                '277'
       331_1  COME_FROM                '243'

  63     331  LOAD_FAST             0  'self'
         334  LOAD_ATTR            13  'panel'
         337  LOAD_ATTR            28  'sv_map'
         340  LOAD_ATTR            33  'setSwallowTouches'
         343  LOAD_GLOBAL           8  'True'
         346  CALL_FUNCTION_1       1 
         349  POP_TOP          
         350  LOAD_CONST            0  ''
         353  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 163

    def init_mark_widget(self):
        self.touch_mode = TOUCH_MODE_MARK

    def init_map_legend(self):
        from logic.comsys.map.map_widget.BigMapLegendWidget import BigMapLegendWidget
        self.map_legend_widget = BigMapLegendWidget(self)

    def init_judge_component(self):
        from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget

        def camera_btn_click_cb():
            self.on_click_close_btn()

        self.judge_observation_list_widget = JudgeObservationListWidget(self.panel.list_tab_change, self.panel.list_choose, on_camera_btn_click=camera_btn_click_cb)
        self.judge_danmu_widget = JudgeDanmuWidget(self.panel.nd_danmu)

    def init_touch_layer_widget(self):
        from logic.comsys.map.map_widget.BigMapTouchLayerWidget import BigMapTouchLayerWidget
        self.touch_layer_widget = BigMapTouchLayerWidget(self)

    def switch_touch_mode(self):
        mode = TOUCH_MODE_ROUTE if self.touch_mode != TOUCH_MODE_ROUTE else TOUCH_MODE_MARK
        self.touch_mode = mode
        is_route_mode = mode == TOUCH_MODE_ROUTE
        self.panel.btn_draw.SetSelect(is_route_mode)
        self.route_board.set_enable_draw(is_route_mode)
        self.touch_layer.SetEnableTouch(not is_route_mode)
        self.tips_draw.setVisible(is_route_mode)

    def init_sub_component(self):
        self.init_slider_component()
        self.init_mark_btn_component()
        self.init_touch_layer_widget()
        if not judge_utils.is_ob():
            self.panel.nd_map_example.setVisible(True)
            self.init_map_legend()
            self.panel.nd_judgement.setVisible(False)
        else:
            self.panel.nd_map_example.setVisible(False)
            self.panel.nd_judgement.setVisible(True)
            self.init_judge_component()

    def init_mark_btn_component(self):
        from logic.comsys.map.map_widget.BigMapMarkBtnWidget import BigMapMarkBtnWidget
        self.mark_ctrl_widget = BigMapMarkBtnWidget(self)
        self.mark_ctrl_widget.set_route_and_mark_visible(not judge_utils.is_ob())

    def on_map_scaling(self, map_scale):
        super(BigMapUI, self).on_map_scaling(map_scale)
        if self.map_scale_slider:
            percent = (map_scale - self.min_map_scale) / (self.max_map_scale - self.min_map_scale) * 100.0
            self.map_scale_slider.force_slider_changed(percent)

    def init_slider_component(self):
        from logic.comsys.common_ui.UIScaleSliderWidget import UIScaleSliderWidget
        init_percent = (self.cur_map_scale - self.min_map_scale) / (self.max_map_scale - self.min_map_scale) * 100.0
        slider_args = {'slider': self.zoom_slider,
           'init_percent': init_percent,
           'scale_callback': self.on_scale_callback,
           'change_step': max((self.max_map_scale - self.min_map_scale) * 0.05, 1)
           }
        self.map_scale_slider = UIScaleSliderWidget(**slider_args)

    def on_scale_callback(self, percent):
        new_scale = (self.max_map_scale - self.min_map_scale) * percent / 100.0 + self.min_map_scale
        self.scale_with_touch_pos(self.panel.sv_map.ConvertToWorldSpacePercentage(50, 50), new_scale)

    def init_parameters(self, **kwargs):
        self.is_mark_btn_show = False
        self.is_extend_list_show = None
        self.cur_map_draw_mode = None
        self._selected_draw_mode_ui_item = None
        self.is_first_player_setted = True
        self.map_scale_slider = None
        self._need_place_name = True
        super(BigMapUI, self).init_parameters(**kwargs)
        self.init_sub_component()
        self.init_map_offset = kwargs.get('center_pos')
        return

    def init_circle(self, show_effect=True):
        super(BigMapUI, self).init_circle(show_effect=True, show_no_signal=True)

    def on_init_complete(self):
        pass

    def on_click_close_btn(self, *args):
        self.close()
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'map_zoom_in'))

    def _on_click_btn_show_name--- This code section failed: ---

 157       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'player_info_widget'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    76  'to 76'

 158      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'player_info_widget'
          18  LOAD_ATTR             2  'set_show_player_name'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             3  'panel'
          27  LOAD_ATTR             4  'btn_show_name'
          30  LOAD_ATTR             5  'GetSelect'
          33  CALL_FUNCTION_0       0 
          36  UNARY_NOT        
          37  CALL_FUNCTION_1       1 
          40  POP_TOP          

 159      41  LOAD_FAST             0  'self'
          44  LOAD_ATTR             3  'panel'
          47  LOAD_ATTR             4  'btn_show_name'
          50  LOAD_ATTR             6  'SetSelect'
          53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             3  'panel'
          59  LOAD_ATTR             4  'btn_show_name'
          62  LOAD_ATTR             5  'GetSelect'
          65  CALL_FUNCTION_0       0 
          68  UNARY_NOT        
          69  CALL_FUNCTION_1       1 
          72  POP_TOP          
          73  JUMP_FORWARD          0  'to 76'
        76_0  COME_FROM                '73'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_finalize_panel(self):
        self.destroy_widget('mark_ctrl_widget')
        self.destroy_widget('touch_layer_widget')
        self.destroy_widget('map_scale_slider')
        self.destroy_widget('map_legend_widget')
        self.destroy_widget('judge_observation_list_widget')
        self.destroy_widget('judge_danmu_widget')
        super(BigMapUI, self).on_finalize_panel()
        self.set_associated_ui_visible(True)
        global_data.emgr.scene_save_map_info_event.emit(self.cur_map_scale, self.panel.sv_map.GetContentOffset())

    def get_min_map_scale(self):
        sz = self.panel.sv_map.getContentSize()
        height_scale = float(sz.height) / self.map_pixel_height
        width_scale = float(sz.width) / self.map_pixel_width
        return max(height_scale, width_scale)

    def init_drawboard(self):
        super(BigMapUI, self).init_drawboard(self.draw_board_drag_end)

    def draw_board_drag_end(self, draw_points):
        if global_data.player and global_data.player.logic:
            t_points = [ (p.x, p.y) for p in draw_points ]
            target = global_data.player.logic
            target.send_event('E_TRY_DRAW_MAP_ROUTE', t_points)
        self.switch_touch_mode()

    def set_associated_ui_visible(self, visible):
        if not visible:
            _types = [
             UI_TYPE_NORMAL]
            if judge_utils.is_ob():
                _types.append(UI_TYPE_TRANS)
            self.hide_all_ui_by_type('BigMapUI', types=_types, exceptions=['MoveRockerUI', 'MoveRockerTouchUI', 'SceneTouchBlockUI', 'BagUIPC', 'PrepareUI', 'GuideUI'])
        else:
            self.revert_hide_all_ui_by_type_action('BigMapUI')

    def scale_with_touch_pos(self, touch_wpos, scale):
        lpos = self.map_nd.getParent().convertToNodeSpace(touch_wpos)
        sz = self.panel.sv_map.GetInnerContentSize()
        zoom_anchor_x = lpos.x / sz.width
        zoom_anchor_y = lpos.y / sz.height
        self.set_map_scale_with_anchor(scale, zoom_anchor_x, zoom_anchor_y)

    def add_common_mark(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        common_mark = super(BigMapUI, self).add_common_mark(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)
        if common_mark:
            common_mark.check_bigmap_action()

    def keyboard_switch_big_map(self, msg, keycode):
        self.close()

    def close(self, *args):
        if judge_utils.is_ob() and not global_data.is_in_judge_camera:
            cur_ob_id = judge_utils.get_ob_target_id()
            if cur_ob_id is None:
                global_data.emgr.battle_show_message_event.emit(get_text_local_content(19610))
                return
        super(BigMapUI, self).close(*args)
        return

    def ui_vkb_custom_func(self):
        self.on_click_close_btn()
        return True

    def _on_ob_com_inited--- This code section failed: ---

 231       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'BigMapUI'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  '_on_ob_com_inited'
          15  LOAD_FAST             1  'pid'
          18  LOAD_FAST             2  'is_ob'
          21  CALL_FUNCTION_2       2 
          24  POP_TOP          

 234      25  LOAD_GLOBAL           3  'hasattr'
          28  LOAD_GLOBAL           1  'BigMapUI'
          31  CALL_FUNCTION_2       2 
          34  POP_JUMP_IF_FALSE    68  'to 68'

 235      37  LOAD_GLOBAL           4  'judge_utils'
          40  LOAD_ATTR             5  'is_ob'
          43  CALL_FUNCTION_0       0 
          46  POP_JUMP_IF_FALSE    68  'to 68'

 236      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             6  'destroy_widget'
          55  LOAD_CONST            1  'poison_direction'
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          
          62  JUMP_ABSOLUTE        68  'to 68'
          65  JUMP_FORWARD          0  'to 68'
        68_0  COME_FROM                '65'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 31

    def get_player_info_widget(self):
        return self.player_info_widget