# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPreviewCharacter.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import world
import math3d
from logic.gcommon.common_const.collision_const import CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, GROUP_CHARACTER_INCLUDE, MASK_CHARACTER_ROBOT, GROUP_CHARACTER_ROBOT

class ComPreviewCharacter(UnitCom):
    SLOW_MODEL_POS_SCALE = 0.8
    BIND_EVENT = {'E_MOVE': '_move_toward',
       'E_MOVE_STOP': '_move_stop',
       'E_DELTA_YAW': '_on_yaw',
       'E_SET_YAW': '_on_set_yaw',
       'G_YAW': '_get_yaw',
       'E_SET_WALK_DIRECTION': 'set_walk_direction',
       'G_WALK_DIRECTION': 'get_walk_direction',
       'E_SET': 'get_walk_direction',
       'E_CHANGE_SPEED': '_change_speed'
       }

    def __init__(self):
        super(ComPreviewCharacter, self).__init__()
        self.speed = 100
        self._yaw = 0
        self._rock_dir = math3d.vector(0, 0, 0)
        self._world_move_dir = self._rock_dir
        self._normalized_rock_dir = self._rock_dir

    def _get_character_logic_height(self, character, actual_height):
        return actual_height - character.getRadius() * 2.0 - character.getSkinWidth() * 2.0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPreviewCharacter, self).init_from_dict(unit_obj, bdict)
        self.init_charactor()
        self._init_position(bdict)
        self.character.activate(self.scene.scene_col)

    def init_charactor(self):
        import collision
        import math
        width, height, stepheight = CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, 0.6
        max_slope = 60
        padding = 0.001
        added_margin = 0.02
        pos_interpolate = 0.5
        self.character = collision.Character(width, height, stepheight)
        self.character.setPadding(padding)
        self.character.setAddedMargin(added_margin)
        self.character.setMaxSlope(math.radians(max_slope))
        self.character.setSmoothFactor(pos_interpolate)
        self.character.enableForceSync = True
        self.scene.scene_col.add_character(self.character)
        character_height = self._get_character_logic_height(self.character, height)
        self.character.setHeight(character_height)
        self.character.filter = MASK_CHARACTER_ROBOT
        self.character.group = GROUP_CHARACTER_ROBOT
        self.character.setPositionChangedCallback(self._on_pos_changed)

    def _init_position(self, bdict):
        pos = bdict.get('position', (0, 0, 0))
        init_pos = math3d.vector(pos[0], pos[1], pos[2])
        self.character.physicalPosition = init_pos
        self.scene.viewer_position = init_pos
        self._on_pos_changed(init_pos)

    def _move_toward(self, move_dir):
        self._normalized_rock_dir = move_dir
        self.send_event('E_ACTION_MOVE', move_dir)
        move_dir *= self.speed
        self._rock_dir = move_dir
        move_dir = move_dir * math3d.matrix.make_rotation_y(self._yaw)
        self._world_move_dir = move_dir
        self.set_walk_direction(move_dir)

    def _move_stop(self):
        self.send_event('E_ACTION_MOVE_STOP')
        self._rock_dir = math3d.vector(0, 0, 0)
        self._normalized_rock_dir = self._rock_dir
        self._world_move_dir = self._rock_dir
        self.set_walk_direction(self._rock_dir)

    def _on_pos_changed(self, pos, *arg):
        old_model_position = self.ev_g_model_position()
        if self.character.verticalVelocity < 0:
            pos_y = old_model_position.y + self.SLOW_MODEL_POS_SCALE * (pos.y - old_model_position.y)
            pos.y = pos_y
        model = self.ev_g_model()
        if model:
            model.position = pos

    def _change_speed(self, speed):
        pass

    def get_walk_direction(self):
        return self._normalized_rock_dir

    def set_walk_direction(self, move_dir, reach_target_callback=None, reach_target_pos=None):
        self.send_event('E_CHARACTER_WALK', move_dir)
        model_rot_mat = math3d.matrix.make_rotation_y(self._yaw)
        model_rot = math3d.matrix_to_rotation(model_rot_mat)
        self.character.setCharacterDirection(model_rot)
        reach_target_pos = reach_target_pos or math3d.vector(0, 0, 0)
        self.character.setOnReachTargetCallback(reach_target_pos, reach_target_callback)

    def _on_set_yaw(self, yaw, force_change_spd=True):
        if yaw is None:
            return
        else:
            self._yaw = yaw
            self.send_event('E_ACTION_SET_YAW', yaw)
            model = self.ev_g_model()
            if model:
                model.rotation_matrix = math3d.matrix.make_rotation_y(yaw)
            self._on_yaw(0, force_change_spd)
            return

    def _get_yaw(self):
        return self._yaw

    def _on_yaw(self, yaw, force_change_spd=True):
        self._yaw += yaw
        self.send_event('E_ACTION_DELTA_YAW', yaw)
        if self.ev_g_is_jump():
            return
        self._rotate_model(yaw)
        if force_change_spd:
            move_dir = self._rock_dir * math3d.matrix.make_rotation_y(self._yaw)
            self._world_move_dir = move_dir
            self.set_walk_direction(move_dir)

    def _rotate_model(self, delta):
        model = self.ev_g_model()
        if model:
            model.rotate_y(delta)