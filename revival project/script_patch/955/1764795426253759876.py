# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/ConcertModelPlayer.py
from __future__ import absolute_import
from six.moves import range
import math3d
import world
from common.framework import Functor
from logic.gutils import lobby_model_display_utils
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.mecha_skin_utils import MechaSocketResAgent
from common.cfg import confmgr
from .LodObject import LodObject
from logic.gutils.mecha_skin_utils import get_mecha_conf_ex_weapon_sfx_id
s_aj_pos = (
 (830, 834, 1945), 235.0, (2.0, 2.0, 2.0))

class ConcertModelPlayer(LodObject):

    def __init__(self):
        super(ConcertModelPlayer, self).__init__()
        self.human_model = None
        self.human_model_id = None
        self.human_head_model = None
        self.pendant_socket_model = None
        self.human_anim_name = None
        self.human_anim_start_time = 0.0
        self.cur_skin_id = None
        self.animation_all_time = 0
        self.pos_rot_scale = s_aj_pos
        self.model_data = {}
        self.ext_data = {}
        self.is_same_gis = True
        self.item_lobby_type = None
        self.loaded_callback = None
        self.is_cache = False
        self.get_other_model_play_time_cb = None
        self.mecha_socket_res_agent = None
        return

    def set_model_load_callback(self, cb, get_time_cb):
        self.get_other_model_play_time_cb = get_time_cb
        self.loaded_callback = cb

    def destroy(self):
        super(ConcertModelPlayer, self).destroy()
        self.loaded_callback = None
        self.get_other_model_play_time_cb = None
        self.model_data = {}
        if self.human_model_id:
            global_data.model_mgr.remove_model_by_id(self.human_model_id)
            self.human_model_id = None
        if self.human_head_model:
            ity = get_lobby_item_type(self.cur_skin_id)
            if ity == L_ITEM_TYPE_MECHA_SKIN:
                if self.ext_data.get('need_skin_sfx', True) and self.mecha_socket_res_agent:
                    self.mecha_socket_res_agent.destroy()
            self.human_head_model.destroy()
            self.human_head_model = None
        if self.pendant_socket_model:
            self.pendant_socket_model.destroy()
            self.pendant_socket_model = None
        if self.human_model:
            is_clear_socket_model = self.ext_data.get('is_clear_socket_model', True)
            global_data.model_mgr.remove_model(self.human_model, is_clear_socket_model=is_clear_socket_model)
            self.human_model = None
        self.ext_data = {}
        return

    def update_is_same_gis(self):
        ity = get_lobby_item_type(self.cur_skin_id)
        if ity == L_ITEM_TYPE_ROLE_SKIN:
            role_id = self.model_data.get('role_id')
            self.is_same_gis = self.model_data.get('is_l_model', False)
            sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex')
            if sex == 0 or role_id in (111, ):
                self.is_same_gis = True
        else:
            self.is_same_gis = True

    def update_time(self, t):
        self.animation_all_time = t
        if self.item_lobby_type == L_ITEM_TYPE_MECHA_SKIN:
            self.tick()

    def change_human_model(self, start_time, skin_id, anim_name, pos_rot_scale=None, ext_dict=None, is_cache=False):
        self.human_anim_start_time = start_time
        self.ext_data = ext_dict
        if self.cur_skin_id == skin_id and self.human_model:
            self.play_animation(anim_name, self.animation_all_time - self.human_anim_start_time)
        else:
            if skin_id != self.cur_skin_id:
                if self.human_model_id:
                    global_data.model_mgr.remove_model_by_id(self.human_model_id)
                    self.human_model_id = None
                if self.human_model:
                    is_clear_socket_model = self.ext_data.get('is_clear_socket_model', True)
                    global_data.model_mgr.remove_model(self.human_model, is_clear_socket_model=is_clear_socket_model)
                    self.human_model = None
                if self.human_head_model:
                    self.human_head_model.destroy()
                    self.human_head_model = None
                if self.pendant_socket_model:
                    self.pendant_socket_model.destroy()
                    self.pendant_socket_model = None
                self.cur_skin_id = skin_id
                self.item_lobby_type = get_lobby_item_type(self.cur_skin_id)
            if self.item_lobby_type == L_ITEM_TYPE_MECHA_SKIN:
                self.clear_lod_model()
            if not self.cur_skin_id:
                return
            mpath = self.ext_data.get('mpath')
            if not mpath:
                model_data = lobby_model_display_utils.get_lobby_model_data(skin_id, consider_second_model=False)
                self.model_data = model_data[0]
                self.update_is_same_gis()
                mpath, sub_mesh_data = self.get_preview_model_data(skin_id=skin_id)
            else:
                sub_mesh_data = self.ext_data.get('sub_mesh_data')
                self.is_same_gis = self.ext_data.get('is_same_gis', True)
                str_cur_skin_id = str(self.cur_skin_id)
                if self.cur_skin_id and str_cur_skin_id.isdigit():
                    self.item_lobby_type = get_lobby_item_type(self.cur_skin_id)
                else:
                    self.item_lobby_type = self.ext_data.get('item_lobby_type', L_ITEM_TYPE_ROLE_SKIN)
            self.human_anim_name = anim_name
            if pos_rot_scale:
                self.pos_rot_scale = pos_rot_scale
            pos = math3d.vector(*self.pos_rot_scale[0])
            self.human_model_id = global_data.model_mgr.create_model_in_scene(mpath, pos, on_create_func=Functor(self.on_load_model_complete, sub_mesh_data))
        return

    def get_preview_model_data(self, role_id=None, skin_id=None, lod_level='h'):
        from logic.gutils import item_utils
        import logic.gutils.dress_utils as dress_utils
        ity = get_lobby_item_type(skin_id)
        if ity == L_ITEM_TYPE_ROLE_SKIN:
            if not role_id:
                role_id = item_utils.get_lobby_item_belong_no(skin_id)
            mpath = dress_utils.get_role_model_path_by_lod(role_id, skin_id, lod_level)
            item_no = dress_utils.get_role_item_no(role_id, skin_id)
            head_res_path_new = mpath.replace('{}.gim'.format(lod_level), 'parts/{}_head.gim'.format(lod_level))
            return (
             mpath, head_res_path_new)
        if ity == L_ITEM_TYPE_MECHA_SKIN:
            from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_path
            if not role_id:
                role_id = item_utils.get_lobby_item_belong_no(skin_id)
            mpath = get_mecha_model_path(role_id, skin_id)
            submesh_path = get_mecha_model_h_path(role_id, skin_id)
            return (
             mpath, submesh_path)
        return ('', '')

    def get_res_path(self):
        mpath, sub_mesh_data = self.get_preview_model_data(skin_id=self.cur_skin_id)
        return mpath

    def on_load_model_complete(self, sub_mesh_data, model, *args):
        self.human_model_id = None
        self.human_model = model
        if sub_mesh_data:
            if self.is_same_gis:
                self.human_model.add_mesh(sub_mesh_data)
            else:
                head_model = world.model(sub_mesh_data, None)
                self.human_model.bind('head', head_model)
                self.human_head_model = head_model
                if head_model.has_anim(self.human_anim_name):
                    self.play_animation(self.human_anim_name, self.animation_all_time - self.human_anim_start_time, head_model)
        is_l_model = self.model_data.get('is_l_model', False)
        pendant_socket_name = self.model_data.get('pendant_socket_name')
        pendant_socket_res_path = self.model_data.get('pendant_socket_res_path')
        if pendant_socket_res_path:
            if not pendant_socket_name or is_l_model and self.model_data.get('head_pendant_l_same_gis', 0):
                model.add_mesh(pendant_socket_res_path)
            else:
                pendant_socket_model = world.model(pendant_socket_res_path, None)
                self.pendant_socket_model = pendant_socket_model
                self.human_model.bind(pendant_socket_name, pendant_socket_model, world.BIND_TYPE_ALL)
                if pendant_socket_model.has_anim(self.human_anim_name):
                    self.play_animation(self.human_anim_name, self.animation_all_time - self.human_anim_start_time, pendant_socket_model)
        self.human_model.world_rotation_matrix = math3d.matrix.make_rotation_y(self.pos_rot_scale[1] / 180.0 * 3.14)
        self.human_model.scale = math3d.vector(*self.pos_rot_scale[2])
        if self.item_lobby_type == L_ITEM_TYPE_MECHA_SKIN:
            if self.ext_data.get('need_skin_sfx', True):
                self.mecha_socket_res_agent = MechaSocketResAgent()
                if self.ext_data.get('need_shiny_weapon'):
                    shiny_weapon_id = get_mecha_conf_ex_weapon_sfx_id(self.cur_skin_id)
                else:
                    shiny_weapon_id = None
                self.mecha_socket_res_agent.load_skin_model_and_effect(model, self.cur_skin_id, shiny_weapon_id, need_listen_anim_enter_leave=False)
        self.check_ext_data()
        is_play = False
        if self.get_other_model_play_time_cb:
            played_time = self.get_other_model_play_time_cb()
            if played_time is not None and played_time > 0:
                self.play_animation(self.human_anim_name, played_time)
                is_play = True
        if not is_play:
            self.play_animation(self.human_anim_name, self.animation_all_time - self.human_anim_start_time)
        if self.loaded_callback:
            self.loaded_callback()
        if self.item_lobby_type == L_ITEM_TYPE_MECHA_SKIN:
            cur_lod_level = 0
            lod_config = {'lod_0': [10, 'h'],'lod_1': [50, 'l'],'lod_2': [130, 'l1'],'lod_3': [-1, 'l2']}
            self.set_lod_model(model, sub_mesh_data, cur_lod_level, lod_config)
        return

    def check_ext_data(self, model=None):
        if model is None:
            model = self.human_model
        if self.ext_data:
            hide_sockets = self.ext_data.get('hide_sockets', [])
            for socket_name in hide_sockets:
                obj = model.get_socket_obj(socket_name, 0)
                if obj:
                    obj.visible = False

            show_sockets = self.ext_data.get('show_sockets', [])
            for socket_name in show_sockets:
                obj = model.get_socket_obj(socket_name, 0)
                if obj:
                    obj.visible = True

            hide_submeshes = self.ext_data.get('hide_submeshes', [])
            if hide_submeshes:
                for i in range(model.get_submesh_count()):
                    name = model.get_submesh_name(i)
                    if name in hide_submeshes:
                        model.set_submesh_visible(i, False)

            model_sfx = self.ext_data.get('model_sfx', '')
            if model_sfx:
                ity = get_lobby_item_type(self.cur_skin_id)
                if ity == L_ITEM_TYPE_MECHA_SKIN:
                    global_data.sfx_mgr.create_sfx_on_model(model_sfx, model, 'fx_root')
                else:
                    global_data.sfx_mgr.create_sfx_on_model(model_sfx, model, 'head')
        return

    def play_animation(self, anim_name, anim_time, model=None):
        import world
        start_time = 0
        if self.ext_data:
            force_ani_start_time = self.ext_data.get('force_ani_start_time', None)
            if force_ani_start_time is not None:
                start_time = force_ani_start_time
        anim_time = anim_time + start_time
        if not model:
            self.human_model.play_animation(anim_name, 1.0, 0, anim_time * 1000.0, world.PLAY_FLAG_DEF_LOOP)
        else:
            model.play_animation(anim_name, 1.0, 0, anim_time * 1000.0, world.PLAY_FLAG_DEF_LOOP)
        return

    def get_model_position(self):
        if self.item_lobby_type == L_ITEM_TYPE_ROLE_SKIN:
            if self.human_model:
                model_pos_bone = self.ext_data.get('model_pos_bone', '')
                if model_pos_bone:
                    soc = self.human_model.get_bone_matrix(model_pos_bone, world.SPACE_TYPE_WORLD)
                else:
                    soc = self.human_model.get_socket_matrix('head', world.SPACE_TYPE_WORLD)
                if soc:
                    return soc.translation
                else:
                    return self.human_model.world_position

        elif self.human_model:
            soc = self.human_model.get_socket_matrix('part_point0', world.SPACE_TYPE_WORLD)
            if soc:
                trans = soc.translation
                return math3d.vector(trans.x, self.human_model.world_position.y, trans.z)
            else:
                return self.human_model.world_position

        return None

    def sync_anim_time(self):
        if self.human_model:
            self.play_animation(self.human_anim_name, self.animation_all_time - self.human_anim_start_time)

    def is_loaded(self):
        if self.human_model:
            return True
        else:
            return False

    def get_model_anim_play_time(self):
        force_ani_start_time = self.ext_data.get('force_ani_start_time', 0)
        if self.human_model:
            return self.human_model.anim_time / 1000.0 - force_ani_start_time
        else:
            return None
            return None

    def on_load_mesh_completed(self, model):
        self.check_ext_data(model)

    def set_anim_rate(self, anim_rate):
        if self.human_model:
            self.human_model.anim_rate = anim_rate

    def get_anim_is_loop(self):
        return False

    def get_anim_rate(self):
        if self.human_model:
            return self.human_model.anim_rate
        else:
            return 0

    def get_skin_id(self):
        return self.cur_skin_id