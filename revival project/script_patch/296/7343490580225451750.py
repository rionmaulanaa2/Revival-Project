# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAtkHand.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
import time
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_EXCLUDE, GROUP_CAN_SHOOT, GROUP_SHOOTUNIT
from logic.gcommon.const import HIT_PART_HEAD, HIT_PART_BODY
import logic.gcommon.common_const.animation_const as animation_const
EMPTY_HAND_BONE = [
 animation_const.BONE_RIGHT_HAND_NAME, animation_const.BONE_RIGHT_HAND_NAME, animation_const.BONE_LEFT_HAND_NAME]
ACT_LIFE_TIME = 0.6

class ComAtkHand(UnitCom):
    BIND_EVENT = {'E_ATTACK_START': '_on_attack_start',
       'E_ATTACK_END': '_on_attack_end',
       'E_EMPTY_HAND_ACT': 'create_col',
       'E_EMPTY_HAND_ACT_END': 'empty_hand_attack_end'
       }

    def __init__(self):
        super(ComAtkHand, self).__init__(False)
        self._item_id = 0
        self._socket_name = None
        self._col_obj = None
        self._model = None
        self._act_time = 0
        self._continuous_attack = False
        return

    def _on_attack_start(self, *args):
        self._continuous_attack = True

    def _on_attack_end(self, *args):
        self._continuous_attack = False

    def empty_hand_attack_end(self, *args):
        if self._continuous_attack:
            self._continuous_attack = False

    def create_col(self, punch_idx):
        if not self.is_unit_obj_type('LAvatar'):
            return
        self._model = self.ev_g_model()
        if not self._model:
            return
        side_len = 0.1 * NEOX_UNIT_SCALE
        size = math3d.vector(side_len, side_len, side_len)
        self._col_obj = collision.col_object(collision.BOX, size, 0, GROUP_CHARACTER_EXCLUDE)
        self.scene.scene_col.add_object(self._col_obj)
        self._model.bind_col_obj(self._col_obj, EMPTY_HAND_BONE[punch_idx])
        self.need_update = True
        self._act_time = time.time()

    def install_weapon(self, weapon, is_init, is_switch_mode=False):
        if is_init:
            self.send_event('E_FINISH_SWITCH_GUN', 0)

    def check_hand_attack(self, col_object):
        my_pos = self._col_obj.position
        direction = self._col_obj.rotation_matrix.right * (NEOX_UNIT_SCALE * 0.5)
        result = global_data.emgr.scene_melee_attack_event.emit(col_object, my_pos, direction)
        if result:
            return result[0]
        else:
            return (None, -1, None)

    def tick(self, delta):
        if not self._model:
            return
        else:
            scene = self.scene
            if time.time() - self._act_time >= ACT_LIFE_TIME:
                self.need_update = False
                scene.scene_col.remove_object(self._col_obj)
                self._col_obj = None
                self._model = None
                return
            ls = scene.scene_col.static_test(self._col_obj, GROUP_SHOOTUNIT, GROUP_SHOOTUNIT, collision.INCLUDE_FILTER)
            if ls and len(ls) >= 1:
                unit_id, part_id, pos = self.check_hand_attack(ls[0])
                if not unit_id:
                    return
                if part_id != HIT_PART_HEAD:
                    part_id = HIT_PART_BODY
                self._act_time -= ACT_LIFE_TIME
                self.send_event('E_CALL_SYNC_METHOD', 'do_atk_melee', (unit_id, 0, part_id, [pos.x, pos.y, pos.z]), True)
            return