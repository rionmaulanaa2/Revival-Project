# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/PlanSkinDefineWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.vscene.parts.PartModelDisplay import CLobbyModel
from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_PLAN_POS_SUB_SKIN, FASHION_OTHER_PENDANT_LIST
from common.algorithm import resloader
import game3d
from logic.gutils.new_template_utils import SingleChooseWidget
SKIN_PLAN_MAX_COUNT = 3
EMPTY_SKIN_PLAN_DATA = [-1, -1, -1, -1]
import weakref
from logic.gutils import dress_utils, lobby_model_display_utils, template_utils

class PlanRenderTarget(object):

    def __init__(self):
        self.model_objs = []
        self.force_refresh = False
        self.plan_target = None
        self.model_data = {}
        self.is_scene_ready = False
        self.is_need_update_show_model = False
        self.scene = None
        self._view_flag = True
        self.scene_data = {}
        self.init_scene_data()
        self.plan_data_dict = {}
        return

    def init_scene_data(self):
        self.box_name = 'plan_box'
        self.scene_data = {'box_name': self.box_name}

    def destroy--- This code section failed: ---

  42       0  LOAD_GLOBAL           0  'resloader'
           3  LOAD_ATTR             1  'del_res_attr'
           6  LOAD_ATTR             1  'del_res_attr'
           9  CALL_FUNCTION_2       2 
          12  POP_TOP          

  43      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             2  'clear_models'
          19  CALL_FUNCTION_0       0 
          22  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9

    def set_plan(self, plan_data, sprite_obj):
        self.plan_data_dict = plan_data
        self.sprite_obj = sprite_obj
        self.is_need_update_show_model = True
        if not self.plan_target:
            self.init_plan_render_target(sprite_obj)
        if self.is_scene_ready:
            self.check_update_show_model()

    def get_preview_model_data(self, plan_data_dict, other_preview_decoration=None, need_show_ani=False):
        role_id = plan_data_dict.get('role_id')
        skin_id = plan_data_dict.get('skin_id')
        preview_decoration = plan_data_dict.get('preview_decoration', {})
        if not role_id or not skin_id:
            log_error('error plan data dict', self.plan_data_dict)
        mpath = dress_utils.get_role_model_path_by_lod(role_id, skin_id, 'h')
        item_no = dress_utils.get_role_item_no(role_id, skin_id)
        if other_preview_decoration:
            preview_decoration.update(other_preview_decoration)
        if mpath is not None:
            head_id = preview_decoration.get(FASHION_POS_HEADWEAR)
            bag_id = preview_decoration.get(FASHION_POS_BACK)
            suit_id = preview_decoration.get(FASHION_POS_SUIT_2)
            other_pendants = [ preview_decoration.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no, skin_id=skin_id, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            from logic.gutils import item_utils
            from logic.gcommon.item import lobby_item_type
            is_mecha = item_utils.get_lobby_item_type(item_no) in [lobby_item_type.L_ITEM_TYPE_MECHA_SKIN, lobby_item_type.L_ITEM_TYPE_MECHA]
            if not need_show_ani:
                for data in model_data:
                    if is_mecha:
                        if not data['mecha_end_ani']:
                            continue
                        data['show_anim'] = data['mecha_end_ani']
                        data['end_anim'] = data['mecha_end_ani']
                    else:
                        if not data['end_anim']:
                            continue
                        data['show_anim'] = data['end_anim']

            return model_data
        else:
            return

    def init_plan_render_target--- This code section failed: ---

 102       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'math3d'
           9  STORE_FAST            2  'math3d'
          12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'math'
          21  STORE_FAST            3  'math'

 103      24  LOAD_FAST             1  'sprite_obj'
          27  LOAD_ATTR             2  'getContentSize'
          30  CALL_FUNCTION_0       0 
          33  STORE_FAST            4  'sz'

 104      36  BUILD_MAP_6           6 

 105      39  LOAD_CONST            2  4278190080L
          42  LOAD_CONST            3  'scn_bg_color'
          45  STORE_MAP        

 106      46  LOAD_CONST            4  30.0
          49  LOAD_CONST            5  'cam_fov'
          52  STORE_MAP        

 107      53  LOAD_FAST             4  'sz'
          56  LOAD_ATTR             3  'width'
          59  LOAD_CONST            6  2
          62  BINARY_MULTIPLY  
          63  LOAD_CONST            7  'rt_width'
          66  STORE_MAP        

 108      67  LOAD_FAST             4  'sz'
          70  LOAD_ATTR             4  'height'
          73  LOAD_CONST            6  2
          76  BINARY_MULTIPLY  
          77  LOAD_CONST            8  'rt_height'
          80  STORE_MAP        

 109      81  LOAD_FAST             2  'math3d'
          84  LOAD_ATTR             5  'vector'
          87  LOAD_CONST            1  ''
          90  LOAD_FAST             3  'math'
          93  LOAD_ATTR             6  'pi'
          96  LOAD_CONST            1  ''
          99  CALL_FUNCTION_3       3 
         102  LOAD_CONST            9  'cam_euler'
         105  STORE_MAP        

 110     106  LOAD_FAST             2  'math3d'
         109  LOAD_ATTR             5  'vector'
         112  LOAD_CONST            1  ''
         115  LOAD_CONST           10  18
         118  LOAD_CONST           11  25
         121  CALL_FUNCTION_3       3 
         124  LOAD_CONST           12  'cam_pos'
         127  STORE_MAP        
         128  STORE_FAST            5  'MAP_RT_CONF'

 112     131  LOAD_CONST            1  ''
         134  LOAD_CONST           13  ('RenderTargetHolder',)
         137  IMPORT_NAME           7  'common.uisys.render_target'
         140  IMPORT_FROM           8  'RenderTargetHolder'
         143  STORE_FAST            6  'RenderTargetHolder'
         146  POP_TOP          

 113     147  LOAD_FAST             0  'self'
         150  LOAD_ATTR             9  'plan_target'
         153  POP_JUMP_IF_TRUE    189  'to 189'

 114     156  LOAD_FAST             6  'RenderTargetHolder'
         159  LOAD_CONST            0  ''
         162  LOAD_FAST             1  'sprite_obj'
         165  LOAD_FAST             5  'MAP_RT_CONF'
         168  LOAD_CONST           14  'all_light'
         171  LOAD_CONST           15  'dir_light'
         174  BUILD_LIST_1          1 
         177  CALL_FUNCTION_259   259 
         180  LOAD_FAST             0  'self'
         183  STORE_ATTR            9  'plan_target'
         186  JUMP_FORWARD          0  'to 189'
       189_0  COME_FROM                '186'

 115     189  LOAD_FAST             0  'self'
         192  LOAD_ATTR             9  'plan_target'
         195  LOAD_ATTR            11  'scn'
         198  LOAD_ATTR            12  'load_env'
         201  LOAD_CONST           16  'scene/scene_env_confs/bw.xml'
         204  CALL_FUNCTION_1       1 
         207  POP_TOP          

 116     208  LOAD_CONST           17  16777215
         211  LOAD_FAST             0  'self'
         214  LOAD_ATTR             9  'plan_target'
         217  LOAD_ATTR            11  'scn'
         220  STORE_ATTR           13  'background_color'

 117     223  LOAD_FAST             0  'self'
         226  LOAD_ATTR             9  'plan_target'
         229  LOAD_ATTR            14  'start_render_target'
         232  CALL_FUNCTION_0       0 
         235  POP_TOP          

 119     236  LOAD_GLOBAL          15  'weakref'
         239  LOAD_ATTR            16  'ref'
         242  LOAD_FAST             0  'self'
         245  LOAD_ATTR             9  'plan_target'
         248  LOAD_ATTR            11  'scn'
         251  CALL_FUNCTION_1       1 
         254  LOAD_FAST             0  'self'
         257  STORE_ATTR           17  'scene'

 120     260  LOAD_CONST           18  'model\\others\\bw_box.gim'
         263  STORE_FAST            7  'mpath'

 121     266  LOAD_GLOBAL          18  'resloader'
         269  LOAD_ATTR            19  'load_res_attr'

 122     272  LOAD_ATTR            19  'load_res_attr'

 123     275  LOAD_FAST             7  'mpath'

 124     278  LOAD_FAST             0  'self'
         281  LOAD_ATTR            20  'on_load_box_model_complete'

 125     284  BUILD_MAP_0           0 
         287  LOAD_CONST           20  'res_type'

 126     290  LOAD_CONST           21  'MODEL'
         293  LOAD_CONST           22  'priority'

 127     296  LOAD_GLOBAL          21  'game3d'
         299  LOAD_ATTR            22  'ASYNC_HIGH'
         302  CALL_FUNCTION_517   517 
         305  POP_TOP          
         306  LOAD_CONST            0  ''
         309  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_517' instruction at offset 302

    def on_load_box_model_complete(self, model, userdata, *args):
        model.name = self.box_name
        model.visible = False
        self.plan_target.scn.add_object(model)
        self.is_scene_ready = True
        self.check_update_show_model()

    def check_update_show_model(self):
        if self.is_need_update_show_model and self.is_scene_ready:
            self.clear_models()
            self.model_data = self.get_preview_model_data(self.plan_data_dict)

            def on_finish_create_model(model, *args):
                if model:
                    model.all_materials.enable_write_alpha = True

            self.on_change_display_model(self.model_data, create_callback=on_finish_create_model, is_render_target_model=True, support_mirror=False)

    def on_change_display_model(self, model_data, **kwargs):
        if self.model_data == model_data and self.model_objs and not self.force_refresh:
            if model_data is None:
                return
            create_callback = kwargs.get('create_callback', None)
            is_play_show_anim = False
            if len(model_data) > 0:
                is_play_show_anim = model_data[0].get('show_anim', None) != None
            if is_play_show_anim:
                for one_model_obj in self.model_objs:
                    one_model_obj.create_callback = create_callback
                    one_model_obj.play_show_anim()

            return
        else:
            self.force_refresh = False
            self.model_data = model_data
            self.clear_models()
            if not model_data:
                return
            for data in model_data:
                obj = CLobbyModel(self, data, **kwargs)
                self.model_objs.append(obj)

            return

    def clear_models(self):
        for obj in self.model_objs:
            obj.destroy()

        self.model_objs = []


class SkinPlanWidget(object):

    def __init__(self, panel, parent):
        self.panel = panel
        self.role_id = 0
        self.top_skin_id = 0
        self.plan_list = []
        self.plan_widget_list = {}
        self.parent = parent
        self._fetch_callback = None
        self._apply_callback = None
        self.single_choose_widget = None
        self.single_choose_widget = SingleChooseWidget()
        self.single_choose_widget.SetCallbacks(self.on_select_status_change, self.on_select_status_ui_update)
        return

    def set_callback(self, fetch_callback, apply_callback):
        self._fetch_callback = fetch_callback
        self._apply_callback = apply_callback

    def destroy(self):
        self.set_callback(None, None)
        self.panel = None
        self.parent = None
        if self.single_choose_widget:
            self.single_choose_widget.destroy()
        self.single_choose_widget = None
        for widget in six.itervalues(self.plan_widget_list):
            widget.destroy()

        self.plan_widget_list = {}
        return

    def on_select_status_change(self, idx, is_sel):
        pass

    def on_select_status_ui_update(self, ui_item, is_sel):
        ui_item.nd_choose.setVisible(is_sel)

    def refresh_plan_list(self):
        self.panel.bar.list_plan.SetInitCount(SKIN_PLAN_MAX_COUNT)
        allItem = self.panel.bar.list_plan.GetAllItem()
        self.single_choose_widget.init(self.panel, allItem, ui_item_btn_name='btn_plan')
        for idx, ui_item in enumerate(allItem):
            self.refresh_plan_ui_by_index(ui_item, idx)

    def refresh_plan_ui_by_index(self, ui_item, idx):
        has_valid_plan_data = False
        if idx < len(self.plan_list):
            try:
                skin_id = self.plan_list[idx][FASHION_PLAN_POS_SUB_SKIN]
                if skin_id != -1 and skin_id != 0 and skin_id != None:
                    has_valid_plan_data = True
            except:
                pass

        else:
            has_valid_plan_data = False
        if not has_valid_plan_data:
            ui_item.nd_empty.setVisible(True)
            ui_item.nd_model.setVisible(False)
        else:
            ui_item.nd_empty.setVisible(False)
            ui_item.nd_model.setVisible(True)
            widget = self.plan_widget_list.get(idx)
            if not widget:
                self.plan_widget_list[idx] = PlanRenderTarget()
            widget = self.plan_widget_list.get(idx)
            if widget:
                fashion_dict, _ = dress_utils.skin_plan_to_fashion_dict(self.plan_list[idx])
                plan_dict = {'role_id': self.role_id,
                   'skin_id': self.plan_list[idx][FASHION_PLAN_POS_SUB_SKIN],
                   'preview_decoration': fashion_dict
                   }
                widget.set_plan(plan_dict, ui_item.sp_model)
        ui_item.lab_plan_name.SetString('\xe6\x96\xb9\xe6\xa1\x88%s' % str(idx + 1))
        ui_item.btn_edit.setVisible(False)

        @ui_item.btn_use.callback()
        def OnClick(btn, touch, idx=idx):
            self.apply_plan(idx)
            self.single_choose_widget.set_ui_item_select_status_by_idx(idx, False)

        @ui_item.btn_save.callback()
        def OnClick(btn, touch, idx=idx):
            if self._fetch_callback:
                ls = self._fetch_callback()
                self.save_cur_preview_plan(idx, ls)
                self.single_choose_widget.set_ui_item_select_status_by_idx(idx, False)

        return

    def save_cur_preview_plan(self, idx, preview_data):
        if not self.top_skin_id:
            log_error('invalid top skin id!')
            return
        if not global_data.player:
            return
        if idx < SKIN_PLAN_MAX_COUNT:
            if len(self.plan_list) < SKIN_PLAN_MAX_COUNT:
                for i in range(len(self.plan_list), SKIN_PLAN_MAX_COUNT):
                    self.plan_list.append(list())

            self.plan_list[idx] = preview_data
            if idx < len(self.plan_list):
                if global_data.player:
                    global_data.player.upload_fashion_scheme(self.top_skin_id, self.plan_list)
                ui_item = self.panel.bar.list_plan.GetItem(idx)
                if ui_item:
                    self.refresh_plan_ui_by_index(ui_item, idx)

    def apply_plan(self, idx):
        if idx < len(self.plan_list):
            plan_data = self.plan_list[idx]
            if plan_data:
                skin_id = plan_data[FASHION_PLAN_POS_SUB_SKIN]
                preview_data_dict, _ = dress_utils.skin_plan_to_fashion_dict(plan_data)
                if skin_id:
                    if self._apply_callback:
                        self._apply_callback(skin_id, preview_data_dict)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(860090))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(860090))
        else:
            global_data.game_mgr.show_tip(get_text_by_id(860090))

    def hide_plan_list(self):
        self.panel.bar.list_plan.setVisible(False)

    def show_plan_list(self):
        self.panel.bar.list_plan.setVisible(True)

    def set_plan_info(self, role_id, top_skin_id, plan_list):
        self.role_id = role_id
        self.top_skin_id = top_skin_id
        self.plan_list = plan_list
        self.refresh_plan_list()