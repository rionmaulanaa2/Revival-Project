# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrajectoryAppearance.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.weapon_const import BULLET_RIFLE_TYPE, BULLET_SNIPPER_TYPE, BULLET_LASER_TYPE, BULLET_END_POSITION_TYPE, WP_RAY_GRENADES_GUN, WP_AIM_RAY_GRENADES_GUN
from logic.gutils.firearm_sfx_mapping_utils import check_sfx_mapping_initialized, encode_sfx_info, decode_sfx_info, get_correspond_sfx_info_for_ai
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
from logic.gutils.frame_data_utils import filter_duplicated_execution_with_arg_key
from common.utils.sfxmgr import CREATE_SRC_OTHER_SYNC, CREATE_SRC_OTHER_SYNC_FREQUENT, CREATE_SRC_OTHER_SYNC_SHOTGUN
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
import logic.gcommon.common_utils.bcast_utils as bcast
import exception_hook
import world
import math3d
import random
MAX_TRAJECTORY_SFX_PER_TYPE = 4
MIN_SHOW_TRAJ_LEN = 10 * NEOX_UNIT_SCALE
MAX_SHOW_TRAJ_LEN = 1000 * NEOX_UNIT_SCALE
MECHA_VEHICLE_SEAT_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMechaTrans', 'LMotorcycle', 'LSeat'))
CHECK_TYPE_MAP = {801001: CREATE_SRC_OTHER_SYNC_FREQUENT,
   801002: CREATE_SRC_OTHER_SYNC_FREQUENT,
   801003: CREATE_SRC_OTHER_SYNC_FREQUENT,
   10323: CREATE_SRC_OTHER_SYNC_SHOTGUN,
   10324: CREATE_SRC_OTHER_SYNC_SHOTGUN,
   800902: CREATE_SRC_OTHER_SYNC_SHOTGUN,
   800905: CREATE_SRC_OTHER_SYNC_SHOTGUN,
   801805: CREATE_SRC_OTHER_SYNC_SHOTGUN,
   801806: CREATE_SRC_OTHER_SYNC_SHOTGUN
   }
SYNC_FREQUENCY_LIMIT = {1011: 0.1,
   10031: 0.1,
   10032: 0.1,
   10033: 0.1,
   10041: 0.1,
   10042: 0.1,
   10043: 0.1,
   800101: 0.12,
   801001: 0.1,
   801002: 0.1,
   801003: 0.1,
   801401: 0.12
   }
RELATIONSHIP_AVATAR = 0
RELATIONSHIP_GROUPMATE = 1
RELATIONSHIP_ENEMY = 2
RAY_GRENADE_WEAPON_TYPES = {
 WP_RAY_GRENADES_GUN, WP_AIM_RAY_GRENADES_GUN}

class ComTrajectoryAppearance(UnitCom):
    BIND_EVENT = {'E_ON_DRIVER_CHANGE': 'on_driver_change',
       'E_REFRESH_MODEL': 'on_refresh_skin_and_shiny_weapon_id',
       'E_SHOW_MINE_TRAJECTORY': 'on_show_mine_trajectory',
       'E_SHOW_SYNC_TRAJECTORY': 'on_show_sync_trajectory',
       'E_SHOW_MINE_SOCK_TRAJECTORY': 'on_show_mine_sock_trajectory',
       'E_SHOW_SYNC_SOCK_TRAJECTORY': 'on_show_sync_sock_trajectory',
       'E_SHOW_AI_SHOOT': 'on_show_ai_shoot_trajectory'
       }

    def __init__(self):
        super(ComTrajectoryAppearance, self).__init__()
        self._cur_tick = 0
        self._cur_weapon_side = 0
        self._rifle_traj_cfg_list = []
        self.owner_id = None
        self.relationship = RELATIONSHIP_ENEMY
        self.skin_id, self.shiny_weapon_id = (None, None)
        self.cache_config = {}
        self.need_trajectory_tick = {}
        self.last_sync_time = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrajectoryAppearance, self).init_from_dict(unit_obj, bdict)
        check_sfx_mapping_initialized()
        self.cache_config = {}
        self.need_trajectory_tick = {}
        self.sd.ref_aim_model = None
        self.sd.update_aim_model_trans_func = None
        return

    def on_init_complete(self):
        self.refresh_owner_id()
        self.on_refresh_skin_and_shiny_weapon_id()
        self.refresh_relationship(global_data.cam_lplayer)
        global_data.emgr.scene_observed_player_setted_event += self.refresh_relationship

    def tick(self, dt):
        self._update_rifle_traj()

    def destroy(self):
        self.sd.ref_aim_model = None
        self.sd.update_aim_model_trans_func = None
        global_data.emgr.scene_observed_player_setted_event -= self.refresh_relationship
        self.cache_config = {}
        self.need_trajectory_tick = {}
        remove_sfx = global_data.bullet_sfx_mgr.remove_sfx
        for cfg in self._rifle_traj_cfg_list:
            remove_sfx(cfg.sfx)

        self._rifle_traj_cfg_list = []
        super(ComTrajectoryAppearance, self).destroy()
        return

    @staticmethod
    def _get_lentity_owner_id(lentity):
        mask = lentity.MASK
        if mask & MECHA_VEHICLE_SEAT_TAG_VALUE:
            return lentity.share_data.ref_driver_id
        else:
            if mask & preregistered_tags.HUMAN_TAG_VALUE:
                return lentity.id
            print('============= \xe5\xbe\x85\xe9\xaa\x8c\xe8\xaf\x81class', lentity.__class__.__name__)
            return lentity.id

    def refresh_owner_id(self):
        self.owner_id = self._get_lentity_owner_id(self.unit_obj)

    def on_driver_change(self, new_driver_id):
        self.owner_id = new_driver_id

    def on_refresh_skin_and_shiny_weapon_id(self):
        skin_and_shiny_weapon_id = self.ev_g_mecha_skin_and_shiny_weapon_id()
        if skin_and_shiny_weapon_id:
            self.skin_id, self.shiny_weapon_id = skin_and_shiny_weapon_id

    def refresh_relationship(self, new_cam_lplayer):
        if new_cam_lplayer:
            cam_lplayer_owner_id = self._get_lentity_owner_id(new_cam_lplayer)
            if cam_lplayer_owner_id == self.owner_id:
                self.relationship = RELATIONSHIP_AVATAR
            else:
                groupmate = self.ev_g_groupmate()
                if groupmate and cam_lplayer_owner_id in groupmate:
                    self.relationship = RELATIONSHIP_GROUPMATE
                else:
                    my_camp_id = self.ev_g_camp_id()
                    if my_camp_id is not None and my_camp_id == new_cam_lplayer.ev_g_camp_id():
                        self.relationship = RELATIONSHIP_GROUPMATE
                    else:
                        self.relationship = RELATIONSHIP_ENEMY
        else:
            self.relationship = RELATIONSHIP_ENEMY
        return

    def on_show_mine_trajectory(self, wp_type, src_pos=None, tar_pos=None, accumulate_level=0, sfx_path=None, sync_sfx_path=None, sfx_scale=1.0):
        if not tar_pos:
            return
        try:
            src_pos = src_pos or self._get_traj_src_pos(tar_pos)
            if not src_pos or not tar_pos or (tar_pos - src_pos).length < MIN_SHOW_TRAJ_LEN:
                return
        except TypeError as e:
            exception_hook.post_stack('[TRACE] TypeError src_pos:{} type:{}; tar_pos:{} type{}'.format(src_pos, type(src_pos), tar_pos, type(tar_pos)))
            return

        self._show_trajectory(wp_type, src_pos, tar_pos, sfx_path, sfx_scale=sfx_scale, is_mine=True)
        sfx_code = encode_sfx_info(sync_sfx_path, sfx_scale)
        sync_src_pos = (src_pos.x, src_pos.y, src_pos.z)
        sync_tar_pos = (tar_pos.x, tar_pos.y, tar_pos.z)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_SYNC_TRAJECTORY, (wp_type, sync_src_pos, sync_tar_pos, accumulate_level, sfx_code)])

    def on_show_sync_trajectory(self, wp_type, src_pos, tar_pos, accumulate_level, sfx_code):
        if wp_type in SYNC_FREQUENCY_LIMIT and self.relationship != RELATIONSHIP_AVATAR:
            cur_time = global_data.game_time
            if cur_time - self.last_sync_time.get(wp_type, 0.0) < SYNC_FREQUENCY_LIMIT[wp_type]:
                return
            self.last_sync_time[wp_type] = cur_time
        src_pos = math3d.vector(*src_pos)
        tar_pos = math3d.vector(*tar_pos)
        sfx_path, sfx_scale = decode_sfx_info(sfx_code)
        self._show_trajectory(wp_type, src_pos, tar_pos, sfx_path, sfx_scale=sfx_scale, is_mine=False)

    def on_show_mine_sock_trajectory(self, wp_type, socket_name=None, tar_pos=None, accumulate_level=0, sfx_path=None, sync_sfx_path=None, sfx_scale=1.0):
        if not tar_pos:
            return
        else:
            src_pos = self._get_traj_src_pos_by_socket(socket_name, None)
            if not src_pos or (tar_pos - src_pos).length < MIN_SHOW_TRAJ_LEN:
                return
            self._show_trajectory(wp_type, src_pos, tar_pos, sfx_path, sfx_scale=sfx_scale, socket_name=socket_name, side=self._cur_weapon_side, is_mine=True)
            sfx_code = encode_sfx_info(sync_sfx_path, sfx_scale)
            sync_tar_pos = (tar_pos.x, tar_pos.y, tar_pos.z)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_SYNC_SOCK_TRAJECTORY, (wp_type, socket_name, sync_tar_pos, accumulate_level, sfx_code)])
            return

    def on_show_sync_sock_trajectory(self, wp_type, socket_name, tar_pos, accumulate_level, sfx_code):
        if wp_type in SYNC_FREQUENCY_LIMIT and self.relationship != RELATIONSHIP_AVATAR:
            cur_time = global_data.game_time
            if cur_time - self.last_sync_time.get(wp_type, 0.0) < SYNC_FREQUENCY_LIMIT[wp_type]:
                return
            self.last_sync_time[wp_type] = cur_time
        tar_pos = math3d.vector(*tar_pos)
        src_pos = self._get_traj_src_pos_by_socket(socket_name, None)
        if not src_pos or (tar_pos - src_pos).length < MIN_SHOW_TRAJ_LEN:
            return
        else:
            sfx_path, sfx_scale = decode_sfx_info(sfx_code)
            self._show_trajectory(wp_type, src_pos, tar_pos, sfx_path, sfx_scale=sfx_scale, socket_name=socket_name)
            return

    def on_show_ai_shoot_trajectory(self, tar_id, is_hit, air_pos):
        wp_type = self.ev_g_weapon_type()
        if not wp_type:
            return
        tar_ent = EntityManager.getentity(tar_id)
        if not (tar_ent and tar_ent.logic):
            return
        if air_pos:
            tar_pos = math3d.vector(*air_pos)
        else:
            model = tar_ent.logic.ev_g_model()
            if not model or not model.valid:
                tar_pos = tar_ent.logic.ev_g_position()
            elif is_hit:
                tar_pos = model.center_w
            else:
                tar_pos = model.center_w
                radius = model.bounding_radius
                rparm = [ random.uniform(0.5, 1) * random.choice([-1, 1]) * radius for i in range(3) ]
                tar_pos += math3d.vector(*rparm)
        if not tar_pos:
            return
        src_pos = self.ev_g_trajectory_start_point()
        if not src_pos or (tar_pos - src_pos).length < MIN_SHOW_TRAJ_LEN:
            return
        sfx_path, sync_sfx_path, sfx_scale = get_correspond_sfx_info_for_ai(wp_type)
        self._show_trajectory(wp_type, src_pos, tar_pos, sfx_path, sfx_scale=sfx_scale, is_mine=False)
        sfx_code = encode_sfx_info(sync_sfx_path, sfx_scale)
        sync_src_pos = (src_pos.x, src_pos.y, src_pos.z)
        sync_tar_pos = (tar_pos.x, tar_pos.y, tar_pos.z)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_SYNC_TRAJECTORY, (wp_type, sync_src_pos, sync_tar_pos, 0, sfx_code)])

    def _get_traj_src_pos(self, tar_pos):
        src_pos = self.ev_g_get_fire_pos()
        if not src_pos:
            src_pos = self.ev_g_aim_position()
            if not src_pos:
                return
            traj_vector = tar_pos - src_pos
            if not traj_vector.is_zero:
                traj_vector.normalize()
                src_pos = src_pos + traj_vector * NEOX_UNIT_SCALE
        return src_pos

    @filter_duplicated_execution_with_arg_key(2)
    def _get_traj_src_pos_by_socket(self, socket_name, weapon_side):
        src_pos = None
        if self.sd.ref_is_mecha:
            model = self.sd.ref_aim_model
            if not model:
                model = self.ev_g_model()
            elif self.sd.update_aim_model_trans_func:
                self.sd.update_aim_model_trans_func()
            if model:
                matrix = model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
                if matrix:
                    src_pos = matrix.translation
        elif self.unit_obj is global_data.cam_lplayer and global_data.cam_model:
            trans = global_data.emgr.get_aim_gun_fire_matrix.emit()
            if trans:
                src_pos = trans[0]
        else:
            weapon_model = None
            if weapon_side is not None:
                cur_weapon_side = weapon_side
            else:
                cur_weapon_side = self._cur_weapon_side
            if cur_weapon_side == 1:
                weapon_model = self.sd.ref_left_hand_weapon_model
            if not weapon_model:
                weapon_model = self.sd.ref_hand_weapon_model
            if weapon_side is None:
                self._cur_weapon_side = (self._cur_weapon_side + 1) % 2
            if weapon_model:
                matrix = weapon_model.get_socket_matrix('kaihuo', world.SPACE_TYPE_WORLD)
                if matrix:
                    src_pos = matrix.translation
        return src_pos

    def _show_trajectory(self, wp_type, src_pos, tar_pos, sfx_path, sfx_scale=1.0, socket_name=None, side=None, is_mine=False):
        if src_pos is None or tar_pos is None:
            return
        else:
            length = (tar_pos - src_pos).length
            if length < MIN_SHOW_TRAJ_LEN or length > MAX_SHOW_TRAJ_LEN:
                return
            if wp_type in self.cache_config:
                traj_type, speed, acc_speed, camp_diff = self.cache_config[wp_type]
            else:
                res_conf = confmgr.get('firearm_res_config', str(wp_type))
                traj_type = res_conf['cSfxBulletFlyingType']
                weapon_kind = confmgr.get('firearm_config', str(wp_type), 'iKind')
                speed = res_conf.get('cSfxBulletSpeed', 200)
                acc_speed = res_conf.get('cSfxBulletAccSpeed', 100000)
                if weapon_kind in RAY_GRENADE_WEAPON_TYPES:
                    self.need_trajectory_tick[wp_type] = not res_conf.get('cExtraParam', {}).get('ignore_trajectory_tick', True)
                else:
                    self.need_trajectory_tick[wp_type] = True
                camp_diff = res_conf.get('cExtraParam', {}).get('camp_diff', 0)
                self.cache_config[wp_type] = (traj_type, speed, acc_speed, camp_diff)
            ex_data = {'need_diff_process': camp_diff and self.relationship == RELATIONSHIP_ENEMY
               }
            sfx_mgr = global_data.bullet_sfx_mgr

            def create_cb(sfx):
                if not self.is_valid():
                    sfx_mgr.remove_sfx(sfx)
                    return
                if traj_type == BULLET_RIFLE_TYPE:
                    self._on_create_rifle_traj(sfx, speed, acc_speed, src_pos, tar_pos, socket_name, side, sfx_scale, self.need_trajectory_tick[wp_type])
                elif traj_type == BULLET_SNIPPER_TYPE:
                    self._on_create_snipper_traj(sfx, src_pos, tar_pos)
                elif traj_type in (BULLET_LASER_TYPE, BULLET_END_POSITION_TYPE):
                    self._on_create_laser_traj(sfx, src_pos, tar_pos)
                else:
                    sfx_mgr.remove_sfx(sfx)

            def remove_cb(sfx):
                if not self.is_valid():
                    return
                if traj_type == BULLET_RIFLE_TYPE:
                    self._on_remove_rifle_traj(sfx)

            if is_mine:
                sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_cb, on_remove_func=remove_cb, ex_data=ex_data)
            else:
                check_type = CHECK_TYPE_MAP.get(wp_type, CREATE_SRC_OTHER_SYNC)
                sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_cb, on_remove_func=remove_cb, ex_data=ex_data, int_check_type=check_type, int_check_pos=src_pos)
            return

    def _on_create_rifle_traj(self, sfx, speed, acc_speed, src_pos, tar_pos, socket_name, side, sfx_scale, need_trajectory_tick):
        traj_vector = tar_pos - src_pos
        if traj_vector.is_zero:
            traj_vector = math3d.vector(0, 0, 1)
        traj_vector.normalize()
        sfx.scale = math3d.vector(1, 1, 1)
        src_pos += traj_vector * 1 * NEOX_UNIT_SCALE
        sfx.set_placement(src_pos, traj_vector, math3d.vector(0, 1, 0))
        is_scale = sfx_scale > 1 if self.sd.ref_is_mecha else False
        is_cam_unit = global_data.cam_lctarget and self.unit_obj and global_data.cam_lctarget.id == self.unit_obj.id
        if self.sd.ref_is_mecha:
            scale_y = 40 if 1 else 100
            sfx.enable_trajectory_ctrl(src_pos, tar_pos, speed, acc_speed, bool(is_cam_unit), scale_y, is_scale, sfx_scale, 1, is_scale, sfx_scale, 1)
            if need_trajectory_tick and is_cam_unit and socket_name and side is not None:
                cfg = RifleTrajectoryConfig(sfx, socket_name, side)
                self._rifle_traj_cfg_list.append(cfg)
                self.need_update = self.need_update or True
                self._cur_tick = 0
        return

    def _on_remove_rifle_traj(self, sfx):
        for cfg in self._rifle_traj_cfg_list:
            if cfg.sfx == sfx:
                self._rifle_traj_cfg_list.remove(cfg)
                break

        if len(self._rifle_traj_cfg_list) == 0 and self.need_update:
            self.need_update = False
            self._cur_tick = 0

    def _on_create_snipper_traj(self, sfx, src_pos, tar_pos):
        traj_sfx_len = 4.2
        traj_vector = tar_pos - src_pos
        scale = min(traj_vector.length, 50 * NEOX_UNIT_SCALE) / traj_sfx_len
        sfx.scale = math3d.vector(scale, 1, scale)
        if traj_vector.is_zero:
            traj_vector = math3d.vector(0, 0, 1)
        sfx.set_placement(src_pos, traj_vector, math3d.vector(0, 1, 0))

    def _on_create_laser_traj(self, sfx, src_pos, tar_pos):
        sfx.position = src_pos
        sfx.end_pos = tar_pos
        forward = tar_pos - src_pos
        if forward.is_zero:
            forward = math3d.vector(0, 0, 1)
        sfx.set_placement(src_pos, forward, math3d.vector(0, 1, 0))

    def _update_rifle_traj(self):
        for cfg in self._rifle_traj_cfg_list:
            if self._cur_tick % cfg.tick != 0:
                continue
            src_pos = self._get_traj_src_pos_by_socket(cfg.socket, cfg.weapon_side)
            if src_pos:
                cfg.sfx.set_trajectory_ctrl_src_pos(src_pos)

        if not self._rifle_traj_cfg_list:
            self.need_update = False
            self._cur_tick = 0
        else:
            self._cur_tick += 1


class RifleTrajectoryConfig(object):

    def __init__(self, sfx, socket, weapon_side):
        super(RifleTrajectoryConfig, self).__init__()
        self.sfx = sfx
        self.socket = socket
        self.weapon_side = weapon_side
        self.tick = 3