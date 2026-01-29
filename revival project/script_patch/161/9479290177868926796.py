# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComMechaTransparentModel.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from common.utils.pc_platform_utils import get_shader_name_from_tech_name
import game3d
import render
SFX_TRANSPARENT_ALPHA_PERCENT = 0.5
NEED_HIDE_MESH_MECHA = (8034, )

class ComMechaTransparentModel(UnitCom):
    BIND_EVENT = {'E_SET_MODEL_OPACITY': 'enter_opacity_mode',
       'E_LEAVE_MODEL_OPACITY': 'leave_opacity_mode',
       'G_IS_MODEL_OPACITY': 'get_is_model_opacity',
       'E_DISABLE_TRANSPARENT': 'disable_transparent'
       }

    def __init__(self):
        super(ComMechaTransparentModel, self).__init__()
        self.need_update = False
        self._is_in_opacity = False
        self._is_enable = True
        self.hided_mesh = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaTransparentModel, self).init_from_dict(unit_obj, bdict)
        self.need_hide_mesh = self.ev_g_mecha_id() in NEED_HIDE_MESH_MECHA
        self.sd.ref_model_opacity = 255

    def enter_opacity_mode(self, opacity):
        model = self.ev_g_model()
        if model and model.valid:
            if not self.ev_g_is_avatar():
                model.set_rendergroup_and_priority(0, 0)
                model.enable_dynamic_culling(False)
                self.sd.ref_socket_res_agent.refresh_render_priority(0)
        model = self.ev_g_model()
        self._set_model_opacity(model, opacity)
        if not self._is_in_opacity:
            self._is_in_opacity = True
            if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.cam_lctarget and self.unit_obj == global_data.cam_lctarget:
                global_data.emgr.camera_lctarget_open_prez.emit(self._is_in_opacity)
        self.sd.ref_model_opacity = opacity
        if self.need_hide_mesh and self.hided_mesh is None:
            self.hided_mesh = []
            sub_count = model.get_submesh_count()
            for index in range(sub_count):
                sub_material = model.get_sub_material(index)
                if sub_material.transparent_mode > 1 and model.get_submesh_visible(index):
                    self.hided_mesh.append(index)
                    model.set_submesh_visible(index, False)

        return

    def leave_opacity_mode--- This code section failed: ---

  66       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_is_in_opacity'
           6  POP_JUMP_IF_FALSE   297  'to 297'

  67       9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             1  'ev_g_model'
          15  CALL_FUNCTION_0       0 
          18  STORE_FAST            1  'model'

  68      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  '_set_model_opaque'
          27  LOAD_FAST             1  'model'
          30  CALL_FUNCTION_1       1 
          33  POP_TOP          

  69      34  LOAD_GLOBAL           3  'False'
          37  LOAD_FAST             0  'self'
          40  STORE_ATTR            0  '_is_in_opacity'

  70      43  LOAD_GLOBAL           4  'game3d'
          46  LOAD_ATTR             5  'get_platform'
          49  CALL_FUNCTION_0       0 
          52  LOAD_GLOBAL           4  'game3d'
          55  LOAD_ATTR             6  'PLATFORM_IOS'
          58  COMPARE_OP            2  '=='
          61  POP_JUMP_IF_FALSE   116  'to 116'
          64  LOAD_GLOBAL           7  'global_data'
          67  LOAD_ATTR             8  'cam_lctarget'
          70  POP_JUMP_IF_FALSE   116  'to 116'
          73  LOAD_FAST             0  'self'
          76  LOAD_ATTR             9  'unit_obj'
          79  LOAD_GLOBAL           7  'global_data'
          82  LOAD_ATTR             8  'cam_lctarget'
          85  COMPARE_OP            2  '=='
        88_0  COME_FROM                '70'
        88_1  COME_FROM                '61'
          88  POP_JUMP_IF_FALSE   116  'to 116'

  71      91  LOAD_GLOBAL           7  'global_data'
          94  LOAD_ATTR            10  'emgr'
          97  LOAD_ATTR            11  'camera_lctarget_open_prez'
         100  LOAD_ATTR            12  'emit'
         103  LOAD_FAST             0  'self'
         106  LOAD_ATTR             0  '_is_in_opacity'
         109  CALL_FUNCTION_1       1 
         112  POP_TOP          
         113  JUMP_FORWARD          0  'to 116'
       116_0  COME_FROM                '113'

  74     116  LOAD_FAST             1  'model'
         119  POP_JUMP_IF_FALSE   297  'to 297'
         122  LOAD_FAST             1  'model'
         125  LOAD_ATTR            13  'valid'
       128_0  COME_FROM                '119'
         128  POP_JUMP_IF_FALSE   297  'to 297'

  75     131  LOAD_FAST             0  'self'
         134  LOAD_ATTR            14  'ev_g_is_avatar'
         137  CALL_FUNCTION_0       0 
         140  POP_JUMP_IF_TRUE    194  'to 194'

  76     143  LOAD_FAST             1  'model'
         146  LOAD_ATTR            15  'set_rendergroup_and_priority'
         149  LOAD_CONST            1  28
         152  LOAD_CONST            2  ''
         155  CALL_FUNCTION_2       2 
         158  POP_TOP          

  77     159  LOAD_FAST             1  'model'
         162  LOAD_ATTR            16  'enable_dynamic_culling'
         165  LOAD_GLOBAL          17  'True'
         168  CALL_FUNCTION_1       1 
         171  POP_TOP          

  78     172  LOAD_FAST             0  'self'
         175  LOAD_ATTR            18  'sd'
         178  LOAD_ATTR            19  'ref_socket_res_agent'
         181  LOAD_ATTR            20  'refresh_render_priority'
         184  LOAD_CONST            1  28
         187  CALL_FUNCTION_1       1 
         190  POP_TOP          
         191  JUMP_FORWARD          0  'to 194'
       194_0  COME_FROM                '191'

  80     194  LOAD_FAST             0  'self'
         197  LOAD_ATTR            21  'need_hide_mesh'
         200  POP_JUMP_IF_FALSE   294  'to 294'
         203  LOAD_GLOBAL          22  'getattr'
         206  LOAD_GLOBAL           3  'False'
         209  CALL_FUNCTION_2       2 
       212_0  COME_FROM                '200'
         212  POP_JUMP_IF_FALSE   294  'to 294'

  81     215  LOAD_FAST             1  'model'
         218  LOAD_ATTR            23  'get_submesh_count'
         221  CALL_FUNCTION_0       0 
         224  STORE_FAST            2  'sub_count'

  82     227  SETUP_LOOP           49  'to 279'
         230  LOAD_FAST             0  'self'
         233  LOAD_ATTR            24  'hided_mesh'
         236  GET_ITER         
         237  FOR_ITER             38  'to 278'
         240  STORE_FAST            3  'index'

  83     243  LOAD_FAST             2  'sub_count'
         246  LOAD_FAST             3  'index'
         249  COMPARE_OP            0  '<'
         252  POP_JUMP_IF_FALSE   259  'to 259'

  84     255  BREAK_LOOP       
         256  JUMP_FORWARD          0  'to 259'
       259_0  COME_FROM                '256'

  85     259  LOAD_FAST             1  'model'
         262  LOAD_ATTR            25  'set_submesh_visible'
         265  LOAD_FAST             3  'index'
         268  LOAD_GLOBAL          17  'True'
         271  CALL_FUNCTION_2       2 
         274  POP_TOP          
         275  JUMP_BACK           237  'to 237'
         278  POP_BLOCK        
       279_0  COME_FROM                '227'

  86     279  LOAD_CONST            0  ''
         282  LOAD_FAST             0  'self'
         285  STORE_ATTR           24  'hided_mesh'
         288  JUMP_ABSOLUTE       294  'to 294'
         291  JUMP_ABSOLUTE       297  'to 297'
         294  JUMP_FORWARD          0  'to 297'
       297_0  COME_FROM                '294'

  87     297  LOAD_CONST            4  255
         300  LOAD_FAST             0  'self'
         303  LOAD_ATTR            18  'sd'
         306  STORE_ATTR           27  'ref_model_opacity'
         309  LOAD_CONST            0  ''
         312  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 209

    def disable_transparent(self, is_disable):
        if is_disable:
            model = self.ev_g_model()
            self._set_model_opaque(model)
        self._is_enable = not is_disable

    @staticmethod
    def _check_need_block_transparent(model_res):
        for index in range(model_res.get_submesh_count()):
            sub_material = model_res.get_sub_material(index)
            if get_shader_name_from_tech_name(sub_material.get_technique_name()) == 'g93shader\\head_spline':
                global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b{}\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81\xe8\xae\xbe\xe7\xbd\xae\xe5\x8d\x8a\xe9\x80\x8f\xe6\x98\x8e\xef\xbc\x8c\xe8\xaf\xb7\xe5\xb0\x86g93shader\\head_spline\xe6\x9d\x90\xe8\xb4\xa8\xe6\x94\xb9\xe4\xb8\xbag93shader\\head_spline_alpha\xef\xbc\x8c\xe6\x88\x96\xe5\x9c\xa8163\xe8\xa1\xa8\xe6\xb7\xbb\xe5\x8a\xa0ignore_transparent\xe5\xad\x97\xe6\xae\xb5'.format(model_res.filename))
                global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b{}\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81\xe8\xae\xbe\xe7\xbd\xae\xe5\x8d\x8a\xe9\x80\x8f\xe6\x98\x8e\xef\xbc\x8c\xe8\xaf\xb7\xe5\xb0\x86g93shader\\head_spline\xe6\x9d\x90\xe8\xb4\xa8\xe6\x94\xb9\xe4\xb8\xbag93shader\\head_spline_alpha\xef\xbc\x8c\xe6\x88\x96\xe5\x9c\xa8163\xe8\xa1\xa8\xe6\xb7\xbb\xe5\x8a\xa0ignore_transparent\xe5\xad\x97\xe6\xae\xb5'.format(model_res.filename))
                global_data.game_mgr.show_tip('\xe6\xa8\xa1\xe5\x9e\x8b{}\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81\xe8\xae\xbe\xe7\xbd\xae\xe5\x8d\x8a\xe9\x80\x8f\xe6\x98\x8e\xef\xbc\x8c\xe8\xaf\xb7\xe5\xb0\x86g93shader\\head_spline\xe6\x9d\x90\xe8\xb4\xa8\xe6\x94\xb9\xe4\xb8\xbag93shader\\head_spline_alpha\xef\xbc\x8c\xe6\x88\x96\xe5\x9c\xa8163\xe8\xa1\xa8\xe6\xb7\xbb\xe5\x8a\xa0ignore_transparent\xe5\xad\x97\xe6\xae\xb5'.format(model_res.filename))
                return True

        return False

    def _set_model_opacity(self, model, opacity):
        if not self._is_enable:
            return
        if model and model.valid:
            if global_data.is_multi_pass_support:
                model.enable_prez_transparent(True, opacity / 255)
                for model_res in self.sd.ref_socket_res_agent.prez_transparent_model_res_list:
                    model_res.enable_prez_transparent(True, opacity / 255)

                for model_res in self.sd.ref_socket_res_agent.alpha_transparent_model_res_list:
                    model_res.alpha = int(opacity)

                self.sd.ref_socket_res_agent.set_sfx_res_alpha_percent(SFX_TRANSPARENT_ALPHA_PERCENT)
            elif global_data.feature_mgr.is_support_ext_tech_fix():
                from logic.gutils.tech_pass_utils import set_prez_transparent
                set_prez_transparent(model, True, int(opacity))
                for model_res in self.sd.ref_socket_res_agent.prez_transparent_model_res_list:
                    set_prez_transparent(model_res, True, int(opacity))

                for model_res in self.sd.ref_socket_res_agent.alpha_transparent_model_res_list:
                    model_res.alpha = int(opacity)

                self.sd.ref_socket_res_agent.set_sfx_res_alpha_percent(SFX_TRANSPARENT_ALPHA_PERCENT)

    def _set_model_opaque(self, model):
        if not self._is_enable:
            return
        if model:
            if global_data.is_multi_pass_support:
                model.all_materials.alpha = 255
                model.enable_prez_transparent(False, 255)
                for model_res in self.sd.ref_socket_res_agent.prez_transparent_model_res_list:
                    model_res.all_materials.alpha = 255
                    model_res.enable_prez_transparent(False, 255)

                for model_res in self.sd.ref_socket_res_agent.alpha_transparent_model_res_list:
                    model_res.alpha = 255

                self.sd.ref_socket_res_agent.set_sfx_res_alpha_percent(1.0)
                self.sd.ref_socket_res_agent.refresh_render_priority()
            elif global_data.feature_mgr.is_support_ext_tech_fix():
                from logic.gutils.tech_pass_utils import set_prez_transparent
                set_prez_transparent(model, False, 255)
                for model_res in self.sd.ref_socket_res_agent.prez_transparent_model_res_list:
                    set_prez_transparent(model_res, False, 255)

                for model_res in self.sd.ref_socket_res_agent.alpha_transparent_model_res_list:
                    model_res.alpha = 255

                self.sd.ref_socket_res_agent.set_sfx_res_alpha_percent(1.0)
                self.sd.ref_socket_res_agent.refresh_render_priority()

    def get_is_model_opacity(self):
        return self._is_in_opacity

    def destroy(self):
        self._is_valid and self.leave_opacity_mode()
        super(ComMechaTransparentModel, self).destroy()