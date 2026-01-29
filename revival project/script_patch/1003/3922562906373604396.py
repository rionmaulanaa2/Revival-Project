# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComAlignOnGround.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.animation_const import TURN_X_FULL_BODY_NODE
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.const import NEOX_UNIT_SCALE
from math import degrees
import math3d
CHECK_DISTANCE = 3 * NEOX_UNIT_SCALE
FORCE_MODEL_OFFSET = {8020: {True: 11.2,
          False: 0
          },
   8022: {True: 11.2,
          False: 0
          },
   8032: {True: 20.0,
          False: 0
          },
   8033: {True: 11.2,
          False: 0
          }
   }

class ComAlignOnGround(UnitCom):
    BIND_EVENT = {'E_ENABLE_ALIGN_ON_GROUND': 'enable_align_on_ground'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComAlignOnGround, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_align_on_ground_enabled = False
        self.max_twist_angle = 70

    def _reset_twist_angle(self):
        animator = self.ev_g_animator()
        if animator:
            turn_full_body_node = animator.find(TURN_X_FULL_BODY_NODE)
            if turn_full_body_node:
                turn_full_body_node.twistAngle = 0

    def enable_align_on_ground(self, flag, max_twist_angle=None):
        if self.sd.ref_align_on_ground_enabled == flag:
            return
        else:
            if max_twist_angle is not None:
                self.max_twist_angle = max_twist_angle
            self.sd.ref_align_on_ground_enabled = flag
            self.send_event('E_ENABLE_Z_CAPSULE', flag)
            self.send_event('E_REFRESH_CHARACTER_Y_OFFSET', FORCE_MODEL_OFFSET.get(self.sd.ref_mecha_id, {}).get(flag, 0))
            if flag:
                self.update_align_appearance()
                self.regist_event('E_ROTATE', self.update_align_appearance)
                if G_POS_CHANGE_MGR:
                    self.regist_pos_change(self.update_align_appearance)
                else:
                    self.regist_event('E_POSITION', self.update_align_appearance)
            else:
                self._reset_twist_angle()
                self.unregist_event('E_ROTATE', self.update_align_appearance)
                if G_POS_CHANGE_MGR:
                    self.unregist_pos_change(self.update_align_appearance)
                else:
                    self.unregist_event('E_POSITION', self.update_align_appearance)
            return

    def update_align_appearance(self, *args):
        character = self.sd.ref_character
        if not character or not character.valid or not character.isActive():
            return
        character.setCharacterDirection(math3d.matrix_to_rotation(self.sd.ref_rotatedata.rotation_mat))
        animator = self.ev_g_animator()
        if not animator:
            return
        turn_full_body_node = animator.find(TURN_X_FULL_BODY_NODE)
        if not turn_full_body_node:
            return
        rot = character.calculateGroundAngle(CHECK_DISTANCE)
        degree = degrees(rot)
        if degree > self.max_twist_angle:
            degree = self.max_twist_angle
        elif degree < -self.max_twist_angle:
            degree = -self.max_twist_angle
        turn_full_body_node.twistAngle = degree