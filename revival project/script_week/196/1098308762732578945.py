# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaStaticCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
import world
import math3d
import collision
from logic.gcommon.common_const.collision_const import MECHA_STAND_WIDTH, MECHA_STAND_HEIGHT, MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, TERRAIN_GROUP, GROUP_MECHA_BALL
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
import weakref
import world
from logic.client.const.game_mode_const import GAME_MODE_PVE_EDIT

class ComMechaStaticCollision(ComObjCollision):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'G_COL_CHARACTER': '_get_col_character',
       'E_RESET_SHOOT_COL': 'reset_col_info',
       'E_DISABLE_SHOOT_COL': 'disable_col',
       'E_DEATH': 'disable_col',
       'E_HEALTH_HP_EMPTY': 'disable_col',
       'E_SWITCH_MODEL': 'on_switch_model'
       }

    def __init__(self):
        super(ComMechaStaticCollision, self).__init__()
        from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE
        self._mask = GROUP_DEFAULT_VISIBLE | GROUP_MECHA_BALL
        self._group = GROUP_DEFAULT_VISIBLE
        self.simulate_fall = True
        self.capsule_size = None
        self.static_col_height = 0.0
        self.hit_col = None
        self.col_binded = False
        self._all_time_disable = False
        return

    def init_from_dict(self, unit, bdict):
        self.simulate_fall = False
        self.capsule_size = bdict.get('capsule_size', None)
        self.is_reycling = bdict.get('pre_standby', False)
        super(ComMechaStaticCollision, self).init_from_dict(unit, bdict)
        return

    def get_collision_info(self):
        import collision
        physic_info = self.ev_g_mecha_config('PhysicConfig')
        width = physic_info['character_size'][0] * NEOX_UNIT_SCALE
        radius = width / 2
        total_height = physic_info['character_size'][1] * NEOX_UNIT_SCALE
        height = total_height - width
        self.static_col_height = total_height / 2
        bounding_box = math3d.vector(radius, height, 0)
        mask = self._mask
        group = self._group
        mass = 0
        return {'collision_type': collision.CAPSULE,'bounding_box': bounding_box,'mask': mask,'group': group,'mass': mass,'is_character': True
           }

    def _get_col_character(self):
        return self._col_obj

    def _create_col_obj(self):
        game_mode = global_data.game_mode.get_mode_type()
        if game_mode == GAME_MODE_PVE_EDIT and not self.ev_g_is_avatar():
            return
        else:
            if self.ev_g_death() or self.is_reycling or self._all_time_disable:
                return
            super(ComMechaStaticCollision, self)._create_col_obj()
            if self._col_obj:
                self.send_event('E_SET_SKIP_RAY_CHECK_CID', self._col_obj.cid)
                model = self._model()
                fall_pos = model.position
                driver = self.sd.ref_driver_id
                if driver and global_data.player and driver == global_data.player.id:
                    avatar_control = True
                else:
                    avatar_control = False
                if self.simulate_fall and avatar_control:
                    start = fall_pos
                    end = math3d.vector(start.x, start.y - 10000, start.z)
                    start.y += 20
                    result = self.scene.scene_col.hit_by_ray(start, end, 0, GROUP_CAN_SHOOT | WATER_MASK, TERRAIN_GROUP | WATER_GROUP, collision.INCLUDE_FILTER)
                    if result and result[0]:
                        fall_pos = result[1]
                        model.position = fall_pos
                self.scene.scene_col.remove_object(self._col_obj)

                def bind_col--- This code section failed: ---

  94       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'ev_g_death'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_FALSE    75  'to 75'

  95      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'unregister_logic_timer'
          21  LOAD_DEREF            0  'self'
          24  LOAD_ATTR             4  'timer_id'
          27  CALL_FUNCTION_1       1 
          30  POP_TOP          

  96      31  LOAD_CONST            0  ''
          34  LOAD_DEREF            0  'self'
          37  STORE_ATTR            4  'timer_id'

  97      40  LOAD_DEREF            0  'self'
          43  LOAD_ATTR             6  'scene'
          46  LOAD_ATTR             7  'scene_col'
          49  LOAD_ATTR             8  'remove_object'
          52  LOAD_DEREF            0  'self'
          55  LOAD_ATTR             9  '_col_obj'
          58  CALL_FUNCTION_1       1 
          61  POP_TOP          

  98      62  LOAD_CONST            0  ''
          65  LOAD_DEREF            0  'self'
          68  STORE_ATTR            9  '_col_obj'

  99      71  LOAD_CONST            0  ''
          74  RETURN_END_IF    
        75_0  COME_FROM                '9'

 100      75  LOAD_DEREF            1  'model'
          78  POP_JUMP_IF_FALSE   366  'to 366'
          81  LOAD_DEREF            1  'model'
          84  LOAD_ATTR            10  'valid'
        87_0  COME_FROM                '78'
          87  POP_JUMP_IF_FALSE   366  'to 366'

 101      90  LOAD_DEREF            0  'self'
          93  LOAD_ATTR            11  'is_unit_obj_type'
          96  LOAD_CONST            1  'LMecha'
          99  CALL_FUNCTION_1       1 
         102  POP_JUMP_IF_TRUE    120  'to 120'
         105  LOAD_DEREF            0  'self'
         108  LOAD_ATTR            11  'is_unit_obj_type'
         111  LOAD_CONST            2  'LMechaRobot'
         114  CALL_FUNCTION_1       1 
       117_0  COME_FROM                '102'
         117  POP_JUMP_IF_FALSE   271  'to 271'

 102     120  LOAD_GLOBAL          12  'MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y'
         123  LOAD_ATTR            13  'get'
         126  LOAD_DEREF            0  'self'
         129  LOAD_ATTR            14  'sd'
         132  LOAD_ATTR            15  'ref_mecha_id'
         135  LOAD_CONST            0  ''
         138  CALL_FUNCTION_2       2 
         141  STORE_FAST            0  'local_pos_y'

 103     144  LOAD_FAST             0  'local_pos_y'
         147  LOAD_CONST            0  ''
         150  COMPARE_OP            8  'is'
         153  POP_JUMP_IF_FALSE   165  'to 165'

 108     156  LOAD_CONST            3  40.0
         159  STORE_FAST            0  'local_pos_y'
         162  JUMP_FORWARD          0  'to 165'
       165_0  COME_FROM                '162'

 109     165  LOAD_GLOBAL          16  'type'
         168  LOAD_FAST             0  'local_pos_y'
         171  CALL_FUNCTION_1       1 
         174  LOAD_GLOBAL          17  'tuple'
         177  COMPARE_OP            8  'is'
         180  POP_JUMP_IF_FALSE   212  'to 212'

 110     183  LOAD_DEREF            0  'self'
         186  LOAD_ATTR            14  'sd'
         189  LOAD_ATTR            18  'ref_using_second_model'
         192  POP_JUMP_IF_FALSE   202  'to 202'
         195  POP_JUMP_IF_FALSE     4  'to 4'
         198  BINARY_SUBSCR    
         199  JUMP_FORWARD          4  'to 206'
         202  JUMP_FORWARD          5  'to 210'
         205  BINARY_SUBSCR    
       206_0  COME_FROM                '199'
         206  STORE_FAST            0  'local_pos_y'
         209  JUMP_FORWARD          0  'to 212'
       212_0  COME_FROM                '209'

 111     212  LOAD_DEREF            1  'model'
         215  LOAD_ATTR            19  'bind_col_obj'
         218  LOAD_DEREF            0  'self'
         221  LOAD_ATTR             9  '_col_obj'
         224  LOAD_GLOBAL          20  'BONE_BIPED_NAME'
         227  CALL_FUNCTION_2       2 
         230  POP_TOP          

 112     231  LOAD_GLOBAL          21  'math3d'
         234  LOAD_ATTR            22  'matrix'
         237  LOAD_ATTR            23  'make_translation'
         240  LOAD_CONST            5  ''
         243  LOAD_DEREF            0  'self'
         246  LOAD_ATTR            24  'static_col_height'
         249  LOAD_FAST             0  'local_pos_y'
         252  BINARY_SUBTRACT  
         253  LOAD_CONST            5  ''
         256  CALL_FUNCTION_3       3 
         259  LOAD_DEREF            0  'self'
         262  LOAD_ATTR             9  '_col_obj'
         265  STORE_ATTR           25  'bone_matrix'
         268  JUMP_FORWARD         83  'to 354'

 114     271  LOAD_DEREF            1  'model'
         274  LOAD_ATTR            26  'bounding_box'
         277  STORE_FAST            1  'box'

 115     280  LOAD_FAST             1  'box'
         283  LOAD_GLOBAL          21  'math3d'
         286  LOAD_ATTR            27  'vector'
         289  LOAD_CONST            6  0.6
         292  LOAD_CONST            4  1
         295  LOAD_CONST            7  0.8
         298  CALL_FUNCTION_3       3 
         301  INPLACE_MULTIPLY 
         302  STORE_FAST            1  'box'

 116     305  LOAD_GLOBAL          28  'collision'
         308  LOAD_ATTR            29  'col_object'
         311  LOAD_GLOBAL          28  'collision'
         314  LOAD_ATTR            30  'BOX'
         317  LOAD_FAST             1  'box'
         320  LOAD_GLOBAL          31  'GROUP_CAN_SHOOT'
         323  LOAD_GLOBAL          31  'GROUP_CAN_SHOOT'
         326  CALL_FUNCTION_4       4 
         329  LOAD_DEREF            0  'self'
         332  STORE_ATTR           32  'hit_col'

 117     335  LOAD_DEREF            1  'model'
         338  LOAD_ATTR            19  'bind_col_obj'
         341  LOAD_DEREF            0  'self'
         344  LOAD_ATTR            32  'hit_col'
         347  LOAD_GLOBAL          20  'BONE_BIPED_NAME'
         350  CALL_FUNCTION_2       2 
         353  POP_TOP          
       354_0  COME_FROM                '268'

 118     354  LOAD_GLOBAL          33  'True'
         357  LOAD_DEREF            0  'self'
         360  STORE_ATTR           34  'col_binded'
         363  JUMP_FORWARD          0  'to 366'
       366_0  COME_FROM                '363'
         366  LOAD_CONST            0  ''
         369  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 195

                passenger = self.ev_g_passenger_info()
                if passenger is None or len(passenger) <= 0:
                    end = model.get_bone_matrix(BONE_BIPED_NAME, world.SPACE_TYPE_WORLD).translation
                    end.y = self.static_col_height
                    start = math3d.vector(end.x, end.y - MECHA_STAND_HEIGHT, end.z)
                    self._raise_up(start, end, bind_col)
                else:
                    bind_col()
            return

    def destroy(self):
        if self._col_obj:
            if self.col_binded:
                model = self._model()
                if model and model.valid:
                    model.unbind_col_obj(self._col_obj)
            else:
                self.scene.scene_col.remove_object(self._col_obj)
            global_data.emgr.scene_remove_shoot_body_event.emit(self._col_obj.cid)
            self._col_obj = None
        if self.hit_col:
            if self.col_binded:
                model = self._model()
                if model and model.valid:
                    model.unbind_col_obj(self.hit_col)
            else:
                self.scene.scene_col.remove_object(self.hit_col)
            self.hit_col = None
        super(ComMechaStaticCollision, self).destroy()
        return

    def _raise_up(self, start, end, callback):
        if self.is_unit_obj_type('LMechaRobot'):
            return
        else:
            from common.utils.timer import CLOCK, RELEASE
            self.cnt = 0
            self.timer_id = None
            self._col_obj.position = start

            def _raise():
                if not self or not self.is_valid():
                    return RELEASE
                else:
                    self.cnt += 1
                    pos = math3d.vector(0, 0, 0)
                    u = self.cnt * 1.0 / 30
                    if u > 1.0:
                        u = 1.0
                        global_data.game_mgr.unregister_logic_timer(self.timer_id)
                        self.timer_id = None
                        if callback:
                            callback()
                    pos.intrp(start, end, u)
                    if self._col_obj:
                        self._col_obj.position = pos
                    else:
                        return RELEASE
                    return

            self.timer_id = global_data.game_mgr.register_logic_timer(func=_raise, interval=0.03, times=-1, mode=CLOCK)
            return

    def disable_col(self):
        if not self._col_obj:
            return
        else:
            if self.col_binded:
                model = self._model()
                if model and model.valid:
                    model.unbind_col_obj(self._col_obj)
            else:
                self.scene.scene_col.remove_object(self._col_obj)
            global_data.emgr.scene_remove_shoot_body_event.emit(self._col_obj.cid)
            self._col_obj = None
            return

    def reset_col_info(self):
        if not self._col_obj:
            return
        model = self._model()
        if model and model.valid:
            if self.is_unit_obj_type('LMecha') or self.is_unit_obj_type('LMechaRobot'):
                model.bind_col_obj(self._col_obj, BONE_BIPED_NAME)
            else:
                box = model.bounding_box
                box *= math3d.vector(0.6, 1, 0.8)
                self.hit_col = collision.col_object(collision.BOX, box, GROUP_CAN_SHOOT, GROUP_CAN_SHOOT)
                model.bind_col_obj(self.hit_col, BONE_BIPED_NAME)
        if self.hit_col:
            self.hit_col.group = GROUP_CAN_SHOOT
            self.hit_col.mask = GROUP_CAN_SHOOT

    def on_switch_model(self, model):
        self.disable_col()
        self._model = weakref.ref(model)
        self._model_cache = model
        self._create_col_obj()

    def disable_col_all_time(self):
        self._all_time_disable = True
        self.disable_col()