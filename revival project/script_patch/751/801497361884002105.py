# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMechaDisplay.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
import math
import world
import game3d
import math3d
import collision
import render
from . import ScenePart
from common.cfg import confmgr
from common.framework import Functor
from logic.comsys.battle.TeammateWidget.LobbyTeamateMechaTipUI import LobbyTeamateMechaTipUI
from logic.gcommon.common_const.collision_const import MASK_CHARACTER_ROBOT, GROUP_CHARACTER_ROBOT
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID, get_mecha_skin_item_no, get_mecha_model_path, get_mecha_model_h_path, get_mecha_model_lod_path, mecha_lobby_id_2_battle_id, get_mecha_model_offset_y, battle_id_to_mecha_lobby_id
from logic.gutils import mecha_utils
from logic.gutils.mecha_skin_utils import get_mecha_skin_shiny_id, MechaSocketResAgent
from logic.gutils import item_utils
from logic.gcommon.common_utils import decal_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data
from ext_package.ext_decorator import has_skin_ext
from logic.gutils.jump_to_ui_utils import get_jumping_to_skin_define_tag
from logic.gutils import skin_define_utils
EMPTY_SUBMESH_NAME = 'empty'
PRESET_CAM_NAME = 'cam_hangar'
DEFAULT_MECHA_ID = 8001
_HASH_force_sun_shadow = game3d.calc_string_hash('force_sun_shadow')
_HASH_SCAN = game3d.calc_string_hash('t_ScanLineTex_1')
_HASH_SCAN1 = game3d.calc_string_hash('t_ScanLineTex_2')
CHUCHANG_ANIM_UI_MAP = {'RoleInfoUI': 'LotteryMainUI',
   'MechaDetails': 'LotteryMainUI'
   }
MOUNT_ANIM_NAME = {8011: 'j_mount'
   }

class PartMechaDisplay(ScenePart.ScenePart):
    INIT_EVENT = {'player_enter_visit_scene_event': 'on_enter_visit',
       'player_leave_visit_scene_event': 'on_leave_visit',
       'clear_lobby_mecha_display_event': 'on_clear_mecha_display',
       'move_camera_to_display_mecha_position_event': 'move_camera_dis_mecha_position',
       'lobby_mecha_display_reset': 'on_reset_display_model',
       'lobby_cur_display_mecha': 'get_cur_meche',
       'lobby_cur_mecha_id': 'get_cur_meche_id',
       'lobby_cur_mecha_clothing_id': 'get_cur_clothing_id',
       'lobby_cur_mecha_shiny_weapon_id': 'get_cur_meche_shiny_weapon_id',
       'movie_model_anim': 'on_movie_anim',
       'movie_model_hidden': 'on_movie_model_hidden',
       'rotate_mecha_model': 'rotate_mecha',
       'reset_mecha_model_rotate': 'reset_rotate_model',
       'player_add_teammate_mech_event': 'on_player_add_teammate',
       'player_del_teammate_mech_event': 'on_player_del_teammate',
       'player_teammate_mech_update_event': 'on_player_teammate_info_update',
       'player_teammate_mech_clean_event': 'on_player_teammate_info_clean',
       'role_fashion_chagne': 'on_role_fashion_chagne',
       'player_leave_team_event': 'on_player_leave_team',
       'avatar_finish_create_event': 'on_avatar_finish_create',
       'check_mecha_chuchang': 'on_check_mecha_chuchang',
       'reopen_by_mecha_chuchang': 'on_reopen_by_mecha_chuchang',
       'check_reopen_by_mecha_chuchang': 'on_check_reopen_by_mecha_chuchang',
       'refresh_avatar_model_custom_skin': 'on_refresh_avatar_model_custom_skin',
       'display_quality_change': 'on_display_quality_change',
       'set_last_chuchang_id': 'on_set_last_chuchang_id',
       'preview_change_display_model': 'on_preview_change_display_model'
       }

    def __init__(self, scene, name):
        super(PartMechaDisplay, self).__init__(scene, name, True)
        self.empty_model = None
        self.empty_model_socket_res_agent = None
        self.empty_model_hologram = None
        self.empty_model_hologram_socket_res_agent = None
        self.mecha_head_ui = None
        self.cur_mecha_id = None
        self.cur_clothing_id = None
        self.shiny_weapon_id = None
        self._other_index_to_models = {}
        self._other_index_to_model_socket_res_agents = {}
        self._other_mecha_info = {}
        self._other_uid_to_index = {}
        self._other_loading_models = {}
        self.temate_tip_uis = {}
        self.mecha_cols = {}
        self._holo_sub_model_list = []
        self._mecha_view_flag = False
        self.mecha_display_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self.save_cam_transform_mat = math3d.matrix()
        self.cur_euler_rot = math3d.vector(0, 0, 0)
        self.target_euler_rot = math3d.vector(0, 0, 0)
        self.team_leader_info = None
        self.reopen_by_mecha_chuchang_item = None
        self.reopen_by_mecha_chuchang = False
        self.last_chuchang_id = None
        self.last_scene_type = None
        self.avatar_mecha_model = None
        self.avatar_mecha_model_socket_res_agent = None
        self.avatar_mecha_skin_id = None
        self._holo_timer = None
        self._holo_rotate_speed = 0.05
        self.change_model_lock = {}
        self.preview_pose = None
        return

    def _remove_model_and_socket_res_agent(self, model, socket_res_agent):
        if model and model.valid:
            if model is self.avatar_mecha_model:
                self.avatar_mecha_model = None
            global_data.model_mgr.remove_model(model)
        if socket_res_agent:
            if socket_res_agent is self.avatar_mecha_model_socket_res_agent:
                self.avatar_mecha_model_socket_res_agent = None
            socket_res_agent.destroy()
        return

    def on_display_quality_change(self, quality):
        if global_data.is_ue_model:
            mirror_reflect = quality > 1
            if self.empty_model:
                self.empty_model.mirror_reflect = mirror_reflect
            for model in six.itervalues(self._other_index_to_models):
                if model and model.valid:
                    model.mirror_reflect = mirror_reflect

    def on_enter(self):
        if global_data.player is None:
            return
        else:
            ret_dict = global_data.player.get_teammate_mecha_dict()
            mecha_id, clothing_id, shiny_id = self._get_mecha_model_data()
            self.on_change_display_model(mecha_id, clothing_id, shiny_id)
            for uid, teammate_info in six.iteritems(ret_dict):
                mecha_id = teammate_info.get('lobby_mecha_id', 101008001)
                fashion_id = teammate_info.get('lobby_mecha_fashion_id', DEFAULT_CLOTHING_ID)
                team_idx = teammate_info.get('team_idx', -1)
                shiny_weapon_id = teammate_info.get('lobby_mecha_weapon_sfx', -1)
                self.load_other_models(uid, mecha_id, fashion_id, shiny_weapon_id=shiny_weapon_id, team_idx=team_idx)

            return

    def on_exit(self):
        self.del_model()
        self.clean_other_models()

    def on_pause(self, flag):
        if not flag:
            if not global_data.player:
                return
            is_avatar_mecha_model = not global_data.player.is_in_visit_mode() or global_data.player.is_visit_self()
            if is_avatar_mecha_model and not get_jumping_to_skin_define_tag():
                self.on_refresh_avatar_model_custom_skin()

    def on_enter_visit(self, is_visit_self):
        if is_visit_self:
            return
        self.del_model()
        self.clean_other_models()
        self.on_reset_display_model()

    def on_leave_visit(self, *args):
        self.del_model()
        self.clean_other_models()
        self.on_reset_display_model()

    def on_player_join_team(self, team_info, *args):
        self.del_model()
        self.on_reset_display_model()

    def on_player_leave_team(self, *args):
        self.team_leader_info = None
        self.del_model()
        self.clean_other_models()
        self.on_reset_display_model()
        return

    def on_player_add_teammate(self, teammate_info):
        uid = teammate_info['uid']
        team_idx = teammate_info.get('team_idx', -1)
        lobby_mecha_info = teammate_info.get('lobby_mecha_info', {})
        mecha_item_id = lobby_mecha_info.get('lobby_mecha_id', 101008001)
        fashion_id = lobby_mecha_info.get('lobby_mecha_fashion_id', DEFAULT_CLOTHING_ID)
        mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
        shiny_weapon_id = lobby_mecha_info.get('lobby_mecha_weapon_sfx', -1)
        self.load_other_models(uid, mecha_item_id, fashion_id, shiny_weapon_id=shiny_weapon_id, team_idx=team_idx)

    def on_player_del_teammate(self, teammate_uid):
        self.del_other_models(teammate_uid)

    def on_avatar_finish_create(self, *args):
        team_leader_info = self.team_leader_info
        self.team_leader_info = None
        if team_leader_info:
            mecha_id = team_leader_info.get('mecha_id', 0)
            clothing_id = team_leader_info.get('clothing_id', 0)
            shiny_id = team_leader_info.get('shiny_id', -1)
            self.on_change_display_model(mecha_id, clothing_id, shiny_id)
        return

    def on_role_fashion_chagne(self, item_no, fashion_data):
        lobby_item_type = item_utils.get_lobby_item_type(item_no)
        if lobby_item_type != L_ITEM_TYPE_MECHA:
            return
        self.on_reset_display_model()

    def _get_mecha_model_data(self):
        is_in_visit_mode = global_data.player.is_in_visit_mode()
        if not is_in_visit_mode:
            mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
            mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
            clothing_id = global_data.player.get_mecha_fashion(mecha_item_id)
            skin_item_id = get_mecha_skin_item_no(mecha_id, clothing_id)
            shiny_id = get_mecha_skin_shiny_id(skin_item_id)
            self.first_pos_decal_data = global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_item_id)), [])
            self.first_pos_color_data = global_data.player.get_mecha_color().get(str(skin_item_id), {})
            self.first_pos_pose_data = global_data.player.get_mecha_pose()
        else:
            mecha_item_id = global_data.player.get_visit_mecha_id()
            mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
            clothing_id = global_data.player.get_visit_mecha_fashion(mecha_item_id)
            shiny_id = global_data.player.get_visit_mecha_shiny_weapon_id(mecha_item_id)
            info = global_data.player.get_visit_mecha_info()
            if not has_skin_ext():
                custom_skin_data = {}
            else:
                custom_skin_data = info.get('lobby_mecha_custom_skin', {})
            self.first_pos_decal_data = custom_skin_data.get('decal', [])
            self.first_pos_color_data = custom_skin_data.get('color', {})
            self.first_pos_pose_data = info.get('lobby_mecha_pose', {})
        return (
         mecha_id, clothing_id, shiny_id)

    def on_reset_display_model(self, force_refresh=False):
        from logic.gcommon.common_const import scene_const
        if global_data.game_mgr.scene.scene_type != scene_const.SCENE_LOBBY:
            return
        else:
            if global_data.player is None:
                return
            mecha_id, clothing_id, shiny_id = self._get_mecha_model_data()
            self.on_change_display_model(mecha_id, clothing_id, shiny_id, force_refresh)
            return

    def on_clear_mecha_display(self):
        self.del_model()
        self.cur_mecha_id = None
        self.cur_clothing_id = None
        self.shiny_weapon_id = None
        return

    def move_camera_dis_mecha_position(self):
        scn = self.get_scene()
        if not scn:
            return
        import math
        m = scn.get_model('box_mecha')
        if not m:
            return
        if m.visible:
            m.visible = False
        global_data.emgr.set_fixed_point_camera_event.emit({'position': [m.position.x, m.position.y + 30, m.position.z],'rotation': [
                      0, math.degrees(0.936108827591), 0]
           })

    def get_main_pos_uid(self):
        player = global_data.player
        if not player:
            return
        uid = player.get_visit_uid()
        if not uid and player.is_in_team():
            uid = player.uid
        else:
            uid = player.uid
        return uid

    def on_preview_change_display_model(self, mecha_id=None, clothing_id=None, pose=None):
        self.preview_pose = pose
        if 'preview' in self.change_model_lock:
            del self.change_model_lock['preview']
        if mecha_id and clothing_id:
            self.on_change_display_model(mecha_id, clothing_id, force_refresh=True)
            self.change_model_lock['preview'] = True
        else:
            self.on_reset_display_model()

    def on_change_display_model(self, mecha_id, clothing_id, shiny_id=-1, force_refresh=False):
        if self.change_model_lock:
            return
        else:
            if global_data.player is None:
                self.team_leader_info = {'mecha_id': mecha_id,'clothing_id': clothing_id,'shiny_id': shiny_id}
                return
            if str(mecha_id) not in self.mecha_display_conf:
                return
            if not force_refresh and self.cur_mecha_id and str(self.cur_mecha_id) == str(mecha_id) and self.cur_clothing_id == clothing_id and shiny_id == self.shiny_weapon_id:
                return
            self.del_model()
            self.cur_mecha_id = mecha_id
            self.cur_clothing_id = clothing_id
            self.shiny_weapon_id = shiny_id
            main_pos_uid = self.get_main_pos_uid()
            res_path = get_mecha_model_path(mecha_id, clothing_id)
            item_id = get_mecha_skin_item_no(self.cur_mecha_id, self.cur_clothing_id)
            is_avatar_mecha_model = not global_data.player.is_in_visit_mode() or global_data.player.is_visit_self()
            data = {'item_id': item_id,
               'owner_key': (
                           main_pos_uid, self.cur_mecha_id, self.cur_clothing_id),
               'skin_id': self.cur_clothing_id,
               'shiny_weapon_id': shiny_id,
               'is_avatar_mecha_model': is_avatar_mecha_model,
               'mecha_id': mecha_id,
               'decal_data': self.first_pos_decal_data,
               'color_data': self.first_pos_color_data
               }
            mesh_path = get_mecha_model_h_path(self.cur_mecha_id, self.cur_clothing_id, shiny_weapon_id=shiny_id)
            global_data.model_mgr.create_model(res_path, mesh_path_list=[mesh_path], on_create_func=Functor(self.on_load_first_pos_model_complete, data))
            holo_path = get_mecha_model_lod_path(self.cur_mecha_id, self.cur_clothing_id, 1)
            global_data.model_mgr.create_model(res_path, mesh_path_list=[holo_path], on_create_func=Functor(self.on_load_first_pos_model_hologram_complete, data))
            return

    def del_model(self):
        if self.mecha_head_ui:
            self.mecha_head_ui.destroy()
            self.mecha_head_ui = None
        if self.empty_model:
            global_data.model_mgr.remove_model(self.empty_model)
            self.empty_model = None
        if self.empty_model_socket_res_agent:
            self.empty_model_socket_res_agent.destroy()
            self.empty_model_socket_res_agent = None
        if self.empty_model_hologram:
            self._holo_sub_model_list = []
            global_data.model_mgr.remove_model(self.empty_model_hologram)
            self.empty_model_hologram = None
        if self.empty_model_hologram_socket_res_agent:
            self.empty_model_hologram_socket_res_agent.destroy()
            self.empty_model_hologram_socket_res_agent = None
        self.avatar_mecha_model = None
        self.avatar_mecha_model_socket_res_agent = None
        self.cur_mecha_id = None
        self.cur_clothing_id = None
        self.clear_holo_timer()
        return

    def on_load_first_pos_model_complete(self, data, model, *args):
        scn = self.get_scene()
        if not scn:
            global_data.model_mgr.remove_model(model)
            return
        else:
            m = scn.get_model('box_mecha')
            if not m:
                global_data.model_mgr.remove_model(model)
                return
            if m.visible:
                m.visible = False
            main_pos_uid = self.get_main_pos_uid()
            cur_owner_key = (main_pos_uid, self.cur_mecha_id, self.cur_clothing_id)
            load_owner_key = data['owner_key']
            if load_owner_key != cur_owner_key:
                global_data.model_mgr.remove_model(model)
                return
            self._remove_model_and_socket_res_agent(self.empty_model, self.empty_model_socket_res_agent)
            self.empty_model_socket_res_agent = None
            self.del_mecha_col(0)
            self.empty_model = model
            scn.add_object(model)
            model_offset_y = get_mecha_model_offset_y(self.cur_clothing_id)
            position = math3d.vector(m.position)
            position.y = position.y + model_offset_y
            model.world_position = position
            model.cast_shadow = True
            model.receive_shadow = True
            if global_data.is_ue_model:
                model.mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1
            model.all_materials.enable_write_alpha = False
            model.set_rendergroup_and_priority(world.RENDER_GROUP_ALPHATEST, 0)
            skin_id = data.get('skin_id', None)
            if skin_id:
                shiny_weapon_id = data.get('shiny_weapon_id', -1)
                self.empty_model_socket_res_agent = MechaSocketResAgent()
                self.empty_model_socket_res_agent.load_skin_model_and_effect(self.empty_model, skin_id, shiny_weapon_id)
            self.on_load_model_complete(data)
            self.load_decal_data(model, data['item_id'], data['decal_data'])
            self.load_color_data(model, data['item_id'], data['color_data'])
            model.all_materials.set_macro('TOP_LIGHT_ENABLE', 'TRUE')
            model.all_materials.set_macro('BACK_LIGHT_ENABLE', 'TRUE')
            model.all_materials.rebuild_tech()
            if data['is_avatar_mecha_model']:
                self.avatar_mecha_model = self.empty_model
                self.avatar_mecha_model_socket_res_agent = self.empty_model_socket_res_agent
                self.avatar_mecha_skin_id = data['item_id']
            global_data.emgr.lobby_mecha_model_changed.emit()
            global_data.emgr.show_lobby_mecha_model.emit(main_pos_uid, model)
            is_avatar_mecha_model = not global_data.player.is_in_visit_mode() or global_data.player.is_visit_self()
            if is_avatar_mecha_model:
                self.on_refresh_avatar_model_custom_skin()
            return

    def on_load_first_pos_model_hologram_complete(self, data, model, *args):
        scn = self.get_scene()
        if not scn:
            global_data.model_mgr.remove_model(model)
            return
        else:
            main_pos_uid = self.get_main_pos_uid()
            cur_owner_key = (main_pos_uid, self.cur_mecha_id, self.cur_clothing_id)
            load_owner_key = data['owner_key']
            if load_owner_key != cur_owner_key:
                global_data.model_mgr.remove_model(model)
                return
            self._remove_model_and_socket_res_agent(self.empty_model_hologram, self.empty_model_hologram_socket_res_agent)
            self.empty_model_hologram_socket_res_agent = None
            self.empty_model_hologram = model
            scn.add_object(model)
            model.world_position = math3d.vector(-152.91, 42.07, -438.22)
            model.scale = math3d.vector(0.5, 0.5, 0.5)
            mecha_utils.check_need_flip(model)
            model.all_materials.enable_write_alpha = False
            skin_id = data.get('skin_id', None)
            if skin_id:
                shiny_weapon_id = data.get('shiny_weapon_id', -1)
                self.empty_model_hologram_socket_res_agent = MechaSocketResAgent()
                self.empty_model_hologram_socket_res_agent.load_skin_model_and_effect(self.empty_model_hologram, skin_id, shiny_weapon_id, is_hologram=True)
                self._holo_sub_model_list.extend(self.empty_model_hologram_socket_res_agent.model_res_list)
            self.on_load_hologram_complete(data)
            tex = render.texture('effect/textures/alpha/blur_one_sided.png', False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)
            tex1 = render.texture('effect/textures/alpha/blur1.png', False, False, render.TEXTURE_TYPE_UNKNOWN, game3d.ASYNC_NONE)

            def set_holo_tech--- This code section failed: ---

 508       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'get'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 509      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 510      16  LOAD_DEREF            0  'data'
          19  LOAD_ATTR             1  'get'
          22  LOAD_CONST            2  'skin_id'
          25  LOAD_CONST            0  ''
          28  CALL_FUNCTION_2       2 
          31  LOAD_CONST           13  (201800653, 201801651, 201801652, 201801653)
          34  COMPARE_OP            6  'in'
          37  POP_JUMP_IF_FALSE    70  'to 70'

 512      40  LOAD_CONST            7  50
          43  LOAD_FAST             0  'model'
          46  LOAD_ATTR             3  'all_materials'
          49  STORE_ATTR            4  'alpha'

 513      52  LOAD_GLOBAL           5  'render'
          55  LOAD_ATTR             6  'TRANSPARENT_MODE_BLEND_ADD'
          58  LOAD_FAST             0  'model'
          61  LOAD_ATTR             3  'all_materials'
          64  STORE_ATTR            7  'transparent_mode'
          67  JUMP_FORWARD         27  'to 97'

 515      70  LOAD_CONST            8  200
          73  LOAD_FAST             0  'model'
          76  LOAD_ATTR             3  'all_materials'
          79  STORE_ATTR            4  'alpha'

 516      82  LOAD_GLOBAL           5  'render'
          85  LOAD_ATTR             8  'TRANSPARENT_MODE_ALPHA_R_Z'
          88  LOAD_FAST             0  'model'
          91  LOAD_ATTR             3  'all_materials'
          94  STORE_ATTR            7  'transparent_mode'
        97_0  COME_FROM                '67'

 517      97  LOAD_FAST             0  'model'
         100  LOAD_ATTR             3  'all_materials'
         103  LOAD_ATTR             9  'set_technique'
         106  LOAD_CONST            9  1
         109  LOAD_CONST           10  'shader/vfx_mecha_hologram.nfx::TShader'
         112  CALL_FUNCTION_2       2 
         115  POP_TOP          

 518     116  LOAD_FAST             0  'model'
         119  LOAD_ATTR             3  'all_materials'
         122  LOAD_ATTR            10  'set_texture'
         125  LOAD_GLOBAL          11  '_HASH_SCAN'
         128  LOAD_CONST           11  't_ScanLineTex_1'
         131  LOAD_DEREF            1  'tex'
         134  CALL_FUNCTION_3       3 
         137  POP_TOP          

 519     138  LOAD_FAST             0  'model'
         141  LOAD_ATTR             3  'all_materials'
         144  LOAD_ATTR            10  'set_texture'
         147  LOAD_GLOBAL          12  '_HASH_SCAN1'
         150  LOAD_CONST           12  't_ScanLineTex_2'
         153  LOAD_DEREF            2  'tex1'
         156  CALL_FUNCTION_3       3 
         159  POP_TOP          

 520     160  LOAD_FAST             0  'model'
         163  LOAD_ATTR             3  'all_materials'
         166  LOAD_ATTR            13  'rebuild_tech'
         169  CALL_FUNCTION_0       0 
         172  POP_TOP          
         173  LOAD_CONST            0  ''
         176  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

            mode_list = [
             model]
            mode_list.extend(self._holo_sub_model_list)
            for model in mode_list:
                set_holo_tech(model)

            def rotate_model():
                if self.empty_model_hologram and self.empty_model_hologram.valid:
                    self.empty_model_hologram.rotate_y(0.1 * self._holo_rotate_speed)

            self.clear_holo_timer()
            self._holo_timer = global_data.game_mgr.get_logic_timer().register(func=rotate_model)
            return

    def load_decal_data(self, model, skin_id, decal_list):
        if decal_list and len(decal_list[0]) < 9:
            decal_list = decal_utils.decode_decal_list(decal_list)
        load_model_decal_data(model, skin_id, decal_list, lod_level=0, create_high_quality_decal=True)

    def load_color_data(self, model, skin_id, color_dict):
        if color_dict and isinstance(color_dict, dict):
            color_dict = decal_utils.decode_color(color_dict)
        load_model_color_data(model, skin_id, color_dict)

    def on_load_model_complete(self, data, *args):
        self.empty_model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        player = global_data.player
        if not player:
            return
        else:
            uid = player.get_visit_uid()
            if not uid and player.is_in_team():
                uid = player.uid
            if self.mecha_head_ui:
                self.mecha_head_ui.destroy()
                self.mecha_head_ui = None
            if uid:
                self.mecha_head_ui = self.create_teammate_tip_ui(uid, self.empty_model)
            item_id = data['item_id']
            if self.preview_pose:
                pose = self.preview_pose
            else:
                pose = self.first_pos_pose_data.get(str(battle_id_to_mecha_lobby_id(data['mecha_id'])), None)
            anim_name = item_utils.get_lobby_item_res_path(pose, skin_id=get_main_skin_id(item_id)) if pose else self.get_play_idle_anim(item_id)
            anim_args = self.get_animate_args(pose, anim_name)

            def end_show_anim(*args):
                if self.empty_model:
                    self.empty_model.unregister_event(end_show_anim, 'end', anim_name)
                    self.add_mecha_col(0, self.empty_model, data['owner_key'][1])

            self.empty_model.register_anim_key_event(anim_name, 'end', end_show_anim)
            if self.empty_model_socket_res_agent:
                self.empty_model_socket_res_agent.play_animation(*anim_args)
            else:
                self.empty_model.play_animation(*anim_args)
            self.empty_model.all_materials.set_var(_HASH_force_sun_shadow, 'force_sun_shadow', 1.0)
            scn = self.get_scene()
            if scn and scn == world.get_active_scene():
                sfx_pos = math3d.vector(self.empty_model.position.x, self.empty_model.position.y - self.empty_model.bounding_box.y / 2.0, self.empty_model.position.z)
                sfx_path = 'effect/fx/robot/common/mecha_call_down.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_pos)
            self.reset_rotate_model()
            mecha_utils.check_need_scale(self.empty_model, self.cur_mecha_id, self.cur_clothing_id)
            mecha_utils.check_need_flip(self.empty_model)
            self.empty_model_socket_res_agent.set_scale(self.empty_model.scale.z)
            return

    def on_load_hologram_complete(self, data, *args):
        self.empty_model_hologram.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        player = global_data.player
        if not player:
            return
        else:
            item_id = data['item_id']
            if self.preview_pose:
                pose = self.preview_pose
            else:
                pose = self.first_pos_pose_data.get(str(battle_id_to_mecha_lobby_id(data['mecha_id'])), None)
            anim_name = item_utils.get_lobby_item_res_path(pose, skin_id=get_main_skin_id(item_id)) if pose else self.get_play_idle_anim(item_id)
            anim_args = self.get_animate_args(pose, anim_name)
            if self.empty_model_hologram_socket_res_agent:
                self.empty_model_hologram_socket_res_agent.play_animation(*anim_args)
            else:
                self.empty_model.play_animation(*anim_args)
            self.empty_model_hologram.all_materials.set_var(_HASH_force_sun_shadow, 'force_sun_shadow', 1.0)
            return

    def clean_other_models(self):
        all_uids = six_ex.keys(self._other_uid_to_index)
        for uid in all_uids:
            self.del_other_models(uid)

    def _del_other_model_by_index(self, index):
        model = self._other_index_to_models.get(index, None)
        socket_res_agent = self._other_index_to_model_socket_res_agents.get(index, None)
        self._remove_model_and_socket_res_agent(model, socket_res_agent)
        self._other_index_to_models[index] = None
        self._other_index_to_model_socket_res_agents[index] = None
        return

    def del_other_models(self, uid, del_col=True, team_idx=-1):
        ret, index = self.find_other_models(uid, team_idx)
        self._other_mecha_info.pop(uid, None)
        loading_model_id = self._other_loading_models.pop(index, {}).get('model_id', None)
        if loading_model_id:
            self._other_uid_to_index.pop(uid, None)
            global_data.model_mgr.remove_model_by_id(loading_model_id)
            return (
             ret, index)
        else:
            box_name = 'box_mecha_0%d' % index
            scn = self.get_scene()
            if scn:
                m = scn.get_model(box_name)
                if m:
                    m.active_collision = False
            if not ret:
                return (ret, index)
            self.del_teammate_tip_ui(uid)
            self._del_other_model_by_index(index)
            self._other_uid_to_index.pop(uid, None)
            if del_col:
                self.del_mecha_col(index)
            global_data.emgr.show_lobby_mecha_model.emit(uid, None)
            return (
             ret, index)

    def load_other_models(self, uid, mecha_item_id, clothing_id, shiny_weapon_id=-1, team_idx=-1):
        ret_dict = global_data.player.get_teammate_mecha_dict()
        if not has_skin_ext():
            clothing_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_item_id), 'default_fashion')[0]
            shiny_weapon_id = -1
            ret_dict = {}
        custom_skin_data = {}
        custom_pose = {}
        if uid in ret_dict:
            custom_skin_data = ret_dict[uid].get('lobby_mecha_custom_skin', {})
            custom_pose = ret_dict[uid].get('lobby_mecha_pose', {})
        mecha_info = (mecha_item_id, clothing_id, shiny_weapon_id, team_idx, custom_skin_data, custom_pose)
        if self._other_mecha_info.get(uid, None) == mecha_info:
            return
        else:
            mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
            ret, index = self.del_other_models(uid, team_idx=team_idx, del_col=True)
            self._other_uid_to_index[uid] = index
            self._del_other_model_by_index(index)
            self._other_mecha_info[uid] = mecha_info
            res_path = get_mecha_model_path(mecha_id, clothing_id)
            data = {'index': index,'mecha_id': mecha_id,'clothing_id': clothing_id,'shiny_weapon_id': shiny_weapon_id,'uid': uid}
            data.update({'custom_skin_data': custom_skin_data,'custom_pose': custom_pose})
            mesh_path = get_mecha_model_h_path(mecha_id, clothing_id, shiny_weapon_id=shiny_weapon_id)
            self._other_loading_models[index] = ex_data = {}
            model_id = global_data.model_mgr.create_model(res_path, mesh_path_list=[mesh_path], on_create_func=Functor(self.on_load_other_models_complete, data), ex_data=ex_data)
            return

    def on_load_other_models_complete(self, data, model, *args):
        index = data['index']
        loading_model_id = self._other_loading_models.get(index, {}).get('model_id', None)
        model_id = global_data.model_mgr.get_model_id(model)
        if model_id != loading_model_id:
            global_data.model_mgr.remove_model(model)
            return
        else:
            self._other_loading_models.pop(index, None)
            uid = data['uid']
            mecha_id = data['mecha_id']
            clothing_id = data['clothing_id']
            shiny_weapon_id = data['shiny_weapon_id']
            custom_skin_data = data['custom_skin_data']
            custom_pose = data['custom_pose']
            index = self._other_uid_to_index.get(uid, -1)
            if index < 0 or not global_data.player:
                global_data.model_mgr.remove_model(model)
                return
            scn = self.get_scene()
            if not scn:
                global_data.model_mgr.remove_model(model)
                return
            box_name = 'box_mecha_0%d' % index
            m = scn.get_model(box_name)
            if not m:
                global_data.model_mgr.remove_model(model)
                return
            scn.add_object(model)
            model_offset_y = get_mecha_model_offset_y(clothing_id)
            position = math3d.vector(m.position)
            position.y = position.y + model_offset_y
            model.world_position = position
            self._del_other_model_by_index(index)
            self._other_index_to_models[index] = model
            self.add_teammate_tip_ui(uid, model)
            socket_res_agent = MechaSocketResAgent()
            self._other_index_to_model_socket_res_agents[index] = socket_res_agent
            socket_res_agent.load_skin_model_and_effect(model, clothing_id, shiny_weapon_id)
            model.all_materials.set_var(_HASH_force_sun_shadow, 'force_sun_shadow', 1.0)
            model.rotation_matrix = math3d.euler_to_matrix(self.get_model_euler_rotate(index))
            model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
            item_id = get_mecha_skin_item_no(data['mecha_id'], data['clothing_id'])
            pose = custom_pose.get(str(battle_id_to_mecha_lobby_id(mecha_id)), None)
            anim_name = item_utils.get_lobby_item_res_path(pose, skin_id=get_main_skin_id(item_id)) if pose else self.get_play_idle_anim(item_id)

            def end_show_anim(*args):
                model.unregister_event(end_show_anim, 'end', anim_name)
                self.add_mecha_col(index, model, mecha_id)

            model.register_anim_key_event(anim_name, 'end', end_show_anim)
            if global_data.is_ue_model:
                model.mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1
            model.all_materials.enable_write_alpha = False
            model.set_rendergroup_and_priority(world.RENDER_GROUP_ALPHATEST, 0)
            mecha_utils.check_need_flip(model)
            self.load_decal_data(model, clothing_id, custom_skin_data.get('decal', []))
            self.load_color_data(model, clothing_id, custom_skin_data.get('color', {}))
            if global_data.player and uid == global_data.player.uid:
                self.avatar_mecha_model = model
                self.avatar_mecha_model_socket_res_agent = socket_res_agent
                self.avatar_mecha_skin_id = clothing_id
            global_data.emgr.show_lobby_mecha_model.emit(uid, model)
            anim_args = self.get_animate_args(pose, anim_name)
            socket_res_agent.play_animation(*anim_args)
            return

    def get_play_idle_anim(self, item_id):
        item_conf = confmgr.get('lobby_item', str(item_id), default={})
        lobby_ani_name = item_conf.get('lobby_ani_name', [])
        return lobby_ani_name or 'shutdown_01'

    def del_teammate_tip_ui(self, uid):
        teammate_tip_ui = self.temate_tip_uis.get(uid, None)
        if teammate_tip_ui:
            teammate_tip_ui.destroy()
            del self.temate_tip_uis[uid]
        return

    def create_teammate_tip_ui(self, uid, model):
        nd = global_data.uisystem.load_template_create('lobby/teamate_mecha_tip')
        teammate_tip_ui = LobbyTeamateMechaTipUI(nd, uid, model)
        teammate_tip_ui.show()
        return teammate_tip_ui

    def add_teammate_tip_ui(self, uid, model):
        self.del_teammate_tip_ui(uid)
        self.temate_tip_uis[uid] = self.create_teammate_tip_ui(uid, model)

    def rotate_mecha(self, rotate_times):
        self.target_euler_rot = math3d.vector(0, self.target_euler_rot.y + rotate_times * math.pi * 2, 0)

    def get_model(self):
        if self.empty_model and self.empty_model.valid:
            return self.empty_model
        else:
            return None

    def reset_rotate_model(self):
        if not self.empty_model:
            return
        if self._mecha_view_flag:
            self.cur_euler_rot = math3d.vector(0, 0, 0)
            self.target_euler_rot = math3d.vector(self.cur_euler_rot.x, self.cur_euler_rot.y, self.cur_euler_rot.z)
            self.empty_model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, 0, 0))
        else:
            self.cur_euler_rot = self.get_model_euler_rotate(0)
            self.target_euler_rot = math3d.vector(self.cur_euler_rot.x, self.cur_euler_rot.y, self.cur_euler_rot.z)
            self.empty_model.rotation_matrix = math3d.euler_to_matrix(self.cur_euler_rot)

    def add_mecha_col(self, index, model, mecha_id):
        scn = self.get_scene()
        if not scn:
            return
        if index not in self.mecha_cols:
            fix_scale = 0.7
            if mecha_id in (8008, 8009, 8011, 8012):
                fix_scale = 1.0
            col = collision.col_object(collision.CAPSULE, model.bounding_box * fix_scale)
            col.mask = MASK_CHARACTER_ROBOT
            col.group = GROUP_CHARACTER_ROBOT
            scn.scene_col.add_object(col)
            col.position = model.world_position
            self.mecha_cols[index] = col

    def del_mecha_col(self, index):
        if index not in self.mecha_cols:
            return
        scn = self.get_scene()
        if not scn:
            return
        scn.scene_col.remove_object(self.mecha_cols[index])
        del self.mecha_cols[index]

    def get_model_euler_rotate(self, index):
        euler_rot = math3d.vector(0, confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'mecha%d' % index, 'yaw'), 0)
        return euler_rot

    def get_cur_meche(self):
        return self.empty_model

    def get_cur_meche_id(self):
        return self.cur_mecha_id or 8001

    def get_cur_clothing_id(self):
        return self.cur_clothing_id or 0

    def get_cur_meche_shiny_weapon_id(self):
        return self.shiny_weapon_id or 0

    def on_movie_anim(self, parameter):
        if parameter.get('tag', '') == 'lobby_mecha' and self.empty_model:
            self._mecha_view_flag = True
            self.reset_rotate_model()
            anim_name = parameter['anim_name']
            if anim_name == 'mount':
                anim_name = MOUNT_ANIM_NAME.get(self.get_cur_meche_id(), anim_name)
            if self.empty_model_socket_res_agent:
                self.empty_model_socket_res_agent.play_animation(anim_name)
            else:
                self.empty_model.play_animation(anim_name)

    def on_movie_model_hidden(self, parameter):
        if parameter.get('tag', '') == 'lobby_mecha' and self.empty_model:
            self.empty_model.visible = False

    def find_other_models(self, uid, team_idx=-1):
        if uid in self._other_uid_to_index:
            return (
             True, self._other_uid_to_index[uid])
        else:
            is_in_visit_mode = global_data.player.is_visit_others()
            if is_in_visit_mode:
                owner_idx = global_data.player.get_visit_admin_team_idx()
            else:
                owner_idx = global_data.player.get_team_idx()
            if owner_idx is not None and team_idx < owner_idx:
                return (False, team_idx + 1)
            return (
             False, team_idx)
            return

    def on_player_teammate_info_update(self, uid, updated_uinfo):
        if not global_data.player:
            return
        if uid == global_data.player.get_visit_uid():
            return
        team_idx = updated_uinfo.get('team_idx', -1)
        lobby_mecha_info = updated_uinfo.get('lobby_mecha_info', {})
        mecha_id = lobby_mecha_info.get('lobby_mecha_id', 101008001)
        fashion_id = lobby_mecha_info.get('lobby_mecha_fashion_id', DEFAULT_CLOTHING_ID)
        shiny_weapon_id = lobby_mecha_info.get('lobby_mecha_weapon_sfx', -1)
        self.load_other_models(uid, mecha_id, fashion_id, shiny_weapon_id=shiny_weapon_id, team_idx=team_idx)

    def on_player_teammate_info_clean(self):
        self.clean_other_models()

    def on_update(self, dt):
        if self.empty_model and self._mecha_view_flag:
            self.cur_euler_rot.intrp(self.cur_euler_rot, self.target_euler_rot, 0.2)
            self.empty_model.rotation_matrix = math3d.euler_to_matrix(self.cur_euler_rot)

    def on_set_last_chuchang_id(self, id):
        self.last_chuchang_id = id

    def on_check_mecha_chuchang(self, clothing_id, ui_name, force_show_chuchang=False):
        result = global_data.emgr.is_forbid_mecha_chuchang_scene.emit()
        if result and result[0]:
            return False
        else:
            if clothing_id == self.last_chuchang_id and not force_show_chuchang:
                return False
            self.last_chuchang_id = clothing_id
            item_type = item_utils.get_lobby_item_type(clothing_id)
            cur_skin_cnf = None
            if item_type == L_ITEM_TYPE_MECHA_SKIN:
                cur_skin_cnf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
            else:
                if item_type == L_ITEM_TYPE_ROLE_SKIN:
                    cur_skin_cnf = confmgr.get('role_info', 'RoleSkin', 'Content', str(clothing_id))
                if cur_skin_cnf and cur_skin_cnf.get('chuchang_anim'):
                    global_data.emgr.show_mecha_chuchang_scene.emit(clothing_id, belong_ui_name=ui_name)
                    return True
            return False

    def on_reopen_by_mecha_chuchang(self, mecha_skin_id):
        self.reopen_by_mecha_chuchang_item = mecha_skin_id
        self.reopen_by_mecha_chuchang = True

    def on_check_reopen_by_mecha_chuchang(self, id):
        if self.reopen_by_mecha_chuchang:
            self.reopen_by_mecha_chuchang = False
            return id == self.reopen_by_mecha_chuchang_item
        return False

    def hide_all_teammate_tip_ui(self):
        if self.temate_tip_uis:
            for uid, tip_ui in six.iteritems(self.temate_tip_uis):
                tip_ui and tip_ui.hide()

        self.mecha_head_ui and self.mecha_head_ui.hide()
        return False

    def on_refresh_avatar_model_custom_skin(self):
        if self.change_model_lock:
            return
        else:
            if not global_data.player:
                return
            if self.avatar_mecha_model and self.avatar_mecha_model.valid:
                skin_id = self.avatar_mecha_skin_id
                self.load_decal_data(self.avatar_mecha_model, skin_id, global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), []))
                self.load_color_data(self.avatar_mecha_model, skin_id, global_data.player.get_mecha_color().get(str(skin_id), {}))
                mecha_id = item_utils.get_lobby_item_belong_no(self.avatar_mecha_skin_id)
                pose = global_data.player.get_mecha_pose().get(str(mecha_id), None)
                anim_name = item_utils.get_lobby_item_res_path(pose, skin_id=get_main_skin_id(self.avatar_mecha_skin_id)) if pose else self.get_play_idle_anim(self.avatar_mecha_skin_id)
                anim_args = self.get_animate_args(pose, anim_name)
                if self.avatar_mecha_model_socket_res_agent:
                    self.avatar_mecha_model_socket_res_agent.play_animation(*anim_args)
                else:
                    self.avatar_mecha_model.play_animation(*anim_args)
                if self.empty_model_hologram:
                    if self.empty_model_hologram_socket_res_agent:
                        self.empty_model_hologram_socket_res_agent.play_animation(*anim_args)
                    else:
                        self.empty_model_hologram.play_animation(*anim_args)
            return

    def clear_holo_timer(self):
        if self._holo_timer:
            global_data.game_mgr.unregister_logic_timer(self._holo_timer)
            self._holo_timer = None
        return

    def get_animate_args(self, mecha_pose, anim_name):
        is_gesture_pose = skin_define_utils.is_mecha_gesture_pose(mecha_pose)
        loop = world.PLAY_FLAG_LOOP if is_gesture_pose else world.PLAY_FLAG_NO_LOOP
        return [
         anim_name, 0, -1, 0, loop, 1.0]