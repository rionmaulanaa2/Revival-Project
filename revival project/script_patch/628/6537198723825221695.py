# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComDataBase.py
from __future__ import absolute_import
import cython
from ..UnitCom import UnitCom
from ..system import ComSystemMgr
import math3d

class ComDataBase(UnitCom):

    def get_share_data_name(self):
        return ''

    def __init__(self, auto_add_to_system=True):
        super(ComDataBase, self).__init__()
        self._in_system = False
        self._add_to_system_when_init = auto_add_to_system
        self._share_data_name = self.get_share_data_name()

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataBase, self).init_from_dict(unit_obj, bdict)
        if self._share_data_name:
            setattr(self.unit_obj.sd, self._share_data_name, self)
        if self._add_to_system_when_init:
            self._add_to_system()

    def cache(self):
        self._remove_from_system()
        if self._share_data_name:
            setattr(self.unit_obj.sd, self._share_data_name, None)
        self._do_cache()
        super(ComDataBase, self).cache()
        return

    def destroy(self):
        if not self._is_valid:
            return
        else:
            self._remove_from_system()
            if self._share_data_name and getattr(self.unit_obj.sd, self._share_data_name):
                setattr(self.unit_obj.sd, self._share_data_name, None)
            self._do_destroy()
            super(ComDataBase, self).destroy()
            return

    def activate_ecs(self):
        if not self._in_system:
            self._add_to_system()

    def deactivate_ecs(self):
        if self._in_system:
            self._remove_from_system()

    def _add_to_system(self):
        ComSystemMgr.g_com_sysmgr.add_data(self)
        self._in_system = True

    def _remove_from_system(self):
        if self._in_system:
            ComSystemMgr.g_com_sysmgr.remove_data(self)
            self._in_system = False

    def _do_cache(self):
        pass

    def _do_destroy(self):
        pass