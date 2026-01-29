# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComLodWeapon.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
import game3d
import world
import math
import math3d
from logic.gcommon.component.client.com_base_appearance.ComLodBase import ComLodBase
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.gcommon.cdata.status_config as status_config
EMPTY_SUBMESH_NAME = 'empty'
ROTATE_DATA = {animation_const.WEAPON_TYPE_FLAMER: 90,
   animation_const.WEAPON_TYPE_BAZOOKA: 90,
   animation_const.WEAPON_TYPE_SHRAPNEL: 180
   }

class ComLodWeapon(ComLodBase):
    BIND_EVENT = {'E_GUN_MODEL_LOADED': 'on_gun_model_loaded',
       'E_ROTATE_WEAPON': 'on_rotate_weapon',
       'E_RESET_ROTATE_WEAPON': 'on_reset_rotate_weapon'
       }

    def __init__(self):
        super(ComLodWeapon, self).__init__()
        self._load_mesh_task = None
        return

    def on_gun_model_loaded(self, model, is_ak, hand_pos):
        res_path = model.get_file_path()
        if self.ev_g_is_avatar():
            res_path = res_path.replace('empty.gim', 'l1.gim')
        else:
            res_path = res_path.replace('empty.gim', 'l2.gim')
        mesh_idx = model.get_mesh_by_name(res_path)
        if mesh_idx >= 0:
            return
        else:
            self.on_add_lod_model(None, (res_path, hand_pos))
            return

    def on_add_lod_model(self, load_model, user_data, *args):
        res_path = user_data[0]
        hand_pos = user_data[1]
        model = None
        if hand_pos == animation_const.WEAPON_POS_LEFT:
            model = self.sd.ref_left_hand_weapon_model
        else:
            model = self.sd.ref_hand_weapon_model
        if model is not None:
            global_data.model_mgr.create_mesh_async(self._load_mesh_task, res_path, model, self.on_load_mesh_completed)
        return

    def on_load_mesh_completed(self, model):
        model.set_submesh_visible(EMPTY_SUBMESH_NAME, False)
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            if model.get_submesh_name(i) != 'hit':
                model.set_submesh_hitmask(i, world.HIT_SKIP)

        if self.ev_g_is_avatar() and self.ev_g_is_in_any_state((status_config.ST_PICK, status_config.ST_RUSH)):
            self.on_rotate_weapon()

    def on_rotate_weapon(self):
        action_id = self.ev_g_weapon_action_id()
        if action_id and action_id in animation_const.WEAPON_ROTATE_TYPE_LIST:
            model = self.sd.ref_hand_weapon_model
            if model and model.valid:
                cur_matrix = model.rotation_matrix
                model.rotation_matrix = cur_matrix.make_rotation_y(math.pi * ROTATE_DATA[action_id] / 180)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_ROTATE_WEAPON, ()), True, False, True)

    def on_reset_rotate_weapon(self):
        action_id = self.ev_g_weapon_action_id()
        if action_id and action_id in animation_const.WEAPON_ROTATE_TYPE_LIST:
            model = self.sd.ref_hand_weapon_model
            if model and model.valid:
                model.rotation_matrix = math3d.matrix()
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_RESET_ROTATE_WEAPON, ()), True, False, True)

    def destroy(self):
        super(ComLodWeapon, self).destroy()