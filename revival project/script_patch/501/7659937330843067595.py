# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTVMissileAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance, RES_TYPE_MODEL, RES_TYPE_SFX
from common.cfg import confmgr
import math3d
UP_VECTOR = math3d.vector(0, 1, 0)

class ComTVMissileAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_CONTROL_TARGET_CHANGE': 'on_control_target_change',
       'E_POSITION': 'on_position',
       'E_DELTA_YAW': 'on_camera_yaw',
       'E_DELTA_PITCH': 'on_camera_pitch',
       'G_CAM_PITCH': 'on_get_pitch',
       'G_IS_CAMPMATE': 'on_get_is_teammate'
       })
    MODEL_PATH = 'character/weapons/1068_tvmissile/1068/daodan.gim'

    def init_from_dict(self, unit_obj, bdict):
        super(ComTVMissileAppearance, self).init_from_dict(unit_obj, bdict)
        self.owner_eid = bdict['owner_id']
        self.is_avatar = self.owner_eid == global_data.player.id
        self.faction_id = bdict.get('faction_id', 0)
        self.weapon_id = bdict['npc_id']
        direction = bdict['direction']
        self.direction = math3d.vector(*direction)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.on_position)

    def destroy(self):
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.on_position)
        super(ComTVMissileAppearance, self).destroy()

    def get_model_info(self, unit_obj, bdict):
        position = bdict.get('position', (0, 390, -95)) or (0, 390, -95)
        pos = math3d.vector(*position)
        is_enemy = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != self.faction_id
        if self.MODEL_PATH.endswith('.sfx'):
            self.load_res_func = self.load_sfx
            sfx_diff = confmgr.get('grenade_res_config', str(self.weapon_id), 'cCustomParam', 'camp_diff', default=0)
            self._sfx_ex_data = {'need_diff_process': sfx_diff and is_enemy}
        else:
            self._sfx_ex_data = {}
        return (
         self.MODEL_PATH, None, (pos, self.MODEL_PATH))

    def on_load_model_complete(self, model, user_data):
        super(ComTVMissileAppearance, self).on_load_model_complete(model, user_data)
        self.send_event('E_HUMAN_MODEL_LOADED', model, None)
        model.rotation_matrix = math3d.matrix.make_orient(self.direction, UP_VECTOR)
        self.sd.ref_logic_trans.yaw_target = self.direction.yaw
        self.sd.ref_common_motor.set_yaw_time(0)
        pitch = self.direction.pitch
        self.sd.ref_logic_trans.pitch_target = pitch
        self.sd.ref_rotatedata.set_body_pitch_to_head(0)
        self.sd.ref_rotatedata.set_use_pitch_limit(False)
        return

    def on_position(self, pos):
        if self.model:
            self.model.position = pos

    def on_camera_yaw(self, yaw):
        self.sd.ref_logic_trans.yaw_target += yaw

    def on_camera_pitch(self, pitch):
        self.sd.ref_logic_trans.pitch_target += pitch
        self.is_avatar and self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)

    def on_get_pitch(self):
        return self.sd.ref_logic_trans.pitch_target

    def on_get_is_teammate(self, other_faction_id):
        return self.faction_id == other_faction_id