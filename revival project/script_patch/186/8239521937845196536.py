# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNightmareBoxAppearance.py
from __future__ import absolute_import
import six
from six.moves import range
from .ComPickAppearance import ComPickAppearance
import math3d
import collision
import logic.gcommon.time_utility as tutil
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import common.utils.timer as timer
CIRCLE_EFFECTS = [
 'effect/fx/monster/yemu_monster/ym_quan.sfx',
 'effect/fx/monster/yemu_monster/ym_quan_10m.sfx',
 'effect/fx/monster/yemu_monster/ym_quan_5m.sfx']
CIRCLE_DISAPPEAR_EFFECTS = [
 'effect/fx/monster/yemu_monster/ym_quan_end.sfx',
 'effect/fx/monster/yemu_monster/ym_quan_10m_end.sfx',
 'effect/fx/monster/yemu_monster/ym_quan_5m_end.sfx']
BOX_SEAL_EFFECT = 'effect/fx/monster/yemu_monster/ym_jingu.sfx'
BOX_UNSEAL_EFFECT = 'effect/fx/monster/yemu_monster/ym_baoxiang.sfx'
BOX_WAKE_EFFECT = 'effect/fx/monster/yemu_monster/ym_up_guangzhu.sfx'
BOX_OPEN_EFFECT = 'effect/fx/monster/yemu_monster/ym_baoxiang_baokai.sfx'
BOX_ENERGY_EFFECT = 'effect/fx/monster/yemu_monster/ym_red_guangdian.sfx'

class ComNightmareBoxAppearance(ComPickAppearance):
    BIND_EVENT = ComPickAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_START_AWAKE': '_start_awake',
       'E_SET_AWAKE': '_set_awake',
       'E_ON_MONSTER_KILLED': '_on_monster_killed'
       })
    CIRCLE_NUM = 3

    def __init__(self):
        super(ComNightmareBoxAppearance, self).__init__()
        self._sound_id = None
        self._sound_player_id = None
        self._check_timer = None
        self.col = None
        self.seal_sfx_id = None
        self.wake_sfx_id = None
        self.circle_effects = {}
        self.point_effects = {}
        return

    def reuse(self, share_data):
        super(ComNightmareBoxAppearance, self).reuse(share_data)
        self._sound_id = None
        self._sound_player_id = None
        self._check_timer = None
        self.col = None
        self.seal_sfx_id = None
        self.wake_sfx_id = None
        self.circle_effects = {}
        self.point_effects = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComNightmareBoxAppearance, self).init_from_dict(unit_obj, bdict)
        self._position = math3d.vector(*bdict.get('position', (0, 0, 0)))
        self._awake_level = bdict.get('awake_level', 0)
        self._is_awake = bdict.get('is_awake', False)
        self._server_start_time = bdict.get('start_time', 0)
        self._circle_level = 0

    def destroy(self):
        self.del_box_sound()
        super(ComNightmareBoxAppearance, self).destroy()

    def cache(self):
        self.del_box_sound()
        super(ComNightmareBoxAppearance, self).cache()

    def on_load_model_complete(self, model, userdata):
        model.scale = math3d.vector(3, 3, 3)
        model.world_position = math3d.vector(self._position)
        if self.is_scene_box_open():
            if not model or not model.valid:
                return
            model.play_animation('open')
            if model.has_socket('bind_pos'):
                sfx = model.get_socket_objects('bind_pos')
                if sfx:
                    sfx[0].destroy()
        else:
            self.add_box_sound(self._position, self.item_id)
        if not self._is_awake:
            for level in range(1, self._awake_level + 1):
                self.create_circle_effect(level)

        if not self.is_scene_box_open():
            self.seal_sfx_id = global_data.sfx_mgr.create_sfx_on_model(BOX_SEAL_EFFECT, model, 'bind_pos')
        from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_GRENADE, GROUP_CHARACTER_INCLUDE, GROUP_STATIC_SHOOTUNIT, GROUP_MECHA_BALL
        box = model.bounding_box * 3
        self.col = collision.col_object(collision.BOX, box, 0, 0, 0, True)
        self.col.mask = GROUP_GRENADE | GROUP_CHARACTER_INCLUDE | GROUP_STATIC_SHOOTUNIT | GROUP_MECHA_BALL
        self.col.group = BUILDING_GROUP
        self.col.position = model.center_w
        self.col.rotation_matrix = self.model.rotation_matrix
        self.scene.scene_col.add_object(self.col)
        if self.is_scene_box_open():
            self.col.position += math3d.vector(0, 8, 0)
        self._sound_id = global_data.sound_mgr.register_game_obj('item_backpack')
        global_data.sound_mgr.set_position(self._sound_id, model.world_position)
        global_data.sound_mgr.set_switch('box', 'treasure_chest02_loop', self._sound_id)
        self._check_timer = global_data.game_mgr.register_logic_timer(self.check_sound, interval=1, times=-1, mode=timer.CLOCK)

    def _start_awake(self, level):
        self._awake_level = level
        if level <= 0:
            self.clear_circle_effect(True)
        elif self.model and self.model.valid:
            self.create_circle_effect(level)

    def _set_awake(self):
        if not self.model or not self.model.valid:
            return
        self._is_awake = True
        self.wake_sfx_id = global_data.sfx_mgr.create_sfx_on_model(BOX_UNSEAL_EFFECT, self.model, 'bind_pos')
        self.wake_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(BOX_WAKE_EFFECT, self.model.position)
        self.clear_circle_effect(True)
        global_data.sound_mgr.play_sound('Play_treasure_chest', self.model.world_position, ('box',
                                                                                            'treasure_chest02_activation_completed'))

    def _on_monster_killed(self, position):
        position = math3d.vector(*position)
        position.y += 2 * NEOX_UNIT_SCALE

        def add_fly_point(sfx):
            if len(self.point_effects) <= 0:
                self.need_update = True
            self.point_effects[sfx] = [
             0, position]

        global_data.sfx_mgr.create_sfx_in_scene(BOX_ENERGY_EFFECT, position, on_create_func=add_fly_point)

    def on_scene_box_stat_change(self, status):
        super(ComNightmareBoxAppearance, self).on_scene_box_stat_change(status)
        self.clear_box_effects()
        self.del_box_sound()
        if self.model and self.model.valid:
            global_data.sfx_mgr.create_sfx_in_scene(BOX_OPEN_EFFECT, self.model.position + math3d.vector(0, 2 * NEOX_UNIT_SCALE, 0))
            global_data.sound_mgr.play_sound('Play_treasure_chest', self.model.world_position, ('box',
                                                                                                'treasure_chest02_unlock'))
        if self.col:

            def move_up():
                if not self.is_valid() or not self.col or not self.col.valid:
                    return timer.RELEASE
                self.col.position += math3d.vector(0, 1, 0)

            global_data.game_mgr.register_logic_timer(move_up, interval=0.03, times=8, mode=timer.CLOCK)

    def on_model_destroy(self):
        super(ComNightmareBoxAppearance, self).on_model_destroy()
        self.clear_box_effects()
        self.clear_circle_effect()
        self.clear_point_sfx()
        if self.col:
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def clear_box_effects(self):
        if self.seal_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.seal_sfx_id)
            self.seal_sfx_id = None
        if self.wake_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.wake_sfx_id)
            self.wake_sfx_id = None
        return

    def create_circle_effect(self, level):
        if level in self.circle_effects and self.circle_effects[level]:
            global_data.sfx_mgr.remove_sfx_by_id(self.circle_effects[level])
        self.circle_effects[level] = global_data.sfx_mgr.create_sfx_in_scene(CIRCLE_EFFECTS[level - 1], self.model.position)
        global_data.sound_mgr.play_sound('Play_treasure_chest', self.model.world_position, ('box',
                                                                                            'treasure_chest02_activation'))

    def clear_circle_effect(self, show_disappear_effect=False):
        for level, sfx_id in six.iteritems(self.circle_effects):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
            if show_disappear_effect:
                global_data.sfx_mgr.create_sfx_in_scene(CIRCLE_DISAPPEAR_EFFECTS[level - 1], self.model.position)

        self.circle_effects = {}

    def clear_point_sfx(self):
        for sfx in six.iterkeys(self.point_effects):
            global_data.sfx_mgr.remove_sfx(sfx)

        self.point_effects = {}

    def tick(self, delta):
        if not self.model or not self.model.valid:
            return
        finished = []
        target_pos = self.model.position + math3d.vector(0, NEOX_UNIT_SCALE, 0)
        for sfx, info in six.iteritems(self.point_effects):
            time, start_pos = info
            time += delta
            u = time / 1.0
            if u >= 1.0:
                finished.append(sfx)
                global_data.sfx_mgr.remove_sfx(sfx)
                continue
            pos = math3d.vector(0, 0, 0)
            pos.intrp(start_pos, target_pos, u)
            sfx.position = pos
            self.point_effects[sfx][0] = time

        for sfx in finished:
            del self.point_effects[sfx]

        if len(self.point_effects) <= 0:
            self.need_update = False

    def check_sound(self):
        if not self.model or not self.model.valid:
            return
        else:
            cam_lplayer = global_data.cam_lplayer
            if not cam_lplayer:
                return
            player_pos = cam_lplayer.ev_g_model_position()
            if not player_pos:
                return
            distance_sqr = (player_pos - self.model.world_position).length_sqr
            if distance_sqr < self.BOX_SOUND_MIN_DIS_SQR and not self._sound_player_id and self._sound_id:
                self._sound_player_id = global_data.sound_mgr.post_event('Play_treasure_chest', self._sound_id)
            elif distance_sqr > self.BOX_SOUND_MAX_DIS_SQR and self._sound_player_id:
                global_data.sound_mgr.stop_playing_id(self._sound_player_id)
                self._sound_player_id = None
            return

    def del_box_sound(self, *args):
        if self._sound_player_id:
            global_data.sound_mgr.stop_playing_id(self._sound_player_id)
            self._sound_player_id = None
        if self._sound_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_id)
            self._sound_id = None
        if self._check_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_timer)
            self._check_timer = None
        return