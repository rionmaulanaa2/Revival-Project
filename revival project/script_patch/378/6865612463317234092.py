# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/Skill8037SinkClient.py
from __future__ import absolute_import
from .SkillCommon import SkillCommon

class Skill8037SinkClient(SkillCommon):

    def __init__(self, skill_id, unit_obj, data):
        super(Skill8037SinkClient, self).__init__(skill_id, unit_obj, data)
        self._sink_add_time = data.get('sink_add_time', 0)

    def get_add_sink_duration(self):
        return self._sink_add_time