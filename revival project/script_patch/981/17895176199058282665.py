# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCharacterCollision.py
from __future__ import absolute_import
from __future__ import print_function
from .ComObjCollision import ComObjCollision
import math3d
import math
import common.utils.timer as timer
import collision
import logic.gcommon.common_const.collision_const as collision_const

class ComCharacterCollision(ComObjCollision):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_ON_BEING_OBSERVE': 'on_observe',
       'E_DEATH': '_on_dead',
       'E_DEFEATED': '_on_dead',
       'E_REVIVE': '_on_revive',
       'G_COL_CHARACTER': '_get_col_character',
       'E_COL_CHARACTER_ON': '_set_col_on',
       'E_COL_CHARACTER_OFF': '_set_col_off'
       }

    def __init__(self):
        super(ComCharacterCollision, self).__init__()
        from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE, GROUP_CAMERA_COLL
        self._mask = GROUP_DEFAULT_VISIBLE
        self._group = GROUP_DEFAULT_VISIBLE
        self._hide = False
        self._timer = None
        return

    def init_from_dict(self, unit, bdict):
        super(ComCharacterCollision, self).init_from_dict(unit, bdict)

    def get_collision_info(self):
        from logic.gcommon.common_const.collision_const import CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT
        width, height = CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT
        height = height - width * 2
        bounding_box = math3d.vector(width, height, 0)
        mask = self._mask
        group = self._group
        mass = 0
        return {'collision_type': collision.CAPSULE,'bounding_box': bounding_box,'mask': mask,'group': group,'mass': mass,'is_character': True
           }

    def _get_col_character(self):
        return self._col_obj

    def _set_col_off(self):
        if not self._col_obj:
            return
        self._hide = True
        self._col_obj.group = 0
        self._col_obj.mask = 0

    def _set_col_on(self):
        if not self._col_obj:
            return
        self._hide = False
        self._col_obj.group = self._group
        self._col_obj.mask = self._mask

    def destroy_col(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        if self._col_obj:
            model = self.model
            if model:
                model.unbind_col_obj(self._col_obj)
            global_data.emgr.scene_remove_shoot_body_event.emit(self._col_obj.cid)
        super(ComCharacterCollision, self).destroy_col()
        return

    def _create_col_obj(self):
        if self.ev_g_is_pure_mecha() is True:
            return
        else:
            import logic.gcommon.common_const.animation_const as animation_const
            super(ComCharacterCollision, self)._create_col_obj()
            if self._col_obj:
                self._col_obj.car_ishurt = True
                model = self.model
                if model:
                    model.bind_col_obj(self._col_obj, animation_const.BONE_BIPED_NAME)
                global_data.emgr.scene_add_shoot_body_event.emit(self._col_obj.cid, self.unit_obj)
                result = self.scene.scene_col.static_test(self._col_obj, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER)
                if result:
                    self._set_col_off()
                    if self._timer:
                        global_data.game_mgr.unregister_logic_timer(self._timer)
                        self._timer = None
                    self._timer_id = global_data.game_mgr.register_logic_timer(self.test_open_col_tick, interval=0.1, times=-1, mode=timer.CLOCK)
            return

    def test_open_col_tick(self, *args):
        if not self._col_obj:
            return timer.RELEASE
        else:
            result = self.scene.scene_col.static_test(self._col_obj, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER)
            if not result:
                self._timer = None
                self._set_col_on()
                return timer.RELEASE
            return

    def on_model_load_complete(self, model):
        super(ComCharacterCollision, self).on_model_load_complete(model)

    def destroy(self):
        self.destroy_col()
        super(ComCharacterCollision, self).destroy()

    def _on_dead(self, *args):
        self.destroy_col()

    def _on_revive(self, *args):
        self._create_col_obj()

    def on_observe(self, is_observe):
        from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE, GROUP_CAMERA_COLL
        if is_observe:
            self._mask = GROUP_DEFAULT_VISIBLE
            self._group = GROUP_DEFAULT_VISIBLE
        else:
            self._mask = GROUP_DEFAULT_VISIBLE
            self._group = GROUP_DEFAULT_VISIBLE
        if self._col_obj and not self._hide:
            self._col_obj.mask = self._mask
            self._col_obj.group = self._group

    def _sync_model_rotation_to_col(self, pitch):
        yaw = self.ev_g_yaw()
        euler = math3d.vector(pitch, yaw, 0)
        rot = math3d.rotation(0, 0, 0, 1)
        rot.set_euler_deg(euler)
        if not math.isnan(rot.x):
            fix_y_rotate = math3d.rotation(0, 0, 0, 1)
            fix_y_rotate.set_axis_angle(math3d.vector(0, 1, 0), math.pi / 2.0)
            fix_z_rotate = math3d.rotation(0, 0, 0, 1)
            fix_z_rotate.set_axis_angle(math3d.vector(0, 0, 1), math.pi / 2.0)
            final_rotate = rot * fix_y_rotate * fix_z_rotate
            rotation_matrix = math3d.rotation_to_matrix(final_rotate)
            self._col_obj.rotation_matrix = rotation_matrix
            print('test--_sync_model_rotation_to_col--pitch =', pitch, '--yaw =', yaw, '--unit_obj =', self.unit_obj, '--rot =', rot, '--final_rotate =', final_rotate, '--rotation_matrix =', rotation_matrix)