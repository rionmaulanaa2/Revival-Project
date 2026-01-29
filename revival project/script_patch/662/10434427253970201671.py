# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFishHeadTargetAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
import world
import time
HIT_RECOVER_TIME = 0.2
HIT_DEFORM_TIME = 0.2

class ComFishHeadTargetAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_FISH_HEAD_TARGET_LOW_HP': 'on_fish_target_hp_low',
       'E_ON_HIT_BOMB_INFO': 'on_bomb_hit_fish_head',
       'E_HIT_BLOOD_SFX': 'on_hit_fish_head'
       })

    def __init__(self):
        super(ComFishHeadTargetAppearance, self).__init__()
        self.fish_pos = None
        self.fish_scale = None
        self.fish_rot_mat = None
        self.damage_sfx_id = None
        self.die_sfx_scale = None
        self.init_bone_world_mat = {}
        self.hit_anim_timer = None
        self.last_hit_time = None
        self.hurt_dir = None
        self.end_anim = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFishHeadTargetAppearance, self).init_from_dict(unit_obj, bdict)
        pos = bdict.get('position')
        self.fish_pos = math3d.vector(*pos)
        scale = bdict.get('scale')
        self.fish_scale = math3d.vector(*scale)
        rot = bdict.get('rot')
        self.fish_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))
        die_sfx_scale = bdict.get('die_sfx_scale')
        self.die_sfx_scale = math3d.vector(*die_sfx_scale)

    def cache(self):
        super(ComFishHeadTargetAppearance, self).cache()
        self.remove_damage_sfx()

    def get_model_info(self, unit_obj, bdict):
        model_path = 'model_new/scene/building/xunlianchang/items_outside_xl_target_05.gim'
        return (
         model_path, None, None)

    def on_load_model_complete(self, model, user_data):
        model.world_position = self.fish_pos
        model.rotation_matrix = self.fish_rot_mat
        model.scale = self.fish_scale
        self.init_bone_world_mat['root'] = model.get_bone_matrix('root', 1)
        self.init_hit_timer()

    def destroy(self):
        self.remove_damage_sfx()
        self.create_die_sfx()
        self.init_bone_world_mat = {}
        self.clear_hit_timer()
        super(ComFishHeadTargetAppearance, self).destroy()

    def create_die_sfx(self):
        sfx_path = 'effect/fx/mecha/8025/8025_vice_baozha.sfx'
        up_offset = 0

        def create_cb(sfx):
            sfx.scale = self.die_sfx_scale

        die_sfx_pos = math3d.vector(self.fish_pos.x, self.fish_pos.y + up_offset, self.fish_pos.z)
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, die_sfx_pos, duration=3, on_create_func=create_cb)

    def create_damage_sfx(self):
        sfx_path = 'effect/fx/robot/common/mecha_sunhuai.sfx'
        up_offset = 0
        damage_sfx_pos = math3d.vector(self.fish_pos.x, self.fish_pos.y + up_offset, self.fish_pos.z)
        self.damage_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, damage_sfx_pos)

    def remove_damage_sfx(self):
        if self.damage_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.damage_sfx_id)
            self.damage_sfx_id = None
        return

    def on_fish_target_hp_low(self):
        if self.damage_sfx_id:
            return
        self.create_damage_sfx()

    def deform_bone(self, bone_name):
        world_mat2 = self.model.get_bone_matrix(bone_name, 1)
        self.end_anim = False
        v = world_mat2.translation
        world_mat2.do_translate(-v)
        world_mat2.do_rotation(math3d.euler_to_matrix(math3d.vector(math.pi * self.hurt_dir.z / 180, math.pi * 0 / 180, -math.pi * self.hurt_dir.x / 180)))
        world_mat2.do_translate(v)
        final_euler = math3d.matrix_to_euler(self.init_bone_world_mat[bone_name].rotation)
        temp_euler = math3d.matrix_to_euler(world_mat2.rotation)
        if (final_euler - temp_euler).length > 1.0:
            return
        self.model.set_bone_matrix(bone_name, 2, world_mat2, 1)

    def recover_bone(self, bone_name):
        final_rotate = self.init_bone_world_mat[bone_name].rotation
        final_euler = math3d.matrix_to_euler(final_rotate)
        bone_mat = self.model.get_bone_matrix(bone_name, 1)
        temp_euler = math3d.matrix_to_euler(bone_mat.rotation)
        d_euler = final_euler - temp_euler
        v = bone_mat.translation
        bone_mat.do_translate(-v)
        bone_mat.do_rotation(math3d.euler_to_matrix(d_euler))
        bone_mat.do_translate(v)
        self.model.set_bone_matrix(bone_name, 1, self.init_bone_world_mat[bone_name], 1)

    def tick_hit(self):
        if not self.model or not self.last_hit_time:
            return
        check_time = time.time()
        dt = check_time - self.last_hit_time
        if dt <= HIT_DEFORM_TIME:
            self.deform_bone('root')
        if dt > HIT_DEFORM_TIME and dt < HIT_DEFORM_TIME + HIT_RECOVER_TIME and not self.end_anim:
            self.end_anim = 1
            self.recover_bone('root')

    def init_hit_timer(self):
        self.clear_hit_timer()
        self.hit_anim_timer = global_data.game_mgr.register_logic_timer(self.tick_hit, interval=0.03, times=-1, mode=2)

    def clear_hit_timer(self):
        if self.hit_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.hit_anim_timer)
        self.hit_anim_timer = None
        return

    def on_bomb_hit_fish_head(self, bomb_pos, damage):
        if not self.model:
            return
        self.last_hit_time = time.time()
        self.hurt_dir = self.model.world_position - bomb_pos
        self.hurt_dir.y = 0
        self.hurt_dir.normalize()

    def on_hit_fish_head(self, begin_pos, hit_pos, shot_type, **kwargs):
        self.last_hit_time = time.time()
        self.hurt_dir = hit_pos - begin_pos
        self.hurt_dir.y = 0
        self.hurt_dir.normalize()