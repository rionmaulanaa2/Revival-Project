# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComSpringAnim.py
from __future__ import absolute_import
import six
import math
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_const import character_anim_const
from logic.gutils import dress_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon import time_utility as tutil
ENABLE_SPRING_ANIM = True
OBSERVE_TARGET_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet', 'LMecha'))

class ComSpringAnim(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_INIT_SPRING_ANI': 'on_init_spring_ani',
       'E_LOAD_APPEND_SOFT': 'on_load_append_soft',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states'
       }

    def __init__(self):
        super(ComSpringAnim, self).__init__()
        self.part_models_wind_param = {}
        self.spring_anim_enable = False
        self._wind_blowing = False
        self.wind_dir = math3d.vector(0, 0, 1)
        self.wind_info_update_ts = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpringAnim, self).init_from_dict(unit_obj, bdict)
        self.model = None
        self.base_conf_file = None
        self.cur_conf_file = None
        self.soft_bone_param = {}
        self.switch_states = None
        self.switch_conf_name = None
        if self.unit_obj.MASK & OBSERVE_TARGET_TAG_VALUE:
            self.model = self.ev_g_model()
            if not self.model:
                return
            self.reset_spring_conf(True)
        global_data.emgr.scene_wind_info_update += self.on_wind_info_updated
        return

    def destroy(self):
        if self.part_models_wind_param:
            self.enable_spring_anim(False)
            self.clear_spring_anim()
            self.part_models_wind_param = None
        self.model = None
        global_data.emgr.scene_wind_info_update -= self.on_wind_info_updated
        super(ComSpringAnim, self).destroy()
        return

    def update_spring_anim(self, new_bone_param):
        if not self.model or not self.model.valid:
            return
        self.soft_bone_param = new_bone_param
        self.clear_spring_anim()
        self.init_spring_anim()

    def enable_spring_anim(self, enable):
        if not self.model or not self.model.valid:
            return
        if enable:
            if not self.is_active:
                return

            def enable():
                if not self.model or not self.model.valid:
                    return
                for part_model in six.iterkeys(self.part_models_wind_param):
                    if part_model and part_model.valid:
                        part_model.get_spring_anim(True).enable_physx()

                self.model.get_spring_anim(True).set_max_offset_constrain('biped', 9)
                self.spring_anim_enable = True
                self.update_com_need_updated()

            global_data.game_mgr.delay_exec(0.5, enable)
        else:
            for part_model in six.iterkeys(self.part_models_wind_param):
                if part_model and part_model.valid:
                    part_model.get_spring_anim(True).disable_physx()

            self.spring_anim_enable = False
            self.update_com_need_updated()

    def on_model_loaded(self, model):
        if not ENABLE_SPRING_ANIM:
            return
        self.clear_spring_anim()
        self.model = model
        self.reset_spring_conf(False)

    def reset_spring_conf(self, init_spring=False):
        if not self.model or not self.model.valid:
            return
        self.base_conf_file = dress_utils.get_file_name(self.model)
        self.cur_conf_file = self.base_conf_file
        data = confmgr.get(self.cur_conf_file)
        self.soft_bone_param = data._conf
        state_conf = self.soft_bone_param.get('state_conf')
        if state_conf:
            self.switch_states = state_conf.get('states')
            self.switch_conf_name = state_conf.get('conf_name')
        if init_spring:
            self.on_init_spring_ani()

    def on_init_spring_ani(self):
        self.clear_spring_anim()
        self.init_spring_anim()

    def enter_states(self, new_state):
        if self.switch_states and new_state in self.switch_states and self.cur_conf_file and self.cur_conf_file != self.switch_conf_name:
            self.cur_conf_file = self.switch_conf_name
            data = confmgr.get(self.cur_conf_file)
            self.soft_bone_param = data._conf
            self.on_init_spring_ani()

    def leave_states(self, leave_state, new_state=None):
        if self.switch_states and self.cur_conf_file and self.cur_conf_file != self.base_conf_file:
            for state in self.switch_states:
                if self.ev_g_get_state(state):
                    return

            self.reset_spring_conf(True)

    def get_soft_bone_data(self):
        return self.soft_bone_param

    def set_active(self, active):
        self.is_active = active
        self.enable_spring_anim(active)

    def clear_spring_anim(self):
        if not self.part_models_wind_param:
            return
        for part_model in six.iterkeys(self.part_models_wind_param):
            if part_model and part_model.valid:
                part_model.get_spring_anim(True).clear_spring_anim()

        self.spring_anim_enable = False
        self.update_com_need_updated()

    def init_spring_anim(self):
        if not self.soft_bone_param:
            return
        if not self.sd.ref_finish_load_lod_model:
            return
        part_models_wind_param = dress_utils.init_spring_anim(self.model, self.soft_bone_param)
        if part_models_wind_param:
            self.model.get_spring_anim(True).set_max_offset_constrain('biped', 9)
        self.part_models_wind_param = part_models_wind_param
        self.spring_anim_enable = True
        self.update_com_need_updated()

    def on_load_append_soft(self):
        pass

    def on_wind_info_updated(self, wind_blowing, wind_dir=None):
        if not self.part_models_wind_param:
            return
        self._wind_blowing = wind_blowing
        if wind_dir:
            self.wind_dir = math3d.vector(math.cos(wind_dir), 0, -math.sin(wind_dir))
        self.wind_info_update_ts = tutil.time()
        self.update_com_need_updated()

    def update_com_need_updated(self):
        self.need_update = self.spring_anim_enable and self.wind_blowing

    def tick(self, delta):
        if not self.wind_dir:
            return
        elapsed_time = tutil.time() - self.wind_info_update_ts
        wind_end_finish = True
        for part_model, wind_param in six.iteritems(self.part_models_wind_param):
            if not part_model or not part_model.valid:
                continue
            anim = part_model.get_spring_anim(True)
            if not anim:
                continue
            for root_bone in wind_param:
                if not self.wind_blowing and elapsed_time >= root_bone['child_count'] * root_bone['child_delay']:
                    continue
                wind_end_finish = False
                for idx in range(root_bone['child_count']):
                    if self.wind_blowing:
                        if elapsed_time < idx * root_bone['child_delay']:
                            continue
                        wave_val = -math.cos((elapsed_time - idx * root_bone['child_delay']) * root_bone['wave_rate']) * 0.5 + 0.5
                        wave_val = root_bone['wave_range'] * wave_val + (1 - root_bone['wave_range'])
                        anim.apply_force(root_bone['root_name'], self.wind_dir * root_bone['strength'] * wave_val, idx)
                    else:
                        if elapsed_time > idx * root_bone['child_delay']:
                            continue
                        wave_val = -math.cos((elapsed_time - idx * root_bone['child_delay']) * root_bone['wave_rate']) * 0.5 + 0.5
                        anim.apply_force(root_bone['root_name'], self.wind_dir * root_bone['strength'] * wave_val, idx)

        if not self.wind_blowing and wind_end_finish:
            self.need_update = False

    def enable_static_wind(self, enable):
        self.static_wind = enable
        if enable and not self._wind_blowing:
            self.wind_info_update_ts = tutil.time()
        self.update_com_need_updated()

    @property
    def wind_blowing--- This code section failed: ---

 230       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'False'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    19  'to 19'

 231      15  LOAD_GLOBAL           2  'True'
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

 232      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             3  '_wind_blowing'
          25  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9