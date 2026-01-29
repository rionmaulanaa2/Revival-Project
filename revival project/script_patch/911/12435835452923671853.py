# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGrenadeAppearance.py
from __future__ import absolute_import
import six
from six.moves import range
from .ComBaseModelAppearance import ComBaseModelAppearance, RES_TYPE_MODEL, RES_TYPE_SFX
from common.cfg import confmgr
import weakref
import math3d
import world
from logic.gutils.dress_utils import get_mecha_model_path
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path
from logic.gcommon.common_const.weapon_const import WP_RAY_EXPLOSION_WEAPON_LIST
from logic.gutils.trick_bullet_utils import load_trick_bullet, destroy_real_bullet_model
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gcommon.const import HIT_PART_BODY, HIT_PART_TO_SOCKET_INDEX
from logic.gutils import weapon_skin_utils
from ext_package.ext_decorator import has_skin_ext
import random
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.client_unit_tag_utils import register_unit_tag
import os
ATTACH_UNIT_TAG_VALUE = register_unit_tag(('LMechaTrans', 'LMecha', 'LMechaRobot',
                                           'LMonster'))
MEHCA_8003_SUB_WEAPON_ID = {
 800302, 800303, 800304}

class ComGrenadeAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ADD_SFX': 'add_sfx',
       'E_ON_ATTACH_EXPLOSIVE': 'attach_mecha',
       'E_ON_PLAY_HIT_SFX': 'play_hit_sfx'
       })
    PICK_CONF_PATH = 'grenade_config'

    def __init__(self):
        super(ComGrenadeAppearance, self).__init__()
        self.object_conf = None
        self.item_id = None
        self.appearance_type = RES_TYPE_MODEL
        self.replace_sfx_id = None
        self.replace_sfx = None
        self.attached_mecha_model_ref = None
        self.attached_mecha_unit = None
        self.process_event(True)
        self.extra_sfx_id_list = []
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'app_resume_event': self.on_app_resume
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComGrenadeAppearance, self).init_from_dict(unit_obj, bdict)
        self.faction_id = bdict.get('faction_id', 0)
        if has_skin_ext():
            self._skin_id = bdict.get('skin_id', None)
            self._shiny_weapon_id = bdict.get('shiny_weapon_id', None)
        else:
            self._skin_id, self._shiny_weapon_id = (None, None)
        self._forward = bdict.get('dir', [1, 0, 0])
        if self._forward is None:
            self._forward = [
             1, 0, 0]
        self._forward = math3d.vector(*self._forward)
        self.rot_while_moving = confmgr.get('grenade_res_config', str(bdict['item_itype']), 'cCustomParam', 'rot_while_moving', default=0)
        self.last_position = self._position
        self.accumulate_rate = bdict.get('accumulate_rate', 0.0)
        self._model_path = None
        self._use_trick_bullet = False
        self._unique_key = bdict['uniq_key']
        self._owner_id = bdict['owner_id']
        self.replace_sfx_id = None
        self.replace_sfx = None
        self.attached_mecha_model_ref = None
        self.attached_mecha_unit = None
        self.attach_socket_name = 'part_point1'
        self.attach_position_offset = math3d.vector(0, 0, 0)
        self.attach_transformation = None
        self.need_update = self.rot_while_moving
        self.extra_sfx_id_list = []
        self.bind_sfx_count = bdict.get('bind_sfx_count', 0)
        return

    def _remove_extra_sfxes(self):
        for sfx_id in self.extra_sfx_id_list:
            global_data.bullet_sfx_mgr.remove_sfx_by_id(sfx_id)

        del self.extra_sfx_id_list[:]

    def cache(self):
        self._destroy_model()
        super(ComGrenadeAppearance, self).cache()
        self.object_conf = None
        self.item_id = None
        self.attached_mecha_model_ref = None
        self.attached_mecha_unit = None
        self.appearance_type = RES_TYPE_MODEL
        return

    def get_model_info(self, unit_obj, bdict):
        item_id = bdict['item_itype']
        self.item_id = item_id
        if confmgr.get('firearm_config', str(item_id), 'iKind') in WP_RAY_EXPLOSION_WEAPON_LIST:
            return (None, None, None)
        else:
            m_pos = bdict.get('m_position')
            if m_pos:
                pos = m_pos if 1 else bdict.get('position', [0, 0, 0])
                direction = bdict.get('dir', [0, 0, 1])
                up = bdict.get('up', [0, 1, 0])
                if not up:
                    up = [
                     0, 1, 0]
                self.object_conf = confmgr.get(self.PICK_CONF_PATH, str(item_id), default=None)
                is_enemy = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != self.faction_id
                grenade_res_conf = confmgr.get('grenade_res_config', str(item_id), default={})
                model_path = grenade_res_conf.get('cRes', None)
                if is_enemy:
                    model_path = grenade_res_conf.get('cEnemyRes', model_path)
                if grenade_res_conf.get('cCustomParam', {}).get('use_relative_path', False):
                    skin_model_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(self._skin_id), 'model_path', default='')
                    if not skin_model_path:
                        try:
                            mecha_id = str(item_id)[:4]
                            skin_model_path = get_mecha_model_path(mecha_id, None, None)
                        except:
                            pass

                    if skin_model_path:
                        model_path = os.path.dirname(skin_model_path) + '/' + model_path
                else:
                    skin_model_path = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, item_id, 'cRes')
                    if skin_model_path:
                        model_path = skin_model_path
                        if is_enemy:
                            model_path = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, item_id, 'cEnemyRes', default=model_path)
                    skin_model_path = weapon_skin_utils.get_weapon_skin_grenade_weapon_sfx_path(self._skin_id, 'cRes')
                    if skin_model_path:
                        model_path = skin_model_path
                model_path = model_path or 'model_new/mecha/8001/8001/empty.gim'
            if model_path.endswith('.sfx'):
                self.load_res_func = self.load_sfx
                self.appearance_type = RES_TYPE_SFX
                sfx_diff = confmgr.get('grenade_res_config', str(self.item_id), 'cCustomParam', 'camp_diff', default=0)
                self._sfx_ex_data = {'need_diff_process': sfx_diff and is_enemy}
            else:
                self._sfx_ex_data = {}
            self._model_path = model_path
            return (
             model_path, None, (pos, direction, up))

    def _hide_bullet(self):
        if self.model and self.model.valid:
            self.model.visible = False

    def on_load_model_complete(self, model, userdata):
        pos, direction, up = userdata
        pos = math3d.vector(*pos)
        if direction:
            direction = math3d.vector(*direction)
        else:
            direction = math3d.vector(0, 0, 1)
        up = math3d.vector(*up)
        if up.is_zero:
            up = math3d.vector(0, 1, 0)
        if direction.is_zero:
            direction = math3d.vector(0, 0, 1)
        model.set_placement(pos, direction, up)
        res_config = confmgr.get('grenade_res_config', str(self.item_id), default={})
        scale = res_config.get('fBulletSfxScale')
        if scale:
            model.scale = math3d.vector(scale, scale, scale)
        res_custom_param = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, self.item_id, 'cCustomParam', default={}) or res_config.get('cCustomParam', {})
        for socket, sfx_path in res_custom_param.get('sfx_info', []):
            self.extra_sfx_id_list.append(global_data.bullet_sfx_mgr.create_sfx_on_model(sfx_path, model, socket))

        ex_sfx_info = res_custom_param.get('ex_sfx_info', {})
        if ex_sfx_info:
            bind_sfx_count = self.bind_sfx_count or ex_sfx_info.get('bind_sfx_count', 1)
            bind_sfx_socket = ex_sfx_info.get('bind_socket', 'sword_{}')
            bind_sfx_path = ex_sfx_info.get('bind_sfx_path', 'effect/fx/robot/robot_qishi/robot_qishi_jianqi.sfx')
            for i in range(bind_sfx_count):
                self.extra_sfx_id_list.append(global_data.bullet_sfx_mgr.create_sfx_on_model(bind_sfx_path, model, bind_sfx_socket.format(i + 1)))

        if not global_data.battle:
            return
        owner_entity = global_data.battle.get_entity(self._owner_id)
        if not owner_entity:
            return
        unit = owner_entity.logic
        if not unit.is_valid():
            return
        conf = confmgr.get('grenade_config', str(self.item_id), 'cCustomParam', default={})
        add_rate = conf.get('max_acc_add_radius_rate', 0.0) * self.accumulate_rate
        if res_custom_param.get('apply_col_radius_rate_to_sfx_scale', False):
            add_rate += self.ev_g_col_radius_rate()
        model.scale *= 1 + add_rate
        trick_bullet_count = conf.get('trick_bullet_count', 0)
        if trick_bullet_count > 0:
            if global_data.cam_lplayer and global_data.cam_lplayer.id == unit.share_data.ref_driver_id:
                scale_rate = 1.0
            else:
                scale_rate = conf.get('scale_others', 1.0)
            scale_rate += add_rate
            self._use_trick_bullet = True
            if 'min_scale_range' in conf:
                scale_data_list = []
                for i in range(trick_bullet_count + 1):
                    min_v = random.uniform(*conf['min_scale_range']) * scale_rate
                    max_v = min_v + random.uniform(*conf['add_scale_range']) * scale_rate
                    scale_data_list.append([min_v, max_v, conf['scale_up_duration']])

            else:
                scale_data_list = [ [1.0 * scale_rate, 1.0 * scale_rate, 0.0] for i in range(trick_bullet_count + 1) ]
            interval = confmgr.get('firearm_config', str(self.item_id), 'fCDTime')
            interval /= trick_bullet_count + 1
            skin_sfx_dict = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, self.item_id, 'cCustomParam')
            if skin_sfx_dict:
                trick_bullet_sfx = skin_sfx_dict.get('trick_bullet_sfx', self._model_path)
            else:
                trick_bullet_sfx = conf.get('trick_bullet_sfx', self._model_path)
            weapon_pos = conf.get('weapon_pos', PART_WEAPON_POS_MAIN1)
            load_trick_bullet(self._unique_key, model, trick_bullet_count, trick_bullet_sfx, interval, scale_data_list, unit, weapon_pos)
        if self.attached_mecha_unit:
            self._hide_bullet()
            self.change_sfx()

    def tick(self, dt):
        if self.attached_mecha_unit and self.attached_mecha_unit.is_valid():
            mecha_model = self.attached_mecha_model_ref()
            if not mecha_model.visible:
                cur_mecha_model = self.attached_mecha_unit.ev_g_model()
                if not cur_mecha_model:
                    return
                self.attached_mecha_model_ref = weakref.ref(cur_mecha_model)
                if self.replace_sfx and self.replace_sfx.valid:
                    self.replace_sfx.remove_from_parent()
                    cur_mecha_model.bind(self.attach_socket_name, self.replace_sfx, world.BIND_TYPE_ALL)
                    self.replace_sfx.position = self.attach_position_offset
                    self.replace_sfx.transformation = self.attach_transformation
                    self.replace_sfx.visible = True
        if self.rot_while_moving and self.model and self.model.valid:
            cur_pos = self.model.position
            move_vec = cur_pos - self.last_position
            if not move_vec.is_zero:
                move_vec.normalize()
                self._forward = move_vec
                self.model.rotation_matrix = math3d.matrix.make_orient(self._forward, math3d.vector(0, 1, 0))
            self.last_position = cur_pos

    def attach_mecha(self, mecha_model, item_info, unit_obj):
        if unit_obj.MASK & ATTACH_UNIT_TAG_VALUE == 0:
            return
        else:
            extra_info = item_info.get('extra_info')
            final_part = HIT_PART_BODY
            is_right = True
            if extra_info:
                for part_info in six.itervalues(extra_info):
                    part = part_info.get('part')
                    if part is None:
                        continue
                    if part != HIT_PART_BODY:
                        final_part = part
                        is_right = part_info.get('is_right', True)
                        break

            socket_indexs = HIT_PART_TO_SOCKET_INDEX.get(final_part)
            socket_name = 'part_point%d' % (socket_indexs[0] if is_right else socket_indexs[1])
            if not mecha_model.has_socket(socket_name):
                socket_name = 'part_point1'
            self.attached_mecha_model_ref = weakref.ref(mecha_model)
            self.attached_mecha_unit = unit_obj
            self.attach_position_offset = math3d.vector(random.randint(-2, 2), random.randint(-2, 2), random.randint(-2, 2))
            forward = math3d.vector(*item_info['rot_euler'])
            forward.normalize()
            sock_mat = mecha_model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
            sock_mat.inverse()
            mat = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
            self.attach_transformation = mat * sock_mat.rotation
            self._hide_bullet()
            self.change_sfx()
            if unit_obj.sd.ref_second_model_dir:
                self.need_update = True
            return

    def _refresh_replace_sfx_appearance(self, sfx):
        if not sfx.valid:
            return False
        if self.attached_mecha_unit:
            attached_mecha_model = self.attached_mecha_unit.ev_g_model()
            if attached_mecha_model and attached_mecha_model.valid:
                sfx.remove_from_parent()
                sfx.inherit_flag &= ~world.INHERIT_SCALE
                attached_mecha_model.bind(self.attach_socket_name, sfx, world.BIND_TYPE_ALL)
                sfx.position = self.attach_position_offset
                sfx.transformation = self.attach_transformation
                return True
        if self.model:
            sfx.remove_from_parent()
            self.scene.add_object(sfx)
            sfx.inherit_flag = self.model.inherit_flag
            sfx.world_position = self.model.position
            sfx.world_transformation = self.model.transformation
            return True
        return False

    def change_sfx(self):
        if self.replace_sfx:
            self._refresh_replace_sfx_appearance(self.replace_sfx)
            return
        else:
            if self.replace_sfx_id:
                return
            custom_data = confmgr.get('grenade_res_config', str(self.item_id), 'cCustomParam', default={})
            if custom_data and custom_data.get('attach_model'):

                def create_cb(sfx):
                    if self._refresh_replace_sfx_appearance(sfx):
                        self.replace_sfx = sfx
                    else:
                        global_data.bullet_sfx_mgr.remove_sfx(sfx)

                sfx_diff = custom_data.get('camp_diff', 0)
                ex_data = {'need_diff_process': sfx_diff and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != self.faction_id}
                attach_model_path = custom_data.get('attach_model')
                skin_custom_data = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, self.item_id, 'cCustomParam')
                if skin_custom_data and 'attach_model' in skin_custom_data:
                    attach_model_path = skin_custom_data['attach_model']
                init_pos = self.model.position if self.model else None
                self.replace_sfx_id = global_data.bullet_sfx_mgr.create_sfx_in_scene(attach_model_path, on_create_func=create_cb, ex_data=ex_data, int_check_type=CREATE_SRC_SIMPLE, int_check_pos=init_pos)
            return

    def play_hit_sfx(self, attach_unit):
        custom_data = confmgr.get('grenade_res_config', str(self.item_id), 'cCustomParam')
        if custom_data and custom_data.get('hit_sfx'):

            def create_cb(sfx):
                if custom_data.get('show_hit_dir', 0):
                    forward = -self._forward
                    m_mat = sfx.world_rotation_matrix
                    sfx.world_rotation_matrix = m_mat.make_rotation_x(forward.pitch) * m_mat.make_rotation_y(forward.yaw)

            hit_sfx = custom_data.get('hit_sfx')
            skin_custom_data = get_mecha_skin_grenade_weapon_sfx_path(self._skin_id, self._shiny_weapon_id, self.item_id, 'cCustomParam')
            if skin_custom_data and 'hit_sfx' in skin_custom_data:
                hit_sfx = skin_custom_data['hit_sfx']
            sfx_diff = custom_data.get('camp_diff', 0)
            ex_data = {'need_diff_process': sfx_diff and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != self.faction_id}
            pos = None
            if self.model:
                pos = self.model.world_position
            elif self.sd.ref_col_obj:
                pos = self.sd.ref_col_obj.position
            pos and global_data.bullet_sfx_mgr.create_sfx_in_scene(hit_sfx, pos=pos, on_create_func=create_cb, ex_data=ex_data, int_check_type=CREATE_SRC_SIMPLE)
        if attach_unit and attach_unit.is_valid():
            attach_unit.send_event('E_ATTACH_BY_GRENADE', self._owner_id)
        self._hide_bullet()
        self.change_sfx()
        return

    def _remove_replace_sfx(self):
        if self.replace_sfx_id:
            global_data.bullet_sfx_mgr.remove_sfx_by_id(self.replace_sfx_id)
            self.replace_sfx_id = None
            self.replace_sfx = None
        return

    def _destroy_model(self):
        self._remove_extra_sfxes()
        sfx = self.get_model()
        if sfx and self.appearance_type == RES_TYPE_SFX:
            self._model = None
            if self._use_trick_bullet:
                destroy_real_bullet_model(self._unique_key, str(sfx))
                global_data.bullet_sfx_mgr.shutdown_sfx(sfx)
            elif sfx.visible:
                import game3d
                from common.framework import Functor
                func = Functor(global_data.bullet_sfx_mgr.shutdown_sfx, sfx)
                game3d.delay_exec(40, func)
            else:
                global_data.bullet_sfx_mgr.remove_sfx(sfx)
        self._remove_replace_sfx()
        return

    def on_app_resume(self):
        self._remove_replace_sfx()

    def destroy(self):
        self.attached_mecha_unit = None
        self.attached_mecha_model_ref = None
        self._destroy_model()
        super(ComGrenadeAppearance, self).destroy()
        self.process_event(False)
        return