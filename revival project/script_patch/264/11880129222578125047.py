# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/IUnitCom.py
from __future__ import absolute_import
import cython

class IUnitCom(object):

    def __init__(self):
        self.is_active = False

    def init_from_dict(self, unit_obj, bdict):
        pass

    def destroy(self):
        pass

    def get_client_dict(self):
        return {}

    def get_settle_dict(self):
        return {}

    def reset(self):
        pass

    @property
    def logger(self):
        return None

    @property
    def scene(self):
        return global_data.game_mgr.scene

    def update_from_dict(self, unit_obj, bdict):
        pass

    def on_init_complete(self):
        pass

    def on_post_init_complete(self, bdict):
        pass

    def init_event(self):
        pass

    def is_valid(self):
        return False

    def is_enable(self, use_idx=None):
        return False

    def tick(self, delta):
        pass

    def destroy_event(self):
        pass

    def rebind_event(self):
        pass

    def destroy_from_unit(self):
        pass

    def on_destroy(self):
        raise Exception('PLEASE USE destroy() INSTEAD !!!!!!!!!!!!!!!!!!')

    def _unbind_event_interface(self):
        pass