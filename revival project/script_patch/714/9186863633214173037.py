# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillHeat8037.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from common.cfg import confmgr

class SkillHeat8037(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillHeat8037, self).__init__(skill_id, unit_obj, data)

    def do_skill(self, *args):
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        ext_info = skill_conf.get('ext_info', {})
        building_id = ext_info['building_id']
        target_pos, rotation = args
        pos, rot = self.get_building_pos(target_pos, rotation)
        forward = self._unit_obj.ev_g_forward()
        ext_param = {'rot': rot
           }
        if forward:
            ext_param['forward'] = (
             forward.x, 0, forward.z)
        return (
         building_id, pos, ext_param)

    def get_building_pos(self, target_pos, rotation):
        return (
         (
          target_pos.x, target_pos.y, target_pos.z), (rotation.x, rotation.y, rotation.z, rotation.w))