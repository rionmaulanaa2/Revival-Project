# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComLodHuman.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
import world
import math3d
import render
from logic.gcommon.item.item_const import LOD_L
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import const
from logic.gcommon.component.client.com_base_appearance.ComLodBase import ComLodBase
from logic.gcommon.component.client.ComBaseModelAppearance import RES_TYPE_UNKNOWN
import game3d
from logic.gutils import dress_utils
import logic.gcommon.common_utils.bcast_utils as bcast
from common.utils.path import check_file_exist
from common.utils.timer import CLOCK, RELEASE
import random
import weakref
from common.utils import pc_platform_utils
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_SUIT_2, FASHION_POS_BACK, FASHION_OTHER_PENDANT_LIST
from common.cfg import confmgr
import C_file
from logic.gutils.role_skin_utils import load_improved_skin_model_and_effect, get_improve_skin_body_path, load_normal_skin_model_and_effect, clear_role_skin_model_and_effect
from logic.gcommon.item.item_const import FASHION_POS_WEAPON_SFX
from logic.manager_agents.manager_decorators import sync_exec
EMPTY_SUBMESH_NAME = 'empty'
MIN_LOD_LEVEL = 3
TRANSPARENT_SUBMESH_RENDER_PRIORITY = {'201002057': {'20_2009_h_1': -2
                 },
   '201002058': {'20_2009_h_1': -2
                 },
   '201002059': {'20_2007_h_1': -2
                 },
   '201001351': {'13_2006_h_head_1': -2
                 },
   '201003171': {'31_2002_h_2': 2
                 }
   }
NEED_MODIFY_TRANSPARENT_LEVEL = {
 'h', 'l', 'l1'}

class ComLodHuman(ComLodBase):
    PUPPET_LOD_CONFIG = {0: LOD_L,1: LOD_L,2: LOD_L}
    LOD_TMP_BLACK_LIST = frozenset([])
    BIND_EVENT = {'E_CHARACTER_ATTR': '_change_character_attr',
       'E_HUMAN_MODEL_LOADED': 'on_humman_model_load',
       'E_CLOTHING_CHANGED': '_dressup',
       'E_RESET_RENDER_STAGE': 'reset_render_stage',
       'E_CHANGE_ANIM_MOVE_DIR': 'change_anim_move_dir',
       'E_SET_ANIM_STATE': '_set_soft_bone_anim_state',
       'E_CHANGE_FASHION': 'change_fashion',
       'E_FORCE_HIGH_MODEL': 'force_hight_model',
       'E_FORCE_LOBBY_OUTLINE': 'force_lobby_outline',
       'G_FORCE_LOBBY_OUTLINE': 'get_force_lobby_outline',
       'E_FORCE_SHADER_LOD_LEVEL': 'force_shader_lod_level',
       'G_FORCE_SHADER_LOD_LEVEL': 'get_shader_force_lod_level',
       'E_HIT_MODEL_LOADED': 'on_hit_model_loaded'
       }

    def __init__(self):
        super(ComLodHuman, self).__init__()
        self.enable_human_lod = True
        self._model_lod_name = ''
        self._softbone = None
        self._softbone_list = {}
        self._softbone_display = None
        self._softbone_m_to_name = None
        self._last_select_bone = None
        self._select_mtg = None
        self._unselect_mtg = None
        self._dresser = None
        self._shadow_task_id = 0
        self._cur_body_res_path = None
        self._cur_head_res_path = None
        self._cur_bag_res_path = None
        self._last_body_res_path = None
        self._last_head_res_path = None
        self._last_bag_res_path = None
        self._load_body_mesh_task = None
        self._load_head_mesh_task = None
        self._load_bag_mesh_task = None
        self._is_force_high_model = False
        self._is_lobby_outline = False
        self._force_shader_lod_level = None
        self._update_softbone_tick = False
        self.head_socket_name = 'neck'
        self.head_model_path = None
        self.head_model = None
        self.head_animator = None
        self.head_pendant_type = None
        self.pendant_socket_name = None
        self.pendant_socket_res_path = None
        self.head_pendant_l_same_gis = None
        self.bag_pendant_l_same_gis = None
        self.bag_socket_name = None
        self.bag_model_path = None
        self.bag_socket_name2 = None
        self.bag_model_path2 = None
        self.pendant_data_list = None
        self.head_sfx = None
        self.head_pendant_random_anim_timer = None
        self.head_pendant_anim_index = 0
        self.head_pendant_model = None
        self._cur_head_pendant_res_path = None
        self._last_head_pendant_res_path = None
        self._load_head_pendant_mesh_task = None
        self._load_other_pendant_mesh_task_dict = {}
        self._last_other_pendant_res_path_dict = {}
        self._cur_other_pendant_res_path_dict = {}
        self.dressed_clothing_id = None
        self.improved_skin_sfx_id = None
        self.sub_model_list = []
        self.sfx_id_list = []
        self.finish_load_body_and_head_num = 0
        self.need_load_model_num = 0
        self.finish_load_model_num = 0
        self.model_lod_level = 'l'
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLodHuman, self).init_from_dict(unit_obj, bdict)
        if self.enable_human_lod:
            self.init_events()
        self.need_update = True

    def int_data(self):
        conf_name = 'CharacterLodConst'
        if pc_platform_utils.is_pc_hight_quality_simple():
            conf_name = 'CharacterLodConstPC'
        self._lod_config = confmgr.get('c_human_lod_conf', conf_name, 'Content')

    def init_events(self):
        econf = {'display_quality_change': self.on_display_quality_change
           }
        is_puppet_com = self.is_unit_obj_type('LPuppet') or self.is_unit_obj_type('LPuppetRobot')
        if is_puppet_com:
            econf['ui_enter_aim'] = self.update_lod_on_change_aim
            econf['ui_leave_aim'] = self.update_lod_on_change_aim
        global_data.emgr.bind_events(econf)

    def init_lod(self):
        model = self.ev_g_model()
        if not model:
            return
        if self.enable_human_lod:
            if self.ev_g_is_avatar():
                self.load_lod_model()
                return
            model.lod_callback = self.update_lod
            model.visible = False
            quality = global_data.game_mgr.gds.get_actual_quality()
            self.on_display_quality_change(quality)
        else:
            self.load_lod_model()

    def update_lod_on_change_aim(self):
        self.update_lod(self._cur_lod_level)

    def update_cur_lod(self):
        if global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_in_aim:
            lod_level = self._start_lod_level + self._cur_lod_level
            if lod_level < MIN_LOD_LEVEL:
                if self._cur_lod_level == self._to_lod_level:
                    return
        elif self._cur_lod_level == self._to_lod_level:
            return
        self._cur_lod_level = self._to_lod_level
        self.load_lod_model()

    def force_hight_model(self, is_force):
        self._is_force_high_model = is_force
        self.load_lod_model()

    def force_lobby_outline(self, is_lobby_outline, is_force=False):
        if self._is_lobby_outline == is_lobby_outline and not is_force:
            return
        self._is_lobby_outline = is_lobby_outline
        from common.utils import pc_platform_utils
        model = self.ev_g_model()
        if not model:
            return
        if is_lobby_outline:
            pc_platform_utils.set_multi_pass_outline(model)
        else:
            pc_platform_utils.disable_multi_pass_outline(model)

    def get_force_lobby_outline(self):
        return self._is_lobby_outline

    def force_shader_lod_level(self, level, is_force=False):
        if self._force_shader_lod_level == level and not is_force:
            return
        else:
            self._force_shader_lod_level = level
            model = self.ev_g_model()
            if not model:
                return
            if level is not None:
                model.all_materials.set_macro('LOD_LEVEL', str(level))
            else:
                from logic.vscene.global_display_setting import GlobalDisplaySeting
                quality = GlobalDisplaySeting().get_actual_quality()
                from logic.gutils.shader_warmup import DEFAULT_LOD_MAPPING
                lod_level = DEFAULT_LOD_MAPPING.get(quality, 2)
                model.all_materials.set_macro('LOD_LEVEL', str(lod_level))
            return

    def get_shader_force_lod_level(self):
        return self._force_shader_lod_level

    def get_lod_level_name_fixed_lod(self):
        lod_level = ''
        if self.ev_g_is_avatar() or self._is_force_high_model:
            lod_level = 'l'
        else:
            lod_level = 'l1'
        return lod_level

    def get_lod_level_name(self):
        lod_name = 'l'
        lod_level = self._start_lod_level + self._cur_lod_level
        if self.ev_g_is_avatar():
            start_lod_level, lod_dist_list = self.calc_lod_dist()
            lod_level = start_lod_level
        if lod_level > 0:
            lod_name += str(lod_level)
        if lod_level >= MIN_LOD_LEVEL and global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_in_aim:
            lod_name = 'l2'
        if lod_level > MIN_LOD_LEVEL or lod_name == 'l4':
            lod_name = 'l3'
        if self._is_force_high_model:
            lod_name = 'l'
        return lod_name

    def check_file_exist_ex(self, file_path):
        if file_path in self.LOD_TMP_BLACK_LIST:
            return False
        return check_file_exist(file_path)

    def load_lod_model(self, force_lod_level=None, force_skin_id=None, force_head_id=None, force_bag_id=None, force_suit_id=None):
        model = self.ev_g_model()
        if not model:
            return
        else:
            if self.enable_human_lod:
                lod_level = self.get_lod_level_name()
            else:
                lod_level = self.get_lod_level_name_fixed_lod()
            is_test = force_lod_level or force_skin_id or force_head_id or force_bag_id or force_suit_id
            if self._model_lod_name == lod_level and not is_test:
                return
            self._model_lod_name = lod_level
            if force_lod_level:
                lod_level = force_lod_level
            self.model_lod_level = lod_level
            role_id = self.ev_g_role_id()
            role_id = int(role_id)
            fashion_dict = self.ev_g_fashion()
            self.dressed_clothing_id = fashion_dict.get(FASHION_POS_SUIT)
            suit_id = fashion_dict.get(FASHION_POS_SUIT_2)
            head_id = fashion_dict.get(FASHION_POS_HEADWEAR)
            bag_id = fashion_dict.get(FASHION_POS_BACK)
            self.improved_skin_sfx_id = fashion_dict.get(FASHION_POS_WEAPON_SFX, None)
            other_pendant_list = [ fashion_dict.get(p) for p in FASHION_OTHER_PENDANT_LIST if fashion_dict.get(p) ]
            head_id, bag_id, suit_id, other_pendant_list = dress_utils.get_real_dec_dict_with_check_completion_and_replacement(self.dressed_clothing_id, head_id, bag_id, suit_id, other_pendant_list, self.improved_skin_sfx_id)
            if force_skin_id:
                self.dressed_clothing_id = force_skin_id
            if force_bag_id and dress_utils.check_valid_decoration(self.dressed_clothing_id, force_bag_id):
                bag_id = force_bag_id
            if force_head_id and dress_utils.check_valid_decoration(self.dressed_clothing_id, force_head_id):
                head_id = force_head_id
            if force_suit_id and dress_utils.check_valid_decoration(self.dressed_clothing_id, force_suit_id):
                suit_id = force_suit_id
            res_path = dress_utils.get_role_model_path(role_id, self.dressed_clothing_id)
            body_res_path = res_path
            if self.improved_skin_sfx_id:
                body_res_path = get_improve_skin_body_path(self.improved_skin_sfx_id, lod=lod_level) or res_path
            body_res_path = body_res_path.replace('empty.gim', '%s.gim' % lod_level)
            model = self.ev_g_model()
            self.clear_lod_model_all_loaded_info()
            if self.check_file_exist_ex(body_res_path):
                self.need_load_model_num += 1
                self.on_add_fullbody_model(None, body_res_path)
            else:
                print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % body_res_path)
            self.head_pendant_type, head_res_path, self.pendant_socket_name, self.pendant_socket_res_path, self.head_pendant_l_same_gis, self.pendant_random_anim_list, self.bag_socket_name, self.bag_model_path, self.bag_socket_name2, self.bag_model_path2, self.bag_pendant_l_same_gis, self.pendant_data_list = dress_utils.get_pendant_res_lod_conf(lod_level, res_path, self.dressed_clothing_id, head_id, bag_id, suit_id, other_pendant_list)
            self.load_bag_model(self.bag_model_path, self.bag_socket_name)
            self.load_bag_model(self.bag_model_path2, self.bag_socket_name2)
            if self.pendant_data_list:
                for pendant_data in self.pendant_data_list:
                    self.load_one_other_pendant(pendant_data)

            if self.check_file_exist_ex(head_res_path):
                self.need_load_model_num += 1
                self.on_add_head_model(None, head_res_path)
            else:
                print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % head_res_path)
            if self.pendant_socket_res_path:
                if self.pendant_socket_res_path.endswith('.sfx'):
                    if not self.head_sfx:
                        global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path, model, self.pendant_socket_name, on_create_func=self.create_head_sfx_callback)
                elif self.head_pendant_l_same_gis:
                    if self.check_file_exist_ex(self.pendant_socket_res_path):
                        self.need_load_model_num += 1
                        self.ev_g_load_model(self.pendant_socket_res_path, self.on_add_head_pendant_model, self.pendant_socket_res_path, sync_priority=game3d.ASYNC_HIGH)
                    else:
                        print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % self.pendant_socket_res_path)
                elif model.has_socket(self.pendant_socket_name):
                    model_list = model.get_socket_objects(self.pendant_socket_name)
                    if len(model_list) <= 0:
                        if self.check_file_exist_ex(self.pendant_socket_res_path):
                            self.need_load_model_num += 1
                            self.ev_g_load_model(self.pendant_socket_res_path, self.on_add_head_pendant_model, self.pendant_socket_res_path, sync_priority=game3d.ASYNC_HIGH)
                        else:
                            print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % self.bag_model_path)
            import version
            if version.get_tag() == 'trunk':
                import device_compatibility
                from logic.client.const import game_mode_const
                lpos = global_data.sound_mgr.get_listener_pos()
                dist = (lpos - self.ev_g_model().world_position).length / 13.0
                dist_config = self.calc_lod_dist()[1]
                if global_data.game_mgr.gds:
                    quality = global_data.game_mgr.gds.get_actual_quality()
                else:
                    quality = 0
                perf_flag = device_compatibility.get_device_perf_flag()
                if self.ev_g_is_avatar():
                    camp_flag = 0
                elif global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self.unit_obj.ev_g_camp_id()):
                    camp_flag = 1
                else:
                    camp_flag = 2
                game_mode = global_data.game_mode.get_mode_type()
                game_mode_idx = game_mode_const.get_game_mode_index(game_mode)
                index = ','.join([str(game_mode_idx), str(perf_flag), str(quality), str(camp_flag)])
            return

    def load_bag_model(self, res_path, socket_name):
        if res_path:
            model = self.ev_g_model()
            if not self.bag_pendant_l_same_gis and socket_name:
                model_list = model.get_socket_objects(socket_name)
                if len(model_list) <= 0:
                    if self.check_file_exist_ex(res_path):
                        self.need_load_model_num += 1
                        self.ev_g_load_model(res_path, self.on_add_bag_model, (res_path, socket_name), sync_priority=game3d.ASYNC_HIGH)
                    else:
                        print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % res_path)
            elif self.check_file_exist_ex(res_path):
                self.need_load_model_num += 1
                self.ev_g_load_model(res_path, self.on_add_bag_model, (res_path, socket_name), sync_priority=game3d.ASYNC_HIGH)
            else:
                print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % res_path)

    def load_one_other_pendant(self, other_pendent_data):
        model = self.ev_g_model()
        head_pendant_l_same_gis = other_pendent_data.get('head_pendant_l_same_gis')
        res_path = other_pendent_data.get('res_path')
        socket_name = other_pendent_data.get('socket_name')
        if head_pendant_l_same_gis or not socket_name:
            if self.check_file_exist_ex(res_path):
                self.ev_g_load_model(res_path, self.on_add_other_pendant_model, other_pendent_data, sync_priority=game3d.ASYNC_HIGH)
            else:
                print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % res_path)
        elif socket_name:
            model_list = model.get_socket_objects(socket_name)
            if len(model_list) <= 0:
                if self.check_file_exist_ex(res_path):
                    self.ev_g_load_model(res_path, self.on_add_other_pendant_model, other_pendent_data, sync_priority=game3d.ASYNC_HIGH)
                else:
                    print('ERROR: [ComLodHuman] load_lod_model failed for no res_file:%s.....' % self.bag_model_path)

    def on_humman_model_load(self, model, user_data, *arg):
        self.init_lod()
        res_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.dressed_clothing_id), 'hit_path', default=None)
        if not res_path:
            role_id = self.ev_g_role_id()
            res_path = 'character/{0}/hit/hit.gim'.format(role_id)
            if not C_file.find_res_file(res_path, ''):
                if confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex', default=0) == 1:
                    res_path = 'character/11/hit/hit.gim'
                else:
                    res_path = 'character/12/hit/hit.gim'
        self.need_load_model_num += 1
        self.send_event('E_TRY_LOAD_HIT_MODEL', model, res_path)
        return

    def on_hit_model_loaded(self):
        model = self.ev_g_model()
        if not model:
            return
        self.finish_load_model_num += 1
        self.on_finish_loaded_lod_model(model)

    def create_head_sfx_callback(self, sfx, *args):
        self.head_sfx = sfx

    def on_add_fullbody_model(self, load_model, res_path, *args):
        model = self.ev_g_model()
        if not model:
            return
        if self._cur_body_res_path:
            self._last_body_res_path = self._cur_body_res_path
        self._cur_body_res_path = res_path
        self._load_body_mesh_task = global_data.model_mgr.create_mesh_async(self._load_body_mesh_task, res_path, model, self.on_load_fullbody_mesh_completed, self.on_before_add_body_new_mesh)

    def on_add_head_model(self, load_model, res_path, *args):
        model = self.ev_g_model()
        if not model:
            return
        if self._cur_head_res_path:
            self._last_head_res_path = self._cur_head_res_path
        self._cur_head_res_path = res_path
        if dress_utils.is_assemble_style(res_path):
            self.ev_g_load_model(res_path, self.on_add_head_assemble_style, res_path, sync_priority=game3d.ASYNC_HIGH)
        else:
            self._load_head_mesh_task = global_data.model_mgr.create_mesh_async(self._load_head_mesh_task, res_path, model, self.on_load_head_mesh_completed, self.on_before_add_head_new_mesh)

    def on_add_head_assemble_style(self, head_model, *args):
        from common.animate import animator
        import logic.gcommon.common_const.animation_const as animation_const
        model = self.ev_g_model()
        if not model:
            return
        else:
            if getattr(head_model, 'set_forbid_cull_by_parent'):
                head_model.set_forbid_cull_by_parent(True)
            self.head_model = head_model
            model.bind(self.head_socket_name, head_model, world.BIND_TYPE_ALL)
            if head_model:
                self.head_animator = animator.Animator(head_model, animation_const.DEFAULT_HEAD_XML, self.unit_obj)
                self.head_animator.Load(True, self.on_load_head_animator_complete, None)
            return

    def on_load_head_animator_complete(self, *args):
        src_animator = self.ev_g_animator()
        dst_animator = self.head_animator
        if src_animator and dst_animator:
            dst_animator.SetIgnoreParamError(True)
            src_animator.RegSlaveAnimator('head', dst_animator)

    def _play_head_pendant_model_anim(self):
        if not self.pendant_random_anim_list:
            self.head_pendant_random_anim_timer = None
            return RELEASE
        else:
            if not self.head_pendant_model:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            head_pendant_model = self.head_pendant_model()
            if not head_pendant_model or not head_pendant_model.valid:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            anim_name, min_duration, max_duration = self.pendant_random_anim_list[self.head_pendant_anim_index * 3:self.head_pendant_anim_index * 3 + 3]
            self.head_pendant_anim_index = (self.head_pendant_anim_index + 1) % 2
            duration = random.uniform(min_duration, max_duration)
            head_pendant_model.play_animation(anim_name)
            self.head_pendant_random_anim_timer = global_data.game_mgr.register_logic_timer(self._play_head_pendant_model_anim, interval=duration, times=1, mode=CLOCK)
            return

    def on_add_head_pendant_model(self, load_model, res_path, *args):
        model = self.ev_g_model()
        if not model:
            return
        if self.head_pendant_l_same_gis:
            if self._cur_head_pendant_res_path:
                self._last_head_pendant_res_path = self._cur_head_pendant_res_path
            self._cur_head_pendant_res_path = res_path
            self._load_head_pendant_mesh_task = global_data.model_mgr.create_mesh_async(self._load_head_pendant_mesh_task, res_path, model, self.on_load_mesh_completed, self.on_before_add_head_pendant_new_mesh)
        elif self.pendant_socket_name:
            model.bind(self.pendant_socket_name, load_model, world.BIND_TYPE_ALL)
            self.head_pendant_model = weakref.ref(load_model)
            self.head_pendant_anim_index = 0
            self._play_head_pendant_model_anim()
            self.finish_load_model_num += 1
            self.on_finish_loaded_lod_model(model)

    def on_add_bag_model(self, load_model, data, *args):
        model = self.ev_g_model()
        if not model:
            return
        res_path, socket_name = data
        if not self.bag_pendant_l_same_gis and socket_name:
            model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
            self.finish_load_model_num += 1
            self.on_finish_loaded_lod_model(model)
            return
        if self._cur_bag_res_path:
            self._last_bag_res_path = self._cur_bag_res_path
        self._cur_bag_res_path = res_path
        self._load_bag_mesh_task = global_data.model_mgr.create_mesh_async(self._load_bag_mesh_task, res_path, model, self.on_load_mesh_completed, self.on_before_add_bag_new_mesh)

    def on_add_other_pendant_model(self, load_model, data, *args):
        model = self.ev_g_model()
        if not model:
            return
        else:
            from common.framework import Functor
            head_pendant_l_same_gis = data.get('head_pendant_l_same_gis')
            res_path = data.get('res_path')
            socket_name = data.get('socket_name')
            pendant_type = data.get('pendant_type')
            if head_pendant_l_same_gis or not socket_name:
                if self._cur_other_pendant_res_path_dict.get(pendant_type):
                    self._last_other_pendant_res_path_dict[pendant_type] = self._cur_other_pendant_res_path_dict.get(pendant_type)
                self._cur_other_pendant_res_path_dict[pendant_type] = res_path
                task = self._load_other_pendant_mesh_task_dict.get(res_path, None)
                self.need_load_model_num += 1
                new_task = global_data.model_mgr.create_mesh_async(task, res_path, model, self.on_load_mesh_completed, Functor(self.on_before_add_other_pendant_new_mesh, data))
                self._load_other_pendant_mesh_task_dict[res_path] = new_task
            elif socket_name:
                model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
                anim = data.get('pendant_l_anim')
                if anim and load_model.has_anim(anim):
                    load_model.play_animation(anim, -1, world.TRANSIT_TYPE_DEFAULT, 0, True)
                self.send_event('E_INIT_BODY_SOCKET_ANIMATOR', socket_name)
            return

    def on_before_add_body_new_mesh(self, model):
        if self._last_body_res_path:
            model.remove_mesh(self._last_body_res_path)
            self._last_body_res_path = None
            self.send_event('E_DESTROY_BODY_SOCKET_ANIMATOR')
        return

    def on_before_add_head_new_mesh(self, model):
        if self._last_head_res_path:
            model.remove_mesh(self._last_head_res_path)
            self._last_head_res_path = None
            self.send_event('E_DESTROY_HAIR_ANIMATOR')
        return

    def on_before_add_head_pendant_new_mesh(self, model):
        if self._last_head_pendant_res_path:
            model.remove_mesh(self._last_head_pendant_res_path)
            self._last_head_pendant_res_path = None
        return

    def on_before_add_bag_new_mesh(self, model):
        if self._last_bag_res_path:
            model.remove_mesh(self._last_bag_res_path)
            self._last_bag_res_path = None
        return

    def on_before_add_other_pendant_new_mesh(self, new_data, model):
        pendant_type = new_data.get('pendant_type')
        last_res_path = self._last_other_pendant_res_path_dict.get(pendant_type)
        if last_res_path:
            model.remove_mesh(last_res_path)
            self._last_other_pendant_res_path_dict[pendant_type] = None
        return

    def on_load_mesh_completed(self, model):
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            try:
                submesh_name = model.get_submesh_name(i)
            except:
                submesh_name = 'unknown_cn_str'

            if submesh_name != 'hit':
                model.set_submesh_hitmask(i, world.HIT_SKIP)

        owner_model = model
        self.send_event('E_HUMAN_LOD_LOADED', owner_model)
        self.finish_load_model_num += 1
        self.on_finish_loaded_lod_model(model)
        if global_data.debug_perf_switch_global:
            avatar_visible = global_data.get_debug_perf_val('enable_avatar_model', True)
            model.visible = avatar_visible

    def on_load_fullbody_mesh_completed(self, model):
        self.finish_load_body_and_head_num += 1
        self.create_normal_skin_model_and_effect(model)
        self.on_load_mesh_completed(model)
        self.send_event('E_INIT_BODY_SOCKET_ANIMATOR')
        if self.ev_g_is_avatar() and global_data.is_multi_pass_support:
            pc_platform_utils.set_multi_pass_outline(model)

    def on_load_head_mesh_completed(self, model):
        self.finish_load_body_and_head_num += 1
        self.create_normal_skin_model_and_effect(model)
        self.on_load_mesh_completed(model)
        self.send_event('E_INIT_HAIR_MODEL')
        if self.ev_g_is_avatar() and global_data.is_multi_pass_support:
            pc_platform_utils.set_multi_pass_outline(model)

    def on_finish_loaded_lod_model(self, model):
        if self.need_load_model_num > self.finish_load_model_num:
            return
        self.update_sub_model_render_priority(model)
        self.sd.ref_finish_load_lod_model = True
        if self.improved_skin_sfx_id:
            self.create_improved_skin_model_effect(model)
        self.handle_socket_objects(model)
        self.send_event('E_INIT_SPRING_ANI')
        if self._is_lobby_outline:
            self.force_lobby_outline(self._is_lobby_outline, is_force=True)
        if self._force_shader_lod_level:
            self.force_shader_lod_level(self._force_lod_level, is_force=True)

    def update_sub_model_render_priority(self, model):
        if self.model_lod_level in NEED_MODIFY_TRANSPARENT_LEVEL and str(self.dressed_clothing_id) in TRANSPARENT_SUBMESH_RENDER_PRIORITY:
            submesh_count = model.get_submesh_count()
            render_priority_setting = TRANSPARENT_SUBMESH_RENDER_PRIORITY[str(self.dressed_clothing_id)]
            for index in range(submesh_count):
                submesh_name = model.get_submesh_name(index)
                submesh_name = submesh_name.replace('_{}'.format(self.model_lod_level), '_h')
                if submesh_name in render_priority_setting:
                    model.set_submesh_rendergroup_and_priority(index, world.RENDER_GROUP_TRANSPARENT, render_priority_setting[submesh_name])

    def clear_lod_model_all_loaded_info(self):
        self.need_load_model_num = 0
        self.finish_load_model_num = 0
        self.finish_load_body_and_head_num = 0
        self.clear_skin_model_effect()

    def clear_skin_model_effect(self):
        model = self.ev_g_model()
        if model and model.valid:
            clear_role_skin_model_and_effect(model)

    def create_normal_skin_model_and_effect(self, model):
        if self.finish_load_body_and_head_num < 2:
            return
        if not self.improved_skin_sfx_id:
            self.sd.ref_role_skin_sub_model = load_normal_skin_model_and_effect(model, self.dressed_clothing_id, lod_level=self._model_lod_name)

    def create_improved_skin_model_effect(self, model):
        if self.ev_g_defeated():
            return
        else:
            self.clear_skin_model_effect()
            fashion = self.ev_g_fashion()
            improved_skin_sfx_id = fashion.get(FASHION_POS_WEAPON_SFX, None)
            if improved_skin_sfx_id:
                self.sd.ref_role_skin_sub_model = load_improved_skin_model_and_effect(model, improved_skin_sfx_id, lod_level=self._model_lod_name)
                if self.sd.ref_role_skin_sub_model:
                    self.send_event('E_HUMAN_LOD_LOADED', model)
            model = self.ev_g_model()
            if not model:
                return
            self.handle_socket_objects(model)
            return

    def handle_socket_objects(self, model):
        socket_name_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.dressed_clothing_id), 'sockets_hide_in_mecha')
        if socket_name_list:
            for socket_name in socket_name_list:
                socket_model = model.get_socket_obj(socket_name, 0)
                if not socket_model and model.has_socket(socket_name):
                    model_list = model.get_socket_objects(socket_name)
                    if model_list:
                        socket_model = model_list[0]
                if socket_model:
                    socket_model.visible = model.visible
                    if type(socket_model) == world.model:
                        socket_model.cast_shadow = True

    def _change_character_attr(self, name, *arg):
        if name == 'enable_softbone_h52':
            import data.softbone_global_arg_h52 as softbone_global_arg_h52
            import data.softbone_bone_arg as softbone_bone_arg_h52
            if not self._softbone:
                model = self.ev_g_model()
                softbone = model.get_soft_bone(True)
                softbone.gravity = softbone_global_arg_h52.gravity
                softbone.blend_animation = bool(softbone_global_arg_h52.blend_animation)
                softbone.iteration = softbone_global_arg_h52.iteration
                softbone.init()
                self._softbone = softbone
                enable_bone_anim = True
                enable_childs = True
                for one_bone_config in softbone_bone_arg_h52.bone_list:
                    softbone.set_bone_param(one_bone_config['name'], enable_bone_anim, one_bone_config['mass'], one_bone_config['damping'], one_bone_config['stiffness'], one_bone_config['strict_stiffness'], one_bone_config['high_simulation'], enable_childs)
                    self._softbone_list[one_bone_config['name']] = one_bone_config

                if hasattr(softbone, 'add_bone_special_param'):
                    for anim_state, bone_list in six.iteritems(softbone_bone_arg_h52.special_bone_list):
                        for one_bone_config in bone_list:
                            softbone.add_bone_special_param(one_bone_config['name'], anim_state, one_bone_config['mass'], one_bone_config['damping'], one_bone_config['stiffness'])

        elif name == 'disble_softbone_h52':
            if self._softbone:
                self._softbone.uninit()
                self._softbone = None
            self._softbone_list = {}
        return

    def _init_dresser_finish(self):
        if not self._dresser:
            return
        else:
            if self.ev_g_ctrl_mecha() is None:
                model_visible = self.ev_g_model_visibility()
                if model_visible:
                    self.send_event('E_SHOW_MODEL')
            else:
                ctrl_target = self.ev_g_control_target()
                if ctrl_target and ctrl_target.logic and ctrl_target.id != self.unit_obj.id:
                    model_visible = self.ev_g_model_visibility()
                    if model_visible:
                        self.send_event('E_SHOW_MODEL')
                    else:
                        self.send_event('E_HIDE_MODEL')
            return

    def change_fashion(self, suit_id):
        old_suit_id = self._dresser.get_suit_id()
        if old_suit_id == suit_id:
            return
        else:
            self._dresser.set_suit_id(suit_id)
            self._dressup(None, self._init_dresser_finish)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_CHANGE_FASHION, (suit_id,)), True, False, True)
            return

    def init_dresser(self, dress_dict):
        model = self.ev_g_model()
        role_id = self.ev_g_role_id()
        style = self.ev_g_dress_style()
        lod_value = LOD_L
        clothing = self.ev_g_clothing()
        suit_id = dress_utils.get_suit_id_by_clothing(clothing, role_id)
        from logic.units.LPuppet import LPuppet
        if isinstance(self.unit_obj, LPuppet):
            lod_value = self.PUPPET_LOD_CONFIG.get(0)
        self._dresser = dress_utils.DresserModel(model, role_id, lod_value, style, dress_dict=dress_dict, suit_id=suit_id)

    def _dressup(self, dress_pos, callback=None):
        if not self._dresser:
            return

        def _cb():
            if callback:
                callback()
            self._default_dressup_finish_callback()

        clothing = self.ev_g_clothing()
        self._dresser.dress(clothing, _cb, valid_checker=self.is_valid)

    def _default_dressup_finish_callback(self):
        self.send_event('E_DRESS_CHANGED_FINISHED')

    def change_anim_move_dir(self, dir_x, dir_y, *args):
        move_dir = self.ev_g_eight_dir(dir_x, dir_y)
        self._set_soft_bone_anim_state('move_back' if move_dir is not None and move_dir >= 6 else 'default')
        return

    def _set_soft_bone_anim_state(self, anim_state='default'):
        if self._softbone and hasattr(self._softbone, 'set_anim_state'):
            self._softbone.set_anim_state(anim_state)

    def destroy(self):
        self.clear_lod_model_all_loaded_info()
        super(ComLodHuman, self).destroy()
        self.head_pendant_model = None
        if self.head_pendant_random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.head_pendant_random_anim_timer)
            self.head_pendant_random_anim_timer = None
        if self._shadow_task_id:
            self.send_event('E_CANCEL_LOAD_TASK', self._shadow_task_id)
            self._shadow_task_id = 0
        if self._softbone:
            self._softbone.uninit()
            self._softbone = None
        if self._dresser:
            self._dresser.destroy()
        if self.head_animator:
            self.head_animator.destroy()
            self.head_animator = None
        return