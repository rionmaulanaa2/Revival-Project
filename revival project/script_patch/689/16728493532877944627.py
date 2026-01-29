# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_pet/ComPetAnimMgr.py
import six
import math
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.character_anim_const import *
import logic.gcommon.common_utils.bcast_utils as bcast
from mobile.common.EntityManager import EntityManager
CHECK_ANIM_VALID = True
DEFAULT_ANIM_NAME = 'idle'
NODES = {1: [
     'single'],
   4: [
     '4.action_f', '4.action_b', '4.action_l', '4.action_r'],
   6: [
     '6.action_f', '6.action_b', '6.action_fl', '6.action_fr', '6.action_bl', '6.action_br']
   }
DIR_SUFIX = {1: [
     ''],
   2: [
     '_f', '_b'],
   4: [
     '_l', '_r', '_f', '_b'],
   6: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b'],
   7: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', ''],
   8: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', '_l', '_r'],
   9: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', '_l', '_r', '']
   }
BLEND_NODE = {4: 'blend_4',
   6: 'blend_6'
   }
SINGLE_NODE = 'single'
SCALE_NODE = ['single', 'blend_4', 'blend_6']
ENTRY_NODE = 'Entry'
MAX_TWIST_YAW = 180
BLEND_MODE_PARAM = 'blend_type'

class ComPetAnimMgr(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_MIRROR_ANIMATOR_LOADED': 'on_load_mirror_animator_complete',
       'E_ENABLE_ANIM': 'install_anim_event',
       'E_POST_ACTION': 'post_anim_to_animator',
       'E_ENABLE_ANIM_LOG': 'enable_log'
       }

    def __init__(self):
        super(ComPetAnimMgr, self).__init__()
        self._animator = None
        self._mirror_animator = None
        self._model = None
        self._action_list = []
        self._last_action = None
        self.sd.ref_anim = None
        self.sd.ref_anim_rate = 1.0
        self.anim_name_set = set()
        self.sd.ref_anim_param = {}
        self._enable_log = False
        self._twist_yaw_enable = False
        self._twist_yaw_register = False
        self._twist_pitch_enable = False
        self._twist_pitch_register = False
        self._twist_root_yaw_enable = False
        self._twist_root_yaw_register = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPetAnimMgr, self).init_from_dict(unit_obj, bdict)
        self.owner_logic = bdict.get('owner_logic', None)
        if not self.owner_logic:
            owner_id = bdict.get('owner_id', None)
            owner = EntityManager.getentity(owner_id)
            if owner:
                self.owner_logic = owner.logic
        return

    def on_init_complete(self):
        pass

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        model = self.ev_g_model()
        if model:
            self.anim_name_set = set(model.get_anim_names())
        self._animator = animator
        self._model = model
        self.on_change_anim_move_dir(0, 0)
        not self.sd.ref_is_refreshing_whole_model and self.install_anim_event()
        self.post_anim_to_animator(DEFAULT_ANIM_NAME, 1, loop=True)
        self.send_event('E_ANIM_MGR_INIT')

    def on_load_mirror_animator_complete(self, mirror_animator):
        self._mirror_animator = mirror_animator

    def install_anim_event(self, regist=True):
        animator = self.ev_g_animator()
        if not animator:
            return
        event_list = [('G_EIGHT_DIR', self.calculate_eight_dir),
         (
          'E_ANIM_RATE', self.on_change_anim_rate),
         (
          'E_ANIM_PHASE', self.on_change_anim_phase),
         (
          'G_ANIM_PHASE', self.get_anim_phase),
         (
          'E_DISABLE_ANIM', lambda *args: self.install_anim_event(False)),
         (
          'E_USE_CACHE_POS', self.use_cache_pos),
         (
          'E_PAUSE_ANIM', self.pause),
         (
          'E_RESUME_ANIM', self.resume),
         (
          'E_CHANGE_ANIM_MOVE_DIR', self.on_change_anim_move_dir)]
        reg_func = self.regist_event if regist else self.unregist_event
        for event_func in event_list:
            reg_func(*event_func)

    def destroy(self):
        super(ComPetAnimMgr, self).destroy()
        self.install_anim_event(False)
        self._animator = None
        self._mirror_animator = None
        self._model = None
        return

    def pause(self):
        if not self._animator:
            return
        self._animator.pause()
        if self._mirror_animator:
            self._mirror_animator.pause()

    def resume(self):
        if not self._animator:
            return
        self._animator.resume()
        if self._mirror_animator:
            self._mirror_animator.resume()

    def use_cache_pos(self, dir_type, **kwargs):
        anim_nodes = NODES
        if dir_type not in anim_nodes:
            log_error('Invalid dir_type {0} !!!!!!!!!'.format(dir_type))
            return

        def handle_node--- This code section failed: ---

 164       0  LOAD_FAST             0  'node'
           3  POP_JUMP_IF_TRUE     10  'to 10'

 165       6  LOAD_CONST            0  ''
           9  RETURN_END_IF    
        10_0  COME_FROM                '3'

 166      10  LOAD_DEREF            0  'kwargs'
          13  LOAD_ATTR             0  'get'
          16  LOAD_CONST            1  'cache_pos_blend_time'
          19  LOAD_CONST            2  0.2
          22  CALL_FUNCTION_2       2 
          25  STORE_FAST            1  'cache_pos_blend_time'

 167      28  LOAD_FAST             0  'node'
          31  LOAD_ATTR             1  'SetMaxBlendOutTime'
          34  LOAD_FAST             1  'cache_pos_blend_time'
          37  CALL_FUNCTION_1       1 
          40  POP_TOP          

 168      41  LOAD_GLOBAL           2  'getattr'
          44  LOAD_GLOBAL           3  'None'
          47  LOAD_CONST            0  ''
          50  CALL_FUNCTION_3       3 
          53  POP_JUMP_IF_FALSE    69  'to 69'

 169      56  LOAD_FAST             0  'node'
          59  LOAD_ATTR             4  'UseCachedPosInterpolate'
          62  CALL_FUNCTION_0       0 
          65  POP_TOP          
          66  JUMP_FORWARD          0  'to 69'
        69_0  COME_FROM                '66'
          69  LOAD_CONST            0  ''
          72  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 50

        if dir_type in BLEND_NODE:
            node_name = BLEND_NODE[dir_type]
            handle_node(self._animator.find(node_name))
            if self._mirror_animator:
                handle_node(self._mirror_animator.find(node_name))

    def enable_log(self, enable):
        self._enable_log = enable

    def post_anim_to_animator(self, anim_name, dir_type, **kwargs):
        is_my_pet = self.ev_g_is_my_pet()
        if is_my_pet:
            if kwargs.get('from_sync', False):
                return
            kwargs['from_sync'] = True
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_POST_ACTION, (anim_name, dir_type), dict(kwargs)))
        if not self._animator:
            if not self._last_action:
                self._last_action = []
            else:
                not_add_on_have_server_action = kwargs.get('not_add_on_have_server_action', False)
                if not_add_on_have_server_action:
                    return
            args = [
             anim_name, dir_type]
            action = [args, kwargs]
            self._last_action.append(action)
            return
        else:
            if not anim_name:
                return
            anim_nodes = NODES
            self.sd.ref_anim = anim_name
            self.sd.ref_anim_dir = dir_type
            anim_nodes = anim_nodes[dir_type]
            keep_phase = kwargs.get('keep_phase', False)
            if dir_type in BLEND_NODE:
                node_name = BLEND_NODE[dir_type]
                if not node_name:
                    log_error('Invalid dir_type {0} for pet animator!!!!!!!!!'.format(dir_type))
                use_cache_pos = kwargs.get('use_cache_pos', False)
                if use_cache_pos:
                    self.use_cache_pos(dir_type, **kwargs)
                if not keep_phase:
                    node = self._animator.find(node_name)
                    if node:
                        phase = kwargs.get('phase', 0) or 0
                        node.phase = phase
                    if self._mirror_animator:
                        node = self._mirror_animator.find(node_name)
                        if node:
                            phase = kwargs.get('phase', 0) or 0
                            node.phase = phase
            time_scale = 1.0
            if 'timeScale' in kwargs:
                time_scale = kwargs.pop('timeScale')
                self.on_change_anim_rate(time_scale)
            ignore_sufix = kwargs.get('ignore_sufix', False)
            blend_time = kwargs.get('blend_time', 0.2)
            force_upate_anim = kwargs.get('force_upate_anim', True)
            yaw_list = kwargs.get('yaw_list', [])

            def handle_node(node_name, mirror):
                if mirror:
                    animator = self._mirror_animator if 1 else self._animator
                    return animator or None
                else:
                    node = animator.find(node_name)
                    if not node:
                        return
                    yaw = 0
                    if yaw_list:
                        yaw = yaw_list[idx]
                    node.SetMaxBlendOutTime(blend_time)
                    dir_anim_name = anim_name
                    if not ignore_sufix:
                        dir_anim_name = anim_name + DIR_SUFIX[dir_type][idx]
                    dir_anim_name = self.check_anim_name(dir_anim_name)
                    animator.replace_clip_name(node_name, dir_anim_name, keep_phase, force=force_upate_anim)
                    node.loop = False
                    node.yaw = yaw
                    for k, v in six.iteritems(kwargs):
                        if v is None:
                            continue
                        if hasattr(node, k):
                            setattr(node, k, v)

                    return

            for idx, node_name in enumerate(anim_nodes):
                handle_node(node_name, False)
                handle_node(node_name, True)

            self._animator.SetInt(BLEND_MODE_PARAM, dir_type)
            if self._mirror_animator:
                self._mirror_animator.SetInt(BLEND_MODE_PARAM, dir_type)
            if is_my_pet and 'yaw_offset' in kwargs:
                enter_intrp_duration = kwargs.get('enter_yaw_offset_intrp_duration', 0.2)
                leave_intrp_duration = kwargs.get('leave_yaw_offset_intrp_duration', enter_intrp_duration)
                anim_duration = self._model.get_anim_length(self.sd.ref_anim) / 1000.0 / time_scale
                self.send_event('E_SET_PET_YAW_OFFSET', kwargs['yaw_offset'], enter_intrp_duration, leave_intrp_duration, anim_duration)
            else:
                self.send_event('E_SET_PET_YAW_OFFSET', None)
            return

    def on_change_anim_move_dir(self, dir_x, dir_y):
        if not self._animator:
            return
        if abs(dir_x) <= 0.01:
            dir_x = 0
        elif dir_x >= 0.99:
            dir_x = 1
        elif dir_x <= -0.99:
            dir_x = -1
        if abs(dir_y) <= 0.01:
            dir_y = 0
        elif dir_y >= 0.99:
            dir_y = 1
        elif dir_y <= -0.99:
            dir_y = -1
        if self.sd.ref_tmp_forbid_anim_dir:
            dir_x = 0
            dir_y = 0
        self._animator.SetFloat('dir_x', dir_x)
        self._animator.SetFloat('dir_y', dir_y)
        if self._mirror_animator:
            self._mirror_animator.SetFloat('dir_x', dir_x)
            self._mirror_animator.SetFloat('dir_y', dir_y)
        self.sd.ref_anim_param['dir_x'] = dir_x
        self.sd.ref_anim_param['dir_y'] = dir_y

    def calculate_eight_dir(self, dir_x, dir_y):
        radian = math.atan2(dir_y, dir_x)
        angle = math.degrees(radian)
        if angle == 0:
            if dir_x == 0.0:
                return 0
        if angle < 0:
            angle += 360.0
        tolerant_angle = 22.5
        convert_angle = angle + tolerant_angle
        if convert_angle >= 360.0:
            convert_angle -= 360.0
        section_index = math.ceil(convert_angle / tolerant_angle)
        move_dir = math.ceil(section_index / 2)
        return move_dir

    def on_change_anim_rate(self, anim_rate, **kwargs):
        self.send_event('E_ACTION_SYNC_ANIM_RATE', anim_rate)
        self.sd.ref_anim_rate = anim_rate
        if self._animator:
            for node_name in SCALE_NODE:
                node = self._animator.find(node_name)
                if node:
                    node.timeScale = anim_rate

        if self._mirror_animator:
            for node_name in SCALE_NODE:
                node = self._mirror_animator.find(node_name)
                if node:
                    node.timeScale = anim_rate

    def get_anim_rate(self):
        return self.sd.ref_anim_rate

    def get_anim_phase(self):
        dir_value = self._animator.GetInt(BLEND_MODE_PARAM)
        if not dir_value:
            log_error('test--get_anim_phase--step2--error--dir_value =', dir_value)
            return
        else:
            node_name = ''
            if dir_value > 1:
                node_name = BLEND_NODE.get(dir_value, None)
                if not node_name:
                    log_error('test--get_anim_phase--step3--error--dir_value =', dir_value, '--have not node')
                    return 0
            else:
                node_name = SINGLE_NODE
            node = self._animator.find(node_name)
            if node:
                return node.phase
            return 0

    def on_change_anim_phase(self, phase):
        if not self._animator:
            return

        def handle_node(index, node):
            if not node:
                return
            node.phase = phase
            if index:
                all_child_states = node.GetChildStates()
                for index, one_child_state in enumerate(all_child_states):
                    one_child_node = one_child_state.childNode
                    one_child_node.phase = phase

        for index, node_name in enumerate(SCALE_NODE):
            handle_node(index, self._animator.find(node_name))
            if self._mirror_animator:
                handle_node(index, self._mirror_animator.find(node_name))

    def check_anim_name(self, name):
        if not CHECK_ANIM_VALID or name in self.anim_name_set:
            return name
        else:
            log_error('[Resource error] Animation Name (' + name + ') not in model resource')
            return DEFAULT_ANIM_NAME