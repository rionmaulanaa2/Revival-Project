# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/unit_tag_utils.py
from __future__ import absolute_import
from mobile.common.mobilecommon import singleton

@singleton
class UnitTagMgr(object):

    def __init__(self):
        self.unit_name_to_mask_map = {}
        self.unit_names_to_tag_value_map = {}

    def refresh_unit_name_to_mask_map(self, unit_name_to_mask_map):
        self.unit_name_to_mask_map = unit_name_to_mask_map

    def register_unit_tag(self, unit_names):
        if not unit_names:
            return 0
        if isinstance(unit_names, str):
            unit_names = (
             unit_names,)
        unit_name_tuple = tuple(sorted(unit_names))
        if unit_name_tuple in self.unit_names_to_tag_value_map:
            return self.unit_names_to_tag_value_map[unit_name_tuple]
        tag_value = 0
        unit_name_to_mask_map = self.unit_name_to_mask_map
        for unit_name in unit_name_tuple:
            if unit_name in unit_name_to_mask_map:
                tag_value |= unit_name_to_mask_map[unit_name]

        self.unit_names_to_tag_value_map[unit_name_tuple] = tag_value
        return tag_value


@singleton
class PreregisteredTags(object):
    pass


unit_tag_mgr = UnitTagMgr()
preregistered_tags = PreregisteredTags()