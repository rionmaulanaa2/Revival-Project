# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_pet/ComPetAppearance.py
import six
import six_ex
import math3d
import game3d
import math
import world
import time
from common.cfg import confmgr
from logic.gcommon import time_utility
from ..ComAnimatorAppearance import ComAnimatorAppearance
from mobile.common.EntityManager import EntityManager
from common.animate import animator
from logic.gcommon.common_utils.parachute_utils import STAGE_LAND, STAGE_ISLAND
from logic.gcommon.common_const.ui_operation_const import ENABLE_PET_TRANSPARENT
PET_VISIBLE_STAGE = STAGE_LAND | STAGE_ISLAND
SHOW_MODEL_SFX = 'effect/fx/pet/pet_yaodaoji_203_start_01_coco.sfx'
HIDE_MODEL_SFX = 'effect/fx/pet/pet_yaodaoji_203_end_01_coco.sfx'
MODEL_OPACITY = 0.3
THROWABLE_FLY_TIME = 0.5

class ComPetAppearance(ComAnimatorAppearance):
    DEFAULT_XML = 'animator_conf/pet.xml'
    BIND_EVENT = ComAnimatorAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REFRESH_MODEL': 'refresh_model',
       'E_REFRESH_MODEL_SCALE': 'refresh_model_scale',
       'G_PLAY_ANIM': '_play_anim',
       'G_ANIM_LEN_BY_KEY': 'get_anim_length_by_key',
       'G_ANIM_LEN_BY_NAME': 'get_anim_length_by_name',
       'G_IS_MY_PET': 'is_my_pet',
       'G_SKIN_ID': 'get_skin_id',
       'E_SET_LEVEL': 'set_level',
       'G_ANIM_INFO': 'get_anim_info',
       'G_LEVEL': 'get_level',
       'E_OWNER_INITED': 'bind_owner_event',
       'E_FOLLOW_TARGET_CHANGED': 'on_follow_target_changed',
       'E_FORCE_INVIS': 'on_force_invis',
       'E_BUFF_FROM_ME_TO_TARGET': 'shoot_throwable',
       'E_PET_LOD_CHANGED': 'on_lod_changed'
       })

    @property
    def owner_logic(self):
        if self._owner_logic:
            return self._owner_logic
        else:
            if self._owner_id:
                owner = EntityManager.getentity(self._owner_id)
                if owner:
                    self._owner_logic = owner.logic
                    return self._owner_logic
            return None

    def __init__(self):
        super(ComPetAppearance, self).__init__()
        self.cur_lod = None
        self.sub_models = {}
        self.need_lod_sub_models = set()
        self.bind_sfxs = {}
        self.mirror_sub_models = {}
        self.mirror_need_lod_sub_models = set()
        self.mirror_bind_sfxs = {}
        self.mirror_model = None
        self.animator_mirror = None
        self.owner_is_landed = False
        self.follow_target = None
        self.on_mecha = False
        self.model_trans = False
        self.force_invis = False
        self.last_anim_idx = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPetAppearance, self).init_from_dict(unit_obj, bdict)
        self._owner_logic = bdict.get('owner_logic', None)
        self._owner_id = bdict.get('owner_id', None)
        if not self._owner_logic:
            owner = EntityManager.getentity(self._owner_id)
            if owner:
                self._owner_logic = owner.logic
        self.skin_id = bdict.get('pet_id', None)
        self.level = bdict.get('level', 1)
        self.skin_conf = confmgr.get('c_pet_info', str(self.skin_id), default={})
        self.valid_socket_res = [ v for v in self.skin_conf.get('normal_res_info_list', []) if v if v.get('level', 1) <= self.level <= v.get('level_cap', 99) ]
        self.pet_valid_fix = not global_data.battle or bdict.get('pet_enemy_visible', False)
        self.pet_valid = True
        self.on_owner_camp_changed()
        self.sound_id = global_data.sound_mgr.register_game_obj('pet' + str(self.unit_obj.id))
        self.bind_owner_event(True)
        self.need_transparent = global_data.battle and self.is_my_pet() and global_data.player.get_setting(ENABLE_PET_TRANSPARENT)
        self.skill_throwable = self.skin_conf.get('skill_throwable', None)
        return

    def bind_owner_event(self, is_bind=True):
        if not self.owner_logic:
            return
        regist_func = self.owner_logic.regist_event if is_bind else self.owner_logic.unregist_event
        econf = {'E_PARACHUTE_STATUS_CHANGED': self.on_owner_parachute_stage_changed,
           'E_HIDE_PET_MODEL': self.hide_model,
           'E_SHOW_PET_MODEL': self.show_model,
           'E_DEATH': self.hide_model,
           'E_DEFEATED': self.hide_model,
           'E_SET_CAMP': (
                        self.on_owner_camp_changed, 99),
           'E_REFRESH_CAMP_SIDE_SHOW': (
                                      self.on_owner_camp_changed, 99),
           'E_ON_MOVIE_ANIM': self.on_owner_movie_anim
           }
        for event, func in six.iteritems(econf):
            if isinstance(func, (list, tuple)):
                func, priority = func
                if is_bind:
                    regist_func(event, func, priority)
                else:
                    regist_func(event, func)
            else:
                regist_func(event, func)

        world_econf = {global_data.emgr.player_revived: self.on_player_revived}
        for event, func in six.iteritems(world_econf):
            if is_bind:
                event += func
            else:
                event -= func

        self.on_owner_parachute_stage_changed(self.owner_logic.sd.ref_parachute_stage)

    def get_model_info(self, unit_obj, bdict):
        mpath = self.skin_conf.get('model_path', None)
        if not mpath:
            log_error('\xe5\xae\xa0\xe7\x89\xa9\xe6\xa8\xa1\xe5\x9e\x8b\xe8\xb7\xaf\xe5\xbe\x84\xe7\xbc\xba\xe5\xa4\xb1\xef\xbc\x81\xef\xbc\x81\xe6\xa3\x80\xe6\x9f\xa5220\xe8\xa1\xa8\xef\xbc\x81\xe7\x9a\xae\xe8\x82\xa4id:{}'.format(self.skin_id))
        udata = {'custom_model_name': 'player_pet' if self.is_my_pet() else 'player_pet_{}'.format(unit_obj.id),'custom_model_name_prefix': 'player_pet'
           }
        return (
         mpath, None, udata)

    def is_my_pet(self):
        if self._owner_id:
            if global_data.player and global_data.player.id == self._owner_id:
                return True
        elif global_data.lobby_player and self.owner_logic == global_data.lobby_player:
            return True
        return False

    def get_skin_id(self):
        return self.skin_id

    def on_load_model_complete(self, model, userdata):
        super(ComPetAppearance, self).on_load_model_complete(model, userdata)
        model.pickable = self.is_my_pet()
        self.send_event('E_PET_MODEL_LOADED', model, userdata)
        self.refresh_socket_res()
        self._play_anim('idle_anim')
        mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
        if mode_disp and mode_disp.get_reflect_rt():
            model_path = self.skin_conf.get('model_path', None)
            global_data.model_mgr.create_model(model_path, mesh_path_list=[model_path.replace('empty.gim', 'h.gim')], on_create_func=self.on_load_mirror_model_complete)
        else:
            self.refresh_model_scale()
        return

    def on_load_mirror_model_complete(self, mirror_model, *args):
        self.mirror_model = mirror_model
        self.refresh_socket_res(mirror=True)
        self.animator_mirror = animator.Animator(mirror_model, self.DEFAULT_XML, self.unit_obj)
        self.animator_mirror.Load(False, lambda *args: self.send_event('E_MIRROR_ANIMATOR_LOADED', self.animator_mirror))
        mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
        if mode_disp:
            mode_disp.add_model_to_mirror(self.model, mirror_model, True)
        self.refresh_model_scale()

    def refresh_socket_res(self, mirror=False):
        model = mirror and self.mirror_model if 1 else self.model
        if not model or not model.valid:
            return
        else:
            sub_models = self.mirror_sub_models if mirror else self.sub_models
            need_lod_sub_models = self.mirror_need_lod_sub_models if mirror else self.need_lod_sub_models
            bind_sfxs = self.mirror_bind_sfxs if mirror else self.bind_sfxs
            for bind_models in six.itervalues(sub_models):
                for bind_info in six.itervalues(bind_models):
                    bind_info['valid'] = False

            for bind_sfxs in six.itervalues(bind_sfxs):
                for bind_info in six.itervalues(bind_sfxs):
                    bind_info['valid'] = False

            valid_socket_res = self.valid_socket_res
            if valid_socket_res:
                self.cur_lod = self.ev_g_lod_level_name()
                if self.cur_lod:
                    self.cur_lod = '%s.gim' % self.cur_lod
                for res_info in valid_socket_res:
                    res_path = res_info.get('res_path', None)
                    if not res_path:
                        continue
                    if res_path.endswith('.gim'):
                        if res_path not in sub_models:
                            sub_models[res_path] = {}
                        need_lod = res_info.get('need_lod', False)
                        real_res_path = res_path
                        if need_lod:
                            if self.cur_lod:
                                real_res_path = res_path.replace('h.gim', self.cur_lod)
                            need_lod_sub_models.add(res_path)
                        socket_list = res_info.get('socket_list', [])
                        if socket_list:
                            for socket in socket_list:
                                if socket in sub_models[res_path]:
                                    sub_model = sub_models[res_path][socket]['model']
                                    if sub_model and sub_model.valid:
                                        sub_models[res_path][socket]['valid'] = True
                                        continue
                                    sub_models[res_path].pop(socket)
                                if not model.has_socket(socket):
                                    log_error('\xe5\xae\xa0\xe7\x89\xa9\xe5\xb0\x9d\xe8\xaf\x95\xe6\x8c\x82\xe6\x8e\xa5\xe5\xad\x90\xe6\xa8\xa1\xe5\x9e\x8b\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x81\xef\xbc\x81\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xef\xbc\x81sub_model:', res_path, 'socket:', socket)
                                    continue
                                sub_model = world.model(real_res_path, None)
                                model.bind(socket, sub_model)
                                sub_models[res_path][socket] = {'model': sub_model,'valid': True}

                        elif 'SUBMESH' in sub_models[res_path]:
                            sub_models[res_path]['SUBMESH']['valid'] = True
                        else:
                            model.add_mesh(real_res_path)
                            sub_models[res_path]['SUBMESH'] = {'valid': True}
                    elif res_path.endswith('.sfx'):
                        if res_path not in bind_sfxs:
                            bind_sfxs[res_path] = {}
                        socket_list = res_info.get('socket_list', [])
                        if socket_list:
                            for socket in socket_list:
                                if socket in bind_sfxs[res_path]:
                                    sfx_id = bind_sfxs[res_path][socket]['sfx_id']
                                    sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                                    if sfx:
                                        bind_sfxs[res_path][socket]['valid'] = True
                                        continue
                                    bind_sfxs[res_path].pop(socket)
                                if not model.has_socket(socket):
                                    log_error('\xe5\xae\xa0\xe7\x89\xa9\xe5\xb0\x9d\xe8\xaf\x95\xe6\x8c\x82\xe6\x8e\xa5\xe7\x89\xb9\xe6\x95\x88\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x81\xef\xbc\x81\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xef\xbc\x81sfx:', res_path, 'socket:', socket)
                                    continue
                                sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, on_create_func=lambda sfx: self.on_create_sfx_callback(sfx, mirror), on_remove_func=lambda sfx, rp=res_path, s=socket: self.on_remove_sfx_callback(sfx, rp, s, mirror))
                                bind_sfxs[res_path][socket] = {'sfx_id': sfx_id,'valid': True}

            for res_path in six_ex.keys(sub_models):
                bind_models = sub_models[res_path]
                for socket in six_ex.keys(bind_models):
                    if bind_models[socket]['valid']:
                        continue
                    if socket == 'SUBMESH':
                        model.remove_mesh(res_path)
                    else:
                        model.unbind(bind_models[socket]['model'])
                    bind_models.pop(socket)

            for res_path in six_ex.keys(bind_sfxs):
                bind_info = bind_sfxs[res_path]
                for socket in six_ex.keys(bind_info):
                    if bind_info[socket]['valid']:
                        continue
                    global_data.sfx_mgr.remove_sfx_by_id(bind_info[socket]['sfx_id'])

            return

    def on_lod_changed(self):
        cur_lod = self.ev_g_lod_level_name()
        if cur_lod == self.cur_lod:
            return
        self.switch_res_lod(cur_lod, False)
        self.switch_res_lod(cur_lod, True)
        self.cur_lod = cur_lod

    def switch_res_lod(self, lod_name, mirror):
        if mirror:
            model = self.mirror_model if 1 else self.model
            if not model or not model.valid:
                return
            need_lod_sub_models = self.mirror_need_lod_sub_models if mirror else self.need_lod_sub_models
            return need_lod_sub_models or None
        else:
            if mirror:
                sub_models = self.mirror_sub_models if 1 else self.sub_models
                return sub_models or None
            for res_path in need_lod_sub_models:
                if res_path not in sub_models:
                    continue
                old_res_path = res_path.replace('h.gim', self.cur_lod)
                new_res_path = old_res_path.replace('h.gim', lod_name)
                for socket, bind_info in six.iteritems(sub_models[res_path]):
                    if not bind_info['valid']:
                        continue
                    if socket == 'SUBMESH':
                        model.remove_mesh(old_res_path)
                        model.add_mesh(new_res_path)
                    else:
                        model.unbind(bind_info['model'])
                        sub_model = world.model(new_res_path, None)
                        model.bind(socket, sub_model)
                        bind_info['model'] = sub_model

            return

    def on_create_sfx_callback(self, sfx, mirror=False):
        model = mirror and self.mirror_model if 1 else self.model
        if not model or not model.valid:
            return
        visible = model.visible
        if visible ^ sfx.visible:
            sfx.visible = visible

    def on_remove_sfx_callback(self, sfx, res_path, socket, mirror=False):
        bind_sfxs = mirror and self.mirror_bind_sfxs if 1 else self.bind_sfxs
        if res_path not in bind_sfxs:
            return
        if socket not in bind_sfxs[res_path]:
            return
        bind_sfxs[res_path].pop(socket)

    def refresh_model_scale(self):
        if not self.model or not self.model.valid:
            return
        scale_type = 'mecha_scale' if self.on_mecha else 'human_scale'
        scale = self.skin_conf.get(scale_type, 1.0)
        scale_vec = math3d.vector(scale, scale, scale)
        self.model.scale = scale_vec
        if self.mirror_model:
            self.mirror_model.scale = scale_vec

    def _play_anim(self, anim_key, *args, **kwargs):
        anim_name, dir_type, anim_kwargs = self.get_anim_info(anim_key)
        if not anim_name:
            return
        else:
            if isinstance(anim_name, list):
                anim_idx = 0
                if anim_key in self.last_anim_idx:
                    anim_idx = self.last_anim_idx[anim_key]
                    anim_idx += 1
                    anim_idx %= len(anim_name)
                self.last_anim_idx[anim_key] = anim_idx
                anim_name = anim_name[anim_idx]
            self.send_event('E_POST_ACTION', anim_name, dir_type, **anim_kwargs)
            sound_conf = self.skin_conf.get('sound_conf', None)
            if sound_conf:
                sound_name = sound_conf.get(anim_key, None)
                if sound_name:
                    global_data.sound_mgr.post_event(sound_name, self.sound_id, pos=self.model.position)
            if kwargs.get('ret_len', False):
                return self.get_anim_length_by_name(anim_name)
            return

    def get_anim_info(self, anim_key, check_level=True):
        anim_info = self.skin_conf.get(anim_key, None)
        if not anim_info:
            return (None, None, None)
        else:
            if type(anim_info) == str:
                anim_info = [
                 anim_info, 1, {}]
            avaliable_level = anim_info[2].get('level', 1)
            if check_level and self.level < avaliable_level:
                return (None, None, None)
            return anim_info

    def get_anim_length_by_key(self, anim_key):
        anim_name, _, _ = self.get_anim_info(anim_key, False)
        if isinstance(anim_name, list):
            anim_name = anim_name[0]
        return self.get_anim_length_by_name(anim_name)

    def get_anim_length_by_name(self, anim_name):
        if self.model and self.model.valid and self.model.has_anim(anim_name):
            return self.model.get_anim_length(anim_name) / 1000.0
        return 0

    def refresh_model(self, force=False):
        if self.model:
            cur_mpath, _, userdata = self.get_model_info(self.unit_obj, None)
            if cur_mpath != self.model.filename.replace('\\', '/') or force:
                self.send_event('E_BEGIN_REFRESH_WHOLE_MODEL')
                self.sd.ref_is_refreshing_whole_model = True
                self._position = self._model.position
                model = world.model(cur_mpath, None)
                self._load_callback(model, userdata, self.use_idx)
                self.model.visible = True
        return

    def set_level(self, level):
        self.level = level
        self.refresh_model(True)
        self.valid_socket_res = {'normal_res_info_list': [ v for v in self.skin_conf.get('normal_res_info_list', []) if v and v.get('level', 1) <= self.level ]}

    def get_level(self):
        return self.level

    def on_owner_camp_changed(self, *args):
        if self.pet_valid_fix:
            return
        self.pet_valid = True
        if not self.pet_valid_fix and self._owner_id and global_data.cam_lplayer and not (global_data.cam_lplayer.id == self._owner_id or global_data.cam_lplayer.ev_g_is_campmate_by_eid(self._owner_id)):
            self.pet_valid = False
        self._set_model_visible(self.model_visible)

    def on_owner_movie_anim(self, parameter):
        if parameter['anim_name'] == 'mount':
            self.hide_model()

    def on_player_revived(self, player_id):
        if player_id == self._owner_id:
            self.show_model()

    def on_owner_parachute_stage_changed(self, parachute_stage):
        self.owner_is_landed = True if parachute_stage is None else bool(parachute_stage & PET_VISIBLE_STAGE)
        self._set_model_visible(self.model_visible)
        return

    def on_follow_target_state_changed(self, *args):
        if not self.follow_target_status_com:
            return
        cur_state = self.follow_target_status_com.set_st
        from logic.gcommon.cdata.status_config import ST_STAND, ST_CROUCH
        from logic.gcommon.cdata.mecha_status_config import MC_STAND
        if self.on_mecha:
            trans = len(cur_state) != 1 or MC_STAND not in cur_state
        else:
            trans = len(cur_state) != 1 or ST_STAND not in cur_state and ST_CROUCH not in cur_state
        self.set_model_transparent(trans)

    def on_follow_target_changed(self, follow_target, on_mecha):
        self.on_mecha = on_mecha
        if not self.need_transparent:
            return
        else:
            econf = {'E_ENTER_STATE': (
                               self.on_follow_target_state_changed, 99),
               'E_LEAVE_STATE': (
                               self.on_follow_target_state_changed, 99)
               }
            if self.follow_target:
                for event, (func, prio) in six.iteritems(econf):
                    self.follow_target.unregist_event(event, func)

            self.follow_target = follow_target
            self.follow_target_status_com = None
            if self.follow_target:
                for event, (func, prio) in six.iteritems(econf):
                    self.follow_target.regist_event(event, func, prio)

                self.follow_target_status_com = self.follow_target.get_com('ComStatusMechaClient' if on_mecha else 'ComStatusHuman')
            return

    def on_force_invis(self, invis):
        self.force_invis = invis
        self._set_model_visible(self.model_visible)

    def _set_model_visible(self, visible):
        self.model_visible = visible
        visible = self.pet_valid and not self.force_invis and self.owner_is_landed and not self._owner_logic.ev_g_death() and not self._owner_logic.ev_g_defeated() and visible
        if not self.model or not self.model.valid:
            return
        self.model.visible = visible
        for bind_models in six.itervalues(self.sub_models):
            for bind_info in six.itervalues(bind_models):
                if 'model' in bind_info:
                    bind_info['model'].visible = visible

        for bind_sfxs in six.itervalues(self.bind_sfxs):
            for bind_info in six.itervalues(bind_sfxs):
                sfx_id = bind_info['sfx_id']
                sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                if sfx:
                    sfx.visible = visible

        global_data.sfx_mgr.create_sfx_on_model(SHOW_MODEL_SFX if visible else HIDE_MODEL_SFX, self.model, 'fx_root')

    def set_model_transparent(self, trans):
        if not self.model or not self.model.valid:
            return
        if not self.model_trans ^ trans:
            return
        self.model_trans = trans
        opacity = MODEL_OPACITY if trans else 1.0
        if global_data.is_multi_pass_support:
            self.model.enable_prez_transparent(trans, opacity)
            for bind_models in six.itervalues(self.sub_models):
                for bind_info in six.itervalues(bind_models):
                    if 'model' in bind_info:
                        bind_info['model'].enable_prez_transparent(trans, opacity)

        elif global_data.feature_mgr.is_support_ext_tech_fix():
            int_op = int(opacity * 255)
            from logic.gutils.tech_pass_utils import set_prez_transparent
            set_prez_transparent(self.model, trans, int_op)
            for bind_models in six.itervalues(self.sub_models):
                for bind_info in six.itervalues(bind_models):
                    if 'model' in bind_info:
                        set_prez_transparent(bind_info['model'], trans, int_op)

        for bind_sfxs in six.itervalues(self.bind_sfxs):
            for bind_info in six.itervalues(bind_sfxs):
                sfx_id = bind_info['sfx_id']
                sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                if sfx:
                    sfx.alpha_percent = opacity

    def destroy(self):
        if self.mirror_model:
            self.animator_mirror.destroy()
            self.animator_mirror = None
            mode_disp = global_data.game_mgr.scene.get_com('PartMirror')
            if mode_disp:
                mode_disp.remove_model_from_mirror(self.model)
            global_data.model_mgr.remove_model(self.mirror_model)
            self.mirror_model = None
        if self.sound_id:
            global_data.sound_mgr.unregister_game_obj(self.sound_id)
            self.sound_id = None
        self.bind_owner_event(False)
        super(ComPetAppearance, self).destroy()
        return

    def shoot_throwable--- This code section failed: ---

 558       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'skill_throwable'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 559       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 560      13  LOAD_CONST            1  -1
          16  LOAD_CONST            2  ('NEOX_UNIT_SCALE',)
          19  IMPORT_NAME           1  'logic.gcommon.const'
          22  IMPORT_FROM           2  'NEOX_UNIT_SCALE'
          25  STORE_FAST            6  'NEOX_UNIT_SCALE'
          28  POP_TOP          

 561      29  LOAD_FAST             5  'data'
          32  LOAD_ATTR             3  'get'
          35  LOAD_CONST            3  'add_time'
          38  LOAD_CONST            4  ''
          41  CALL_FUNCTION_2       2 
          44  STORE_FAST            7  'add_time'

 562      47  LOAD_GLOBAL           4  'time_utility'
          50  LOAD_ATTR             5  'time'
          53  CALL_FUNCTION_0       0 
          56  STORE_FAST            8  'cur_time'

 563      59  LOAD_FAST             8  'cur_time'
          62  LOAD_FAST             7  'add_time'
          65  LOAD_GLOBAL           6  'THROWABLE_FLY_TIME'
          68  BINARY_ADD       
          69  COMPARE_OP            5  '>='
          72  POP_JUMP_IF_FALSE    79  'to 79'

 564      75  LOAD_CONST            0  ''
          78  RETURN_END_IF    
        79_0  COME_FROM                '72'

 565      79  LOAD_FAST             0  'self'
          82  LOAD_ATTR             7  'ev_g_position'
          85  CALL_FUNCTION_0       0 
          88  STORE_DEREF           0  'start_pos'

 566      91  LOAD_DEREF            0  'start_pos'
          94  POP_JUMP_IF_TRUE    101  'to 101'

 567      97  LOAD_CONST            0  ''
         100  RETURN_END_IF    
       101_0  COME_FROM                '94'

 568     101  LOAD_CONST            0  ''
         104  STORE_FAST            9  'target_mat'

 569     107  LOAD_FAST             1  'target'
         110  LOAD_ATTR             9  'ev_g_model'
         113  CALL_FUNCTION_0       0 
         116  STORE_FAST           10  'target_model'

 570     119  LOAD_FAST            10  'target_model'
         122  POP_JUMP_IF_FALSE   228  'to 228'
         125  LOAD_FAST            10  'target_model'
         128  LOAD_ATTR            10  'valid'
       131_0  COME_FROM                '122'
         131  POP_JUMP_IF_FALSE   228  'to 228'

 571     134  LOAD_FAST             1  'target'
         137  LOAD_ATTR            11  'sd'
         140  LOAD_ATTR            12  'ref_is_mecha'
         143  UNARY_NOT        
         144  POP_JUMP_IF_FALSE   186  'to 186'
         147  LOAD_FAST            10  'target_model'
         150  LOAD_ATTR            13  'has_socket'
         153  LOAD_CONST            5  'neck'
         156  CALL_FUNCTION_1       1 
       159_0  COME_FROM                '144'
         159  POP_JUMP_IF_FALSE   186  'to 186'

 572     162  LOAD_FAST            10  'target_model'
         165  LOAD_ATTR            14  'get_socket_matrix'
         168  LOAD_CONST            5  'neck'
         171  LOAD_GLOBAL          15  'world'
         174  LOAD_ATTR            16  'SPACE_TYPE_WORLD'
         177  CALL_FUNCTION_2       2 
         180  STORE_FAST            9  'target_mat'
         183  JUMP_ABSOLUTE       228  'to 228'

 573     186  LOAD_FAST            10  'target_model'
         189  LOAD_ATTR            13  'has_socket'
         192  LOAD_CONST            6  'part_point1'
         195  CALL_FUNCTION_1       1 
         198  POP_JUMP_IF_FALSE   228  'to 228'

 574     201  LOAD_FAST            10  'target_model'
         204  LOAD_ATTR            14  'get_socket_matrix'
         207  LOAD_CONST            6  'part_point1'
         210  LOAD_GLOBAL          15  'world'
         213  LOAD_ATTR            16  'SPACE_TYPE_WORLD'
         216  CALL_FUNCTION_2       2 
         219  STORE_FAST            9  'target_mat'
         222  JUMP_ABSOLUTE       228  'to 228'
         225  JUMP_FORWARD          0  'to 228'
       228_0  COME_FROM                '225'

 575     228  LOAD_FAST             9  'target_mat'
         231  POP_JUMP_IF_FALSE   246  'to 246'

 576     234  LOAD_FAST             9  'target_mat'
         237  LOAD_ATTR            17  'translation'
         240  STORE_DEREF           1  'end_pos'
         243  JUMP_FORWARD         35  'to 281'

 578     246  LOAD_FAST             1  'target'
         249  LOAD_ATTR            18  'ev_g_model_position'
         252  CALL_FUNCTION_0       0 
         255  LOAD_GLOBAL          19  'math3d'
         258  LOAD_ATTR            20  'vector'
         261  LOAD_CONST            4  ''
         264  LOAD_CONST            7  0.5
         267  LOAD_FAST             6  'NEOX_UNIT_SCALE'
         270  BINARY_MULTIPLY  
         271  LOAD_CONST            4  ''
         274  CALL_FUNCTION_3       3 
         277  BINARY_ADD       
         278  STORE_DEREF           1  'end_pos'
       281_0  COME_FROM                '243'

 579     281  LOAD_CLOSURE          1  'end_pos'
         284  LOAD_CLOSURE          0  'start_pos'
         290  LOAD_CONST               '<code_object set_sfx_rot>'
         293  MAKE_CLOSURE_0        0 
         296  STORE_FAST           11  'set_sfx_rot'

 584     299  LOAD_GLOBAL          21  'global_data'
         302  LOAD_ATTR            22  'sfx_mgr'
         305  LOAD_ATTR            23  'create_sfx_in_scene'
         308  LOAD_FAST             0  'self'
         311  LOAD_ATTR             0  'skill_throwable'
         314  LOAD_CONST            9  'on_create_func'
         317  LOAD_FAST            11  'set_sfx_rot'
         320  CALL_FUNCTION_257   257 
         323  STORE_FAST           12  'sfx_id'

 585     326  LOAD_GLOBAL          24  'hasattr'
         329  LOAD_GLOBAL          10  'valid'
         332  CALL_FUNCTION_2       2 
         335  POP_JUMP_IF_TRUE    350  'to 350'

 586     338  BUILD_MAP_0           0 
         341  LOAD_FAST             0  'self'
         344  STORE_ATTR           25  'throwable_dict'
         347  JUMP_FORWARD          0  'to 350'
       350_0  COME_FROM                '347'

 587     350  BUILD_MAP_3           3 

 588     353  LOAD_FAST             7  'add_time'
         356  LOAD_GLOBAL           6  'THROWABLE_FLY_TIME'
         359  BINARY_ADD       
         360  LOAD_CONST           11  'end_time'
         363  STORE_MAP        

 589     364  LOAD_DEREF            0  'start_pos'
         367  LOAD_CONST           12  'start_pos'
         370  STORE_MAP        

 590     371  LOAD_DEREF            1  'end_pos'
         374  LOAD_CONST           13  'end_pos'
         377  STORE_MAP        
         378  LOAD_FAST             0  'self'
         381  LOAD_ATTR            25  'throwable_dict'
         384  LOAD_FAST            12  'sfx_id'
         387  STORE_SUBSCR     

 592     388  LOAD_GLOBAL          24  'hasattr'
         391  LOAD_GLOBAL          14  'get_socket_matrix'
         394  CALL_FUNCTION_2       2 
         397  UNARY_NOT        
         398  POP_JUMP_IF_TRUE    411  'to 411'
         401  LOAD_FAST             0  'self'
         404  LOAD_ATTR            26  'throwable_timer'
         407  UNARY_NOT        
       408_0  COME_FROM                '398'
         408  POP_JUMP_IF_FALSE   441  'to 441'

 593     411  LOAD_GLOBAL          21  'global_data'
         414  LOAD_ATTR            27  'game_mgr'
         417  LOAD_ATTR            28  'register_logic_timer'
         420  LOAD_FAST             0  'self'
         423  LOAD_ATTR            29  'update_throwable'
         426  LOAD_CONST           15  1
         429  CALL_FUNCTION_2       2 
         432  LOAD_FAST             0  'self'
         435  STORE_ATTR           26  'throwable_timer'
         438  JUMP_FORWARD          0  'to 441'
       441_0  COME_FROM                '438'
         441  LOAD_CONST            0  ''
         444  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 332

    def update_throwable(self):
        cur_time = time_utility.time()
        remove_id = []
        for sfx_id, info in six.iteritems(self.throwable_dict):
            end_time = info.get('end_time', 0)
            if cur_time >= end_time:
                remove_id.append(sfx_id)
                continue
            if 'sfx' not in info:
                sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                if not sfx or not sfx.valid:
                    continue
                info['sfx'] = sfx
            sfx = info['sfx']
            elapsed_time = THROWABLE_FLY_TIME - end_time + cur_time
            sfx.position = info['start_pos'] + (info['end_pos'] - info['start_pos']) * (elapsed_time / THROWABLE_FLY_TIME)

        for sfx_id in remove_id:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
            del self.throwable_dict[sfx_id]