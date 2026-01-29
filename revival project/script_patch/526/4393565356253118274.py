# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComLobbyModel.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.gcommon.common_const import lobby_ani_const
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import DEFAULT_ROLE_ID
from common.algorithm import resloader
from logic.gutils import dress_utils
from common.animate import animator
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST, FASHION_POS_WEAPON_SFX
from logic.gutils.role_skin_utils import load_improved_skin_model_and_effect, get_improve_skin_body_path, load_normal_skin_model_and_effect, clear_role_skin_model_and_effect
import game3d
import world
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE
from common.cfg import confmgr
import math3d
from common.utils import pc_platform_utils
from common.utils.timer import CLOCK, RELEASE
import random
from logic.gcommon.component.client.com_human_appearance.ComLodHuman import TRANSPARENT_SUBMESH_RENDER_PRIORITY
PENDANT_BUG_LIST = {'201001154': ('weiba_11_2005', ),
   '201001741': ('guashi_17', ),
   '201011153': ('hair_99', ),
   '201001564': ('hudiejie_15_2014', 'pugongying', 'hair_15_2014'),
   '201001565': ('hudiejie_15_2014', 'pugongying', 'hair_15_2014'),
   '201001566': ('hudiejie_15_2014', 'pugongying', 'hair_15_2014')
   }
BLEND_MOVE_FIX = [
 '_bl', '_fl', '_b', '_f', '_br', '_fr']
BLEND_MOVE_NODE = ['src_move_bl', 'src_move_fl', 'src_move_b', 'src_move_f', 'src_move_br', 'src_move_fr']

class ComLobbyModel(UnitCom):
    SCENE_TYPE = [
     'Lobby', 'PVELobby']
    BIND_EVENT = {'E_POSITION': 'on_pos_changed',
       'G_POSITION': 'get_pos',
       'E_SET_ROTATION_MATRIX': 'on_set_rotation_matrix',
       'G_MODEL': '_get_model',
       'E_MODEL_VISIBLE': 'set_model_visible',
       'G_MODEL_POSITION': 'get_model_position',
       'E_SET_MODEL_VISIBLE': 'set_model_visible',
       'E_CHARACTER_ATTR': 'change_character_attr',
       'E_REFRESH_LOBBY_PLAYER_MODEL': 'on_refresh_player_model',
       'E_ON_LOBBYPUPPET_DATA_CHANGE': 'on_refresh_player_model',
       'G_MOUNTING': 'is_mounting',
       'G_ANIMATOR': '_get_animator',
       'E_SET_ANIMATOR_INT_STATE': 'set_ani_int_state',
       'E_SET_ANIMATOR_FLOAT_STATE': 'set_ani_float_state',
       'G_MODEL_YAW': 'get_yaw',
       'E_REGISTER_ANIM_ACTIVE': '_register_active_event',
       'E_UNREGISTER_ANIM_ACTIVE': '_unregister_active_event',
       'E_REGISTER_ANIM_STATE_EXIT': '_register_state_exit_event',
       'E_UNREGISTER_ANIM_STATE_EXIT': '_unregister_state_exit_event',
       'E_REGISTER_CHANGE_CLIP_EVENT': '_register_change_clip_event'
       }

    def __init__(self):
        super(ComLobbyModel, self).__init__(True)
        self._role_id = DEFAULT_ROLE_ID
        self.dressed_clothing_id = None
        self.suit_id = None
        self.model_id = None
        self.head_id = None
        self.bag_id = None
        self.model = None
        self._animator = None
        self.sd.ref_animator_mirror = None
        self.mirror_model = None
        self.mirror_model_id = None
        self._model_visible = False
        self.improved_skin_sfx_id = None
        self.ready_for_improved_skin_flags = {}
        self.can_load_improved_skin_res = {}
        self._free_dir_x = 0
        self._free_dir_y = 1
        self._active_event = {}
        self._state_exit_event = {}
        self._flag_delay_refresh = False
        self.pendant_socket_name = None
        self.head_model_path = None
        self.head_pendant_type = None
        self.pendant_socket_res_path = None
        self.head_pendant_l_same_gis = None
        self.pendant_random_anim_list = None
        self.bag_pendant_l_same_gis = None
        self.bag_socket_name = None
        self.bag_model_path = None
        self.bag_socket_name2 = None
        self.bag_model_path2 = None
        self.pendant_data_list = None
        self.other_pendant_list = None
        self.head_pendant_random_anim_timer = None
        self.head_pendant_anim_index = 0
        self.head_pendant_model = None
        self.process_event(True)
        self.load_model_idx = 0
        return

    def process_event(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'display_quality_change': self.on_display_quality_change
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def tick(self, dt):
        if not self.model_id:
            if self.check_scene() and global_data.player:
                self.load_model()
                if self.model_id:
                    self.need_update = False

    def check_scene(self):
        scene = world.get_active_scene()
        if scene.scene_type not in self.SCENE_TYPE:
            return False
        return True

    def _get_animator(self):
        return self._animator

    @property
    def model_visible(self):
        return self._model_visible

    @model_visible.setter
    def model_visible(self, visible):
        self._model_visible = visible
        model = self._get_model()
        if model:
            model.visible = visible

    def set_model_visible(self, flag):
        self.model_visible = flag

    def get_model_position(self):
        model = self._get_model()
        if model:
            return model.world_position

    def init_from_dict(self, unit_obj, bdict):
        super(ComLobbyModel, self).init_from_dict(unit_obj, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.on_pos_changed)

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            if self.model:
                print('test--ComLobbyModel--animator_info--self.unit_obj =', self.unit_obj, '--xml_path =', self._animator.GetXmlFile(), '--self.model.visible =', self.model.visible, '--position =', self.model.position)
                only_active = arg[0]
                if self._animator:
                    self._animator.print_info(active=only_active)

    def _check_load_improved_skin_model_and_effect(self, model, mirror=False):
        model_key = str(model)
        if not self.can_load_improved_skin_res[model_key]:
            return
        if self.ready_for_improved_skin_flags[model_key] != 0:
            return
        load_improved_skin_model_and_effect(model, self.improved_skin_sfx_id, auto_load_trigger_at_intervals_res=True, lod_level='l')
        if mirror:
            self.send_event('E_INIT_MIRROR_SPRING_ANI')
        else:
            self.send_event('E_INIT_SPRING_ANI')
        self.handle_socket_objects(self.model)

    def modify_ready_for_improved_skin_flag(self, model, offset, mirror=False):
        if self.improved_skin_sfx_id is None:
            return
        else:
            model_key = str(model)
            self.ready_for_improved_skin_flags[model_key] += offset
            self._check_load_improved_skin_model_and_effect(model, mirror)
            return

    def load_model(self):
        role_id = self.ev_g_role_id()
        if role_id is None:
            return
        else:
            self._role_id = role_id
            fashion_data = self.ev_g_fashion_info()
            self.dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            path = dress_utils.get_role_model_path_by_lod(role_id, self.dressed_clothing_id, lod_level='l')
            if not path:
                return
            fashion_data = self.ev_g_fashion_info()
            self.dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            self.improved_skin_sfx_id = fashion_data.get(FASHION_POS_WEAPON_SFX, None)
            if self.improved_skin_sfx_id is not None:
                correct_sfx_id = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.dressed_clothing_id), 'improved_skin_sfx_item', default=None)
                if correct_sfx_id != self.improved_skin_sfx_id:
                    if self.ev_g_is_avatar():
                        uid = global_data.player.uid
                    else:
                        uid = self.ev_g_lobby_user_data_by_key('uid')
                    error_text = '[Improved sfx error]uid:{}|skin_id:{}|wrong_sfx_id:{}|correct_sfx_id:{}|'.format(str(uid), str(self.dressed_clothing_id), str(self.improved_skin_sfx_id), str(correct_sfx_id))
                    import exception_hook
                    exception_hook.post_error(error_text)
                    self.improved_skin_sfx_id = correct_sfx_id
            res_path = path.replace('l.gim', 'empty.gim')
            if self.improved_skin_sfx_id:
                path = get_improve_skin_body_path(self.improved_skin_sfx_id, lod='l') or path
            mesh_path_list = [
             path]
            self.suit_id = fashion_data.get(FASHION_POS_SUIT_2)
            self.head_id = fashion_data.get(FASHION_POS_HEADWEAR)
            self.bag_id = fashion_data.get(FASHION_POS_BACK)
            self.other_pendant_list = sorted([ fashion_data.get(p) for p in FASHION_OTHER_PENDANT_LIST if fashion_data.get(p) ])
            self.head_id, self.bag_id, self.suit_id, self.other_pendant_list = dress_utils.get_real_dec_dict_with_check_completion_and_replacement(self.dressed_clothing_id, self.head_id, self.bag_id, self.suit_id, self.other_pendant_list, self.improved_skin_sfx_id)
            self.head_pendant_type, self.head_res_path, self.pendant_socket_name, self.pendant_socket_res_path, self.head_pendant_l_same_gis, self.pendant_random_anim_list, self.bag_socket_name, self.bag_model_path, self.bag_socket_name2, self.bag_model_path2, self.bag_pendant_l_same_gis, self.pendant_data_list = dress_utils.get_pendant_res_lod_conf('l', res_path, self.dressed_clothing_id, self.head_id, self.bag_id, self.suit_id, self.other_pendant_list)
            mesh_path_list.append(self.head_res_path)
            if self.head_pendant_l_same_gis:
                mesh_path_list.append(self.pendant_socket_res_path)
            if self.bag_model_path:
                if self.bag_pendant_l_same_gis or not self.bag_socket_name:
                    mesh_path_list.append(self.bag_model_path)
            if self.bag_model_path2:
                if self.bag_pendant_l_same_gis or not self.bag_socket_name2:
                    mesh_path_list.append(self.bag_model_path2)
            if self.other_pendant_list and self.pendant_data_list:
                for pendant_data in self.pendant_data_list:
                    if pendant_data.get('head_pendant_l_same_gis'):
                        mesh_path_list.append(pendant_data.get('res_path'))
                    elif pendant_data.get('res_path') and not pendant_data.get('socket_name'):
                        mesh_path_list.append(pendant_data.get('res_path'))

            self.res_path = res_path
            self.mesh_path_list = mesh_path_list
            self.load_model_idx += 1
            self.model_id = global_data.model_mgr.create_model_in_scene(res_path, mesh_path_list=mesh_path_list, on_create_func=lambda model, load_idx=self.load_model_idx: self.on_load_model_complete(model, load_idx))
            return

    def on_role_fashion_change(self, item_no, fashion_data):
        lobby_item_type = item_utils.get_lobby_item_type(item_no)
        if lobby_item_type != L_ITEM_TYPE_ROLE:
            return
        self.on_refresh_player_model()

    def check_res_changed(self):
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2
        fashion_data = self.ev_g_fashion_info()
        new_role_id = self.ev_g_role_id()
        new_clothind_id = fashion_data.get(FASHION_POS_SUIT)
        new_head_id = fashion_data.get(FASHION_POS_HEADWEAR)
        new_bag_id = fashion_data.get(FASHION_POS_BACK)
        new_suit_id = fashion_data.get(FASHION_POS_SUIT_2)
        new_improved_skin_sfx_id = fashion_data.get(FASHION_POS_WEAPON_SFX)
        new_other_pendant_list = sorted([ fashion_data.get(p) for p in FASHION_OTHER_PENDANT_LIST if fashion_data.get(p) ])
        model = self._get_model()
        if model is None:
            return True
        else:
            self.model_visible = bool(self.ev_g_is_pos_inited())
            if new_role_id == self._role_id and new_bag_id == self.bag_id and new_head_id == self.head_id and new_clothind_id == self.dressed_clothing_id and new_suit_id == self.suit_id and new_other_pendant_list == self.other_pendant_list and new_improved_skin_sfx_id == self.improved_skin_sfx_id:
                return False
            return True

    def on_refresh_player_model(self):
        if self._flag_delay_refresh:
            return
        else:
            if global_data.player is None:
                return
            if not self.check_res_changed():
                return
            self._flag_delay_refresh = True
            global_data.game_mgr.next_exec(self.delay_refresh_player_model)
            return

    def delay_refresh_player_model(self):
        self._flag_delay_refresh = False
        if global_data.game_mgr.scene.scene_type not in self.SCENE_TYPE:
            return
        else:
            if global_data.player is None:
                return
            self.reset_animator()
            self.reset_res()
            self.load_model()
            return

    def _get_model(self):
        if self.model and self.model.valid:
            return self.model
        else:
            return None

    def _release_head_pendant_random_anim_timer(self):
        if self.head_pendant_random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.head_pendant_random_anim_timer)
            self.head_pendant_random_anim_timer = None
        return

    def _clear_improved_skin_model_and_effect(self, model):
        model_key = str(model)
        clear_role_skin_model_and_effect(model, clear_trigger_interval=True)
        self.ready_for_improved_skin_flags.pop(model_key, None)
        return

    def reset_res(self):
        self.del_socket_model(self.bag_socket_name)
        self.del_socket_model(self.bag_socket_name2)
        self.del_socket_model(self.pendant_socket_name)
        if self.other_pendant_list and self.pendant_data_list:
            for pendant_data in self.pendant_data_list:
                if pendant_data.get('head_pendant_l_same_gis'):
                    continue
                res_path = pendant_data.get('res_path')
                socket_name = pendant_data.get('socket_name')
                self.del_socket_model(socket_name, res_path)

        self.head_pendant_model = None
        self._release_head_pendant_random_anim_timer()
        if self.model_id:
            if self.mirror_model_id:
                mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
                if mode_disp:
                    mode_disp.remove_model_from_mirror(self.model)
                mirror_model = global_data.model_mgr.get_model_by_id(self.mirror_model_id)
                if mirror_model and mirror_model.valid:
                    self._clear_improved_skin_model_and_effect(mirror_model)
                    mirror_model.destroy()
                global_data.model_mgr.remove_model_by_id(self.mirror_model_id)
                self.mirror_model_id = None
                self.mirror_model = None
            if self.model and self.model.valid:
                self._clear_improved_skin_model_and_effect(self.model)
                self.model.destroy()
            global_data.model_mgr.remove_model_by_id(self.model_id)
            self.model_id = None
        self.model = None
        return

    def del_socket_model(self, socket_name, res_path=None):
        if not socket_name:
            return
        else:
            socket_model_name = 'socket_model_%s' % socket_name
            if res_path:
                socket_model_name = '%s_%s' % (socket_model_name, res_path)
            resloader.del_res_attr(self, socket_model_name, True)
            setattr(self, socket_model_name, None)
            socket_model_name = 'mirror_socket_model_%s' % socket_name
            if res_path:
                socket_model_name = '%s_%s' % (socket_model_name, res_path)
            resloader.del_res_attr(self, socket_model_name, True)
            setattr(self, socket_model_name, None)
            return

    def destroy(self):
        self.process_event(False)
        self.reset_animator()
        self.reset_res()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.on_pos_changed)
        super(ComLobbyModel, self).destroy()

    def on_display_quality_change(self, quality):
        if global_data.is_ue_model:
            if self.model:
                self.model.mirror_reflect = quality > 1

    def on_load_mirror_model_complete(self, mirror_model, *args):
        if not mirror_model or not mirror_model.valid:
            return
        else:
            scene = world.get_active_scene()
            if not self.model or scene.scene_type not in self.SCENE_TYPE or not self.is_valid():
                global_data.model_mgr.remove_model_by_id(self.mirror_model_id)
                self.mirror_model_id = None
                return
            mirror_model.set_submesh_visible('empty', False)
            scale = dress_utils.get_lobby_model_scale(self._role_id, self.dressed_clothing_id)
            mirror_model.scale = math3d.vector(scale, scale, scale)
            if mirror_model:
                mirror_model.cast_shadow = True
                mirror_model.receive_shadow = True
            self.mirror_model = mirror_model
            model_key = str(mirror_model)
            self.ready_for_improved_skin_flags[model_key] = 0
            self.can_load_improved_skin_res[model_key] = False
            hair_model = mirror_model.get_socket_obj('gj_hair', 0)
            if hair_model:
                hair_model.follow_same_bone_model(self.sd.ref_hair_model)
            self.sd.ref_animator_mirror = animator.Animator(mirror_model, lobby_ani_const.XML_PATH, self.unit_obj)
            self.sd.ref_animator_mirror.Load(False)
            self.send_event('E_MIRROR_MODEL_LOADED', mirror_model)
            if not self.pendant_socket_res_path or self.pendant_socket_res_path.endswith('.sfx') or self.head_pendant_l_same_gis:
                self.send_event('E_INIT_MIRROR_SPRING_ANI')
            if not self.improved_skin_sfx_id:
                load_normal_skin_model_and_effect(mirror_model, self.dressed_clothing_id, 'l')
            self.load_socket_bag(self.bag_model_path, self.bag_socket_name, mirror_model, mirror=True)
            self.load_socket_bag(self.bag_model_path2, self.bag_socket_name2, mirror_model, mirror=True)
            if self.pendant_socket_res_path:
                if self.pendant_socket_res_path.endswith('.sfx'):
                    global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path, mirror_model, self.pendant_socket_name)
                else:
                    self.load_head_socket_model(mirror_model, mirror=True)
            if any(self.other_pendant_list) and self.pendant_data_list:
                self.load_other_pendant(self.pendant_data_list, mirror_model, mirror=True)
            mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
            if mode_disp:
                mode_disp.add_model_to_mirror(self.model, mirror_model, True)
            self.can_load_improved_skin_res[model_key] = True
            self._check_load_improved_skin_model_and_effect(mirror_model)
            return

    def on_load_model_complete(self, model, load_model_idx):
        if not model or not model.valid:
            return
        else:
            if load_model_idx != self.load_model_idx:
                global_data.model_mgr.remove_model(model)
                return
            scene = world.get_active_scene()
            self.sd.ref_finish_load_lod_model = True
            if scene.scene_type not in self.SCENE_TYPE or not self.is_valid() or not global_data.player:
                global_data.model_mgr.remove_model_by_id(self.model_id)
                self.model_id = None
                if not global_data.player:
                    self.need_update = True
                return
            try:
                model.set_submesh_visible('empty', False)
            except Exception as e:
                import exception_hook
                exception_hook.post_error('invalid model without empty-submesh {}'.format(str(model.filename)))

            self.model = model
            self.model_visible = True
            scale = dress_utils.get_lobby_model_scale(self._role_id, self.dressed_clothing_id)
            model.scale = math3d.vector(scale, scale, scale)
            if model:
                model.cast_shadow = True
                model.receive_shadow = True
            model.world_position = self.ev_g_ctrl_position()
            model.world_rotation_matrix = self.ev_g_rotation_matrix()
            self.load_animator()
            self.send_event('E_MODEL_LOADED', model)
            if not self.improved_skin_sfx_id:
                load_normal_skin_model_and_effect(model, self.dressed_clothing_id, 'l')
            if not self.pendant_socket_res_path or self.pendant_socket_res_path.endswith('.sfx') or self.head_pendant_l_same_gis:
                self.send_event('E_INIT_SPRING_ANI')
            model_key = str(model)
            self.ready_for_improved_skin_flags[model_key] = 0
            self.can_load_improved_skin_res[model_key] = False
            self.load_socket_bag(self.bag_model_path, self.bag_socket_name, model)
            self.load_socket_bag(self.bag_model_path2, self.bag_socket_name2, model)
            if self.pendant_socket_res_path:
                if self.pendant_socket_res_path.endswith('.sfx'):
                    global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path, model, self.pendant_socket_name)
                else:
                    self.load_head_socket_model(model)
            if any(self.other_pendant_list) and self.pendant_data_list:
                self.load_other_pendant(self.pendant_data_list, model)
            self.send_event('E_INIT_HAIR_MODEL')
            self.send_event('E_INIT_BODY_SOCKET_ANIMATOR')
            self.can_load_improved_skin_res[model_key] = True
            self._check_load_improved_skin_model_and_effect(model)
            if global_data.is_multi_pass_support:
                pc_platform_utils.set_multi_pass_outline(model, is_lobby_display=True)
            self.send_event('E_HUMAN_MODEL_LOADED', model)
            self.send_event('S_FOOT_IK_ENABLE', True)
            if global_data.is_ue_model:
                model.mirror_reflect = global_data.game_mgr.gds.get_actual_quality() > 1
            model.all_materials.set_macro('RIM_LIGHT_ENABLE', 'TRUE')
            model.all_materials.rebuild_tech()
            model.enable_dynamic_culling(False)
            pc_platform_utils.set_alpha_submesh_rendergroup(model)
            mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
            if mode_disp and mode_disp.get_reflect_rt():
                self.mirror_model_id = global_data.model_mgr.create_model(self.res_path, mesh_path_list=self.mesh_path_list, on_create_func=self.on_load_mirror_model_complete)
            socket_list = PENDANT_BUG_LIST.get(str(self.dressed_clothing_id), None)
            if socket_list is not None:
                for socket in socket_list:
                    sub_model = model.get_socket_obj(socket)
                    if sub_model and type(model) == world.model:
                        sub_model.cast_shadow = True

                self.send_event('E_INIT_SPRING_ANI')
            self.handle_socket_objects(model)
            if str(self.dressed_clothing_id) in TRANSPARENT_SUBMESH_RENDER_PRIORITY:
                submesh_count = model.get_submesh_count()
                render_priority_setting = TRANSPARENT_SUBMESH_RENDER_PRIORITY[str(self.dressed_clothing_id)]
                for index in range(submesh_count):
                    submesh_name = model.get_submesh_name(index)
                    submesh_name = submesh_name.replace('_l', '_h')
                    if submesh_name in render_priority_setting:
                        model.set_submesh_rendergroup_and_priority(index, world.RENDER_GROUP_TRANSPARENT, render_priority_setting[submesh_name])

            return

    def handle_socket_objects(self, model):
        socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.dressed_clothing_id), 'sockets_in_socket_obj')
        if socket_name_list:
            for socket_name in socket_name_list:
                socket_model = model.get_socket_obj(socket_name, 0)
                if not socket_model and model.has_socket(socket_name):
                    model_list = model.get_socket_objects(socket_name)
                    if model_list:
                        socket_model = model_list[0]
                if socket_model:
                    socket_model.visible = model.visible
                    socket_model.cast_shadow = True

    def load_head_socket_model(self, model, mirror=False):
        if self.head_pendant_l_same_gis:
            return
        self.modify_ready_for_improved_skin_flag(model, 1, mirror)
        socket_model_name = mirror or 'socket_model_%s' % self.pendant_socket_name if 1 else 'mirror_socket_model_%s' % self.pendant_socket_name
        resloader.load_res_attr(self, socket_model_name, self.pendant_socket_res_path, self.on_load_head_pendant_model_complete, (
         self.pendant_socket_name, model, mirror), res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def _play_head_pendant_model_anim(self):
        if not self.pendant_random_anim_list:
            self.head_pendant_random_anim_timer = None
            return RELEASE
        else:
            if not self.head_pendant_model or not self.head_pendant_model.valid:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            anim_name, min_duration, max_duration = self.pendant_random_anim_list[self.head_pendant_anim_index * 3:self.head_pendant_anim_index * 3 + 3]
            self.head_pendant_anim_index = (self.head_pendant_anim_index + 1) % 2
            duration = random.uniform(min_duration, max_duration)
            self.head_pendant_model.play_animation(anim_name)
            self.head_pendant_random_anim_timer = global_data.game_mgr.register_logic_timer(self._play_head_pendant_model_anim, interval=duration, times=1, mode=CLOCK)
            return

    def on_load_head_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        pendant_socket_name, model, mirror = data
        if not model:
            return
        model.bind(pendant_socket_name, load_model, world.BIND_TYPE_ALL)
        if mirror:
            self.send_event('E_INIT_MIRROR_SPRING_ANI')
        else:
            self.send_event('E_INIT_SPRING_ANI')
        self.modify_ready_for_improved_skin_flag(model, -1, mirror)
        self.head_pendant_model = load_model
        self.head_pendant_anim_index = 0
        self._play_head_pendant_model_anim()

    def load_socket_bag(self, res_path, socket_name, model, mirror=False):
        if self.bag_pendant_l_same_gis:
            return
        if res_path and socket_name:
            self.modify_ready_for_improved_skin_flag(model, 1, mirror)
            socket_model_name = mirror or 'socket_model_%s' % socket_name if 1 else 'mirror_socket_model_%s' % socket_name
            resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_bag_pendant_model_complete, (
             socket_name, model, mirror), res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def on_load_bag_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        socket_name, model, mirror = data
        if not model or not model.valid:
            return
        model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
        if mirror:
            self.send_event('E_INIT_MIRROR_SPRING_ANI')
        else:
            self.send_event('E_INIT_SPRING_ANI')
        self.modify_ready_for_improved_skin_flag(model, -1, mirror)

    def load_other_pendant(self, other_pendant_list, model, mirror=False):
        for pendant_data in other_pendant_list:
            if pendant_data.get('head_pendant_l_same_gis'):
                continue
            res_path = pendant_data.get('res_path')
            socket_name = pendant_data.get('socket_name')
            anim = pendant_data.get('pendant_l_anim')
            if socket_name:
                self.load_other_pendant_model(res_path, socket_name, model, mirror, anim)

    def load_other_pendant_model(self, res_path=None, socket_name=None, model=None, mirror=False, anim=None):
        if res_path and socket_name:
            self.modify_ready_for_improved_skin_flag(model, 1, mirror)
            socket_model_name = mirror or 'socket_model_%s_%s' % (socket_name, res_path) if 1 else 'mirror_socket_model_%s_%s' % (socket_name, res_path)
            resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_other_pendant_model_complete, (
             socket_name, model, mirror, anim), res_type='MODEL', priority=game3d.ASYNC_HIGH)

    def on_load_other_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid or not self.is_valid():
            load_model.destroy()
            return
        socket_name, model, mirror, anim = data
        if not model or not model.valid:
            return
        model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
        if anim and load_model.has_anim(anim):
            load_model.play_animation(anim, -1, world.TRANSIT_TYPE_DEFAULT, 0, True)
        if mirror:
            self.send_event('E_INIT_MIRROR_SPRING_ANI')
        else:
            self.send_event('E_INIT_SPRING_ANI')
        self.modify_ready_for_improved_skin_flag(model, -1, mirror)
        self.send_event('E_INIT_BODY_SOCKET_ANIMATOR', socket_name)

    def load_animator(self):
        self._animator = animator.Animator(self.model, lobby_ani_const.XML_PATH, self.unit_obj)
        self._animator.Load(False, self.on_load_animator_complete)

    def on_load_animator_complete(self, *args):
        self.send_event('E_ANIMATOR_LOADED')
        for arg, callback_list in six.iteritems(self._active_event):
            for callback in callback_list:
                self._animator.register_active_event(arg, callback)

        for arg, callback_list in six.iteritems(self._state_exit_event):
            for callback in callback_list:
                self._animator.register_state_exit_event(arg, callback)

        self._active_event = {}
        self._state_exit_event = {}
        self.replace_animation()

    def replace_animation(self):
        clip_name_dict = confmgr.get('lobby_item', str(self.dressed_clothing_id), 'player_move_ani_name')
        if not clip_name_dict:
            return
        node_name = 'src_stand'
        clip_name = clip_name_dict.get(node_name, '')
        if clip_name:
            self._animator.replace_clip_name('src_move_o', clip_name)
            if self.sd.ref_animator_mirror:
                self.sd.ref_animator_mirror.replace_clip_name('src_move_o', clip_name)
        move_name = 'blend_move'
        move_clip_name = clip_name_dict.get(move_name, '')
        if move_clip_name:
            for i in range(len(BLEND_MOVE_NODE)):
                node_move = self._animator.find(BLEND_MOVE_NODE[i])
                if node_move:
                    self._animator.replace_clip_name(BLEND_MOVE_NODE[i], move_clip_name + BLEND_MOVE_FIX[i])
                    if self.sd.ref_animator_mirror:
                        self.sd.ref_animator_mirror.replace_clip_name(BLEND_MOVE_NODE[i], move_clip_name + BLEND_MOVE_FIX[i])

    def reset_animator(self):
        if self._animator:
            self._animator.destroy()
            self._animator = None
        if self.sd.ref_animator_mirror:
            self.sd.ref_animator_mirror.destroy()
            self.sd.ref_animator_mirror = None
        return

    def on_pos_changed(self, pos):
        model = self._get_model()
        if model:
            model.world_position = pos
            if not self._model_visible:
                self.model_visible = True

    def get_pos(self):
        model = self._get_model()
        if model:
            return model.world_position

    def is_mounting(self):
        if self._animator:
            return self._animator.GetInt('state_idx') == lobby_ani_const.STATE_MOUNT

    def set_ani_int_state(self, name, value):
        if self.is_mounting() and value in (lobby_ani_const.STATE_IDLE, lobby_ani_const.STATE_MOVE):
            return
        if self._animator:
            self._animator.SetInt(name, value)
            if self.sd.ref_animator_mirror:
                self.sd.ref_animator_mirror.SetInt(name, value)

    def set_ani_float_state(self, name, value):
        if self._animator:
            value = float('%.2f' % value)
            self._animator.SetFloat(name, value)
            if self.sd.ref_animator_mirror:
                self.sd.ref_animator_mirror.SetFloat(name, value)

    def on_set_rotation_matrix(self, matrix):
        model = self._get_model()
        if model:
            model.world_rotation_matrix = matrix

    def get_yaw(self):
        model = self._get_model()
        if model:
            return model.world_rotation_matrix.yaw
        return 0.0

    def register_one_type_event(self, arg, callback, event_dict):
        if not isinstance(arg, (list, tuple)):
            arg = (
             arg,)
        for one_arg in arg:
            event_list = event_dict.setdefault(one_arg, [])
            event_list.append(callback)

    def _register_active_event(self, arg, callback):
        if self._animator:
            self._animator.register_active_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._active_event)

    def _unregister_active_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_active_event(arg, callback)

    def _register_state_exit_event(self, arg, callback):
        if self._animator:
            self._animator.register_state_exit_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._state_exit_event)

    def _unregister_state_exit_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_state_exit_event(arg, callback)

    def _register_change_clip_event(self, node_name, params, callback, data=None, ignore_active=False):
        animator = self._animator
        if not animator:
            return
        source_node = animator.find(node_name)
        if not source_node:
            return
        if not ignore_active:
            if not source_node.IsActiveInHierarchy():
                return
        for param_name in params:
            self.register_anim_param_listener(param_name, node_name, callback, data)

    def register_anim_param_listener(self, param_name, node_name, callback, data=None):
        animator = self._animator
        if not animator:
            return
        animator.RegisterParamListener(param_name, node_name, callback, data)