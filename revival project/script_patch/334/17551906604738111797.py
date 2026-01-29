# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckMechaShooter.py
from __future__ import absolute_import
import world
import math3d
import collision
from common.utils.path import check_file_exist
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import GROUP_ALL_SHOOTUNIT

class ComArtCheckMechaShooter(UnitCom):
    BIND_EVENT = {'E_FIRE': 'fire',
       'E_SET_ATTR': 'try_set_attr',
       'G_ACTION_DOWN': 'on_action_btn_down',
       'E_ACTION_UP': 'on_action_btn_up'
       }

    def __init__(self):
        super(ComArtCheckMechaShooter, self).__init__(True)
        self.fire_sfx = 'effect/fx/robot/robot_01/robot01_jiatelin_start.sfx'
        self.bullet_sfx = 'effect/fx/robot/robot_01/robot01_jiatelin_bullet.sfx'
        self.hit_sfx = 'effect/fx/robot/robot_01/robot01_jiatelin_hit.sfx'
        self.bullet_speed = 500.0
        self.bullet_max_dist = 1000.0
        self.fire_cd = 0.2
        self.fire_cd_timer = -1
        self.fire_socket = ['fx_spark_kaihuo_01', 'fx_spark_kaihuo_02']
        self.fire_index = 0
        self.bullet_list = []
        self.keep_fire = False

    def try_set_attr(self, attr_name, value):
        if hasattr(self, attr_name):
            setattr(self, attr_name, value)

    def fire(self):
        if self.fire_cd_timer > 0:
            return
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        scn = self.scene
        if not scn:
            return
        if self.fire_socket:
            if self.fire_index >= len(self.fire_socket):
                self.fire_index = 0
            fire_socket = self.fire_socket[self.fire_index]
            fire_socket_valid = model.has_socket(fire_socket)
        else:
            fire_socket_valid = False
        model_rot = model.rotation_matrix
        model_forward = model_rot.forward
        model_forward.normalize()
        if fire_socket_valid:
            fire_pos = model.get_socket_matrix(fire_socket, world.SPACE_TYPE_WORLD).translation
        else:
            fire_pos = model.position + model_forward * 13.0 + math3d.vector(0, 50, 0)
        ray_end = fire_pos + model_forward * self.bullet_max_dist
        res = scn.scene_col.hit_by_ray(fire_pos, ray_end, 0, 65535, GROUP_ALL_SHOOTUNIT, collision.INCLUDE_FILTER, False)
        if res and res[0]:
            ray_end = res[1]
        if fire_socket_valid and check_file_exist(self.fire_sfx):
            global_data.sfx_mgr.create_sfx_on_model(self.fire_sfx, model, fire_socket)
        if check_file_exist(self.bullet_sfx):

            def bullet_created--- This code section failed: ---

  69       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'bullet_list'
           6  LOAD_ATTR             1  'append'
           9  BUILD_MAP_6           6 

  70      12  BUILD_MAP_1           1 
          15  STORE_MAP        

  71      16  LOAD_DEREF            1  'model_forward'
          19  LOAD_CONST            2  'forward'
          22  STORE_MAP        

  72      23  LOAD_DEREF            0  'self'
          26  LOAD_ATTR             2  'bullet_speed'
          29  LOAD_CONST            3  'speed'
          32  STORE_MAP        

  73      33  LOAD_DEREF            2  'ray_end'
          36  LOAD_CONST            4  'end_pos'
          39  STORE_MAP        

  74      40  LOAD_GLOBAL           3  'False'
          43  LOAD_CONST            5  'exploded'
          46  STORE_MAP        

  75      47  LOAD_DEREF            3  'res'
          50  LOAD_CONST            6  ''
          53  BINARY_SUBSCR    
          54  LOAD_CONST            7  'hit'
          57  STORE_MAP        
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          

  77      62  LOAD_DEREF            4  'model_rot'
          65  LOAD_FAST             0  'sfx'
          68  STORE_ATTR            4  'rotation_matrix'

Parse error at or near `STORE_MAP' instruction at offset 15

            global_data.sfx_mgr.create_sfx_in_scene(self.bullet_sfx, fire_pos, on_create_func=bullet_created)
        if len(self.fire_socket) > 1:
            self.fire_index += 1
            if self.fire_index >= len(self.fire_socket):
                self.fire_index = 0
        self.fire_cd_timer = self.fire_cd

    def tick(self, delta):
        if self.fire_cd_timer > 0:
            self.fire_cd_timer -= delta
        left_bullets = []
        while self.bullet_list:
            bullet_data = self.bullet_list.pop()
            bullet_data = self.tick_bullet(delta, bullet_data)
            if bullet_data:
                left_bullets.append(bullet_data)

        self.bullet_list = left_bullets
        if self.keep_fire:
            self.fire()

    def tick_bullet(self, delta, bullet_data):
        sfx = bullet_data['sfx']
        if not sfx or not sfx.valid:
            return
        if bullet_data['exploded']:
            sfx.destroy()
            if bullet_data['hit'] and check_file_exist(self.hit_sfx):
                global_data.sfx_mgr.create_sfx_in_scene(self.hit_sfx, bullet_data['end_pos'])
            return
        cur_pos = sfx.position
        move_dist = delta * bullet_data['speed']
        end_dist = (bullet_data['end_pos'] - cur_pos).length
        if end_dist <= move_dist:
            sfx.position = bullet_data['end_pos']
            bullet_data['exploded'] = True
        else:
            sfx.position = cur_pos + bullet_data['forward'] * move_dist
        return bullet_data

    def on_action_btn_down(self, action):
        if action == 'action1':
            self.keep_fire = True

    def on_action_btn_up(self, action):
        if action == 'action1':
            self.keep_fire = False

    def destroy(self):
        super(ComArtCheckMechaShooter, self).destroy()
        while self.bullet_list:
            bullet_data = self.bullet_list.pop()
            sfx = bullet_data['sfx']
            sfx and sfx.destroy()