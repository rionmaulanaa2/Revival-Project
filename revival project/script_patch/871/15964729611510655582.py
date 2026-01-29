# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComSpringAnimMirror.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_const import character_anim_const
from logic.gutils.dress_utils import get_file_name, init_spring_anim
from logic.gutils.client_unit_tag_utils import register_unit_tag
ENABLE_SPRING_ANIM = True
OBSERVE_TARGET_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet', 'LMecha'))

class ComSpringAnimMirror(UnitCom):
    BIND_EVENT = {'E_MIRROR_MODEL_LOADED': 'on_model_loaded',
       'E_INIT_MIRROR_SPRING_ANI': 'on_init_spring_ani'
       }

    def __init__(self):
        super(ComSpringAnimMirror, self).__init__()
        self.part_models = []

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpringAnimMirror, self).init_from_dict(unit_obj, bdict)
        self.model = None
        self.soft_bone_param = {}
        if self.unit_obj.MASK & OBSERVE_TARGET_TAG_VALUE:
            self.model = self.ev_g_model()
            if not self.model:
                return
            self.clear_spring_anim()
            data_file = get_file_name(self.model)
            data = confmgr.get(data_file)
            self.soft_bone_param = data._conf
            self.init_spring_anim()
        return

    def destroy(self):
        if self.part_models:
            self.enable_spring_anim(False)
            self.clear_spring_anim()
            self.part_models = None
        self.model = None
        super(ComSpringAnimMirror, self).destroy()
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
                for part_model in self.part_models:
                    if part_model and part_model.valid:
                        part_model.get_spring_anim(True).enable_physx()

                self.model.get_spring_anim(True).set_max_offset_constrain('biped', 9)

            global_data.game_mgr.delay_exec(0.5, enable)
        else:
            for part_model in self.part_models:
                if part_model and part_model.valid:
                    part_model.get_spring_anim(True).disable_physx()

    def on_model_loaded(self, model):
        if not ENABLE_SPRING_ANIM:
            return
        self.clear_spring_anim()
        self.model = model
        data_file = get_file_name(model)
        data = confmgr.get(data_file)
        self.soft_bone_param = data._conf

    def on_init_spring_ani(self):
        self.clear_spring_anim()
        self.init_spring_anim()

    def get_soft_bone_data(self):
        return self.soft_bone_param

    def set_active(self, active):
        self.is_active = active
        self.enable_spring_anim(active)

    def clear_spring_anim(self):
        for part_model in self.part_models:
            if part_model and part_model.valid:
                part_model.get_spring_anim(True).clear_spring_anim()

    def init_spring_anim(self):
        if not self.soft_bone_param:
            return
        part_models = init_spring_anim(self.model, self.soft_bone_param)
        if part_models:
            self.model.get_spring_anim(True).set_max_offset_constrain('biped', 9)
        self.part_models = six_ex.keys(part_models)